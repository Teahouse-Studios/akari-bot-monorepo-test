"""pytest 适配层的根级 conftest。

自研框架的测试基座要求 ``AKARI_CONFIG_PATH`` 与 ``AKARI_UNION_MERGE_LOGS_PATH`` 在任何
``akaribot.core.*`` 导入之前生效——``akaribot.core.constants`` 导入期即由 akaribot.core.paths
固化配置目录与合并日志目录，``akaribot.core.config`` 导入期还会执行配置版本迁移（见
akaribot/testing/runner.py 的 ``_install_test_config``）。因此这里先导入 tester 完成配置铺设，
再让 pytest 收集测试模块；引导也不能放进 pytest 插件模块，因为 ``-p``/entry-point 插件会先于
conftest 导入。

用例的收集与执行见 akaribot/testing/pytest_plugin.py，pytest 只是这套框架的第二个前端。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 导入 tester 即完成测试配置铺设，必须早于任何 akaribot.core.* 导入（说明见本文件开头的 docstring）。
from tester import test_config_path  # noqa: E402,F401

import pytest  # noqa: E402

from akaribot.testing.mock.database import close_db, init_db  # noqa: E402
from akaribot.testing.mock.loader import load_modules  # noqa: E402
from akaribot.testing.mock.random import Random  # noqa: E402
from akaribot.testing.pytest_plugin import (  # noqa: E402
    PytestTester,
    close_session_loop,
    make_item,
    run_in_session_loop,
)


def pytest_pycollect_makeitem(collector, name, obj):
    return make_item(collector, name, obj)


def pytest_sessionfinish(session, exitstatus):
    close_session_loop()


@pytest.fixture
def tester():
    """纯 pytest 风格用例的运行器。"""
    run_in_session_loop(close_db())
    run_in_session_loop(init_db())
    run_in_session_loop(load_modules(show_logs=False, monkey_patches={"Random": Random()}))
    yield PytestTester("pytest")
    run_in_session_loop(close_db())
