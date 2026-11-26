# Satori 适配器

Satori 适配器通过 Satori 服务端接入多个平台，覆盖群聊与私信。具体平台的消息与会话由服务端转接。

## 平台概述

适配器以 WebSocket 连接 Satori 服务端，持续接收事件，并通过服务端接口发送消息。

消息内容按 Satori 消息元素解析，图片、音频与视频转换为对应的消息元素。引用会保留为回复目标。

可用的平台取决于服务端登录的账号。同一服务端上的多个平台账号可同时在线。

群聊目标前缀为 `Satori|Channel`，私信目标前缀为 `Satori|Private`。两个前缀均属于 `Satori` 客户端身份。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-satori
```

安装完成后由守护进程按配置启动。当 `bot_satori.enable = true` 时启动服务。

## 配置

配置表为 `bot_satori`，密钥表为 `bot_satori_secret`。两张表均保存在 `config/bot_satori.toml` 中。

需要连接多个 Satori 服务端时，可使用 `akaribot adapter instance add satori <实例 ID>` 新增实例。实例表名为 `bot_satori-<实例 ID>`，密钥表名为 `bot_satori-<实例 ID>_secret`。两张表均保存在 `config/bot_satori-<实例 ID>.toml` 中。

两个已启用的实例填写相同且非空的 `satori_token` 时，守护进程会中止启动。

主要字段如下，完整字段与默认值参见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Satori 客户端。 |
| `satori_host` | str | `127.0.0.1` | Satori 服务端的主机名或 IP。 |
| `satori_port` | int | `5140` | Satori 服务端的端口。 |
| `satori_token` | str | `""` | 服务端的访问令牌，位于密钥表。 |
| `satori_enable_listening_self_message` | bool | `false` | 是否监听机器人自身消息。 |
| `satori_admin_roles` | list | `["admin", "owner"]` | 视为管理员的角色 ID 或名称。 |

## 必填信息

- `satori_token`：服务端启用鉴权时填写，取值与服务端配置一致。未启用鉴权时留空。

## 连接方式

适配器仅发起出站连接，目标为 `satori_host:satori_port`，默认为 `127.0.0.1:5140`。

- `satori_secure` 为 `true` 时使用 TLS 连接。
- `satori_path` 填写服务端的路径前缀。服务端位于反向代理的 `/satori` 路径下时，填写 `satori`。
- 启动时等待服务端账号上线，最长 120 秒。服务端没有可用账号时启动失败。
- 连接断开后按递增的间隔重连。
- 鉴权失败、服务端关闭连接或重连次数耗尽时，适配器退出。守护进程重新启动适配器。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 转换为图片、音频与视频消息元素，本地文件先上传至服务端。 |
| Markdown | 不支持 | 消息按纯文本发送。 |
| 按钮与动作文本 | 不支持 | — |
| 表情回应 | 支持 | 用于表示处理状态。回应事件不触发命令。 |
| 引用回复 | 支持 | 发送时引用触发消息。 |
| 输入状态 | 支持 | 在群聊的触发消息上添加回应表情。 |
| 消息撤回 | 支持 | 群聊与私信均可撤回。 |
| 群组管理 | 支持 | 包含禁言、踢出与封禁。 |
| 权限组 | 支持 | 通过服务器角色实现，接受角色 ID 或名称。 |
| 消息节点 | 不支持 | 消息节点由框架渲染为图片后发送。 |
| 私信 | 支持 | 私聊频道按需创建。 |
| RSS 推送 | 支持 | — |

链接管理与内容审核分别由 core 的 `config.enable_urlmanager` 与 `config.enable_dirty_check` 两个配置项控制。

## 私信与群聊

- 群聊的目标前缀为 `Satori|Channel`，私信的目标前缀为 `Satori|Private`。场景 ID 中包含平台名称，例如 `Satori|Channel|qq|<服务器 ID>|<频道 ID>`。
- 适配器首次发送私信时请求服务端创建私聊频道，并缓存返回的频道 ID。
- 群聊消息以 @机器人开头时视为对机器人的指令。是否必须 @机器人由 core 的 `mention_required` 控制。
- 以 @其他成员开头的群聊消息不进入处理流程。
- 群聊消息以 @机器人开头且没有其他内容时，按帮助命令 `~help` 处理。
- 机器人默认不处理自身与其他机器人发送的消息。启用 `satori_enable_listening_self_message` 后，机器人也会处理自身消息。
- 启用 core 的 `config.enable_tos` 后，机器人被移出服务器时会写入违规记录，相关场景会被封禁。

## 外部依赖

- 可用的 Satori 服务端及其已登录的平台账号。
- 图片上传、消息撤回与禁言等操作仅在服务端与接入的平台支持对应接口时可用。
