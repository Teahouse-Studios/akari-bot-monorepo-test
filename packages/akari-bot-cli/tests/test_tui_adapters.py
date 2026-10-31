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
    normalize_snapshot,
)
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.config import ConfigField, ConfigFormScreen, SetResult
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
# 缺少适配器包的配置：启用的仍列出以暴露问题，未启用的与未安装平台一样不进列表。
MISSING_ENABLED = AdapterRecord(
    platform="kook", client_name="Kook", table="bot_kook", enable=True, enabled=True, installed=False
)
MISSING_DISABLED = AdapterRecord(
    platform="matrix", client_name="Matrix", table="bot_matrix", enable=False, enabled=False, installed=False
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


def _missing_source() -> StaticAdapterSource:
    return _source(snapshot=AdapterSnapshot(instances=(INSTALLED, MISSING_ENABLED, MISSING_DISABLED)))


async def _test_list_hides_uninstalled_disabled():
    async def body(app, page, pilot, source):
        platforms = [record.platform for record in page._records_in_row_order()]
        await pilot.press("q")
        return platforms

    platforms = await _with_page(body, _missing_source())
    return platforms == ["kook", "telegram"]


async def _test_uninstalled_row_marked():
    async def body(app, page, pilot, source):
        await _select(page, "kook")
        await pilot.pause()
        record = page.selected_record
        rows = page.row_texts()
        detail = page.detail_text
        await pilot.press("q")
        return record.installable, rows, detail

    installable, rows, detail = await _with_page(body, _missing_source())
    return (
        installable
        and any(i18n.t("cli.tui.adapters.state_not_installed") in row for row in rows)
        and i18n.t("cli.tui.adapters.detail_not_installed", platform="kook") in detail
    )


async def _test_button_follows_state():
    async def body(app, page, pilot, source):
        await _select(page, "kook")
        await pilot.pause()
        not_installed = str(page.query_one("#toggle", compat.Button).label)
        await _select(page, "telegram")
        await pilot.pause()
        installed = str(page.query_one("#toggle", compat.Button).label)
        await pilot.press("q")
        return not_installed, installed

    not_installed, installed = await _with_page(body, _missing_source())
    # 按钮文字随所选行切换，并带上切换键 e。
    return not_installed == compat.key_hint(i18n.t("cli.tui.adapters.action_install"), "e") and installed == (
        compat.key_hint(i18n.t("cli.tui.adapters.action_disable"), "e")
    )


async def _test_install_action_streams_output():
    # 按 i 打开安装对话框，只列未安装的平台；回车安装高亮项并显示进度。
    async def body(app, page, pilot, source):
        await pilot.press("i")
        await pilot.pause()
        platforms = [value for value, _ in app.screen.options]
        await pilot.press("down", "enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return platforms, source.installed, page._stream_lines, page.status_text

    platforms, installed, lines, status = await _with_page(body)
    return (
        platforms == ["discord", "onebot"]
        and installed == ["onebot"]
        and list(lines) == ["Resolved 1 package", "Installed 1 package"]
        and i18n.t("cli.tui.adapters.stub_install_ok") in status
    )


async def _test_toggle_on_uninstalled_installs():
    # 缺包的已启用配置按 e 走安装对话框并预选该平台，不改动启用状态。
    async def body(app, page, pilot, source):
        await _select(page, "kook")
        await pilot.pause()
        await pilot.press("e")
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.installed, source.toggles

    installed, toggles = await _with_page(body, _missing_source())
    return installed == ["kook"] and toggles == []


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


async def _test_refresh_keeps_row_highlighted():
    # 关键回归：重建列表后选中行必须仍然亮着——ListView 只在 index 变化时打高亮。
    source = _source(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE), instance_root="/tmp/inst"))

    async def body(app, page, pilot, chosen):
        list_view = page.query_one("#adapter-list", compat.ListView)
        await _select(page, "discord")
        await pilot.pause()
        target = list_view.index
        before = [bool(item.highlighted) for item in list_view.children]
        page.refresh_instances()
        await page.wait_for_idle()
        await pilot.pause()
        after = (list_view.index, [bool(item.highlighted) for item in list_view.children])
        await pilot.press("q")
        return target, before, after

    target, before, after = await _with_page(body, source)

    def only(flags, index):
        return index is not None and flags[index] is True and sum(flags) == 1

    return only(before, target) and after[0] == target and only(after[1], target)


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


