---
order: 30
submenu: 钩子
---

# parser_policies

以下为消息入口的内置策略，按入口顺序执行。同一入口内先执行优先级数值小的策略。

| 入口 | 优先级 | 行为 |
| --- | --- | --- |
| `SESSION_READY` | 10 | 丢弃 `ignored_sender`、同场景其它机器人、黑名单用户与被本场景限制用户的消息 |
| `COMMAND_PREPARE` | 5 | 场景冷却：非管理员在 `cooldown_time` 内只收到一次提示 |
| `COMMAND_PREPARE` | 30 | 模块路由：权限、平台能力、场景启用状态与自动启用确认 |
| `COMMAND_ROUTE` | 20 | 禁止发言场景只放行 `mute` |
| `COMMAND_BEFORE_EXECUTE` | 10 | 命令级权限校验 |
| `COMMAND_BEFORE_EXECUTE` | 100 | 执行锁被占用时提示“正在运行” |
| `REGEX_ROUTE` | 10 | 跳过正则禁用前缀、禁止发言场景与运行中提醒 |
| `REGEX_PREPARE` | 5 / 15 | 正则权限与冷却 |
| `COMMAND_UNMATCHED` | 100 | 未匹配时提示语法错误或未加载提示 |
| `OUTGOING_BEFORE_SEND` | 10 | 阻止发往禁止发言场景的主动推送 |

场景冷却状态保存在模块的 runtime 中。同版本热重载后，这些状态仍然保留。管理员不受冷却限制。
