# 核心运行时

`akaribot.core` 是 AkariBot 的运行时与公共设施，随 `akari-bot-core` 分发。同一分发还包含内置模块包
`akaribot.modules.core`，其文档见[内置模块](../../modules/core/doc/index.md)。

## 定位

- 提供守护进程入口、Server 进程、消息解析、会话模型与平台进程的公共契约。
- 提供模块与适配器依赖的公共 API 门面：模块导入 `akaribot.core.api`，适配器额外导入
  `akaribot.core.api.adapters`。
- 维护包发现（entry points）、配置、数据库、计划任务、JobQueue 与本地化快照。
- 内置模块本身只依赖公共 API，与外部模块包地位相同。

`akaribot`、`akaribot.modules`、`akaribot.adapters` 是 PEP 420 命名空间目录；`akaribot.core` 是常规包。
公共 API 版本常量是 `CORE_API_VERSION = 1`，门面以 `__api_version__` 暴露，模块包在 `manifest.toml`
的 `requires_core_api` 中声明兼容区间。

## 依赖关系

| 依赖 | 用途 |
| --- | --- |
| `akari-bot-i18n` | `Locale`、文案快照与术语校验 |
| `akari-bot-webrender` | 网页与元素截图渲染 |
| `tortoise-orm` | ORM、连接管理与迁移执行 |
| `APScheduler` | 模块与核心计划任务 |
| `fastapi`、`uvicorn` | 内置 WebSocket Hub 与 HTTP 服务 |
| `httpx`、`httpx-ws` | 出站请求与 WebSocket 客户端 |

可选依赖以 extra 提供：

| extra | 内容 |
| --- | --- |
| `s3` | `boto3`，对象存储 |
| `mysql` | `asyncmy` 驱动 |
| `image`、`chart` | `matplotlib`，统计图表 |
| `full` | 上述三项加品牌与表情资源包 |

## 进程模型概览

| 进程 | 职责 |
| --- | --- |
| BotDaemon | 取实例锁、执行 pre-init、派生并监督子进程 |
| pre-init | 唯一可写配置的进程，补写配置、建表、执行迁移 |
| 平台进程 | 每个适配器实例一个，持有平台 SDK 与上下文 |
| Server | 解析消息、执行模块、运行计划任务 |
| jobqueue-hub | WebSocket 后端的内置 Hub，可选 |

实例根由 `AKARI_INSTANCE_DIR` 决定，未设置时取进程当前目录。配置目录可用 `AKARI_CONFIG_PATH` 单独指定。
详情见[架构](architecture.md)。

## 文档导航

| 页面 | 内容 |
| --- | --- |
| [架构](architecture.md) | 进程拓扑、启动与重启、消息收发链路、计划任务 |
| [JobQueue](queue.md) | 后端选择、Peer 注册、RPC 与信号、超时与关闭 |
| [配置](config.md) | 配置模板、表布局、字段注释、只读约束 |
| [数据库](database.md) | 双连接、模型、union 数据、迁移 |
| [WebRender](webrender.md) | 渲染服务配置、运行模式、启动与降级 |
| [模块开发](module-development.md) | 模块、命令、权限、配置、hook、i18n |
| [消息 API](message-api.md) | `MessageSession`、等待接口、消息链与消息元素 |
| [权限](permissions.md) | 角色、模块与命令级权限、模块授权、机器人权限 |
| [适配器开发](adapter-development.md) | 适配器入口、特性声明、上下文管理器 |
| [公共 API](public-api.md) | 模块与适配器可依赖的 API 面与版本约束 |
| [本地化](i18n.md) | `I18NContext`、语言文件与占位符规则 |
| [占位符](placeholders.md) | KE 码、I18N 标记、AT 码的语法与转义 |
| [常见问题](faq.md) | 帮助、模块启用、权限、更新、贡献与许可 |
