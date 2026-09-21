"""根目录兼容层：``bot`` 转发到 :mod:`akaribot.core.entrypoints.run`。

机器人入口已迁入 core 包，本文件只保留两个历史用法：

- ``import bot``：把 ``sys.modules["bot"]`` 换成 run 模块本身，旧模块的全部名字（含私有名）
  因此原样可见。不做逐个再导出：``packages/akari-bot-core/tests/test_jobqueue_daemon.py`` 与
  ``tests/unit/test_multi_instance.py`` 会给 ``daemon.server_stop_event`` 等模块级变量赋值后再调
  ``daemon.cleanup_processes()``，只有同一模块对象才能让这类赋值被函数读到。
- ``python bot.py``：转发到 run 模块的 ``main()``，实例锁与守护循环都在那里。

新代码请改用 ``python -m akaribot.core.entrypoints.run``。
"""

import sys

from akaribot.core.entrypoints import run as _run

# 兼容面：既有用例经 ``import bot as daemon`` 使用的名字在此集中核对，缺失时导入期即报错，
# 而不是等到用例里出现 AttributeError。
_COMPAT_NAMES = (
    "CONFIG_READONLY_ENV",
    "Logger",
    "AdapterInstance",
    "_is_daemon_log",
    "check_instance_conflicts",
    "cleanup_processes",
    "disabled_bots",
    "discover_adapter_instances",
    "go",
    "jobqueue_hub_go",
    "jobqueue_hub_stop_event",
    "main",
    "multiprocessing",
    "pre_init",
    "processes",
    "run_bot",
    "server_go",
    "server_stop_event",
    "terminate_process",
    "warn_if_database_jobqueue_uses_sqlite",
)

_missing_compat_names = [name for name in _COMPAT_NAMES if not hasattr(_run, name)]
if _missing_compat_names:
    raise ImportError(f"akaribot.core.entrypoints.run 缺少兼容名：{_missing_compat_names}")

if __name__ == "__main__":
    _run.main()
else:
    sys.modules[__name__] = _run
