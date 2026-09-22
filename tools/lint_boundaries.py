"""import 分层检查。

对 monorepo 布局（packages[/<group>]/<dist>/akaribot/{core,modules,adapters}）做 AST 静态检查，
规格见 generated_docs/monorepo_refactor_tasks.md 的 T4.6（#n 即该节表格的条号）：

    B1  warn/error  模块包 import 其它模块包的非 .api 内部路径（#2；packages/modules 下的官方包为 error）
    B2  error       模块包 import akaribot.adapters.*（#3，平台能力只能经 SessionInfo / Features 声明式获取）
    B3  error       模块包 import akaribot.core.api.adapters（该面只供适配器使用，T4.7(d)）
    B4  error       akaribot.core.* import akaribot.modules.* 或 akaribot.adapters.*（core 不依赖可能缺席的包）
    B5  error       适配器包 import akaribot.modules.*（适配器不依赖具体模块）
    B6  error       模块包 import 其它模块包，却未在自身 pyproject 的 dependencies 里声明该分发（#1）
    B7  error       包含 akaribot/{,modules/,adapters/}__init__.py（#4，命名空间污染 R2）
    B8  warn        模块包 import 的 akaribot.core 深路径符号未收录进 akaribot.core.api（#5）
    B9  error       适配器 entry point 名含 '-'（#6，会与多实例分隔符冲突，T1B.1）
    B10 error       官方模块包（packages/modules/*）import 其它模块包（#7，官方不建立模块间依赖）

B7 与 B9 不是 import 规则：前者看文件是否存在，后者读 pyproject.toml。命中位置分别是 __init__.py 的
第 1 行与 entry point 名的定义行，--diff 的改动行范围因此也覆盖 pyproject.toml。B1 与 B10 是两条相互
独立的规则（#2 与 #7）：官方包的非 .api 跨模块 import 会同时命中两条，规格要求两条并存。

B8 按被 import 的符号判定，不按模块路径：符号面取 api/__init__.py、api/base.py、api/adapters.py 三处
__all__ 的字面量并集（AST 解析，不导入 core）。走门面的写法（akaribot.core.api[.*]）一律不报，深路径
取到门面已承诺的符号也不报 —— 那只是尚未改成门面写法，属于迁移工作，不是本规则的对象。

规则 1 与 7 并存：B6 是「用了就得声明」，对扫描到的所有模块包生效；B10 是「官方包不许互相依赖」，
只约束 packages/modules/ 下的包。B6 把 akaribot.modules.<x> 按源码目录与 entry point 双重索引映射到
分发名，映射不到的（第三方装进 site-packages）跳过；声明解析支持 `akari-bot-core[s3]` 这类 extra 写法
与 `>=` / `==` / 直接引用等描述符。`from x import *` 不逐个计名，动态 import（importlib / __import__）
不产生 ast.Import 节点，均不检查。

既有违规由 tools/boundary_lint_baseline.txt 豁免，检查只对新增与修改的行生效；基线键为
`<路径>\t<规则>\t<被 import 的路径或名字>`，不含行号。

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
import tomllib
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "tools" / "boundary_lint_baseline.txt"

# 收录范围：packages/ 下的全部分发源码。tests/ 与 tools/ 依赖全部层，不在约束内。
SCAN_DIRS = ("packages",)
EXCLUDED_DIR_NAMES = {"__pycache__", ".venv", ".git"}
# 分发清单：packages/<dist>/ 与 packages/<group>/<dist>/ 两层；容器目录（adapters、modules）无 pyproject。
DIST_PYPROJECT_PATTERNS = ("packages/*/pyproject.toml", "packages/*/*/pyproject.toml")

# 命名空间根标志：源码位于 <dist>/akaribot/<layer>/…，据此定位分层与包路径。
NAMESPACE_ROOT = "akaribot"
# 分层取命名空间根之后的第一段目录名；akaribot.testing 不在受约束的三层内，规则不适用。
LAYER_CORE = "core"
LAYER_MODULES = "modules"
LAYER_ADAPTERS = "adapters"
# 命名空间根与两个共享分层目录出现 __init__.py 会把命名空间包截断，故按「akaribot 之后的目录后缀」禁。
NAMESPACE_FORBIDDEN_INIT = {(), ("modules",), ("adapters",)}
# 官方模块包的判定前缀：T4.6 #2 的 error 升级与 #7 都只看这一层目录。
OFFICIAL_MODULES_PREFIX = ("packages", "modules")

MODULES_ROOT = "akaribot.modules"
ADAPTERS_ROOT = "akaribot.adapters"
CORE_ROOT = "akaribot.core"
CORE_API_ROOT = "akaribot.core.api"
# 模块包对外承诺的路径只有 akaribot.modules.<x>.api，包根与其余子路径都算内部实现。
MODULE_PUBLIC_SEGMENT = "api"
# 适配器专用门面：模块 import 它，多半是在做本应交给适配器的事（T4.7(d)）。
ADAPTERS_FACADE = "akaribot.core.api.adapters"
MODULE_ENTRY_POINT_GROUP = "akaribot.modules"
ADAPTER_ENTRY_POINT_GROUP = "akaribot.adapters"
# B8 的符号面来源：门面本体、实现模块与适配器面。
CORE_API_ALL_SOURCES = ("__init__.py", "base.py", "adapters.py")

LEVEL_ERROR = "error"
LEVEL_WARN = "warn"

RULE_DESCRIPTIONS = {
    "B1": f"模块包 import 其它模块包的非 .{MODULE_PUBLIC_SEGMENT} 内部路径（T4.6 #2）",
    "B2": f"模块包 import {ADAPTERS_ROOT}.*（T4.6 #3）",
    "B3": f"模块包 import {ADAPTERS_FACADE}（T4.7(d)）",
    "B4": f"core import {MODULES_ROOT}.* 或 {ADAPTERS_ROOT}.*（T4.6 背景约束）",
    "B5": f"适配器包 import {MODULES_ROOT}.*（T4.6 背景约束）",
    "B6": "模块包 import 其它模块包，但未在自身 pyproject 的 dependencies 里声明该分发（T4.6 #1）",
    "B7": f"包含 {NAMESPACE_ROOT}/{{,modules/,adapters/}}__init__.py，污染命名空间（T4.6 #4）",
    "B8": f"模块包的 {CORE_ROOT} 深路径 import 取了未收录进 {CORE_API_ROOT} 的符号（T4.6 #5）",
    "B9": "适配器 entry point 名含 '-'，与多实例分隔符冲突（T4.6 #6）",
    "B10": "官方模块包（packages/modules/*）import 了其它模块包（T4.6 #7）",
    "B11": "CLI 包内用 sys.executable 启动实例进程（T6.5：冻结后它指向二进制自身）",
}

# B1 的基础级别为 warn：第三方包跨模块取内部路径可能确有需要。包归属为官方（OFFICIAL_MODULES_PREFIX）
# 时该条升级为 error，级别随命中一起记录在 Violation 上，故本表只存静态基础级别。
RULE_LEVELS = {
    "B1": LEVEL_WARN,
    "B2": LEVEL_ERROR,
    "B3": LEVEL_ERROR,
    "B4": LEVEL_ERROR,
    "B5": LEVEL_ERROR,
    "B6": LEVEL_ERROR,
    "B7": LEVEL_ERROR,
    "B8": LEVEL_WARN,
    "B9": LEVEL_ERROR,
    "B10": LEVEL_ERROR,
    "B11": LEVEL_ERROR,
}


@dataclass(frozen=True)
class Location:
    """文件在分层中的归属。

    :param relative: 仓库根相对 POSIX 路径。路径一律相对仓库根计算，绝对路径中的
        `.worktrees/` 等目录名不参与判断。
    :param layer: 分层名，取 LAYER_CORE / LAYER_MODULES / LAYER_ADAPTERS；不在命名空间内为空串。
    :param owner: akaribot.modules.<x> 或 akaribot.adapters.<x> 的 <x>；不属这两层时为 None。
    :param package: 文件所属的点分包路径，用于解析相对 import。
    :param dist_relative: 文件所属分发的目录（仓库根相对）；不在任何分发内时为 None。
    :param official: 文件所属分发是否官方模块包（packages/modules/<dist>）。
    """

    relative: str
    layer: str
    owner: str | None
    package: str
    dist_relative: str | None = None
    official: bool = False


@dataclass(frozen=True)
class ImportRef:
    """一处 import。

    :param line: 行号，从 1 开始。
    :param target: 折算成绝对的被 import 路径：`from a.b import c` 记 `a.b.c`，`import a.b` 记 `a.b`。
    :param symbol: 被取用的名字：`from a.b import c [as d]` 取 c（别名只是本地改名），
        `import a.b [as d]` 取 d，无别名时取末段 b。
    :param module_form: 是否 `import …` 形式，即 target 本身就是模块路径而非符号路径。
    """

    line: int
    target: str
    symbol: str
    module_form: bool = False


@dataclass(frozen=True, order=True)
class Violation:
    """一处分层违规。

    :param path: 仓库根相对 POSIX 路径。
    :param line: 行号，从 1 开始；B7 固定在文件第 1 行。
    :param rule: 规则编号。
    :param target: 被 import 的绝对点分路径、entry point 名或命名空间路径。
    :param level: 该条的级别；B1 随包归属变化，故由命中携带而非查 RULE_LEVELS。
    :param detail: 追加说明，例如 B8 命中的符号名与深路径来源。
    """

    path: str
    line: int
    rule: str
    target: str
    level: str
    detail: str = ""

    def key(self) -> str:
        """基线文件的稳定键。不含行号，代码移动后仍能命中豁免。"""
        return f"{self.path}\t{self.rule}\t{self.target}"

    def __str__(self) -> str:
        detail = f"\n    {self.detail}" if self.detail else ""
        return f"{self.path}:{self.line}: {self.level} {self.rule} {RULE_DESCRIPTIONS[self.rule]}\n    {self.target}{detail}"


@dataclass(frozen=True)
class Dist:
    """packages/ 下的一个分发（pyproject.toml 所在目录）。

    :param relative: 分发目录，仓库根相对 POSIX 路径。
    :param name: `[project].name`，已按 PEP 503 规范化。
    :param dependencies: `[project].dependencies` 里的分发名，同样规范化。
    :param module_owners: 该分发提供的 akaribot.modules.<x> 的 <x> 集合。
    :param adapter_entry_points: 适配器 entry point 的 (名, pyproject 行号) 列表。
    :param official: 是否位于 packages/modules/ 下，即官方模块包。
    """

    relative: str
    name: str
    dependencies: frozenset[str]
    module_owners: frozenset[str]
    adapter_entry_points: tuple[tuple[str, int], ...]
    official: bool


@dataclass(frozen=True)
class Workspace:
    """一次检查共用的全仓索引。"""

    dists: tuple[Dist, ...]
    owner_to_dists: dict[str, tuple[Dist, ...]]
    core_api_names: frozenset[str]

    def dist_for(self, relative: str) -> Dist | None:
        """取包含该文件的分发；嵌套时取最长匹配的分发目录。"""
        best: Dist | None = None
        for dist in self.dists:
            if relative.startswith(f"{dist.relative}/") and (best is None or len(dist.relative) > len(best.relative)):
                best = dist
        return best


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


def iter_pyproject_files() -> list[Path]:
    """枚举 packages/ 下各分发的 pyproject.toml，按路径排序。"""
    found: set[Path] = set()
    for pattern in DIST_PYPROJECT_PATTERNS:
        found.update(PROJECT_ROOT.glob(pattern))
    return sorted(found)


def normalize_dist_name(name: str) -> str:
    """PEP 503 规范化分发名：转小写，并把 -、_、. 统一为 -。"""
    return re.sub(r"[-_.]+", "-", name).strip().lower()


def dependency_name(raw: str) -> str | None:
    """从一条 PEP 508 依赖声明里取分发名。

    支持 `akari-bot-core[s3]>=0.1.0,<1.0`、`pkg @ git+https://…` 与环境标记等写法。
    """
    head = raw.split(";", 1)[0].strip()
    match = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", head)
    return normalize_dist_name(match.group(1)) if match else None


def find_key_line(text: str, header: str, key: str) -> int:
    """在 TOML 文本里定位某个 section 下某个键的行号，找不到时返回 1。

    tomllib 不提供位置信息，故按文本扫描；entry point 名可能含 '-'，匹配前须转义。
    """
    pattern = re.compile(rf"^\s*(?:\"{re.escape(key)}\"|'{re.escape(key)}'|{re.escape(key)})\s*=")
    inside = False
    fallback = 1
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("["):
            inside = stripped == header
            continue
        if pattern.match(raw):
            if inside:
                return number
            if fallback == 1:
                fallback = number
    return fallback


def load_distributions() -> tuple[Dist, ...]:
    """读取各分发的元数据：名字、依赖、提供的模块段、适配器 entry point。"""
    dists: list[Dist] = []
    for path in iter_pyproject_files():
        relative = path.parent.relative_to(PROJECT_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            data = tomllib.loads(text)
        except (tomllib.TOMLDecodeError, OSError, UnicodeDecodeError) as error:
            print(f"无法解析 pyproject，跳过 {relative}：{error}", file=sys.stderr)
            continue

        project = data.get("project") or {}
        name = normalize_dist_name(str(project.get("name") or path.parent.name))
        dependencies = frozenset(
            filter(None, (dependency_name(str(item)) for item in project.get("dependencies") or []))
        )
        entry_points = project.get("entry-points") or {}
        module_entry_points = entry_points.get(MODULE_ENTRY_POINT_GROUP) or {}
        module_owners = {
            str(value)[len(MODULES_ROOT) + 1 :].split(".")[0]
            for value in module_entry_points.values()
            if str(value).startswith(f"{MODULES_ROOT}.")
        }
        module_dir = source_root(path.parent.name) / LAYER_MODULES
        if module_dir.is_dir():
            module_owners.update(
                child.name for child in module_dir.iterdir() if child.is_dir() and child.name not in EXCLUDED_DIR_NAMES
            )
        adapter_header = f'[project.entry-points."{ADAPTER_ENTRY_POINT_GROUP}"]'
        adapter_points = tuple(
            (str(point), find_key_line(text, adapter_header, str(point)))
            for point in (entry_points.get(ADAPTER_ENTRY_POINT_GROUP) or {})
        )
        dists.append(
            Dist(
                relative=relative,
                name=name,
                dependencies=dependencies,
                module_owners=frozenset(module_owners),
                adapter_entry_points=adapter_points,
                official=tuple(relative.split("/")[:2]) == OFFICIAL_MODULES_PREFIX,
            )
        )
    return tuple(dists)


def extract_all_names(tree: ast.AST) -> set[str]:
    """取模块级 `__all__ = [...]` 中的字符串字面量；`*_base.__all__` 这类星号元素由调用方并入。"""
    names: set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, (ast.List, ast.Tuple)):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        for element in node.value.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                names.add(element.value)
    return names


def source_root(dist_relative: str) -> Path:
    """分发源码根：优先 ``<dist>/akaribot``，退回 ``<dist>/akaribot``。

    源码根从 ``<dist>/akaribot`` 压成 ``<dist>/akaribot`` 后，按固定层级拼接的路径会静默落空
    （B8 的符号面会变空、规则不再生效），故两种布局都认。

    :param dist_relative: 分发目录的仓库根相对路径。
    :return: 源码根目录。
    """
    flat = PROJECT_ROOT / dist_relative / NAMESPACE_ROOT
    return flat if flat.is_dir() else PROJECT_ROOT / dist_relative / "src" / NAMESPACE_ROOT


def load_core_api_names(dists: tuple[Dist, ...]) -> frozenset[str]:
    """取 akaribot.core.api 承诺的符号面，AST 解析 __all__ 字面量，不导入 core。"""
    api_dir = next(
        (candidate for dist in dists if (candidate := source_root(dist.relative) / LAYER_CORE / "api").is_dir()),
        None,
    )
    if api_dir is None:
        print(f"未找到 {CORE_API_ROOT} 目录，B8 的符号面为空，该规则不生效。", file=sys.stderr)
        return frozenset()

    names: set[str] = set()
    for file_name in CORE_API_ALL_SOURCES:
        path = api_dir / file_name
        if not path.is_file():
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError, OSError) as error:
            print(f"无法解析 {path.name} 的 __all__：{error}", file=sys.stderr)
            continue
        names |= extract_all_names(tree)
    if not names:
        print(f"{CORE_API_ROOT} 的 __all__ 为空，B8 不生效。", file=sys.stderr)
    return frozenset(names)


def load_workspace() -> Workspace:
    """一次性建立分发索引、模块段索引与 core 门面符号面。"""
    dists = load_distributions()
    owners: dict[str, list[Dist]] = collections.defaultdict(list)
    for dist in dists:
        for owner in sorted(dist.module_owners):
            owners[owner].append(dist)
    return Workspace(
        dists=dists,
        owner_to_dists={owner: tuple(items) for owner, items in owners.items()},
        core_api_names=load_core_api_names(dists),
    )


def locate(path: Path, workspace: Workspace) -> Location:
    """计算文件的分层归属。

    以路径中的 NAMESPACE_ROOT 段定位源码根：其后第一段是分层名，第二段是模块包或适配器包名。
    package 一律取点分导入路径，供相对 import 折算使用；dist 由 Workspace 的最长前缀匹配给出。
    """
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    dist = workspace.dist_for(relative)
    parts = relative.split("/")
    if NAMESPACE_ROOT not in parts:
        return Location(relative=relative, layer="", owner=None, package="")
    namespace = parts[parts.index(NAMESPACE_ROOT) :]
    layer = namespace[1] if len(namespace) > 2 else ""
    owner = namespace[2] if layer in (LAYER_MODULES, LAYER_ADAPTERS) and len(namespace) > 3 else None
    return Location(
        relative=relative,
        layer=layer,
        owner=owner,
        package=".".join(namespace[:-1]),
        dist_relative=dist.relative if dist else None,
        official=bool(dist and dist.official),
    )


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


def resolve_imports(tree: ast.AST, package: str) -> list[ImportRef]:
    """把文件内的 import 全部归一到绝对点分路径与绑定名。

    `from a.b import c` 记为 `a.b.c`：c 既可能是子模块也可能是属性，两种情形下「触取了
    a.b 内部」的结论一致。`from … import c as d` 的本地别名不改变被取用的名字 c。

    :param tree: 已解析的语法树。
    :param package: 文件所属的点分包路径。
    :return: ImportRef 列表。
    """
    resolved: list[ImportRef] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            resolved.extend(
                ImportRef(node.lineno, alias.name, alias.asname or alias.name.split(".")[-1], True)
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            base = resolve_relative(node, package)
            if not base:
                continue
            resolved.extend(ImportRef(node.lineno, f"{base}.{alias.name}", alias.name) for alias in node.names)
    return resolved


def under(path: str, prefix: str) -> bool:
    """点分路径是否等于 prefix 或位于其下。"""
    return path == prefix or path.startswith(f"{prefix}.")


def module_owner(target: str) -> str | None:
    """取 akaribot.modules.<x> 中的 <x>；不在该前缀下时返回 None。"""
    if not target.startswith(f"{MODULES_ROOT}."):
        return None
    return target[len(MODULES_ROOT) + 1 :].split(".")[0] or None


def b1_level(location: Location) -> str:
    """B1 的级别：官方模块包升级为 error，其它（第三方在自己的仓库里复用本工具）保留 warn。"""
    return LEVEL_ERROR if location.official else LEVEL_WARN


def check_declared_dependency(
    location: Location, line: int, target: str, owner: str, workspace: Workspace
) -> list[Violation]:
    """规则 B6：跨模块 import 须在自身 pyproject 的 dependencies 里声明目标分发。"""
    target_dists = workspace.owner_to_dists.get(owner)
    if not target_dists:
        return []
    declaring = workspace.dist_for(location.relative)
    if declaring is None:
        return []
    names = {dist.name for dist in target_dists}
    if names & declaring.dependencies:
        return []
    detail = f"{declaring.name} 的 dependencies 未声明 {' 或 '.join(sorted(names))}，跨模块 import 必须先声明"
    return [Violation(location.relative, line, "B6", target, LEVEL_ERROR, detail)]


def check_core_symbol(location: Location, ref: ImportRef, workspace: Workspace) -> list[Violation]:
    """规则 B8：深路径 import 的符号是否在 akaribot.core.api 的承诺面内。

    按符号而非模块路径判定：深路径取到门面已承诺的名字只算尚未迁移写法，不报。符号面为空
    （core api 缺失或被改坏）时整条规则不生效，避免把所有深路径 import 都刷成告警。
    """
    if not workspace.core_api_names or ref.symbol == "*" or ref.symbol in workspace.core_api_names:
        return []
    source = ref.target if ref.module_form else ref.target.rsplit(".", 1)[0]
    detail = f"符号「{ref.symbol}」未收录进 {CORE_API_ROOT}（深路径来源 {source}）"
    return [Violation(location.relative, ref.line, "B8", ref.target, LEVEL_WARN, detail)]


def check_module_import(location: Location, ref: ImportRef, workspace: Workspace) -> list[Violation]:
    """规则 B1、B2、B3、B6、B8、B10：模块包侧的 import 限制。"""
    found: list[Violation] = []
    target, line = ref.target, ref.line
    if under(target, ADAPTERS_ROOT):
        found.append(Violation(location.relative, line, "B2", target, LEVEL_ERROR))
    if under(target, ADAPTERS_FACADE):
        found.append(Violation(location.relative, line, "B3", target, LEVEL_ERROR))

    owner = module_owner(target)
    if owner and owner != location.owner:
        tail = target[len(MODULES_ROOT) + 1 :].split(".")
        public = len(tail) > 1 and tail[1] == MODULE_PUBLIC_SEGMENT
        if not public:
            found.append(Violation(location.relative, line, "B1", target, b1_level(location)))
        # B10 与 B1 独立：官方包连对方的 .api 也不许依赖（T4.6 #7）。
        if location.official:
            found.append(Violation(location.relative, line, "B10", target, LEVEL_ERROR))
        found.extend(check_declared_dependency(location, line, target, owner, workspace))

    if target != CORE_ROOT and under(target, CORE_ROOT) and not under(target, CORE_API_ROOT):
        found.extend(check_core_symbol(location, ref, workspace))
    return found


def check_import(location: Location, ref: ImportRef, workspace: Workspace) -> list[Violation]:
    """对单个 import 施加全部规则。"""
    if location.layer == LAYER_MODULES:
        return check_module_import(location, ref, workspace)
    if location.layer == LAYER_CORE and (under(ref.target, MODULES_ROOT) or under(ref.target, ADAPTERS_ROOT)):
        return [Violation(location.relative, ref.line, "B4", ref.target, LEVEL_ERROR)]
    if location.layer == LAYER_ADAPTERS and under(ref.target, MODULES_ROOT):
        return [Violation(location.relative, ref.line, "B5", ref.target, LEVEL_ERROR)]
    return []


# 允许的位置是**冻结感知的 CLI 自调用**（冻结时它是二进制、非冻结时是解释器加 -m 模块名）；
# 反之把它当解释器启动实例进程，冻结后会重新调起 CLI，必须经 system_python()。
SYS_EXECUTABLE_ALLOWED = (
    "akaribot/cli/tui/",  # 各页的 cli_argv 构造
    "akaribot/cli/commands/new.py",  # 脚手架末尾自调用 CLI
    "akaribot/cli/instance.py",  # system_python()：非冻结时它就是可用解释器，冻结时才改搜索
)


def check_cli_sys_executable(location: Location, tree: ast.AST) -> list[Violation]:
    """规则 B11：CLI 包内不得用 sys.executable 启动实例进程。

    Nuitka onefile 冻结后 sys.executable 指向 CLI 二进制自身，用它启动实例进程会重新调起 CLI
    而不是 Python；启动实例一律经 ``Instance.python``（实例 venv 解释器或系统 Python）。

    :param location: 文件位置。
    :param tree: 已解析的语法树。
    :return: 违规列表。
    """
    if not location.relative.startswith("packages/akari-bot-cli/"):
        return []
    if any(prefix in location.relative for prefix in SYS_EXECUTABLE_ALLOWED):
        return []
    found: list[Violation] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute) or node.attr != "executable":
            continue
        value = node.value
        if isinstance(value, ast.Name) and value.id == "sys":
            found.append(
                Violation(
                    path=location.relative,
                    line=node.lineno,
                    rule="B11",
                    target="sys.executable",
                    level=LEVEL_ERROR,
                    detail="请经 Instance.python 解析解释器",
                )
            )
    return found


def check_file(path: Path, workspace: Workspace) -> tuple[list[Violation], bool, int]:
    """检查单个文件。

    :return: 三元组——违规列表；文件是否成功解析；未走门面的 core 深路径 import 处数（观察值，
        不构成规则，供迁移进度参考）。
    """
    location = locate(path, workspace)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=location.relative)
    except (SyntaxError, UnicodeDecodeError, OSError) as error:
        print(f"无法解析，跳过 {location.relative}：{error}", file=sys.stderr)
        return [], False, 0

    found: list[Violation] = check_cli_sys_executable(location, tree)
    deep_core = 0
    for ref in resolve_imports(tree, location.package):
        found.extend(check_import(location, ref, workspace))
        if location.layer == LAYER_MODULES and under(ref.target, CORE_ROOT) and not under(ref.target, CORE_API_ROOT):
            deep_core += 1
    return found, True, deep_core


def check_namespace_pollution(paths: list[Path], workspace: Workspace) -> list[Violation]:
    """规则 B7：akaribot 命名空间根与 modules、adapters 分层目录不得含 __init__.py。

    只认分发源码根下的路径（<dist>/src/akaribot 或平铺布局的 <dist>/akaribot），
    以免把 tests/fixtures 下的同名目录误判成命名空间污染。命中位置固定为第 1 行：
    违规事实是文件存在，而不是某一行的内容。
    """
    found: list[Violation] = []
    for path in paths:
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        if not relative.endswith("/__init__.py"):
            continue
        dist = workspace.dist_for(relative)
        if dist is None:
            continue
        parts = relative[len(dist.relative) + 1 :].split("/")
        if parts[0] == "src":
            parts = parts[1:]
        tail = tuple(parts[1:-1])
        if not parts or parts[0] != NAMESPACE_ROOT or tail not in NAMESPACE_FORBIDDEN_INIT:
            continue
        namespace = ".".join((NAMESPACE_ROOT, *tail))
        detail = f"{namespace} 是命名空间目录，其 __init__.py 会使其它分发的同名目录不可见（R2）"
        found.append(Violation(relative, 1, "B7", namespace, LEVEL_ERROR, detail))
    return found


def check_adapter_entry_points(workspace: Workspace) -> list[Violation]:
    """规则 B9：适配器 entry point 名含 '-'，会与多实例名分隔符冲突（T1B.1）。"""
    found: list[Violation] = []
    for dist in workspace.dists:
        for point, line in dist.adapter_entry_points:
            if "-" not in point:
                continue
            detail = "entry point 名不得含 '-'，否则与多实例分隔符冲突（T1B.1）"
            found.append(Violation(f"{dist.relative}/pyproject.toml", line, "B9", point, LEVEL_ERROR, detail))
    return found


def check_files(files: list[Path], workspace: Workspace) -> tuple[list[Violation], int, int]:
    """检查全部文件。

    :return: 三元组——违规列表；因无法解析而跳过的文件数；core 深路径 import 处数（观察值）。
    """
    violations: list[Violation] = []
    unparsed = 0
    deep_core = 0
    for path in files:
        found, parsed, deep = check_file(path, workspace)
        violations.extend(found)
        unparsed += 0 if parsed else 1
        deep_core += deep
    return violations, unparsed, deep_core


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
    文件，而新写的模块文件正是分层检查最需要覆盖的对象。pyproject.toml 一并纳入，因为
    B9 的违规位置在 entry point 定义行上。

    :param base_ref: 比较基准，如 `HEAD~1` 或提交 SHA。
    :return: (仓库根相对 POSIX 路径, 行号) 集合；git 调用失败时返回 None，调用方回退为
        全量检查。返回空集表示基准之后确实没有任何改动。
    """
    try:
        result = subprocess.run(
            # git 的 pathspec 里不含斜杠的模式按全路径通配：`*.py` 能命中任意深度，
            # 而字面量 `pyproject.toml` 只命中仓库根，故嵌套清单用 `*pyproject.toml`。
            ["git", "diff", "--unified=0", "--no-color", base_ref, "--", "*.py", "*pyproject.toml"],
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
        if not relative.endswith(".py") and Path(relative).name != "pyproject.toml":
            continue
        if EXCLUDED_DIR_NAMES & set(relative.split("/")):
            continue
        try:
            line_count = len((PROJECT_ROOT / relative).read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeDecodeError):
            continue
        # 空文件（新建的 __init__.py 就是这种）也要给出第 1 行，否则 B7 在 --diff 下会漏。
        for line in range(1, max(line_count, 1) + 1):
            scope.add((relative, line))
    return scope


def level_label(rule: str, violations: list[Violation]) -> str:
    """规则的级别标签：取静态级别，或该规则命中里实际出现过的级别（B1 两种都可能）。"""
    levels = sorted({violation.level for violation in violations if violation.rule == rule})
    return "/".join(levels) if levels else RULE_LEVELS[rule]


def generate_baseline(violations: list[Violation]) -> None:
    """把当前全部违规写入基线文件。"""
    keys = sorted({v.key() for v in violations})
    counts = collections.Counter(key.split("\t")[1] for key in keys)
    header = [
        "# import 分层检查（tools/lint_boundaries.py）的基线豁免清单。",
        "# 每行一条，格式：<路径>\\t<规则编号>\\t<被 import 的路径或名字>。不含行号，代码移动后豁免仍然有效。",
        "# 键由 tools/lint_boundaries.py --generate-baseline 生成，随清理逐步缩小。",
        "# 生成时的违规总数："
        + str(len(keys))
        + "（"
        + "，".join(f"{rule} {level_label(rule, violations)} {counts.get(rule, 0)}" for rule in RULE_LEVELS)
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

    workspace = load_workspace()
    files = iter_source_files()
    all_violations, unparsed, deep_core = check_files(files, workspace)
    all_violations.extend(check_namespace_pollution(files, workspace))
    all_violations.extend(check_adapter_entry_points(workspace))
    all_violations.sort()

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
        f"{rule} {level_label(rule, all_violations)} {scope_counts.get(rule, 0)}/{total_counts.get(rule, 0)}"
        for rule in RULE_LEVELS
    )
    errors = [v for v in reported if v.level == LEVEL_ERROR]
    warns = [v for v in reported if v.level == LEVEL_WARN]

    scope_note = f"，范围为 {args.diff} 之后的新增/修改行" if args.diff else ""
    unparsed_note = f"，跳过无法解析的文件 {unparsed} 个" if unparsed else ""
    print(f"规则命中（本次检查/全量）：{detail}。")
    print(
        f"检查文件 {len(files)} 个{scope_note}{unparsed_note}："
        f"error {len(errors)}，warn {len(warns)}，基线豁免 {baselined}。"
    )
    print(f"观察（不属于任何规则）：B8 的口径下模块包仍有 {deep_core} 处 core 深路径 import 未走门面。")
    print("warn 是否使检查失败：否。B1 对第三方包、B8 对门面尚未收录的符号保留 warn，既有命中由基线豁免。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
