"""变更检测与选择性构建矩阵。

按 `git diff --name-only <base>..<head>` 的改动清单映射到 workspace 成员，输出 CI 的构建矩阵。
规格见 generated_docs/monorepo_refactor_tasks.md 的 T6.1：

    包内文件改动                          → 该分发名进入矩阵
    core 包（akari-bot-core）改动         → 矩阵取全部成员（full，core 是公共面）
    根 pyproject.toml、uv.lock、tools/**  → 同上（全局变更）
    其余无法归属到任何包的路径            → 同上（宁可多构建，不可漏构建）
    仅文档类路径                          → 不进矩阵（如 *.md、generated_docs/**、LICENSE）

成员清单与分发名口径与 tools/lint_versions.py 一致：成员由根 pyproject.toml 的
[tool.uv.workspace].members 展开，分发名读成员自己的 [project].name，不按目录名推断。
`--json` 输出的 packages 在 full 为真时同样是全部成员，CI 的 matrix 消费方式无需分支。

`--base` 缺省或无法解析时输出全部成员并置 full=true，对应 workflow_dispatch 一类手动触发。
PR 与 push 事件传入的基准是分支尖端而非共同祖先，故先取 merge-base 再比对：直接两点对比会把
基准分支自身的改动算成头部的改动（反向误报）。基准是头部祖先时 merge-base 即基准，结果与两点等价。

用法：
    uv run python tools/changed_packages.py --base <sha> --json   # PR base / push before
    uv run python tools/changed_packages.py --base <sha>          # 人类可读
    uv run python tools/changed_packages.py --json                # 无基准：全部成员，full=true

退出码：正常 0；workspace 成员无法解析时 2。git 调用失败按全量处理并返回 0。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_PYPROJECT = PROJECT_ROOT / "pyproject.toml"

# core 是公共面：它的改动影响全部包，矩阵随即转为全量。
CORE_DISTRIBUTION = "akari-bot-core"
PACKAGES_ROOT = "packages"

# 全局变更：根配置与锁文件、全仓工具都会改变每个包的构建与测试前提。
GLOBAL_FILES = {"pyproject.toml", "uv.lock"}
GLOBAL_PREFIXES = ("tools/",)

# 文档类路径不进入任何 wheel，也不构成任何包的测试前提，故不触发构建。
DOC_FILES = {"LICENSE", ".gitignore", ".gitattributes", ".editorconfig", ".pre-commit-config.yaml"}
DOC_PREFIXES = ("generated_docs/",)
DOC_SUFFIXES = (".md",)

# 人类可读输出里触发点的显示上限，避免一次大范围改动刷屏。
MAX_REASONS = 20


class ConfigError(RuntimeError):
    """根 pyproject 或成员 pyproject 不满足检查所需的结构。"""


@dataclass(frozen=True)
class Member:
    """一个 workspace 成员。

    :param name: [project].name 书写形式的分发名，即 CI 的构建单元。
    :param directory: 包目录的仓库根相对 POSIX 路径，无尾斜杠。
    """

    name: str
    directory: str


@dataclass(frozen=True)
class Matrix:
    """一次变更检测的结果。

    :param packages: 需要构建的分发名，按包目录排序；full 为真时即全部成员。
    :param full: 是否需要全量构建。
    :param reasons: 触发全量的触发点与原因，供人类可读输出。
    :param member_files: 分发名到包内改动文件数的映射，仅定向构建时有意义。
    :param doc_files: 判定为无构建影响的文档类路径数。
    :param total_files: 改动路径总数。
    :param base: 实际使用的比较基准 SHA；未比对时为 None。
    :param head: 比较终点引用。
    """

    packages: list[str]
    full: bool
    reasons: list[str]
    member_files: dict[str, int] = field(default_factory=dict)
    doc_files: int = 0
    total_files: int = 0
    base: str | None = None
    head: str = "HEAD"


def load_toml(path: Path) -> dict:
    """读取 TOML 文件。"""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def discover_members() -> list[Member]:
    """按根 pyproject 的 members glob 展开成员，分发名取各成员自己的 [project].name。"""
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
            name = load_toml(pyproject).get("project", {}).get("name")
            if not name:
                raise ConfigError(f"{pyproject.relative_to(PROJECT_ROOT).as_posix()} 缺少 [project].name")
            directory = candidate.relative_to(PROJECT_ROOT).as_posix()
            if name in found:
                raise ConfigError(f"成员名重复：{name} 同时出现在 {found[name].directory} 与 {directory}")
            found[name] = Member(name=name, directory=directory)
    if not found:
        raise ConfigError(f"{ROOT_PYPROJECT.name} 的 [tool.uv.workspace].members 未展开出任何成员")
    return sorted(found.values(), key=lambda member: member.directory)


def git_output(arguments: list[str], *, nul: bool = False) -> list[str]:
    """运行 git 并返回输出项；nul 为真时按 NUL 分隔。

    统一关闭 core.quotePath，含中文的路径不会变成八进制转义；NUL 分隔使含空格的路径不被切断。
    """
    command = ["git", "-c", "core.quotePath=false", *arguments]
    result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
    separator = "\0" if nul else "\n"
    return [item for item in result.stdout.split(separator) if item.strip()]


def resolve_commit(ref: str) -> str | None:
    """把引用解析为提交 SHA；解析不了返回 None。"""
    try:
        lines = git_output(["rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return lines[0].strip() if lines else None


def resolve_base(base: str, head: str) -> str:
    """取 base 与 head 的共同祖先；取不到时退回 base 本身。"""
    try:
        lines = git_output(["merge-base", base, head])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return base
    return lines[0].strip() if lines else base


def changed_files(base: str, head: str) -> list[str]:
    """取 `git diff --name-only base..head` 的改动路径，仓库根相对 POSIX 形式。"""
    return git_output(["diff", "--name-only", "-z", "--no-color", f"{base}..{head}"], nul=True)


def package_directory(path: str) -> str | None:
    """从 packages/ 下的路径推断包目录，供已不在 workspace 的包（删除、改名）兜底。"""
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == PACKAGES_ROOT and parts[1].startswith("akari-bot-"):
        return "/".join(parts[:2])
    if len(parts) >= 3 and parts[0] == PACKAGES_ROOT and parts[2].startswith("akari-bot-"):
        return "/".join(parts[:3])
    return None


def classify(path: str, members: list[Member]) -> tuple[str, str]:
    """把一个改动路径归类。

    :param path: 仓库根相对 POSIX 路径。
    :param members: workspace 成员清单。
    :return: 二元组——类别（member/core/global/doc/unknown）与人类可读的原因。
    """
    for member in sorted(members, key=lambda item: len(item.directory), reverse=True):
        if path.startswith(member.directory + "/"):
            if member.name == CORE_DISTRIBUTION:
                return "core", path
            return "member", member.name
    if path in GLOBAL_FILES or path.startswith(GLOBAL_PREFIXES):
        return "global", f"{path}（全局变更）"
    directory = package_directory(path)
    if directory is not None:
        return "unknown", f"{directory}（包已不在当前 workspace 成员内，可能是删除或改名）"
    if path in DOC_FILES or path.endswith(DOC_SUFFIXES) or path.startswith(DOC_PREFIXES):
        return "doc", f"{path}（文档）"
    return "unknown", f"{path}（无法归属到任何包）"


def build_matrix(paths: list[str], members: list[Member], note: str | None, base: str | None, head: str) -> Matrix:
    """把改动路径清单折算成构建矩阵。

    :param paths: 改动路径清单。
    :param members: workspace 成员清单。
    :param note: 未比对的原因（缺省基准、基准无法解析、git 失败）；非空即全量。
    :param base: 实际使用的比较基准 SHA，未比对时为 None。
    :param head: 比较终点引用。
    :return: 构建矩阵。
    """
    all_names = [member.name for member in members]
    member_files: dict[str, int] = {}
    triggers: dict[str, str] = {}
    doc_files = 0
    if note is not None:
        triggers[note] = note
    for path in paths:
        kind, detail = classify(path, members)
        if kind == "member":
            member_files[detail] = member_files.get(detail, 0) + 1
        elif kind == "doc":
            doc_files += 1
        elif kind == "core":
            triggers["core"] = f"{CORE_DISTRIBUTION}（公共面，例如 {detail}）"
        else:
            triggers[detail] = detail
    if triggers:
        return Matrix(
            packages=all_names,
            full=True,
            reasons=sorted(triggers.values()),
            doc_files=doc_files,
            total_files=len(paths),
            base=base,
            head=head,
        )
    packages = [name for name in all_names if name in member_files]
    return Matrix(
        packages=packages,
        full=False,
        reasons=[],
        member_files=member_files,
        doc_files=doc_files,
        total_files=len(paths),
        base=base,
        head=head,
    )


def print_matrix(matrix: Matrix) -> None:
    """人类可读输出。"""
    scope = f"{matrix.base}..{matrix.head}" if matrix.base else "无基准"
    print(f"比较范围：{scope}，改动路径 {matrix.total_files} 个，其中文档类 {matrix.doc_files} 个。")
    if matrix.full:
        print(f"构建矩阵：全量（full=true），共 {len(matrix.packages)} 个包。")
        print("触发全量的路径：")
        for reason in matrix.reasons[:MAX_REASONS]:
            print(f"  {reason}")
        if len(matrix.reasons) > MAX_REASONS:
            print(f"  ……另有 {len(matrix.reasons) - MAX_REASONS} 项")
        print("全量矩阵包含全部成员：")
    else:
        print(f"构建矩阵：定向（full=false），共 {len(matrix.packages)} 个包。")
    for name in matrix.packages:
        count = matrix.member_files.get(name)
        print(f"  {name}" if count is None else f"  {name}（改动 {count} 个路径）")


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(
        description="变更检测与选择性构建矩阵",
        epilog=(
            "core 是公共面，它的改动与根配置、锁文件、tools/ 一样转全量；其余无法归属到任何包的路径\n"
            "同样转全量，宁可多构建不可漏构建。文档类路径不影响任何 wheel 与测试前提，不进矩阵。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base", metavar="REV", help="比较基准；缺省或无法解析时输出全部成员并置 full=true")
    parser.add_argument("--head", metavar="REV", default="HEAD", help="比较终点，默认 HEAD")
    parser.add_argument("--json", action="store_true", help='输出 {"packages": [...], "full": bool}')
    return parser


def main() -> int:
    """入口。返回进程退出码，0 表示检测完成。"""
    args = build_parser().parse_args()

    try:
        members = discover_members()
    except (ConfigError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"无法读取 workspace 成员：{error}", file=sys.stderr)
        return 2

    base: str | None = None
    paths: list[str] = []
    note: str | None = None
    head = resolve_commit(args.head) or args.head
    if not args.base:
        note = "未提供 --base，按全量处理"
    else:
        resolved_base = resolve_commit(args.base)
        resolved_head = resolve_commit(args.head)
        if resolved_base is None or resolved_head is None:
            note = f"基准 {args.base} 或终点 {args.head} 无法解析为提交，按全量处理"
            print(note + "。", file=sys.stderr)
        else:
            base = resolve_base(resolved_base, resolved_head)
            try:
                paths = changed_files(base, resolved_head)
            except (subprocess.CalledProcessError, FileNotFoundError) as error:
                note = "git diff 失败，按全量处理"
                base = None
                print(f"{note}：{error}", file=sys.stderr)

    matrix = build_matrix(paths, members, note, base, head)
    if args.json:
        print(json.dumps({"packages": matrix.packages, "full": matrix.full}, ensure_ascii=False))
    else:
        print_matrix(matrix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
