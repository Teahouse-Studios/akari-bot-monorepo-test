"""Textual 兼容层：TUI 内全部 Textual 用法经此收口。

上游 Textual 跨版本有 API 变动史——widget 的导出位置、消息类名、``Binding`` 构造参数、
``run`` / ``run_test`` 的关键字、CSS 属性的名称与取值、鼠标相关开关——把导入与调用集中在
本模块后，升级 Textual 只需改这一个文件。本模块只做再导出、薄包装与终端宽度计算，不含业务逻辑。

约定：``akaribot/cli/tui`` 下的其它模块一律 ``from akaribot.cli.tui import _compat as compat``，
不得直接 ``import textual``，也不得直接 ``import rich``。
"""

from __future__ import annotations

import importlib
import importlib.resources
import os
import sys
from collections.abc import AsyncIterator, Iterable, Iterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from rich.cells import cell_len, chop_cells, get_character_cell_size
from rich.markup import escape as _rich_escape
from rich.text import Text
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.css.stylesheet import Stylesheet
from textual.pilot import Pilot
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Input, Label, ListItem, ListView, ProgressBar, Static

from akaribot.cli import i18n

__all__ = [
    "App",
    "Binding",
    "BindingType",
    "Button",
    "ComposeResult",
    "Footer",
    "Header",
    "Horizontal",
    "Input",
    "KEY_ALIASES",
    "Label",
    "ListItem",
    "ListView",
    "Pilot",
    "ProgressBar",
    "Screen",
    "Static",
    "Stylesheet",
    "TEXTUAL_PIN",
    "TerminalCapability",
    "Vertical",
    "VerticalScroll",
    "Widget",
    "align_rows",
    "app_test",
    "bind",
    "bindings",
    "cell_width",
    "check_textual_version",
    "column_width",
    "display_width",
    "events",
    "fit_cells",
    "highlighted_index",
    "is_interactive_terminal",
    "load_stylesheet",
    "notify",
    "on",
    "pad_cells",
    "plain_text",
    "pop_screen",
    "progress_phase",
    "push_screen",
    "reactive",
    "read_resource_text",
    "resource_inventory",
    "run_app",
    "set_text_selection",
    "textual_version",
    "truncate_cells",
    "widget_cells",
    "work",
]

TEXTUAL_PIN = "8.2.8"
"""与 ``pyproject.toml`` 中 ``textual==8.2.8`` 一致的期望版本。

本模块的包装按该版本的行为编写与实测；运行期版本不一致时自检必须报错，
以免「依赖被顶版」的表现被误判成界面缺陷。
"""

KEY_ALIASES = {
    "solidus": "slash",
    "forward_slash": "slash",
    "esc": "escape",
    "return": "enter",
}
"""键名别名表。

Textual 对非字母数字键的命名由 Unicode 名派生（``/`` 即 ``SOLIDUS``），历史上出现过
``solidus`` / ``slash`` 两种写法，故在 :func:`bind` 内统一归一，页面只写规范名。
"""


def textual_version() -> str:
    """返回运行期 Textual 版本号。"""
    module = importlib.import_module("textual")
    return str(getattr(module, "__version__", "unknown"))


def check_textual_version(pin: str = TEXTUAL_PIN) -> tuple[bool, str]:
    """比对运行期版本与紧钉版本。

    :param pin: 期望版本，默认取 :data:`TEXTUAL_PIN`。
    :return: 二元组——是否符合紧钉；可直接打印的说明文本。
    """
    found = textual_version()
    return found == pin, i18n.t("cli.tui.selfcheck.textual_version", pin=pin, found=found)


# region 宽度计算（中文宽字符对齐）

# 理由：``len()`` 数的是码点，中日韩字符与 emoji 在终端占 2 列，直接用它排版必然错位。
# ``rich.cells`` 与 Textual 渲染同源，故列表列宽、详情标签列与截断统一走这里。


def cell_width(char: str) -> int:
    """返回单个字符占用的终端列数。"""
    return get_character_cell_size(char)


def display_width(text: str) -> int:
    """返回字符串占用的终端列数，中文与 emoji 按 2 列计。"""
    return cell_len(text)


