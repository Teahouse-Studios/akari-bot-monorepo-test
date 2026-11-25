# Satori 配置项

本文整理了 Satori 适配器的配置表项与填写时的注意事项。

配置表为 `bot_satori`，密钥表为 `bot_satori_secret`。两张表均保存在 `config/bot_satori.toml` 中。常规配置项位于 `[bot_satori]`，密钥项位于 `[bot_satori_secret]`。

## 配置表 `bot_satori`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Satori 客户端。 |
| `satori_host` | str | `127.0.0.1` | Satori 服务端的主机名或 IP。 |
| `satori_port` | int | `5140` | Satori 服务端的端口。 |
| `satori_path` | str | `""` | 服务端的路径前缀，用于反向代理部署。 |
| `satori_secure` | bool | `false` | 是否以 HTTPS 与 WSS 连接服务端。 |
| `satori_timeout` | int | `30` | API 请求的超时时间，单位为秒。 |
| `satori_enable_listening_self_message` | bool | `false` | 是否监听机器人自身消息。 |
| `satori_admin_roles` | list | `["admin", "owner"]` | 视为管理员的角色 ID 或名称。 |
| `satori_typing_emoji` | str | `⌛` | 处理消息时添加的回应表情。 |
| `satori_limited_emoji` | str | `❌` | 处理出错时添加的回应表情。 |

## 密钥表 `bot_satori_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `satori_token` | str | `""` | 服务端的访问令牌。 |

## 说明

- `satori_host` 仅填写主机名或 IP，不包含协议前缀与端口。是否使用 TLS 由 `satori_secure` 控制。
- `satori_path` 不以斜杠开头时会自动补全，为空时连接服务端根路径。事件与接口地址均以该前缀为基准。
- `satori_token` 为空时不发送访问令牌。服务端启用鉴权时必须填写，取值与服务端一致。
- 适配器将 `satori_admin_roles` 与成员的角色 ID 或角色名称比对，不区分大小写。匹配的成员按平台原生管理员处理。
- `satori_typing_emoji` 与 `satori_limited_emoji` 仅在群聊的触发消息上添加，留空时不添加回应表情。
- `satori_timeout` 作用于 API 请求与媒体上传，单位为秒。
