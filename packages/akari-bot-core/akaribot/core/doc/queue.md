# JobQueue

JobQueue 是平台进程与 Server 之间的跨进程通信层，同时提供 Peer 注册表与消息传输。业务代码通过
`PlatformAPI`、`ServerAPI` 与信号声明使用它，不直接操作队列表。

## 后端

配置位于 `config/jobqueue.toml`，`[jobqueue].jobqueue_backend` 取 `database` 或 `websocket`。两种后端
互斥：同一逻辑集群的进程必须使用相同值，运行期间不支持切换。

| 比较项 | `database` | `websocket` |
| --- | --- | --- |
| 传输 | 轮询 `job_queues` 表 | Hub 内实时路由 |
| 离线任务 | 保留待领取记录 | 不保留，目标离线即不可用 |
| 额外组件 | 无 | Hub 进程或外部 Hub |
| 适用场景 | 可并发写入的共享数据库 | 默认选项，SQLite 与高频 RPC |

`jobqueue_websocket_mode` 区分 `embedded` 与 `external`。内置模式从 `jobqueue_websocket_url` 解析监听
地址，仅接受回环地址上的 `ws`；连接外部 Hub 须使用 `wss` 并配置共享令牌。`jobqueue_node_id` 是节点
标签，为空时由 pre-init 生成 UUID 写回配置。`jobqueue_websocket_token` 为空时同样在启动前生成并落盘。

## Peer 与寻址

每个进程有两个身份：

- `peer_id`：每次进程生命周期内唯一，用于实例直投。
- `service`：稳定的服务组标识（如 `Server`、`QQ`），同组成员竞争领取普通 RPC，实现任播。

进程状态依次为 `starting`、`ready`、`maintenance`、`draining`、`stopped`。`check_job_queue()` 注册
实例并切换为 `ready`；每 15 秒续租，每 10 秒按权威注册表对账；租约 45 秒未续期即判定离线。关闭时先
广播 `draining`，处理完在途任务后广播 `stopped`。

`core.alive.Alive` 是进程内的同步路由缓存，只复用已由注册表确认的记录。需要亲和性的调用使用
`ServiceRoute` 描述 service、角色与路由键，运行时按 Rendezvous Hash 从 `ready` 实例中选择目标。

## RPC

共享契约声明在 `akaribot/core/queue/contracts.py`：

```python
from akaribot.core.queue.contracts import PlatformAPI, ServerAPI

message_ids = await PlatformAPI.send_message(session_info, message, quote=False)
modules = await ServerAPI.get_modules_list()
task_id = await PlatformAPI.post_message.submit(session_info, message, module_name)
```

- 直接 `await` 等待远端结果；`.submit()` 只等待后端接受投递。
- `ContextManager` 上的平台方法通过 `context_method()` 自动绑定，参数签名取自方法本身。
- 默认超时：普通调用 120 秒，信号 30 秒，消息处理与发送最长 7200 秒。每个请求有独立 deadline。
- 失败以 `RpcError` 子类抛出：`RpcUnavailableError`（目标不可达）、`RpcTimeoutError`、`RpcCancelledError`、
  `RpcMethodNotFoundError`、`RpcProtocolError`，远端异常包装为 `RpcRemoteError` 并保留 traceback。
- 不提供 exactly-once。发送、禁言等有外部副作用的调用不得因超时自动重试。

`PlatformAPI.post_message` 在目标通道发送失败时，把 `SessionInfo.next_hops` 交回 Server 继续尝试下
一跳；整条通道都不可用时返回空列表。

## 信号

信号按发送时刻的在线实例逐条投递，各目标独立 ACK：

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

`.emit()` 不要求回包，`.gather()` 逐实例等待 ACK。信号处理器须幂等，版本化数据以持久化状态为准。

## 数据表

| 表 | 内容 |
| --- | --- |
| `job_queues` | 任务记录：目标、来源、动作、参数、状态、领取者与结果 |
| `job_queue_peers` | Peer 注册表：角色、service、状态、能力、元数据与租约 |

`database` 后端以 `pending` 条件原子领取任务，每轮候选上限 100 条；终态记录在调用方读取后删除，
并由每小时后台任务兜底清理。`websocket` 后端不持久化任务与终态。

## 关闭与维护

维护窗口先停止领取新任务，再等待已进入的处理完成。数据库热重载在维护窗口内独占连接；关闭期间结果
接收器继续运行，直到会话与后台任务清理完毕才停止。轮询器异常退出时，实例撤销注册并释放本地等待方，
避免以「可路由但无法收发」的状态存活。
