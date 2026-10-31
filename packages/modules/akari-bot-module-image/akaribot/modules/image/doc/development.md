---
title: 安装与开发
---

# image：安装与开发

本页说明 `image` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-image
```

模块名为 `image`，命令前缀为 `image`，没有别名。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 模块声明 `required_superuser=True`，仅机器人超级用户可执行。
- 未声明平台限制，所有已接入平台可用。
- 平台需支持接收与发送图片：输入依赖消息中的图片元素，输出为转换后的图片。

## 数据表

无。图片只在内存中转换，不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`Pillow>=13.0.0,<13.1.0`。
- 不访问外部服务。
