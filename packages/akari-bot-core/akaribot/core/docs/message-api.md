# 消息 API 参考

本文列出模块处理函数可用的消息接口、消息链与消息元素。接口与参数均从 `akaribot.core.api` 导入，模块声明与命令模板的编写规范参见[模块开发](module-development.md)。

## 会话对象

模块处理函数接收 `Bot.MessageSession` 实例。该对象本身仅保存会话快照与当前解析状态，场景及用户相关字段均通过 `session_info` 读取（例如通过 `msg.session_info.bot_name` 获取机器人的本地化展示名称）。

| 字段或属性 | 说明 |
| --- | --- |
| `session_info` | `SessionInfo` 快照。目标、发送者、平台能力、语言与权限均记录于该快照中 |
| `sent` / `trigger_msg` | 已发送消息链列表（默认空）。parser 处理后的触发文本 |
| `matched_msg` / `parsed_msg` | 正则或事件的匹配结果。命令参数解析结果，无模板模块可能为 `None` |
| `target` / `t` / `t_str` | `target` 已弃用，等价于 `session_info`。`t`、`t_str` 按会话语言翻译键或文本 |

场景字段通过 `msg.session_info` 访问：

| 字段 | 说明 |
| --- | --- |
| `target_id`、`target_from`、`client_name` | 场景 ID、场景来源与客户端名称 |
| `sender_id`、`sender_from`、`sender_name` | 发送者元数据（主动推送会话中可能为空） |
| `message_id`、`reply_id`、`messages`、`session_id`、`timestamp` | 触发消息、回复目标、原始消息链、会话 UUID 与时间戳 |
| `prefixes`、`muted`、`custom_admins`、`enabled_modules` | 可用命令前缀、禁止发言状态、自定义管理员 union ID 与已启用模块 |
| `locale`、`timezone_offset`、`display_timezone_offset`、`tmp` | `Locale` 对象（语言代码通过 `locale.locale` 获取）、场景与个人显示时区偏移（`timedelta`，未设置时为 `None`）与临时字典 |
| `tz`、`display_tz`、`tz_label`、`display_tz_label` | 场景时区与展示时区（`tzinfo`）及其规范偏移字符串。展示时区未设置时跟随场景时区 |
| `bot_name`、`bot_id`、`is_private`、`fetch`、`support_*` | 本地化机器人名称与平台账号 ID，包含私聊标识、主动会话标识及各项平台能力标志 |

## 发送消息

| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `send_message()` | `message_chain`、`quote=True`、`disable_secret_check=False`、`callback=None`、`callback_id=None`、`callback_timeout=1800`、`callback_once=False` | 发送并返回 `FinishedSession` |
| `finish()` | 参数同 `send_message()`，`message_chain` 可省略 | 发送后抛出 `SessionFinished`。不传入消息链时仅结束会话 |
| `send_direct_message()` | `message_chain`、`disable_secret_check=False` | 提交后立即返回 `None`。消息 ID 由其他接口提供 |
| `send_private_message()` | `message_chain`、`user_id=None`、`disable_secret_check=False` | 私聊发送，返回消息 ID 列表。空列表表示失败 |

`send_message()` 的 `callback` 回调函数在用户引用回复或点击交互按钮后执行，传入的回调参数为对应响应的 `MessageSession` 实例。

`callback_id` 为按钮回调机制所使用的虚拟回复 ID，其生成与校验规则如下：

- 省略 `callback_id` 时，框架会为缺少 `reply_id` 的按钮生成虚拟 ID。
- 消息中未包含交互按钮时，框架按实际消息 ID 绑定。

`callback_timeout` 默认取值为 1800 秒。传入 `None` 表示不设置超时。`callback_once=True` 表示首次触发后失效。

调用返回的 `FinishedSession` 对象包含已发送消息的 `message_id`。`delete()` 为异步方法，用于撤回或删除已投递的消息。当第三方平台未返回消息唯一标识时，`message_id` 将为空列表。

```python
from akaribot.core.api import Bot, I18NContext, Image, Plain
async def show(msg: Bot.MessageSession):
    sent = await msg.send_message([Plain("你好，"), Image("https://example.com/avatar.png")])
    if sent.message_id:
        await sent.delete()
    await msg.finish(I18NContext("demo.done"))
```

<NoticeBox type="warning">

发送路径默认执行 `MessageChain.is_safe` 的敏感信息扫描。检查未通过时，整条消息链将被替换为 `error.message.chain.unsafe`。仅当确认内容安全时，才允许传入 `disable_secret_check=True` 跳过检查。

</NoticeBox>

## 等待用户输入

| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `wait_confirm()` | `message_chain=None`、`quote=True`、`delete=True`、`timeout=120`、`append_instruction=True`、`no_confirm_action=True`、`release_execution_lock=True`、`consume_any_message=False`、`confirm_token=None` | 等待确认，返回 `bool` |
| `wait_next_message()` | `message_chain=None`、`quote=True`、`delete=False`、`timeout=120`、`append_instruction=True` | 等待同一发送者的下一条消息 |
| `wait_reply()` | `message_chain`、`quote=True`、`delete=False`、`timeout=120`、`all_=False`、`append_instruction=True` | 等待对该消息的引用回复 |
| `wait_anyone()` | `message_chain=None`、`quote=False`、`delete=False`、`timeout=120` | 等待场景内任意成员的消息 |

等待消息的方法均返回新的 `MessageSession` 实例，`wait_confirm()` 例外，仅返回 `bool`。

- 默认超时 120 秒。传入 `None` 关闭超时。
- 超时、取消或无法获取结果时抛出 `WaitCancelException`。
- 等待期间默认释放执行锁。方法返回前重新获取该锁，获取失败按取消处理。
- `wait_confirm()` 在 `confirm_token` 非 `None` 时进入严格确认模式，必须原样回复该口令，才视为确认。普通模式接受 `confirm_command` 中的确认词。发送 `no` 返回 `False`。
- `consume_any_message=True` 时，任意消息都会结束等待，返回值仍按是否为确认词判断。
- 全局 `no_confirm` 开启时，直接返回 `no_confirm_action`。
- 平台不支持引用回复时，`wait_reply()` 改用 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示。`all_=True` 时接受任意成员的回复。
- `wait_next_message()` 与 `wait_anyone()` 匹配到的消息仍交给常规解析器（parser）处理。`wait_confirm()` 与 `wait_reply()` 会取走匹配到的消息，该消息不会交给常规解析器（parser）处理。

```python
from akaribot.core.api import Bot, WaitCancelException
async def choose(msg: Bot.MessageSession):
    try:
        if not await msg.wait_confirm("确认继续吗？", timeout=60):
            await msg.finish("已取消")
    except WaitCancelException:
        await msg.finish("等待超时")
```

<NoticeBox type="warning">

`WaitCancelException` 与 `SessionFinished` 均继承自 `BaseException`，无法通过 `except Exception` 捕获。

</NoticeBox>

## 权限

| 方法 | 参数 | 说明 |
| --- | --- | --- |
| `check_super_user()` | 无，同步 | 发送者是否为超级用户 |
| `check_permission()` | 无，异步 | 自定义管理员或超级用户返回 `True`，否则检查平台原生权限 |
| `check_native_permission()` | `user_id=None`，异步 | 指定成员或发送者的平台原生管理员权限 |

```python
from akaribot.core.api import Bot
async def manage(msg: Bot.MessageSession):
    if not msg.check_super_user() and not await msg.check_permission():
        await msg.finish("权限不足")
```

## 其他操作

| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `as_display()` | `text_only=False`、`element_filter=None`、`connector="\n"` | 将触发消息序列化为文本字符串。`text_only=True` 仅保留 `PlainElement` 文本，非文本元素按 KE 码、AT 码等字符串表示 |
| `delete()` | `reason=None` | 删除触发消息 |
| `sleep()` / `hold()` / `release()` / `start_typing()` / `end_typing()` | `s` / 无 | 暂停并释放执行锁（恢复失败时抛出 `WaitCancelException`）。保持或释放平台上下文。开始或结束输入状态 |
| `format_time()` / `format_num()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` / `number`、`precision=0` | 依据会话时区与语言环境格式化时间戳 / 依据语言规则缩放并格式化数值（支持万、亿、兆或 k、M、G 计数制） |
| `call_onebot_api()` / `call_api()` | `api_name`、`**kwargs` | 将调用转发至 OneBot 扩展接口（`call_api()` 为已废弃接口）。若平台不支持该调用，将返回 `{"success": False, "error": ...}` |
| `restrict_member()` / `unrestrict_member()` | `user_id`、`duration=None`、`reason=None`、`wait=False` / `user_id`、`wait=False` | 执行禁言或解除禁言限制，当 `duration=None` 时表示永久禁言 |
| `kick_member()` / `ban_member()` / `unban_member()` | `user_id`、`reason=None`（`unban` 无 reason） | 移除、封禁或解除封禁群组成员 |

`now()` 与 `today()` 按场景时区返回当前时间与日期，业务代码获取当前时间时应调用这两个方法。

主动会话（`FetchedMessageSession`）不包含 `session_info.messages`。调用 `as_display()` 前，请先检查其是否为空。

- `as_display()` 的 `text_only` 默认值为 `False`，`MessageChain.to_str()` 默认值为 `True`。
- `add_reaction()`、`remove_reaction()` 作用于触发消息。
- `grant_permission_group()`、`revoke_permission_group()` 管理平台权限组。
- `handle_error_signal()` 提交错误信号。

```python
from akaribot.core.api import Bot
async def report(msg: Bot.MessageSession):
    await msg.delete()
    await msg.sleep(1.5)
    await msg.send_message(msg.format_time(msg.session_info.timestamp or 0.0))
```

## 消息链

