"""CLI 根命令的入口行为测试（P1-9）。

锁定三件事：``--version`` 只把 metadata 里的版本号写到 stdout 并以 0 退出；裸调用打印帮助而不是
``Missing command.`` 错误；冻结产物取不到分发 metadata 时版本查询仍不抛异常。用例只经
:class:`typer.testing.CliRunner` 调用根应用，不起子进程，也不碰任何实例目录。
"""

import inspect
import os
from importlib import metadata
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import typer

from typer.testing import CliRunner

from akaribot.cli import __version__, i18n, main
from akaribot.cli.commands.init import init as init_command
from akaribot.testing import func_case, Tester

_MISSING_COMMAND = "Missing command"


class _FrozenMetadata:
    PackageNotFoundError = metadata.PackageNotFoundError

    @staticmethod
    def version(name: str) -> str:
        """复现冻结环境下 importlib.metadata 的失败路径。

        :param name: 分发名。
        :return: 不会返回，固定抛 PackageNotFoundError。
        """
        raise metadata.PackageNotFoundError(name)


class _UnreadableMetadata:
    @staticmethod
    def version(name: str) -> str:
        """复现读取元数据时的 I/O 失败。

        :param name: 分发名。
        :return: 不会返回，固定抛 OSError。
        """
        raise OSError(f"cannot read metadata for {name}")


def _use_cli_locale() -> None:
    # 框架连的是 core 的 akari-bot 命名空间，取 CLI 文案前要接上本包的快照。
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _run(*args: str):
    return CliRunner().invoke(main.app, list(args))


async def _test_version_stdout_only_version():
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
    try:
        return main.version_string() == metadata.version(main.DIST_NAME)

    except Exception:
        return False


async def _test_bare_invocation_prints_help():
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
    try:
        result = _run("new", "--help")
        return result.exit_code == 0 and "Usage:" in result.stdout and "akaribot new" in result.stdout

    except Exception:
        return False


async def _test_bare_invocation_enters_tui_on_terminal():
    # 可交互终端下裸调用直接进界面，不打印帮助。
    calls: list[str] = []
    try:
        with (
            mock.patch.object(main, "_tui_available", return_value=True),
            mock.patch("akaribot.cli.instance.find_instance_root", return_value=Path("/tmp/inst")),
            mock.patch("akaribot.cli.commands.tui.run_interactive", side_effect=lambda **_: calls.append("tui")),
        ):
            result = _run()
        return result.exit_code == 0 and calls == ["tui"] and "Usage:" not in result.stdout
    except Exception:
        return False


async def _test_bare_invocation_guides_init_without_instance():
    # 没有实例时先问一句，复用 init 本体初始化，再进界面。
    calls: list[tuple] = []
    found = {"count": 0}

    def _find(*args, **kwargs):
        found["count"] += 1
        # 第一次找不到实例（触发引导），初始化后能找到。
        return None if found["count"] == 1 else Path("/tmp/inst")

    def _init(path, **kwargs):
        calls.append(("init", str(path), kwargs.get("locale")))

    try:
        with (
            mock.patch.object(main, "_tui_available", return_value=True),
            mock.patch("akaribot.cli.instance.find_instance_root", side_effect=_find),
            mock.patch("akaribot.cli.commands.init.init", side_effect=_init),
            mock.patch("akaribot.cli.commands.tui.run_interactive", side_effect=lambda **_: calls.append(("tui",))),
        ):
            result = CliRunner().invoke(main.app, ["--lang", "en_us"], input="y\n")
        return result.exit_code == 0 and calls == [("init", str(Path.cwd()), "en_us"), ("tui",)]
    except Exception:
        return False


async def _test_bare_invocation_aborts_when_init_declined():
    # 拒绝初始化时不进界面，也不调用 init。
    calls: list[str] = []
    try:
        with (
            mock.patch.object(main, "_tui_available", return_value=True),
            mock.patch("akaribot.cli.instance.find_instance_root", return_value=None),
            mock.patch("akaribot.cli.commands.init.init", side_effect=lambda *a, **k: calls.append("init")),
            mock.patch("akaribot.cli.commands.tui.run_interactive", side_effect=lambda **_: calls.append("tui")),
        ):
            result = CliRunner().invoke(main.app, [], input="n\n")
        return result.exit_code != 0 and calls == []
    except Exception:
        return False


async def _test_init_is_callable_with_defaults():
    # ``_ensure_instance`` 只传路径与语言，故 init 的其余参数必须都有真实默认值。参数一旦改成必填
    # （或默认值变成 typer 的 OptionInfo），裸调用入口会在运行时失败，而 ``akaribot init`` 子命令
    # 仍然正常，这条守卫专门盯住这个差值。
    try:
        signature = inspect.signature(init_command)
        required = [
            name
            for name, parameter in signature.parameters.items()
            if name != "path" and parameter.default is inspect.Parameter.empty
        ]
        option_like = [
            name
            for name, parameter in signature.parameters.items()
            if isinstance(parameter.default, (typer.models.OptionInfo, typer.models.ArgumentInfo))
        ]
        return required == [] and option_like == []
    except Exception:
        return False


