---
title: 安装与开发
---

# mojang-status：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-mojang_status
```

安装后，管理员需要在会话中执行 `module enable mojang-status` 启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入的平台均可以使用。命令依次请求三个接口，将三项结果整合在单条消息中返回。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core`。外部服务为以下三个接口：

- `https://api.mojang.com`：玩家信息
- `https://sessionserver.mojang.com`：正版验证
- `https://api.minecraftservices.com`：Mojang 服务

每个接口仅请求一次，失败后不再重试。

应答状态码为 200 或 400 至 409 时判定为在线。`request_url` 把 5xx 应答与连接失败转为外部服务异常，这类应答不进入状态判定，由框架按外部服务错误处理。其余应答判定为未知。
