---
order: 33
submenu: 钩子
---

# tos

此 Hook 用令牌桶限制命令和正则的调用频率。超过限制后，机器人临时封禁该发送者。

说明：

- 相关配置项为 `enable_tos`、`tos_warning_counts`、`tos_temp_ban_time` 和 `report_targets`。
- 机器人在 `COMMAND_BEFORE_PARSE` 和 `REGEX_BEFORE_EXECUTE` 阶段计数，在 `COMMAND_PREPARE` 和 `REGEX_PREPARE` 阶段检查发送者是否处于临时封禁。
- `EXECUTION_ERROR` 捕获 `AbuseWarning`。警告次数超过 `tos_warning_counts` 后，机器人临时封禁该发送者，封禁时长由 `tos_temp_ban_time` 控制，默认 300 秒。
- 模块提供带名称的 Hook：`check_temp_ban`、`remove_temp_ban`、`report` 和 `warning_counts`，供 `abuse` 等模块调用。
