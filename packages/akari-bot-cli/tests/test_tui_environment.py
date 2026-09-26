"""环境页：托管方式、解释器、装了哪些包，以及三个环境动作。

环境是实例级信息，单独一页展示：页面上半是托管方式、解释器、core 版本与包数量，下半是包清单，
底部是「改用托管 venv / 改用系统解释器 / 重建实例 venv」。三个动作都会换掉实例正在用的解释器，
因此按模式只放出适用的那个，且实例运行期间一律拒绝。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.environment import EnvironmentPackage, EnvironmentState, StaticEnvironmentSource
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case

PACKAGES = (
    EnvironmentPackage("akari-bot-core", "0.1.0"),
    EnvironmentPackage("akari-bot-module-wiki", "0.2.0", editable=True),
    EnvironmentPackage("akari-bot-adapter-telegram", "0.1.0"),
)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticEnvironmentSource:
    params = {
        "state": EnvironmentState(
            mode="managed",
            python="/tmp/inst/.venv/bin/python",
            venv_dir="/tmp/inst/.venv",
            ready=True,
            packages=PACKAGES,
            core_version="0.1.0",
        )
    }
    params.update(kwargs)
    return StaticEnvironmentSource(**params)


async def _with_page(body, source=None, size=(120, 34)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"environment": chosen}, initial_page="environment", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("environment")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _shown(page) -> list[str]:
    return [kind for kind in ("adopt", "release", "recreate") if page.query_one(f"#{kind}", compat.Button).display]


async def _test_lists_installed_packages():
    # 页面要回答「环境里装了什么」：每个分发包一行，版本与可编辑标记都在。
    async def body(app, page, pilot, source):
        rows = page.rows
        fields = page.query_one("#fields", compat.Static).render()
        await pilot.press("q")
        return rows, str(fields)

    rows, fields = await _with_page(body)
    # 顺序即数据源给出的顺序（CLI 按分发名排序），页面不重排。
    return (
        rows
        == (
            "akari-bot-core 0.1.0",
            "akari-bot-module-wiki 0.2.0（可编辑）",
            "akari-bot-adapter-telegram 0.1.0",
        )
        and i18n.t("cli.tui.environment.package_count", count=3) in fields
        and i18n.t("cli.tui.environment.mode_managed", venv="/tmp/inst/.venv") in fields
    )


async def _test_search_narrows_packages():
    async def body(app, page, pilot, source):
        page.set_query("module")
        await pilot.pause()
        narrowed = page.rows
        page.set_query("")
        await pilot.pause()
        restored = len(page.rows)
        await pilot.press("q")
        return narrowed, restored

    narrowed, restored = await _with_page(body)
    return narrowed == ("akari-bot-module-wiki 0.2.0（可编辑）",) and restored == 3


async def _test_package_probe_failure_degrades():
    source = _source(state=EnvironmentState(mode="managed", python="/tmp/inst/.venv/bin/python", packages=None))

    async def body(app, page, pilot, source):
        rows = page.rows
        fields = str(page.query_one("#fields", compat.Static).render())
        await pilot.press("q")
        return rows, fields

    rows, fields = await _with_page(body, source)
    return rows == () and i18n.t("cli.tui.environment.probe_failed") in fields


async def _test_only_applicable_action_is_offered():
    async def body(app, page, pilot, source):
        shown = _shown(page)
        await pilot.press("q")
        return shown

    managed = await _with_page(body)
    external = await _with_page(
        body, _source(state=EnvironmentState(mode="external", python="/usr/bin/python3", ready=True, packages=()))
    )
    unknown = await _with_page(body, _source(state=EnvironmentState()))

    async def fields_body(app, page, pilot, source):
        text = str(page.query_one("#fields", compat.Static).render())
        await pilot.press("q")
        return text

    # 模式读不到时不能当成「外部解释器」展示：那会让人以为可以接管。
    text = await _with_page(fields_body, _source(state=EnvironmentState()))
    return (
        managed == ["release", "recreate"]
        and external == ["adopt"]
        and unknown == []
        and i18n.t("cli.tui.environment.mode_unknown") in text
    )


async def _test_action_needs_two_presses():
    async def body(app, page, pilot, source):
        page.request_action("recreate")
        await pilot.pause()
        first = list(source.actions), page.status_text
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return first, list(source.actions)

    first, second = await _with_page(body)
    return first[0] == [] and first[1] and second == ["recreate"]


async def _test_switching_action_asks_again():
    async def body(app, page, pilot, source):
        page.request_action("release")
        await pilot.pause()
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("release")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.actions)

    actions = await _with_page(body)
    return actions == []


async def _test_refused_while_running():
    source = _source(running=True)

    async def body(app, page, pilot, source):
        before = page.status_text
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.actions), page.status_text == before

    actions, untouched = await _with_page(body, source)
    return actions == [] and untouched


async def _test_inapplicable_action_refused():
    # 快捷键绕过隐藏也能按到，此时必须拒绝，而不是跑一个注定失败的命令。
    async def body(app, page, pilot, source):
        page.request_action("adopt")
        await pilot.pause()
        adopted = list(source.actions)
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return adopted, list(source.actions)

    adopted, rebuilt = await _with_page(body)
    return adopted == [] and rebuilt == ["recreate"]


async def _test_failure_reports_detail_and_reloads():
    source = _source(action_result=OperationResult(False, "重建失败", "boom"))

    async def body(app, page, pilot, source):
        before = source.calls["state"]
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        # 动作结束后会重新读取一次；后台任务注册有延迟，轮询到计数变化为止。
        deadline = time.monotonic() + 5.0
        while source.calls["state"] <= before and time.monotonic() < deadline:
            await pilot.pause()
        status = page.status_text
        after = source.calls["state"]
        await pilot.press("q")
        return status, after, before

    status, after, before = await _with_page(body, source)
    return "重建失败" in status and "boom" in status and after > before


@func_case
async def test_tui_environment(tester: Tester):
    """cli.tui.environment: 环境信息与环境动作测试"""
    _use_cli_locale()
    await tester.test(_test_lists_installed_packages, "列出环境里装了什么")
    await tester.test(_test_search_narrows_packages, "搜索收窄包清单")
    await tester.test(_test_package_probe_failure_degrades, "包列表探测失败只降级")
    await tester.test(_test_only_applicable_action_is_offered, "只显示当前托管方式适用的动作")
    await tester.test(_test_action_needs_two_presses, "环境动作需二次确认")
    await tester.test(_test_switching_action_asks_again, "换动作后重新确认且不执行")
    await tester.test(_test_refused_while_running, "实例运行中拒绝环境动作")
    await tester.test(_test_inapplicable_action_refused, "不适用的动作被拒绝")
    await tester.test(_test_failure_reports_detail_and_reloads, "失败时给出原因并重新读取")
    return tester
