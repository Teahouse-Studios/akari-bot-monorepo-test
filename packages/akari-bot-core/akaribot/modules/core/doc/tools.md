# 工具

本组包含信息查询、消息复述、运维与调试命令：`about`、`say`、`echo`、`post`、`post-whitelist`、`jobqueue`、`restart`、`update`、`update&restart`、`features`、`analytics`、`url-audit`、`webrender`、`raise`。

## about

基础模块，别名 `version`、`ping`、`status` 指向对应子命令。

### `about`

<CommandUsage usage="about" permission="public" />

输出简介、仓库与反馈链接、制作人员入口。配图与链接按品牌资产与 `repo_url`、`issue_url`、`donate_url` 配置生成，平台支持按钮时以按钮呈现。

### `about version`

<CommandUsage usage="about version" permission="public" />

输出机器人版本。源码运行时附带对应提交链接，发行版附带发行标签链接；版本号未知时给出提示。链接由 `enable_commit_url` 控制。

### `about credits`

<CommandUsage usage="about credits" permission="public" />

输出制作人员名单。品牌资产中缺少名单文件或内容为空时提示不可用。

### `about permissions`

<CommandUsage usage="about permissions [<qq_group_id>]" :params="['qq_group_id=QQ 群号，用于生成权限链接']" permission="public" />

仅 QQBot 平台可用。生成 QQBot 群聊的权限配置链接。省略群号时返回带占位提示的命令补全入口，群号非数字时返回提示。

### `about ping`

<CommandUsage usage="about ping" permission="public" />

返回 Pong 与运行时长、CPU、内存、磁盘占用。

### `about status`

<CommandUsage usage="about status" permission="superuser" />

输出系统与运行时详情，含进程占用与 WebRender 状态。

## say

模块级权限为超级用户。

### `say`

<CommandUsage usage="say <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

以消息链解析并复述给定内容，不引用原消息，发送者的平台账号标记写入文本。

### `say md`

<CommandUsage usage="say md <display_msg>" :params="['display_msg=要复述的消息内容']" permission="superuser" />

以 Markdown 复述给定内容，并附带一个按钮示例。

## echo

模块级权限为超级用户。

### `echo`

<CommandUsage :usage="['echo', 'echo [<display_msg>]']" :params="['display_msg=要原文复述的消息内容']" permission="superuser" />

原文复述给定内容，不解析消息元素。省略参数时等待下一条消息，复述其显示文本。

## post

模块级权限为超级用户。

### `post`

<CommandUsage usage="post <target> <post_msg>" :params="['target=目标场景 ID，须带平台前缀', 'post_msg=推送内容，支持 KE 码']" permission="superuser" />

向指定场景推送主动消息，执行前要求确认。目标 ID 须带平台前缀，否则提示当前场景前缀；`post_msg` 支持 KE 码。

### `post global`

<CommandUsage usage="post global <post_msg>" :params="['post_msg=广播内容，支持 KE 码']" permission="superuser" />

向全部启用场景广播主动消息，执行前要求确认。

## post-whitelist

<ModuleAlias names="post_whitelist" />

模块级权限为超级用户。

### `post-whitelist`

<CommandUsage usage="post-whitelist <group_id>" :params="['group_id=QQ 群 ID，须带平台前缀']" permission="superuser" />

仅 QQ 平台可用。切换 QQ 群的主动推送优先级。参数须为 `QQ|Group|` 前缀的完整 ID，场景尚无 union 时先确认再创建。该开关写入场景数据的 `in_post_whitelist`，适配器在主动推送时据此把场景放入高优先级队列。

## jobqueue

模块级权限为超级用户。

### `jobqueue clear`

<CommandUsage usage="jobqueue clear" permission="superuser" />

清空计划任务队列，包含执行中的任务。

## restart

模块级权限为超级用户。

### `restart`

<CommandUsage usage="restart [--force]" permission="superuser" :options="[{flag: '--force', desc: '跳过确认与等待强制重启'}]" />

Web 平台不注册，仅在子进程模式可用。重启全部子进程。默认等待在途命令并确认，60 秒内仍有命令在执行时给出提示；`--force` 跳过确认与等待。 执行前把发起会话写入 `data/private/<client>/.cache_restart_author`，进程以退出码 33 结束，由守护进程重启全部子进程，完成后提示投递回原场景。

## raise

模块级权限为超级用户。

### `raise`

<CommandUsage usage="raise [<args>]" :params="['args=异常信息，省略时用内置文案']" permission="superuser" />

抛出 `TestException`，用于验证错误上报链路。参数作为异常信息，省略时使用内置文案。

## update

模块级权限为超级用户。

### `update`

<CommandUsage usage="update [--force]" permission="superuser" :options="[{flag: '--force', desc: '强制重置与更新源代码'}]" />

更新机器人及其依赖，委托 `akaribot module update --all --non-interactive --defer-runtime --json` 完成。 更新由 CLI 子进程执行，机器人与 Server 进程只读配置，不直接写盘或迁移数据库；二进制封装模式下拒绝执行并提示改用发行包。报告列出成功、失败与跳过的包，存在未热装载的包时提示执行 `restart`，否则说明已热装载。

## update&restart

<ModuleAlias names="u&r" />

模块级权限为超级用户。

### `update&restart`

<CommandUsage usage="update&restart [--force]" permission="superuser" :options="[{flag: '--force', desc: '跳过确认，强制重置与更新源代码并强制重启'}]" />

