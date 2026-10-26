# 架构

本页描述当前进程拓扑、启动与关闭路径，以及一条消息从平台进入再到平台发出的完整链路。

## 进程拓扑

| 进程 | 启动方式 | 职责 |
| --- | --- | --- |
| BotDaemon | `python -m akaribot.core.entrypoints.run` | 取实例锁、执行 pre-init、派生并监督子进程 |
| pre-init | 守护进程以 `spawn`（Windows、macOS）或 `forkserver` 派生 | 补写配置、建表、执行数据库迁移 |
| 平台进程 | 每个适配器实例一个，进程名为 `client_name` | 持有平台 SDK、消息上下文与按钮状态 |
| Server | 进程名 `server` | 解析消息、执行模块、运行计划任务 |
| jobqueue-hub | 进程名 `jobqueue-hub`，仅内置 WebSocket 后端 | 维护 Peer 连接、任播选择与信号投递 |

守护进程在任何子进程启动之前置位 `AKARI_CONFIG_READONLY=1`，此后所有子进程只读配置；pre-init 清除该
标记，是唯一的配置写入者。实例锁为 `<实例根>/.bot.lock`，同实例重复启动以退出码 1 中止。

## 启动顺序

1. 守护进程选择语言、生成仅含 `default_locale` 与 `config_version` 的 `config.toml` 骨架（首次运行）。
2. pre-init 子进程加载配置模板，补写缺失项，`init_db(generate_schemas=True)` 建表并执行迁移。
3. 守护进程发现适配器实例，先检查同一平台是否配置了重复凭据或端口，再逐个启动平台进程。
4. 若 JobQueue 使用 `websocket` 且模式为 `embedded`，先启动 Hub 并等待就绪事件（上限 10 秒）。
5. 启动 Server 进程，随后每秒检查各子进程状态。

## 退出码与重启

| 退出码 | 含义 | 守护进程动作 |
| --- | --- | --- |
| `0` | 正常退出 | Server 退出则整体退出，平台进程退出则不再重启 |
| `33` | 请求重启 | 清理导入缓存后重启全部子进程 |
| `78` | 配置性错误，重试无意义 | 移除该进程，不再重启 |
| 其它 | 异常退出 | 平台进程重启，同一实例 60 秒内连续三次失败后放弃 |

`~restart` 先把发起会话写入 `data/private/<client>/.cache_restart_author`，再调用
`core.server.terminate.restart()`：清理全部资源后 `os._exit(33)`。新 Server 启动后最多等待 60 秒，
等目标平台进程以新的 `peer_id` 注册为 `ready`，再投递重启提示；模块加载失败信息来自
`.cache_loader`。

## Server 初始化

`core.server.run.main()` 依次完成：

```text
build_locale_snapshot(...)        构建语言快照并连接
init_async(send_prompt=False)     数据库、模块、计划任务、密钥集合
JobQueueServer.check_job_queue()  注册 Peer 并开始领取任务
JobQueueServer.wait_ready()       等待本实例可路由
load_prompt(...)                  投递重启提示（best-effort）
```

`init_async` 还注册 `hourly-background` 核心任务，每小时执行会话后台检查、清理过期队列记录与临时字典。
主循环每秒检查队列轮询任务；轮询器异常退出会被视为致命错误，进程随即退出并由守护进程处理。

## 消息收发链路

入站：

1. 平台进程构造 `SessionInfo`（平台、场景、发送者、消息链、`ctx_slot`），调用
   `Bot.process_message()`。
2. `Bot.process_message()` 以后台任务登记上下文与存活标记，经 `ServerAPI.receive_message` 投递到
   Server；平台 SDK 上下文在处理结束后释放。
3. Server 侧 `parser()` 刷新会话信息，依次经过 `SESSION_READY`、`SESSION_BEFORE_WAIT` 等 hook，
   尝试投递等待任务，然后判定命令前缀。
4. 命令路径解析别名（最长匹配），获取执行锁，再由模块的命令模板匹配；正则路径在
   `REGEX_ROUTE` 之后遍历候选模块。
5. 模块函数通过 `MessageSession` 读取 `session_info`、`parsed_msg`、`trigger_msg`。

出站：

1. `MessageSession.send_message()` 规范化消息链（关键词过滤、媒体压缩、敏感内容检查），经过
   `OUTGOING_BEFORE_SEND` hook 后调用 `PlatformAPI.send_message`。
2. Server 以 `owner_peer_id` 把调用定向到接收原消息的平台进程；平台进程的 `ContextManager`
   执行实际发送并返回消息 ID。
3. 主动推送（`Bot.post_message`）按场景组与消息通道归拢会话，每个通道只选一个队首发送，失败时
   把剩余下一跳交回 Server。

## 计划任务

`SchedulerLifecycle` 统一管理模块任务与核心任务：

- 模块任务 ID 为 `module:<模块>:<序号>`，核心任务为 `core:<名称>`。
- `CronTrigger`、`DateTrigger` 原样使用；`IntervalTrigger` 按 `schedule_interval_multiplier` 缩放间隔。
- 单任务 `max_instances=1`，错过触发允许 30 秒宽限。
- 卸载、重载与关闭前进入维护窗口：暂停调度、等待启动临界区、取消并收集运行中的任务。
- 认证失败或关闭期间提交的任务在启动临界区被拒绝。

## 关闭顺序

`cleanup_sessions()` 依次停止新任务入口、等待在途队列处理、取消 handler、关闭 Scheduler、停止后台
初始化、关闭模块 runtime、执行已登记的后台清理，最后在队列关闭窗口内停止轮询、关闭 WebRender 与
数据库连接。守护进程按平台进程、Server、Hub 的顺序终止子进程，Hub 最后退出以便传递关闭信号与回包。
