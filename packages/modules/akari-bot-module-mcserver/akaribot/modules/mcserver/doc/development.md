---
title: 安装与开发
---

# mcserver：安装与开发

本页说明 `mcserver` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcserver
```

安装后在会话中由管理员用 `module enable mcserver` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 查询直接连接目标服务器，网络需允许访问对应端口；超时回落时需可访问 `motd.wd-api.com`。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`mcstatus>=14.1.0,<15.0.0`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：目标 Minecraft 服务器（Java 版协议与基岩版 RakNet 查询）、`motd.wd-api.com` 超时回落接口。
