"""适配器页：未安装的平台也要出现，并提供安装与启用／禁用。

两页各管一段：模块页只列模块，适配器页列出全部平台——未安装的给安装入口，已装的给启用／禁用。
未安装的平台若不出现在列表里，用户只能另开命令去猜有哪些适配器可选；适配器若混进模块页，又会
让人以为「安装模块」能装适配器。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.adapters import (
    AdapterRecord,
    AdapterSnapshot,
    AdapterSourceError,
    StaticAdapterSource,
    available_adapter_records,
)
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

INSTALLED = AdapterRecord(
    platform="telegram",
    instance_id="",
    client_name="Telegram",
    table="bot_telegram",
    enable=True,
    enabled=True,
    installed=True,
)
CANDIDATES = (
    AdapterRecord(platform="discord", installed=False, developers=("OasisAkari",)),
    AdapterRecord(platform="onebot", installed=False),
    AdapterRecord(platform="telegram", installed=True),
)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticAdapterSource:
    params = {
        "snapshot": AdapterSnapshot(instances=(INSTALLED,), instance_root="/tmp/inst"),
        "available": CANDIDATES,
        "install_lines": ["Resolved 1 package", "Installed 1 package"],
    }
    params.update(kwargs)
    return StaticAdapterSource(**params)


async def _with_page(body, source: StaticAdapterSource | None = None):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"adapters": chosen}, initial_page="adapters", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(120, 34)) as pilot:
        page = app.page("adapters")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _select(page, platform: str) -> None:
    order = page._records_in_row_order()
    target = next(index for index, record in enumerate(order) if record.platform == platform)
    rows = [index for index, kind in enumerate(page._row_kinds) if kind == "instance"]
    page.query_one("#adapter-list", compat.ListView).index = rows[target]


async def _test_uninstalled_platforms_are_listed():
    async def body(app, page, pilot, source):
        platforms = [record.platform for record in page._records_in_row_order()]
        await pilot.press("q")
        return platforms

    platforms = await _with_page(body)
    return platforms == ["discord", "onebot", "telegram"]


async def _test_uninstalled_row_marked():
    async def body(app, page, pilot, source):
        await _select(page, "discord")
        await pilot.pause()
        record = page.selected_record
        rows = page.row_texts()
        detail = page.detail_text
        await pilot.press("q")
        return record.installable, record.display_id, rows, detail

    installable, display_id, rows, detail = await _with_page(body)
    return (
        installable
        and display_id == "—"
        and any(i18n.t("cli.tui.adapters.state_not_installed") in row for row in rows)
        and i18n.t("cli.tui.adapters.detail_not_installed", platform="discord") in detail
    )


async def _test_button_follows_state():
    async def body(app, page, pilot, source):
        await _select(page, "onebot")
        await pilot.pause()
        not_installed = str(page.query_one("#toggle", compat.Button).label)
        await _select(page, "telegram")
        await pilot.pause()
        installed = str(page.query_one("#toggle", compat.Button).label)
        await pilot.press("q")
        return not_installed, installed

    not_installed, installed = await _with_page(body)
    return not_installed == i18n.t("cli.tui.adapters.action_install") and installed == i18n.t(
        "cli.tui.adapters.action_disable"
    )


async def _test_install_action_streams_output():
    async def body(app, page, pilot, source):
        await _select(page, "onebot")
        await pilot.pause()
        await pilot.press("i")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.installed, page._stream_lines, page.status_text

    installed, lines, status = await _with_page(body)
    return (
        installed == ["onebot"]
        and list(lines) == ["Resolved 1 package", "Installed 1 package"]
        and i18n.t("cli.tui.adapters.stub_install_ok") in status
    )


async def _test_toggle_on_uninstalled_installs():
    async def body(app, page, pilot, source):
        await _select(page, "discord")
        await pilot.pause()
        await pilot.press("e")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.installed, source.toggles

    installed, toggles = await _with_page(body)
    return installed == ["discord"] and toggles == []


async def _test_toggle_still_works_for_installed():
    async def body(app, page, pilot, source):
        await _select(page, "telegram")
        await pilot.pause()
        await pilot.press("e")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.toggles, source.installed

    toggles, installed = await _with_page(body)
    return toggles == [("bot_telegram", False)] and installed == []


async def _test_summary_counts_instances_only():
    async def body(app, page, pilot, source):
        text = page.summary_text
        await pilot.press("q")
        return text

    text = await _with_page(body)
    return (
        i18n.t("cli.tui.adapters.summary_counts", total=1, enabled=1, platforms=1) in text
        and i18n.t("cli.tui.adapters.summary_installable", count=2) in text
    )


async def _test_available_failure_keeps_instances():
    class _Broken(StaticAdapterSource):
        def list_available(self):
            raise AdapterSourceError("registry 不可用")

    source = _Broken(snapshot=AdapterSnapshot(instances=(INSTALLED,)), available=CANDIDATES)

    async def body(app, page, pilot, chosen):
        platforms = [record.platform for record in page._records_in_row_order()]
        await pilot.press("q")
        return platforms, page.summary_text

    platforms, summary = await _with_page(body, source)
    return platforms == ["telegram"] and i18n.t("cli.tui.adapters.available_failed", error="registry 不可用") in summary


async def _test_modules_page_excludes_adapters():
    # 模块页既不列已装适配器，也不列未装适配器：两页各管一段。
    installed = [
        ModuleRecord(name="coin", dist="akari-bot-module-coin", kind="module", state="installed"),
        ModuleRecord(name="telegram", dist="akari-bot-adapter-telegram", kind="adapter", state="installed"),
    ]
    available = [
        *installed,
        ModuleRecord(name="wiki", dist="akari-bot-module-wiki", kind="module", state="available"),
        ModuleRecord(name="discord", dist="akari-bot-adapter-discord", kind="adapter", state="available"),
    ]
    source = StaticModuleSource(records=installed, available=available)
    app = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(110, 30)) as pilot:
        page = app.modules_page()
        await page.wait_for_idle()
        await pilot.pause()
        kinds = {record.kind for record in page.visible_records}
        names = [record.name for record in page.visible_records]
        await pilot.press("q")
    return kinds == {"module"} and names == ["coin", "wiki"]


def _test_available_normalizer_reads_module_available_json():
    records = available_adapter_records(
        [
            {"name": "discord", "kind": "adapter", "installed": False, "developers": ["OasisAkari"]},
            {"name": "telegram", "kind": "adapter", "installed": True, "developers": []},
        ]
    )
    return (
        len(records) == 2
        and records[0].platform == "discord"
        and records[0].installable
        and records[0].developers == ("OasisAkari",)
        and not records[1].installable
    )


def _test_adapter_record_installable_semantics():
    missing = AdapterRecord(platform="kook", table="bot_kook", installed=False)
    return missing.installable and missing.configured


@func_case
async def test_tui_adapters(tester: Tester):
    """cli.tui.adapters: 未安装平台与安装入口测试"""
    _use_cli_locale()
    await tester.test(_test_uninstalled_platforms_are_listed, "未安装平台并入列表且不重复")
    await tester.test(_test_uninstalled_row_marked, "未安装行标注状态与详情")
    await tester.test(_test_button_follows_state, "按钮随安装状态切换")
    await tester.test(_test_install_action_streams_output, "按 i 安装并显示进度")
    await tester.test(_test_toggle_on_uninstalled_installs, "未安装时按 e 走安装")
    await tester.test(_test_toggle_still_works_for_installed, "已安装时按 e 切换启用")
    await tester.test(_test_summary_counts_instances_only, "摘要只计真实例")
    await tester.test(_test_available_failure_keeps_instances, "清单失败不清空实例")
    await tester.test(_test_modules_page_excludes_adapters, "模块页不列适配器")
    await tester.test(_test_available_normalizer_reads_module_available_json, "解析可安装清单")
    await tester.test(_test_adapter_record_installable_semantics, "缺包但有配置也算可安装")
    return tester
