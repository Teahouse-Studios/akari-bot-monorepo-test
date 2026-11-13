---
title: 安装与开发
---

# mcserver：安装与开发

本文将会介绍此模块的安装、配置、网络要求与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcserver
```

安装完成后，请让管理员在会话中执行 `module enable mcserver` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令未声明管理员或超级用户限制，普通用户可以直接执行。模块没有声明平台限制，`available_for` 取默认值 `*`。

查询会直接连接目标服务器，需要网络允许访问对应端口。Java 版查询会解析 SRV 记录，超时后改用 `motd.wd-api.com` 的 HTTP 接口。基岩版查询在超时后同样改用 `motd.wd-api.com` 的接口。

两个版本的结果在发送前都会经过 core 的内容安全检查。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`、`mcstatus>=14.1.0,<15.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为目标 Minecraft 服务器与 `motd.wd-api.com`。目标服务器分别使用 Java 版协议与基岩版 RakNet 查询，`motd.wd-api.com` 在查询超时后提供结果。
