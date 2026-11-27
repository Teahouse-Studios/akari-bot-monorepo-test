"""自研测试框架的运行器，根目录兼容实现 ``tester.py`` 的主体。

入口有两个：``python -m akaribot.testing`` 与根目录的兼容实现 ``tester.py``。测试配置的初始化
发生在该模块导入期，且必须早于任何 ``akaribot.core`` 导入，因此该模块的导入顺序不可调整。
仓库根由 ``AKARI_REPO_ROOT`` 或 :func:`_resolve_repo_root` 确定，不按本文件位置回推。
"""

from akaribot.core.environment import check_python_version  # skipcq

check_python_version()  # noqa

import argparse
import atexit
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from loguru import logger

# 测试配置引导。
TEST_CONFIG_PATH_ENV = "AKARI_CONFIG_PATH"  # 必须与 core.constants.path.CONFIG_PATH_ENV 保持一致。

# union 合并日志目录，必须与 core.constants.path.UNION_MERGE_LOGS_PATH_ENV 一致。
# 用例会真实执行到合并流程，逐次写入的快照日志仅在人工回溯真实合并时才有意义，
# 留在 data/ 中会导致其随每次测试运行越积越多。
TEST_UNION_MERGE_LOGS_PATH_ENV = "AKARI_UNION_MERGE_LOGS_PATH"

# 语言快照缓存目录。用例会导入 bot，而守护进程在导入阶段将该变量默认设为 data/i18n_cache。
# 测试进程必须先将环境变量固定为自有的临时目录，否则框架启动时发布的快照与之后的读取方（包括新启动的
# 子进程）会指向不同位置。
TEST_I18N_CACHE_DIR_ENV = "AKARI_BOT_I18N_CACHE_DIR"

# 测试所需的配置覆盖项，格式为 (表名称, 键名称, 值)。在扁平布局下一个表名称对应一个配置文件，
# 映射由 CFGManager 的写入路径完成。
TEST_CONFIG_OVERRIDES: list[tuple[str, str, object]] = [
    ("config", "enable_petal", True),
    # 通用测试进程不启动守护进程所管理的 WebSocket Hub。数据库后端
    # 作为自包含测试环境。WebSocket 的真实连接行为由专项用例显式建立 Hub 验证。
    ("jobqueue", "jobqueue_backend", "database"),
]


def _write_minimal_config(path: Path, locale: str, version: int) -> None:
    # 注释先以 i18n 标记写入磁盘，待 i18n 快照就绪后由配置模板扫描统一翻译。版本号读取当前值，因为
    # core/builtins/config/update.py 的迁移在导入阶段执行，低于目标版本会被逐级升级。
    # 该函数必须在 ``AKARI_CONFIG_PATH`` 设置之后调用，其内的 core.constants 导入会固定配置目录。
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


@dataclass(frozen=True)
class TestEnvironment:
    """本次测试运行实际使用的输出文件路径。"""

    config_path: Path
    union_merge_logs_path: Path
    i18n_cache_path: Path


_environment: TestEnvironment | None = None
_created_paths: list[Path] = []


def _install_test_union_merge_logs() -> Path:
    # 日志写入仍会被完整执行，产物随进程退出一并删除。需要留存时设置 ``AKARI_UNION_MERGE_LOGS_PATH``。
    # 已显式设置过的运行器（如 tests/run_one.py）直接沿用，不再新建目录。
    configured = os.environ.get(TEST_UNION_MERGE_LOGS_PATH_ENV)
    if configured:
        return Path(configured)

    path = Path(tempfile.mkdtemp(prefix="akari_test_union_merge_logs_"))
    os.environ[TEST_UNION_MERGE_LOGS_PATH_ENV] = str(path)
    _created_paths.append(path)
    return path


