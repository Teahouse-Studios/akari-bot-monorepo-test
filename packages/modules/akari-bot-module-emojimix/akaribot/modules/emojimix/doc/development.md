---
title: 安装与开发
---

# emojimix：安装与开发

本页说明 `emojimix` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-emojimix
```

安装后在会话中由管理员用 `module enable emojimix` 开启。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 合成图直接从 Emoji Kitchen 的静态资源地址引用，不经过本地缓存。
- `list` 在 Discord 平台按每 200 个一批分条发送，其余平台合并为一条消息。
- 支持列表随包分发在 `assets/emoji_data.json`，包含受支持 Emoji、组合与对应资源目录日期。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`emoji`、`orjson`、`akari-bot-core`。
- 外部服务：`www.gstatic.com` 的 Emoji Kitchen 静态图片。
