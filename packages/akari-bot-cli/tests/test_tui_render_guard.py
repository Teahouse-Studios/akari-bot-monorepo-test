"""渲染守卫的契约：页面不可用时跳过并记账，页面可用时选择器错误照常抛出。

守卫在页面构造时统一包装 `_render*` / `_sync*` / `_set_*` / `_paint*`：页面卸载后落地的取数与
轮询没有可写的控件，跳过并记进 `RenderGuard`；页面仍在运行时的 `NoMatches` 原样上抛，否则
worker 表面成功、页面只保留旧内容。用例用真实 `TuiApp` 与替身数据源，只给页面类补探针方法。
"""

import asyncio
import logging
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.modules import ModuleRecord, ModulesPage, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORD = ModuleRecord(name="coin", dist="akari-bot-module-coin", version="0.1.0", state="installed")
MISSING_SELECTOR = "#tui-render-guard-missing"
LOGGER_NAME = "akaribot.cli.tui._compat"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _render_guard_probe(self: ModulesPage) -> None:
    self.query_one(MISSING_SELECTOR, compat.Static)


def _render_guard_race_probe(self: ModulesPage) -> None:
    # 进入时页面可用、抛错时已被卸下：模拟取数落地那一刻的卸载竞态。
    self._tui_mounted_once = True
    self._is_mounted = False
    self.query_one(MISSING_SELECTOR, compat.Static)


def _sync_guard_probe(self: ModulesPage) -> str:
    return "sync"


def _set_guard_probe(self: ModulesPage) -> str:
    return "set"


def _paint_guard_probe(self: ModulesPage) -> str:
    return "paint"


def _on_tick_guard_probe(self: ModulesPage) -> str:
    return "tick"


def public_guard_probe(self: ModulesPage) -> str:
    return "public"


PROBE_METHODS = {
    "_render_guard_probe": _render_guard_probe,
    "_render_guard_race_probe": _render_guard_race_probe,
    "_sync_guard_probe": _sync_guard_probe,
    "_set_guard_probe": _set_guard_probe,
    "_paint_guard_probe": _paint_guard_probe,
    "_on_tick_guard_probe": _on_tick_guard_probe,
    "public_guard_probe": public_guard_probe,
}


async def _with_app(body, *, initial_page: str = "modules", size: tuple[int, int] = (100, 30)):
    app = TuiApp(
        source=StaticModuleSource([RECORD]),
        initial_page=initial_page,
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=size) as pilot:
        await pilot.pause()
        await asyncio.sleep(0.3)
        return await body(app, pilot)


async def _test_active_page_selector_error_raises():
    async def body(app, pilot):
        page = app.page("modules")
        state = (compat.mounted(page), page.is_mounted, app.is_running)
        raised = ""
        try:
            page._render_guard_probe()
        except compat.NoMatches:
            raised = "NoMatches"
        skipped = page.render_guard.skipped_renders
        await pilot.press("q")
        return state, raised, skipped

    state, raised, skipped = await _with_app(body)
    return state == (True, True, True) and raised == "NoMatches" and skipped == 0


async def _test_wrapped_renders_run_when_available():
    async def body(app, pilot):
        page = app.page("modules")
        values = (
            page._sync_guard_probe(),
            page._set_guard_probe(),
            page._paint_guard_probe(),
            page.public_guard_probe(),
            page._on_tick_guard_probe(),
        )
        await pilot.press("q")
        return values, page.render_guard.skipped_renders

    values, skipped = await _with_app(body)
    return values == ("sync", "set", "paint", "public", "tick") and skipped == 0


async def _test_guard_wraps_only_render_entry_prefixes():
    async def body(app, pilot):
        page = app.page("modules")
        overridden = set(page.__dict__)
        await pilot.press("q")
        return overridden

    overridden = await _with_app(body)
    wrapped = {
        "_render_guard_probe",
        "_render_guard_race_probe",
        "_sync_guard_probe",
        "_set_guard_probe",
        "_paint_guard_probe",
    }
    untouched = {"_on_tick_guard_probe", "public_guard_probe"}
    return wrapped <= overridden and not untouched & overridden


async def _test_exited_app_skips_and_counts():
    async def body(app, pilot):
        page = app.page("modules")
        # 与 mounted() 的判据一致：应用已请求退出后页面不再可用；不经 app.exit() 以免终止本次运行。
        app._exit = True
        values = (
            page._render_guard_probe(),
            page._sync_guard_probe(),
            page.public_guard_probe(),
            page._on_tick_guard_probe(),
        )
        app._exit = False
        skipped = page.render_guard.skipped_renders
        last = page.render_guard.last_skipped_method
        await pilot.press("q")
        return values, skipped, last

    values, skipped, last = await _with_app(body)
    return values == (None, None, "public", "tick") and skipped == 2 and last == "_sync_guard_probe"


