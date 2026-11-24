---
order: 17
---

# purge

此模块提供缓存清理命令与定时清理任务，模块级所需权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

此命令清空实例的 `cache/` 目录。若目录为空，机器人会输出提示信息。

此模块同时注册了定时清理任务，按照 `auto_purge_crontab` 执行，默认值为 `0 0 * * *`。命令与定时任务均不会修改 `data/` 目录以及数据库。

<ChatExample
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
