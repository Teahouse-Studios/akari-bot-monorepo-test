import asyncio

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.config import ConfigField, StaticConfigSource
from akaribot.cli.tui.database import ColumnInfo, StaticDatabaseSource, TableInfo
from akaribot.testing import Tester, func_case


async def _test_dirty_quit_keeps_or_discards():
    for key in ("q", "ctrl+q"):
        source = StaticConfigSource(("config",), {"config": (ConfigField("name", value="before"),)})
        app = TuiApp(sources={"config": source}, initial_page="config")
        async with compat.app_test(app, size=(80, 24)) as pilot:
            await pilot.pause()
            await app.page("config").wait_for_idle()
            await pilot.pause()
            page = app.page("config")
            page.row_for("name").set_text("edited")
            page.focus_primary()
            await pilot.press(key)
            await pilot.pause()
            if len(app.screen_stack) != 2 or page.dirty_note() not in app.screen.choice_hint:
                return False
            await pilot.press(key)
            await pilot.pause()
            if len(app.screen_stack) != 2:
                return False
            await pilot.click("#choice-cancel")
            await pilot.pause()
            if not app.is_running or page.row_for("name").text != "edited":
                return False
            await pilot.press(key)
            await pilot.pause()
            await pilot.click("#choice-0")
            await pilot.pause()
            if not app._exit:
                return False
    return True


async def _test_hidden_dirty_database_and_busy_quit():
    source = StaticDatabaseSource(
        (TableInfo("items", columns=(ColumnInfo("id", pk=True), ColumnInfo("value"))),),
        {"items": ({"id": "one", "value": "before"},)},
    )
    app = TuiApp(sources={"database": source}, initial_page="database")
    async with compat.app_test(app, size=(80, 24)) as pilot:
        await pilot.pause()
        await app.page("database").wait_for_idle()
        await pilot.pause()
        page = app.page("database")
        page.set_editor_value("value", "edited")
        app.show_page("misc")
        app.run_worker(asyncio.sleep(30), group="test-background")
        await pilot.pause()
        await pilot.press("ctrl+q")
        await pilot.pause()
        hint = app.screen.choice_hint
        if not page.dirty_note() or page.dirty_note() not in hint or "test-background" not in hint:
            return False
        await pilot.press("escape")
        await pilot.pause()
        return app.is_running and page.editor_values()["value"] == "edited" and source.writes == []


async def _test_clean_quit_has_no_dialog():
    app = TuiApp(initial_page="misc")
    async with compat.app_test(app, size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("ctrl+q")
        return app._exit and len(app.screen_stack) == 1


async def _test_cancel_quit_restores_edit_focus():
    source = StaticConfigSource(("config",), {"config": (ConfigField("name", value="before"),)})
    app = TuiApp(sources={"config": source}, initial_page="config")
    async with compat.app_test(app, size=(80, 24)) as pilot:
        await pilot.pause()
        page = app.page("config")
        await page.wait_for_idle()
        await pilot.pause()
        row = page.row_for("name")
        row.set_text("edited")
        editor = row.query_one(compat.Input)
        editor.focus()
        await pilot.pause()
        await pilot.press("ctrl+q")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        return app.focused is editor and row.text == "edited" and app.is_running


@func_case
async def test_tui_quit(tester: Tester):
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")
    await tester.test(_test_dirty_quit_keeps_or_discards, "退出确认保护配置编辑且连发不叠框")
    await tester.test(_test_hidden_dirty_database_and_busy_quit, "退出同时提示隐藏页数据库编辑和后台任务")
    await tester.test(_test_clean_quit_has_no_dialog, "无未保存内容和任务时直接退出")
    await tester.test(_test_cancel_quit_restores_edit_focus, "取消退出恢复字段输入焦点")
    return tester
