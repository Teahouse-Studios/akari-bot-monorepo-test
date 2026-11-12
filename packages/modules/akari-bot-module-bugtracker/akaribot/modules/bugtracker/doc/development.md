---
title: 安装与开发
---

# bugtracker：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-bugtracker
```

安装后在会话中由管理员用 `module enable bugtracker` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

页面截图依赖 WebRender 的元素截图能力，关闭时只发送文本与链接。`zh_cn` 会话若命中 spx 翻译表，标题后追加 `(spx: 译文)`；翻译表在进程内缓存，仅首次使用时拉取。状态为 `Open` 或 `Resolved` 时与类型同行展示，其余状态单独成行。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `orjson`、`akari-bot-core`。外部服务 `bugs.mojang.com`（JQL 搜索接口）、`spxx-db.teahouse.team`（中文翻译表）、WebRender。
