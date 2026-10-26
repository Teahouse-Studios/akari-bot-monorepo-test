# 解析器

本组模块全部为 `hidden=True` 的基础模块，不提供用户命令，由 `HookPoint` 入口驱动：
`parser_errors`、`parser_policies`、`parser_routing`、`tos`、`typo`、`telemetry`、`retired_policy`。

## parser_policies

消息入口的内置策略，按入口顺序执行：

| 入口 | 优先级 | 行为 |
| --- | --- | --- |
| `SESSION_READY` | 10 | 丢弃 `ignored_sender`、同场景其它机器人、黑名单用户与被本场景限制用户的消息 |
| `COMMAND_PREPARE` | 5 | 场景冷却：非管理员在 `cooldown_time` 内只收到一次提示 |
| `COMMAND_PREPARE` | 30 | 模块路由：权限、平台能力、场景启用状态与自动启用确认 |
| `COMMAND_ROUTE` | 20 | 静音场景只放行 `mute` |
| `COMMAND_BEFORE_EXECUTE` | 10 | 命令级权限校验 |
| `COMMAND_BEFORE_EXECUTE` | 100 | 执行锁被占用时提示「正在运行」 |
| `REGEX_ROUTE` | 10 | 跳过正则禁用前缀、静音场景与运行中提醒 |
| `REGEX_PREPARE` | 5 / 15 | 正则权限与冷却 |
| `COMMAND_UNMATCHED` | 100 | 未匹配时提示语法错误或未加载提示 |
| `OUTGOING_BEFORE_SEND` | 10 | 抑制发往静音场景的主动推送 |

场景冷却状态保存在模块 runtime 中，同版本热重载后保留。管理员不受冷却限制。

## parser_routing

处理同一现实场景存在多条消息通道时的重复消息：

- `CHANNEL_CLAIM` 优先级 1 读取场景的 `channel_id` 映射。
- 优先级 100 按「union + 通道 + 命令摘要」在 10 秒窗口内只允许一个平台场景认领，其余候选被丢弃。
- 认领记录保留 30 秒后过期，进程重启后清空。

## parser_errors

统一处理命令与正则抛出的异常：

| 异常 | 反馈 |
| --- | --- |
| `NoReportException` | 回显异常文本，不进入上报流程 |
| `ExternalException` | 回显异常文本与外部错误说明 |
| `AbuseWarning` | 回显提示与拒绝原因，不进入上报流程 |
| `SendMessageFailed` | 触发平台错误提示与限流文案 |
| 其它异常 | 回显错误详情、上报场景与问题反馈地址，并发送错误报告 |

错误详情按平台能力渲染：支持 Markdown 时使用围栏代码块，否则按纯文本解析。启用表情且平台支持图片时
附带随机表情。上报通过 `send_report()` 发送到 `report_targets`，同时写入 SMTP 报告（若启用）。
模块还提供具名 hook `format_error_detail`，供 RPC 错误报告复用同一格式化逻辑。

## tos

使用令牌桶限制命令与正则的调用频率，并在超限时执行临时封禁：

- 配置项：`enable_tos`、`tos_warning_counts`、`tos_temp_ban_time`、`report_targets`。
- `COMMAND_BEFORE_PARSE`、`REGEX_BEFORE_EXECUTE` 计数；`COMMAND_PREPARE`、`REGEX_PREPARE` 检查临时封禁。
- `EXECUTION_ERROR` 捕获 `AbuseWarning`，警告次数超过 `tos_warning_counts` 后临时封禁，时长由
  `tos_temp_ban_time` 控制（默认 300 秒）。
- 具名 hook：`check_temp_ban`、`remove_temp_ban`、`report`、`warning_counts`，供 `abuse` 等模块调用。

## typo

命令未匹配到模块时给出拼写建议：

- 只在 `unmatched_kind == "module"` 且用户未关闭 `typo_check` 时触发。
- 相似度阈值取自 `typo_check_module_score`、`typo_check_command_score`、`typo_check_args_score`、
  `typo_check_options_score`，长度差异比例由 `typo_check_module_diff_ratio` 控制。
- 建议以 `RecoveryProposal` 返回，由解析器决定是否重试纠正后的命令。

## telemetry

在 `EXECUTION_FINISHED` 与 `FINISHED` 入口统计：

- 每次命令或正则执行递增 `Info.command_parsed`。
- 每条消息解析结束递增 `Info.message_parsed`。
- `enable_analytics` 开启时写入 `analytics_data`，记录场景、发送者、命令、模块与模块类型。
- 写入失败只记录日志，不影响命令收尾。

配置 `enable_analytics` 关闭后停止写表，进程内计数继续累加。

## retired_policy

配合 `config.toml` 的 `retired_clients` 处理退役客户端：

- 退役客户端的消息只放行 `merge` 白名单命令，模块别名改写前实际输入的首词也参与判定。
- 同一消息通道存在未退役场景时，退役场景让出等待任务与命令认领。
- `retired_clients` 为空时策略不生效；非空的 `merge` 模块据此加载，见[会话](session.md)。

配置格式为 `<源客户端> -> <目标客户端>`，仅填写源客户端表示不提供迁移。
