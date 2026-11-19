# Satori 适配器

Satori 适配器实现 Satori 协议，接入 Satori 服务端。具体平台的消息与会话由服务端转接。

## 平台概述

适配器通过 WebSocket 连接 Satori 服务端，按事件接收消息，按接口发送消息。会话标识以 `Satori|Channel` 与 `Satori|Private` 两种前缀区分群组与私聊场景。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-satori
```

安装后由守护进程按配置启动，启动条件为 `bot_satori.enable = true`。

## 配置

配置表为 `bot_satori`，密钥表为 `bot_satori_secret`，两张表同处 `config/bot_satori.toml`。

配置项如下：

| 字段 | 说明 |
| --- | --- |
| `satori_host` | 服务端地址，默认 `127.0.0.1` |
| `satori_port` | 服务端端口，默认 `5140` |
| `satori_path` | 连接路径，为空时按协议默认值 |
| `satori_secure` | 是否使用 TLS 连接 |
| `satori_token` | 访问令牌，写入 secret 表 |
| `satori_admin_roles` | 视为管理员的角色名，默认 `admin`、`owner` |