| 方法或属性 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `append()` / `insert()` / `remove()` | 元素或纯文本（`insert` 另有 `index`） | 追加与插入会将纯字符串转换为 `PlainElement`。`remove()` 按元素删除 |
| `extend()` / `copy()` | 另一条链或元素列表 / 无 | 原地拼接或复制 |
| `contains()` / `only()` | 元素类型或类型元组 | 是否包含某类元素、是否仅包含某类元素 |

`+` 运算符返回深拷贝元素后的全新消息链，`+=` 运算符执行原地追加修改。两者的右值操作数支持 `MessageChain`、元素列表或单一消息元素，不支持纯字符串。`in` 运算符仅用于匹配元素类型（例如 `PlainElement in chain`），若传入元素实例将抛出 `TypeError`。`MessageChain.assign()` 接收已有消息链时直接原样返回而不执行复制。若需要独立副本，请显式调用 `copy()`。

```python
from akaribot.core.api import Image, MessageChain, Plain
chain = MessageChain.assign([Plain("标题"), Image("https://example.com/cover.png")])
chain += Plain("\n结尾")
text = chain.to_str(text_only=True)
```

`PlatformMessageChain.assign()` 依据 `session_info.target_from` 选择平台对应的专属消息链，若缺少匹配键则回退至 `default` 项。`I18NMessageChain.assign()` 依据 `session_info.locale.locale` 语言标识选择对应的消息链，此类型消息链必须包含 `default` 回退项，否则抛出 `ValueError`。两类多态链均在发送管线中自动完成解析分发。

## 消息元素

| 构造器 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `Plain()` / `Markdown()` | `*texts`、`disable_joke=False`、`allow_parse=True` | 纯文本与 Markdown 文本。`allow_parse=False` 时不解析 KE 码与多语言标记 |
| `Image()` / `Audio()` / `Video()` | `path`、`headers=None`、`max_h=None`、`allow_split=True` / `path` | 本地路径、URL、Base64 或 PIL 图片。音频与视频 |
| `Embed()` / `EmbedField()` | `title=None`、`description=None`、`url=None`、`timestamp`（默认采用导入时时间）、`color=0x0091FF`、`image=None`、`thumbnail=None`、`author=None`、`footer=None`、`fields=None` / `name`、`value`、`inline=False` | 富文本卡片与字段 |
| `I18NContext()` | `key`、`fallback=True`、`locale_failed_prompt=True`、`disable_joke=False`、`**kwargs` | 按会话语言解析的文案 |
| `Mention()` | `user_id` | 提及用户，格式为平台前缀加用户 ID |
| `Url()` | `url`、`trusted=None`、`md_format=False`、`md_format_name=None` | 链接元素，受 URL 策略限制 |
| `FormattedTime()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` | 按会话时区格式化的时间 |
| `ActionText()` | `text`、`show=None`、`reference=False`、`show_on_fallback=True`、`quote_on_fallback=False` | 可点击的命令文本 |
| `Button()` / `ButtonFrame()` | `show`、`value`、`reply_id=None`、`permission=OWNER`、`click_limit=1` / `rows` | 按钮与按钮区域 |

```python
from akaribot.core.api import Embed, I18NContext
async def card(msg: Bot.MessageSession):
    await msg.finish([
        I18NContext("demo.card.title", user=msg.session_info.sender_name),
        Embed(title="状态", description="运行正常"),
    ])
```

<NoticeBox type="warning">

`Plain`、`Image`、`Embed` 等名称绑定的是对应元素的 `assign` 类方法。类型判断使用 `PlainElement`、`ImageElement`、`EmbedElement` 等真实类。

</NoticeBox>

## 消息节点与渲染

`MessageNodes.assign(values, name=None)` 将多条 `MessageChain` 组合封装为转发消息节点列表，省略 `name` 参数时将自动生成默认节点名称。`send_message()` 原生支持 `MessageNodes`。若当前平台未声明具备 `support_handle_message_nodes` 能力，框架将自动把消息节点合成渲染为图片后发送。

```python
from akaribot.core.api import MessageChain, MessageNodes, Plain
nodes = MessageNodes.assign([
    MessageChain.assign([Plain("第一条")]),
    MessageChain.assign([Plain("第二条")]),
])
await msg.send_message(nodes)
```

发送路径会处理以下情况：

- `I18NContext` 按会话语言解析。`Markdown` 在平台不支持 `support_markdown` 时转为纯文本。
- 若目标平台未声明 `support_embed` 能力，`Embed` 富文本卡片将降级为图文混排输出。若未声明 `support_action_text`，`ActionText` 将转换为常规纯文本。若未声明 `support_button`，`Button` 与 `ButtonFrame` 将被过滤移除。
- 空消息链将被替换为 `error.message.chain.empty`。未通过 `is_safe` 检查的整条消息链将被替换为 `error.message.chain.unsafe`，发送时传入 `disable_secret_check=True` 的情况除外。
