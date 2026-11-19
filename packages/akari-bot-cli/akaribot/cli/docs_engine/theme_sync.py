"""主题模板 submodule 同步。

同步只更新源码检出的 submodule 工作区，不暂存父仓库 gitlink，也不提交或推送。主题文件内容
参与构建指纹，因此同步后的下一次构建会重新生成站点。
"""

from __future__ import annotations

import configparser
import os
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from .model import DocsError

THEME_SUBMODULE = "vendor/akari-bot-docs-template"
_LOG_TAIL_LIMIT = 2000

Runner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]
LogSink = Callable[[str], None]


@dataclass(frozen=True)
class ThemeSyncResult:
    """一次主题模板同步的结果。

    :param repo: 执行 git 的仓库根。
    :param path: 主题 submodule 目录。
    :param before: 同步前的工作区提交；未初始化时为空串，回退为父仓库记录的提交。
    :param after: 同步后的工作区提交。
    :param changed: 提交是否变化或是否为首次初始化。
    :param log: git 输出。
    """

    repo: Path
    path: Path
    before: str
    after: str
    changed: bool
    log: str = ""


def source_repository() -> Path | None:
    """返回包含本 CLI 源码的仓库根；安装形态没有源码仓库时返回 ``None``。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / "packages" / "akari-bot-cli" / "pyproject.toml").is_file():
            return parent
    return None


def theme_repository(instance_root: Path, explicit: str | None = None) -> Path:
    """定位声明主题 submodule 的仓库。

    :param instance_root: 实例根，作为源码检出不可用时的回退。
    :param explicit: 显式仓库路径。
    :return: 仓库根。
    :raises DocsError: 找不到声明该 submodule 的仓库。
    """
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not _declares_theme(root):
            raise DocsError("cli.docs.error.theme_repo_missing", path=str(root))
        return root
    for root in (source_repository(), Path(instance_root).expanduser().resolve()):
        if root is not None and _declares_theme(root):
            return root
    raise DocsError("cli.docs.error.theme_repo_missing", path=str(instance_root))


def sync_theme_submodule(
    instance_root: Path,
    explicit_repo: str | None = None,
    runner: Runner | None = None,
    log: LogSink | None = None,
) -> ThemeSyncResult:
    """同步主题模板 submodule 到远端最新提交。

    :param instance_root: 实例根。
    :param explicit_repo: 显式仓库路径；缺省从 CLI 源码检出或实例根定位。
    :param runner: git 执行器，测试可注入。
    :param log: git 输出行回调。
    :return: 同步结果。
    :raises DocsError: 仓库缺失、git 不可用或同步失败。
    """
    repo = theme_repository(instance_root, explicit_repo)
    path = repo / THEME_SUBMODULE
    lines: list[str] = []

    def emit(line: str) -> None:
        lines.append(line)
        if log is not None:
            log(line)

    def execute(argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        proc = _execute(argv, repo, runner)
        for line in (proc.stdout or "").splitlines():
            if line.strip():
                emit(line)
        return proc

    try:
        before = _working_head(path, runner) or _recorded_head(repo, runner)
        for argv in (
            ["git", "-C", str(repo), "submodule", "sync", "--", THEME_SUBMODULE],
            ["git", "-C", str(repo), "submodule", "update", "--init", "--remote", "--", THEME_SUBMODULE],
        ):
            proc = execute(argv)
            if proc.returncode != 0:
                raise DocsError(
                    "cli.docs.error.theme_sync_failed",
                    reason=_tail(proc.stderr or proc.stdout or "\n".join(lines)),
                    path=str(repo),
                )
    except FileNotFoundError as exc:
        raise DocsError("cli.docs.error.git_missing") from exc
    except OSError as exc:
        raise DocsError("cli.docs.error.theme_sync_failed", reason=str(exc), path=str(repo)) from exc
    after = _working_head(path, runner) or _recorded_head(repo, runner)
    changed = bool(after) and (not before or before != after)
    return ThemeSyncResult(
        repo=repo,
        path=path,
        before=before,
        after=after,
        changed=changed,
        log="\n".join(lines),
    )


def _declares_theme(root: Path) -> bool:
    path = root / ".gitmodules"
    if not path.is_file():
        return False
    parser = configparser.ConfigParser()
    try:
        parser.read(path, encoding="utf-8")
    except (OSError, configparser.Error):
        return False
    for section in parser.sections():
        if section.startswith("submodule") and parser.get(section, "path", fallback="").strip() == THEME_SUBMODULE:
            return True
    return False


def _working_head(path: Path, runner: Runner | None) -> str:
    if not path.is_dir():
        return ""
    return _git_output(["git", "-C", str(path), "rev-parse", "HEAD"], runner)


def _recorded_head(repo: Path, runner: Runner | None) -> str:
    return _git_output(["git", "-C", str(repo), "rev-parse", f"HEAD:{THEME_SUBMODULE}"], runner)


def _git_output(argv: Sequence[str], runner: Runner | None) -> str:
    proc = _run(argv, Path(argv[2]) if len(argv) > 2 else Path.cwd(), runner)
    return (proc.stdout or "").strip() if proc.returncode == 0 else ""


def _execute(argv: Sequence[str], cwd: Path, runner: Runner | None) -> subprocess.CompletedProcess[str]:
    if runner is not None:
        return runner(argv, cwd)
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_PAGER": "cat"}
    process = subprocess.Popen(  # noqa: S603 - 命令由本模块组装，参数固定
        list(argv),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )
    lines: list[str] = []
    try:
        stream = process.stdout
        if stream is not None:
            for raw in stream:
                lines.append(raw.rstrip())
        returncode = process.wait()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    return subprocess.CompletedProcess(list(argv), returncode, "\n".join(lines), "")


def _run(argv: Sequence[str], cwd: Path, runner: Runner | None) -> subprocess.CompletedProcess[str]:
    if runner is not None:
        return runner(argv, cwd)
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_PAGER": "cat"}
    return subprocess.run(  # noqa: S603 - 命令由本模块组装，参数固定
        list(argv),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
    )


def _tail(text: str) -> str:
    content = (text or "").strip()
    return content[-_LOG_TAIL_LIMIT:] if content else "git command failed"
