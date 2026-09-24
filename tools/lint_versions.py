"""内部版本约束一致性检查。

对 workspace 的每个成员，检查其 [project].dependencies 中指向其它成员的条目：

    V1 error  约束区间不含目标成员的实际版本，并打印建议写法
    V2 error  各包对 akari-bot-core 的约束字符串必须一致
    V3 warn   指向其它成员的约束钉到了具体版本（== 或 ~=）
    V4 warn   条目无法解析或目标成员无静态版本，跳过该条校验

为什么 uv lock 发现不了：workspace 内部的 [tool.uv.sources] 只在开发期生效，
uv.lock 记的是 editable 路径，成员写的版本约束被丢弃，uv lock 与 uv sync 都不报错。

uv build 出的 wheel METADATA 仍原样带着这些约束，用户的解析器会照此拒绝安装；
本检查补的就是这段空档：约束开发期不生效、发布期才生效，PR 阶段无人比对。

成员清单由根 pyproject.toml 的 [tool.uv.workspace].members 推导，不硬编码包名。
第 3 条是关键：core 升大版本时只需一次全局替换加一次 lint 复核，不会有漏网的包。

用法：
    uv run python tools/lint_versions.py                  # 全量检查
    uv run python tools/lint_versions.py --diff HEAD~1    # 只报告该基准之后改动所触发或所在的违规

退出码：error 为 0 时返回 0（warn 不影响），否则 1；工具自身无法运行返回 2。
"""

from __future__ import annotations

import argparse
import collections
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_PYPROJECT = PROJECT_ROOT / "pyproject.toml"

# 第 3 条只约束对 core 的写法；名字用规范化形式比较，大小写与下划线差异不参与判断。
CORE_DISTRIBUTION = "akari-bot-core"
CORE_NAME = canonicalize_name(CORE_DISTRIBUTION)

LEVEL_ERROR = "error"
LEVEL_WARN = "warn"

RULE_DESCRIPTIONS = {
    "V1": "内部依赖约束不含目标成员的实际版本",
    "V2": f"对 {CORE_DISTRIBUTION} 的约束字符串不一致",
    "V3": "内部依赖约束钉到了具体版本",
    "V4": "条目无法解析或目标成员无静态版本，校验跳过",
}
RULE_LEVELS = {
    "V1": LEVEL_ERROR,
    "V2": LEVEL_ERROR,
    "V3": LEVEL_WARN,
    "V4": LEVEL_WARN,
}

# 依赖字符串在 pyproject 里以字面量出现，反查行号用；跨行书写时回退到 dependencies 数组行。
QUOTED_PATTERN = re.compile(r'"([^"]*)"|\'([^\']*)\'')
DEPENDENCIES_ARRAY_PATTERN = re.compile(r"^dependencies\s*=\s*\[")
# 报告用书写形式：SpecifierSet 的 str 会按字典序重排（如 >=0.1.0,<1.0 变成 <1.0,>=0.1.0）。
NAME_EXTRAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\s*(?:\[[^\]]*\])?\s*")


class ConfigError(RuntimeError):
    """根 pyproject 或成员 pyproject 不满足检查所需的结构。"""


@dataclass(frozen=True)
class Member:
    """一个 workspace 成员。

    :param name: 规范化分发名，用于与依赖条目的名字比对。
    :param display: pyproject 里书写的分发名，用于报告。
    :param version: 静态版本；声明为 dynamic 或无法解析时为 None。
    :param path: 该成员 pyproject.toml 的仓库根相对 POSIX 路径。
    """

    name: str
    display: str
    version: Version | None
    path: str


@dataclass(frozen=True)
class Dependency:
    """成员声明的一条依赖。

    :param raw: pyproject 中原始书写形式。
    :param line: 该条目所在行号，从 1 开始。
    :param requirement: 解析结果；非 PEP 508 写法时为 None。
    :param written: 条目中约束部分的书写形式，无约束（含 direct reference）时为空串。
    """

    raw: str
    line: int
    requirement: Requirement | None
    written: str

    def display(self) -> str:
        """报告用约束文本。"""
        return self.written or "无版本约束"


