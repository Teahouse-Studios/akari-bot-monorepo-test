"""测试框架自身的单元测试。"""

import inspect
import json
import re
import asyncio
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import AsyncMock, patch

from akaribot.core.builtins.session.internal import MessageSession
from akaribot.testing import func_case, Tester, Raise
from akaribot.testing.expectations import Contains, ContainsAll, ContainsAny, Regex
from akaribot.testing.junit import JUnitReport, JUnitTestCase, JUnitTestSuite
from akaribot.testing.mock.http import MockHTTPResponse
from akaribot.testing.mock.session import MockMessageSession
from akaribot.core.logger import Logger

# request_url 支持以 fmt 指定返回形式，mock 响应必须覆盖代码库中实际用到的全部取值。
REQUIRED_RESPONSE_FORMATS = ("json", "text", "read", "content")


def _test_mock_session_signature_matches_real():
    drifted = {}
    for name in dir(MessageSession):
        if name.startswith("__"):
            continue
        real = getattr(MessageSession, name, None)
        mock = MockMessageSession.__dict__.get(name)
        if mock is None or not callable(real) or not callable(mock):
            continue
        try:
            real_params = inspect.signature(real).parameters
            mock_params = inspect.signature(mock).parameters
        except (ValueError, TypeError):
            continue
        missing = [p for p in real_params if p not in mock_params]
        if missing:
            drifted[name] = missing

    if drifted:
        Logger.error(f"MockMessageSession signature drift: {drifted}")
    return not drifted


def _test_mock_response_supports_all_formats():
    response = MockHTTPResponse(status_code=200, text="{}", content=b"binary")
    missing = [fmt for fmt in REQUIRED_RESPONSE_FORMATS if not hasattr(response, fmt)]
    if missing:
        Logger.error(f"MockHTTPResponse missing formats: {missing}")
    return not missing


async def _test_contains_matches_non_text_element():
    from akaribot.core.builtins.message.elements import ImageElement, PlainElement

    result = {"output": [PlainElement.assign("hello"), ImageElement.assign(path="https://example.com/a.png")]}
    return (
        await Contains("KE:image").match(result)
        and await Contains("hello").match(result)
        and await Regex(re.compile(r"\[KE:image")).match(result)
        and await ContainsAll("hello", "KE:image").match(result)
        and await ContainsAny("nope", "KE:image").match(result)
    )


async def _test_contains_still_rejects_absent_text():
    from akaribot.core.builtins.message.elements import PlainElement

    result = {"output": [PlainElement.assign("hello")]}
    return not await Contains("definitely_absent_token").match(result)


def _test_junit_coerces_error_details_to_text():
    from xml.etree import ElementTree

    case = JUnitTestCase("error")
    case.error = ("Test error", True)
    suite = JUnitTestSuite("tester")
    suite.add_testcase(case)
    report = JUnitReport()
    report.add_testsuite(suite)
    error = ElementTree.fromstring(report.to_xml_string()).find(".//error")
    return error is not None and error.get("message") == "Test error" and error.text == "True"


async def _test_integrate_preserves_unexpected_exception():
    error = ValueError("boom")
    raw_result = {
        "input": "~broken",
        "exception": error,
        "exception_message": "boom",
        "traceback": "traceback: boom",
        "action": ["(raise ValueError)", "boom"],
        "output": None,
    }
    tester = Tester("exception")
    with patch("akaribot.testing.tester.run_test_case", new=AsyncMock(return_value=raw_result)):
        result = await tester.integrate("~broken", Contains("success"))
    return (
        result.get("match") is False
        and result.get("exception") is error
        and result.get("traceback") == "traceback: boom"
    )


async def _test_integrate_expected_exception_is_not_runner_error():
    error = ValueError("boom")
    raw_result = {
        "input": "~broken",
        "exception": error,
        "exception_message": "boom",
        "traceback": "traceback: boom",
        "action": ["(raise ValueError)", "boom"],
        "output": None,
    }
    tester = Tester("expected_exception")
    with patch("akaribot.testing.tester.run_test_case", new=AsyncMock(return_value=raw_result)):
        result = await tester.integrate("~broken", Raise(ValueError, "boom"))
    return result.get("match") is True and "traceback" not in result


