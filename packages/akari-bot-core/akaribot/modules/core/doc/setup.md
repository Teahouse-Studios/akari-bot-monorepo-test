---
order: 21
---

# setup

模块为基础模块，别名 `toggle`、`prefix`、`locale`、`lang`、`alias` 分别指向对应子命令。命令同时作用于场景域与个人域，`setup list` 展示全部设置项。

### `setup typing`

<CommandUsage usage="setup typing" permission="public" />

切换“正在输入”提示，缺省开启，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup typing',
    '机器人：已关闭输入提示。',
  ]"
/>

### `setup check`

<CommandUsage usage="setup check" permission="public" />

切换命令拼写检查，缺省开启，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup check',
    '机器人：已关闭命令语法检查提示。',
  ]"
/>

### `setup markdown`

<CommandUsage usage="setup markdown" permission="public" />

切换 Markdown 渲染，设置保存在个人域。平台不支持该开关时返回提示，配置不变。

<ChatExample
  :log="[
    '用户：~setup markdown',
    '机器人：此平台不支持 Markdown 消息。',
  ]"
/>

### `setup dark`

<CommandUsage usage="setup dark" permission="public" />

切换暗色模式，设置保存在个人域。

<ChatExample
  :log="[
    '用户：~setup dark',
    '机器人：已开启深色模式。',
  ]"
/>

### `setup list`

<CommandUsage :usage="['setup list', 'setup list target', 'setup list sender']" permission="public" />

展示设置面板。省略域参数时同时列出场景域与个人域；场景域的修改入口按场景管理员权限显示，个人域对所有人开放。

<ChatExample
  :log="[
    '用户：~setup list',
    '机器人：【群聊设置】',
    '语言：简体中文 修改（`~setup locale zh_cn`）',
    '静音：已关闭 开启（`~mute`）',
  ]"
/>

### `setup prefix list`

<CommandUsage usage="setup prefix list" permission="public" />

列出默认命令前缀与本场景的自定义前缀。

<ChatExample
  :log="[
    '用户：~setup prefix list',
    '机器人：默认命令前缀：~, ～',
    '自定义命令前缀为空。',
  ]"
/>

### `setup prefix add`

<CommandUsage usage="setup prefix add <prefix>" :params="['prefix=要添加的命令前缀']" permission="admin" />

增加场景命令前缀。前缀已存在时返回重复提示。

<ChatExample
  :log="[
    '用户：~setup prefix add !',
    '机器人：已添加自定义命令前缀：!',
  ]"
/>

### `setup prefix remove`

<CommandUsage usage="setup prefix remove <prefix>" :params="['prefix=要移除的命令前缀']" permission="admin" />

移除场景命令前缀，前缀不存在时返回未找到提示。

<ChatExample
  :log="[
    '用户：~setup prefix remove !',
    '机器人：已移除自定义命令前缀：!',
  ]"
/>

### `setup prefix reset`

<CommandUsage usage="setup prefix reset" permission="admin" />

清空场景自定义前缀。

<ChatExample
  :log="[
    '用户：~setup prefix reset',
    '机器人：已重置自定义命令前缀列表。',
  ]"
/>

### `setup locale`

<CommandUsage :usage="['setup locale', 'setup locale [<lang>]']" :params="['lang=语言代码，如 zh_cn']" permission="public" />

省略语言代码时列出可用语言与翻译进度；给出语言代码时设置场景语言，该形式要求场景管理员权限。语言代码不在可用列表内时返回提示并列出可选值。

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

重新加载语言文件。加载失败时返回提示并列出出错的文件。

<ChatExample
  :log="[
    '用户：~setup locale reload',
    '机器人：成功。',
  ]"
/>

### `setup alias list`

<CommandUsage usage="setup alias list [--legacy]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}]" />

列出场景自定义命令别名，默认渲染为图片表格，`--legacy` 改用文本表格。

<ChatExample
  :log="[
    '用户：~setup alias list --legacy',
    '机器人：自定义命令别名列表：',
    'wk -> ~wiki',
  ]"
/>

### `setup alias add`

<CommandUsage usage="setup alias add <alias> <command>" :params="['alias=自定义命令别名', 'command=替换文本，须以命令前缀开头']" permission="admin" />

增加场景命令别名。替换文本须以命令前缀开头，别名与替换文本都须含占位符之外的文字，占位符写作 `${名称}`；不满足时返回对应提示。别名重复时返回已存在提示。

<ChatExample
  :log="[
    '用户：~setup alias add wk ~wiki',
    '机器人：已添加自定义命令别名：wk -> ~wiki',
  ]"
/>

### `setup alias remove`

<CommandUsage usage="setup alias remove <alias>" :params="['alias=自定义命令别名']" permission="admin" />

移除场景命令别名。

<ChatExample
  :log="[
    '用户：~setup alias remove wk',
    '机器人：已移除自定义命令别名：wk',
  ]"
/>

### `setup alias reset`

<CommandUsage usage="setup alias reset" permission="admin" />

清空场景命令别名。

<ChatExample
  :log="[
    '用户：~setup alias reset',
    '机器人：已重置自定义命令别名列表。',
  ]"
/>

### `setup timeoffset`

<CommandUsage usage="setup timeoffset <offset>" :params="['offset=时区偏移，如 8、-5:30；reset 恢复默认值']" permission="admin" />

设置场景时区偏移，格式为 `8`、`-5:30`。小时超过 12 或分钟达到 60 时提示格式错误；写入时规范化为 `+8`、`-5:30` 形式。参数为 `reset` 时清除场景偏移，恢复为未设置。

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

设置个人显示时区偏移，覆盖场景时区，格式与 `setup timeoffset` 相同。参数为 `reset` 时清除个人偏移，恢复为跟随场景时区。

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

设置场景命令冷却秒数，负数按 0 处理。

<ChatExample
  :log="[
    '用户：~setup cooldown 5',
    '机器人：已将命令冷却时间设置为 5 秒。',
  ]"
/>

### `setup invalid-module-prompt`

<CommandUsage usage="setup invalid-module-prompt" permission="admin" />

切换未知模块的提示。

<ChatExample
  :log="[
    '用户：~setup invalid-module-prompt',
    '机器人：已关闭“模块不存在”提示。',
  ]"
/>

### `setup sign`

<CommandUsage usage="setup sign" permission="admin" />

仅在 enable_petal 为真时注册。切换场景签到开关，缺省开启，由 `petal` 模块的签到命令读取。

### `setup emote`

<CommandUsage usage="setup emote" permission="admin" />

仅在 use_emote 为真时注册。切换场景表情开关。

## 数据键

`setup` 与 `set` 改写的键存放在 union 的 JSON 列：

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
| 个人 | `dark_mode` | 暗色模式 |
| 个人 | `timezone_offset` | 显示时区偏移 |
