"""``akaribot adapter instance remove``：只删除适配器实例的配置文件。

移除入口一旦让用户以为不可逆数据已被清除，命令的成功返回就是假的。当前实现只删除该实例的配置
文件，场景与用户数据留在库里，故 ``--purge-data`` 不作为可执行选项存在；本文件守住这条契约与
「默认只删配置」的行为。
"""

import io
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from rich.console import Console
from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import adapter as adapter_command
from akaribot.testing import Tester, func_case

CLIENT_NAME = "Telegram"
CONFIG_TEXT = "[bot_telegram]\nenable = true\n"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path):
    (root / "config").mkdir(parents=True)
    (root / "akaribot.toml").write_text("", encoding="utf-8")
    (root / "config" / "bot_telegram.toml").write_text(CONFIG_TEXT, encoding="utf-8")
    return SimpleNamespace(root=root)


def _run_remove(instance, **kwargs) -> str:
    # 命中 core 的取数（registry / schema）全部由替身接管，本命令只走配置文件的读写。
    buffer = io.StringIO()
    console = Console(file=buffer, width=400, force_terminal=False)
    with (
        patch.dict(os.environ, {adapter_command.CONFIG_ENV: ""}),
        patch.object(adapter_command, "open_instance", return_value=instance),
        patch.object(adapter_command, "fetch_adapters", return_value=adapter_command.AdapterRegistry()),
        patch.object(adapter_command, "Console", lambda *args, **options: console),
    ):
        adapter_command.instance_remove(**kwargs)
    return buffer.getvalue()


def _test_remove_deletes_config_and_keeps_data():
    with TemporaryDirectory(prefix="akari-adapter-remove-") as raw:
        root = Path(raw) / "instance"
        instance = _make_instance(root)
        config = root / "config" / "bot_telegram.toml"
        out = _run_remove(instance, platform="telegram", instance_id=None, dry_run=False)
        removed = not config.exists()
    return (
        removed
        and i18n.t("cli.adapter.instance.remove.file_removed", path=config) in out
        and i18n.t("cli.adapter.instance.remove.keep_hint", client_name=CLIENT_NAME) in out
        and i18n.t("cli.adapter.instance.remove.recheck") in out
    )


def _test_dry_run_keeps_config():
    with TemporaryDirectory(prefix="akari-adapter-remove-") as raw:
        root = Path(raw) / "instance"
        instance = _make_instance(root)
        config = root / "config" / "bot_telegram.toml"
        out = _run_remove(instance, platform="telegram", instance_id=None, dry_run=True)
        kept = config.exists()
    return kept and i18n.t("cli.adapter.instance.remove.dry_run") in out


def _test_purge_data_is_not_an_option():
    runner = CliRunner()
    helped = runner.invoke(adapter_command.app, ["instance", "remove", "--help"])
    rejected = runner.invoke(adapter_command.app, ["instance", "remove", "telegram", "--purge-data"])
    # 说明段落由 locales 提供，这里只认选项表：它才是「该旗标是否存在」的判据。
    options_block = helped.stdout.split("Options", 1)[-1]
    return (
        helped.exit_code == 0
        and "--purge-data" not in options_block
        and "--yes" not in options_block
        and rejected.exit_code != 0
        and "No such option" in rejected.output
    )


@func_case
async def test_adapter_instance_remove(tester: Tester):
    """cli.commands.adapter: 实例移除只删配置测试"""
    _use_cli_locale()
    await tester.test(_test_remove_deletes_config_and_keeps_data, "默认只删除配置文件")
    await tester.test(_test_dry_run_keeps_config, "--dry-run 不改动文件")
    await tester.test(_test_purge_data_is_not_an_option, "--purge-data 不再是可执行选项")
    return tester
