"""maimai 绑定表的 OAuth 列变更。

水鱼分发给用户各自部署的应用属于公开客户端，换取令牌接口对它不可用，仅能为每位用户各自保存一个
refresh token，落雪侧则保存用户的授权令牌。旧行没有 refresh token，用户重新完成一次绑定时才写入。

同一批变更同时删除落雪的旧好友码列。该列不在模型中，旧表上为 NOT NULL 且无默认值，不删除会让
新绑定写入直接失败。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext

REVISION = "0003_oauth_columns"
DEPENDS_ON = "0002_union_id"

OAUTH_COLUMNS = (
    ("module_maimai_diving_prober_bind_info", "refresh_token", "VARCHAR(1024)"),
    ("module_maimai_diving_prober_bind_info", "subject", "VARCHAR(512)"),
    ("module_maimai_lxns_prober_bind_info", "refresh_token", "VARCHAR(1024)"),
)

OBSOLETE_COLUMNS = (("module_maimai_lxns_prober_bind_info", "friend_code"),)


async def upgrade(ctx: MigrationContext) -> None:
    """
    补充 OAuth 列并删除落雪的旧好友码列。

    :param ctx: 迁移上下文。
    """
    for table, column, column_type in OAUTH_COLUMNS:
        # 未启用该模块时这张表可能根本不存在，此时无需迁移。
        if not await ctx.has_table(table):
            continue
        if await ctx.has_column(table, column):
            continue
        await ctx.add_column(table, column, column_type)
    for table, column in OBSOLETE_COLUMNS:
        if not await ctx.has_table(table):
            continue
        if not await ctx.has_column(table, column):
            continue
        await ctx.drop_column(table, column)
