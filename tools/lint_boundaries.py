"""import 分层检查。

对 monorepo 布局（packages[/<group>]/<dist>/src/akaribot/{core,modules,adapters}）做 AST
静态检查，规格见 generated_docs/monorepo_refactor_tasks.md 的 T4.6：

    B1  warn   模块包 import 其它模块包的非 .api 内部路径
    B2  error  模块包 import akaribot.adapters.*（平台能力应经 SessionInfo / Features 声明式获取）
    B3  error  模块包 import akaribot.core.api.adapters（该面只供适配器使用）
    B4  error  akaribot.core.* import akaribot.modules.* 或 akaribot.adapters.*（core 不得依赖可能缺席的包）
    B5  error  适配器包 import akaribot.modules.*（适配器不得依赖具体模块）

模块公开面取 akaribot.modules.<x>.api，由拆包后 manifest 的 public_api 承诺兼容性。当前没有模块
提供 api.py，故 B1 的命中都是既有内部调用；wiki 家族拆分时合并为一个包，部分命中会转为包内调用。

动态 import（importlib / __import__）不产生 ast.Import 节点，不检查；依赖声明、entry point
命名、命名空间包污染与跨包版本约束属拆包后事项，见 T4.6 / T4.8。既有违规由
tools/boundary_lint_baseline.txt 豁免，检查只对新增与修改的行生效。

用法：
    uv run python tools/lint_boundaries.py                      # 全量，仅报基线外违规
    uv run python tools/lint_boundaries.py --diff HEAD~1        # 只查该基准之后的新增/修改行
    uv run python tools/lint_boundaries.py --generate-baseline  # 重建基线
    uv run python tools/lint_boundaries.py --show-baseline      # 同时打印基线内违规
"""

from __future__ import annotations

import argparse
import ast
import collections
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "tools" / "boundary_lint_baseline.txt"

# 收录范围：packages/ 下的全部分发源码。tests/ 与 tools/ 依赖全部层，不在约束内。
SCAN_DIRS = ("packages",)
EXCLUDED_DIR_NAMES = {"__pycache__", ".venv", ".git"}

# 命名空间根标志：源码位于 <dist>/src/akaribot/<layer>/…，据此定位分层与包路径。
NAMESPACE_ROOT = "akaribot"
# 分层取命名空间根之后的第一段目录名；akaribot.testing 不在受约束的三层内，规则不适用。
LAYER_CORE = "core"
LAYER_MODULES = "modules"
LAYER_ADAPTERS = "adapters"

MODULES_ROOT = "akaribot.modules"
ADAPTERS_ROOT = "akaribot.adapters"
# 模块包对外承诺的路径只有 akaribot.modules.<x>.api，包根与其余子路径都算内部实现。
MODULE_PUBLIC_SEGMENT = "api"
# 适配器专用门面：模块 import 它，多半是在做本应交给适配器的事（T4.7(d)）。
ADAPTERS_FACADE = "akaribot.core.api.adapters"

LEVEL_ERROR = "error"
LEVEL_WARN = "warn"

RULE_DESCRIPTIONS = {
    "B1": f"模块包 import 其它模块包的非 .{MODULE_PUBLIC_SEGMENT} 内部路径",
    "B2": f"模块包 import {ADAPTERS_ROOT}.*",
    "B3": f"模块包 import {ADAPTERS_FACADE}",
    "B4": f"core import {MODULES_ROOT}.* 或 {ADAPTERS_ROOT}.*",
    "B5": f"适配器包 import {MODULES_ROOT}.*",
}

# B1 不计入退出码：拆包前没有模块承诺 .api 面，跨模块取内部路径是既有的合法用法，且 wiki
# 家族合并为一个包后其中一部分会变成包内调用；T4.6 规划在官方包上把它收紧为 error。
RULE_LEVELS = {
    "B1": LEVEL_WARN,
    "B2": LEVEL_ERROR,
    "B3": LEVEL_ERROR,
    "B4": LEVEL_ERROR,
    "B5": LEVEL_ERROR,
}


