---
order: 54
---

# post-whitelist

<ModuleAlias names="post_whitelist" />

模块级权限为超级用户。

### `post-whitelist`

<CommandUsage usage="post-whitelist <group_id>" :params="['group_id=QQ 群 ID，须带平台前缀']" permission="superuser" platforms="QQ" />

仅 QQ 平台可用。切换 QQ 群的主动推送优先级。参数须为 `QQ|Group|` 前缀的完整 ID，场景尚无 union 时先确认再创建。该开关写入场景数据的 `in_post_whitelist`，适配器在主动推送时据此把场景放入高优先级队列。

<ChatExample
  :log="[
    '用户：~post-whitelist QQ|Group|123456789',
    '机器人：成功为群聊设置了以下参数：in_post_whitelist -> True',
  ]"
/>
