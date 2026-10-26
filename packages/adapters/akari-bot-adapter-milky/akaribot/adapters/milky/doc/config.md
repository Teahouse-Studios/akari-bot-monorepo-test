# Milky 配置项

配置表为 `bot_milky`，密钥表为 `bot_milky_secret`，两张表同处 `config/bot_milky.toml`：普通项在 `[bot_milky]`，密钥项在 `[bot_milky_secret]`。

## 配置表 `bot_milky`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Milky 客户端。 |
| `qq_host` | str | `http://127.0.0.1:8080` | Milky 协议端 HTTP 服务的地址。 |
| `qq_enable_listening_self_message` | bool | `false` | 是否开启自身消息监听。 |
| `qq_enable_temp_session` | bool | `true` | 是否开启临时会话。 |
| `qq_allow_approve_friend` | bool | `false` | 是否自动同意好友请求。 |
| `qq_allow_approve_group_invite` | bool | `false` | 是否自动同意群邀请。 |
| `qq_typing_emoji` | int | `181` | 正在处理消息时挂载的回应表情 ID，需协议端支持。 |
| `qq_limited_emoji` | int | `10060` | 消息处理失败时挂载的回应表情 ID，需协议端支持。 |
| `qq_initiative_msg_cooldown` | int | `10` | 主动消息发送的冷却时间，单位为秒。 |

## 密钥表 `bot_milky_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `qq_access_token` | str | `""` | 连接协议端 HTTP 服务的访问令牌。 |

## 说明

- `qq_host` 未带协议时按 `http://` 补全，末尾斜杠会被去除。
- 回应表情 ID 参见 [QQ 开放平台表情文档](https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#Emoji)。
