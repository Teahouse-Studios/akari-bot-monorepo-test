# 管理

本组包含场景管理与权限维护命令：`admin`、`mute`、`module`、`auth`、`superuser`、`abuse`、`set`、`purge`。

## admin

模块级权限为场景管理员。别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应子命令。

### `admin add`

<CommandUsage usage="admin add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

将用户加入本场景管理员。`<user>` 须为带平台前缀的完整 ID（如 `QQ|123456`），缺少前缀时提示先用 `bind whoami` 查询。平台原生管理员与已在列表中的用户无需执行该命令。

<ChatExample
  :log="[
    '用户：~admin add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为机器人管理员。',
  ]"
/>

### `admin remove`

<CommandUsage usage="admin remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

移除场景管理员。移除自己时须按提示输入确认内容后才执行；平台原生管理员身份不受该命令影响。

<ChatExample
  :log="[
    '用户：~admin remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出机器人管理员。',
  ]"
/>

### `admin list`

<CommandUsage usage="admin list" permission="admin" />

列出本场景的管理员，按 union 展开为绑定的平台账号，一行对应一个 union。

<ChatExample
  :log="[
    '用户：~admin list',
    '机器人：当前被手动设置的机器人管理员：',
    'QQ|123456',
  ]"
/>

### `admin ban`

<CommandUsage usage="admin ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

禁止用户在本场景使用机器人。不能封禁自己。封禁记录按 union 存储，同一用户绑定的其它平台账号一并生效。

<ChatExample
  :log="[
    '用户：~admin ban QQ|123456',
    '机器人：成功限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin unban`

<CommandUsage usage="admin unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

解除对用户的封禁。

<ChatExample
  :log="[
    '用户：~admin unban QQ|123456',
    '机器人：成功取消限制用户 QQ|123456 使用机器人。',
  ]"
/>

### `admin ban list`

<CommandUsage usage="admin ban list" permission="admin" />

列出本场景被禁止的用户，按 union 展开为绑定的平台账号。

<ChatExample
  :log="[
    '用户：~admin ban list',
    '机器人：当前被设置限制使用机器人的成员：',
    'QQ|123456',
  ]"
/>

### `admin leave`

<CommandUsage usage="admin leave" permission="admin" platforms="QQ 群聊" />

仅 QQ 群聊可用。使机器人退出当前群聊，执行前须确认。命令只注册于 `QQ|Group` 场景。

<ChatExample
  :log="[
    '用户：~admin leave',
    '机器人：你确定吗？此操作不可逆。',
    '用户：是',
    '机器人：已执行，再见。',
  ]"
/>

## mute

模块级权限为场景管理员。

### `mute`

<CommandUsage usage="mute" permission="admin" />

切换本场景的静音状态。静音期间除 `mute` 外的命令与正则都不执行，对静音场景的主动推送同样被抑制；再次执行恢复。

<ChatExample
  :log="[
    '用户：~mute',
    '机器人：成功静音。',
    '用户：~mute',
    '机器人：成功取消静音。',
  ]"
/>

## module

命令级权限按子命令区分，`list` 对所有人开放，`enable` 与 `disable` 要求场景管理员，`load`、`reload`、`unload` 要求超级用户。别名 `enable`、`disable`、`load`、`reload`、`unload` 可省略 `module`。

### `module list`

<CommandUsage usage="module list [--legacy] [--img]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

列出当前平台可用的模块及启用状态。默认渲染为图片表格，`--legacy` 改用文本表格。

<ChatExample
  :log="[
    '用户：~module list --legacy',
    '机器人：当前可用的模块有：',
    '🔐 arcaea | 🔐 cytoid | 🔐 dice | 🔐 hitokoto',
    '使用“`~help <模块名称>`”查看详细信息。',
  ]"
/>

### `module enable`

<CommandUsage usage="module enable <module>..." :params="['module=要启用的模块名，可给出多个']" permission="admin" />

