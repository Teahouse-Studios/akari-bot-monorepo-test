"""日志页：进程计数、贴底跟随与关键词过滤。

进程行括号里的数字是「该进程有多少个日志文件」，它是判断日志是否轮转过的依据，因此必须与当前
过滤无关：选中某个进程后，其余进程的计数不能跟着变，否则看上去像在随机跳动。
跟随只在视口贴底时滚动，用户上滚即暂停；关键词过滤只作用于显示缓冲，不改 offset，也不打断跟随。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.logs import LogsPage, StaticLogSource
from akaribot.testing import Tester, func_case

FILES = {
    "BotDaemon_2026-09-24.log": ["a1", "a2"],
    "BotDaemon_2026-09-25.log": ["b1"],
    "BotDaemon_debug_2026-09-25.log": ["d1"],
    "Server_2026-09-25.log": ["s1", "s2", "s3"],
    "Server_debug_2026-09-25.log": ["s4"],
}

LONG_FILE = "BotDaemon_2026-09-25.log"
LONG_LINES = {LONG_FILE: [f"line {index:03d}" for index in range(60)]}

FILTER_LINES = {LONG_FILE: ["boot ok", "ERROR disk full", "warn low memory", "error retry", "boot done"]}


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticLogSource:
    params = {"files": FILES}
    params.update(kwargs)
    return StaticLogSource(**params)


async def _with_page(body, source=None, size=(110, 32)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"logs": chosen}, initial_page="logs", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("logs")
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _labels(page) -> tuple[str, ...]:
    return page.process_labels()


async def _test_counts_are_file_counts():
    # 括号里的数字是该进程的日志文件数，「全部进程」是总数。
    async def body(app, page, pilot, source):
        labels = _labels(page)
        await pilot.press("q")
        return labels

    labels = await _with_page(body)
    return (
        i18n.t("cli.tui.logs.process_item", name=i18n.t("cli.tui.logs.all_processes"), count=5) in labels
        and i18n.t("cli.tui.logs.process_item", name="BotDaemon", count=3) in labels
        and i18n.t("cli.tui.logs.process_item", name="Server", count=2) in labels
    )


async def _test_counts_survive_process_filter():
    # 关键回归：切换进程过滤后，各进程的计数必须与过滤无关。
    async def body(app, page, pilot, source):
        before = _labels(page)
        for process in ("BotDaemon", "Server", None):
            page.select_process(process)
            await pilot.pause()
            if _labels(page) != before:
                await pilot.press("q")
                return before, _labels(page)
        await pilot.press("q")
        return before, before

    before, after = await _with_page(body)
    return before == after and len(before) == 3


async def _test_filter_keeps_following_in_that_process():
    # 过滤只影响可见文件与跟随目标，不影响计数。
    async def body(app, page, pilot, source):
        page.select_process("Server")
        await pilot.pause()
        followed = page.followed_file
        await pilot.press("q")
        return followed.name, followed.process, len(page.files)

    name, process, visible = await _with_page(body)
    return process == "Server" and name.startswith("Server") and visible == 2


async def _test_rescan_picks_up_new_file():
    # 重新枚举后计数跟着目录走：新一天的文件出现，计数加一。
    async def body(app, page, pilot, source):
        before = _labels(page)
        source.append("Server_2026-09-26.log", "s5")
        page.action_rescan()
        await pilot.pause()
        after = _labels(page)
        await pilot.press("q")
        return before, after

    before, after = await _with_page(body)
    return (
        i18n.t("cli.tui.logs.process_item", name="Server", count=2) in before
        and i18n.t("cli.tui.logs.process_item", name="Server", count=3) in after
        and i18n.t("cli.tui.logs.process_item", name=i18n.t("cli.tui.logs.all_processes"), count=6) in after
    )


async def _test_scroll_back_is_not_yanked_to_end():
    # 上滚后跟随周期不得把视口拽回底部；上滚即暂停，恢复后重新贴底。
    async def body(app, page, pilot, source):
        pane = page.query_one("#log-pane", compat.VerticalScroll)
        await pilot.pause()
        pinned = pane.is_vertical_scroll_end
        pane.scroll_home(animate=False)
        await pilot.pause()
        detached = not pane.is_vertical_scroll_end
        source.append(LONG_FILE, "line 060")
        page.follow_once()
        await pilot.pause()
        kept = pane.scroll_offset.y == 0 and page.visible_text.endswith("line 060")
        page._tick()
        await pilot.pause()
        paused = page.paused
        hint = i18n.t("cli.tui.logs.status_resume_hint") in page.status_text
        page.toggle_pause()
        await pilot.pause()
        back = pane.is_vertical_scroll_end
        await pilot.press("q")
        return pinned, detached, kept, paused, hint, back

    pinned, detached, kept, paused, hint, back = await _with_page(body, source=_source(files=LONG_LINES))
    return pinned and detached and kept and paused and hint and back


async def _test_keyword_filter_limits_display_only():
    # 过滤只改显示：缓冲、offset 与跟随都不动，命中行数进状态栏，Esc 清空后恢复全文。
    async def body(app, page, pilot, source):
        await pilot.press("slash")
        await pilot.pause()
        focused = page.query_one("#filter", compat.Input).has_focus
        before_offset = page.read_offset
        before_lines = page.buffer_lines
        page.set_filter("error")
        await pilot.pause()
        shown = page.visible_text
        hits = page.filter_hits
        offset_kept = page.read_offset == before_offset
        buffer_kept = page.buffer_lines == before_lines
        counted = i18n.t("cli.tui.logs.status_filter", keyword="error", hits=2) in page.status_text
        source.append(LONG_FILE, "error again")
        page.follow_once()
        await pilot.pause()
        followed = page.visible_text.endswith("error again") and page.read_offset > before_offset
        await pilot.press("escape")
        await pilot.pause()
        cleared = page.filter_keyword == "" and len(page.visible_text.split("\n")) == len(page.buffer_lines)
        await pilot.press("q")
        return focused, shown, hits, offset_kept, buffer_kept, counted, followed, cleared

    focused, shown, hits, offset_kept, buffer_kept, counted, followed, cleared = await _with_page(
        body, source=_source(files=FILTER_LINES)
    )
    return (
        focused
        and shown == "ERROR disk full\nerror retry"
        and hits == 2
        and offset_kept
        and buffer_kept
        and counted
        and followed
        and cleared
    )


async def _test_low_frequency_bindings_stay_out_of_footer():
    hidden = {binding.key for binding in LogsPage.BINDINGS if not binding.show}
    shown = {binding.key for binding in LogsPage.BINDINGS if binding.show}
    return {"d", "r", "escape"} <= hidden and {"space", "c", "slash"} <= shown


@func_case
async def test_tui_logs(tester: Tester):
    """cli.tui.logs: 进程计数、贴底跟随与关键词过滤测试"""
    _use_cli_locale()
    await tester.test(_test_counts_are_file_counts, "计数是各进程的日志文件数")
    await tester.test(_test_counts_survive_process_filter, "切换过滤后计数不变")
    await tester.test(_test_filter_keeps_following_in_that_process, "过滤只影响可见文件与跟随目标")
    await tester.test(_test_rescan_picks_up_new_file, "重新枚举后计数随目录更新")
    await tester.test(_test_scroll_back_is_not_yanked_to_end, "上滚后不被跟随拽回底部，上滚即暂停")
    await tester.test(_test_keyword_filter_limits_display_only, "关键词过滤只改显示并报出命中行数")
    await tester.test(_test_low_frequency_bindings_stay_out_of_footer, "低频键位不进页脚")
    return tester
