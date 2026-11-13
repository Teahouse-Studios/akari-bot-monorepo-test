---
order: 61
---

# analytics

<ModuleAlias names="ana" />

模块级权限为超级用户。

### `analytics`

<CommandUsage usage="analytics" permission="superuser" />

输出命令总数、今日数量与首条记录时间。

<ChatExample
  :log="[
    '用户：~analytics',
    '机器人：机器人已执行命令次数（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：12486',
    '今日已执行命令次数：98',
  ]"
/>

### `analytics days`

<CommandUsage usage="analytics days [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

输出近 30 天的命令数折线图，可按模块过滤。

<ChatExample
  :log="[
    '用户：~analytics days',
    '机器人：最近 30 天的所有命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>

### `analytics year`

<CommandUsage usage="analytics year [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

输出近 12 个月的命令数折线图，可按模块过滤。

<ChatExample
  :log="[
    '用户：~analytics year petal',
    '机器人：最近一年的“petal”命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>

### `analytics modules`

<CommandUsage usage="analytics modules [<rank>]" :params="['rank=列出的模块数，缺省为 30']" permission="superuser" />

输出模块命令调用排行，横向条形图，`<rank>` 缺省为 30。

<ChatExample
  :log="[
    '用户：~analytics modules 5',
    '机器人：（横向条形图：模块命令调用次数排行，取前 5 个模块）',
  ]"
/>

统计关闭时提示已停用；缺少 `matplotlib` 时提示安装 `image` extra，不生成图表。数据写入由 `telemetry` 完成，见[telemetry](telemetry.md)。
