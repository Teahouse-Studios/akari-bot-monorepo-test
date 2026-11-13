---
order: 13
---

# auth

模块级权限为超级用户，只对声明了 `required_superuser` 的模块生效。

### `auth add`

<CommandUsage usage="auth add <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户授权使用的模块名']" permission="superuser" />

授权用户在指定模块中执行超级用户命令。目标模块未声明 `required_superuser` 时拒绝执行；授权记录同时保存授权者，执行前要求确认。

<ChatExample
  :log="[
    '用户：~auth add QQ|123456 update',
    '机器人：你确定吗？',
    '（此为危险操作，完全发送“我授权用户 QQ|123456 使用模块 update。”来确认）',
    '用户：我授权用户 QQ|123456 使用模块 update。',
  ]"
/>

### `auth remove`

<CommandUsage usage="auth remove <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户授权使用的模块名']" permission="superuser" />

撤销授权，只删除本人授予的条目。授权者失去超级用户身份后，该条授权不再生效。

<ChatExample
  :log="[
    '用户：~auth remove QQ|123456 update',
    '机器人：已取消 QQ|123456 使用模块 update 的授权。',
  ]"
/>

### `auth list`

<CommandUsage usage="auth list <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

列出用户获得的模块授权。

<ChatExample
  :log="[
    '用户：~auth list QQ|123456',
    '机器人：QQ|123456 被 QQ|654321 授权使用模块 update',
  ]"
/>
