---
order: 55
---

# jobqueue

此模块可以清空计划任务队列。模块级权限为超级用户。

### `jobqueue clear`

<CommandUsage usage="jobqueue clear" permission="superuser" />

此命令清空计划任务队列，正在执行的任务也一并删除。

<ChatExample
  :log="[
    '用户：~jobqueue clear',
    '机器人：成功。',
  ]"
/>
