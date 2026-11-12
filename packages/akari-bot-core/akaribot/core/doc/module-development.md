# 模块开发

模块包以独立分发包发布，经 entry point `akaribot.modules` 发现，只导入 `akaribot.core.api` 的公共面。

## 包结构

```text
akari-bot-module-<name>/
  pyproject.toml
  akaribot/modules/<name>/
    __init__.py         module() 声明与组件
    config.py           @on_module_config 配置模板，可选
    database/models.py  数据模型，可选
    locales/zh_cn.json  文案与配置注释
    manifest.toml       包元数据
```

```toml
# pyproject.toml
dependencies = ["akari-bot-core>=0.1.0,<1.0"]

[project.entry-points."akaribot.modules"]
dice = "akaribot.modules.dice"

# manifest.toml
schema = 1
requires_core_api = ">=1,<2"
config_table = "module_dice"
provides_modules = ["dice"]
```

清单字段：

| 字段 | 说明 |
| --- | --- |
| `schema` | 清单结构版本，当前为 `1` |
| `requires_core_api` | 核心 API 兼容区间，默认 `>=1,<2` |
| `locales`、`assets` | 语言文件与资源目录，默认 `locales`；相对导入包目录解析 |
| `migrations`、`config_migrations` | 数据库迁移与配置迁移目录 |
| `config_table`、`config_schema_version` | 配置表名；新生成配置写入的结构版本，默认 `1` |
| `provides_modules` | 分发包提供的模块名 |
| `owned_tables` | 数据清理时归属本包的表 |
| `credential_fields` | 启动前用于多实例查重的凭据字段 |

未识别的键只记录告警，不影响加载。

## 发现与加载

`PackageRegistry` 读取已安装分发的 entry points，`load_order()` 按依赖关系给出激活顺序；模块只依赖 `akaribot.core.api` 的公共面，包之间不直接导入。目录扫描仅在分发缺少 entry point 时兜底。

安装、卸载与重载在 JobQueue 排空与 Scheduler 维护窗口内完成：按稳定 ID 替换注册项，等待在途任务退出后生效。加载失败原因写入 `.cache_loader`，`~module reload` 返回 `(状态, 重载次数)`，失败时状态为假。

## 声明模块

```python
from akaribot.core.api import Bot, I18NContext, module

dice = module("dice", alias=["rd", "roll"], desc="{I18N:dice.help.desc}", doc=True)
```

| 参数 | 说明 |
| --- | --- |
| `module_name` | 命令首词，同时作为模块标识 |
| `alias` | 别名，可传字符串、列表或 `{别名: 完整命令}` 映射 |
| `desc` / `doc` / `hidden` | 帮助简介、线上说明与隐藏开关 |
| `recommend_modules` / `base` / `load` | 推荐模块、强制开启与加载开关 |
| `rss` / `regex` / `event` | 声明所需平台能力，决定模块能否在该场景启用 |
| `required_admin` / `required_superuser` / `required_base_superuser` | 模块级权限 |
| `required_bot_permissions` | 开启前要求机器人具备的平台权限 |
| `suppress_invalid_prompt` / `available_for` / `exclude_from` | 提示开关与平台范围 |

## 命令

```python
@dice.command("<dices> [<dc>] {{I18N:dice.help}}")
async def _(msg: Bot.MessageSession, dices: str, dc: int | None = None):
    await msg.finish(I18NContext("dice.message.result", dices=dices))
```

- `<name>`：位置参数，对应同名函数参数；缺席时使用默认值或 `None`。
- `[flag]`：标志选项，标注为 `bool` 的函数参数直接得到真假。
- `[-b]`、`[--foo <bar>]`：带杠选项，下划线按连字符匹配；仅一个子参数时直接传入子参数值，`[-p <page>]` 也可直接使用子参数名 `page`；无法作参数名的元素用 `Param` 标注。
- 模板末尾的 `{{I18N:key}}` 是帮助文案，不参与解析。

`int`、`float`、`bool` 参数按标注转换。一个命令可注册多个模板，命中任一即可；`priority` 越大越先匹配。

解析结果写入 `parsed_msg`：位置参数以模板中的参数名为键，带杠选项归入选项名，选项名接受 `-l` 与 `--l` 两种写法，并做下划线到连字符的映射。函数中注解为 `Bot.MessageSession` 的参数由框架注入，其余参数按名从 `parsed_msg` 取值；转换失败抛出 `InvalidCommandFormatError`。

## 正则与定时任务

```python
@dice.regex(r"^roll (\d+)$", mode="M", show_typing=False)
async def _(msg: Bot.MessageSession):
    count = int(msg.matched_msg.group(1))


@dice.schedule(CronTrigger.from_crontab("0 4 * * *"))
async def _daily(): ...
```

