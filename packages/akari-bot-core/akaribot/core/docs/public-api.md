# 公开 API

本文按分类列出 `akaribot.core.api` 导出的主要接口名称与对应用途。

平台适配器另有 `akaribot.core.api.adapters`，收录仅供适配器使用的设施。

```python
from akaribot.core.api import Bot, I18NContext, MessageChain, Plain
```

`__all__` 列出了公开接口的全部名称。新增导出时，必须同时更新 `__all__` 与来源映射。

## 版本与兼容

`akaribot.core.api.__api_version__` 读取 `core.registry.CORE_API_VERSION`。各成员包在 `manifest.toml` 的 `requires_core_api` 中声明兼容范围，官方包统一声明为 `">=1,<2"`。

框架在注册包之前检查该范围。版本不满足要求时，框架拒绝注册该包并记录原因。该包因此不会出现在模块或适配器清单中。

公开接口仅读取静态声明。配置缺失时未能绑定的名称，将在首次访问时重新解析，因此 CLI 与框架可以在配置就绪之前读取 `__api_version__`。模块与适配器的声明方式分别参见[模块开发](module-development.md)与[适配器开发](adapter-development.md)。

## `Bot`

`Bot` 为运行时入口，保存全局状态，并提供跨场景推送与会话获取能力。

### `Bot.MessageSession`

命令处理函数的参数类型。实际对象为当前会话的 `MessageSession`。

### `post_message()`

`Bot.post_message(module_name, message, session_list=None, **kwargs)` 向启用了该模块的场景推送消息。`session_list` 为空时，按模块启用状态自动获取目标场景。

同一条消息通道仅推送一次，其余会话作为发送失败时的备用会话。

### `fetch_target()`

`Bot.fetch_target(...)` 按目标信息读取场景快照，返回 `FetchedSessionInfo`。需要向指定场景主动发送消息时，先调用 `FetchedMessageSession.from_session_info()` 将其转换为会话对象。

### `get_enabled_this_module()`

`Bot.get_enabled_this_module(module_name)` 返回启用了指定模块的场景列表。定时任务缺少消息上下文时，通常先调用它获取目标场景，再调用 `post_message()` 执行推送。

### `Hook.trigger()`

`Bot.Hook.trigger(name, ...)` 调用带名称的 Hook。名称在 `@module.hook(name=...)` 中声明。

## `MessageSession`

`MessageSession` 代表当前会话上下文，消息发送、交互等待、删除、权限检查与执行互斥锁均由此对象提供。

### `send_message()`

发送一条消息并返回 `FinishedSession`。传入纯字符串时自动包装为仅包含 `PlainElement` 的消息链。

默认会引用触发消息，并执行敏感信息检查。参数与失败处理参见[消息 API](message-api.md)。

### `finish()`

发送最终回复并结束当前处理。调用后模块代码不会继续执行，框架会抛出 `SessionFinished`。

### `delete()`

删除触发当前会话的消息。平台不支持删除操作时，按平台能力返回结果或抛出异常。

### `check_bot_state()`

读取机器人在当前场景的权限快照，返回 `BotState`。结果会写入 `SessionInfo.bot_state`，供 `Module.unsupported_bot_permissions()` 检查模块权限。

### `wait_confirm()`

等待用户确认。普通模式按确认词判断，用户回复 `no` 时返回 `False`。`confirm_token` 不为 `None` 时，必须原样回复口令。超时或取消时抛出 `WaitCancelException`。

### `wait_next_message()`

等待当前会话的下一条消息，返回新的 `MessageSession`。命中的消息仍会进入常规 parser。命令消息不会完成等待，等待保持挂起，直到收到非命令消息或超时。

### `wait_reply()`

等待引用当前消息的回复。平台不支持引用时，改用 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示。`all_=True` 时接受任意成员回复。

### `wait_anyone()`

等待场景内任意成员发送消息，返回新的 `MessageSession`。

等待方法默认释放执行锁，返回前重新获取。超时、取消或重新获取失败都抛出 `WaitCancelException`。

## `SessionInfo`

`SessionInfo` 是可跨进程传输的会话快照，不包含活动连接。

主要属性：

- `target_id`、`target_from`：场景标识与平台名。
- `sender_id`、`sender_name`：发送者。
- `client_name`、`bot_id`、`bot_name`：平台客户端与机器人身份。
- `locale`：当前语言。
- `support_*`：平台能力标志。
- `bot_state`：最近一次 `check_bot_state()` 的结果。

字段的具体含义参见[消息 API](message-api.md)与[适配器开发](adapter-development.md)。

