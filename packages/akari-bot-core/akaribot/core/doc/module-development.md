# 模块开发

本文将会带你生成、安装并运行第一个模块，同时说明模块的包结构、命令、Hook、配置和运行期资源。阅读前，你需要了解 Python 异步编程，并熟悉本仓库的包管理方式。

## 准备工作

先打开一个终端，进入实例目录，执行：

```bash
akaribot tui
```

左侧是页面列表，右侧是当前页面。用 ↑/↓ 选中“开发”，按 Enter 打开。页脚会列出当前页可用的按键。

开发页列出当前实例与工作区的包。按 `n` 打开“新建包”对话框。

## 生成第一个模块

在“新建包”对话框中填写以下内容：

| 字段 | 本次填写 | 说明 |
| --- | --- | --- |
| 名称 | `greet` | 模块名，建议使用小写字母、数字和下划线，不能包含空格或斜杠 |
| 类型 | 模块 | 默认值。按钮可以在模块与适配器之间切换，本教程保持模块 |
| 目标目录 | `akari-modules` | 相对当前工作区根目录，未配置工作区时相对实例根目录。包会放在该目录下的 `akari-bot-module-greet/` |
| 生成配置 | 不勾选 | 先不生成配置模板 |
| 生成数据库 | 不勾选 | 先不生成数据库与迁移 |
| 生成测试 | 勾选 | 默认已勾选，保留一条集成测试 |

用 Tab 在名称、类型、目标目录和三个复选项之间移动。空格切换复选项状态。最后把焦点移到“生成包”，按 Enter。

按 Esc 或选择“关闭”会放弃本次填写，不会创建文件。

生成过程中的输出会显示在输出区。完成后状态栏提示生成成功，按 `o` 查看完整输出。新包会出现在开发页的包列表中。

生成的目录结构如下。其中 `akari-modules` 是上一步填写的目标目录。

```text
akari-modules/akari-bot-module-greet/
  .github/workflows/publish.yml
  README.md
  akaribot/modules/greet/__init__.py
  akaribot/modules/greet/locales/zh_cn.json
  akaribot/modules/greet/manifest.toml
  pyproject.toml
  tests/test_greet.py
```

生成配置和生成数据库两项没有勾选，所以没有 `config.py`、`database/` 等目录。需要时再添加。

### 生成的文件

| 文件 | 用途 |
| --- | --- |
| `pyproject.toml` | 分发包名、依赖与 `akaribot.modules` 入口 |
| `manifest.toml` | 包清单，声明语言目录与提供的模块名 |
| `akaribot/modules/greet/__init__.py` | 模块声明与命令实现 |
| `locales/zh_cn.json` | 帮助文本与回复文案 |
| `tests/test_greet.py` | 一条集成测试，核对命令回复 |
| `README.md` | 包的安装、命令与结构说明 |
| `.github/workflows/publish.yml` | 推送版本标签后上传到 PyPI 的工作流 |

### 先看生成的代码

打开 `akaribot/modules/greet/__init__.py`，会看到下面这段代码。

```python
"""greet 模块。"""

from akaribot.core.api import (
    Bot,
    I18NContext,
    module,
)

mod = module(
    "greet",
    desc="{I18N:greet.help.desc}",
    doc=True,
)


@mod.command()
async def _(msg: Bot.MessageSession):
    await msg.finish(I18NContext("greet.message.hello"))
```

`@mod.command()` 没有写模板，注册的是模块的默认命令。它的调用形式是 `~greet default`，不是 `~greet hello`。

`module()` 的 `desc` 指向模块说明。处理函数调用 `msg.finish()`，把 `I18NContext` 对应的文案发送到当前会话。

文案在 `locales/zh_cn.json`：

```json
{
    "greet.help": "执行 greet 的默认命令。",
    "greet.help.desc": "greet 模块。",
    "greet.message.hello": "Hello World!"
}
```

`greet.help.desc` 是模块说明，`greet.help` 是默认命令的帮助文本。回复文案目前还是 `Hello World!`，下一节修改它。

## 修改第一条回复

打开 `locales/zh_cn.json`，把 `greet.message.hello` 改成：

```json
"greet.message.hello": "你好，世界！"
```

如果生成时保留了测试，`tests/test_greet.py` 里的预期文案也要同步修改：

```python
@func_case
async def test_greet_default(tester: Tester):
    """default 命令返回预期文案。"""
    await tester.integrate(
        "~greet default",
        Contains("你好，世界！"),
        "greet 的 default 命令应返回预期文案",
    )
    return tester
```

