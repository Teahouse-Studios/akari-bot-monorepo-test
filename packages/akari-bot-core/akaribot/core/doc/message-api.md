# 消息 API 参考

本页列出模块处理函数可用的消息接口、参数与边界，不重复模块声明与命令模板的教程；那部分见[模块开发](module-development.md)。文中名字均从 `akaribot.core.api` 导入。

## 会话对象

模块函数接收 `Bot.MessageSession`。对象本身只保存会话快照与本次解析状态，场景字段统一经 `session_info` 读取，例如 `msg.session_info.bot_name` 取机器人名称。

| 字段或属性 | 说明 |
| --- | --- |
| `session_info` | `SessionInfo` 快照；目标、发送者、平台能力、语言与权限都在这里 |
| `sent` / `trigger_msg` | 已发送消息链列表（默认空）；parser 归一化后的触发文本 |
| `matched_msg` / `parsed_msg` | 正则或事件的匹配结果；命令参数解析结果，无模板模块可能为 `None` |
| `target` / `t` / `t_str` | `target` 已弃用，等价于 `session_info`；`t`、`t_str` 按会话语言翻译键或文本 |

场景字段通过 `msg.session_info` 访问：

| 字段 | 说明 |
| --- | --- |
| `target_id`、`target_from`、`client_name` | 场景 ID、场景来源与客户端名 |
| `sender_id`、`sender_from`、`sender_name` | 发送者信息；主动会话可能为空 |
| `message_id`、`reply_id`、`messages`、`session_id`、`timestamp` | 触发消息、回复目标、原始消息链、会话 UUID 与时间戳 |
| `prefixes`、`muted`、`custom_admins`、`enabled_modules` | 可用命令前缀、静音状态、自定义管理员 union ID 与已启用模块 |
| `locale`、`timezone_offset`、`tmp` | `Locale` 对象（语言代码取 `locale.locale`）、`timedelta` 时区偏移与临时字典 |
| `bot_name`、`bot_id`、`is_private`、`fetch`、`support_*` | 本地化机器人名称与 ID；私聊、主动会话与平台能力标志 |

## 发送消息

| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `send_message()` | `message_chain`、`quote=True`、`disable_secret_check=False`、`callback=None`、`callback_id=None`、`callback_timeout=1800`、`callback_once=False` | 发送并返回 `FinishedSession` |
| `finish()` | 参数同 `send_message()`，`message_chain` 可省略 | 发送后抛出 `SessionFinished`；不传链时只结束会话 |
| `send_direct_message()` | `message_chain`、`disable_secret_check=False` | 提交投递后立即返回 `None`，不等待平台回执，也不提供消息 ID |
| `send_private_message()` | `message_chain`、`user_id=None`、`disable_secret_check=False` | 私聊发送，返回消息 ID 列表；空列表表示失败 |

`send_message()` 的 `callback` 不是发送完成回调，而是用户引用或点击该消息后执行的异步回调，入参为回复的 `MessageSession`。`callback_id` 是按钮回调使用的虚拟回复 ID，省略时由框架为缺少 `reply_id` 的按钮生成，没有按钮时按实际消息 ID 绑定；`callback_timeout` 默认 1800 秒，传 `None` 不自动过期；`callback_once=True` 在首次触发后失效。返回值 `FinishedSession` 提供 `message_id` 与异步 `delete()`，平台没有返回 ID 时 `message_id` 可能是空列表。

```python
from akaribot.core.api import Bot, I18NContext, Image, Plain
async def show(msg: Bot.MessageSession):
    sent = await msg.send_message([Plain("你好，"), Image("https://example.com/avatar.png")])
    if sent.message_id:
        await sent.delete()
    await msg.finish(I18NContext("demo.done"))
```

<NoticeBox type="warning">
`disable_secret_check=True` 会跳过 `MessageChain.is_safe` 的敏感信息扫描。仅对已确认安全的内容使用；否则框架会把整条链替换为 `error.message.chain.unsafe`。
</NoticeBox>

## 等待用户输入

| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `wait_confirm()` | `message_chain=None`、`quote=True`、`delete=True`、`timeout=120`、`append_instruction=True`、`no_confirm_action=True`、`release_execution_lock=True`、`consume_any_message=False`、`confirm_token=None` | 等待确认，返回 `bool` |
| `wait_next_message()` | `message_chain=None`、`quote=True`、`delete=False`、`timeout=120`、`append_instruction=True` | 等待同一发送者的下一条消息 |
| `wait_reply()` | `message_chain`、`quote=True`、`delete=False`、`timeout=120`、`all_=False`、`append_instruction=True` | 等待对该消息的引用回复 |
| `wait_anyone()` | `message_chain=None`、`quote=False`、`delete=False`、`timeout=120` | 等待场景内任意成员的消息 |

等待方法都返回新的 `MessageSession`（`wait_confirm()` 返回 `bool`）。默认超时 120 秒，传 `None` 关闭超时；超时、取消或无法取得结果时抛出 `WaitCancelException`。等待期间执行锁会被释放，返回前重新获取，重新获取失败同样按取消处理。

`wait_confirm()` 在 `confirm_token` 非 `None` 时进入严格确认模式，只有完整回复该口令才算确认；普通模式接受 `confirm_command` 中的确认词，用户发送 `no` 会得到 `False`，`consume_any_message=True` 时任意消息都会结束等待，返回值仍按其是否为确认词判定；全局 `no_confirm` 开启时直接返回 `no_confirm_action`。`wait_reply()` 在平台不支持引用回复时退化为 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示；`all_=True` 时接受任意成员的回复。`wait_next_message()` 与 `wait_anyone()` 命中的消息仍会继续进入常规 parser，`wait_confirm()` 与 `wait_reply()` 会消费命中的消息。

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
`WaitCancelException` 与 `SessionFinished` 都继承 `BaseException`，`except Exception` 捕获不到。不要用裸 `except` 包裹包含 `wait_*()` 或 `finish()` 的代码，否则等待取消或会话结束会被吞掉。
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
| `as_display()` | `text_only=False`、`element_filter=None`、`connector="\n"` | 把触发消息转为字符串；`text_only=True` 只保留 `PlainElement` 文本，非文本元素按 KE 码、AT 码等字符串表示 |
| `delete()` | `reason=None` | 删除触发消息，不是删除已发送消息 |
| `sleep()` / `hold()` / `release()` / `start_typing()` / `end_typing()` | `s` / 无 | 暂停并释放执行锁（恢复失败抛 `WaitCancelException`）；保持或释放平台上下文；开始或结束输入状态 |
| `format_time()` / `format_num()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` / `number`、`precision=0` | 按会话时区与语言格式化时间 / 按语言缩放数字（万、亿、兆或 k、M、G） |
| `call_onebot_api()` / `call_api()` | `api_name`、`**kwargs` | 透传 OneBot 扩展接口；`call_api()` 已弃用。平台不支持时返回 `{"success": False, "error": ...}` |
| `restrict_member()` / `unrestrict_member()` | `user_id`、`duration=None`、`reason=None`、`wait=False` / `user_id`、`wait=False` | 禁言与解除禁言，`duration=None` 表示永久 |
| `kick_member()` / `ban_member()` / `unban_member()` | `user_id`、`reason=None`（`unban` 无 reason） | 移除、封禁、解封成员 |

主动会话（`FetchedMessageSession`）没有 `session_info.messages`，调用 `as_display()` 前先判空。`as_display()` 的 `text_only` 默认是 `False`，而 `MessageChain.to_str()` 的默认是 `True`。`add_reaction()`、`remove_reaction()` 作用于触发消息；`grant_permission_group()`、`revoke_permission_group()` 管理平台权限组；`handle_error_signal()` 提交错误信号。

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
| `MessageChain.assign()` / `create()` / `from_list()` | `elements=None` / 无 / `lst` | 由字符串、元素、元素列表或元组构造；创建空链；从 `to_list()` 结果还原 |
| `as_sendable()` | `session_info=None`、`parse_message=True`、`enable_markdown=True` | 解析多语言与 KE 码，并按平台能力降级 |
| `to_str()` / `to_list()` / `to_kecode()` | `text_only=True`、`element_filter=None`、`connector="\n"` | 转为字符串、字典列表或 KE 码 |
| `is_safe` | 属性 | 是否不含敏感信息 |
| `append()` / `insert()` / `remove()` | `element`（`insert` 另有 `index`） | 追加与插入会把字符串归一化为 `PlainElement`；`remove()` 按元素删除 |
| `extend()` / `copy()` | 另一条链或元素列表 / 无 | 原地拼接或复制 |
| `contains()` / `only()` | 元素类型或类型元组 | 是否含某类元素、是否只含某类元素 |

