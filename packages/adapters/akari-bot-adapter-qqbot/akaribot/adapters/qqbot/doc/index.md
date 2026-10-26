# QQ 机器人（官方）适配器

通过 QQ 开放平台官方机器人接口接入群聊、私信与服务器频道。

## 平台概述

适配器使用 AppID 与 AppSecret 登录 QQ 开放平台，默认经 WebSocket Gateway 接收事件，也可切换为 Webhook 由平台回调。会话分为群聊、C2C 私信、服务器频道与频道私信；启动时会同步全局菜单与指令面板。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-qqbot
```

安装后由守护进程按配置启动，启动条件为 `bot_qqbot.enable = true`。

## 配置

配置表为 `bot_qqbot`，密钥表为 `bot_qqbot_secret`，两张表同处 `config/bot_qqbot.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add qqbot <实例 ID>` 新增实例；实例表名为 `bot_qqbot-<实例 ID>`，密钥表名为 `bot_qqbot-<实例 ID>_secret`，两张表同处 `config/bot_qqbot-<实例 ID>.toml`。

主要字段如下，完整字段与默认值见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 QQ 机器人客户端。 |
| `qq_bot_appid` | str \| int | `""` | 机器人 AppID。 |
| `qq_bot_secret` | str | `""` | 机器人 AppSecret，位于密钥表。 |
| `qq_bot_openid` | str | `""` | 机器人自身 OpenID，用于识别 @机器人。 |
| `qq_use_markdown` | bool | `false` | 是否启用 Markdown 消息。 |
| `qq_use_webhook` | bool | `false` | 是否使用 Webhook 接收事件。 |

## 必填凭据

- `qq_bot_appid` 与 `qq_bot_secret`：在 QQ 开放平台机器人管理页获取，两者共同确定一个机器人账号。
- `qq_bot_openid`：选填；机器人自身的 OpenID，群聊中识别 @机器人 时使用。
- `qq_bot_certified`：选填；机器人是否已通过企业或个人认证，未认证时主动消息配额更低。
- `qq_bot_uid` 与 `qq_bot_qqnum`：选填；会话数据中携带的机器人 UID 与 QQ 号，按平台提供的信息填写。

## 监听地址与端口

仅在 `qq_use_webhook = true` 时监听：

- 地址 `qq_webhook_host`，默认 `0.0.0.0`。
- 端口 `qq_webhook_port`，默认 `8080`。
- 路径 `qq_webhook_path`，默认 `/`，须与开放平台配置的回调地址一致。

Webhook 模式由平台回调驱动，适配器只提供 HTTP，公网 HTTPS 由反向代理终止。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 附件按类型转换。 |
| Markdown | 视配置 | 由 `qq_use_markdown` 控制；服务器频道始终按纯文本发送。 |
| 按钮与动作文本 | 视配置 | 仅在启用 Markdown 时可用。 |
| 表情回应 | 不支持 | — |
| 引用回复 | 支持 | — |
| 输入状态 | 支持 | 通过挂载回应表情表示正在处理。 |
| 消息撤回 | 支持 | — |
| 群组管理 | 不支持 | — |
| 权限组 | 部分支持 | 服务器频道支持，群聊与私信不支持。 |
| 消息节点 | 视配置 | 仅在启用 Markdown 时可用。 |
| 私信 | 支持 | C2C 与频道私信均标记为私密。 |
| RSS 推送 | 支持 | 群聊 @ 消息的能力集关闭 RSS。 |

## 私信与群聊

- 群聊目标前缀为 `QQBot|Group`，C2C 私信为 `QQBot|C2C`，服务器频道为 `QQBot|Guild`，频道私信为 `QQBot|Direct`。
- 群聊中 @机器人 的消息始终处理；未获「读取全部消息」权限时平台不推送其他群消息，获得权限后普通群消息同样处理。
- 群聊 @ 消息使用受限能力集，关闭 RSS 与全量消息读取。
- 开启 Markdown 后，用户仍可在会话中关闭 Markdown 渲染，届时按钮、动作文本与消息节点一并停用。
- `qq_private_bot = true` 时按私域机器人订阅服务器全量消息事件。
- 同一回调重复投递的消息会按消息 ID 去重。

## 外部依赖

- QQ 开放平台 API 与事件推送。
- 可选 S3 兼容对象存储：Markdown 图片上传失败时作为回退外链。
- Webhook 模式需要公网可达的 HTTPS 反向代理。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
