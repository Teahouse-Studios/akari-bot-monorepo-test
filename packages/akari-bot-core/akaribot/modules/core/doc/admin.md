---
order: 10
---

# admin

模块级权限为场景管理员。别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应子命令。

### `admin add`

<CommandUsage usage="admin add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

将用户加入本场景管理员。`<user>` 须为带平台前缀的完整 ID（如 `QQ|123456`），缺少前缀时提示先用 `bind whoami` 查询。平台原生管理员与已在列表中的用户无需执行该命令。

<ChatExample
  :log="[
    '用户：~admin add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为机器人管理员。',
  ]"
/>

### `admin remove`

<CommandUsage usage="admin remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

移除场景管理员。移除自己时须按提示输入确认内容后才执行；平台原生管理员身份不受该命令影响。

<ChatExample
  :log="[
    '用户：~admin remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出机器人管理员。',
  ]"
/>

### `admin list`

<CommandUsage usage="admin list" permission="admin" />

列出本场景的管理员，按 union 展开为绑定的平台账号，一行对应一个 union。

<ChatExample
  :log="[
    '用户：~admin list',
    '机器人：当前被手动设置的机器人管理员：',
    'QQ|123456',
  ]"
/>

### `admin ban`

<CommandUsage usage="admin ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

禁止用户在本场景使用机器人。不能封禁自己。封禁记录按 union 存储，同一用户绑定的其它平台账号一并生效。

<ChatExample
  :log="[
    '用户：~admin ban QQ|123456',
    '机器人：成功限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin unban`

<CommandUsage usage="admin unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

解除对用户的封禁。

<ChatExample
  :log="[
    '用户：~admin unban QQ|123456',
    '机器人：成功取消限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin ban list`

<CommandUsage usage="admin ban list" permission="admin" />

列出本场景被禁止的用户，按 union 展开为绑定的平台账号。

<ChatExample
  :log="[
    '用户：~admin ban list',
    '机器人：当前被设置限制使用机器人的成员：',
    'QQ|123456',
  ]"
/>

### `admin leave`

<CommandUsage usage="admin leave" permission="admin" platforms="QQ 群聊" />

仅 QQ 群聊可用。使机器人退出当前群聊，执行前须确认。命令只注册于 `QQ|Group` 场景。

<ChatExample
  :log="[
    '用户：~admin leave',
    '机器人：你确定吗？此操作不可逆。',
    '用户：是',
    '机器人：已执行，再见。',
  ]"
/>
