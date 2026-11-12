---
title: 安装与开发
---

# nbnhhsh：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-nbnhhsh
```

安装后在会话中由管理员用 `module enable nbnhhsh` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块声明支持语言为简体中文，未声明平台限制，所有已接入平台可用。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core` 与 `orjson`。外部服务为 `https://lab.magiconch.com/api/nbnhhsh/guess`，以 JSON 请求体提交待查询文本。
