# oba

查询 OpenBMCLAPI 的实时仪表盘、节点排行、节点搜索与赞助商信息，数据来自公共接口。

## 命令

### `oba status`

<CommandUsage usage="oba status" permission="public" />

获取仪表盘数据。展示当前在线节点数、5 分钟负载百分比、总带宽、当前出网带宽、当日请求数、当日全网总流量，并附上 OpenBMCLAPI 版本与查询时间，版本号取不到时省略。

### `oba node`

<CommandUsage usage="oba node [<rank>]" :params="['rank=节点排名，从 1 开始']" permission="public" />

获取指定排名节点的状态，省略排名时取第 1 名。以绿、红方块表示节点启用状态，列出节点名称、ID、当日流量、当日请求数与查询时间；节点带赞助商时单独发送赞助商名称、网站与横幅图片，横幅发送失败时只发文字。排名小于 1 或超出排行榜范围时返回无效节点提示。

### `oba top`

<CommandUsage usage="oba top [<rank>]" :params="['rank=起始排名，从 1 开始']" permission="public" />

从指定排名开始列出至多 10 个节点，省略排名时从第 1 名开始，排名小于 1 时按第 1 名处理。每行给出名次、节点名称、ID、当日流量、当日请求数与赞助商名称，名单达到显示上限时在末尾附折叠提示。

### `oba search`

<CommandUsage usage="oba search <keyword>" :params="['keyword=节点或赞助商名称关键词']" permission="public" />

按节点名称或赞助商名称搜索，对关键词做不区分大小写的正则匹配。展示格式与 `oba top` 一致，名次沿用完整排行榜中的位置；命中超过 10 条时截断并附折叠提示，未找到时返回未找到结果提示。

### `oba sponsor`

<CommandUsage usage="oba sponsor" permission="public" />

获取随机节点赞助商，发送赞助商名称、网站与横幅图片，横幅发送失败时只发文字。消息附有该赞助商与 Teahouse Studios 无从属关系的说明。
