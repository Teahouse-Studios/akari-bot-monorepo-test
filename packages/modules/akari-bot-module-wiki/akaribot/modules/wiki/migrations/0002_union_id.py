"""Wiki 与 WikiLog 场景设置表改为关联 union。

两张表以平台场景 ID 为主键，场景换号后失去设置。union ID 沿用原平台 ID，因此仅需改列名。
WikiLog 与 Wiki 同属一个包，其表结构随 Wiki 一并维护。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext

REVISION = "0002_union_id"

TARGET_TABLES = ("module_wiki_target_set_info", "module_wikilog_target_set_info")


async def upgrade(ctx: MigrationContext) -> None:
    """
    将场景设置表的主键列重命名为 union_id。

    :param ctx: 迁移上下文。
    """
    for table in TARGET_TABLES:
        if not await ctx.has_column(table, "target_id"):
            continue
        await ctx.rename_column(table, "target_id", "union_id", "VARCHAR(512) NOT NULL")
