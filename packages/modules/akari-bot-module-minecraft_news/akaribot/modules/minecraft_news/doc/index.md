# minecraft-news

定时推送 Minecraft 官网新闻与 Minecraft Feedback 的更新记录。

## 命令

模块不提供聊天命令，消息由定时任务触发：

- `minecraft-news` 推送官网文章的标题、摘要、链接与封面图。
- `feedback-news` 推送 Feedback 的 beta 与 article 两个分区的文章名称与链接。

`minecraft-news` 首轮只登记现有文章标题，不补发历史文章；`feedback-news` 没有启动静默，首轮轮询到的未记录条目会立即推送。封面图读取失败时只发送文本与链接。