def truncate_cells(text: str, width: int, ellipsis: str = "…") -> str:
    """按终端列宽截断，且不劈开宽字符；被截断时补省略号。

    :param text: 原始文本。
    :param width: 可用的终端列数，小于等于 0 时返回空串。
    :param ellipsis: 截断标记，默认省略号占 1 列。
    :return: 显示宽度不超过 ``width`` 的文本。
    """
    if width <= 0:
        return ""
    if display_width(text) <= width:
        return text
    mark_width = display_width(ellipsis)
    keep = width if mark_width > width else width - mark_width
    head = ""
    if keep > 0:
        chunk = "".join(chop_cells(text, keep)[:1])
        head = chunk if display_width(chunk) <= keep else chunk[:-1]
    return f"{head}{ellipsis}" if 0 < mark_width <= width else head


def pad_cells(text: str, width: int, align: str = "left") -> str:
    """按终端列宽补空格。

    :param text: 原始文本，超宽时不截断，由调用方决定是否先经 :func:`truncate_cells`。
    :param width: 目标终端列数。
    :param align: ``left`` / ``right`` / ``center``。
    :return: 补齐到 ``width`` 列的文本。
    """
    padding = width - display_width(text)
    if padding <= 0:
        return text
    if align == "right":
        return " " * padding + text
    if align == "center":
        left = padding // 2
        return " " * left + text + " " * (padding - left)
    return text + " " * padding


def fit_cells(text: str, width: int, align: str = "left", ellipsis: str = "…") -> str:
    """先按列宽截断再补齐，用于定宽列。"""
    return pad_cells(truncate_cells(text, width, ellipsis), width, align)


def column_width(values: Iterable[str]) -> int:
    """返回一组文本的最大显示宽度，用于确定列宽。"""
    return max((display_width(value) for value in values), default=0)


def align_rows(rows: Sequence[tuple[str, str]], gap: int = 2, align: str = "left") -> list[str]:
    """把两列文本按显示宽度对齐成定宽行。

    :param rows: 二元组序列——左列（标签）与右列（值）。
    :param gap: 两列之间的空格数。
    :param align: 左列对齐方式。
    :return: 每行一条、左列已补齐的文本。
    """
    label_width = column_width(label for label, _ in rows)
    return [f"{pad_cells(label, label_width, align)}{' ' * gap}{value}" for label, value in rows]


# endregion


# region 包内资源与样式表

# 理由：``App.CSS_PATH`` 依赖 App 子类所在文件的磁盘路径，Nuitka onefile 冻结后该路径不成立；
# 因此样式表统一由 ``importlib.resources`` 读取文本后赋给 ``App.CSS``，并在读不到时回退内联常量。


def read_resource_text(package: str, resource: str) -> str | None:
    """读取包内文本资源。

    :param package: 包名，如 ``akaribot.cli.tui``。
    :param resource: 包内相对路径，如 ``app.tcss``。
    :return: 资源文本；资源缺失或当前打包形态不提供可读资源时返回 ``None``。
    """
    try:
        target = importlib.resources.files(package).joinpath(resource)
    except (ImportError, ModuleNotFoundError, TypeError):
        return None
    try:
        if not target.is_file():
            return None
        return target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def resource_inventory(package: str) -> list[str]:
    """列出包内可读资源名，供自检报告冻结产物的资源可达性。"""
    try:
        entries = importlib.resources.files(package).iterdir()
    except (ImportError, ModuleNotFoundError, OSError, TypeError):
        return []
    names: list[str] = []
    for entry in entries:
        try:
            names.append(entry.name)
        except (AttributeError, OSError):
            continue
    return sorted(names)


def load_stylesheet(package: str, resource: str, fallback: str) -> tuple[str, str]:
    """加载样式表文本，优先包内资源，缺失时回退内联常量。

    :param package: 资源所在包。
    :param resource: 包内资源名。
    :param fallback: 内联样式表文本。
    :return: 二元组——样式表文本与来源说明（``resource:app.tcss`` 或 ``inline:app.py``）。
    """
    text = read_resource_text(package, resource)
    if text is None:
        return fallback, f"inline:{resource.replace('.tcss', '.py')}"
    return text, f"resource:{resource}"


