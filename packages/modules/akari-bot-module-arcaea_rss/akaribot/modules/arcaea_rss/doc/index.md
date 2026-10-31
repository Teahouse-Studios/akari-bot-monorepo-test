# arcaea-rss

定时读取 Arcaea 官方安装包接口，发现新版本号时向启用了该模块的会话推送版本与下载地址。
模块标记为 RSS 模块，不提供聊天命令。

模块名 `arcaea-rss`，别名 `arc-rss`、`arcaea_rss`、`arc_rss`。

## 命令

模块没有注册 `command()` 或 `regex()`。消息由定时任务触发：

- 每 60 秒读取一次 `https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk/`。
- 返回的版本号不在已记录列表中时，推送版本号与下载地址。

进程启动后的首次轮询只登记当前版本，不发送消息，避免重启后重复推送。
