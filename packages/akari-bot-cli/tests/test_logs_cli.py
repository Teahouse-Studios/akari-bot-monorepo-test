"""``akaribot logs``：文件名解析、增量读取与命令输出。

日志文件名约定与 offset 增量读取都在 ``akaribot.cli.logs``，界面日志页与命令共用同一份实现；
用例锁定约定本身、环形缓冲的丢弃统计，以及命令层在进程过滤、级别选择、``--json`` / ``--path``
与跟随上的行为。整份用例不起实例进程，也不连 core。
"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli import logs as log_files
from akaribot.cli.commands import logs as logs_command
from akaribot.testing import Tester, func_case

FILE_NAME = "BotDaemon_2026-09-25.log"
DEBUG_NAME = "BotDaemon_debug_2026-09-25.log"


class _FakeInstance:
    # 命令只读实例根的 ``logs`` 子目录，替身给一个 root 即可。
    def __init__(self, root: Path) -> None:
        self.root = Path(root)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _write_log(directory: Path, name: str, text: str, *, mtime: float) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(text, encoding="utf-8")
    os.utime(path, (mtime, mtime))
    return path


def _invoke(root: Path | str, argv: list[str]):
    with patch.object(logs_command, "require_instance", return_value=_FakeInstance(Path(root))):
        return CliRunner().invoke(logs_command.app, argv)


def _numbered(count: int, prefix: str = "b") -> str:
    return "".join(f"{prefix}{index:02d}\n" for index in range(count))


async def _test_parse_log_name_rules():
    plain = log_files.parse_log_name(FILE_NAME)
    debug = log_files.parse_log_name(DEBUG_NAME)
    underscored = log_files.parse_log_name("My_Process_2026-09-24.log")
    return (
        plain == ("BotDaemon", False, "2026-09-25")
        and debug == ("BotDaemon", True, "2026-09-25")
        and underscored == ("My_Process", False, "2026-09-24")
        and log_files.parse_log_name("RunConsole_2026-09-24.txt") is None
        and log_files.parse_log_name("BotDaemon.log") is None
        and log_files.parse_log_name("BotDaemon_2026-9-24.log") is None
    )


async def _test_tui_page_shares_parse_rule():
    from akaribot.cli.tui import logs as tui_logs

    return tui_logs.parse_log_name is log_files.parse_log_name and tui_logs.LogFileInfo is log_files.LogFileInfo


async def _test_list_log_files_orders_and_filters():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        logs_dir = root / "logs"
        _write_log(logs_dir, "BotDaemon_2026-09-24.log", "old\n", mtime=100.0)
        _write_log(logs_dir, DEBUG_NAME, "dbg\n", mtime=200.0)
        _write_log(logs_dir, "Server_2026-09-25.log", "srv\n", mtime=300.0)
        (logs_dir / "notes.md").write_text("x", encoding="utf-8")
        names = [info.name for info in log_files.list_log_files(logs_dir)]
        server = [info.name for info in log_files.list_log_files(logs_dir, "Server")]
        levels = [(info.name, info.level_label, info.date) for info in log_files.list_log_files(logs_dir, "BotDaemon")]
        try:
            log_files.list_log_files(root / "missing")
            missing = ""
        except log_files.LogReadError as error:
            missing = error.reason
        return (
            names == ["Server_2026-09-25.log", DEBUG_NAME, "BotDaemon_2026-09-24.log"]
            and server == ["Server_2026-09-25.log"]
            and levels == [(DEBUG_NAME, "debug", "2026-09-25"), ("BotDaemon_2026-09-24.log", "INFO", "2026-09-24")]
            and missing == "dir_missing"
        )


async def _test_read_since_keeps_half_line_for_next_round():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / FILE_NAME
        path.write_text("a1\na2\npart", encoding="utf-8")
        first = log_files.read_since(path, 0)
        path.write_text("a1\na2\npartial done\n", encoding="utf-8")
        second = log_files.read_since(path, first.offset)
        path.write_text("short\n", encoding="utf-8")
        third = log_files.read_since(path, second.offset)
        return (
            first.lines == ("a1", "a2")
            and first.pending
            and first.offset == 6
            and second.lines == ("partial done",)
            and not second.pending
            and third.reset
            and third.lines == ("short",)
        )


async def _test_read_last_lines_reports_truncation():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / FILE_NAME
        path.write_text(_numbered(20, "line"), encoding="utf-8")
        tail = log_files.read_last_lines(path, 3)
        capped = log_files.read_last_lines(path, 3, max_bytes=16, chunk_bytes=8)
        empty = log_files.read_last_lines(path, 0)
        return (
            tail.lines == ("line17", "line18", "line19")
            and not tail.truncated
            and capped.truncated
            and capped.lines[-1] == "line19"
            and len(capped.lines) <= 3
            and empty.lines == ()
            and empty.truncated
        )


async def _test_ring_buffer_counts_dropped_lines():
    buffer = log_files.LogRingBuffer(3)
    first = buffer.extend(["a", "b"])
    second = buffer.extend(["c", "d"])
    lines = buffer.lines
    dropped = buffer.dropped
    buffer.clear()
    bulk = log_files.LogRingBuffer(2).extend(["a", "b", "c"])
    return (
        first == 0
        and second == 1
        and lines == ("b", "c", "d")
        and dropped == 1
        and bulk == 1
        and buffer.lines == ()
        and buffer.dropped == 0
    )


async def _test_command_tails_default_file_and_lines():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        logs_dir = root / "logs"
        _write_log(logs_dir, FILE_NAME, _numbered(60), mtime=200.0)
        _write_log(logs_dir, "Server_2026-09-25.log", "s1\ns2\ns3\n", mtime=100.0)
        default = _invoke(root, [])
        short = _invoke(root, ["--lines", "2"])
        other = _invoke(root, ["--process", "Server"])
        path_only = _invoke(root, ["--path"])
        return (
            default.exit_code == 0
            and len(default.stdout.splitlines()) == 50
            and default.stdout.splitlines()[0] == "b10"
            and short.stdout.splitlines() == ["b58", "b59"]
            and other.stdout.splitlines() == ["s1", "s2", "s3"]
            and path_only.stdout.strip() == str(logs_dir / FILE_NAME)
        )


async def _test_command_selects_level_and_emits_json():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        logs_dir = root / "logs"
        _write_log(logs_dir, FILE_NAME, "info line\n", mtime=200.0)
        _write_log(logs_dir, DEBUG_NAME, "debug line\n", mtime=100.0)
        debug = _invoke(root, ["--process", "BotDaemon", "--debug"])
        info = _invoke(root, ["--process", "BotDaemon", "--info"])
        payload = json.loads(_invoke(root, ["--json", "--lines", "1"]).stdout.strip().splitlines()[-1])
    with TemporaryDirectory() as other:
        other_logs = Path(other) / "logs"
        _write_log(other_logs, DEBUG_NAME, "debug line\n", mtime=10.0)
        missing_info = _invoke(other, ["--info"])
    return (
        debug.stdout.strip() == "debug line"
        and info.stdout.strip() == "info line"
        and payload["name"] == FILE_NAME
        and payload["process"] == "BotDaemon"
        and payload["level"] == "INFO"
        and payload["date"] == "2026-09-25"
        and payload["lines"] == ["info line"]
        and payload["count"] == 1
        and payload["requested"] == 1
        and payload["truncated"] is False
        and payload["follow"] is False
        and payload["file"].endswith(FILE_NAME)
        and missing_info.exit_code == 1
        and i18n.t("cli.logs.level_missing", level="INFO", process=i18n.t("cli.logs.all_processes"))
        in missing_info.output
    )


def _flat(text: str) -> str:
    # 临时目录路径很长，rich 会在终端宽度处折行；比对时去掉全部空白，避免断言依赖路径长度。
    return "".join(text.split())


async def _test_command_rejects_bad_requests():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        logs_dir = root / "logs"
        _write_log(logs_dir, FILE_NAME, "a\n", mtime=10.0)
        both_levels = _invoke(root, ["--debug", "--info"])
        both_outputs = _invoke(root, ["--path", "--json"])
        negative = _invoke(root, ["--lines=-1"])
    with TemporaryDirectory() as empty_root:
        (Path(empty_root) / "logs").mkdir()
        no_files = _invoke(empty_root, [])
    with TemporaryDirectory() as absent_root:
        absent = _invoke(absent_root, [])
    return (
        both_levels.exit_code == 1
        and _flat(i18n.t("cli.logs.conflict_level")) in _flat(both_levels.output)
        and both_outputs.exit_code == 1
        and _flat(i18n.t("cli.logs.conflict_output")) in _flat(both_outputs.output)
        and negative.exit_code == 1
        and _flat(i18n.t("cli.logs.bad_lines", value=-1)) in _flat(negative.output)
        and no_files.exit_code == 1
        and _flat(
            i18n.t(
                "cli.logs.no_files",
                path=Path(empty_root) / "logs",
                process=i18n.t("cli.logs.all_processes"),
            )
        )
        in _flat(no_files.output)
        and absent.exit_code == 1
        and _flat(i18n.t("cli.logs.dir_missing", path=Path(absent_root) / "logs")) in _flat(absent.output)
    )


async def _test_empty_file_is_reported():
    # 实例空闲时当天的日志是空的：要说明一句，否则用户以为命令没生效。
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_log(root / "logs", FILE_NAME, "", mtime=10.0)
        result = _invoke(root, [])
    return result.exit_code == 0 and _flat(
        i18n.t("cli.logs.empty_file", path=Path(root) / "logs" / FILE_NAME)
    ) in _flat(result.output)


async def _test_follow_file_emits_new_lines():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / FILE_NAME
        path.write_text("first\nsecond\n", encoding="utf-8")
        batches: list[tuple[str, ...]] = []
        rounds = {"count": 0}

        def emit(chunk: log_files.LogChunk) -> None:
            batches.append(chunk.lines)
            if len(batches) == 1:
                path.write_text("first\nsecond\nthird\n", encoding="utf-8")

        def stop() -> bool:
            # 上限同时兜住「跟随不再前进」的回归：那种情况下循环不会自己退出。
            rounds["count"] += 1
            return len(batches) >= 2 or rounds["count"] > 10

        final = logs_command.follow_file(
            path,
            6,
            emit=emit,
            interval=0.0,
            should_stop=stop,
            sleep=lambda _seconds: None,
        )
    return batches == [("second",), ("third",)] and final == 19


async def _test_follow_batch_payload_is_structured():
    chunk = log_files.LogChunk(lines=("second",), offset=19, reset=True)
    info = log_files.LogFileInfo(process="BotDaemon", path=Path("/tmp") / FILE_NAME)
    payload = logs_command._batch_payload(info, chunk)
    return (
        payload["file"] == str(Path("/tmp") / FILE_NAME)
        and payload["lines"] == ["second"]
        and payload["count"] == 1
        and payload["offset"] == 19
        and payload["reset"] is True
    )


@func_case
async def test_logs_cli(tester: Tester):
    """cli.logs: 日志解析、增量读取与命令输出测试"""
    _use_cli_locale()
    await tester.test(_test_parse_log_name_rules, "文件名解析出进程、debug 与日期")
    await tester.test(_test_tui_page_shares_parse_rule, "界面日志页共用同一份解析规则")
    await tester.test(_test_list_log_files_orders_and_filters, "文件清单按最新排序并支持进程过滤")
    await tester.test(_test_read_since_keeps_half_line_for_next_round, "增量读取不消费未写完的半行")
    await tester.test(_test_read_last_lines_reports_truncation, "按行取尾部并报告截断")
    await tester.test(_test_ring_buffer_counts_dropped_lines, "环形缓冲统计丢弃行数")
    await tester.test(_test_command_tails_default_file_and_lines, "命令默认打印末尾 50 行并支持过滤与路径")
    await tester.test(_test_command_selects_level_and_emits_json, "级别选择与 JSON 输出")
    await tester.test(_test_command_rejects_bad_requests, "互斥选项与无效参数被拒绝")
    await tester.test(_test_empty_file_is_reported, "空日志文件给出说明")
    await tester.test(_test_follow_file_emits_new_lines, "跟随只输出新增行")
    await tester.test(_test_follow_batch_payload_is_structured, "跟随批次是结构化 JSON")
    return tester