测试里的预期文案和实际文案不一致时，测试会失败。改完文案后，把 `zh_cn.json` 和测试里的预期文案一起检查。

## 安装并启用

生成的文件还在目标目录里，TUI 不会自动把它装进实例。切到侧栏的“模块”页，先按 `c` 清除选择，再按 `i` 打开安装对话框。

在输入框里填入刚才生成的包目录，路径用输出区显示的完整路径。按“下一步”。TUI 识别到目录后，安装方式里会出现“可编辑安装本地目录”。选中它，安装就开始。

可编辑安装直接使用这份源码，改代码后不需要重新打包。安装完成后，模块页会刷新列表，`greet` 出现在列表里。

如果实例正在运行，新模块会直接加载，不需要重启。实例未运行时，模块会在下次启动时加载。

安装只是把模块放进实例。普通模块还需要在场景内启用。场景管理员在会话中执行：

```text
~module enable greet
```

基础模块始终开启，不需要这一步。`greet` 是普通模块，所以要先启用。修改代码后，重启实例，或者由超级用户在会话中执行：

```text
~module reload greet
```

## 对话示例

下面的对话假设模块已经安装，并且当前场景已启用 `greet`。

<ChatExample
  :log="[
    '用户：~module enable greet',
    '机器人：成功：开启模块“greet”。',
    '用户：~greet default',
    '机器人：你好，世界！',
  ]"
/>

`~module enable greet` 只需要执行一次。之后的 `~greet default` 会命中 `@mod.command()` 注册的默认命令，返回你在 `zh_cn.json` 中写的文案。

如果机器人没有响应，先检查三件事：

- 模块是否安装成功。回到“模块”页，看 `greet` 是否在列表里，状态是否为已安装。
- 当前场景是否启用模块。在会话中执行 `~module list`。
- 修改文案后是否重载。执行 `~module reload greet`，或重启实例。

## 继续开发

生成模板只提供最小可运行结构。别名、平台范围、权限、配置、数据库与 Hook 按需补充。

- 修改 `module()` 的参数，可以声明别名、支持平台和模块级权限。参数见下文“声明模块”。
- 想给默认命令换一个名字，把 `@mod.command()` 改成 `@mod.command("hello {{I18N:greet.help.hello}}")`，并同步修改 `greet.help.hello` 与测试中的 `~greet hello`。
- 修改 `@mod.command()` 的模板，可以增加位置参数、标志选项和帮助文本。规则见下文“命令”。
- 需要定时执行或监听消息时，使用 `@mod.schedule()`、`@mod.hook()` 或 `@mod.event()`。
- 需要保存配置或数据时，在 `config.py` 和 `database/models.py` 中声明，并同步修改 `manifest.toml`。

## 包结构与清单

```text
akari-bot-module-<name>/
  pyproject.toml
  akaribot/modules/<name>/
    __init__.py         module() 声明与组件
    config.py           @on_module_config 配置模板，可选
    database/models.py  数据模型，可选
    locales/zh_cn.json  文案与配置注释
    manifest.toml       包元数据
```

`pyproject.toml` 声明依赖和入口，`manifest.toml` 声明清单字段。

```toml
# pyproject.toml
dependencies = ["akari-bot-core>=0.1.0,<1.0"]

[project.entry-points."akaribot.modules"]
dice = "akaribot.modules.dice"

# manifest.toml
schema = 1
requires_core_api = ">=1,<2"
config_table = "module_dice"
provides_modules = ["dice"]
```

清单字段如下：

| 字段 | 说明 |
| --- | --- |
| `schema` | 清单结构版本，当前为 `1` |
| `requires_core_api` | 核心 API 兼容区间，默认 `>=1,<2` |
| `locales`、`assets` | 语言文件与资源目录，默认 `locales`，相对导入包目录解析 |
| `migrations`、`config_migrations` | 数据库迁移与配置迁移目录 |
| `config_table`、`config_schema_version` | 配置表名，新生成配置写入的结构版本，默认 `1` |
| `provides_modules` | 分发包提供的模块名 |
| `owned_tables` | 数据清理时归属本包的表 |
| `credential_fields` | 启动前用于多实例查重的登录信息字段 |

未识别的键只会给出告警，不影响加载。

## 发现与加载

`PackageRegistry` 读取已安装分发包声明的模块入口，`load_order()` 按依赖关系给出激活顺序。模块只依赖 `akaribot.core.api` 的公开接口，包之间不直接导入。分发包缺少模块声明时，框架才用目录扫描发现模块。

