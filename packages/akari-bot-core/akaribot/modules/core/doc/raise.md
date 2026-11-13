---
order: 57
---

# raise

模块级权限为超级用户。

### `raise`

<CommandUsage usage="raise [<args>]" :params="['args=异常信息，省略时用内置文案']" permission="superuser" />

此命令抛出 `TestException`，用于验证错误上报链路。参数会作为异常信息，省略参数时使用内置文案。

<ChatExample
  :log="[
    '用户：~raise 测试错误上报',
    '机器人：执行命令时发生错误：',
    '测试错误上报',
    '请将此信息报告给机器人所有者。',
  ]"
/>