在场景内启用指定模块，一次可给出多个。启用前检查平台能力（正则、事件、RSS）与机器人权限，缺失时给出具体原因；模块声明了推荐模块时，随后询问是否一并启用。

<ChatExample
  :log="[
    '用户：~module enable dice',
    '机器人：成功：开启模块“dice”。',
  ]"
/>

### `module enable all`

<CommandUsage usage="module enable all" permission="admin" />

启用全部可启用模块，跳过基础模块、隐藏模块、仅超级用户授权使用的模块，以及当前平台不支持或缺少机器人权限的模块。

<ChatExample
  :log="[
    '用户：~module enable all',
    '机器人：成功：开启模块“arcaea”。',
    '成功：开启模块“dice”。',
    '成功：开启模块“hitokoto”。',
  ]"
/>

### `module disable`

<CommandUsage usage="module disable <module>..." :params="['module=要停用的模块名，可给出多个']" permission="admin" />

在场景内停用指定模块。基础模块不可停用，该情形返回提示而不改动场景配置。

<ChatExample
  :log="[
    '用户：~module disable dice',
    '机器人：成功：关闭模块“dice”。',
  ]"
/>

### `module disable all`

<CommandUsage usage="module disable all" permission="admin" />

停用全部可停用模块，跳过基础模块、隐藏模块与仅超级用户授权使用的模块。

<ChatExample
  :log="[
    '用户：~module disable all',
    '机器人：成功：关闭模块“arcaea”。',
    '成功：关闭模块“dice”。',
    '成功：关闭模块“hitokoto”。',
  ]"
/>

### `module load`

<CommandUsage usage="module load <module>..." :params="['module=要加载的模块名，可给出多个']" permission="superuser" />

加载已卸载的模块，对所有场景生效。

<ChatExample
  :log="[
    '用户：~module load dice',
    '机器人：成功加载模块：dice',
  ]"
/>

### `module reload`

<CommandUsage usage="module reload <module>..." :params="['module=要重载的模块名，可给出多个']" permission="superuser" />

重新加载指定模块。依赖该模块的其它模块一并重载，重载范围超出给定模块时执行前列出范围并要求确认。

<ChatExample
  :log="[
    '用户：~module reload dice',
    '机器人：成功重载模块：',
    'dice',
    '未发现已加载的其余文件。',
  ]"
/>

### `module unload`

<CommandUsage usage="module unload <module>..." :params="['module=要卸载的模块名，可给出多个']" permission="superuser" />

卸载已加载的模块，对所有场景生效。基础模块不可卸载。

<ChatExample
  :log="[
    '用户：~module unload dice',
    '机器人：成功卸载模块：dice',
  ]"
/>

## auth

模块级权限为超级用户，只对声明了 `required_superuser` 的模块生效。

### `auth add`

<CommandUsage usage="auth add <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户授权使用的模块名']" permission="superuser" />

授权用户在指定模块中执行超级用户命令。目标模块未声明 `required_superuser` 时拒绝执行；授权记录同时保存授权者，执行前要求确认。

<ChatExample
  :log="[
    '用户：~auth add QQ|123456 update',
    '机器人：你确定吗？',
    '（此为危险操作，完全发送“我授权用户 QQ|123456 使用模块 update。”来确认）',
    '用户：我授权用户 QQ|123456 使用模块 update。',
  ]"
/>

### `auth remove`

<CommandUsage usage="auth remove <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户授权使用的模块名']" permission="superuser" />

撤销授权，只删除本人授予的条目。授权者失去超级用户身份后，该条授权不再生效。

<ChatExample
  :log="[
    '用户：~auth remove QQ|123456 update',
    '机器人：已取消 QQ|123456 使用模块 update 的授权。',
  ]"
/>

### `auth list`

<CommandUsage usage="auth list <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

列出用户获得的模块授权。

<ChatExample
  :log="[
    '用户：~auth list QQ|123456',
    '机器人：QQ|123456 被 QQ|654321 授权使用模块 update',
  ]"
/>

## superuser

<ModuleAlias names="su" />

