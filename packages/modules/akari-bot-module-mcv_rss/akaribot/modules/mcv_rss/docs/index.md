# mcv-rss

此模块会定时检测 Minecraft：Java 版启动器与基岩版商店版本，发现新版本时向启用了对应模块的会话推送消息。

## 推送

`mcv-rss` 与 `mcbv-rss` 都不提供聊天命令，消息由定时任务触发：

- `mcv-rss` 检测 Java 版正式版与快照，发现新版本时推送版本号、更新时间与推送时间。
- `mcbv-rss` 检测基岩版正式版，发现新版本时推送版本号。

`mcv-rss` 检测到新版本时还会检查更新日志标题。标题未记录时，`mcv-rss` 会向启用了 `minecraft-news` 的会话推送 `minecraft.net` 的更新日志链接。

启用后的首轮轮询不会补发已经发布的版本。`mcv-rss` 首轮只记录当前版本，不补记旧版本，也不发送消息。更新日志标题会另行缓存，但不推送。`mcbv-rss` 首轮既不记录也不推送，下一轮仍检测到未记录版本时才发送。

## 推送示例

### Java 版正式版

<ChatExample
  :log="[
    '用户：~module enable mcv-rss',
    '机器人：成功：开启模块“mcv-rss”。',
    '〰〰〰',
    '机器人：启动器已更新 26.3 正式版。',
    '更新时间： 2026-09-15 19:23:02 (UTC+8)',
    '推送时间：2026-09-15 19:24:02 (UTC+8)',
  ]"
/>

### Java 版快照

<ChatExample
  :log="[
    '用户：~module enable mcv-rss',
    '机器人：成功：开启模块“mcv-rss”。',
    '〰〰〰',
    '机器人：启动器已更新 26.4-snapshot-8 快照。',
    '更新时间： 2026-11-10 22:20:05 (UTC+8)',
    '推送时间：2026-11-10 22:21:05 (UTC+8)',
  ]"
/>

### 基岩版

<ChatExample
  :log="[
    '用户：~module enable mcbv-rss',
    '机器人：成功：开启模块“mcbv-rss”。',
    '〰〰〰',
    '机器人：Google Play 商店已更新基岩版 1.26.62.1 正式版。',
  ]"
/>

`mcbv-rss` 通过 Google Play 查询版本。若 `ip_country` 为 `China`，或没有配置 `ip_country`，则不推送。
