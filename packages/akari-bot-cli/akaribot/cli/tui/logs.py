"""Logs 页：实时跟随实例 ``logs/`` 下的日志，并按进程过滤。

数据流：界面只读 :class:`LogSource`；默认实现 :class:`FileLogSource` 按文件名
``<进程>[_debug]_<日期>.log`` 归组进程与文件，读取一律带 offset 增量进行，只取新增字节。
两条不变式：只显示以换行结尾的完整行；offset 不越过未写完的半行，故重复读取不会丢行、
也不会重复显示。显示缓冲是定长环形缓冲，仅在确有新行时重绘。
"""

from __future__ import annotations

import re
import time
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat

ALL_PROCESSES = "all"
"""进程过滤里的「不过滤」项；取值只作内部标识，展示文案在用到时按当前语言取。"""

READ_CHUNK_BYTES = 64 * 1024
"""单次增量读取的字节上限，限制每次跟随的代价。"""

TAIL_CHUNK_BYTES = 128 * 1024
"""首次跟随或切换目标时回看的字节上限，避免把整份历史日志读进内存。"""

DEFAULT_BUFFER_LINES = 200
"""显示缓冲的行数上限。"""

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

_LOG_NAME_PATTERN = re.compile(r"^(?P<process>.+?)(?P<debug>_debug)?_(?P<date>\d{4}-\d{2}-\d{2})\.log$")


def _filter_name(process: str | None) -> str:
    if not process or process == ALL_PROCESSES:
        return i18n.t("cli.tui.logs.all_processes")
    return process


class LogSourceError(RuntimeError):
    """数据源不可用：日志目录缺失、文件不可读或读取失败。"""


def parse_log_name(name: str) -> tuple[str, bool] | None:
    """把日志文件名解析为「进程名 + 是否 debug」；不符合命名规则时返回 ``None``。

    :param name: 文件名，形如 ``BotDaemon_2026-09-21.log`` 或 ``Server_debug_2026-09-21.log``。
    :return: 二元组——进程名与是否 debug；不是日志文件时为 ``None``。
    """
    match = _LOG_NAME_PATTERN.match(name)
    if match is None:
        return None
    return match.group("process"), match.group("debug") is not None


@dataclass(frozen=True)
class LogFileInfo:
    """一个可跟随的日志文件。

    :param process: 进程名，取自文件名前缀。
    :param path: 文件路径。
    :param size: 字节大小。
    :param modified: 最后修改时间（``stat().st_mtime``）。
    :param debug: 文件名是否带 ``_debug`` 标记。
    """

    process: str
    path: Path
    size: int = 0
    modified: float = 0.0
    debug: bool = False

    @property
    def name(self) -> str:
        """返回文件名。"""
        return self.path.name

    @property
    def level_label(self) -> str:
        """返回日志级别标签。"""
        return "debug" if self.debug else "INFO"


@dataclass(frozen=True)
class LogChunk:
    """一次增量读取的结果。

    :param lines: 本次读到的完整行，可能为空。
    :param offset: 下次读取的起点字节偏移。
    :param reset: 文件被截断或轮转，本次从头读取。
    :param pending: 文件末尾仍有未消费字节（半行未写完，或本次触到读取上限）。
    :param path: 所属文件名，供状态栏展示。
    """

    lines: tuple[str, ...] = ()
    offset: int = 0
    reset: bool = False
    pending: bool = False
    path: str = ""


