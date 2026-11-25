# 核心运行时

本页说明核心运行时的架构定位、依赖关系与进程拓扑。

`akaribot.core` 为 AkariBot 的核心运行时框架，负责提供公共 API 与底层基础设施，由 `akari-bot-core` 包提供。该包同时包含内置功能模块 `akaribot.modules.core`，相关说明参见[内置模块](../../modules/core/docs/index.md)。

## 定位

`akaribot.core` 提供守护进程入口、Server 进程、消息解析和会话模型，同时定义平台进程与 Server 共用的接口。包发现、配置、数据库、计划任务、JobQueue 和本地化数据均由该核心包管理。

外部功能模块与平台适配器均通过标准公共 API 接入 core。模块导入 `akaribot.core.api`，适配器额外导入 `akaribot.core.api.adapters`。内置核心模块同样严格遵循该分层调用规范。

- `akaribot`、`akaribot.modules`、`akaribot.adapters` 属于 [PEP 420](https://peps.python.org/pep-0420/) 命名空间目录，不包含 `__init__.py`。
- `akaribot.core` 是常规包。
- `CORE_API_VERSION` 定义公共 API 的版本号，运行时通过 `__api_version__` 导出该版本号。
- 模块包在 `manifest.toml` 的 `requires_core_api` 中声明支持的版本范围。

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
| `full` | 上述三项以及品牌与表情资源包 |

## 进程模型概览

| 进程 | 职责 |
| --- | --- |
| BotDaemon | 获取防止实例重复启动的锁文件，执行 pre-init，启动并监控子进程 |
| pre-init | 唯一可写入配置的进程，补充缺失的配置项、创建数据表、执行迁移 |
| 平台进程 | 对应每个适配器实例，持有平台 SDK 与上下文 |
| Server | 解析消息、执行模块、运行计划任务 |
| jobqueue-hub | WebSocket 后端的内置 Hub，可选 |

实例根目录由 `AKARI_INSTANCE_DIR` 指定，未设置时使用进程的当前目录。配置目录可以通过 `AKARI_CONFIG_PATH` 单独指定。详情参见[架构](architecture.md)。

## 文档导航

| 页面 | 内容 |
| --- | --- |
| [架构](architecture.md) | 代码结构、进程拓扑、启动与重启、消息收发链路、计划任务 |
| [开发流程](development-workflow.md) | 环境、日常命令、检查项、代码风格、分支与提交、文档工具链 |
| [JobQueue](queue.md) | 后端选择、节点注册、RPC 与信号、超时与关闭 |
| [配置](config.md) | 配置模板、表布局、字段注释、只读约束 |
| [数据库](database.md) | 双连接、模型、union 数据、迁移 |
| [WebRender](webrender.md) | 渲染服务配置、运行模式、启动与降级 |
| [模块开发](module-development.md) | 模块、命令、权限、配置、hook、i18n |
| [消息 API](message-api.md) | `MessageSession`、等待接口、消息链与消息元素 |
| [权限](permissions.md) | 角色、模块与命令级权限、模块授权、机器人权限 |
| [适配器开发](adapter-development.md) | 适配器入口、特性声明、上下文管理器 |
| [公共 API](public-api.md) | 模块与适配器可依赖的公开 API 与版本要求 |
| [本地化](i18n.md) | `I18NContext`、语言文件与占位符规则 |
| [占位符](placeholders.md) | KE 码、I18N 标记、AT 码的语法与转义 |
| [常见问题](faq.md) | 帮助、模块启用、权限、更新、贡献与许可 |
