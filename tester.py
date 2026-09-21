from akaribot.core.version import check_python_version  # skipcq

check_python_version()  # noqa

import atexit
import os
import shutil
import tempfile
from pathlib import Path

from loguru import logger

# ========== 测试配置引导 ==========
TEST_CONFIG_PATH_ENV = "AKARI_CONFIG_PATH"  # 须与 core.constants.path.CONFIG_PATH_ENV 一致

# union 合并日志目录，须与 core.constants.path.UNION_MERGE_LOGS_PATH_ENV 一致。
# 用例会真实走到合并流程，逐次写下的快照日志只在人工回溯真实合并时才有意义，
# 留在 data/ 里只会随每次测试运行越积越多。
TEST_UNION_MERGE_LOGS_PATH_ENV = "AKARI_UNION_MERGE_LOGS_PATH"

# 测试所需的配置覆盖项，格式为 (表名, 键名, 值)。文件名不再逐项硬编码：现行扁平布局下
# 一个表名恰好对应一个配置文件，映射由 CFGManager 的写入路径完成（P4.4 后由 ConfigLayout 提供）。
TEST_CONFIG_OVERRIDES: list[tuple[str, str, object]] = [
    ("config", "enable_petal", True),
    # 通用测试进程不启动守护进程所管理的 WebSocket Hub。数据库后端
    # 作为自包含测试基座；WebSocket 的真实连接行为由专项用例显式建立 Hub 验证。
    ("jobqueue", "jobqueue_backend", "database"),
]


def _write_minimal_config(path: Path, locale: str, version: int) -> None:
    """写出仅含 default_locale 与 config_version 的配置骨架。

    注释先以 i18n 标记落盘，待 i18n 快照就绪后由配置模板扫描统一翻译。版本号取当前值：
    core/config/update.py 的迁移在导入期执行，低于目标版本会被逐级升级。
    本函数须在 ``AKARI_CONFIG_PATH`` 置位之后调用，其内的 core.constants 导入会固化配置目录。

    :param path: 配置目录。
    :param locale: 默认语言代码。
    :param version: 当前配置版本号。
    """
    from akaribot.core.constants import config_filename

    (path / config_filename).write_text(
        "# {I18N:config.header.line.1}\n"
        "# {I18N:config.header.line.2}\n"
        "# {I18N:config.header.line.3}\n"
        "\n"
        f'default_locale = "{locale}" # {{I18N:config.comments.default_locale}}\n'
        f"config_version = {version} # {{I18N:config.comments.config_version}}\n",
        encoding="utf-8",
    )


def _install_test_union_merge_logs() -> Path:
    """
    把 union 合并日志引到临时目录，避免测试合成的日志堆积在 data/ 中。

    日志写入本身仍被完整走到，只是产物随进程退出一并删除；需要留存时
    可自行设置 ``AKARI_UNION_MERGE_LOGS_PATH``，已显式设置的值优先。
    先行设置过的运行器（如 tests/run_one.py）直接沿用，不再另建一份目录。

    :return: 日志目录的路径。
    """
    configured = os.environ.get(TEST_UNION_MERGE_LOGS_PATH_ENV)
    if configured:
        return Path(configured)

    path = Path(tempfile.mkdtemp(prefix="akari_test_union_merge_logs_"))
    os.environ[TEST_UNION_MERGE_LOGS_PATH_ENV] = str(path)
    atexit.register(lambda: shutil.rmtree(path, ignore_errors=True))
    return path


