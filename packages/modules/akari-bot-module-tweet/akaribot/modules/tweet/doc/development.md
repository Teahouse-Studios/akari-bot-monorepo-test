---
title: 安装与开发
---

# tweet：安装与开发

本页说明 `tweet` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-tweet
```

安装后在会话中由管理员用 `module enable tweet` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令与正则匹配对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 摘要图依赖实例启用 WebRender；未启用时无法生成截图。
- 图片发送能力由平台决定，不支持图片的平台无法展示摘要图。

## 数据表

无。manifest 未声明 `owned_tables`，推文数据不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`orjson`。
- 外部服务：`react-tweet.vercel.app` 数据接口、`react-tweet-next.vercel.app` 渲染页面与 WebRender 截图服务。
