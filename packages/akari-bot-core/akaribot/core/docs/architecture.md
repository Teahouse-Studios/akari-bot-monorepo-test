# 架构

本文介绍 AkariBot 实例的内部结构。

## 介绍

AkariBot 采用模块化多包架构。core 提供运行时环境与基础公共设施，内置模块、外部模块及平台适配器均作为独立成员包维护。

实例启动时，守护进程负责启动并监控子进程。各子进程分别承担配置初始化、平台连接、消息处理与计划任务调度。

## 代码结构

```text
packages/
  akari-bot-core/       akaribot.core 与内置模块 akaribot.modules.core
  akari-bot-testing/    akaribot.testing
  akari-bot-cli/        akaribot.cli
  akari-bot-html2text/  内嵌的 html2text 副本
  akari-bot-assets-*/   字体、表情和品牌资源，分别单独打包
  modules/…             外部模块，导入名 akaribot.modules.<名>
  adapters/…            平台适配器，导入名 akaribot.adapters.<名>
```

补充说明：

- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，不带 `__init__.py`。查找包时以 `pyproject.toml` 中声明的入口为准，仅在入口缺失时才扫描目录。
- 执行 `akaribot <子命令>` 时，命令行工具（CLI）通过子进程调用 `python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc,data,docs}`。
- 仓库根目录保留兼容导入入口。`bot.py`、`tester.py` 通过 `sys.modules` 把原有模块名称映射至新实现。`core/database/update.py` 仅负责将历史版本遗留的升级操作交给当前实现处理。

## 进程拓扑

| 进程 | 启动方式 | 职责 |
| --- | --- | --- |
| BotDaemon | `python -m akaribot.core.entrypoints.run` | 检查同一实例是否已经启动，执行 pre-init，启动并监控子进程 |
| pre-init | 守护进程以 `spawn`（Windows、macOS）或 `forkserver` 启动 | 补充缺失的配置项，创建数据表，执行数据库迁移 |
| 平台进程 | 每个适配器实例对应一个进程，进程名称为 `client_name` | 维护平台 SDK 连接，保存消息上下文和按钮状态 |
| Server | 进程名称为 `server` | 解析消息，执行模块，运行计划任务 |
| jobqueue-hub | 进程名称为 `jobqueue-hub`，仅用于内置 WebSocket 后端 | 维护节点连接，选择接收任务的节点，传递控制信号 |

在启动任何子进程前，守护进程均会设置环境变量 `AKARI_CONFIG_READONLY=1`。此后所有子进程仅能读取配置。仅 pre-init 进程具备配置写入权限，并在执行写入前清除该标记。

`<实例根目录>/.bot.lock` 用于防止同一实例重复启动。若尝试再次启动同一实例，新进程将以退出码 1 退出。

## 启动顺序

1. 守护进程先选择语言，并生成初始 `config.toml`。该文件仅在首次运行时生成，仅包含 `default_locale` 和 `config_version`。
2. pre-init 子进程加载配置模板，补充缺失项，调用 `init_db(generate_schemas=True)` 创建数据表并执行迁移。
3. 守护进程读取适配器实例。它会先检查同一平台是否有重复的登录信息或端口配置，再逐个启动平台进程。
4. 若 JobQueue 使用 `websocket` 后端且模式为 `embedded`，守护进程会先启动 Hub 并等待其进入就绪状态，最多等待 10 秒。
5. 启动 Server 进程。随后守护进程每秒检查一次各子进程的运行状态。

## 退出码与重启

| 退出码 | 含义 | 守护进程操作 |
| --- | --- | --- |
| `0` | 正常退出 | Server 退出时整体退出，平台进程退出时不重启 |
| `33` | 请求重启 | 清理导入缓存，重启全部子进程 |
| `78` | 配置错误，无法恢复 | 移除该进程，不再重启 |
| 其他 | 异常退出 | 平台进程会重启，同一实例在 60 秒内连续失败三次后不再重启 |

`~restart` 首先将发起重启的会话记录保存至 `data/private/<client>/.cache_restart_author`，随后调用 `core.server.terminate.restart()`。该函数负责释放全部运行时资源，并以退出码 33 终止进程（`os._exit(33)`）。

