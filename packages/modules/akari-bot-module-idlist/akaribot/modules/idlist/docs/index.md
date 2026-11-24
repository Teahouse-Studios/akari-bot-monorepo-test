# idlist

此模块用于查询 Minecraft：基岩版的 ID 映射表，按照关键词检索标识符及其对应值。

## 命令

### `idlist`

<CommandUsage usage="idlist <query>" :params="['query=检索关键词']" permission="public" />

按照关键词查询 ID 映射表。每条结果显示为“枚举名：键 -> 值”，取值仅截取首行。单次最多展示 5 条结果。若命中总数超过 5 条，将返回折叠提示与完整结果页链接。未检索到匹配项时返回未找到提示。

<ChatExample
  :log="[
    '用户：~idlist chiseled_polished_blackstone',
    '机器人：方块：chiseled_polished_blackstone -> 雕纹磨制黑石',
    '物品：chiseled_polished_blackstone -> 雕纹磨制黑石',
    '配方：minecraft:chiseled_polished_blackstone -> <工作台>磨制黑石台阶*2->雕纹磨制黑石',
  ]"
/>
