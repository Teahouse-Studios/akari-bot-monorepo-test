---
title: 安装与开发
---

# color：安装与开发

本页说明 `color` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-color
```

安装后在会话中由管理员用 `module enable color` 开启。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 输出为 Embed，含 HEX、RGB、HSL 三个字段与两个颜色名字段；仅在颜色名与色值完全一致时使用
  「颜色名称」，否则标注为「最相似的」名称。
- 色卡文字使用资源包字体 Noto Sans CJK DemiLight，文字颜色按背景亮度在黑与白之间切换。
- Material Design 名称表随包分发在 `assets/material_colors.json`。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`Pillow`、`numpy`、`webcolors`、`orjson`、`akari-bot-assets-fonts`、`akari-bot-core`。
- 不使用外部网络服务，颜色名称表全部随包或随依赖分发。
