# WebUI 控制台

Web 适配器在实例内启动 FastAPI 与 uvicorn 服务，提供浏览器控制台和内置 API。控制台使用单一会话
连接机器人，可发送消息、管理配置、查看日志与统计数据。适配器不依赖任何平台账号。

## 启用与安装

```sh
akaribot module add akari-bot-adapter-web
```

也可以在 `akaribot init` 时加 `--adapter web`。`bot_web.enable` 默认为 `true`，安装后随实例启动。
前端静态资源优先取实例的 `data/webui/dist`，不存在时使用 `akari-bot-webui` 分发包。

## 访问地址

默认监听 `127.0.0.1:6485`，控制台地址为 `http://127.0.0.1:6485/webui`。服务启动时会把实际地址
写入日志；`web_host` 为 `0.0.0.0` 时还会列出本机网络地址。

`web_port` 被占用时，服务从该端口起在 `127.0.0.1` 上向后探测，最多尝试 100 个端口；全部不可用
时记录 `API port is disabled.` 并结束 Web 适配器进程。`web_port = 0` 直接禁用服务。端口发生回退后，
应以日志中的实际端口访问。

`enable_https = true` 只把日志与 `/api/init` 返回的访问协议改成 `https`，服务本身不加载证书，
TLS 必须在反向代理终止。

## 配置

配置表为 `bot_web`，密钥表为 `bot_web_secret`，两张表同处 `config/bot_web.toml`。`web_host`、
`web_port`、`enable`、`enable_https`、`allow_origins`、`forwarded_allow_ips` 与
`login_max_attempt` 在 Web 服务启动时读取，修改后需重启实例。

| 字段 | 表 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `bot_web` | `true` | 是否启动 Web 服务。 |
| `enable_https` | `bot_web` | `false` | 访问地址是否使用 HTTPS。 |
| `web_host` | `bot_web` | `127.0.0.1` | 监听地址，`0.0.0.0` 表示所有地址。 |
| `web_port` | `bot_web` | `6485` | 监听端口，`0` 表示禁用。 |
| `login_max_attempt` | `bot_web` | `5` | 10 分钟内允许的登录失败次数。 |
| `heartbeat_attempt` | `bot_web` | `3` | 心跳消息尝试次数。 |
| `heartbeat_interval` | `bot_web` | `30` | 心跳间隔，单位秒。 |
| `heartbeat_timeout` | `bot_web` | `5` | 心跳回应超时，单位秒。 |
| `allow_origins` | `bot_web_secret` | `[]` | 允许的 CORS 来源列表。 |
| `forwarded_allow_ips` | `bot_web_secret` | `["127.0.0.1"]` | 可信反向代理地址列表。 |
| `jwt_secret` | `bot_web_secret` | `""` | 内置 API 的 JWT 签名密钥。 |

`jwt_secret` 为空时，Web 服务首次启动会生成 32 字节随机值并写回 `bot_web_secret`；修改该值会使
已签发的令牌全部失效。

## 登录与密码

未设置密码时，`POST /api/login` 不校验口令，直接签发令牌。首次登录后应立刻在控制台设置强口令；
把服务暴露到公网前必须先设置密码。

密码以 Argon2 哈希保存在 `data/private/web/.password`。删除该文件即可重置：密码与已启用的两步验证、
恢复代码一并失效，之后可再次免密登录并设置新密码。运行中的服务每 30 秒检查一次文件，发现被删除时
记录安全事件。

<NoticeBox type="danger">
删除密码文件等同于把控制台恢复为无密码状态。删除前先停止实例或限制端口访问，设置新密码后再恢复。
</NoticeBox>

登录失败按来源 IP 计入 10 分钟滑动窗口，超过 `login_max_attempt` 后封禁该 IP 1 小时；同一窗口内
失败达到 3 次起逐次增加响应延迟，最多 5 秒。登录与令牌校验接口另有每分钟 10 次的限流。

令牌有效期 24 小时。修改密码会更新密码文件的 `last_updated`，此前签发的令牌随即失效。控制台支持
TOTP 两步验证，启用时生成 8 个一次性恢复代码；启用两步验证后不能通过 API 清除密码，需先关闭两步
验证。

## 反向代理与 HTTPS

- `forwarded_allow_ips` 传给 uvicorn，只有来自这些地址的 `X-Forwarded-For` 才会被采信；默认仅
  信任本机。代理不在本机时，填入代理地址；`["*"]` 信任所有来源，不建议在不可控网络中使用。
- `allow_origins` 控制浏览器跨域访问；留空表示不向其它来源开放 CORS。前后端分离部署时填入控制台
  的实际来源，`["*"]` 表示信任所有来源。
- 由反向代理终止 TLS，再把请求转发到 `127.0.0.1:6485`；同时把 `enable_https` 设为 `true`，使
  日志与前端拿到正确的访问协议。直接对外监听时，公网端口应在防火墙中放行，并先设置密码。

## 功能范围

控制台与内置 API 当前覆盖：

- 面板与运行信息：系统、进程、内存、磁盘、机器人版本与消息统计（`/api/server-info`）。
- 统计：消息量与按模块汇总的调用次数（`/api/analytics`、`/api/analytics/modules`）。
- 配置：列出、读取、写入与删除 `config/` 下的 TOML 文件；`config.toml` 受保护，不能通过接口删除。
- 日志：通过 `/ws/logs` 推送当天 `logs/*_<日期>.log` 的新增内容。
- 聊天：通过 `/ws/chat` 发送文本与图片、添加表情回应，并处理按钮回调与心跳。
- 会话与用户：查询和修改场景、用户数据，调整屏蔽、静音、信任、超级管理员与模块启用状态。
- 模块：模块列表、说明文档、关联模块，以及重载、装载与卸载。
- 文件：浏览与编辑实例的 `assets/`、`data/`、`cache/` 及模块的 `assets/` 与 `data/`，支持上传、
  新建、重命名、下载与删除；媒体文件经 `/api/media/{token}` 读取。
- WebRender：查看状态、启动或停止服务并执行测试渲染。
- 更新与重启：`/api/update` 与 `/api/restart`。

设置环境变量 `DEV_MODE=true` 后，额外开放 `/api/dev/database/*` 的数据库模型浏览与 SQL 执行，
以及 `/api/dev/files/*` 的开发文件接口。
