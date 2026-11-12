# maimai

查询舞萌 DX 与 CHUNITHM 的曲目资料、谱面成绩、B50/B30、名牌板、段位与评级进度，并支持绑定水鱼查分器与落雪咖啡屋账号。

<ModuleAlias names="mai" />

除特别标注外，命令对普通用户开放。曲目类命令不要求登录；成绩类命令按玩家当前选择的数据源访问水鱼或落雪，并需要相应账号的绑定。难度参数接受全称、三字母缩写与中文（绿、黄、红、紫、白），大小写不敏感。

## 查询

### `maimai base`

<CommandUsage usage="maimai base <constant> [<constant_max>] [-p <page>]" :params="['constant=定数下限', 'constant_max=定数上限，省略时只查单一定数', 'page=页码，缺省为 1']" permission="public" :options="[{flag: '-p', desc: '指定页数，默认为 1。'}]" />

按定数或定数范围搜索谱面。`<constant>` 为定数下限，`<constant_max>` 可省略；定数须大于 0，范围写反时以较小值为下限并提示实际区间。结果超过一页时输出图片。

### `maimai level`

<CommandUsage usage="maimai level <level> [-p <page>]" :params="['level=等级，如 13+ 或 15', 'page=页码，缺省为 1']" permission="public" :options="[{flag: '-p', desc: '指定页数，默认为 1。'}]" />

按等级搜索谱面。`<level>` 取 `1` 至 `15`，加号等级只有 `7+` 至 `14+`。结果超过一页时输出图片。

### `maimai new`

<CommandUsage usage="maimai new [-p <page>]" :params="['page=页码，缺省为 1']" permission="public" :options="[{flag: '-p', desc: '指定页数，默认为 1。'}]" />

查看当前版本的新曲。结果超过一页时输出图片。

### `maimai search`

<CommandUsage usage="maimai search <keyword> [-p <page>]" :params="['keyword=歌名或其中的一部分', 'page=页码，缺省为 1']" permission="public" :options="[{flag: '-p', desc: '指定页数，默认为 1。'}]" />

按歌名搜索，`<keyword>` 可只给歌名的一部分；只匹配歌名，不查询别名。结果超过一页时输出图片，`-p` 指定页数，缺省为 1。

### `maimai id`

<CommandUsage usage="maimai id <id>" :params="['id=歌曲 ID，可加 id 前缀']" permission="public" />

按 ID 查询歌曲信息与各难度谱面。`<id>` 可直接写数字，也可加 `id` 前缀；ID 大于 100000 的宴谱读取宴会场数据，输出会场信息与物量。

### `maimai song`

<CommandUsage usage="maimai song <id_or_alias>" :params="['id_or_alias=歌曲 ID 或歌名、别名']" permission="public" />

按 ID 或别名查询歌曲信息与各难度谱面。`<id_or_alias>` 加 `id` 前缀时按 ID 直查，否则按歌名或别名解析；命中多首时列出候选并要求用完整命令重发。

### `maimai chart`

<CommandUsage usage="maimai chart <id_or_alias>" :params="['id_or_alias=歌曲 ID 或歌名、别名']" permission="public" />

查询各难度谱面的物量、定数与谱师，`<id_or_alias>` 的解析方式同 `maimai song`。宴谱输出宴会场信息与左右谱面物量。命中多首时列出候选并要求用完整命令重发。

### `maimai alias`

<CommandUsage usage="maimai alias <sid>" :params="['sid=歌曲 ID，可加 id 前缀']" permission="public" />

查询歌曲的别名。`<sid>` 为歌曲 ID，可加 `id` 前缀；别名达到 20 条时以图片输出。

### `maimai random`

<CommandUsage usage="maimai random" permission="public" />

从全部曲目中随机一首，返回歌曲信息与各难度定数。

### `maimai random <diff+level>`

<CommandUsage usage="maimai random <diff+level> [<dx_type>]" :params="['diff+level=难度与等级组合，如紫14+，* 为不限', 'dx_type=谱面类型 dx 或 sd，也可写中文']" permission="public" />

按难度、等级与类型随机。`<diff+level>` 不分隔书写，例如 `紫14+`、`14+`，写 `*` 表示不限难度与等级；`<dx_type>` 取 `dx`、`sd`、`标准` 或 `標準`，缺省不筛选类型。条件无法解析或无匹配曲目时返回失败提示。

### `maimai scoreline`

<CommandUsage usage="maimai scoreline <id_or_alias> <diff>" :params="['id_or_alias=歌曲 ID 或歌名、别名', 'diff=谱面难度全称、缩写或中文']" permission="public" />

查询谱面分数线，输出 101% 的目标分表与单个 BREAK 2550、2000 的换算。`<diff>` 接受难度全称、三字母缩写与中文；谱面不存在时返回未找到提示。

### `maimai calc`

