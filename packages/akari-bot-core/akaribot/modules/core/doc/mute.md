---
order: 11
---

# mute

模块级权限为场景管理员。

### `mute`

<CommandUsage usage="mute" permission="admin" />

切换本场景的静音状态。静音期间除 `mute` 外的命令与正则都不执行，对静音场景的主动推送同样被抑制；再次执行恢复。

<ChatExample
  :log="[
    '用户：~mute',
    '机器人：成功静音。',
    '用户：~mute',
    '机器人：成功取消静音。',
  ]"
/>
