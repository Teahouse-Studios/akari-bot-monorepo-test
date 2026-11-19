---
title: 安装与开发
---

# mojang-status：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mojang_status
```

安装后，管理员需要在会话中执行 `module enable mojang-status` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入平台都可以使用。命令依次请求三个接口，把三项结果放在一条消息里返回。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core`。外部服务为以下三个接口：

- `https://api.mojang.com`：玩家信息
- `https://sessionserver.mojang.com`：正版验证
- `https://api.minecraftservices.com`：Mojang 服务

每个接口只请求一次，失败不重试。应答为 200 或 400 至 409 时判定为在线。异常信息以 50 开头时显示离线，其余可识别的异常显示未知。常规 HTTP 5xx 应答由框架按外部服务错误处理。
