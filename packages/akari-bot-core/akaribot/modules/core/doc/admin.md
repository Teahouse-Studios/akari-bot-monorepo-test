---
order: 10
---

# admin

此模块用于管理本场景的管理员名单与封禁名单，也可以让机器人退出群聊。模块级权限为场景管理员。别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应的子命令，可以直接调用。

### `admin add`

<CommandUsage usage="admin add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

此命令把用户加入本场景的机器人管理员名单。`<user>` 须为带平台前缀的完整 ID（如 `QQ|123456`），缺少前缀时，机器人会提示先用 `bind whoami` 查询。平台原生管理员与已在名单中的用户无需执行此命令。

<ChatExample
  :log="[
    '用户：~admin add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为机器人管理员。',
  ]"
/>

### `admin remove`

<CommandUsage usage="admin remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

此命令把用户移出本场景的机器人管理员名单。移除自己时，机器人会要求输入确认内容，确认后才执行。平台原生管理员无法通过此命令移除。

<ChatExample
  :log="[
    '用户：~admin remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出机器人管理员。',
  ]"
/>

### `admin list`

<CommandUsage usage="admin list" permission="admin" />

此命令列出本场景的管理员。名单按用户记录，展示时展开为该用户绑定的平台账号，一行对应一个用户。

<ChatExample
  :log="[
    '用户：~admin list',
    '机器人：当前被手动设置的机器人管理员：',
    'QQ|123456',
  ]"
/>

### `admin ban`

<CommandUsage usage="admin ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

此命令禁止用户在本场景使用机器人，不能封禁自己。封禁记录按用户保存，同一用户绑定的其他平台账号一并受限。

<ChatExample
  :log="[
    '用户：~admin ban QQ|123456',
    '机器人：成功限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin unban`

<CommandUsage usage="admin unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

此命令解除对用户的封禁。

<ChatExample
  :log="[
    '用户：~admin unban QQ|123456',
    '机器人：成功取消限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin ban list`

<CommandUsage usage="admin ban list" permission="admin" />

此命令列出本场景被禁止的用户。名单按用户记录，展示时展开为该用户绑定的平台账号。

<ChatExample
  :log="[
    '用户：~admin ban list',
    '机器人：当前被设置限制使用机器人的成员：',
    'QQ|123456',
  ]"
/>

### `admin leave`

<CommandUsage usage="admin leave" permission="admin" platforms="QQ 群聊" />

此命令仅在 QQ 群聊可用，用于让机器人退出当前群聊，执行前需要你确认。命令只注册于 `QQ|Group` 场景。

<ChatExample
  :log="[
    '用户：~admin leave',
    '机器人：你确定吗？此操作不可逆。',
    '用户：是',
    '机器人：已执行，再见。',
  ]"
/>
