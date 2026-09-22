"""把 Wiki API 名单并入全局 URL 名单。

名单原先按 Wiki API 各存一张表，与其它模块的 URL 规则互相独立，同一域名要在多处各配一遍。
并入全局 URL 用户规则文件后只有一份来源，迁移成功后即可删除旧表。

导入失败时不删旧表：``import_user_rules`` 对不合法的规则会抛出异常，此时数据仍在原表中，
下一次启动可重试，不会因中途失败丢掉用户配置。
"""

from __future__ import annotations

from akaribot.core.api import MigrationContext, GlobalURLAllowlist, GlobalURLBlocklist

REVISION = "0003_url_rules_to_global"
DEPENDS_ON = "0002_union_id"

URL_RULE_TABLES = (
    ("module_wiki_allow_list", GlobalURLAllowlist),
    ("module_wiki_block_list", GlobalURLBlocklist),
)


async def upgrade(ctx: MigrationContext) -> None:
    """
    迁移旧名单并删除旧表。

    :param ctx: 迁移上下文。
    """
    for table, rule_list in URL_RULE_TABLES:
        if not await ctx.has_table(table):
            continue
        rows = await ctx.fetch_all(f"SELECT {ctx.quote('api_link')} FROM {ctx.quote(table)};")
        rule_list.import_user_rules(row["api_link"] for row in rows)
        await ctx.execute(f"DROP TABLE {ctx.quote(table)};")
