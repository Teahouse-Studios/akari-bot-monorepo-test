---
order: 60
---

# features

此模块可以查看当前会话的能力标志。模块级权限为超级用户。

### `features`

<CommandUsage usage="features" permission="superuser" />

此命令逐项列出当前会话的能力标志，并主动获取同一场景的会话作为对照，有差异的项用 `*` 标出。主动获取失败时，主动会话一列显示未知。字段来自 `Features`，见[适配器开发](../../../core/doc/adapter-development.md)。

<ChatExample
  :log="[
    '用户：~features',
    '机器人：QQ|Group 的特性标志（当前会话 / 主动会话）：',
    'support_image: 是 / 是',
    'support_audio: 否 / 否',
  ]"
/>
