# Telegram 适配器

Telegram 适配器以机器人身份接入 Telegram 私聊、群组、超级群组与频道。

## 平台概述

适配器通过 Telegram Bot API 长轮询接收更新，不需要公网地址或本地端口。

消息按聊天类型区分场景，支持文本、图片、音频、视频与文档。按钮回调与行内查询均作为命令处理。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-telegram
```

安装后由守护进程按配置启动。`bot_telegram.enable = true` 时启动。

## 配置

配置表为 `bot_telegram`，密钥表为 `bot_telegram_secret`。两张表均保存在 `config/bot_telegram.toml`。

需要多个机器人账号时，可使用 `akaribot adapter instance add telegram <实例 ID>` 新增实例。实例表名为 `bot_telegram-<实例 ID>`，密钥表名为 `bot_telegram-<实例 ID>_secret`。两张表均保存在 `config/bot_telegram-<实例 ID>.toml`。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Telegram 客户端。 |
| `telegram_api_url` | str | `""` | 自定义 Bot API 地址，留空使用官方地址。 |

密钥表字段：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `telegram_token` | str | `""` | Telegram 机器人令牌。 |

写入示例：

```sh
akaribot config set enable true --table bot_telegram
akaribot config set telegram_token <令牌> --table bot_telegram_secret
```

## 必填信息

- `telegram_token`：由 BotFather 创建机器人后获得。
- 机器人需要在目标群组内，并具备读取消息、发送消息、删除消息与限制成员的权限。
- 使用自建 Bot API 服务时填写 `telegram_api_url`，该地址作为 API 基础地址。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 文档按 MIME 类型归入图片、音频或视频。 |
| Markdown | 不支持 | 消息按纯文本发送。 |
| 按钮与动作文本 | 支持 | 按钮回调与行内查询均可触发命令。 |
| 表情回应 | 不支持 | — |
| 引用回复 | 支持 | 保留被回复消息的 ID。 |
| 输入状态 | 不支持 | — |
| 消息撤回 | 支持 | — |
| 群组管理 | 支持 | 包含禁言、踢出与封禁。 |
| 权限组 | 不支持 | — |
| 消息节点 | 不支持 | — |
| 私聊 | 支持 | 私聊标记为私密。 |
| RSS 推送 | 支持 | — |

## 私聊与群聊

- 私聊的目标前缀是 `Telegram|Private`，群组是 `Telegram|Group`，超级群组是 `Telegram|Supergroup`，频道是 `Telegram|Channel`。
- 私聊不需要 @机器人。其他聊天是否必须 @机器人由 core 的 `mention_required` 控制。
- 匿名管理员的消息与以频道身份发言的消息均无用户来源，适配器直接予以忽略。

## 外部依赖

- Telegram Bot API，或通过 `telegram_api_url` 指定的自建 Bot API 服务。
- 出站连接读取 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
