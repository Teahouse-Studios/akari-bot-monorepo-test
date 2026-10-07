import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.run import StaticRunSource
from akaribot.testing import Tester, func_case


async def _test_run_buttons_remain_visible_after_resize():
    source = StaticRunSource()
    app = TuiApp(sources={"run": source}, initial_page="run", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(120, 40)) as pilot:
        page = app.page("run")
        await page.wait_for_idle()
        for width, height in ((80, 24), (60, 20), (100, 30), (120, 40)):
            await pilot.resize_terminal(width, height)
            await pilot.pause()
            buttons = tuple(page.query("#actions Button"))
            if len(buttons) != 6 or any(not page.region.contains_region(button.region) for button in buttons):
                return False
            if page.query_one("#table-pane", compat.VerticalScroll).content_region.height < 3:
                return False
            if width == 60 and len({button.region.y for button in buttons}) < 2:
                return False
            if width == 60:
                before = source.calls["status"]
                await pilot.click(page.query_one("#refresh", compat.Button), offset=(2, 1))
                await pilot.pause()
                await page.wait_for_idle()
                if source.calls["status"] <= before:
                    return False
        return True


@func_case
async def test_tui_run_layout(tester: Tester):
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")
    await tester.test(_test_run_buttons_remain_visible_after_resize, "终端缩放后运行页按钮可见且可点击")
    return tester
