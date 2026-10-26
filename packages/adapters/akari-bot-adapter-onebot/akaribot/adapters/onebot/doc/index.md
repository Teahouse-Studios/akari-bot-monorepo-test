# OneBot 适配器

通过 OneBot 反向 WebSocket 接入 QQ，处理群聊、私信与通知事件。

## 平台概述

适配器在本地启动 WebSocket 服务，由 OneBot 协议端反向连接。消息按 CQ 码或消息段解析，群聊与私信分别归属 `QQ|Group` 与 `QQ|Private` 前缀，两个前缀同属 `QQ` 客户端身份。除消息外还处理戳一戳、群消息表情点赞、好友请求、群邀请以及机器人被禁言、被移出群聊等通知。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-onebot
```

安装后由守护进程按配置启动，启动条件为 `bot_onebot.enable = true`。

## 配置

配置表为 `bot_onebot`，密钥表为 `bot_onebot_secret`，两张表同处 `config/bot_onebot.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add onebot <实例 ID>` 新增实例；实例表名为 `bot_onebot-<实例 ID>`，密钥表名为 `bot_onebot-<实例 ID>_secret`，两张表同处 `config/bot_onebot-<实例 ID>.toml`。

主要字段如下，完整字段与默认值见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 OneBot 服务。 |
| `qq_host` | str | `127.0.0.1:8080` | 反向 WebSocket 监听地址，格式为 `host:port`。 |
| `qq_access_token` | str | `""` | 连接鉴权令牌，位于密钥表。 |
| `qq_enable_temp_session` | bool | `true` | 是否处理临时会话。 |
| `qq_enable_listening_self_message` | bool | `false` | 是否监听机器人自身消息。 |

## 必填凭据

- `qq_access_token`：协议端配置的 Access Token；协议端未启用鉴权时留空。

## 监听地址与端口

- 适配器默认监听 `127.0.0.1:8080`，可通过 `qq_host` 改为其他 `host:port`。
- OneBot 协议端须使用反向 WebSocket 连接，可用路径为 `/ws`、`/ws/event` 与 `/ws/api`。
- 服务启动超时时间为 120 秒。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | — |
| Markdown | 不支持 | 消息按纯文本发送。 |
| 按钮与动作文本 | 不支持 | — |
| 表情回应 | 支持 | 通过群消息表情点赞实现。 |
| 引用回复 | 支持 | — |
| 输入状态 | 支持 | 通过挂载回应表情表示正在处理。 |
| 消息撤回 | 支持 | 群聊与私信均可撤回。 |
| 群组管理 | 支持 | 含禁言、踢出与管理员设置。 |
| 权限组 | 支持 | — |
| 消息节点 | 支持 | 合并转发按消息节点处理。 |
| 私信 | 支持 | — |
| RSS 推送 | 支持 | — |

链接管理与内容审核分别由 core 配置 `config.enable_urlmanager` 与 `config.enable_dirty_check` 控制。

## 私信与群聊

- 群聊目标前缀为 `QQ|Group`，私信为 `QQ|Private`；临时会话由 `qq_enable_temp_session` 控制。
- 群聊是否必须 @机器人 由 core 配置 `mention_required` 决定。
- 机器人默认不处理自身发送的消息，开启 `qq_enable_listening_self_message` 后一并处理。
- 开启 core 配置 `config.quick_confirm` 时，戳一戳会触发确认命令。
- 好友请求与群邀请默认仅对超级管理员与受信用户自动同意，其余请求分别由 `qq_allow_approve_friend` 与 `qq_allow_approve_group_invite` 控制。
- 开启 core 配置 `config.enable_tos` 时，机器人被禁言或被移出群聊会记入违规记录并封禁相关场景。

## 外部依赖

- 兼容 OneBot 的协议端，并配置为反向 WebSocket。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