正则选项包括 `flags`、`desc`、`logging`、`show_typing`、`text_only`、`element_filter`、`trigger_once_startup`、`skip_long_message_confirm`。定时任务接受 `CronTrigger`、`DateTrigger`、`IntervalTrigger` 及 `And`、`Or` 组合，`IntervalTrigger` 的间隔按 `schedule_interval_multiplier` 缩放。模块未加载时其命令、正则与计划任务都不执行；非基础模块在场景未启用时，命令与正则在 `parser_policies` 的模块路由阶段被拦截。

## Hook 与事件

```python
from akaribot.core.api import HookPoint

@dice.hook(point=HookPoint.COMMAND_UNMATCHED, priority=50, name="suggest")
async def _(ctx): ...
```

- `point` 取 `HookPoint` 常量；`priority` 升序执行，默认 100；`timeout` 默认 5 秒，`<=0` 不限时。
- `server_scope=True` 不受场景模块开关限制，仍遵守全局停用与平台约束。
- 具名 hook 由 `Bot.Hook.trigger("名称", ...)` 调用；`@dice.event("name")` 绑定平台事件。

`HookPoint` 覆盖消息生命周期：`SESSION_READY`、`SESSION_BEFORE_WAIT`、`MESSAGE_NORMALIZED`、`COMMAND_PREPARE`、`COMMAND_BEFORE_PARSE`、`COMMAND_BEFORE_EXECUTE`、`COMMAND_ROUTE`、`COMMAND_UNMATCHED`、`REGEX_ROUTE`、`REGEX_CANDIDATE`、`CHANNEL_CLAIM`、`REGEX_PREPARE`、`REGEX_BEFORE_EXECUTE`、`EXECUTION_FINISHED`、`EXECUTION_ERROR`、`FINISHED`、`OUTGOING_BEFORE_SEND`、`OUTGOING_SENT`、`OUTGOING_FAILED`。路由与候选阶段的 hook 返回 `Stop` 可终止后续处理。

具名钩子按 `模块名.钩子名` 注册。`Bot.Hook.trigger("模块.钩子")` 只调用该模块的回调；名称不带点时广播给同名钩子，单个回调失败记录后继续。

## 权限

模块级 `required_*` 对所有命令生效，命令级参数可进一步收紧。运行期用 `await msg.check_permission()` 判断场景管理员，`msg.check_super_user()` 判断超级用户。基础模块强制开启；普通模块需在场景内 `~module enable`，`~auth` 可授予单个用户模块级超级用户权限。

## 配置、数据库与本地化

- 配置在 `config.py` 用 `@on_module_config("<模块>")` 声明，表名 `module_<模块>`，注释键为 `config.comments.module_<模块>.<字段名>`，详见[配置](config.md)。
- 模型放在 `database/models.py` 并继承 `DBModel`，表名在 `Meta.table` 声明；新增表在 `owned_tables` 登记，结构变更通过 `migrations/` 发布，详见[数据库](database.md)。
- 文案一律 `I18NContext("key", **参数)`，只在包内 `locales/zh_cn.json` 建节点，详见[本地化](i18n.md)。

## 常用工具

- `CoolDown(key, msg, delay, whole_target=False)`：按用户或整个场景记录冷却，`check()` 返回剩余秒数。
- `gained_petal()`、`lost_petal()`、`cost_petal()`、`sign_get_petal()`、`settle_petals()`：读写花瓣余额并在消息中提示。
- `PlayState(game, msg)`：按会话保存小游戏状态，默认 `GAME_EXPIRED`（3600 秒）后过期，`running()` 以上下文管理器标记进行中。

## 运行期资源

`Bind.Module` 提供受框架管理的接口：`state()` 跨重载保留进程内状态，`cache()` 在版本变化时失效，`resource()` 懒加载并在关闭时释放，`cache_path()` 返回受管缓存目录。`cleanup()` 注册退出清理，`spawn()` 创建受追踪的后台任务；热重载按稳定 ID 替换注册项，并等待在途任务退出。

## 会话接口

`send_message()` 发送并返回消息 ID；`finish()` 发送后抛出 `SessionFinished`；`wait_confirm()`、`wait_next_message()`、`wait_reply()`、`wait_anyone()` 等待后续消息，超时或取消抛出 `WaitCancelException`；`sleep()` 在暂停期间释放执行锁。`delete()` 删除触发消息；`hold()`、`release()` 保持与释放平台上下文。同一会话已有命令在运行时，新命令收到“正在运行”提示。
