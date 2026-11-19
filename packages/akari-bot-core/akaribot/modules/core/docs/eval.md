---
order: 23
---

# eval

此模块仅在开发模式下加载，可以执行 Python 表达式。模块级权限为超级用户。

### `eval`

<CommandUsage usage="eval <expr>" :params="['expr=要执行的 Python 表达式']" permission="superuser" />

此命令在包含 `msg` 和 `Bot` 的命名空间中执行表达式。结果以纯文本返回，不经过敏感内容检查。表达式抛出异常时，异常会被包装成 `NoReportException` 后回显，不进入错误上报流程。
