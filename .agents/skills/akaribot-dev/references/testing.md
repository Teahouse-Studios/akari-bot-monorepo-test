# 测试指南

## 目录

- [测试框架](#91-测试框架)
- [断言类型](#92-断言类型)
- [测试环境的真实行为](#93-测试环境的真实行为)
- [测试规范](#94-测试规范)
- [运行测试](#95-运行测试)

本文件只说明测试框架和运行方式。修改测试时，还要读取被测功能所属的 reference；不要从测试 mock 反推生产 API。

---

## 9. 测试指南

### 9.1 测试框架

AkariBot 使用自研测试框架（**非 pytest**），实现在 `packages/akari-bot-testing/` 的 `akaribot.testing` 包内：

| 文件 | 职责 |
| --- | --- |
| `runner.py` | 收集与执行、JUnit 报告、CI 判定 |
| `tester.py` | `Tester`，两种用例注册接口 |
| `decorator.py` | `@func_case` 与 `@case` |
| `expectations.py` | 全部断言类型 |
| `mock/` | parser、database、loader、random、fixtures、scheduler、session、webrender 等替身 |
| `pytest_plugin.py` | pytest 前端，把同一批用例接入 pytest 收集器 |

入口有三个，都跑同一份实现：

```bash
.venv/bin/python -m akaribot.testing     # 模块入口，推荐
.venv/bin/python tester.py               # 根目录兼容层，既有 CI 仍在用
.venv/bin/akaribot test                  # CLI 子命令，在实例环境里运行
```

用例位置分两类：跨包用例在仓库根的 `tests/`（`tests/unit/` 纯函数、`tests/integration/` 完整命令链路、`tests/fixtures/` 录制的 HTTP 响应）；包自带用例随包归位，放在 `packages/<分发>/tests/`，例如 `packages/modules/akari-bot-module-wiki/tests/`。runner 同时收集这两类（`packages/*/tests`、`packages/*/*/tests`）。

有两种写法。

**写法一：`@func_case` + `Tester`**（主流写法）

一个被 `@func_case` 标记的 async 函数就是一个测试用例，接收 `tester: Tester`。现有用例通常在末尾 `return tester`；框架也会从传入的 tester 收集结果，因此省略返回仍可运行，但新用例保持该惯例更清晰：

```python
from akaribot.testing import Contains, Tester, func_case


@func_case
async def test_version(tester: Tester):
    """version 命令测试。"""
    await tester.integrate("~version", Contains("版本"), "version 应输出版本信息")
    return tester
```

`Tester` 只有两个下断言的方法：

```python
async def integrate(input_, expected=None, note=None, timeout=None)
# 集成测试：input_ 是命令字符串（或字符串列表 = 连续多条消息），
# expected 传 Expectation；为 None 时框架转为人工复核

async def test(func, note=None)
# 纯函数测试：func 返回真值即通过，支持同步/异步
```

注意：**没有 `tester.expect()`**。

**写法二：`@case` 装饰器**（把用例直接挂在命令定义上）

```python
from akaribot.testing import Match, case


@case("~test say Hello", Match("Hello is Hello"))
@test.command("say <word>")
async def _(msg: Bot.MessageSession, word: str):
    await msg.finish(f"{word} is {msg.parsed_msg['<word>']}")
```

### 9.2 断言类型

全部定义在 `akaribot.testing.expectations`，公共入口 `from akaribot.testing import ...`，均继承 `Expectation`：

| 断言 | 用途 |
| --- | --- |
| `Match(text)` | 渲染后的消息文本精确匹配 |
| `Equal(message)` | 可发送消息链完全相等 |
| `Contains(text)` | 包含匹配 |
| `ContainsAll(*texts)` | 全部包含 |
| `ContainsAny(*texts)` | 任一包含 |
| `StartsWith(text)` | 前缀匹配 |
| `EndsWith(text)` | 后缀匹配 |
| `Regex(pattern)` | 正则匹配 |
| `InOrder(*types)` | 指定消息元素类型按顺序出现 |
| `Length(...)` | 消息链元素总数校验 |
| `Count(type, ...)` | 指定消息元素类型数量校验 |
| `OutputCount(...)` | 平台 action 条目数量校验 |
| `Exist(type, func=None)` | 存在指定消息元素类型 |
| `StructureEqual(*types)` | 元素数量、顺序和类型严格一致 |
| `AnyOutput()` | 有输出即可 |
| `Empty()` | 无输出 |
| `Raise(exc)` | 期望抛出异常 |
| `NoException()` | 期望不抛异常 |
| `ActionContains(...)` | 校验产生的平台动作（撤回、禁言等） |
| `Predicate(func)` | 自定义函数 |
| `All(...)` | AND 组合 |
| `Any(...)` | OR 组合 |
| `Not(...)` | NOT 取反 |

`Any` 同时是框架的匹配器与 `typing.Any` 的名字：从包根导入时不要写 `from akaribot.testing import Any` 去取类型注解，辅助名一律以下划线开头，避免遮住匹配器。

### 9.3 测试环境的真实行为

**测试走的不是生产 `parser()`**，而是 `akaribot.testing.mock.parser` 里的简化版。两个关键差异：

1. 它用不带平台过滤参数的模块列表，且**不检查模块是否已启用**——集成测试里**不需要**先 `~module enable <模块>`，直接发命令就能命中。
2. `run_test_case()` 会把测试发送者建成 **superuser**，mock 权限检查也大多直接通过——许多权限受限的命令在测试里仍能跑通。

反过来说：**测试通过不代表该命令在真实平台上可达**。模块级、命令级和正则级的平台过滤行为并不一致，模块开关与真实平台权限也没有被完整覆盖；改动涉及 `available_for` / `exclude_from` / 启用状态 / 权限时要另行确认。

其他环境替身在 `akaribot.testing.mock` 下：`database`（内存库）、`loader`（模块加载）、`random`（固定随机种子）、`fixtures`（HTTP 响应回放）、`scheduler`、`session`、`webrender`。需要覆盖 Config 时用 `unittest.mock.patch`。

测试引导还会把会落盘的内容移出仓库：整份配置来自临时目录（`AKARI_CONFIG_PATH`），union 合并日志写进临时目录（`AKARI_UNION_MERGE_LOGS_PATH`）并在收尾时删除。用例会真实走到合并流程，不隔离的话每次测试运行都会在 `data/union_merge_logs/` 里留下大量合成的快照。需要留存这些日志时自行设置 `AKARI_UNION_MERGE_LOGS_PATH` 指向保留目录即可，已显式设置的值优先。

这两处隔离发生在 `akaribot.testing.runner` 的导入期，且必须早于任何 `akaribot.core` 导入；`akaribot/testing/__init__.py` 因此不静态导入 `runner` 与 `tester`，见 `AGENTS.md` 的陷阱一节。

`akaribot.testing.mock.loader` 直接消费发现层（`PackageRegistry.modules()`）的清单，与生产入口同源。新增模块包后要先用 `akaribot module add -e .` 装进当前环境，否则发现层看不到它，用例不会命中。

### 9.4 测试规范

- 避免使用 `AnyOutput()`，尽量用 `Contains()` 校验关键内容
- 发现疑似 Bug 时提醒用户检查，不自行修复
- 涉及网络的模块先用 `tests/capture_http_fixtures.py` 录 fixture，再让测试离线回放
- 模块自带用例放 `packages/modules/akari-bot-module-<名>/tests/`，文件名 `test_<名>.py`

### 9.5 运行测试

```bash
CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing
COVERAGE=1 CI=1 .venv/bin/python -m akaribot.testing     # 附带覆盖率报告（htmlcov/index.html）
```

**自动化运行必须设置 `CI=1`**：非 CI 模式下，没有 `expected` 的用例和等待交互输入耗尽的用例可能调用 `input()`，在非交互终端里直接卡死。CI 模式会跳过需要人工复核的项目，交互输入不足则失败而不是等待。完整测试还会生成 JUnit 报告 `junit.xml`。CI 里另有 `AKARI_TEST_TIME_SCALE=10`，放宽对耗时用例的判定。

`python -m akaribot.testing` **不解析命令行参数**：`runner.run()` 不接受参数，传入的 `--help`、路径、`--case` 都会被忽略并直接开始跑全量。`akaribot test` 的 `path` / `--case` 选项会把参数透传给同一入口，在 runner 支持筛选之前同样不生效；按单个入口验证请用 `tests/run_one.py`。

Git Bash 下如果输出是乱码，在命令前加 `PYTHONIOENCODING=UTF-8`；该变量须在解释器启动前设置，`runner.py` 里的 `os.environ.setdefault` 对本次进程的 stdout 编码已经来不及了。

**跑单个测试入口**：使用仓库内的 `tests/run_one.py`。第一个参数是**包内路径**的用例文件（相对仓库根），第二个参数是入口函数名；省略时运行该文件中所有以 `test_` 开头的入口。脚本会补项目根到 `sys.path`，强制 CI 模式，并在收尾时用 `os._exit` 强制退出，避免框架遗留的后台任务导致进程挂起。

```bash
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py packages/modules/akari-bot-module-wiki/tests/test_wiki_markdown.py
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py tests/unit/test_bot_state.py test_bot_state
```

`tests/run_one.py` 强制使用 CI 模式，不适合需要 `expected=None` 人工复核的用例。

**基线**：全量用例的失败集合须与 `tools/test_baseline.txt` 逐名一致（`tools/check_test_baseline.py` 对拍），
当前为空——全量 248 条全部通过。新增失败、失败消失或错误文本变化都会使对拍失败。

CI 工作流见 `.github/workflows/run-builtin-tester.yml`；其中的只读包目录一轮会先 `chmod -R a-w packages`，用于复现 wheel 安装与只读挂载下包目录不可写的约束。

---