def _install_test_config() -> Path:
    """
    铺好一份测试专用配置，并令其后的导入一律指向它。

    配置不再取自仓库内的配置快照：只写最小骨架，其余键由配置模板扫描补全，
    因此仓库里不存在需要与代码同步维护的派生配置。

    :return: 临时配置目录的路径。
    """
    path = Path(tempfile.mkdtemp(prefix="akari_test_config_"))

    # 顺序约束：AKARI_CONFIG_PATH 与 AKARI_UNION_MERGE_LOGS_PATH 都须先于任何 core.* 导入生效。
    # 二者分别固化为配置目录与合并日志目录，未置位时都会落到真实的 config/ 与 data/。
    os.environ[TEST_CONFIG_PATH_ENV] = str(path)

    from akaribot.core.constants import default_locale
    from akaribot.core.constants.version import config_version

    _write_minimal_config(path, default_locale, config_version)

    from akaribot.core.config import CFGManager
    from akaribot.core.config.scan import scan_config_templates
    from akaribot.core.constants import lang_list
    from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot

    # i18n 快照须先接上：模板生成的注释取自配置文件声明的语言，未接上时全部退化为 i18n 键名。
    build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")

    failed_templates = scan_config_templates()
    if failed_templates:
        logger.warning(f"Failed to generate test config from templates: {failed_templates}")

    # 覆盖项走配置管理器的写入路径，使磁盘与内存副本保持一致：直接改写文件时，
    # 同一文件系统时间戳精度内的改动可能躲过 watch() 的重载判定。
    for table, key, value in TEST_CONFIG_OVERRIDES:
        CFGManager.write(key, value, table_name=table)

    atexit.register(lambda: shutil.rmtree(path, ignore_errors=True))
    return path


# 两项引导都必须早于本模块后续的 core.* 导入。合并日志目录在前：它的取值只依赖环境变量，
# 而配置引导内部会导入 core.constants，届时未置位的变量即被永久固化。
test_union_merge_logs_path = _install_test_union_merge_logs()
test_config_path = _install_test_config()

import asyncio
import glob
import importlib.util
import inspect
import sys
import traceback
from types import FunctionType
from typing import TypedDict

from dotenv import load_dotenv

from akaribot.core.builtins.utils import confirm_command
from akaribot.core.constants import ascii_art, cache_path, tests_path
from akaribot.testing.decorator import CaseEntry, get_registry
from akaribot.testing.expectations import Expectation
from akaribot.testing.logger import TestLoggingLogger
from akaribot.testing.junit import JUnitReport, JUnitTestSuite, JUnitTestCase
from akaribot.testing.mock.database import close_db, get_last_init_error, init_db
from akaribot.testing.mock.loader import load_modules
from akaribot.testing.mock.random import Random
from akaribot.testing.process import run_case_entry, run_function_entry

Logger = TestLoggingLogger("TEST")


def _source_import_roots() -> list[Path]:
    """源码检出下提供 ``akaribot`` 命名空间的目录。

    各包源码存放在 ``packages[/<类>]/<包名>/src``，仓库根本身不再有可导入的 ``akaribot``。
    判据只用目录是否存在，不依赖已安装分发的 metadata：安装形态下这些目录不存在，结果为空列表。
    仓库根一并保留，使 ``tester`` 等根级脚本对子进程仍可导入。

    :return: 参与 PYTHONPATH 的目录列表，按路径排序。
    """
    root = Path(__file__).resolve().parent
    candidates = [root, *sorted(root.glob("packages/*/src")), *sorted(root.glob("packages/*/*/src"))]
    return [path for path in candidates if path.is_dir()]


load_dotenv()
os.environ.setdefault("PYTHONIOENCODING", "UTF-8")
os.environ.setdefault("PYTHONPATH", os.pathsep.join(str(path) for path in _source_import_roots()))

IS_CI = os.environ.get("CI", "0") == "1"
ENABLE_COVERAGE = os.environ.get("COVERAGE", "0") == "1"
MAX_CONCURRENT = 1

# Coverage 集成
_coverage_instance = None
if ENABLE_COVERAGE:
    try:
        import coverage

        _coverage_instance = coverage.Coverage(
            source=["akaribot"],
            omit=[
                "*/tests/*",
                "*/test_*",
                "*/__pycache__/*",
                "*/.venv/*",
            ],
        )
        _coverage_instance.start()
        Logger.info("Coverage collection enabled.")
    except ImportError:
        Logger.warning("coverage package not installed. Run: pip install coverage")
        _coverage_instance = None
    except Exception as e:
        Logger.warning(f"Failed to initialize coverage: {e}")
        _coverage_instance = None

junit_report = JUnitReport()
junit_registry_suite = JUnitTestSuite("Registry Tests")
junit_func_suite = JUnitTestSuite("Function Tests")


