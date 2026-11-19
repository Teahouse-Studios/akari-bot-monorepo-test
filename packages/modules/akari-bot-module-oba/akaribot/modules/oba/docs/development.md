---
title: 安装与开发
---

# oba：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-oba
```

安装后，管理员需要在会话中执行 `module enable oba` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

所有命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入的平台均可使用。赞助商横幅以图片消息发送，平台需要支持发送图片才能显示。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core`。外部服务为 `https://bd.bangbang93.com/openbmclapi`，提供 `metric/dashboard`、`metric/version`、`metric/rank`、`sponsor` 与 `sponsor/<id>` 接口。