@dataclass(frozen=True)
class Location:
    """文件在分层中的归属。

    :param relative: 仓库根相对 POSIX 路径。路径一律相对仓库根计算，绝对路径中的
        `.worktrees/` 等目录名不参与判断。
    :param layer: 分层名，取 LAYER_CORE / LAYER_MODULES / LAYER_ADAPTERS；不在命名空间内为空串。
    :param owner: akaribot.modules.<x> 或 akaribot.adapters.<x> 的 <x>；不属这两层时为 None。
    :param package: 文件所属的点分包路径，用于解析相对 import。
    """

    relative: str
    layer: str
    owner: str | None
    package: str


@dataclass(frozen=True, order=True)
class Violation:
    """一处分层违规。

    :param path: 仓库根相对 POSIX 路径。
    :param line: 行号，从 1 开始。
    :param rule: 规则编号。
    :param target: 被 import 的绝对点分路径。
    """

    path: str
    line: int
    rule: str
    target: str

    def key(self) -> str:
        """基线文件的稳定键。不含行号，代码移动后仍能命中豁免。"""
        return f"{self.path}\t{self.rule}\t{self.target}"

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {RULE_LEVELS[self.rule]} {self.rule} {RULE_DESCRIPTIONS[self.rule]}\n    {self.target}"


def iter_source_files() -> list[Path]:
    """枚举需要检查的 Python 文件，按路径排序。"""
    files: list[Path] = []
    for dir_name in SCAN_DIRS:
        base = PROJECT_ROOT / dir_name
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if EXCLUDED_DIR_NAMES & set(path.relative_to(PROJECT_ROOT).parts):
                continue
            files.append(path)
    return sorted(set(files))


def locate(path: Path) -> Location:
    """计算文件的分层归属。

    以路径中的 NAMESPACE_ROOT 段定位源码根：其后第一段是分层名，第二段是模块包或适配器包名。
    package 一律取点分导入路径，供相对 import 折算使用。
    """
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    parts = relative.split("/")
    if NAMESPACE_ROOT not in parts:
        return Location(relative=relative, layer="", owner=None, package="")
    namespace = parts[parts.index(NAMESPACE_ROOT) :]
    layer = namespace[1] if len(namespace) > 2 else ""
    owner = namespace[2] if layer in (LAYER_MODULES, LAYER_ADAPTERS) and len(namespace) > 3 else None
    return Location(relative=relative, layer=layer, owner=owner, package=".".join(namespace[:-1]))


def resolve_relative(node: ast.ImportFrom, package: str) -> str:
    """把相对 import 的 module 与 level 折算成绝对包路径。

    :param node: ImportFrom 节点。
    :param package: 文件所属的点分包路径。
    :return: 绝对包路径；层级超出包根时返回空串。
    """
    if not node.level:
        return node.module or ""
    segments = package.split(".") if package else []
    keep = len(segments) - node.level + 1
    if keep < 0:
        return ""
    base = segments[:keep]
    if node.module:
        base = [*base, *node.module.split(".")]
    return ".".join(base)


def resolve_imports(tree: ast.AST, package: str) -> list[tuple[int, str]]:
    """把文件内的 import 全部归一到绝对点分路径。

    `from a.b import c` 记为 `a.b.c`：c 既可能是子模块也可能是属性，两种情形下「触取了
    a.b 内部」的结论一致。别名不参与判断，`from .x import modules` 这类以关键字命名的
    导入因此不会被误判。

    :param tree: 已解析的语法树。
    :param package: 文件所属的点分包路径。
    :return: (行号, 绝对点分路径) 列表。
    """
    resolved: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            resolved.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = resolve_relative(node, package)
            if not base:
                continue
            resolved.extend((node.lineno, f"{base}.{alias.name}") for alias in node.names)
    return resolved


