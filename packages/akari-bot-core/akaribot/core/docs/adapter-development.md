# 适配器开发

本文介绍适配器的包结构、能力声明与平台入口。

适配器负责连接第三方平台与 core。它接收平台消息，转换为 core 的会话对象后提交 Server。core 发出的消息与平台操作由它转交平台 SDK 执行。

适配器在 `pyproject.toml` 的 `akaribot.adapters` 入口点中声明平台键与包路径的对应关系，目录名称采用平台键命名。

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

`manifest.toml` 通过 `config_table = "bot_telegram"` 指向 `config.py` 中的配置表。`credential_fields = ["telegram_token"]` 列出登录字段。启动实例前，守护进程会读取这两项配置，并检查同一平台的多个实例是否使用了相同的账号或令牌。

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

`platform_name` 是平台展示名称，`client_name` 由它生成，多实例部署时附带实例后缀（如 `Telegram-alt`）。两个前缀列表传入 `client_init()`，用于校验会话 ID 并建立平台路由映射。

守护进程在导入适配器之前设置 `instance_id`。当 `bot_<平台>.toml` 中的 `enable` 为 `true` 时，守护进程启动该实例。

## 多实例

同一适配器可以启动多个实例。实例 ID 匹配 `[a-z0-9_]{1,24}`，配置表名称为 `bot_<平台>-<实例ID>`，例如 `bot_telegram-alt`。

当指定了实例 ID 时，`Info.resolve_client_name(platform_name)` 返回 `平台-实例ID`（例如 `Telegram-alt`）。`platform_name` 本身保持不变。

实例配置表控制对应实例的启用状态，平台基础配置表保存该平台的默认配置项。

启动实例前，守护进程会读取 `manifest.toml` 的 `credential_fields`，并检查同一平台其他实例的登录信息和监听端口。

若同一平台已存在相同的登录信息或监听端口，守护进程将输出冲突提示并拒绝启动该实例。

## 能力声明

在 `features.py` 中创建 `Features` 实例，`ContextManager` 通过类属性引用该实例：

```python
from akaribot.core.api.adapters import Features

features = Features(support_image=True, support_delete=True, support_private_msg=True)
```

| 分组 | 字段 |
| --- | --- |
| 媒体与格式 | `support_image`、`support_audio`、`support_video`、`support_markdown`、`support_markdown_extension`、`support_markdown_toggle`、`support_embed`、`support_card` |
| 交互 | `support_mention`、`support_reaction`、`support_quote`、`support_typing`、`support_wait`、`support_action_text`、`support_button` |
| 管理 | `support_delete`、`support_manage`、`support_permission_group` |
| 消息范围与开关 | `read_all_messages`、`support_rss`、`support_private_msg`、`support_handle_message_nodes`、`require_enable_modules`、`require_check_dirty_words`、`use_url_md_format`、`use_url_manager`、`use_running_mention` |

各适配器当前声明的能力如下，新增适配器后可对照同平台的实现：

<AdapterCapabilities />

- `client_init()` 注册节点时，将上述能力标志写入 `capabilities`。
- `Module.unsupported_reason()` 依据 `read_all_messages` 和 `support_rss` 标志，判断正则、事件与 RSS 模块在当前会话中是否可用。
- `check_bot_state()` 返回 `BotState`。
- `can_*` 字段记录机器人是否具备执行对应操作的能力，`permissions` 保存平台返回的原生权限。
- 检查结果写入 `SessionInfo`。
- `Module.unsupported_bot_permissions()` 读取该检查结果，验证模块所需的权限。若机器人缺少模块所需权限，该模块将不会启用。

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

- `Bot.register_bot()` 设置 `PrivateData` 目录与 `Info.client_name`。`register_context_manager()` 返回 `ctx_slot`，构造 `SessionInfo` 时必须将 `ctx_slot` 一并传入。指定 `fetch_session=True` 的管理器用于主动获取会话。
- 接收到消息时构造 `SessionInfo`（包含场景、发送者、`message_id`、`reply_id`、`messages`、`ctx_slot`、`bot_id`），随后调用 `Bot.process_message(session, ctx)`。平台事件通过 `EventInfo.assign(...)` 与 `Bot.process_event()` 投递。
- `client_init()` 初始化数据库连接（可选 `load_module_db=True`）、连接语言快照并注册节点。`client_cleanup()` 取消轮询、释放上下文并关闭连接。

## ContextManager

`ContextManager` 以类属性保存 `session_id` 到平台上下文的映射：

- `add_context()` 与 `del_context()` 用于添加和移除上下文。
- `activate_context()` 与 `deactivate_context()` 标记入站消息的处理区间，在该区间内不释放上下文。
- `hold_context()` 与 `release_context()` 用于跨消息保持上下文，支持多层嵌套。

必须实现的抽象方法：

| 方法 | 用途 |
| --- | --- |
| `check_native_permission()`、`check_bot_state()` | 平台原生管理员与机器人权限快照 |
| `send_message()`、`send_private_msg()` | 发送频道消息与私聊消息 |
| `delete_message()`、`restrict_member()`、`unrestrict_member()`、`kick_member()` | 删除、禁言、解除与移除 |
| `ban_member()`、`unban_member()`、`grant_permission_group()`、`revoke_permission_group()` | 封禁与权限组 |
| `add_reaction()`、`remove_reaction()`、`error_signal()`、`start_typing()`、`end_typing()` | 表情、错误提示与输入状态 |

`derive_private_session()` 是基类的具体方法，依据 `target_id` 与 `target_from` 生成私聊会话副本，`send_private_msg()` 的实现可以直接调用它。

需要跨进程调用的方法由 `PlatformAPI` 包装为对应接口。Server 执行跨进程调用时依据 `SessionInfo` 选择上下文管理器。平台扩展接口由 `PlatformAPI` 声明，并由具体适配器绑定实现。

## 配置与本地化

- 适配器配置通过 `@on_bot_config("<平台>")` 声明，表名称为 `bot_<平台>`。
- 密钥写入 `[bot_<平台>_secret]`。
- 字段配置注释键名称为 `config.comments.bot_<平台>.<字段名>`。密钥表的配置注释需附带 `_secret` 后缀。
- 面向用户的文案仅在适配器包的 `locales/zh_cn.json` 中创建，具体参见[配置](config.md)与[本地化](i18n.md)。
