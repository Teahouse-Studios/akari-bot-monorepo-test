# mcv-rss

定时检测 Minecraft：Java 版启动器与基岩版商店版本，发现新版本时向启用了对应模块的会话推送。
包内注册两个 RSS 模块：`mcv-rss` 与 `mcbv-rss`，均不提供聊天命令。

## 命令

模块没有注册 `command()` 或 `regex()`。消息由定时任务触发：

- `mcv-rss` 每 60 秒读取 `piston-meta.mojang.com` 的版本清单，登记新的 release 与 snapshot。
- `mcbv-rss` 每 180 秒读取 Google Play 的 `com.mojang.minecraftpe` 版本号，登记新的正式版。

发现新版本时，`mcv-rss` 向对应会话推送版本号、记录时间与推送时间；`mcbv-rss` 推送版本号。
`mcv-rss` 还会按版本号构造 `minecraft.net` 更新日志地址，标题未记录时向 `minecraft-news` 模块
推送更新日志链接，并把标题写入与 `minecraft_news` 共用的记录。

启动静默：`mcv-rss` 首次成功轮询只登记当前版本与更新日志标题，不发送消息；`mcbv-rss` 首轮只解除
静默标志，不登记也不推送，下一轮若仍检测到未记录版本则发送。
