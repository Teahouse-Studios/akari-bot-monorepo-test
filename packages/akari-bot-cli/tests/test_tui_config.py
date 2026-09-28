"""配置页：编辑未保存时的拦截。

表单行与原始文本都只改控件、不落盘；换表、重读、切模式与强制刷新都会重建编辑区，故这些路径
必须先问一次「放弃未保存的改动？」，选择保留则动作不执行且编辑仍在。
"""

import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.config import (
    KIND_BOOL,
    KIND_INT,
    KIND_LIST,
    MODE_FORM,
    MODE_RAW,
    ConfigField,
    ConfigPage,
    StaticConfigSource,
)
from akaribot.testing import Tester, func_case

FIELDS = {
    "config": (
        ConfigField(key="count", table="config", kind=KIND_INT, value=3),
        ConfigField(key="enable", table="config", kind=KIND_BOOL, value=True),
    ),
    "module_wiki": (
        ConfigField(key="prefixes", table="module_wiki", kind=KIND_LIST, value=["wiki", "维基"]),
        ConfigField(key="enable", table="module_wiki", kind=KIND_BOOL, value=False),
    ),
    # 没有字段的表用于核对表单区提示的读取路径。
    "empty_table": (),
}
RAW = {
    "config": "[config]\ncount = 3\nenable = true\n",
    "module_wiki": '[module_wiki]\nprefixes = ["wiki", "维基"]\nenable = false\n',
    "empty_table": "",
}


def _source() -> StaticConfigSource:
    return StaticConfigSource(tables=("config", "module_wiki", "empty_table"), fields=FIELDS, raw=RAW)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _screen_title(app: TuiApp) -> str:
    # 模态框自己记着标题，不必经渲染层取文本。
    return str(getattr(app.screen, "choice_title", ""))


async def _with_page(body, source=None, size=(110, 32)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"config": chosen}, initial_page="config", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("config")
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _test_dirty_note_tracks_edits():
    # 未编辑时不说有改动；改过之后说明里带上表名。
    async def body(app, page, pilot, source):
        clean = (page.is_dirty(), page.dirty_note())
        page.row_for("count").set_text("9")
        await pilot.pause()
        dirty = (page.is_dirty(), page.dirty_note())
        expected = i18n.t("cli.tui.config.dirty_note", table="config")
        await pilot.press("q")
        return clean, dirty, expected

    clean, dirty, expected = await _with_page(body)
    return clean == (False, "") and dirty[0] is True and dirty[1] == expected


async def _test_table_switch_keeps_edits():
    # 选择保留改动时：动作不执行、表不变、编辑仍在、列表高亮拨回当前表。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        table_list = page.query_one("#table-list", compat.ListView)
        table_list.index = 1
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        title = _screen_title(app)
        await pilot.press("escape")
        await pilot.pause()
        kept = (
            page.selected_table,
            page.row_for("count").text,
            page.is_dirty(),
            compat.highlighted_index(table_list),
        )
        await pilot.press("q")
        return opened, title, kept

    opened, title, kept = await _with_page(body)
    return opened and title == i18n.t("cli.tui.config.dirty_title") and kept == ("config", "9", True, 0)


async def _test_table_switch_discards_edits():
    # 选择放弃改动时：切到新表，旧编辑随表单重建消失。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        table_list = page.query_one("#table-list", compat.ListView)
        table_list.index = 1
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        table = page.selected_table
        fields = sorted(row.field.key for row in page.field_rows())
        dirty = page.is_dirty()
        await pilot.press("q")
        return table, fields, dirty

    table, fields, dirty = await _with_page(body)
    return table == "module_wiki" and fields == ["enable", "prefixes"] and dirty is False


async def _test_reload_asks_before_rereading():
    # ctrl+r 重读先问：保留则不取数，放弃才重读并退回载入值。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        before = dict(source.calls)
        page.action_reload()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        kept = (dict(source.calls) == before, page.is_dirty())
        page.action_reload()
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        text = page.row_for("count").text
        await pilot.press("q")
        return opened, kept, dict(source.calls), text

    opened, kept, calls, text = await _with_page(body)
    return opened and kept == (True, True) and calls["list"] > 0 and calls["schema"] > 0 and text == "3"


