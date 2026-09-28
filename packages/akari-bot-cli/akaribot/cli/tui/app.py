"""TUI 应用装配：App 子类、全局键位与启动入口。

页面实现放在 :mod:`akaribot.cli.tui.modules` 等兄弟模块；本模块只负责把页面装进 App、
声明全局键位，并回报启动耗时（规格关注首屏是否超过 1 秒）。
"""

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

# 侧栏顺序即页面顺序；key 同时用于控件 id（page-<key> / nav-<key>），第二项是侧栏标题的文案键。
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

    :param source: 模块数据源，缺省为 :class:`SubprocessModuleSource`。
    :param boot_started_at: 启动计时起点，由 :func:`run_tui` 传入。
    :param boot_note: 进入界面前发生的事（如自动登记了当前实例），挂载时以通知报出。
    """

    # 文案在类创建时取值：main.py 的 --lang 早于界面模块导入，改语言需重启进程。
    TITLE = i18n.t("cli.tui.app.title")
    SUB_TITLE = i18n.t("cli.tui.app.subtitle")
    CSS = STYLESHEET
    ENABLE_COMMAND_PALETTE = False
    # 只保留真正全局的动作。页面键位（r、/、i、u、Esc 等）由各页自行声明：注册在这里会作用于
    # 隐藏页——停在配置页按 u 曾会卸载模块页选中项。
    BINDINGS = compat.bindings(
        ("q", "quit", i18n.t("cli.tui.app.bind_quit")),
        ("ctrl+q", "quit", i18n.t("cli.tui.app.bind_quit")),
        ("question_mark", "show_help", i18n.t("cli.tui.app.bind_help")),
        ("ctrl+t", "toggle_theme", i18n.t("cli.tui.app.bind_toggle_theme"), False),
        # 前后翻页常驻可用但不必占页脚：页脚在 80 列下要留给本页高频键位。
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
        # 主题在挂载前注册并激活：样式表里的 $primary 等变量在首次解析时就要取到品牌色。
        compat.install_akari_themes(self)
        self.module_source: ModuleSource = source if source is not None else SubprocessModuleSource()
        # 各页数据源的可注入映射（键为 PAGES 的 key）；缺省时各页自建子进程实现，便于无头测试。
        self.sources: dict[str, Any] = dict(sources or {})
        self.cache_ttl = cache_ttl
        self.boot_note = boot_note
        self.initial_page = initial_page if any(key == initial_page for key, _, _ in PAGES) else "dashboard"
        self.active_page = self.initial_page
        self.instance_root = context.active_root()
        self.startup_ms: float = 0.0
        self.first_paint_ms: float = 0.0
        self._boot_started_at = boot_started_at if boot_started_at is not None else time.monotonic()

    def _instance_label(self) -> str:
        # 优先用注册名（与 `instance list`、概览页清单一致），未登记时退回实例自报名，再退回目录名。
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
        # 界面同时管多个实例：标题栏必须写明当前是哪一个，否则在配置页改 secret、在数据库页删数据项
        # 时看不出改的是谁。
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
        keys = [key for key, _, _ in PAGES]
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
            hint=i18n.t("cli.tui.app.help_hint"),
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
            yield compat.ListView(
                *[
                    compat.ListItem(compat.Label(i18n.t(title_key), markup=False), id=f"nav-{key}")
                    for key, title_key, _ in PAGES
                ],
                id="nav",
            )
            with compat.Vertical(id="content"):
                for key, _, page_class in PAGES:
                    yield self._build_page(key, page_class)
        yield compat.Footer()

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
        return page

    def switch_instance(self, root: Path) -> None:
        """切换当前管理的实例，并让所有页面改指新实例。

        各页数据源在取数时才解析实例根，故这里只需重挂载页面：新页面首次显示时会重新取数，
        注入的替身数据源保持不变，自动化断言仍按同一份数据源核对调用次数。
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
        """记录启动耗时、切到初始页，并在首帧后补记首屏时间与焦点。

        挂载期 Textual 尚未定焦点，此时调用 ``focus_primary()`` 会被随后的默认聚焦覆盖（焦点落在
        侧栏上，页级键位随之失效），故首帧之后再补一次。
        """
        self.startup_ms = (time.monotonic() - self._boot_started_at) * 1000.0
        self._sync_subtitle()
        self.show_page(self.initial_page)
        self._announce_boot_note()
        self.call_after_refresh(self._mark_first_paint)
        self.call_after_refresh(self.focus_active_page)

    def _announce_boot_note(self) -> None:
        # 首屏未必是概览页，进界面前发生的事只能用通知报出来，否则要等用户翻到概览页才看得到。
        if not self.boot_note:
            return
        compat.notify(self, self.boot_note, title=i18n.t("cli.tui.app.boot_note_title"))

    def _reset_pending(self, key: str) -> None:
        # 页面实现 reset_pending() 才需要复位；没有待确认状态的页面不必实现。
        try:
            page = self.query_one(f"#page-{key}")
        except Exception:  # noqa: BLE001 - 页面尚未挂载时无事可做
            return
        reset = getattr(page, "reset_pending", None)
        if callable(reset):
            reset()

    # 收集各页未保存改动的说明；页面实现 dirty_note() 才参与。
    def _dirty_notes(self) -> list[str]:
        notes: list[str] = []
        for key, _, _ in PAGES:
            try:
                page = self.query_one(f"#page-{key}")
            except Exception:  # noqa: BLE001 - 未挂载的页面没有脏值
                continue
            probe = getattr(page, "dirty_note", None)
            if not callable(probe):
                continue
            note = str(probe() or "").strip()
            if note:
                notes.append(note)
        return notes

    def focus_active_page(self) -> None:
        """把焦点交给当前页的主控件。"""
        focus_primary = getattr(self.query_one(f"#page-{self.active_page}"), "focus_primary", None)
        if callable(focus_primary):
            focus_primary()

    def show_page(self, key: str) -> None:
        """切换可见页面，并同步侧栏选中项与焦点。

        侧栏高亮、可见页面与 ``active_page`` 三者必须一致：只改 ``display`` 会让高亮停在旧项上，
        用户据此判断不出当前页，启动后的第一次按键也可能落到侧栏。

        :param key: 页面键，取自 :data:`PAGES`。
        """
        target = self.query_one(f"#page-{key}")
        # 离开的页面可能正等着第二次确认：切页后那次确认的语境已经不同，必须作废，否则用户以为
        # 自己在回答第一次询问，实际直接执行了破坏性动作。
        self._reset_pending(self.active_page)
        # 先亮目标页再隐藏旧页：反过来做的话，焦点会先随旧页一起被隐藏，Textual 会把焦点改派给
        # 隐藏页里的滚动容器（它只看控件自身的 display，不看祖先），页级键位随即错页。
        target.display = True
        self.active_page = key
        # 隐藏页不取数：只打开模块页时，其它页不应各自启动子进程、读日志或探测实例。
        activate = getattr(target, "activate", None)
        if callable(activate):
            activate()
        self.focus_active_page()
        for page_key, _, _ in PAGES:
            if page_key != key:
                self.query_one(f"#page-{page_key}").display = False
        self._sync_nav(key)

    def _sync_nav(self, key: str) -> None:
        # 侧栏的 ``Highlighted`` 会反过来调 :meth:`show_page`，故仅在索引确实不同的时候写回，
        # 避免「同步高亮 → 触发选中 → 再次同步」的往返。
        nav = self.query_one("#nav", compat.ListView)
        index = next((position for position, (page_key, _, _) in enumerate(PAGES) if page_key == key), 0)
        if compat.highlighted_index(nav) != index:
            nav.index = index

    @compat.on(compat.ListView.Selected, "#nav")
    def _on_nav_selected(self, event: compat.ListView.Selected) -> None:
        item_id = event.item.id or ""
        if item_id.startswith("nav-"):
            self.show_page(item_id.removeprefix("nav-"))

    def page(self, key: str) -> compat.Widget:
        """按 key 取页面控件，供测试与键位动作使用。"""
        return self.query_one(f"#page-{key}")

    def _mark_first_paint(self) -> None:
        self.first_paint_ms = (time.monotonic() - self._boot_started_at) * 1000.0

    def modules_page(self) -> ModulesPage:
        """返回 Modules 页控件。"""
        return self.query_one(ModulesPage)

    def action_quit(self) -> None:
        """退出应用；仍有后台任务在跑时先问一次，免得把装了一半的子进程丢在后台。"""
        pending = self._running_workers()
        if not pending:
            self.exit(0)
            return

        def _decide(choice: str | None) -> None:
            if choice == "quit":
                self.exit(0)

        compat.ask_choice(
            self,
            title=i18n.t("cli.tui.app.quit_busy_title"),
            hint=i18n.t(
                "cli.tui.app.quit_busy_hint",
                actions=i18n.t("cli.common.list_separator").join(pending[:6]),
            ),
            options=(("quit", i18n.t("cli.tui.app.quit_busy_confirm")),),
            cancel_label=i18n.t("cli.tui.app.quit_busy_cancel"),
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
    """启动 TUI 并阻塞到退出。

    :param source: 模块数据源，缺省为子进程实现。
    :param sources: 各页数据源映射，键为页面 key。
    :param initial_page: 启动时显示的页面 key。
    :param mouse: 是否请求鼠标追踪；哑终端或 tmux 下可经 ``--no-mouse`` 关闭。
    :param headless: 是否无头运行，供冻结产物自检使用。
    :param boot_note: 进入界面前发生的事，挂载时以通知报出；空串表示没有要报的。
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
