"""页面切换契约：侧栏高亮、可见页面、焦点与键位归属。

四者必须一致，否则用户判断不出当前页，且页级键位会被 App 级同键接管——停在配置页按 u 曾会
卸载模块页的选中项。本文件逐页断言这四条，并固定「隐藏页不取数」的启动行为。
"""

import asyncio
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import PAGES, TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORD = ModuleRecord(name="coin", dist="akari-bot-module-coin", version="0.1.0", state="installed")


class _Counting:
    # 用真实数据源而不是空替身：页面会读返回值的字段（如 ``snapshot.error``），返回空列表的替身
    # 会直接让页面抛异常，测到的就不是「有没有取数」而是替身不够像。
    def __init__(self, inner) -> None:
        self._inner = inner
        self.calls: dict[str, int] = {}

    def __getattr__(self, name: str):
        attribute = getattr(self._inner, name)
        if not callable(attribute):
            return attribute

        def _record(*args, **kwargs):
            self.calls[name] = self.calls.get(name, 0) + 1
            return attribute(*args, **kwargs)

        return _record


def _real_sources(root) -> dict:
    from akaribot.cli.tui.adapters import SubprocessAdapterSource
    from akaribot.cli.tui.config import SubprocessConfigSource
    from akaribot.cli.tui.dashboard import LocalDashboardSource
    from akaribot.cli.tui.dev import SubprocessDevSource
    from akaribot.cli.tui.logs import FileLogSource
    from akaribot.cli.tui.run import SubprocessRunSource

    return {
        "dashboard": _Counting(LocalDashboardSource(root=root)),
        "adapters": _Counting(SubprocessAdapterSource(root=root, timeout=10.0)),
        "config": _Counting(SubprocessConfigSource(root=root, timeout=10.0)),
        "logs": _Counting(FileLogSource(root=root)),
        "run": _Counting(SubprocessRunSource(root=root, timeout=10.0)),
        "dev": _Counting(SubprocessDevSource(root=root, timeout=10.0)),
    }


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _nav_index(app: TuiApp) -> int | None:
    return compat.highlighted_index(app.query_one("#nav", compat.ListView))


async def _with_app(body, *, initial_page: str = "modules", sources=None):
    app = TuiApp(
        source=StaticModuleSource([RECORD]),
        sources=sources,
        initial_page=initial_page,
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=(100, 30)) as pilot:
        await pilot.pause()
        await asyncio.sleep(0.3)
        return await body(app, pilot)


async def _test_initial_page_matches_sidebar():
    async def body(app, pilot):
        await pilot.press("q")
        return app.active_page, _nav_index(app), app.page("modules").display

    active, index, visible = await _with_app(body)
    return active == "modules" and index == 1 and visible is True


async def _test_show_page_syncs_every_page():
    async def body(app, pilot):
        observed = []
        for position, (key, _, _) in enumerate(PAGES):
            app.show_page(key)
            await pilot.pause()
            others = [other for other, _, _ in PAGES if other != key]
            observed.append((key, _nav_index(app), all(not app.page(other).display for other in others)))
        await pilot.press("q")
        return observed

    observed = await _with_app(body)
    return all(index == position and only_one for position, (_, index, only_one) in enumerate(observed))


async def _test_every_page_takes_focus():
    async def body(app, pilot):
        focused = []
        for key, _, _ in PAGES:
            app.show_page(key)
            await pilot.pause()
            await asyncio.sleep(0.1)
            focused.append((key, app.focused is not None))
        await pilot.press("q")
        return focused

    focused = await _with_app(body)
    return all(has_focus for _, has_focus in focused)


async def _test_focus_stays_on_active_page():
    async def body(app, pilot):
        inside = []
        for key, _, _ in PAGES:
            app.show_page(key)
            await pilot.pause()
            await asyncio.sleep(0.1)
            node = app.focused
            inside.append(node is not None and app.page(key) in node.ancestors_with_self)
        await pilot.press("q")
        return inside

    inside = await _with_app(body)
    return all(inside)


async def _test_module_keys_do_not_fire_elsewhere():
    async def body(app, pilot):
        source = app.module_source
        leaked = []
        for key in ("dashboard", "adapters", "config", "logs", "run", "dev"):
            app.show_page(key)
            await pilot.pause()
            await asyncio.sleep(0.1)
            before = dict(source.calls)
            for pressed in ("i", "u", "r", "escape"):
                await pilot.press(pressed)
                await pilot.pause()
            await asyncio.sleep(0.1)
            changed = {name: source.calls[name] - before.get(name, 0) for name in source.calls}
            leaked.append((key, {name: delta for name, delta in changed.items() if delta}))
        await pilot.press("q")
        return leaked

    leaked = await _with_app(body)
    return all(not delta for _, delta in leaked)


