---
title: 安装与开发
---

# mojang-status：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mojang_status
```

安装后在会话中由管理员用 `module enable mojang-status` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。查询为串行请求，三项结果在一条消息内返回。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core`。外部服务为以下三个接口：

- `https://api.mojang.com`：玩家信息
- `https://sessionserver.mojang.com`：正版验证
- `https://api.minecraftservices.com`：Mojang 服务

每个接口只尝试一次，失败不重试。接口返回 200 或 400 至 409 应答时判定为在线；错误值以 50 开头时显示离线；其余可识别异常显示未知；常规 HTTP 5xx 应答由框架按外部服务错误处理。
