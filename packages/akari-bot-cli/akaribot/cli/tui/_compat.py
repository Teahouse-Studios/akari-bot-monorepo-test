"""Textual 兼容层：TUI 内全部 Textual 用法经此收口。

上游 Textual 跨版本有 API 变动史——widget 的导出位置、消息类名、``Binding`` 构造参数、
``run`` / ``run_test`` 的关键字、CSS 属性的名称与取值、鼠标相关开关——把导入与调用集中在
本模块后，升级 Textual 只需改这一个文件。本模块只做再导出、薄包装与终端宽度计算，不含业务逻辑。

约定：``akaribot/cli/tui`` 下的其它模块一律 ``from akaribot.cli.tui import _compat as compat``，
不得直接 ``import textual``，也不得直接 ``import rich``。
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.resources
import os
import sys
import time
from collections.abc import AsyncIterator, Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import asynccontextmanager
from typing import Any

from rich.cells import cell_len, chop_cells, get_character_cell_size
from rich.markup import escape as _rich_escape
from rich.text import Text
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.css.stylesheet import Stylesheet
from textual.pilot import Pilot
from textual.reactive import reactive
from textual.css.query import NoMatches
from textual.screen import Screen
from textual.theme import Theme
from textual.worker import WorkerFailed
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, ListItem, ListView, ProgressBar, Static

from akaribot.cli import i18n

__all__ = [
    "AKARI_DARK_PALETTE",
    "AKARI_LIGHT_PALETTE",
    "AKARI_THEME_DARK",
    "AKARI_THEME_LIGHT",
    "App",
    "Binding",
    "BindingType",
    "Button",
    "Checkbox",
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
    "TextPromptScreen",
    "align_rows",
    "CONFIRM_DEBOUNCE_SECONDS",
    "PendingConfirm",
    "ButtonFlow",
    "HelpScreen",
    "ask_choice",
    "button_width",
    "mounted",
    "ask_text",
    "app_test",
    "bind",
    "bindings",
    "build_theme",
    "cell_width",
    "check_textual_version",
    "column_width",
    "display_width",
    "events",
    "fit_cells",
    "focus_first",
    "focus_now",
    "highlighted_index",
    "install_akari_themes",
    "is_interactive_terminal",
    "load_stylesheet",
    "notify",
    "on",
    "pad_cells",
    "plain_text",
    "pop_screen",
    "show_help",
    "progress_phase",
    "push_screen",
    "reactive",
    "read_resource_text",
    "resource_inventory",
    "run_app",
    "set_text_selection",
    "textual_version",
    "toggle_akari_theme",
    "truncate_cells",
    "wait_for_idle",
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


# region 品牌主题

# 主题名与调色板取自 character_marked.png（品牌立绘）：不透明部分以浅紫与粉色为主，暗部是深紫褐。
# 深色版取暗部作底、亮部作强调色；浅色版用图里的浅底与深色描边。语义色按同一色相家族调和。
AKARI_THEME_DARK = "akari-dark"
AKARI_THEME_LIGHT = "akari-light"

AKARI_DARK_PALETTE: dict[str, str] = {
    "primary": "#d69cdd",
    "secondary": "#f5b8e0",
    "accent": "#fbc1ed",
    "foreground": "#f7e5fa",
    "background": "#17101a",
    "surface": "#221726",
    "panel": "#2c1e31",
    "success": "#9ed7a6",
    "warning": "#f2c48a",
    "error": "#f2809b",
}
AKARI_LIGHT_PALETTE: dict[str, str] = {
    "primary": "#8e4f9e",
    "secondary": "#b361a8",
    "accent": "#c2499e",
    "foreground": "#3a2438",
    "background": "#fdfbf5",
    "surface": "#f9e6f6",
    "panel": "#f2d3fd",
    "success": "#2f7d4f",
    "warning": "#8a5a12",
    "error": "#b3324f",
}


def build_theme(name: str, palette: Mapping[str, str], *, dark: bool) -> Theme:
    """按调色板构造主题对象。

    :param name: 主题名。
    :param palette: 颜色映射，键同 :class:`~textual.theme.Theme` 的字段名。
    :param dark: 是否为深色主题。
    :return: 主题对象。
    """
    return Theme(name=name, dark=dark, **palette)


def install_akari_themes(app: App[Any], *, dark: bool = True) -> str:
    """注册品牌主题并激活其中一个。

    :param app: 应用实例。
    :param dark: 为真时激活深色版，否则激活浅色版。
    :return: 激活的主题名。
    """
    app.register_theme(build_theme(AKARI_THEME_DARK, AKARI_DARK_PALETTE, dark=True))
    app.register_theme(build_theme(AKARI_THEME_LIGHT, AKARI_LIGHT_PALETTE, dark=False))
    chosen = AKARI_THEME_DARK if dark else AKARI_THEME_LIGHT
    app.theme = chosen
    return chosen


def toggle_akari_theme(app: App[Any]) -> str:
    """在品牌深色与浅色主题之间切换。

    :param app: 应用实例。
    :return: 切换后的主题名。
    """
    chosen = AKARI_THEME_LIGHT if app.theme == AKARI_THEME_DARK else AKARI_THEME_DARK
    app.theme = chosen
    return chosen


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


def bindings(*items: tuple[str, str, str] | tuple[str, str, str, bool]) -> list[BindingType]:
    """批量构造键位绑定。

    每项为 ``(key, action, description)`` 或 ``(key, action, description, show)``：四元组的第 4 项为
    ``False`` 时该键位不进页脚，用于低频或危险动作——页脚在 80 列终端下装不下十几条键位。
    """
    result: list[BindingType] = []
    for item in items:
        key, action, description, *rest = item
        result.append(bind(key, action, description, show=rest[0] if rest else True))
    return result


# 模态确认的连发闸门：鼠标双击与键盘连发会在几十毫秒内送来同一个动作的两次请求，第二次会把
# 确认框叠成两层——用户答的是下面那层。故同一个目标在最短间隔内只接受一次。
CONFIRM_DEBOUNCE_SECONDS = 0.4


class PendingConfirm:
    """破坏性动作弹确认框前的连发闸门。

    页面在弹框前调用 :meth:`accept`：返回 ``False`` 表示这是防抖窗口内的重复触发，调用方应直接
    返回（既不弹框也不执行）。:meth:`reset` 在切页、刷新、换选中项时清掉记录，下一次触发立即放行。
    """

    # 防抖窗口做成类属性：生产路径用模块常量，自动化断言可以压缩等待——用例里的两次触发只隔
    # 几毫秒，按真实窗口会让每条确认都多等 0.4 秒。
    debounce: float = CONFIRM_DEBOUNCE_SECONDS

    def __init__(self) -> None:
        self.key = ""
        self.at = 0.0

    def accept(self, key: str, *, now: float | None = None) -> bool:
        """是否接受这次触发。

        :param key: 目标标识，如动作名或记录主键；换目标立即放行。
        :param now: 当前时刻，缺省取 :func:`time.monotonic`；用例注入以求可断言。
        :return: ``True`` 表示应当继续弹确认框。
        """
        moment = time.monotonic() if now is None else now
        if self.key == key and moment - self.at < self.debounce:
            return False
        self.key = key
        self.at = moment
        return True

    def reset(self) -> None:
        """清掉记录，下一次触发立即放行。"""
        self.key = ""
        self.at = 0.0


def highlighted_index(list_view: ListView) -> int | None:
    """取当前高亮项下标，无高亮时返回 ``None``。

    理由：``ListView.index`` 与 ``highlighted_child`` 的语义在版本间有出入，统一读 ``index``。
    """
    index = getattr(list_view, "index", None)
    return index if isinstance(index, int) and index >= 0 else None


async def wait_for_idle(app: App[Any], is_busy: Callable[[], bool], *, timeout: float = 30.0) -> bool:
    """等到页面既不忙、也没有未完成的后台任务。

    ``workers.wait_for_complete()`` 在任务刚被 ``run_worker`` 调度、尚未注册时会立即返回，只靠它
    判断会让自动化断言读到中间状态（实测同一用例在全量运行下偶发失败、单独运行必过）。故先等
    worker 队列，再看页面自己的忙碌标志，两轮都空闲才算结束。

    :param app: 应用实例。
    :param is_busy: 返回页面是否仍在处理中。
    :param timeout: 最长等待秒数。
    :return: 是否在超时前进入空闲。
    """
    deadline = time.monotonic() + timeout
    while True:
        await app.workers.wait_for_complete()
        if not is_busy():
            return True
        if time.monotonic() >= deadline:
            return False
        await asyncio.sleep(0.02)


def focus_now(widget: Widget) -> bool:
    """立即把焦点交给控件，不等下一轮消息。

    ``Widget.focus()`` 内部走 ``call_later``，真正生效要等下一次消息循环。隐藏旧页时 Textual 会
    先 ``blur()`` 并改派焦点，延后的那次聚焦就晚了——隐藏页里的滚动容器会拿到焦点，那一页的键位
    随之生效。切页时先同步聚焦目标页，旧页隐藏时便不再触发改派。

    :param widget: 目标控件。
    :return: 是否同步设置成功；失败时退回常规的延后聚焦。
    """
    try:
        widget.screen.set_focus(widget)
    except Exception:  # noqa: BLE001 - 未挂载或 Textual 内部签名变动时退回常规路径
        widget.focus()
        return False
    return True


def focus_first(page: Widget, *selectors: str) -> bool:
    """按顺序把焦点交给第一个可用的候选控件，全都不行时聚焦页面本身。

    Textual 拒绝聚焦空的 ``ListView``：``focus()`` 静默失效，``app.focused`` 仍为 ``None``。
    列表尚在加载或实例里没有数据时，切页后焦点因此悬空，页级键位全部不响应。故列表为空时
    退到下一个候选，最后兜底到页面容器。

    聚焦走 :func:`focus_now` 而非 ``Widget.focus()``：后者延迟到下一轮消息，切页隐藏旧页时会被
    Textual 的改派抢在前面。

    :param page: 页面控件。
    :param selectors: 候选控件的 CSS 选择器，按优先级排列。
    :return: 是否把焦点交给了候选控件（``False`` 表示落到了页面容器上）。
    """
    for selector in selectors:
        try:
            widget = page.query_one(selector)
        except Exception:  # noqa: BLE001 - 候选控件可能尚未装配，跳过即可
            continue
        if isinstance(widget, ListView) and len(widget) == 0:
            continue
        focus_now(widget)
        return True
    focus_now(page)
    return False


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


def push_screen(app: App[Any], screen: Screen[Any] | str, callback: Callable[[Any], None] | None = None) -> Any:
    """推入一个页面，可选地把关闭结果交给回调。

    理由：``push_screen`` 的 ``callback`` / ``wait_for_dismiss`` / ``mode`` 参数是逐版本加上的；
    回调存在时按关键字传入，不存在时保持只传页面对象。
    """
    if callback is None:
        return app.push_screen(screen)
    return app.push_screen(screen, callback)


class TextPromptScreen(Screen[str | None]):
    """单行文本输入的模态框：回车或「确认」提交，「取消」或 Esc 返回 ``None``。

    :param title: 标题。
    :param hint: 说明文字，写清提交后会发生什么。
    :param confirm_label: 确认按钮文字。
    :param cancel_label: 取消按钮文字。
    :param placeholder: 输入框占位符。
    :param initial: 输入框初始值。
    """

    DEFAULT_CSS = """
    TextPromptScreen {
        align: center middle;
    }
    TextPromptScreen #prompt-box {
        width: 72;
        max-width: 90%;
        height: auto;
        border: round $primary;
        background: $surface;
        padding: 1 1;
    }
    TextPromptScreen #prompt-title {
        text-style: bold;
    }
    TextPromptScreen #prompt-hint {
        color: $text-muted;
    }
    TextPromptScreen #prompt-actions {
        height: 3;
        align-horizontal: right;
    }
    """

    def __init__(
        self,
        *,
        title: str,
        hint: str = "",
        confirm_label: str,
        cancel_label: str,
        placeholder: str = "",
        initial: str = "",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.prompt_title = title
        self.prompt_hint = hint
        self.placeholder = placeholder
        self.initial = initial
        self.confirm_label = confirm_label
        self.cancel_label = cancel_label

    def compose(self) -> ComposeResult:
        """装配输入框与两个按钮。"""
        with Vertical(id="prompt-box"):
            yield Static(plain_text(self.prompt_title), id="prompt-title", markup=False)
            if self.prompt_hint:
                yield Static(plain_text(self.prompt_hint), id="prompt-hint", markup=False)
            yield Input(value=self.initial, placeholder=self.placeholder, id="prompt-input")
            with Horizontal(id="prompt-actions"):
                yield Button(self.confirm_label, id="prompt-confirm", variant="primary")
                yield Button(self.cancel_label, id="prompt-cancel")

    def on_mount(self) -> None:
        """打开即聚焦输入框。"""
        focus_now(self.query_one("#prompt-input", Input))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """回车提交。"""
        self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮提交或取消。"""
        if event.button.id == "prompt-confirm":
            self._submit()
        elif event.button.id == "prompt-cancel":
            self.dismiss(None)

    def key_escape(self) -> None:
        """Esc 取消。"""
        self.dismiss(None)

    def _submit(self) -> None:
        value = self.query_one("#prompt-input", Input).value.strip()
        self.dismiss(value or None)


