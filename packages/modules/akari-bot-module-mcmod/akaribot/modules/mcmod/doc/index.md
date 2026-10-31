# mcmod

检索 MC 百科（mcmod.cn）的 Mod 条目，返回搜索结果第一条的名称、链接与简介。模块名 `mcmod`，别名
`moddetails`，后者等价于 `mcmod details`。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcmod <mod_name>` | 按 Mod 名称搜索，可使用无歧义缩写或准确名称 | 所有用户 |
| `mcmod details <content>` | 按内容搜索，可使用物品、方块或实体的 ID 或准确名称 | 所有用户 |

两条命令都只取搜索结果的第一条，输出名称、链接与简介；页面为空或没有匹配条目时返回未找到结果。
名称搜索使用 `https://search.mcmod.cn/s?key=`，内容搜索在此基础上附加 `filter=3` 参数。