async def _test_function_entry_timeout_is_structured_failure():
    from akaribot.testing.process import run_function_entry

    async def stuck():
        await asyncio.Event().wait()

    async def slow(tester):
        await tester.test(stuck, "卡住的子测试")

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
    ):
        result = await run_function_entry(slow, is_ci=True, timeout=0.01)
    return (
        result.get("timeout") is True
        and result.get("timeout_limit") == 0.01
        and result.get("active_test") == "卡住的子测试"
        and result.get("completed_tests") == 0
    )


async def _test_function_entry_timeout_resets_on_progress():
    from akaribot.testing.process import run_function_entry

    async def step():
        await asyncio.sleep(0.02)
        return True

    async def progressing(tester):
        for _ in range(12):
            await tester.test(step)
        return tester

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
    ):
        result = await run_function_entry(progressing, is_ci=True, timeout=0.2)
    return not result.get("timeout") and all(entry.get("match") for entry in result.get("results", []))


async def _test_protocol_exception_is_recorded_without_stopping_function_test():
    from akaribot.core.constants import WaitCancelException
    from akaribot.testing.process import run_function_entry

    async def cancelled_wait():
        raise WaitCancelException

    async def fine():
        return True

    async def mixed(tester):
        await tester.test(cancelled_wait, "等待取消")
        await tester.test(fine, "后续测试")
        return tester

    orphan_cancelled = asyncio.Event()
    orphan_started = asyncio.Event()
    orphan_task = {}

    async def orphan():
        try:
            orphan_started.set()
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            orphan_cancelled.set()
            raise

    async def unhandled_protocol_exception(_tester):
        orphan_task["task"] = asyncio.create_task(orphan(), name="test-protocol-exception-orphan")
        await orphan_started.wait()
        raise WaitCancelException

    try:
        with (
            patch("akaribot.testing.process.close_db", new=AsyncMock()),
            patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
            patch("akaribot.testing.process.load_modules", new=AsyncMock()),
        ):
            result = await run_function_entry(mixed, is_ci=True)
            unhandled_result = await run_function_entry(unhandled_protocol_exception, is_ci=True)

        results = result.get("results", [])
        task = orphan_task.get("task")
        return (
            not result.get("error")
            and len(results) == 2
            and results[0].get("match") is False
            and results[0].get("exception_type") == "WaitCancelException"
            and results[1].get("match") is True
            and unhandled_result.get("error")
            and unhandled_result.get("cleanup_pending") is False
            and task is not None
            and task.done()
            and task.cancelled()
            and orphan_cancelled.is_set()
        )
    finally:
        task = orphan_task.get("task")
        if task is not None and not task.done():
            task.cancel()
        if task is not None:
            await asyncio.gather(task, return_exceptions=True)


async def _test_case_entry_cancels_orphaned_tasks_before_next_database_context():
    from akaribot.testing.process import run_case_entry

    cancelled = asyncio.Event()
    orphan_task = None

    async def orphan():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    async def fake_run_test_case(*_args, **_kwargs):
        nonlocal orphan_task
        orphan_task = asyncio.create_task(orphan(), name="test-orphaned-case-entry-task")
        await asyncio.sleep(0)
        return {"input": "~case", "output": [], "action": [], "expected": None}

    entry = {
        "func": lambda _msg: None,
        "input": "~case",
        "expected": None,
        "note": None,
        "timeout": None,
        "file": None,
        "line": 0,
    }
    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
        patch("akaribot.testing.process.run_test_case", new=fake_run_test_case),
    ):
        await run_case_entry(entry, is_ci=True)
    return orphan_task is not None and orphan_task.cancelled() and cancelled.is_set()


async def _test_function_entry_bounds_cancellation_cleanup():
    from akaribot.testing.process import run_function_entry

    cleanup_started = asyncio.Event()
    release_cleanup = asyncio.Event()

    async def stuck_after_cancel():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cleanup_started.set()
            await release_cleanup.wait()

    async def stubborn(tester):
        await tester.test(stuck_after_cancel, "延迟取消的子测试")

    try:
        with (
            patch("akaribot.testing.process.close_db", new=AsyncMock()),
            patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
            patch("akaribot.testing.process.load_modules", new=AsyncMock()),
            patch("akaribot.testing.tasks.CANCEL_TIMEOUT", 0.01),
        ):
            result = await asyncio.wait_for(run_function_entry(stubborn, is_ci=True, timeout=0.01), timeout=0.1)
        return result.get("timeout") is True and result.get("cleanup_pending") is True and cleanup_started.is_set()
    finally:
        release_cleanup.set()
        await asyncio.sleep(0)


