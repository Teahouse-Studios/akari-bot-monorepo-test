# 测试框架

`akaribot.testing` 是 AkariBot 的测试框架，提供自研运行器与 pytest 插件两个前端。两者共用用例写法、匹配器、环境隔离与 mock 组件，区别在于收集方式与报告输出。

| 前端 | 入口 | 适用场景 |
| --- | --- | --- |
| 自研运行器 | `python -m akaribot.testing`、根目录 `tester.py` | 集成用例与包内用例 |
| pytest 插件 | `pytest tests/unit` | 单元测试 |

根目录 `conftest.py` 在导入阶段初始化测试环境，并注册 pytest 插件。

## 运行入口

在源码克隆中运行全量测试：

```sh
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing
```

根目录 `tester.py` 是兼容实现，转发至同一运行器，参数与行为一致。

单元测试由 pytest 执行：

```sh
CI=1 .venv/bin/python -m pytest tests/unit
```

包安装至实例后，也可以使用 CLI：

```sh
akaribot test --ci
akaribot test packages/akari-bot-core/tests/test_registry.py --ci
```

`akaribot test` 先确认实例环境中能导入 `akaribot.testing`，缺少该包时提示安装 `akari-bot-testing`。无法识别的参数原样传递给运行器。

## 运行器选项

- `paths`：仅运行这些测试文件或目录。相对路径按仓库根目录解析，目录递归收集 `*.py`。省略时按默认根目录收集。
- `--case <子串>`：仅运行名称包含该子串的 `@func_case`，可多次指定。没有任何匹配时记录一条失败。
- `--ci`：CI 模式，跳过需要人工复核的用例。
- `--coverage`：收集覆盖率。

运行器在导入阶段识别 `--ci` 与 `--coverage`。环境变量 `CI=1` 与 `COVERAGE=1` 具有相同效果。

## 收集范围

运行器默认收集仓库根目录的 `tests/` 下全部测试文件（包括 `tests/unit/`），源码克隆下还会收集 `packages/*/tests` 与 `packages/*/*/tests`。`tests/integration/` 中跳过文件名以 `_` 或 `.` 开头的辅助模块，其余目录整份收集。设置 `AKARI_TEST_FILTER` 后，仅保留路径包含该子串的集成用例。

测试文件放在 `tests/unit/`（纯函数）、`tests/integration/`（完整命令流程）与 `packages/*/tests/`（包内自测）。跨包共享的 HTTP 测试数据放在 `tests/fixtures/http/`。

## CI 模式

自动化运行必须设置 `CI=1` 或指定 `--ci`。未指定 `expected` 的用例与交互输入耗尽的用例，在非 CI 模式下会调用 `input()`，在非交互终端中挂起。

CI 模式跳过人工复核，交互输入不足直接判定失败。`CI=1` 时测试时限系数默认为 10，可用 `AKARI_TEST_TIME_SCALE` 覆盖。完整运行在输出根目录生成 `junit.xml`，源码克隆下即仓库根目录。

CI 模式下存在失败用例或未收集到用例时退出码非 0。

## 覆盖率

启用覆盖率后输出控制台报告与 `htmlcov/index.html`。CI 模式下另生成 `coverage.xml`。运行环境需要安装 `coverage`。

## 准备阶段耗时

设置 `AKARI_TEST_SETUP_TIMING=1` 后，每个入口在准备完成时打印一行 `[SETUP]` 日志，分别记录关闭数据库、初始化数据库与加载模块的耗时。初始化数据库另拆分为模型模块查找、模型模块导入、建立连接与建表四段，依次对应 `db_fetch`、`db_import`、`db_init` 与 `db_schema`。字段 `db_models` 记录模型模块数。

同一行还记录 `cpu`（自上一个入口以来累计的进程 CPU 时间）、`threads`、`tasks` 与 `top_threads`，用于判断准备阶段是否被后台负载拖慢。

## pytest 前端

pytest 插件把每个 `@func_case` 收集为独立用例，并把 `Tester` 替换为 `PytestTester`。入口内的子测试失败直接判定为该 pytest 用例失败，不汇总为运行器结果。

- 全部用例在同一个会话事件循环中执行，与生产环境中数据库连接、HTTP 客户端与队列节点的绑定方式一致。
- 单个用例的超时时间可用 `@pytest.mark.akari_timeout` 标记或 `AKARI_TEST_TIMEOUT` 指定，默认值为 120 秒乘以时限系数，计算时系数最多取 5。
- `tester` fixture 提供 `PytestTester`，供 pytest 风格用例使用。

## 单入口运行

开发阶段仅运行单个文件或单个入口。示例：

```sh
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py tests/unit/test_message.py test_message_plain
```

第二个参数为入口函数名称，省略时运行该文件中全部以 `test_` 开头的入口函数。脚本强制 CI 模式，收尾使用 `os._exit` 退出，避免框架遗留的后台任务阻塞进程。该脚本不生成 JUnit 报告，不适合需要 `expected=None` 人工复核的用例。

## 环境隔离

运行器在导入阶段建立隔离环境，这一步必须先于任何 `akaribot.core` 导入：

- 配置来自临时目录，环境变量 `AKARI_CONFIG_PATH` 指向它。运行器写入最小配置后扫描配置模板补全其余项。随后叠加测试覆盖项，其中 `config.enable_petal` 为 `True`，`jobqueue.jobqueue_backend` 为 `database`。测试结束后删除该目录。
- union 合并日志写入临时目录（`AKARI_UNION_MERGE_LOGS_PATH`），测试结束后删除。明确设置的值优先。
- 语言快照缓存写入临时目录（`AKARI_BOT_I18N_CACHE_DIR`），测试结束后删除。明确设置的值优先。
- 数据库使用内存 SQLite，每个用例入口前重建。
- HTTP 与 WebRender 的录制数据从 `tests/fixtures/` 回放，未录制的请求不访问真实网络。设置 `AKARI_TEST_ALLOW_LIVE_HTTP=1` 时放行未录制的请求。

需要留存合并日志时，将 `AKARI_UNION_MERGE_LOGS_PATH` 指向待保存的目录即可。

## 编写用例

用例写法、匹配器、Fixture 与常见陷阱参见[编写用例](writing-tests.md)。
