---
title: 命令
order: 10
description: 舞萌 DX 模块的全部命令、选项、权限与数据源。
---

# 命令

`maimai` 模块（别名 `mai`）提供舞萌 DX 的曲目、谱面与成绩查询。下文以 `maimai` 表示命令前缀，实际前缀由实例配置决定。除特别标注外，命令对普通用户开放。

曲目类命令读取实例本地的曲目库、别名库与包内资料，不要求登录；成绩类命令按玩家当前选择的数据源访问水鱼或落雪，并需要相应账号的绑定。本地曲目库来自水鱼，别名库来自 yuzuchan，段位资料随包分发。难度参数接受全称、三字母缩写与中文（绿、黄、红、紫、白），大小写不敏感。

## 查询

| 命令 | 选项 | 说明 | 数据源 |
| --- | --- | --- | --- |
| `maimai base <constant> [<constant_max>] [-p <page>]` | `-p <page>` | 按定数或定数范围搜索谱面 | 本地曲目库 |
| `maimai level <level> [-p <page>]` | `-p <page>` | 按等级搜索谱面 | 本地曲目库 |
| `maimai new [-p <page>]` | `-p <page>` | 查看当前版本新曲 | 本地曲目库 |
| `maimai search <keyword> [-p <page>]` | `-p <page>` | 按歌名（可只给一部分）搜索 | 本地曲目库 |
| `maimai id <id>` | 无 | 按 ID 查询歌曲 | 本地曲目库、曲绘 |
| `maimai song <id_or_alias>` | 无 | 按 ID 或别名查询歌曲 | 本地曲目库、别名库、曲绘 |
| `maimai chart <id_or_alias>` | 无 | 按 ID 或别名查询各难度谱面 | 本地曲目库、别名库、曲绘 |
| `maimai alias <sid>` | 无 | 查询歌曲别名（`sid` 为歌曲 ID） | 本地别名库 |
| `maimai random` | 无 | 完全随机一首歌曲 | 本地曲目库 |
| `maimai random <diff+level> [<dx_type>]` | 无 | 按难度、等级与类型随机，`*` 表示不限难度与等级 | 本地曲目库 |
| `maimai scoreline <id_or_alias> <diff>` | 无 | 查询谱面分数线与 BREAK 换算 | 本地曲目库、别名库 |
| `maimai calc <base> <score>` | 无 | 按定数与达成率计算单曲 Rating | 本地计算 |
| `maimai grade <grade>` | 无 | 查询段位认定列表 | 包内段位资料 |

`id`、`song`、`chart`、`scoreline` 与 `score` 的 ID 可加 `id` 前缀（如 `id834`）；不加前缀时按歌名或别名解析，命中多首会列出候选。`search` 只匹配歌名，不查询别名。`random` 的 `<dx_type>` 取 `dx`、`sd`、`标准` 或 `標準`，缺省不筛选类型；`<diff+level>` 中的难度与等级不分隔，例如 `紫14+`、`14+`。`grade` 支持普通段位、真段位与 EXPERT／MASTER 各级，例如 `十段`、`真初段`、`MASTER超上级`。

<CommandUsage usage="maimai score <id_or_alias>" permission="public" type="command" :aliases="['mai']" note="查询绑定账号在该曲目各难度的成绩；需要绑定当前数据源的账号。" />

## 成绩与绑定

| 命令 | 选项 | 说明 | 数据源 |
| --- | --- | --- | --- |
| `maimai b50 [<user>]` | 无 | 查询玩家 B50 图片 | 所选数据源 |
| `maimai score <id_or_alias>` | 无 | 查询绑定账号的单曲成绩 | 所选数据源 |
| `maimai plate <plate> [-l]` | `-l` | 查看名牌板完成进度；`-l` 输出完成表 | 所选数据源 |
| `maimai process <level> <goal> [-l]` | `-l` | 查看指定等级的目标评价进度；`-l` 输出完成表 | 所选数据源 |
| `maimai scorelist <level> [-p <page>]` | `-p <page>` | 查看指定等级的分数列表 | 所选数据源 |
| `maimai rank` | 无 | 查看水鱼分数排行 | 水鱼（仅此数据源） |
| `maimai bind df` | 无 | 绑定水鱼账号 | 水鱼 OAuth |
| `maimai unbind df` | 无 | 解绑水鱼账号 | 水鱼 OAuth |
| `maimai bind lx [<auth_code>]` | 无 | 绑定落雪账号；不带参数时返回授权链接 | 落雪 OAuth |
| `maimai unbind lx` | 无 | 解绑落雪账号 | 落雪 OAuth |

`b50` 与 `score`、`plate`、`process`、`scorelist` 使用玩家当前选择的数据源。`b50` 不填玩家时查询绑定账号：水鱼在 QQ 平台未绑定时可按 QQ 号查询，其余平台需要 `bind df`；落雪按好友码查询他人，未填写时使用绑定账号。`score`、`plate`、`process`、`scorelist` 只查询绑定账号，不接受玩家参数；水鱼侧需要已配置 OAuth 应用并完成授权。`process` 的等级取 `1` 至 `15+`，目标取 `A` 至 `SSS+`、`FC`、`FC+`、`AP`、`AP+`、`SYNC`、`FS`、`FS+`、`FDX`、`FDX+`。`rank` 只在数据源为水鱼时可用，切换到落雪后会提示切回。

<CommandUsage usage="maimai b50 [<user>]" permission="public" type="command" :aliases="['mai']" note="水鱼填查分器用户名，落雪填好友码；留空查询绑定账号。落雪按好友码查询他人需要开发者令牌。" />

<CommandUsage usage="maimai plate <plate> [-l]" permission="public" type="command" :aliases="['mai']" :options="[{flag:'-l', desc:'输出完成表图片'}]" note="名牌板名按游戏内名称填写，例如「舞神」；成绩取自绑定账号。" />

`bind df` 使用设备码流程，发送授权链接后等待用户在浏览器完成授权。`bind lx` 使用授权码流程：首次发送命令返回授权链接，完成授权后把授权码或回调地址作为 `<auth_code>` 再次发送。`unbind` 删除本地绑定记录，水鱼解绑同时撤销授权。两个游戏共用同一份绑定记录。

## 设置与维护

| 命令 | 选项 | 说明 | 权限 |
| --- | --- | --- | --- |
| `maimai switch` | 无 | 切换当前用户的数据源，目标数据源需已绑定 | 超级用户 |
| `maimai update [--no-cover]` | `--no-cover` | 更新曲目库、别名与封面 | 超级用户 |

`switch` 与 `update` 使用 `required_superuser`，其余命令使用默认的公开权限。`switch` 在水鱼与落雪之间切换，未绑定目标数据源时会返回对应的绑定命令。`update` 从水鱼下载曲目库与封面、从 yuzuchan 更新别名；`--no-cover` 跳过封面下载。每日 0 点的定时任务只更新别名。

<CommandUsage usage="maimai update [--no-cover]" permission="superuser" type="command" :aliases="['mai']" :options="[{flag:'--no-cover', desc:'跳过封面下载'}]" note="曲目库、别名与封面写入实例数据目录。" />
