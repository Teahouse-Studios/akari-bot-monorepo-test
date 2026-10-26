# Milky 适配器

通过 Milky 协议端连接 QQ，接入群聊、私信与好友、群邀请事件。

## 平台概述

适配器作为 HTTP 客户端连接 Milky 协议端，订阅事件流并调用协议端接口收发消息，不监听本地端口。事件流断开后每隔 5 秒重连。群聊与私信分别归属 `QQ|Group` 与 `QQ|Private` 前缀，两个前缀同属 `QQ` 客户端身份。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-milky
```

安装后由守护进程按配置启动，启动条件为 `bot_milky.enable = true`。

## 配置

配置表为 `bot_milky`，密钥表为 `bot_milky_secret`，两张表同处 `config/bot_milky.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add milky <实例 ID>` 新增实例；实例表名为 `bot_milky-<实例 ID>`，密钥表名为 `bot_milky-<实例 ID>_secret`，两张表同处 `config/bot_milky-<实例 ID>.toml`。

主要字段如下，完整字段与默认值见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Milky 客户端。 |
| `qq_host` | str | `http://127.0.0.1:8080` | Milky 协议端 HTTP 服务地址。 |
| `qq_access_token` | str | `""` | 协议端访问令牌，位于密钥表。 |
| `qq_enable_temp_session` | bool | `true` | 是否处理临时会话。 |
| `qq_enable_listening_self_message` | bool | `false` | 是否监听机器人自身消息。 |

## 必填凭据

- `qq_host`：Milky 协议端 HTTP 服务的基地址，未写协议时按 `http://` 处理。
- `qq_access_token`：协议端要求鉴权时填写，与协议端配置一致。

## 监听地址与端口

适配器不监听端口，全部连接由 `qq_host` 主动发起。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | — |
| Markdown | 不支持 | 消息按纯文本发送。 |
| 按钮与动作文本 | 不支持 | — |
| 表情回应 | 支持 | 仅群聊可用。 |
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
- 好友请求与群邀请默认仅对超级管理员与受信用户自动同意，其余请求分别由 `qq_allow_approve_friend` 与 `qq_allow_approve_group_invite` 控制。

## 外部依赖

- 可用的 Milky 协议端及其 HTTP 服务。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