async def _test_cancelled_progress_waiter_does_not_reset_deadline():
    from akaribot.testing.process import run_function_entry

    async def cancelled_waiter(_self, _after_revision):
        raise asyncio.CancelledError

    async def stuck(_tester):
        await asyncio.Event().wait()

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
        patch.object(Tester, "_wait_for_progress", new=cancelled_waiter),
    ):
        result = await asyncio.wait_for(run_function_entry(stuck, is_ci=True, timeout=0.01), timeout=0.1)
    return result.get("timeout") is True and result.get("cleanup_pending") is False


async def _test_unit_subtest_exception_keeps_running_and_counts_once():
    import tester as tester_module

    async def boom():
        raise RuntimeError("unit boom")

    async def fine():
        return True

    from akaribot.testing.decorator import func_case as _fc

    @_fc
    async def mixed(tester):
        await tester.test(boom, "失败子测试")
        await tester.test(fine, "成功子测试")
        return tester

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
    ):
        from akaribot.testing.process import run_function_entry

        res = await run_function_entry(mixed, is_ci=True)

    class FakeSuite:
        def __init__(self, name):
            self.name = name
            self.test_cases = []

        def add_testcase(self, tc):
            self.test_cases.append(tc)

    func_suite = FakeSuite("Function Tests")
    registry_suite = FakeSuite("Registry Tests")

    class _NullLogger:
        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    fake_spec = types.SimpleNamespace(
        name="tests__fake_case",
        loader=types.SimpleNamespace(exec_module=lambda mod: None),
    )
    original_modules = dict(sys.modules)

    with (
        patch.object(tester_module, "Logger", _NullLogger()),
        patch.object(tester_module, "init_db", new=AsyncMock(return_value=True)),
        patch.object(tester_module, "close_db", new=AsyncMock()),
        patch.object(tester_module, "load_modules", new=AsyncMock()),
        patch.object(tester_module, "get_registry", return_value=[]),
        patch.object(tester_module, "run_function_entry", new=AsyncMock(return_value=res)),
        patch.object(tester_module, "_collect_test_files", return_value=[str(Path("tests/integration/_fake_case.py"))]),
        patch.object(tester_module.importlib.util, "spec_from_file_location", return_value=fake_spec),
        patch.object(tester_module, "junit_func_suite", func_suite),
        patch.object(tester_module, "junit_registry_suite", registry_suite),
        patch.object(tester_module, "junit_report") as junit_report,
        patch.object(tester_module.importlib.util, "module_from_spec", return_value=types.SimpleNamespace()),
    ):
        sys.modules.clear()
        sys.modules.update(original_modules)
        junit_report.test_suites = []
        fake_inspect = types.SimpleNamespace(
            getmembers=lambda mod, predicate=None: [("mixed", mixed)],
            isfunction=lambda obj: obj is mixed,
        )
        await tester_module.main(inspect_module=fake_inspect)

    names = [tc.name for tc in func_suite.test_cases]
    failed_cases = [tc for tc in func_suite.test_cases if tc.failure or tc.error]
    checks = {
        "exception_recorded": res["results"][0].get("exception_type") == "RuntimeError",
        "kept_running": len(res["results"]) == 2 and res["results"][1].get("match") is True,
        "two_cases": len(func_suite.test_cases) == 2,
        "no_double_count": len(failed_cases) == 2,
        "subtest_named": any("失败子测试" in name for name in names),
    }
    if not all(checks.values()):
        raise AssertionError(
            f"runner accounting regression: {checks}; "
            f"cases={[(tc.name, bool(tc.failure), bool(tc.error)) for tc in func_suite.test_cases]}"
        )
    return True


async def _test_function_entry_does_not_misclassify_test_timeout():
    from akaribot.testing.process import run_function_entry

    async def inner_timeout():
        raise TimeoutError("inner deadline")

    async def timed_test(tester):
        await tester.test(inner_timeout, "内部超时")
        return tester

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
    ):
        result = await run_function_entry(timed_test, is_ci=True, timeout=0.2)
    (subtest,) = result.get("results", [])
    return (
        not result.get("timeout")
        and subtest.get("match") is False
        and subtest.get("exception_type") == "TimeoutError"
        and "inner deadline" in subtest.get("exception_message", "")
        and "inner deadline" in subtest.get("traceback", "")
        and subtest.get("note") == "内部超时"
    )


