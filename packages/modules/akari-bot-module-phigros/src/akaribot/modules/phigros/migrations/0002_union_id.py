"""Phigros 绑定表改挂 union。

绑定原本以平台 ID 为主键，平台换号即失去绑定。union ID 沿用原平台 ID，因此只需改列名；同一
版还补上国际服标记，旧行一律按国服处理。
"""

from __future__ import annotations

from core.database.migration import MigrationContext

REVISION = "0002_union_id"

BIND_TABLE = "module_phigros_bind_info"


async def upgrade(ctx: MigrationContext) -> None:
    """
    改主键列名并补上国际服标记。

    :param ctx: 迁移上下文。
    """
    if await ctx.has_column(BIND_TABLE, "sender_id"):
        await ctx.rename_column(BIND_TABLE, "sender_id", "union_id", "VARCHAR(512) NOT NULL")
    if not await ctx.has_column(BIND_TABLE, "is_international"):
        await ctx.add_column(BIND_TABLE, "is_international", "INT", null=False, default="0")