def _install_test_i18n_cache() -> Path:
    # 快照缓存的取值仅依赖环境变量，因此必须先于配置引导，因为后者构建语言快照时会读取它。
    configured = os.environ.get(TEST_I18N_CACHE_DIR_ENV)
    if configured:
        return Path(configured)

    path = Path(tempfile.mkdtemp(prefix="akari_test_i18n_cache_"))
    os.environ[TEST_I18N_CACHE_DIR_ENV] = str(path)
    _created_paths.append(path)
    return path


def _install_test_config() -> Path:
    # 准备好一份测试专用配置，并令其后的导入均指向该配置。
    # 配置不读取自仓库内的配置快照，仅写入最小结构，其余键由配置模板扫描补全，
    # 因此仓库中不存在需要与代码同步维护的生成配置。
    path = Path(tempfile.mkdtemp(prefix="akari_test_config_"))

    # 顺序约束上，AKARI_CONFIG_PATH 与 AKARI_UNION_MERGE_LOGS_PATH 均必须先于任何 core.* 导入生效。
    # 二者分别固定为配置目录与合并日志目录。未设置时均会指向真实的 config/ 与 data/。
    os.environ[TEST_CONFIG_PATH_ENV] = str(path)

    from akaribot.core.constants import default_locale
    from akaribot.core.constants.version import config_version

    _write_minimal_config(path, default_locale, config_version)

    from akaribot.core.config import CFGManager
    from akaribot.core.config.scan import scan_config_templates
    from akaribot.core.constants import lang_list
    from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot

    # i18n 快照必须先完成加载关联，因为模板生成的注释读取自配置文件声明的语言，未完成加载关联时全部退化为 i18n 键名称。
    build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")

    failed_templates = scan_config_templates()
    if failed_templates:
        logger.warning(f"Failed to generate test config from templates: {failed_templates}")

    # 覆盖项通过配置管理器的写入路径处理，使磁盘与内存副本保持一致。直接改写文件时，
    # 同一文件系统时间戳精度内的改动可能绕过 watch() 的重载判定。
    for table, key, value in TEST_CONFIG_OVERRIDES:
        CFGManager.write(key, value, table_name=table)

    _created_paths.append(path)
    return path


def cleanup_test_environment() -> None:
    """删除本次运行创建的临时目录。由环境变量显式指定的目录保留。"""
    while _created_paths:
        shutil.rmtree(_created_paths.pop(), ignore_errors=True)


def prepare_test_environment() -> TestEnvironment:
    """返回本次测试运行的输出文件路径。环境初始化已在该模块导入阶段完成，重复调用返回同一份路径。"""
    global _environment
    if _environment is None:
        _environment = TestEnvironment(
            config_path=test_config_path,
            union_merge_logs_path=test_union_merge_logs_path,
            i18n_cache_path=test_i18n_cache_path,
        )
    return _environment


# 三项引导均必须早于该模块后续的 core.* 导入。合并日志目录与语言快照缓存在前，因为它们的取值仅依赖
# 环境变量，而配置引导内部会导入 core.constants 并构建语言快照，届时未设置的变量即被永久固定。
test_union_merge_logs_path = _install_test_union_merge_logs()
test_i18n_cache_path = _install_test_i18n_cache()
test_config_path = _install_test_config()
atexit.register(cleanup_test_environment)

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
from akaribot.testing.logger import TEST_LOGGER
from akaribot.testing.junit import JUnitReport, JUnitTestSuite, JUnitTestCase
from akaribot.testing.mock.database import close_db, get_last_init_error, init_db
from akaribot.testing.mock.loader import load_modules
from akaribot.testing.mock.random import Random
from akaribot.testing.process import run_case_entry, run_function_entry

Logger = TEST_LOGGER

# 源码克隆形态下的仓库根目录由根目录兼容实现 tester.py 在导入该模块前设置，取值必须与其一致。
REPO_ROOT_ENV = "AKARI_REPO_ROOT"