JobQueue 处理完现有任务、Scheduler 进入维护时段后，框架才会执行安装、卸载和重载。框架会替换原有注册项，但要等正在运行的任务退出后才生效。加载失败原因写入 `.cache_loader`。`ModulesManager.reload_module()` 返回 `(状态, 重载次数)`。命令 `~module reload` 失败时会给出提示。

## 声明模块

```python
from akaribot.core.api import Bot, I18NContext, module

dice = module("dice", alias=["rd", "roll"], desc="{I18N:dice.help.desc}", doc=True)
```

`module()` 的参数如下：

| 参数 | 说明 |
| --- | --- |
| `module_name` | 命令首词，同时作为模块标识 |
| `alias` | 别名，可传字符串、列表或 `{别名: 完整命令}` 映射 |
| `desc` / `doc` / `hidden` | 帮助简介、线上说明与隐藏开关 |
| `recommend_modules` / `base` / `load` | 推荐模块、强制开启与加载开关 |
| `rss` / `regex` / `event` | 声明所需平台能力，决定模块能否在该场景启用 |
| `required_admin` / `required_superuser` / `required_base_superuser` | 模块级权限 |
| `required_bot_permissions` | 开启前要求机器人具备的平台权限 |
| `suppress_invalid_prompt` / `available_for` / `exclude_from` | 提示开关与平台范围 |

## 命令

```python
@dice.command("<dices> [<dc>] {{I18N:dice.help}}")
async def _(msg: Bot.MessageSession, dices: str, dc: int | None = None):
    await msg.finish(I18NContext("dice.message.result", dices=dices))
```

模板元素分四类：

- `<name>` 是位置参数，对应同名函数参数。没有提供参数时，使用默认值或 `None`。
- `[flag]` 是标志选项。标注为 `bool` 的函数参数会直接得到布尔值。
- `[-b]`、`[--foo <bar>]` 是以连字符开头的选项。选项名中的下划线按连字符匹配。选项只有一个子参数时，直接把子参数的值传给同名函数参数。`[-p <page>]` 也可以直接使用子参数名 `page`。无法作为参数名的元素用 `Param` 标注。
- 模板末尾用双层花括号包裹的 `I18N:key` 是帮助文案，不参与解析。

`int`、`float`、`bool` 参数按类型标注转换。一个命令可以注册多个模板，命中任意一个即可。`priority` 越大，越先匹配。

解析结果写入 `parsed_msg`。位置参数以模板中的参数名为键。

以连字符开头的选项会以选项名作为键。`-l` 和 `--l` 按同一个选项处理，选项名中的下划线会映射为连字符。

函数中标注为 `Bot.MessageSession` 的参数由框架注入，其余参数按名称从 `parsed_msg` 读取。转换失败时抛出 `InvalidCommandFormatError`。

## 等待用户交互

命令执行到一半需要用户回答时，用 `MessageSession` 的等待方法。这些方法会暂停当前命令，收到消息后再继续。

| 方法 | 适合的场景 | 返回 |
| --- | --- | --- |
| `wait_confirm()` | 只需要用户回答是或否 | `bool` |
| `wait_next_message()` | 收集同一用户的下一条消息 | `MessageSession` |
| `wait_reply()` | 要求用户引用某条提示再回复 | `MessageSession` |
| `wait_anyone()` | 让场景内任意成员回答 | `MessageSession` |

这些方法默认等待 120 秒。等待期间默认释放执行锁，返回前重新获取。超时、用户取消或重新获取失败都会抛出 `WaitCancelException`。

下面的例子在 `greet` 模块上继续添加命令。文案键要写进 `locales/zh_cn.json`。

```python
from akaribot.core.api import Bot, I18NContext, WaitCancelException
```

### 等待确认

```python
@greet.command("reset")
async def _(msg: Bot.MessageSession):
    try:
        confirmed = await msg.wait_confirm(
            I18NContext("greet.message.reset.confirm"),
            timeout=60,
        )
    except WaitCancelException:
        await msg.finish(I18NContext("greet.message.timeout"))
        return
    if not confirmed:
        await msg.finish(I18NContext("greet.message.cancelled"))
        return
    await msg.finish(I18NContext("greet.message.reset.done"))
```

`wait_confirm()` 默认引用原消息，并在收到回答后删除机器人发出的提示。它只把确认词当作回答，用户发送其他内容时会继续等待。

