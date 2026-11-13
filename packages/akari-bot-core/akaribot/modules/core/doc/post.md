---
order: 53
---

# post

模块级权限为超级用户。

### `post`

<CommandUsage usage="post <target> <post_msg>" :params="['target=目标场景 ID，须带平台前缀', 'post_msg=推送内容，支持 KE 码']" permission="superuser" />

此命令向指定场景推送主动消息，执行前要求确认。目标场景 ID 须带平台前缀，缺少前缀时，机器人会提示当前场景使用的前缀。`post_msg` 支持 KE 码。

<ChatExample
  :log="[
    '用户：~post QQ|Group|987654321 今晚 23:00 例行维护。',
    '机器人：此操作将会为群聊 QQ|Group|987654321 推送以下消息，是否继续？',
    '用户：是',
    '机器人：推送消息完成。',
  ]"
/>

### `post global`

<CommandUsage usage="post global <post_msg>" :params="['post_msg=广播内容，支持 KE 码']" permission="superuser" />

此命令向全部启用场景广播主动消息，执行前要求确认。

<ChatExample
  :log="[
    '用户：~post global 全部群聊将于今晚 23:00 重启。',
    '机器人：警告：此操作将会为所有群聊推送以下消息，是否继续？',
    '用户：是',
    '机器人：推送消息完成。',
  ]"
/>
