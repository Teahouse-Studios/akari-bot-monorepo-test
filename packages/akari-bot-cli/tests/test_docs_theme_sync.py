"""``akaribot.cli.docs.theme_sync``：主题模板 submodule 同步。"""

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli.docs import theme_sync
from akaribot.cli.docs.model import DocsError
from akaribot.testing import Tester, func_case


class _Git:
    def __init__(self, *, fail_update: bool = False) -> None:
        self.head = "a" * 40
        self.updated = False
        self.fail_update = fail_update
        self.calls: list[tuple[list[str], Path]] = []

    def __call__(self, argv, cwd: Path):
        args = list(argv)
        self.calls.append((args, Path(cwd)))
        if "rev-parse" in args:
            value = self.head if self.updated else "a" * 40
            return subprocess.CompletedProcess(args, 0, f"{value}\n", "")
        if "update" in args:
            if self.fail_update:
                return subprocess.CompletedProcess(args, 2, "", "remote rejected\n")
            self.updated = True
            self.head = "b" * 40
            return subprocess.CompletedProcess(args, 0, "updated\n", "")
        if "sync" in args:
            return subprocess.CompletedProcess(args, 0, "synced\n", "")
        return subprocess.CompletedProcess(args, 0, "", "")


def _repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    (repo / ".gitmodules").write_text(
        '[submodule "vendor/akari-bot-docs-template"]\n'
        "\tpath = vendor/akari-bot-docs-template\n"
        "\turl = https://github.com/Teahouse-Studios/akari-bot-docs-template.git\n",
        encoding="utf-8",
    )
    (repo / "vendor" / "akari-bot-docs-template").mkdir(parents=True)
    return repo


async def _test_sync_updates_and_reports_change():
    with TemporaryDirectory(prefix="akari-theme-sync-") as raw:
        repo = _repo(Path(raw))
        git = _Git()
        lines: list[str] = []
        result = theme_sync.sync_theme_submodule(
            Path(raw),
            explicit_repo=str(repo),
            runner=git,
            log=lines.append,
        )
    subcommands = [args[4] for args, _ in git.calls if len(args) > 4 and args[3] == "submodule"]
    return (
        result.repo == repo.resolve()
        and result.path == (repo / theme_sync.THEME_SUBMODULE).resolve()
        and result.before == "a" * 40
        and result.after == "b" * 40
        and result.changed
        and subcommands == ["sync", "update"]
        and "synced" in result.log
        and "updated" in lines
    )


async def _test_sync_failure_is_reported():
    with TemporaryDirectory(prefix="akari-theme-sync-") as raw:
        repo = _repo(Path(raw))
        try:
            theme_sync.sync_theme_submodule(Path(raw), explicit_repo=str(repo), runner=_Git(fail_update=True))
        except DocsError as exc:
            error = (str(exc), exc.params.get("reason"))
        else:
            error = ("", "")
    return error == ("cli.docs.error.theme_sync_failed", "remote rejected")


async def _test_missing_git_is_reported():
    with TemporaryDirectory(prefix="akari-theme-sync-") as raw:
        repo = _repo(Path(raw))

        def missing(argv, cwd):
            raise FileNotFoundError("git")

        try:
            theme_sync.sync_theme_submodule(Path(raw), explicit_repo=str(repo), runner=missing)
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return error == "cli.docs.error.git_missing"


async def _test_missing_repository_is_reported():
    with TemporaryDirectory(prefix="akari-theme-sync-") as raw:
        with patch.object(theme_sync, "source_repository", return_value=None):
            try:
                theme_sync.sync_theme_submodule(Path(raw))
            except DocsError as exc:
                error = (str(exc), exc.params.get("path"))
            else:
                error = ("", "")
    return error == ("cli.docs.error.theme_repo_missing", str(Path(raw)))


@func_case
async def test_docs_theme_sync(tester: Tester):
    """cli.docs.theme_sync: submodule 同步、提交报告与失败映射"""
    await tester.test(_test_sync_updates_and_reports_change, "同步命令顺序、提交前后与日志")
    await tester.test(_test_sync_failure_is_reported, "同步失败映射为引擎错误")
    await tester.test(_test_missing_git_is_reported, "缺少 git 时报告安装提示")
    await tester.test(_test_missing_repository_is_reported, "缺少 submodule 仓库时报错")
    return tester
