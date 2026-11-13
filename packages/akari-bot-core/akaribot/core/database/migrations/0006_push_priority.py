"""场景绑定表增设主动推送优先级。

同一场景可能绑定多个平台账号，主动推送时按优先级择一投递，优先级最高的账号先收到消息。
列默认 0，旧记录按原有顺序参与排序。
"""

from __future__ import annotations

from akaribot.core.database.migration import MigrationContext

REVISION = "0006_push_priority"
DEPENDS_ON = "0005_rebuild_job_queues"

TABLE = "target_union_bind"
COLUMN = "push_priority"


async def upgrade(ctx: MigrationContext) -> None:
    """
    补充推送优先级列。

    ``ALTER TABLE ... ADD COLUMN`` 在不同方言下均不支持 ``IF NOT EXISTS``，故先探测再执行。

    :param ctx: 迁移上下文。
    """
    if await ctx.has_column(TABLE, COLUMN):
        return
    await ctx.execute(f"ALTER TABLE {ctx.quote(TABLE)} ADD COLUMN {ctx.quote(COLUMN)} INT NOT NULL DEFAULT 0;")