async def _test_add_instance_dialog_creates_on_chosen_platform():
    # 对话框列出已安装的平台（含仅见于 installed_platforms、尚无实例的平台），预选当前行的平台，
    # 确认后按所选平台与输入的实例 ID 新建。
    installed = normalize_snapshot({"installed_platforms": ["kook"]}).installed_platforms
    source = _source(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE), installed_platforms=installed))

    async def body(app, page, pilot, chosen):
        await _select(page, "telegram")
        await pilot.pause()
        await pilot.press("n")
        await pilot.pause()
        screen = app.screen
        platforms = [value for value, _ in screen.options]
        preselected = screen.query_one("#pick-list", compat.ListView).index
        await pilot.press(*"alt", "enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return platforms, preselected, list(chosen.added)

    platforms, preselected, added = await _with_page(body, source)
    return platforms == ["discord", "kook", "telegram"] and preselected == 2 and added == [("telegram", "alt")]


async def _test_add_instance_rejects_invalid_ids():
    # 空、非法与重名的实例 ID 都在对话框内提示且不关闭；取消后不执行。
    source = _source(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE)))

    async def body(app, page, pilot, chosen):
        await _select(page, "discord")
        await pilot.pause()
        page.request_add_instance()
        await pilot.pause()
        screen = app.screen
        observed = []
        for value in ("", "Bad ID", "work"):
            screen.query_one("#pick-input", compat.Input).value = value
            await pilot.pause()
            await pilot.press("enter")
            await pilot.pause()
            observed.append((app.screen is screen, str(screen.query_one("#pick-error", compat.Static).content)))
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return observed, list(chosen.added), page.status_text

    observed, added, status = await _with_page(body, source)
    expected = [
        i18n.t("cli.tui.adapters.instance_id_required"),
        i18n.t("cli.tui.adapters.instance_id_invalid", instance_id="Bad ID"),
        i18n.t("cli.tui.adapters.instance_id_exists", platform="discord", instance_id="work"),
    ]
    return (
        observed == [(True, text) for text in expected]
        and added == []
        and status == i18n.t("cli.tui.adapters.add_cancelled")
    )


FORM_TABLE = "bot_discord-work"
FORM_FIELDS = (
    ConfigField(key="enable", table=FORM_TABLE, kind="bool", type_name="bool", value=False),
    ConfigField(key="port", table=FORM_TABLE, kind="int", type_name="int", value=8080, default=8080),
    ConfigField(key="api_url", table=FORM_TABLE, kind="str", value="<Replace me>", is_placeholder=True),
    ConfigField(key="token", table=FORM_TABLE, kind="str", secret=True, value="<Replace me>", is_placeholder=True),
)


def _form_source(**kwargs) -> StaticAdapterSource:
    return _source(
        snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE)), config_fields={FORM_TABLE: FORM_FIELDS}, **kwargs
    )


async def _open_form(page, pilot) -> None:
    await _select(page, "telegram")
    await pilot.pause()
    page.on_add_chosen(("discord", "work"))
    await page.wait_for_idle()
    await pilot.pause()


def _form_row(screen, key: str):
    return next(row for row in screen.rows() if row.field.key == key)


async def _test_add_instance_form_writes_filled_fields():
    # 待填写项排最前且为空，留空不写入；密钥写入 _secret 段，enable 排最后、最后写入；关闭后高亮新实例。
    source = _form_source()

    async def body(app, page, pilot, chosen):
        await _open_form(page, pilot)
        screen = app.screen
        order = [row.field.key for row in screen.rows()]
        prefill = (_form_row(screen, "api_url").text, _form_row(screen, "token").text, _form_row(screen, "port").text)
        focused_first = app.focused is _form_row(screen, "api_url").control()
        _form_row(screen, "token").set_text("tok")
        _form_row(screen, "enable").query_one(compat.Button).press()
        await pilot.pause()
        before = chosen.calls["list"]
        await pilot.press("ctrl+s")
        await page.wait_for_idle()
        await pilot.pause()
        closed = not isinstance(app.screen, ConfigFormScreen)
        selected = page.selected_record.key
        await pilot.press("q")
        return (
            order,
            prefill,
            focused_first,
            list(chosen.config_written),
            closed,
            chosen.calls["list"] > before,
            selected,
            page.status_text,
        )

    order, prefill, focused, written, closed, reloaded, selected, status = await _with_page(body, source)
    return (
        order == ["api_url", "token", "port", "enable"]
        and prefill == ("", "", "8080")
        and focused
        and written == [(f"{FORM_TABLE}_secret", "token", "tok"), (FORM_TABLE, "enable", "true")]
        and closed
        and reloaded
        and selected == FORM_TABLE
        and status == i18n.t("cli.tui.adapters.config_form_saved", name="discord/work", count=2)
    )