def under(path: str, prefix: str) -> bool:
    """点分路径是否等于 prefix 或位于其下。"""
    return path == prefix or path.startswith(f"{prefix}.")


def check_module_import(location: Location, line: int, target: str) -> list[Violation]:
    """规则 B1~B3：模块包侧的 import 限制。"""
    found: list[Violation] = []
    if under(target, ADAPTERS_ROOT):
        found.append(Violation(location.relative, line, "B2", target))
    if under(target, ADAPTERS_FACADE):
        found.append(Violation(location.relative, line, "B3", target))
    if under(target, MODULES_ROOT):
        tail = target[len(MODULES_ROOT) + 1 :].split(".")
        owner = tail[0]
        public = len(tail) > 1 and tail[1] == MODULE_PUBLIC_SEGMENT
        if owner and owner != location.owner and not public:
            found.append(Violation(location.relative, line, "B1", target))
    return found


def check_import(location: Location, line: int, target: str) -> list[Violation]:
    """对单个 import 施加全部规则。"""
    found: list[Violation] = []
    if location.layer == LAYER_MODULES:
        found.extend(check_module_import(location, line, target))
    elif location.layer == LAYER_CORE:
        if under(target, MODULES_ROOT) or under(target, ADAPTERS_ROOT):
            found.append(Violation(location.relative, line, "B4", target))
    elif location.layer == LAYER_ADAPTERS and under(target, MODULES_ROOT):
        found.append(Violation(location.relative, line, "B5", target))
    return found


def check_file(path: Path) -> tuple[list[Violation], bool]:
    """检查单个文件。

    :return: 二元组——违规列表；文件是否成功解析。
    """
    location = locate(path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=location.relative)
    except (SyntaxError, UnicodeDecodeError, OSError) as error:
        print(f"无法解析，跳过 {location.relative}：{error}", file=sys.stderr)
        return [], False

    found: list[Violation] = []
    for line, target in resolve_imports(tree, location.package):
        found.extend(check_import(location, line, target))
    return found, True


def check_files(files: list[Path]) -> tuple[list[Violation], int]:
    """检查全部文件。

    :return: 二元组——违规列表；因无法解析而跳过的文件数。
    """
    violations: list[Violation] = []
    unparsed = 0
    for path in files:
        found, parsed = check_file(path)
        violations.extend(found)
        unparsed += 0 if parsed else 1
    violations.sort()
    return violations, unparsed


def load_baseline() -> set[str]:
    """读取基线豁免键。"""
    if not BASELINE_PATH.is_file():
        return set()
    keys: set[str] = set()
    for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        keys.add(line)
    return keys


