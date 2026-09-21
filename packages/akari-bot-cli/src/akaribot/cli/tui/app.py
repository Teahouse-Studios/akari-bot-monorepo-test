"""TUI 应用装配：App 子类、全局键位与启动入口。

页面实现放在 :mod:`akaribot.cli.tui.modules` 等兄弟模块；本模块只负责把页面装进 App、
声明全局键位，并回报启动耗时（规格关注首屏是否超过 1 秒）。
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Any

from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.adapters import AdaptersPage
from akaribot.cli.tui.config import ConfigPage
from akaribot.cli.tui.dashboard import DashboardPage
from akaribot.cli.tui.dev import DevPage
from akaribot.cli.tui.logs import LogsPage
from akaribot.cli.tui.modules import ModuleSource, ModulesPage, SubprocessModuleSource
from akaribot.cli.tui.run import RunPage

# 侧栏顺序即页面顺序；key 同时用于控件 id（page-<key> / nav-<key>）。
PAGES: tuple[tuple[str, str, type], ...] = (
    ("dashboard", "Dashboard", DashboardPage),
    ("modules", "Modules", ModulesPage),
    ("adapters", "Adapters", AdaptersPage),
    ("config", "Config", ConfigPage),
    ("logs", "Logs", LogsPage),
    ("run", "Run", RunPage),
    ("dev", "Dev", DevPage),
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
    """

    TITLE = "AkariBot"
    SUB_TITLE = "实例管理"
    CSS = STYLESHEET
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = compat.bindings(
        ("q", "quit", "退出"),
        ("ctrl+q", "quit", "退出"),
        ("r", "refresh_modules", "刷新"),
        ("slash", "focus_search", "搜索"),
        ("i", "install_module", "安装"),
        ("u", "uninstall_module", "卸载"),
        ("escape", "clear_search", "清空搜索"),
    )

    def __init__(
        self,
        source: ModuleSource | None = None,
        *,
        sources: dict[str, Any] | None = None,
        boot_started_at: float | None = None,
        cache_ttl: float = 30.0,
        initial_page: str = "modules",
    ) -> None:
        super().__init__()
        self.module_source: ModuleSource = source if source is not None else SubprocessModuleSource()
        # 各页数据源的可注入映射（键为 PAGES 的 key）；缺省时各页自建子进程实现，便于无头测试。
        self.sources: dict[str, Any] = dict(sources or {})
        self.cache_ttl = cache_ttl
        self.initial_page = initial_page if any(key == initial_page for key, _, _ in PAGES) else "modules"
        self.active_page = self.initial_page
        self.startup_ms: float = 0.0
        self.first_paint_ms: float = 0.0
        self._boot_started_at = boot_started_at if boot_started_at is not None else time.monotonic()

    def compose(self) -> compat.ComposeResult:
        """装配侧栏与七个页面。"""
        yield compat.Header()
        with compat.Horizontal(id="shell"):
            yield compat.ListView(
                *[compat.ListItem(compat.Label(title, markup=False), id=f"nav-{key}") for key, title, _ in PAGES],
                id="nav",
            )
            with compat.Vertical(id="content"):
                for key, _, page_class in PAGES:
                    yield self._build_page(key, page_class)
        yield compat.Footer()

    def _build_page(self, key: str, page_class: type) -> compat.Widget:
        """按页构造控件，注入该页的数据源（若提供）。

        :param key: 页面键。
        :param page_class: 页面类。
        :return: 页面控件。
        """
        source = self.sources.get(key)
        if key == "modules":
            module_source = source if source is not None else self.module_source
            page = page_class(module_source, cache_ttl=self.cache_ttl, id=f"page-{key}")
        elif source is None:
            page = page_class(id=f"page-{key}")
        else:
            page = page_class(source, id=f"page-{key}")
        # 各页自行声明 __init__ 签名（不接受 classes），故样式类在此追加。
        page.add_class("page")
        return page

    def on_mount(self) -> None:
        """记录启动耗时、切到初始页，并在首帧后补记首屏时间。"""
        self.startup_ms = (time.monotonic() - self._boot_started_at) * 1000.0
        self.show_page(self.initial_page)
        self.call_after_refresh(self._mark_first_paint)

    def show_page(self, key: str) -> None:
        """切换可见页面，并同步侧栏选中项。

        :param key: 页面键，取自 :data:`PAGES`。
        """
        for page_key, _, _ in PAGES:
            self.query_one(f"#page-{page_key}").display = page_key == key
        self.active_page = key

    @compat.on(compat.ListView.Selected, "#nav")
    def _on_nav_selected(self, event: compat.ListView.Selected) -> None:
        """侧栏选中即切换页面。"""
        item_id = event.item.id or ""
        if item_id.startswith("nav-"):
            self.show_page(item_id.removeprefix("nav-"))

    def page(self, key: str) -> compat.Widget:
        """按 key 取页面控件，供测试与键位动作使用。"""
        return self.query_one(f"#page-{key}")

    def _mark_first_paint(self) -> None:
        """首帧渲染回调。"""
        self.first_paint_ms = (time.monotonic() - self._boot_started_at) * 1000.0

    def modules_page(self) -> ModulesPage:
        """返回 Modules 页控件。"""
        return self.query_one(ModulesPage)

    def action_quit(self) -> None:
        """退出应用并返回退出码 0。"""
        self.exit(0)

    def action_refresh_modules(self) -> None:
        """键位动作：强制刷新模块列表。"""
        self.modules_page().refresh_records(force=True)

    def action_install_module(self) -> None:
        """键位动作：安装当前目标。"""
        self.modules_page().request_install()

    def action_uninstall_module(self) -> None:
        """键位动作：卸载当前目标。"""
        self.modules_page().request_uninstall()

    def action_focus_search(self) -> None:
        """键位动作：聚焦搜索框。"""
        self.modules_page().focus_search()

    def action_clear_search(self) -> None:
        """键位动作：清空搜索框。"""
        self.modules_page().clear_search()


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
        return (
            f"启动 {self.startup_ms:.0f} ms，首帧 {self.first_paint_ms:.0f} ms，"
            f"共运行 {self.total_ms:.0f} ms，退出码 {self.exit_code}"
        )


def run_tui(
    source: ModuleSource | None = None,
    *,
    sources: dict[str, Any] | None = None,
    initial_page: str = "modules",
    mouse: bool = True,
    headless: bool = False,
) -> TuiRunResult:
    """启动 TUI 并阻塞到退出。

    :param source: 模块数据源，缺省为子进程实现。
    :param sources: 各页数据源映射，键为页面 key。
    :param initial_page: 启动时显示的页面 key。
    :param mouse: 是否请求鼠标追踪；哑终端或 tmux 下可经 ``--no-mouse`` 关闭。
    :param headless: 是否无头运行，供冻结产物自检使用。
    :return: 运行统计。
    """
    started = time.monotonic()
    app = TuiApp(source=source, sources=sources, initial_page=initial_page, boot_started_at=started)
    value = compat.run_app(app, mouse=mouse, headless=headless)
    total_ms = (time.monotonic() - started) * 1000.0
    exit_code = value if isinstance(value, int) else 0
    return TuiRunResult(
        exit_code=exit_code,
        startup_ms=app.startup_ms,
        first_paint_ms=app.first_paint_ms,
        total_ms=total_ms,
    )
