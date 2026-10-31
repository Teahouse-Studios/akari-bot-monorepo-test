# mcplayer

通过玩家名或 UUID 查询 Minecraft：Java 版玩家，返回名称、UUID、NameMC 链接与皮肤、渲染图、披风图片。
模块名 `mcplayer`，别名 `namemc`。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcplayer <username_or_uuid>` | 查询玩家信息 | 所有用户 |

参数长度为 32 时按无连字符 UUID 处理；长度为 36 且含 4 个连字符时按带连字符 UUID 处理，去掉连字符
后查询；其余输入按玩家名解析为 UUID。UUID 查询走 Mojang 的 `user/profile` 接口，玩家名查询走
`users/profiles/minecraft` 接口。

皮肤与披风从 Crafatar 获取：渲染图为全身像，皮肤为原始皮肤文件，存在披风时附带披风图。玩家不存在
或名称无法解析时返回未找到提示；Crafatar 请求失败时降级为名称、UUID 与 NameMC 链接。
