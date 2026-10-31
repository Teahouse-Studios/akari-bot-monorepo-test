---
title: 安装与开发
---

# arcaea-rss：安装与开发

本页说明 `arcaea-rss` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-arcaea_rss
```

安装后在需要接收推送的会话中由管理员用 `module enable arcaea-rss` 开启。未启用的会话收不到消息。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 推送通过 `Bot.post_message` 发送，目标为开启了该模块的会话，无需用户交互。
- 接口请求只尝试一次，失败后等待下一个周期，调试模式下记录异常堆栈。
- 已推送的版本号按客户端写入 core 的 `stored_data`，同一实例内的多个客户端各自维护记录。

## 数据表

manifest 未声明 `owned_tables`；版本记录保存在 core 的 `stored_data` 表，键为
`<客户端名>|arcaea_rss`。

## 依赖与外部服务

- 依赖：`orjson`、`akari-bot-core`。
- 外部服务：`webapi.lowiro.com` 的安装包信息接口。
