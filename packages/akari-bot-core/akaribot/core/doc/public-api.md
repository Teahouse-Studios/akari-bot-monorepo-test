# 公共 API

`akaribot.core.api` 是模块与适配器唯一应依赖的公共面。core 内部模块可以移动或改名，门面承诺的名字
保持不变；直接 import `akaribot.core.builtins.*` 这类深路径不属于公共契约。平台适配器另有
`akaribot.core.api.adapters`，收录只有适配器使用的设施。

```python
from akaribot.core.api import Bot, I18NContext, MessageChain, Plain
```

门面的 `__all__` 是完整承诺清单。本页按用途介绍常用名字，不逐项罗列；新增导出须同时更新
`__all__` 与来源映射。

## 版本与兼容

`akaribot.core.api.__api_version__` 取 `core.registry.CORE_API_VERSION`，当前为 `1`。包在
`manifest.toml` 的 `requires_core_api` 声明兼容区间，官方包写 `">=1,<2"`。发现层在注册前校验该
区间，不满足的包被拒绝并记录原因，不进入模块或适配器清单。

门面在导入期不读取实例配置；依赖配置的名字在首次访问时惰性导入，因此 CLI 与发现层可以在配置
就绪之前读取 `__api_version__`。模块与适配器的声明方式分别见[模块开发](module-development.md)与
[适配器开发](adapter-development.md)。

## 会话与消息

| 名字 | 用途 |
| --- | --- |
| `Bot` | 运行时入口与全局状态；`Bot.MessageSession` 是命令函数的入参类型 |
| `MessageSession` | 当前会话：发送、等待、删除、权限判断与执行锁 |
| `SessionInfo` | 可跨进程传输的会话快照，含目标、发送者、平台能力与语言 |
| `FetchedMessageSession`、`FinishedSession` | 主动抓取的会话与已发送消息的句柄 |
| `SessionFinished`、`WaitCancelException` | `finish()` 终止与等待取消的异常 |

发送与等待方法的完整参数见[消息 API](message-api.md)；`MessageSession` 的常用入口是
`send_message()`、`finish()`、`wait_confirm()`、`wait_next_message()`、`wait_reply()` 与
`wait_anyone()`。

## 消息元素与消息链

`Plain`、`Image`、`Audio`、`Video`、`Markdown`、`Embed`、`EmbedField`、`Url`、`Mention`、
`ActionText`、`Button`、`ButtonFrame`、`FormattedTime`、`I18NContext` 与 `Raw` 是构造消息的
便捷类；对应的 `*Element` 类是可序列化的元素模型。`BaseElement` 是元素基类。

| 名字 | 用途 |
| --- | --- |
| `MessageChain` | 多个元素组成的消息链，支持拼接、序列化与安全检查 |
| `I18NMessageChain`、`PlatformMessageChain` | 按语言或平台选择消息链，须含 `default` 键 |
| `MessageNodes` | 合并转发消息节点 |
| `Chainable` | 可作为发送入参的类型联合 |
| `get_message_chain()` | 把平台链或多语言链折算为当前会话可用的消息链 |
| `match_kecode()`、`escape_special_char()` | KE 码解析与结构字符转义 |

元素可以互相嵌套，`I18NContext` 的参数值支持字符串、数字与消息元素。按钮用 `ButtonPermission`、
`ButtonRows`、`arrange_buttons()` 与 `build_button_rows()` 布局。

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

`@module.hook()` 的 `point` 取 `HookPoint` 常量，`priority` 升序执行；`@module.event()` 绑定平台
事件。具名 hook 由 `Bot.Hook.trigger("名称", ...)` 调用。hook 的完整语义见[模块开发](module-development.md)。

## 配置与数据库

配置面提供 `CoreConfig`、`BaseConfig`、`CoreSecretConfig` 与 `CFGManager`，以及声明模块配置的
`on_module_config()`、`on_bot_config()`。字段在模板类中声明，读取经元类按属性名取值；表布局与
只读约束见[配置](config.md)。

数据库面提供 `DBModel`、`SenderUnionInfo`、`TargetUnionInfo`、`SenderUnionBind`、
`TargetUnionBind`、`StoredData`、`ModuleStatus`、`AnalyticsData`、`JobQueuesTable` 等核心模型，
以及 `UNION_SCOPE_SENDER`、`UNION_SCOPE_TARGET`、`union_mutation()` 等 union 数据设施。
模块自有模型继承 `DBModel`，迁移用 `MigrationContext` 与 `fetch_module_db()`；字段与表清单可用
`get_model_fields()`、`get_model_names()` 查询。详见[数据库](database.md)。

## JobQueue 与跨进程

JobQueue 没有单独的模块门面类。业务代码通过共享 RPC 契约声明跨进程动作：

- `ServerAPI`：模块面导出，调用 Server 进程的模块、会话与 WebRender 控制接口。
- `PlatformAPI`：从 `akaribot.core.queue.contracts` 导入，调用平台发送、管理、表情等动作。
- `RpcError`：RPC 失败的基类；具体子类区分不可达、超时、取消、方法不存在与协议错误。

直接 `await` 等待远端结果，`.submit()` 只等待投递。后端选择、Peer 注册、超时与关闭流程见
[JobQueue](queue.md)；模块不应直接读写 `job_queues` 表。

## WebRender 与图像

`web_render` 是渲染服务单例，`init_web_render()`、`check_web_render_status()` 与
`close_web_render()` 管理其生命周期。截图参数用 `PageScreenshotOptions`、
`ElementScreenshotOptions`、`SectionScreenshotOptions`、`SourceOptions`、`RawOptions`、
`LegacyScreenshotOptions` 与 `ReplaceElementScreenshotOptions` 描述；图像辅助有 `ImageTable`、
`image_table_render()`、`msgchain2image()` 与 `svg_render()`。服务配置与降级见 [WebRender](webrender.md)。

## 工具

工具面包括 `Logger`、`Locale`、`lang_list`、`Alive`、`Info`、`Secret`、`Random`、`SecureRandom`、
`CoolDown`、`TokenBucket`、`ExpiringTempDict`，HTTP 的 `get_url()`、`post_url()`、`request_url()`、
`download()`，文本与数据的 `chunk_list()`、`truncate_text()`、`parse_time_string()`、`converter`，
URL 审计的 `GlobalURLAllowlist`、`GlobalURLBlocklist`、`URLRule`、`evaluate_url_policy()`，以及
`run_sys_command()`、`restart`、`send_email()` 等运维设施。

## 适配器面

`akaribot.core.api.adapters` 提供 `ContextManager`、`PlatformAPI`、`Features`、`BotState`、
`client_init()`、`client_cleanup()`、`check_queue()`、`Temp` 与 `S3Storage`／`S3StorageAPI`。
按钮与媒体辅助包括 `BUTTON_TOKEN_PREFIX`、`RegisteredButton`、`ButtonState`、
`ButtonConsumeResult`、`consume_button()`、`register_button_rows()`、`compress_image()`、
`compress_media_chain()`、`resolve_media_path()` 与 `image_split()`。

两个门面共享的名字（`Bot`、`SessionInfo` 与消息元素等）只在 `akaribot.core.api`
导出；适配器同时依赖两个门面。适配器入口、能力声明与上下文管理器的实现要求见
[适配器开发](adapter-development.md)。
