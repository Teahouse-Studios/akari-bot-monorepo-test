---
order: 60
---

# features

模块级权限为超级用户。

### `features`

<CommandUsage usage="features" permission="superuser" />

逐项列出当前会话的能力标志。同时抓取该场景的会话快照作对比，差异项以 `*` 标出，抓取失败时第二列显示未知。字段来自 `Features`，见[适配器开发](../../../core/doc/adapter-development.md)。

<ChatExample
  :log="[
    '用户：~features',
    '机器人：QQ|Group 的特性标志（当前会话 / 主动会话）：',
    'support_image: 是 / 是',
    'support_audio: 否 / 否',
  ]"
/>
