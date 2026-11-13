---
order: 17
---

# purge

此模块提供缓存清理命令与定时清理任务，模块级权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

此命令清空实例的 `cache/` 目录，目录为空时给出提示。

此模块还注册了定时清理任务，按 `auto_purge_crontab` 执行，默认值为 `0 0 * * *`。命令与定时任务都不会改动 `data/` 目录和数据库。

<ChatExample
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
