# QQ 机器人（官方）配置项

配置表为 `bot_qqbot`，密钥表为 `bot_qqbot_secret`，两张表同处 `config/bot_qqbot.toml`：普通项在 `[bot_qqbot]`，密钥项在 `[bot_qqbot_secret]`。

## 配置表 `bot_qqbot`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 QQ 机器人客户端。 |
| `qq_bot_appid` | str \| int | `""` | 机器人 AppID。 |
| `qq_bot_openid` | str | `""` | 机器人自身 OpenID。 |
| `qq_bot_enable_send_url` | bool | `false` | 服务器频道与频道私信发送纯文本时是否保留链接；关闭时含链接的行会被丢弃。 |
| `qq_private_bot` | bool | `false` | 是否为私域机器人。 |
| `qq_typing_emoji` | int | `181` | 正在处理消息时挂载的回应表情 ID。 |
| `qq_limited_emoji` | int | `10060` | 消息处理失败时挂载的回应表情 ID。 |
| `qq_use_markdown` | bool | `false` | 是否使用 Markdown 格式消息。 |
| `qq_bot_certified` | bool | `true` | 机器人是否已通过企业或个人认证，未认证时主动消息配额更低。 |
| `qq_navigation_sync_strict` | bool | `false` | 全局菜单与指令面板同步失败时是否阻止启动。 |
| `qq_use_webhook` | bool | `false` | 是否使用 Webhook 接收事件，关闭则连接 Gateway。 |
| `qq_webhook_host` | str | `0.0.0.0` | Webhook 监听地址。 |
| `qq_webhook_port` | int | `8080` | Webhook 监听端口。 |
| `qq_webhook_path` | str | `/` | Webhook 回调路径，须与开放平台配置一致。 |
| `qq_bot_uid` | str | `""` | 机器人 UID。 |
| `qq_bot_qqnum` | str | `""` | 机器人 QQ 号。 |
| `qq_api_url` | str | `""` | 自定义 API 基地址，留空使用官方地址。 |

## 密钥表 `bot_qqbot_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `qq_bot_secret` | str | `""` | 机器人 AppSecret。 |

## 说明

- 两个实例的 `qq_bot_appid` 与 `qq_bot_secret` 均相同时，视为同一机器人账号，守护进程据此检查多实例凭据冲突。
- `qq_use_markdown` 同时决定按钮、动作文本与消息节点能力；服务器频道不受该配置影响。
- 回应表情 ID 参见 [QQ 开放平台表情文档](https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#Emoji)。
- Webhook 模式只监听 HTTP，TLS 由反向代理终止。
