---
order: 51
---

# say

此模块用于把给定内容按消息链格式解析后发送，不引用原消息。模块级权限为超级用户。

### `say`

<CommandUsage usage="say <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

文本中包含发送者平台前缀的用户 ID 会被转换为 AT 码，消息发送后渲染为对该用户的提及。

<ChatExample
  :log="[
    '用户：~say 今晚 23:00 例行维护，请提前保存。',
    '机器人：今晚 23:00 例行维护，请提前保存。',
  ]"
/>

### `say md`

<CommandUsage usage="say md <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

此命令按照 Markdown 格式复述指定内容，并附加按钮示例。

<ChatExample
  :log="[
    '用户：~say md **维护通知**：今晚 23:00 重启。',
    '机器人：**维护通知**：今晚 23:00 重启。',
  ]"
/>
