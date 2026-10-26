# Minecraft 版本推送

定时检测 Minecraft：Java 版启动器与基岩版商店版本，发现新版本时向启用了对应模块的会话推送。
包内注册两个 RSS 模块：`mcv-rss` 与 `mcbv-rss`，均不提供聊天命令。

## 安装

```bash
akaribot module add akari-bot-module-mcv_rss
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `mcv-rss` | `mcv_rss`、`mcvrss` | Java 版正式版与快照推送 |
| `mcbv-rss` | `mcbv_rss`、`mcbvrss` | 基岩版商店版本推送 |

按需在会话中由管理员用 `module enable mcv-rss` 或 `module enable mcbv-rss` 开启。只有启用了对应
模块的会话会收到消息。

## 命令

模块没有注册 `command()` 或 `regex()`。消息由定时任务触发：

- `mcv-rss` 每 60 秒读取 `piston-meta.mojang.com` 的版本清单，登记新的 release 与 snapshot。
- `mcbv-rss` 每 180 秒读取 Google Play 的 `com.mojang.minecraftpe` 版本号，登记新的正式版。

发现新版本时，`mcv-rss` 向对应会话推送版本号、记录时间与推送时间；`mcbv-rss` 推送版本号。
`mcv-rss` 还会按版本号构造 `minecraft.net` 更新日志地址，标题未记录时向 `minecraft-news` 模块
推送更新日志链接，并把标题写入与 `minecraft_news` 共用的记录。

启动静默：`mcv-rss` 首次成功轮询只登记当前版本与更新日志标题，不发送消息；`mcbv-rss` 首轮只解除
静默标志，不登记也不推送，下一轮若仍检测到未记录版本则发送。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 模块没有命令；推送目标为启用了对应模块的会话，启用操作由场景管理员完成。
- 两个模块均声明 `rss=True`，未声明平台限制。
- `mcv-rss` 抓取更新日志页面需在 core 配置中开启 `webrender.enable`；投递更新日志需目标会话启用
  `minecraft-news` 模块。
- `mcbv-rss` 在出口 IP 国家为 `China` 或尚未探测到国家时跳过本轮。

## 数据表

manifest 未声明 `owned_tables`，模块不拥有数据表。已记录版本写入 core 的 `stored_data`：

- `<客户端名>|mcv_rss`：已记录的 Java 版正式版与快照。
- `<客户端名>|mcbv_rss`：已记录的基岩版正式版。
- `<客户端名>|mcnews`：已处理的更新日志标题，与 `minecraft_news` 共用。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`beautifulsoup4>=4.11.1,<5.0.0`、`google-play-scraper>=1.2.2,<2.0.0`、
  `orjson>=3.10.9,<4.0.0`。
- 外部服务：`piston-meta.mojang.com`（版本清单）、`www.minecraft.net`（更新日志页面，经 WebRender）、
  Google Play（基岩版版本号）。
