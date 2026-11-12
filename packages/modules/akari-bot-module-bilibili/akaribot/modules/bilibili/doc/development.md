---
title: 安装与开发
---

# bilibili：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-bilibili
```

安装后在会话中由管理员用 `module enable bilibili` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

通过 WebRender 以 stealth 模式请求 `api.bilibili.com`，需开启 `webrender.enable`。Discord 频道会话的 Embed 输出需要平台支持 Embed 消息元素与图片消息。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `httpx`（短链跳转解析）、`orjson`、`akari-bot-core`。外部服务 `api.bilibili.com`（经 WebRender）、`b23.tv` 等短链服务。
