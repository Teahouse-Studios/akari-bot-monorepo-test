"""Textual 兼容接口、终端宽度计算与公共控件。

TUI 的其他模块通过本模块使用 Textual 和 Rich。
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.resources
import logging
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
import functools

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

_logger = logging.getLogger(__name__)

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
    "NoMatches",
    "Pilot",
    "ProgressBar",
    "RenderGuard",
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
    "guard_renders",
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

兼容接口以此版本为依据，版本不匹配时自检报告错误。
"""

KEY_ALIASES = {
    "solidus": "slash",
    "forward_slash": "slash",
    "esc": "escape",
    "return": "enter",
}
"""键名别名表。

Textual 的键名以 ``slash`` 表示 ``/``；绑定时将 Unicode 名称等别名统一为该键名。
"""


def textual_version() -> str:
    """返回运行期 Textual 版本号。"""
    module = importlib.import_module("textual")
    return str(getattr(module, "__version__", "unknown"))


def check_textual_version(pin: str = TEXTUAL_PIN) -> tuple[bool, str]:
    """检查运行期 Textual 版本是否符合依赖约束。

    :param pin: 要求的版本。
    :return: 版本是否匹配及检查结果说明。
    """
    found = textual_version()
    return found == pin, i18n.t("cli.tui.selfcheck.textual_version", pin=pin, found=found)


# region 宽度计算（中文宽字符对齐）

# 码点数量与终端列宽不同；宽度计算使用与 Textual 一致的 rich.cells。


def cell_width(char: str) -> int:
    """返回单个字符占用的终端列数。"""
    return get_character_cell_size(char)


def display_width(text: str) -> int:
    """返回字符串占用的终端列数，中文与 emoji 按 2 列计。"""
    return cell_len(text)


