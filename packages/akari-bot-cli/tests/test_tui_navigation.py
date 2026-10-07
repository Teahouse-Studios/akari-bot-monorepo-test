"""页面切换契约：侧栏高亮、可见页面、焦点与键位归属。

四者必须一致，以保证页级键位作用于当前可见页面。本文件逐页断言交互归属与隐藏页不取数的行为。
侧栏分组与键盘翻页顺序由 NAV_PLAN 决定，高亮下标按条目 id 折算回 PAGES 的页面创建顺序。
"""

import asyncio
import json
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context
from akaribot.cli.tui.app import NAV_GROUPS, NAV_PLAN, PAGE_BLURB, PAGES, TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORD = ModuleRecord(name="coin", dist="akari-bot-module-coin", version="0.1.0", state="installed")
FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "sidebar.json"


class _Counting:
    # 使用真实数据源保留完整返回结构，避免替身结构不符导致误报。

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
        # 杂项页使用替身，避免启动 CLI 子进程。
        "misc": _Counting(StaticMiscSource()),
    }


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _nav_index(app: TuiApp) -> int | None:
    # 侧栏混排着四个分组标题，高亮下标不等于页面下标，按高亮项的 id 折算回 PAGES 顺序。
    nav = app.query_one("#nav", compat.ListView)
    position = compat.highlighted_index(nav)
    if position is None or position >= len(nav.children):
        return None
    item_id = nav.children[position].id or ""
    if not item_id.startswith("nav-"):
        return None
    return _page_index(item_id.removeprefix("nav-"))


def _fragment() -> dict[str, str]:
    return json.loads(FRAGMENT.read_text(encoding="utf-8"))


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
    # 首屏应显示当前实例及其运行状态。
    app = TuiApp(source=StaticModuleSource([RECORD]), boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(100, 30)) as pilot:
        await pilot.pause()
        page = app.active_page
        highlighted = _nav_index(app)
        await pilot.press("q")
    return page == "dashboard" and highlighted == _page_index("dashboard")


async def _test_subtitle_names_the_current_instance():
    # 标题栏持续显示实例标识，确保写操作的目标明确。
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
    async def body(app, pilot):
        keys = [(child.id or "").removeprefix("nav-") for child in app.query_one("#nav").children if not child.disabled]
        app.show_page(keys[0])
        visited = []
        for _ in keys:
            visited.append(app.active_page)
            await pilot.press("ctrl+right")
            await pilot.pause()
        wrapped = app.active_page
        await pilot.press("ctrl+left")
        await pilot.pause()
        previous = app.active_page
        return visited == keys and wrapped == keys[0] and previous == keys[-1]

    return await _with_app(body)


async def _test_help_overlay_lists_page_keys():
    # 页脚仅显示高频键位，? 应列出完整快捷键。
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
    async def body(app, pilot):
        for key, _, _ in PAGES:
            app.show_page(key)
            await pilot.pause()
            footer = app.query_one(compat.Footer)
            keys = [child for child in footer.children if getattr(child, "action", "")]
            if not keys or any(not footer.region.contains_region(child.region) for child in keys):
                return False
            descriptions = {getattr(child, "description", "") for child in keys}
            if not {i18n.t("cli.tui.app.bind_quit"), i18n.t("cli.tui.app.bind_help")} <= descriptions:
                return False
        return True

    return await _with_app(body, size=(80, 24))


async def _test_busy_quit_asks_first():
    # 后台任务运行时退出需确认，避免中断未完成的操作。
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
        # 后台任务运行期间再次退出仍需确认，应用由测试上下文关闭。
        again = type(app.screen).__name__
        return asked, stayed, again

    asked, stayed, again = await _with_app(body)
    return asked == "ChoiceScreen" and stayed is True and again == "ChoiceScreen"


async def _test_switching_instance_asks_when_dirty():
    # 切换实例会重新挂载页面，有未保存更改时需确认。
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
            page.query_one
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
    # 卸载请求应打开确认框且不立即执行，刷新键仍应触发读取。
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
        before = (app.active_page, _nav_index(app))
        await pilot.press("down")
        await pilot.pause()
        after = (app.active_page, _nav_index(app))
        await pilot.press("q")
        return before, after

    # 侧栏顺序由 NAV_PLAN 决定；此处验证方向键仅移动高亮，不切换页面。
    before, after = await _with_app(body)
    return (
        before == ("modules", _page_index("modules"))
        and after[0] == "modules"
        and after[1] is not None
        and after[1] != before[1]
    )


async def _test_sidebar_selection_switches_page():
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        nav.focus()
        await pilot.pause()
        await pilot.press("down")
        await pilot.pause()
        highlighted = _nav_index(app)
        await pilot.press("enter")
        await pilot.pause()
        await asyncio.sleep(0.2)
        active = app.active_page
        index = _nav_index(app)
        focused = app.focused
        await pilot.press("q")
        return highlighted, active, index, focused is not None

    highlighted, active, index, has_focus = await _with_app(body)
    opened = [key for key, _, _ in PAGES][highlighted] if highlighted is not None else ""
    return (
        highlighted is not None
        and highlighted != _page_index("modules")
        and active == opened
        and index == highlighted
        and has_focus
    )


