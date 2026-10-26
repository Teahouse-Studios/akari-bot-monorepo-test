# 配置

本组包含配置维护与场景设置：`config`、`database`、`eval`、`setup`。前三个面向超级用户，`setup` 面向
普通用户与场景管理员。

## config

模块级权限为超级用户，别名 `cfg`。

| 命令 | 说明 |
| --- | --- |
| `~config get <k> [<table_name>]` | 读取配置项 |
| `~config write <k> <v> [<table_name>] [-s]` | 写入配置项 |
| `~config delete <k> [<table_name>]` | 删除配置项 |

- `write` 把 `true`、`false` 转为布尔值，整数与浮点转为对应数值，`[...]` 形式按 JSON 解析为列表，其余
  按字符串写入。
- `-s` 表示按密钥项处理：核心配置写入 `[secret]`，平台与模块配置写入对应的 `_secret` 表。
- 新增尚不存在的键会改变配置文件结构，执行前要求确认。
- 表名为 `bot_<平台>`、`module_<模块>` 等，省略时在 `config.toml` 的表内查找。
- 配置为只读的进程不能直接写入，该命令经 `CFGManager.edit_write()` 与 `edit_delete()` 授权执行。

字段布局、只读约束与版本机制见[配置](../../../core/doc/config.md)。

## setup

模块为基础模块，别名 `toggle`、`prefix`、`locale`、`lang`、`alias` 分别指向对应子命令。命令同时作用于
场景域与个人域，`~setup list` 可查看全部设置项。

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~setup typing` | 所有人 | 切换「正在输入」提示 |
| `~setup check` | 所有人 | 切换命令拼写检查 |
| `~setup markdown` | 所有人 | 切换 Markdown 渲染，需平台支持 |
| `~setup dark` | 所有人 | 切换暗色模式 |
| `~setup list [target|sender]` | 所有人 | 展示设置面板；修改入口按管理员权限显示 |
| `~setup prefix list` | 所有人 | 列出默认前缀与场景自定义前缀 |
| `~setup prefix add <prefix>` | 管理员 | 增加场景命令前缀 |
| `~setup prefix remove <prefix>` | 管理员 | 移除场景命令前缀 |
| `~setup prefix reset` | 管理员 | 清空场景自定义前缀 |
| `~setup locale` | 所有人 | 展示可用语言 |
| `~setup locale <lang>` | 管理员 | 设置场景语言 |
| `~setup locale reload` | 超级用户 | 重新加载语言文件 |
| `~setup alias list [--legacy]` | 所有人 | 列出场景自定义命令别名 |
| `~setup alias add <alias> <command>` | 管理员 | 增加别名，替换文本须以命令前缀开头 |
| `~setup alias remove <alias>` | 管理员 | 移除别名 |
| `~setup alias reset` | 管理员 | 清空别名 |
| `~setup timeoffset <offset>` | 管理员 | 设置场景时区偏移，如 `8`、`-5:30` |
| `~setup cooldown <second>` | 管理员 | 设置命令冷却秒数，负数按 0 处理 |
| `~setup invalid-module-prompt` | 管理员 | 切换未知模块的提示 |
| `~setup sign` | 管理员 | 切换签到开关，仅在 `enable_petal` 时注册 |
| `~setup emote` | 管理员 | 切换表情开关，仅在 `use_emote` 时注册 |

别名支持 `${名称}` 占位符，按占位符数量选择最长匹配；`--legacy` 以文本表格代替图片。

## 数据键

`setup` 与 `set` 改写的键存放在 union 的 JSON 列：

| 域 | 键 | 用途 |
| --- | --- | --- |
| 场景 | `command_prefix` | 自定义命令前缀 |
| 场景 | `command_alias` | 自定义命令别名 |
| 场景 | `cooldown_time` | 命令冷却秒数 |
| 场景 | `timezone_offset` | 时区偏移 |
| 场景 | `invalid_module_prompt` | 未知模块提示开关 |
| 场景 | `use_emote` | 表情开关 |
| 场景 | `petal_sign` | 签到开关 |
| 个人 | `typing_prompt` | 输入状态提示 |
| 个人 | `typo_check` | 拼写检查 |
| 个人 | `use_markdown` | Markdown 渲染 |
| 个人 | `dark_mode` | 暗色模式 |

## database

仅在开发模式加载，模块级权限为超级用户，别名 `db`。

| 命令 | 说明 |
| --- | --- |
| `~database model` | 列出全部表 |
| `~database field <model> [--legacy]` | 列出表的字段、类型与可空性 |
| `~database exec <sql> [-p <page>] [--legacy]` | 执行 SQL，按每页 10 行展示结果 |

`--legacy` 以文本表格输出，否则优先渲染为图片。该模块直接操作数据库，仅用于调试与排障。

## eval

仅在开发模式加载，模块级权限为超级用户。

| 命令 | 说明 |
| --- | --- |
| `~eval <expr>` | 在包含 `msg` 与 `Bot` 的命名空间中执行表达式 |

结果以纯文本返回并跳过敏感内容检查；异常包装为 `NoReportException` 后回显，不进入错误上报流程。
