# 权限

本文说明 AkariBot 的权限分层架构与检查机制。

权限分为普通用户、场景管理员、超级用户与基础超级用户四层。模块与命令通过装饰器声明对应权限层级，解析器在匹配模块和执行命令前执行检查。`~auth` 可以将单个模块的超级用户权限授予指定用户。

## 角色

| 角色 | 获得方式 | 判定接口 |
| --- | --- | --- |
| 普通用户 | 默认角色，无需授予 | 无 |
| 场景管理员 | 平台原生管理员、场景自定义管理员，或超级用户 | `msg.check_permission()` |
| 超级用户 | 数据库中的 `SenderUnionInfo.superuser` 标志 | `msg.check_super_user()` |
| 基础超级用户 | `config.toml` 的 `[config].base_superuser` 名单 | `sender_id` 与名单精确匹配 |

`check_permission()` 依次判断场景自定义管理员与超级用户，最后调用适配器平台的 `check_native_permission()`。

### 场景管理员

场景自定义管理员保存在 `TargetUnionInfo.custom_admins`，记录其 Union ID，因此同一用户绑定的多个平台账号共享该权限。管理命令由 `admin` 模块提供：

| 命令 | 说明 |
| --- | --- |
| `~admin add <user>` | 添加场景管理员。目标必须与发送者同平台，已是平台原生管理员时拒绝 |
| `~admin remove <user>` | 移除场景管理员。移除自己时要求确认 |
| `~admin list` | 列出场景自定义管理员 |

`admin` 模块整体声明 `required_admin=True`。自定义名单仅记录非原生管理员。`add` 与 `remove` 仅处理此类管理员，当目标已具备平台原生管理员身份时返回提示。

### 超级用户

超级用户控制机器人本身的行为，权限高于场景管理员。授予与撤销命令由 `superuser` 模块（别名 `su`）提供：

| 命令 | 说明 |
| --- | --- |
| `~superuser add <user>` | 将用户写入数据库，并标记为 `superuser` |
| `~superuser remove <user>` | 清除标志。移除自己时要求确认 |

`<user>` 必须为形如 `QQ|123456` 的完整用户 ID。用户尚未建立记录时，机器人先要求交互确认，再初始化 Union 记录。

<NoticeBox type="danger" title="谨慎授予超级用户">

超级用户可以执行 `~config`、`~eval`、`~restart`、`~module unload` 等高危命令，也可以通过 `~auth` 转授模块权限。该权限仅应授予具备机器人后端与配置合法访问权限的人员。

</NoticeBox>

### 基础超级用户

`base_superuser` 为 `[config]` 表下的用户 ID 列表，也支持配置单个字符串。在 pre-init 阶段，名单中的用户将被解析为 Union 并写入数据库，同时标记为超级用户。`required_base_superuser` 直接比对 `session_info.sender_id` 与配置名单，该名单仅能通过配置文件修改。

## 模块级权限

`module()` 接受以下三个布尔参数，对模块内的全部命令生效：

```python
from akaribot.core.api import module
demo = module("demo", required_admin=True)
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `required_admin` | `False` | 要求场景管理员权限。拒绝执行时提示该场景的管理员 |
| `required_superuser` | `False` | 要求超级用户权限，或持有该模块 `~auth` 授权的用户 |
| `required_base_superuser` | `False` | 要求发送者包含在 `base_superuser` 名单中 |

框架按 `required_base_superuser`、`required_superuser`、`required_admin` 的顺序执行检查，任一项未通过即拒绝执行。命令级权限仅能比模块级更严格。非基础模块仍需要在场景内启用，声明了 `required_superuser` 的模块仅允许超级用户启用。

## 命令级权限

`@module.command()`、`@module.regex()` 接受同名的三个参数，用于给单个命令或正则追加更严格的要求：

```python
@demo.command("export <target>", required_admin=True)
async def _(msg, target: str): ...
```

框架先解析命令模板，再执行命令级检查，最后调用处理函数。单个命令可以提高权限要求，但不可放宽模块级权限限制。

`required_admin=True` 要求场景管理员权限，`required_superuser=True` 要求超级用户权限。命令级权限仅能在模块级权限的基础上提高要求，不可降低限制门槛。

## 模块授权

`auth` 模块让超级用户将单个模块的超级用户权限授予普通用户：

| 命令 | 说明 |
| --- | --- |
| `~auth add <user> <module>` | 授权。要求确认口令，同一授权者重复授权会提示已存在 |
| `~auth remove <user> <module>` | 撤销当前发送者授予的权限 |
| `~auth list <user>` | 列出该用户持有的模块授权 |

授权记录保存在 `SenderUnionInfo.sender_data["module_auth"]` 中，每项包含模块名与授权者 ID。授权仅对声明了 `required_superuser` 的模块生效，`auth add` 将拒绝为其他模块授权。执行授权时可以使用模块别名代替模块名。

授权者不再是超级用户时，其授予的权限自动失效。

## 机器人权限

说明：

- `required_bot_permissions`：启用模块前检查机器人是否具备指定平台权限。
- 机器人缺少必要权限时，模块无法在当前场景启用。

```python
demo = module("demo", required_bot_permissions=["can_manage_messages"])
```

字段名对应 `BotState` 的属性名：

- `available`
- `joined`
- `is_owner`
- `is_admin`
- `can_read_messages`
- `can_read_all_messages`
- `can_send_messages`
- `can_send_proactive_messages`
- `can_manage_messages`
- `can_manage_members`
- `can_restrict_members`
- `can_react`
- `can_send_private_messages`

平台自定义权限写入为 `permissions.<名称>`。

`event` 与 `regex` 模块会自动包含 `can_read_all_messages`。`rss` 模块会自动加入 `can_send_proactive_messages`。

权限检查仅将平台明确返回的 `False` 判定为缺少对应权限。返回 `None` 或状态查询失败时按未知状态处理，并允许继续启用。`~module enable all` 将跳过缺少机器人权限的模块。

## 相关文档

模块声明与命令模板参见[模块开发](module-development.md)。平台权限查询与能力声明参见[适配器开发](adapter-development.md)。内置管理模块参见[内置模块](../../modules/core/docs/index.md)。
