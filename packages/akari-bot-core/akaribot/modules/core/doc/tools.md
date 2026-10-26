# 工具

本组包含信息查询、消息复述、运维与调试命令：`about`、`say`、`echo`、`post`、`post-whitelist`、
`jobqueue`、`restart`、`update`、`update&restart`、`features`、`analytics`、`url-audit`、`webrender`、`raise`。

## about

基础模块，别名 `version`、`ping`、`status` 指向对应子命令。

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~about` | 所有人 | 简介、仓库与反馈链接、制作人员入口 |
| `~about credits` | 所有人 | 制作人员名单，资源缺失时提示不可用 |
| `~about permissions [<qq_group_id>]` | 所有人 | QQBot 权限配置链接，仅 `QQBot` |
| `~ping` | 所有人 | 返回 Pong 与运行时长、CPU、内存、磁盘占用 |
| `~status` | 超级用户 | 系统与运行时详情，含进程占用与 WebRender 状态 |

## say 与 echo

| 命令 | 说明 |
| --- | --- |
| `~say <display_msg>` | 以消息链解析并复述，不引用原消息 |
| `~say md <display_msg>` | 以 Markdown 复述并附带按钮示例 |
| `~echo [<display_msg>]` | 原文复述，不解析消息元素 |
| `~echo` | 等待下一条消息后复述其显示文本 |

两者均为超级用户模块。`say` 会把平台账号标记写入文本，`echo` 使用 `allow_parse=False` 避免二次解析。

## post 与 post-whitelist

| 命令 | 说明 |
| --- | --- |
| `~post <target> <post_msg>` | 向指定场景发送消息，执行前确认 |
| `~post global <post_msg>` | 向全部启用场景广播，执行前确认 |
| `~post-whitelist <group_id>` | 切换 QQ 群的主动推送优先级，仅 `QQ` |

`post_msg` 支持 KE 码。目标 ID 必须带平台前缀，否则提示当前场景前缀。`post-whitelist` 把
`in_post_whitelist` 写入场景数据，适配器在主动推送时据此把该场景放入高优先级队列。

## jobqueue、restart、raise

| 命令 | 说明 |
| --- | --- |
| `~jobqueue clear` | 清空队列任务，包含执行中的任务 |
| `~restart [--force]` | 重启全部子进程；默认等待在途命令并确认 |
| `~raise [<args>]` | 抛出 `TestException`，用于验证错误上报链路 |

`restart` 在 `Web` 平台不注册，仅在子进程模式可用。执行前把发起会话写入
`data/private/<client>/.cache_restart_author`，随后进程以退出码 33 结束，由守护进程重启全部子进程；
重启完成后提示投递给原场景。`--force` 跳过确认与等待。

## update 与 update&restart

| 命令 | 说明 |
| --- | --- |
| `~update [--force]` | 委托 `akaribot module update --all --non-interactive --defer-runtime --json` |
| `~update&restart [--force]` | 先更新，再走重启流程，别名 `u&r` |

- 更新由 CLI 子进程执行，机器人与 Server 进程只读配置，不直接写盘或迁移数据库。
- 二进制封装模式下拒绝执行并提示改用发行包。
- 报告列出成功、失败、跳过的包；存在未热装载的包时提示执行 `~restart`。
- `update&restart` 在 `Web` 平台不注册，仅在子进程模式可用。

## features

| 命令 | 说明 |
| --- | --- |
| `~features` | 逐项列出当前会话的能力标志 |

同时抓取该场景的会话快照并对比，差异项以 `*` 标出；抓取失败时第二列显示未知。字段来自 `Features`，
见[适配器开发](../../../core/doc/adapter-development.md)。

## analytics

超级用户模块，别名 `ana`，依赖 `enable_analytics` 与可选依赖 `matplotlib`。

| 命令 | 说明 |
| --- | --- |
| `~analytics` | 统计总数、今日数量与首条记录时间 |
| `~analytics days [<module>]` | 近 30 天折线图，可按模块过滤 |
| `~analytics year [<module>]` | 近 12 个月折线图 |
| `~analytics modules [<rank>]` | 模块使用排行，默认前 30 |

统计关闭时提示已停用；缺少 `matplotlib` 时提示安装 `image` extra，不生成图表。数据写入由
`telemetry` 完成，见[解析器](parser.md)。

## url-audit

超级用户模块，维护全局 URL 允许与阻止规则。

| 命令 | 说明 |
| --- | --- |
| `~url-audit allowlist add <url>` | 添加精确允许规则 |
| `~url-audit allowlist add-regex <url>` | 添加正则允许规则 |
| `~url-audit allowlist remove <url>` / `remove-regex <url>` | 移除规则 |
| `~url-audit allowlist query <url>` | 查询命中规则 |
| `~url-audit allowlist list` | 列出全部允许规则 |
| `~url-audit blocklist add <url>` / `add-regex <url>` | 添加阻止规则 |
| `~url-audit blocklist remove <url>` / `remove-regex <url>` | 移除阻止规则 |
| `~url-audit blocklist query <url>` | 查询是否被阻止 |
| `~url-audit blocklist list` | 列出全部阻止规则 |

规则存放在实例 `data/url_audit/`，列表以图片表格展示。规则不合法时返回具体原因。是否启用 URL 管理
由 `enable_urlmanager` 控制。

## webrender

超级用户模块，控制网页渲染服务。

| 命令 | 说明 |
| --- | --- |
| `~webrender status` | 输出渲染服务状态 |
| `~webrender start` | 启动本地渲染服务 |
| `~webrender stop` | 停止渲染服务 |
| `~webrender reload` | 重启渲染服务 |

服务参数在 `config/webrender.toml`，包括 `enable`、`browser_type`、`browser_executable_path`、
`headless`、`remote_only` 与 `remote_web_render_url`。渲染不可用时，依赖截图的命令按各自策略降级。
