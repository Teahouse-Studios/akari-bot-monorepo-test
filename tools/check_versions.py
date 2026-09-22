"""版本守卫：包内有源码改动但 [project].version 未变则失败。

按 `git diff --name-only <base>..<head>` 取改动清单，落在哪个包目录内就算哪个包有改动；
再比对两端 [project].version：有源码改动而版本一字未改即违规，退出码 1
（规格见 generated_docs/monorepo_refactor_tasks.md 的 T6.2）。

包内 tests/ 与缓存目录不进 wheel，其改动不要求升版本；--strict 把包内任何文件都算作改动。
包内的 pyproject.toml 改动算改动：依赖与入口点会原样写进 wheel 元数据。

例外：`base..head` 区间内的提交信息里写了独立的 `Skip-Version` trailer 时按声明范围豁免——
`Skip-Version: true` 豁免全部成员，`Skip-Version: <分发名>[, <分发名>]` 只豁免列出的成员。
正文里顺带提到该 token 不算，必须是行首即 token 的独立整行。基准缺省或无法解析为提交时不比对，
只提示并返回 0；工具自身无法运行时返回 2。

成员清单与分发名口径与 tools/lint_versions.py 一致：成员由根 pyproject.toml 的
[tool.uv.workspace].members 展开，分发名与版本读成员自己的 [project].name / [project].version。

用法：
    uv run python tools/check_versions.py --base <sha>            # PR base / push before
    uv run python tools/check_versions.py --base <sha> --strict   # tests/ 改动也要求升版本
    uv run python tools/check_versions.py                         # 无基准：只提示，退出码 0
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from packaging.version import InvalidVersion, Version

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_PYPROJECT = PROJECT_ROOT / "pyproject.toml"

DEFAULT_SKIP_TRAILER = "Skip-Version"

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
    """取 `git diff --name-only base..head` 的改动路径，仓库根相对 POSIX 形式。

    用 NUL 分隔输出，含空格或换行的路径不会被切断。
    """
    output = git_text(["diff", "--name-only", "-z", "--no-color", f"{base}..{head}"])
    return [path for path in output.split("\0") if path.strip()]


def skip_commits(base: str, head: str, trailer: str) -> list[tuple[str, str, tuple[str, ...]]]:
    """返回区间内声明了跳过 trailer 的提交。

    只认**独立整行**的 trailer（``Token: 值`` 或 ``Token #值``，行首即 token），不认正文里顺带
    提到的字符串：曾经因为一次提交在说明文字里写了两次旧标记，整个区间的版本守卫被静默放行，
    之后一百多个提交的重构等于没有这道闸。取值含义见 :func:`parse_exemption`。

    :param base: 区间起点（含）。
    :param head: 区间终点（含）。
    :param trailer: trailer 的 token，如 ``Skip-Version``。
    :return: 三元组列表——短 SHA、标题、该提交豁免的分发名元组（空元组表示豁免全部）。
    """
    output = git_text(["log", "--format=%h%x1f%s%x1f%B%x1e", f"{base}..{head}"])
    hits: list[tuple[str, str, tuple[str, ...]]] = []
    for record in output.split("\x1e"):
        fields = record.split("\x1f")
        if len(fields) < 3:
            continue
        exemption = parse_exemption(fields[2], trailer)
        if exemption is None:
            continue
        hits.append((fields[0].strip(), fields[1].strip(), exemption))
    return hits


def trailer_block(message: str) -> list[str]:
    """取提交信息的 trailer 段：末尾连续非空行。

    与 git 的 trailer 约定一致（trailer 必须在最后一段），因此正文中间或缩进的代码块里出现
    同样的字样不会被误当声明。整段可能为空——末尾是空行时说明该提交没有 trailer。
    """
    block: list[str] = []
    for line in reversed(message.rstrip().splitlines()):
        if not line.strip():
            break
        block.append(line)
    block.reverse()
    return block


def parse_exemption(message: str, trailer: str) -> tuple[str, ...] | None:
    """从提交信息的 trailer 段里解析跳过声明。

    ``Token: true`` 豁免全部成员；``Token: <分发名>[, <分发名>]`` 只豁免列出的成员。绑定到具体
    分发是必要的：一个标记放行整个区间全部成员时，豁免范围与实际未升版本的包毫无关系。

    只认行首即 token 的独立整行（``Token: 值`` 或 ``Token #值``）：token 前有缩进、或出现在正文
    中间时都不算，否则解释功能的一句话就能关掉整段区间的检查。

    :param message: 提交信息全文。
    :param trailer: trailer 的 token。
    :return: 豁免的分发名元组；空元组表示全部。没有该 trailer 时返回 ``None``。
    :raises ConfigError: 出现了 trailer 但取值无法识别——静默忽略会让豁免失效得毫无提示。
    """
    pattern = re.compile(rf"{re.escape(trailer)}\s*[:#]\s*(.*)$", re.IGNORECASE)
    for line in trailer_block(message):
        match = pattern.match(line.rstrip())
        if match is None:
            continue
        value = match.group(1).strip()
        if value.lower() == "true":
            return ()
        names = tuple(part.strip() for part in value.split(",") if part.strip())
        if not names:
            raise ConfigError(f"提交信息里的 {trailer} 没有取值：应写 true 或逗号分隔的分发名")
        return names
    return None


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
        print("    处理：升 [project].version，或在该提交信息里写独立的 Skip-Version trailer")


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(
        description="版本守卫：包内有源码改动但 version 未变则失败",
        epilog=(
            "包外改动（根配置、tools/、文档）不归任何包，不触发本检查。tests/ 与缓存目录不进 wheel，\n"
            "其改动默认不要求升版本，--strict 可收紧。提交信息里有独立的 Skip-Version trailer 时\n"
            "按声明范围豁免：true 为全部成员，逗号分隔的分发名只豁免列出的成员。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base", metavar="REV", help="比较基准；缺省时只提示，退出码 0")
    parser.add_argument("--head", metavar="REV", default="HEAD", help="比较终点，默认 HEAD")
    parser.add_argument(
        "--skip-trailer",
        metavar="TOKEN",
        default=DEFAULT_SKIP_TRAILER,
        help="跳过用的 trailer token，默认 Skip-Version",
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
        hits = skip_commits(base, resolved_head, args.skip_trailer)
    except ConfigError as error:
        print(f"跳过 trailer 无法解析：{error}", file=sys.stderr)
        return 2
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"读取提交信息失败：{error}", file=sys.stderr)
        return 2

    known = {member.name for member in members}
    exempt: set[str] = set()
    blanket = False
    for sha, subject, names in hits:
        if not names:
            blanket = True
            print(f"  {sha} {subject}：Skip-Version: true，豁免区间内全部成员")
            continue
        unknown = [name for name in names if name not in known]
        if unknown:
            print(f"提交 {sha} 的 {args.skip_trailer} 列了不属于本 workspace 的分发：{unknown}", file=sys.stderr)
            return 2
        exempt.update(names)
        print(f"  {sha} {subject}：豁免 {list(names)}")
    if blanket:
        print(f"区间 {base}..{resolved_head} 内有提交声明豁免全部成员，版本守卫放行，退出码 0。")
        return 0
    if exempt:
        print(f"区间 {base}..{resolved_head} 内声明的豁免分发：{sorted(exempt)}")

    try:
        paths = changed_files(base, resolved_head)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"git diff 失败：{error}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    touched = 0
    skipped = 0
    for member in members:
        files = [path for path in paths if path.startswith(member.directory + "/")]
        if not files:
            continue
        touched += 1
        if member.name in exempt:
            skipped += 1
            continue
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
    exemption_note = f"，按 trailer 豁免 {skipped}" if skipped else ""
    print(
        f"{scope} 改动涉及 {touched} 个成员：违规 {len(violations)}，"
        f"无需判定 {touched - len(findings) - skipped}，通过 {len(findings) - len(violations)}{exemption_note}。"
    )
    if violations:
        print(f"版本守卫失败：{len(violations)} 个包有源码改动但 version 未变，退出码 1。")
        return 1
    print("版本守卫通过：区间内不存在「有源码改动但 version 未变」的包，退出码 0。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