删除数据、解绑账号这类不可逆操作，可以传 `confirm_token` 要求用户完整输入口令，避免用户只点一下按钮就通过确认。

### 收集下一条消息

```python
@greet.command("rename")
async def _(msg: Bot.MessageSession):
    try:
        reply = await msg.wait_next_message(
            I18NContext("greet.message.rename.prompt"),
            delete=True,
            timeout=60,
        )
    except WaitCancelException:
        await msg.finish(I18NContext("greet.message.timeout"))
        return
    name = reply.as_display(text_only=True).strip()
    if not name:
        await msg.finish(I18NContext("greet.message.rename.empty"))
        return
    await msg.finish(I18NContext("greet.message.rename.done", name=name))
```

`wait_next_message()` 只接受触发命令的用户发来的下一条消息。这条消息仍会走常规解析流程。如果用户发的是一条命令，那条命令也可能被执行。`delete=True` 会在等待结束后删除机器人发出的提示。

### 等待引用回复

```python
@greet.command("apply")
async def _(msg: Bot.MessageSession):
    try:
        reply = await msg.wait_reply(
            I18NContext("greet.message.apply.prompt"),
            timeout=120,
        )
    except WaitCancelException:
        await msg.finish(I18NContext("greet.message.timeout"))
        return
    note = reply.as_display(text_only=True).strip()
    await msg.finish(I18NContext("greet.message.apply.done", note=note))
```

`wait_reply()` 要求用户引用机器人发出的那条提示再回复。平台不支持引用时，它会改为等待下一条消息。传 `all_=True` 时改为等待场景内任意成员。

### 等待任何人回答

```python
@greet.command("quiz")
async def _(msg: Bot.MessageSession):
    try:
        reply = await msg.wait_anyone(
            I18NContext("greet.message.quiz.prompt"),
            timeout=30,
        )
    except WaitCancelException:
        await msg.finish(I18NContext("greet.message.quiz.timeout"))
        return
    answer = reply.as_display(text_only=True).strip()
    await msg.finish(I18NContext("greet.message.quiz.result", answer=answer))
```

`wait_anyone()` 不要求引用，等待场景内第一个回答的成员。适合抢答、投票和多人协作。它的提示不会自动附加操作说明，需要在 `greet.message.quiz.prompt` 里写清楚怎么回答。

只需要暂停几秒时，用 `await msg.sleep(3)`。它和等待方法一样，会在暂停期间释放执行锁。

<NoticeBox type="warning" title="等待异常">
`WaitCancelException` 和 `SessionFinished` 继承 `BaseException`，`except Exception` 捕获不到。等待超时、用户取消、会话结束要分别处理。
</NoticeBox>

## 正则匹配

命令需要先写命令前缀才能触发，正则匹配没有这个要求。只要消息里出现符合正则的文本，对应的处理函数就会执行。它适合识别链接、编号和固定格式的句子。

下面用 bilibili 模块识别 av 号。`bili` 是它的模块实例，换成自己的模块变量即可：

```python
import re

from akaribot.core.api import Bot, PlainElement

@bili.regex(
    r"av(\d+)\b",
    flags=re.I,
    mode="A",
    desc="{I18N:bilibili.help.regex.av}",
    element_filter=(PlainElement,),
)
async def _(msg: Bot.MessageSession):
    for video_id in msg.matched_msg[:5]:
        # 演示用，实际项目应使用 I18NContext 组装视频信息
        await msg.send_message(f"找到 av{video_id}")
```

`mode="A"` 使用 `findall`，找出消息里的全部匹配并去重。`msg.matched_msg` 是匹配文本组成的元组。例子只取前 5 个，避免一条消息触发太多次回复。这里的回复文本只是演示，实际模块应换成查询到的视频信息。

`mode="M"` 使用 `re.match`，只从文本开头匹配。命中后 `msg.matched_msg` 是正则的 Match 对象，可以用 `group()` 取分组：

```python
from akaribot.core.api import Bot, I18NContext

@greet.regex(r"签到 (\d+)", mode="M")
async def _(msg: Bot.MessageSession):
    count = int(msg.matched_msg.group(1))
    await msg.finish(I18NContext("greet.message.sign", count=count))
```

常用选项：

