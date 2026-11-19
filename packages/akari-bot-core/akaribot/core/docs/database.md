# 数据库

本文将会介绍数据库的连接划分、union 数据、迁移执行与热重载。

数据库层基于 Tortoise ORM，负责连接管理、模型注册、启动迁移与热重载。业务模型继承 `akaribot.core.api.DBModel`，通过 `get_by_target_id()`、`get_by_sender_id()` 关联到会话或 union。

## 双连接

`init_db()` 注册两个连接与两个应用：

| 连接 | 默认连接串 | 应用 | 内容 |
| --- | --- | --- | --- |
| `default` | `sqlite://database/save.db` | `models` | 核心模型与各包的模型 |
| `local` | `sqlite://database/local.db` | `local_models` | 本机缓存表 |

`default` 的连接串取自 `CoreSecretConfig.db_path`。SQLite 的相对路径以实例根为基准解析，进程可以从任意目录启动。

连接参数先设置 `busy_timeout=30000`，再启用 WAL。并发启动时，等待写锁的时间也受这个超时约束。

`local` 存放可随时重建的本机数据，例如关键词检测缓存和外部平台活动记录。这些数据与业务表分开，不会争用同一把写锁。

```python
from tortoise import fields

from akaribot.core.api import DBModel


class MyModuleData(DBModel):
    union_id = fields.CharField(max_length=512, db_index=True)
    payload = fields.JSONField(default={})

    class Meta:
        table = "module_my_data"
```

包的模型文件由发现层收集：`PackageRegistry.db_model_paths()` 给出导入路径，`init_db()` 把它们追加到 `models` 应用。`get_model_names()` 与 `get_model_fields()` 供 `~database` 命令枚举表与字段。

## union 数据

平台账号与场景的 ID 会变化，业务数据统一关联到 union：

| 表 | 关键列 | 说明 |
| --- | --- | --- |
| `sender_union_info` | `union_id` | 用户数据：`blocked`、`trusted`、`superuser`、`warns`、`petal`、`sender_data` |
| `sender_union_bind` | `sender_id` → `union_id` | 平台账号到用户 union 的映射 |
| `target_union_info` | `union_id` | 场景数据：`muted`、`locale`、`modules`、`custom_admins`、`banned_users`、`target_data` |
| `target_union_bind` | `target_id` → `union_id`，`channel_id` | 平台场景到场景 union 的映射与消息通道号 |

`resolve_union(id, create)` 返回所属 union，必要时新建。`TargetUnionInfo.config_module()`、`switch_mute()`、`edit_target_data()`、`SenderUnionInfo.edit_sender_data()` 在事务内以 `select_for_update()` 改写 JSON 列。

同一 union 下 `channel_id` 相同的场景被视为同一条消息通道，主动推送按通道只发送一次。`delete_union()` 会先校验引用，再级联清理该 union 所在域的全部表。

跨表写入同一 union 时，先进入 `union_mutation()`，再在 `default` 事务里锁住 union 行：

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

查询与写入必须共用同一个 `connection`，否则 `select_for_update()` 的行锁不覆盖后续写入。

核心包在 `manifest.toml` 的 `owned_tables` 中声明自己拥有的表，数据清理时据此判断表的归属。分发包的模型与表由各自的 `manifest.toml` 声明。模块包目录内没有 `database/models.py` 时不拥有独立表。

## 迁移

每个包把 revision 放在 `migrations/`（或 `manifest.migrations` 声明的目录）：

```python
REVISION = "0003_union_core"
DEPENDS_ON = "0002_banned_users_and_nullable_sender"


async def upgrade(ctx):
    ...
```

- `REVISION` 非空，`DEPENDS_ON` 只能指向同包 revision。`DEPENDS_ON` 未声明时，按 revision 字典序执行。
- 执行顺序固定为 core 的全部待应用 revision，再按包名执行各包。不支持跨包依赖。
- 已应用记录写入 `schema_migrations`（`package`、`revision`、`applied_at`、`checksum`），以 `(package, revision)` 唯一。revision 文件改动后 checksum 随之变化，可以据此发现文件已被修改。
- 每条 revision 必须可重复执行：MySQL 的 DDL 自动提交，无法与版本记录写入同一事务，因此每一步先探测再执行。SQLite 支持事务性 DDL，Runner 把单条 revision 与版本记录包进同一事务。
- `MigrationContext` 提供 `execute()`、`execute_script()`、`fetch_all()`、`has_table()`、`has_column()`、`rename_table()`、`rename_column()`，按方言生成 SQL。

迁移只在创建数据表的写入进程中执行。pre-init 以 `generate_schemas=True` 调用 `init_db()`，随后运行 `run_startup_migrations()`。平台进程与 Server 不创建数据表，也不修改表结构。

## 热重载

模块安装、卸载或数据库维护会替换连接：

1. `prepare_db_reload()` 在旧 context 仍可用时初始化新 context。
2. 激活前先进入 JobQueue 排空与 Scheduler 维护窗口，停止领取新任务并取消运行中的计划任务。
3. `activate_db_reload()` 原子替换全局 context，随后关闭旧 context。
4. 失败时 `close_prepared_db_reload()` 丢弃未激活的 context，旧连接保持可用。

`close_db()` 关闭连接并清除 Tortoise 的全局与任务级 context，使后续初始化从干净状态开始。
