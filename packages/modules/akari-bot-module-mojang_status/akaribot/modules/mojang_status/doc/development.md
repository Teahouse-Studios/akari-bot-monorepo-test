---
title: 安装与开发
---

# mojang-status：安装与开发

本页说明 `mojang-status` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mojang_status
```

安装后在会话中由管理员用 `module enable mojang-status` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 查询为串行请求，三项结果在一条消息内返回。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 外部服务：Mojang 账号接口、会话服务器接口与 Minecraft 服务接口。