@dataclass(frozen=True, order=True)
class Violation:
    """一处约束违规。

    :param path: 相对仓库根的 POSIX 路径。
    :param line: 行号，从 1 开始。
    :param rule: 规则编号。
    :param detail: 追加在结论之后的证据与建议，可含多行。
    :param scope: 触发该违规的 pyproject 路径集合，供 --diff 过滤；不参与比较与打印。
    """

    path: str
    line: int
    rule: str
    detail: str
    scope: frozenset[str] = field(default=frozenset(), compare=False)

    def __str__(self) -> str:
        head = f"{self.path}:{self.line}: {RULE_LEVELS[self.rule]} {self.rule} {RULE_DESCRIPTIONS[self.rule]}"
        body = "\n".join(f"    {line}" for line in self.detail.splitlines())
        return f"{head}\n{body}"


def load_toml(path: Path) -> dict:
    """读取 TOML 文件。"""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def member_pyprojects() -> list[Path]:
    """按根 pyproject 的 members glob 展开成员清单，排除 exclude。"""
    workspace = load_toml(ROOT_PYPROJECT).get("tool", {}).get("uv", {}).get("workspace", {})
    excluded = {path for pattern in workspace.get("exclude", []) for path in PROJECT_ROOT.glob(pattern)}
    found: set[Path] = set()
    for pattern in workspace.get("members", []):
        for candidate in PROJECT_ROOT.glob(pattern):
            if not candidate.is_dir() or candidate in excluded:
                continue
            pyproject = candidate / "pyproject.toml"
            if pyproject.is_file():
                found.add(pyproject)
    if not found:
        raise ConfigError(f"{ROOT_PYPROJECT.name} 的 [tool.uv.workspace].members 未展开出任何成员")
    return sorted(found)


def discover_members() -> dict[str, Member]:
    """读全部成员的 [project] 名字与版本，返回规范化名到成员的映射。"""
    members: dict[str, Member] = {}
    for pyproject in member_pyprojects():
        project = load_toml(pyproject).get("project", {})
        display = project.get("name")
        if not display:
            raise ConfigError(f"{pyproject.relative_to(PROJECT_ROOT).as_posix()} 缺少 [project].name")
        name = canonicalize_name(display)
        if name in members:
            raise ConfigError(f"成员名重复：{display} 同时出现在 {members[name].path}")
        raw_version = project.get("version")
        try:
            version = Version(raw_version) if isinstance(raw_version, str) else None
        except InvalidVersion:
            version = None
        relative = pyproject.relative_to(PROJECT_ROOT).as_posix()
        members[name] = Member(name=name, display=display, version=version, path=relative)
    return members


def dependency_lines(pyproject: Path) -> tuple[dict[str, int], int]:
    """建立依赖字面量到行号的映射。

    :return: 二元组——字面量到行号的映射（取首次出现）；dependencies 数组行的回退行号。
    """
    mapping: dict[str, int] = {}
    array_line: int | None = None
    for number, raw in enumerate(pyproject.read_text(encoding="utf-8").splitlines(), start=1):
        if array_line is None and DEPENDENCIES_ARRAY_PATTERN.match(raw):
            array_line = number
        for double, single in QUOTED_PATTERN.findall(raw):
            mapping.setdefault(double or single, number)
    return mapping, array_line or 1


def written_specifier(raw: str) -> str:
    """取条目里约束部分的书写形式，环境标记与 direct reference 不算约束。"""
    tail = NAME_EXTRAS_PATTERN.sub("", raw).split(";")[0].strip()
    return tail if tail[:1] in ("=", "<", ">", "!", "~") else ""


def member_dependencies(member: Member) -> list[Dependency]:
    """读成员的 [project].dependencies，逐条解析为 Requirement。

    解析不了或不是 PEP 508 写法的条目保留为 requirement=None，交由 V4 报告。
    optional-dependencies 与 dependency-groups 不在约束内。
    """
    pyproject = PROJECT_ROOT / member.path
    declared = load_toml(pyproject).get("project", {}).get("dependencies", [])
    lines, fallback = dependency_lines(pyproject)
    dependencies: list[Dependency] = []
    for raw in declared:
        line = lines.get(raw, fallback) if isinstance(raw, str) else fallback
        try:
            requirement = Requirement(raw)
        except (InvalidRequirement, TypeError):
            requirement = None
        written = written_specifier(raw) if isinstance(raw, str) else ""
        dependencies.append(Dependency(raw=str(raw), line=line, requirement=requirement, written=written))
    return dependencies