def ask_text(
    app: App[Any],
    *,
    title: str,
    confirm_label: str,
    cancel_label: str,
    hint: str = "",
    placeholder: str = "",
    initial: str = "",
    callback: Callable[[str | None], None],
) -> None:
    """弹出单行输入框，把结果交给回调。

    ``push_screen`` 的 ``callback`` 参数是逐步加上的，故把回调包在页面里而不是交给 Textual。
    这里只推入页面，回调由 :meth:`TextPromptScreen.dismiss` 触发。
    """
    screen = TextPromptScreen(
        title=title,
        hint=hint,
        confirm_label=confirm_label,
        cancel_label=cancel_label,
        placeholder=placeholder,
        initial=initial,
    )
    push_screen(app, screen, callback)


class ChoiceScreen(Screen[str | None]):
    """多选一的模态框：每个选项一个按钮，Esc 或「取消」返回 ``None``。

    :param title: 标题。
    :param hint: 说明文字，写清各选项的差别。
    :param options: ``(取值, 按钮文字)`` 列表，按给出顺序排列。
    :param cancel_label: 取消按钮文字。
    """

    DEFAULT_CSS = """
    ChoiceScreen {
        align: center middle;
    }
    ChoiceScreen #choice-box {
        width: 72;
        max-width: 90%;
        height: auto;
        border: round $primary;
        background: $surface;
        padding: 1 1;
    }
    ChoiceScreen #choice-title {
        text-style: bold;
    }
    ChoiceScreen #choice-hint {
        color: $text-muted;
    }
    ChoiceScreen #choice-actions {
        height: auto;
        align-horizontal: right;
    }
    ChoiceScreen Button {
        margin: 0 0 0 1;
    }
    """

    def __init__(
        self,
        *,
        title: str,
        options: Sequence[tuple[str, str]],
        cancel_label: str,
        hint: str = "",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.choice_title = title
        self.choice_hint = hint
        self.options = tuple(options)
        self.cancel_label = cancel_label

    def compose(self) -> ComposeResult:
        """装配标题、说明与每个选项一个按钮。"""
        with Vertical(id="choice-box"):
            yield Static(plain_text(self.choice_title), id="choice-title", markup=False)
            if self.choice_hint:
                yield Static(plain_text(self.choice_hint), id="choice-hint", markup=False)
            with Horizontal(id="choice-actions"):
                for index, (_, label) in enumerate(self.options):
                    yield Button(label, id=f"choice-{index}", variant="primary" if index == 0 else "default")
                yield Button(self.cancel_label, id="choice-cancel")

    def on_mount(self) -> None:
        """打开即聚焦第一个选项，回车即选中它；没有选项时只留取消按钮。"""
        if self.options:
            focus_now(self.query_one("#choice-0", Button))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮即结果：取消按钮返回 ``None``。"""
        button_id = event.button.id or ""
        if button_id == "choice-cancel":
            self.dismiss(None)
            return
        if button_id.startswith("choice-"):
            index = int(button_id.removeprefix("choice-"))
            if 0 <= index < len(self.options):
                self.dismiss(self.options[index][0])

    def key_escape(self) -> None:
        """Esc 取消。"""
        self.dismiss(None)


def ask_choice(
    app: App[Any],
    *,
    title: str,
    options: Sequence[tuple[str, str]],
    cancel_label: str,
    callback: Callable[[str | None], None],
    hint: str = "",
) -> None:
    """弹出多选一的模态框，把选中的取值交给回调；取消时为 ``None``。"""
    push_screen(app, ChoiceScreen(title=title, options=options, cancel_label=cancel_label, hint=hint), callback)


ButtonSpec = tuple[str, str] | tuple[str, str, str]


def mounted(widget: Widget) -> bool:
    """控件是否还在控件树里。

    后台取数与定时轮询可能在页面卸载（切实例重挂载、退出界面）之后才落地，此时按 id 取控件会抛
    ``NoMatches``，界面退出时会连带把异常抛给用户。渲染入口先问一句再动手。
    """
    return bool(getattr(widget, "is_mounted", False))


def button_width(button: Button) -> int:
    """按钮占用的列数：标签宽度加左右各一格内边距。

    按钮没有边框，``padding`` 是 ``0 1``，故自然宽度就是标签宽度加二。
    """
    return display_width(str(button.label)) + 2


class ButtonFlow(Grid):
    """按可用宽度自动折行的按钮区。

    界面里一组动作（实例操作、环境装卸、解释器动作）在宽终端下一行放得下，窄终端下要折行；
    固定按两行摆放会在宽终端下空出整行高度与右侧大片空白。这里用网格摆放按钮：列数按自然宽度
    算出来，一行放得下就一行，放不下才折行，且优先在 ``breaks`` 标出的语义分组处断开。

    按钮始终是同一个控件、始终挂在树里（只换列数），故标签与禁用状态不会丢，页面随时可以按 id
    取用。列宽取该列最宽的那个按钮，行内因此对齐。

    :param specs: ``(id, 标签)`` 或 ``(id, 标签, variant)`` 序列，顺序即摆放顺序。
    :param breaks: 允许断行的位置，给出该组最后一个按钮的 ``id``；一组自身超宽时按按钮继续拆。
    """

    DEFAULT_CSS = """
    ButtonFlow {
        grid-columns: auto;
        grid-rows: auto;
        grid-gutter: 0;
        height: auto;
        width: 100%;
    }
    ButtonFlow Button {
        min-width: 0;
    }
    """

    def __init__(self, *specs: ButtonSpec, breaks: tuple[str, ...] = (), id: str | None = None) -> None:
        super().__init__(id=id)
        self._specs = specs
        self._breaks = breaks
        # 按钮只建一次并一直挂在树里：重排只改列数，标签与禁用状态都留着。
        self._buttons: dict[str, Button] = {}
        self._columns = 0

    def compose(self) -> ComposeResult:
        """按顺序装配按钮；列数在首次排布时按宽度算。"""
        for spec in self._specs:
            yield self._build(spec[0])

    def on_mount(self) -> None:
        """首次排布前算一次列数。"""
        self.relayout()

    def on_resize(self, event: events.Resize) -> None:
        """宽度变化后重算列数。"""
        self.relayout(event.size.width)

    def relayout(self, width: int | None = None) -> None:
        """按 ``width`` 重算列数；列数没变时不动样式。

        :param width: 可用列数；缺省取当前控件宽度。
        """
        available = self.size.width if width is None else width
        if available <= 0:
            return
        columns = self._columns_for(available)
        if columns == self._columns:
            return
        self._columns = columns
        self.styles.grid_size_columns = columns

    def _columns_for(self, width: int) -> int:
        # 列数按最长的那一行定：网格按行优先填充，行长即列数。列宽取该列最宽者（网格按列对齐），
        # 故还要按列宽复核总宽，超了就减一列重算。
        rows = self._pack(width)
        columns = max((len(row) for row in rows), default=1)
        while columns > 1 and self._grid_width(rows, columns) > width:
            columns -= 1
        return max(1, columns)

    def _grid_width(self, rows: tuple[tuple[str, ...], ...], columns: int) -> int:
        widest = [0] * columns
        for row in rows:
            for index, button_id in enumerate(row):
                if index < columns:
                    widest[index] = max(widest[index], self._natural_width(button_id))
        return sum(widest)

    def _pack(self, width: int) -> tuple[tuple[str, ...], ...]:
        # 先按语义分组装：一组放得进当前行就并进去，放不进就换行；一组自身超宽时把它的按钮
        # 按宽度继续拆，保证窄终端下仍然不溢出。
        rows: list[list[str]] = []
        current: list[str] = []
        used = 0
        for group in self._groups():
            need = sum(self._natural_width(spec[0]) for spec in group)
            if current and used + need > width:
                rows.append(current)
                current, used = [], 0
            for spec in group:
                button_id = spec[0]
                item = self._natural_width(button_id)
                if current and used + item > width:
                    rows.append(current)
                    current, used = [], 0
                current.append(button_id)
                used += item
        if current:
            rows.append(current)
        return tuple(tuple(row) for row in rows)

    def _natural_width(self, button_id: str) -> int:
        # 以控件当前的标签为准：状态改写会换标签（安装服务 / 卸载服务），装箱要跟着变；
        # 不适用的按钮会被页面隐藏（display=False），它们不占宽度也不该触发折行。
        button = self._buttons.get(button_id)
        if button is not None:
            return 0 if button.display is False else button_width(button)
        for spec in self._specs:
            if spec[0] == button_id:
                return display_width(spec[1]) + 2
        return 0

    def _groups(self) -> list[list[ButtonSpec]]:
        groups: list[list[ButtonSpec]] = []
        current: list[ButtonSpec] = []
        for spec in (item for item in self._specs if self._natural_width(item[0]) > 0):
            current.append(spec)
            if spec[0] in self._breaks:
                groups.append(current)
                current = []
        if current:
            groups.append(current)
        return groups

    def _build(self, button_id: str) -> Button:
        cached = self._buttons.get(button_id)
        if cached is not None:
            return cached
        for spec in self._specs:
            if spec[0] == button_id:
                variant = spec[2] if len(spec) > 2 else "default"
                button = Button(spec[1], id=button_id, variant=variant)
                self._buttons[button_id] = button
                return button
        raise KeyError(button_id)


class HelpScreen(Screen[None]):
    """当前页键位一览的浮层：列出本页与全局键位，Esc / q / ? 关闭。

    :param title: 标题。
    :param hint: 说明文字。
    :param rows: ``(键位, 说明)`` 列表，按展示顺序。
    :param close_label: 关闭按钮文字。
    """

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    HelpScreen #help-box {
        width: 88;
        max-width: 94%;
        height: 80%;
        border: round $primary;
        background: $surface;
        padding: 1 1;
    }
    HelpScreen #help-title {
        text-style: bold;
    }
    HelpScreen #help-hint {
        color: $text-muted;
    }
    HelpScreen #help-list {
        height: 1fr;
    }
    HelpScreen #help-actions {
        height: 3;
        align-horizontal: right;
    }
    """

    def __init__(
        self,
        *,
        title: str,
        rows: Sequence[tuple[str, str]],
        close_label: str,
        hint: str = "",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.help_title = title
        self.help_hint = hint
        self.rows = tuple(rows)
        self.close_label = close_label

    def compose(self) -> ComposeResult:
        """装配标题、说明与键位清单。"""
        with Vertical(id="help-box"):
            yield Static(plain_text(self.help_title), id="help-title", markup=False)
            if self.help_hint:
                yield Static(plain_text(self.help_hint), id="help-hint", markup=False)
            yield ListView(
                *[
                    ListItem(Static(plain_text(_help_row(key, description)), markup=False))
                    for key, description in self.rows
                ],
                id="help-list",
            )
            with Horizontal(id="help-actions"):
                yield Button(self.close_label, id="help-close", variant="primary")

    def on_mount(self) -> None:
        """打开即聚焦关闭按钮。"""
        focus_now(self.query_one("#help-close", Button))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """关闭按钮即关闭。"""
        if event.button.id == "help-close":
            self.dismiss(None)

    def key_escape(self) -> None:
        """Esc 关闭。"""
        self.dismiss(None)

    def key_q(self) -> None:
        """q 关闭。"""
        self.dismiss(None)

    def key_question_mark(self) -> None:
        """再按一次 ? 关闭。"""
        self.dismiss(None)


def _help_row(key: str, description: str) -> str:
    return f"{key:<14} {description}"


def show_help(
    app: App[Any],
    *,
    title: str,
    rows: Sequence[tuple[str, str]],
    close_label: str,
    hint: str = "",
) -> None:
    """弹出键位一览浮层。"""
    push_screen(app, HelpScreen(title=title, rows=rows, close_label=close_label, hint=hint))


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
    :param size: 虚拟终端尺寸，``(宽， 高)``，用于验证窄终端布局。

    理由：``run_test`` 的 ``headless`` 与 ``size`` 为关键字参数，早期版本没有 ``size``，
    统一由本包装提供默认 80×24。另外吞掉退出阶段的 ``NoMatches``：取数与轮询可能在页面卸载之后
    才落地，``run_test`` 会把这类 ``WorkerFailed`` 当成用例失败抛出，而界面此时已经在关闭，
    用户看不到任何异常（各页渲染入口另有 ``mounted()`` 判断，这里是兜底）。
    """
    try:
        async with app.run_test(headless=True, size=size) as pilot:
            yield pilot
    except WorkerFailed as error:
        if app.is_running or not isinstance(error.__cause__, NoMatches):
            raise


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