async def _test_function_entry_init_failure_is_error():
    from akaribot.testing.process import run_function_entry

    async def noop(_tester):
        return None

    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=False)),
    ):
        result = await run_function_entry(noop, is_ci=True)
    return bool(result.get("error")) and not result.get("skipped")


def _test_setup_timing_flag_reads_environment():
    import os

    from akaribot.testing.process import SETUP_TIMING_ENV, _setup_timing_enabled

    samples = ((None, False), ("", False), ("0", False), ("1", True), ("true", True), ("YES", True))
    try:
        for value, expected in samples:
            if value is None:
                os.environ.pop(SETUP_TIMING_ENV, None)
            else:
                os.environ[SETUP_TIMING_ENV] = value
            if _setup_timing_enabled() is not expected:
                return False
    finally:
        os.environ.pop(SETUP_TIMING_ENV, None)
    return True


def _test_setup_timing_reports_database_stages():
    from akaribot.testing.process import format_setup_timing

    plain = format_setup_timing("func", "noop", 0.1, 0.2, 0.05)
    if " db_models=" in plain:
        return False

    detailed = format_setup_timing(
        "func",
        "noop",
        0.1,
        0.2,
        0.05,
        {"models": 5.0, "fetch_db": 0.002, "import_models": 0.011, "tortoise_init": 3.8, "schemas": 0.007},
    )
    if not detailed.startswith("[SETUP] kind=func name=noop close_db=0.100s"):
        return False
    return (
        " db_models=5" in detailed
        and " db_fetch=0.002s" in detailed
        and " db_import=0.011s" in detailed
        and " db_init=3.800s" in detailed
        and " db_schema=0.007s" in detailed
    )


async def _test_setup_timing_reports_runtime_state():
    from akaribot.testing.process import _runtime_snapshot, format_setup_timing

    runtime = _runtime_snapshot()
    threads = int(runtime["threads"])
    tasks = int(runtime["tasks"])
    if float(runtime["cpu"]) < 0.0 or threads < 1 or tasks < 1 or not runtime["top_threads"]:
        return False
    text = format_setup_timing("func", "noop", 0.1, 0.2, 0.05, None, runtime)
    return " cpu=" in text and f" threads={threads}" in text and f" tasks={tasks}" in text and " top_threads=" in text


async def _test_setup_timing_logs_preparation_phases():
    import os
    from unittest.mock import Mock

    from akaribot.testing.process import SETUP_TIMING_ENV, run_function_entry

    async def noop(_tester):
        return None

    info = Mock()
    with (
        patch.dict(os.environ, {SETUP_TIMING_ENV: "1"}),
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
        patch("akaribot.testing.process.TEST_LOGGER.info", new=info),
    ):
        await run_function_entry(noop, is_ci=True, timeout=None)

    lines = [call.args[0] for call in info.call_args_list if str(call.args[0]).startswith("[SETUP]")]
    if len(lines) != 1 or "kind=func name=noop " not in lines[0]:
        return False
    if " close_db=" not in lines[0] or " init_db=" not in lines[0] or " load_modules=" not in lines[0]:
        return False

    info.reset_mock()
    os.environ.pop(SETUP_TIMING_ENV, None)
    with (
        patch("akaribot.testing.process.close_db", new=AsyncMock()),
        patch("akaribot.testing.process.init_db", new=AsyncMock(return_value=True)),
        patch("akaribot.testing.process.load_modules", new=AsyncMock()),
        patch("akaribot.testing.process.TEST_LOGGER.info", new=info),
    ):
        await run_function_entry(noop, is_ci=True, timeout=None)
    return not [call for call in info.call_args_list if str(call.args[0]).startswith("[SETUP]")]


def _test_union_merge_logs_stay_out_of_repo_data():
    from akaribot.core.constants.path import data_path, union_merge_logs_path
    from akaribot.core.database.models import UNION_SCOPE_SENDER
    from akaribot.modules.core.common_tools._union_merge import write_merge_log

    repo_logs_dir = data_path / "union_merge_logs"
    before = set(repo_logs_dir.glob("*.json")) if repo_logs_dir.is_dir() else set()

    new_union = "UNIONTEST|merge-log-isolation"
    write_merge_log(new_union, UNION_SCOPE_SENDER, {"keep_ids": [], "drop_ids": []})

    leaked = (set(repo_logs_dir.glob("*.json")) if repo_logs_dir.is_dir() else set()) - before
    if leaked:
        Logger.error(f"Merge logs leaked into {repo_logs_dir}: {sorted(path.name for path in leaked)}")
        return False

    # 写入本身仍必须发生，仅是放置在隔离目录中。若日志改为空操作，泄漏检查会产生虚假通过判定。
    if not list(union_merge_logs_path.glob(f"*_{new_union.replace('|', '-')}.json")):
        Logger.error(f"Expected a merge log under {union_merge_logs_path}, found none")
        return False
    return True


