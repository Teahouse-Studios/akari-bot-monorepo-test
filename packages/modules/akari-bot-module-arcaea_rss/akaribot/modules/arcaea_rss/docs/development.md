---
title: 安装与开发
---

# arcaea-rss：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-arcaea_rss
```

安装后，管理员在需要接收推送的会话中执行 `module enable arcaea-rss` 启用模块。未启用该模块的会话不会接收到推送消息。

## 配置项

<ModuleConfig />

## 权限与平台能力

推送通过 `Bot.post_message` 发送，目标为启用了该模块的会话，无需用户参与交互。

机器人每 60 秒轮询一次 `https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk/`。接口请求仅尝试一次，失败后等待下一个周期，并在调试模式下记录异常调用栈。

机器人启动后的第一次检查仅记录当前版本。之后出现新版本时，推送版本号与下载地址。同一版本仅推送一次。

已推送的版本号按客户端分别写入 core 中的 `stored_data` 数据表。同一实例下的多个客户端各自维护独立记录。

## 数据表

<ModuleData />

版本记录保存在 core 中的 `stored_data` 数据表中，键名格式为 `<客户端名>|arcaea_rss`。

## 依赖与外部服务

依赖 `orjson` 与 `akari-bot-core`。外部服务为 `webapi.lowiro.com` 提供的安装包信息接口。
