# 适配器开发

适配器包把平台消息与操作接入 core，经 entry point `akaribot.adapters` 发现，目录名即平台键。

## 包结构

```text
akari-bot-adapter-<平台>/
  pyproject.toml
  akaribot/adapters/<平台>/
    info.py      平台名与 ID 前缀
    features.py  能力声明
    config.py    @on_bot_config 配置模板
    context.py   ContextManager 实现
    bot.py       平台入口与事件绑定
    manifest.toml
```

```toml
[project.entry-points."akaribot.adapters"]
telegram = "akaribot.adapters.telegram"
```

`manifest.toml` 声明 `config_table = "bot_telegram"` 与 `credential_fields = ["telegram_token"]`。
前者指向 `config.py` 中的配置表，后者供守护进程在启动前检查同一平台的多个实例是否配置了相同账号或
令牌。

## info.py

```python
from akaribot.core.constants import Info

platform_name = "Telegram"
client_name = Info.resolve_client_name(platform_name)

sender_prefix = f"{client_name}|User"
sender_prefix_list = [sender_prefix]

target_prefix = client_name
target_prefix_list = [f"{client_name}|Private", f"{client_name}|Group"]
```

`platform_name` 是平台展示名，`client_name` 由它派生，多实例时带实例后缀（如 `Telegram-alt`）。
两个前缀列表交给 `client_init()`，用于校验会话 ID 与建立平台路由。`instance_id` 在导入适配器之前由
守护进程置位，`bot_<平台>.toml` 的 `enable` 决定实例是否启动。

## 能力声明

`features.py` 创建 `Features` 实例，`ContextManager` 以类属性引用它：

```python
from akaribot.core.api.adapters import Features

features = Features(support_image=True, support_delete=True, support_private_msg=True)
```

| 分组 | 字段 |
| --- | --- |
| 媒体与格式 | `support_image`、`support_audio`、`support_video`、`support_markdown`、`support_markdown_extension`、`support_embed` |
| 交互 | `support_mention`、`support_reaction`、`support_quote`、`support_typing`、`support_wait`、`support_action_text`、`support_button` |
| 管理 | `support_delete`、`support_manage`、`support_permission_group` |
| 消息范围与开关 | `read_all_messages`、`support_rss`、`support_handle_message_nodes`、`require_enable_modules`、`require_check_dirty_words` |

能力标志同时进入 `client_init()` 的 Peer capabilities。`Module.unsupported_reason()` 依据
`read_all_messages` 与 `support_rss` 拒绝正则、事件与 RSS 模块；`check_bot_state()` 返回的 `BotState`
以 `can_*` 与 `permissions` 描述实际权限，`Module.unsupported_bot_permissions()` 据此阻止启用
缺失权限的模块。

## 平台入口

```python
from akaribot.core.api import Bot
from akaribot.core.api.adapters import client_cleanup, client_init

Bot.register_bot(client_name=client_name)
ctx_id = Bot.register_context_manager(TelegramContextManager)
Bot.register_context_manager(TelegramFetchedContextManager, fetch_session=True)


async def on_startup():
    await client_init(target_prefix_list, sender_prefix_list)


async def on_shutdown():
    await client_cleanup()
```

- `Bot.register_bot()` 设置 `PrivateData` 目录与 `Info.client_name`；`register_context_manager()` 返回
  `ctx_slot` 并填入 `SessionInfo`，`fetch_session=True` 的管理器用于主动抓取会话。
- 收到消息时构造 `SessionInfo`（场景、发送者、`message_id`、`reply_id`、`messages`、`ctx_slot`、`bot_id`），
  再调用 `Bot.process_message(session, ctx)`；平台事件经 `EventInfo.assign(...)` 与
  `Bot.process_event()` 投递。
- `client_init()` 初始化数据库连接（可选 `load_module_db=True`）、连接语言快照并注册 Peer；
  `client_cleanup()` 取消轮询、释放上下文并关闭连接。

## ContextManager

`ContextManager` 以类属性保存 `session_id` 到平台上下文的映射：`add_context()`、`del_context()` 登记与
移除；`activate_context()`、`deactivate_context()` 标记入站处理区间，期间不删除上下文；
`hold_context()`、`release_context()` 跨消息保持上下文，支持嵌套。

须实现的抽象方法：

| 方法 | 用途 |
| --- | --- |
| `check_native_permission()`、`check_bot_state()` | 平台原生管理员与机器人权限快照 |
| `send_message()`、`send_private_msg()`、`derive_private_session()` | 发送、私聊与派生私聊会话 |
| `delete_message()`、`restrict_member()`、`unrestrict_member()`、`kick_member()` | 删除、禁言、解除与移除 |
| `ban_member()`、`unban_member()`、`grant_permission_group()`、`revoke_permission_group()` | 封禁与权限组 |
| `add_reaction()`、`remove_reaction()`、`error_signal()`、`start_typing()`、`end_typing()` | 表情、错误提示与输入状态 |

这些方法由 `PlatformAPI` 的 `context_method()` 自动绑定，Server 跨进程调用时按 `SessionInfo` 选择
上下文管理器。平台自有扩展接口须在 `PlatformAPI` 中显式声明并绑定实现；适配器不直接调用 Server
内部函数，也不写配置文件。

## 配置与本地化

适配器配置用 `@on_bot_config("<平台>")` 声明，表名为 `bot_<平台>`，密钥写入 `[bot_<平台>_secret]`，
字段注释键为 `config.comments.bot_<平台>.<字段名>`（密钥表带 `_secret`）。用户文案只在包内
`locales/zh_cn.json` 建节点，详见[配置](config.md)与[本地化](i18n.md)。
