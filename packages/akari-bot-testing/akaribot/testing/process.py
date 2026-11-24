import asyncio
import os
import threading
import time
import traceback
from types import FunctionType
from typing import Any, Callable

from akaribot.core.builtins.message.chain import MessageChain, match_kecode
from akaribot.core.builtins.message.elements import PlainElement
from akaribot.core.constants.exceptions import SessionFinished
from akaribot.core.database.models import SenderUnionInfo, TargetUnionInfo
from akaribot.core.logger import Logger
from akaribot.testing.logger import TEST_LOGGER
from akaribot.testing.mock.database import close_db, get_last_init_error, get_last_init_timings, init_db
from akaribot.testing.mock.loader import load_modules
from akaribot.testing.mock.parser import parser
from akaribot.testing.mock.random import Random
from akaribot.testing.mock.session import MockMessageSession
from akaribot.core.utils.container import ExpiringTempDict
from .decorator import CaseEntry
from .expectations import Expectation
from .tasks import PROGRESS_TASK_PREFIX, cancel_orphan_tasks, cancel_task
from .timing import TIME_SCALE

# 无进展超时监控随测试时限系数放大，但封顶 5 倍，这样在性能受限的计算机上子测试可以更久，
# 真正无响应时也避免使单个用例占用整个 CI 任务过长时间。
DEFAULT_FUNCTION_TEST_TIMEOUT = 120.0 * min(TIME_SCALE, 5.0)

# 设置该变量后，每个入口打印一行准备阶段耗时，便于定位耗时偏高的准备步骤。
SETUP_TIMING_ENV = "AKARI_TEST_SETUP_TIMING"


def _setup_timing_enabled() -> bool:
    return os.environ.get(SETUP_TIMING_ENV, "").strip().lower() in {"1", "true", "yes"}


_runtime_cpu_mark: float | None = None


# 准备耗时突然变大时，需要区分是准备本身变慢，还是进程受其他负载影响，因此同时采集
# 自上一个入口以来累计的进程 CPU 时间、活动线程数与未完成任务数。
def _runtime_snapshot() -> dict[str, object]:
    global _runtime_cpu_mark
    cpu = time.process_time()
    cpu_delta = 0.0 if _runtime_cpu_mark is None else cpu - _runtime_cpu_mark
    _runtime_cpu_mark = cpu
    counts: dict[str, int] = {}
    for thread in threading.enumerate():
        counts[thread.name] = counts.get(thread.name, 0) + 1
    top = sorted(counts.items(), key=lambda item: -item[1])[:3]
    try:
        tasks = len(asyncio.all_tasks())
    except RuntimeError:
        tasks = -1
    return {
        "cpu": cpu_delta,
        "threads": threading.active_count(),
        "tasks": tasks,
        "top_threads": ",".join(f"{thread_name}x{count}" for thread_name, count in top),
    }


def format_setup_timing(
    kind: str,
    name: str,
    close_db: float,
    init_db: float,
    load_modules: float,
    db_timings: dict[str, float] | None = None,
    runtime: dict[str, object] | None = None,
) -> str:
    """把入口准备阶段的耗时与进程运行状态拼接为一行日志。"""
    text = (
        f"[SETUP] kind={kind} name={name} close_db={close_db:.3f}s "
        f"init_db={init_db:.3f}s load_modules={load_modules:.3f}s "
        f"setup={close_db + init_db + load_modules:.3f}s"
    )
    if db_timings:
        text += (
            f" db_models={int(db_timings.get('models', 0))}"
            f" db_fetch={db_timings.get('fetch_db', 0.0):.3f}s"
            f" db_import={db_timings.get('import_models', 0.0):.3f}s"
            f" db_init={db_timings.get('tortoise_init', 0.0):.3f}s"
            f" db_schema={db_timings.get('schemas', 0.0):.3f}s"
        )
    if runtime:
        text += (
            f" cpu={float(runtime.get('cpu', 0.0)):.3f}s"
            f" threads={int(runtime.get('threads', 0))}"
            f" tasks={int(runtime.get('tasks', 0))}"
            f" top_threads={runtime.get('top_threads', '')}"
        )
    return text


class _FunctionTestNoProgress(Exception):
    pass


def _infrastructure_error(input_, expected, message: str) -> list[dict]:
    return [{"input": input_, "expected": expected, "traceback": message, "action": []}]


