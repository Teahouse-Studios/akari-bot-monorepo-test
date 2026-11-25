---
title: 安装与开发
---

# mcv-rss：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-mcv_rss
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `mcv-rss` | `mcv_rss`、`mcvrss` | Java 版正式版与快照推送 |
| `mcbv-rss` | `mcbv_rss`、`mcbvrss` | 基岩版商店版本推送 |

若需要在会话中接收推送，管理员可以在会话中执行 `module enable mcv-rss` 或 `module enable mcbv-rss` 启用对应模块。仅启用了对应模块的会话才会收到推送消息。

## 配置项

<ModuleConfig />

## 权限与平台能力

两个模块均不提供聊天命令，仅向启用了对应模块的会话推送。场景管理员负责启用模块。两个模块均声明了 `rss=True`，未声明平台限制。

`mcv-rss` 若需要获取更新日志页面，需要在 core 配置中开启 `webrender.enable`。推送更新日志还要求目标会话启用 `minecraft-news` 模块。`mcbv-rss` 在出口 IP 所属国家为 `China`，或尚未探测到国家时，本轮不执行推送。

## 首轮轮询

启用后的首轮轮询不会补发已经发布的版本。

`mcv-rss` 首轮仅记录当前版本并缓存更新日志标题，不推送消息。

`mcbv-rss` 首轮既不记录版本，也不推送消息。下一轮仍检测到未记录的版本时才会发送。

## 数据表

<ModuleData />

版本记录写入 core 的 `stored_data` 数据表中。`<客户端名>|mcv_rss` 保存 Java 版正式版与快照，`<客户端名>|mcbv_rss` 保存基岩版正式版。`<客户端名>|mcnews` 保存已处理的更新日志标题，与 `minecraft_news` 共用。

## 依赖与外部服务

运行依赖 <PackageDependencies package="akari-bot-module-mcv_rss" />。外部服务为 `piston-meta.mojang.com`、`www.minecraft.net` 与 Google Play。

`piston-meta.mojang.com` 提供版本清单，`www.minecraft.net` 的更新日志页面通过 WebRender 获取，`com.mojang.minecraftpe` 的版本号来自 Google Play。`mcv-rss` 每 60 秒读取一次版本清单，`mcbv-rss` 每 180 秒读取一次 Google Play 版本号。
