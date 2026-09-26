"""杂项页：只放不属于其它页面的一次性操作，目前是「迁移项目」。

页面平时只有一个按钮，点击后弹出输入框要旧项目路径；拿到路径后再按一次才执行——旧目录只读，
但迁移会往实例里写配置与数据。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.misc import StaticMiscSource
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


async def _with_page(body, source=None, size=(100, 30)):
    chosen = source if source is not None else StaticMiscSource()
    app = TuiApp(sources={"misc": chosen}, initial_page="misc", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("misc")
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _test_page_offers_one_button():
    # 页面只放一个按钮，不常驻输入框。
    async def body(app, page, pilot, source):
        buttons = [child.id for child in page.query(compat.Button)]
        inputs = len(page.query(compat.Input))
        await pilot.press("q")
        return buttons, inputs

    buttons, inputs = await _with_page(body)
    return buttons == ["migrate"] and inputs == 0


async def _test_click_opens_prompt_and_cancel_is_safe():
    # 点击后弹出输入框；取消不会调用数据源。
    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        closed = len(app.screen_stack) == 1
        status = page.status_text
        await pilot.press("q")
        return opened, closed, status, list(source.migrated)

    opened, closed, status, migrated = await _with_page(body)
    return opened and closed and migrated == [] and status


async def _test_prompt_asks_before_migrating():
    # 输入路径后不立即执行：状态栏先问一次，再按一次 m 才迁移。
    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        # 输入框在模态屏幕上，不在页面子树里。
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/old-project"
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        asked = (list(source.migrated), page.status_text, page.pending_project)
        page.request_migrate()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, list(source.migrated)

    asked, migrated = await _with_page(body)
    return asked[0] == [] and asked[1] and asked[2] == "/tmp/old-project" and migrated == ["/tmp/old-project"]


async def _test_enter_key_submits_prompt():
    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/other"
        await pilot.press("enter")
        await pilot.pause()
        pending = page.pending_project
        await pilot.press("q")
        return pending

    pending = await _with_page(body)
    return pending == "/tmp/other"


async def _test_failure_keeps_page_usable():
    source = StaticMiscSource(OperationResult(False, "迁移失败", "boom"))

    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/old"
        await pilot.press("enter")
        await pilot.pause()
        page.request_migrate()
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        page.request_migrate()
        await pilot.pause()
        reopened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.press("q")
        return status, reopened, list(source.migrated)

    status, reopened, migrated = await _with_page(body, source)
    return "迁移失败" in status and "boom" in status and reopened and migrated == ["/tmp/old"]


@func_case
async def test_tui_misc(tester: Tester):
    """cli.tui.misc: 迁移项目的按钮与输入框测试"""
    _use_cli_locale()
    await tester.test(_test_page_offers_one_button, "页面只放一个按钮")
    await tester.test(_test_click_opens_prompt_and_cancel_is_safe, "点击弹出输入框且取消安全")
    await tester.test(_test_prompt_asks_before_migrating, "输入路径后仍需确认")
    await tester.test(_test_enter_key_submits_prompt, "回车提交输入框")
    await tester.test(_test_failure_keeps_page_usable, "迁移失败后界面仍可用")
    return tester