async def _test_tui_entry_registers_active_instance():
    # 站在实例目录里进界面时自动补登记：本机清单与自启策略随后才有对象可管。
    from akaribot.cli.commands import tui as tui_cmd
    from akaribot.cli.instances import InstanceRegistry

    with TemporaryDirectory(prefix="akari-entry-") as raw:
        base = Path(raw)
        instance = base / "demo"
        instance.mkdir()
        (instance / "akaribot.toml").write_text('[instance]\nname = "demo"\nlocale = "zh_cn"\n', encoding="utf-8")
        plain = base / "plain"
        plain.mkdir()
        with mock.patch.dict(os.environ, {"AKARIBOT_HOME": str(base / "home"), "AKARI_INSTANCE_DIR": str(instance)}):
            first = tui_cmd.register_active()
            second = tui_cmd.register_active()
            entries = InstanceRegistry().load()
        with mock.patch.dict(os.environ, {"AKARIBOT_HOME": str(base / "home"), "AKARI_INSTANCE_DIR": str(plain)}):
            refused = tui_cmd.register_active()
    return (
        "demo" in first
        and str(instance.resolve()) in first
        and second == ""
        and refused == ""
        and [entry.name for entry in entries] == ["demo"]
        and entries[0].root == instance.resolve()
        and entries[0].locale == "zh_cn"
    )


async def _test_tui_entry_hands_the_note_to_the_ui():
    # 自动登记的结论要交给界面报出来，否则用户看不到注册表被动过。
    from akaribot.cli.commands import tui as tui_cmd

    seen: list[str] = []

    class _Result:
        exit_code = 0

        def summary(self) -> str:
            return "done"

    def _run_tui(**kwargs):
        seen.append(str(kwargs.get("boot_note", "")))
        return _Result()

    with (
        mock.patch("akaribot.cli.tui._compat.is_interactive_terminal", return_value=True),
        mock.patch("akaribot.cli.tui.app.run_tui", side_effect=_run_tui),
        mock.patch.object(tui_cmd, "register_active", return_value="已自动登记 demo"),
    ):
        try:
            tui_cmd.run_interactive()
        except Exception as error:  # typer.Exit 是正常收尾
            code = getattr(error, "exit_code", None)
            if code not in (0, None):
                return False
    return seen == ["已自动登记 demo"]


async def _test_tui_entry_adopts_the_only_child_instance():
    # 站在仓库根这类「装着实例的目录」时，唯一的下级实例就是要管的那个：登记并切换过去。
    from akaribot.cli.commands import tui as tui_cmd
    from akaribot.cli.tui import context

    with TemporaryDirectory(prefix="akari-discover-") as raw:
        base = Path(raw)
        project = base / "project"
        project.mkdir()
        solo = project / "only"
        solo.mkdir()
        (solo / "akaribot.toml").write_text('[instance]\nname = "only"\n', encoding="utf-8")
        home = base / "home"
        previous = context.active_root()
        try:
            with mock.patch.dict(os.environ, {"AKARIBOT_HOME": str(home), "AKARI_INSTANCE_DIR": ""}):
                context.set_active_root(None)
                with mock.patch("akaribot.cli.instance.Path.cwd", return_value=project):
                    single = tui_cmd.register_active()
                    switched = context.active_root()
                # 再放一个实例进去，并换一份空注册表：下级有两个实例时不猜，只报候选。
                second = project / "second"
                second.mkdir()
                (second / "akaribot.toml").write_text("[instance]\n", encoding="utf-8")
                context.set_active_root(None)
                with mock.patch.dict(os.environ, {"AKARIBOT_HOME": str(base / "home2"), "AKARI_INSTANCE_DIR": ""}):
                    with mock.patch("akaribot.cli.instance.Path.cwd", return_value=project):
                        ambiguous = tui_cmd.register_active()
                untouched = context.active_root()
        finally:
            context.set_active_root(previous)
    return (
        "only" in single
        and str(solo) in single
        and switched == solo.resolve()
        and str(solo) in ambiguous
        and str(second) in ambiguous
        and untouched is None
    )


@func_case
async def test_cli_main(tester: Tester):
    """CLI 根命令：版本查询、裸调用帮助、参数顺序与冻结兜底"""
    _use_cli_locale()
    await tester.test(_test_version_stdout_only_version, "--version 只输出版本号并退出 0")
    await tester.test(_test_version_matches_distribution_metadata, "版本号与分发 metadata 一致")
    await tester.test(_test_bare_invocation_prints_help, "裸调用打印帮助且无 Missing command")
    await tester.test(_test_version_and_help_first_wins, "--version 与 --help 同时给出时先出现的先生效")
    await tester.test(_test_version_falls_back_when_metadata_missing, "冻结产物无 metadata 时回退包内常量")
    await tester.test(_test_subcommand_still_dispatches, "子命令派发不受影响")
    await tester.test(_test_bare_invocation_enters_tui_on_terminal, "终端下裸调用进界面")
    await tester.test(_test_bare_invocation_guides_init_without_instance, "无实例时引导初始化")
    await tester.test(_test_bare_invocation_aborts_when_init_declined, "拒绝初始化时不进界面")
    await tester.test(_test_init_is_callable_with_defaults, "init 参数均有默认值可直调")
    await tester.test(_test_tui_entry_registers_active_instance, "进界面时自动登记所在实例")
    await tester.test(_test_tui_entry_hands_the_note_to_the_ui, "自动登记的结论交给界面报出")
    await tester.test(_test_tui_entry_adopts_the_only_child_instance, "唯一的下级实例被发现并切换")

    return tester