## `FetchedMessageSession`

主动获取的会话。用 `FetchedMessageSession.from_session_info()` 创建。`Bot.fetch_target()` 返回的快照可以直接传入。

该对象继承 `MessageSession` 的发送与等待方法，但未包含 `session_info.messages`。调用 `as_display()` 前需要先检查消息列表是否为空。

## `FinishedSession`

已发送消息的封装对象，`send_message()` 返回该对象。

### `assign()`

`FinishedSession.assign(session, message_id)` 用于创建该对象，传入单个消息 ID 时会自动转换为列表。

### `delete()`

删除这条已发送的消息。实际删除操作交给 `PlatformAPI.delete_message`。

## `MessageChain`

`MessageChain` 是多个消息元素组成的消息链，支持拼接、序列化与安全检查。

### `create()`

创建空消息链对象。

### `assign()`

`MessageChain.assign(elements)` 从字符串、元素、元素列表或另一条消息链创建消息链。传入另一条消息链时直接返回该实例，其他输入执行深拷贝。

### `is_safe`

属性。遍历消息元素，检查是否包含敏感信息。发送前默认采用该检查结果。

### `to_str()`

将消息链转换为字符串。设置 `text_only=True` 时仅拼接纯文本，`element_filter` 可限定转换的元素类型，`connector` 指定连接符。

## `I18NMessageChain`

按语言选择消息链。`I18NMessageChain.assign(values)` 的 `values` 以语言代码为键，必须包含 `default`。

发送时按当前会话语言选取对应消息链。无匹配语言时使用 `default`。

## `PlatformMessageChain`

按平台选择消息链。`PlatformMessageChain.assign(values)` 的 `values` 以平台名称为键，且必须包含 `default` 项。

选择顺序是 `PlatformMessageChain` > `I18NMessageChain` > `MessageChain`。

## `MessageNodes`

`MessageNodes` 为合并转发消息的节点列表。`MessageNodes.assign(values, name=None)` 将多条 `MessageChain` 组合为节点列表，`name` 省略时自动生成。

`is_safe` 属性检查所有节点。平台未声明 `support_handle_message_nodes` 能力时，框架将节点渲染为图片后发送。

## 消息元素

`Plain`、`Image`、`Audio`、`Video`、`Markdown`、`Embed`、`EmbedField`、`Url`、`Mention`、`ActionText`、`Button`、`ButtonFrame`、`FormattedTime`、`I18NContext` 与 `Raw` 是构造消息的便捷类。对应的 `*Element` 类是可序列化的元素模型，`BaseElement` 是元素基类。

`I18NContext` 的参数值支持字符串、数字与消息元素。按钮的排布用 `ButtonPermission`、`ButtonRows`、`arrange_buttons()` 与 `build_button_rows()`。

### `get_message_chain()`

将平台消息链或多语言消息链转换为当前会话可用的 `MessageChain`。

### `match_kecode()`、`escape_special_char()`

前者用于解析 KE 码，后者用于转义 KE 码的结构字符。元素类型与参数规则参见[占位符](placeholders.md)。

## `module()`

`module(name, ...)` 声明模块并返回 `Bind.Module`。后续的命令、正则、定时任务、Hook 与事件均挂载于该对象上。

## `Bind.Module`

### `command()`

`command(template, ...)` 绑定命令。模板里的参数会映射到处理函数的同名参数。

### `regex()`

`regex(pattern, mode="M", ...)` 绑定正则。`mode="M"` 从消息开头匹配，`mode="A"` 在消息内查找。

### `schedule()`

`schedule(trigger)` 绑定定时任务。触发器支持 `CronTrigger`、`IntervalTrigger`、`DateTrigger`、`AndTrigger` 与 `OrTrigger`。

### `hook()`

`hook(point=..., priority=..., name=...)` 绑定 Hook。`priority` 数值越小越优先执行。带名称的 Hook 由 `Bot.Hook.trigger()` 触发调用。

### `event()`

`event(event_name, ...)` 绑定平台事件。事件回调的参数是 `EventInfo`。

## `CommandParser`

`CommandParser` 按模块的命令模板解析输入，并生成帮助文档。

核心入口为 `return_formatted_help_doc(locale=None)`。该方法按当前用户权限过滤命令，返回可直接发送的帮助文本。

## `ModulesManager`

`ModulesManager` 维护模块注册、别名、Hook、事件与依赖关系。

