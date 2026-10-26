# 权限

AkariBot 的权限分为普通用户、场景管理员、超级用户与基础超级用户四层。模块和命令通过装饰器声明
所需层级，parser 在模块路由与命令执行前依次检查；`~auth` 可以在模块级把超级用户权限授予单个用户。

## 角色

| 角色 | 获得方式 | 判定接口 |
| --- | --- | --- |
| 普通用户 | 默认角色，无需授予 | 无 |
| 场景管理员 | 平台原生管理员、场景自定义管理员，或超级用户 | `msg.check_permission()` |
| 超级用户 | 数据库中的 `SenderUnionInfo.superuser` 标志 | `msg.check_super_user()` |
| 基础超级用户 | `config.toml` 的 `[config].base_superuser` 名单 | `sender_id` 与名单精确匹配 |

`check_permission()` 依次判断发送者是否为场景自定义管理员、超级用户，最后请求平台的
`check_native_permission()`。

### 场景管理员

场景自定义管理员存放在 `TargetUnionInfo.custom_admins`，记录 union ID，因此同一用户绑定的多个
平台账号共享权限。管理命令由 `admin` 模块提供：

| 命令 | 说明 |
| --- | --- |
| `~admin add <user>` | 添加场景管理员；目标须与发送者同平台，已是平台原生管理员时拒绝 |
| `~admin remove <user>` | 移除场景管理员；移除自己时要求确认 |
| `~admin list` | 列出场景自定义管理员 |

`admin` 模块整体声明 `required_admin=True`；平台原生管理员不写入自定义名单，`add` 与 `remove`
遇到原生管理员会直接提示无需操作。

### 超级用户

超级用户控制机器人本身的行为，权限高于场景管理员。授予与撤销由 `superuser` 模块（别名 `su`）提供：

| 命令 | 说明 |
| --- | --- |
| `~superuser add <user>` | 将用户写入数据库并置位 `superuser` |
| `~superuser remove <user>` | 清除标志；移除自己时要求确认 |

`<user>` 必须是形如 `QQ|123456` 的完整用户 ID；用户尚未建立记录时会先要求确认并初始化 union。

<NoticeBox type="danger" title="谨慎授予超级用户">
超级用户可以执行 `~config`、`~eval`、`~restart`、`~module unload` 等高危命令，也能通过 `~auth`
转授模块权限。只应向能够合法访问机器人后端与配置的人授予。
</NoticeBox>

### 基础超级用户

`base_superuser` 是 `[config]` 表下的用户 ID 列表，也接受单个字符串。pre-init 阶段会把名单中的
用户解析为 union 并写入数据库，同时置位超级用户；`required_base_superuser` 则直接比较
`session_info.sender_id` 与配置名单。名单只能通过配置文件维护。

## 模块级权限

`module()` 接受三个布尔参数，作用于模块内全部命令：

```python
from akaribot.core.api import module
demo = module("demo", required_admin=True)
```

| 参数 | 默认 | 作用 |
| --- | --- | --- |
| `required_admin` | `False` | 要求场景管理员；拒绝时提示该场景的管理员 |
| `required_superuser` | `False` | 要求超级用户，或持有该模块 `~auth` 授权的用户 |
| `required_base_superuser` | `False` | 要求发送者在 `base_superuser` 名单中 |

检查顺序为 `required_base_superuser`、`required_superuser`、`required_admin`，命中即拒绝，模块级
要求无法被命令放宽。非基础模块还需在场景内启用，声明 `required_superuser` 的模块只有超级用户能启用。

## 命令级权限

`@module.command()`、`@module.regex()` 接受同名的三个参数，用于在模块级要求之上进一步收紧单个
组件：

```python
@demo.command("export <target>", required_admin=True)
async def _(msg, target: str): ...
```

命令级检查发生在模板解析之后、函数调用之前。由于只能收紧、不能放宽，模块已声明
`required_superuser` 时，单个命令再声明 `required_admin` 不会降低门槛。`~auth` 的授权对模块内的
全部命令生效，不区分具体组件。

## 模块授权

`auth` 模块让超级用户把某个模块的超级用户权限授予普通用户，而不必提升为全局超级用户：

| 命令 | 说明 |
| --- | --- |
| `~auth add <user> <module>` | 授权；要求确认口令，同一授权者重复授权会提示已存在 |
| `~auth remove <user> <module>` | 撤销当前发送者给出的授权 |
| `~auth list <user>` | 列出该用户持有的模块授权 |

授权记录写在 `SenderUnionInfo.sender_data["module_auth"]`，每项包含模块名与授权者 ID。授权只对
声明了 `required_superuser` 的模块有效，`auth add` 会拒绝其他模块；模块别名同样命中。授权者不再是
超级用户时，其给出的授权自动失效。`auth` 模块本身要求超级用户权限。

## 机器人权限

`required_bot_permissions` 与用户角色无关，它约束机器人在场景中必须具备的平台权限，在
`~module enable` 时检查：

```python
demo = module("demo", required_bot_permissions=["can_manage_messages"])
```

字段取 `BotState` 的属性名，例如 `can_read_all_messages`、`can_send_messages`、
`can_send_proactive_messages`、`can_manage_messages`、`can_manage_members`、
`can_restrict_members`、`can_react`；平台自定义权限写成 `permissions.<名称>`。`event` 与 `regex`
模块自动追加 `can_read_all_messages`，`rss` 模块自动追加 `can_send_proactive_messages`。

检查只把平台明确返回的 `False` 视为缺失；`None` 与状态查询失败都不会阻止启用，避免把临时的 RPC
错误误报为权限不足。`~module enable all` 会跳过缺少机器人权限的模块。

## 相关文档

模块声明与命令模板见[模块开发](module-development.md)，平台权限查询与能力声明见
[适配器开发](adapter-development.md)，内置管理模块见[内置模块](../../modules/core/doc/index.md)。
