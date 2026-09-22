"""``module remove --purge-data`` 的配置定位与清理顺序。

旧实现按 ``provides_modules`` 猜 ``config/modules/<名>.toml``，而 ``CFGManager.load()`` 只扫描
``config/*.toml``（扁平路径），那条路径下永远没有文件，于是 ``--purge-data`` 从不删配置；清理还
排在 uv uninstall 之后，那时清单已随分发消失，连该删什么表都解析不出来。此处固定：按
``manifest.config_table`` 定位扁平文件、适配器实例表按前缀覆盖、任一步失败即返回 False。
"""

import contextlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import module as module_command
from akaribot.cli.instance import Instance, PackageInfo
from akaribot.testing import Tester, func_case

MODULE_DIST = "akari-bot-module-wiki"
ADAPTER_DIST = "akari-bot-adapter-telegram"


def _use_cli_locale() -> None:
    """把语言快照切回 CLI 命名空间，否则断言只能拿到键名。"""
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path) -> Instance:
    """建一个只带元数据文件的最小实例，并备好扁平 ``config/``。"""
    (root / "akaribot.toml").write_text("", encoding="utf-8")
    (root / "config").mkdir(parents=True, exist_ok=True)
    return Instance(root)


def _module_package() -> PackageInfo:
    """wiki 模块包：声明表与配置表。"""
    return PackageInfo(
        dist=MODULE_DIST,
        kind="module",
        name="wiki",
        provides_modules=("wiki", "wikilog"),
        owned_tables=("module_wiki_site_info",),
        config_table="module_wiki",
    )


def _adapter_package() -> PackageInfo:
    """telegram 适配器包：基表加两个实例表。"""
    return PackageInfo(
        dist=ADAPTER_DIST,
        kind="adapter",
        name="telegram",
        provides_modules=("telegram",),
        config_table="bot_telegram",
    )


def _test_flat_config_path_is_resolved_by_config_table():
    """基表按 config_table 的扁平路径定位，不再猜 config/modules/<名>.toml。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        flat = instance.config_dir / "module_wiki.toml"
        flat.write_text("", encoding="utf-8")
        legacy = instance.config_dir / "modules"
        legacy.mkdir()
        (legacy / "wiki.toml").write_text("", encoding="utf-8")
        base, instances = module_command._config_files(instance, _module_package())
    return base == [flat] and instances == []


def _test_adapter_instance_tables_are_matched_by_prefix():
    """适配器实例表按 ``<基表>-`` 前缀匹配，其它表不受影响。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        base = instance.config_dir / "bot_telegram.toml"
        alt = instance.config_dir / "bot_telegram-alt.toml"
        other = instance.config_dir / "bot_discord.toml"
        for path in (base, alt, other):
            path.write_text("", encoding="utf-8")
        base_files, instances = module_command._config_files(instance, _adapter_package())
    return base_files == [base] and instances == [alt] and other not in instances


def _test_missing_config_table_deletes_nothing():
    """清单没声明 config_table 时不去猜文件名，返回空。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        (instance.config_dir / "module_dice.toml").write_text("", encoding="utf-8")
        package = PackageInfo(dist="akari-bot-module-dice", kind="module", name="dice", provides_modules=("dice",))
        base, instances = module_command._config_files(instance, package)
    return base == [] and instances == []


def _test_instance_config_is_kept_without_confirmation():
    """未确认删除实例配置时只删基表，实例表原样保留并如实报告。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        base = instance.config_dir / "bot_telegram.toml"
        alt = instance.config_dir / "bot_telegram-alt.toml"
        for path in (base, alt):
            path.write_text("", encoding="utf-8")
        purged: list[str] = []
        original = engine.db_purge
        engine.db_purge = lambda inst, dist: purged.append(dist) or True
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = module_command._purge(
                    instance, [_adapter_package()], yes=True, dry_run=False, purge_instances=False
                )
        finally:
            engine.db_purge = original
        kept_alt = alt.is_file()
        removed_base = not base.is_file()
    return result is True and kept_alt and removed_base


def _test_instance_config_is_removed_when_confirmed():
    """确认后实例表一并删除。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        base = instance.config_dir / "bot_telegram.toml"
        alt = instance.config_dir / "bot_telegram-alt.toml"
        for path in (base, alt):
            path.write_text("", encoding="utf-8")
        original = engine.db_purge
        engine.db_purge = lambda inst, dist: True
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = module_command._purge(
                    instance, [_adapter_package()], yes=True, dry_run=False, purge_instances=True
                )
        finally:
            engine.db_purge = original
        gone = not base.exists() and not alt.exists()
    return result is True and gone


def _test_table_purge_failure_is_reported_and_not_swallowed():
    """表删除失败时返回 False——静默成功会让用户以为数据已清干净。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        flat = instance.config_dir / "module_wiki.toml"
        flat.write_text("", encoding="utf-8")
        original = engine.db_purge
        engine.db_purge = lambda inst, dist: False
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = module_command._purge(
                    instance, [_module_package()], yes=True, dry_run=False, purge_instances=True
                )
        finally:
            engine.db_purge = original
    return result is False


def _test_file_removal_failure_is_reported():
    """配置文件删不掉时同样返回 False，而不是只记一条成功。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        flat = instance.config_dir / "module_wiki.toml"
        flat.write_text("", encoding="utf-8")
        original_unlink = Path.unlink
        original_purge = engine.db_purge

        def failing_unlink(self, *args: Any, **kwargs: Any):
            raise OSError("read-only")

        # 表这一步固定成功：本用例只针对「文件删不掉」，让结果不被真实子进程的成败左右。
        engine.db_purge = lambda inst, dist: True
        Path.unlink = failing_unlink
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = module_command._purge(
                    instance, [_module_package()], yes=True, dry_run=False, purge_instances=True
                )
        finally:
            Path.unlink = original_unlink
            engine.db_purge = original_purge
        survived = flat.is_file()
    return result is False and survived


def _test_dry_run_writes_nothing():
    """dry-run 只打印计划，不删表也不删文件。"""
    with TemporaryDirectory(prefix="akari-cli-purge-") as directory:
        instance = _make_instance(Path(directory))
        flat = instance.config_dir / "module_wiki.toml"
        flat.write_text("", encoding="utf-8")
        original = engine.db_purge
        engine.db_purge = lambda inst, dist: (_ for _ in ()).throw(AssertionError("dry-run 不应删表"))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = module_command._purge(
                    instance, [_module_package()], yes=False, dry_run=True, purge_instances=True
                )
        finally:
            engine.db_purge = original
        still_there = flat.is_file()
    return result is True and still_there


@func_case
async def test_cli_module_purge(tester: Tester):
    """cli.commands.module: 卸载清理的配置定位与顺序测试"""
    _use_cli_locale()
    await tester.test(_test_flat_config_path_is_resolved_by_config_table, "按 config_table 定位扁平配置")
    await tester.test(_test_adapter_instance_tables_are_matched_by_prefix, "适配器实例表按前缀匹配")
    await tester.test(_test_missing_config_table_deletes_nothing, "无 config_table 时不猜文件名")
    await tester.test(_test_instance_config_is_kept_without_confirmation, "未确认时保留实例配置")
    await tester.test(_test_instance_config_is_removed_when_confirmed, "确认后删除实例配置")
    await tester.test(_test_table_purge_failure_is_reported_and_not_swallowed, "删表失败不静默")
    await tester.test(_test_file_removal_failure_is_reported, "删文件失败不静默")
    await tester.test(_test_dry_run_writes_nothing, "dry-run 零写入")
    return tester