async def _run_registry_entry(semaphore: asyncio.Semaphore, entry: CaseEntry, test_number: int) -> dict:
    Logger.trace(f"_run_registry_entry START: TEST{test_number}")
    async with semaphore:
        Logger.trace(f"_run_registry_entry ACQUIRED semaphore: TEST{test_number}")
        fn = entry["func"]
        note = entry.get("note") or (fn.__doc__ if fn.__doc__ else None)
        file_loc = f"{entry.get('file')}:{entry.get('line')}"
        Logger.info(f"TEST{test_number}: {fn.__name__} ({file_loc})")
        if fn.__doc__:
            Logger.info(f"DOC: {fn.__doc__}")

        Logger.trace(f"_run_registry_entry run_case_entry: TEST{test_number}")
        results = await run_case_entry(entry, IS_CI)
        Logger.trace(f"_run_registry_entry DONE: TEST{test_number}")
        return {"test_number": test_number, "results": results, "note": note}


class FuncTestResult(TypedDict):
    """单个 @func_case 测试的运行结果。"""

    fn: FunctionType
    path: str
    res: dict


def _test_roots() -> list[Path]:
    """测试文件根目录。

    仓库根的 ``tests/`` 承载跨包用例与共享夹具，各成员包自带的 ``tests/`` 随包分发。

    :return: 存在的目录列表，包内目录按路径排序。
    """
    repo_root = Path(__file__).resolve().parent
    roots = [Path(tests_path)]
    for pattern in ("packages/*/tests", "packages/*/*/tests"):
        roots.extend(root for root in sorted(repo_root.glob(pattern)) if root.is_dir())
    return [root for root in roots if root.is_dir()]


def _test_module_key(path: str) -> str:
    """测试文件的合成模块名。

    按仓库根相对路径生成：不同包里可以存在同名测试文件，仅取文件名会互相覆盖。

    :param path: 测试文件路径。
    :return: ``sys.modules`` 中使用的模块名。
    """
    repo_root = Path(__file__).resolve().parent
    try:
        relative = Path(path).resolve().relative_to(repo_root)
    except ValueError:
        relative = Path(path)
    return "tests_" + "_".join(part.replace("-", "_") for part in relative.with_suffix("").parts)


def _collect_test_files() -> list[str]:
    """收集全部待运行的测试文件。

    :return: 文件路径列表，按路径排序且去重。
    """
    files: list[str] = []
    for root in _test_roots():
        files.extend(glob.glob(os.path.join(root, "**", "*.py"), recursive=True))
    return sorted(set(files))


async def _run_func_test(fn: FunctionType, path: str) -> FuncTestResult:
    Logger.trace(f"_run_func_test START: {fn.__name__} ({path})")
    res = await run_function_entry(fn, IS_CI)
    Logger.trace(f"_run_func_test DONE: {fn.__name__}")
    return {"fn": fn, "path": path, "res": res}


