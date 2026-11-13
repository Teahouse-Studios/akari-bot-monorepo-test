---
title: 安装与开发
---

# color：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-color
```

安装后，管理员需要在会话中执行 `module enable color`。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块以 Embed 消息回复，平台需要支持 Embed 消息元素与图片消息。

色卡文字使用资源包字体 Noto Sans CJK DemiLight，文字颜色按背景亮度在黑色与白色之间切换。Material Design 名称表随包分发，位于 `assets/material_colors.json`。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `Pillow`、`numpy`、`webcolors`、`orjson`、`akari-bot-assets-fonts`、`akari-bot-core`。

模块不使用外部网络服务，颜色名称表随包或随依赖分发。
