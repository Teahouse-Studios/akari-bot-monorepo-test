"""查看实例日志。

日志文件名约定 ``<进程>[_debug]_<日期>.log``，解析与增量读取在 :mod:`akaribot.cli.logs`，与界面
日志页共用一份实现。本模块只做参数校验、目标文件选择与输出。
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Annotated

import typer

from akaribot.cli import i18n
from akaribot.cli.instance import InstancePathOption, FlatCommandGroup, fail, require_instance, warn
from akaribot.cli.logs import (
    DEFAULT_TAIL_LINES,
    LogChunk,
    LogFileInfo,
    LogReadError,
    list_log_files,
    read_last_lines,
    read_since,
)

FOLLOW_INTERVAL_SECONDS = 1.0
"""跟随模式的读取周期（秒）。"""

LEVEL_LABELS = {"auto": "", "info": "INFO", "debug": "debug"}
"""目标文件选择策略的展示标签：最新、最新的 INFO 文件、最新的 debug 文件。"""

app = typer.Typer(
    help=i18n.t("cli.logs.help"),
    cls=FlatCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def logs(
    process: Annotated[str | None, typer.Option("--process", help=i18n.t("cli.logs.option_process"))] = None,
    follow: Annotated[bool, typer.Option("--follow", help=i18n.t("cli.logs.option_follow"))] = False,
    debug: Annotated[bool, typer.Option("--debug", help=i18n.t("cli.logs.option_debug"))] = False,
    info: Annotated[bool, typer.Option("--info", help=i18n.t("cli.logs.option_info"))] = False,
    lines: Annotated[int, typer.Option("--lines", help=i18n.t("cli.logs.option_lines"))] = DEFAULT_TAIL_LINES,
    path_only: Annotated[bool, typer.Option("--path", help=i18n.t("cli.logs.option_path"))] = False,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
    instance: InstancePathOption = None,
) -> None:
    """打印日志文件末尾的若干行；``--follow`` 持续输出新增行，直到 Ctrl+C。

    ``--path`` 只打印选中的文件路径，便于脚本自行处理；``--json`` 输出结构化结果，
    跟随模式下每批新增行输出一行 JSON。
    """
    target = require_instance(instance)
    if debug and info:
        fail(i18n.t("cli.logs.conflict_level"))
    if path_only and as_json:
        fail(i18n.t("cli.logs.conflict_output"))
    if lines < 0:
        fail(i18n.t("cli.logs.bad_lines", value=lines))
    directory = target.root / "logs"
    try:
        files = list_log_files(directory, process)
    except LogReadError as error:
        fail(_read_error(error))
    if not files:
        fail(i18n.t("cli.logs.no_files", path=directory, process=_process_label(process)))
    level = "debug" if debug else ("info" if info else "auto")
    chosen = _choose_file(files, level)
    if chosen is None:
        fail(i18n.t("cli.logs.level_missing", level=LEVEL_LABELS[level], process=_process_label(process)))
    if path_only:
        typer.echo(str(chosen.path))
        return
    try:
        chunk = read_last_lines(chosen.path, lines)
    except LogReadError as error:
        fail(_read_error(error))
    if as_json:
        typer.echo(json.dumps(_payload(chosen, chunk, requested=lines, follow=follow), ensure_ascii=False))
    else:
        _emit_lines(chunk)
        if chunk.truncated:
            warn(i18n.t("cli.logs.truncated", count=len(chunk.lines)))
        elif not chunk.lines:
            # 实例空闲时当天的日志是空的：不说明一句，用户以为命令没生效。
            warn(i18n.t("cli.logs.empty_file", path=chosen.path))
    if not follow:
        return
    emit = _emit_json(chosen) if as_json else _emit_lines
    try:
        follow_file(chosen.path, chunk.offset, emit=emit)
    except KeyboardInterrupt:
        return
    except LogReadError as error:
        fail(_read_error(error))


def follow_file(
    path: Path,
    offset: int,
    *,
    emit: Callable[[LogChunk], None],
    interval: float = FOLLOW_INTERVAL_SECONDS,
    should_stop: Callable[[], bool] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """从 ``offset`` 起持续读取新增行并交给 ``emit``，直到 ``should_stop`` 为真。

    :param path: 日志文件。
    :param offset: 起始字节偏移。
    :param emit: 每批新增行的回调。
    :param interval: 两轮读取之间的间隔秒数；非正数表示不等待。
    :param should_stop: 停止判据；``None`` 表示一直跟随。
    :param sleep: 等待实现，测试用它避免真实等待。
    :return: 结束时的字节偏移。
    """
    if interval > 0:
        sleep(interval)
    while should_stop is None or not should_stop():
        chunk = read_since(path, offset)
        offset = chunk.offset
        if chunk.lines:
            emit(chunk)
        if interval > 0:
            sleep(interval)
    return offset


def _choose_file(files: Sequence[LogFileInfo], level: str) -> LogFileInfo | None:
    if not files:
        return None
    if level == "debug":
        return next((info for info in files if info.debug), None)
    if level == "info":
        return next((info for info in files if not info.debug), None)
    return files[0]


def _process_label(process: str | None) -> str:
    return process or i18n.t("cli.logs.all_processes")


def _read_error(error: LogReadError) -> str:
    if error.reason == "dir_missing":
        return i18n.t("cli.logs.dir_missing", path=error.path)
    if error.reason == "dir_unreadable":
        return i18n.t("cli.logs.dir_unreadable", path=error.path, error=error.error)
    return i18n.t("cli.logs.file_unreadable", path=error.path, error=error.error)


def _payload(info: LogFileInfo, chunk: LogChunk, *, requested: int, follow: bool) -> dict[str, object]:
    return {
        "file": str(info.path),
        "name": info.name,
        "process": info.process,
        "level": info.level_label,
        "date": info.date,
        "lines": list(chunk.lines),
        "count": len(chunk.lines),
        "requested": requested,
        "offset": chunk.offset,
        "reset": chunk.reset,
        "pending": chunk.pending,
        "truncated": chunk.truncated,
        "follow": follow,
    }


def _batch_payload(info: LogFileInfo, chunk: LogChunk) -> dict[str, object]:
    return {
        "file": str(info.path),
        "lines": list(chunk.lines),
        "count": len(chunk.lines),
        "offset": chunk.offset,
        "reset": chunk.reset,
    }


def _emit_lines(chunk: LogChunk) -> None:
    if chunk.reset:
        warn(i18n.t("cli.logs.follow_reset"))
    for line in chunk.lines:
        typer.echo(line)


def _emit_json(info: LogFileInfo) -> Callable[[LogChunk], None]:
    def emit(chunk: LogChunk) -> None:
        typer.echo(json.dumps(_batch_payload(info, chunk), ensure_ascii=False))

    return emit
