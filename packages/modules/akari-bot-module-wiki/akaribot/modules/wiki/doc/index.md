# wiki

面向 MediaWiki 站点的综合工具包：查询页面与模板、按 InterWiki 跳转、自定义请求头与前缀、审核 Wiki API 地址、管理 Wiki 机器人账号、监控滥用日志与最近更改，以及订阅中文 Minecraft Wiki 的每周页面与茶馆周报。

`wiki`、`ab`、`rc`、`newbie`、`user` 的查询使用当前场景设置的默认 Wiki；`wiki-audit` 与 `wiki-bot` 不依赖默认 Wiki。

## wiki

### `wiki`

<CommandUsage :usage="['wiki', 'wiki <pagename> [-l <lang>]']" :params="['pagename=页面标题，可带 InterWiki 前缀', 'lang=语言代码，如 zh、en']" permission="public" :options="[{flag: '-l', desc: '查找该页面的对应语言版本；无结果时返回当前语言。'}]" />

省略标题时查询默认 Wiki 的主页，未设置默认 Wiki 时返回设置提示。填写标题时查询对应页面；参数含模板或解析函数表达式时按魔术字求值查询。已配置的自定义前缀会附加在标题前，标题带已配置的 InterWiki 前缀时改查对应的 Wiki。

### `wiki magic`

<CommandUsage usage="wiki magic <expression> [-p <page>]" :params="['expression=魔术字表达式，可省略花括号', 'page=求值用的页面上下文']" permission="public" :options="[{flag: '-p', desc: '指定魔术字求值时的页面上下文；含空格的标题用引号包裹。'}]" />

查询目标 Wiki 注册的魔术字与扩展解析函数，返回短文本或查询链接，支持 `#expr`、字符串处理与站点变量。表达式不完整、包含未支持的魔术字、缺少页面上下文或结果过长时返回对应提示。

### `wiki id`

<CommandUsage usage="wiki id <pageid> [-l <lang>]" :params="['pageid=数字页面 ID，可带 InterWiki 前缀', 'lang=语言代码，如 zh、en']" permission="public" :options="[{flag: '-l', desc: '查找该页面的对应语言版本；无结果时返回当前语言。'}]" />

按页面 ID 查询。`<pageid>` 必须为数字，可带 InterWiki 前缀；非数字时返回提示。

### `wiki random`

<CommandUsage usage="wiki random" permission="public" />

随机查询一个条目命名空间页面。

### `wiki search`

<CommandUsage usage="wiki search <pagename>" :params="['pagename=搜索关键词']" permission="public" />

搜索页面，至多返回 5 条结果，回复编号或点击按钮查询对应页面。

### `wiki render`

<CommandUsage usage="wiki render <mode>" :params="['mode=渲染方式 button、auto、off']" permission="admin" />

切换页面渲染方式。`button` 在消息中提供预览按钮，`auto` 自动渲染页面摘要与 Infobox，`off` 关闭页面渲染。取值不在三者之内时返回错误提示。

### `wiki set`

<CommandUsage usage="wiki set <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="admin" :aliases="['wiki_start_site']" />

设置场景默认 Wiki，参数为页面地址、站点地址或 API 地址。每个场景保存一个默认 Wiki，重复设置覆盖原值；地址无法解析时返回失败详情，处于全局阻止列表时拒绝设置。

`wiki iw` 组的子命令均可用 `interwiki` 代替，例如 `interwiki list`。

### `wiki iw add`

<CommandUsage usage="wiki iw add <interwiki> <wikiurl>" :params="['interwiki=InterWiki 前缀名', 'wikiurl=站点地址，解析为 API 地址']" permission="admin" :aliases="['wiki iw set']" />

添加自定义 InterWiki，`<interwiki>` 为前缀名，`<wikiurl>` 解析为 API 地址后保存。前缀已存在时覆盖原值，地址无法解析时返回失败详情。

### `wiki iw remove`

<CommandUsage usage="wiki iw remove <interwiki>" :params="['interwiki=InterWiki 前缀名']" permission="admin" :aliases="['wiki iw del', 'wiki iw delete']" />

删除自定义 InterWiki，未设置的前缀同样返回成功。

### `wiki iw list`

<CommandUsage usage="wiki iw list [--legacy]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本列表。'}]" />

列出当前设置的自定义 InterWiki，并附查看默认 Wiki InterWiki 的链接。平台支持图片时渲染为表格图片，`--legacy` 强制文本列表；没有设置时提示添加命令。

### `wiki iw get`

<CommandUsage usage="wiki iw get <interwiki>" :params="['interwiki=InterWiki 前缀名']" permission="public" />

获取 InterWiki 对应的 API 地址。前缀未配置时返回未找到提示。

### `wiki headers show`

<CommandUsage usage="wiki headers show" permission="public" />

列出当前场景设置的自定义请求标头，以 JSON 对象返回；未设置时返回空对象。

### `wiki headers add`

