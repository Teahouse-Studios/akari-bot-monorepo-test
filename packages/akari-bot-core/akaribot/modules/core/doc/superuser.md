---
order: 14
---

# superuser

<ModuleAlias names="su" />

模块级权限为超级用户。

### `superuser add`

<CommandUsage usage="superuser add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户设为超级用户。用户尚未建立 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~superuser add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为超级用户。',
  ]"
/>

### `superuser remove`

<CommandUsage usage="superuser remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

取消用户的超级用户身份。移除自己时须按提示输入确认内容。`config.toml` 的 `base_superuser` 属于基础超级用户，在启动时写入数据库，只能通过配置维护。

<ChatExample
  :log="[
    '用户：~superuser remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出超级用户。',
  ]"
/>
