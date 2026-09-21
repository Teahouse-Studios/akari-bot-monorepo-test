"""core 基线。

v1 时代的表由 ``generate_schemas`` 依模型直接建立，没有需要单独执行的变更；本 revision 只
用于给 core 一个可依赖的起点。
"""

from __future__ import annotations

from core.database.migration import MigrationContext

REVISION = "0001_initial"
DEPENDS_ON = None


async def upgrade(ctx: MigrationContext) -> None:
    """
    基线迁移，无实际变更。

    :param ctx: 迁移上下文。
    """