def suggest_constraint(version: Version) -> str:
    """给出与成员实际版本相容的区间写法：下界取实际版本，上界取下一个主版本。"""
    return f">={version},<{version.major + 1}.0"


def pinned_version(specifiers: SpecifierSet) -> str | None:
    """返回钉到具体版本的 specifier，没有则返回 None。

    == 与 === 视为钉版本（`==1.2.*` 通配除外）；~= 只在版本含三段以上时视为钉版本，
    `~=1.2` 等价于 >=1.2,<2.0，属正常区间写法。
    """
    for specifier in sorted(specifiers, key=str):
        if specifier.operator in ("==", "===") and not specifier.version.endswith(".*"):
            return str(specifier)
        if specifier.operator == "~=" and len(specifier.version.split(".")) >= 3:
            return str(specifier)
    return None


def collect_dependencies(
    members: dict[str, Member],
) -> tuple[list[Violation], dict[str, list[tuple[Member, Dependency]]], int]:
    """遍历全部成员，跑 V1/V3/V4，同时收集对 core 的约束写法。

    :return: 三元组——违规列表；core 约束比较键到（来源成员， 条目）列表的映射；内部依赖边总数。
    """
    violations: list[Violation] = []
    core_specs: dict[str, list[tuple[Member, Dependency]]] = collections.defaultdict(list)
    internal_edges = 0
    for member in sorted(members.values(), key=lambda item: item.path):
        for dependency in member_dependencies(member):
            if dependency.requirement is None:
                violations.append(
                    Violation(
                        member.path,
                        dependency.line,
                        "V4",
                        f"无法解析为 PEP 508 依赖：{dependency.raw}",
                        frozenset({member.path}),
                    )
                )
                continue
            target = members.get(canonicalize_name(dependency.requirement.name))
            if target is None:
                continue
            internal_edges += 1

            specifiers = dependency.requirement.specifier
            written = dependency.display()
            if target.version is None:
                violations.append(
                    Violation(
                        member.path,
                        dependency.line,
                        "V4",
                        f"目标成员 {target.display} 未声明静态版本，无法校验：{dependency.raw}",
                        frozenset({member.path, target.path}),
                    )
                )
            elif not specifiers.contains(target.version, prereleases=True):
                violations.append(
                    Violation(
                        member.path,
                        dependency.line,
                        "V1",
                        f"{target.display} 实际版本 {target.version}，约束 {written} 不含该版本；"
                        f"应改为 {suggest_constraint(target.version)}",
                        frozenset({member.path, target.path}),
                    )
                )

            pinned = pinned_version(specifiers)
            if pinned:
                hint = f"，建议改为 {suggest_constraint(target.version)}" if target.version else ""
                violations.append(
                    Violation(
                        member.path,
                        dependency.line,
                        "V3",
                        f"对 {target.display} 的约束 {pinned} 钉到具体版本，该成员一升版即失配{hint}",
                        frozenset({member.path}),
                    )
                )

            if target.name == CORE_NAME:
                core_specs[str(specifiers)].append((member, dependency))
    return violations, core_specs, internal_edges