def truncate_cells(text: str, width: int, ellipsis: str = "…") -> str:
    """按终端列宽截断，保持宽字符完整；被截断时补省略号。

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
    """将两列文本按显示宽度对齐。

    :param rows: 二元组序列——左列（标签）与右列（值）。
    :param gap: 两列之间的空格数。
    :param align: 左列对齐方式。
    :return: 每行一条、左列已补齐的文本。
    """
    label_width = column_width(label for label, _ in rows)
    return [f"{pad_cells(label, label_width, align)}{' ' * gap}{value}" for label, value in rows]


# endregion


# region 包内资源与样式表

# 冻结环境中的源文件路径不可用，样式表通过包内资源读取；资源缺失时使用内联样式。


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
    """解析样式表并校验主题变量。

    :param css: 样式表文本。
    :param path: 错误信息中的文件名。
    :param app: 提供主题变量的应用实例。
    :return: 解析后的样式表。
    """
    sheet = Stylesheet(variables=app.get_css_variables() if app is not None else None)
    sheet.add_source(css, read_from=("tui", path))
    sheet.parse()
    return sheet


# endregion


# region 品牌主题

# 调色板取自品牌立绘 character_marked.png，并分别适配深色与浅色背景。
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


def bind(key: str, action: str, description: str, *, show: bool = True) -> BindingType:
    """构造快捷键绑定并规范键名。

    :param key: 键名，如 ``q``、``ctrl+r``。
    :param action: 对应的动作名。
    :param description: 快捷键说明。
    :param show: 是否在页脚显示。
    :return: Textual 绑定对象。
    """
    return Binding(KEY_ALIASES.get(key, key), action, description, show=show)


def bindings(*items: tuple[str, str, str] | tuple[str, str, str, bool]) -> list[BindingType]:
    """批量构造快捷键绑定。

    :param items: 三元组 ``(key, action, description)`` 或含 ``show`` 的四元组。
    :return: 绑定列表；``show=False`` 的快捷键不在页脚显示。
    """
    result: list[BindingType] = []
    for item in items:
        key, action, description, *rest = item
        result.append(bind(key, action, description, show=rest[0] if rest else True))
    return result


# 双击与按键连发可能重复触发同一请求，防抖窗口用于防止确认框重复打开。
CONFIRM_DEBOUNCE_SECONDS = 0.4


class PendingConfirm:
    """确认请求的防抖记录。

    同一目标在防抖窗口内仅接受一次请求；切页、刷新或选择变化时应清除记录。
    """

    # 允许测试调整防抖窗口，避免依赖固定的实际等待时间。
    debounce: float = CONFIRM_DEBOUNCE_SECONDS

    def __init__(self) -> None:
        self.key = ""
        self.at = 0.0

    def accept(self, key: str, *, now: float | None = None) -> bool:
        """判断是否接受确认请求。

        :param key: 操作目标标识。
        :param now: 当前时间，默认使用单调时钟。
        :return: 是否可打开确认框。
        """
        moment = time.monotonic() if now is None else now
        if self.key == key and moment - self.at < self.debounce:
            return False
        self.key = key
        self.at = moment
        return True

    def reset(self) -> None:
        """清除防抖记录。"""
        self.key = ""
        self.at = 0.0


def highlighted_index(list_view: ListView) -> int | None:
    """返回当前高亮项索引，无高亮项时返回 ``None``。"""
    index = getattr(list_view, "index", None)
    return index if isinstance(index, int) and index >= 0 else None


async def wait_for_idle(app: App[Any], is_busy: Callable[[], bool], *, timeout: float = 30.0) -> bool:
    """等待后台任务与页面操作均完成。

    :param app: 应用实例。
    :param is_busy: 返回页面是否仍在处理操作。
    :param timeout: 最长等待秒数。
    :return: 是否在超时前进入空闲状态。
    """
    # 任务注册可能延迟，需同时检查 worker 队列与页面忙碌状态。
    deadline = time.monotonic() + timeout
    while True:
        await app.workers.wait_for_complete()
        if not is_busy():
            return True
        if time.monotonic() >= deadline:
            return False
        await asyncio.sleep(0.02)


def focus_now(widget: Widget) -> bool:
    """同步设置控件焦点。

    :param widget: 目标控件。
    :return: 是否同步设置成功；失败时使用异步聚焦。
    """
    # 同步聚焦可避免切页时 Textual 将焦点分配给隐藏页面。
    try:
        widget.screen.set_focus(widget)
    except Exception:  # noqa: BLE001 - 未挂载或 Textual 内部签名变动时退回常规路径
        widget.focus()
        return False
    return True


def focus_first(page: Widget, *selectors: str) -> bool:
    """聚焦首个可用的候选控件；无可用候选时聚焦页面容器。

    :param page: 页面控件。
    :param selectors: 按优先级排列的 CSS 选择器。
    :return: 是否聚焦候选控件。
    """
    # 空列表不可聚焦，需保留后续候选与页面容器作为回退目标。
    for selector in selectors:
        try:
            widget = page.query_one(selector)
        except Exception:  # noqa: BLE001 - 跳过尚未装配的候选控件
            continue
        if isinstance(widget, ListView) and len(widget) == 0:
            continue
        focus_now(widget)
        return True
    focus_now(page)
    return False


def plain_text(value: str, style: str | None = None) -> Text:
    """构造不解析标记的富文本。

    :param value: 原始文本。
    :param style: 可选的 Rich 样式名。
    :return: 可用于 ``Static.update`` 的文本对象。
    """
    return Text(value, style=style)


def escape_markup(value: str) -> str:
    """转义文本中的标记字符，仅在确实需要拼接标记时使用。"""
    return _rich_escape(value)


def notify(app: App[Any], message: str, *, severity: str = "information", title: str = "") -> None:
    """显示通知；未挂载或不支持通知时返回。"""
    notify_fn = getattr(app, "notify", None)
    if notify_fn is None:
        return
    try:
        notify_fn(message, title=title, severity=severity)
    except Exception:  # noqa: BLE001 - 通知失败不应中断界面操作
        return


def push_screen(app: App[Any], screen: Screen[Any] | str, callback: Callable[[Any], None] | None = None) -> Any:
    """打开页面，并通过可选回调传递关闭结果。"""
    if callback is None:
        return app.push_screen(screen)
    return app.push_screen(screen, callback)


class TextPromptScreen(Screen[str | None]):
    """单行文本输入的模态框：回车或「确认」提交，「取消」或 Esc 返回 ``None``。

    :param title: 标题。
    :param hint: 操作后果说明。
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
        max-height: 90%;
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
    TextPromptScreen #prompt-description {
        height: 1fr;
        min-height: 1;
        overflow-x: hidden;
    }
    TextPromptScreen #prompt-actions {
        height: auto;
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
            with VerticalScroll(id="prompt-description"):
                yield Static(plain_text(self.prompt_title), id="prompt-title", markup=False)
                if self.prompt_hint:
                    yield Static(plain_text(self.prompt_hint), id="prompt-hint", markup=False)
            yield Input(value=self.initial, placeholder=self.placeholder, id="prompt-input")
            yield ButtonFlow(
                ("prompt-confirm", self.confirm_label, "primary"),
                ("prompt-cancel", self.cancel_label),
                id="prompt-actions",
            )

    def on_mount(self) -> None:
        """打开即聚焦输入框。"""
        focus_now(self.query_one("#prompt-input", Input))
        self.call_after_refresh(_fit_dialog, self, "prompt", 3)

    def on_resize(self, event: events.Resize) -> None:
        self.call_after_refresh(_fit_dialog, self, "prompt", 3)

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
    """打开单行输入框，通过回调返回输入值；取消时返回 ``None``。"""
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
    :param hint: 选项说明。
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
        max-height: 90%;
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
    ChoiceScreen #choice-description {
        height: 1fr;
        min-height: 1;
        overflow-x: hidden;
    }
    ChoiceScreen #choice-actions {
        height: auto;
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
            with VerticalScroll(id="choice-description"):
                yield Static(plain_text(self.choice_title), id="choice-title", markup=False)
                if self.choice_hint:
                    yield Static(plain_text(self.choice_hint), id="choice-hint", markup=False)
            yield ButtonFlow(
                *(
                    (f"choice-{index}", label, "primary" if index == 0 else "default")
                    for index, (_, label) in enumerate(self.options)
                ),
                ("choice-cancel", self.cancel_label),
                id="choice-actions",
            )

    def on_mount(self) -> None:
        """聚焦首个选项；无选项时聚焦取消按钮。"""
        if self.options:
            focus_now(self.query_one("#choice-0", Button))
        else:
            focus_now(self.query_one("#choice-cancel", Button))
        self.call_after_refresh(_fit_dialog, self, "choice")

    def on_resize(self, event: events.Resize) -> None:
        self.call_after_refresh(_fit_dialog, self, "choice")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """返回选项值；取消按钮返回 ``None``。"""
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