async def main(inspect_module=inspect):
    Logger.trace("main() START")

    cache_path.mkdir(parents=True, exist_ok=True)

    Logger.trace("main() init_db")
    try:
        if not await init_db():
            Logger.critical(f"Failed to initialize database. Aborting tests.\n{get_last_init_error()}")
            await close_db()
            return 1
    except Exception:
        Logger.exception()
        await close_db()
        return 1

    Logger.trace("main() load_modules")
    try:
        await load_modules(monkey_patches={"Random": Random()})
    except Exception:
        Logger.exception("Failed to load modules for tests:")
        await close_db()
        return 1

    Logger.trace("main() get_registry")
    Logger.info(ascii_art)
    Logger.info("=" * 60)
    Logger.info("Tester is running. Please wait...")
    Logger.info("=" * 60)
    registry = get_registry()
    Logger.trace(f"main() registry has {len(registry)} entries")

    test_number = 0
    total = 0
    passed = 0
    failed = 0
    total_test_cost = 0.0
    force_exit = False

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    registry_tasks = []

    Logger.trace("main() creating registry tasks")
    for idx, entry in enumerate(registry, 1):
        task = _run_registry_entry(semaphore, entry, idx)
        registry_tasks.append(task)

    Logger.trace(f"main() gathering {len(registry_tasks)} registry tasks")
    registry_results = await asyncio.gather(*registry_tasks, return_exceptions=True)
    Logger.trace(f"main() registry tasks completed, got {len(registry_results)} results")

    for registry_index, reg_result in enumerate(registry_results, 1):
        if isinstance(reg_result, Exception):
            Logger.error(f"Error during test execution: {reg_result}")
            Logger.trace(f"main() EXCEPTION in registry result: {reg_result}")
            failed += 1
            total += 1
            junit_testcase = JUnitTestCase(
                name=f"TEST{registry_index}_runner", classname=f"RegistryTest.{registry_index}"
            )
            junit_testcase.error = ("Test runner error", repr(reg_result))
            junit_registry_suite.add_testcase(junit_testcase)
            continue

        if not isinstance(reg_result, dict):
            Logger.trace(f"main() non-dict result: {type(reg_result)}")
            failed += 1
            total += 1
            junit_testcase = JUnitTestCase(
                name=f"TEST{registry_index}_invalid_result", classname=f"RegistryTest.{registry_index}"
            )
            junit_testcase.error = ("Invalid test result", repr(reg_result))
            junit_registry_suite.add_testcase(junit_testcase)
            continue

        Logger.info("-" * 60)

        test_number = reg_result.get("test_number")
        note = reg_result.get("note")
        results = reg_result.get("results", [])
        Logger.trace(f"main() processing TEST{test_number} with {len(results)} results")

        for r in results:
            total += 1
            inp = r.get("input")
            tcost = r.get("time_cost", 0.0)
            test_case_name = f"TEST{test_number}_{total}"
            junit_testcase = JUnitTestCase(
                name=test_case_name, classname=f"RegistryTest.{test_number}", time=tcost if tcost else 0.0
            )

            if "timeout" in r:
                Logger.error(f"INPUT: {inp}")
                if note:
                    Logger.error(f"NOTE: {note}")
                Logger.error("RESULT: FAIL (timeout)")
                failed += 1
                junit_testcase.failure = (
                    "Test timeout",
                    f"Test exceeded timeout limit\nInput: {inp}\nNote: {note or 'N/A'}",
                )
                junit_registry_suite.add_testcase(junit_testcase)
                continue

            if "traceback" in r:
                Logger.error(f"INPUT: {inp}")
                if note:
                    Logger.error(f"NOTE: {note}")
                Logger.error("ERROR during execution:")
                Logger.error(r.get("traceback"))
                failed += 1
                junit_testcase.error = ("Test execution error", r.get("traceback", "Unknown error"))
                junit_registry_suite.add_testcase(junit_testcase)
                continue

            action = r.get("action", [])
            fmted_output = "\n".join(action) if action else "[NO OUTPUT]"
            expected = r.get("expected")
            Logger.info(f"INPUT: {inp}")
            if note:
                Logger.info(f"NOTE: {note}")
            Logger.info(f"OUTPUT:\n{fmted_output}")

            if isinstance(expected, Expectation):
                Logger.info(f"EXPECT: {expected}")
                Logger.trace(f"main() matching expectation for TEST{test_number}")
                match = await expected.match(r)
                Logger.trace(f"main() match result: {match}")
                if match:
                    Logger.success("RESULT: PASS")
                    passed += 1
                elif match is False:
                    Logger.error("RESULT: FAIL")
                    failed += 1
                    junit_testcase.failure = ("Assertion failed", f"Expected: {expected}\nActual: {fmted_output}")
                    junit_registry_suite.add_testcase(junit_testcase)
                    continue
            else:
                if IS_CI:
                    Logger.info("RESULT: SKIP (expects manual review, unavailable in CI)")
                    junit_testcase.skipped = "Manual review required (unavailable in CI)"
                    junit_registry_suite.add_testcase(junit_testcase)
                    continue
                else:
                    Logger.trace(
                        f"main() MANUAL REVIEW required for TEST{test_number} - this will HANG in non-CI mode!"
                    )
                    try:
                        Logger.warning("REVIEW: Did the output meet expectations? [y/N]")
                        check = input()
                        if check in confirm_command:
                            Logger.success("RESULT: PASS")
                            passed += 1
                        else:
                            Logger.error("RESULT: FAIL")
                            failed += 1
                            junit_testcase.failure = (
                                "Manual review failed",
                                f"Expected: {expected}\nActual: {fmted_output}",
                            )
                            junit_registry_suite.add_testcase(junit_testcase)
                            continue
                    except (EOFError, KeyboardInterrupt):
                        print("")
                        Logger.warning("Interrupted by user.")
                        os._exit(1)

            junit_registry_suite.add_testcase(junit_testcase)

            if tcost is not None:
                Logger.info(f"TIME COST: {tcost:.06f}s")
                total_test_cost += tcost
        Logger.info("-" * 60)

    Logger.trace("main() starting func tests discovery")
    pyfiles = _collect_test_files()
    if pyfiles:
        Logger.trace(f"main() found {len(pyfiles)} test files")
        func_tasks: list[tuple[FunctionType, str]] = []

        for path in pyfiles:
            Logger.trace(f"main() importing {path}")
            spec = importlib.util.spec_from_file_location(_test_module_key(path), path)
            if not spec or not spec.loader:
                message = f"Failed resolving tests file {path}."
                Logger.error(message)
                failed += 1
                total += 1
                junit_testcase = JUnitTestCase(name=Path(path).name, classname="TestCollection")
                junit_testcase.error = ("Test file resolution error", message)
                junit_func_suite.add_testcase(junit_testcase)
                continue
            mod = importlib.util.module_from_spec(spec)
            try:
                sys.modules[spec.name] = mod
                spec.loader.exec_module(mod)
            except Exception:
                import_error = traceback.format_exc()
                Logger.exception(f"Failed importing tests file {path}:")
                failed += 1
                total += 1
                junit_testcase = JUnitTestCase(name=Path(path).name, classname="TestCollection")
                junit_testcase.error = ("Test file import error", import_error)
                junit_func_suite.add_testcase(junit_testcase)
                continue

            for _, fn in inspect_module.getmembers(mod, inspect_module.isfunction):
                if not getattr(fn, "_func_case", False):
                    continue

                Logger.trace(f"main() found func_case: {fn.__name__} in {path}")
                func_tasks.append((fn, path))

        Logger.trace(f"main() running {len(func_tasks)} func tests sequentially")
        func_results = []
        for fn, path in func_tasks:
            Logger.trace(f"main() about to run func test: {fn.__name__}")
            try:
                result = await _run_func_test(fn, path)
                func_results.append(result)
                if result["res"].get("cleanup_pending"):
                    force_exit = True
                    Logger.error(f"Stopping after {fn.__name__}: timed-out task did not finish cancellation cleanup.")
                    break
            except Exception as e:
                Logger.error(f"main() EXCEPTION running func test {fn.__name__}: {e}")
                func_results.append({"fn": fn, "path": path, "res": {"error": repr(e)}})
            Logger.trace(f"main() finished func test: {fn.__name__}")
        Logger.trace(f"main() all func tests completed, got {len(func_results)} results")

        for idx, func_result in enumerate(func_results):
            Logger.trace(f"main() processing func result {idx}/{len(func_results)}")
            if not isinstance(func_result, dict):
                Logger.trace(f"main() non-dict func result at index {idx}")
                failed += 1
                total += 1
                junit_testcase = JUnitTestCase(name=f"invalid_result_{idx}", classname="FunctionTest")
                junit_testcase.error = ("Invalid function test result", repr(func_result))
                junit_func_suite.add_testcase(junit_testcase)
                continue

            fn = func_result["fn"]
            path = func_result["path"]
            res = func_result.get("res", {})

            test_number = len(registry) + idx + 1

            Logger.info(f"TEST{test_number}: {fn.__name__} ({path})")
            if fn.__doc__:
                Logger.info(f"DOC: {fn.__doc__}")

            Logger.info("-" * 60)

            if res.get("skipped"):
                Logger.trace(f"main() func test {fn.__name__} skipped")
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
                junit_testcase.skipped = "Test skipped"
                junit_func_suite.add_testcase(junit_testcase)
                total += 1
                continue
            if res.get("timeout"):
                Logger.trace(f"main() func test {fn.__name__} timed out")
                failed += 1
                total += 1
                timeout_limit = res.get("timeout_limit")
                active_test = res.get("active_test")
                completed_tests = res.get("completed_tests", 0)
                detail = f"No progress for {timeout_limit} seconds after {completed_tests} completed subtests"
                if active_test:
                    detail += f"\nActive subtest: {active_test}"
                if res.get("cleanup_pending"):
                    detail += "\nCancellation cleanup exceeded its deadline"
                Logger.error(detail)
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
                junit_testcase.failure = ("Function test timeout", detail)
                junit_func_suite.add_testcase(junit_testcase)
                continue
            if res.get("error"):
                Logger.trace(f"main() func test {fn.__name__} has error")
                failed += 1
                total += 1
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
                junit_testcase.error = ("Test error", res.get("error", "Unknown error"))
                junit_func_suite.add_testcase(junit_testcase)
                continue

            entries = res["entries"]
            if not entries:
                Logger.warning(f"No inputs registered in func test {fn.__name__}; skipping.")
                Logger.trace(f"main() func test {fn.__name__} has no entries")
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
                junit_testcase.skipped = "No inputs registered"
                junit_func_suite.add_testcase(junit_testcase)
                total += 1
                continue

            results = res["results"]
            Logger.trace(f"main() processing func test {fn.__name__} with {len(results)} results")

            subtest_number = 0
            func_pass = True
            func_error_msgs: list[str] = []
            for r_idx, r in enumerate(results):
                Logger.trace(f"main() processing result {r_idx}/{len(results)} for {fn.__name__}")
                type_ = r.get("type")
                note = r.get("note")
                inp = r.get("input")

                if "timeout" in r:
                    if type_ == "integration":
                        Logger.error(f"INPUT: {inp}")
                    if note:
                        Logger.error(f"NOTE: {note}")
                    Logger.error("RESULT: FAIL (timeout)")
                    func_pass = False
                    if type_ == "integration":
                        func_error_msgs.append(f"Test timeout for input: {inp}")
                    else:
                        func_error_msgs.append("Test timeout")
                    break

                if "traceback" in r:
                    if type_ == "integration":
                        Logger.error(f"INPUT: {inp}")
                    if note:
                        Logger.error(f"NOTE: {note}")
                    Logger.error("ERROR during execution:")
                    Logger.error(r.get("traceback"))
                    func_pass = False
                    func_error_msgs.append(r.get("traceback", "Unknown error"))
                    if type_ == "integration":
                        break
                    Logger.error("RESULT: FAIL (exception)")
                    continue

                expected = r.get("expected")
                action = r.get("action", [])
                fmted_output = "\n".join(action) if action else "[NO OUTPUT]"

                Logger.trace(f"main() checking result: expected={expected}, match={r.get('match')}")
                if type_ == "integration":
                    Logger.info(f"INPUT: {inp}")
                if note:
                    Logger.info(f"NOTE: {note}")
                if type_ == "integration":
                    Logger.info(f"OUTPUT:\n{fmted_output}")

                if expected is not None:
                    Logger.info(f"EXPECT: {expected}")

                if r.get("match"):
                    Logger.trace("main() match is truthy, PASS")
                    Logger.success("RESULT: PASS")
                    continue
                Logger.trace("main() match is falsy or None, checking expected...")
                if expected is None:
                    if IS_CI:
                        Logger.info("RESULT: SKIP (expects manual review, unavailable in CI)")
                        continue
                    Logger.trace(f"main() MANUAL REVIEW required for func test {fn.__name__} - this will HANG!")
                    try:
                        Logger.warning("REVIEW: Did the output meet expectations? [y/N]")
                        check = input()
                        if check in confirm_command:
                            Logger.success("RESULT: PASS")
                            continue
                        func_pass = False
                        func_error_msgs.append(f"Manual review failed for input: {inp}")
                    except (EOFError, KeyboardInterrupt):
                        print("")
                        Logger.warning("Interrupted by user.")
                        os._exit(1)
                else:
                    Logger.error("RESULT: FAIL")
                    func_pass = False
                    func_error_msgs.append(f"Expected: {expected}\nActual: {fmted_output}")
                break

            func_error_msg = "\n".join(func_error_msgs)
            if func_pass:
                Logger.success(f"FUNC ({fn.__name__}) RESULT: PASS")
                passed += 1
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
            else:
                Logger.error(f"FUNC ({fn.__name__}) RESULT: FAIL")
                failed += 1
                junit_testcase = JUnitTestCase(
                    name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
                )
                junit_testcase.failure = ("Function test failed", func_error_msg)

            junit_func_suite.add_testcase(junit_testcase)

            for failed_result in results:
                if failed_result.get("match"):
                    continue
                if "traceback" not in failed_result:
                    continue
                subtest_number += 1
                subtest_name = failed_result.get("note") or getattr(
                    failed_result.get("expected"), "__name__", str(failed_result.get("expected"))
                )
                junit_subtest = JUnitTestCase(
                    name=f"{fn.__name__}::{subtest_name}",
                    classname=f"FunctionTest.{test_number}.{subtest_number}",
                    time=res.get("time_cost", 0.0),
                )
                if failed_result.get("type") == "integration":
                    junit_subtest.error = ("Test execution error", failed_result.get("traceback", "Unknown error"))
                else:
                    junit_subtest.failure = (
                        f"Subtest raised {failed_result.get('exception_type', 'Exception')}",
                        failed_result.get("traceback", "Unknown error"),
                    )
                junit_func_suite.add_testcase(junit_subtest)

            tcost = res.get("time_cost")
            if tcost is not None:
                Logger.info(f"TIME COST: {tcost:.06f}s")
                total_test_cost += tcost

            total += 1
            Logger.info("-" * 60)

    Logger.trace("main() all tests processed")
    if total > 0:
        Logger.info(f"TOTAL: {total}")
        if passed:
            Logger.success(f"PASSED: {passed}")
        if failed:
            Logger.error(f"FAILED: {failed}")
        Logger.info(f"TIME COST: {total_test_cost:.06f}s")
        Logger.info("=" * 60)
    else:
        Logger.warning(
            "No tests registered. Use `akaribot.testing.case` or `akaribot.testing.test_case` to register tests."
        )

    if IS_CI:
        try:
            junit_report.add_testsuite(junit_registry_suite)
            if junit_func_suite.test_cases:
                junit_report.add_testsuite(junit_func_suite)

            junit_output_path = Path("junit.xml")
            junit_report.write_to_file(junit_output_path)
            Logger.success(f"JUnit XML report generated: {junit_output_path}")
        except Exception as e:
            Logger.error(f"Failed to generate JUnit XML report: {e}")

    if force_exit:
        Logger.error("Forcing tester shutdown because a timed-out task is still running.")
        shutil.rmtree(test_config_path, ignore_errors=True)
        shutil.rmtree(test_union_merge_logs_path, ignore_errors=True)
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)

    # Coverage 报告生成
    if _coverage_instance:
        try:
            _coverage_instance.stop()
            _coverage_instance.save()

            # 生成控制台报告
            Logger.info("=" * 60)
            Logger.info("Coverage Report:")
            _coverage_instance.report(show_missing=True)

            # 生成 HTML 报告
            html_dir = Path("htmlcov")
            _coverage_instance.html_report(directory=str(html_dir))
            Logger.success(f"HTML coverage report generated: {html_dir}/index.html")

            # 生成 XML 报告（可选，用于 CI 集成）
            if IS_CI:
                _coverage_instance.xml_report(outfile="coverage.xml")
                Logger.success("XML coverage report generated: coverage.xml")
        except Exception as e:
            Logger.error(f"Failed to generate coverage report: {e}")

    Logger.trace("main() close_db")
    await close_db()

    Logger.trace("main() END")
    return 1 if IS_CI and (failed > 0 or total == 0) else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
