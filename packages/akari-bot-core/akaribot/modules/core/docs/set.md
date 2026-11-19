---
order: 16
---

# set

此模块可以直接改写目标场景或用户的数据。模块级权限为超级用户。参数中的 ID 须带平台前缀。目标场景不存在时，机器人会先请你确认，再创建。

### `set target module enable`

<CommandUsage usage="set target module enable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要启用的模块名，可给出多个']" permission="superuser" />

此命令在目标场景启用模块。不在当前平台可用列表中的模块名会被忽略。如果给出的模块名全都无效，命令返回失败提示。

<ChatExample
  :log="[
    '用户：~set target module enable QQ|Group|123456789 wiki',
    '机器人：成功为群聊开启以下模块：wiki',
  ]"
/>

### `set target module disable`

<CommandUsage usage="set target module disable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要停用的模块名，可给出多个']" permission="superuser" />

此命令在目标场景停用模块，只处理该场景已启用的模块。

<ChatExample
  :log="[
    '用户：~set target module disable QQ|Group|123456789 wiki',
    '机器人：成功为群聊关闭以下模块：wiki',
  ]"
/>

### `set target module list`

<CommandUsage usage="set target module list <target>" :params="['target=带平台前缀的场景完整 ID']" permission="superuser" />

此命令列出目标场景已启用的模块，按名称排序。

<ChatExample
  :log="[
    '用户：~set target module list QQ|Group|123456789',
    '机器人：此群聊已开启的模块：',
    'dice | wiki',
  ]"
/>

### `set target data get`

<CommandUsage usage="set target data get <target> [<k>]" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名，省略时列出全部']" permission="superuser" />

此命令读取场景数据。省略键时列出全部键值，给出键时只返回该键的值。常见场景数据键包括 `command_prefix`、`cooldown_time`。

<ChatExample
  :log="[
    '用户：~set target data get QQ|Group|123456789 cooldown_time',
    '机器人：5',
  ]"
/>

### `set target data edit`

<CommandUsage usage="set target data edit <target> <k> <v>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

此命令写入场景数据。`<v>` 为 `[...]` 或 `{...}` 时按 JSON 解析。值为 `true` 或 `false` 时存为布尔值，其余按字符串写入。

<ChatExample
  :log="[
    '用户：~set target data edit QQ|Group|123456789 cooldown_time 5',
    '机器人：成功为群聊设置了以下参数：cooldown_time -> 5',
  ]"
/>

### `set target data delete`

<CommandUsage usage="set target data delete <target> <k>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名']" permission="superuser" />

此命令删除场景数据键。

<ChatExample
  :log="[
    '用户：~set target data delete QQ|Group|123456789 cooldown_time',
    '机器人：成功。',
  ]"
/>

### `set sender data get`

<CommandUsage usage="set sender data get <user> [<k>]" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名，省略时列出全部']" permission="superuser" />

此命令读取用户数据。省略键时列出全部键值，给出键时只返回该键的值。常见用户数据键包括 `typing_prompt`、`module_auth`。

<ChatExample
  :log="[
    '用户：~set sender data get QQ|123456 dark_mode',
    '机器人：True',
  ]"
/>

### `set sender data edit`

<CommandUsage usage="set sender data edit <user> <k> <v>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

此命令写入用户数据，值的解析规则与 `set target data edit` 相同。

<ChatExample
  :log="[
    '用户：~set sender data edit QQ|123456 dark_mode true',
    '机器人：成功为群聊设置了以下参数：dark_mode -> True',
  ]"
/>

### `set sender data delete`

<CommandUsage usage="set sender data delete <user> <k>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名']" permission="superuser" />

此命令删除用户数据键。

<ChatExample
  :log="[
    '用户：~set sender data delete QQ|123456 dark_mode',
    '机器人：成功。',
  ]"
/>