Web 平台不注册，仅在子进程模式可用。先更新再走重启流程。`--force` 跳过确认与等待，其余情形先确认并等待在途命令；更新报告发出后进程按 `restart` 的流程结束，由守护进程拉起全部子进程。

## features

模块级权限为超级用户。

### `features`

<CommandUsage usage="features" permission="superuser" />

逐项列出当前会话的能力标志。同时抓取该场景的会话快照作对比，差异项以 `*` 标出，抓取失败时第二列显示未知。字段来自 `Features`，见[适配器开发](../../../core/doc/adapter-development.md)。

## analytics

<ModuleAlias names="ana" />

模块级权限为超级用户。

### `analytics`

<CommandUsage usage="analytics" permission="superuser" />

输出命令总数、今日数量与首条记录时间。

### `analytics days`

<CommandUsage usage="analytics days [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

输出近 30 天的命令数折线图，可按模块过滤。

### `analytics year`

<CommandUsage usage="analytics year [<module>]" :params="['module=按模块名筛选，省略则不筛选']" permission="superuser" />

输出近 12 个月的命令数折线图，可按模块过滤。

### `analytics modules`

<CommandUsage usage="analytics modules [<rank>]" :params="['rank=列出的模块数，缺省为 30']" permission="superuser" />

输出模块命令调用排行，横向条形图，`<rank>` 缺省为 30。

统计关闭时提示已停用；缺少 `matplotlib` 时提示安装 `image` extra，不生成图表。数据写入由 `telemetry` 完成，见[解析器](parser.md)。

## url-audit

模块级权限为超级用户，维护全局 URL 允许与阻止规则。规则存放在实例 `data/url_audit/`，是否启用由 `enable_urlmanager` 控制。

### `url-audit allowlist add`

<CommandUsage usage="url-audit allowlist add <url>" :params="['url=要加入允许列表的 URL']" permission="superuser" />

向用户自定义的全局允许列表添加精确 URL。规则已存在时返回提示。

### `url-audit allowlist add-regex`

<CommandUsage usage="url-audit allowlist add-regex <url>" :params="['url=要加入的正则表达式，需完整匹配']" permission="superuser" />

向允许列表添加正则规则，正则须能完整匹配 URL。规则不合法时返回具体原因。

### `url-audit allowlist remove`

<CommandUsage usage="url-audit allowlist remove <url>" :params="['url=要移除的精确 URL']" permission="superuser" />

从允许列表移除精确 URL，规则不存在时返回提示。

### `url-audit allowlist remove-regex`

<CommandUsage usage="url-audit allowlist remove-regex <url>" :params="['url=要移除的正则表达式']" permission="superuser" />

从允许列表移除正则规则。

### `url-audit allowlist query`

<CommandUsage usage="url-audit allowlist query <url>" :params="['url=要查询的 URL']" permission="superuser" />

查询 URL 命中的允许规则，逐条列出规则来源与内容；未命中时提示不被允许。

### `url-audit allowlist list`

<CommandUsage usage="url-audit allowlist list" permission="superuser" />

列出全部允许规则，以图片表格展示来源、类型与规则内容；列表为空时返回提示。

### `url-audit blocklist add`

<CommandUsage usage="url-audit blocklist add <url>" :params="['url=要加入阻止列表的 URL']" permission="superuser" />

向用户自定义的全局阻止列表添加精确 URL。规则已存在时返回提示。

### `url-audit blocklist add-regex`

<CommandUsage usage="url-audit blocklist add-regex <url>" :params="['url=要加入的正则表达式，需完整匹配']" permission="superuser" />

向阻止列表添加正则规则，正则须能完整匹配 URL。规则不合法时返回具体原因。

### `url-audit blocklist remove`

<CommandUsage usage="url-audit blocklist remove <url>" :params="['url=要移除的精确 URL']" permission="superuser" />

从阻止列表移除精确 URL，规则不存在时返回提示。

### `url-audit blocklist remove-regex`

<CommandUsage usage="url-audit blocklist remove-regex <url>" :params="['url=要移除的正则表达式']" permission="superuser" />

从阻止列表移除正则规则。

### `url-audit blocklist query`

<CommandUsage usage="url-audit blocklist query <url>" :params="['url=要查询的 URL']" permission="superuser" />

查询 URL 命中的阻止规则；未命中时提示未被阻止。

### `url-audit blocklist list`

<CommandUsage usage="url-audit blocklist list" permission="superuser" />

列出全部阻止规则，以图片表格展示来源、类型与规则内容；列表为空时返回提示。

## webrender

模块级权限为超级用户，控制网页渲染服务。

### `webrender status`

<CommandUsage usage="webrender status" permission="superuser" />

输出渲染服务状态。

### `webrender start`

<CommandUsage usage="webrender start" permission="superuser" />

启动本地渲染服务，成功后刷新运行时记录的渲染状态。

### `webrender stop`

<CommandUsage usage="webrender stop" permission="superuser" />

停止渲染服务，并同步运行时状态。

### `webrender reload`

<CommandUsage usage="webrender reload" permission="superuser" />

先关闭再启动渲染服务，用于加载新的配置。

服务参数在 `config/webrender.toml`，包括 `enable`、`browser_type`、`browser_executable_path`、`headless`、`remote_only` 与 `remote_web_render_url`。渲染不可用时，依赖截图的命令按各自策略降级。
