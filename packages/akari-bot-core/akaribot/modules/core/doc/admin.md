# 管理

本组包含场景管理与权限维护命令：`admin`、`mute`、`module`、`auth`、`superuser`、`abuse`、`set`、`purge`。

## admin

模块级权限为场景管理员。别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应子命令。

### `admin add`

<CommandUsage usage="admin add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

将用户加入本场景管理员。`<user>` 须为带平台前缀的完整 ID（如 `QQ|123456`），缺少前缀时提示先用 `bind whoami` 查询。平台原生管理员与已在列表中的用户无需执行该命令。

### `admin remove`

<CommandUsage usage="admin remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

移除场景管理员。移除自己时须按提示输入确认内容后才执行；平台原生管理员身份不受该命令影响。

### `admin list`

<CommandUsage usage="admin list" permission="admin" />

列出本场景的管理员，按 union 展开为绑定的平台账号，一行对应一个 union。

### `admin ban`

<CommandUsage usage="admin ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

禁止用户在本场景使用机器人。不能封禁自己。封禁记录按 union 存储，同一用户绑定的其它平台账号一并生效。

### `admin unban`

<CommandUsage usage="admin unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="admin" />

解除对用户的封禁。

### `admin ban list`

<CommandUsage usage="admin ban list" permission="admin" />

列出本场景被禁止的用户，按 union 展开为绑定的平台账号。

### `admin leave`

<CommandUsage usage="admin leave" permission="admin" />

仅 QQ 群聊可用。使机器人退出当前群聊，执行前须确认。命令只注册于 `QQ|Group` 场景。

## mute

模块级权限为场景管理员。

### `mute`

<CommandUsage usage="mute" permission="admin" />

切换本场景的静音状态。静音期间除 `mute` 外的命令与正则都不执行，对静音场景的主动推送同样被抑制；再次执行恢复。

## module

命令级权限按子命令区分，`list` 对所有人开放，`enable` 与 `disable` 要求场景管理员，`load`、`reload`、`unload` 要求超级用户。别名 `enable`、`disable`、`load`、`reload`、`unload` 可省略 `module`。

### `module list`

<CommandUsage usage="module list [--legacy] [--img]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

列出当前平台可用的模块及启用状态。默认渲染为图片表格，`--legacy` 改用文本表格。

### `module enable`

<CommandUsage usage="module enable <module>..." :params="['module=要启用的模块名，可给出多个']" permission="admin" />

在场景内启用指定模块，一次可给出多个。启用前检查平台能力（正则、事件、RSS）与机器人权限，缺失时给出具体原因；模块声明了推荐模块时，随后询问是否一并启用。

### `module enable all`

<CommandUsage usage="module enable all" permission="admin" />

启用全部可启用模块，跳过基础模块、隐藏模块、仅超级用户可用的模块，以及当前平台不支持或缺少机器人权限的模块。

### `module disable`

<CommandUsage usage="module disable <module>..." :params="['module=要停用的模块名，可给出多个']" permission="admin" />

在场景内停用指定模块。基础模块不可停用，该情形返回提示而不改动场景配置。

### `module disable all`

<CommandUsage usage="module disable all" permission="admin" />

停用全部可停用模块，跳过基础模块、隐藏模块与仅超级用户可用的模块。

### `module load`

<CommandUsage usage="module load <module>..." :params="['module=要加载的模块名，可给出多个']" permission="superuser" />

加载已卸载的模块，对所有场景生效。

### `module reload`

<CommandUsage usage="module reload <module>..." :params="['module=要重载的模块名，可给出多个']" permission="superuser" />

重新加载指定模块。依赖该模块的其它模块一并重载，重载范围超出给定模块时执行前列出范围并要求确认。

### `module unload`

<CommandUsage usage="module unload <module>..." :params="['module=要卸载的模块名，可给出多个']" permission="superuser" />

卸载已加载的模块，对所有场景生效。基础模块不可卸载。

## auth

模块级权限为超级用户，只对声明了 `required_superuser` 的模块生效。

### `auth add`

<CommandUsage usage="auth add <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户可用的模块名']" permission="superuser" />

授权用户在指定模块中执行超级用户命令。目标模块未声明 `required_superuser` 时拒绝执行；授权记录同时保存授权者，执行前要求确认。

### `auth remove`

<CommandUsage usage="auth remove <user> <module>" :params="['user=带平台前缀的用户完整 ID', 'module=声明了仅超级用户可用的模块名']" permission="superuser" />

撤销授权，只删除本人授予的条目。授权者失去超级用户身份后，该条授权不再生效。

### `auth list`

<CommandUsage usage="auth list <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

列出用户获得的模块授权。

## superuser

<ModuleAlias names="su" />

模块级权限为超级用户。

### `superuser add`

<CommandUsage usage="superuser add <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户设为超级用户。用户尚未建立 union 时先确认再创建。