`+` 返回新链并深拷贝元素，`+=` 原地修改；两者都接受 `MessageChain`、元素列表或单个元素，不接受裸字符串。`in` 只接受元素类型，例如 `PlainElement in chain`；传入实例会抛 `TypeError`。`MessageChain.assign()` 传入已有链时原样返回，不复制；需要独立副本时用 `copy()`。

```python
from akaribot.core.api import Image, MessageChain, Plain
chain = MessageChain.assign([Plain("标题"), Image("https://example.com/cover.png")])
chain += Plain("\n结尾")
text = chain.to_str(text_only=True)
```

`PlatformMessageChain.assign()` 按 `session_info.target_from` 选择链，缺失时回退 `default`；`I18NMessageChain.assign()` 按 `session_info.locale.locale` 选择，且必须包含 `default` 键，否则抛 `ValueError`。这两类链都由发送路径自动解析。

## 消息元素

| 构造器 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `Plain()` / `Markdown()` | `*texts`、`disable_joke=False`、`allow_parse=True` | 纯文本与 Markdown 文本；`allow_parse=False` 时不解析 KE 码与多语言标记 |
| `Image()` / `Audio()` / `Video()` | `path`、`headers=None`、`max_h=None`、`allow_split=True` / `path` | 本地路径、URL、Base64 或 PIL 图片；音频与视频 |
| `Embed()` / `EmbedField()` | `title=None`、`description=None`、`url=None`、`timestamp`（缺省取导入时时间）、`color=0x0091FF`、`image=None`、`thumbnail=None`、`author=None`、`footer=None`、`fields=None` / `name`、`value`、`inline=False` | 富文本卡片与字段 |
| `I18NContext()` | `key`、`fallback=True`、`locale_failed_prompt=True`、`disable_joke=False`、`**kwargs` | 按会话语言解析的文案 |
| `Mention()` | `user_id` | 提及用户，格式为平台前缀加用户 ID |
| `Url()` | `url`、`trusted=None`、`md_format=False`、`md_format_name=None` | 链接元素，受 URL 策略约束 |
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
`Plain`、`Image`、`Embed` 等名字绑定的是对应元素的 `assign` 类方法，不是元素类。类型判断应使用 `PlainElement`、`ImageElement`、`EmbedElement` 等真实类，`isinstance(x, Plain)` 会报错。
</NoticeBox>

## 消息节点与渲染

`MessageNodes.assign(values, name=None)` 把多条 `MessageChain` 组成转发节点列表，`name` 省略时自动生成。`send_message()` 接受 `MessageNodes`；平台未声明 `support_handle_message_nodes` 时，框架会把它渲染为图片再发送。

```python
from akaribot.core.api import MessageChain, MessageNodes, Plain
nodes = MessageNodes.assign([
    MessageChain.assign([Plain("第一条")]),
    MessageChain.assign([Plain("第二条")]),
])
await msg.send_message(nodes)
```

发送路径统一处理以下降级：

- `I18NContext` 按会话语言解析；`Markdown` 在平台不支持 `support_markdown` 时转为纯文本。
- `Embed` 在平台不支持 `support_embed` 时转为文本与图片；`ActionText` 在平台不支持 `support_action_text` 时转为纯文本；`Button` 与 `ButtonFrame` 在平台不支持 `support_button` 时丢弃。
- 空链替换为 `error.message.chain.empty`；未通过 `is_safe` 的链替换为 `error.message.chain.unsafe`，除非发送时传入 `disable_secret_check=True`。
