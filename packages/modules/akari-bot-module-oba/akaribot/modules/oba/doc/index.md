# oba

此模块可以查询 OpenBMCLAPI 的实时仪表盘、节点排行与赞助商信息，也可以按名称搜索节点。数据来自公共接口。

## 命令

### `oba status`

<CommandUsage usage="oba status" permission="public" />

此命令用于获取仪表盘数据，展示当前在线节点数、5 分钟负载百分比、总带宽、当前出网带宽、当日请求数、当日全网总流量。消息另外附带 OpenBMCLAPI 版本与查询时间，取不到版本号时省略版本一项。

<ChatExample
  :log="[
    '用户：~oba status',
    '机器人：当前在线节点：21 个',
    '5 分钟负载：65.86%',
    '总带宽：4091 Mbps',
    '当前出网带宽：2694.27 Mbps',
    '当日请求：80938008 次',
    '当日全网总流量：16.40 TB',
    'OpenBMCLAPI 最新版本: 1.15.0@3e45349',
    '查询时间：2026 年 11 月 12 日 22:50:00',
  ]"
/>

### `oba node`

<CommandUsage usage="oba node [<rank>]" :params="['rank=节点排名，从 1 开始']" permission="public" />

说明：

- 获取指定排名节点的状态。省略排名时取第 1 名。
- 用绿色与红色方块表示节点是否启用。
- 输出节点名称、ID、当日流量、当日请求数与查询时间。
- 节点带赞助商时，单独发送赞助商名称、网站与横幅图片。横幅发送失败时只发送文字部分。
- 排名小于 1 或超出排行榜范围时返回无效节点提示。

<ChatExample
  :log="[
    '用户：~oba node',
    '机器人：🟩节点名称：大機機',
    '节点 ID：`6aaa9a7e835f5088b109e630`',
    '当日流量：2.76 TB | 当日请求数：13552970',
    '查询时间：2026 年 11 月 12 日 22:50:00',
  ]"
/>

### `oba top`

<CommandUsage usage="oba top [<rank>]" :params="['rank=起始排名，从 1 开始']" permission="public" />

此命令从指定排名开始列出至多 10 个节点。省略排名时从第 1 名开始，排名小于 1 时按第 1 名处理。每个节点给出名次、节点名称、ID、当日流量、当日请求数与赞助商名称，末尾附折叠提示。

<ChatExample
  :log="[
    '用户：~oba top',
    '机器人：🟩 | 1 | 大機機 | `6aaa9a7e835f5088b109e630`',
    '2.76 TB | 13552970',
    '节点赞助商：未知',
    '🟩 | 2 | 小雞雞2 | `6aafa697344966d359faac8a`',
    '2.64 TB | 12966384',
    '节点赞助商：未知',
    '……仅显示前 10 条内容。',
  ]"
/>

### `oba search`

<CommandUsage usage="oba search <keyword>" :params="['keyword=节点或赞助商名称关键词']" permission="public" />

此命令按节点名称或赞助商名称搜索，对关键词做不区分大小写的正则匹配。展示格式与 `oba top` 一致，名次沿用完整排行榜中的位置。命中超过 10 条时只保留前 10 条并附折叠提示，没有命中时返回未找到提示。

<ChatExample
  :log="[
    '用户：~oba search 小雞雞',
    '机器人：🟩 | 2 | 小雞雞2 | `6aafa697344966d359faac8a`',
    '2.64 TB | 12966384',
    '节点赞助商：未知',
  ]"
/>

### `oba sponsor`

<CommandUsage usage="oba sponsor" permission="public" />

此命令用于获取随机节点赞助商，发送赞助商名称、网站与横幅图片。横幅发送失败时只发送文字部分。消息附有该赞助商与 Teahouse Studios 无从属关系的说明。

<ChatExample
  :log="[
    '用户：~oba sponsor',
    '机器人：节点赞助商：才……才不是笨蛋大笨蛋！',
    '赞助商网站：`https://up.sc.cn/link/S8PNWufk`',
    '注意：此处展示的 OpenBMCLAPI 节点赞助商与 Teahouse Studios 无任何从属关系。',
  ]"
/>