<CommandUsage usage="maimai calc <base> <score>" :params="['base=谱面定数', 'score=达成率，如 100.5']" permission="public" />

按谱面定数与达成率计算单曲 Rating。`<base>` 为定数，`<score>` 为达成率。

### `maimai grade`

<CommandUsage usage="maimai grade <grade>" :params="['grade=段位名称，如十段、真初段']" permission="public" />

查询段位认定列表。`<grade>` 支持普通段位、真段位与 EXPERT／MASTER 各级，例如 `十段`、`真初段`、`MASTER超上级`。

## 成绩与绑定

### `maimai b50`

<CommandUsage usage="maimai b50 [<user>]" :params="['user=水鱼用户名或落雪好友码']" permission="public" />

查询玩家的 B50 列表并生成图片。数据源为水鱼时 `<user>` 为查分器用户名，留空查询绑定账号，QQ 平台未绑定时按 QQ 号查询；数据源为落雪时 `<user>` 为好友码，留空使用绑定账号的令牌。

### `maimai score`

<CommandUsage usage="maimai score <id_or_alias>" :params="['id_or_alias=歌曲 ID 或歌名、别名']" permission="public" />

查询绑定账号在该曲目各难度的成绩，`<id_or_alias>` 的解析方式同 `maimai song`。

### `maimai plate`

<CommandUsage usage="maimai plate <plate> [-l]" :params="['plate=名牌板名称，如舞神']" permission="public" :options="[{flag: '-l', desc: '输出完成表图片。'}]" />

查看绑定账号的名牌板完成进度。`<plate>` 按游戏内名牌板名称填写，例如“舞神”；`-l` 输出完成表图片。真将与除“霸者”“覇者”以外的“者”类名牌板不可查询。

### `maimai process`

<CommandUsage usage="maimai process <level> <goal> [-l]" :params="['level=等级，如 13+ 或 15', 'goal=目标评价，如 AP 或 FDX+']" permission="public" :options="[{flag: '-l', desc: '输出完成表图片。'}]" />

查看玩家在指定等级的目标评价完成进度。`<level>` 取 `1` 至 `15`，加号等级只有 `7+` 至 `14+`；`<goal>` 取 `A` 至 `SSS+`、`FC`、`FC+`、`AP`、`AP+`、`SYNC`、`FS`、`FS+`、`FDX`、`FDX+`；`-l` 输出完成表图片。

### `maimai scorelist`

<CommandUsage usage="maimai scorelist <level> [-p <page>]" :params="['level=等级，如 13+ 或 15', 'page=页码，缺省为 1']" permission="public" :options="[{flag: '-p', desc: '指定页数。'}]" />

查看绑定账号在指定等级的分数列表。`-p` 非数字时按第 1 页处理。

### `maimai rank`

<CommandUsage usage="maimai rank" permission="public" />

查看水鱼的全服分数排行。数据源为落雪时返回提示，并给出切回水鱼的命令。

### `maimai bind df`

<CommandUsage usage="maimai bind df" permission="public" />

绑定 Diving-Fish（水鱼）查分器账号，使用设备码流程：发送授权链接后等待在浏览器完成授权。水鱼与落雪共用同一份绑定记录。

### `maimai unbind df`

<CommandUsage usage="maimai unbind df" permission="public" />

解除水鱼账号绑定，同时撤销授权。

### `maimai bind lx`

<CommandUsage usage="maimai bind lx [<auth_code>]" :params="['auth_code=落雪授权码或回调地址']" permission="public" />

绑定落雪咖啡屋查分器账号，使用授权码流程：不带参数时返回授权链接，完成授权后把授权码或回调地址作为 `<auth_code>` 再次发送。

### `maimai unbind lx`

<CommandUsage usage="maimai unbind lx" permission="public" />

解除落雪账号绑定。

## 设置与维护

### `maimai switch`

<CommandUsage usage="maimai switch" permission="superuser" />

切换当前用户的数据源，在水鱼与落雪之间二选一。目标数据源未绑定时返回对应的绑定命令。

### `maimai update`

<CommandUsage usage="maimai update [--no-cover]" permission="superuser" :options="[{flag: '--no-cover', desc: '跳过曲绘下载。'}]" />

更新曲目库与别名库，缺省同时下载曲绘；`--no-cover` 跳过曲绘。失败时返回更新失败提示。每日 0 点的定时任务只更新别名。

## 正则句式

以“是什么歌”结尾的句子会自动识别并查询：`<ID 或别名>是什么歌` 按 ID 或别名查询歌曲信息，ID 需加 `id` 前缀；同类句式还有“有什么别名”“有什么分”“段位表”“进度”与“完成表”。完整句式见 [正则句式](regex.md)。

## CHUNITHM

CHUNITHM 的命令、数据源与相对舞萌 DX 的差异见 [CHUNITHM](chunithm.md)。
