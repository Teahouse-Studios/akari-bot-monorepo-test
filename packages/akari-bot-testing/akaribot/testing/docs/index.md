# 测试框架

本文将会介绍此框架的运行入口、测试范围与环境隔离。

`akaribot.testing` 是 AkariBot 的自研测试框架与运行器。用例直接调用真实模块与简化的消息解析器，不使用 pytest 的用例收集与 fixture 机制。根目录的 `conftest.py` 只是兼容适配层，行为差异以本框架为准。

## 运行入口

在源码仓库内：

```sh
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing
```

根目录的 `tester.py` 是兼容层，转发到同一个运行器，参数与行为一致。包安装到实例后，也可以用 CLI：

```sh
akaribot test --ci
akaribot test packages/akari-bot-core/tests/test_registry.py --ci
```

`akaribot test` 先确认实例环境里能导入 `akaribot.testing`，缺包时提示安装 `akari-bot-testing`。无法识别的参数原样交给运行器。

## 测试范围

运行器默认收集仓库根的 `tests/`，在源码仓库中还会收集 `packages/*/tests` 与 `packages/*/*/tests`。给出位置参数时只跑这些文件或目录，相对路径按仓库根解析。

- `--case <子串>`：只跑名字含该子串的 `@func_case`，可重复。
- `--ci`：CI 模式，跳过需要人工复核的用例。非 CI 模式下，缺少期望值的用例可能等待输入。
- `--coverage`：收集覆盖率，入口脚本需要安装 `coverage`。

测试文件放在 `tests/unit/`（纯函数）、`tests/integration/`（完整命令链路）与 `packages/*/tests/`（包内自测）。跨包共享的 HTTP 测试数据放在 `tests/fixtures/http/`。

## CI 模式

自动化运行必须设置 `CI=1` 或传 `--ci`。没有 `expected` 的用例，以及交互输入耗尽的用例，在非 CI 模式下会调用 `input()`，在非交互终端里挂起。

CI 模式跳过人工复核，交互输入不足直接判失败。`--ci` 还会把 CI 开关写入环境变量，因为运行器在导入期就读取它。

CI 模式另设 `AKARI_TEST_TIME_SCALE=10` 放宽超时。完整运行会生成 `junit.xml`。覆盖率开启时另生成 `htmlcov/index.html` 与 `coverage.xml`。

## 单入口运行

开发期只跑一个文件或一个入口。示例：

```sh
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py tests/unit/test_message.py test_message_plain
```

第二个参数是入口函数名，省略时运行该文件中所有以 `test_` 开头的入口函数。脚本强制 CI 模式，收尾用 `os._exit` 退出，避免框架遗留的后台任务挂住进程。

因此，它不适合需要 `expected=None` 人工复核的用例。`tester.py` 与模块入口没有路径或用例筛选参数。

## 环境隔离

运行器在导入期建立隔离环境，这一步必须先于任何 `akaribot.core` 导入：

- 配置来自临时目录，环境变量 `AKARI_CONFIG_PATH` 指向它，测试结束后删除。
- union 合并日志写入临时目录（`AKARI_UNION_MERGE_LOGS_PATH`），测试结束后删除。显式设置的值优先。
- 数据库使用内存 SQLite，每个用例入口前重建。
- HTTP 响应从 `tests/fixtures/http/` 回放，网络模块不访问真实服务。

需要留存合并日志时，把 `AKARI_UNION_MERGE_LOGS_PATH` 指向要保存的目录即可。

## 编写用例

用例写法、匹配器、fixture 与常见陷阱见 [编写用例](writing-tests.md)。