def _test_load_modules_reuses_locale_snapshot():
    from akaribot.testing.mock import loader

    builds = []

    with (
        patch.object(loader, "_locale_snapshot_errors", None),
        patch.object(loader, "build_locale_snapshot", side_effect=lambda *args, **kwargs: builds.append(1) or []),
        patch.object(loader, "connect_locale_snapshot") as connect_snapshot,
    ):
        loader._load_locale_snapshot()
        loader._load_locale_snapshot()

    # 快照仅构建一次，但每个入口仍要重置翻译连接的状态。
    return len(builds) == 1 and connect_snapshot.call_count == 2


def _test_http_fixtures_registered_once_per_directory():
    from akaribot.testing.mock import fixtures
    from akaribot.testing.mock.http import HTTPMock

    with tempfile.TemporaryDirectory() as directory:
        fixture_dir = Path(directory)
        (fixture_dir / "cached.json").write_text(
            json.dumps({"url": "https://example.com/cached-fixture", "status_code": 200, "text": "ok"}),
            encoding="utf-8",
        )
        before = len(HTTPMock.get_all_responses())
        try:
            first = fixtures.load_http_fixtures(fixture_dir)
            second = fixtures.load_http_fixtures(fixture_dir)
            added = len(HTTPMock.get_all_responses()) - before
        finally:
            fixtures._registered_dirs.pop(fixture_dir.resolve(), None)

    return first == 1 and second == 1 and added == 1


async def _test_main_reports_registry_case_before_next_entry():
    import tester as tester_module

    events = []

    class _RecordingLogger:
        def __getattr__(self, name):
            def record(*args, **kwargs):
                events.append(str(args[0]) if args else "")

            return record

    async def fake_run_entry(entry, test_number):
        events.append(f"RUN{test_number}")
        return {
            "test_number": test_number,
            "results": [
                {
                    "type": "integration",
                    "input": "~fake",
                    "output": None,
                    "action": [],
                    "expected": None,
                    "match": None,
                }
            ],
            "note": None,
        }

    class _FakeSuite:
        def __init__(self):
            self.test_cases = []

        def add_testcase(self, testcase):
            self.test_cases.append(testcase)

    async def fake_case(msg):
        pass

    registry_entry = {
        "func": fake_case,
        "input": "~fake",
        "expected": None,
        "note": None,
        "timeout": None,
        "file": "fake.py",
        "line": 1,
    }
    registry_suite = _FakeSuite()
    func_suite = _FakeSuite()

    with (
        patch.object(tester_module, "Logger", _RecordingLogger()),
        patch.object(tester_module, "IS_CI", True),
        patch.object(tester_module, "init_db", new=AsyncMock(return_value=True)),
        patch.object(tester_module, "close_db", new=AsyncMock()),
        patch.object(tester_module, "load_modules", new=AsyncMock()),
        patch.object(tester_module, "get_registry", return_value=[registry_entry, registry_entry]),
        patch.object(tester_module, "_run_registry_entry", new=fake_run_entry),
        patch.object(tester_module, "_collect_test_files", return_value=[]),
        patch.object(tester_module, "junit_registry_suite", registry_suite),
        patch.object(tester_module, "junit_func_suite", func_suite),
        patch.object(tester_module, "junit_report") as junit_report,
    ):
        junit_report.test_suites = []
        exit_code = await tester_module.main()

    header_one = next(index for index, event in enumerate(events) if event.startswith("TEST1:"))
    header_two = next(index for index, event in enumerate(events) if event.startswith("TEST2:"))
    second_run = events.index("RUN2")
    checks = {
        "reported_before_next_run": header_one < second_run < header_two,
        "one_case_per_entry": len(registry_suite.test_cases) == 2,
        "exit_ok": exit_code == 0,
    }
    if not all(checks.values()):
        raise AssertionError(f"registry reporting regression: {checks}; events={events}")
    return True


