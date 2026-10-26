# Web 控制台适配器

在实例内启动 Web 服务，提供 WebUI 控制台与内置 API。

## 平台概述

适配器基于 FastAPI 与 uvicorn 启动 HTTP 服务，前端静态资源来自 `akari-bot-webui` 分发包或实例的 `data/webui/dist` 目录。控制台以单一会话连接机器人，可发送消息、查看配置、管理会话与文件、查看日志与统计数据。该适配器默认启用，不依赖任何平台账号。访问、认证与反向代理的完整说明见 [WebUI 控制台](webui.md)。

## 安装

在实例目录内执行：

```sh
akaribot module add akari-bot-adapter-web
```

适配器的 `enable` 默认为 `true`，安装后随守护进程启动。

## 配置

配置表为 `bot_web`，密钥表为 `bot_web_secret`，两张表同处 `config/bot_web.toml`。

需要多个 Web 服务实例时，用 `akaribot adapter instance add web <实例 ID>` 新增实例；实例表名为 `bot_web-<实例 ID>`，密钥表名为 `bot_web-<实例 ID>_secret`，两张表同处 `config/bot_web-<实例 ID>.toml`。

主要字段如下，完整字段与默认值见 [config.md](config.md)。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `true` | 是否启动 Web 服务。 |
| `web_host` | str | `127.0.0.1` | 监听地址，`0.0.0.0` 表示监听所有地址。 |
| `web_port` | int | `6485` | 监听端口，`0` 表示禁用服务。 |
| `enable_https` | bool | `false` | 访问地址是否使用 HTTPS。 |
| `jwt_secret` | str | `""` | 内置 API 的 JWT 签名密钥，位于密钥表。 |

## 监听地址与端口

- 默认监听 `127.0.0.1:6485`，WebUI 地址为 `http://127.0.0.1:6485/webui`。
- 端口被占用时从 `web_port` 起向后尝试，最多 100 个端口；没有可用端口时进程退出。
- `web_port = 0` 时直接禁用服务。
- `enable_https = true` 只改变访问地址的协议与 WebUI 配置，TLS 由反向代理终止。

## 认证

- 未设置密码时，登录接口直接签发令牌；应在首次访问后设置密码。
- 支持 Argon2 密码哈希、TOTP 两步验证与恢复代码。
- 令牌有效期 24 小时，修改密码后旧令牌失效。
- `login_max_attempt` 控制 10 分钟内的登录失败上限，超限后封禁来源 IP 1 小时。
- `jwt_secret` 为空时首次启动自动生成并写回配置。
- `allow_origins` 控制 CORS 来源；`forwarded_allow_ips` 指定可信反向代理。

## 平台能力

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 图片、音频、视频 | 支持 | 发送支持三类媒体；入站支持文本与图片。 |
| Markdown | 支持 | 支持渲染，用户可切换 Markdown 渲染。 |
| 按钮与动作文本 | 支持 | 控制台内交互。 |
| 表情回应 | 支持 | 控制台内回应。 |
| 引用回复 | 不支持 | — |
| 输入状态 | 支持 | — |
| 消息撤回 | 支持 | — |
| 群组管理 | 不支持 | — |
| 权限组 | 不支持 | — |
| 消息节点 | 支持 | — |
| 私信 | 支持 | 控制台会话为私密会话。 |
| RSS 推送 | 不支持 | — |

控制台不受场景级模块开关限制，`require_enable_modules` 为 `false`。

## 私信与群聊

- 目标固定为 `Web|Console|0`，发送者固定为 `Web|0`，会话按私密处理。
- `Web|0` 在服务启动时自动获得超级管理员身份。
- 不存在群聊场景；所有控制台消息进入同一会话。

## 外部依赖

- `akari-bot-webui` 提供 WebUI 静态资源；实例内存在 `data/webui/dist` 时优先使用该目录。
- uvicorn 提供 HTTP 服务；公网部署时由反向代理终止 TLS。
