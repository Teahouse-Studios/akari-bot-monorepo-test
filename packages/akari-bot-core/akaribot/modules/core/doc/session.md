# 会话

本组处理场景与身份的绑定、旧客户端迁移、花瓣积分与帮助：`bind`、`merge`、`petal`、`help`。

## bind

基础模块，负责把不同平台上的同一用户、同一现实场景归入同一个 union。别名 `whoami`、`merge`、
`merge token` 指向对应子命令。

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~bind` | 所有人 | 查看当前用户与场景的 union 及已绑定 ID |
| `~bind whoami` | 所有人 | 显示平台 ID、union ID 与权限身份 |
| `~bind self` | 所有人 | 列出当前用户绑定的全部账号 |
| `~bind start` | 私聊所有人；群内管理员 | 生成绑定码 |
| `~bind token <code>` | 私聊所有人；群内管理员 | 用绑定码完成绑定 |
| `~bind self remove <user>` | 所有人 | 解绑账号，最后一个账号不可解绑 |
| `~bind target` | 管理员 | 查看场景绑定的平台入口 |
| `~bind target remove <target>` | 管理员 | 解绑场景入口，最后一个入口不可解绑 |
| `~bind channel` | 管理员 | 查看当前场景的消息通道 |
| `~bind channel set <channel>` | 管理员 | 设置消息通道号 |
| `~bind channel reset` | 管理员 | 重置消息通道号 |

- 绑定码为 6 位大写字母与数字，有效期 300 秒，只保存在 Server 进程内存中，重启即失效。
- 私聊中生成的码同时包含用户与私聊场景，兑换后两者一并绑定；群内绑定只合并场景组。
- 绑定码的使用场景必须与生成场景同属私聊或群聊，跨类型兑换会被拒绝。
- `enable_bind_auto` 开启时额外注册 `~bind auto`、`~bind channel probe`、`~bind channel confirm`，
  用于同一场景内多个机器人实例的自动配对。

场景数据中的 `command_prefix`、`command_alias` 与场景 union 一起迁移，绑定后由合并结果统一维护。

## merge

隐藏模块，仅在 `retired_clients` 非空时加载。命令注册在 `bind` 上，模块本身只承载退役公告的正则
触发器。

| 命令 | 平台 | 说明 |
| --- | --- | --- |
| `~bind merge` | 退役来源客户端 | 在旧客户端上生成迁移码 |
| `~bind merge-token <code>` | 目标客户端 | 在新客户端兑换迁移码，合并用户与场景数据 |

迁移码与绑定码分开存放，互不消费。迁移会改写模块表中以平台 ID 为主键的数据，并同步场景管理员、
封禁列表与消息通道。`retired_clients` 的格式为 `<源客户端> -> <目标客户端>`，只写源客户端表示
不提供迁移，此时不注册迁移命令，仅保留退役公告。

## petal

花瓣为跨平台积分，仅在 `enable_petal` 为真时加载。

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~petal` | 所有人 | 查询自己的花瓣 |
| `~petal sign` | 所有人 | 每日签到，场景可用 `~setup sign` 关闭 |
| `~petal give <petal> <user>` | 所有人 | 向同一客户端的用户转账，需确认 |
| `~petal [<user>]` | 超级用户 | 查询指定用户花瓣 |
| `~petal modify <petal> [<user>]` | 超级用户 | 增减花瓣 |
| `~petal clear [<user>]` | 超级用户 | 清零花瓣 |
| `~petal bud send <petal> <count> <passcode>` | 所有人 | 发放花瓣红包 |
| `~petal bud <passcode>` | 所有人 | 领取红包 |
| `~petal bud info <id>` | 所有人 | 查看红包详情 |
| `~petal bud release` | 超级用户 | 退回未领取的红包 |

相关配置：`enable_get_petal`、`petal_gained_limit`、`petal_lost_limit`、`petal_sign_min`、
`petal_sign_max`、`petal_sign_rate`、`petal_rebate_rate`、`petal_reset_crontab`。定时任务按
`petal_reset_crontab`（默认每月 1 日 `0 0 1 * *`）结算花瓣。转账与红包要求目标用户属于同一客户端，
避免跨平台刷取。

## help

基础模块，输出模块清单与命令帮助。

| 命令 | 说明 |
| --- | --- |
| `~help [--legacy] [--img]` | 按场景可用模块列出清单与启用状态 |
| `~help <module> [--legacy] [--img]` | 展示模块简介与命令模板 |

- 帮助只列出当前平台可用且已加载的模块；`hidden=True` 的模块不出现。
- 超级用户命令对非超级用户隐藏，管理员命令对普通成员隐藏。
- 场景可通过按钮或 `~enable <module>` 打开未启用模块。
- `--img` 优先渲染图片，渲染不可用时回退文本；`--legacy` 强制文本表格。
- 清单中的模块顺序与启用状态取自场景的 `modules` 列，基础模块始终显示为已启用。

模块的帮助文案来自命令模板末尾的 `{{I18N:key}}`；模块简介来自 `module(desc=...)`。
