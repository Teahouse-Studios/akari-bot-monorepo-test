---
order: 55
---

# jobqueue

模块级权限为超级用户。

### `jobqueue clear`

<CommandUsage usage="jobqueue clear" permission="superuser" />

清空计划任务队列，包含执行中的任务。

<ChatExample
  :log="[
    '用户：~jobqueue clear',
    '机器人：成功。',
  ]"
/>