- `flags` 传 `re.I` 等正则选项。
- `desc` 是帮助里的说明。
- `logging=False` 不记录每次命中，`show_typing=False` 不显示正在输入。
- `trigger_once_startup=True` 让每个场景只在启动后命中一次，适合发迁移提示或一次性公告。
- `skip_long_message_confirm=True` 跳过超长消息确认。只在对匹配结果有把握时使用。
- `element_filter=(PlainElement,)` 只匹配纯文本，避免把图片说明或提及当成正文。

正则处理函数会在每条消息上运行，不要在里面做网络请求或遍历大量数据。耗时的操作放到后台任务里。

## 定时任务

`@greet.schedule()` 注册后台任务。任务函数不接收 `msg`，也没有会话上下文。需要主动发消息时，用 `Bot.post_message()`。

每天凌晨 4 点清理模块缓存：

```python
from akaribot.core.api import CronTrigger

@greet.schedule(CronTrigger.from_crontab("0 4 * * *"))
async def clean_cache():
    for path in greet.cache_path("tmp").glob("*.tmp"):
        path.unlink(missing_ok=True)
```

`CronTrigger.from_crontab()` 接收五段 crontab 表达式，依次是分钟、小时、日期、月份、星期。它按实例时区计算下一次执行时间。

每 30 分钟检查一次更新：

```python
from akaribot.core.api import IntervalTrigger

@greet.schedule(IntervalTrigger(minutes=30))
async def refresh():
    ...
```

`IntervalTrigger` 的间隔会按 `schedule_interval_multiplier` 调整。测试或调试时可以用这个配置把周期缩短。

定时任务也可以主动推送消息。下面这个任务每周一早上 9 点向启用了 `greet` 的场景推送提醒：

```python
@greet.schedule(CronTrigger.from_crontab("0 9 * * MON"))
async def weekly_report():
    await Bot.post_message("greet", I18NContext("greet.message.weekly"))
```

`Bot.post_message()` 只发送到启用了 `greet` 的场景。没有场景启用模块时，它不会发送任何消息。

定时任务还接受 `DateTrigger`，也可以用 `AndTrigger`、`OrTrigger` 组合多个触发器。同一个函数可以叠加多个 `@schedule`，每个装饰器注册一个任务。

模块未加载时，它的命令、正则和定时任务都不会执行。场景没有启用某个非基础模块时，该模块的命令和正则会在 `parser_policies` 的模块匹配阶段被拦截。

## Hook 与事件

Hook 挂在消息处理链的固定位置，用来观察或改变处理结果。它不替代命令，适合做统计、拦截、统一错误提示和平台事件响应。

### 命令执行后统计

```python
from akaribot.core.api import Bot, HookPoint, Logger

@greet.hook(point=HookPoint.EXECUTION_FINISHED, priority=50, name="count")
async def _(ctx: Bot.ParserHookContext):
    if ctx.module_name != "greet":
        return
    Logger.info(f"greet 执行完成: {ctx.command_first_word}")
```

在 `EXECUTION_FINISHED` 阶段，Hook 只能继续执行，不能改写结果。`priority` 越小越先执行，默认 100。`timeout` 默认 5 秒，`<=0` 表示不限时。

`server_scope=True` 让 Hook 不受场景模块开关限制，但仍受全局停用状态和平台范围限制。

### 拦截出站消息

```python
@greet.hook(point=HookPoint.OUTGOING_BEFORE_SEND, priority=10, name="mute_guard")
async def _(ctx: Bot.ParserHookContext):
    if ctx.session_info.fetch and ctx.session_info.muted:
        return ctx.Stop()
```

`OUTGOING_BEFORE_SEND` 在平台发送前执行。返回 `ctx.Stop()` 可以取消这次发送，也可以修改 `ctx.outgoing.chain` 改写内容。它同时作用于命令回复和 `Bot.post_message()` 的主动推送，适合在机器人被禁止发言的场景里统一拦下出站消息。

### 统一处理执行错误

```python
@greet.hook(point=HookPoint.EXECUTION_ERROR, priority=90, name="friendly_error", timeout=0)
async def _(ctx: Bot.ParserHookContext):
    if ctx.module_name != "greet":
        return
    error = ctx.data.get("error")
    if not isinstance(error, Exception):
        return
    Logger.error(f"greet 执行失败: {error!r}")
    await ctx.msg.send_message(I18NContext("greet.message.error"))
    return ctx.Handled()
```

`EXECUTION_ERROR` 的 `ctx.data` 里有 `error`、`module_type`，部分错误还有 `error_kind`。返回 `ctx.Handled()` 表示已经处理，框架不再记录未处理错误。只处理你认识的异常，其余交给默认处理。

