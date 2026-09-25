"""命令页：把 CLI 的命令面完整搬进界面。

参数清单、默认值与帮助文本都取自 CLI 自身的命令树（Typer/Click），执行仍是 ``akaribot <子命令>``
子进程。CLI 新增子命令或参数后本页自动跟上，界面不需要跟着改；子进程的标准输入指向空设备，
需要交互确认的命令在这里会直接失败并回报退出码，不会与界面争抢键盘。
"""

from __future__ import annotations

import asyncio
import subprocess
from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.instance import default_instance_root
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process

KIND_ARGUMENT = "argument"
KIND_OPTION = "option"
KIND_FLAG = "flag"

# 命令树里不由本页收集的参数：帮助与版本由框架处理，实例根经环境变量钉住。
SKIPPED_PARAM_NAMES = frozenset({"help", "version", "ctx"})
SKIPPED_OPTS = frozenset({"--instance", "-I"})

# 输出面板保留的行数上限。命令可能输出上千行，全部留在控件里只会拖慢渲染。
OUTPUT_TAIL_LINES = 400
STREAM_TAIL_LINES = 40
NAME_WIDTH = 26
DEFAULT_TIMEOUT_SECONDS = 900.0


class CommandError(RuntimeError):
    """命令无法执行：必填参数缺失或参数取值非法。"""


@dataclass(frozen=True)
class CommandParam:
    """一个命令行参数。

    :param name: 参数名，与命令函数签名一致。
    :param kind: ``argument`` / ``option`` / ``flag``。
    :param flags: 主选项写法；位置参数为空。
    :param secondary: 取反写法，如 ``--no-color``。
    :param required: 是否必填。
    :param multiple: 是否可重复给出。
    :param default: 命令声明的默认值。
    :param help: 帮助文本，取自 CLI 自身。
    :param title: 展示名；留空时按参数名生成。
    """

    name: str
    kind: str
    flags: tuple[str, ...] = ()
    secondary: tuple[str, ...] = ()
    required: bool = False
    multiple: bool = False
    default: Any = None
    help: str = ""
    title: str = ""

    def primary(self) -> str:
        """返回主写法。"""
        return self.flags[0] if self.flags else self.name

    def label(self) -> str:
        """返回界面上的参数名。"""
        if self.title:
            return self.title
        if self.kind == KIND_ARGUMENT:
            return f"<{self.name}>"
        return " / ".join((*self.flags, *self.secondary))

    def marks(self) -> str:
        """返回必填与可重复的标记文本。"""
        marks: list[str] = []
        if self.required:
            marks.append(i18n.t("cli.tui.commands.mark_required"))
        if self.multiple:
            marks.append(i18n.t("cli.tui.commands.mark_multiple"))
        return " ".join(marks)

    def default_text(self) -> str:
        """返回预填进输入框的默认值；无标量默认值时为空白。"""
        if self.kind == KIND_FLAG or self.default is None:
            return ""
        if isinstance(self.default, str | int | float):
            return str(self.default)
        return ""

    def default_enabled(self) -> bool:
        """返回开关型参数的初始勾选状态。"""
        return self.kind == KIND_FLAG and bool(self.default)

    def negate(self) -> str:
        """返回取反写法；没有时返回空串。"""
        return self.secondary[0] if self.secondary else ""


@dataclass(frozen=True)
class CommandEntry:
    """一条可执行的 CLI 命令。

    :param path: 子命令路径，如 ``("module", "add")``。
    :param summary: 一句话说明，取自 CLI 自身。
    :param params: 需要界面收集的参数。
    """

    path: tuple[str, ...]
    summary: str = ""
    params: tuple[CommandParam, ...] = ()

    def name(self) -> str:
        """返回命令行写法。"""
        return " ".join(self.path)

    def search_text(self) -> str:
        """返回可搜索文本。"""
        return " ".join((self.name(), self.summary)).casefold()


@dataclass(frozen=True)
class CommandResult:
    """一次命令执行的结果。

    :param ok: 是否以 0 退出。
    :param code: 退出码；未起进程时为 ``-1``。
    :param tail: 输出尾部，供失败时展示。
    :param argv: 实际执行的参数（不含 CLI 入口本身）。
    """

    ok: bool
    code: int
    tail: str = ""
    argv: tuple[str, ...] = ()


