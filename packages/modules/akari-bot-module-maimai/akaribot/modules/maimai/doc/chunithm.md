---
title: CHUNITHM
order: 30
description: CHUNITHM 的命令、数据源与相对舞萌 DX 的差异。
---

# CHUNITHM

提供 CHUNITHM 的曲目、谱面与 B30 查询。

<ModuleAlias names="chu" />

除 `update` 外，命令对普通用户开放。

<NoticeBox type="info">

CHUNITHM 的曲目资料来自落雪咖啡屋的曲目表，封面从落雪下载。成绩数据按玩家选择的数据源读取：默认落雪，实例未配置落雪 OAuth 时回落到水鱼。成绩绑定与水鱼、落雪账号共用，舞萌绑定的账号同样可用于 CHUNITHM。

</NoticeBox>

## 查询

### `chunithm base`

<CommandUsage usage="chunithm base <constant> [<constant_max>] [-p <page>]" :params="['constant=定数下限', 'constant_max=定数上限', 'page=页码']" permission="public" :options="[{flag: '-p <page>', desc: '指定页数，默认为 1。'}]" />

按定数搜索谱面，给出 `constant_max` 时按定数范围搜索，两端顺序相反时自动交换。定数不大于 0 时返回无效等级提示。结果按歌曲 ID 排序，逐条列出 ID、歌名、难度、等级与定数；结果超出一页时渲染为图片，渲染失败时发送文本并附页码提示。

<ChatExample
  :log="[
    '用户：~chunithm base 14.8',
    '机器人：以下为定数 14.8 的曲目列表：',
    '118 - 腐れ外道とチョコレゐト Ultima 14+ (14.8)',
  ]"
/>

### `chunithm level`

<CommandUsage usage="chunithm level <level> [-p <page>]" :params="['level=等级，如 14+', 'page=页码']" permission="public" :options="[{flag: '-p <page>', desc: '指定页数，默认为 1。'}]" />

按等级搜索谱面，等级写作 `14+` 一类形式。无匹配曲目时返回未找到提示，分页与输出格式同 `chunithm base`。

<ChatExample
  :log="[
    '用户：~chunithm level 14+',
    '机器人：以下为 14+ 级的曲目列表：',
    '7 - 初音ミクの消失 Master 14+ (14.5)',
  ]"
/>

### `chunithm search`

<CommandUsage usage="chunithm search <keyword> [-p <page>]" :params="['keyword=歌名或其一部分', 'page=页码']" permission="public" :options="[{flag: '-p <page>', desc: '指定页数，默认为 1。'}]" />

按歌名搜索，关键词可为歌名的一部分，只匹配歌名、不查询别名库。无匹配曲目时返回未找到提示，分页与输出格式同 `chunithm base`。

<ChatExample
  :log="[
    '用户：~chunithm search Grievous',
    '机器人：“Grievous”的搜索结果：',
    '751 - Grievous Lady',
  ]"
/>

### `chunithm chart`

<CommandUsage usage="chunithm chart <song>" :params="['song=歌曲 ID 或完整歌名']" permission="public" />

查询各难度谱面，逐难度给出等级、定数、TAP／HOLD／SLIDE／AIR／FLICK 物量与谱师，并附曲绘。参数为纯数字或带 `id` 前缀时按 ID 解析，否则按完整歌名匹配，不查询别名库，例如 `chunithm chart id1086`。只有一档难度的 WORLD'S END 谱面以星级展示定数。

<ChatExample
  :log="[
    '用户：~chunithm chart 751',
    '机器人：751 - Grievous Lady',
    'Basic 4 (4.0)',
    'TAP：205/HOLD：144/SLIDE：168/AIR：52/FLICK：0',
  ]"
/>

### `chunithm id`

<CommandUsage usage="chunithm id <id>" :params="['id=歌曲 ID']" permission="public" />

按 ID 查询歌曲，输出艺术家、分类、BPM、版本与各难度定数，并附曲绘。歌曲不存在时返回未找到提示。

<ChatExample
  :log="[
    '用户：~chunithm id 751',
    '机器人：751 - Grievous Lady',
    '艺术家：Team Grimoire vs Laur「Arcaea」',
    '难度：4.0/9.0/12.4/14.8',
  ]"
/>

### `chunithm song`

<CommandUsage usage="chunithm song <song>" :params="['song=歌曲 ID 或完整歌名']" permission="public" />

