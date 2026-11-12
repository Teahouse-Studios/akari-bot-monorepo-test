---
title: 安装与开发
---

# mcserver：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mcserver
```

安装后在会话中由管理员用 `module enable mcserver` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令未声明管理员或超级用户限制，普通用户可执行。模块未声明平台限制，`available_for` 取默认值 `*`。查询直接连接目标服务器，网络需允许访问对应端口。Java 版查询会解析 SRV 记录，超时后改用 `motd.wd-api.com` 的 HTTP 接口；基岩版同样在超时后回落该服务。发送前，Java 版与基岩版的结果分别经过 core 的内容安全检查。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`、`mcstatus>=14.1.0,<15.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为目标 Minecraft 服务器（Java 版协议与基岩版 RakNet 查询）与 `motd.wd-api.com` 超时回落接口。
