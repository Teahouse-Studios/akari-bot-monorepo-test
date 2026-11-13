---
order: 15
---

# abuse

<ModuleAlias names="ae" />

模块级权限为超级用户。

### `abuse check`

<CommandUsage usage="abuse check <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

查看用户的警告次数、临时封禁与黑白名单状态。用户尚无 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~abuse check QQ|123456',
    '机器人：用户 QQ|123456 已被警告 2 次。',
    '（此用户已处于黑名单）',
  ]"
/>

### `abuse warn`

<CommandUsage usage="abuse warn <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=增加的警告次数，缺省为 1']" permission="superuser" />

增加警告次数，`<count>` 缺省为 1。累计次数超过 `tos_warning_counts` 且用户不在白名单时，用户转入黑名单。临时封禁的时长取自 `tos_temp_ban_time`，由 `tos` 钩子执行，见[tos](tos.md)。

<ChatExample
  :log="[
    '用户：~abuse warn QQ|123456',
    '机器人：成功警告用户 QQ|123456 1 次。此用户已被警告 3 次。',
  ]"
/>

### `abuse revoke`

<CommandUsage usage="abuse revoke <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=减少的警告次数，缺省为 1']" permission="superuser" />

减少警告次数，`<count>` 缺省为 1。

<ChatExample
  :log="[
    '用户：~abuse revoke QQ|123456',
    '机器人：成功移除用户 QQ|123456 的 1 次警告。此用户已被警告 2 次。',
  ]"
/>

### `abuse clear`

<CommandUsage usage="abuse clear <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户的警告次数清零。

<ChatExample
  :log="[
    '用户：~abuse clear QQ|123456',
    '机器人：成功清除用户 QQ|123456 的警告。',
  ]"
/>

### `abuse untempban`

<CommandUsage usage="abuse untempban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

解除临时封禁，交由 `tos.remove_temp_ban` 钩子处理。

<ChatExample
  :log="[
    '用户：~abuse untempban QQ|123456',
    '机器人：成功解除用户 QQ|123456 的临时封禁。',
  ]"
/>

### `abuse ban`

<CommandUsage usage="abuse ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入黑名单并清除白名单身份。

<ChatExample
  :log="[
    '用户：~abuse ban QQ|123456',
    '机器人：成功将用户 QQ|123456 加入黑名单。',
  ]"
/>

### `abuse unban`

<CommandUsage usage="abuse unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出黑名单。

<ChatExample
  :log="[
    '用户：~abuse unban QQ|123456',
    '机器人：成功将用户 QQ|123456 移除黑名单。',
  ]"
/>

### `abuse trust`

<CommandUsage usage="abuse trust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入白名单并移出黑名单。白名单用户不触发警告封禁。

<ChatExample
  :log="[
    '用户：~abuse trust QQ|123456',
    '机器人：成功将用户 QQ|123456 加入白名单。',
  ]"
/>

### `abuse distrust`

<CommandUsage usage="abuse distrust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出白名单。

<ChatExample
  :log="[
    '用户：~abuse distrust QQ|123456',
    '机器人：成功将用户 QQ|123456 移除白名单。',
  ]"
/>

### `abuse block`

<CommandUsage usage="abuse block <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" platforms="QQ" />

仅 QQ 可用。屏蔽指定场景，`<target>` 须为 `QQ|Group|` 前缀的完整 ID，且不能是当前场景。

<ChatExample
  :log="[
    '用户：~abuse block QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 加入黑名单。',
  ]"
/>

### `abuse unblock`

<CommandUsage usage="abuse unblock <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" platforms="QQ" />

仅 QQ 可用。解除对指定场景的屏蔽。

<ChatExample
  :log="[
    '用户：~abuse unblock QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 移除黑名单。',
  ]"
/>