def _fit_dialog(screen: Screen[Any], prefix: str, input_height: int = 0) -> None:
    if not screen.is_mounted:
        return
    box = screen.query_one(f"#{prefix}-box")
    description = screen.query_one(f"#{prefix}-description")
    actions = screen.query_one(f"#{prefix}-actions", ButtonFlow)
    actions.relayout()
    buttons = list(actions.query(Button))
    rows = (len(buttons) + actions._columns - 1) // max(actions._columns, 1)
    action_height = rows * max((button.region.height for button in buttons), default=3)
    width = max(description.scrollable_content_region.width, 1)
    text_height = sum(child.get_content_height(description.size, screen.size, width) for child in description.children)
    desired = text_height + action_height + input_height + box.styles.gutter.height
    box.styles.height = min(desired, max(int(screen.size.height * 0.9), 1))


ButtonSpec = tuple[str, str] | tuple[str, str, str]


def mounted(widget: Widget) -> bool:
    """判断控件当前是否允许访问子控件。

    应用退出、控件正在移除或已卸载时返回 ``False``；首次挂载期间允许访问。
    """
    # Textual 先卸载子控件，父控件的 is_mounted 可能尚未更新。
    app = getattr(widget, "app", None)
    if bool(getattr(app, "_exit", False)) or not bool(getattr(app, "is_running", True)):
        return False
    if bool(getattr(widget, "_pruning", False)):
        return False
    if getattr(widget, "_tui_mounted_once", False) and not getattr(widget, "is_mounted", False):
        return False
    return True


