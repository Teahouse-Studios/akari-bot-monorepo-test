# 消息、会话与命令解析

## 目录

- [Bot 类](#51-bot-类-akaribotcorebuiltinsbot)
- [消息系统](#52-消息系统-akaribotcorebuiltinsmessage)
- [会话系统](#53-会话系统-akaribotcorebuiltinssession)
- [命令解析器](#54-命令解析器-akaribotcorebuiltinsparser)
- [KE 码](#122-ke-码消息元素文本表示)
- [上下文保持](#123-上下文保持长任务)
- [执行锁](#124-执行锁防并发)
- [TOS 与错字纠正](#125-tos-限流)
- [自定义异常](#128-自定义异常)

这是当前最大的一份参考文件。只修改 loader、配置、数据库或队列时不要读取它；对应内容在 `infrastructure.md`。只修改模块声明和业务命令时先读 `module-development.md`，仅在涉及消息、会话或 parser API 时再加载本文件。

---

### 5.1 Bot 类 (`akaribot.core.builtins.bot`)

中央枢纽类，源码在 `packages/akari-bot-core/akaribot/core/builtins/bot/__init__.py`。大多数需要类状态的方法为 `@classmethod`；纯转发方法也可能是 `@staticmethod`：

```python
class Bot:
    # 类型/工具引用（供模块使用，避免模块再去 import 深层路径）
    MessageSession = MessageSession
    FetchedMessageSession = FetchedMessageSession
    ModuleHookContext = ModuleHookContext
    ParserHookContext = ParserHookContext
    EventInfo = EventInfo
    ExecutionLockList = ExecutionLockList
    Info = Info
    Temp = Temp
    PrivateData = PrivateData

    # 上下文管理
    ContextSlots: list[ContextManager] = []  # 已注册的平台上下文管理器
    fetched_session_ctx_slot = 0             # fetch_target 用的 slot
    base_superuser_list = CoreConfig.base_superuser

    # 消息与事件入口（除特别标注外为 @classmethod）
    async def process_message(cls, session_info, ctx, features_override=None)
    # 平台消息入口：注入 Features、登记平台上下文，再经 ServerAPI.receive_message 投递
    async def process_event(cls, event_info)         # 无触发消息的平台事件入口
    async def cancel_pending_messages(cls) -> None   # 取消并等待仍在投递的后台消息任务

    # 主动发送
    async def post_message(cls, module_name, message, session_list=None, **kwargs)
    # 主动发送消息到启用了指定模块的所有会话
    @staticmethod
    async def post_global_message(message, session_list=None, **kwargs)
    # 主动发送消息到所有会话（不限模块）

    # 会话抓取、场景组展开与通道归拢
    async def fetch_target(cls, target_id, sender_id=None, create=False, is_private=False)
    async def fetch_target_list(cls, target_list, create=False) -> list[FetchedSessionInfo]
    async def resolve_union_targets(cls, target_list) -> list[str]
    async def fetch_union_target_list(cls, target_list, create=False) -> list[FetchedSessionInfo]
    @staticmethod
    async def group_sessions_by_channel(session_list) -> list[list[FetchedSessionInfo]]
    async def pick_channel_heads(cls, session_list) -> list[FetchedSessionInfo]
    async def get_enabled_this_module(cls, module) -> list[FetchedSessionInfo]

    async def send_direct_message(cls, target, message, disable_secret_check=False)
    async def send_direct_message_to_union_target(cls, union_id, message, disable_secret_check=False)
    async def send_private_message(cls, session_info, message, user_id=None) -> list[str]

    async def start_typing(cls, session_info) -> None
    async def end_typing(cls, session_info) -> None

    def register_context_manager(cls, ctx_manager, fetch_session=False) -> int
    # 注册平台上下文管理器，返回 slot 索引
    def register_bot(cls, client_name=None, private_data_path=None)

    # camelCase 别名
    postMessage = post_message
    postGlobalMessage = post_global_message

    class Hook:
        @staticmethod
        async def trigger(module_or_hook_name, session_info=None, args=None, timeout=None)
        # 触发模块钩子或自定义钩子；timeout 覆盖订阅默认执行预算，<=0 表示不限时
```

`process_message()` 把消息交给后台任务后立即返回，平台 SDK 的回调因此不被服务端处理阻塞。`fetch_target()` 的 `is_private` 供调用方指明私聊语义：主动获取的会话没有平台事件可依据，缺省按非私聊处理。

**模块依赖面**：`Bot` 在模块末尾以 `add_export(Bot)` 注册进 `akaribot.core.exports` 的全局 `exports` 对象，核心内部以 `exports["Bot"]` 取用，避免循环导入。模块与适配器作者不照此取名字，改从门面导入：

```python
from akaribot.core.api import Bot, MessageChain, MessageSession, Plain, Features
```

适配器另有专用门面 `akaribot.core.api.adapters`，收录 `ContextManager`、`BotState`、`PlatformAPI`、`client_init`、`client_cleanup` 等只有适配器会用的设施，`ContextManager` 只在适配器面导出。模块包 import `akaribot.core` 深路径时，`tools/lint_boundaries.py` 的 B8 规则按被 import 的符号是否收录进门面记为 warn。

**包发现与包清单**：模块包与适配器包由 `akaribot.core.registry.PackageRegistry` 经 entry points（`akaribot.modules` / `akaribot.adapters`）发现，目录扫描只是兜底。每个包在自身的导入包目录下放 `manifest.toml`，其中 `requires_core_api` 按 PEP 440 描述符声明所需的 core 公共 API 区间，与 `akaribot.core.registry.CORE_API_VERSION`（当前为 `1`）比对；`provides_modules` 登记注册的模块名，`owned_tables` 登记数据表，`locales`、`assets`、`migrations`、`config_table` 声明资源与配置的相对位置。

**入口**：真实入口是 `akaribot.core.entrypoints.run` 的 `main()`（`python -m akaribot.core.entrypoints.run`），根 `bot.py` 只是把 `import bot` 换成 run 模块本身、把 `python bot.py` 转发到 `main()` 的兼容层；测试运行器的真实入口是 `akaribot.testing.runner.run()`（`python -m akaribot.testing`），根 `tester.py` 同为兼容层。

### 5.2 消息系统 (`akaribot.core.builtins.message`)

#### MessageChain (`chain.py`)

```python
@define
class MessageChain:
    values: list[MessageElement]  # 消息元素列表

    @classmethod
    def create(cls)               # 空链
    @classmethod
    def assign(cls, elements)     # 工厂方法，支持 str/list/tuple/dict/元素/链/None
    @classmethod
    def from_list(cls, lst)       # 从 to_list() 的结果还原

    def as_sendable(self, session_info) -> list  # 转换为可发送格式
    def to_str(self, text_only=True, element_filter=None, connector="\n") -> str
    def to_list(self) -> list[dict]              # 序列化（跨进程用）
    def to_kecode(self) -> str                   # 转 KE 码
    @property
    def is_safe(self) -> bool     # 安全检查（敏感信息过滤）

    # 列表式操作
    def append(self, element)
    def remove(self, element)
    def insert(self, index, element)
    def extend(self, other)
    def copy(self)
    def contains(self, types) -> bool   # 是否含指定元素类型
    def only(self, types) -> bool       # 是否只含指定元素类型
```

支持 `+`、`+=`、`in`、迭代、`len()`、`str()` 操作。`assign()` 对链本身不做深拷贝，对列表输入返回深拷贝后的新链。

#### 消息元素 (`elements.py`, `internal.py`)

```python
# elements.py - 基类
class BaseElement:
    def kecode(self) -> str       # KE 码表示

# 具体元素（字段以真实定义为准）
@define
class PlainElement(BaseElement):
    text: str
    disable_joke: bool = False        # 跳过愚人节文本替换
    allow_parse: bool = True          # 是否参与 KE 码、i18n 与平台消息标记解析

@define
class MarkdownElement(PlainElement):  # 保留 Markdown 格式，平台不支持时降级为纯文本
    ...

@define
class ImageElement(BaseElement):
    path: str                          # 本地路径、URL 或 base64
    headers: dict[str, Any] | None = None
    need_get: bool = False             # 是否需要先下载
    cached_b64: str | None = None
    max_h: int | None = None           # 高度上限，超出后按平台能力压缩
    allow_split: bool = True

@define
class AudioElement(BaseElement):
    path: str

@define
class VideoElement(BaseElement):
    path: str

@define
class URLElement(BaseElement):
    original_url: str
    url: str
    trusted: bool | None = None        # 链接跳板
    applied_md_format: bool = False    # Markdown 格式
    md_format_name: str | None = None  # Markdown 显示名

@define
class FormattedTimeElement(BaseElement):
    timestamp: float
    date: bool = True
    simple: bool = False
    time: bool = True
    seconds: bool = True
    timezone: bool = True

@define
class EmbedFieldElement(BaseElement):
    name: str
    value: str
    inline: bool = False

@define
class EmbedElement(BaseElement):
    title: str | None = None
    description: str | None = None
    url: str | None = None
    timestamp: float = ...
    color: int = 0x0091FF
    image: ImageElement | None = None
    thumbnail: ImageElement | None = None
    author: str | None = None
    footer: str | None = None
    fields: list[EmbedFieldElement] | None = None

@define
class MentionElement(BaseElement):
    client: str                        # 注意：是 client + id 两个字段
    id: str

@define
class I18NContextElement(BaseElement):
    key: str
    kwargs: dict[str, Any]             # 模板参数
    fallback: bool = True
    locale_failed_prompt: bool = True
    disable_joke: bool = False

@define
class ActionTextElement(BaseElement):
    text: PlainElement | I18NContextElement
    show: PlainElement | I18NContextElement | None = None
    reference: bool = False            # 是否引用触发消息
    show_on_fallback: bool = True      # 平台不支持时是否退化为展示文本
    quote_on_fallback: bool = False

@define
class ButtonElement(BaseElement):
    show: str
    value: str
    reply_id: str | None = None
    permission: ButtonPermission = ButtonPermission.OWNER
    click_limit: int | None = 1

@define
class ButtonFrameElement(BaseElement):
    rows: list[ButtonRows]             # 显式指定按钮行布局

@define
class RawElement(BaseElement):
    value: str                         # 原样透传给平台
```

```python
# internal.py - 便捷别名。注意这些是 .assign 工厂方法，不是类本身
Plain = plain = PlainElement.assign
Markdown = markdown = MarkdownElement.assign
Image = image = ImageElement.assign
Audio = audio = AudioElement.assign          # 语音，原 Voice 别名已由 Audio 取代
Video = video = VideoElement.assign
Embed = embed = EmbedElement.assign
EmbedField = embed_field = EmbedFieldElement.assign
Url = url = URLElement.assign
FormattedTime = formatted_time = FormattedTimeElement.assign
I18NContext = i18n_context = I18NContextElement.assign
Mention = mention = MentionElement.assign
Raw = raw = RawElement.assign
ActionText = action_text = ActionTextElement.assign
Button = button = ButtonElement.assign
ButtonFrame = button_frame = ButtonFrameElement.assign
```

> **重要**：`Plain` 等名字绑定的是 `XxxElement.assign` 这个 classmethod，**不是类**。所以 `isinstance(x, Plain)` 会直接报错，类型判断必须用 `elements.py` 里的真实类（`PlainElement` 等）。`assign` 会做参数归一化（例如 `I18NContext("key", a=1)` 把 `a=1` 收进 `kwargs` 字段），因此构造消息元素一律走别名，不要直接调类构造器。`contains()` / `only()` 的入参同样取真实类；`ButtonPermission`、`ButtonRows`、`ButtonPayload` 只有类本身，没有 `assign` 别名。

#### 消息链类型优先级

```
PlatformMessageChain > I18NMessageChain > MessageChain
```

归拢由 `get_message_chain(session, chain)` 完成：先按 `session.target_from` 在 `PlatformMessageChain` 中取平台分支，再按 `session.locale.locale` 在 `I18NMessageChain` 中取语言分支，最后落到 `MessageChain`，任一层的字典键缺失时取该层的 `"default"`。平台特定消息链可以覆盖默认行为；`MessageNodes`（合并转发消息）不参与这三级降级，传入时原样返回。

### 5.3 会话系统 (`akaribot.core.builtins.session`)

#### SessionInfo (`info.py`)

```python
@define
class SessionInfo:
    # 基本信息（只有前三个是必需的）
    target_id: str                    # 目标 ID（如 "QQ|Group|123456"）
    target_from: str                  # 平台来源（如 "QQ", "Discord"）
    client_name: str                  # 客户端名称
    platform_name: str = ""           # 平台展示名，多实例下不含实例后缀
    platform_from: str = ""           # 平台级场景前缀，默认实例下等于 target_from
    owner_peer_id: str | None = None  # 认领该会话的 JobQueue 进程
    sender_id: str | None = None
    sender_from: str | None = None
    sender_name: str | None = None

    # 消息信息
    message_id: str | None = None
    reply_id: str | None = None
    messages: MessageChain | None = None
    timestamp: float | None = None
    session_id: str | None = None     # 由 assign() 生成

    # 平台能力标志（由 Features 注入）
    superuser: bool = False
    support_image / support_audio / support_video / support_mention / support_embed
    support_delete / support_manage / support_permission_group / support_markdown / support_markdown_extension
    support_reaction / support_quote / support_rss / support_typing
    support_wait / support_handle_message_nodes / support_private_msg
    support_action_text / support_button / support_markdown_toggle     # 均默认 False

    # 数据库模型（挂的是 union 行，不是平台 ID 行）
    target_union_info: TargetUnionInfo = None
    sender_union_info: SenderUnionInfo | None = None
    target_union_id: str = ""
    sender_union_id: str | None = None
    target_channel_id: int = 1        # 本会话在场景组内的消息通道号

    # 权限与配置
    banned_users: list | None = None
    custom_admins: list | None = None
    locale: Locale = ...              # 注意是 Locale 对象，不是 str
    timezone_offset: timedelta | None = None
    bot_name / bot_id: str | None = None
    muted: bool | None = None
    enabled_modules: list | None = None
    petal: int | None = None
    prefixes: list[str] = []          # 平台前缀、场景自定义前缀与全局前缀合并后的结果
    platform_prefixes: list[str] = [] # 仅平台侧传入的前缀，供 refresh_info 重新合并
    next_hops: list[str] = []         # 主动推送失败时的下一跳场景
    ctx_slot: int | None = 0          # 指向 Bot.ContextSlots 的索引
    fetch: bool = False
    is_private: bool = False           # 由平台适配器显式判定

    # 行为开关（由 Features 注入）
    require_enable_modules: bool = True
    read_all_messages: bool = True
    require_check_dirty_words: bool = False
    use_url_manager: bool = False
    use_url_md_format: bool = False
    use_running_mention: bool = True
    tmp: dict[str, str] = {}          # 单次处理内的临时数据

    @classmethod
    async def assign(cls, target_id, client_name=None, target_from=None, ...) -> "SessionInfo"
    # 异步工厂方法 - 从数据库加载信息
    async def refresh_info(self)      # 重新拉取数据库状态

    def get_common_target_id(self) -> str    # 取 target_id 的最后一段
    def get_common_sender_id(self) -> str    # 取 sender_id 的最后一段
    @property
    def channel_key(self) -> str             # "union ID|通道号"，现实场景的内存态键
    @property
    def typing_prompt_enabled(self) -> bool
    @property
    def invalid_module_prompt_enabled(self) -> bool
```

`assign()` 并发解析两侧 union 行，`target_channel_id` 取自 `target_union_info.bind.channel_id`；`refresh_info()` 只替换 ORM 对象与派生的权限、语言、前缀、通道号，保留入队时的平台两段，两侧 union 行在排队期间被删除时抛 `ValueError`。冷却、游戏状态、等待任务这类「同一个现实场景内共享」的内存态须按 `channel_key` 建键，只按 union 建键会把仅共享配置、实为不同现实场景的双方并作一处。

`EventInfo` 与 `SessionInfo` 同文件，是平台事件的载体（`event_name`、`data` 与场景、用户两侧的 union 字段），由 `Bot.process_event()` 投递。`FetchedSessionInfo` 是 `SessionInfo` 的空子类，标记主动抓取的会话；`ModuleHookContext` 承载模块钩子的 `args` 与 `session_info`。

#### MessageSession (`internal.py`)

传给模块处理函数的主要对象：

```python
@define
class MessageSession:
    session_info: SessionInfo           # 一切状态的入口
    sent: list[MessageChain] = []       # 已发送消息
    trigger_msg: str = ""               # 触发消息文本
    matched_msg: Match | tuple | None = None  # 正则匹配结果
    parsed_msg: dict = {}               # 解析后的参数
    command_original_word: str = ""     # 别名改写前的命令首词

    @property
    def target(self) -> SessionInfo     # 已废弃，等价于 session_info，新代码不要用
    @property
    def t(self)                         # 本会话语言的翻译函数
    @property
    def t_str(self)                     # 本会话语言的模板函数

    @classmethod
    async def from_session_info(cls, session: SessionInfo)

    # 发送消息
    async def send_message(self, message_chain, quote=True, ...) -> FinishedSession
    async def finish(self, message_chain=None, ...) -> NoReturn  # 发送并抛 SessionFinished
    async def send_direct_message(self, message_chain, disable_secret_check=False)
    async def send_private_message(self, message_chain, user_id=None, ...) -> list[str]
    # 私信给某个用户（默认是本会话的用户），消息不进当前场景，返回空列表即发送失败
    # （平台不支持私信、未加好友、对方关了私信……），需要私密投递的内容据此判定成败

    # 等待用户交互
    async def wait_confirm(self, message_chain=None, timeout=120, ...) -> bool
    async def wait_next_message(self, message_chain=None, timeout=120, ...) -> MessageSession
    async def wait_reply(self, message_chain, timeout=120, all_=False, ...) -> MessageSession
    async def wait_anyone(self, message_chain=None, timeout=120, ...) -> MessageSession
    async def verify_user(self, message_chain=None, timeout=120, delete=True) -> bool
    # 数字验证：抽三个数字并指定其一，支持按钮的平台点按钮，其余平台发数字
    async def sleep(self, s: float)     # 会顺带释放并重获执行锁的 sleep

    # 权限检查
    def check_super_user(self) -> bool          # 同步
    async def check_permission(self) -> bool    # 注意是 async，必须 await
    async def check_native_permission(self) -> bool
    async def check_bot_state(self) -> BotState # 机器人在场景内的成员与原生权限快照

    # 消息转换 / 格式化
    def as_display(self, text_only=False, element_filter=None, connector="\n") -> str
    def format_time(self, timestamp, date=True, simple=False, time=True, seconds=True, timezone=True) -> str
    def format_num(self, number, precision=0) -> str  # 按语言习惯格式化数字

    # 平台操作（通过 JobQueue 回到 bot 进程）
    async def delete(self, reason=None)         # 删除的是本条消息，无 message_id 参数
    async def restrict_member(self, user_id, duration=None, reason=None, wait=False)
    async def unrestrict_member(self, user_id, wait=False)
    async def kick_member(self, user_id, reason=None)
    async def ban_member(self, user_id, reason=None)
    async def unban_member(self, user_id)
    async def grant_permission_group(self, user_id, permission_group_id, reason=None, wait=False)
    async def revoke_permission_group(self, user_id, permission_group_id, reason=None, wait=False)
    async def add_reaction(self, emoji)         # 只接 emoji，作用于本条消息
    async def remove_reaction(self, emoji)
    async def handle_error_signal(self)
    async def hold(self) / async def release(self)      # 长任务保持上下文
    async def start_typing(self) / async def end_typing(self)

    # 平台原生 API 直通
    async def call_onebot_api(self, api_name, **kwargs)
    async def call_api(self, api_name, **kwargs)        # 已废弃，转发到 call_onebot_api
```

`wait_*` 系列在超时或用户取消时抛 `WaitCancelException`；`wait_reply()` 在平台不支持引用时退化为 `wait_next_message()` 或 `wait_anyone()`。`verify_user()` 与 `wait_next_message()` 支持传入 `possibly_choices`，按钮平台据此渲染候选。既有调用点另有小驼峰别名（`waitConfirm`、`sendMessage`、`checkPermission` 等），新代码使用下划线命名。

**`FinishedSession`**：`send_message()` 的返回值，含 `session`、`message_id` 与 `delete()` 方法。
**`FetchedMessageSession`**：`MessageSession` 的子类，由 `Bot.fetch_target()` 产出，用于主动发消息（没有真实触发消息）；`Bot.send_private_message()` 也借它复用同一条发送链路。`wait_*` 取得的回复会话与原始命令共享同一个 `ExecutionState`（见 12.4），但不取得最终清理所有权。

#### ContextManager (`context.py`)

平台适配器必须实现的抽象基类：

```python
class ContextManager(ABC):
    context: dict[str, Any] = {}          # session_id -> 平台上下文
    features: Features = Features()
    typing_flags: dict[str, asyncio.Event] = {}       # 输入状态标志
    context_marks_hold: dict[str, int] = {}           # 嵌套保持计数

    # 上下文生命周期
    @classmethod
    def add_context(cls, session_info, context)
    @classmethod
    def del_context(cls, session_info)     # 被保持时跳过删除
    @classmethod
    def hold_context(cls, session_info)    # 防止删除（长任务），支持嵌套
    @classmethod
    def release_context(cls, session_info) # 释放保持，计数归零即删除

    # 派生一份指向私聊场景的 SessionInfo（换掉 target、清掉 session_id / message_id），
    # 各平台的 send_private_msg 靠它复用自家的 send_message，不必重写一遍渲染逻辑
    @classmethod
    def derive_private_session(cls, session_info, target_id, target_from) -> SessionInfo

    # 平台必须实现的 17 个抽象方法（全部是 @classmethod + @abstractmethod）
    async def check_native_permission(cls, session_info) -> bool
    async def check_bot_state(cls, session_info) -> BotState
    async def send_message(cls, session_info, message, quote=True) -> list[str]
    async def send_private_msg(cls, session_info, user_id, message) -> list[str]
    # 私信给 user_id（带平台前缀），session_info 只提供语言与能力上下文；
    # 实现必须吞掉平台异常并返回 []，调用方以"有没有拿到消息 ID"判定成败
    async def delete_message(cls, session_info, message_id, reason=None) -> None
    async def restrict_member(cls, session_info, user_id, duration=None, reason=None) -> None
    async def unrestrict_member(cls, session_info, user_id) -> None
    async def kick_member(cls, session_info, user_id, reason=None) -> None
    async def ban_member(cls, session_info, user_id, reason=None) -> None
    async def unban_member(cls, session_info, user_id) -> None
    async def grant_permission_group(cls, session_info, user_id, permission_group_id, reason=None) -> None
    async def revoke_permission_group(cls, session_info, user_id, permission_group_id, reason=None) -> None
    async def add_reaction(cls, session_info, message_id, emoji) -> None
    async def remove_reaction(cls, session_info, message_id, emoji) -> None
    async def start_typing(cls, session_info) -> None
    async def end_typing(cls, session_info) -> None
    async def error_signal(cls, session_info) -> None
```

平台不支持某个能力时，实现里直接 `pass`（或抛 `NotImplementedError`）并在 `Features` 里把对应 `support_*` 置 `False`；框架靠 `Features` 决定是否调用，而不是靠捕获异常。基类实现会在 `session_id` 不在 `cls.context` 时抛 `ValueError`，`hold_context()` 在同样情形下抛 `SessionContextUnavailable`。`BotState` 定义在 `session/bot_state.py`，字段为可空布尔（`joined`、`is_admin`、`can_send_private_messages` 等），`None` 表示平台未暴露该状态；平台特有字段留在 `permissions` 与 `raw` 中。

#### Features (`features.py`)

平台能力声明。`Bot.process_message()` 会把这些字段注入到 `SessionInfo` 的同名字段上。

```python
@define
class Features:
    # 消息能力
    support_image: bool = False
    support_audio: bool = False
    support_video: bool = False
    support_mention: bool = False
    support_embed: bool = False
    support_delete: bool = False
    support_manage: bool = False
    support_permission_group: bool = False
    support_markdown: bool = False
    support_markdown_extension: bool = False
    support_reaction: bool = False
    support_quote: bool = False
    support_rss: bool = False
    support_typing: bool = False
    support_wait: bool = False
    support_handle_message_nodes: bool = False
    support_private_msg: bool = False
    support_action_text: bool = False
    support_button: bool = False
    support_markdown_toggle: bool = False

    # 行为开关
    use_url_md_format: bool = False
    use_url_manager: bool = False
    use_running_mention: bool = True       # 注意默认是 True
    require_check_dirty_words: bool = False
    require_enable_modules: bool = True    # 注意默认是 True
    read_all_messages: bool = True         # 是否可读取场景内全部消息

    @classmethod
    def override(cls, **kwargs) -> Features
    # 等价于直接构造实例，保留本方法仅为兼容既有调用点
```

平台必须用关键字参数构造 `Features` **实例**，不要通过子类覆盖默认值，也不要把 `Features` 类本身赋给 ContextManager。子类化会静默丢字段：attrs 只把带类型注解的名字视作字段，子类中漏写注解的同名属性会在 `slots` 重建类时被删除，读到的仍是基类默认值；需要在既有能力集上微调时用 `attrs.evolve()`。

#### 多实例

适配器实例身份由 `akaribot.core.constants.info.Info` 承载：`platform_name` 是平台展示名（同一平台的全部实例共用），`instance_id` 是实例 ID（空串表示默认实例），`client_name` 由两者派生。`Info.resolve_client_name(platform_name, instance_id)` 在实例 ID 为空时原样返回平台展示名，否则返回 `<平台>-<实例 ID>`，分隔符固定为 `-`，因为 `|` 是 `target_id` 的段分隔符。实例 ID 须匹配 `Info.INSTANCE_ID_PATTERN`（`[a-z0-9_]{1,24}`），适配器的 entry point 名不得含 `-`。

`client_name` 是 `target_id` 与 `sender_id` 前缀的组成部分（如 `Telegram-alt|Group|12345`），因此实例 ID 一经使用不可更改；`akaribot adapter` 不提供 `instance rename`，需要更换时按「新建实例 + 迁移数据」处理。旧部署经 `akaribot migrate legacy <目录>` 迁移后一律落在默认实例（实例 ID 为空），`target_id` 前缀逐字节保持历史取值。

多实例引入平台两段判据：`platform_name` 与 `platform_from` 是平台级的两段，默认实例下分别等于 `client_name` 与 `target_from`。模块、命令、正则与 hook 的 `available_for` / `exclude_from` 由 `akaribot.core.utils.platform_scope` 按 `target_from`、`client_name`、`platform_from`、`platform_name` 四段判分，`platform_from` 为空表示平台未知、判为允许；跨进程反序列化的会话（含升级前入队的旧消息）缺少平台两段时，`refresh_info()` 按已知的 `client_name` 与 `target_from` 补齐。配置侧同理：适配器配置表以 `bot_<平台>` 为基表，实例表名为 `bot_<平台>-<实例 ID>`，`CFGManager` 读取时把基表名解析到当前实例的作用域，模块配置与 `config` 表不参与作用域；实例发现以配置中的 `bot_*` 表为索引，表名去前缀后按第一个 `-` 拆成「适配器 + 实例 ID」，再与该表自己的 `enable` 核对。

推送侧据此归拢：`fetch_union_target_list()` 把一个场景组展开为组内全部平台场景，`group_sessions_by_channel()` 按「场景组 + 消息通道」分组，`pick_channel_heads()` 选出每条通道的队首并把其余场景写入队首的 `next_hops`。`post_message()`、`post_global_message()` 与 `send_direct_message_to_union_target()` 都先经这组方法归拢，同一通道只推送一次；队首发送失败时由 `ServerAPI.post_next_hop` 换用下一跳，全员掉线的通道整条跳过。`send_direct_message_to_union_target()` 的消息参数可以是接受队首会话、返回消息内容的异步工厂，返回 `None` 表示该通道不发送。

### 5.4 命令解析器 (`akaribot.core.builtins.parser`)

#### 模板语法 (`args.py`)

```
<arg>              # 必需参数
[flag <arg>]       # 可选参数（带标志）
{description}      # 描述文本（不参与解析）
...                # 变长参数
{{I18N:key}}       # i18n 描述（双花括号）
```

示例：

```python
"echo <text>"                    # 必需参数
"search <query> [-l <lang>]"     # 可选参数
"choice <items> ..."             # 变长参数
"hello {{I18N:module.help}}"     # i18n 描述
```

模板由 `ArgumentPattern`、`OptionalPattern`、`DescPattern` 组成，整体包在带 `priority` 的 `Template` 中；嵌套深度上限为 `MAX_NEST_DEPTH`（10），越界抛 `InvalidTemplatePattern`。`templates_to_str()` 把模板列表还原为可读文本，纠错与帮助文档共用它。

#### parser() 主函数 (`message.py`)

消息处理核心流程：

```python
async def parser(msg: MessageSession):
    # 0. 刷新会话信息
    await msg.session_info.refresh_info()

    # 1. 入站策略：忽略发送者、同场景其它机器人、受限身份
    ready_result = await _dispatch_stage(HookPoint.SESSION_READY, msg)

    # 2. 分发 SESSION_BEFORE_WAIT 后检查任务队列
    wait_result = await _dispatch_stage(HookPoint.SESSION_BEFORE_WAIT, msg)
    if await SessionTaskManager.check(msg, allow_wait_fallthrough=True):
        return

    # 3. 取该平台/客户端可用的模块，把消息转成可读文本
    modules = ModulesManager.return_modules_list(*platform_fields(msg.session_info))
    msg.trigger_msg = normalize_space(msg.as_display())
    await _dispatch_stage(HookPoint.MESSAGE_NORMALIZED, msg)
    if len(msg.trigger_msg) == 0:
        return

    # 4. 命令前缀匹配
    disable_prefix, in_prefix_list = _get_prefixes(msg)
    if in_prefix_list or disable_prefix:
        command_first_word = await _process_command(msg, modules, disable_prefix, in_prefix_list)
        # 命令路由 → 通道认领 → 执行锁 → 模块匹配
        if command_first_word in modules:
            await _execute_module(msg, modules, command_first_word, identify_str)
        else:
            # 未匹配时请求恢复建议，确认后按最新注册表重解析
            await _try_command_recovery(msg, modules, command_first_word, identify_str)
        return msg

    # 5. 正则匹配
    if not await _confirm_long_regex_message(msg, modules):
        return msg
    await _execute_regex(msg, modules, identify_str)
    return msg
```

主流程在 `finally` 中统一收尾：先 `release_execution_resources()` 释放各等待结果持有的平台上下文，再由持有最终所有权的原始 parser 调用 `ExecutionLockList.remove(msg)`，最后分发 `HookPoint.FINISHED`。

#### parser 入口 hook (`hooks/points.py`)

`HookPoint` 是 parser 与出站生命周期的入口常量，订阅走 `ParserHookExecutor`，按阶段分发并返回类型化结果（`Continue`、`Stop`、`Handled`、`RecoveryProposal`、`RewriteTrigger`）。命令侧入口按序为 `SESSION_READY`（会话信息刷新后）、`SESSION_BEFORE_WAIT`、`MESSAGE_NORMALIZED`（文本规范化后）、`COMMAND_ROUTE`（前缀与别名解析后）、`COMMAND_PREPARE`（命令候选选定后，冷却、临封与模块策略）、`COMMAND_BEFORE_PARSE`（模板解析前，ToS 令牌桶计数）、`COMMAND_BEFORE_EXECUTE`（模板解析后）、`COMMAND_UNMATCHED`（未匹配时给出纠错建议）、`CHANNEL_CLAIM`，以及收尾的 `EXECUTION_FINISHED`、`EXECUTION_ERROR`、`FINISHED`。

正则侧另有 `REGEX_ROUTE`、`REGEX_CANDIDATE`、`REGEX_PREPARE`、`REGEX_BEFORE_EXECUTE`；出站侧为 `OUTGOING_BEFORE_SEND`、`OUTGOING_SENT`、`OUTGOING_FAILED`，由 `dispatch_outgoing_before_send()` 与 `dispatch_outgoing_result()` 分发，可改写待发消息链。公开入口为 `dispatch_parser_hook(point, msg, ...)`。

#### 消息通道 (message channel)

`TargetUnionBind.channel_id` 用来表达「同一个场景组内 `channel_id` 相同的场景 = 现实中的同一个场景」。

- 编号在组内从 1 开始逐个递增（`TargetUnionBind.next_channel_id()`），**默认各占一号，也就是默认谁也不跟谁去重**。
  取用当前会话的通道号直接读 `session_info.target_channel_id`，不要去翻模型内部；需要现实场景级的内存态键时用 `session_info.channel_key`。
- 用户侧由 `~bind channel` 一组命令管理：`~bind channel` 查当前通道与同通道的其它场景，`~bind channel set <channel>` 指定通道号，`~bind channel reset` 归还通道号。跨机器人互认走 `~bind auto` 的握手流程，`channel probe` 与 `channel confirm` 是握手内部命令。
- **命令去重**：`akaribot/modules/core/hooks/routing.py` 订阅 `CHANNEL_CLAIM`，以模块 runtime 状态做抢占式认领。
  认领键是「场景组 ID + 通道号 + 触发文本的 SHA-256」，跨平台的消息 ID 无法互通，判定「同一条消息」靠触发文本 hash 一致加收到时间相差不超过 `CHANNEL_DEDUP_WINDOW`（10 秒）。查表与写入之间不能有 `await`，靠单线程事件循环保证原子性。
- **推送去重**：见 5.3 的多实例小节。
- 另有 `target_data["bots_id"]` 记录彼此的机器人账号，用于屏蔽对方发的消息（见 `TargetUnionInfo.list_peer_bots()`），与消息去重是两件事。

> 测试环境**不走这个 `parser()`**，走的是 `akaribot/testing/mock/parser.py` 的简化版：它不跑入站策略与通道认领，未命中模块或正则时返回 `None`，而不是继续走纠错与默认提示。诊断测试与生产差异时，同时读取主技能直接链接的 `testing.md`。

#### 入口与验证命令

```bash
uv sync --all-extras --dev                                    # 重建环境，与 CI 的 --locked 版本同口径
CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 \
    .venv/bin/python -m akaribot.testing                      # 全量测试（根 tester.py 为兼容层）
CI=1 PYTHONIOENCODING=UTF-8 .venv/bin/python tests/run_one.py \
    packages/modules/akari-bot-module-wiki/tests/test_wiki_markdown.py   # 单入口，路径取包内相对路径
```

`tests/run_one.py` 的第二个位置参数是入口函数名，省略时运行文件中全部 `test_*` 入口。运行测试前须先装齐依赖，否则用例会因缺少可选依赖而报 `OptionalDependencyMissing`。

---

### 12.2 KE 码（消息元素文本表示）

格式为 `[KE:type,param1=value1,param2=value2]`：

```
[KE:plain,text=Hello World]
[KE:markdown,text=**Hello**]
[KE:image,path=https://example.com/img.png]
[KE:audio,path=/path/to/audio.ogg]
[KE:video,path=/path/to/video.mp4]
[KE:url,text=https://example.com,trusted=1]
[KE:i18n,i18nkey=my_module.message.hello,name=World]
[KE:mention,userid=QQ|123456789]
[KE:action_text,text=/help,reference=0]
[KE:button,data=...]
[KE:button_frame,data=...]
```

用于日志、模板字符串、跨进程传递。`MessageChain.to_kecode()` 生成，`match_kecode()` 与 `MessageChain.assign()` 能反向解析混排文本（`"Hello [KE:plain,text=World] !"` → 三个块）。语音元素的 KE 类型为 `audio`（对应 `AudioElement`），视频为 `video`；`text` 参数经 urlencode 编码，因为 KE 码按顶层逗号切分参数、按方括号判定块边界。`FormattedTimeElement` 没有独立 KE 类型，退化为 `[KE:plain,text=...]`；`EmbedElement` 与 `RawElement` 未提供 KE 码表示（`kecode()` 只有占位实现，返回 `None`）。

### 12.3 上下文保持（长任务）

平台上下文（SDK 的 event 对象等）默认在一轮消息处理结束后被清掉。长任务需要显式保持，否则后续 `send_message` 会找不到上下文。

模块里用 `MessageSession` 的方法（跨进程走 JobQueue）：

```python
await msg.hold()
# 长时间运行的任务
await msg.release()
```

适配器进程内部则直接操作 `ContextManager`：

```python
ctx_manager.hold_context(session_info)
ctx_manager.release_context(session_info)
```

保持是可嵌套的计数：`hold_context()` 每次加一，`release_context()` 每次减一，减到零才真正删除上下文。`hold_context()` 在上下文已不存在时抛 `SessionContextUnavailable`，`msg.hold()` 会把远端抛出的同名异常与本地的 `ValueError("Session not found in context")` 一并转成该异常。`msg.sleep(s)` 内部已经处理了释放与重获执行锁，长等待优先用它；等待型方法取得的回复会话由原始 parser 的执行域统一释放，模块无须手动 `release()`。

### 12.4 执行锁（防并发）

```python
# 自动管理，同一身份的命令串行执行。锁的粒度是身份域，不是 target_id
class ExecutionLockList:
    _list: dict[str, frozenset[str]] = {}   # lease token -> 该 lease 覆盖的身份键

    @classmethod
    async def acquire(cls, msg, *, wait=False) -> bool   # 取锁，wait 表示冲突时排队
    @classmethod
    async def is_locked(cls, msg) -> bool                # 按当前 Union 绑定集检查冲突
    @classmethod
    async def reserve(cls, msg, keys) -> bool            # 扩展 lease 身份域（Union 合并用）
    @classmethod
    async def refresh(cls, msg) -> bool                  # 按数据库最新绑定集刷新覆盖范围
    @classmethod
    def add(cls, msg) / def remove(cls, msg)             # 兼容无 I/O 的旧调用点与释放
    @classmethod
    def check(cls, msg) -> bool                          # 无 I/O 的兼容检查
    @classmethod
    def get(cls) -> set[str]                             # 取全部被锁身份（调试用）
    @classmethod
    def state(cls, msg) -> ExecutionState                # 会话的 server-only 执行状态
```

每把锁是带随机 token 的 lease，覆盖该用户的 Union ID、当前物理账号以及 Union 中的全部绑定账号。检查新会话时会重新展开其当前 Union，因此等待期间即使发生合并或解绑，只要新旧身份仍共享任一物理账号，两段执行就不会并发。`add()` 与 `check()` 只使用会话已有身份、不做数据库往返，生产 parser 走 `acquire()` 与 `is_locked()`；`count()` 返回活跃 lease 数，可排除调用方自身。

`wait_*` 取得的回复会话与原命令共享同一个 `ExecutionState`，因而无论模块后续用哪个会话继续等待，操作的都是同一把锁；`ExecutionState.held_contexts` 记录待释放的等待结果。锁是**进程内内存**，server 进程崩溃重启后自动清空。也可通过 `Bot.ExecutionLockList` 访问。

### 12.5 TOS 限流

`akaribot/modules/core/hooks/tos.py` 的 `_msg_counter()` 用令牌桶双层限流，经 `HookPoint.COMMAND_BEFORE_PARSE` 接入：

- 命令级：同一条命令 `TokenBucket(10, 300)` —— 10 次/300 秒
- 全局级：所有命令 `TokenBucket(20, 300)` —— 20 次/300 秒

计数键是 `sender_union_id`（缺失时退回 `sender_id`）。任一桶耗尽即形成业务拒绝：先固定 `Stop`，再尽力完成处罚通知，上报或提示发送失败不会把已确认超限的命令放行。累计警告数达到 `tos_warning_counts`（默认 5）后临时封禁 `tos_temp_ban_time` 秒（默认 300），并通过 `tos_report()` 上报管理员；`tos_report()` 统一交给 `akaribot.core.smtp.send_report`，启用 SMTP 邮件上报时发邮件，未启用时才回传到配置的上报场景。整套机制由 `enable_tos` 配置开关控制，超级用户豁免。

另有一套独立的**群组手动冷却**（`cooldown_time`，存在 `TargetUnionInfo.target_data` 里），由 `akaribot/modules/core/hooks/policies.py` 的 `_check_target_cooldown()` 处理，挂在 `COMMAND_PREPARE` 与 `REGEX_PREPARE` 上，管理员豁免。

### 12.6 错字纠正

`akaribot/modules/core/hooks/typo.py` 的 `suggest_correction()`，用 `rapidfuzz` 逐层模糊匹配：模块名 → 命令 → 选项 → 参数，命中后返回 `RecoveryProposal`，核心恢复协调器再按最新注册表重解析执行；确认环节用 `wait_confirm` 问用户「是不是想输入 xxx」，草稿不跨 120 秒等待持有。

阈值全部可配（`Config(...)`，默认值如下）：

| 配置项 | 默认 | 作用 |
|--------|------|------|
| `typo_check_module_score` | `0.6` | 模块名相似度下限 |
| `typo_check_command_score` | `0.3` | 命令相似度下限 |
| `typo_check_options_score` | `0.3` | 选项相似度下限 |
| `typo_check_args_score` | `0.5` | 参数相似度下限 |
| `typo_check_module_diff_ratio` | `0.5` | 模块名**长度比**下限 |
| `typo_check_args_diff_ratio` | `0.5` | 参数**数量比**下限 |

长度比那两项是为了挡住「短输入误匹配到长命令」（源码注释举的例子是 `~p` → `~decrypt`）：`min_len / max_len < ratio` 就丢弃这个匹配。

用户可以在自己的 `sender_data` 里把 `typo_check` 设成 `False` 关掉这个功能（`~setup` 提供开关）。

---

### 12.8 自定义异常

定义在 `akaribot.core.constants.exceptions`，共 16 个；其中 `SendMessageFailed`、`SessionFinished`、`WaitCancelException`、`AbuseWarning`、`ConfigValueError`、`ExternalException`、`InvalidHelpDocTypeError`、`SessionContextUnavailable`、`NoReportException`、`TestException` 已收录进 `akaribot.core.api`，其余 6 个只能从深路径取用，会被 B8 记为 warn。**注意前三个继承的是 `BaseException` 而不是 `Exception`** —— 它们是控制流信号，不能被业务代码里的 `except Exception` 吞掉：

```python
class SendMessageFailed(BaseException):   """发送消息失败"""
class SessionFinished(BaseException):     """会话完成，终止处理（msg.finish() 抛出）"""
class WaitCancelException(BaseException): """等待被用户取消"""
```

其余 13 个中，`OptionalDependencyMissing` 继承 `ImportError`（让既有的 `except ImportError` 兜底逻辑继续生效），`SessionContextUnavailable` 继承 `ValueError`，其余继承 `Exception`：

| 异常                       | 含义                     |
| -------------------------- | ------------------------ |
| `AbuseWarning`             | 滥用警告（触发 TOS 处理）|
| `ConfigFileNotFound`       | 配置文件不存在           |
| `ConfigOperationError`     | 配置操作失败             |
| `ConfigValueError`         | 配置值非法               |
| `ExternalException`        | 外部服务异常             |
| `OptionalDependencyMissing`| 可选依赖未安装           |
| `InvalidCommandFormatError`| 命令格式非法             |
| `InvalidHelpDocTypeError`  | 帮助文档类型非法         |
| `SessionContextUnavailable`| 平台上下文已不可用       |
| `InvalidTemplatePattern`   | 命令模板语法非法         |
| `NoReportException`        | 不上报的异常             |
| `QueueAlreadyRunning`      | 队列已在运行             |
| `TestException`            | 测试专用                 |

> 在模块里 `try` 包裹含 `await msg.finish()` 的代码时，用 `except Exception` 是安全的（`SessionFinished` 不会被捕获）；但如果写了 `except BaseException` 或裸 `except:`，命令会卡住不返回。

---
