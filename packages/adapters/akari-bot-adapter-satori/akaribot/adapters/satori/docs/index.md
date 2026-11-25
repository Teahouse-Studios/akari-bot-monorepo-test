# Satori 适配器

Satori 适配器实现 Satori 协议，连接 Satori 服务端。具体平台的消息与会话由服务端转接。

## 平台概述

适配器通过 WebSocket 连接 Satori 服务端，按事件接收消息，按接口发送消息。

会话标识使用 `Satori|Channel` 与 `Satori|Private` 两种前缀区分群组和私聊场景。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-satori
```

安装后由守护进程按配置启动。`bot_satori.enable = true` 时启动。

## 配置

配置表为 `bot_satori`，密钥表为 `bot_satori_secret`。两张表均保存在 `config/bot_satori.toml`。

配置项如下：

| 字段 | 说明 |
| --- | --- |
| `enable` | 是否启动 Satori 客户端，默认 `false` |
| `satori_host` | 服务端地址，默认 `127.0.0.1` |
| `satori_port` | 服务端端口，默认 `5140` |
| `satori_path` | 连接路径，为空时按协议默认值 |
| `satori_secure` | 是否使用 TLS 连接 |
| `satori_timeout` | API 请求超时时间，单位为 s，默认 `30` |
| `satori_enable_listening_self_message` | 是否监听机器人自身消息，默认 `false` |
| `satori_token` | 访问令牌，位于密钥表 |
| `satori_admin_roles` | 视为管理员的角色名，默认 `admin`、`owner` |
| `satori_typing_emoji` | 处理消息时添加的反应表情，默认 `⌛` |
| `satori_limited_emoji` | 处理出错时添加的反应表情，默认 `❌` |
