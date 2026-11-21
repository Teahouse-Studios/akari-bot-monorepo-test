# Discord 适配器

Discord 适配器以机器人身份连接 Discord，接收服务器频道消息、私信、表情回应和成员变动事件。

## 平台概述

适配器通过 Discord Bot Gateway 建立长连接。消息按频道划分场景，私信会话标记为私密。

机器人启动时注册斜杠命令。用户在频道或私信中使用斜杠命令，机器人按普通命令处理。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-discord
```

安装后由守护进程按配置启动。`bot_discord.enable = true` 时启动。

## 配置

配置表为 `bot_discord`，密钥表为 `bot_discord_secret`。两张表都写在 `config/bot_discord.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add discord <实例 ID>` 新增实例。实例表名为 `bot_discord-<实例 ID>`，密钥表名为 `bot_discord-<实例 ID>_secret`。两张表都写在 `config/bot_discord-<实例 ID>.toml`。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Discord 客户端。 |

密钥表字段：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `discord_token` | str | `""` | Discord 机器人令牌。 |

写入示例：

```sh
akaribot config set enable true --table bot_discord
akaribot config set discord_token <令牌> --table bot_discord_secret
```

## 必填信息

- `discord_token`：在 Discord Developer Portal 的 Bot 页面获取。
- 在开发者门户的 Bot 页面开启 Message Content Intent 与 Server Members Intent。不开时机器人收不到消息正文与成员事件。
- 机器人需要读取频道、发送消息、管理消息和添加表情回应的权限。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 附件按类型转换为对应消息元素。 |
| Markdown | 支持 | 不支持表格、代码块等扩展。 |
| 按钮与动作文本 | 支持 | 通过消息组件交互。 |
| 表情回应 | 支持 | 用户添加回应可触发命令处理。 |
| 引用回复 | 支持 | 保留被回复消息的 ID。 |
| 输入状态 | 支持 | 处理期间显示正在输入。 |
| 消息撤回 | 支持 | 按消息 ID 删除。 |
| 群组管理 | 支持 | 含禁言、踢出与封禁。 |
| 权限组 | 支持 | — |
| 消息节点 | 不支持 | — |
| 私信 | 支持 | 私信会话标记为私密。 |
| RSS 推送 | 支持 | — |

## 私信与群聊

- 服务器频道的目标前缀是 `Discord|Channel`。
- 私信的目标前缀是 `Discord|DM|Channel`。
- 服务器事件的目标前缀是 `Discord|Guild`。
- 私信不需要 @机器人。频道消息是否必须 @机器人由 core 的 `mention_required` 控制。
- 机器人忽略自身和其他机器人发送的消息。

## 外部依赖

- Discord API 与 Gateway。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