class RenderGuard:
    """记录页面不可用时跳过的渲染次数及最近一次方法名。"""

    def __init__(self) -> None:
        self._skipped_renders = 0
        self._last_skipped_method = ""

    @property
    def skipped_renders(self) -> int:
        """因页面不可用而跳过的渲染次数。"""
        return self._skipped_renders

    @property
    def last_skipped_method(self) -> str:
        """最近一次因页面不可用而跳过的渲染方法名，未跳过时为空串。"""
        return self._last_skipped_method

    def _record_skip(self, method: str) -> None:
        self._skipped_renders += 1
        self._last_skipped_method = method


def guard_renders(page: Widget) -> None:
    """为页面渲染方法添加生命周期检查。

    页面不可用时跳过渲染并记录统计；页面可用时保留选择器异常。
    """
    page._tui_mounted_once = False
    page.render_guard = RenderGuard()
    _guard_mount(page)
    for name in dir(type(page)):
        if not name.startswith(("_render", "_sync", "_set_", "_paint")):
            continue
        method = getattr(page, name, None)
        if not callable(method):
            continue
        setattr(page, name, _guarded(page, method))


def _guard_mount(page: Widget) -> None:
    # 首次 on_mount 需要执行渲染，卸载检查仅适用于已完成挂载的页面。
    original = getattr(page, "on_mount", None)

    def on_mount() -> None:
        if original is not None:
            original()
        page._tui_mounted_once = True

    page.on_mount = on_mount


def _guarded(page: Widget, method: Callable[..., Any]) -> Callable[..., Any]:
    # 实例属性不参与描述符绑定，闭包须保留页面对象与已绑定方法。
    name = getattr(method, "__name__", "")

    @functools.wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not mounted(page):
            _record_skip(page, name)
            return None
        try:
            return method(*args, **kwargs)
        except NoMatches:
            # 检查后仍可能发生卸载，仅在控件不可用时忽略此竞态产生的异常。
            if mounted(page):
                raise
            _record_skip(page, name)
            return None

    return wrapper


def _record_skip(page: Widget, method: str) -> None:
    guard = page.render_guard
    guard._record_skip(method)
    _logger.debug(
        "TUI render skipped: page=%s method=%s skipped=%d", type(page).__name__, method, guard.skipped_renders
    )


def button_width(button: Button) -> int:
    """返回按钮的自然列宽，包括左右内边距。"""
    return display_width(str(button.label)) + 2


