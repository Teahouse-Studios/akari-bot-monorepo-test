# KOOK 适配器

KOOK 适配器以机器人身份连接 KOOK 开放平台，接入服务器频道、私聊和成员事件。

## 平台概述

适配器通过 KOOK 开放平台网关建立长连接。消息来自服务器频道或私聊，频道消息按 KOOK Markdown（KMD）解析。

服务器成员的加入和退出事件由网关推送。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-kook
```

安装完成后，守护进程按配置启动适配器。当 `bot_kook.enable = true` 时启动服务。

## 配置

配置表为 `bot_kook`，密钥表为 `bot_kook_secret`。两张表均保存在 `config/bot_kook.toml` 中。

需要多个机器人账号时，可使用 `akaribot adapter instance add kook <实例 ID>` 新增实例。实例表名为 `bot_kook-<实例 ID>`，密钥表名为 `bot_kook-<实例 ID>_secret`。两张表均保存在 `config/bot_kook-<实例 ID>.toml` 中。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 KOOK 客户端。 |

密钥表字段：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `kook_token` | str | `""` | KOOK 机器人令牌。 |

写入示例：

```sh
akaribot config set enable true --table bot_kook
akaribot config set kook_token <令牌> --table bot_kook_secret
```

## 必填信息

- `kook_token`：在 KOOK 开发者平台的机器人页面获取。
- 首先将机器人邀请至目标服务器。机器人需要读取消息、发送消息以及撤回消息的权限。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 发送支持三类媒体，入站处理文本与图片。 |
| Markdown | 支持 | 使用 KMD 渲染，链接按 Markdown 格式发送。 |
| 按钮与动作文本 | 不支持 | — |
| 表情回应 | 支持 | 频道与私聊的回应事件均可触发命令处理。 |
| 引用回复 | 支持 | — |
| 输入状态 | 不支持 | — |
| 消息撤回 | 支持 | — |
| 群组管理 | 不支持 | — |
| 权限组 | 支持 | — |
| 消息节点 | 不支持 | — |
| 私信 | 支持 | 私聊会话标记为私密。 |
| RSS 推送 | 支持 | — |

发送前的内容审核由 core 配置 `config.enable_dirty_check` 控制。

## 私信与群聊

- 服务器频道的目标前缀是 `KOOK|Group`。
- 私聊的目标前缀是 `KOOK|Person`。
- 服务器事件的目标前缀是 `KOOK|Guild`。
- 私聊不需要 @机器人。频道消息是否必须 @机器人由 core 的 `config.mention_required` 控制。
- 频道消息仅处理文本和图片。

## 外部依赖

- KOOK 开放平台 API 与 Gateway。
- 出站连接读取 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
