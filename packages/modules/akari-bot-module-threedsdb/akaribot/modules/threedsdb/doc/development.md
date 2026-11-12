---
title: 安装与开发
---

# 3dsdb：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-threedsdb
```

安装后在会话中由管理员用 `module enable 3dsdb` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。结果以文本消息返回，不依赖图片或网络。

## 数据表

<ModuleData />

应用清单以只读 JSON 随包分发，位于 `assets/data/list_JP.json`、`list_TW.json`、`list_KR.json`、`list_US.json` 与 `list_GB.json`。

## 依赖与外部服务

依赖 `akari-bot-core` 与 `orjson`，不使用外部网络服务。