### 响应平台事件

```python
from akaribot.core.api import Bot, Logger

@greet.event("member_joined", available_for="QQBot|Group")
async def _(event: Bot.EventInfo):
    Logger.info(f"新成员加入: {event.target_id}, {event.sender_id}")
```

`@greet.event("事件名")` 订阅适配器上报的事件，不经过命令解析，也没有 `msg`。`available_for` 限定平台与场景类型。例如 QQBot 群聊会上报 `member_joined` 和 `member_left`。

事件字段由适配器决定，常用 `target_id`、`sender_id` 和 `data`。需要发欢迎语时，先把事件目标转成会话，再调用发送方法。

`HookPoint` 覆盖消息生命周期的以下阶段：

- 会话与消息：`SESSION_READY`、`SESSION_BEFORE_WAIT`、`MESSAGE_NORMALIZED`。
- 命令处理：`COMMAND_PREPARE`、`COMMAND_BEFORE_PARSE`、`COMMAND_BEFORE_EXECUTE`、`COMMAND_ROUTE`、`COMMAND_UNMATCHED`。
- 正则匹配：`REGEX_ROUTE`、`REGEX_CANDIDATE`、`CHANNEL_CLAIM`、`REGEX_PREPARE`、`REGEX_BEFORE_EXECUTE`。
- 执行：`EXECUTION_FINISHED`、`EXECUTION_ERROR`、`FINISHED`。
- 出站：`OUTGOING_BEFORE_SEND`、`OUTGOING_SENT`、`OUTGOING_FAILED`。

在路由或候选阶段，Hook 返回 `Stop` 会终止后续处理。

带名称的 Hook 按 `模块名.钩子名` 注册。`Bot.Hook.trigger("模块.钩子")` 只调用这个模块的回调。名称中没有点时，调用会广播给同名 Hook。某个回调失败时，框架记录错误后继续执行其他回调。

## 权限

模块级 `required_*` 对所有命令生效。命令上配置的权限只能比模块级更严，不能放宽。

运行期可以调用 `await msg.check_permission()` 判断当前用户是否为场景管理员，调用 `msg.check_super_user()` 判断是否为超级用户。

基础模块始终开启。普通模块需要在场景内执行 `~module enable`。`~auth` 可以给单个用户授予模块级超级用户权限。

## 配置、数据库与本地化

- 配置在 `config.py` 中用 `@on_module_config("<模块>")` 声明，表名为 `module_<模块>`。配置注释写在 `config.comments.module_<模块>.<字段名>` 下。详见[配置](config.md)。
- 模型放在 `database/models.py`，继承 `DBModel`，表名在 `Meta.table` 声明。新增表要写进 `owned_tables`。结构变更用 `migrations/` 下的脚本完成。详见[数据库](database.md)。
- 文案一律用 `I18NContext("key", **参数)`，并且只在包内 `locales/zh_cn.json` 中创建对应条目。详见[本地化](i18n.md)。

## 常用工具

- `CoolDown(key, msg, delay, whole_target=False)`：按用户或整个场景记录冷却时间，`check()` 返回剩余秒数。
- `gained_petal()`、`lost_petal()`、`cost_petal()`、`sign_get_petal()`、`reset_petals_if_due()`：读写花瓣余额，并在消息中提示。
- `PlayState(game, msg)`：按会话保存小游戏状态。默认在 3600 秒（`GAME_EXPIRED`）后过期。`running()` 作为上下文管理器标记进行中状态。

## 运行期资源

`Bind.Module` 提供由框架管理的资源接口：

- `state()` 跨重载保留进程内状态。
- `cache()` 在版本变化时失效。
- `resource()` 首次使用时加载，并在关闭时释放。
- `cache_path()` 返回框架管理的缓存目录。
- `cleanup()` 注册退出清理。
- `spawn()` 创建由框架跟踪的后台任务。

重载会替换原有注册项，并等待正在运行的任务退出。

## 会话接口

`send_message()` 发送消息并返回消息 ID。`finish()` 发送后抛出 `SessionFinished`。

`wait_confirm()`、`wait_next_message()`、`wait_reply()`、`wait_anyone()` 的用法见上文“等待用户交互”。`sleep()` 在暂停期间释放执行锁。

`delete()` 删除触发消息。`hold()`、`release()` 保持和释放平台上下文。

同一个用户已有命令正在执行时，新命令不会执行，机器人会回复“当前有命令正在执行，请稍后再试。”
