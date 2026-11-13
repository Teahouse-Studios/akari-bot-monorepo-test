---
order: 22
---

# database

<ModuleAlias names="db" />

仅在开发模式加载，模块级权限为超级用户。该模块直接操作数据库，用于调试与排障。

### `database model`

<CommandUsage usage="database model" permission="superuser" />

列出核心与各模块注册的数据表名。

### `database field`

<CommandUsage usage="database field <model> [--legacy]" :params="['model=数据表名']" permission="superuser" :options="[{flag: '--legacy', desc: '强制使用文本模式'}]" />

列出表的字段、类型与可空性。默认渲染为图片表格，`--legacy` 或平台不支持图片时改用文本表格；表名不存在时返回无结果提示。

### `database exec`

<CommandUsage usage="database exec <sql> [-p <page>] [--legacy]" :params="['sql=要执行的 SQL 语句', 'page=结果页码，每页 10 行']" permission="superuser" :options="[{flag: '-p', desc: '指定页码，每页 10 行'}, {flag: '--legacy', desc: '强制使用文本模式'}]" />

执行 SQL 语句。`SELECT` 查询按每页 10 行展示，页码超出范围时取最近的有效页；其它语句直接执行并返回影响行数。默认渲染为图片表格，`--legacy` 或平台不支持图片时改用文本表格。
