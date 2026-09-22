"""CLI 根命令的入口行为测试（P1-9）。

锁定三件事：``--version`` 只把 metadata 里的版本号写到 stdout 并以 0 退出；裸调用打印帮助而不是
``Missing command.`` 错误；冻结产物取不到分发 metadata 时版本查询仍不抛异常。用例只经
:class:`typer.testing.CliRunner` 调用根应用，不起子进程，也不碰任何实例目录。
"""

from importlib import metadata
from unittest import mock

from typer.testing import CliRunner

from akaribot.cli import __version__, main
from akaribot.testing import func_case, Tester

_MISSING_COMMAND = "Missing command"


class _FrozenMetadata:
    """模拟 Nuitka onefile 冻结产物：``.dist-info`` 未随产物保留，查询一律失败。"""

    PackageNotFoundError = metadata.PackageNotFoundError

    @staticmethod
    def version(name: str) -> str:
        """复现冻结环境下 importlib.metadata 的失败路径。

        :param name: 分发名。
        :return: 不会返回，固定抛 PackageNotFoundError。
        """
        raise metadata.PackageNotFoundError(name)


class _UnreadableMetadata:
    """模拟冻结产物里 metadata 的其它失败形态：文件缺失、路径扫描异常等。"""

    @staticmethod
    def version(name: str) -> str:
        """复现读取元数据时的 I/O 失败。

        :param name: 分发名。
        :return: 不会返回，固定抛 OSError。
        """
        raise OSError(f"cannot read metadata for {name}")


def _run(*args: str):
    """在隔离环境里调用一次根应用。

    :param args: 命令行参数。
    :return: CliRunner 的结果对象。
    """
    return CliRunner().invoke(main.app, list(args))


async def _test_version_stdout_only_version():
    """测试 --version - 只输出版本号并以 0 退出，不带 Missing command"""
    try:
        result = _run("--version")
        return (
            result.exit_code == 0
            and result.stdout.strip() == metadata.version(main.DIST_NAME)
            and _MISSING_COMMAND not in result.output
        )

    except Exception:
        return False


async def _test_version_matches_distribution_metadata():
    """测试版本来源 - version_string() 等于 importlib.metadata.version("akari-bot-cli")"""
    try:
        return main.version_string() == metadata.version(main.DIST_NAME)

    except Exception:
        return False


async def _test_bare_invocation_prints_help():
    """测试裸调用 - 帮助走 stdout，stderr 为空且不出现 Missing command"""
    try:
        result = _run()
        return (
            result.exit_code == main.NO_COMMAND_EXIT_CODE
            and "Usage:" in result.stdout
            and "Commands" in result.stdout
            and result.stderr == ""
            and _MISSING_COMMAND not in result.output
        )

    except Exception:
        return False


async def _test_version_and_help_first_wins():
    """测试 --version 与 --help 同时给出 - 先出现的先生效，两者都以 0 退出"""
    try:
        version_first = _run("--version", "--help")
        help_first = _run("--help", "--version")
        return (
            version_first.exit_code == 0
            and version_first.stdout.strip() == metadata.version(main.DIST_NAME)
            and help_first.exit_code == 0
            and "Usage:" in help_first.stdout
        )

    except Exception:
        return False


async def _test_version_falls_back_when_metadata_missing():
    """测试冻结兜底 - 无分发 metadata 时回退包内常量，版本查询与 --version 都不抛异常"""
    try:
        with mock.patch.object(main, "metadata", _FrozenMetadata):
            missing = main.version_string()
            missing_run = _run("--version")
        with mock.patch.object(main, "metadata", _UnreadableMetadata):
            unreadable = main.version_string()
        return (
            missing == __version__
            and unreadable == __version__
            and missing_run.exit_code == 0
            and missing_run.stdout.strip() == __version__
        )

    except Exception:
        return False


async def _test_subcommand_still_dispatches():
    """测试子命令派发 - 根回调允许无子命令后，带子命令的调用仍交给子应用"""
    try:
        result = _run("new", "--help")
        return result.exit_code == 0 and "Usage:" in result.stdout and "akaribot new" in result.stdout

    except Exception:
        return False


@func_case
async def test_cli_main(tester: Tester):
    """CLI 根命令：版本查询、裸调用帮助、参数顺序与冻结兜底"""
    await tester.test(_test_version_stdout_only_version, "--version 只输出版本号并退出 0")
    await tester.test(_test_version_matches_distribution_metadata, "版本号与分发 metadata 一致")
    await tester.test(_test_bare_invocation_prints_help, "裸调用打印帮助且无 Missing command")
    await tester.test(_test_version_and_help_first_wins, "--version 与 --help 同时给出时先出现的先生效")
    await tester.test(_test_version_falls_back_when_metadata_missing, "冻结产物无 metadata 时回退包内常量")
    await tester.test(_test_subcommand_still_dispatches, "子命令派发不受影响")

    return tester
