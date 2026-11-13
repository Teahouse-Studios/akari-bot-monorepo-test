# minecraft-news

定时推送 Minecraft 官网新闻与 Minecraft Feedback 的更新记录。

## 推送

模块不提供聊天命令，消息由定时任务触发：

- `minecraft-news` 推送官网文章的标题、摘要、链接与封面图。
- `feedback-news` 推送 Feedback 的 beta 与 article 两个分区的文章名称与链接。

`minecraft-news` 首轮只登记现有文章标题，不补发历史文章；`feedback-news` 没有启动静默，首轮轮询到的未记录条目会立即推送。封面图读取失败时只发送文本与链接。

## 推送示例

### 官网新闻

<ChatExample
  :log="[
    '用户：~module enable minecraft-news feedback-news',
    '机器人：成功：开启模块“minecraft-news”。',
    '机器人：成功：开启模块“feedback-news”。',
    '〰〰〰',
    '机器人：Minecraft 官网发布了新的文章：',
    'Marketplace Spotlight: The Sound Effects Edition',
    '  Welcome to the loudest article you\'ve ever read',
    'https://www.minecraft.net/en-us/article/marketplace-spotlight-sound-effects',
    '![文章封面](minecraft-news-example.jpg)',
  ]"
/>

### Feedback 更新

<ChatExample
  :log="[
    '用户：~module enable minecraft-news feedback-news',
    '机器人：成功：开启模块“minecraft-news”。',
    '机器人：成功：开启模块“feedback-news”。',
    '〰〰〰',
    '机器人：Minecraft Feedback 发布了新的文章：',
    'Minecraft Beta & Preview - 26.70.24',
    'https://feedback.minecraft.net/hc/en-us/articles/50285693907213-Minecraft-Beta-Preview-26-70-24',
  ]"
/>

### 更新日志

`mcv-rss` 检测到 Java 版新版本，且更新日志标题尚未记录时，会向启用了 `minecraft-news` 的会话追加一条更新日志：

<ChatExample
  :log="[
    '机器人：Minecraft 官网发布了 26.4-snapshot-8 的更新日志：',
    'https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-8',
  ]"
/>
