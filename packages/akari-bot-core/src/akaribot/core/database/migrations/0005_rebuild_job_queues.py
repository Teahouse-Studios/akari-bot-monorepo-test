"""重建任务队列表。

JobQueue 记录仅表示进程间的在途任务，不属于需要跨版本保留的业务数据。协议 v2 的表结构与旧
协议不兼容，保留无法可靠解释或继续执行的历史任务只会带来误执行，故直接丢弃旧表并按当前模型
重新建表。
"""

from __future__ import annotations

from core.database.migration import MigrationContext

REVISION = "0005_rebuild_job_queues"
DEPENDS_ON = "0003_union_core"


async def upgrade(ctx: MigrationContext) -> None:
    """
    丢弃旧任务队列表并重建。

    ``DROP TABLE IF EXISTS`` 与 safe 建表都可重复执行，无需额外探测。

    :param ctx: 迁移上下文。
    """
    await ctx.execute(f"DROP TABLE IF EXISTS {ctx.quote('job_queues')};")
    await ctx.generate_schemas()
