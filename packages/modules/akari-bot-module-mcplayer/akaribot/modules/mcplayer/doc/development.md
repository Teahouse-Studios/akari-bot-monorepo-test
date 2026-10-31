---
title: 安装与开发
---

# mcplayer：安装与开发

本页说明 `mcplayer` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcplayer
```

安装后在会话中由管理员用 `module enable mcplayer` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 成功获取皮肤时输出包含图片消息，平台需支持发送图片。

## 数据表

无数据库表。披风图缓存为 core 缓存目录下的 `<uuid>_fixed.png`。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`Pillow>=13.0.0,<13.1.0`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：`api.mojang.com`（玩家名与 UUID 互查）、`crafatar.com`（渲染图、皮肤、披风）。
- 结果中的 NameMC 链接指向 `namemc.com`，仅作为链接输出，不请求该站。
