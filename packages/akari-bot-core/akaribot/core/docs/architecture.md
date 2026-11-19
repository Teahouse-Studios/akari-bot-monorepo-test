# 架构

本文将会介绍 AkariBot 实例的内部结构。

## 介绍

AkariBot 的代码按分发包拆分。core 提供运行时和公共设施，内置模块、外部模块和平台适配器各自单独打包。

实例启动时，守护进程负责启动并监督子进程。这些子进程分别处理配置初始化、平台连接、消息和计划任务。

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

几点说明：

- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，不带 `__init__.py`。查找包时，以入口声明为准，目录扫描只作为备用方式。
- CLI 不依赖 core。执行 `akaribot <子命令>` 时，CLI 通过子进程调用 `python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。
- 仓库根目录保留了旧的导入入口。`bot.py`、`tester.py` 通过 `sys.modules` 把旧模块名映射到新实现。`core/database/update.py` 只负责把旧版本的升级请求转交给当前实现。

## 进程拓扑

| 进程 | 启动方式 | 职责 |
| --- | --- | --- |
| BotDaemon | `python -m akaribot.core.entrypoints.run` | 检查同一实例是否已经启动，执行 pre-init，启动并监督子进程 |
| pre-init | 守护进程以 `spawn`（Windows、macOS）或 `forkserver` 启动 | 补充缺失的配置项，创建数据表，执行数据库迁移 |
| 平台进程 | 每个适配器实例对应一个进程，进程名为 `client_name` | 持有平台 SDK、消息上下文和按钮状态 |
| Server | 进程名 `server` | 解析消息，执行模块，运行计划任务 |
| jobqueue-hub | 进程名 `jobqueue-hub`，仅内置 WebSocket 后端 | 维护节点连接，选择接收任务的节点，传递控制信号 |

守护进程会在任何子进程启动前设置 `AKARI_CONFIG_READONLY=1`。此后所有子进程只能读取配置。pre-init 是唯一可以写配置的进程，它会清除这个标记。

`<实例根>/.bot.lock` 用来防止同一实例重复启动。同一实例第二次启动时，新进程会以退出码 1 结束。

## 启动顺序

1. 守护进程先选择语言，并生成初始 `config.toml`。这个文件只在首次运行时生成，只包含 `default_locale` 和 `config_version`。
2. pre-init 子进程加载配置模板，补充缺失项，调用 `init_db(generate_schemas=True)` 创建数据表并执行迁移。
3. 守护进程读取适配器实例。它先检查同一平台是否有重复的登录信息或端口配置，再逐个启动平台进程。
4. 如果 JobQueue 使用 `websocket` 后端，且模式为 `embedded`，守护进程会先启动 Hub，等它就绪，最多等 10 秒。
5. 启动 Server 进程。之后，守护进程每秒检查一次各子进程的状态。

## 退出码与重启

| 退出码 | 含义 | 守护进程动作 |
| --- | --- | --- |
| `0` | 正常退出 | Server 退出时整体退出，平台进程退出时不重启 |
| `33` | 请求重启 | 清理导入缓存，重启全部子进程 |
| `78` | 配置错误，重试无效 | 移除该进程，不再重启 |
| 其它 | 异常退出 | 平台进程会重启，同一实例在 60 秒内连续失败三次后不再重启 |

`~restart` 先把发起重启的会话写入 `data/private/<client>/.cache_restart_author`，再调用 `core.server.terminate.restart()`。这个函数清理全部资源，然后调用 `os._exit(33)`。

新的 Server 启动后，会等目标平台进程以新的 `peer_id` 注册为 `ready`，最多等 60 秒，然后发送重启提示。模块加载失败的信息记录在 `.cache_loader` 中。

## Server 初始化

`core.server.run.main()` 依次完成：

```text
build_locale_snapshot(...)        构建语言快照并连接
init_async(send_prompt=False)     数据库、模块、计划任务、密钥集合
JobQueueServer.check_job_queue()  注册节点并开始领取任务
JobQueueServer.wait_ready()       等待本实例可以接收任务
load_prompt(...)                  投递重启提示（尽力而为）
```

`init_async` 还会注册 `hourly-background` 核心任务。这个任务每小时执行一次会话后台检查，清理过期的队列记录和临时字典。

主循环每秒检查一次队列轮询任务是否仍在运行。轮询器异常退出会被视为致命错误。此时进程立即退出，由守护进程处理。

## 消息收发

消息分为入站和出站两条链路。平台进程负责与平台 SDK 交互，Server 负责解析消息并执行模块。

### 入站

1. 平台进程构造 `SessionInfo`，其中包含平台、场景、发送者、消息链和 `ctx_slot`，然后调用 `Bot.process_message()`。
2. `Bot.process_message()` 在后台保存上下文并设置存活标记，再通过 `ServerAPI.receive_message` 把消息投递给 Server。处理结束后，平台 SDK 的上下文会被释放。
3. Server 端的 `parser()` 刷新会话信息，依次执行 `SESSION_READY`、`SESSION_BEFORE_WAIT` 等 Hook，检查是否有等待这条消息的任务，再判断命令前缀。
4. 命令路径先解析别名，按最长匹配选中模块并获取执行锁，再由模块的命令模板完成匹配。正则路径在 `REGEX_ROUTE` Hook 之后遍历候选模块。
5. 模块函数通过 `MessageSession` 读取 `session_info`、`parsed_msg` 和 `trigger_msg`。

### 出站

1. `MessageSession.send_message()` 先整理消息链，再执行关键词过滤、媒体压缩和敏感内容检查。之后经过 `OUTGOING_BEFORE_SEND` Hook，再调用 `PlatformAPI.send_message`。
2. Server 根据 `owner_peer_id` 把调用交给接收原消息的平台进程。平台进程的 `ContextManager` 完成实际发送，并返回消息 ID。
3. 主动推送由 `Bot.post_message` 发起。它按场景组和消息通道整理会话。每个通道只让队列中的第一个会话发送，其余会话留作备用。发送失败时，平台进程把备用会话列表交回 Server，Server 再依次尝试下一个会话。

## 计划任务

`SchedulerLifecycle` 统一管理模块任务和核心任务：

- 模块任务 ID 为 `module:<模块>:<序号>`，核心任务 ID 为 `core:<名称>`。
- `CronTrigger` 和 `DateTrigger` 直接使用，`IntervalTrigger` 按 `schedule_interval_multiplier` 调整间隔。
- 每个任务最多同时运行一个实例（`max_instances=1`）。错过触发后最多延迟 30 秒执行。
- 卸载、重载和关闭前会进入维护时段。这段时间内先暂停调度，等正在启动的任务进入运行状态，再取消并收集正在运行的任务。
- 维护期间提交、但还没开始执行的任务，会在启动前被拒绝。

## 关闭顺序

`cleanup_sessions()` 按以下顺序收尾：

1. 停止接收新任务。
2. 等待正在处理的队列任务完成。
3. 取消消息处理器。
4. 关闭调度器。
5. 停止后台初始化。
6. 关闭模块运行环境。
7. 执行预先安排的后台清理任务。

最后，它在关闭队列前停止轮询，并关闭 WebRender 和数据库连接。

守护进程按平台进程、Server、Hub 的顺序终止子进程。Hub 最后退出，以便传递关闭信号并返回结果。