<CommandUsage usage="wiki headers add <headers>" :params="['headers=JSON 对象，标头名与内容']" permission="admin" />

添加或覆盖请求标头，`<headers>` 为 JSON 对象，键为标头名、值为对应内容。参数不是 JSON 对象时返回失败提示。

### `wiki headers remove`

<CommandUsage usage="wiki headers remove <headerkey>" :params="['headerkey=要删除的标头名']" permission="admin" />

按名称删除一个请求标头，标头不存在时返回失败提示。

### `wiki headers reset`

<CommandUsage usage="wiki headers reset" permission="admin" />

清空当前场景设置的全部自定义请求标头。

### `wiki prefix set`

<CommandUsage usage="wiki prefix set <prefix>" :params="['prefix=拼在查询标题前的文本']" permission="admin" />

设置查询标题时附加的前缀。设置后查询会把前缀拼在标题之前，用于统一命名空间或区分同名页面。

### `wiki prefix reset`

<CommandUsage usage="wiki prefix reset" permission="admin" />

清除自定义前缀，恢复按原样查询标题。

### `wiki redlink`

<CommandUsage usage="wiki redlink" permission="admin" />

切换页面不存在时是否返回编辑链接，每次执行在开启与关闭之间切换。

## wiki-inline

<ModuleAlias names="wiki_inline, wiki_regex" />

模块无命令，按消息内容触发。

- `[[标题]]`：查询页面，忽略 `#` 开头的标题，去重后至多处理 5 个。
- `{{模板}}`：解析模板调用与解析函数。
- `≺标题≻` 或 `⧼标题⧽`：查询 MediaWiki 命名空间页面。
- Wiki 页面 URL：生成 Infobox 预览或返回文件，行为受渲染方式影响。

## wiki-audit

<ModuleAlias names="wiki_audit, wau" />

### `wiki-audit trust`

<CommandUsage usage="wiki-audit trust <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="superuser" />

从 Wiki 页面、站点或 API 地址解析 API 地址，并加入全局 URL 允许列表。地址无法解析或处于阻止列表时返回失败。

### `wiki-audit block`

<CommandUsage usage="wiki-audit block <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="superuser" />

从 Wiki 页面、站点或 API 地址解析 API 地址，并加入全局 URL 阻止列表。地址无法解析时返回失败。

### `wiki-audit distrust`

<CommandUsage usage="wiki-audit distrust <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="superuser" />

从全局 URL 用户允许列表移除该 API 地址。地址不在列表中时返回未找到。

### `wiki-audit unblock`

<CommandUsage usage="wiki-audit unblock <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="superuser" />

从全局 URL 用户阻止列表移除该 API 地址。地址不在列表中时返回未找到。

### `wiki-audit query`

<CommandUsage usage="wiki-audit query <wikiurl>" :params="['wikiurl=页面、站点或 API 地址']" permission="superuser" />

解析 API 地址并查询命中的全局允许列表规则，返回规则来源。未命中时返回未授权结论。

## wiki-bot

<ModuleAlias names="wiki_bot, wbot" />

### `wiki-bot login`

<CommandUsage usage="wiki-bot login <apilink> <account> <password>" :params="['apilink=页面、站点或 API 地址', 'account=机器人账号用户名', 'password=账号密码']" permission="superuser" />

登录 Wiki 机器人账号并保存。账号已存在时提示先登出，登录失败时返回失败原因。

### `wiki-bot logout`

<CommandUsage usage="wiki-bot logout <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

删除已保存的机器人账号。

### `wiki-bot toggle`

<CommandUsage usage="wiki-bot toggle" permission="superuser" />

切换当前场景是否使用机器人账号，返回开启或关闭结果。

## ab、rc、newbie、user

### `ab`

<CommandUsage usage="ab [--legacy]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式。'}]" />

获取默认 Wiki 的最近滥用日志。QQ 平台具备合并转发或渲染能力时优先返回对应结果，否则返回普通消息；获取失败或日志受查看权限限制时返回错误提示。

### `rc`

<CommandUsage usage="rc [--legacy]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式。'}]" />

获取默认 Wiki 的最近更改。QQ 平台具备合并转发或渲染能力时优先返回对应结果，否则返回普通消息；获取失败或日志受查看权限限制时返回错误提示。

### `newbie`

<CommandUsage usage="newbie" permission="public" />

获取默认 Wiki 的新用户日志。

### `user`

<CommandUsage usage="user <username>" :params="['username=用户名，可带 InterWiki 前缀']" permission="public" />

查询 MediaWiki 用户信息。`username` 可带 InterWiki 前缀，前缀须在已配置的 InterWiki 中，否则按原名查询。

## wikilog

### `wikilog add wiki`

<CommandUsage usage="wikilog add wiki <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

添加一个 Wiki 到监控列表。地址无法解析时返回失败原因，已在列表中时返回操作失败。

### `wikilog reset wiki`

