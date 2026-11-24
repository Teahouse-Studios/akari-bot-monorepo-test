"""pytest 的根级 conftest：铺设测试环境并注册 akari 的 pytest 插件。

测试基座要求 ``AKARI_CONFIG_PATH``、``AKARI_UNION_MERGE_LOGS_PATH`` 与语言快照缓存目录在任何
``akaribot.core.*`` 导入之前生效（见 akaribot/testing/runner.py 的引导函数）：``akaribot.core.constants``
导入期即由 akaribot.core.paths 固化配置目录与合并日志目录，``akaribot.core.config`` 导入期还会执行
配置版本迁移。引导也不能放进 pytest 插件模块，因为 ``-p``/entry-point 插件会先于 conftest 导入。

用例的收集与执行见 akaribot/testing/pytest_plugin.py，pytest 只是这套框架的第二个前端。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 导入 tester 即完成测试环境初始化，必须早于任何 akaribot.core.* 导入（说明参见本文件开头的 docstring）。
from tester import prepare_test_environment  # noqa: E402

prepare_test_environment()

import pytest  # noqa: E402

from akaribot.testing.pytest_plugin import PytestTester  # noqa: E402

pytest_plugins = ["akaribot.testing.pytest_plugin"]


@pytest.fixture
def tester():
    """纯 pytest 风格用例的运行器，子测试失败直接判定为用例失败。"""
    yield PytestTester("pytest")
