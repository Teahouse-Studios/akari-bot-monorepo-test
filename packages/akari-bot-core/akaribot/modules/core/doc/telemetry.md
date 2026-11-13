---
order: 35
submenu: 钩子
---

# telemetry

在 `EXECUTION_FINISHED` 与 `FINISHED` 入口统计：

- 每次命令或正则执行递增 `Info.command_parsed`。
- 每条消息解析结束递增 `Info.message_parsed`。
- `enable_analytics` 开启时写入 `analytics_data`，记录场景、发送者、命令、模块与模块类型。
- 写入失败只记录日志，不影响命令收尾。

配置 `enable_analytics` 关闭后停止写表，进程内计数继续累加。