async def _test_detached_page_skips_and_counts():
    async def body(app, pilot):
        page = app.page("modules")
        # 卸载竞态：Textual 的消息处理器按类的 MRO 查找，实例级 on_mount 不会被派发，故直接置成
        # 页面挂载过又被卸下的状态，事后恢复以免影响本次运行的收尾。
        page._tui_mounted_once = True
        page._is_mounted = False
        available = compat.mounted(page)
        value = page._sync_guard_probe()
        skipped = page.render_guard.skipped_renders
        last = page.render_guard.last_skipped_method
        page._tui_mounted_once = False
        page._is_mounted = True
        await pilot.press("q")
        return available, value, skipped, last

    available, value, skipped, last = await _with_app(body)
    return available is False and value is None and skipped == 1 and last == "_sync_guard_probe"


async def _test_removing_or_stopped_page_skips_and_counts():
    async def body(app, pilot):
        page = app.page("modules")
        # 界面仍在运行时切实例重挂载：旧页进入移除流程，子控件正在被卸下。
        page._pruning = True
        while_removing = compat.mounted(page)
        value = page._sync_guard_probe()
        page._pruning = False
        # 退出流程里应用已停止运行但尚未请求退出，子控件先一步被卸下。
        app._running = False
        stopped = compat.mounted(page)
        second = page._sync_guard_probe()
        app._running = True
        skipped = page.render_guard.skipped_renders
        last = page.render_guard.last_skipped_method
        await pilot.press("q")
        return while_removing, value, stopped, second, skipped, last

    while_removing, value, stopped, second, skipped, last = await _with_app(body)
    return (
        while_removing is False
        and value is None
        and stopped is False
        and second is None
        and skipped == 2
        and last == "_sync_guard_probe"
    )


async def _test_race_no_matches_is_skipped():
    async def body(app, pilot):
        page = app.page("modules")
        value = page._render_guard_race_probe()
        skipped = page.render_guard.skipped_renders
        last = page.render_guard.last_skipped_method
        page._tui_mounted_once = False
        page._is_mounted = True
        await pilot.press("q")
        return value, skipped, last

    value, skipped, last = await _with_app(body)
    return value is None and skipped == 1 and last == "_render_guard_race_probe"


async def _test_skip_logs_at_debug_level():
    records: list[logging.LogRecord] = []

    class _Collect(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    logger = logging.getLogger(LOGGER_NAME)
    handler = _Collect()
    previous = logger.level
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:

        async def body(app, pilot):
            page = app.page("modules")
            app._exit = True
            page._sync_guard_probe()
            app._exit = False
            await pilot.press("q")
            return page.render_guard.last_skipped_method

        last = await _with_app(body)
    finally:
        logger.setLevel(previous)
        logger.removeHandler(handler)
    messages = [record.getMessage() for record in records if record.levelno == logging.DEBUG]
    return last == "_sync_guard_probe" and any("_sync_guard_probe" in message for message in messages)


def _test_diagnostics_are_read_only():
    guard = compat.RenderGuard()
    rejected = []
    for name in ("skipped_renders", "last_skipped_method"):
        try:
            setattr(guard, name, 1)
        except AttributeError:
            rejected.append(name)
    return rejected == ["skipped_renders", "last_skipped_method"] and guard.skipped_renders == 0


async def _test_remounted_pages_keep_the_guard():
    # 切实例会重建全部页面，新页面必须带上独立的守卫与探针包装。
    async def body(app, pilot):
        before = app.page("modules").render_guard
        with TemporaryDirectory(prefix="akari-guard-") as raw:
            root = Path(raw) / "target"
            root.mkdir()
            previous = context.active_root()
            app.switch_instance(root)
            await pilot.pause()
            await asyncio.sleep(0.4)
            context.set_active_root(previous)
        page = app.page("modules")
        raised = ""
        try:
            page._render_guard_probe()
        except compat.NoMatches:
            raised = "NoMatches"
        independent = page.render_guard is not before
        skipped = page.render_guard.skipped_renders
        await pilot.press("q")
        return independent, raised, skipped

    independent, raised, skipped = await _with_app(body)
    return independent and raised == "NoMatches" and skipped == 0


@func_case
async def test_tui_render_guard(tester: Tester):
    """cli.tui._compat: 渲染守卫的选择器错误与卸载跳过测试"""
    _use_cli_locale()
    for name, method in PROBE_METHODS.items():
        setattr(ModulesPage, name, method)
    try:
        await tester.test(_test_active_page_selector_error_raises, "活动页面选择不存在时抛 NoMatches")
        await tester.test(_test_wrapped_renders_run_when_available, "页面可用时被包装的渲染照常执行")
        await tester.test(_test_guard_wraps_only_render_entry_prefixes, "守卫只包装约定的方法前缀")
        await tester.test(_test_exited_app_skips_and_counts, "应用退出后跳过渲染并记账")
        await tester.test(_test_detached_page_skips_and_counts, "页面卸下后跳过渲染并记账")
        await tester.test(_test_removing_or_stopped_page_skips_and_counts, "页面移除中与应用停止后跳过渲染并记账")
        await tester.test(_test_race_no_matches_is_skipped, "卸载瞬间的 NoMatches 兜底并记账")
        await tester.test(_test_skip_logs_at_debug_level, "跳过时记一条 debug 日志")
        await tester.test(_test_diagnostics_are_read_only, "诊断属性只读")
        await tester.test(_test_remounted_pages_keep_the_guard, "切实例重建的页面仍受守卫保护")
    finally:
        for name in PROBE_METHODS:
            delattr(ModulesPage, name)
    return tester
