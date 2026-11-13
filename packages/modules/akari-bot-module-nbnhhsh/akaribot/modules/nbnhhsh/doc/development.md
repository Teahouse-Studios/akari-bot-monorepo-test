---
title: 安装与开发
---

# nbnhhsh：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-nbnhhsh
```

安装后，管理员需要在会话中执行 `module enable nbnhhsh` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块声明的支持语言只有简体中文。模块没有声明平台限制，所有已接入平台都可以使用。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core` 与 `orjson`。外部服务为 `https://lab.magiconch.com/api/nbnhhsh/guess`，请求以 JSON 格式提交待查询文本。
