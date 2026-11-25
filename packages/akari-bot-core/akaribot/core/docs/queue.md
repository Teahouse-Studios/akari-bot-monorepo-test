# JobQueue

本文说明 JobQueue 的传输后端、节点路由机制、RPC、信号通信与停机流程。

`JobQueue` 为平台进程与 Server 之间的跨进程通信层，提供节点注册表与消息传输服务。业务代码通过 `PlatformAPI`、`ServerAPI` 与信号声明调用其功能。

## 后端

配置位于 `config/jobqueue.toml`，`[jobqueue].jobqueue_backend` 可选 `database` 或 `websocket`。两种后端互斥。同一逻辑集群的进程必须使用相同的值，切换后端需要重启进程。

| 比较项 | `database` | `websocket` |
| --- | --- | --- |
| 传输 | 轮询 `job_queues` 数据表 | Hub 内实时路由 |
| 离线任务 | 保留待认领记录 | 不保留，目标离线即不可用 |
| 额外组件 | 无 | Hub 进程或外部 Hub |
| 适用场景 | 支持并发写入的共享数据库 | 默认选项，SQLite 与高频 RPC |

`jobqueue_websocket_mode` 区分 `embedded` 与 `external`。内置模式从 `jobqueue_websocket_url` 解析监听地址，仅接受回环地址上的 `ws` 连接。连接外部 Hub 必须使用 `wss`，并配置共享令牌。

`jobqueue_node_id` 是节点标签，为空时 pre-init 会生成 UUID 并写回配置。

`jobqueue_websocket_token` 为空时，启动前会生成令牌并写回配置。

## 节点身份与定位

每个进程有两个身份：

- `peer_id`：进程启动时生成，用于将请求直接定向发送至该进程。
- `service`：按名称固定的服务组标识（如 `Server`、`QQ`）。同组成员竞争认领普通 RPC 请求，且每个请求仅由单个节点接收。

进程生命周期状态依次为 `starting`、`ready`、`maintenance`、`draining` 与 `stopped`。`check_job_queue()` 注册实例并将状态切换为 `ready`。

节点每 15 秒更新一次注册信息，每 10 秒与注册表核对一次。若超过 45 秒未更新，节点将被判定为离线。关闭流程中，节点先广播 `draining` 状态。处理完毕正在执行的任务后，节点广播 `stopped`。

`core.alive.Alive` 为进程内的同步路由缓存，仅复用已由注册表确认的记录。若需要将同一业务键固定路由至同一实例，可以使用 `ServiceRoute` 声明 service、角色与路由键。运行时按 Rendezvous Hash 算法从 `ready` 实例中选取目标节点。

## RPC

共享接口约定声明在 `akaribot/core/queue/contracts.py`：

```python
from akaribot.core.queue.contracts import PlatformAPI, ServerAPI

message_ids = await PlatformAPI.send_message(session_info, message, quote=False)
modules = await ServerAPI.get_modules_list()
task_id = await PlatformAPI.post_message.submit(session_info, message, module_name)
```

- 直接使用 `await` 将等待远程执行结果，调用 `.submit()` 则仅等待后端接收任务。
- `ContextManager` 上的平台方法由 `context_method()` 自动绑定，参数签名继承自方法本身。
- 默认超时：普通调用 120 秒，信号 30 秒，消息处理与发送最长 7200 秒。每个请求有独立的截止时间。
- 失败时抛出 `RpcError` 的子类：`RpcUnavailableError`（目标不可达）、`RpcTimeoutError`、`RpcCancelledError`、`RpcMethodNotFoundError`、`RpcProtocolError`，远程异常在客户端重新抛出。
- RPC 请求至少被投递一次，且可能发生重复投递。发送消息、禁言等具有外部副作用的调用在超时后，由调用方自行判断是否重试。

`PlatformAPI.post_message` 在目标通道发送失败时，将 `SessionInfo.next_hops` 返回给 Server，由 Server 继续尝试下一跳。整条通道均不可用时，该方法返回空列表。

## 信号

信号按发送时刻的在线实例逐条发送，各目标独立确认：

```python
from akaribot.core.queue.peer import PeerSelector
from akaribot.core.queue.rpc import signal


@signal("cache.invalidate", timeout=30)
async def invalidate_cache(version: int) -> None: ...


@invalidate_cache.bind(JobQueueServer)
async def invalidate_server_cache(version: int) -> None: ...


receipt = await invalidate_cache.emit(PeerSelector.role("server"), version=8)
report = await invalidate_cache.gather(PeerSelector.service("Server"), version=8)
```

`.emit()` 仅负责发送信号，`.gather()` 逐个实例等待确认。信号处理函数必须具备幂等性，同一信号接收多次时的结果与接收一次相同。携带版本号的数据以持久化状态为准。

## 数据表

| 表 | 内容 |
| --- | --- |
| `job_queues` | 任务记录（目标、来源、动作、参数、状态、认领者与结果） |
| `job_queue_peers` | 节点注册表（角色、service、状态、能力、元数据与注册有效期） |

`database` 后端以 `pending` 为条件执行原子认领任务，每轮候选上限为 100 条。已结束的任务记录在调用方读取后删除，遗漏的记录由每小时运行一次的后台任务清理。`websocket` 后端不持久化保存任务记录与结束状态。

## 关闭与维护

进入维护窗口后，节点停止认领新任务，并等待已开始的处理流程执行完毕。数据库热重载在维护窗口内执行，期间排他占用数据库连接。

关闭流程中，结果接收器保持运行。会话与后台任务清理完毕后，结果接收器停止运行。轮询器异常退出时，实例撤销注册并释放本地等待方。
