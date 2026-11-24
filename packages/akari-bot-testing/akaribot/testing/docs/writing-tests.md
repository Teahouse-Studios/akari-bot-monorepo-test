# 编写用例

## 文件位置

| 目录 | 内容 |
| --- | --- |
| `tests/unit/` | 纯函数与类型测试 |
| `tests/integration/` | 覆盖完整命令链路的集成测试 |
| `tests/fixtures/http/` | 录制的 HTTP 响应 |
| `tests/helpers/` | RPC worker 等辅助进程 |
| `packages/*/tests/` | 包自带的测试 |

文件名称以 `test_` 开头。不同包可以存在同名文件，运行器按仓库相对路径生成模块名称。

## `@func_case`

由 `@func_case` 标记的 async 函数为一个测试用例，其参数为 `Tester`。用例通常在末尾返回 `return tester`，框架也会从传入对象中收集测试结果。

示例：

```python
from akaribot.testing import Contains, Tester, func_case


@func_case
async def test_version(tester: Tester):
    await tester.integrate("~version", Contains("版本"), "version 应输出版本信息")
    return tester
```

`Tester` 仅提供两个检查方法：

- `await tester.integrate(input_, expected=None, note=None, timeout=None)`：发送一条命令并校验输出。`input_` 为字符串列表时表示连续多条消息，用于交互式命令。
- `await tester.test(func, note=None)`：调用纯函数或谓词，返回 True 即通过，支持同步与异步。框架不提供 `tester.expect()`。

`expected` 参数传入 `Expectation` 实例。传入 `None` 表示人工复核，仅可在交互式全量运行中使用。

## `@case`

`@case` 将用例挂载在命令定义旁，模块被导入时注册。

示例：

```python
from akaribot.testing import Match, case


@case("~test say Hello", Match("Hello is Hello"))
@test.command("say <word>")
async def _(msg: Bot.MessageSession, word: str):
    await msg.finish(f"{word} is {msg.parsed_msg['<word>']}")
```

说明：

- 第一个参数为输入内容，第二个参数为期望值，此外可指定 `note` 与 `timeout`。
- `@case` 用例的并发上限为 1。

## 匹配器

全部匹配器继承 `Expectation`，可用 `&`、`|`、`~` 组合，也可直接用 `All`、`Any`、`Not`。

| 匹配器 | 判定 |
| --- | --- |
| `Match(text)` | 渲染后的文本精确相等，默认不区分大小写 |
| `Equal(message)` | 可发送消息链完全相等 |
| `Contains` / `ContainsAll` / `ContainsAny` | 包含一个 / 全部 / 任一字符串 |
| `StartsWith` / `EndsWith` / `Regex` | 前缀、后缀、正则 |
| `InOrder` / `StructureEqual` | 元素按给定类型的顺序出现 / 数量、顺序与类型严格一致 |
| `Length` / `Count` / `OutputCount` | 元素总数 / 某类型数量 / 平台动作条目数 |
| `Exist` | 存在指定类型的元素 |
| `Empty` / `AnyOutput` | 无输出 / 有输出 |
| `Raise` / `NoException` | 期望异常 / 期望不抛出异常 |
| `ActionContains` | 平台动作包含指定内容 |
| `Predicate(func)` | 自定义判定函数 |

`Contains` 同时检查纯文本与带媒体描述的完整文本。`ActionContains` 用于撤回、禁止发言等平台动作。

## 测试环境

集成测试使用 `akaribot/testing/mock/parser.py` 的简化解析器，与生产解析器存在三点差异：

1. 不按平台过滤模块。
2. 命令分发不检查模块是否处于启用状态，无需先 `~module enable`。
3. 发送者被设为 superuser，多数权限检查直接通过。

因此测试通过并不代表命令在真实平台上可达。涉及平台过滤、模块开关与权限判定的修改需要另行验证。

其余模拟组件：

- `mock/database.py`：内存 SQLite，运行用例前重新构建。
- `mock/loader.py`：加载全部已发现模块，可注入 monkey patch。
- `mock/random.py`：固定种子，随机输出可复现。
- `mock/http.py` 与 `mock/fixtures.py`：按 URL、方法、请求体摘要回放 HTTP 响应。
- `mock/session.py`：记录 `sent`、`action` 与按钮数据。

需要替换 `Config` 等全局对象时，请使用 `unittest.mock.patch`。

## Fixture

load_modules() 会自动加载 tests/fixtures/http/ 目录下的全部 JSON 文件。新增网络模块用例时，请先使用 tests/capture_http_fixtures.py 录制真实响应，再在测试中离线回放；手工构造测试数据时可以使用 save_fixture()。

文件名称为 URL、方法与请求体摘要的哈希，同一 URL 上不同请求体各自独立成文件。

## 常见陷阱

- 自动化运行必须设置 `CI=1`。否则人工复核与交互输入会挂起。
- `tests/run_one.py` 强制 CI 模式，不适用于需要人工复核的用例。结束时调用的 `os._exit` 会跳过常规清理。
- 仅检查对外行为，不要检查私有属性、调用次数、日志条数或提示文案的完整措辞。
- 比较结构化返回值时优先声明必需字段，避免因新增字段导致既有用例失败。
- 集成用例会启动队列轮询与后台任务。用例结束前确保会话正常关闭，避免残留未完成的后台任务。
- Windows 下运行中文测试时设置 `PYTHONIOENCODING=UTF-8`。
- 不要在本地运行全量用例。全量由 CI 承担，本地仅运行改动相关的文件或入口。
