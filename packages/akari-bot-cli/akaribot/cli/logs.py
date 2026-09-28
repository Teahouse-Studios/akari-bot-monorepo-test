"""日志文件的命名解析与增量读取。

日志文件名约定 ``<进程>[_debug]_<日期>.log``（日期形如 ``2026-09-24``）。本模块是这条约定的唯一
实现，``akaribot logs`` 与界面日志页共用同一份解析与读取规则。读取按字节 offset 递增，只消费以
换行结尾的完整行：末尾的半行留给下一次，故重复读取既不丢行也不重复显示。显示侧的行缓冲与丢弃
统计同样在这里，两处的缓冲上限语义因而一致。
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import re
from typing import NamedTuple

READ_CHUNK_BYTES = 64 * 1024
"""单次增量读取的字节上限。"""

TAIL_CHUNK_BYTES = 128 * 1024
"""回看文件尾部时的单次读取字节上限。"""

TAIL_LINES_MAX_BYTES = 4 * 1024 * 1024
"""按行取尾部时允许回看的字节上限，到达上限即视为截断。"""

DEFAULT_BUFFER_LINES = 200
"""显示缓冲的默认行数上限。"""

DEFAULT_TAIL_LINES = 50
"""默认输出的末尾行数。"""

_LOG_NAME_PATTERN = re.compile(r"^(?P<process>.+?)(?P<debug>_debug)?_(?P<date>\d{4}-\d{2}-\d{2})\.log$")


class LogName(NamedTuple):
    """日志文件名的解析结果。

    :param process: 进程名，取自文件名前缀。
    :param debug: 文件名是否带 ``_debug`` 标记。
    :param date: 日期，形如 ``2026-09-24``。
    """

    process: str
    debug: bool
    date: str


@dataclass(frozen=True)
class LogFileInfo:
    """一个可读取的日志文件。

    :param process: 进程名，取自文件名前缀。
    :param path: 文件路径。
    :param date: 日期，取自文件名。
    :param size: 字节大小。
    :param modified: 最后修改时间（``stat().st_mtime``）。
    :param debug: 文件名是否带 ``_debug`` 标记。
    """

    process: str
    path: Path
    date: str = ""
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
    :param truncated: 因字节上限没有回看到所需内容，更早的行未读取。
    :param path: 所属文件名，供状态栏与报告展示。
    """

    lines: tuple[str, ...] = ()
    offset: int = 0
    reset: bool = False
    pending: bool = False
    truncated: bool = False
    path: str = ""


class LogReadError(RuntimeError):
    """日志目录或文件不可读。

    :param path: 出错的目录或文件。
    :param reason: ``dir_missing`` / ``dir_unreadable`` / ``stat`` / ``read``。
    :param error: 原始 ``OSError``；目录缺失时为 ``None``。
    """

    def __init__(self, path: Path | str, reason: str, error: OSError | None = None) -> None:
        super().__init__(f"{reason}: {path}")
        self.path = Path(path)
        self.reason = reason
        self.error = error


class LogRingBuffer:
    """定长行缓冲：写满后丢弃最早的行，并累计丢弃行数。

    :param limit: 行数上限，至少为 1。
    """

    def __init__(self, limit: int = DEFAULT_BUFFER_LINES) -> None:
        self.limit = max(int(limit), 1)
        self.dropped = 0
        self._lines: deque[str] = deque(maxlen=self.limit)

    def extend(self, lines: Sequence[str]) -> int:
        """追加行，返回本次丢弃的行数。"""
        before = len(self._lines)
        self._lines.extend(lines)
        dropped = before + len(lines) - len(self._lines)
        self.dropped += dropped
        return dropped

    def clear(self) -> None:
        """清空缓冲并重置丢弃计数。"""
        self._lines.clear()
        self.dropped = 0

    @property
    def lines(self) -> tuple[str, ...]:
        """返回缓冲中的行。"""
        return tuple(self._lines)

    def __len__(self) -> int:
        return len(self._lines)


def parse_log_name(name: str) -> LogName | None:
    """把日志文件名解析为进程名、debug 标记与日期；不符合命名规则时返回 ``None``。

    :param name: 文件名，形如 ``BotDaemon_2026-09-21.log`` 或 ``Server_debug_2026-09-21.log``。
    :return: 解析结果；不是日志文件时为 ``None``。
    """
    match = _LOG_NAME_PATTERN.match(name)
    if match is None:
        return None
    return LogName(
        process=match.group("process"),
        debug=match.group("debug") is not None,
        date=match.group("date"),
    )


