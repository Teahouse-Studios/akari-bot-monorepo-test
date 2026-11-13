---
order: 51
---

# say

模块级权限为超级用户。

### `say`

<CommandUsage usage="say <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

以消息链解析并复述给定内容，不引用原消息，发送者的平台账号标记写入文本。

<ChatExample
  :log="[
    '用户：~say 今晚 23:00 例行维护，请提前保存。',
    '机器人：今晚 23:00 例行维护，请提前保存。',
  ]"
/>

### `say md`

<CommandUsage usage="say md <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

以 Markdown 复述给定内容，并附带一个按钮示例。

<ChatExample
  :log="[
    '用户：~say md **维护通知**：今晚 23:00 重启。',
    '机器人：**维护通知**：今晚 23:00 重启。',
  ]"
/>