- `load_module(module_name)`：加载一个模块，注册它的命令、正则、计划任务与 Hook。
- `reload_module(module_name)`：重新加载模块，并刷新命令、Hook 与配置字段。
- `get_module_and_alias_first_words(module_or_alias)`：返回模块名与别名对应的首词。

## `ModuleRuntimeManager`

`ModuleRuntimeManager` 管理运行时状态。

- `get_or_create(module_name)`：获取模块的 `ModuleRuntime`，没有时创建。
- `ModuleRuntime.get()`：读取模块实例。
- `ModuleRuntime.get_state()`：读取运行状态。

`ModuleStatus` 是记录模块加载状态的数据模型。

## `HookPoint` 与返回值

`HookPoint` 列出命令、正则、会话与执行生命周期的 Hook 位置。

Hook 可以返回：

- `Handled`：表示本次 Hook 已处理。
- `Stop`：终止后续处理，可附带消息与作用范围。
- `StopScope`：`Stop` 的作用范围。
- `RecoveryProposal`：向调用方提出恢复建议。

具体触发点与执行顺序参见[模块开发](module-development.md)。

## `CFGManager`

`CFGManager` 负责配置文件的读写操作。模板类在导入阶段确定各字段的读取规则，用户配置保存在 `config/`，默认配置层保存在 `config/global/`。

### `load()`

读取全局层与用户层，合并成当前配置。

### `save()`

仅将发生变动的用户配置写回用户层，不修改全局默认层。

### `get()`

按字段名读取配置值。值类型不符合模板声明时输出警告，并返回原值。

### `delete()`

删除用户层中的配置键。删除后，该键恢复为全局默认值。

### `edit_write()`、`edit_delete()`

交互式编辑写入与删除接口。仅在明确授权的范围内使用，供 `~config` 与启动阶段密钥初始化流程调用。

`CoreConfig`、`BaseConfig` 与 `CoreSecretConfig` 是配置模板类。`on_module_config()` 与 `on_bot_config()` 用来声明模块配置与适配器配置。

## `DBModel`

`DBModel` 为业务数据模型的基类。

- `get_by_target_id()`：按场景 ID 读取记录，可指定是否创建。
- `get_by_sender_id()`：按发送者 ID 读取记录，可指定是否创建。

模块自有模型继承 `DBModel`，迁移用 `MigrationContext` 与 `fetch_module_db()`。

## `SenderUnionInfo`、`TargetUnionInfo` 与绑定表

`SenderUnionInfo` 保存发送者 Union 数据，`TargetUnionInfo` 保存场景 Union 数据。`SenderUnionBind` 与 `TargetUnionBind` 保存平台 ID 至 Union 的映射。

场景数据包括 `muted`、`locale`、`modules`、`custom_admins`、`banned_users` 与 `target_data`。

`StoredData`、`ModuleStatus`、`AnalyticsData`、`JobQueuesTable` 是 core 自带的数据模型。

### `UNION_SCOPE_SENDER`、`UNION_SCOPE_TARGET`

指定 union 的作用域。

### `union_mutation()`

跨表写入同一 Union 时，先调用该接口，再在 `default` 事务中排他锁定 Union 行。

### `get_model_names()`、`get_model_fields()`

枚举当前数据库的数据表与字段。`~database` 命令使用上述接口生成帮助文本，参见[数据库](database.md)。

## `ServerAPI`

`ServerAPI` 是模块与 Server 进程之间的 RPC 接口约定。

常见方法：

- `receive_message()`、`receive_event()`：将消息或平台事件交由 Server 处理。
- `trigger_hook()`：触发带名称的 Hook。
- `direct_message()`：直接向会话发送消息。
- `report_error()`：上报错误。
- `get_bot_version()`、`get_web_render_status()`、`get_runtime_stats()`：读取运行状态。

直接使用 `await` 将等待远程执行结果，调用 `.submit()` 则仅等待后端接收任务。

## `PlatformAPI`

`PlatformAPI` 是 Server 与平台进程之间的 RPC 接口约定。

消息发送与操作：

- `send_message()`、`send_private_msg()`、`post_message()`。
- `delete_message()`、`restrict_member()`、`unrestrict_member()`、`kick_member()`、`ban_member()`、`unban_member()`。

查询与权限：

- `check_native_permission()`、`check_bot_state()`。
- `grant_permission_group()`、`revoke_permission_group()`。

交互与扩展：

- `add_reaction()`、`remove_reaction()`、`start_typing()`、`end_typing()`、`error_signal()`。
- `hold_context()`、`release_context()`。
- `call_onebot_api()`：调用平台明确支持的 OneBot 扩展。

## `RpcError`

