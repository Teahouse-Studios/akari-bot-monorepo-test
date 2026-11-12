# 会话

本组处理场景与身份的绑定、旧客户端迁移、花瓣积分与帮助：`bind`、`merge`、`petal`、`help`。

## bind

基础模块，负责把不同平台上的同一用户、同一现实场景归入同一个 union。别名 `whoami`、`merge`、`merge token` 指向对应子命令。

### `bind`

<CommandUsage usage="bind" permission="public" />

查看当前用户与当前场景各自所属的 union，以及其中已绑定的平台账号。

### `bind whoami`

<CommandUsage usage="bind whoami" permission="public" />

显示发送者的平台 ID、union ID 与权限身份，同时列出当前场景的平台 ID 与 union ID。场景管理员、平台原生管理员与超级用户身份分别标注。

### `bind self`

<CommandUsage usage="bind self" permission="public" />

列出当前用户绑定的全部账号。

### `bind start`

<CommandUsage usage="bind start" permission="public" />

群内执行要求场景管理员权限。生成绑定码。私聊中直接签发并同时包含发送者与私聊场景，兑换后两者一并绑定；群内只合并场景组。

### `bind token`

<CommandUsage usage="bind token <code>" :params="['code=另一处生成的绑定码']" permission="public" />

群内执行要求场景管理员权限。用绑定码完成绑定。绑定码的使用场景须与签发场景同属私聊或群聊，跨类型兑换被拒绝；绑定码失效时返回提示。

### `bind self remove`

<CommandUsage usage="bind self remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="public" />

解绑当前用户的某个账号，执行前要求确认。最后一个账号不可解绑。

### `bind target`

<CommandUsage usage="bind target" permission="admin" />

查看当前场景绑定的平台入口。

### `bind target remove`

<CommandUsage usage="bind target remove <target>" :params="['target=带平台前缀的场景完整 ID']" permission="admin" />

解绑当前场景的某个平台入口，执行前要求确认。最后一个入口不可解绑。

### `bind channel`

<CommandUsage usage="bind channel" permission="admin" />

查看当前场景的消息通道号，以及共用该通道的其它场景数量与编号。

### `bind channel set`

<CommandUsage usage="bind channel set <channel>" :params="['channel=消息通道号']" permission="admin" />

设置当前场景的消息通道号，通道号相同的场景在命令与推送上去重。

### `bind channel reset`

<CommandUsage usage="bind channel reset" permission="admin" />

把当前场景的消息通道号重置为默认值。

### `bind auto`

<CommandUsage usage="bind auto" permission="admin" />

仅在 enable_bind_auto 为真时注册。与同一场景内的其它机器人实例自动配对。配对完成后合并场景组、统一消息通道号，并互相记录对方账号以屏蔽其消息。

### `bind channel probe`

<CommandUsage usage="bind channel probe <token>" :params="['token=一次性握手口令']" permission="public" />

内部命令，由 bind auto 自动发出，无需手动执行。握手响应入口。口令为一次性使用，一经认领即作废。

### `bind channel confirm`

<CommandUsage usage="bind channel confirm <token>" :params="['token=一次性握手口令']" permission="public" />

内部命令，由 bind auto 自动发出，无需手动执行。握手闭合入口。双方确认处于同一场景后，把两个场景合成同一条消息通道。

绑定码为 6 位大写字母与数字，有效期 300 秒，只保存在 Server 进程内存中，重启即失效。场景数据中的 `command_prefix`、`command_alias` 与场景 union 一起迁移，绑定后由合并结果统一维护。

## merge

隐藏模块，仅在 `retired_clients` 非空时加载。命令注册在 `bind` 上，模块本身只承载退役公告的正则触发器。

### `bind merge`

<CommandUsage usage="bind merge" permission="public" />

仅退役来源客户端注册。在旧客户端上生成迁移码。私聊中一并迁移发送者与私聊场景，群内执行要求场景管理员权限。

### `bind merge-token`

<CommandUsage usage="bind merge-token <code>" :params="['code=另一处生成的迁移码']" permission="public" />