def diff_scope(base_ref: str) -> set[tuple[str, int]] | None:
    """取 `git diff <base_ref>` 中新增或修改的行号集合。

    比 tools/lint_comments.py 的同名函数多收录未跟踪的新文件：git diff 不显示未跟踪
    文件，而新写的模块文件正是分层检查最需要覆盖的对象。

    :param base_ref: 比较基准，如 `HEAD~1` 或提交 SHA。
    :return: (仓库根相对 POSIX 路径, 行号) 集合；git 调用失败时返回 None，调用方回退为
        全量检查。返回空集表示基准之后确实没有任何改动。
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--unified=0", "--no-color", base_ref, "--", "*.py"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"git diff {base_ref} 失败，回退为全量检查：{error}", file=sys.stderr)
        return None

    lines: set[tuple[str, int]] = set()
    current: str | None = None
    hunk = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
    for raw in result.stdout.splitlines():
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            current = None if target == "/dev/null" else target[2:] if target.startswith("b/") else target
            continue
        match = hunk.match(raw)
        if match and current:
            start = int(match.group(1))
            count = int(match.group(2) or 1)
            for offset in range(count):
                lines.add((current, start + offset))

    lines.update(untracked_scope())
    return lines


def untracked_scope() -> set[tuple[str, int]]:
    """未跟踪的新文件整文件计入检查范围。"""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "--", *SCAN_DIRS],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"git ls-files 失败，未跟踪文件不在检查范围内：{error}", file=sys.stderr)
        return set()

    scope: set[tuple[str, int]] = set()
    for raw in result.stdout.splitlines():
        relative = raw.strip()
        if not relative.endswith(".py"):
            continue
        if EXCLUDED_DIR_NAMES & set(relative.split("/")):
            continue
        try:
            line_count = len((PROJECT_ROOT / relative).read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeDecodeError):
            continue
        for line in range(1, line_count + 1):
            scope.add((relative, line))
    return scope


def generate_baseline(violations: list[Violation]) -> None:
    """把当前全部违规写入基线文件。"""
    keys = sorted({v.key() for v in violations})
    counts = collections.Counter(key.split("\t")[1] for key in keys)
    header = [
        "# import 分层检查（tools/lint_boundaries.py）的基线豁免清单。",
        "# 每行一条，格式：<路径>\\t<规则编号>\\t<被 import 的点分路径>。不含行号，代码移动后豁免仍然有效。",
        "# 键由 tools/lint_boundaries.py --generate-baseline 生成，随清理逐步缩小。",
        "# 生成时的违规总数："
        + str(len(keys))
        + "（"
        + "，".join(f"{rule} {RULE_LEVELS[rule]} {counts.get(rule, 0)}" for rule in RULE_LEVELS)
        + "）。",
        "",
    ]
    BASELINE_PATH.write_text("\n".join(header + keys) + "\n", encoding="utf-8")
    print(f"基线已写入 {BASELINE_PATH.relative_to(PROJECT_ROOT)}，共 {len(keys)} 条。")


def main() -> int:
    """入口。返回进程退出码，0 表示无基线外的违规。"""
    parser = argparse.ArgumentParser(description="import 分层检查")
    parser.add_argument("--diff", metavar="BASE_REF", help="只检查该基准之后新增或修改的行")
    parser.add_argument("--generate-baseline", action="store_true", help="重建基线豁免文件")
    parser.add_argument("--show-baseline", action="store_true", help="同时打印基线内的违规")
    args = parser.parse_args()

    files = iter_source_files()
    all_violations, unparsed = check_files(files)

    if args.generate_baseline:
        generate_baseline(all_violations)
        return 0

    baseline = load_baseline()
    scope = diff_scope(args.diff) if args.diff else None

    reported: list[Violation] = []
    baselined = 0
    for violation in all_violations:
        if scope is not None and (violation.path, violation.line) not in scope:
            continue
        if violation.key() in baseline:
            baselined += 1
            if args.show_baseline:
                reported.append(violation)
            continue
        reported.append(violation)

    for violation in reported:
        print(violation)

    total_counts = collections.Counter(v.rule for v in all_violations)
    scope_counts = collections.Counter(v.rule for v in reported)
    detail = "，".join(
        f"{rule} {RULE_LEVELS[rule]} {scope_counts.get(rule, 0)}/{total_counts.get(rule, 0)}" for rule in RULE_LEVELS
    )
    errors = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_ERROR]
    warns = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_WARN]

    scope_note = f"，范围为 {args.diff} 之后的新增/修改行" if args.diff else ""
    unparsed_note = f"，跳过无法解析的文件 {unparsed} 个" if unparsed else ""
    print(f"规则命中（本次检查/全量）：{detail}。")
    print(
        f"检查文件 {len(files)} 个{scope_note}{unparsed_note}："
        f"error {len(errors)}，warn {len(warns)}，基线豁免 {baselined}。"
    )
    print("warn 是否使检查失败：否。B1 的公开面（模块 .api）在拆包前尚不存在，跨模块取内部路径属既有用法。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
