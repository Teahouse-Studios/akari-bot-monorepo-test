"""Logs 页：实时跟随实例 ``logs/`` 下的日志，并按进程过滤。

数据流：界面只读 :class:`LogSource`；默认实现 :class:`FileLogSource` 经 :mod:`akaribot.cli.logs`
归组进程与文件（文件名约定与增量读取规则见该模块），读取一律带 offset 进行，只取新增字节。
两条不变式：只显示以换行结尾的完整行；offset 不越过未写完的半行，故重复读取不会丢行、
也不会重复显示。显示缓冲是定长环形缓冲，仅在确有新行时重绘。
"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.logs import (
    DEFAULT_BUFFER_LINES,
    READ_CHUNK_BYTES,
    TAIL_CHUNK_BYTES,
    LogChunk,
    LogFileInfo,
    LogReadError,
    LogRingBuffer,
    list_log_files,
    parse_log_name,
    read_since,
    read_tail,
)
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context

ALL_PROCESSES = "all"
"""进程过滤里的「不过滤」项；取值只作内部标识，展示文案在用到时按当前语言取。"""

DEFAULT_FOLLOW_SECONDS = 1.0
"""默认跟随周期（秒）。"""

DEFAULT_RESCAN_SECONDS = 15.0
"""重新枚举日志目录的周期（秒），用于跨日轮转时切换文件。"""

DEBUG_MODES = ("auto", "info", "debug")
# debug 偏好是对端取值，界面按当前语言取标签，故这里只存文案键。
_DEBUG_MODE_KEYS = {
    "auto": "cli.tui.logs.debug_auto",
    "info": "cli.tui.logs.debug_info",
    "debug": "cli.tui.logs.debug_debug",
}


def _filter_name(process: str | None) -> str:
    if not process or process == ALL_PROCESSES:
        return i18n.t("cli.tui.logs.all_processes")
    return process


class LogSourceError(RuntimeError):
    """数据源不可用：日志目录缺失、文件不可读或读取失败。"""


@runtime_checkable
class LogSource(Protocol):
    """日志数据源接口；测试注入替身，生产直接读文件系统。"""

    def list_processes(self) -> Sequence[str]:
        """返回日志目录里出现过的进程名。"""

    def list_files(self, process: str | None = None) -> Sequence[LogFileInfo]:
        """按进程过滤返回日志文件，最新的排在前面。"""

    def read_since(self, path: Path, offset: int, *, max_bytes: int = READ_CHUNK_BYTES) -> LogChunk:
        """从 ``offset`` 起增量读取，只返回新增的完整行。"""

    def read_tail(self, path: Path, *, max_bytes: int = TAIL_CHUNK_BYTES) -> LogChunk:
        """读取文件尾部的若干行，并把 offset 对齐到已读位置。"""


class StaticLogSource:
    """替身数据源：按「文件名 → 行列表」登记内容，``offset`` 即行号游标。

    :param files: 文件名到初始行列表的映射，文件名须符合 ``<进程>[_debug]_<日期>.log``。
    :param mtimes: 文件名到最后修改时间的映射，缺省按登记顺序递增，用于断言「取最新文件」。
    """

    def __init__(
        self,
        files: Mapping[str, Sequence[str]] | None = None,
        *,
        mtimes: Mapping[str, float] | None = None,
    ) -> None:
        self._lines: dict[str, list[str]] = {name: list(lines) for name, lines in (files or {}).items()}
        self._mtimes = dict(mtimes or {})
        self.calls = {"processes": 0, "files": 0, "read": 0, "tail": 0}
        self.read_offsets: list[tuple[str, int]] = []
        self.fail_on_read: str = ""

    def append(self, name: str, *lines: str) -> None:
        """向指定文件追加行，模拟日志继续写入。"""
        self._lines.setdefault(name, []).extend(lines)

    def truncate(self, name: str, lines: Sequence[str]) -> None:
        """用新的行列表替换文件内容，模拟轮转或截断。"""
        self._lines[name] = list(lines)

    def list_processes(self) -> Sequence[str]:
        """见 :meth:`LogSource.list_processes`。"""
        self.calls["processes"] += 1
        names = []
        for name in self._lines:
            parsed = parse_log_name(name)
            if parsed is not None and parsed.process not in names:
                names.append(parsed.process)
        return tuple(sorted(names))

    def list_files(self, process: str | None = None) -> Sequence[LogFileInfo]:
        """见 :meth:`LogSource.list_files`。"""
        self.calls["files"] += 1
        infos: list[LogFileInfo] = []
        for index, (name, lines) in enumerate(self._lines.items()):
            parsed = parse_log_name(name)
            if parsed is None:
                continue
            if process is not None and parsed.process != process:
                continue
            infos.append(
                LogFileInfo(
                    process=parsed.process,
                    path=Path("/stub/logs") / name,
                    date=parsed.date,
                    size=len(lines),
                    modified=self._mtimes.get(name, float(index)),
                    debug=parsed.debug,
                )
            )
        return tuple(sorted(infos, key=lambda info: (info.modified, info.name), reverse=True))

    def read_since(self, path: Path, offset: int, *, max_bytes: int = READ_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_since`；``offset`` 按行号解释。"""
        del max_bytes
        name = Path(path).name
        self.calls["read"] += 1
        self.read_offsets.append((name, offset))
        if self.fail_on_read == name:
            raise LogSourceError(i18n.t("cli.tui.logs.src_stub_refused", name=name))
        lines = self._lines.get(name, [])
        if offset > len(lines):
            return LogChunk(lines=tuple(lines), offset=len(lines), reset=True, path=name)
        return LogChunk(lines=tuple(lines[offset:]), offset=len(lines), path=name)

    def read_tail(self, path: Path, *, max_bytes: int = TAIL_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_tail`；``max_bytes`` 在替身里解释为行数上限。"""
        name = Path(path).name
        self.calls["tail"] += 1
        lines = self._lines.get(name, [])
        keep = max(int(max_bytes), 1)
        tail = lines[-keep:]
        return LogChunk(lines=tuple(tail), offset=len(lines), path=name)


class FileLogSource:
    """默认数据源：直接读实例 ``logs/`` 目录，不起子进程。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param logs_dir: 直接指定日志目录；给定后不再解析实例根。
    :param chunk_bytes: 单次增量读取的字节上限。
    """

    def __init__(self, *, root: Path | str | None = None, logs_dir: Path | str | None = None) -> None:
        self.root = Path(root) if root is not None else None
        self.logs_dir = Path(logs_dir) if logs_dir is not None else None

    def logs_path(self) -> Path:
        """返回日志目录；未显式指定时按实例根拼接 ``logs``。"""
        if self.logs_dir is not None:
            return self.logs_dir
        found = context.active_root()
        if found is not None:
            return found / "logs"
        from akaribot.cli.tui.dashboard import resolve_instance_root

        root = self.root if self.root is not None else resolve_instance_root()
        if root is None:
            raise LogSourceError(i18n.t("cli.tui.logs.src_no_instance"))
        return root / "logs"

    def list_processes(self) -> Sequence[str]:
        """见 :meth:`LogSource.list_processes`。"""
        names: set[str] = set()
        for info in self.list_files(None):
            names.add(info.process)
        return tuple(sorted(names))

    def list_files(self, process: str | None = None) -> Sequence[LogFileInfo]:
        """见 :meth:`LogSource.list_files`；目录不存在时抛出 :class:`LogSourceError`。"""
        directory = self.logs_path()
        try:
            return list_log_files(directory, process)
        except LogReadError as error:
            raise LogSourceError(self._directory_error(error)) from error

    def read_since(self, path: Path, offset: int, *, max_bytes: int = READ_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_since`。"""
        try:
            return read_since(path, offset, max_bytes=max_bytes)
        except LogReadError as error:
            raise LogSourceError(self._file_error(error)) from error

    def read_tail(self, path: Path, *, max_bytes: int = TAIL_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_tail`。"""
        try:
            return read_tail(path, max_bytes=max_bytes)
        except LogReadError as error:
            raise LogSourceError(self._file_error(error)) from error

    @staticmethod
    def _directory_error(error: LogReadError) -> str:
        if error.reason == "dir_missing":
            return i18n.t("cli.tui.logs.src_dir_missing", path=error.path)
        return i18n.t("cli.tui.logs.src_dir_unreadable", path=error.path, error=error.error)

    @staticmethod
    def _file_error(error: LogReadError) -> str:
        # stat 与 read 分开：前者多为文件已被轮转掉，后者是读取本身失败。
        key = "cli.tui.logs.src_file_unreadable" if error.reason == "stat" else "cli.tui.logs.src_file_read_failed"
        return i18n.t(key, path=error.path, error=error.error)


class LogsPage(compat.Vertical):
    """Logs 页控件。

    :param source: 数据源，缺省为 :class:`FileLogSource`。
    :param follow_interval: 跟随周期（秒）；``None`` 或非正数表示不自动跟随，只手动刷新。
    :param rescan_seconds: 重新枚举日志目录的间隔（秒），用于跨日轮转时切换文件。
    :param buffer_lines: 显示缓冲的行数上限，超出后丢弃最早的行。
    :param chunk_bytes: 单次增量读取的字节上限。
    :param prefer_debug: 初始 debug 偏好，取 ``auto`` / ``info`` / ``debug``。
    """

    DEFAULT_CSS = """
    LogsPage {
        layout: vertical;
        height: 1fr;
    }
    LogsPage #target {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    LogsPage #filter-row {
        height: 3;
    }
    LogsPage #filter {
        width: 1fr;
    }
    LogsPage #body {
        height: 1fr;
    }
    LogsPage #process-list {
        width: 24;
        min-width: 16;
        border: round $primary;
    }
    LogsPage #process-list > ListItem {
        padding: 0 1;
    }
    LogsPage #process-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    LogsPage #log-pane {
        width: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    LogsPage #log-view {
        width: 1fr;
    }
    LogsPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    LogsPage #status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    BINDINGS = compat.bindings(
        ("space", "toggle_pause", i18n.t("cli.tui.logs.bind_toggle_pause")),
        ("c", "clear", i18n.t("cli.tui.logs.bind_clear")),
        ("slash", "focus_filter", i18n.t("cli.tui.logs.bind_filter")),
        # debug、重新扫描与清空过滤都有按钮或输入框提示，页脚在 80 列下装不下十几条键位。
        ("d", "cycle_debug", i18n.t("cli.tui.logs.bind_cycle_debug"), False),
        ("r", "rescan", i18n.t("cli.tui.logs.bind_rescan"), False),
        ("escape", "clear_filter", i18n.t("cli.tui.logs.bind_clear_filter"), False),
    )

    can_focus = True

    def __init__(
        self,
        source: LogSource | None = None,
        *,
        follow_interval: float | None = DEFAULT_FOLLOW_SECONDS,
        rescan_seconds: float = DEFAULT_RESCAN_SECONDS,
        buffer_lines: int = DEFAULT_BUFFER_LINES,
        chunk_bytes: int = READ_CHUNK_BYTES,
        prefer_debug: str = "auto",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: LogSource = source if source is not None else FileLogSource()
        self.follow_interval = follow_interval
        self.rescan_seconds = rescan_seconds
        self.chunk_bytes = chunk_bytes
        self.buffer_limit = max(int(buffer_lines), 1)
        self.last_error: str = ""
        self._processes: tuple[str, ...] = ()
        self._files: tuple[LogFileInfo, ...] = ()
        self._process_labels: tuple[str, ...] = ()
        self._selected: str | None = None
        self._followed: LogFileInfo | None = None
        self._offset: int = 0
        self._buffer = LogRingBuffer(self.buffer_limit)
        self._paused: bool = False
        self._prefer_debug: str = prefer_debug if prefer_debug in DEBUG_MODES else "auto"
        self._filter: str = ""
        self._last_chunk: LogChunk | None = None
        self._scanned_at: float = 0.0
        self._rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：上方关键词过滤，左侧进程过滤，右侧日志正文。"""
        yield compat.Static(i18n.t("cli.tui.logs.target_none"), id="target", markup=False)
        with compat.Horizontal(id="filter-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.logs.filter_placeholder"), id="filter")
        with compat.Horizontal(id="body"):
            yield compat.ListView(id="process-list")
            with compat.VerticalScroll(id="log-pane"):
                yield compat.Static(i18n.t("cli.tui.logs.reading"), id="log-view", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.logs.action_pause"), id="pause")
            yield compat.Button(i18n.t("cli.tui.logs.action_clear"), id="clear")
            yield compat.Button(i18n.t("cli.tui.logs.debug_button", label=self.debug_label), id="debug")
            yield compat.Button(i18n.t("cli.tui.logs.action_rescan"), id="refresh")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；枚举日志与周期跟随推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时枚举日志目录，并按周期跟随。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_files()
        if self.follow_interval and self.follow_interval > 0:
            self.set_interval(self.follow_interval, self._tick)

    def focus_primary(self) -> None:
        """把焦点交给进程列表，供上层在页面切换时调用。"""
        compat.focus_first(self, "#process-list")

    # region 状态读取（供测试与上层使用）

    @property
    def processes(self) -> tuple[str, ...]:
        """返回可选的进程名，不含「全部进程」。"""
        return self._processes

    @property
    def files(self) -> tuple[LogFileInfo, ...]:
        """返回当前进程过滤下可见的文件，按最新在前排序。"""
        return self.visible_files

    @property
    def visible_files(self) -> tuple[LogFileInfo, ...]:
        """返回当前过滤下可见的文件。

        枚举结果始终保留完整清单，过滤在读取时进行：进程行的文件计数若跟着过滤结果算，选中一个
        进程后其余进程的计数会全变成 0，看上去像在随机跳动。
        """
        if self._selected is None:
            return self._files
        return tuple(info for info in self._files if info.process == self._selected)

    @property
    def selected_process(self) -> str | None:
        """返回当前过滤的进程；``None`` 表示不过滤。"""
        return self._selected

    @property
    def followed_file(self) -> LogFileInfo | None:
        """返回当前跟随的文件。"""
        return self._followed

    def process_labels(self) -> tuple[str, ...]:
        """返回最近一次渲染出的进程行文本，供自动化断言核对计数。"""
        return self._process_labels

    @property
    def read_offset(self) -> int:
        """返回当前读取偏移；文件数据源里单位为字节。

        命名避开 ``Widget.offset``（控件在父容器里的位置），以免覆盖基类属性。
        """
        return self._offset

    @property
    def paused(self) -> bool:
        """返回是否处于暂停跟随状态。"""
        return self._paused

    @property
    def debug_preference(self) -> str:
        """返回 debug 偏好：``auto`` / ``info`` / ``debug``。"""
        return self._prefer_debug

    @property
    def debug_label(self) -> str:
        """返回 debug 偏好的本地化标签。"""
        key = _DEBUG_MODE_KEYS.get(self._prefer_debug)
        return i18n.t(key) if key else self._prefer_debug

    @property
    def last_chunk(self) -> LogChunk | None:
        """返回最近一次增量读取结果，供断言 offset 是否生效。"""
        return self._last_chunk

    @property
    def buffer_lines(self) -> tuple[str, ...]:
        """返回显示缓冲中的行。"""
        return self._buffer.lines

    @property
    def dropped_lines(self) -> int:
        """返回显示缓冲丢弃的行数。"""
        return self._buffer.dropped

    @property
    def filter_keyword(self) -> str:
        """返回关键词过滤；空串表示不过滤。"""
        return self._filter

    @property
    def filter_hits(self) -> int:
        """返回关键词在当前缓冲中的命中行数；未启用过滤时为 0。"""
        return len(self._matched_lines()) if self._filter else 0

    @property
    def visible_text(self) -> str:
        """返回日志面板当前渲染出的纯文本。"""
        return self._rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    # endregion

    # region 枚举与跟随

    def refresh_files(self) -> None:
        """重新枚举进程与文件，必要时切换跟随目标并载入目标尾部。"""
        self._scanned_at = time.monotonic()
        try:
            processes = tuple(self.source.list_processes())
            if self._selected is not None and self._selected not in processes:
                self._selected = None
            files = tuple(self.source.list_files(None))
        except Exception as error:  # noqa: BLE001 - 枚举失败只更新状态栏
            self._processes = ()
            self._files = ()
            self._followed = None
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_process_list()
            self._render_target()
            self._render_log()
            self._set_status(i18n.t("cli.tui.logs.status_scan_failed", error=self.last_error))
            return
        self._processes = processes
        self._files = files
        self.last_error = ""
        chosen = self._choose_file(self.visible_files)
        if chosen is None:
            self._followed = None
            self._offset = 0
            self._buffer.clear()
            self._render_process_list()
            self._render_target()
            self._render_log()
            self._set_status(i18n.t("cli.tui.logs.status_no_files", filter_name=_filter_name(self._selected)))
            return
        if self._followed is None or chosen.name != self._followed.name:
            self._switch_to(chosen)
        else:
            self._followed = chosen
        self._render_process_list()
        self._render_target()
        self._set_status(self._status_line())

    def _choose_file(self, files: Sequence[LogFileInfo]) -> LogFileInfo | None:
        if not files:
            return None
        if self._prefer_debug == "debug":
            for info in files:
                if info.debug:
                    return info
        elif self._prefer_debug == "info":
            for info in files:
                if not info.debug:
                    return info
        return files[0]

    def _switch_to(self, info: LogFileInfo) -> None:
        try:
            chunk = self.source.read_tail(info.path, max_bytes=TAIL_CHUNK_BYTES)
        except Exception as error:  # noqa: BLE001 - 读取失败只更新状态栏
            self._followed = info
            self._offset = 0
            self.last_error = f"{type(error).__name__}: {error}"
            self._set_status(i18n.t("cli.tui.logs.status_tail_failed", error=self.last_error))
            return
        self._followed = info
        self._last_chunk = chunk
        self._offset = chunk.offset
        self._buffer.clear()
        self._buffer.extend(chunk.lines)
        self._render_log()
        self._pin_to_end()
        self._set_status(self._status_line())

    def select_process(self, process: str | None) -> None:
        """切换进程过滤，并重新枚举与对齐跟随目标。

        :param process: 进程名；``None`` 表示不过滤。
        """
        self._selected = process
        self.refresh_files()

    def follow_once(self) -> LogChunk | None:
        """执行一次增量跟随；暂停中或没有目标时返回 ``None``。

        :return: 本次读取结果；确实读到新行时才重绘。
        """
        if self._paused:
            return None
        followed = self._followed
        if followed is None:
            return None
        try:
            chunk = self.source.read_since(followed.path, self._offset, max_bytes=self.chunk_bytes)
        except Exception as error:  # noqa: BLE001 - 读取失败只更新状态栏
            self.last_error = f"{type(error).__name__}: {error}"
            self._set_status(i18n.t("cli.tui.logs.status_follow_failed", error=self.last_error))
            return None
        self._last_chunk = chunk
        self._offset = chunk.offset
        self.last_error = ""
        if chunk.lines:
            self._append(chunk.lines)
        self._render_target()
        self._set_status(self._status_line(reset=chunk.reset))
        return chunk

    def _append(self, lines: Sequence[str]) -> None:
        self._buffer.extend(lines)
        self._render_log()

    def _tick(self) -> None:
        if not self.display:
            return
        if self._pause_on_scroll_back():
            return
        if time.monotonic() - self._scanned_at >= self.rescan_seconds:
            self.refresh_files()
        self.follow_once()

    def _pause_on_scroll_back(self) -> bool:
        # 视口离开底部即用户上滚：跟随暂停，避免下一个周期把视口拽回底部。
        if self._paused:
            return False
        pane = self._log_pane()
        if pane is None or pane.is_vertical_scroll_end:
            return False
        self.pause()
        return True

    # endregion

    # region 交互

    def pause(self) -> None:
        """暂停跟随；offset 保持不变，恢复后从暂停位置继续。"""
        self._paused = True
        self._sync_actions()
        self._set_status(self._status_line())

    def resume(self) -> None:
        """恢复跟随，补读暂停期间新增的行并回到缓冲末尾。"""
        self._paused = False
        self._sync_actions()
        self.follow_once()
        self._pin_to_end()
        self._set_status(self._status_line())

    def toggle_pause(self) -> None:
        """在暂停与恢复之间切换。"""
        if self._paused:
            self.resume()
        else:
            self.pause()

    def clear_buffer(self) -> None:
        """清屏：只清显示缓冲，不改 offset，因此不会重读历史日志。"""
        self._buffer.clear()
        self._render_log()
        self._pin_to_end()
        self._set_status(i18n.t("cli.tui.logs.status_cleared", offset=self._offset))

    def set_filter(self, value: str) -> None:
        """设置关键词过滤框内容，等价于用户键入。"""
        self.query_one("#filter", compat.Input).value = value

    def focus_filter(self) -> None:
        """把焦点移到关键词过滤框。"""
        self.query_one("#filter", compat.Input).focus()

    def clear_filter(self) -> None:
        """清空关键词过滤；已为空时把焦点交回进程列表。"""
        field = self.query_one("#filter", compat.Input)
        if field.value:
            field.value = ""
            return
        compat.focus_first(self, "#process-list")

    def cycle_debug_preference(self) -> None:
        """在「自动 → 仅 INFO → 仅 debug」之间循环切换。"""
        index = DEBUG_MODES.index(self._prefer_debug)
        self._prefer_debug = DEBUG_MODES[(index + 1) % len(DEBUG_MODES)]
        button = self.query_one("#debug", compat.Button)
        button.label = i18n.t("cli.tui.logs.debug_button", label=self.debug_label)
        self.refresh_files()

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        index = compat.highlighted_index(event.list_view)
        process = self._process_at(index)
        if process != self._selected:
            self.select_process(process)

    @compat.on(compat.Input.Changed, "#filter")
    def _on_filter_changed(self, event: compat.Input.Changed) -> None:
        self._filter = event.value.strip()
        self._render_log()
        self._set_status(self._status_line())

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "pause":
            self.toggle_pause()
        elif button_id == "clear":
            self.clear_buffer()
        elif button_id == "debug":
            self.cycle_debug_preference()
        elif button_id == "refresh":
            self.refresh_files()

    def action_toggle_pause(self) -> None:
        """键位动作：暂停或恢复跟随。"""
        self.toggle_pause()

    def action_clear(self) -> None:
        """键位动作：清屏。"""
        self.clear_buffer()

    def action_cycle_debug(self) -> None:
        """键位动作：切换 debug 偏好。"""
        self.cycle_debug_preference()

    def action_focus_filter(self) -> None:
        """键位动作：把焦点移到关键词过滤框。"""
        self.focus_filter()

    def action_clear_filter(self) -> None:
        """键位动作：清空关键词过滤。"""
        self.clear_filter()

    def action_rescan(self) -> None:
        """键位动作：重新枚举日志目录。"""
        self.refresh_files()

    # endregion

    # region 渲染

    def _process_at(self, index: int | None) -> str | None:
        if index is None or index <= 0 or index > len(self._processes):
            return None
        return self._processes[index - 1]

    def _render_process_list(self) -> None:
        list_view = self.query_one("#process-list", compat.ListView)
        labels = [self._process_label(None)]
        labels.extend(self._process_label(name) for name in self._processes)
        self._process_labels = tuple(labels)
        list_view.clear()
        list_view.extend(compat.ListItem(compat.Static(label, markup=False)) for label in labels)
        index = 0 if self._selected is None else (self._processes.index(self._selected) + 1)
        list_view.index = min(index, max(len(labels) - 1, 0))

    def _process_label(self, process: str | None) -> str:
        # 计数始终针对完整清单：它表示该进程（或全部进程）有多少个日志文件，与当前过滤无关。
        count = sum(1 for info in self._files if process is None or info.process == process)
        return i18n.t("cli.tui.logs.process_item", name=_filter_name(process), count=count)

    def _render_target(self) -> None:
        followed = self._followed
        if followed is None:
            text = i18n.t("cli.tui.logs.target_none_filtered", filter_name=_filter_name(self._selected))
        else:
            text = i18n.t(
                "cli.tui.logs.target_following",
                name=followed.name,
                process=followed.process,
                level=followed.level_label,
                offset=self._offset,
                state=self._paused_text(),
            )
        self.query_one("#target", compat.Static).update(compat.plain_text(self._clip(text)))

    def _matched_lines(self) -> tuple[str, ...]:
        lines = self._buffer.lines
        if not self._filter:
            return lines
        needle = self._filter.lower()
        return tuple(line for line in lines if needle in line.lower())

    def _render_log(self) -> None:
        lines = self._matched_lines()
        if lines:
            text = "\n".join(lines)
        elif self._filter:
            text = i18n.t("cli.tui.logs.filter_empty", keyword=self._filter)
        else:
            text = i18n.t("cli.tui.logs.log_empty")
        self._rendered = text
        self.query_one("#log-view", compat.Static).update(compat.plain_text(text))
        if self._at_end():
            self._pin_to_end()

    def _log_pane(self) -> compat.VerticalScroll | None:
        try:
            return self.query_one("#log-pane", compat.VerticalScroll)
        except Exception:  # noqa: BLE001 - 未挂载时没有滚动容器
            return None

    def _at_end(self) -> bool:
        pane = self._log_pane()
        return pane is None or bool(pane.is_vertical_scroll_end)

    def _scroll_to_end(self) -> None:
        pane = self._log_pane()
        if pane is None:
            return
        scroll_end = getattr(pane, "scroll_end", None)
        if not callable(scroll_end):
            return
        try:
            scroll_end(animate=False)
        except TypeError:
            scroll_end()

    def _pin_to_end(self) -> None:
        self._scroll_to_end()
        # 本帧的 max_scroll_y 还停在追加内容之前，布局完成后再贴一次底，下一个周期才不会
        # 把「刚追加完、布局尚未跟上」误判成用户上滚。
        if self.is_mounted:
            self.call_after_refresh(self._scroll_to_end)

    def _paused_text(self) -> str:
        return i18n.t("cli.tui.logs.paused" if self._paused else "cli.tui.logs.following")

    def _status_line(self, *, reset: bool = False) -> str:
        # 顺序：跟随状态、恢复提示、过滤命中、文件名、offset、缓冲、丢弃行数、异常提示。
        # 恢复提示与命中行数排在前列：状态栏按宽度裁剪，跟随周期里用户最需要先看到这两项。
        followed = self._followed
        parts = [self._paused_text()]
        if self._paused:
            parts.append(i18n.t("cli.tui.logs.status_resume_hint"))
        if self._filter:
            parts.append(i18n.t("cli.tui.logs.status_filter", keyword=self._filter, hits=self.filter_hits))
        if followed is not None:
            parts.append(followed.name)
        parts.append(f"offset {self._offset}")
        parts.append(i18n.t("cli.tui.logs.status_buffer", buffered=len(self._buffer), limit=self.buffer_limit))
        if self._buffer.dropped:
            parts.append(i18n.t("cli.tui.logs.status_dropped", dropped=self._buffer.dropped))
        if reset:
            parts.append(i18n.t("cli.tui.logs.status_reset"))
        pending = self._last_chunk is not None and self._last_chunk.pending
        if pending and not self._paused:
            parts.append(i18n.t("cli.tui.logs.status_pending"))
        return self._clip(i18n.t("cli.tui.logs.status_separator").join(parts))

    def _clip(self, text: str) -> str:
        width = self._inner_width()
        return compat.truncate_cells(text, width) if width > 0 else text

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 78
        return max(outer - 2, 16)

    def _sync_actions(self) -> None:
        key = "cli.tui.logs.action_resume" if self._paused else "cli.tui.logs.action_pause"
        self.query_one("#pause", compat.Button).label = i18n.t(key)

    def _set_status(self, text: str) -> None:
        clipped = self._clip(text)
        self._status_rendered = clipped
        self.query_one("#status", compat.Static).update(compat.plain_text(clipped))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存内容重排，不重新读文件。"""
        self._render_target()
        self._render_log()
        # 视口高度变了，max_scroll_y 随之变化；跟随中要重新贴底，暂停时保留用户的位置。
        if not self._paused:
            self._pin_to_end()
        self._set_status(self._status_line())

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
