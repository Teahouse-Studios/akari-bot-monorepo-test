---
order: 61
---

# analytics

<ModuleAlias names="ana" />

此模块用于统计命令的调用次数与分布。模块级权限为超级用户。

### `analytics`

<CommandUsage usage="analytics" permission="superuser" />

此命令输出命令总数、今日命令数与首条记录的时间。

<ChatExample
  :log="[
    '用户：~analytics',
    '机器人：机器人已执行命令次数（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：12486',
    '今日已执行命令次数：98',
  ]"
/>

### `analytics days`

<CommandUsage usage="analytics days [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

此命令输出近 30 天的命令数折线图，可按模块过滤。

<ChatExample
  :log="[
    '用户：~analytics days',
    '机器人：最近 30 天的所有命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>

### `analytics year`

<CommandUsage usage="analytics year [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

此命令输出近 12 个月的命令数折线图，可按模块过滤。

<ChatExample
  :log="[
    '用户：~analytics year petal',
    '机器人：最近一年的“petal”命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>

### `analytics modules`

<CommandUsage usage="analytics modules [<rank>]" :params="['rank=列出的模块数，默认为 30']" permission="superuser" />

此命令以横向条形图输出模块命令调用排行。`<rank>` 默认为 30。

<ChatExample
  :log="[
    '用户：~analytics modules 5',
    '机器人：（横向条形图：模块命令调用次数排行，取前 5 个模块）',
  ]"
/>

统计功能关闭时，机器人提示该功能已停用。缺少 `matplotlib` 时，机器人提示安装 `image` extra，不生成图表。统计数据由 `telemetry` 写入，见[telemetry](telemetry.md)。
