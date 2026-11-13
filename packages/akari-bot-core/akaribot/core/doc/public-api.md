# 公共 API

本文整理了 `akaribot.core.api` 导出的名字与用途。

`akaribot.core.api` 是模块与适配器唯一应依赖的公开接口。core 内部模块可以移动或改名，公开接口导出的名字保持不变。直接 import `akaribot.core.builtins.*` 这类内部路径不属于公开接口。

平台适配器另有 `akaribot.core.api.adapters`，收录只有适配器使用的设施。

```python
from akaribot.core.api import Bot, I18NContext, MessageChain, Plain
```

`__all__` 列出了公开接口的全部名字。新增导出时，须同时更新 `__all__` 与来源映射。

## 版本与兼容

`akaribot.core.api.__api_version__` 取 `core.registry.CORE_API_VERSION`，当前为 `1`。各包在 `manifest.toml` 的 `requires_core_api` 中声明兼容范围，官方包写 `">=1,<2"`。框架在注册包之前检查这个范围。不满足要求的包会被拒绝，不进入模块或适配器清单，框架会记录原因。

公开接口在导入时不会读取实例配置。只有依赖配置的名字会在首次访问时载入，因此 CLI 与框架可以在配置就绪之前读取 `__api_version__`。模块与适配器的声明方式分别见[模块开发](module-development.md)与 [适配器开发](adapter-development.md)。

## 会话与消息

| 名字 | 用途 |
| --- | --- |
| `Bot` | 运行时入口与全局状态。`Bot.MessageSession` 是命令函数的入参类型 |
| `MessageSession` | 当前会话：发送、等待、删除、权限判断与执行锁 |
| `SessionInfo` | 可跨进程传输的会话快照，含目标、发送者、平台能力与语言 |
| `FetchedMessageSession`、`FinishedSession` | 主动抓取的会话与已发送消息的句柄 |
| `SessionFinished`、`WaitCancelException` | `finish()` 终止与等待取消的异常 |

发送与等待方法的完整参数见[消息 API](message-api.md)。`MessageSession` 的常用入口是 `send_message()`、`finish()`、`wait_confirm()`、`wait_next_message()`、`wait_reply()` 与 `wait_anyone()`。

## 消息元素与消息链

`Plain`、`Image`、`Audio`、`Video`、`Markdown`、`Embed`、`EmbedField`、`Url`、`Mention`、`ActionText`、`Button`、`ButtonFrame`、`FormattedTime`、`I18NContext` 与 `Raw` 是构造消息的便捷类，对应的 `*Element` 类是可序列化的元素模型。`BaseElement` 是元素基类。

| 名字 | 用途 |
| --- | --- |
| `MessageChain` | 多个元素组成的消息链，支持拼接、序列化与安全检查 |
| `I18NMessageChain`、`PlatformMessageChain` | 按语言或平台选择消息链，须含 `default` 键 |
| `MessageNodes` | 合并转发消息节点 |
| `Chainable` | 可作为发送入参的类型联合 |
| `get_message_chain()` | 把平台链或多语言链折算为当前会话可用的消息链 |
| `match_kecode()`、`escape_special_char()` | KE 码解析与结构字符转义 |

元素可以互相嵌套，`I18NContext` 的参数值支持字符串、数字与消息元素。按钮的排布用 `ButtonPermission`、`ButtonRows`、`arrange_buttons()` 与 `build_button_rows()`。

## 模块与 Hook

| 名字 | 用途 |
| --- | --- |
| `module()` | 声明模块，返回可绑定命令、正则、计划任务与 hook 的对象 |
| `Bind.Module` | `module()` 的返回类型，提供 `command()`、`regex()`、`schedule()`、`hook()`、`event()` |
| `Module`、`CommandMeta` | 模块与命令的元数据 |
| `CommandParser` | 解析命令模板并生成帮助文档 |
| `ModulesManager`、`ModuleRuntimeManager`、`ModuleStatus` | 模块注册、运行期状态与装载状态 |
| `HookPoint` | 命令、正则、会话与执行生命周期的 hook 位置 |
| `Handled`、`Stop`、`StopScope`、`RecoveryProposal` | hook 返回值：标记已处理、终止后续处理或提出恢复建议 |

