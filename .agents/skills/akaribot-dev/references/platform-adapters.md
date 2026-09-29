# 平台适配器开发

## 目录

- [适配器包结构](#81-适配器包结构)
- [平台标识](#82-infopy)
- [Features 能力实例](#83-featurespy)
- [消息入口](#84-botpy)
- [ContextManager 实现](#85-contextpy)
- [包元数据与启用](#86-包元数据与启用)
- [导入面](#87-导入面)

开始适配器改动前，同时读取 `architecture.md` 与 `messaging-and-parser.md`；涉及配置、JobQueue 或 loader 时再读取 `infrastructure.md`。路由以主 `SKILL.md` 为准，不要把本文件当作唯一入口。

---

## 8. 平台适配器开发

### 8.1 适配器包结构

每个平台适配器是一个独立分发，源码在 `packages/adapters/akari-bot-adapter-<平台>/`：

```
packages/adapters/akari-bot-adapter-<平台>/
├── pyproject.toml                       # 分发元数据与 entry point
└── akaribot/adapters/<平台>/
    ├── manifest.toml                    # 包内清单：配置表、凭据字段、监听字段
    ├── info.py                          # 平台标识常量
    ├── features.py                      # 平台能力声明
    ├── bot.py                           # 入口：注册与消息处理
    ├── context.py                       # ContextManager 实现
    ├── client.py                        # SDK 客户端（可选）
    ├── config.py                        # 平台配置模板（可选）
    └── locales/zh_cn.json               # 平台文案，只提交 zh_cn
```

`akaribot/adapters/` 是 PEP 420 命名空间目录，不得放 `__init__.py`（门禁 B7）。包内可以放辅助模块，官方适配器现有 `action_text.py`、`buttons.py`、`context_snapshot.py`、`events.py`、`interactions.py`、`message_builder.py` 等，按需参考。

适配器与模块的依赖方向是单向的：适配器不得 import `akaribot.modules.*`（B5），模块也不得 import `akaribot.adapters.*`（B2）。

### 8.2 info.py

```python
from akaribot.core.api import Info

platform_name = "MyPlatform"
client_name = Info.resolve_client_name(platform_name)

target_group_prefix = f"{client_name}|Group"
target_private_prefix = f"{client_name}|Private"
```

`Info.resolve_client_name()` 会把实例 ID 拼进 `client_name`：默认实例不加后缀，其余实例形如 `MyPlatform-alt`。该值同时进入 `target_id` / `sender_id` 前缀，因此实例 ID 一经使用不可更改（CLI 不提供重命名）。

entry point 名不得含 `-`（门禁 B9）：`-` 是多实例分隔符，两者冲突会导致 `client_name` 无法反解。

### 8.3 features.py

```python
from attrs import evolve

from akaribot.core.api import Features

features = Features(
    support_image=True,
    support_mention=True,
    support_embed=True,
    support_delete=True,
    support_quote=True,
    support_rss=True,
    support_typing=True,
    support_wait=True,
)

# 同一平台的不同入口需要微调能力时，从实例复制而不是子类化
slash_features = evolve(features, require_enable_modules=False)
```

平台能力必须以 `Features(...)` 实例声明，不得子类化 `Features`，也不得把类对象赋给 `ContextManager.features`。完整字段以 `akaribot/core/builtins/session/features.py` 为准；官方适配器中 `telegram` 覆盖能力较全，`discord` 次之。

### 8.4 bot.py

```python
from akaribot.core.api import Bot, SessionInfo

from .context import MyPlatformContextManager
from .info import client_name, target_group_prefix

Bot.register_bot(client_name=client_name)
ctx_id = Bot.register_context_manager(MyPlatformContextManager)


async def message_handler(event):
    session = await SessionInfo.assign(
        target_id=f"{target_group_prefix}|{event.group_id}",
        sender_id=f"{client_name}|{event.user_id}",
        target_from=client_name,
        client_name=client_name,
    )
    await Bot.process_message(session, event)
```

`Bot.register_bot()` 与 `Bot.register_context_manager()` 都在导入期执行：entry point 指向本包，core 发现包时导入它即完成注册。需要为拉取历史消息单独提供上下文管理器时，再调用一次并传 `fetch_session=True`，参考 `TelegramFetchedContextManager`。

### 8.5 context.py

```python
from typing import Any

from akaribot.core.api.adapters import ContextManager

from .features import features as platform_features


class MyPlatformContextManager(ContextManager):
    context: dict[str, Any] = {}
    features = platform_features

    # 17 个抽象方法一个都不能少；不支持的能力留空实现，并在 Features 里置 False
    @classmethod
    async def check_native_permission(cls, session_info) -> bool: ...

    @classmethod
    async def check_bot_state(cls, session_info): ...

    @classmethod
    async def send_message(cls, session_info, message, quote=True) -> list[str]: ...

    @classmethod
    async def send_private_msg(cls, session_info, user_id, message) -> list[str]: ...

    @classmethod
    async def delete_message(cls, session_info, message_id, reason=None) -> None: ...

    @classmethod
    async def restrict_member(cls, session_info, user_id, duration=None, reason=None) -> None: ...

    @classmethod
    async def unrestrict_member(cls, session_info, user_id) -> None: ...

    @classmethod
    async def kick_member(cls, session_info, user_id, reason=None) -> None: ...

    @classmethod
    async def ban_member(cls, session_info, user_id, reason=None) -> None: ...

    @classmethod
    async def unban_member(cls, session_info, user_id) -> None: ...

    @classmethod
    async def grant_permission_group(cls, session_info, user_id, permission_group_id, reason=None) -> None: ...

    @classmethod
    async def revoke_permission_group(cls, session_info, user_id, permission_group_id, reason=None) -> None: ...

    @classmethod
    async def add_reaction(cls, session_info, message_id, emoji) -> None: ...

    @classmethod
    async def remove_reaction(cls, session_info, message_id, emoji) -> None: ...

    @classmethod
    async def start_typing(cls, session_info) -> None: ...

    @classmethod
    async def end_typing(cls, session_info) -> None: ...

    @classmethod
    async def error_signal(cls, session_info) -> None: ...
```

行为约定：

- `send_message()` 返回平台消息 ID 列表，供后续撤回、加表情使用；`send_private_msg()` 在平台不支持私信或发送失败时吞掉平台异常并返回 `[]`。
- `check_bot_state()` 返回 `BotState`，用于判断机器人自身在该场景的成员状态与平台权限。
- 抽象方法列表以 `akaribot/core/builtins/session/context.py` 的 `ContextManager` 为准；新增抽象方法属于 core 的 API 变更，需同步全部官方适配器。

### 8.6 包元数据与启用

**entry point**（`pyproject.toml`）：

```toml
[project.entry-points."akaribot.adapters"]
my_platform = "akaribot.adapters.my_platform"
```

对 core 的依赖约束必须与仓库其余包字面一致（当前为 `akari-bot-core>=0.1.0,<1.0`），由 `tools/lint_versions.py` 检查。

**manifest.toml**（包内，适配器只用到以下字段）：

```toml
config_table = "bot_my_platform"
credential_fields = ["my_platform_token"]
listen_fields = ["web_host", "web_port"]
supports_replicas = false
id_columns = []
```

- `config_table`：`config.py` 中 `on_bot_config("<平台>")` 登记的表名，缺省按 `bot_<平台>` 推导；
- `credential_fields`：`akaribot doctor` 据此检测「两个实例配了同一账号」；
- `listen_fields`：`akaribot doctor` 据此检测端口冲突；
- `supports_replicas`：默认 `false`，多数平台 SDK 不允许同账号双连接；
- `id_columns`：为将来的实例重命名预留，当前不实现。

**配置模板**（`config.py`）：

```python
from akaribot.core.config.decorator import on_bot_config


@on_bot_config("my_platform")
class MyPlatformConfig:
    enable: bool = False
    my_platform_token: str = ""


@on_bot_config("my_platform", secret=True)
class MyPlatformSecretConfig:
    my_platform_token: str = ""
```

**启用与多实例**：

```bash
akaribot adapter list                          # 按平台列出全部实例
akaribot adapter instance add telegram beta    # 新建实例：写 config/bot_telegram.toml 的 [bot_telegram-beta]
akaribot adapter instance remove telegram beta
```

配置写扁平路径 `config/<基表>.toml`，同一平台的全部实例共用一个文件的不同表：默认实例是 `[bot_telegram]`，其余实例是 `[bot_telegram-<实例 ID>]`。core 的 `CFGManager.load()` 只扫描 `config/*.toml`，写到 `config/adapters/` 的表对 core 不可见。分层布局的读取侧已兼容，但写入仍走扁平路径。

适配器随实例 venv 安装：`akaribot module add telegram`（`add` 同时接受模块名与适配器名）。

### 8.7 导入面

适配器依赖两个门面：

- `akaribot.core.api`：与模块共享的公共面（`Bot`、`SessionInfo`、消息元素、`Features`、`ContextManager` 等）；
- `akaribot.core.api.adapters`：只有适配器使用的设施（`PlatformAPI`、`BotState`、按钮运行时、媒体压缩、S3 存储等）。

模块包不得 import `akaribot.core.api.adapters`（B3），该面只供适配器使用。两个门面都按需解析名字：配置文件缺失时导入期中途中断，未绑定的名字在首次访问时重试，因此发现层可以在配置就绪前安全导入。

官方适配器当前仍有大量 `akaribot.core.*` 深路径 import（`tools/lint_boundaries.py` 的 B8 以 warn 记录），迁移到门面是进行中的工作；新增代码一律写门面路径。

---

