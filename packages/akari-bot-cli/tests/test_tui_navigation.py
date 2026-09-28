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
from akaribot.cli.tui import context
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


def _page_index(key: str) -> int:
    # 页面顺序调整时用例自动适配，不使用固定下标。
    return [page_key for page_key, _, _ in PAGES].index(key)


def _real_sources(root) -> dict:
    from akaribot.cli.tui.adapters import SubprocessAdapterSource
    from akaribot.cli.tui.config import SubprocessConfigSource
    from akaribot.cli.tui.dashboard import LocalDashboardSource
    from akaribot.cli.tui.dev import SubprocessDevSource
    from akaribot.cli.tui.doctor import SubprocessDoctorSource
    from akaribot.cli.tui.environment import SubprocessEnvironmentSource
    from akaribot.cli.tui.misc import StaticMiscSource
    from akaribot.cli.tui.logs import FileLogSource
    from akaribot.cli.tui.run import SubprocessRunSource

    return {
        "dashboard": _Counting(LocalDashboardSource(root=root)),
        "adapters": _Counting(SubprocessAdapterSource(root=root, timeout=10.0)),
        "config": _Counting(SubprocessConfigSource(root=root, timeout=10.0)),
        "logs": _Counting(FileLogSource(root=root)),
        "run": _Counting(SubprocessRunSource(root=root, timeout=10.0)),
        "dev": _Counting(SubprocessDevSource(root=root, timeout=10.0)),
        "doctor": _Counting(SubprocessDoctorSource(root=root, timeout=10.0)),
        "environment": _Counting(SubprocessEnvironmentSource(root=root, query_timeout=10.0, action_timeout=10.0)),
        # 杂项页没有预取，替身即可；真源会在用例里起一次 CLI 子进程。
        "misc": _Counting(StaticMiscSource()),
    }


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _nav_index(app: TuiApp) -> int | None:
    return compat.highlighted_index(app.query_one("#nav", compat.ListView))


async def _with_app(body, *, initial_page: str = "modules", sources=None, size=(100, 30)):
    app = TuiApp(
        source=StaticModuleSource([RECORD]),
        sources=sources,
        initial_page=initial_page,
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=size) as pilot:
        await pilot.pause()
        await asyncio.sleep(0.3)
        return await body(app, pilot)


async def _test_initial_page_matches_sidebar():
    async def body(app, pilot):
        await pilot.press("q")
        return app.active_page, _nav_index(app), app.page("modules").display

    active, index, visible = await _with_app(body)
    return active == "modules" and index == _page_index("modules") and visible is True


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


async def _test_initial_page_is_dashboard():
    # 首屏落在概览：第一次进来最该看到的是「我在管哪个实例、它跑没跑」，而不是包列表。
    app = TuiApp(source=StaticModuleSource([RECORD]), boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(100, 30)) as pilot:
        await pilot.pause()
        page = app.active_page
        highlighted = _nav_index(app)
        await pilot.press("q")
    return page == "dashboard" and highlighted == _page_index("dashboard")


async def _test_subtitle_names_the_current_instance():
    # 标题栏要写明当前实例：在配置页改 secret、数据库页删数据项时，看不出改的是哪一个最危险。
    with TemporaryDirectory(prefix="akari-nav-") as raw:
        root = Path(raw) / "demo-instance"
        root.mkdir()
        (root / "akaribot.toml").write_text('[instance]\nname = "demo"\n', encoding="utf-8")
        previous = context.active_root()
        context.set_active_root(root)
        try:
            app = TuiApp(source=StaticModuleSource([RECORD]), boot_started_at=time.monotonic())
            async with compat.app_test(app, size=(100, 30)) as pilot:
                await pilot.pause()
                named = app.sub_title
                await pilot.press("q")
        finally:
            context.set_active_root(previous)
    return "demo-instance" in named and i18n.t("cli.tui.app.subtitle") != named


async def _test_page_step_keys_walk_the_sidebar():
    # ctrl+← / ctrl+→ 逐页走，越界回到另一端；不依赖鼠标点侧栏。
    async def body(app, pilot):
        first = app.active_page
        await pilot.press("ctrl+right")
        await pilot.pause()
        second = (app.active_page, _nav_index(app))
        await pilot.press("ctrl+left")
        await pilot.pause()
        back = app.active_page
        for _ in range(len(PAGES) - 1):
            await pilot.press("ctrl+left")
            await pilot.pause()
        wrapped = app.active_page
        await pilot.press("q")
        return first, second, back, wrapped

    # 从 modules 连按 len(PAGES)-1 次「上一页」等于往回绕一圈，落在它的下一页。
    start = _page_index("modules")
    expected_wrap = [key for key, _, _ in PAGES][(start + 1) % len(PAGES)]
    first, second, back, wrapped = await _with_app(body)
    return (
        first == "modules"
        and second == ("adapters", _page_index("adapters"))
        and back == "modules"
        and wrapped == expected_wrap
    )


async def _test_help_overlay_lists_page_keys():
    # 页脚在 80 列下装不下十几条键位，故 ? 要给出一份完整清单。
    async def body(app, pilot):
        await pilot.press("question_mark")
        await pilot.pause()
        screen = app.screen
        opened = type(screen).__name__
        rows = [str(item.query_one(compat.Static).content) for item in screen.query(compat.ListItem)]
        text = "\n".join(rows)
        await pilot.press("escape")
        await pilot.pause()
        closed = type(app.screen).__name__
        await pilot.press("q")
        return opened, text, closed

    opened, text, closed = await _with_app(body)
    return opened == "HelpScreen" and "u" in text and closed == "Screen"


