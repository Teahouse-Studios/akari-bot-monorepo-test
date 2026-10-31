---
title: 安装与开发
---

# minecraft-news：安装与开发

本页说明 `minecraft-news` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-minecraft_news
```

| 模块 | 别名 | 用途 |
| --- | --- | --- |
| `minecraft-news` | `minecraft_news`、`minecraftnews`、`mcnews` | 官网新闻推送 |
| `feedback-news` | `feedback_news`、`feedbacknews` | Feedback 更新记录推送 |

按需在会话中由管理员用 `module enable minecraft-news` 或 `module enable feedback-news` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 模块没有命令；推送目标为启用了对应模块的会话，启用操作由场景管理员完成。
- 两个模块均声明 `rss=True`，未声明平台限制。
- `minecraft-news` 读取文章 JSON 与封面图需开启 `webrender.enable`；平台需支持图片消息才能显示封面。
- `feedback-news` 使用普通 HTTP 请求，每个分区只尝试一次，失败后等待下一周期。

## 数据表

manifest 未声明 `owned_tables`，模块不拥有数据表。已记录数据写入 core 的 `stored_data`：

- `<客户端名>|mcnews`：`minecraft-news` 已记录的文章标题，`mcv_rss` 的更新日志标题也写入此键。
- `<客户端名>|mcfeedbacknews`：`feedback-news` 已记录的文章名称。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：`www.minecraft.net` 的新闻文章网格 JSON 与封面图、`minecraftfeedback.zendesk.com`
  的两个帮助中心分区（beta 与 article）。
