---
order: 14
---

# superuser

<ModuleAlias names="su" />

此模块用于维护超级用户名单。模块内所有命令都要求超级用户权限。

### `superuser add`

<CommandUsage usage="superuser add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

此命令将用户设为超级用户。用户还没有 union 记录时，机器人先要求确认，再创建记录。

<ChatExample
  :log="[
    '用户：~superuser add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为超级用户。',
  ]"
/>

### `superuser remove`

<CommandUsage usage="superuser remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

此命令取消用户的超级用户身份。移除自己时，机器人会要求输入确认内容。`config.toml` 中的 `base_superuser` 是基础超级用户名单，启动时写入数据库，只能通过配置维护。

<ChatExample
  :log="[
    '用户：~superuser remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出超级用户。',
  ]"
/>
