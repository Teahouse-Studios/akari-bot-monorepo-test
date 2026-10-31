# wiki

面向 MediaWiki 站点的综合工具包：查询页面与模板、按 InterWiki 跳转、自定义请求头与前缀、审核 Wiki API 地址、管理 Wiki 机器人账号、监控滥用日志与最近更改，以及订阅中文 Minecraft Wiki 的每周页面与茶馆周报。

本包注册 12 个模块，安装一次即可使用全部能力。

## 命令概览

下表省略命令前缀，前缀由实例配置决定。`wiki` 是主要入口。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `wiki` / `wiki <pagename> [-l <lang>]` | 查询主页或指定页面 | 所有用户 |
| `wiki search <pagename>` | 搜索页面 | 所有用户 |
| `wiki id <pageid> [-l <lang>]` | 按页面 ID 查询 | 所有用户 |
| `wiki random` | 随机页面 | 所有用户 |
| `wiki magic <expression> [-p <page>]` | 查询魔术字与解析函数 | 所有用户 |
| `wiki set <wikiurl>` | 设置默认 Wiki | 会话管理员 |
| `wiki iw add/remove/list/get` | 管理 InterWiki | 增删需会话管理员 |
| `wiki render <mode>` | 切换渲染方式 | 会话管理员 |

每条命令的参数、权限与输出见[命令表](commands.md)。