class ButtonFlow(Grid):
    """按可用宽度折行排列按钮，并保留控件状态。

    :param specs: ``(id, 标签)`` 或 ``(id, 标签, variant)`` 序列。
    :param breaks: 优先断行位置，各项为分组末尾按钮的标识。
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
        max-width: 100%;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(self, *specs: ButtonSpec, breaks: tuple[str, ...] = (), id: str | None = None) -> None:
        super().__init__(id=id)
        self._specs = specs
        self._breaks = breaks
        # 重排保留按钮实例，避免丢失标签、禁用状态或焦点。
        self._buttons: dict[str, Button] = {}
        self._columns = 0

    def compose(self) -> ComposeResult:
        """按声明顺序创建按钮。"""
        for spec in self._specs:
            yield self._build(spec[0])

    def on_mount(self) -> None:
        """首次排布前算一次列数。"""
        self.relayout()

    def on_resize(self, event: events.Resize) -> None:
        """宽度变化后重算列数。"""
        self.relayout()

    def relayout(self, width: int | None = None) -> None:
        """按 ``width`` 重算列数与列宽。

        :param width: 可用列数；缺省取当前控件宽度。
        """
        available = self.size.width if width is None else width
        if available <= 0:
            return
        columns = self._columns_for(available)
        self._columns = columns
        self.styles.grid_size_columns = columns
        self.styles.grid_columns = " ".join(str(min(value, available)) for value in self._column_widths(columns))

    def _columns_for(self, width: int) -> int:
        # 网格按列对齐，须复核每列最大宽度之和，避免长短标签混排时溢出。
        rows = self._pack(width)
        columns = max((len(row) for row in rows), default=1)
        while columns > 1 and sum(self._column_widths(columns)) > width:
            columns -= 1
        return max(1, columns)

    def _column_widths(self, columns: int) -> list[int]:
        widest = [0] * columns
        visible = [spec[0] for spec in self._specs if self._natural_width(spec[0]) > 0]
        for index, button_id in enumerate(visible):
            column = index % columns
            widest[column] = max(widest[column], self._natural_width(button_id))
        return widest

    def _pack(self, width: int) -> tuple[tuple[str, ...], ...]:
        # 优先保留语义分组；单组超宽时允许在组内换行。
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
        # 状态切换可能修改标签或隐藏按钮，宽度应以当前可见内容为准。
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
    """快捷键帮助浮层：列出本页与全局快捷键，Esc / q / ? 关闭。

    :param title: 标题。
    :param hint: 说明文字。
    :param rows: ``(键位, 说明)`` 列表，按展示顺序。
    :param close_label: 关闭按钮文字。
    :param nav_hint: 固定的导航说明，各页相同。
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
    HelpScreen #help-nav {
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
        nav_hint: str = "",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.help_title = title
        self.help_hint = hint
        self.help_nav = nav_hint
        self.rows = tuple(rows)
        self.close_label = close_label

    def compose(self) -> ComposeResult:
        """装配标题、说明与键位清单。"""
        with Vertical(id="help-box"):
            yield Static(plain_text(self.help_title), id="help-title", markup=False)
            if self.help_hint:
                yield Static(plain_text(self.help_hint), id="help-hint", markup=False)
            if self.help_nav:
                yield Static(plain_text(self.help_nav), id="help-nav", markup=False)
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
    nav_hint: str = "",
) -> None:
    """打开快捷键帮助。"""
    push_screen(app, HelpScreen(title=title, rows=rows, close_label=close_label, hint=hint, nav_hint=nav_hint))


def pop_screen(app: App[Any]) -> Any:
    """弹出当前页面。"""
    return app.pop_screen()


def widget_cells(widget: Widget) -> tuple[int, int]:
    """返回控件宽度和高度，单位分别为终端列和行。"""
    size = widget.size
    return int(size.width), int(size.height)


# endregion


# region 运行、鼠标与进度


def is_interactive_terminal() -> bool:
    """判断标准输入输出是否连接交互终端。"""
    return bool(sys.stdin.isatty() and sys.stdout.isatty())


def set_text_selection(widget: Widget, enabled: bool) -> None:
    """设置鼠标文本选择功能。

    :param widget: 目标控件。
    :param enabled: 是否允许选择文本。
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
    """以无头模式运行应用，并提供交互测试控制器。

    :param app: 应用实例。
    :param size: 虚拟终端尺寸，单位为列和行。
    """
    try:
        async with app.run_test(headless=True, size=size) as pilot:
            yield pilot
    except WorkerFailed as error:
        # 原始异常可能保存在 WorkerFailed.error 或 __cause__ 中，须检查两种来源。
        cause = getattr(error, "error", None) or error.__cause__
        if app.is_running or not isinstance(cause, NoMatches):
            raise


def progress_phase(bar: ProgressBar, done: float, total: float = 100.0) -> None:
    """按已完成阶段更新进度条。

    :param bar: 进度条控件。
    :param done: 已完成阶段数。
    :param total: 阶段总数。
    """
    bar.update(total=total, progress=done)


def progress_reset(bar: ProgressBar) -> None:
    """把进度条归零。"""
    bar.update(total=100.0, progress=0.0)


# endregion


# region 终端能力（自检报告用）


class TerminalCapability:
    """终端能力的检测结果。"""

    def __init__(self, name: str, available: bool, detail: str) -> None:
        self.name = name
        self.available = available
        self.detail = detail

    def __str__(self) -> str:
        state = i18n.t("cli.tui.selfcheck.available" if self.available else "cli.tui.selfcheck.unavailable")
        return i18n.t("cli.tui.selfcheck.capability", name=self.name, state=state, detail=self.detail)


def terminal_capabilities() -> Iterator[TerminalCapability]:
    """读取当前终端的环境信息及可用能力。"""
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
