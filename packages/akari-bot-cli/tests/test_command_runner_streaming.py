"""``CommandRunner`` 的实时转发。

安装与卸载可能跑上几分钟。沿用 ``capture_output`` 时这段时间界面上没有任何变化，操作者无法
区分「正在装」与「卡住了」；uv 即使输出被重定向也会打印 ``Resolved … / Installed …`` 这类进度行，
转发即可见。本文件固定三件事：逐行转发、失败仍能摘要、转发走 stderr 以免污染 ``--json`` 的 stdout。
"""

import io
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from rich.console import Console

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import CliError
from akaribot.testing import Tester, func_case

PRINT_TWO = [sys.executable, "-c", "print('first line'); print('second line')"]
FAIL_WITH = [sys.executable, "-c", "import sys; print('boom: detail'); sys.exit(3)"]


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _capture(argv: list[str], **kwargs):
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with patch.object(engine, "err_console", console):
        completed = engine.CommandRunner().run_streaming(argv, **kwargs)
    return completed, buffer.getvalue()


def _test_output_is_forwarded_line_by_line():
    completed, forwarded = _capture(PRINT_TWO)
    return completed.returncode == 0 and "first line" in forwarded and "second line" in forwarded


def _test_tail_is_kept_for_error_summary():
    completed, _ = _capture(FAIL_WITH)
    return completed.returncode == 3 and "boom: detail" in completed.stderr


def _test_run_checked_reports_failure_with_detail():
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with patch.object(engine, "err_console", console):
        try:
            engine.CommandRunner().run_checked(FAIL_WITH, what="安装测试包", stream=True)
        except CliError as error:
            return "boom" in str(error)
    return False


def _test_forwarding_does_not_touch_stdout():
    stdout = io.StringIO()
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    original = sys.stdout
    sys.stdout = stdout
    try:
        with patch.object(engine, "err_console", console):
            engine.CommandRunner().run_streaming(PRINT_TWO)
    finally:
        sys.stdout = original
    return stdout.getvalue() == "" and "first line" in buffer.getvalue()


def _test_dry_run_does_not_execute():
    with TemporaryDirectory(prefix="akari-stream-") as raw:
        proof = Path(raw) / "proof"
        argv = [sys.executable, "-c", f"open({str(proof)!r}, 'w').write('x')"]
        buffer = io.StringIO()
        console = Console(file=buffer, width=200, force_terminal=False)
        with patch.object(engine, "console", console):
            result = engine.CommandRunner(dry_run=True).run_streaming(argv)
        dry_left_nothing = not proof.exists()
        with patch.object(engine, "err_console", Console(file=io.StringIO(), width=200)):
            engine.CommandRunner().run_streaming(argv)
        real_ran = proof.exists()
    return result.returncode == 0 and result.stderr == "" and dry_left_nothing and real_ran


def _test_verbose_echoes_the_command():
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with patch.object(engine, "err_console", console):
        engine.CommandRunner(verbose=True).run_streaming(PRINT_TWO)
    text = buffer.getvalue()
    return "first line" in text and "-c" in text


def _test_missing_executable_raises_cli_error():
    try:
        engine.CommandRunner().run_streaming(["/nonexistent/akaribot-uv", "--version"])
    except CliError:
        return True
    return False


@func_case
async def test_command_runner_streaming(tester: Tester):
    """cli.venv.CommandRunner: 实时转发与失败摘要测试"""
    _use_cli_locale()
    await tester.test(_test_output_is_forwarded_line_by_line, "逐行转发子进程输出")
    await tester.test(_test_tail_is_kept_for_error_summary, "保留输出供失败摘要")
    await tester.test(_test_run_checked_reports_failure_with_detail, "失败时抛出带原因的 CliError")
    await tester.test(_test_forwarding_does_not_touch_stdout, "转发走 stderr，不污染 stdout")
    await tester.test(_test_dry_run_does_not_execute, "dry-run 只回显不执行")
    await tester.test(_test_verbose_echoes_the_command, "verbose 额外回显命令")
    await tester.test(_test_missing_executable_raises_cli_error, "可执行文件缺失抛 CliError")
    return tester
