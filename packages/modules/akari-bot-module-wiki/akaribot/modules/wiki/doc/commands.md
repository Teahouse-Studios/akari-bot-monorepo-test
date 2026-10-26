# 命令表

本页列出本包注册的全部命令与正则触发方式。命令前缀由实例配置决定，表中省略。`wiki`、`ab`、`rc`、`newbie`、`user` 的查询使用当前场景设置的默认 Wiki；`wiki-audit` 与 `wiki-bot` 不依赖默认 Wiki。

## wiki

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `wiki` | 查询默认 Wiki 的主页 | 所有用户 |
| `wiki <pagename> [-l <lang>]` | 查询页面；`-l` 查找对应语言版本，无结果时返回当前语言 | 所有用户 |
| `wiki magic <expression> [-p <page>]` | 查询魔术字与扩展解析函数，返回短文本或查询链接；`-p` 指定页面上下文 | 所有用户 |
| `wiki id <pageid> [-l <lang>]` | 按页面 ID 查询，`pageid` 可带 InterWiki 前缀 | 所有用户 |
| `wiki random` | 随机查询一个条目命名空间页面 | 所有用户 |
| `wiki search <pagename>` | 搜索页面，至多返回 5 条结果 | 所有用户 |
| `wiki render <mode>` | 切换渲染方式：`button`、`auto` 或 `off` | 会话管理员 |
| `wiki set <wikiurl>` | 设置场景默认 Wiki，参数可为页面、站点或 API 地址 | 会话管理员 |
| `wiki iw add <interwiki> <wikiurl>` | 添加自定义 InterWiki | 会话管理员 |
| `wiki iw remove <interwiki>` | 删除自定义 InterWiki | 会话管理员 |
| `wiki iw list [--legacy]` | 列出 InterWiki；`--legacy` 强制文本列表 | 所有用户 |
| `wiki iw get <interwiki>` | 获取 InterWiki 对应的 API 地址 | 所有用户 |
| `wiki headers show` | 列出当前请求头 | 所有用户 |
| `wiki headers add <headers>` | 以 JSON 合并自定义请求头 | 会话管理员 |
| `wiki headers remove <headerkey>` | 删除指定请求头 | 会话管理员 |
| `wiki headers reset` | 清空自定义请求头 | 会话管理员 |
| `wiki prefix set <prefix>` | 设置页面标题前缀 | 会话管理员 |
| `wiki prefix reset` | 清除页面标题前缀 | 会话管理员 |
| `wiki redlink` | 切换页面不存在时是否返回编辑链接 | 会话管理员 |

命令别名：`wiki_start_site` 等同 `wiki set`，`interwiki` 等同 `wiki iw`，`wiki iw set` 等同 `wiki iw add`，`wiki iw del` 与 `wiki iw delete` 等同 `wiki iw remove`。

渲染方式含义：

- `button`：在消息中提供预览按钮。
- `auto`：自动渲染页面摘要与 Infobox。
- `off`：关闭页面渲染。

## wiki-inline

模块无命令，按消息内容触发。

| 触发形式 | 行为 |
| --- | --- |
| `[[标题]]` | 查询页面，忽略 `#` 开头的标题，去重后至多处理 5 个 |
| `{{模板}}` | 解析模板调用与解析函数 |
| `≺标题≻` 或 `⧼标题⧽` | 查询 MediaWiki 命名空间页面 |
| Wiki 页面 URL | 生成 Infobox 预览或返回文件，行为受渲染方式影响 |

## wiki-audit

模块要求超级用户权限。

| 命令 | 说明 |
| --- | --- |
| `wiki-audit trust <wikiurl>` | 解析 API 地址并加入全局 URL 允许列表 |
| `wiki-audit block <wikiurl>` | 解析 API 地址并加入全局 URL 阻止列表 |
| `wiki-audit distrust <wikiurl>` | 从全局 URL 用户允许列表移除该地址 |
| `wiki-audit unblock <wikiurl>` | 从全局 URL 用户阻止列表移除该地址 |
| `wiki-audit query <wikiurl>` | 查询该地址命中的允许列表规则 |

