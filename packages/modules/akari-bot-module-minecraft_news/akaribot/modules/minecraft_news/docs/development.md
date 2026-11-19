---
title: 安装与开发
---

# minecraft-news：安装与开发

本文将会介绍这两个模块的安装、配置、数据表与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-minecraft_news
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `minecraft-news` | `minecraft_news`、`minecraftnews`、`mcnews` | 官网新闻推送 |
| `feedback-news` | `feedback_news`、`feedbacknews` | Feedback 更新记录推送 |

要开启对应模块，请让管理员在需要的会话中执行 `module enable minecraft-news` 或 `module enable feedback-news`。两个模块互相声明对方为推荐模块，启用其中一个时会提示启用另一个。

## 配置项

<ModuleConfig />

## 权限与平台能力

两个模块都没有命令，推送目标是启用了对应模块的会话，启用操作由场景管理员完成。两个模块都声明了 `rss=True`，未声明平台限制。

`minecraft-news` 读取文章 JSON 与封面图需要开启 `webrender.enable`，平台还需要支持图片消息才能显示封面。`feedback-news` 使用普通 HTTP 请求，每个分区只尝试一次，失败后等待下一周期。

## 数据表

<ModuleData />

已记录的数据写入 core 的 `stored_data`。`<客户端名>|mcnews` 保存 `minecraft-news` 已记录的文章标题，`mcv_rss` 的更新日志标题也写入此键。`<客户端名>|mcfeedbacknews` 保存 `feedback-news` 已记录的文章名称。

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `www.minecraft.net` 与 `minecraftfeedback.zendesk.com`。

`www.minecraft.net` 提供新闻文章的 JSON 与封面图，`minecraftfeedback.zendesk.com` 提供两个帮助中心分区（beta 与 article，每次各读取 5 篇）。两个模块的定时任务均为每 600 秒执行一次。
