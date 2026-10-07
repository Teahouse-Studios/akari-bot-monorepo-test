from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.testing import Tester, func_case


def _visible_in_box(screen, prefix):
    box = screen.query_one(f"#{prefix}-box")
    return screen.region.contains_region(box.region) and all(
        box.content_region.contains_region(button.region) for button in screen.query(compat.Button)
    )


async def _test_choice_buttons_fit_after_resize():
    app = compat.App()
    compat.install_akari_themes(app)
    results = []
    async with compat.app_test(app, size=(80, 24)) as pilot:
        compat.ask_choice(
            app,
            title="卸载模块",
            hint="目标配置与数据表：\n" + "需要确认的配置文件与数据表。" * 100,
            options=(
                ("keep", "保留数据卸载"),
                ("purge", "连数据一起清（--purge-data）"),
                ("cascade", "连同依赖一起卸载（--cascade）"),
            ),
            cancel_label="取消",
            callback=results.append,
        )
        for size in ((80, 24), (60, 20), (120, 40), (80, 24)):
            await pilot.resize_terminal(*size)
            await pilot.pause()
            if not _visible_in_box(app.screen, "choice"):
                return False
            description = app.screen.query_one("#choice-description")
            if description.max_scroll_y <= 0:
                return False
            description.focus()
            await pilot.press("end")
            await pilot.pause()
            if description.scroll_target_y <= 0:
                return False
        await pilot.click("#choice-cancel")
        await pilot.pause()
        return results == [None] and len(app.screen_stack) == 1


async def _test_short_choice_stays_compact():
    app = compat.App()
    async with compat.app_test(app, size=(80, 24)) as pilot:
        compat.ask_choice(app, title="确认", options=(("yes", "执行"),), cancel_label="取消", callback=lambda _: None)
        await pilot.pause()
        return _visible_in_box(app.screen, "choice") and app.screen.query_one("#choice-box").region.height < 12


async def _test_prompt_keeps_input_and_cancel_visible():
    app = compat.App()
    results = []
    async with compat.app_test(app, size=(60, 20)) as pilot:
        compat.ask_text(
            app,
            title="确认清理",
            hint="目标配置与数据表：\n" + "需要确认的配置文件与数据表。" * 100,
            confirm_label="清理并卸载",
            cancel_label="取消",
            callback=results.append,
        )
        for size in ((60, 20), (80, 24)):
            await pilot.resize_terminal(*size)
            await pilot.pause()
            screen = app.screen
            box = screen.query_one("#prompt-box")
            if not _visible_in_box(screen, "prompt") or not box.content_region.contains_region(
                screen.query_one("#prompt-input").region
            ):
                return False
        await pilot.press("a", "b", "c")
        if app.screen.query_one("#prompt-input", compat.Input).value != "abc":
            return False
        await pilot.click("#prompt-cancel")
        await pilot.pause()
        return results == [None]


@func_case
async def test_tui_dialogs(tester: Tester):
    i18n.t("cli.tui.common.status_ready")
    await tester.test(_test_choice_buttons_fit_after_resize, "长说明确认框缩放后选项与取消均可见")
    await tester.test(_test_short_choice_stays_compact, "简短确认框按内容收缩")
    await tester.test(_test_prompt_keeps_input_and_cancel_visible, "长说明输入框仍可输入和取消")
    return tester