模块级权限为超级用户。

### `superuser add`

<CommandUsage usage="superuser add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户设为超级用户。用户尚未建立 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~superuser add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为超级用户。',
  ]"
/>

### `superuser remove`

<CommandUsage usage="superuser remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

取消用户的超级用户身份。移除自己时须按提示输入确认内容。`config.toml` 的 `base_superuser` 属于基础超级用户，在启动时写入数据库，只能通过配置维护。

<ChatExample
  :log="[
    '用户：~superuser remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出超级用户。',
  ]"
/>

## abuse

<ModuleAlias names="ae" />

模块级权限为超级用户。

### `abuse check`

<CommandUsage usage="abuse check <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

查看用户的警告次数、临时封禁与黑白名单状态。用户尚无 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~abuse check QQ|123456',
    '机器人：用户 QQ|123456 已被警告 2 次。',
    '（此用户已处于黑名单）',
  ]"
/>

### `abuse warn`

<CommandUsage usage="abuse warn <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=增加的警告次数，缺省为 1']" permission="superuser" />

增加警告次数，`<count>` 缺省为 1。累计次数超过 `tos_warning_counts` 且用户不在白名单时，用户转入黑名单。临时封禁的时长取自 `tos_temp_ban_time`，由 `tos` 钩子执行，见[解析器](parser.md)。

<ChatExample
  :log="[
    '用户：~abuse warn QQ|123456',
    '机器人：成功警告用户 QQ|123456 1 次。此用户已被警告 3 次。',
  ]"
/>

### `abuse revoke`

<CommandUsage usage="abuse revoke <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=减少的警告次数，缺省为 1']" permission="superuser" />

减少警告次数，`<count>` 缺省为 1。

<ChatExample
  :log="[
    '用户：~abuse revoke QQ|123456',
    '机器人：成功移除用户 QQ|123456 的 1 次警告。此用户已被警告 2 次。',
  ]"
/>

### `abuse clear`

<CommandUsage usage="abuse clear <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户的警告次数清零。

<ChatExample
  :log="[
    '用户：~abuse clear QQ|123456',
    '机器人：成功清除用户 QQ|123456 的警告。',
  ]"
/>

### `abuse untempban`

<CommandUsage usage="abuse untempban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

解除临时封禁，交由 `tos.remove_temp_ban` 钩子处理。

<ChatExample
  :log="[
    '用户：~abuse untempban QQ|123456',
    '机器人：成功解除用户 QQ|123456 的临时封禁。',
  ]"
/>

### `abuse ban`

<CommandUsage usage="abuse ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入黑名单并清除白名单身份。

<ChatExample
  :log="[
    '用户：~abuse ban QQ|123456',
    '机器人：成功将用户 QQ|123456 加入黑名单。',
  ]"
/>

### `abuse unban`

<CommandUsage usage="abuse unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出黑名单。

<ChatExample
  :log="[
    '用户：~abuse unban QQ|123456',
    '机器人：成功将用户 QQ|123456 移除黑名单。',
  ]"
/>

### `abuse trust`

<CommandUsage usage="abuse trust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入白名单并移出黑名单。白名单用户不触发警告封禁。

<ChatExample
  :log="[
    '用户：~abuse trust QQ|123456',
    '机器人：成功将用户 QQ|123456 加入白名单。',
  ]"
/>

### `abuse distrust`

<CommandUsage usage="abuse distrust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出白名单。

<ChatExample
  :log="[
    '用户：~abuse distrust QQ|123456',
    '机器人：成功将用户 QQ|123456 移除白名单。',
  ]"
/>

### `abuse block`

<CommandUsage usage="abuse block <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" platforms="QQ" />

仅 QQ 可用。屏蔽指定场景，`<target>` 须为 `QQ|Group|` 前缀的完整 ID，且不能是当前场景。

<ChatExample
  :log="[
    '用户：~abuse block QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 加入黑名单。',
  ]"
/>

### `abuse unblock`

