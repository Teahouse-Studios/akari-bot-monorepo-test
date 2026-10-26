# OneBot 配置项

配置表为 `bot_onebot`，密钥表为 `bot_onebot_secret`，两张表同处 `config/bot_onebot.toml`：普通项在 `[bot_onebot]`，密钥项在 `[bot_onebot_secret]`。

## 配置表 `bot_onebot`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 OneBot 服务。 |
| `qq_host` | str | `127.0.0.1:8080` | WebSocket 主服务器的地址，格式为 `host:port`；协议端使用反向 WebSocket 连接。 |
| `qq_enable_listening_self_message` | bool | `false` | 是否开启自身消息监听。 |
| `qq_enable_temp_session` | bool | `true` | 是否开启临时会话。 |
| `qq_allow_approve_friend` | bool | `false` | 是否自动同意好友请求。 |
| `qq_allow_approve_group_invite` | bool | `false` | 是否自动同意群邀请。 |
| `qq_typing_emoji` | int | `181` | 正在处理消息时挂载的回应表情 ID，需协议端支持。 |
| `qq_limited_emoji` | int | `10060` | 消息处理失败时挂载的回应表情 ID，需协议端支持。 |
| `qq_initiative_msg_cooldown` | int | `10` | 主动消息发送的冷却时间，单位为秒。 |

## 密钥表 `bot_onebot_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `qq_access_token` | str | `""` | 连接 WebSocket 服务器的 Access Token。 |

## 说明

- `qq_host` 按 `host:port` 解析，不包含协议前缀。
- 反向 WebSocket 的可用路径为 `/ws`、`/ws/event` 与 `/ws/api`。
- 回应表情 ID 参见 [QQ 开放平台表情文档](https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#Emoji)。
