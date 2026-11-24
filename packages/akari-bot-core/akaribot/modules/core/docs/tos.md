---
order: 33
submenu: 钩子
---

# tos

此 Hook 基于令牌桶算法限制命令与正则表达式的调用频率。超出限制后，机器人将临时限制该发送者。

说明：

- 配置项包括 `enable_tos`、`tos_warning_counts`、`tos_temp_ban_time` 与 `report_targets`。
- 机器人在 `COMMAND_BEFORE_PARSE` 与 `REGEX_BEFORE_EXECUTE` 阶段计数，在 `COMMAND_PREPARE` 与 `REGEX_PREPARE` 阶段检查发送者是否处于临时限制状态。
- `EXECUTION_ERROR` 捕获 `AbuseWarning`。警告次数超过 `tos_warning_counts` 后，机器人将临时限制该发送者，限制时长通过 `tos_temp_ban_time` 控制，默认 300 秒。
- 模块提供命名 Hook（`check_temp_ban`、`remove_temp_ban`、`report` 与 `warning_counts`），供 `abuse` 等模块调用。