def _split_complete_lines(raw: bytes, limit: int) -> tuple[tuple[str, ...], int]:
    if not raw:
        return (), 0
    cut = raw.rfind(b"\n")
    if cut < 0:
        if len(raw) < limit:
            return (), 0
        return (raw.decode("utf-8", errors="replace"),), len(raw)
    return tuple(raw[:cut].decode("utf-8", errors="replace").split("\n")), cut + 1


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
            if parsed is not None and parsed[0] not in names:
                names.append(parsed[0])
        return tuple(sorted(names))

    def list_files(self, process: str | None = None) -> Sequence[LogFileInfo]:
        """见 :meth:`LogSource.list_files`。"""
        self.calls["files"] += 1
        infos: list[LogFileInfo] = []
        for index, (name, lines) in enumerate(self._lines.items()):
            parsed = parse_log_name(name)
            if parsed is None:
                continue
            if process is not None and parsed[0] != process:
                continue
            infos.append(
                LogFileInfo(
                    process=parsed[0],
                    path=Path("/stub/logs") / name,
                    size=len(lines),
                    modified=self._mtimes.get(name, float(index)),
                    debug=parsed[1],
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
        if not directory.is_dir():
            raise LogSourceError(i18n.t("cli.tui.logs.src_dir_missing", path=directory))
        try:
            entries = list(directory.iterdir())
        except OSError as error:
            raise LogSourceError(i18n.t("cli.tui.logs.src_dir_unreadable", path=directory, error=error)) from error
        infos: list[LogFileInfo] = []
        for entry in entries:
            parsed = parse_log_name(entry.name)
            if parsed is None or not entry.is_file():
                continue
            if process is not None and parsed[0] != process:
                continue
            try:
                stat = entry.stat()
            except OSError:
                continue
            infos.append(
                LogFileInfo(
                    process=parsed[0],
                    path=entry,
                    size=stat.st_size,
                    modified=stat.st_mtime,
                    debug=parsed[1],
                )
            )
        return tuple(sorted(infos, key=lambda info: (info.modified, info.name), reverse=True))

    def read_since(self, path: Path, offset: int, *, max_bytes: int = READ_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_since`。"""
        target = Path(path)
        size = self._stat_size(target)
        reset = offset > size
        start = 0 if reset else max(offset, 0)
        raw = self._read_at(target, start, max_bytes)
        lines, consumed = _split_complete_lines(raw, max_bytes)
        return LogChunk(
            lines=lines,
            offset=start + consumed,
            reset=reset,
            pending=start + len(raw) > start + consumed,
            path=target.name,
        )

    def read_tail(self, path: Path, *, max_bytes: int = TAIL_CHUNK_BYTES) -> LogChunk:
        """见 :meth:`LogSource.read_tail`。"""
        target = Path(path)
        size = self._stat_size(target)
        start = max(size - max_bytes, 0)
        raw = self._read_at(target, start, max_bytes)
        base = start
        if start > 0:
            cut = raw.find(b"\n")
            if cut >= 0:
                raw = raw[cut + 1 :]
                base = start + cut + 1
        lines, consumed = _split_complete_lines(raw, max_bytes)
        return LogChunk(
            lines=lines,
            offset=base + consumed,
            pending=base + len(raw) > base + consumed,
            path=target.name,
        )

    @staticmethod
    def _stat_size(target: Path) -> int:
        try:
            return target.stat().st_size
        except OSError as error:
            raise LogSourceError(i18n.t("cli.tui.logs.src_file_unreadable", path=target, error=error)) from error

    @staticmethod
    def _read_at(target: Path, start: int, max_bytes: int) -> bytes:
        try:
            with target.open("rb") as handle:
                handle.seek(start)
                return handle.read(max_bytes)
        except OSError as error:
            raise LogSourceError(i18n.t("cli.tui.logs.src_file_read_failed", path=target, error=error)) from error


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
        ("d", "cycle_debug", i18n.t("cli.tui.logs.bind_cycle_debug")),
        ("r", "rescan", i18n.t("cli.tui.logs.bind_rescan")),
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
        self._buffer: deque[str] = deque(maxlen=self.buffer_limit)
        self._paused: bool = False
        self._prefer_debug: str = prefer_debug if prefer_debug in DEBUG_MODES else "auto"
        self._dropped: int = 0
        self._last_chunk: LogChunk | None = None
        self._scanned_at: float = 0.0
        self._rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：左侧进程过滤，右侧日志正文。"""
        yield compat.Static(i18n.t("cli.tui.logs.target_none"), id="target", markup=False)
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
        return tuple(self._buffer)

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
            self._dropped = 0
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
        self._dropped = 0
        self._buffer.extend(chunk.lines)
        self._render_log()
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
        room = self._buffer.maxlen or 0
        overflow = len(self._buffer) + len(lines) - room
        if overflow > 0:
            self._dropped += min(overflow, len(self._buffer))
        self._buffer.extend(lines)
        self._render_log()

    def _tick(self) -> None:
        if not self.display:
            return
        if time.monotonic() - self._scanned_at >= self.rescan_seconds:
            self.refresh_files()
        self.follow_once()

    # endregion

    # region 交互

    def pause(self) -> None:
        """暂停跟随；offset 保持不变，恢复后从暂停位置继续。"""
        self._paused = True
        self._sync_actions()
        self._set_status(self._status_line())

    def resume(self) -> None:
        """恢复跟随，并立即补读暂停期间新增的行。"""
        self._paused = False
        self._sync_actions()
        self.follow_once()

    def toggle_pause(self) -> None:
        """在暂停与恢复之间切换。"""
        if self._paused:
            self.resume()
        else:
            self.pause()

    def clear_buffer(self) -> None:
        """清屏：只清显示缓冲，不改 offset，因此不会重读历史日志。"""
        self._buffer.clear()
        self._dropped = 0
        self._render_log()
        self._set_status(i18n.t("cli.tui.logs.status_cleared", offset=self._offset))

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

    def _render_log(self) -> None:
        if self._buffer:
            text = "\n".join(self._buffer)
        else:
            text = i18n.t("cli.tui.logs.log_empty")
        self._rendered = text
        self.query_one("#log-view", compat.Static).update(compat.plain_text(text))
        self._scroll_to_end()

    def _scroll_to_end(self) -> None:
        try:
            pane = self.query_one("#log-pane", compat.VerticalScroll)
        except Exception:  # noqa: BLE001 - 未挂载时无需滚动
            return
        scroll_end = getattr(pane, "scroll_end", None)
        if not callable(scroll_end):
            return
        try:
            scroll_end(animate=False)
        except TypeError:
            scroll_end()

    def _paused_text(self) -> str:
        return i18n.t("cli.tui.logs.paused" if self._paused else "cli.tui.logs.following")

    def _status_line(self, *, reset: bool = False) -> str:
        # 顺序：跟随状态、文件名、offset、缓冲、丢弃行数、异常提示。
        followed = self._followed
        parts = [self._paused_text()]
        if followed is not None:
            parts.append(followed.name)
        parts.append(f"offset {self._offset}")
        parts.append(i18n.t("cli.tui.logs.status_buffer", buffered=len(self._buffer), limit=self.buffer_limit))
        if self._dropped:
            parts.append(i18n.t("cli.tui.logs.status_dropped", dropped=self._dropped))
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
        self._set_status(self._status_line())

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