<CommandUsage usage="wikilog reset wiki <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

将该 Wiki 的监控配置恢复为默认值。

### `wikilog remove wiki`

<CommandUsage usage="wikilog remove wiki <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

从监控列表移除一个 Wiki。地址不在列表中时返回操作失败。

### `wikilog enable`

<CommandUsage usage="wikilog enable <apilink> <logtype>" :params="['apilink=页面、站点或 API 地址', 'logtype=日志类型，ab、rc 或全名']" permission="superuser" />

启用一种类型的日志监控，`logtype` 取 `ab`、`rc` 或对应全名。取值无效或 Wiki 未加入监控列表时返回失败提示。

### `wikilog disable`

<CommandUsage usage="wikilog disable <apilink> <logtype>" :params="['apilink=页面、站点或 API 地址', 'logtype=日志类型，ab、rc 或全名']" permission="superuser" />

禁用一种类型的日志监控。

### `wikilog filter set`

<CommandUsage usage="wikilog filter set <apilink> <logtype> ..." :params="['apilink=页面、站点或 API 地址', 'logtype=日志类型，ab、rc 或全名']" permission="superuser" />

为某一类型的日志设置条件过滤器，`...` 为多条正则。未给出条件时提示设置对象为空。

### `wikilog filter reset`

<CommandUsage usage="wikilog filter reset <apilink> <logtype>" :params="['apilink=页面、站点或 API 地址', 'logtype=日志类型，ab、rc 或全名']" permission="superuser" />

重置某一类型日志的条件过滤器。

### `wikilog filter test`

<CommandUsage usage="wikilog filter test <filters> <example>" :params="['filters=匹配样本的正则表达式', 'example=用于匹配的样例文本']" permission="superuser" />

测试条件过滤器能否匹配给定样例，返回匹配位置。表达式有误时提示匹配失败。

### `wikilog filter example`

<CommandUsage usage="wikilog filter example <example>" :params="['example=待转换的 JSON 数据']" permission="superuser" />

将数据转换为条件过滤器可识别的样例。样本不是合法 JSON 时提示格式无效。

### `wikilog api get`

<CommandUsage usage="wikilog api get <apilink> <logtype>" :params="['apilink=页面、站点或 API 地址', 'logtype=日志类型，ab、rc 或全名']" permission="superuser" />

获取指定 Wiki 的指定 API 数据链接。

### `wikilog rcshow set`

<CommandUsage usage="wikilog rcshow set <apilink> ..." :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

为最近更改日志设置筛选条件，取值见下文列表。条件无效时返回提示。

### `wikilog rcshow reset`

<CommandUsage usage="wikilog rcshow reset <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

重置最近更改日志设置的筛选条件。

### `wikilog bot enable`

<CommandUsage usage="wikilog bot enable <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

启用机器人获取日志。

### `wikilog bot disable`

<CommandUsage usage="wikilog bot disable <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

禁用机器人获取日志。

### `wikilog keepalive enable`

<CommandUsage usage="wikilog keepalive enable <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

启用机器人登录状态检查。

### `wikilog keepalive disable`

<CommandUsage usage="wikilog keepalive disable <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

禁用机器人登录状态检查。

### `wikilog note set`

<CommandUsage usage="wikilog note set <apilink> ..." :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

设置一条 Wiki 的备注，监控消息中以备注替换 Wiki 名称。Wiki 未加入监控列表时返回失败。

### `wikilog note remove`

<CommandUsage usage="wikilog note remove <apilink>" :params="['apilink=页面、站点或 API 地址']" permission="superuser" />

移除一条 Wiki 的备注。

### `wikilog list`

<CommandUsage usage="wikilog list" permission="superuser" />

列出所有已设置的内容。

`logtype` 接受 `ab`、`rc`、`abuselog`、`recentchanges`、`AbuseLog` 与 `RecentChanges`。最近更改筛选条件取 `!anon`、`!autopatrolled`、`!bot`、`!minor`、`!patrolled`、`!redirect`、`anon`、`autopatrolled`、`bot`、`minor`、`patrolled`、`redirect` 与 `unpatrolled`。

## weekly

### `weekly`

<CommandUsage usage="weekly" permission="public" />

获取中文 Minecraft Wiki 的每周页面，QQ 系平台附带图片。

### `weekly image`

<CommandUsage usage="weekly image" permission="public" />

获取每周页面的截图版。

### `weekly teahouse`

<CommandUsage usage="weekly teahouse" permission="public" />

获取茶馆周报。

### `weekly teahouse image`

<CommandUsage usage="weekly teahouse image" permission="public" />

获取茶馆周报的截图版。

## RSS

`weekly-rss` 与 `teahouse-weekly-rss` 没有命令，只提供 RSS 订阅：前者在每周一 9:00 推送中文 Minecraft Wiki 每周页面，后者在每周一 9:30 推送茶馆周报。推送同时提供简体中文与繁体中文文本，QQ 平台使用图片版本。
