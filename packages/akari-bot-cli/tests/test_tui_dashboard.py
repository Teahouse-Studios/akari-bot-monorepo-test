"""概览页：实例信息与运行状态。

环境信息与环境动作已移到「环境」页、旧项目迁移移到「杂项」页，本页只留实例本身：根目录、名称、
语言、core 版本与来源、运行状态与判据、更新提示。
"""

import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dashboard import (
    DashboardSnapshot,
    InstanceRow,
    ServiceRow,
    StaticDashboardSource,
    StaticInstanceListSource,
    StaticServiceControl,
)
from akaribot.testing import Tester, func_case

SNAPSHOT = DashboardSnapshot(
    instance_root="/tmp/fake-instance",
    instance_name="demo",
    instance_mode="installed",
    locale="zh_cn",
    core_version="0.1.0",
    core_origin="akaribot.toml",
    running=True,
    running_detail="锁文件被持有：/tmp/fake-instance/.bot.lock",
    update_hint="",
)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _instance_rows() -> tuple[InstanceRow, ...]:
    return (
        InstanceRow(name="alpha", root=Path("/tmp/alpha"), running=True, autostart=True),
        InstanceRow(name="beta", root=Path("/tmp/beta"), running=False, restart_on_crash=True),
    )


async def _with_page(body, source=None, size=(110, 32), instances=None, service=None):
    chosen = source if source is not None else StaticDashboardSource(SNAPSHOT, running=True)
    listed = instances if instances is not None else StaticInstanceListSource(_instance_rows())
    control = service if service is not None else StaticServiceControl()
    app = TuiApp(
        sources={"dashboard": chosen, "dashboard_instances": listed, "dashboard_service": control},
        initial_page="dashboard",
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("dashboard")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen, listed, control)


def _fields(page) -> dict[str, str]:
    return dict(page.rows)


async def _test_fields_show_instance_facts():
    async def body(app, page, pilot, source, listed, control):
        rows = _fields(page)
        await pilot.press("q")
        return rows

    rows = await _with_page(body)
    return (
        rows[i18n.t("cli.tui.dashboard.field_instance_root")] == "/tmp/fake-instance"
        and rows[i18n.t("cli.tui.dashboard.field_instance_name")] == "demo"
        and rows[i18n.t("cli.tui.dashboard.field_core_version")] == "0.1.0"
        and rows[i18n.t("cli.tui.dashboard.field_core_origin")] == "akaribot.toml"
        and i18n.t("cli.tui.common.unknown") not in rows.values()
    )


async def _test_state_follows_probe():
    # 运行状态由锁文件探测决定，行文本带状态标记。
    async def body(app, page, pilot, source, listed, control):
        running = _fields(page)[i18n.t("cli.tui.dashboard.field_state")]
        source.set_running(False)
        page.refresh_running()
        await pilot.pause()
        stopped = _fields(page)[i18n.t("cli.tui.dashboard.field_state")]
        await pilot.press("q")
        return running, stopped

    running, stopped = await _with_page(body)
    return running.startswith("●") and stopped.startswith("○") and running != stopped


async def _test_refresh_rereads_snapshot():
    async def body(app, page, pilot, source, listed, control):
        before = source.calls["snapshot"]
        page.refresh_snapshot(force=True)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return before, source.calls["snapshot"]

    before, after = await _with_page(body)
    return after > before


async def _test_load_failure_degrades_to_status():
    class Failing:
        """快照读取必定失败的数据源，用于断言降级行为。"""

        calls = {"snapshot": 0, "probe": 0}

        def snapshot(self):
            self.calls["snapshot"] += 1
            raise RuntimeError("boom")

        def probe_running(self):
            return None

    async def body(app, page, pilot, source, listed, control):
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body, Failing())
    return "boom" in status


async def _test_instance_list_marks_state_and_policy():
    # 清单每行给运行状态与策略标记，未登记的当前实例也要出现，否则看不到自己在管哪个。
    async def body(app, page, pilot, source, listed, control):
        context.set_active_root("/tmp/alpha")
        page.refresh_instances()
        await pilot.pause()
        rows = page.instance_rows
        await pilot.press("q")
        return rows

    rows = await _with_page(body)
    return (
        [row.name for row in rows] == ["alpha", "beta"]
        and rows[0].autostart
        and rows[1].restart_on_crash
        and rows[0].state_label.startswith("●")
        and rows[1].state_label.startswith("○")
    )


async def _test_enter_switches_instance():
    # 在清单里选中一条即切换当前实例：上下文与所有页面的下一次取数都指向它。
    with TemporaryDirectory(prefix="akari-switch-") as raw:
        beta = Path(raw) / "beta"
        beta.mkdir()
        (beta / "akaribot.toml").write_text("[instance]\nname = 'beta'\n", encoding="utf-8")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=Path("/tmp/alpha"), running=True),
                InstanceRow(name="beta", root=beta, running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            await page.wait_for_idle()
            await pilot.pause()
            active = context.active_root()
            status = page.status_text
            await pilot.press("q")
            return active, status, chosen

        active, status, _ = await _with_page(body, instances=listed)
    # 上下文里的根按真实路径保存：macOS 的临时目录本身是软链接。
    return active == beta.resolve() and status


async def _test_switch_refused_for_missing_directory():
    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.switch_to_selected()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body)
    return i18n.t("cli.tui.dashboard.switch_missing").split("${")[0].strip() in status


