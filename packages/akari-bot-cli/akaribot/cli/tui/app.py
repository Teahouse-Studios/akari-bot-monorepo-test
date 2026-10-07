"""TUI 应用装配、页面注册、全局快捷键与启动入口。"""

from __future__ import annotations

from pathlib import Path

import hashlib
import time
from dataclasses import dataclass
from typing import Any

from akaribot.cli import i18n
from akaribot.cli.instances import InstanceRegistry
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context
from akaribot.cli.tui.adapters import AdaptersPage
from akaribot.cli.tui.config import ConfigPage
from akaribot.cli.tui.dashboard import DashboardPage
from akaribot.cli.tui.database import DatabasePage
from akaribot.cli.tui.environment import EnvironmentPage
from akaribot.cli.tui.dev import DevPage
from akaribot.cli.tui.doctor import DoctorPage
from akaribot.cli.tui.logs import LogsPage
from akaribot.cli.tui.misc import MiscPage
from akaribot.cli.tui.modules import ModuleSource, ModulesPage, SubprocessModuleSource
from akaribot.cli.tui.run import RunPage

# key 同时用于控件 id（page-<key> / nav-<key>），第二项是侧栏标题的文案键。
PAGES: tuple[tuple[str, str, type], ...] = (
    ("dashboard", "cli.tui.nav.dashboard", DashboardPage),
    ("environment", "cli.tui.nav.environment", EnvironmentPage),
    ("database", "cli.tui.nav.database", DatabasePage),
    ("modules", "cli.tui.nav.modules", ModulesPage),
    ("adapters", "cli.tui.nav.adapters", AdaptersPage),
    ("config", "cli.tui.nav.config", ConfigPage),
    ("logs", "cli.tui.nav.logs", LogsPage),
    ("run", "cli.tui.nav.run", RunPage),
    ("dev", "cli.tui.nav.dev", DevPage),
    ("doctor", "cli.tui.nav.doctor", DoctorPage),
    ("misc", "cli.tui.nav.misc", MiscPage),
)

# 侧栏分组同时决定阅读顺序与键盘翻页顺序。
NAV_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("cli.tui.nav.group.runtime", ("dashboard", "run", "logs", "doctor")),
    ("cli.tui.nav.group.platform", ("config", "adapters", "modules")),
    ("cli.tui.nav.group.data", ("environment", "database")),
    ("cli.tui.nav.group.dev", ("dev", "misc")),
)

# 页面用途说明显示在快捷键帮助中。
PAGE_BLURB: dict[str, str] = {
    "dashboard": "cli.tui.nav.blurb.dashboard",
    "environment": "cli.tui.nav.blurb.environment",
    "database": "cli.tui.nav.blurb.database",
    "modules": "cli.tui.nav.blurb.modules",
    "adapters": "cli.tui.nav.blurb.adapters",
    "config": "cli.tui.nav.blurb.config",
    "logs": "cli.tui.nav.blurb.logs",
    "run": "cli.tui.nav.blurb.run",
    "dev": "cli.tui.nav.blurb.dev",
    "doctor": "cli.tui.nav.blurb.doctor",
    "misc": "cli.tui.nav.blurb.misc",
}

# 分组标题参与侧栏索引，页面按 NAV_GROUPS 顺序排列。
NAV_PLAN: tuple[tuple[str, str], ...] = tuple(
    item
    for group_key, page_keys in NAV_GROUPS
    for item in (("group", group_key), *(("page", key) for key in page_keys))
)


def _nav_position(key: str) -> int:
    # 侧栏包含分组标题，索引需按 NAV_PLAN 计算。
    return next((position for position, entry in enumerate(NAV_PLAN) if entry == ("page", key)), 0)


INLINE_CSS = """
Screen {
    layout: vertical;
}

Header {
    dock: top;
}

Footer {
    dock: bottom;
}

TuiApp #shell {
    height: 1fr;
}

TuiApp #nav {
    width: 18;
    border-right: solid $panel;
}

TuiApp #nav ListItem {
    height: auto;
}

TuiApp #nav Label {
    width: 1fr;
    text-wrap: nowrap;
    text-overflow: ellipsis;
}

TuiApp #nav .nav-group {
    color: $text-muted;
    text-style: bold;
}

TuiApp #content {
    width: 1fr;
}

TuiApp .page {
    height: 1fr;
}
"""

