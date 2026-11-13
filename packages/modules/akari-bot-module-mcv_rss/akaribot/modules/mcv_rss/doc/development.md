---
title: 安装与开发
---

# mcv-rss：安装与开发

本文将会介绍 `mcv-rss` 与 `mcbv-rss` 的安装、配置、数据表与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcv_rss
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `mcv-rss` | `mcv_rss`、`mcvrss` | Java 版正式版与快照推送 |
| `mcbv-rss` | `mcbv_rss`、`mcbvrss` | 基岩版商店版本推送 |

需要接收推送的会话，请让管理员执行 `module enable mcv-rss` 或 `module enable mcbv-rss` 开启对应模块。只有启用了模块的会话才会收到消息。

## 配置项

<ModuleConfig />

## 权限与平台能力

两个模块都没有命令，只向启用了对应模块的会话推送。场景管理员负责开启模块。两个模块都声明了 `rss=True`，未声明平台限制。

`mcv-rss` 要抓取更新日志页面，需要在 core 配置里开启 `webrender.enable`。推送更新日志还需要目标会话启用 `minecraft-news` 模块。`mcbv-rss` 在出口 IP 所属国家为 `China`，或尚未探测到国家时，本轮不推送。

## 数据表

<ModuleData />

版本记录写入 core 的 `stored_data`。`<客户端名>|mcv_rss` 保存 Java 版正式版与快照，`<客户端名>|mcbv_rss` 保存基岩版正式版。`<客户端名>|mcnews` 保存已处理的更新日志标题，与 `minecraft_news` 共用。

## 依赖与外部服务

运行依赖 `akari-bot-core`、`beautifulsoup4>=4.11.1,<5.0.0`、`google-play-scraper>=1.2.2,<2.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `piston-meta.mojang.com`、`www.minecraft.net` 与 Google Play。

`piston-meta.mojang.com` 提供版本清单，`www.minecraft.net` 的更新日志页面由 WebRender 抓取，`com.mojang.minecraftpe` 的版本号来自 Google Play。`mcv-rss` 每 60 秒读取一次版本清单，`mcbv-rss` 每 180 秒读取一次 Google Play 版本号。
