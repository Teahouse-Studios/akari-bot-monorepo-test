"""概览页：实例信息与运行状态。

环境信息与环境动作已移到「环境」页、旧项目迁移移到「杂项」页，本页只留实例本身：根目录、名称、
语言、core 版本与来源、运行状态与判据、更新提示。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dashboard import DashboardSnapshot, StaticDashboardSource
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


async def _with_page(body, source=None, size=(110, 32)):
    chosen = source if source is not None else StaticDashboardSource(SNAPSHOT, running=True)
    app = TuiApp(sources={"dashboard": chosen}, initial_page="dashboard", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("dashboard")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _fields(page) -> dict[str, str]:
    return dict(page.rows)


async def _test_fields_show_instance_facts():
    async def body(app, page, pilot, source):
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
    async def body(app, page, pilot, source):
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
    async def body(app, page, pilot, source):
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

    async def body(app, page, pilot, source):
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body, Failing())
    return "boom" in status


@func_case
async def test_tui_dashboard(tester: Tester):
    """cli.tui.dashboard: 实例信息与运行状态测试"""
    _use_cli_locale()
    await tester.test(_test_fields_show_instance_facts, "展示实例根、名称与版本")
    await tester.test(_test_state_follows_probe, "运行状态跟着探测结果")
    await tester.test(_test_refresh_rereads_snapshot, "刷新重新读取快照")
    await tester.test(_test_load_failure_degrades_to_status, "读取失败只降级到状态栏")
    return tester
