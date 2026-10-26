# 内置模块

`akaribot.modules.core` 随 `akari-bot-core` 分发，模块清单以
`packages/akari-bot-core/akaribot/modules/core/manifest.toml` 的 `provides_modules` 为准，共 37 个。

## 约定

- 所有内置模块都声明为 `base=True`，在任意场景强制开启，无需 `~module enable`。
- 命令默认以 `~` 或 `～` 开头，前缀可在 `config.toml` 的 `command_prefix` 与场景的 `setup prefix`
  中调整。
- 权限分三级：场景管理员（`required_admin`）、超级用户（`required_superuser`）、基础超级用户
  （`required_base_superuser`）。超级用户可在场景内由 `~superuser add` 授权。
- 隐藏模块（`hidden=True`）不出现在帮助列表，只由 hook、事件或内部调用触发。
- 标为「仅开发模式」的模块只在 `dev_mode` 下注册。

## 分组导航

| 分组 | 模块 | 页面 |
| --- | --- | --- |
| 管理 | `admin`、`mute`、`module`、`auth`、`superuser`、`abuse`、`set`、`purge` | [管理](admin.md) |
| 配置 | `config`、`database`、`eval`、`setup` | [配置](config.md) |
| 解析器 | `parser_errors`、`parser_policies`、`parser_routing`、`tos`、`typo`、`telemetry`、`retired_policy` | [解析器](parser.md) |
| 会话 | `bind`、`merge`、`petal`、`help` | [会话](session.md) |
| 工具 | `about`、`say`、`echo`、`post`、`post-whitelist`、`jobqueue`、`restart`、`update`、`update&restart`、`features`、`analytics`、`url-audit`、`webrender`、`raise` | [工具](tools.md) |

## 模块与命令一览

| 模块 | 主要命令 | 权限 |
| --- | --- | --- |
| `admin` | `add`、`remove`、`list`、`ban`、`unban`、`leave` | 管理员 |
| `mute` | 切换场景静音 | 管理员 |
| `module` | `list`、`enable`、`disable`、`load`、`reload`、`unload` | 管理员 / 超级用户 |
| `auth` | `add`、`remove`、`list` | 超级用户 |
| `superuser` | `add`、`remove` | 超级用户 |
| `abuse` | `check`、`warn`、`revoke`、`clear`、`ban`、`unban`、`trust`、`distrust` 等 | 超级用户 |
| `set` | `target module ...`、`target data ...`、`sender data ...` | 超级用户 |
| `purge` | 清空缓存 | 超级用户 |
| `config` | `get`、`write`、`delete` | 超级用户 |
| `database` | `model`、`field`、`exec` | 超级用户，仅开发模式 |
| `eval` | 执行表达式 | 超级用户，仅开发模式 |
| `setup` | `typing`、`check`、`list`、`prefix`、`locale`、`alias` 等 | 按子命令 |
| `bind` | 绑定码、`self`、`target`、`channel`、`whoami` | 按子命令 |
| `help` | 模块列表与详情 | 所有人 |
| `petal` | 花瓣查询、签到、转账 | 按子命令 |
| `about` | 版本、状态、制作人员 | 所有人 |
| `say`、`echo` | 复述消息 | 超级用户 |
| `post` | 定向与全局推送 | 超级用户 |
| `restart` | 重启进程 | 超级用户 |
| `update`、`update&restart` | 委托 CLI 更新 | 超级用户 |
| `analytics` | 使用统计 | 超级用户 |
| `url-audit` | URL 允许与阻止列表 | 超级用户 |
| `webrender` | 渲染服务状态与控制 | 超级用户 |

## 相关文档

模块框架本身（`module()`、命令模板、权限模型）见[模块开发](../../../core/doc/module-development.md)；
内置模块使用的配置、数据库与本地化机制见[配置](../../../core/doc/config.md)、
[数据库](../../../core/doc/database.md) 与 [本地化](../../../core/doc/i18n.md)。