RPC 失败的基类。具体子类区分不可达、超时、取消、方法不存在与协议错误。

## `web_render`

`web_render` 是渲染服务单例。

- `init_web_render()`：启动渲染服务。
- `check_web_render_status()`：检查渲染服务状态。
- `close_web_render()`：关闭渲染服务。

## 截图参数

截图参数用以下类描述：

- `PageScreenshotOptions`：整页截图参数。
- `SectionScreenshotOptions`：元素选择器与区域截图参数。
- `SourceOptions`：网页源码抓取参数。
- `RawOptions`：直接传递原始内容。

## 图像辅助

- `ImageTable`：图片表格的数据。
- `image_table_render()`：将表格渲染为图片。
- `msgchain2image()`：将消息链渲染为图片。
- `svg_render()`：将 SVG 渲染为图片元素。

服务配置与降级参见 [WebRender](webrender.md)。

## `Logger`

`Logger` 提供分级日志。业务代码通过它输出调试、信息、警告与错误级别的日志，模块不需要自己配置日志器。

## `Locale`

`Locale` 负责当前语言的文案。`Locale.t()` 用于获取文案，`Locale.t_str()` 处理已经是文案的字符串。`lang_list` 是可用语言表。

## `Info`

`Info` 提供实例与平台信息。

- `Info.resolve_client_name(platform_name)`：有实例 ID 时返回 `平台-实例ID`。
- `Info.instance_id`：当前实例 ID。

## `Secret`

`Secret` 标记配置字段为敏感密钥。携带该标记的字段写入密钥配置表，不进入普通配置表。

## `Random`、`SecureRandom`

`Random` 提供可复现的随机数。`SecureRandom` 使用安全随机源，适合生成令牌、验证码一类的值。

## `CoolDown`、`TokenBucket`

`CoolDown` 控制同一键的触发间隔。`TokenBucket` 按容量与速率限制调用次数。

## `ExpiringTempDict`

带过期时间的临时字典。写入时指定有效期，读取时自动清理过期项。

## HTTP 与文本工具

HTTP：

- `get_url()`、`post_url()`、`request_url()`：发送请求。
- `download()`：下载文件。

文本与数据：

- `chunk_list()`：按长度切分列表。
- `truncate_text()`：截断文本。
- `converter`：结构化数据转换。

## URL 审计

- `GlobalURLAllowlist`、`GlobalURLBlocklist`：全局 URL 允许与阻止名单。
- `URLRule`：单条 URL 规则。
- `evaluate_url_policy()`：按规则判断 URL 是否放行。

## 运维

- `run_sys_command()`：执行系统命令。
- `restart`：重启入口。
- `send_email()`：发送邮件。

## 适配器接口

`akaribot.core.api.adapters` 提供适配器专用的名称。

### `ContextManager`

`ContextManager` 为平台上下文管理器，负责实现消息发送、删除、禁言、权限组、表情回应与输入中状态等平台操作。

### `PlatformAPI`

适配器端的 RPC 接口。`context_method()` 将 `ContextManager` 的方法绑定为支持远程调用的操作。

### `Features`

`Features` 声明平台能力。`client_init()` 注册节点时，将对应能力标志写入 `capabilities`。

### `BotState`

`BotState` 为机器人在当前场景的权限快照。`can_*` 字段指示是否允许执行对应操作，`permissions` 保存平台返回的权限集合。

### `client_init()`、`client_cleanup()`

`client_init()` 初始化平台客户端并注册能力。`client_cleanup()` 清理连接与临时资源。

### `check_queue()`

检查平台进程的队列状态，供启动与健康检查使用。

### `Temp`、`S3Storage`、`S3StorageAPI`

`Temp` 提供临时文件目录。`S3Storage` 与 `S3StorageAPI` 提供对象存储读写。

### 按钮与媒体辅助

按钮：

- `BUTTON_TOKEN_PREFIX`、`RegisteredButton`、`ButtonState`、`ButtonConsumeResult`。
- `consume_button()`、`register_button_rows()`。

媒体：

- `compress_image()`、`compress_media_chain()`。
- `resolve_media_path()`、`image_split()`。

两个公开接口共有的名称（`Bot`、`SessionInfo` 与消息元素等）仅在 `akaribot.core.api` 中导出。适配器同时依赖这两个接口。适配器入口、能力声明与上下文管理器的实现要求参见[适配器开发](adapter-development.md)。

## 完整导出清单

类、函数、常量、方法签名与参数的完整列表参见[完整 API 导出清单](api-reference.md)。本页仅保留分类说明和常用接口。