@runtime_checkable
class CommandSource(Protocol):
    """命令执行者。"""

    async def run(self, args: Sequence[str], on_line: Callable[[str], None]) -> CommandResult:
        """执行一条命令，逐行回调输出。"""
        ...

    def stop(self) -> None:
        """请求终止当前命令；没有在跑的命令时不动作。"""
        ...


@runtime_checkable
class CommandCatalog(Protocol):
    """命令清单来源。"""

    def commands(self) -> Sequence[CommandEntry]:
        """返回全部可执行命令。"""
        ...


class StaticCommandCatalog:
    """固定清单，供自动化断言使用。

    :param entries: 命令条目。
    """

    def __init__(self, entries: Sequence[CommandEntry]) -> None:
        self._entries = tuple(entries)

    def commands(self) -> Sequence[CommandEntry]:
        """返回构造时给定的条目。"""
        return self._entries


class TyperCommandCatalog:
    """从 CLI 自身的 Typer 应用导出命令树。"""

    def commands(self) -> Sequence[CommandEntry]:
        """返回 CLI 注册的全部子命令。"""
        return build_catalog()


class StaticCommandSource:
    """固定输出，供自动化断言使用。

    :param lines: 逐行回调的输出。
    :param code: 退出码。
    """

    def __init__(self, *, lines: Sequence[str] = (), code: int = 0) -> None:
        self.lines = tuple(lines)
        self.code = code
        self.calls: list[tuple[str, ...]] = []
        self.stopped = 0

    async def run(self, args: Sequence[str], on_line: Callable[[str], None]) -> CommandResult:
        """见 :meth:`CommandSource.run`。"""
        self.calls.append(tuple(args))
        for line in self.lines:
            on_line(line)
        return CommandResult(self.code == 0, self.code, "\n".join(self.lines[-STREAM_TAIL_LINES:]), tuple(args))

    def stop(self) -> None:
        """见 :meth:`CommandSource.stop`。"""
        self.stopped += 1


