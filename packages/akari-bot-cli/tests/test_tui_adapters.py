"""适配器页的安装入口、实例移除确认及 peer 状态测试。"""

import json
import subprocess
import sys
import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.adapters import (
    AdapterRecord,
    AdapterSnapshot,
    AdapterSourceError,
    StaticAdapterSource,
    SubprocessAdapterSource,
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
ALTERNATE = AdapterRecord(
    platform="discord",
    instance_id="work",
    client_name="Discord-work",
    table="bot_discord-work",
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


async def _with_page(body, source: StaticAdapterSource | None = None, *, size=(120, 34)):
    chosen = source if source is not None else _source()
    app = TuiApp(
        source=StaticModuleSource(),
        sources={"adapters": chosen},
        initial_page="adapters",
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("adapters")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _select(page, platform: str) -> None:
    order = page._records_in_row_order()
    target = next(index for index, record in enumerate(order) if record.platform == platform)
    rows = [index for index, kind in enumerate(page._row_kinds) if kind == "instance"]
    page.query_one("#adapter-list", compat.ListView).index = rows[target]


async def _open_remove_modal(page, pilot) -> None:
    page.request_remove_instance()
    await pilot.pause()


async def _choose_mode(app, pilot, index: int) -> None:
    # 此用例通过控件 API 验证操作流程，按钮可见性由布局用例验证。
    app.screen.query_one(f"#choice-{index}", compat.Button).press()
    await pilot.pause()


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
    # 适配器由独立页面管理，模块页排除所有适配器记录。
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


def _peer_source(payload) -> tuple[SubprocessAdapterSource, list[tuple[str, ...]]]:
    calls: list[tuple[str, ...]] = []

    def runner(argv, **kwargs):
        calls.append(tuple(argv))
        return subprocess.CompletedProcess(argv, 0, stdout=json.dumps(payload, ensure_ascii=False), stderr="")

    source = SubprocessAdapterSource(
        root="/tmp/akari-peer-instance",
        runner=runner,
        instance_factory=lambda: {"python": sys.executable},
    )
    return source, calls


def _test_peer_status_reads_core_snapshot():
    # 数据结构与 ``python -m akaribot.core.entrypoints.peers --json`` 保持一致。
    # 顶层包含 available/note；peer 记录同时包含页面未使用的 role/online。
    payload = {
        "peers": [
            {
                "peer_id": "Internal|47d7c765-ae6b-4b8a-9f30-12609f5b1a0c",
                "service": "CLI",
                "role": "cli",
                "state": "expired",
                "online": False,
                "lease_until": "2026-09-22T12:04:53.378047+00:00",
                "metadata": {"pid": 6830},
            },
            {
                "peer_id": "Telegram|8f2b0d3a",
                "service": "Telegram",
                "role": "client",
                "state": "ready",
                "online": True,
                "lease_until": "2999-01-01T00:00:00+00:00",
                "metadata": {"client_name": "Telegram"},
            },
            {
                "peer_id": "Worker|31c6f0",
                "service": "",
                "role": "worker",
                "state": "starting",
                "online": False,
                "lease_until": None,
                "metadata": {},
            },
        ],
        "available": True,
        "note": "",
    }
    source, calls = _peer_source(payload)
    snapshot = source.peer_status()
    expired = snapshot.status_for("CLI")
    ready = snapshot.status_for("Telegram")
    starting = snapshot.status_for("Worker|31c6f0")
    return (
        calls == [(sys.executable, "-m", "akaribot.core.entrypoints.peers", "--json")]
        and snapshot.available
        and snapshot.note == ""
        and len(snapshot.statuses) == 3
        and expired.client_name == "CLI"
        and expired.state == "expired"
        and expired.alive is False
        and expired.label == i18n.t("cli.tui.adapters.offline")
        and expired.detail == i18n.t("cli.tui.adapters.peer_state", state="expired")
        and ready.state == "ready"
        and ready.alive is True
        and ready.label == i18n.t("cli.tui.adapters.online")
        and ready.error == ""
        and starting.client_name == "Worker|31c6f0"
        and starting.state == "starting"
        and starting.alive is False
    )


def _test_peer_status_unavailable_reports_note():
    note = "数据库不可用：unable to open database file"
    source, _ = _peer_source({"peers": [], "available": False, "note": note})
    snapshot = source.peer_status()
    status = snapshot.status_for("Telegram")
    return (
        snapshot.available is False
        and snapshot.note == note
        and status.alive is None
        and status.label == i18n.t("cli.tui.common.unknown")
        and status.detail == note
        and status.detail != i18n.t("cli.tui.adapters.peer_missing")
    )


def _test_peer_status_shape_anomaly_degrades():
    # 无效响应应显示不可用原因，避免与空记录混淆。
    cases = (
        ([], i18n.t("cli.tui.adapters.peer_not_object")),
        ("no peers", i18n.t("cli.tui.adapters.peer_not_object")),
        ({}, i18n.t("cli.tui.adapters.peer_missing_field", field="available")),
        ({"available": True}, i18n.t("cli.tui.adapters.peer_missing_field", field="peers")),
        ({"peers": [], "note": ""}, i18n.t("cli.tui.adapters.peer_missing_field", field="available")),
        ({"peers": {}, "available": True}, i18n.t("cli.tui.adapters.peer_missing_field", field="peers")),
    )
    for payload, expected in cases:
        source, _ = _peer_source(payload)
        snapshot = source.peer_status()
        status = snapshot.status_for("Telegram")
        if snapshot.available or snapshot.note != expected:
            return False
        if status.alive is not None or status.label != i18n.t("cli.tui.common.unknown"):
            return False
        if status.detail != expected or status.detail == i18n.t("cli.tui.adapters.peer_missing"):
            return False
    return True


async def _test_peer_unavailable_page_shows_note():
    note = "peer 表不可读：no such table: job_queue_peers"
    source, _ = _peer_source({"peers": [], "available": False, "note": note})
    peers = source.peer_status()

    async def body(app, page, pilot, chosen):
        summary = page.summary_text
        await _select(page, "telegram")
        await pilot.pause()
        detail = page.detail_text
        await pilot.press("q")
        return summary, detail

    summary, detail = await _with_page(body, _source(peers=peers))
    return (
        i18n.t("cli.tui.adapters.peer_status_unknown", note=note) in summary
        and i18n.t("cli.tui.adapters.peer_status_unknown_hint") in summary
        and i18n.t("cli.tui.common.unknown") in detail
        and note in detail
        and i18n.t("cli.tui.adapters.peer_missing") not in detail
    )


async def _test_add_instance_uses_input_and_platform():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.query_one("#new-instance", compat.Input).value = "work"
        await pilot.pause()
        page.request_add_instance()
        await page.wait_for_idle()
        await pilot.pause()
        value = page.query_one("#new-instance", compat.Input).value
        await pilot.press("q")
        return list(chosen.added), value, page.status_text

    added, value, status = await _with_page(body, source)
    return added == [("telegram", "work")] and value == "" and status


async def _test_add_instance_rejects_bad_id():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.query_one("#new-instance", compat.Input).value = "Bad ID"
        await pilot.pause()
        page.request_add_instance()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(chosen.added), page.status_text

    added, status = await _with_page(body, source)
    return added == [] and status


async def _test_remove_instance_opens_modal_on_first_press():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await _choose_mode(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        screens = len(app.screen_stack)
        await pilot.press("q")
        return opened, labels, hint, screens, list(chosen.removed)

    opened, labels, hint, screens, removed = await _with_page(body, source)
    return (
        opened
        and all("{I18N:" not in label for label in labels)
        and labels == [i18n.t("cli.tui.adapters.remove_choice_plain"), i18n.t("cli.tui.adapters.cancel")]
        and hint == i18n.t("cli.tui.adapters.remove_only_hint", name=i18n.t("cli.tui.adapters.default_id"))
        and screens == 1
        and removed == [("telegram", "")]
    )


async def _test_remove_choice_cancel_keeps_instance():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return list(chosen.removed), status

    removed, status = await _with_page(body, source)
    return removed == [] and status == i18n.t("cli.tui.adapters.remove_cancelled")


async def _test_remove_repeat_within_debounce_opens_one_modal():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        depth = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return depth, list(chosen.removed)

    depth, removed = await _with_page(body, source)
    return depth == 2 and removed == []


async def _test_remove_requires_control_key():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        page.query_one("#adapter-list", compat.ListView).focus()
        await pilot.press("d")
        await pilot.pause()
        untouched = len(app.screen_stack) == 1 and not chosen.removed
        pairs = tuple((binding.key, binding.action) for binding in page.BINDINGS)
        await pilot.press("q")
        return untouched and ("d", "remove_instance") not in pairs and ("ctrl+d", "remove_instance") in pairs

    return await _with_page(body, source)


# 复位后同一目标应立即允许重新触发。
async def _test_remove_confirm_resets_on_refresh():
    source = _source()

    async def body(app, page, pilot, chosen):
        page._gate.accept("probe")
        page.refresh_instances(force=True)
        await page.wait_for_idle()
        await pilot.pause()
        reopened = page._gate.accept("probe")
        await pilot.press("q")
        return reopened, list(chosen.removed)

    reopened, removed = await _with_page(body, source)
    return reopened and removed == []


async def _test_remove_confirm_resets_on_highlight():
    source = _source(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE), instance_root="/tmp/inst"))

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page._gate.accept("probe")
        await _select(page, "discord")
        await pilot.pause()
        reopened = page._gate.accept("probe")
        await pilot.press("q")
        return reopened, list(chosen.removed)

    reopened, removed = await _with_page(body, source)
    return reopened and removed == []


async def _test_remove_confirm_resets_on_page_switch():
    source = _source()

    async def body(app, page, pilot, chosen):
        page._gate.accept("probe")
        app.show_page("modules")
        await pilot.pause()
        app.show_page("adapters")
        await pilot.pause()
        reopened = page._gate.accept("probe")
        await pilot.press("q")
        return reopened, list(chosen.removed)

    reopened, removed = await _with_page(body, source)
    return reopened and removed == []


async def _test_ctrl_d_opens_same_remove_modal():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        await pilot.press("ctrl+d")
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await _choose_mode(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        screens = len(app.screen_stack)
        await pilot.press("q")
        return opened, labels, hint, screens, list(chosen.removed)

    opened, labels, hint, screens, removed = await _with_page(body, source)
    return (
        opened
        and all("{I18N:" not in label for label in labels)
        and labels == [i18n.t("cli.tui.adapters.remove_choice_plain"), i18n.t("cli.tui.adapters.cancel")]
        and hint == i18n.t("cli.tui.adapters.remove_only_hint", name=i18n.t("cli.tui.adapters.default_id"))
        and screens == 1
        and removed == [("telegram", "")]
    )


async def _test_remove_message_states_data_kept():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        await _open_remove_modal(page, pilot)
        await _choose_mode(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        result = page.last_result
        status = page.status_text
        await pilot.press("q")
        return result, status

    result, status = await _with_page(body, source)
    expected = i18n.t("cli.tui.adapters.remove_kept", name=i18n.t("cli.tui.adapters.default_id"))
    # 数据源仅报告配置更改，数据保留说明由页面补充。
    return result == expected and expected in status and i18n.t("cli.tui.adapters.stub_instance_ok") not in result


def _test_pending_confirm_gate_debounce_and_reset():
    # 防抖窗口内忽略重复请求；窗口结束或复位后允许重新触发。
    gate = compat.PendingConfirm()
    accepted = gate.accept("x", now=100.0)
    burst = gate.accept("x", now=100.1)
    accepted_again = gate.accept("x", now=101.0)
    gate.reset()
    after_reset = gate.accept("x", now=101.1)
    return accepted and not burst and accepted_again and after_reset


async def _test_footer_keeps_page_bindings_within_80_columns():
    source = _source()
    app = TuiApp(
        source=StaticModuleSource(),
        sources={"adapters": source},
        initial_page="adapters",
        boot_started_at=time.monotonic(),
    )
    page_actions = {"refresh", "install", "remove_instance"}
    async with compat.app_test(app, size=(80, 24)) as pilot:
        page = app.page("adapters")
        await page.wait_for_idle()
        await pilot.pause()
        footer = app.query_one(compat.Footer)
        # 此用例仅检查页面声明的键位。
        keys = [child for child in footer.children if getattr(child, "action", "") in page_actions]
        content_width = sum(compat.widget_cells(child)[0] for child in keys)
        visible = tuple(binding.key for binding in page.BINDINGS if binding.show)
        hidden = tuple(binding.key for binding in page.BINDINGS if not binding.show)
        await pilot.press("q")
    return len(keys) == 2 and content_width <= 80 and visible == ("r", "i") and hidden == ("e", "a", "ctrl+d")


async def _test_instance_op_reloads_list():
    source = _source()

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        page.query_one("#new-instance", compat.Input).value = "work"
        await pilot.pause()
        before = chosen.calls["list"]
        page.request_add_instance()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return before, chosen.calls["list"]

    before, after = await _with_page(body, source)
    return after > before


async def _test_narrow_layout_keeps_controls_visible():
    async def body(app, page, pilot, chosen):
        for platform in ("telegram", "discord"):
            await _select(page, platform)
            await pilot.pause()
            widgets = [*page.query("#actions Button"), page.query_one("#new-instance", compat.Input)]
            if any(not page.region.contains_region(widget.region) for widget in widgets):
                return False
            if page.query_one("#adapter-list", compat.ListView).content_region.height < 3:
                return False
        return True

    return all([await _with_page(body, size=size) for size in ((80, 24), (60, 20))])


@func_case
async def test_tui_adapters(tester: Tester):
    """cli.tui.adapters: 未安装平台与安装入口测试"""
    _use_cli_locale()
    await tester.test(_test_pending_confirm_gate_debounce_and_reset, "确认闸门防抖与复位")
    # 放大防抖窗口，避免执行速度影响重复请求的判断。
    with mock.patch.object(compat.PendingConfirm, "debounce", 60.0):
        await tester.test(_test_remove_repeat_within_debounce_opens_one_modal, "连发两次请求不叠模态框")
    # 关闭防抖延迟，使交互用例无需等待；防抖行为由专项用例验证。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
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
        await tester.test(_test_peer_status_reads_core_snapshot, "解析 core peer 快照的真实字段")
        await tester.test(_test_peer_status_unavailable_reports_note, "入口不可用时以 note 作为原因")
        await tester.test(_test_peer_status_shape_anomaly_degrades, "快照形状异常降级为未知")
        await tester.test(_test_peer_unavailable_page_shows_note, "快照不可用时页面显示未知与原因")
        await tester.test(_test_add_instance_uses_input_and_platform, "按输入框与平台新增实例")
        await tester.test(_test_add_instance_rejects_bad_id, "非法实例 ID 不执行")
        await tester.test(_test_remove_instance_opens_modal_on_first_press, "请求移除即弹模态")
        await tester.test(_test_remove_choice_cancel_keeps_instance, "取消移除模态不执行并提示")
        await tester.test(_test_remove_confirm_resets_on_refresh, "刷新作废待确认的移除")
        await tester.test(_test_remove_confirm_resets_on_highlight, "换选中项作废待确认的移除")
        await tester.test(_test_remove_confirm_resets_on_page_switch, "切页作废待确认的移除")
        await tester.test(_test_remove_requires_control_key, "仅 Ctrl+D 触发移除，单字母 d 不执行操作")
        await tester.test(_test_ctrl_d_opens_same_remove_modal, "ctrl+d 弹同一个仅移除确认框")
        await tester.test(_test_remove_message_states_data_kept, "移除后提示写明数据保留")
        await tester.test(_test_footer_keeps_page_bindings_within_80_columns, "80 列页脚不溢出")
        await tester.test(_test_instance_op_reloads_list, "实例变更后重载列表")
        await tester.test(_test_narrow_layout_keeps_controls_visible, "窄屏列表、输入框与操作按钮保持可见")
    return tester