async def _test_footer_fits_eighty_columns():
    # 页脚在 80 列下会静默截断：把低频键位藏起来（bindings 四元组第 4 项 False）后仍要量一遍。
    async def body(app, pilot):
        widths: dict[str, int] = {}
        for key, _, _ in PAGES:
            app.show_page(key)
            await pilot.pause()
            await asyncio.sleep(0.05)
            footer = app.query_one(compat.Footer)
            widths[key] = compat.display_width(str(footer.render()))
        await pilot.press("q")
        return widths

    widths = await _with_app(body, size=(80, 24))
    return all(width <= 80 for width in widths.values())


async def _test_busy_quit_asks_first():
    # 后台任务在跑时按 q 必须先问一次：装了一半的 uv 子进程不该被丢在后台。
    async def body(app, pilot):
        app.run_worker(asyncio.sleep(2.0), group="demo-task")
        await pilot.pause()
        await pilot.press("q")
        await pilot.pause()
        asked = type(app.screen).__name__
        await pilot.press("escape")
        await pilot.pause()
        stayed = app.is_running
        await pilot.press("q")
        await pilot.pause()
        # 任务仍在跑，第二次按 q 依然只提问；用例结束由 app_test 收尾。
        again = type(app.screen).__name__
        return asked, stayed, again

    asked, stayed, again = await _with_app(body)
    return asked == "ChoiceScreen" and stayed is True and again == "ChoiceScreen"


async def _test_switching_instance_asks_when_dirty():
    # 切实例会重挂载页面：有未保存改动时要先问一次。
    with TemporaryDirectory(prefix="akari-nav-") as raw:
        root = Path(raw) / "target"
        root.mkdir()
        (root / "akaribot.toml").write_text('[instance]\nname = "target"\n', encoding="utf-8")

        async def body(app, pilot):
            page = app.page("database")
            page.dirty_note = lambda: "数据库页有一条未写入的新数据项"
            previous = context.active_root()
            app.switch_instance(root)
            await pilot.pause()
            asked = type(app.screen).__name__
            page.query_one  # 占位：保持页面引用存活
            await pilot.click("#choice-cancel") if False else None
            app.screen.query_one("#choice-0", compat.Button).press()
            await pilot.pause()
            await asyncio.sleep(0.2)
            switched = context.active_root()
            context.set_active_root(previous)
            await pilot.press("q")
            return asked, switched

        asked, switched = await _with_app(body)
    return asked == "ChoiceScreen" and switched is not None and switched.name == "target"


async def _test_module_keys_fire_on_modules_page():
    # 卸载现在一次按键即弹处置方式框，故这里断言「弹了框、没有直接卸」与「r 仍触发取数」。
    async def body(app, pilot):
        source = app.module_source
        app.show_page("modules")
        await pilot.pause()
        await asyncio.sleep(0.1)
        before = dict(source.calls)
        await pilot.press("u")
        await pilot.pause()
        await asyncio.sleep(0.2)
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("r")
        await pilot.pause()
        await asyncio.sleep(0.2)
        await pilot.press("q")
        return (
            opened,
            source.calls.get("uninstall", 0) - before.get("uninstall", 0),
            source.calls.get("list", 0) - before.get("list", 0),
        )

    opened, uninstalls, lists = await _with_app(body)
    return opened and uninstalls == 0 and lists >= 1


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
    return active == "modules" and index == _page_index("logs")


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
    return active == "logs" and index == _page_index("logs") and has_focus


@func_case
async def test_tui_navigation(tester: Tester):
    """cli.tui.app: 页面切换、焦点与键位归属测试"""
    _use_cli_locale()
    await tester.test(_test_initial_page_matches_sidebar, "启动页与侧栏高亮一致")
    await tester.test(_test_show_page_syncs_every_page, "逐页切换同步侧栏且只显示一页")
    await tester.test(_test_every_page_takes_focus, "每页都有焦点落点")
    await tester.test(_test_focus_stays_on_active_page, "焦点落在当前页内")
    await tester.test(_test_module_keys_do_not_fire_elsewhere, "其它页按 i/u/r/Esc 不触碰模块")
    await tester.test(_test_initial_page_is_dashboard, "首屏落在概览页")
    await tester.test(_test_subtitle_names_the_current_instance, "标题栏写明当前实例")
    await tester.test(_test_page_step_keys_walk_the_sidebar, "翻页键逐页走且越界折返")
    await tester.test(_test_help_overlay_lists_page_keys, "帮助浮层列出本页键位")
    await tester.test(_test_footer_fits_eighty_columns, "80 列下每页页脚不溢出")
    await tester.test(_test_busy_quit_asks_first, "有后台任务时退出先确认")
    await tester.test(_test_switching_instance_asks_when_dirty, "切换实例前先处理未保存改动")
    await tester.test(_test_module_keys_fire_on_modules_page, "模块页页级键位生效")
    await tester.test(_test_hidden_pages_do_not_load, "隐藏页不取数")
    await tester.test(_test_first_visit_loads_once, "首次访问取一次数")
    await tester.test(_test_sidebar_browse_does_not_switch, "侧栏浏览只移高亮不切页")
    await tester.test(_test_sidebar_selection_switches_page, "侧栏 Enter 切页并同步")
    return tester