<CommandUsage usage="abuse unblock <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" platforms="QQ" />

仅 QQ 可用。解除对指定场景的屏蔽。

<ChatExample
  :log="[
    '用户：~abuse unblock QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 移除黑名单。',
  ]"
/>

## set

模块级权限为超级用户，直接改写目标场景或用户的数据，参数中的 ID 须带平台前缀。目标场景不存在时先确认再创建。

### `set target module enable`

<CommandUsage usage="set target module enable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要启用的模块名，可给出多个']" permission="superuser" />

在目标场景启用模块。不在当前平台可用列表中的模块名被忽略，全部无效时返回失败提示。

<ChatExample
  :log="[
    '用户：~set target module enable QQ|Group|123456789 wiki',
    '机器人：成功为群聊开启以下模块：wiki',
  ]"
/>

### `set target module disable`

<CommandUsage usage="set target module disable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要停用的模块名，可给出多个']" permission="superuser" />

在目标场景停用模块，只处理目标场景已启用的模块。

<ChatExample
  :log="[
    '用户：~set target module disable QQ|Group|123456789 wiki',
    '机器人：成功为群聊关闭以下模块：wiki',
  ]"
/>

### `set target module list`

<CommandUsage usage="set target module list <target>" :params="['target=带平台前缀的场景完整 ID']" permission="superuser" />

列出目标场景已启用的模块，按名称排序。

<ChatExample
  :log="[
    '用户：~set target module list QQ|Group|123456789',
    '机器人：此群聊已开启的模块：',
    'dice | wiki',
  ]"
/>

### `set target data get`

<CommandUsage usage="set target data get <target> [<k>]" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名，省略时列出全部']" permission="superuser" />

读取场景数据。省略键时列出全部键值，场景数据键如 `command_prefix`、`cooldown_time`。

<ChatExample
  :log="[
    '用户：~set target data get QQ|Group|123456789 cooldown_time',
    '机器人：5',
  ]"
/>

### `set target data edit`

<CommandUsage usage="set target data edit <target> <k> <v>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

写入场景数据。`<v>` 为 `[...]` 或 `{...}` 时按 JSON 解析，`true`、`false` 转为布尔值，其余按字符串写入。

<ChatExample
  :log="[
    '用户：~set target data edit QQ|Group|123456789 cooldown_time 5',
    '机器人：成功为群聊设置了以下参数：cooldown_time -> 5',
  ]"
/>

### `set target data delete`

<CommandUsage usage="set target data delete <target> <k>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名']" permission="superuser" />

删除场景数据键。

<ChatExample
  :log="[
    '用户：~set target data delete QQ|Group|123456789 cooldown_time',
    '机器人：成功。',
  ]"
/>

### `set sender data get`

<CommandUsage usage="set sender data get <user> [<k>]" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名，省略时列出全部']" permission="superuser" />

读取用户数据。省略键时列出全部键值，用户数据键如 `typing_prompt`、`module_auth`。

<ChatExample
  :log="[
    '用户：~set sender data get QQ|123456 dark_mode',
    '机器人：True',
  ]"
/>

### `set sender data edit`

<CommandUsage usage="set sender data edit <user> <k> <v>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

写入用户数据，值的解析规则与 `set target data edit` 相同。

<ChatExample
  :log="[
    '用户：~set sender data edit QQ|123456 dark_mode true',
    '机器人：成功为群聊设置了以下参数：dark_mode -> True',
  ]"
/>

### `set sender data delete`

<CommandUsage usage="set sender data delete <user> <k>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名']" permission="superuser" />

删除用户数据键。

<ChatExample
  :log="[
    '用户：~set sender data delete QQ|123456 dark_mode',
    '机器人：成功。',
  ]"
/>

## purge

模块级权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

清空实例 `cache/` 目录，目录为空时给出提示。同一模块注册了按 `auto_purge_crontab`（默认 `0 0 * * *`）执行的定时清理，命令与定时任务都不触碰 `data/` 与数据库。

<ChatExample
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
