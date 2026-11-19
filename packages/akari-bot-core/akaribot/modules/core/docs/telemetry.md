---
order: 35
submenu: 钩子
---

# telemetry

此 Hook 挂在 `EXECUTION_FINISHED` 和 `FINISHED` 两个位置，统计命令执行与消息解析的次数。

说明：

- 每次执行命令或匹配正则时，`Info.command_parsed` 加一。
- 每条消息解析结束时，`Info.message_parsed` 加一。
- `enable_analytics` 开启时，同时写入 `analytics_data`，记录场景、发送者、命令、模块和模块类型。
- 写入失败时只记录日志，不影响命令收尾。

`enable_analytics` 关闭后不再写入数据表，进程内计数继续累加。
