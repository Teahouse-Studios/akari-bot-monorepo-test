"""TUI 应用装配：App 子类、全局键位与启动入口。

页面实现放在 :mod:`akaribot.cli.tui.modules` 等兄弟模块；本模块只负责把页面装进 App、
声明全局键位，并回报启动耗时（规格关注首屏是否超过 1 秒）。
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass

from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.modules import ModuleSource, ModulesPage, SubprocessModuleSource

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

TuiApp #sidebar-hint {
    height: 1;
    padding: 0 1;
    color: $text-muted;
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
        boot_started_at: float | None = None,
        cache_ttl: float = 30.0,
    ) -> None:
        super().__init__()
        self.module_source: ModuleSource = source if source is not None else SubprocessModuleSource()
        self.cache_ttl = cache_ttl
        self.startup_ms: float = 0.0
        self.first_paint_ms: float = 0.0
        self._boot_started_at = boot_started_at if boot_started_at is not None else time.monotonic()

    def compose(self) -> compat.ComposeResult:
        """装配外壳与 Modules 页。"""
        yield compat.Header()
        yield ModulesPage(self.module_source, cache_ttl=self.cache_ttl, id="modules-page")
        yield compat.Footer()

    def on_mount(self) -> None:
        """记录启动耗时，并在首帧后补记首屏时间。"""
        self.startup_ms = (time.monotonic() - self._boot_started_at) * 1000.0
        self.call_after_refresh(self._mark_first_paint)

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


def run_tui(source: ModuleSource | None = None, *, mouse: bool = True, headless: bool = False) -> TuiRunResult:
    """启动 TUI 并阻塞到退出。

    :param source: 模块数据源，缺省为子进程实现。
    :param mouse: 是否请求鼠标追踪；哑终端或 tmux 下可经 ``--no-mouse`` 关闭。
    :param headless: 是否无头运行，供冻结产物自检使用。
    :return: 运行统计。
    """
    started = time.monotonic()
    app = TuiApp(source=source, boot_started_at=started)
    value = compat.run_app(app, mouse=mouse, headless=headless)
    total_ms = (time.monotonic() - started) * 1000.0
    exit_code = value if isinstance(value, int) else 0
    return TuiRunResult(
        exit_code=exit_code,
        startup_ms=app.startup_ms,
        first_paint_ms=app.first_paint_ms,
        total_ms=total_ms,
    )
