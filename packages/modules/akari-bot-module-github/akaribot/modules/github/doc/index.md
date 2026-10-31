# github

通过 GitHub REST API 查询仓库、用户或组织信息，并按关键词搜索仓库。仓库结果包含 Star、Fork、语言与许可证，用户结果包含关注数、公开仓库数与最近活跃时间。

## 命令

| 命令 | 说明 |
| --- | --- |
| `github <name>` | 自动识别：名称含 `/` 时查询仓库，否则查询用户或组织 |
| `github repo <name>` | 查询仓库信息，并附带 OpenGraph 预览图 |
| `github user <name>` | 查询用户或组织信息 |
| `github search <keyword>` | 搜索仓库，最多列出 5 条结果 |

仓库、用户与搜索接口共用同一个可选令牌；未配置令牌时以匿名身份请求。

### `github <name>`

名称含 `/` 时按仓库查询，否则查询用户或组织，是 `repo` 与 `user` 的快捷写法。

### `github repo <name>`

查询仓库的 Star、Fork、语言与许可证，并附带 OpenGraph 预览图；仓库不存在时返回未找到提示。

### `github user <name>`

查询用户或组织的关注数、公开仓库数与最近活跃时间；名称不存在时返回未找到提示。

### `github search <keyword>`

按关键词搜索仓库，最多列出 5 条结果；无匹配时返回未找到提示。
