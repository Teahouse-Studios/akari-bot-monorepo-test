# mcmod

此模块用于检索 MC 百科（mcmod.cn）的 Mod 条目，返回搜索结果中首条记录的名称、链接与简介。

## 命令

### `mcmod`

<CommandUsage usage="mcmod <mod_name>" :params="['mod_name=Mod 名称或无歧义缩写']" permission="public" />

按照 Mod 名称检索百科条目。`<mod_name>` 接受无歧义缩写或准确名称。

### `mcmod details`

<CommandUsage usage="mcmod details <content>" :params="['content=物品、方块或实体的 ID 或名称']" permission="public" :aliases="['moddetails']" />

按照 Mod 内容检索百科条目。`<content>` 接受物品、方块或实体的 ID 或准确名称。

两条命令均依赖 WebRender 获取页面内容，结果仅选取首条记录，输出名称、链接与简介。若未启用 WebRender、页面为空或不存在匹配条目，均返回未找到结果的提示。
