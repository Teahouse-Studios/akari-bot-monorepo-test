"""版本守卫：包内有源码改动但 [project].version 未变则失败。

按 `git diff --name-only <base>..<head>` 取改动清单，落在哪个包目录内就算哪个包有改动；
再比对两端 [project].version：有源码改动而版本一字未改即违规，退出码 1
（规格见 generated_docs/monorepo_refactor_tasks.md 的 T6.2）。

包内 tests/ 与缓存目录不进 wheel，其改动不要求升版本；--strict 把包内任何文件都算作改动。
包内的 pyproject.toml 改动算改动：依赖与入口点会原样写进 wheel 元数据。

例外：`base..head` 区间内任一提交的信息含 [skip-version]（用 --skip-marker 可改）时，整次检查
放行并返回 0。基准缺省或无法解析为提交时不比对，只提示并返回 0；工具自身无法运行时返回 2。

成员清单与分发名口径与 tools/lint_versions.py 一致：成员由根 pyproject.toml 的
[tool.uv.workspace].members 展开，分发名与版本读成员自己的 [project].name / [project].version。

用法：
    uv run python tools/check_versions.py --base <sha>            # PR base / push before
    uv run python tools/check_versions.py --base <sha> --strict   # tests/ 改动也要求升版本
    uv run python tools/check_versions.py                         # 无基准：只提示，退出码 0
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from packaging.version import InvalidVersion, Version

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_PYPROJECT = PROJECT_ROOT / "pyproject.toml"

DEFAULT_SKIP_MARKER = "[skip-version]"

# 不进 wheel 的目录：其改动不要求升版本；--strict 时该豁免失效。
# pyproject.toml 不在豁免内：依赖与入口点会写进 wheel 元数据，改动同样要发新版。
NON_SHIPPED_SEGMENTS = {"tests", "__pycache__", ".pytest_cache"}

# 报告里每个包的改动文件显示上限，超出只计数量。
MAX_FILES_SHOWN = 8


class ConfigError(RuntimeError):
    """根 pyproject 或成员 pyproject 不满足检查所需的结构。"""


@dataclass(frozen=True)
class Member:
    """一个 workspace 成员。

    :param name: [project].name 书写形式的分发名。
    :param version: 当前工作树的静态版本；声明为 dynamic 或缺失时为 None。
    :param directory: 包目录的仓库根相对 POSIX 路径，无尾斜杠。
    :param pyproject: 该成员 pyproject.toml 的仓库根相对 POSIX 路径。
    """

    name: str
    version: str | None
    directory: str
    pyproject: str


@dataclass(frozen=True)
class Finding:
    """一个包的守卫结论。

    :param name: 分发名。
    :param base_version: 基准侧的版本；新增包或动态版本时为 None。
    :param head_version: 当前版本；动态版本时为 None。
    :param files: 触发结论的包内改动路径。
    :param conclusion: 结论文本。
    :param is_violation: 是否为违规（决定退出码）。
    """

    name: str
    base_version: str | None
    head_version: str | None
    files: list[str] = field(default_factory=list)
    conclusion: str = ""
    is_violation: bool = False


def load_toml(path: Path) -> dict:
    """读取 TOML 文件。"""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def discover_members() -> list[Member]:
    """按根 pyproject 的 members glob 展开成员，读各成员自己的 [project] 名字与版本。"""
    workspace = load_toml(ROOT_PYPROJECT).get("tool", {}).get("uv", {}).get("workspace", {})
    excluded = {path for pattern in workspace.get("exclude", []) for path in PROJECT_ROOT.glob(pattern)}
    found: dict[str, Member] = {}
    for pattern in workspace.get("members", []):
        for candidate in PROJECT_ROOT.glob(pattern):
            if not candidate.is_dir() or candidate in excluded:
                continue
            pyproject = candidate / "pyproject.toml"
            if not pyproject.is_file():
                continue
            project = load_toml(pyproject).get("project", {})
            name = project.get("name")
            if not name:
                raise ConfigError(f"{pyproject.relative_to(PROJECT_ROOT).as_posix()} 缺少 [project].name")
            directory = candidate.relative_to(PROJECT_ROOT).as_posix()
            if name in found:
                raise ConfigError(f"成员名重复：{name} 同时出现在 {found[name].directory} 与 {directory}")
            raw_version = project.get("version")
            found[name] = Member(
                name=name,
                version=raw_version if isinstance(raw_version, str) else None,
                directory=directory,
                pyproject=pyproject.relative_to(PROJECT_ROOT).as_posix(),
            )
    if not found:
        raise ConfigError(f"{ROOT_PYPROJECT.name} 的 [tool.uv.workspace].members 未展开出任何成员")
    return sorted(found.values(), key=lambda member: member.directory)


def git_text(arguments: list[str]) -> str:
    """运行 git 并返回原始标准输出。

    统一关闭 core.quotePath，含中文的路径不会变成八进制转义。
    """
    command = ["git", "-c", "core.quotePath=false", *arguments]
    result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
    return result.stdout


def resolve_commit(ref: str) -> str | None:
    """把引用解析为提交 SHA；解析不了返回 None。"""
    try:
        lines = [
            line
            for line in git_text(["rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"]).splitlines()
            if line.strip()
        ]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return lines[0].strip() if lines else None


def resolve_base(base: str, head: str) -> str:
    """取 base 与 head 的共同祖先；取不到时退回 base 本身。

    取共同祖先是必要的：PR 事件传入的是基准分支尖端，直接两点比对会把基准分支自身的改动
    算成头部的改动，从而在无关包上报出「有改动未升版本」。基准是头部祖先时结果与两点等价。
    """
    try:
        lines = [line for line in git_text(["merge-base", base, head]).splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return base
    return lines[0].strip() if lines else base


def changed_files(base: str, head: str) -> list[str]:
    """取 `git diff --name-only base..head` 的改动路径，仓库根相对 POSIX 形式。"""
    output = git_text(["diff", "--name-only", "--no-color", f"{base}..{head}"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def skip_commits(base: str, head: str, marker: str) -> list[str]:
    """返回区间内提交信息含标记的提交，格式为「短 SHA 标题」。

    提交信息取全文（%B），标记写在标题或正文里都算；分隔符用不可打印字符，避免正文换行干扰。
    """
    output = git_text(["log", "--format=%h%x1f%s%x1f%B%x1e", f"{base}..{head}"])
    hits: list[str] = []
    for record in output.split("\x1e"):
        fields = record.split("\x1f")
        if len(fields) < 3 or marker not in fields[2]:
            continue
        hits.append(f"{fields[0].strip()} {fields[1].strip()}")
    return hits


def version_at(commit: str, pyproject: str) -> tuple[bool, str | None]:
    """读某提交下成员 pyproject 的 [project].version。

    :param commit: 提交 SHA。
    :param pyproject: 成员 pyproject.toml 的仓库根相对 POSIX 路径。
    :return: 二元组——该文件在提交中是否存在；静态版本字符串（缺失、动态或无法解析为 None）。
    """
    try:
        raw = git_text(["show", f"{commit}:{pyproject}"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None
    try:
        project = tomllib.loads(raw).get("project", {})
    except tomllib.TOMLDecodeError:
        return True, None
    version = project.get("version")
    return True, version if isinstance(version, str) else None


def is_source_change(member: Member, path: str, strict: bool) -> bool:
    """判定包内某个改动路径是否要求升版本。

    :param member: 该路径所属成员。
    :param path: 仓库根相对 POSIX 路径，须位于成员目录内。
    :param strict: 为真时包内任何文件都要求升版本。
    :return: 需要升版本时为真。
    """
    if strict:
        return True
    relative = path[len(member.directory) + 1 :]
    return not NON_SHIPPED_SEGMENTS & set(relative.split("/")[:-1])


def compare_versions(base_version: str | None, head_version: str | None) -> int | None:
    """比较两侧版本；任一侧无法解析时返回 None。"""
    try:
        return (Version(head_version) > Version(base_version)) - (Version(head_version) < Version(base_version))
    except (InvalidVersion, TypeError):
        return None


def inspect_member(member: Member, files: list[str], base: str, strict: bool) -> Finding | None:
    """对一个在区间内有改动的成员给出结论。

    :param member: 成员。
    :param files: 区间内该成员目录下的改动路径。
    :param base: 基准提交 SHA。
    :param strict: 为真时 tests/ 等非发布目录的改动也要求升版本。
    :return: 结论；无需判定（如新增包、动态版本）时返回 None。
    """
    sources = sorted(path for path in files if is_source_change(member, path, strict))
    if not sources:
        return Finding(
            name=member.name,
            base_version=None,
            head_version=member.version,
            files=files,
            conclusion=f"包内 {len(files)} 个改动均在 tests/ 或缓存目录，不要求升版本",
        )

    exists, base_version = version_at(base, member.pyproject)
    if not exists:
        return Finding(
            name=member.name,
            base_version=None,
            head_version=member.version,
            files=sources,
            conclusion="基准中无此包（新增成员），不要求升版本",
        )
    if base_version is None or member.version is None:
        return Finding(
            name=member.name,
            base_version=base_version,
            head_version=member.version,
            files=sources,
            conclusion="存在动态或缺失的 version，无法判定，跳过",
        )

    order = compare_versions(base_version, member.version)
    if base_version == member.version or order == 0:
        return Finding(
            name=member.name,
            base_version=base_version,
            head_version=member.version,
            files=sources,
            conclusion="包内源码改动但 version 未变",
            is_violation=True,
        )
    note = "，且为版本回退" if order is not None and order < 0 else ""
    return Finding(
        name=member.name,
        base_version=base_version,
        head_version=member.version,
        files=sources,
        conclusion=f"版本已变 {base_version} → {member.version}{note}",
    )


def print_finding(finding: Finding) -> None:
    """打印一个包的结论及其改动文件。"""
    level = "违规" if finding.is_violation else "通过"
    if finding.base_version is None:
        versions = f"{finding.head_version or '无版本'}"
    else:
        versions = f"{finding.base_version} → {finding.head_version or '无版本'}"
    print(f"{finding.name} {versions}：{level}，{finding.conclusion}")
    if not finding.files:
        return
    for path in finding.files[:MAX_FILES_SHOWN]:
        print(f"    {path}")
    if len(finding.files) > MAX_FILES_SHOWN:
        print(f"    ……另有 {len(finding.files) - MAX_FILES_SHOWN} 个改动路径")
    if finding.is_violation:
        print("    处理：升 [project].version，或在该区间内某个提交的信息里写 [skip-version]")


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(
        description="版本守卫：包内有源码改动但 version 未变则失败",
        epilog=(
            "包外改动（根配置、tools/、文档）不归任何包，不触发本检查。tests/ 与缓存目录不进 wheel，\n"
            "其改动默认不要求升版本，--strict 可收紧。区间内任一提交信息含跳过标记时整次放行。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base", metavar="REV", help="比较基准；缺省时只提示，退出码 0")
    parser.add_argument("--head", metavar="REV", default="HEAD", help="比较终点，默认 HEAD")
    parser.add_argument(
        "--skip-marker", metavar="TEXT", default=DEFAULT_SKIP_MARKER, help="跳过标记，默认 [skip-version]"
    )
    parser.add_argument("--strict", action="store_true", help="包内任何文件（含 tests/）改动都要求升版本")
    return parser


def main() -> int:
    """入口。返回进程退出码，1 表示有违规，0 表示通过或仅提示。"""
    args = build_parser().parse_args()

    try:
        members = discover_members()
    except (ConfigError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"无法读取 workspace 成员：{error}", file=sys.stderr)
        return 2

    if not args.base:
        print("未提供 --base，无区间可比，版本守卫只提示：跳过检查，退出码 0。")
        return 0

    resolved_head = resolve_commit(args.head)
    resolved_base = resolve_commit(args.base)
    if resolved_base is None or resolved_head is None:
        print(f"基准 {args.base} 或终点 {args.head} 无法解析为提交，版本守卫只提示：跳过检查，退出码 0。")
        return 0
    base = resolve_base(resolved_base, resolved_head)

    try:
        hits = skip_commits(base, resolved_head, args.skip_marker)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"读取提交信息失败：{error}", file=sys.stderr)
        return 2
    if hits:
        print(f"区间 {base}..{resolved_head} 内有提交信息含 {args.skip_marker}，版本守卫放行，退出码 0：")
        for hit in hits:
            print(f"  {hit}")
        return 0

    try:
        paths = changed_files(base, resolved_head)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"git diff 失败：{error}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    touched = 0
    for member in members:
        files = [path for path in paths if path.startswith(member.directory + "/")]
        if not files:
            continue
        touched += 1
        finding = inspect_member(member, files, base, args.strict)
        if finding is not None:
            findings.append(finding)

    violations = [finding for finding in findings if finding.is_violation]
    for finding in findings:
        print_finding(finding)

    stray = [
        path
        for path in paths
        if path.startswith("packages/") and not any(path.startswith(member.directory + "/") for member in members)
    ]
    if stray:
        print(f"区间内有 {len(stray)} 个改动路径不属于任何当前成员（包删除或改名），无需升版本：")
        for path in stray[:MAX_FILES_SHOWN]:
            print(f"    {path}")

    scope = f"区间 {base}..{resolved_head}"
    print(
        f"{scope} 改动涉及 {touched} 个成员：违规 {len(violations)}，"
        f"无需判定 {touched - len(findings)}，通过 {len(findings) - len(violations)}。"
    )
    if violations:
        print(f"版本守卫失败：{len(violations)} 个包有源码改动但 version 未变，退出码 1。")
        return 1
    print("版本守卫通过：区间内不存在「有源码改动但 version 未变」的包，退出码 0。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