`@module.hook()` 的 `point` 取 `HookPoint` 常量，`priority` 数值小的先执行。`@module.event()` 绑定平台事件。带名称的 Hook 由 `Bot.Hook.trigger("名称", ...)` 调用，完整语义见[模块开发](module-development.md)。

## 配置与数据库

配置相关的名字有 `CoreConfig`、`BaseConfig`、`CoreSecretConfig` 与 `CFGManager`，以及声明模块配置的 `on_module_config()`、`on_bot_config()`。字段在模板类中声明，读取时由元类按属性名取值。表布局与只读限制见[配置](config.md)。

数据库相关的名字有 `DBModel`、`SenderUnionInfo`、`TargetUnionInfo`、`SenderUnionBind`、`TargetUnionBind`、`StoredData`、`ModuleStatus`、`AnalyticsData`、`JobQueuesTable` 等核心模型，以及 `UNION_SCOPE_SENDER`、`UNION_SCOPE_TARGET`、`union_mutation()` 等 union 数据工具。模块自有的模型继承 `DBModel`，迁移用 `MigrationContext` 与 `fetch_module_db()`。字段与表清单可用 `get_model_fields()`、`get_model_names()` 查询，详见[数据库](database.md)。

## JobQueue 与跨进程

JobQueue 没有单独的公开接口类。业务代码通过共享的 RPC 契约声明跨进程动作：

- `ServerAPI`：从模块公开接口导出，调用 Server 进程的模块、会话与 WebRender 控制接口。
- `PlatformAPI`：从 `akaribot.core.queue.contracts` 导入，调用平台发送、管理、表情等动作。
- `RpcError`：RPC 失败的基类。具体子类区分不可达、超时、取消、方法不存在与协议错误。

直接 `await` 会等待远程结果，`.submit()` 只等到后端接收任务为止。后端选择、节点注册、超时与关闭流程见 [JobQueue](queue.md)。模块不应直接读写 `job_queues` 表。

## WebRender 与图像

`web_render` 是渲染服务单例，`init_web_render()`、`check_web_render_status()` 与 `close_web_render()` 管理其生命周期。截图参数用 `PageScreenshotOptions`、`ElementScreenshotOptions`、`SectionScreenshotOptions`、`SourceOptions`、`RawOptions`、`LegacyScreenshotOptions` 与 `ReplaceElementScreenshotOptions` 描述。图像辅助有 `ImageTable`、`image_table_render()`、`msgchain2image()` 与 `svg_render()`。服务配置与降级见 [WebRender](webrender.md)。

## 工具

工具相关的名字有 `Logger`、`Locale`、`lang_list`、`Alive`、`Info`、`Secret`、`Random`、`SecureRandom`、`CoolDown`、`TokenBucket` 与 `ExpiringTempDict`。HTTP 相关的是 `get_url()`、`post_url()`、`request_url()` 与 `download()`。

文本与数据相关的是 `chunk_list()`、`truncate_text()`、`parse_time_string()` 与 `converter`。URL 审计相关的是 `GlobalURLAllowlist`、`GlobalURLBlocklist`、`URLRule` 与 `evaluate_url_policy()`。运维相关的是 `run_sys_command()`、`restart`、`send_email()`。

## 适配器面

`akaribot.core.api.adapters` 提供 `ContextManager`、`PlatformAPI`、`Features`、`BotState`、`client_init()`、`client_cleanup()`、`check_queue()`、`Temp` 与 `S3Storage`／`S3StorageAPI`。按钮与媒体辅助包括 `BUTTON_TOKEN_PREFIX`、`RegisteredButton`、`ButtonState`、`ButtonConsumeResult`、`consume_button()`、`register_button_rows()`、`compress_image()`、`compress_media_chain()`、`resolve_media_path()` 与 `image_split()`。

两个公开接口共有的名字（`Bot`、`SessionInfo` 与消息元素等）只在 `akaribot.core.api` 导出。适配器同时依赖这两个接口。适配器入口、能力声明与上下文管理器的实现要求见 [适配器开发](adapter-development.md)。