STYLESHEET, STYLESHEET_ORIGIN = compat.load_stylesheet(
    __package__ or "akaribot.cli.tui",
    "app.tcss",
    INLINE_CSS,
)


def stylesheet_summary() -> dict[str, str | int]:
    """返回样式表来源、长度与摘要，供 ``tui --self-check`` 打印。"""
    return {
        "origin": STYLESHEET_ORIGIN,
        "bytes": len(STYLESHEET.encode("utf-8")),
        "sha256": hashlib.sha256(STYLESHEET.encode("utf-8")).hexdigest()[:16],
        "lines": STYLESHEET.count("\n") + 1,
    }


class TuiApp(compat.App[int]):
    """AkariBot 交互界面。

    :param source: 模块数据源，默认为 :class:`SubprocessModuleSource`。
    :param boot_started_at: 启动计时起点。
    :param boot_note: 界面启动时显示的通知内容。
    """

    # 文案在类创建时取值：main.py 的 --lang 早于界面模块导入，改语言需重启进程。
    TITLE = i18n.t("cli.tui.app.title")
    SUB_TITLE = i18n.t("cli.tui.app.subtitle")
    CSS = STYLESHEET
    ENABLE_COMMAND_PALETTE = False
    # 页面快捷键由各页声明，防止应用级绑定触发隐藏页面的操作。
    BINDINGS = compat.bindings(
        ("q", "quit", i18n.t("cli.tui.app.bind_quit")),
        ("ctrl+q", "quit", i18n.t("cli.tui.app.bind_quit")),
        ("question_mark", "show_help", i18n.t("cli.tui.app.bind_help")),
        ("ctrl+t", "toggle_theme", i18n.t("cli.tui.app.bind_toggle_theme"), False),
        # 页脚空间有限，页面切换快捷键仅在帮助中显示。
        ("ctrl+right", "next_page", i18n.t("cli.tui.app.bind_next_page"), False),
        ("ctrl+left", "previous_page", i18n.t("cli.tui.app.bind_previous_page"), False),
    )

    def __init__(
        self,
        source: ModuleSource | None = None,
        *,
        sources: dict[str, Any] | None = None,
        boot_started_at: float | None = None,
        cache_ttl: float = 30.0,
        initial_page: str = "dashboard",
        boot_note: str = "",
    ) -> None:
        super().__init__()
        # 首次解析样式表前必须注册主题，以提供 $primary 等变量。
        compat.install_akari_themes(self)
        self.module_source: ModuleSource = source if source is not None else SubprocessModuleSource()
        # 数据源支持注入，以便在无头测试中隔离子进程。
        self.sources: dict[str, Any] = dict(sources or {})
        self.cache_ttl = cache_ttl
        self.boot_note = boot_note
        self.initial_page = initial_page if any(key == initial_page for key, _, _ in PAGES) else "dashboard"
        self.active_page = self.initial_page
        self.instance_root = context.active_root()
        self.startup_ms: float = 0.0
        self.first_paint_ms: float = 0.0
        self._quit_confirming = False
        self._quit_gate = compat.PendingConfirm()
        self._boot_started_at = boot_started_at if boot_started_at is not None else time.monotonic()

    def _instance_label(self) -> str:
        # 名称优先采用注册表记录，未登记时使用目录名。
        root = self.instance_root or context.active_root()
        if root is None:
            return i18n.t("cli.tui.app.instance_unknown")
        try:
            entry = InstanceRegistry().find_by_root(Path(root))
        except Exception:  # noqa: BLE001 - 注册表不可用时退回路径名
            entry = None
        if entry is not None and entry.name:
            return entry.name
        return Path(root).name or str(root)

    def _sync_subtitle(self) -> None:
        # 标题栏标识当前实例，便于确认配置与数据操作的目标。
        self.sub_title = i18n.t("cli.tui.app.subtitle_with_instance", name=self._instance_label())

    def _running_workers(self) -> list[str]:
        names: list[str] = []
        for worker in self.workers:
            if worker.is_finished or worker.is_cancelled:
                continue
            names.append(worker.group or worker.name or i18n.t("cli.tui.app.worker_unnamed"))
        return names

    def action_next_page(self) -> None:
        """键位动作：切到下一个页面。"""
        self._step_page(1)

    def action_previous_page(self) -> None:
        """键位动作：切到上一个页面。"""
        self._step_page(-1)

    def _step_page(self, delta: int) -> None:
        keys = [key for kind, key in NAV_PLAN if kind == "page"]
        index = keys.index(self.active_page) if self.active_page in keys else 0
        self.show_page(keys[(index + delta) % len(keys)])

    def action_show_help(self) -> None:
        """键位动作：列出当前页与全局键位。"""
        page = self.query_one(f"#page-{self.active_page}")
        rows: list[tuple[str, str]] = []
        seen: set[str] = set()
        for binding in [*getattr(page, "BINDINGS", ()), *self.BINDINGS]:
            key = str(getattr(binding, "key", ""))
            if not key or key in seen:
                continue
            seen.add(key)
            rows.append((key, str(getattr(binding, "description", ""))))
        compat.show_help(
            self,
            title=i18n.t("cli.tui.app.help_title", page=i18n.t(self._page_title_key(self.active_page))),
            hint=i18n.t("cli.tui.app.help_purpose", purpose=i18n.t(PAGE_BLURB[self.active_page])),
            nav_hint=i18n.t("cli.tui.app.help_nav"),
            rows=tuple(rows),
            close_label=i18n.t("cli.tui.app.help_close"),
        )

    @staticmethod
    def _page_title_key(key: str) -> str:
        for page_key, title_key, _ in PAGES:
            if page_key == key:
                return title_key
        return "cli.tui.app.title"

    def action_toggle_theme(self) -> None:
        """键位动作：在品牌深色与浅色主题之间切换。"""
        chosen = compat.toggle_akari_theme(self)
        name = i18n.t("cli.tui.app.theme_dark" if chosen == compat.AKARI_THEME_DARK else "cli.tui.app.theme_light")
        compat.notify(
            self,
            i18n.t("cli.tui.app.theme_switched", name=name),
            severity="information",
            title=i18n.t("cli.tui.app.bind_toggle_theme"),
        )

    def compose(self) -> compat.ComposeResult:
        """装配侧栏与全部页面。"""
        yield compat.Header()
        with compat.Horizontal(id="shell"):
            yield compat.ListView(*self._nav_items(), id="nav")
            with compat.Vertical(id="content"):
                for key, _, page_class in PAGES:
                    yield self._build_page(key, page_class)
        yield compat.Footer()

    def _nav_items(self) -> list[compat.ListItem]:
        # 分组标题不可选中，避免导航操作将其作为页面。
        items: list[compat.ListItem] = []
        for position, (kind, value) in enumerate(NAV_PLAN):
            if kind == "group":
                items.append(
                    compat.ListItem(
                        compat.Label(i18n.t(value), markup=False, classes="nav-group"),
                        id=f"navgroup-{position}",
                        disabled=True,
                    )
                )
                continue
            items.append(
                compat.ListItem(
                    compat.Label(i18n.t(self._page_title_key(value)), markup=False),
                    id=f"nav-{value}",
                )
            )
        return items

    def _build_page(self, key: str, page_class: type) -> compat.Widget:
        source = self.sources.get(key)
        if key == "modules":
            module_source = source if source is not None else self.module_source
            page = page_class(module_source, cache_ttl=self.cache_ttl, id=f"page-{key}")
        elif key == "dashboard":
            # 概览页另有实例清单与服务控制两个数据源，键为 dashboard_instances / dashboard_service。
            instances = self.sources.get("dashboard_instances")
            control = self.sources.get("dashboard_service")
            page = page_class(
                source,
                instances=instances,
                service_control=control,
                cache_ttl=self.cache_ttl,
                id=f"page-{key}",
            )
        elif source is None:
            page = page_class(id=f"page-{key}")
        else:
            page = page_class(source, id=f"page-{key}")
        # 各页自行声明 __init__ 签名（不接受 classes），故样式类在此追加。
        page.add_class("page")
        # 统一保护渲染入口，避免异步读取在页面卸载后访问控件。
        compat.guard_renders(page)
        return page

    def switch_instance(self, root: Path) -> None:
        """切换管理实例并重新加载各页面。

        :param root: 目标实例的根目录。
        """
        notes = self._dirty_notes()
        if not notes:
            self._switch_instance(root)
            return
        target = Path(root).expanduser().resolve()

        def _decide(choice: str | None) -> None:
            if choice == "discard":
                self._switch_instance(target)

        compat.ask_choice(
            self,
            title=i18n.t("cli.tui.app.switch_dirty_title"),
            hint=i18n.t("cli.tui.app.switch_dirty_hint", notes=i18n.t("cli.common.list_separator").join(notes)),
            options=(("discard", i18n.t("cli.tui.app.switch_dirty_confirm")),),
            cancel_label=i18n.t("cli.tui.app.switch_dirty_cancel"),
            callback=_decide,
        )

    def _switch_instance(self, root: Path) -> None:
        context.set_active_root(root)
        self.instance_root = Path(root).expanduser().resolve()
        self._sync_subtitle()
        content = self.query_one("#content", compat.Vertical)
        self.run_worker(self._remount_pages(content), group="switch-instance", exclusive=True)

    async def _remount_pages(self, content: compat.Vertical) -> None:
        await content.remove_children()
        await content.mount_all([self._build_page(key, page_class) for key, _, page_class in PAGES])
        self.show_page(self.active_page)

    def on_mount(self) -> None:
        """记录启动耗时、显示初始页面并设置焦点。"""
        self.startup_ms = (time.monotonic() - self._boot_started_at) * 1000.0
        self._sync_subtitle()
        self.show_page(self.initial_page)
        self._announce_boot_note()
        self.call_after_refresh(self._mark_first_paint)
        # Textual 的默认聚焦发生在挂载后，页面焦点需在首帧之后设置。
        self.call_after_refresh(self.focus_active_page)

    def _announce_boot_note(self) -> None:
        # 启动信息通过通知显示，以支持任意初始页面。
        if not self.boot_note:
            return
        compat.notify(self, self.boot_note, title=i18n.t("cli.tui.app.boot_note_title"))

    def _reset_pending(self, key: str) -> None:
        # 待确认状态由实现 reset_pending() 的页面管理。
        try:
            page = self.query_one(f"#page-{key}")
        except Exception:  # noqa: BLE001 - 页面尚未挂载时无需复位
            return
        reset = getattr(page, "reset_pending", None)
        if callable(reset):
            reset()

    # 页面通过 dirty_note() 提供未保存更改摘要。
    def _dirty_notes(self) -> list[str]:
        notes: list[str] = []
        for key, _, _ in PAGES:
            try:
                page = self.query_one(f"#page-{key}")
            except Exception:  # noqa: BLE001 - 未挂载页面无编辑状态
                continue
            probe = getattr(page, "dirty_note", None)
            if not callable(probe):
                continue
            note = str(probe() or "").strip()
            if note:
                notes.append(note)
        return notes

    def focus_active_page(self) -> None:
        """将焦点移至当前页的主控件。"""
        focus_primary = getattr(self.query_one(f"#page-{self.active_page}"), "focus_primary", None)
        if callable(focus_primary):
            focus_primary()

    def show_page(self, key: str) -> None:
        """切换页面，同步侧栏选中项与焦点。

        :param key: 页面键，取自 :data:`PAGES`。
        """
        target = self.query_one(f"#page-{key}")
        # 切页会改变操作上下文，须清除待确认状态。
        self._reset_pending(self.active_page)
        # 先显示并聚焦目标页，避免隐藏旧页时 Textual 将焦点分配给隐藏容器。
        target.display = True
        self.active_page = key
        # 仅激活可见页面，避免隐藏页执行无关的读取与轮询。
        activate = getattr(target, "activate", None)
        if callable(activate):
            activate()
        self.focus_active_page()
        for page_key, _, _ in PAGES:
            if page_key != key:
                self.query_one(f"#page-{page_key}").display = False
        self._sync_nav(key)

    def _sync_nav(self, key: str) -> None:
        # 仅在索引变化时更新，避免侧栏事件重复触发页面同步。
        nav = self.query_one("#nav", compat.ListView)
        index = _nav_position(key)
        if compat.highlighted_index(nav) != index:
            nav.index = index

    @compat.on(compat.ListView.Selected, "#nav")
    def _on_nav_selected(self, event: compat.ListView.Selected) -> None:
        key = (event.item.id or "").removeprefix("nav-")
        if any(key == page_key for page_key, _, _ in PAGES):
            self.show_page(key)
        else:
            # 鼠标点击分组标题仍可能产生 Selected，须恢复当前页高亮。
            self._sync_nav(self.active_page)

    def page(self, key: str) -> compat.Widget:
        """按 key 取页面控件，供测试与键位动作使用。"""
        return self.query_one(f"#page-{key}")

    def _mark_first_paint(self) -> None:
        self.first_paint_ms = (time.monotonic() - self._boot_started_at) * 1000.0

    def modules_page(self) -> ModulesPage:
        """返回 Modules 页控件。"""
        return self.query_one(ModulesPage)

    def action_quit(self) -> None:
        """退出应用；未保存更改或后台任务存在时请求确认。"""
        if self._quit_confirming:
            return
        notes = self._dirty_notes()
        pending = self._running_workers()
        if not notes and not pending:
            self.exit(0)
            return
        if not self._quit_gate.accept("quit"):
            return
        self._quit_confirming = True
        previous_focus = self.focused
        previous_screen = self.screen
        previous_page = self.active_page

        def _restore_focus() -> None:
            if (
                previous_focus is not None
                and compat.mounted(previous_focus)
                and previous_focus.is_mounted
                and self.screen is previous_screen
                and self.active_page == previous_page
            ):
                compat.focus_now(previous_focus)

        def _decide(choice: str | None) -> None:
            self._quit_confirming = False
            self._quit_gate.reset()
            if choice == "quit":
                self.exit(0)
            else:
                self.call_after_refresh(_restore_focus)

        hints = []
        if notes:
            hints.append(i18n.t("cli.tui.app.quit_dirty_hint", notes="\n".join(notes)))
        if pending:
            hints.append(
                i18n.t("cli.tui.app.quit_busy_hint", actions=i18n.t("cli.common.list_separator").join(pending[:6]))
            )
        compat.ask_choice(
            self,
            title=i18n.t("cli.tui.app.quit_busy_title"),
            hint="\n\n".join(hints),
            options=(("quit", i18n.t("cli.tui.app.quit_dirty_confirm" if notes else "cli.tui.app.quit_busy_confirm")),),
            cancel_label=i18n.t("cli.tui.app.quit_dirty_cancel" if notes else "cli.tui.app.quit_busy_cancel"),
            callback=_decide,
        )


