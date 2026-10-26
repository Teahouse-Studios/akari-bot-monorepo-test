# KOOK 适配器

以机器人身份连接 KOOK 开放平台，接入服务器频道、私聊与成员事件。

## 平台概述

适配器通过 KOOK 开放平台网关建立长连接，不监听本地端口。消息以服务器频道或私聊为场景，频道消息按 KOOK Markdown（KMD）解析；服务器成员加入与退出等事件由网关推送。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-kook
```

安装后由守护进程按配置启动，启动条件为 `bot_kook.enable = true`。

## 配置

配置表为 `bot_kook`，密钥表为 `bot_kook_secret`，两张表同处 `config/bot_kook.toml`。

需要多个机器人账号时，用 `akaribot adapter instance add kook <实例 ID>` 新增实例；实例表名为 `bot_kook-<实例 ID>`，密钥表名为 `bot_kook-<实例 ID>_secret`，两张表同处 `config/bot_kook-<实例 ID>.toml`。

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

## 必填凭据

- `kook_token`：在 KOOK 开发者平台的机器人页面获取。
- 机器人须已邀请至目标服务器，并具备读取消息、发送消息与撤回消息的权限。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 发送支持三类媒体；入站处理文本与图片。 |
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

- 服务器频道目标前缀为 `KOOK|Group`，私聊为 `KOOK|Person`，服务器事件使用 `KOOK|Guild`。
- 私聊不要求 @机器人；频道消息是否必须 @ 由 core 配置 `mention_required` 决定。
- 频道消息仅处理文本与图片类型。

## 外部依赖

- KOOK 开放平台 API 与 Gateway。
- 出站连接遵循 core 的 `secret.proxy` 与 `config.proxy_disable_ssl` 设置。