async def _test_forced_refresh_asks():
    # force=True 的刷新路径同样重建编辑区，不能绕过询问。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        before = dict(source.calls)
        page.refresh_tables(force=True)
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        untouched = dict(source.calls) == before
        text = page.row_for("count").text
        await pilot.press("q")
        return opened, untouched, text

    opened, untouched, text = await _with_page(body)
    return opened and untouched and text == "9"


async def _test_mode_switch_asks_before_switching():
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        page.action_mode_raw()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        kept = (page.mode, page.is_dirty())
        page.action_mode_raw()
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        switched = (page.mode, page.row_for("count").text)
        await pilot.press("q")
        return opened, kept, switched

    opened, kept, switched = await _with_page(body)
    return opened and kept == (MODE_FORM, True) and switched == (MODE_RAW, "3")


async def _test_raw_edits_count_as_dirty():
    # 原始文本模式的编辑同样算脏值，说明里仍带当前表名。
    async def body(app, page, pilot, source):
        await page.set_mode(MODE_RAW)
        await pilot.pause()
        loaded = page.is_dirty()
        await page.raw_editor().load_text(RAW["config"] + "count = 9\n")
        await pilot.pause()
        dirty = page.is_dirty()
        note = page.dirty_note()
        await pilot.press("q")
        return loaded, dirty, note

    loaded, dirty, note = await _with_page(body)
    return loaded is False and dirty is True and note == i18n.t("cli.tui.config.dirty_note", table="config")


async def _test_form_hint_reads_widget_text():
    # 没有字段的表在表单区留一句提示，读取路径要能拿到它的纯文本。
    async def body(app, page, pilot, source):
        page.query_one("#table-list", compat.ListView).index = 2
        await page.wait_for_idle()
        await pilot.pause()
        hint = page.form_hint()
        await pilot.press("q")
        return hint

    hint = await _with_page(body)
    return hint == i18n.t("cli.tui.config.hint_table_empty")


async def _test_low_frequency_bindings_stay_out_of_footer():
    # 工具条上都有按钮的动作不进页脚，80 列下才能容纳全局键位。
    async def body(app, page, pilot, source):
        footer = app.query_one(compat.Footer)
        actions = {"save", "mode_form", "mode_raw", "reload", "focus_tables"}
        keys = [child for child in footer.children if getattr(child, "action", "") in actions]
        width = sum(compat.widget_cells(child)[0] for child in keys)
        await pilot.press("q")
        return len(keys), width

    count, width = await _with_page(body, size=(80, 24))
    visible = tuple(binding.key for binding in ConfigPage.BINDINGS if binding.show)
    hidden = tuple(binding.key for binding in ConfigPage.BINDINGS if not binding.show)
    return count == 1 and width <= 80 and visible == ("s",) and hidden == ("f", "t", "ctrl+r", "escape")


@func_case
async def test_tui_config(tester: Tester):
    """cli.tui.config: 未保存改动的拦截测试"""
    _use_cli_locale()
    # 确认原语在 _compat 里共用；用例里的两次按键几乎同时发生，统一压缩防抖窗口。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_dirty_note_tracks_edits, "脏值说明随编辑出现")
        await tester.test(_test_table_switch_keeps_edits, "换表选择保留则不切换")
        await tester.test(_test_table_switch_discards_edits, "换表选择放弃才切换")
        await tester.test(_test_reload_asks_before_rereading, "重读前先问")
        await tester.test(_test_forced_refresh_asks, "强制刷新前先问")
        await tester.test(_test_mode_switch_asks_before_switching, "切模式前先问")
        await tester.test(_test_raw_edits_count_as_dirty, "原始文本的编辑也算脏值")
        await tester.test(_test_form_hint_reads_widget_text, "表单区提示可按纯文本读回")
        await tester.test(_test_low_frequency_bindings_stay_out_of_footer, "低频键位不进页脚")
    return tester
