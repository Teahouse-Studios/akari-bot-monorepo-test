# 数据库

本文介绍 `default` 与 `local` 双数据库连接、union 数据模型、数据迁移机制及热重载流程。

数据库层基于 Tortoise ORM，负责连接管理、模型注册、启动迁移与热重载。

业务模型继承 `akaribot.core.api.DBModel`，通过 `get_by_target_id()`、`get_by_sender_id()` 关联到会话或 union。

## 双连接

`init_db()` 注册两个连接与两个应用：

| 连接 | 默认连接字符串 | 应用 | 内容 |
| --- | --- | --- | --- |
| `default` | `sqlite://database/save.db` | `models` | 核心模型与各成员包的模型 |
| `local` | `sqlite://database/local.db` | `local_models` | 本机缓存表 |

`default` 的连接字符串由 `CoreSecretConfig.db_path` 提供。SQLite 的相对路径以实例根目录为基准解析，进程可以从任意目录启动。

连接参数首先配置 `busy_timeout=30000`，随后启用 WAL 模式。并发启动期间，等待写入锁的时间同样受该超时阈值约束。

`local` 连接用于存储可随时重建的本机数据（如敏感词检测缓存与外部平台活动记录），相关数据独立保存于专用数据库文件中。

```python
from tortoise import fields

from akaribot.core.api import DBModel


class MyModuleData(DBModel):
    union_id = fields.CharField(max_length=512, db_index=True)
    payload = fields.JSONField(default={})

    class Meta:
        table = "module_my_data"
```

框架通过各成员包的发现元数据收集模型文件，由 `PackageRegistry.db_model_paths()` 提供对应的导入路径。

`init_db()` 将上述模型路径注册至 `models` 应用。`get_model_names()` 与 `get_model_fields()` 供 `~database` 命令列出数据表及其字段定义。

## union 数据

鉴于平台原生账号与场景 ID 存在变更可能，所有业务数据统一关联至持久化的 union 实体：

| 表 | 关键列 | 说明 |
| --- | --- | --- |
| `sender_union_info` | `union_id` | 用户数据：`blocked`、`trusted`、`superuser`、`warns`、`petal`、`sender_data` |
| `sender_union_bind` | `sender_id` → `union_id` | 平台账号到用户 union 的映射 |
| `target_union_info` | `union_id` | 场景数据：`muted`、`locale`、`modules`、`custom_admins`、`banned_users`、`target_data` |
| `target_union_bind` | `target_id` → `union_id`，`channel_id` | 平台场景到场景 union 的映射与消息通道编号 |

`resolve_union(id, create)` 解析并返回记录所属的 union。若 `create` 为 `True` 且对应记录不存在，则自动创建新记录。

`TargetUnionInfo.config_module()`、`switch_mute()`、`edit_target_data()` 与 `SenderUnionInfo.edit_sender_data()` 均在数据库事务中执行，通过 `select_for_update()` 实现 JSON 列的安全更新。

同一 union 实体下具有相同 `channel_id` 的场景归属于同一消息通道，主动推送按通道维度仅执行一次投递。

`delete_union()` 首先校验外部引用约束，随后清理该 union 作用域内的全部关联数据表记录。

跨表写入同一 union 时，首先调用 `union_mutation()`，随后在 `default` 事务中对该 union 所在的数据行加锁：

```python
from tortoise.transactions import in_transaction

from akaribot.core.api import SenderUnionInfo, union_mutation


async def bind(union_id: str, username: str) -> bool:
    async with union_mutation():
        async with in_transaction("default") as connection:
            current = await (
                SenderUnionInfo.filter(union_id=union_id)
                .using_db(connection)
                .select_for_update()
                .first()
            )
            if not current:
                return False
            await MyModuleData.update_or_create(
                union_id=union_id,
                defaults={"payload": {"username": username}},
                using_db=connection,
            )
            return True
```

查询与写入操作必须共用同一 `connection`，否则 `select_for_update()` 获取的行级锁无法覆盖后续写入操作。

核心包在 `manifest.toml` 的 `owned_tables` 中声明自身拥有的数据表，数据清理时据此识别数据表所属的包。各成员包的模型与数据表均由各自的 `manifest.toml` 声明。

## 迁移

各成员包将迁移脚本（revision）存放于 `migrations/` 目录（或由 `manifest.migrations` 明确声明的路径）：

```python
REVISION = "0003_union_core"
DEPENDS_ON = "0002_banned_users_and_nullable_sender"


async def upgrade(ctx):
    ...
```

- `REVISION` 非空，`DEPENDS_ON` 仅能指向同包 revision。`DEPENDS_ON` 未声明时，按 revision 字典序执行。
- 执行顺序固定为首先应用 core 的全部待执行 revision，随后按成员包名称字典序依次执行各成员包的迁移。
- 已应用的迁移记录保存于 `schema_migrations`（包含 `package`、`revision`、`applied_at`、`checksum` 字段），以 `(package, revision)` 复合键保持唯一。迁移文件内容发生变动时 checksum 随之变化，系统据此检测已应用迁移文件的异常篡改。
- 每条 revision 必须保持幂等与可重复执行。鉴于 MySQL 的 DDL 操作会自动提交事务，无法与版本记录纳入同一原子事务，因而每个执行步骤均遵循“先探测后执行”原则。SQLite 支持事务性 DDL，Runner 会将单条 revision 与对应版本记录纳入同一原子事务。
- `MigrationContext` 提供 `execute()`、`execute_script()`、`fetch_all()`、`has_table()`、`has_column()`、`rename_table()`、`rename_column()`，按方言生成 SQL。

数据库迁移仅在具备写入权限的初始化进程中执行。pre-init 以 `generate_schemas=True` 参数调用 `init_db()`，随后触发 `run_startup_migrations()`。平台进程与 Server 仅对既有数据执行读写，数据表及表结构的创建与变更均由独立初始化进程完成。

## 热重载

模块安装、卸载或执行数据库维护操作时将触发连接重建：

1. `prepare_db_reload()` 在原有 context 仍可用时初始化新 context。
2. 激活新 context 前，系统会等待 JobQueue 处理完毕队列中的存量任务，并使 Scheduler 进入维护时段以停止接收新任务，同时取消当前运行中的计划任务。
3. `activate_db_reload()` 原子替换全局 context，随后关闭旧 context。
4. 若执行失败，`close_prepared_db_reload()` 会丢弃未激活的 context，原有连接继续保持可用。

`close_db()` 负责释放连接并清理 Tortoise 的全局及任务级 context，确保下一次初始化从干净的初始状态开始。
