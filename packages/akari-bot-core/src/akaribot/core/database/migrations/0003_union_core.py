"""核心表的 v3 变更：数据挂载点由平台 ID 改为 union。

平台场景会换号，数据若以平台 ID 为主键，换号即等于换人；改挂 union 后多个平台身份可以共享
同一份数据。核心两张表随之改名以对齐模型名，统计与审计表则保留原始 ID 另增 union 列，历史
记录不受影响。
"""

from __future__ import annotations

from core.database.migration import MigrationContext
from core.database.models import TargetUnionBind, TargetUnionInfo, backfill_union_binds

REVISION = "0003_union_core"
DEPENDS_ON = "0002_banned_users_and_nullable_sender"

# 旧名到新名。表若已由 generate_schemas 按新模型建出，须先移除这张空表再改名。
CORE_RENAME_TABLES = {
    "sender_info": "sender_union_info",
    "target_info": "target_union_info",
}

# 主键列改为 union_id。旧数据的 union ID 沿用原平台 ID，故只需改名。
CORE_RENAME_COLUMNS = {
    "sender_id": ["sender_union_info"],
    "target_id": ["target_union_info"],
}

# 统计与审计表保留原始 ID，另增 union 列用于聚合。
UNION_RECORD_TABLES = ["analytics_data", "unfriendly_actions"]

# 轮询与区间统计所需的索引：job_queues 每 100 毫秒被轮询，analytics_data 要按区间反复聚合，
# 两者都随行数增长退化为全表扫描。v5 已重建 job_queues，故建索引前须确认目标列仍在。
CORE_INDEXES = (
    ("job_queues", ("target_client", "status"), "idx_job_queues_client_status"),
    ("analytics_data", ("timestamp",), "idx_analytics_data_timestamp"),
)


async def upgrade(ctx: MigrationContext) -> None:
    """
    执行 v3 的核心变更。

    模块表的列改名由各模块包自己的 revision 完成，core 不再登记模块表名。

    :param ctx: 迁移上下文。
    """
    await _rename_tables(ctx)
    await _rename_columns(ctx)
    await backfill_union_binds()
    await _ensure_channel_ids(ctx)
    await _drop_legacy_bots_id()
    await _add_union_record_columns(ctx)
    await _create_indexes(ctx)


async def _rename_tables(ctx: MigrationContext) -> None:
    """
    把核心表改名为 union 命名。

    :param ctx: 迁移上下文。
    """
    for old_table, new_table in CORE_RENAME_TABLES.items():
        if not await ctx.has_table(old_table):
            continue
        if await ctx.has_table(new_table):
            rows = await ctx.fetch_all(f"SELECT COUNT(*) AS cnt FROM {ctx.quote(new_table)};")
            if rows and rows[0]["cnt"]:
                continue
            await ctx.execute(f"DROP TABLE {ctx.quote(new_table)};")
        await ctx.rename_table(old_table, new_table)


async def _rename_columns(ctx: MigrationContext) -> None:
    """
    把核心表的主键列改名为 union_id。

    :param ctx: 迁移上下文。
    """
    for old_column, tables in CORE_RENAME_COLUMNS.items():
        for table in tables:
            if not await ctx.has_column(table, old_column):
                continue
            await ctx.rename_column(table, old_column, "union_id", "VARCHAR(512) NOT NULL")


async def _ensure_channel_ids(ctx: MigrationContext) -> None:
    """
    为绑定行补上消息通道号并按组顺延。

    通道号须在组内逐个顺延：若一律保留默认值，同一 union 下的全部场景会被判定为同一条消息
    通道，命令与推送将相互去重，导致场景不再有消息送达。

    :param ctx: 迁移上下文。
    """
    if not await ctx.has_column("target_union_bind", "channel_id"):
        await ctx.add_column("target_union_bind", "channel_id", "INT", null=False, default="1")
    for union_id in set(await TargetUnionBind.all().values_list("union_id", flat=True)):
        binds = await TargetUnionBind.filter(union_id=union_id).order_by("bound_at")
        for channel_id, bind in enumerate(binds, start=1):
            bind.channel_id = channel_id
            await bind.save()


async def _drop_legacy_bots_id() -> None:
    """清除旧版机器人互认记录。

    旧版 connect 把互认记录存为扁平列表，无法反查某条记录属于哪个场景，解绑时也就无从删除。
    该结构已改为两级字典，旧值直接清除，重新执行一次 ``bind auto`` 即可。
    """
    for target in await TargetUnionInfo.all():
        if isinstance(target.target_data.get("bots_id"), list):
            target.target_data.pop("bots_id")
            await target.save()


async def _add_union_record_columns(ctx: MigrationContext) -> None:
    """
    为统计与审计表增设 union 列并回填。

    :param ctx: 迁移上下文。
    """
    for table in UNION_RECORD_TABLES:
        for column, source in (("target_union_id", "target_id"), ("sender_union_id", "sender_id")):
            if await ctx.has_column(table, column):
                continue
            await ctx.add_column(table, column, "VARCHAR(512)")
            await ctx.execute(
                f"UPDATE {ctx.quote(table)} SET {ctx.quote(column)} = {ctx.quote(source)} "
                f"WHERE {ctx.quote(column)} IS NULL;"
            )


async def _create_indexes(ctx: MigrationContext) -> None:
    """
    为轮询与区间统计补建索引。

    :param ctx: 迁移上下文。
    """
    for table, columns, index_name in CORE_INDEXES:
        if not await ctx.has_column(table, columns[0]):
            continue
        if await ctx.has_index(table, columns[0]):
            continue
        await ctx.create_index(table, list(columns), index_name)
