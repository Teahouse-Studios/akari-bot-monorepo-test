---
order: 33
submenu: 钩子
---

# tos

使用令牌桶限制命令与正则的调用频率，并在超限时执行临时封禁：

- 配置项：`enable_tos`、`tos_warning_counts`、`tos_temp_ban_time`、`report_targets`。
- `COMMAND_BEFORE_PARSE`、`REGEX_BEFORE_EXECUTE` 计数；`COMMAND_PREPARE`、`REGEX_PREPARE` 检查临时封禁。
- `EXECUTION_ERROR` 捕获 `AbuseWarning`，警告次数超过 `tos_warning_counts` 后临时封禁，时长由 `tos_temp_ban_time` 控制（默认 300 秒）。
- 具名 hook：`check_temp_ban`、`remove_temp_ban`、`report`、`warning_counts`，供 `abuse` 等模块调用。
