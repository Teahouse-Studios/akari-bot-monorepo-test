---
title: 安装与开发
---

# color：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-color
```

安装完成后，管理员需要在会话中执行 `module enable color` 命令以启用此模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块通过 Embed 消息回复，运行平台需要具备 Embed 消息元素与图片消息的支持能力。

色卡中的文本使用资源包字体 Noto Sans CJK DemiLight，文本颜色根据背景亮度在黑色与白色之间自动切换。Material Design 颜色名称表随模块安装包分发，存储于 `assets/material_colors.json`。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `Pillow`、`numpy`、`webcolors`、`orjson`、`akari-bot-assets-fonts` 与 `akari-bot-core` 软件包。

此模块不依赖外部网络服务，所有颜色名称表均随安装包或依赖项分发。