async def _test_policy_toggle_writes_registry():
    listed = StaticInstanceListSource(_instance_rows())

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.toggle_policy("autostart")
        await pilot.pause()
        page.toggle_policy("restart_on_crash")
        await pilot.pause()
        await pilot.press("q")
        return list(listed.policies)

    policies = await _with_page(body, instances=listed)
    return policies == [("alpha", {"autostart": False}), ("alpha", {"restart_on_crash": True})]


async def _test_register_instance_from_prompt():
    listed = StaticInstanceListSource(_instance_rows())

    async def body(app, page, pilot, source, listed, control):
        page.request_add_instance()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/gamma"
        await pilot.press("enter")
        await pilot.pause()
        await pilot.press("q")
        return opened, list(listed.added)

    opened, added = await _with_page(body, instances=listed)
    return opened and added == ["/tmp/gamma"]


async def _test_unregister_needs_two_presses():
    listed = StaticInstanceListSource(_instance_rows())

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        asked = list(listed.removed), page.status_text
        page.request_remove_instance()
        await pilot.pause()
        await pilot.press("q")
        return asked, list(listed.removed)

    asked, removed = await _with_page(body, instances=listed)
    return asked[0] == [] and asked[1] and removed == ["alpha"]


async def _test_policy_refused_for_unregistered():
    listed = StaticInstanceListSource((InstanceRow(name="", root=Path("/tmp/plain"), registered=False),))

    async def body(app, page, pilot, source, listed, control):
        page.toggle_policy("autostart")
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status, list(listed.policies)

    status, policies = await _with_page(body, instances=listed)
    return policies == [] and status


async def _test_service_row_reports_state():
    # 概览页要能看出服务装没装：装了就写清后端、注册状态与单元文件位置。
    control = StaticServiceControl(
        ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist"))
    )

    async def body(app, page, pilot, source, listed, control):
        text = str(page.query_one("#service", compat.Static).render())
        await pilot.press("q")
        return text

    text = await _with_page(body, service=control)
    return "launchd" in text and "/tmp/agent.plist" in text


async def _test_service_row_reports_unsupported():
    control = StaticServiceControl(ServiceRow(backend="unsupported", detail="Windows 尚未支持"))

    async def body(app, page, pilot, source, listed, control):
        text = str(page.query_one("#service", compat.Static).render())
        await pilot.press("q")
        return text

    text = await _with_page(body, service=control)
    return "Windows" in text


async def _test_service_install_needs_two_presses():
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        asked = control.calls["install"], page.status_text
        page.request_toggle_service()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, control.calls, page.service_row.installed

    asked, calls, installed = await _with_page(body, service=control)
    return asked[0] == 0 and asked[1] and calls["install"] == 1 and installed


async def _test_service_uninstall_when_installed():
    control = StaticServiceControl(
        ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist")),
        result=ServiceRow(backend="launchd", installed=False, enabled=False),
    )

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        page.request_toggle_service()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return control.calls, page.service_row.installed

    calls, installed = await _with_page(body, service=control)
    return calls["uninstall"] == 1 and calls["install"] == 0 and not installed


@func_case
async def test_tui_dashboard(tester: Tester):
    """cli.tui.dashboard: 实例信息与运行状态测试"""
    _use_cli_locale()
    await tester.test(_test_fields_show_instance_facts, "展示实例根、名称与版本")
    await tester.test(_test_state_follows_probe, "运行状态跟着探测结果")
    await tester.test(_test_refresh_rereads_snapshot, "刷新重新读取快照")
    await tester.test(_test_load_failure_degrades_to_status, "读取失败只降级到状态栏")
    await tester.test(_test_instance_list_marks_state_and_policy, "实例清单带状态与策略标记")
    await tester.test(_test_enter_switches_instance, "在清单里切换实例")
    await tester.test(_test_switch_refused_for_missing_directory, "目录无 akaribot.toml 时拒绝切换")
    await tester.test(_test_policy_toggle_writes_registry, "自启与崩溃重启开关写回注册表")
    await tester.test(_test_register_instance_from_prompt, "输入框登记实例")
    await tester.test(_test_unregister_needs_two_presses, "移除登记需二次确认")
    await tester.test(_test_policy_refused_for_unregistered, "未登记实例不设策略")
    await tester.test(_test_service_row_reports_state, "服务行展示后端与单元文件")
    await tester.test(_test_service_row_reports_unsupported, "平台不支持时如实说明")
    await tester.test(_test_service_install_needs_two_presses, "安装服务需二次确认")
    await tester.test(_test_service_uninstall_when_installed, "已安装时按键走卸载")
    return tester
