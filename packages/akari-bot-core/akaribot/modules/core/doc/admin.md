# 管理

本组包含场景管理与权限维护命令：`admin`、`mute`、`module`、`auth`、`superuser`、`abuse`、`set`、`purge`。

## admin

模块级权限为场景管理员，别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应子命令。

| 命令 | 说明 |
| --- | --- |
| `~admin add <user>` | 将用户加入本场景管理员 |
| `~admin remove <user>` | 移除场景管理员；移除自己需二次确认 |
| `~admin list` | 列出场景管理员 |
| `~admin ban <user>` | 禁止用户在本场景使用机器人 |
| `~admin unban <user>` | 解除禁止 |
| `~admin ban list` | 列出被禁止的用户 |
| `~admin leave` | 让机器人退出当前群，仅 `QQ|Group` |

`<user>` 必须是带平台前缀的完整 ID（如 `QQ|123456`），否则提示先用 `~whoami` 查询。目标用户的
平台原生管理员身份不能被 `add` 或 `remove` 覆盖；封禁与管理员列表存储的是 union ID，因此同一用户
在绑定后的其它平台账号一并生效。

## mute

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~mute` | 管理员 | 切换本场景静音 |

静音场景中除 `~mute` 外的命令与正则都不执行；对静音场景的主动推送同样被抑制。解除静音需要再次
执行 `~mute`。

## module

| 命令 | 权限 | 说明 |
| --- | --- | --- |
| `~module list [--legacy] [--img]` | 所有人 | 列出模块及启用状态；`--img` 强制图片输出 |
| `~module enable <module>...` | 管理员 | 在场景内启用模块，同时提示推荐模块 |
| `~module enable all` | 管理员 | 启用全部可启用模块 |
| `~module disable <module>...` | 管理员 | 在场景内停用模块 |
| `~module disable all` | 管理员 | 停用全部可停用模块 |
| `~module load <module>...` | 超级用户 | 全域加载模块 |
| `~module reload <module>...` | 超级用户 | 热重载模块及其依赖闭包 |
| `~module unload <module>...` | 超级用户 | 全域卸载模块 |

`enable all` 与 `disable all` 跳过基础模块、隐藏模块与仅超级用户可用的模块。启用前会检查平台能力
（正则、事件、RSS）与机器人权限，缺失时给出具体原因。别名 `enable`、`disable`、`load`、`reload`、
`unload` 可省略 `module`。

## auth

| 命令 | 说明 |
| --- | --- |
| `~auth add <user> <module>` | 授权用户执行指定模块的超级用户命令 |
| `~auth remove <user> <module>` | 撤销授权 |
| `~auth list <user>` | 列出用户获得的授权 |

只对声明了 `required_superuser` 的模块生效。授权记录同时保存授权者，授权者失去超级用户身份后该条
授权不再生效。

## superuser

| 命令 | 说明 |
| --- | --- |
| `~superuser add <user>` | 将用户设为超级用户，别名 `~su add` |
| `~superuser remove <user>` | 取消超级用户 |

`config.toml` 的 `base_superuser` 在启动时写入数据库，属于基础超级用户，只能通过配置维护。

## abuse

模块级权限为超级用户，别名 `ae`。

| 命令 | 说明 |
| --- | --- |
| `~abuse check <user>` | 查看警告次数、临时封禁与黑白名单状态 |
| `~abuse warn <user> [<count>]` | 增加警告次数 |
| `~abuse revoke <user> [<count>]` | 减少警告次数 |
| `~abuse clear <user>` | 清零警告次数 |
| `~abuse untempban <user>` | 解除临时封禁 |
| `~abuse ban <user>` / `unban <user>` | 加入或移出黑名单 |
| `~abuse trust <user>` / `distrust <user>` | 加入或移出白名单 |
| `~abuse block <target>` / `unblock <target>` | 屏蔽场景，仅 `QQ` |

警告累计到 `tos_warning_counts` 会触发临时封禁，时长由 `tos_temp_ban_time` 控制，见[解析器](parser.md)。

## set

模块级权限为超级用户，直接改写目标场景或用户的数据，参数中的 ID 必须带平台前缀。

| 命令 | 说明 |
| --- | --- |
| `~set target module enable <target> <modules>...` | 在目标场景启用模块 |
| `~set target module disable <target> <modules>...` | 在目标场景停用模块 |
| `~set target module list <target>` | 列出目标场景已启用模块 |
| `~set target data get <target> [<k>]` | 读取场景数据，省略键时列出全部 |
| `~set target data edit <target> <k> <v>` | 写入场景数据 |
| `~set target data delete <target> <k>` | 删除场景数据键 |
| `~set sender data get <user> [<k>]` | 读取用户数据 |
| `~set sender data edit <user> <k> <v>` | 写入用户数据 |
| `~set sender data delete <user> <k>` | 删除用户数据键 |

目标场景不存在时需要确认后创建。场景数据键如 `command_prefix`、`cooldown_time`，用户数据键如
`typing_prompt`、`module_auth`。

## purge

| 命令 | 说明 |
| --- | --- |
| `~purge` | 清空实例 `cache/` 目录 |

同一模块注册了按 `auto_purge_crontab`（默认 `0 0 * * *`）执行的定时清理，命令与定时任务都直接删除
缓存目录内容，不触碰 `data/` 与数据库。
