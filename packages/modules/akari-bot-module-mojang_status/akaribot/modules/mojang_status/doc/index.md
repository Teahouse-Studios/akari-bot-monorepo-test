# Mojang 服务状态

依次探测 Mojang 账号、会话与 Minecraft 服务三个后端接口，按接口应答汇总各服务的在线情况。

模块名 `mojang-status`，别名 `mojang_status`、`mcstatus`、`mjs`、`mjsb`。

## 安装

```bash
akaribot module add akari-bot-module-mojang_status
```

安装后在会话中由管理员用 `module enable mojang-status` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mojang-status` | 查询各 Mojang 服务的当前状态 | 所有用户 |

每次查询按固定顺序输出三项：

| 服务 | 对应接口 |
| --- | --- |
| 玩家信息 | `https://api.mojang.com` |
| 正版验证 | `https://sessionserver.mojang.com` |
| Mojang 服务 | `https://api.minecraftservices.com` |

状态取值为在线、离线或未知。接口返回 200 或 400 至 409 应答时判定为在线；错误值以 50 开头时显示离线；其余可识别异常显示未知；常规 HTTP 5xx 应答由框架按外部服务错误处理。每个接口只尝试一次，失败不重试。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 查询为串行请求，三项结果在一条消息内返回。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 外部服务：Mojang 账号接口、会话服务器接口与 Minecraft 服务接口。
