---
order: 42
---

# petal

花瓣为跨平台积分，仅在 `enable_petal` 为真时加载。别名 `petals`、`sign` 分别指向 `petal` 与 `petal sign`。

### `petal`

<CommandUsage :usage="['petal', 'petal [<user>]']" :params="['user=带平台前缀的用户完整 ID']" permission="public" />

查询花瓣数量。省略用户时查询本人；指定用户的形式要求超级用户权限，用户尚无 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~petal',
    '机器人：当前花瓣数为 42。',
  ]"
/>

### `petal sign`

<CommandUsage usage="petal sign" permission="public" />

每日签到获得花瓣。场景可通过 `setup sign` 关闭签到，关闭时返回停用提示；当日已签到返回已领取提示。

<ChatExample
  :log="[
    '用户：~petal sign',
    '机器人：签到成功！',
    '获得了 7 片花瓣。',
  ]"
/>

### `petal give`

<CommandUsage usage="petal give <petal> <user>" :params="['petal=转账的花瓣数量', 'user=带平台前缀的用户完整 ID']" permission="public" />

向同一客户端的用户转账花瓣，执行前要求确认。目标须为带客户端前缀的完整 ID，不能是发送者本人；花瓣数量小于等于 0 时返回提示。

<ChatExample
  :log="[
    '用户：~petal give 5 QQ|Group|987654321',
    '机器人：此操作将会将 5 花瓣给予用户 QQ|Group|987654321 ，是否继续？',
    '用户：是',
    '机器人：已将 5 花瓣给予用户 QQ|Group|987654321 ，当前花瓣数为：42。',
  ]"
/>

### `petal modify`

<CommandUsage usage="petal modify <petal> [<user>]" :params="['petal=增减的花瓣数量，负数表示扣除', 'user=带平台前缀的用户完整 ID']" permission="superuser" />

增减指定用户的花瓣，负数表示扣除。省略用户时修改本人；用户尚无 union 时先确认再创建。

<ChatExample
  :log="[
    '用户：~petal modify -10',
    '机器人：已修改 -10 花瓣，当前花瓣数为：32。',
  ]"
/>

### `petal clear`

<CommandUsage usage="petal clear [<user>]" :params="['user=带平台前缀的用户完整 ID']" permission="superuser" />

把花瓣清零。省略用户时处理本人。

<ChatExample
  :log="[
    '用户：~petal clear',
    '机器人：已清除所有花瓣。',
  ]"
/>

### `petal bud send`

<CommandUsage usage="petal bud send <petal> <count> <passcode>" :params="['petal=红包的花瓣总额', 'count=红包份数', 'passcode=领取口令']" permission="public" />

发放花瓣红包，执行前要求确认。`<petal>` 为总额，`<count>` 为份数，`<passcode>` 为领取口令；总额须不小于份数，口令重复时退回已扣除的花瓣。成功时返回红包 ID。

<ChatExample
  :log="[
    '用户：~petal bud send 30 3 布丁',
    '机器人：此操作将花费 30 片花瓣，发出可领取 3 次的花苞（口令：布丁）。是否继续？',
    '用户：是',
    '机器人：花苞已发送！共 30 片花瓣，可领取 3 次。',
  ]"
/>

### `petal bud`

<CommandUsage usage="petal bud <passcode>" :params="['passcode=领取口令']" permission="public" />

用口令领取红包，返回领取结果与获得的花瓣数。

<ChatExample
  :log="[
    '用户：~petal bud 布丁',
    '机器人：领取成功！',
    '获得了 10 片花瓣。',
  ]"
/>

### `petal bud info`

<CommandUsage usage="petal bud info <id>" :params="['id=红包 ID']" permission="public" />

查看红包的发送者、口令、总额、份数与领取记录。

<ChatExample
  :log="[
    '用户：~petal bud info K7QX2M9F',
    '机器人：发送者：QQ|Group|123456789',
    '口令：布丁',
    '总量：30 片｜已领取：2/3 次',
  ]"
/>

### `petal bud release`

<CommandUsage usage="petal bud release" permission="superuser" />

强制释放所有过期花苞，返回释放数量；没有可释放的花苞时返回提示。

<ChatExample
  :log="[
    '用户：~petal bud release',
    '机器人：已释放 2 个过期花苞。',
  ]"
/>

配置项：`enable_get_petal`、`petal_gained_limit`、`petal_lost_limit`、`petal_sign_min`、`petal_sign_max`、`petal_sign_rate`、`petal_rebate_rate`、`petal_reset_crontab`。定时任务按 `petal_reset_crontab`（默认每月 1 日 `0 0 1 * *`）结算花瓣。转账与红包要求目标用户属于同一客户端，避免跨平台刷取。