def parse_stylesheet(css: str, path: str = "<tui>", app: App[Any] | None = None) -> Stylesheet:
    """把样式表文本交给 Textual 解析，语法错误与未定义变量在此暴露。

    :param css: 样式表文本。
    :param path: 报错时显示的名称。
    :param app: 提供主题变量的应用实例；省略时样式表中的 ``$变量`` 无法解析。
    :return: 已解析的 :class:`~textual.css.stylesheet.Stylesheet`。

    理由：``Stylesheet`` 需要 ``App.get_css_variables()`` 提供的主题变量（``$text-muted`` 等），
    脱离应用实例解析会报未定义变量，故把变量来源一并收进本包装。
    """
    sheet = Stylesheet(variables=app.get_css_variables() if app is not None else None)
    sheet.add_source(css, read_from=("tui", path))
    sheet.parse()
    return sheet


# endregion


# region 应用、键位与消息

# 理由：``ComposeResult`` 曾只在 ``textual.app`` 内可用；``ListView`` 等 widget 的模块路径也变过。


def bind(key: str, action: str, description: str, *, show: bool = True) -> BindingType:
    """构造一条键位绑定。

    :param key: 键名，如 ``q``、``ctrl+r``。
    :param action: 动作名，对应 ``action_<name>`` 方法。
    :param description: 页脚显示的文字。
    :param show: 是否在页脚展示。
    :return: Textual 的绑定对象；页面不直接构造 ``Binding``。

    理由：``Binding`` 的参数表在版本间增删过（四元组写法、``id`` / ``system`` / ``group``、
    ``priority`` 语义），页面只提供三元组可把差异挡在本函数内；键名同时经 :data:`KEY_ALIASES` 归一。
    """
    return Binding(KEY_ALIASES.get(key, key), action, description, show=show)


def bindings(*items: tuple[str, str, str]) -> list[BindingType]:
    """批量构造键位绑定，入参为 ``(key, action, description)`` 序列。"""
    return [bind(key, action, description) for key, action, description in items]


def highlighted_index(list_view: ListView) -> int | None:
    """取当前高亮项下标，无高亮时返回 ``None``。

    理由：``ListView.index`` 与 ``highlighted_child`` 的语义在版本间有出入，统一读 ``index``。
    """
    index = getattr(list_view, "index", None)
    return index if isinstance(index, int) and index >= 0 else None


def plain_text(value: str, style: str | None = None) -> Text:
    """构造不做标记解析的富文本。

    :param value: 原始文本。
    :param style: 可选的 Rich 样式名。
    :return: 可直接交给 ``Static.update`` 的文本对象。

    理由：模块名与简介来自子进程 JSON，含 ``[`` 时会被 Textual 标记语法吞掉，故一律关闭解析。
    """
    return Text(value, style=style)


def escape_markup(value: str) -> str:
    """转义文本中的标记字符，仅在确实需要拼接标记时使用。"""
    return _rich_escape(value)


def notify(app: App[Any], message: str, *, severity: str = "information", title: str = "") -> None:
    """弹出通知，未挂载或不支持时静默返回。

    理由：``App.notify`` 的 ``severity`` 由位置参数改为关键字参数，统一按关键字调用。
    """
    notify_fn = getattr(app, "notify", None)
    if notify_fn is None:
        return
    try:
        notify_fn(message, title=title, severity=severity)
    except Exception:  # noqa: BLE001 - 通知失败不应中断界面操作
        return


def push_screen(app: App[Any], screen: Screen[Any] | str) -> Any:
    """推入一个页面。

    理由：``push_screen`` 的 ``callback`` / ``wait_for_dismiss`` / ``mode`` 参数是逐版本加上的，
    页面只传页面对象或名字，返回值由调用方决定是否等待。
    """
    return app.push_screen(screen)


def pop_screen(app: App[Any]) -> Any:
    """弹出当前页面。"""
    return app.pop_screen()


def widget_cells(widget: Widget) -> tuple[int, int]:
    """返回控件的 ``(宽, 高)``，单位为终端列/行。

    理由：``Widget.size`` 由具名元组改为 ``Size`` 数据类，页面统一按二元组使用。
    """
    size = widget.size
    return int(size.width), int(size.height)


# endregion


# region 运行、鼠标与进度


def is_interactive_terminal() -> bool:
    """判断当前标准输入输出是否接在真实终端上。"""
    return bool(sys.stdin.isatty() and sys.stdout.isatty())


