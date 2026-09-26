"""日志页：进程清单的计数与过滤。

进程行括号里的数字是「该进程有多少个日志文件」，它是判断日志是否轮转过的依据，因此必须与当前
过滤无关：选中某个进程后，其余进程的计数不能跟着变，否则看上去像在随机跳动。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.logs import StaticLogSource
from akaribot.testing import Tester, func_case

FILES = {
    "BotDaemon_2026-09-24.log": ["a1", "a2"],
    "BotDaemon_2026-09-25.log": ["b1"],
    "BotDaemon_debug_2026-09-25.log": ["d1"],
    "Server_2026-09-25.log": ["s1", "s2", "s3"],
    "Server_debug_2026-09-25.log": ["s4"],
}


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


@func_case
async def test_tui_logs(tester: Tester):
    """cli.tui.logs: 进程计数与过滤测试"""
    _use_cli_locale()
    await tester.test(_test_counts_are_file_counts, "计数是各进程的日志文件数")
    await tester.test(_test_counts_survive_process_filter, "切换过滤后计数不变")
    await tester.test(_test_filter_keeps_following_in_that_process, "过滤只影响可见文件与跟随目标")
    await tester.test(_test_rescan_picks_up_new_file, "重新枚举后计数随目录更新")
    return tester