新启动的 Server 进程将等待目标平台进程以新的 `peer_id` 注册为 `ready` 状态（超时上限为 60 秒），随后发送重启完成提示。模块加载失败的详细信息记录于 `.cache_loader` 中。

## Server 初始化

`core.server.run.main()` 依次完成：

```text
build_locale_snapshot(...)             构建语言快照
connect_locale_snapshot("akari-bot")   启用语言快照
init_async(send_prompt=False)          初始化数据库、模块、计划任务与密钥
JobQueueServer.check_job_queue()       注册节点并开始领取任务
JobQueueServer.wait_ready()            等待本实例注册完成
load_prompt(...)                       投递重启提示，失败不阻塞启动
```

`init_async` 还会注册 `hourly-background` 核心任务。该任务每小时执行一次会话后台检查，清理过期的队列记录与临时缓存映射。

主循环每秒检查一次队列轮询任务的运行状态。轮询器异常退出将被判定为严重故障，Server 进程立即退出并交由守护进程处理。

## 消息收发

消息分为入站和出站两条链路。平台进程负责与平台 SDK 交互，Server 负责解析消息并执行模块。

### 入站

1. 平台进程构造 `SessionInfo`，其中包含平台、场景、发送者、消息链和 `ctx_slot`，随后调用 `Bot.process_message()`。
2. `Bot.process_message()` 在后台保存上下文并设置保活标记，通过 `ServerAPI.receive_message` 将消息投递至 Server。处理流程结束后，平台 SDK 的上下文将被释放。
3. Server 端的 `parser()` 刷新会话信息，依次执行 `SESSION_READY` 与 `SESSION_BEFORE_WAIT` 等 Hook，检查是否存在等待该消息的挂起任务，随后解析命令前缀。
4. 命令路径首先解析别名，依据最长前缀匹配选定模块并获取执行锁，随后由模块的命令模板执行参数解析。正则匹配路径则在 `REGEX_ROUTE` Hook 执行后遍历候选模块。
5. 模块函数通过 `MessageSession` 读取 `session_info`、`parsed_msg` 和 `trigger_msg`。

### 出站

1. `MessageSession.send_message()` 首先整理消息链，执行敏感词过滤、媒体压缩与合规检查。通过 `OUTGOING_BEFORE_SEND` Hook 处理后，调用 `PlatformAPI.send_message`。
2. Server 依据 `owner_peer_id` 将调用分发至接收原始消息的平台进程。平台进程的 `ContextManager` 执行实际发送，并返回消息 ID。
3. 主动推送由 `Bot.post_message` 发起。该流程依据场景组与消息通道筛选候选会话，各通道优先由队首会话执行投递，其余会话作为备用会话。发送失败时，平台进程将备用会话列表返回至 Server，由 Server 依次尝试后续会话。

## 计划任务

`SchedulerLifecycle` 统一管理模块任务和核心任务：

- 模块任务 ID 为 `module:<模块>:<序号>`，核心任务 ID 为 `core:<名称>`。
- `CronTrigger` 与 `DateTrigger` 直接生效，`IntervalTrigger` 依据 `schedule_interval_multiplier` 按倍数调整触发间隔。
- 每个任务最多同时并发运行单一实例（`max_instances=1`），错过触发时限后最多允许延迟 30 秒执行。
- 卸载、重载和关闭前会进入维护时段。在此期间调度器将停止接收新任务，等待正在启动的任务进入运行状态，随后终止正在运行的任务。
- 维护期间提交但尚未开始执行的任务，将在启动前被直接拒绝。

## 关闭顺序

`cleanup_sessions()` 按以下顺序执行：

1. 停止接收新任务。
2. 等待正在处理的队列任务完成。
3. 取消消息处理器。
4. 关闭调度器。
5. 停止后台初始化。
6. 关闭模块运行环境。
7. 运行预先安排的后台清理任务。

最后停止轮询器，并关闭队列、WebRender 与数据库连接。

守护进程按平台进程、Server、Hub 的顺序终止子进程。Hub 最后退出，以便传递关闭信号并返回结果。
