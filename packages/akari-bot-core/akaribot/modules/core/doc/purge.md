---
order: 17
---

# purge

模块级权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

清空实例 `cache/` 目录，目录为空时给出提示。同一模块注册了按 `auto_purge_crontab`（默认 `0 0 * * *`）执行的定时清理，命令与定时任务都不触碰 `data/` 与数据库。

<ChatExample
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
