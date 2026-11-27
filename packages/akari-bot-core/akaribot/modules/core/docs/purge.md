---
order: 17
---

# purge

此模块用于清理实例缓存，模块级权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

此命令清空实例的 `cache/` 目录。若目录为空，机器人会输出提示信息。

此模块同时注册了定时清理任务，按 `auto_purge_crontab` 执行，默认值为 `0 0 * * *`。清理范围与命令相同。

<ChatExample
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