async def run_case_entry(entry: CaseEntry, is_ci: bool = False) -> list[dict]:
    baseline_tasks = set(asyncio.all_tasks())

    setup_started = time.perf_counter()
    try:
        await close_db()
    except Exception:
        Logger.exception("Error closing database before test")
    closed = time.perf_counter()

    if not await init_db():
        message = f"Failed to reinitialize database for case {entry.get('func')}.\n{get_last_init_error()}"
        Logger.critical(message)
        return _infrastructure_error(entry.get("input"), entry.get("expected"), message)
    initialized = time.perf_counter()

    try:
        try:
            await load_modules(show_logs=False, monkey_patches={"Random": Random()})
        except Exception:
            error = traceback.format_exc()
            Logger.exception("Failed to load modules for tests:")
            return _infrastructure_error(entry.get("input"), entry.get("expected"), error)
        loaded = time.perf_counter()
        if _setup_timing_enabled():
            TEST_LOGGER.info(
                format_setup_timing(
                    "case",
                    str(entry.get("func")),
                    closed - setup_started,
                    initialized - closed,
                    loaded - initialized,
                    get_last_init_timings(),
                    _runtime_snapshot(),
                )
            )

        start = time.perf_counter()
        timeout = entry.get("timeout")
        result = await run_test_case(entry["input"], entry["expected"], entry["func"], is_ci, timeout=timeout)
        elapsed = time.perf_counter() - start
        if "exception" in result and isinstance(result["expected"], Expectation):
            match = await result["expected"].match(result)
            if match:
                del result["traceback"]
        try:
            result["time_cost"] = elapsed
        except Exception:
            pass
        return [result]
    finally:
        # 集成用例会启动 queue poller、waiter 或平台任务，并与后续用例共用事件循环与内存数据库。
        # 游离任务不得越过其捕获的数据库上下文存活。
        if not await cancel_orphan_tasks(baseline_tasks):
            message = "Registry test left a task that did not finish cancellation cleanup."
            Logger.error(message)
            raise RuntimeError(message)


