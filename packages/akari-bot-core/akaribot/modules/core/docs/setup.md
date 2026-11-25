---
order: 21
---

# setup

此模块用于查看与修改机器人的设置。别名 `toggle`、`prefix`、`locale`、`lang` 与 `alias` 各自指向一条子命令。

这些命令分别作用于场景域与个人域。
`setup list` 展示全部设置项。

### `setup typing`

<CommandUsage usage="setup typing" permission="public" />

切换“正在输入”状态提示。此开关默认处于开启状态，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup typing',
    '机器人：已关闭输入提示。',
  ]"
/>

### `setup check`

<CommandUsage usage="setup check" permission="public" />

切换命令拼写检查。此开关默认处于开启状态，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup check',
    '机器人：已关闭命令语法检查提示。',
  ]"
/>

### `setup markdown`

<CommandUsage usage="setup markdown" permission="public" />

切换 Markdown 渲染开关，设置保存在个人域。若平台不支持 Markdown，机器人会返回提示信息，原设置保持不变。

<ChatExample
  :log="[
    '用户：~setup markdown',
    '机器人：此平台不支持 Markdown 消息。',
  ]"
/>

### `setup dark`

<CommandUsage usage="setup dark" permission="public" />

切换深色模式开关，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup dark',
    '机器人：已开启深色模式。',
  ]"
/>

### `setup list`

<CommandUsage :usage="['setup list', 'setup list target', 'setup list sender']" permission="public" />

展示设置面板。若省略域参数，面板会同时列出场景域与个人域。场景域的修改入口仅向场景管理员显示，个人域向所有用户开放。

<ChatExample
  :log="[
    '用户：~setup list',
    '机器人：【群聊设置】',
    '语言：简体中文 修改（`~setup locale zh_cn`）',
    '禁止发言：已关闭 开启（`~mute`）',
  ]"
/>

### `setup prefix list`

<CommandUsage usage="setup prefix list" permission="public" />

列出默认命令前缀与当前场景的自定义前缀。

<ChatExample
  :log="[
    '用户：~setup prefix list',
    '机器人：默认命令前缀：~, ～',
    '自定义命令前缀为空。',
  ]"
/>

### `setup prefix add`

<CommandUsage usage="setup prefix add <prefix>" :params="['prefix=要添加的命令前缀']" permission="admin" />

为当前场景添加命令前缀。若前缀已经存在，机器人会返回重复提示信息。

<ChatExample
  :log="[
    '用户：~setup prefix add !',
    '机器人：已添加自定义命令前缀：!',
  ]"
/>

### `setup prefix remove`

<CommandUsage usage="setup prefix remove <prefix>" :params="['prefix=要移除的命令前缀']" permission="admin" />

移除当前场景的命令前缀。若前缀不存在，机器人会返回未找到提示信息。

<ChatExample
  :log="[
    '用户：~setup prefix remove !',
    '机器人：已移除自定义命令前缀：!',
  ]"
/>

### `setup prefix reset`

<CommandUsage usage="setup prefix reset" permission="admin" />

清空当前场景的自定义命令前缀列表。

<ChatExample
  :log="[
    '用户：~setup prefix reset',
    '机器人：已重置自定义命令前缀列表。',
  ]"
/>

### `setup locale`

<CommandUsage :usage="['setup locale', 'setup locale [<lang>]']" :params="['lang=语言代码，如 zh_cn']" permission="public" />

若省略语言代码，则列出可用语言及其各自的翻译进度。若指定语言代码，命令会设置场景的语言，该操作需要场景管理员权限。若语言代码未包含在可用列表中，机器人会返回提示信息并列出可选值。

<ChatExample
  :log="[
    '用户：~setup locale',
    '机器人：当前使用的语言：简体中文',
    '使用“`~setup locale <语言代码>`”设置语言。',
    '支持的语言列表：\n简体中文\n繁體中文\nEnglish\n日本語\n한국어',
  ]"
/>

### `setup locale reload`

<CommandUsage usage="setup locale reload" permission="superuser" />

重新加载语言文件。加载失败时返回提示，并列出出错的文件。

<ChatExample
  :log="[
    '用户：~setup locale reload',
    '机器人：成功。',
  ]"
/>

### `setup alias list`

<CommandUsage usage="setup alias list [--legacy]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}]" />

列出场景自定义命令别名。结果默认渲染为图片表格，加 `--legacy` 时改用文本表格。

<ChatExample
  :log="[
    '用户：~setup alias list --legacy',
    '机器人：自定义命令别名列表：',
    'wk -> ~wiki',
  ]"
/>

### `setup alias add`

