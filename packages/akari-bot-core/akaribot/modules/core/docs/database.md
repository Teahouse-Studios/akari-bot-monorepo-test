---
order: 22
---

# database

<ModuleAlias names="db" />

此模块用于调试与排查故障，可以直接操作数据库，仅在开发模式下加载。模块级权限为超级用户。

### `database model`

<CommandUsage usage="database model" permission="superuser" />

列出 core 与各模块注册的数据表名称。

### `database field`

<CommandUsage usage="database field <model> [--legacy]" :params="['model=数据表名']" permission="superuser" :options="[{flag: '--legacy', desc: '强制使用文本模式'}]" />

列出每个字段的名称、类型以及是否可以为空。

默认渲染为图片表格。平台不支持图片或指定 `--legacy` 时，使用文本表格呈现。表名称不存在时返回无结果提示。

### `database exec`

<CommandUsage usage="database exec <sql> [-p <page>] [--legacy]" :params="['sql=要执行的 SQL 语句', 'page=结果页码，每页 10 行']" permission="superuser" :options="[{flag: '-p', desc: '指定页码，每页 10 行'}, {flag: '--legacy', desc: '强制使用文本模式'}]" />

执行 SQL 语句。`SELECT` 查询按每页 10 行展示，页码超出范围时使用最接近的有效页码。其他语句直接执行，返回受影响的行数。

默认渲染为图片表格。平台不支持图片或指定 `--legacy` 时，使用文本表格呈现。