def check_core_consistency(core_specs: dict[str, list[tuple[Member, Dependency]]]) -> list[Violation]:
    """第 3 条：对 core 的约束字符串必须全仓一致。

    比较取 packaging 归一化后的 specifier 字符串（书写顺序与空白差异不算不一致），
    取出现次数最多的写法为基准（并列时取字符串序最小者），其余写法逐个报 error。
    报告打印各包的实际书写形式，extra 部分不参与比较；基准写法由全体包共同决定，
    故 scope 取全部涉事文件，任一包改动导致基准翻转时都能被 --diff 报出。
    """
    if len(core_specs) < 2:
        return []
    groups = sorted(core_specs.items(), key=lambda item: (-len(item[1]), item[0]))
    reference_edges = sorted(groups[0][1], key=lambda item: item[0].path)
    example_member, example_dependency = reference_edges[0]
    scope = frozenset(member.path for edges in core_specs.values() for member, _ in edges)
    violations: list[Violation] = []
    for _, edges in groups[1:]:
        for member, dependency in edges:
            violations.append(
                Violation(
                    member.path,
                    dependency.line,
                    "V2",
                    f"本包写 {dependency.display()}，其余 {len(reference_edges)} 处写 {example_dependency.display()}"
                    f"（如 {example_member.path}:{example_dependency.line}）；"
                    f"{CORE_DISTRIBUTION} 升版靠一次全局替换，写法须全仓一致",
                    scope,
                )
            )
    return violations


def changed_pyprojects(base_ref: str) -> set[str] | None:
    """取 `git diff <base_ref>` 与未跟踪文件中改动过的 pyproject.toml。

    :param base_ref: 比较基准，如 `HEAD~1` 或提交 SHA。
    :return: 仓库根相对 POSIX 路径集合；git 调用失败时返回 None，调用方回退为全量检查。
    """
    commands = (
        ["git", "diff", "--name-only", "--no-color", base_ref, "--", "*pyproject.toml"],
        ["git", "ls-files", "--others", "--exclude-standard", "--", "*pyproject.toml"],
    )
    names: set[str] = set()
    for command in commands:
        try:
            result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"{' '.join(command[:2])} 失败，回退为全量检查：{error}", file=sys.stderr)
            return None
        names.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return names


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(
        description="内部版本约束一致性检查",
        epilog=(
            "为什么 uv lock 发现不了：workspace 内部的 [tool.uv.sources] 只在开发期生效，"
            "uv.lock 记的是 editable 路径、\n"
            "成员声明的版本约束被丢弃，因此 uv lock / uv sync 对约束漂移一概不报；"
            "而 uv build 出的 wheel METADATA\n"
            "仍原样发布 Requires-Dist，用户的解析器会照此拒绝安装。本检查在 PR 阶段比对"
            "「声明」与「成员实际版本」，\n"
            "正是补这段开发期不生效、发布期才生效的空档。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--diff",
        metavar="BASE_REF",
        help="只报告由该基准之后改动的 pyproject.toml 触发或所在的违规（含 core 版本变化殃及的下游包）",
    )
    return parser


def main() -> int:
    """入口。返回进程退出码，0 表示无 error。"""
    args = build_parser().parse_args()

    try:
        members = discover_members()
    except (ConfigError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"无法读取 workspace 成员：{error}", file=sys.stderr)
        return 2

    violations, core_specs, internal_edges = collect_dependencies(members)
    violations.extend(check_core_consistency(core_specs))
    violations.sort()

    scope = changed_pyprojects(args.diff) if args.diff else None
    reported = [v for v in violations if scope is None or v.scope & scope]

    for violation in reported:
        print(violation)

    core_edges = sum(len(edges) for edges in core_specs.values())
    total_counts = collections.Counter(v.rule for v in violations)
    scope_counts = collections.Counter(v.rule for v in reported)
    detail = "，".join(
        f"{rule} {RULE_LEVELS[rule]} {scope_counts.get(rule, 0)}/{total_counts.get(rule, 0)}" for rule in RULE_LEVELS
    )
    errors = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_ERROR]
    warns = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_WARN]
    specs = "，".join(f"{edges[0][1].display()}×{len(edges)}" for _, edges in sorted(core_specs.items()))

    scope_note = f"，范围为 {args.diff} 之后改动的 pyproject.toml 触发或所在的违规" if args.diff else ""
    print(f"规则命中（本次报告/全量）：{detail}。")
    print(
        f"检查成员 {len(members)} 个，内部依赖边 {internal_edges} 条，其中 {core_edges} 条指向 {CORE_DISTRIBUTION}：{specs}。"
    )
    print(f"检查结果{scope_note}：error {len(errors)}，warn {len(warns)}。")
    print("warn 是否使检查失败：否。钉版本只影响下游跟随升级，不构成发布阻塞。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