<CommandUsage usage="setup alias add <alias> <command>" :params="['alias=自定义命令别名', 'command=替换文本，须以命令前缀开头']" permission="admin" />

为当前场景添加命令别名。替换文本必须以命令前缀开头。

别名与替换文本均不能仅由占位符构成，且必须包含占位符之外的正文字符，占位符写作 `${名称}`。若不满足上述条件，机器人会返回对应提示信息。若别名重复，则返回已存在提示信息。

<ChatExample
  :log="[
    '用户：~setup alias add wk ~wiki',
    '机器人：已添加自定义命令别名：wk -> ~wiki',
  ]"
/>

### `setup alias remove`

<CommandUsage usage="setup alias remove <alias>" :params="['alias=自定义命令别名']" permission="admin" />

移除当前场景的自定义命令别名。

<ChatExample
  :log="[
    '用户：~setup alias remove wk',
    '机器人：已移除自定义命令别名：wk',
  ]"
/>

### `setup alias reset`

<CommandUsage usage="setup alias reset" permission="admin" />

清空当前场景的自定义命令别名列表。

<ChatExample
  :log="[
    '用户：~setup alias reset',
    '机器人：已重置自定义命令别名列表。',
  ]"
/>

### `setup timeoffset`

<CommandUsage usage="setup timeoffset <offset>" :params="['offset=时区偏移，如 8、-5:30；reset 恢复默认值']" permission="admin" />

设置场景的时区偏移，支持的格式为 `8`、`-5:30`。总偏移的取值范围为 -12 到 +14 小时。分钟数值达到 60 或偏移超出范围时，机器人会返回格式错误提示。写入时统一规范为 `+8`、`-5:30` 的形式。传入参数为 `reset` 时将清除场景偏移，恢复为未设置状态。

<ChatExample
  :log="[
    '用户：~setup timeoffset 8',
    '机器人：已将群聊时区设置为 UTC+8。',
  ]"
/>

<ChatExample
  :log="[
    '用户：~setup timeoffset reset',
    '机器人：已将群聊时区恢复为默认值。',
  ]"
/>

### `setup timezone`

<CommandUsage usage="setup timezone <offset>" :params="['offset=显示时区偏移，如 8、-5:30；reset 跟随场景时区']" permission="public" />

设置个人显示时区偏移，该设置会覆盖场景时区，格式与 `setup timeoffset` 保持一致。传入参数为 `reset` 时将清除个人偏移，恢复为跟随场景时区。

<ChatExample
  :log="[
    '用户：~setup timezone +3',
    '机器人：已将用户显示时区设置为 UTC+3。',
  ]"
/>

<ChatExample
  :log="[
    '用户：~setup timezone reset',
    '机器人：已恢复跟随群聊时区。',
  ]"
/>

### `setup cooldown`

<CommandUsage usage="setup cooldown <second>" :params="['second=命令冷却秒数']" permission="admin" />

设置场景的命令冷却秒数。负数值均按 0 处理。

<ChatExample
  :log="[
    '用户：~setup cooldown 5',
    '机器人：已将命令冷却时间设置为 5 秒。',
  ]"
/>

### `setup invalid-module-prompt`

<CommandUsage usage="setup invalid-module-prompt" permission="admin" />

切换未知模块提示信息的开关。

<ChatExample
  :log="[
    '用户：~setup invalid-module-prompt',
    '机器人：已关闭“模块不存在”提示。',
  ]"
/>

### `setup sign`

<CommandUsage usage="setup sign" permission="admin" />

此命令仅在 `enable_petal` 为 `true` 时注册，用于切换场景的签到开关。该开关默认处于开启状态，`petal` 模块的签到命令会读取此设置。

### `setup emote`

<CommandUsage usage="setup emote" permission="admin" />

此命令仅在 `use_emote` 为 `true` 时注册，用于切换场景的表情开关。

## 数据键

`setup` 与 `set` 写入的键存储在 union 的 JSON 列中：

| 域 | 键 | 用途 |
| --- | --- | --- |
| 场景 | `command_prefix` | 自定义命令前缀 |
| 场景 | `command_alias` | 自定义命令别名 |
| 场景 | `cooldown_time` | 命令冷却秒数 |
| 场景 | `timezone_offset` | 时区偏移 |
| 场景 | `invalid_module_prompt` | 未知模块提示开关 |
| 场景 | `use_emote` | 表情开关 |
| 场景 | `petal_sign` | 签到开关 |
| 个人 | `typing_prompt` | 输入状态提示 |
| 个人 | `typo_check` | 拼写检查 |
| 个人 | `use_markdown` | Markdown 渲染 |
| 个人 | `dark_mode` | 深色模式 |
| 个人 | `timezone_offset` | 显示时区偏移 |
