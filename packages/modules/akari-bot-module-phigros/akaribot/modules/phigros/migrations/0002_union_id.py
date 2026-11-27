"""Phigros 绑定表改为关联 union。

绑定以平台 ID 为主键，平台换号即失去绑定。union ID 沿用原平台 ID，因此仅改列名。同一版
增加国际服标记，旧行按国服处理。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext

REVISION = "0002_union_id"

BIND_TABLE = "module_phigros_bind_info"


async def upgrade(ctx: MigrationContext) -> None:
    """
    修改主键列名并补充国际服标记。

    :param ctx: 迁移上下文。
    """
    if await ctx.has_column(BIND_TABLE, "sender_id"):
        await ctx.rename_column(BIND_TABLE, "sender_id", "union_id", "VARCHAR(512) NOT NULL")
    if not await ctx.has_column(BIND_TABLE, "is_international"):
        await ctx.add_column(BIND_TABLE, "is_international", "INT", null=False, default="0")
