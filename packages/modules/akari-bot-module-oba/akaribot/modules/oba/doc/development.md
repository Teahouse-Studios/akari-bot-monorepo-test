---
title: 安装与开发
---

# oba：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-oba
```

安装后在会话中由管理员用 `module enable oba` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。赞助商信息以图片消息发送横幅，平台需支持发送图片才能显示横幅。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core`。外部服务为 `https://bd.bangbang93.com/openbmclapi` 的 `metric/dashboard`、`metric/version`、`metric/rank`、`sponsor` 与 `sponsor/<id>` 接口。
