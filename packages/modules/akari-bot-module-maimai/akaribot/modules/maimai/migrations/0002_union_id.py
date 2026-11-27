"""maimai 绑定表改为关联 union。

水鱼与落雪两侧的绑定以平台 ID 为主键，平台换号后失去绑定。union ID 沿用原平台 ID，
因此仅需改列名。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext

REVISION = "0002_union_id"

BIND_TABLES = ("module_maimai_diving_prober_bind_info", "module_maimai_lxns_prober_bind_info")


async def upgrade(ctx: MigrationContext) -> None:
    """
    将两张查分绑定表的主键列重命名为 union_id。

    :param ctx: 迁移上下文。
    """
    for table in BIND_TABLES:
        if not await ctx.has_column(table, "sender_id"):
            continue
        await ctx.rename_column(table, "sender_id", "union_id", "VARCHAR(512) NOT NULL")
