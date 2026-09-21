"""核心表的 v2 变更。

``target_info`` 增设 ``banned_users``：封禁状态原先混在 ``target_data.ban`` 里，与场景数据
共用一份 JSON，无法单独建索引也无法区分「未封禁」与「字段缺失」；拆出独立列后封禁判定不再
需要解析整份场景数据。``analytics_data.sender_id`` 同时改为可空，以容纳无发送者的记录。
"""

from __future__ import annotations

from akaribot.core.database.migration import MigrationContext

REVISION = "0002_banned_users_and_nullable_sender"
DEPENDS_ON = "0001_initial"

# 旧库此时仍是 target_info；若表已改名为 target_union_info，说明库已越过本步骤。
LEGACY_TARGET_TABLE = "target_info"

SQLITE_TARGET_REBUILD = """
PRAGMA foreign_keys=off;

CREATE TABLE _new_target_info (
    target_id VARCHAR(512) PRIMARY KEY,
    blocked BOOLEAN NOT NULL,
    muted BOOLEAN NOT NULL,
    locale VARCHAR(32) NOT NULL,
    modules JSON NOT NULL DEFAULT '[]',
    custom_admins JSON NOT NULL DEFAULT '[]',
    banned_users JSON NOT NULL DEFAULT '[]',
    target_data JSON NOT NULL DEFAULT '{}'
);

INSERT INTO _new_target_info (target_id, blocked, muted, locale, modules, custom_admins, banned_users, target_data)
SELECT target_id, blocked, muted, locale, modules, custom_admins, '[]', target_data FROM target_info;

DROP TABLE target_info;
ALTER TABLE _new_target_info RENAME TO target_info;

PRAGMA foreign_keys=on;
"""

SQLITE_ANALYTICS_REBUILD = """
PRAGMA foreign_keys=off;

CREATE TABLE _new_analytics_data (
    id INTEGER PRIMARY KEY,
    module_name VARCHAR(512) NOT NULL,
    module_type VARCHAR(512) NOT NULL,
    target_id VARCHAR(512) NOT NULL,
    sender_id VARCHAR(512),
    command TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO _new_analytics_data (id, module_name, module_type, target_id, sender_id, command, timestamp)
SELECT id, module_name, module_type, target_id, sender_id, command, timestamp FROM analytics_data;

DROP TABLE analytics_data;
ALTER TABLE _new_analytics_data RENAME TO analytics_data;

PRAGMA foreign_keys=on;
"""

MYSQL_TARGET_ALTER = """
ALTER TABLE target_info
    ADD COLUMN banned_users JSON DEFAULT NULL AFTER custom_admins;

UPDATE target_info
SET banned_users =
        IF(
            JSON_CONTAINS_PATH(target_data, 'one', '$.ban'),
            JSON_EXTRACT(target_data, '$.ban'),
            JSON_ARRAY()
        ),
    target_data  = JSON_REMOVE(target_data, '$.ban');
"""


async def upgrade(ctx: MigrationContext) -> None:
    """
    执行 v2 变更。

    :param ctx: 迁移上下文。
    """
    await _add_banned_users(ctx)
    await _make_sender_id_nullable(ctx)


async def _add_banned_users(ctx: MigrationContext) -> None:
    """
    为场景表增设封禁用户列。

    :param ctx: 迁移上下文。
    """
    if not await ctx.has_table(LEGACY_TARGET_TABLE):
        return
    if await ctx.has_column(LEGACY_TARGET_TABLE, "banned_users"):
        return
    if ctx.db_type == "sqlite":
        await ctx.conn.execute_script(SQLITE_TARGET_REBUILD)
        return
    await ctx.conn.execute_query(MYSQL_TARGET_ALTER)


async def _make_sender_id_nullable(ctx: MigrationContext) -> None:
    """
    放宽统计表的发送者列。

    :param ctx: 迁移上下文。
    """
    if not await ctx.has_table("analytics_data"):
        return
    if not await ctx.has_column("analytics_data", "sender_id"):
        return
    if await ctx.column_is_nullable("analytics_data", "sender_id"):
        return
    if ctx.db_type == "sqlite":
        await ctx.conn.execute_script(SQLITE_ANALYTICS_REBUILD)
        return
    await ctx.execute("ALTER TABLE analytics_data MODIFY sender_id VARCHAR(512) NULL;")
