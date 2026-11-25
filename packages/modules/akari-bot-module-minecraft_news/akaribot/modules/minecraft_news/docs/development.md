---
title: 安装与开发
---

# minecraft-news：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

本页说明这两个模块的安装、配置、数据表与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-minecraft_news
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `minecraft-news` | `minecraft_news`、`minecraftnews`、`mcnews` | 官网新闻推送 |
| `feedback-news` | `feedback_news`、`feedbacknews` | Feedback 更新记录推送 |

若需要启用对应模块，管理员可以在目标会话中执行 `module enable minecraft-news` 或 `module enable feedback-news`。两个模块互相声明对方为推荐模块，启用其中一个时会提示启用另一个。

## 配置项

<ModuleConfig />

## 权限与平台能力

两个模块均不提供聊天命令，推送目标为启用了对应模块的会话，启用操作由场景管理员执行。两个模块均声明了 `rss=True`，未声明平台限制。

`minecraft-news` 读取文章 JSON 与封面图需要启用 `webrender.enable`，平台还需要支持图片消息才能显示封面。`feedback-news` 使用普通 HTTP 请求，每个分区仅尝试一次，失败后等待下一周期。

`minecraft-news` 第一次执行检查时，将现有文章标题记录为起点，此后仅推送新文章。`feedback-news` 没有该项起点记录，第一次检查时尚未记录的条目会直接推送。

`minecraft-news` 读取封面图失败时，仅发送标题、摘要与链接。

## 数据表

<ModuleData />

已记录的数据写入 core 的 `stored_data`。`<客户端名>|mcnews` 保存 `minecraft-news` 已记录的文章标题，`mcv_rss` 的更新日志标题也写入此键。`<客户端名>|mcfeedbacknews` 保存 `feedback-news` 已记录的文章名称。

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `orjson`，实际版本范围从包根目录的 `dependencies` 读取。外部服务为 `www.minecraft.net` 与 `minecraftfeedback.zendesk.com`。

`www.minecraft.net` 提供新闻文章的 JSON 与封面图，`minecraftfeedback.zendesk.com` 提供两个帮助中心分区（beta 与 article，每次各读取 5 篇）。两个模块的定时任务均为每 600 秒执行一次。