仅目标客户端注册。在目标客户端兑换迁移码，合并用户与场景数据。迁移码与绑定码分开存放，互不消费。

迁移会改写模块表中以平台 ID 为主键的数据，并同步场景管理员、封禁列表与消息通道。`retired_clients` 的格式为 `<源客户端> -> <目标客户端>`，只写源客户端表示不提供迁移，此时不注册迁移命令，仅保留退役公告。

## petal

花瓣为跨平台积分，仅在 `enable_petal` 为真时加载。别名 `petals`、`sign` 分别指向 `petal` 与 `petal sign`。

### `petal`

<CommandUsage :usage="['petal', 'petal [<user>]']" :params="['user=带平台前缀的用户完整 ID']" permission="public" />

查询花瓣数量。省略用户时查询本人；指定用户的形式要求超级用户权限，用户尚无 union 时先确认再创建。

### `petal sign`

<CommandUsage usage="petal sign" permission="public" />

每日签到获得花瓣。场景可通过 `setup sign` 关闭签到，关闭时返回停用提示；当日已签到返回已领取提示。

### `petal give`

<CommandUsage usage="petal give <petal> <user>" :params="['petal=转账的花瓣数量', 'user=带平台前缀的用户完整 ID']" permission="public" />

向同一客户端的用户转账花瓣，执行前要求确认。目标须为带客户端前缀的完整 ID，不能是发送者本人；花瓣数量小于等于 0 时返回提示。

### `petal modify`

<CommandUsage usage="petal modify <petal> [<user>]" :params="['petal=增减的花瓣数量，负数表示扣除', 'user=带平台前缀的用户完整 ID']" permission="superuser" />

增减指定用户的花瓣，负数表示扣除。省略用户时修改本人；用户尚无 union 时先确认再创建。

### `petal clear`

<CommandUsage usage="petal clear [<user>]" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

把花瓣清零。省略用户时处理本人。

### `petal bud send`

<CommandUsage usage="petal bud send <petal> <count> <passcode>" :params="['petal=红包的花瓣总额', 'count=红包份数', 'passcode=领取口令']" permission="public" />

发放花瓣红包，执行前要求确认。`<petal>` 为总额，`<count>` 为份数，`<passcode>` 为领取口令；总额须不小于份数，口令重复时退回已扣除的花瓣。成功时返回红包 ID。

### `petal bud`

<CommandUsage usage="petal bud <passcode>" :params="['passcode=领取口令']" permission="public" />

用口令领取红包，返回领取结果与当前花瓣数。

### `petal bud info`

<CommandUsage usage="petal bud info <id>" :params="['id=红包 ID']" permission="public" />

查看红包的发送者、口令、总额、份数与领取记录。

### `petal bud release`

<CommandUsage usage="petal bud release" permission="superuser" />

退回所有未领取的红包。

配置项：`enable_get_petal`、`petal_gained_limit`、`petal_lost_limit`、`petal_sign_min`、`petal_sign_max`、`petal_sign_rate`、`petal_rebate_rate`、`petal_reset_crontab`。定时任务按 `petal_reset_crontab`（默认每月 1 日 `0 0 1 * *`）结算花瓣。转账与红包要求目标用户属于同一客户端，避免跨平台刷取。

## help

基础模块，输出模块清单与命令帮助。

### `help`

<CommandUsage :usage="['help [--legacy] [--img]', 'help <module> [--legacy] [--img]']" :params="['module=模块名或别名']" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

省略模块名时按当前场景可用的模块列出清单与启用状态，清单带锁定与订阅标记以及启用、停用入口，`hidden=True` 的模块不出现，平台不支持的模块以删除线标注。给出模块名时展示该模块的简介与命令模板，超级用户命令对非超级用户隐藏，管理员命令对普通成员隐藏。

`--img` 优先渲染图片，渲染不可用时回退文本；`--legacy` 强制文本表格。模块顺序与启用状态取自场景的 `modules` 列，基础模块始终显示为已启用；未启用的模块可通过清单按钮或 `module enable <module>` 打开。模块的帮助文案来自命令模板末尾的 `{{I18N:key}}`，简介来自 `module(desc=...)`。
