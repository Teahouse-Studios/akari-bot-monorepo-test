---
title: 安装与开发
---

# emojimix：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-emojimix
```

安装后在会话中由管理员用 `module enable emojimix` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

合成图直接从 Emoji Kitchen 的静态资源地址引用，不经过本地缓存。支持列表随包分发在 `assets/emoji_data.json`，包含受支持 Emoji、组合与对应资源目录日期。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `emoji`、`orjson`、`akari-bot-core`。外部服务 `www.gstatic.com` 的 Emoji Kitchen 静态图片。