async def _test_sidebar_groups_follow_the_plan():
    # 侧栏按 NAV_GROUPS 分四组：分组标题禁用且不可高亮，页面条目仍覆盖 PAGES 的全部页面。
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        items = [
            (child.id or "", child.disabled, tuple(str(label.render()) for label in child.query(compat.Label)))
            for child in nav.children
        ]
        await pilot.press("q")
        return items

    items = await _with_app(body)
    expected = [
        (f"navgroup-{position}" if kind == "group" else f"nav-{value}", kind == "group")
        for position, (kind, value) in enumerate(NAV_PLAN)
    ]
    observed = [(item_id, disabled) for item_id, disabled, _ in items]
    titles = {key: i18n.t(title_key) for key, title_key, _ in PAGES}
    group_texts = [labels[0] for item_id, disabled, labels in items if disabled and labels]
    plan_groups = [i18n.t(value) for kind, value in NAV_PLAN if kind == "group"]
    pages = {item_id.removeprefix("nav-") for item_id, disabled, _ in items if not disabled}
    return observed == expected and len(NAV_GROUPS) == 4 and pages == set(titles) and group_texts == plan_groups


async def _test_sidebar_items_have_single_label():
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        observed = {}
        for child in nav.children:
            item_id = child.id or ""
            if not item_id.startswith("nav-"):
                continue
            key = item_id.removeprefix("nav-")
            labels = list(child.query(compat.Label))
            observed[key] = tuple(str(label.render()) for label in labels)
        await pilot.press("q")
        return observed

    observed = await _with_app(body)
    titles = {key: i18n.t(title_key) for key, title_key, _ in PAGES}
    return observed == {key: (title,) for key, title in titles.items()}


async def _test_sidebar_fits_eighty_by_twenty_four():
    # 单行页面条目让 80×24 下的侧栏一次显示全部页面。
    async def body(app, pilot):
        nav = app.query_one("#nav", compat.ListView)
        app.show_page("misc")
        await pilot.pause()
        await asyncio.sleep(0.2)
        last = nav.children[-1]
        return (
            len(nav.children),
            nav.max_scroll_y,
            last.region.y >= nav.region.y and last.region.bottom <= nav.region.bottom,
            _nav_index(app),
        )

    count, max_scroll, reached, index = await _with_app(body, size=(80, 24))
    return count == len(NAV_PLAN) and max_scroll == 0 and reached and index == _page_index("misc")


async def _test_help_overlay_adds_navigation_hint():
    # 快捷键浮层同时显示公共导航说明与当前页面用途。
    async def body(app, pilot):
        await pilot.press("question_mark")
        await pilot.pause()
        nav_text = str(app.screen.query_one("#help-nav", compat.Static).render())
        hint_text = str(app.screen.query_one("#help-hint", compat.Static).render())
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return nav_text, hint_text

    nav_text, hint_text = await _with_app(body)
    fragment = _fragment()
    return (
        nav_text == i18n.t("cli.tui.app.help_nav")
        and hint_text == i18n.t("cli.tui.app.help_purpose", purpose=i18n.t(PAGE_BLURB["modules"]))
        and "cli.tui.app.help_nav" in fragment
        and "cli.tui.app.help_purpose" in fragment
    )


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
    await tester.test(_test_sidebar_groups_follow_the_plan, "侧栏按四组归类且页面齐全")
    await tester.test(_test_sidebar_items_have_single_label, "侧栏选项只显示页面名称")
    await tester.test(_test_sidebar_fits_eighty_by_twenty_four, "80 列 24 行下侧栏一次显示全部页面")
    await tester.test(_test_help_overlay_lists_page_keys, "帮助浮层列出本页键位")
    await tester.test(_test_help_overlay_adds_navigation_hint, "帮助浮层补导航说明与本页用途")
    await tester.test(_test_footer_fits_eighty_columns, "80 列下每页页脚不溢出")
    await tester.test(_test_busy_quit_asks_first, "有后台任务时退出先确认")
    await tester.test(_test_switching_instance_asks_when_dirty, "切换实例前先处理未保存改动")
    await tester.test(_test_module_keys_fire_on_modules_page, "模块页页级键位生效")
    await tester.test(_test_hidden_pages_do_not_load, "隐藏页不取数")
    await tester.test(_test_first_visit_loads_once, "首次访问取一次数")
    await tester.test(_test_sidebar_browse_does_not_switch, "侧栏浏览只移高亮不切页")
    await tester.test(_test_sidebar_selection_switches_page, "侧栏 Enter 切页并同步")
    return tester