async def _plugin_cancels_orphan_tasks_after_test():
    from akaribot.testing.tasks import cancel_orphan_tasks, current_tasks

    baseline = await current_tasks()
    cancelled = asyncio.Event()

    async def orphan():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    task = asyncio.create_task(orphan(), name="test-plugin-orphan")
    try:
        completed = await cancel_orphan_tasks(baseline)
    finally:
        if not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
    return completed and task.cancelled() and cancelled.is_set()


async def _plugin_async_timeout_is_failure():
    from akaribot.testing.pytest_plugin import TestTimeout, run_with_timeout

    cancelled = asyncio.Event()

    async def stuck():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    try:
        await run_with_timeout(stuck(), 0.01)
    except TestTimeout:
        return cancelled.is_set()
    return False


async def _plugin_timeout_error_from_test_is_not_timeout():
    from akaribot.testing.pytest_plugin import TestTimeout, run_with_timeout

    async def inner_deadline():
        raise TimeoutError("inner deadline")

    try:
        await run_with_timeout(inner_deadline(), 5)
    except TestTimeout:
        return False
    except TimeoutError as error:
        return str(error) == "inner deadline"
    return False


@func_case
async def test_tester_framework(tester: Tester):
    """akaribot.core.tester 测试框架自身一致性测试"""
    await tester.test(_test_mock_session_signature_matches_real, "mock 会话签名与真实实现一致测试")
    await tester.test(_test_mock_response_supports_all_formats, "mock 响应支持全部 fmt 测试")
    await tester.test(_test_contains_matches_non_text_element, "文本断言命中非文本元素测试")
    await tester.test(_test_contains_still_rejects_absent_text, "文本断言不误报测试")
    await tester.test(_test_junit_coerces_error_details_to_text, "JUnit 异常详情文本化测试")
    await tester.test(_test_integrate_preserves_unexpected_exception, "func_case 保留非预期异常测试")
    await tester.test(_test_integrate_expected_exception_is_not_runner_error, "func_case 预期异常匹配测试")
    await tester.test(_test_function_entry_timeout_is_structured_failure, "func_case 超时结构化失败测试")
    await tester.test(_test_function_entry_timeout_resets_on_progress, "func_case 超时按进展刷新测试")
    await tester.test(
        _test_protocol_exception_is_recorded_without_stopping_function_test,
        "业务控制流异常不终止 func_case 测试",
    )
    await tester.test(
        _test_case_entry_cancels_orphaned_tasks_before_next_database_context,
        "注册表用例之间回收遗留任务测试",
    )
    await tester.test(_test_function_entry_bounds_cancellation_cleanup, "func_case 取消收尾有界测试")
    await tester.test(
        _test_cancelled_progress_waiter_does_not_reset_deadline,
        "进度等待器取消不刷新 watchdog 测试",
    )
    await tester.test(_test_unit_subtest_exception_keeps_running_and_counts_once, "unit 子测试异常续跑且计数一次测试")
    await tester.test(_test_main_reports_registry_case_before_next_entry, "注册表用例逐条汇报测试")
    await tester.test(_test_load_modules_reuses_locale_snapshot, "语言包快照每个进程只建置一次测试")
    await tester.test(_test_http_fixtures_registered_once_per_directory, "HTTP 语料每个目录只注册一次测试")
    await tester.test(_plugin_cancels_orphan_tasks_after_test, "pytest 插件在用例结束后回收遗留任务测试")
    await tester.test(_plugin_async_timeout_is_failure, "pytest 插件将异步用例超时判定为失败测试")
    await tester.test(_plugin_timeout_error_from_test_is_not_timeout, "用例自身抛出的 TimeoutError 不算测试超时")
    await tester.test(_test_function_entry_does_not_misclassify_test_timeout, "子测试超时不冒充 runner 超时测试")
    await tester.test(_test_function_entry_init_failure_is_error, "func_case 初始化错误不可跳过测试")
    await tester.test(_test_setup_timing_flag_reads_environment, "准备耗时开关读取环境变量测试")
    await tester.test(_test_setup_timing_reports_database_stages, "准备耗时日志记录数据库初始化各阶段耗时")
    await tester.test(
        _test_setup_timing_logs_preparation_phases,
        "启用准备耗时日志后逐入口打印三段耗时",
    )
    await tester.test(_test_setup_timing_reports_runtime_state, "准备耗时日志记录 CPU、线程与任务计数测试")
    await tester.test(_test_union_merge_logs_stay_out_of_repo_data, "合并日志不落进 data/ 测试")

    return tester