class SubprocessCommandSource:
    """经子进程执行本 CLI 的任意子命令。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param timeout: 单条命令的秒数上限。
    """

    def __init__(self, *, root: Path | str | None = None, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self.root = Path(root).expanduser().resolve() if root is not None else default_instance_root()
        self.timeout = timeout
        self._process: asyncio.subprocess.Process | None = None

    async def run(self, args: Sequence[str], on_line: Callable[[str], None]) -> CommandResult:
        """见 :meth:`CommandSource.run`。

        语言随界面走：子进程在导入期读 ``--lang``，不传就会用默认语言输出，与界面语言不一致。
        """
        argv = cli_process.cli_argv("--lang", i18n.current_locale(), *args)
        try:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(self.root),
                stdin=subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=cli_process.cli_env(self.root),
            )
        except FileNotFoundError as error:
            raise CommandError(i18n.t("cli.tui.commands.err_exe_missing", path=argv[0], error=error)) from error
        except OSError as error:
            raise CommandError(i18n.t("cli.tui.commands.err_oserror", command=" ".join(args), error=error)) from error
        self._process = process
        tail: deque[str] = deque(maxlen=STREAM_TAIL_LINES)
        try:
            code = await asyncio.wait_for(self._pump(process, on_line, tail), timeout=self.timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            raise CommandError(
                i18n.t("cli.tui.commands.err_timeout", command=" ".join(args), seconds=f"{self.timeout:.0f}")
            ) from None
        finally:
            self._process = None
        return CommandResult(code == 0, code, "\n".join(tail), tuple(args))

    def stop(self) -> None:
        """见 :meth:`CommandSource.stop`。"""
        process = self._process
        if process is not None and process.returncode is None:
            process.terminate()

    @staticmethod
    async def _pump(process: asyncio.subprocess.Process, on_line: Callable[[str], None], tail: deque[str]) -> int:
        stream = process.stdout
        if stream is not None:
            async for raw in stream:
                line = raw.decode("utf-8", errors="replace").rstrip()
                if not line:
                    continue
                tail.append(line)
                on_line(line)
        return await process.wait()


def build_catalog() -> tuple[CommandEntry, ...]:
    """从 CLI 的 Typer 应用导出命令树。

    :return: 按命令行写法排序的命令条目。
    """
    # 延迟导入：main 会装配全部子命令模块，界面启动时没有必要把它们全部牵进来。
    import typer

    from akaribot.cli.main import app as typer_app

    root = typer.main.get_command(typer_app)
    entries: list[CommandEntry] = []
    _collect(root, (), entries)
    return tuple(sorted(entries, key=lambda entry: entry.path))


def _collect(group: Any, prefix: tuple[str, ...], out: list[CommandEntry]) -> None:
    commands = getattr(group, "commands", None)
    if not isinstance(commands, dict):
        return
    if prefix and not commands:
        # 单命令子应用把命令注册在分组回调上（``@app.callback()``），分组自身就是可执行命令。
        out.append(CommandEntry(path=prefix, summary=_summary(group), params=_params(group, passthrough=group)))
        return
    for name in sorted(commands):
        command = commands[name]
        if getattr(command, "hidden", False):
            continue
        path = (*prefix, str(name))
        if isinstance(getattr(command, "commands", None), dict):
            _collect(command, path, out)
            continue
        out.append(CommandEntry(path=path, summary=_summary(command), params=_params(command)))


def _summary(command: Any) -> str:
    getter = getattr(command, "get_short_help_str", None)
    if callable(getter):
        try:
            return str(getter(80)).strip()
        except Exception:  # noqa: BLE001 - 帮助文本缺失不该让整份清单取不到
            pass
    text = str(getattr(command, "help", "") or "").strip()
    return text.splitlines()[0] if text else ""


def _params(command: Any, *, passthrough: Any = None) -> tuple[CommandParam, ...]:
    found: list[CommandParam] = []
    for param in getattr(command, "params", ()):
        name = str(getattr(param, "name", "") or "")
        opts = tuple(getattr(param, "opts", ()) or ())
        if not name or name in SKIPPED_PARAM_NAMES or not getattr(param, "expose_value", True):
            continue
        if SKIPPED_OPTS.intersection(opts):
            continue
        if opts:
            kind = KIND_FLAG if getattr(param, "is_flag", False) else KIND_OPTION
        else:
            kind = KIND_ARGUMENT
        found.append(
            CommandParam(
                name=name,
                kind=kind,
                flags=opts,
                secondary=tuple(getattr(param, "secondary_opts", ()) or ()),
                required=bool(getattr(param, "required", False)),
                multiple=bool(getattr(param, "multiple", False)),
                default=getattr(param, "default", None),
                help=str(getattr(param, "help", "") or ""),
            )
        )
    if passthrough is not None and getattr(passthrough, "passthrough_extra_args", False):
        # 透传分组把未识别参数原样交给 core，界面用一个自由输入表达。
        found.append(
            CommandParam(
                name="extra",
                kind=KIND_ARGUMENT,
                multiple=True,
                help=i18n.t("cli.tui.commands.param_extra_help"),
                title=i18n.t("cli.tui.commands.param_extra"),
            )
        )
    return tuple(found)


class ParamRow(compat.Vertical):
    """一个命令参数的编辑行：参数名、帮助文本与控件。

    :param param: 参数定义。
    """

    def __init__(self, param: CommandParam) -> None:
        super().__init__()
        self.param = param

    def compose(self) -> compat.ComposeResult:
        """按参数类型装配控件。"""
        yield compat.Static(compat.plain_text(self._header()), classes="param-header", markup=False)
        if self.param.help:
            yield compat.Static(compat.plain_text(self.param.help), classes="param-help", markup=False)
        yield self._build_control()

    def _header(self) -> str:
        marks = self.param.marks()
        return f"{self.param.label()} {marks}".strip() if marks else self.param.label()

    def _build_control(self) -> compat.Widget:
        # 控件 id 按参数名生成：自动化断言与脚本据此直接定位某个参数。
        control_id = f"param-{self.param.name}"
        if self.param.kind == KIND_FLAG:
            return compat.Checkbox(
                label=i18n.t("cli.tui.commands.flag_label"),
                value=self.param.default_enabled(),
                id=control_id,
                classes="param-control",
            )
        return compat.Input(
            self.param.default_text(),
            placeholder=i18n.t("cli.tui.commands.param_placeholder"),
            id=control_id,
            classes="param-control",
        )

    def control(self) -> compat.Widget:
        """返回本行的输入控件。"""
        try:
            return self.query_one(".param-control")
        except Exception:  # noqa: BLE001 - 开关型控件不带类名，退回按控件类型取
            return self.query_one(compat.Checkbox)

    def argv(self) -> list[str]:
        """把当前取值展开成 argv 片段。

        :return: 参数片段；必填项为空时抛出 :class:`CommandError`。
        """
        control = self.control()
        if self.param.kind == KIND_FLAG:
            if bool(getattr(control, "value", False)):
                return [self.param.primary()]
            # 默认开启的开关取消勾选时要显式取反，否则子进程仍按默认值执行。
            if self.param.default_enabled() and self.param.negate():
                return [self.param.negate()]
            return []
        text = str(getattr(control, "value", "")).strip()
        if not text:
            if self.param.required:
                raise CommandError(i18n.t("cli.tui.commands.err_required", name=self.param.label()))
            return []
        values = text.split() if self.param.multiple else [text]
        if self.param.kind == KIND_ARGUMENT:
            return values
        flag = self.param.primary()
        expanded: list[str] = []
        for value in values:
            expanded.extend((flag, value))
        return expanded


class CommandsPage(compat.Vertical):
    """命令页控件。

    :param source: 命令执行者，缺省为 :class:`SubprocessCommandSource`。
    :param catalog: 命令清单来源，缺省为 :class:`TyperCommandCatalog`。
    """

    can_focus = True

    BINDINGS = compat.bindings(
        ("x", "run", i18n.t("cli.tui.commands.bind_run")),
        ("c", "clear_output", i18n.t("cli.tui.commands.bind_clear")),
        ("r", "reload_catalog", i18n.t("cli.tui.commands.bind_reload")),
        ("escape", "stop", i18n.t("cli.tui.commands.bind_stop")),
        ("slash", "focus_search", i18n.t("cli.tui.commands.bind_search")),
    )

    DEFAULT_CSS = """
    CommandsPage {
        layout: vertical;
        height: 1fr;
    }
    CommandsPage #search-row {
        height: 3;
        padding: 0 0 0 1;
    }
    CommandsPage #search {
        width: 1fr;
    }
    CommandsPage #command-list {
        height: 1fr;
        min-height: 5;
        border: round $primary;
    }
    CommandsPage #command-list > ListItem {
        padding: 0;
    }
    CommandsPage #command-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    CommandsPage #param-pane {
        height: auto;
        max-height: 12;
        border: round $panel;
        padding: 0 1;
    }
    CommandsPage .param-header {
        color: $text;
    }
    CommandsPage .param-help {
        color: $text-muted;
    }
    CommandsPage #output-pane {
        height: 1fr;
        min-height: 5;
        border: round $panel;
        padding: 0 1;
    }
    CommandsPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    CommandsPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    """

    def __init__(
        self,
        source: CommandSource | None = None,
        catalog: CommandCatalog | None = None,
        *,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: CommandSource = source if source is not None else SubprocessCommandSource()
        self.catalog: CommandCatalog = catalog if catalog is not None else TyperCommandCatalog()
        self.last_error: str = ""
        self.last_result: str = ""
        self._entries: tuple[CommandEntry, ...] = ()
        self._query: str = ""
        self._selected: str = ""
        self._busy: bool = False
        self._output: deque[str] = deque(maxlen=OUTPUT_TAIL_LINES)
        self._rendered_rows: tuple[str, ...] = ()
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.commands.search_placeholder"), id="search")
        yield compat.ListView(id="command-list")
        yield compat.VerticalScroll(id="param-pane")
        yield compat.VerticalScroll(compat.Static("", id="output-text", markup=False), id="output-pane")
        yield compat.Static(compat.plain_text(self._status_rendered), id="status", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.commands.button_run"), id="run", variant="primary")
            yield compat.Button(i18n.t("cli.tui.commands.button_clear"), id="clear")

    def on_mount(self) -> None:
        """装配后不做取数，等本页首次显示时再读命令树。"""
        self._render_rows()
        self._sync_actions()

    def activate(self) -> None:
        """首次显示时读取命令树。"""
        if self._activated:
            return
        self._activated = True
        self.reload_catalog()

    @property
    def entries(self) -> tuple[CommandEntry, ...]:
        """返回全部命令。"""
        return self._entries

    @property
    def visible_entries(self) -> tuple[CommandEntry, ...]:
        """返回应用当前搜索词后的命令。"""
        if not self._query.strip():
            return self._entries
        return tuple(entry for entry in self._entries if entry.search_text().find(self._query.strip().casefold()) >= 0)

    @property
    def selected_entry(self) -> CommandEntry | None:
        """返回列表当前高亮项对应的命令。"""
        entries = self.visible_entries
        if not entries:
            return None
        try:
            list_view = self.query_one("#command-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(entries):
            return None
        return entries[index]

    @property
    def status_text(self) -> str:
        """返回最近一次写入状态栏的文本。"""
        return self._status_rendered

    @property
    def output_text(self) -> str:
        """返回输出面板的当前文本。"""
        return "\n".join(self._output)

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的列表行文本，供自动化断言核对。"""
        return self._rendered_rows

    def reload_catalog(self) -> bool:
        """重新读取命令树。

        :return: 是否读取成功。
        """
        try:
            entries = tuple(self.catalog.commands())
        except Exception as error:  # noqa: BLE001 - 命令树读取失败只降级为空清单
            self.last_error = f"{type(error).__name__}: {error}"
            self._entries = ()
            self._set_status(i18n.t("cli.tui.commands.err_catalog", error=self.last_error))
            self._render_rows()
            self._sync_actions()
            return False
        self._entries = entries
        self.last_error = ""
        self._set_status(i18n.t("cli.tui.commands.status_reloaded", count=len(entries)))
        self._render_rows()
        self._sync_actions()
        return True

    def set_query(self, value: str) -> None:
        """设置搜索词，等价于用户键入。"""
        self.query_one("#search", compat.Input).value = value

    def focus_primary(self) -> None:
        """把焦点交给命令列表；列表为空时退到页面容器。"""
        compat.focus_first(self, "#command-list")

    def action_run(self) -> None:
        """键位动作：执行选中的命令。"""
        self.run_selected()

    def action_clear_output(self) -> None:
        """键位动作：清空输出面板。"""
        self.clear_output()

    def action_reload_catalog(self) -> None:
        """键位动作：重新读取命令树。"""
        self.reload_catalog()

    def action_stop(self) -> None:
        """键位动作：终止正在跑的命令。"""
        if not self._busy:
            return
        self.source.stop()
        self._set_status(i18n.t("cli.tui.commands.status_stopping"))

    def action_focus_search(self) -> None:
        """键位动作：把焦点交给搜索框。"""
        self.query_one("#search", compat.Input).focus()

    def clear_output(self) -> None:
        """清空输出面板。"""
        self._output.clear()
        self._render_output()

    def run_selected(self) -> None:
        """执行选中的命令；必填参数缺失时只提示不执行。"""
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.commands.notify_running"),
                severity="warning",
                title=i18n.t("cli.tui.commands.action_run"),
            )
            return
        entry = self.selected_entry
        if entry is None:
            compat.notify(
                self.app,
                i18n.t("cli.tui.commands.pick_command"),
                severity="warning",
                title=i18n.t("cli.tui.commands.action_run"),
            )
            return
        try:
            args = self._collect_argv(entry)
        except CommandError as error:
            self.last_error = str(error)
            self._set_status(str(error))
            compat.notify(
                self.app,
                str(error),
                severity="warning",
                title=i18n.t("cli.tui.commands.action_run"),
            )
            return
        self.run_worker(self._execute(entry, args), group="commands-run", exclusive=True)

    async def _execute(self, entry: CommandEntry, args: Sequence[str]) -> None:
        self._busy = True
        self._output.clear()
        self._render_output()
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.commands.status_running", command=entry.name()))
        try:
            result = await self.source.run(args, self._on_line)
        except Exception as error:  # noqa: BLE001 - 执行者任意异常都转成结果展示
            result = CommandResult(False, -1, f"{type(error).__name__}: {error}", tuple(args))
        self._busy = False
        self._finish(entry, result)

    def _on_line(self, line: str) -> None:
        # 回调由事件循环里的读取协程调用，因此直接写控件是安全的。
        self._output.append(line)
        self._render_output()

    def _finish(self, entry: CommandEntry, result: CommandResult) -> None:
        if result.code < 0:
            self.last_error = result.tail or i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.commands.status_failed", command=entry.name(), detail=self.last_error))
            compat.notify(
                self.app,
                i18n.t("cli.tui.commands.notify_failed", command=entry.name()),
                severity="error",
                title=entry.name(),
            )
        elif result.ok:
            self.last_result = i18n.t("cli.tui.commands.status_done", command=entry.name(), code=result.code)
            self._set_status(self.last_result)
            compat.notify(self.app, self.last_result, severity="information", title=entry.name())
        else:
            self.last_error = result.tail or i18n.t("cli.tui.common.no_output")
            self._set_status(
                i18n.t(
                    "cli.tui.commands.status_exit",
                    command=entry.name(),
                    code=result.code,
                    detail=self.last_error,
                )
            )
            compat.notify(
                self.app,
                i18n.t("cli.tui.commands.notify_exit_code", command=entry.name(), code=result.code),
                severity="error",
                title=entry.name(),
            )
        self._sync_actions()

    def _collect_argv(self, entry: CommandEntry) -> list[str]:
        argv = list(entry.path)
        for row in self.query(ParamRow):
            argv.extend(row.argv())
        return argv

    def _render_rows(self) -> None:
        entries = self.visible_entries
        list_view = self.query_one("#command-list", compat.ListView)
        inner_width = self._list_inner_width(list_view)
        rows = [self._row_text(entry, inner_width) for entry in entries]
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(row, markup=False)) for row in rows])
        list_view.index = self._index_for_key(entries)
        self._rendered_rows = tuple(rows)
        self.run_worker(self._sync_params, group="commands-params", exclusive=True)

    def _row_text(self, entry: CommandEntry, inner_width: int) -> str:
        name = compat.fit_cells(entry.name(), min(NAME_WIDTH, max(8, inner_width // 3)))
        summary_width = max(0, inner_width - len(name) - 1)
        return f"{name} {compat.truncate_cells(entry.summary, summary_width)}" if summary_width else name

    def _list_inner_width(self, list_view: compat.ListView) -> int:
        try:
            return max(8, compat.widget_cells(list_view) - 2)
        except Exception:  # noqa: BLE001 - 未完成布局时退回一个保守宽度
            return 78

    def _index_for_key(self, entries: Sequence[CommandEntry]) -> int | None:
        for index, entry in enumerate(entries):
            if entry.name() == self._selected:
                return index
        return 0 if entries else None

    async def _sync_params(self) -> None:
        pane = self.query_one("#param-pane", compat.VerticalScroll)
        await pane.remove_children()
        entry = self.selected_entry
        if entry is None:
            await pane.mount(
                compat.Static(compat.plain_text(i18n.t("cli.tui.commands.hint_no_selection")), markup=False)
            )
            return
        self._selected = entry.name()
        if not entry.params:
            await pane.mount(compat.Static(compat.plain_text(i18n.t("cli.tui.commands.hint_no_params")), markup=False))
            return
        await pane.mount(*[ParamRow(param) for param in entry.params])

    def _render_output(self) -> None:
        text = self.output_text or i18n.t("cli.tui.commands.output_placeholder")
        self.query_one("#output-text", compat.Static).update(compat.plain_text(text))
        try:
            self.query_one("#output-pane", compat.VerticalScroll).scroll_end(animate=False)
        except Exception:  # noqa: BLE001 - 未完成布局时无处可滚
            return

    def _sync_actions(self) -> None:
        try:
            self.query_one("#run", compat.Button).disabled = self._busy
        except Exception:  # noqa: BLE001 - 未挂载时不动作
            return

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        try:
            self.query_one("#status", compat.Static).update(compat.plain_text(text))
        except Exception:  # noqa: BLE001 - 未挂载时只留字段
            return

    @compat.on(compat.Input.Changed, "#search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        if event.input.id != "search":
            return
        self._query = event.value
        self._render_rows()

    @compat.on(compat.ListView.Highlighted, "#command-list")
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        self.run_worker(self._sync_params, group="commands-params", exclusive=True)

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "run":
            self.run_selected()
        elif event.button.id == "clear":
            self.clear_output()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
