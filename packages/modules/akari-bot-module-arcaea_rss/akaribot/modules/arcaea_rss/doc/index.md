# Arcaea 版本推送

定时读取 Arcaea 官方安装包接口，发现新版本号时向启用了该模块的会话推送版本与下载地址。
模块标记为 RSS 模块，不提供聊天命令。

模块名 `arcaea-rss`，别名 `arc-rss`、`arcaea_rss`、`arc_rss`。

## 安装

```bash
akaribot module add akari-bot-module-arcaea_rss
```

安装后在需要接收推送的会话中由管理员用 `module enable arcaea-rss` 开启。未启用的会话收不到消息。

## 命令

模块没有注册 `command()` 或 `regex()`。消息由定时任务触发：

- 每 60 秒读取一次 `https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk/`。
- 返回的版本号不在已记录列表中时，推送版本号与下载地址。

进程启动后的首次轮询只登记当前版本，不发送消息，避免重启后重复推送。

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
