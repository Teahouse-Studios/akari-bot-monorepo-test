---
order: 35
submenu: 钩子
---

# telemetry

此 Hook 挂载在 `EXECUTION_FINISHED` 与 `FINISHED` 两个位置，用于统计命令执行与消息解析的次数。

说明：

- 每次执行命令或匹配正则表达式时，`Info.command_parsed` 加一。
- 每条消息解析结束时，`Info.message_parsed` 加一。
- 若 `enable_analytics` 处于开启状态，同时写入 `analytics_data`，记录场景、发送者、命令、模块和模块类型。
- 若写入失败，仅记录日志，命令仍然正常结束。

若 `enable_analytics` 处于关闭状态，不再向数据表写入记录，进程内计数则继续累加。
