---
order: 14
---

# superuser

<ModuleAlias names="su" />

此模块用于维护超级用户名单。模块内全部命令均需要超级用户权限。

### `superuser add`

<CommandUsage usage="superuser add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

此命令将用户设置为超级用户。若该用户尚未包含 union 记录，机器人会先请求确认，确认通过后再创建记录。

<ChatExample
  :log="[
    '用户：~superuser add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为超级用户。',
  ]"
/>

### `superuser remove`

<CommandUsage usage="superuser remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

此命令撤销用户的超级用户身份。移除当前操作者时，机器人会要求输入确认内容。`config.toml` 中的 `base_superuser` 是基础超级用户名单，启动时写入数据库，仅可通过配置文件维护。

<ChatExample
  :log="[
    '用户：~superuser remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出超级用户。',
  ]"
/>
