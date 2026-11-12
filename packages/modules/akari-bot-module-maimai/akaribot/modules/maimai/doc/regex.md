---
title: 正则句式
order: 20
description: 自然语言句式的触发方式、查询内容与账号要求。
---

# 正则句式

直接匹配聊天消息中的自然语言句式，没有命令前缀。

句式中的常用字同时接受简体与繁体写法，例如“什么／什麼”“进度／進度”。所有句式对普通用户开放。

<ModuleAlias names="mai_regex, maimai_regex" />

<NoticeBox type="info">

曲目信息、别名、随机歌曲与段位资料不要求账号。成绩、进度与名牌板句式会读取玩家当前选择的数据源，必须先绑定水鱼（`maimai bind df`）或落雪（`maimai bind lx`）账号。

</NoticeBox>

## 曲目与别名

### `<ID或别名>是什么歌`

<CommandUsage usage="<ID或别名>是什么歌" :params="['ID或别名=歌曲数字 ID 或别名，可带 id 前缀']" permission="public" type="regex" />

查询歌曲的艺术家、分类、BPM、版本与难度。名称以 `id` 开头时按 ID 解析，其余按歌名或别名解析；命中多个别名时返回候选 ID 列表。不需要绑定账号，结果与 `maimai song` 一致。示例：`834是什么歌`、`id834是什么歌`、`PANDORA PARADOXXX是什么歌`。

### `<ID>有什么别名`

<CommandUsage usage="<ID>有什么别名" :params="['ID=歌曲数字 ID，可带 id 前缀']" permission="public" type="regex" />

查询歌曲的别名列表，ID 可带 `id` 前缀，但必须是数字。别名库由 `maimai update` 更新；尚未更新时会提示先执行更新。示例：`834有什么别名`、`id834有什麼別名`。

## 成绩与进度

### `<ID或别名>有什么分`

<CommandUsage usage="<ID或别名>有什么分" :params="['ID或别名=歌曲数字 ID 或别名，可带 id 前缀']" permission="public" type="regex" />

查询绑定账号在该曲目各难度的成绩，包括达成率、评级、连击与同步标记。ID 可带 `id` 前缀；别名命中多首时返回候选列表。查询对象固定为绑定账号，不能指定其他玩家；未绑定时返回对应的绑定命令。成绩按玩家当前选择的数据源读取。

### `<等级> <目标>进度`

<CommandUsage usage="<等级> <目标>进度" :params="['等级=等级，如 14+', '目标=评价目标，如 SSS+']" permission="public" type="regex" />

查看绑定账号在指定等级的目标评价进度，输出文字摘要。等级取 `1` 至 `15`，目标取 `A`、`AA`、`AAA`、`S`、`S+`、`SS`、`SS+`、`SSS`、`SSS+`、`FC`、`FC+`、`AP`、`AP+`、`SYNC`、`FS`、`FS+`、`FDX`、`FDX+`。示例：`14+ SSS+进度`。

### `<等级> <目标>完成表`

<CommandUsage usage="<等级> <目标>完成表" :params="['等级=等级，如 14+', '目标=评价目标，如 SSS+']" permission="public" type="regex" />

与 `进度` 句式相同，额外生成图片。示例：`14+ SSS+完成表`。

### `<名牌板>进度`

<CommandUsage usage="<名牌板>进度" :params="['名牌板=游戏内名牌板名称']" permission="public" type="regex" />

查看绑定账号的名牌板完成情况，输出文字摘要。名牌板名按游戏内名称填写。示例：`舞神进度`。

### `<名牌板>完成表`

<CommandUsage usage="<名牌板>完成表" :params="['名牌板=游戏内名牌板名称']" permission="public" type="regex" />

与名牌板 `进度` 句式相同，输出图片形式的完成列表。示例：`霸者完成表`。

## 随机与段位

### `随个[dx|标准][颜色]<等级>`

<CommandUsage usage="随个[dx|标准][颜色]<等级>" :params="['等级=等级，如 14+']" permission="public" type="regex" />

按条件随机一首歌曲。类型可写 `dx`、`sd`、`标准` 或 `標準`，省略时不筛选类型；颜色可写绿、黄、红、紫、白，省略时不筛选难度；等级必须给出，类型与颜色均可省略。示例：`随个14+`、`随个dx紫14+`、`随个标准13`。该句式不使用 `maimai random` 的 `*` 无条件写法。

### `<段位>段位[认定][列]表`

<CommandUsage usage="<段位>段位[认定][列]表" :params="['段位=段位名称，如十段']" permission="public" type="regex" />

查询段位认定的曲目与通关条件，段位资料随包分发，不访问查分器。段位支持普通段位、真段位以及 EXPERT／MASTER 各级，须使用资料中的名称。示例：`十段段位表`、`真初段段位认定表`、`MASTER超上级段位列表`。

## 匹配说明

- 正则从消息开头匹配。歌名、名牌板或段位前后不要附加其他说明，例如“请问 834 是什么歌”会把“请问 834”当作歌名。
- `有什么别名` 的 ID 必须是数字，不能使用歌名或别名。
- 成绩、进度与名牌板句式只查询绑定账号，未绑定时返回对应的绑定命令；B50 不在正则范围内，使用 `maimai b50`。
- 歌名与别名匹配不区分大小写。

<NoticeBox type="warning">

正则句式没有命令前缀，任何匹配到的消息都会触发查询。若平台不允许读取全部消息，或不需要自然语言触发，只使用命令形式即可。

</NoticeBox>