def set_text_selection(widget: Widget, enabled: bool) -> None:
    """开关鼠标拖选文本。

    :param widget: 目标控件。
    :param enabled: 为 ``False`` 时鼠标点击不再进入文本选择。

    理由：``ALLOW_SELECT`` 是较新版本才拆出的开关（早期只有 App 级），列表页靠它避免
    点击被解释成选择；该属性缺失时静默跳过，不影响键位操作。
    """
    if hasattr(widget, "ALLOW_SELECT"):
        try:
            widget.ALLOW_SELECT = enabled
        except AttributeError:
            return


def run_app(app: App[Any], *, mouse: bool = True, headless: bool = False) -> Any:
    """运行应用。

    :param app: 应用实例。
    :param mouse: 是否请求鼠标追踪；哑终端或 tmux 下可关闭以规避转义序列残留。
    :param headless: 是否无头运行，供自检使用。
    :return: ``App.run`` 的返回值。
    """
    return app.run(headless=headless, mouse=mouse)


@asynccontextmanager
async def app_test(app: App[Any], size: tuple[int, int] = (80, 24)) -> AsyncIterator[Pilot[Any]]:
    """以无头模式启动应用并交出 pilot，用于自动化断言。

    :param app: 应用实例。
    :param size: 虚拟终端尺寸，``(宽, 高)``，用于验证窄终端布局。

    理由：``run_test`` 的 ``headless`` 与 ``size`` 为关键字参数，早期版本没有 ``size``，
    统一由本包装提供默认 80×24。
    """
    async with app.run_test(headless=True, size=size) as pilot:
        yield pilot


def progress_phase(bar: ProgressBar, done: float, total: float = 100.0) -> None:
    """按「阶段」更新进度条。

    :param bar: 进度条控件。
    :param done: 已完成阶段数。
    :param total: 阶段总数。

    理由：子进程式安装拿不到字节级进度，只能按阶段推进；``ProgressBar`` 的
    ``advance`` 与 ``update(progress=...)`` 在不同版本可用性不同，统一走 ``update``。
    """
    bar.update(total=total, progress=done)


def progress_reset(bar: ProgressBar) -> None:
    """把进度条归零。"""
    bar.update(total=100.0, progress=0.0)


# endregion


# region 终端能力（自检报告用）


class TerminalCapability:
    """描述当前终端能验证到什么程度，供自检与 README 的结论表对齐。"""

    def __init__(self, name: str, available: bool, detail: str) -> None:
        self.name = name
        self.available = available
        self.detail = detail

    def __str__(self) -> str:
        state = i18n.t("cli.tui.selfcheck.available" if self.available else "cli.tui.selfcheck.unavailable")
        return i18n.t("cli.tui.selfcheck.capability", name=self.name, state=state, detail=self.detail)


def terminal_capabilities() -> Iterator[TerminalCapability]:
    """逐条报告终端能力，不猜测，只报告本机实际可观测到的事实。"""
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_interactive"),
        is_interactive_terminal(),
        f"stdin.isatty={sys.stdin.isatty()} stdout.isatty={sys.stdout.isatty()}",
    )
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_os"),
        True,
        f"{sys.platform} {os.environ.get('TERM') or i18n.t('cli.tui.selfcheck.term_unset')}",
    )
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_term_program"),
        bool(os.environ.get("TERM_PROGRAM")),
        os.environ.get("TERM_PROGRAM") or i18n.t("cli.tui.selfcheck.term_program_unset"),
    )
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_colorterm"),
        bool(os.environ.get("COLORTERM")),
        os.environ.get("COLORTERM") or i18n.t("cli.tui.selfcheck.not_set"),
    )
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_tmux"),
        bool(os.environ.get("TMUX")),
        os.environ.get("TMUX") or i18n.t("cli.tui.selfcheck.not_in_tmux"),
    )
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_ssh"),
        bool(os.environ.get("SSH_CONNECTION")),
        os.environ.get("SSH_CONNECTION") or i18n.t("cli.tui.selfcheck.not_ssh"),
    )
    frozen = bool(getattr(sys, "frozen", False)) or hasattr(sys, "__compiled__")
    yield TerminalCapability(
        i18n.t("cli.tui.selfcheck.cap_frozen"),
        frozen,
        i18n.t("cli.tui.selfcheck.frozen_flag" if frozen else "cli.tui.selfcheck.source_run"),
    )


# endregion
