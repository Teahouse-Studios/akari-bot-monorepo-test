# Wiki 查询

面向 MediaWiki 站点的综合工具包：查询页面与模板、按 InterWiki 跳转、自定义请求头与前缀、审核 Wiki API 地址、管理 Wiki 机器人账号、监控滥用日志与最近更改，以及订阅中文 Minecraft Wiki 的每周页面与茶馆周报。

本包注册 12 个模块，安装一次即可使用全部能力。

## 安装

```bash
akaribot module add akari-bot-module-wiki
```

安装后在会话中由管理员分别用 `module enable <模块名>` 开启所需模块。

## 模块

| 模块 | 别名 | 说明 | 权限 |
| --- | --- | --- | --- |
| `wiki` | 无 | 页面查询、默认 Wiki、InterWiki、请求头、前缀与渲染方式 | 查询类公开，设置类需会话管理员 |
| `wiki-inline` | `wiki_inline`、`wiki_regex` | 自动解析消息中的 Wiki 语法与链接 | 所有用户 |
| `wiki-audit` | `wiki_audit`、`wau` | 管理全局 URL 允许列表与阻止列表 | 超级用户 |
| `wiki-bot` | `wiki_bot`、`wbot` | 管理 Wiki 机器人账号并切换使用状态 | 超级用户 |
| `wikilog` | 无 | 监控 Wiki 滥用日志与最近更改 | 超级用户 |
| `ab` | 无 | 获取默认 Wiki 的最近滥用日志 | 所有用户 |
| `rc` | 无 | 获取默认 Wiki 的最近更改 | 所有用户 |
| `newbie` | 无 | 获取默认 Wiki 的新用户日志 | 所有用户 |
| `user` | 无 | 查询 MediaWiki 用户信息 | 所有用户 |
| `weekly` | 无 | 获取中文 Minecraft Wiki 每周页面 | 所有用户 |
| `weekly-rss` | `weekly_rss`、`weeklyrss` | 订阅中文 Minecraft Wiki 每周页面 | RSS |
| `teahouse-weekly-rss` | `teahouse_weekly_rss`、`teahouseweeklyrss`、`teahouserss` | 订阅茶馆周报 | RSS |

完整命令与参数见 [命令表](commands.md)。

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

## 配置项

配置表 `module_wiki`（`config/module_wiki.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wiki_allowlist_url` | str | 项目 Issue 模板地址 | Wiki API 加入全局 URL 允许列表的申请网址 |

默认值为 `https://github.com/Teahouse-Studios/akari-bot/issues/new?template=request_wiki_whitelist.yaml`。设置未列入全局允许列表但未被阻止的 Wiki 时，成功提示后会附带该申请地址；已列入阻止列表的 Wiki 拒绝设置。

## 权限与平台能力

- `wiki` 的查询、搜索、随机、魔术字、InterWiki 查看与请求头查看对普通用户开放；`set`、`iw add`、`iw remove`、`headers add`、`headers remove`、`headers reset`、`prefix set`、`prefix reset`、`redlink`、`render` 需要会话管理员权限。
- `wiki-audit`、`wiki-bot` 与 `wikilog` 需要超级用户权限；`wikilog` 同时声明管理员权限，超级用户可直接使用。
- `wiki-inline` 通过正则匹配触发，不需要命令前缀。
- 页面截图与部分 Infobox 预览依赖 WebRender；未启用时改用文本或链接。
- QQ 平台的 `rc` 与 `ab` 在支持消息节点或 WebRender 可用时优先返回合并转发或渲染结果，否则回退到文本。
- URL 允许列表与阻止列表由 core 的全局规则管理；未通过检查的 Wiki 会被阻止或标记为不信任。
- `weekly` 声明支持简体中文与繁体中文；繁体请求使用 `variant=zh-tw`。

## 数据表

manifest 声明四个表。

| 表 | 内容 |
| --- | --- |
| `module_wiki_target_set_info` | 场景级默认 Wiki、InterWiki、请求头与前缀 |
| `module_wiki_site_info` | Wiki 站点信息缓存与更新时间 |
| `module_wiki_bot_account_list` | Wiki 机器人账号与密码 |
| `module_wikilog_target_set_info` | 日志监控目标、过滤器、最近更改筛选、备注与保活开关 |

`module_wiki_target_set_info` 与 `module_wikilog_target_set_info` 按场景归属；包内 `migrations/` 提供表结构升级脚本。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`akari-bot-html2text`、`Pillow`、`aiocqhttp`、`akari-bot-webrender`、`attrs`、`beautifulsoup4`、`feedparser`、`filetype`、`httpx`、`jinja2`、`orjson`、`tortoise-orm`、`wikitextparser`。
- 页面查询使用目标 Wiki 的 `api.php`；站点信息缓存在 `module_wiki_site_info`。
- 每周页面来自 `https://zh.minecraft.wiki`，茶馆周报来自 `https://lakeus.xyz/api.php?action=featuredfeed&feed=teahouse-weekly`。
- 截图与 Infobox 预览依赖 WebRender。
