"""概览页：运行状态与环境（venv）状态、环境动作。

概览页是实例级状态的入口：除运行状态与版本外，还展示环境托管状态，并提供接管 / 解除接管 / 重建
三个动作。动作都要二次确认，且经 CLI 执行，界面不直接改环境。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dashboard import StaticDashboardSource, VenvState
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticDashboardSource:
    params = {
        "venv": VenvState(
            mode="managed",
            python="/tmp/inst/.venv/bin/python",
            venv_dir="/tmp/inst/.venv",
            ready=True,
            packages=44,
            core_version="0.1.0",
        )
    }
    params.update(kwargs)
    return StaticDashboardSource(**params)


async def _with_page(body, source=None, size=(120, 34)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"dashboard": chosen}, initial_page="dashboard", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("dashboard")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _venv_row(page) -> tuple[str, str]:
    return next(row for row in page.rows if row[0] == i18n.t("cli.tui.dashboard.field_venv"))


async def _test_venv_row_shows_state():
    # 环境状态来自 `venv status --json`，概览页把它与运行状态并列展示。
    async def body(app, page, pilot, source):
        row = _venv_row(page)
        await pilot.press("q")
        return row, source.calls["venv"]

    row, calls = await _with_page(body)
    return row[0] == i18n.t("cli.tui.dashboard.field_venv") and "44" in row[1] and calls >= 1


async def _test_venv_row_reports_missing_interpreter():
    source = _source(venv=VenvState(mode="managed", python="/tmp/inst/.venv/bin/python", ready=False))

    async def body(app, page, pilot, source):
        await pilot.press("q")
        return _venv_row(page)[1]

    text = await _with_page(body, source)
    return i18n.t("cli.tui.dashboard.venv_missing").split("${")[0].strip() in text


async def _test_venv_failure_only_degrades_row():
    source = _source(venv=VenvState(error="boom"))

    async def body(app, page, pilot, source):
        await pilot.press("q")
        return _venv_row(page)[1]

    text = await _with_page(body, source)
    return "boom" in text


async def _test_venv_action_needs_two_presses():
    async def body(app, page, pilot, source):
        page.request_venv_action("adopt")
        await pilot.pause()
        first = list(source.venv_actions), page.status_text
        page.request_venv_action("adopt")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return first, list(source.venv_actions)

    first, second = await _with_page(body)
    return first[0] == [] and first[1] and second == ["adopt"]


async def _test_venv_action_switches_on_other_action():
    # 同一位置连按两次才执行；中间换过动作就重新询问，不执行任何一项。
    async def body(app, page, pilot, source):
        page.request_venv_action("adopt")
        await pilot.pause()
        page.request_venv_action("recreate")
        await pilot.pause()
        page.request_venv_action("adopt")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.venv_actions)

    actions = await _with_page(body)
    return actions == []


async def _test_venv_action_failure_keeps_page_usable():
    source = _source(venv_result=OperationResult(False, "重建失败", "boom"))

    async def body(app, page, pilot, source):
        page.request_venv_action("recreate")
        await pilot.pause()
        page.request_venv_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        page.request_venv_action("release")
        await pilot.pause()
        pending = page.status_text
        await pilot.press("q")
        return status, pending, list(source.venv_actions)

    status, pending, actions = await _with_page(body, source)
    return actions == ["recreate"] and pending != status


async def _test_recreate_refreshes_state():
    async def body(app, page, pilot, source):
        before = source.calls["venv"]
        page.request_venv_action("recreate")
        await pilot.pause()
        page.request_venv_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return before, source.calls["venv"]

    before, after = await _with_page(body)
    return after > before


async def _test_migrate_requires_path_and_confirmation():
    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        empty = list(source.migrated)
        page.query_one("#legacy-path", compat.Input).value = "/tmp/old-project"
        await pilot.pause()
        page.request_migrate()
        await pilot.pause()
        first = list(source.migrated), page.status_text
        page.request_migrate()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return empty, first, list(source.migrated)

    empty, first, second = await _with_page(body)
    return empty == [] and first[0] == [] and first[1] and second == ["/tmp/old-project"]


async def _test_migrate_new_path_asks_again():
    # 换了路径就重新询问，避免把确认用在另一个项目上。
    async def body(app, page, pilot, source):
        page.query_one("#legacy-path", compat.Input).value = "/tmp/one"
        await pilot.pause()
        page.request_migrate()
        await pilot.pause()
        page.query_one("#legacy-path", compat.Input).value = "/tmp/two"
        await pilot.pause()
        page.request_migrate()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.migrated)

    migrated = await _with_page(body)
    return migrated == []


@func_case
async def test_tui_dashboard(tester: Tester):
    """cli.tui.dashboard: 环境状态与环境动作测试"""
    _use_cli_locale()
    await tester.test(_test_venv_row_shows_state, "概览展示环境托管状态")
    await tester.test(_test_venv_row_reports_missing_interpreter, "解释器缺失时如实说明")
    await tester.test(_test_venv_failure_only_degrades_row, "环境状态读取失败只降级该行")
    await tester.test(_test_venv_action_needs_two_presses, "环境动作需二次确认")
    await tester.test(_test_venv_action_switches_on_other_action, "换动作后重新确认且不执行")
    await tester.test(_test_venv_action_failure_keeps_page_usable, "环境动作失败后界面仍可用")
    await tester.test(_test_recreate_refreshes_state, "环境动作后重新读取状态")
    await tester.test(_test_migrate_requires_path_and_confirmation, "迁移需填路径并二次确认")
    await tester.test(_test_migrate_new_path_asks_again, "换路径后重新确认迁移")
    return tester
