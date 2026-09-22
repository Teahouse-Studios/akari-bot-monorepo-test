"""Cytoid 绑定表改挂 union。

绑定原本以平台 ID 为主键，平台换号即失去绑定。union ID 沿用原平台 ID，因此只需改列名。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext

REVISION = "0002_union_id"

BIND_TABLES = ("module_cytoid_bind_info",)


async def upgrade(ctx: MigrationContext) -> None:
    """
    把绑定表主键列改名为 union_id。

    :param ctx: 迁移上下文。
    """
    for table in BIND_TABLES:
        if not await ctx.has_column(table, "sender_id"):
            continue
        await ctx.rename_column(table, "sender_id", "union_id", "VARCHAR(512) NOT NULL")
