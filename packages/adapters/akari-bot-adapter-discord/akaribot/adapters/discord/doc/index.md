# Discord 适配器

以机器人身份连接 Discord，接收服务器频道消息、私信、表情回应与成员变动事件。

## 平台概述

适配器通过 Discord Bot Gateway 建立长连接，主动向 Discord 发起连接，不监听本地端口。消息以频道为场景，私信单独标记；斜杠命令在启动时注册，用户在频道或私信中触发后转换为普通命令处理。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-discord
```

安装后由守护进程按配置启动，启动条件为 `bot_discord.enable = true`。

## 配置

配置表为 `bot_discord`，密钥表为 `bot_discord_secret`，两张表同处 `config/bot_discord.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add discord <实例 ID>` 新增实例；实例表名为 `bot_discord-<实例 ID>`，密钥表名为 `bot_discord-<实例 ID>_secret`，两张表同处 `config/bot_discord-<实例 ID>.toml`。

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

## 必填凭据

- `discord_token`：在 Discord Developer Portal 的 Bot 页面获取。
- 开发者门户中须开启 Message Content Intent 与 Server Members Intent，否则收不到消息正文与成员事件。
- 机器人需具备读取频道、发送消息、管理消息与添加表情回应的权限。

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

- 服务器频道目标前缀为 `Discord|Channel`，私信为 `Discord|DM|Channel`，服务器事件使用 `Discord|Guild`。
- 私信不要求 @机器人；群聊是否必须 @ 由 core 配置 `mention_required` 决定。
- 机器人忽略自身与其他机器人发送的消息。

## 外部依赖

- Discord API 与 Gateway。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