## wiki-bot

模块要求超级用户权限。

| 命令 | 说明 |
| --- | --- |
| `wiki-bot login <apilink> <account> <password>` | 登录 Wiki 机器人账号并保存 |
| `wiki-bot logout <apilink>` | 删除已保存的机器人账号 |
| `wiki-bot toggle` | 切换当前场景是否使用机器人账号 |

## ab、rc、newbie、user

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `ab [--legacy]` | 获取默认 Wiki 的最近滥用日志 | 所有用户 |
| `rc [--legacy]` | 获取默认 Wiki 的最近更改 | 所有用户 |
| `newbie` | 获取默认 Wiki 的新用户日志 | 所有用户 |
| `user <username>` | 查询 MediaWiki 用户信息，可带 InterWiki 前缀 | 所有用户 |

`ab` 与 `rc` 在 QQ 平台可用时优先返回合并转发或渲染结果，`--legacy` 强制使用普通消息。

## wikilog

模块要求超级用户权限，并随实例定时轮询已启用监控的 Wiki。

| 命令 | 说明 |
| --- | --- |
| `wikilog add wiki <apilink>` | 添加一个 Wiki 到监控列表 |
| `wikilog reset wiki <apilink>` | 重置该 Wiki 的监控配置 |
| `wikilog remove wiki <apilink>` | 从监控列表移除该 Wiki |
| `wikilog enable <apilink> <logtype>` | 启用日志监控，`logtype` 取 `ab`、`rc` 或对应全名 |
| `wikilog disable <apilink> <logtype>` | 禁用日志监控 |
| `wikilog filter set <apilink> <logtype> ...` | 设置条件过滤器，可传多个正则 |
| `wikilog filter reset <apilink> <logtype>` | 重置条件过滤器 |
| `wikilog filter test <filters> <example>` | 测试过滤器是否匹配样例 |
| `wikilog filter example <example>` | 将 JSON 数据转换为过滤器可识别的样例 |
| `wikilog api get <apilink> <logtype>` | 获取该日志接口的原始数据链接 |
| `wikilog rcshow set <apilink> ...` | 设置最近更改筛选条件 |
| `wikilog rcshow reset <apilink>` | 重置最近更改筛选条件 |
| `wikilog bot enable <apilink>` | 启用机器人账号获取日志 |
| `wikilog bot disable <apilink>` | 禁用机器人账号获取日志 |
| `wikilog keepalive enable <apilink>` | 启用登录状态检查 |
| `wikilog keepalive disable <apilink>` | 禁用登录状态检查 |
| `wikilog note set <apilink> ...` | 设置 Wiki 备注，监控消息中替代 Wiki 名称 |
| `wikilog note remove <apilink>` | 移除 Wiki 备注 |
| `wikilog list` | 列出当前监控配置 |

`logtype` 接受 `ab`、`rc`、`abuselog`、`recentchanges`、`AbuseLog` 与 `RecentChanges`。最近更改筛选条件取 `!anon`、`!autopatrolled`、`!bot`、`!minor`、`!patrolled`、`!redirect`、`anon`、`autopatrolled`、`bot`、`minor`、`patrolled`、`redirect` 与 `unpatrolled`。

## weekly 与 RSS

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `weekly` | 获取中文 Minecraft Wiki 每周页面，QQ 系平台附带图片 | 所有用户 |
| `weekly image` | 获取每周页面的截图版 | 所有用户 |
| `weekly teahouse` | 获取茶馆周报 | 所有用户 |
| `weekly teahouse image` | 获取茶馆周报的截图版 | 所有用户 |

`weekly-rss` 与 `teahouse-weekly-rss` 没有命令，只提供 RSS 订阅：前者在每周一 9:00 推送中文 Minecraft Wiki 每周页面，后者在每周一 9:30 推送茶馆周报。推送同时提供简体中文与繁体中文文本，QQ 平台使用图片版本。
