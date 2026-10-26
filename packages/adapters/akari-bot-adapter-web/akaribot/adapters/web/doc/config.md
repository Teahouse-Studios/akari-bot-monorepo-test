# Web 控制台配置项

配置表为 `bot_web`，密钥表为 `bot_web_secret`，两张表同处 `config/bot_web.toml`：普通项在 `[bot_web]`，密钥项在 `[bot_web_secret]`。

## 配置表 `bot_web`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `true` | 是否启动 Web 服务。 |
| `enable_https` | bool | `false` | 访问地址是否使用 HTTPS；TLS 由反向代理终止。 |
| `web_host` | str | `127.0.0.1` | Web 服务的主机地址，`0.0.0.0` 表示监听所有地址。 |
| `web_port` | int | `6485` | Web 服务的端口号，`0` 表示禁用服务。 |
| `login_max_attempt` | int | `5` | 10 分钟内的登录失败次数上限，超限后封禁来源 IP 1 小时。 |
| `heartbeat_attempt` | int | `3` | 心跳消息发送尝试次数。 |
| `heartbeat_interval` | int | `30` | 心跳消息发送间隔，单位为秒。 |
| `heartbeat_timeout` | int | `5` | 心跳消息回应超时时间，单位为秒。 |

## 密钥表 `bot_web_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `allow_origins` | list | `[]` | API 服务允许的 CORS 来源列表，设为 `"*"` 表示信任所有来源。 |
| `forwarded_allow_ips` | list | `["127.0.0.1"]` | 信任的反向代理来源列表，设为 `"*"` 表示信任所有来源。 |
| `jwt_secret` | str | `""` | 内置 API 的 JWT 签名密钥，为空时首次启动自动生成。 |

## 说明

- `web_port` 被占用时从该端口起向后尝试，最多 100 个端口；全部不可用时进程退出。
- 心跳参数通过 `/api/init` 提供给 WebUI。
- 修改 `jwt_secret` 会使已签发的令牌全部失效。
- `allow_origins` 与 `forwarded_allow_ips` 使用列表语法，例如 `["https://example.com"]`。