async def _test_add_instance_form_stops_at_failure_and_resumes():
    # 校验失败不写入；写入失败停在出错项且不启用，密钥项不显示命令输出；重试不重复已写入的项。
    source = _form_source(config_result={"token": SetResult(False, "写入失败", "boom tok-value")})

    async def body(app, page, pilot, chosen):
        await _open_form(page, pilot)
        screen = app.screen
        _form_row(screen, "port").set_text("abc")
        await pilot.press("ctrl+s")
        await pilot.pause()
        invalid = (list(chosen.config_written), bool(_form_row(screen, "port").error_text))
        _form_row(screen, "port").set_text("8080")
        _form_row(screen, "api_url").set_text("https://a")
        _form_row(screen, "token").set_text("tok-value")
        _form_row(screen, "enable").query_one(compat.Button).press()
        await pilot.pause()
        await pilot.press("ctrl+s")
        await page.wait_for_idle()
        await pilot.pause()
        failed = (list(chosen.config_written), _form_row(screen, "token").error_text, app.screen is screen)
        chosen._config_result.clear()
        await pilot.press("ctrl+s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return invalid, failed, list(chosen.config_written)

    invalid, failed, written = await _with_page(body, source)
    url = (FORM_TABLE, "api_url", "https://a")
    return (
        invalid == ([], True)
        and failed == ([url], "写入失败", True)
        and written == [url, (f"{FORM_TABLE}_secret", "token", "tok-value"), (FORM_TABLE, "enable", "true")]
    )


async def _test_add_instance_form_can_be_skipped():
    # 未保存内容关闭前先确认，取消后内容保留；读不到配置项时实例仍算创建成功，不弹表单。
    class _Broken(StaticAdapterSource):
        def config_fields(self, table):
            raise AdapterSourceError("schema 不可用")

    async def closing(app, page, pilot, chosen):
        await _open_form(page, pilot)
        screen = app.screen
        _form_row(screen, "api_url").set_text("x")
        await pilot.press("escape")
        await pilot.pause()
        asked = type(app.screen).__name__
        await pilot.press("escape")
        await pilot.pause()
        kept = app.screen is screen and _form_row(screen, "api_url").text == "x"
        _form_row(screen, "api_url").set_text("")
        await pilot.press("escape")
        await pilot.pause()
        closed = not isinstance(app.screen, ConfigFormScreen)
        selected = page.selected_record.key
        await pilot.press("q")
        return asked, kept, closed, selected, list(chosen.config_written), page.status_text

    asked, kept, closed, selected, written, status = await _with_page(closing, _form_source())

    async def broken(app, page, pilot, chosen):
        await _open_form(page, pilot)
        form = isinstance(app.screen, ConfigFormScreen)
        await pilot.press("q")
        return form, list(chosen.added), page.status_text, page._busy

    form, added, broken_status, busy = await _with_page(
        broken, _Broken(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE)), available=CANDIDATES)
    )
    return (
        asked == "ChoiceScreen"
        and kept
        and closed
        and selected == FORM_TABLE
        and written == []
        and status == i18n.t("cli.tui.adapters.config_form_skipped", name="discord/work")
        and not form
        and added == [("discord", "work")]
        and "schema 不可用" in broken_status
        and not busy
    )