async def _test_module_keys_fire_on_modules_page():
    async def body(app, pilot):
        source = app.module_source
        app.show_page("modules")
        await pilot.pause()
        await asyncio.sleep(0.1)
        before = dict(source.calls)
        await pilot.press("u")
        await pilot.pause()
        await asyncio.sleep(0.2)
        await pilot.press("r")
        await pilot.pause()
        await asyncio.sleep(0.2)
        await pilot.press("q")
        return source.calls.get("uninstall", 0) - before.get("uninstall", 0), source.calls.get("list", 0) - before.get(
            "list", 0
        )

    uninstalls, lists = await _with_app(body)
    return uninstalls == 1 and lists >= 1


async def _test_hidden_pages_do_not_load():
    with TemporaryDirectory(prefix="akari-nav-") as raw:
        sources = _real_sources(Path(raw))

        async def body(app, pilot):
            await asyncio.sleep(0.5)
            await pilot.press("q")
            return {key: source.calls for key, source in sources.items() if source.calls}

        loaded = await _with_app(body, sources=sources)
    return loaded == {}


async def _test_first_visit_loads_once():
    with TemporaryDirectory(prefix="akari-nav-") as raw:
        sources = _real_sources(Path(raw))

        async def body(app, pilot):
            counts = {}
            for key in ("dashboard", "config"):
                app.show_page(key)
                await pilot.pause()
                await asyncio.sleep(0.4)
                counts[key] = dict(sources[key].calls)
                app.show_page(key)
                await pilot.pause()
                await asyncio.sleep(0.4)
                counts[f"{key}-again"] = dict(sources[key].calls)
            await pilot.press("q")
            return counts

        counts = await _with_app(body, sources=sources)
    return (
        counts["dashboard"] == counts["dashboard-again"]
        and counts["config"] == counts["config-again"]
        and counts["dashboard"]
        and counts["config"]
    )


async def _test_sidebar_browse_does_not_switch():
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        nav.focus()
        await pilot.pause()
        # 侧栏起始高亮落在活动页上，故按目标位置相对移动，不固定按键次数。
        target = [key for key, _, _ in PAGES].index("logs")
        while (_nav_index(app) or 0) < target:
            await pilot.press("down")
            await pilot.pause()
        browsing = (app.active_page, _nav_index(app))
        await pilot.press("q")
        return browsing

    active, index = await _with_app(body)
    return active == "modules" and index == 4


async def _test_sidebar_selection_switches_page():
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        nav.focus()
        await pilot.pause()
        target = [key for key, _, _ in PAGES].index("logs")
        while (_nav_index(app) or 0) < target:
            await pilot.press("down")
            await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        await asyncio.sleep(0.2)
        active = app.active_page
        index = _nav_index(app)
        focused = app.focused
        await pilot.press("q")
        return active, index, focused is not None

    active, index, has_focus = await _with_app(body)
    return active == "logs" and index == 4 and has_focus


@func_case
async def test_tui_navigation(tester: Tester):
    """cli.tui.app: 页面切换、焦点与键位归属测试"""
    _use_cli_locale()
    await tester.test(_test_initial_page_matches_sidebar, "启动页与侧栏高亮一致")
    await tester.test(_test_show_page_syncs_every_page, "逐页切换同步侧栏且只显示一页")
    await tester.test(_test_every_page_takes_focus, "每页都有焦点落点")
    await tester.test(_test_focus_stays_on_active_page, "焦点落在当前页内")
    await tester.test(_test_module_keys_do_not_fire_elsewhere, "其它页按 i/u/r/Esc 不触碰模块")
    await tester.test(_test_module_keys_fire_on_modules_page, "模块页页级键位生效")
    await tester.test(_test_hidden_pages_do_not_load, "隐藏页不取数")
    await tester.test(_test_first_visit_loads_once, "首次访问取一次数")
    await tester.test(_test_sidebar_browse_does_not_switch, "侧栏浏览只移高亮不切页")
    await tester.test(_test_sidebar_selection_switches_page, "侧栏 Enter 切页并同步")
    return tester
