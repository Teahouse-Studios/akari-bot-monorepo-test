---
order: 52
---

# echo

模块级权限为超级用户。

### `echo`

<CommandUsage :usage="['echo', 'echo [<display_msg>]']" :params="['display_msg=要原文复述的消息内容']" permission="superuser" />

原文复述给定内容，不解析消息元素。省略参数时等待下一条消息，复述其显示文本。

<ChatExample
  :log="[
    '用户：~echo',
    '机器人：请发送想要重复的消息。',
    '用户：今天的布丁很好吃',
    '机器人：今天的布丁很好吃',
  ]"
/>