@dataclass(frozen=True)
class RunOptions:
    """本次运行的选择项。

    :param paths: 仅运行这些测试文件或目录。空元组表示按默认根收集。
    :param cases: 仅运行名字里含这些子串的 ``func_case``。空元组表示全部。
    :param ci: 是否按 CI 模式运行（无 Expectation 的用例跳过而不是等待人工输入）。
    :param coverage: 是否启用覆盖率收集。
    """

    paths: tuple[str, ...] = ()
    cases: tuple[str, ...] = ()
    ci: bool = False
    coverage: bool = False


def parse_options(argv: Sequence[str] | None = None) -> RunOptions:
    """解析命令行选项。

    ``--ci`` 与 ``--coverage`` 必须在这里识别：``IS_CI`` / ``ENABLE_COVERAGE`` 在**导入期**
    读取环境变量，等 ``main()`` 再解析已经太晚——这正是“选项拼进了 argv 却完全不生效”的原因。

    :param argv: 参数列表。默认取 ``sys.argv[1:]``。
    :return: 解析结果。
    :raises SystemExit: ``--help`` 或参数不合法。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.testing",
        description="运行 AkariBot 自研测试框架的全部或部分用例。",
    )
    parser.add_argument("paths", nargs="*", help="只跑这些测试文件或目录，默认跑全部根目录")
    parser.add_argument("--case", action="append", default=[], metavar="NAME", help="只跑名字含该子串的用例，可重复")
    parser.add_argument("--ci", action="store_true", help="按 CI 模式运行，跳过需要人工复核的用例")
    parser.add_argument("--coverage", action="store_true", help="启用覆盖率收集")
    args = parser.parse_args(argv)
    return RunOptions(
        paths=tuple(args.paths),
        cases=tuple(args.case),
        ci=bool(args.ci),
        coverage=bool(args.coverage),
    )


def _prescan_mode_flags(argv: Sequence[str]) -> tuple[bool, bool]:
    # 完整解析留至 :func:`run`，因为该模块也会被 ``tester.py`` 等入口以各自的 argv 导入，在导入阶段执行
    # 严格解析会导致那些入口因无关参数直接退出。此处仅执行包含判断，未识别的参数均直接忽略。
    return "--ci" in argv, "--coverage" in argv


# 本次运行的选择项。由 run() 严格解析后覆盖。main() 中的收集与筛选均在其之后读取它。
OPTIONS = RunOptions()

_MODE_CI, _MODE_COVERAGE = _prescan_mode_flags(sys.argv[1:])


def _resolve_repo_root() -> Path | None:
    # 不按该文件位置反推，因为该模块已在包内，反推仅会指向 site-packages。优先使用 ``AKARI_REPO_ROOT``。
    # 否则使用 ``Paths.tests`` 的父目录——源码克隆下 ``tests/`` 位于仓库根目录，再以 ``packages/``
    # 是否存在复核，避免 ``AKARI_TESTS_PATH`` 指向别处时误判。
    explicit = os.environ.get(REPO_ROOT_ENV)
    if explicit:
        return Path(explicit).expanduser().resolve()
    candidate = Path(tests_path).parent
    return candidate if (candidate / "packages").is_dir() else None


REPO_ROOT = _resolve_repo_root()

# 报告输出位置与用例发现同源，源码克隆下固定在仓库根目录，安装形态下改用调用目录。
OUTPUT_ROOT = REPO_ROOT if REPO_ROOT is not None else Path.cwd()


def _source_import_roots() -> list[Path]:
    # 各包源码存放在 ``packages[/<类>]/<包名称>``（源码根目录即包根目录），仓库根目录本身不提供可直接导入的 ``akaribot``。
    # 判断依据仅检查目录是否存在，不依赖已安装包的元数据。仓库根目录不可知时返回空列表，此时
    # ``akaribot`` 由已安装包提供，无需改写 ``PYTHONPATH``。
    if REPO_ROOT is None:
        return []
    candidates = [
        REPO_ROOT,
        # 源码根目录即包根目录或包根目录下的 src 两种布局均支持。
        *sorted(path for path in REPO_ROOT.glob("packages/*") if (path / "akaribot").is_dir()),
        *sorted(path for path in REPO_ROOT.glob("packages/*/*") if (path / "akaribot").is_dir()),
        *sorted(path / "src" for path in REPO_ROOT.glob("packages/*") if (path / "src" / "akaribot").is_dir()),
        *sorted(path / "src" for path in REPO_ROOT.glob("packages/*/*") if (path / "src" / "akaribot").is_dir()),
    ]
    return [path for path in candidates if path.is_dir()]


load_dotenv()
os.environ.setdefault("PYTHONIOENCODING", "UTF-8")
# 空列表时不设置，因为空字符串会引入一条指向当前目录的搜索路径，与安装形态的预期相反。
if source_import_roots := _source_import_roots():
    os.environ.setdefault("PYTHONPATH", os.pathsep.join(str(path) for path in source_import_roots))

IS_CI = os.environ.get("CI", "0") == "1" or _MODE_CI
ENABLE_COVERAGE = os.environ.get("COVERAGE", "0") == "1" or _MODE_COVERAGE
MAX_CONCURRENT = 1

# Coverage 集成。
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

# 本机仅运行部分集成测试时，使用路径子串筛选。
TEST_FILTER_ENV = "AKARI_TEST_FILTER"
INTEGRATION_TESTS_PATH = Path(tests_path) / "integration"


@dataclass
class RegistryTestStats:
    total: int = 0
    passed: int = 0
    failed: int = 0
    time_cost: float = 0.0


async def _run_registry_entry(entry: CaseEntry, test_number: int) -> dict:
    Logger.trace(f"_run_registry_entry START: TEST{test_number}")
    fn = entry["func"]
    note = entry.get("note") or (fn.__doc__ if fn.__doc__ else None)
    results = await run_case_entry(entry, IS_CI)
    Logger.trace(f"_run_registry_entry DONE: TEST{test_number}")
    return {"test_number": test_number, "results": results, "note": note}


async def _report_registry_case(
    entry: CaseEntry, reg_result: dict | Exception, test_number: int, stats: RegistryTestStats
) -> None:
    fn = entry["func"]
    file_loc = f"{entry.get('file')}:{entry.get('line')}"

    Logger.info(f"TEST{test_number}: {fn.__name__} ({file_loc})")
    if fn.__doc__:
        Logger.info(f"DOC: {fn.__doc__}")
    Logger.info("-" * 60)

    if isinstance(reg_result, Exception):
        Logger.error(f"Error during test execution: {reg_result}")
        stats.failed += 1
        stats.total += 1
        junit_testcase = JUnitTestCase(name=f"TEST{test_number}_runner", classname=f"RegistryTest.{test_number}")
        junit_testcase.error = ("Test runner error", repr(reg_result))
        junit_registry_suite.add_testcase(junit_testcase)
        return
    if not isinstance(reg_result, dict):
        stats.failed += 1
        stats.total += 1
        junit_testcase = JUnitTestCase(
            name=f"TEST{test_number}_invalid_result", classname=f"RegistryTest.{test_number}"
        )
        junit_testcase.error = ("Invalid test result", repr(reg_result))
        junit_registry_suite.add_testcase(junit_testcase)
        return

    note = reg_result.get("note")
    results = reg_result.get("results", [])
    for r in results:
        stats.total += 1
        inp = r.get("input")
        tcost = r.get("time_cost", 0.0)
        test_case_name = f"TEST{test_number}_{stats.total}"
        junit_testcase = JUnitTestCase(
            name=test_case_name, classname=f"RegistryTest.{test_number}", time=tcost if tcost else 0.0
        )

        if "timeout" in r:
            Logger.error(f"INPUT: {inp}")
            if note:
                Logger.error(f"NOTE: {note}")
            Logger.error("RESULT: FAIL (timeout)")
            stats.failed += 1
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
            stats.failed += 1
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
            match = await expected.match(r)
            if match:
                Logger.success("RESULT: PASS")
                stats.passed += 1
            elif match is False:
                Logger.error("RESULT: FAIL")
                stats.failed += 1
                junit_testcase.failure = ("Assertion failed", f"Expected: {expected}\nActual: {fmted_output}")
                junit_registry_suite.add_testcase(junit_testcase)
                continue
        else:
            if IS_CI:
                Logger.info("RESULT: SKIP (expects manual review, unavailable in CI)")
                junit_testcase.skipped = "Manual review required (unavailable in CI)"
                junit_registry_suite.add_testcase(junit_testcase)
                continue
            try:
                Logger.warning("REVIEW: Did the output meet expectations? [y/N]")
                check = input()
                if check in confirm_command:
                    Logger.success("RESULT: PASS")
                    stats.passed += 1
                else:
                    Logger.error("RESULT: FAIL")
                    stats.failed += 1
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
            stats.time_cost += tcost

    Logger.info("-" * 60)


class FuncTestResult(TypedDict):
    """单个 @func_case 测试的运行结果。"""

    fn: FunctionType
    path: str
    res: dict


@dataclass
class FuncTestStats:
    total: int = 0
    passed: int = 0
    failed: int = 0
    time_cost: float = 0.0


def _test_roots() -> list[Path]:
    # 仓库根目录的 ``tests/`` 承载跨包用例与共享测试数据，各成员包自带的 ``tests/`` 随包分发。后者仅在
    # 源码克隆下可见，仓库根目录不可知时仅剩 ``Paths.tests``（可由 ``AKARI_TESTS_PATH`` 指定）。
    roots = [Path(tests_path)]
    if REPO_ROOT is not None:
        for pattern in ("packages/*/tests", "packages/*/*/tests"):
            roots.extend(root for root in sorted(REPO_ROOT.glob(pattern)) if root.is_dir())
    return [root for root in roots if root.is_dir()]


def _test_module_key(path: str) -> str:
    # 按相对仓库根目录的路径生成，因为不同包中可以存在同名测试文件，仅读取文件名称会互相覆盖。仓库根目录不可知时
    # 回退至原路径，模块名称的唯一性由绝对路径本身保证。
    relative = Path(path)
    if REPO_ROOT is not None:
        try:
            relative = Path(path).resolve().relative_to(REPO_ROOT)
        except ValueError:
            pass
    return "tests_" + "_".join(part.replace("-", "_") for part in relative.with_suffix("").parts)


def _explicit_test_files() -> list[str]:
    # 目录递归收集 ``*.py``，文件按原样收集。路径按仓库根目录解析，相对路径因此与 ``tests/run_one.py``
    # 的写法一致。传入错误路径时返回空列表，由调用方提示“没有匹配的测试文件”——静默运行全量会导致
    # ``akaribot test <路径>`` 看起来生效，实际并未执行任何筛选。
    files: list[str] = []
    for raw in OPTIONS.paths:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute() and REPO_ROOT is not None:
            candidate = REPO_ROOT / candidate
        if candidate.is_dir():
            files.extend(glob.glob(os.path.join(candidate, "**", "*.py"), recursive=True))
        elif candidate.is_file():
            files.append(str(candidate))
    return sorted({str(Path(path).resolve()) for path in files})


def _iter_integration_files() -> list[str]:
    pattern = str(INTEGRATION_TESTS_PATH / "**" / "*.py")
    files = [
        path for path in sorted(glob.glob(pattern, recursive=True)) if not os.path.basename(path).startswith(("_", "."))
    ]
    selector = os.environ.get(TEST_FILTER_ENV, "").strip().replace("\\", "/")
    if selector:
        files = [path for path in files if selector in path.replace("\\", "/")]
    return files


def _collect_test_files() -> list[str]:
    # 传入位置参数时仅运行这些路径。否则按默认根目录收集，仓库根目录的集成用例由 _iter_integration_files
    # 单独列出，其目录内的辅助模块不参与收集。两种情形均按路径排序且去重。
    if OPTIONS.paths:
        return _explicit_test_files()
    files: list[str] = list(_iter_integration_files())
    for root in _test_roots():
        files.extend(
            path
            for path in glob.glob(os.path.join(root, "**", "*.py"), recursive=True)
            if INTEGRATION_TESTS_PATH not in Path(path).parents
        )
    return sorted(set(files))


async def _run_func_test(fn: FunctionType, path: str) -> FuncTestResult:
    Logger.trace(f"_run_func_test START: {fn.__name__} ({path})")
    res = await run_function_entry(fn, IS_CI)
    Logger.trace(f"_run_func_test DONE: {fn.__name__}")
    return {"fn": fn, "path": path, "res": res}


def _report_func_test(func_result: FuncTestResult, test_number: int, stats: FuncTestStats) -> None:
    fn = func_result["fn"]
    path = func_result["path"]
    res = func_result.get("res", {})

    Logger.info(f"TEST{test_number}: {fn.__name__} ({path})")
    if fn.__doc__:
        Logger.info(f"DOC: {fn.__doc__}")

    Logger.info("-" * 60)

    if res.get("skipped"):
        junit_testcase = JUnitTestCase(
            name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
        )
        junit_testcase.skipped = "Test skipped"
        junit_func_suite.add_testcase(junit_testcase)
        stats.total += 1
        return
    if res.get("timeout"):
        stats.failed += 1
        stats.total += 1
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
        return
    if res.get("error"):
        stats.failed += 1
        stats.total += 1
        junit_testcase = JUnitTestCase(
            name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
        )
        junit_testcase.error = ("Test error", res.get("error", "Unknown error"))
        junit_func_suite.add_testcase(junit_testcase)
        return

    entries = res["entries"]
    if not entries:
        Logger.warning(f"No inputs registered in func test {fn.__name__}; skipping.")
        junit_testcase = JUnitTestCase(
            name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
        )
        junit_testcase.skipped = "No inputs registered"
        junit_func_suite.add_testcase(junit_testcase)
        stats.total += 1
        return

    results = res["results"]
    subtest_number = 0
    func_pass = True
    func_error_msgs: list[str] = []
    for r in results:
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

        if type_ == "integration":
            Logger.info(f"INPUT: {inp}")
        if note:
            Logger.info(f"NOTE: {note}")
        if type_ == "integration":
            Logger.info(f"OUTPUT:\n{fmted_output}")
        if expected is not None:
            Logger.info(f"EXPECT: {expected}")

        if r.get("match"):
            Logger.success("RESULT: PASS")
            continue
        if expected is None:
            if IS_CI:
                Logger.info("RESULT: SKIP (expects manual review, unavailable in CI)")
                continue
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
        stats.passed += 1
        junit_testcase = JUnitTestCase(
            name=fn.__name__, classname=f"FunctionTest.{test_number}", time=res.get("time_cost", 0.0)
        )
    else:
        Logger.error(f"FUNC ({fn.__name__}) RESULT: FAIL")
        stats.failed += 1
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
        stats.time_cost += tcost

    stats.total += 1
    Logger.info("-" * 60)


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

    total = 0
    passed = 0
    failed = 0
    total_test_cost = 0.0
    force_exit = False

    registry_stats = RegistryTestStats()
    for idx, entry in enumerate(registry, 1):
        try:
            reg_result = await _run_registry_entry(entry, idx)
        except Exception as e:
            Logger.trace(f"main() registry entry {idx} raised {e!r}")
            reg_result = e
        # 注册表用例逐条返回结果，每条仅代表自身阶段通过。
        await _report_registry_case(entry, reg_result, idx, registry_stats)
    total += registry_stats.total
    passed += registry_stats.passed
    failed += registry_stats.failed
    total_test_cost += registry_stats.time_cost

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
                if OPTIONS.cases and not any(needle in fn.__name__ for needle in OPTIONS.cases):
                    continue

                Logger.trace(f"main() found func_case: {fn.__name__} in {path}")
                func_tasks.append((fn, path))

        if OPTIONS.cases and not func_tasks:
            Logger.error(f"--case 没有匹配到任何入口：{'、'.join(OPTIONS.cases)}")
            failed += 1
            total += 1
            junit_testcase = JUnitTestCase(name="case_filter", classname="TestCollection")
            junit_testcase.error = ("No matching case", f"--case {list(OPTIONS.cases)} matched nothing")
            junit_func_suite.add_testcase(junit_testcase)

        Logger.trace(f"main() running {len(func_tasks)} func tests sequentially")
        func_stats = FuncTestStats()
        for idx, (fn, path) in enumerate(func_tasks, 1):
            Logger.trace(f"main() about to run func test: {fn.__name__}")
            try:
                func_result = await _run_func_test(fn, path)
            except Exception as e:
                Logger.error(f"main() EXCEPTION running func test {fn.__name__}: {e}")
                func_result = {"fn": fn, "path": path, "res": {"error": repr(e)}}
            # 单元测试用例逐条返回结果。
            _report_func_test(func_result, len(registry) + idx, func_stats)
            Logger.trace(f"main() finished func test: {fn.__name__}")
            if func_result["res"].get("cleanup_pending"):
                force_exit = True
                Logger.error(f"Stopping after {fn.__name__}: timed-out task did not finish cancellation cleanup.")
                break
        passed += func_stats.passed
        failed += func_stats.failed
        total += func_stats.total
        total_test_cost += func_stats.time_cost
        Logger.trace(f"main() all func tests completed, counted {func_stats.total} entries")
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
        Logger.warning("No tests registered. Use `akaribot.testing.func_case` to register integration tests.")

    if IS_CI:
        try:
            junit_report.add_testsuite(junit_registry_suite)
            if junit_func_suite.test_cases:
                junit_report.add_testsuite(junit_func_suite)

            junit_output_path = OUTPUT_ROOT / "junit.xml"
            junit_report.write_to_file(junit_output_path)
            Logger.success(f"JUnit XML report generated: {junit_output_path}")
        except Exception as e:
            Logger.error(f"Failed to generate JUnit XML report: {e}")

    if force_exit:
        Logger.error("Forcing tester shutdown because a timed-out task is still running.")
        cleanup_test_environment()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)

    # Coverage 报告生成。
    if _coverage_instance:
        try:
            _coverage_instance.stop()
            _coverage_instance.save()

            # 生成控制台报告。
            Logger.info("=" * 60)
            Logger.info("Coverage Report:")
            _coverage_instance.report(show_missing=True)

            # 生成 HTML 报告。
            html_dir = OUTPUT_ROOT / "htmlcov"
            _coverage_instance.html_report(directory=str(html_dir))
            Logger.success(f"HTML coverage report generated: {html_dir}/index.html")

            # 生成 XML 报告（可选，用于 CI 集成）。
            if IS_CI:
                coverage_xml = OUTPUT_ROOT / "coverage.xml"
                _coverage_instance.xml_report(outfile=str(coverage_xml))
                Logger.success(f"XML coverage report generated: {coverage_xml}")
        except Exception as e:
            Logger.error(f"Failed to generate coverage report: {e}")

    Logger.trace("main() close_db")
    await close_db()

    Logger.trace("main() END")
    return 1 if IS_CI and (failed > 0 or total == 0) else 0


def run() -> int:
    """同步入口，解析参数、运行选中的用例并返回进程退出码。"""
    global OPTIONS
    OPTIONS = parse_options()
    if OPTIONS.paths and not _explicit_test_files():
        Logger.error(f"位置参数没有匹配到任何测试文件：{'、'.join(OPTIONS.paths)}")
        return 1
    return asyncio.run(main())