def list_log_files(directory: Path | str, process: str | None = None) -> tuple[LogFileInfo, ...]:
    """枚举日志目录里的日志文件，最新的排在前面。

    :param directory: 日志目录。
    :param process: 只保留该进程的文件；``None`` 表示不过滤。
    :return: 文件信息元组。
    :raises LogReadError: 目录缺失或不可读。
    """
    target = Path(directory)
    if not target.is_dir():
        raise LogReadError(target, "dir_missing")
    try:
        entries = list(target.iterdir())
    except OSError as error:
        raise LogReadError(target, "dir_unreadable", error) from error
    infos: list[LogFileInfo] = []
    for entry in entries:
        parsed = parse_log_name(entry.name)
        if parsed is None or not entry.is_file():
            continue
        if process is not None and parsed.process != process:
            continue
        try:
            stat = entry.stat()
        except OSError:
            continue
        infos.append(
            LogFileInfo(
                process=parsed.process,
                path=entry,
                date=parsed.date,
                size=stat.st_size,
                modified=stat.st_mtime,
                debug=parsed.debug,
            )
        )
    return tuple(sorted(infos, key=lambda info: (info.modified, info.name), reverse=True))


def read_since(path: Path | str, offset: int, *, max_bytes: int = READ_CHUNK_BYTES) -> LogChunk:
    """从 ``offset`` 起增量读取，只返回新增的完整行。

    :param path: 日志文件。
    :param offset: 上次读取到的字节偏移。
    :param max_bytes: 单次读取的字节上限。
    :return: 读取结果；``reset`` 为真表示文件被截断或轮转，本次从头读取。
    """
    target = Path(path)
    size = _stat_size(target)
    reset = offset > size
    start = 0 if reset else max(offset, 0)
    raw = _read_at(target, start, max_bytes)
    lines, consumed = _split_complete_lines(raw, max_bytes)
    return LogChunk(
        lines=lines,
        offset=start + consumed,
        reset=reset,
        pending=start + len(raw) > start + consumed,
        path=target.name,
    )


def read_tail(path: Path | str, *, max_bytes: int = TAIL_CHUNK_BYTES) -> LogChunk:
    """读取文件尾部的若干行，并把 offset 对齐到已读位置。

    :param path: 日志文件。
    :param max_bytes: 回看的字节上限。
    :return: 读取结果。
    """
    target = Path(path)
    size = _stat_size(target)
    start = max(size - max_bytes, 0)
    raw = _read_at(target, start, max_bytes)
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


def read_last_lines(
    path: Path | str,
    count: int,
    *,
    max_bytes: int = TAIL_LINES_MAX_BYTES,
    chunk_bytes: int = READ_CHUNK_BYTES,
) -> LogChunk:
    """读取文件末尾的若干完整行。

    :param path: 日志文件。
    :param count: 期望的行数；非正数表示不读取内容。
    :param max_bytes: 向前回看的字节上限。
    :param chunk_bytes: 单次回看的字节数。
    :return: 读取结果，``offset`` 对齐到已读内容的末尾；``truncated`` 为真表示受字节上限所限，
        更早的行没有读取。
    """
    target = Path(path)
    size = _stat_size(target)
    if count <= 0:
        return LogChunk(offset=size, truncated=size > 0, path=target.name)
    start = size
    raw = b""
    while start > 0 and len(raw) < max_bytes:
        step = min(chunk_bytes, start, max_bytes - len(raw))
        start -= step
        raw = _read_at(target, start, step) + raw
        if raw.count(b"\n") > count:
            break
    lines, consumed = _split_complete_lines(raw, max_bytes)
    if start > 0 and lines:
        # 没有读到文件开头时首行可能被截断，丢弃后才能保证每一行都是完整的。
        lines = lines[1:]
    return LogChunk(
        lines=lines[-count:],
        offset=start + consumed,
        truncated=len(lines) < count and start > 0,
        path=target.name,
    )


def _split_complete_lines(raw: bytes, limit: int) -> tuple[tuple[str, ...], int]:
    if not raw:
        return (), 0
    cut = raw.rfind(b"\n")
    if cut < 0:
        if len(raw) < limit:
            return (), 0
        return (raw.decode("utf-8", errors="replace"),), len(raw)
    return tuple(raw[:cut].decode("utf-8", errors="replace").split("\n")), cut + 1


def _stat_size(target: Path) -> int:
    try:
        return target.stat().st_size
    except OSError as error:
        raise LogReadError(target, "stat", error) from error


def _read_at(target: Path, start: int, max_bytes: int) -> bytes:
    try:
        with target.open("rb") as handle:
            handle.seek(start)
            return handle.read(max_bytes)
    except OSError as error:
        raise LogReadError(target, "read", error) from error
