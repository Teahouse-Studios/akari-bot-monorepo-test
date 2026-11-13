---
order: 32
submenu: 钩子
---

# parser_errors

此模块用于统一处理命令与正则表达式抛出的异常。各类异常对应的反馈如下：

| 异常 | 反馈 |
| --- | --- |
| `NoReportException` | 回显异常文本，不进入上报流程 |
| `ExternalException` | 回显异常文本与外部错误说明 |
| `AbuseWarning` | 回显提示与拒绝原因，不进入上报流程 |
| `SendMessageFailed` | 触发平台错误提示与限流文案 |
| 其它异常 | 回显错误详情、上报场景与问题反馈地址，并发送错误报告 |

错误详情按平台能力渲染。支持 Markdown 时使用 Markdown 代码块，否则按纯文本解析。启用表情且平台支持图片时，还会附带随机表情。

上报通过 `send_report()` 发送到 `report_targets`，同时写入 SMTP 报告（若启用）。

模块还提供一个带名称的 Hook `format_error_detail`，RPC 的错误报告复用同一套格式化逻辑。
