---
title: 安装与开发
---

# color：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-color
```

安装后在会话中由管理员用 `module enable color` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

输出为 Embed 消息，平台需支持 Embed 消息元素与图片消息。色卡文字使用资源包字体 Noto Sans CJK DemiLight，文字颜色按背景亮度在黑与白之间切换。Material Design 名称表随包分发在 `assets/material_colors.json`。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `Pillow`、`numpy`、`webcolors`、`orjson`、`akari-bot-assets-fonts`、`akari-bot-core`。不使用外部网络服务，颜色名称表全部随包或随依赖分发。
