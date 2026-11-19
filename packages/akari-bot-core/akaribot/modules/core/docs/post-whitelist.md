---
order: 54
---

# post-whitelist

<ModuleAlias names="post_whitelist" />

模块级权限为超级用户。

### `post-whitelist`

<CommandUsage usage="post-whitelist <group_id>" :params="['group_id=QQ 群 ID，须带平台前缀']" permission="superuser" platforms="QQ" />

此命令切换目标群的主动推送优先级，仅 QQ 平台可用。参数须是以 `QQ|Group|` 开头的完整 ID。目标群还没有场景记录时，机器人先请求确认，确认后再创建。

该开关的值写入场景数据的 `in_post_whitelist`。适配器在主动推送时据此把场景放入高优先级队列。

<ChatExample
  :log="[
    '用户：~post-whitelist QQ|Group|123456789',
    '机器人：成功为群聊设置了以下参数：in_post_whitelist -> True',
  ]"
/>
