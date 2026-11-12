# idlist

查询 Minecraft：基岩版的 ID 表，按关键词检索标识符及其对应值。

## 命令

### `idlist`

<CommandUsage usage="idlist <query>" :params="['query=检索关键词']" permission="public" />

按关键词查询 ID 表。每条结果显示为“枚举名：键 -> 值”，值只取首行，单次最多展示 5 条；命中总数超过 5 条时追加折叠提示与完整结果页链接。无命中时返回未找到提示。