### `superuser remove`

<CommandUsage usage="superuser remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

取消用户的超级用户身份。移除自己时须按提示输入确认内容。`config.toml` 的 `base_superuser` 属于基础超级用户，在启动时写入数据库，只能通过配置维护。

## abuse

<ModuleAlias names="ae" />

模块级权限为超级用户。

### `abuse check`

<CommandUsage usage="abuse check <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

查看用户的警告次数、临时封禁与黑白名单状态。用户尚无 union 时先确认再创建。

### `abuse warn`

<CommandUsage usage="abuse warn <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=增加的警告次数，缺省为 1']" permission="superuser" />

增加警告次数，`<count>` 缺省为 1。累计次数超过 `tos_warning_counts` 且用户不在白名单时，用户转入黑名单。临时封禁的时长取自 `tos_temp_ban_time`，由 `tos` 钩子执行，见[解析器](parser.md)。

### `abuse revoke`

<CommandUsage usage="abuse revoke <user> [<count>]" :params="['user=带平台前缀的用户完整 ID', 'count=减少的警告次数，缺省为 1']" permission="superuser" />

减少警告次数，`<count>` 缺省为 1。

### `abuse clear`

<CommandUsage usage="abuse clear <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户的警告次数清零。

### `abuse untempban`

<CommandUsage usage="abuse untempban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

解除临时封禁，交由 `tos.remove_temp_ban` 钩子处理。

### `abuse ban`

<CommandUsage usage="abuse ban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入黑名单并清除白名单身份。

### `abuse unban`

<CommandUsage usage="abuse unban <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出黑名单。

### `abuse trust`

<CommandUsage usage="abuse trust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户加入白名单并移出黑名单。白名单用户不触发警告封禁。

### `abuse distrust`

<CommandUsage usage="abuse distrust <user>" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

将用户移出白名单。

### `abuse block`

<CommandUsage usage="abuse block <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" />

仅 QQ 可用。屏蔽指定场景，`<target>` 须为 `QQ|Group|` 前缀的完整 ID，且不能是当前场景。

### `abuse unblock`

<CommandUsage usage="abuse unblock <target>" :params="['target=带 QQ|Group| 前缀的场景 ID']" permission="superuser" />

仅 QQ 可用。解除对指定场景的屏蔽。

## set

模块级权限为超级用户，直接改写目标场景或用户的数据，参数中的 ID 须带平台前缀。目标场景不存在时先确认再创建。

### `set target module enable`

<CommandUsage usage="set target module enable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要启用的模块名，可给出多个']" permission="superuser" />

在目标场景启用模块。不在当前平台可用列表中的模块名被忽略，全部无效时返回失败提示。

### `set target module disable`

<CommandUsage usage="set target module disable <target> <modules>..." :params="['target=带平台前缀的场景完整 ID', 'modules=要停用的模块名，可给出多个']" permission="superuser" />

在目标场景停用模块，只处理目标场景已启用的模块。

### `set target module list`

<CommandUsage usage="set target module list <target>" :params="['target=带平台前缀的场景完整 ID']" permission="superuser" />

列出目标场景已启用的模块，按名称排序。

### `set target data get`

<CommandUsage usage="set target data get <target> [<k>]" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名，省略时列出全部']" permission="superuser" />

读取场景数据。省略键时列出全部键值，场景数据键如 `command_prefix`、`cooldown_time`。

### `set target data edit`

<CommandUsage usage="set target data edit <target> <k> <v>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

写入场景数据。`<v>` 为 `[...]` 或 `{...}` 时按 JSON 解析，`true`、`false` 转为布尔值，其余按字符串写入。

### `set target data delete`

<CommandUsage usage="set target data delete <target> <k>" :params="['target=带平台前缀的场景完整 ID', 'k=场景数据键名']" permission="superuser" />

删除场景数据键。

### `set sender data get`

<CommandUsage usage="set sender data get <user> [<k>]" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名，省略时列出全部']" permission="superuser" />

读取用户数据。省略键时列出全部键值，用户数据键如 `typing_prompt`、`module_auth`。

### `set sender data edit`

<CommandUsage usage="set sender data edit <user> <k> <v>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名', 'v=新值，JSON、布尔值或字符串']" permission="superuser" />

写入用户数据，值的解析规则与 `set target data edit` 相同。

### `set sender data delete`

<CommandUsage usage="set sender data delete <user> <k>" :params="['user=带平台前缀的用户完整 ID', 'k=用户数据键名']" permission="superuser" />

删除用户数据键。

## purge

模块级权限为超级用户。

### `purge`

<CommandUsage usage="purge" permission="superuser" />

清空实例 `cache/` 目录，目录为空时给出提示。同一模块注册了按 `auto_purge_crontab`（默认 `0 0 * * *`）执行的定时清理，命令与定时任务都不触碰 `data/` 与数据库。
