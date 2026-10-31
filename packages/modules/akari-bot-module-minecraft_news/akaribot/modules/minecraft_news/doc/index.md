# minecraft-news

定时推送 Minecraft 官网新闻与 Minecraft Feedback 的更新记录。包内注册两个 RSS 模块：
`minecraft-news` 与 `feedback-news`，均不提供聊天命令，并互相推荐启用。

## 命令

模块没有注册 `command()` 或 `regex()`。消息由定时任务触发：

- `minecraft-news` 每 600 秒读取官网文章网格 JSON，对标题未记录的文章推送标题、摘要、链接与封面图。
- `feedback-news` 每 600 秒读取 Feedback 的 beta 与 article 两个分区各 5 篇文章，对名称未记录的
  文章推送名称与链接。

`minecraft-news` 首次成功轮询只登记当前文章标题，不发送消息；`feedback-news` 没有启动静默，首次
轮询到的未记录条目会立即推送。封面图经 WebRender 读取，失败时只发送文本与链接。
