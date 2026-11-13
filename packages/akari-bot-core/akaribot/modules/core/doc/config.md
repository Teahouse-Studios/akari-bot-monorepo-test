---
order: 20
---

# config

<ModuleAlias names="cfg" />

此模块可以读取、写入和删除配置项。模块级权限为超级用户。

### `config get`

<CommandUsage usage="config get <k> [<table_name>]" :params="['k=配置项键名', 'table_name=配置表名，省略时查主表']" permission="superuser" />

读取配置项的值。省略表名时，命令在 `config.toml` 的主表内查找。

<ChatExample
  :log="[
    '用户：~config get auto_purge_crontab',
    '机器人：0 0 * * *',
  ]"
/>

### `config write`

<CommandUsage usage="config write <k> <v> [<table_name>] [-s]" :params="['k=配置项键名', 'v=配置值，按类型解析', 'table_name=配置表名，省略时写主表']" permission="superuser" :options="[{flag: '-s', desc: '是否为密钥配置项'}]" />

写入配置项。配置值按类型解析，`true` 和 `false` 转为布尔值，整数与浮点数转为对应数值。以 `[...]` 写出的值按 JSON 解析为列表，其余内容按字符串写入。`-s` 表示按密钥项处理，核心配置写入 `[secret]`，平台和模块配置写入对应的 `_secret` 表。

写入尚不存在的键会改变配置文件的结构，此时命令会在执行前要求确认。

<ChatExample
  :log="[
    '用户：~config write enable_joke false',
    '机器人：成功。',
  ]"
/>

### `config delete`

<CommandUsage usage="config delete <k> [<table_name>]" :params="['k=配置项键名', 'table_name=配置表名，省略时查主表']" permission="superuser" />

删除配置项。执行时调用 `CFGManager.edit_delete()`，返回成功或失败。

表名形如 `bot_<平台>`、`module_<模块>`。配置只读时，进程不能直接修改配置文件，写入改用 `CFGManager.edit_write()`，删除改用 `edit_delete()`。字段布局、只读限制和版本机制见[配置](../../../core/doc/config.md)。

<ChatExample
  :log="[
    '用户：~config delete enable_joke',
    '机器人：成功。',
  ]"
/>