@dataclass(frozen=True)
class TuiRunResult:
    """一次 TUI 运行的统计。

    :param exit_code: 进程退出码。
    :param startup_ms: 从调用运行到 ``on_mount`` 的毫秒数，含 Textual 导入与样式解析。
    :param first_paint_ms: 到首帧渲染完成的毫秒数。
    :param total_ms: 应用运行的总毫秒数。
    """

    exit_code: int
    startup_ms: float
    first_paint_ms: float
    total_ms: float

    def summary(self) -> str:
        """返回单行文字摘要。"""
        return i18n.t(
            "cli.tui.app.run_summary",
            startup=f"{self.startup_ms:.0f}",
            first_paint=f"{self.first_paint_ms:.0f}",
            total=f"{self.total_ms:.0f}",
            exit_code=self.exit_code,
        )


def run_tui(
    source: ModuleSource | None = None,
    *,
    sources: dict[str, Any] | None = None,
    initial_page: str = "dashboard",
    mouse: bool = True,
    headless: bool = False,
    boot_note: str = "",
) -> TuiRunResult:
    """启动 TUI 并阻塞至退出。

    :param source: 模块数据源，默认使用子进程实现。
    :param sources: 各页数据源映射，键为页面标识。
    :param initial_page: 初始页面标识。
    :param mouse: 是否启用鼠标追踪。
    :param headless: 是否以无头模式运行，用于自检。
    :param boot_note: 启动通知；空字符串表示不显示通知。
    :return: 运行统计。
    """
    started = time.monotonic()
    app = TuiApp(
        source=source,
        sources=sources,
        initial_page=initial_page,
        boot_started_at=started,
        boot_note=boot_note,
    )
    value = compat.run_app(app, mouse=mouse, headless=headless)
    total_ms = (time.monotonic() - started) * 1000.0
    exit_code = value if isinstance(value, int) else 0
    return TuiRunResult(
        exit_code=exit_code,
        startup_ms=app.startup_ms,
        first_paint_ms=app.first_paint_ms,
        total_ms=total_ms,
    )
