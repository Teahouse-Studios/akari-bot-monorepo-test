"""数据库迁移框架测试。"""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import tortoise.context as tortoise_context
from tortoise import Tortoise
from tortoise.context import TortoiseContext

from core.database import fetch_module_db
from core.database.legacy import LATEST_LEGACY_VERSION, LEGACY_MAP, convert_legacy_version
from core.database.migration import (
    MigrationContext,
    MigrationError,
    MigrationModule,
    MigrationRunner,
    order_migrations,
)
from core.database.models import DBVersion, SchemaMigration
from core.registry import PackageRegistry
from core.tester import Tester, func_case
from core.utils.url_audit import GlobalURLAllowlist, GlobalURLBlocklist

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "db"

MAIMAI_PACKAGE = "akari-bot-module-maimai"
DIVING_TABLE = "module_maimai_diving_prober_bind_info"
LXNS_TABLE = "module_maimai_lxns_prober_bind_info"


class _isolated_db:
    """在独立的 Tortoise 上下文里打开一个 SQLite 文件。

    样本库与测试进程自带的库不能共用连接：升级会改动表结构，必须落在文件副本上。
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.context = TortoiseContext()
        self.token = None

    async def __aenter__(self):
        self.token = tortoise_context._current_context.set(self.context)
        await self.context.init(
            config={
                "connections": {"default": f"sqlite://{self.path}"},
                "apps": {
                    "models": {
                        "models": ["core.database.models"] + fetch_module_db(),
                        "default_connection": "default",
                    }
                },
            },
            _enable_global_fallback=False,
        )
        return self

    async def __aexit__(self, *exc):
        await self.context.close_connections()
        tortoise_context._current_context.reset(self.token)


def _patch_rule_paths(root: Path) -> None:
    """把 URL 名单写到临时目录，避免升级用例改动实例数据。"""
    allowlist = root / "allowlist"
    blocklist = root / "blocklist"
    GlobalURLAllowlist.directory = allowlist
    GlobalURLAllowlist.builtin_path = allowlist / "global.txt"
    GlobalURLAllowlist.user_path = allowlist / "user.txt"
    GlobalURLBlocklist.directory = blocklist
    GlobalURLBlocklist.builtin_path = blocklist / "global.txt"
    GlobalURLBlocklist.user_path = blocklist / "user.txt"


def _total_revisions(discovered: dict[str, list[MigrationModule]]) -> int:
    return sum(len(modules) for modules in discovered.values())


async def _test_discovery_covers_legacy_map():
    discovered = await MigrationRunner.discover()
    expected = {(package, revision) for entries in LEGACY_MAP.values() for package, revision in entries}
    actual = {(package, module.revision) for package, modules in discovered.items() for module in modules}
    order = MigrationRunner._order(discovered, None)
    return actual == expected and order[0] == "core" and set(order) == set(discovered) and len(order) == 5


async def _noop_upgrade(ctx: MigrationContext) -> None:
    """排序用例使用的占位迁移。"""


def _module(revision: str, depends_on: str | None = None) -> MigrationModule:
    return MigrationModule(
        package="demo",
        revision=revision,
        path=Path(f"{revision}.py"),
        checksum="",
        depends_on=depends_on,
        upgrade=_noop_upgrade,
    )


async def _test_revision_order_follows_dependencies():
    ordered = order_migrations(
        "demo",
        [_module("0003_c", "0002_b"), _module("0001_a"), _module("0002_b", "0001_a")],
    )
    if [module.revision for module in ordered] != ["0001_a", "0002_b", "0003_c"]:
        return False

    failures = 0
    for candidates in (
        [_module("0001_a"), _module("0001_a")],
        [_module("0001_a", "0009_missing")],
        [_module("0001_a", "0002_b"), _module("0002_b", "0001_a")],
    ):
        try:
            order_migrations("demo", candidates)
        except MigrationError:
            failures += 1
    return failures == 3


async def _test_migration_context_ddl_helpers():
    ctx = MigrationContext(Tortoise.get_connection("default"))
    await ctx.execute('DROP TABLE IF EXISTS "migration_probe";')
    await ctx.execute('CREATE TABLE "migration_probe" ("id" INTEGER PRIMARY KEY, "legacy_id" VARCHAR(512) NOT NULL);')
    try:
        checks = [
            await ctx.has_table("migration_probe"),
            await ctx.has_column("migration_probe", "legacy_id"),
            not await ctx.has_index("migration_probe", "legacy_id"),
        ]
        await ctx.create_index("migration_probe", ["legacy_id"], "idx_migration_probe_legacy")
        checks.append(await ctx.has_index("migration_probe", "legacy_id"))
        await ctx.add_column("migration_probe", "added", "VARCHAR(32)")
        checks.append(await ctx.has_column("migration_probe", "added"))
        checks.append(await ctx.column_is_nullable("migration_probe", "added"))
        await ctx.rename_column("migration_probe", "legacy_id", "union_id", "VARCHAR(512) NOT NULL")
        checks.append(
            await ctx.has_column("migration_probe", "union_id")
            and not await ctx.has_column("migration_probe", "legacy_id")
        )
        await ctx.drop_column("migration_probe", "added")
        checks.append(not await ctx.has_column("migration_probe", "added"))
        await ctx.rename_table("migration_probe", "migration_probe_renamed")
        checks.append(await ctx.has_table("migration_probe_renamed"))
        return all(checks)
    finally:
        await ctx.execute('DROP TABLE IF EXISTS "migration_probe";')
        await ctx.execute('DROP TABLE IF EXISTS "migration_probe_renamed";')


async def _test_new_database_applies_all_revisions():
    with TemporaryDirectory() as temp_dir:
        async with _isolated_db(Path(temp_dir) / "fresh.db"):
            await Tortoise.generate_schemas(safe=True)
            converted = await convert_legacy_version()
            discovered = await MigrationRunner.discover()
            applied = await MigrationRunner.upgrade()
            pending = await MigrationRunner.pending()
            stamped = await SchemaMigration.all().count()
            return (
                converted is None
                and len(applied) == _total_revisions(discovered)
                and pending == {}
                and stamped == _total_revisions(discovered)
            )


async def _test_legacy_fixtures_reach_latest_schema():
    """六条旧版本升级路径都要升到最新结构，且重跑为 no-op"""
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _patch_rule_paths(root)
        GlobalURLAllowlist.clear_cache()
        GlobalURLBlocklist.clear_cache()
        results = []
        for version in range(1, LATEST_LEGACY_VERSION + 1):
            path = root / f"upgrade_v{version}.db"
            shutil.copy(FIXTURES / f"legacy_v{version}.db", path)
            async with _isolated_db(path):
                conn = Tortoise.get_connection("default")
                await Tortoise.generate_schemas(safe=True)
                discovered = await MigrationRunner.discover()
                total = _total_revisions(discovered)
                converted = await convert_legacy_version()
                await MigrationRunner.upgrade()
                pending_after = await MigrationRunner.pending()
                stamped = await SchemaMigration.all().count()
                legacy = await DBVersion.first()
                senders = sorted(
                    row["union_id"]
                    for row in await conn.execute_query_dict('SELECT "union_id" FROM "sender_union_info";')
                )
                remaining = await SchemaMigration.all().count()
                converted_again = await convert_legacy_version()
                applied_again = await MigrationRunner.upgrade()
                results.append(
                    converted == version
                    and converted_again is None
                    and not applied_again
                    and pending_after == {}
                    and stamped == total
                    and remaining == stamped
                    and (legacy is None or legacy.version == LATEST_LEGACY_VERSION)
                    and senders == ["sender|1", "sender|2"]
                )
        GlobalURLAllowlist.clear_cache()
        GlobalURLBlocklist.clear_cache()
        return all(results)


async def _downgrade_maimai_oauth(conn) -> None:
    """把 maimai 绑定表还原成 OAuth 列出现之前的结构。"""
    await conn.execute_query(f'ALTER TABLE "{DIVING_TABLE}" DROP COLUMN "refresh_token";')
    await conn.execute_query(f'ALTER TABLE "{DIVING_TABLE}" DROP COLUMN "subject";')
    await conn.execute_query(f'ALTER TABLE "{LXNS_TABLE}" DROP COLUMN "refresh_token";')
    await conn.execute_query(f'ALTER TABLE "{LXNS_TABLE}" ADD COLUMN "friend_code" VARCHAR(512) NOT NULL DEFAULT \'\';')


async def _maimai_oauth_columns(conn) -> tuple[bool, bool]:
    diving = {row["name"] for row in await conn.execute_query_dict(f'PRAGMA table_info("{DIVING_TABLE}");')}
    lxns = {row["name"] for row in await conn.execute_query_dict(f'PRAGMA table_info("{LXNS_TABLE}");')}
    return {"refresh_token", "subject"} <= diving, "friend_code" in lxns


async def _test_missing_module_package_is_skipped():
    """模块包缺席时其 revision 不被发现，其表也不被触碰"""
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        registry_dirs = PackageRegistry.migration_dirs()

        def without_maimai():
            return [entry for entry in registry_dirs if entry[0] != MAIMAI_PACKAGE]

        outcomes = []
        for absent in (True, False):
            path = root / f"skip_{absent}.db"
            shutil.copy(FIXTURES / f"legacy_v{LATEST_LEGACY_VERSION}.db", path)
            patcher = patch.object(PackageRegistry, "migration_dirs", new=classmethod(lambda cls: without_maimai()))
            if absent:
                patcher.start()
            try:
                async with _isolated_db(path):
                    conn = Tortoise.get_connection("default")
                    await Tortoise.generate_schemas(safe=True)
                    await SchemaMigration.filter(package=MAIMAI_PACKAGE).delete()
                    await _downgrade_maimai_oauth(conn)
                    discovered = await MigrationRunner.discover()
                    applied = await MigrationRunner.upgrade()
                    oauth_present, friend_code_present = await _maimai_oauth_columns(conn)
                    touched = any(package == MAIMAI_PACKAGE for package, _ in applied)
                    outcomes.append((MAIMAI_PACKAGE in discovered, touched, oauth_present, friend_code_present))
            finally:
                if absent:
                    patcher.stop()

        return outcomes[0] == (False, False, False, True) and outcomes[1] == (True, True, True, False)


async def _test_checksum_mismatch_only_warns():
    with TemporaryDirectory() as temp_dir:
        async with _isolated_db(Path(temp_dir) / "checksum.db"):
            await Tortoise.generate_schemas(safe=True)
            await SchemaMigration.create(package="core", revision="0001_initial", checksum="0" * 64)
            applied = await MigrationRunner.upgrade()
            recorded = await SchemaMigration.get(package="core", revision="0001_initial")
            return ("core", "0001_initial") not in applied and recorded.checksum == "0" * 64 and bool(applied)


async def _test_stamp_is_idempotent():
    with TemporaryDirectory() as temp_dir:
        async with _isolated_db(Path(temp_dir) / "stamp.db"):
            await Tortoise.generate_schemas(safe=True)
            await MigrationRunner.stamp("core", ["0001_initial"])
            await MigrationRunner.stamp("core", ["0001_initial"])
            checks = [await SchemaMigration.filter(package="core", revision="0001_initial").count() == 1]
            await MigrationRunner.stamp("absent-package", ["0001_initial"])
            row = await SchemaMigration.get(package="absent-package", revision="0001_initial")
            checks.append(row.checksum is None)
            return all(checks)


@func_case
async def test_database_migration(tester: Tester):
    await tester.test(_test_discovery_covers_legacy_map, "迁移发现结果与旧版本号对照表一致")
    await tester.test(_test_revision_order_follows_dependencies, "迁移按依赖排序且拒绝重名、缺依赖与成环")
    await tester.test(_test_migration_context_ddl_helpers, "迁移上下文的探测与 DDL 在 SQLite 上自洽")
    await tester.test(_test_new_database_applies_all_revisions, "新库执行全部 revision 并留下完整登记")
    await tester.test(_test_legacy_fixtures_reach_latest_schema, "六个旧版本样本库均升到最新结构且重跑为 no-op")
    await tester.test(_test_missing_module_package_is_skipped, "模块包缺席时跳过其 revision 且不触碰其表")
    await tester.test(_test_checksum_mismatch_only_warns, "已应用迁移的 checksum 变化只告警不阻断")
    await tester.test(_test_stamp_is_idempotent, "stamp 可重复执行且允许登记未发现的 revision")
    return tester
