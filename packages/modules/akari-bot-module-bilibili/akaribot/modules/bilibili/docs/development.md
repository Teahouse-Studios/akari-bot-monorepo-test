---
title: 安装与开发
---

# bilibili：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-bilibili
```

安装后，管理员需要在会话中执行 `module enable bilibili` 以启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块通过 WebRender 以 stealth 模式请求 `api.bilibili.com`，实例需要启用 `webrender.enable`。在 Discord 频道会话中输出 Embed，需要平台支持 Embed 消息元素与图片消息。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `httpx`（用于解析短链接跳转）、`orjson` 与 `akari-bot-core`。外部服务包括 `api.bilibili.com`（通过 WebRender 访问）与 `b23.tv` 等短链接跳转服务。