按 ID 或完整歌名查询歌曲，与 `chunithm id` 共用同一处理器，输出格式一致，例如 `chunithm song 1086`。纯数字或 `id` 前缀按 ID 解析，其余按完整歌名匹配。

<ChatExample
  :log="[
    '用户：~chunithm song 7',
    '机器人：7 - 初音ミクの消失',
    '艺术家：cosMo＠暴走P',
    '分类：niconico',
  ]"
/>

### `chunithm random`

<CommandUsage usage="chunithm random [<diff+level>]" :params="['diff+level=难度与等级连写，如 紫14+']" permission="public" />

不填参数时从全部曲目随机，填写时按难度与等级筛选。`<diff+level>` 把二者连写，例如 `紫14+`、`14+`；难度接受全称、三字母缩写与中文（绿、黄、红、紫、黑），大小写不敏感，CHUNITHM 的难度包含 Ultima。只给难度而不给等级或无法解析时返回随机失败提示，无匹配曲目时返回未找到提示；不支持 DX／标准类型筛选与 `*` 无条件写法。

<ChatExample
  :log="[
    '用户：~chunithm random 紫14+',
    '机器人：33 - Blue Noise',
    '2/7/10.1/14.5',
  ]"
/>

## B30 与账号

### `chunithm b30`

<CommandUsage usage="chunithm b30 [<user>]" :params="['user=水鱼用户名或落雪好友码']" permission="public" />

留空时查询绑定账号。查询玩家 B30（含 N20）图片，成绩取自玩家当前选择的数据源。水鱼填查分器用户名，查询他人无需绑定；落雪填好友码，按好友码查询他人需要实例已配置落雪开发者令牌，未配置时只能查询绑定账号，好友码非数字时返回提示。

### `chunithm bind df`

<CommandUsage usage="chunithm bind df" permission="public" />

绑定水鱼查分器账号。命令以设备码流程返回授权链接，授权完成后即完成绑定；实例未配置水鱼授权时返回未配置提示。

### `chunithm unbind df`

<CommandUsage usage="chunithm unbind df" permission="public" />

解除水鱼账号绑定，同时撤销授权。

### `chunithm bind lx`

<CommandUsage usage="chunithm bind lx [<auth_code>]" :params="['auth_code=落雪授权码或回调地址']" permission="public" />

绑定落雪咖啡屋账号。不带参数时返回授权链接，并提示用本命令回传授权码；带授权码或含授权码的回调地址时直接完成绑定，授权码无效时返回提示。

### `chunithm unbind lx`

<CommandUsage usage="chunithm unbind lx" permission="public" />

解除落雪账号绑定。

### `chunithm switch`

<CommandUsage usage="chunithm switch" permission="public" />

在水鱼与落雪之间切换当前用户的 CHUNITHM 数据源。目标数据源未绑定时不切换，并返回对应的绑定命令。

### `chunithm update`

<CommandUsage usage="chunithm update [--no-cover]" permission="superuser" :options="[{flag: '--no-cover', desc: '跳过封面下载。'}]" />

从落雪重新拉取曲目表与封面。`--no-cover` 跳过封面下载，只更新曲目表；更新失败时返回失败提示。

<ChatExample
  :log="[
    '用户：~chunithm update',
    '机器人：成功。',
  ]"
/>

## 与舞萌 DX 的差异

| 方面 | CHUNITHM | 舞萌 DX |
| --- | --- | --- |
| 默认数据源 | 落雪；未配置落雪 OAuth 时回落水鱼 | 水鱼 |
| 成绩图片 | B30，附 N20 | B50 |
| 曲目资料 | 落雪曲目表 | 水鱼曲目库 |
| 别名 | 无别名命令，`chart`／`song` 按完整歌名匹配 | 支持别名查询与别名库 |
| 数据源切换权限 | 普通用户 | 超级用户 |
| 更新内容 | 曲目表与封面 | 曲目库、别名与封面 |

CHUNITHM 没有 `new`、`alias`、`grade`、`scoreline`、`calc`、`plate`、`process`、`rank`、`scorelist`、`score` 与 `b50` 命令，这些命令只在舞萌 DX 侧提供。曲目资料来自落雪而非水鱼，因此舞萌的曲目更新不会改变 CHUNITHM 的曲目表。
