---
title: 安装与开发
---

# mcv-rss：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mcv_rss
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `mcv-rss` | `mcv_rss`、`mcvrss` | Java 版正式版与快照推送 |
| `mcbv-rss` | `mcbv_rss`、`mcbvrss` | 基岩版商店版本推送 |

按需在会话中由管理员用 `module enable mcv-rss` 或 `module enable mcbv-rss` 开启。只有启用了对应模块的会话会收到消息。

## 配置项

<ModuleConfig />

## 权限与平台能力

模块没有命令，推送目标为启用了对应模块的会话，启用操作由场景管理员完成。两个模块均声明 `rss=True`，未声明平台限制。`mcv-rss` 抓取更新日志页面需在 core 配置中开启 `webrender.enable`，投递更新日志需目标会话启用 `minecraft-news` 模块；`mcbv-rss` 在出口 IP 国家为 `China` 或尚未探测到国家时跳过本轮。

## 数据表

<ModuleData />

已记录版本写入 core 的 `stored_data`：`<客户端名>|mcv_rss` 存已记录的 Java 版正式版与快照，`<客户端名>|mcbv_rss` 存已记录的基岩版正式版，`<客户端名>|mcnews` 存已处理的更新日志标题，与 `minecraft_news` 共用。

## 依赖与外部服务

运行依赖 `akari-bot-core`、`beautifulsoup4>=4.11.1,<5.0.0`、`google-play-scraper>=1.2.2,<2.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `piston-meta.mojang.com`（版本清单）、`www.minecraft.net`（更新日志页面，经 WebRender）与 Google Play（`com.mojang.minecraftpe` 版本号）。`mcv-rss` 每 60 秒读取一次版本清单，`mcbv-rss` 每 180 秒读取一次 Google Play 版本号。
