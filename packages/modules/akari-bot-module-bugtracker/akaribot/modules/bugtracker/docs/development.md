---
title: 安装与开发
---

# bugtracker：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-bugtracker
```

安装后，管理员需要在会话中执行 `module enable bugtracker` 以启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

页面截图依赖 WebRender 的元素截图能力。未启用 WebRender 时，机器人仅发送文本与链接。

当会话语言为 `zh_cn` 且 spx 翻译表中包含该漏洞词条时，标题后追加 `(spx: 译文)`。翻译表在进程内缓存，仅在首次使用时拉取。

当漏洞状态为 `Open` 或 `Resolved` 时，状态与类型显示在同一行。其他状态单独占一行。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `orjson` 与 `akari-bot-core`。外部服务为 `bugs.mojang.com`（JQL 搜索接口）、`spxx-db.teahouse.team`（中文翻译表）与 WebRender。