async def run_function_entry(
    fn: FunctionType, is_ci: bool = False, timeout: float | None = DEFAULT_FUNCTION_TEST_TIMEOUT
) -> dict[str, Any]:
    # Every func_case is an isolation boundary. Record existing runner tasks so
    # only work started by this entry is reclaimed after it finishes.
    cleanup_pending = False
    baseline_tasks = set(asyncio.all_tasks())
    setup_started = time.perf_counter()
    try:
        await close_db()
    except Exception:
        Logger.exception("Error closing database before func test")
    closed = time.perf_counter()

    if not await init_db():
        message = f"Failed to reinitialize database for func test {fn.__name__}.\n{get_last_init_error()}"
        Logger.critical(message)
        return {"error": message}
    initialized = time.perf_counter()

    try:
        await load_modules(show_logs=False, monkey_patches={"Random": Random()})
    except Exception:
        error = traceback.format_exc()
        Logger.exception("Failed to load modules for tests:")
        return {"error": error}
    loaded = time.perf_counter()
    if _setup_timing_enabled():
        TEST_LOGGER.info(
            format_setup_timing(
                "func",
                fn.__name__,
                closed - setup_started,
                initialized - closed,
                loaded - initialized,
                get_last_init_timings(),
                _runtime_snapshot(),
            )
        )

    tester = None
    start = time.perf_counter()
    try:
        from akaribot.testing import Tester as TesterClass

        tester = TesterClass(fn.__name__)
        setattr(tester, "is_ci", is_ci)
        if timeout is None:
            returned = await fn(tester)
        else:
            function_task = asyncio.create_task(fn(tester))
            progress_task = None
            progress_revision = tester._progress_revision
            progress_deadline = asyncio.get_running_loop().time() + timeout
            try:
                while True:
                    progress_task = asyncio.create_task(
                        tester._wait_for_progress(progress_revision),
                        name=f"{PROGRESS_TASK_PREFIX}{fn.__name__}",
                    )
                    remaining = max(0.0, progress_deadline - asyncio.get_running_loop().time())
                    done, _ = await asyncio.wait(
                        (function_task, progress_task),
                        timeout=remaining,
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    if function_task in done:
                        progress_task.cancel()
                        await asyncio.gather(progress_task, return_exceptions=True)
                        returned = function_task.result()
                        break
                    if progress_task in done:
                        current_revision = tester._progress_revision
                        if not progress_task.cancelled():
                            current_revision = progress_task.result()
                        if current_revision > progress_revision:
                            progress_revision = current_revision
                            progress_deadline = asyncio.get_running_loop().time() + timeout
                        elif asyncio.get_running_loop().time() >= progress_deadline:
                            raise _FunctionTestNoProgress
                        continue
                    raise _FunctionTestNoProgress
            finally:
                if progress_task is not None and not progress_task.done():
                    await cancel_task(progress_task)
                if not function_task.done():
                    cleanup_pending = not await cancel_task(function_task)
        if isinstance(returned, TesterClass):
            tester = returned
    except _FunctionTestNoProgress:
        elapsed = time.perf_counter() - start
        entries = tester.get_entries() if tester is not None else []
        results = tester.get_results() if tester is not None else []
        active_test = None
        if len(entries) > len(results):
            active_entry = entries[len(results)]
            active_test = active_entry.get("note") or active_entry.get("input")
            if active_test is None:
                expected = active_entry.get("expected")
                active_test = getattr(expected, "__name__", type(expected).__name__)
        message = f"Function test {fn.__name__} made no progress for {timeout} seconds"
        if active_test:
            message += f" while running {active_test!r}"
        Logger.error(f"{message}.")
        cleanup_pending = not await cancel_orphan_tasks(baseline_tasks) or cleanup_pending
        return {
            "timeout": True,
            "time_cost": elapsed,
            "timeout_limit": timeout,
            "active_test": active_test,
            "completed_tests": len(results),
            "cleanup_pending": cleanup_pending,
            "entries": entries,
            "results": results,
        }
    except (asyncio.CancelledError, KeyboardInterrupt, SystemExit, GeneratorExit):
        raise
    except BaseException:
        error = traceback.format_exc()
        Logger.exception(f"Error running test function {fn.__name__}:")
        cleanup_pending = not await cancel_orphan_tasks(baseline_tasks) or cleanup_pending
        return {"error": error, "cleanup_pending": cleanup_pending}

    cleanup_pending = not await cancel_orphan_tasks(baseline_tasks) or cleanup_pending

    elapsed = time.perf_counter() - start
    entries = tester.get_entries()
    results = tester.get_results()
    return {
        "tester": tester,
        "entries": entries,
        "results": results,
        "time_cost": elapsed,
        "cleanup_pending": cleanup_pending,
    }


async def run_test_case(
    input_: str | list[str] | tuple[str, ...],
    expected: Expectation | None = None,
    casetest_target: Callable | None = None,
    is_ci: bool = False,
    timeout: float | None = None,
):
    async def _run_test():
        try:
            await TargetUnionInfo.resolve_union("TEST|Console|0")
            sender_union_info = await SenderUnionInfo.resolve_union("TEST|0")
            await sender_union_info.edit_attr("superuser", True)
        except Exception:
            pass

        msg = MockMessageSession(input_, is_ci=is_ci)
        await msg.async_init(msg.trigger_msg)

        if casetest_target is not None:
            setattr(msg, "_casetest_target", casetest_target)

        try:
            await parser(msg)
        except SessionFinished:
            pass
        except Exception as e:
            err_msg = msg.session_info.locale.t_str(str(e))
            try:
                err_chain = match_kecode(err_msg, disable_joke=True)
            except Exception:
                err_chain = MessageChain.assign(err_msg)

            err_action = [
                x.text if isinstance(x, PlainElement) else str(x) for x in err_chain.as_sendable(msg.session_info)
            ]

            return {
                "input": input_,
                "exception": e,
                "exception_message": err_chain.to_str(),
                "action": [f"(raise {type(e).__name__})"] + err_action,
                "traceback": traceback.format_exc(),
                "expected": expected,
            }
        finally:
            await ExpiringTempDict.clear_all(now=time.time() + 31536000)

        return {
            "input": input_,
            "output": msg.sent,
            "action": msg.action,
            "expected": expected,
        }

    if timeout:
        try:
            result = await asyncio.wait_for(_run_test(), timeout=timeout)
        except asyncio.TimeoutError:
            await ExpiringTempDict.clear_all(now=time.time() + 31536000)
            result = {"input": input_, "expected": expected, "timeout": True}
    else:
        result = await _run_test()
    return result