def _test_subprocess_instance_ops_call_cli():
    # 新增与移除经 adapter instance 子命令执行，成败取决于退出码。
    calls: list[tuple[str, ...]] = []

    def runner(argv, **kwargs):
        calls.append(tuple(argv))
        return subprocess.CompletedProcess(argv, 0 if len(calls) < 3 else 1, stdout="ok", stderr="boom")

    source = SubprocessAdapterSource(root="/tmp/akari-adapter-instance", runner=runner)
    added = source.add_instance("telegram", "alt")
    removed = source.remove_instance(ALTERNATE)
    failed = source.add_instance("telegram", "alt")
    written = source.set_config("bot_telegram-alt_secret", "token", "v")
    return (
        calls[3][-6:] == ("config", "set", "token", "v", "--table", "bot_telegram-alt_secret")
        and not written.ok
        and added.ok
        and removed.ok
        and not failed.ok
        and failed.detail == "boom"
        and calls[0][-5:] == ("adapter", "instance", "add", "telegram", "alt")
        and calls[1][-5:] == ("adapter", "instance", "remove", "discord", "work")
    )


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
    return len(keys) == 2 and content_width <= 80 and visible == ("r", "i") and hidden == ("e", "n", "ctrl+d")


async def _test_instance_op_reloads_list():
    source = _source()

    async def body(app, page, pilot, chosen):
        before = chosen.calls["list"]
        page.on_add_chosen(("telegram", "work"))
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
            if any(not page.region.contains_region(button.region) for button in page.query("#actions Button")):
                return False
            if page.query_one("#adapter-list", compat.ListView).content_region.height < 3:
                return False
        page.request_add_instance()
        await pilot.pause()
        await pilot.pause()
        screen = app.screen
        box = screen.query_one("#pick-box")
        controls = [screen.query_one("#pick-input"), *screen.query("#pick-actions Button")]
        return all(box.region.contains_region(widget.region) for widget in controls)

    source = _source(snapshot=AdapterSnapshot(instances=(INSTALLED, ALTERNATE)))
    return all([await _with_page(body, source, size=size) for size in ((80, 24), (60, 20))])


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
        await tester.test(_test_list_hides_uninstalled_disabled, "未安装且未启用的平台不进列表")
        await tester.test(_test_uninstalled_row_marked, "未安装行标注状态与详情")
        await tester.test(_test_button_follows_state, "按钮随安装状态切换")
        await tester.test(_test_install_action_streams_output, "按 i 从对话框选择未安装平台安装并显示进度")
        await tester.test(_test_toggle_on_uninstalled_installs, "缺包的已启用配置按 e 走安装")
        await tester.test(_test_toggle_still_works_for_installed, "已安装时按 e 切换启用")
        await tester.test(_test_summary_counts_instances_only, "摘要只计真实例")
        await tester.test(_test_refresh_keeps_row_highlighted, "刷新后选中行仍然高亮")
        await tester.test(_test_available_failure_keeps_instances, "清单失败不清空实例")
        await tester.test(_test_modules_page_excludes_adapters, "模块页不列适配器")
        await tester.test(_test_available_normalizer_reads_module_available_json, "解析可安装清单")
        await tester.test(_test_adapter_record_installable_semantics, "缺包但有配置也算可安装")
        await tester.test(_test_peer_status_reads_core_snapshot, "解析 core peer 快照的真实字段")
        await tester.test(_test_peer_status_unavailable_reports_note, "入口不可用时以 note 作为原因")
        await tester.test(_test_peer_status_shape_anomaly_degrades, "快照形状异常降级为未知")
        await tester.test(_test_peer_unavailable_page_shows_note, "快照不可用时页面显示未知与原因")
        await tester.test(_test_add_instance_dialog_creates_on_chosen_platform, "对话框列出已安装平台并按所选平台新建")
        await tester.test(_test_add_instance_rejects_invalid_ids, "空、非法与重名实例 ID 在对话框内提示且不执行")
        await tester.test(
            _test_add_instance_form_writes_filled_fields, "新增实例后弹表单，只写入已填项且 enable 最后写入"
        )
        await tester.test(
            _test_add_instance_form_stops_at_failure_and_resumes, "表单写入失败停在出错项，重试不重复写入"
        )
        await tester.test(
            _test_add_instance_form_can_be_skipped, "表单可跳过且未保存内容先确认，读不到配置项不影响新增"
        )
        await tester.test(_test_subprocess_instance_ops_call_cli, "实例新增与移除经 adapter instance 子命令执行")
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
        await tester.test(_test_narrow_layout_keeps_controls_visible, "窄屏下列表、操作按钮与新增实例对话框保持可见")
    return tester
