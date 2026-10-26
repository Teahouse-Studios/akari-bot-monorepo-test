# Matrix 适配器

以机器人账号登录 Matrix 家服务器，通过客户端同步协议接收房间消息。

## 平台概述

适配器使用访问令牌恢复登录，持续同步房间事件，不监听本地端口。房间邀请会自动接受，房间消息、成员变动与表情回应转换为会话事件；消息编辑与 `m.notice` 消息被忽略。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-matrix
```

安装后由守护进程按配置启动，启动条件为 `bot_matrix.enable = true`。

## 配置

配置表为 `bot_matrix`，密钥表为 `bot_matrix_secret`，两张表同处 `config/bot_matrix.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add matrix <实例 ID>` 新增实例；实例表名为 `bot_matrix-<实例 ID>`，密钥表名为 `bot_matrix-<实例 ID>_secret`，两张表同处 `config/bot_matrix-<实例 ID>.toml`。

主要字段如下，完整字段与默认值见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Matrix 客户端。 |
| `matrix_homeserver` | str | `https://matrix.org` | 家服务器地址。 |
| `matrix_user` | str | `@akaribot:matrix.org` | 机器人完全限定用户 ID。 |
| `matrix_token` | str | `""` | 访问令牌，位于密钥表。 |
| `matrix_device_id` | str | `""` | 设备 ID，位于密钥表。 |

## 必填凭据

- `matrix_homeserver`：机器人账号所属家服务器，末尾不要带斜杠。
- `matrix_user`：形如 `@name:server` 的完全限定用户 ID。
- `matrix_token` 与 `matrix_device_id`：同一登录会话的访问令牌与设备 ID，两者须来自同一设备。
- `matrix_device_name` 可任意填写，启动时会同步为设备显示名。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 按 `m.image`、`m.audio`、`m.video` 转换。 |
| Markdown | 不支持 | 消息按纯文本发送。 |
| 按钮与动作文本 | 不支持 | — |
| 表情回应 | 支持 | `m.reaction` 触发命令处理。 |
| 引用回复 | 支持 | 支持富回复与线程根消息。 |
| 输入状态 | 不支持 | — |
| 消息撤回 | 支持 | 通过 redact 删除消息。 |
| 群组管理 | 不支持 | — |
| 权限组 | 不支持 | — |
| 消息节点 | 不支持 | — |
| 私信 | 支持 | 私信通过仅含双方的房间发送。 |
| RSS 推送 | 支持 | — |

## 私信与群聊

- 所有入站消息的目标前缀均为 `Matrix|Room`，按房间场景处理。
- 私信没有独立通道：发送私信时先查找与用户的直聊房间，不存在则创建。
- 房间消息以机器人完整用户 ID 开头时视为 @机器人；是否必须 @ 由 core 配置 `mention_required` 决定。

## 外部依赖

- Matrix 家服务器。
- 可选端到端加密：运行环境具备 olm 时启用；在此前提下设置 `matrix_megolm_backup_passphrase`，关闭时会导出 Megolm 密钥备份至 `data/private/matrix/megolm_backup/`。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
