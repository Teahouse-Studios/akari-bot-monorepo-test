---
order: 23
---

# eval

仅在开发模式加载，模块级权限为超级用户。

### `eval`

<CommandUsage usage="eval <expr>" :params="['expr=要执行的 Python 表达式']" permission="superuser" />

在包含 `msg` 与 `Bot` 的命名空间中执行表达式。结果以纯文本返回并跳过敏感内容检查；异常包装为 `NoReportException` 后回显，不进入错误上报流程。
