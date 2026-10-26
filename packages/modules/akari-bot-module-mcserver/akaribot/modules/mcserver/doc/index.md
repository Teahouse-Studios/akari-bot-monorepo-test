# Minecraft 服务器状态

查询 Minecraft：Java 版与基岩版服务器的 MOTD、在线人数、版本与游戏模式。模块名 `mcserver`，别名
`server`。

## 安装

```bash
akaribot module add akari-bot-module-mcserver
```

安装后在会话中由管理员用 `module enable mcserver` 开启。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcserver <address:port> [-r] [-p]` | 查询服务器状态 | 所有用户 |

- `<address:port>` 为服务器地址，可带端口；省略端口时 Java 版使用 25565，基岩版使用 19132。
- `-r` 保留原始格式，返回内容不去除 `§` 颜色代码。
- `-p` 在 Java 版结果中附加在线玩家名单；基岩版查询不返回名单。

命令并行查询 Java 版与基岩版，任一版本有响应就发送该版本结果；两个版本都没有响应时返回未找到。
Java 版查询会解析 SRV 记录，并在超时后改用 `motd.wd-api.com` 的 HTTP 接口；基岩版同样在超时后回落
该服务。`localhost`、`192.168.*`、`172.16.*` 至 `172.31.*`、`10.*`、`127.*` 与 `0.0.0.0` 被视
为本地地址并直接拒绝。

发送前，Java 版与基岩版的结果分别经过 core 的内容安全检查。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 查询直接连接目标服务器，网络需允许访问对应端口；超时回落时需可访问 `motd.wd-api.com`。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`mcstatus>=14.1.0,<14.2.0`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：目标 Minecraft 服务器（Java 版协议与基岩版 RakNet 查询）、`motd.wd-api.com` 超时回落接口。
