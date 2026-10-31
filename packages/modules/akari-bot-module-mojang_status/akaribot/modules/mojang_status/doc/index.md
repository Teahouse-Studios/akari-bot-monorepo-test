# mojang-status

依次探测 Mojang 账号、会话与 Minecraft 服务三个后端接口，按接口应答汇总各服务的在线情况。

模块名 `mojang-status`，别名 `mojang_status`、`mcstatus`、`mjs`、`mjsb`。

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
