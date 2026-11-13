---
order: 13
---

# auth

此模块让超级用户把某个模块的超级用户权限授予其他用户。使用此模块的命令需要超级用户权限。授权只对声明了 `required_superuser` 的模块生效。

### `auth add`

<CommandUsage usage="auth add <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户授权使用的模块名']" permission="superuser" />

此命令把指定模块的超级用户权限授予目标用户。执行前需要按提示确认，授权记录中会同时记下授权者。目标模块未声明 `required_superuser` 时，此命令会被拒绝。

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

此命令撤销授权，只删除自己授予的条目。授权者失去超级用户身份后，对应的授权不再生效。

<ChatExample
  :log="[
    '用户：~auth remove QQ|123456 update',
    '机器人：已取消 QQ|123456 使用模块 update 的授权。',
  ]"
/>

### `auth list`

<CommandUsage usage="auth list <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

此命令列出用户获得的模块授权。

<ChatExample
  :log="[
    '用户：~auth list QQ|123456',
    '机器人：QQ|123456 被 QQ|654321 授权使用模块 update',
  ]"
/>
