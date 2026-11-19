---
title: 安装与开发
---

# emojimix：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-emojimix
```

安装后，管理员需要在会话中执行 `module enable emojimix` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

合成图直接引用 Emoji Kitchen 的静态资源地址，不经过本地缓存。支持列表随包分发，保存在 `assets/emoji_data.json`，其中记录受支持的 Emoji、组合与对应的资源目录日期。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `emoji`、`orjson`、`akari-bot-core`。外部服务为 `www.gstatic.com`，提供 Emoji Kitchen 静态图片。
