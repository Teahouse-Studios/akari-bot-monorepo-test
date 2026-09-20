"""按包登记的数据库迁移。

每个包在 ``migrations/`` 下声明 revision。Runner 固定先执行 core 的全部待应用 revision，再按
包名依次执行各模块包——core 的改名与回填须先完成，模块包的列改名随后进行，这条跨包顺序无法用
``DEPENDS_ON`` 表达，故写死在执行顺序里。

硬规则是幂等：MySQL 的 DDL 自动提交，无法把「执行 DDL」与「写 schema_migrations」放进同一事务，
中途失败重跑时非幂等的迁移会重复施加变更。每条 revision 的每一步都要先探测再执行。SQLite 支持
事务性 DDL，Runner 在此额外把单条 revision 连同版本记录包进一个事务。
"""

from __future__ import annotations

import hashlib
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Awaitable, Callable

from tortoise import Tortoise
from tortoise.transactions import in_transaction

from core.database.link import db_type as configured_db_type
from core.database.models import SchemaMigration
from core.logger import Logger

CORE_PACKAGE = "core"

# 包内迁移目录的约定名。包若在 manifest 中声明了 migrations，则以声明为准。
MIGRATIONS_DIRNAME = "migrations"

# 支持事务性 DDL 的方言；其余方言只按先探测再执行的方式保证可重跑。
TRANSACTIONAL_DIALECTS = ("sqlite",)

_LOADED: dict[tuple[str, str], "MigrationModule"] = {}


class MigrationError(RuntimeError):
    """迁移定义或执行不满足契约。"""


def _dialect(conn) -> str:
    """
    取连接的方言名。

    以连接自身的能力为准，而不是模块级配置：测试与转换脚本会在同一进程内使用与配置不同的
    连接，按配置判断会生成错误的 DDL。

    :param conn: 数据库连接。
    :return: 方言名。
    """
    dialect = getattr(getattr(conn, "capabilities", None), "dialect", None)
    return dialect if isinstance(dialect, str) else configured_db_type


class MigrationContext:
    """
    单条 revision 的执行上下文。

    探测与 DDL 均按当前方言生成，revision 只描述要达成什么，不必自行分支 SQLite 与 MySQL。

    :param conn: 数据库连接。
    :param db_type: 方言名；省略时由连接推断。
    """

    def __init__(self, conn, db_type: str | None = None) -> None:
        self.conn = conn
        self.db_type = db_type or _dialect(conn)

    def quote(self, ident: str) -> str:
        """
        按方言给标识符加引号。

        :param ident: 表名或列名。
        :return: 加引号后的标识符。
        """
        return f'"{ident}"' if self.db_type == "sqlite" else f"`{ident}`"

    async def execute(self, sql: str, params: list | None = None) -> None:
        """
        执行一条语句。

        :param sql: SQL 语句。
        :param params: 位置参数。
        """
        if params is None:
            await self.conn.execute_query(sql)
        else:
            await self.conn.execute_query(sql, params)

    async def fetch_all(self, sql: str, params: list | None = None) -> list[dict]:
        """
        执行查询并取回全部行。

        :param sql: SQL 查询。
        :param params: 位置参数。
        :return: 行字典列表。
        """
        if params is None:
            return list(await self.conn.execute_query_dict(sql))
        return list(await self.conn.execute_query_dict(sql, params))

    async def has_table(self, table: str) -> bool:
        """
        判断表是否存在。

        :param table: 表名。
        :return: 是否存在。
        """
        if self.db_type == "sqlite":
            rows = await self.conn.execute_query_dict(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?;", [table]
            )
        else:
            rows = await self.conn.execute_query_dict(
                "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s;",
                [table],
            )
        return bool(rows)

    async def has_column(self, table: str, column: str) -> bool:
        """
        判断列是否存在，表不存在时同样返回 False。

        :param table: 表名。
        :param column: 列名。
        :return: 是否存在。
        """
        if self.db_type == "sqlite":
            rows = await self.conn.execute_query_dict(f"PRAGMA table_info({self.quote(table)});")
            return any(row["name"] == column for row in rows)
        rows = await self.conn.execute_query_dict(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s;",
            [table, column],
        )
        return bool(rows)

    async def column_is_nullable(self, table: str, column: str) -> bool:
        """
        判断列是否可为空。

        用于「收紧或放宽约束」这类无法靠列名判断是否已完成的步骤。

        :param table: 表名。
        :param column: 列名。
        :return: 列可空或不存在时为 True。
        """
        if self.db_type == "sqlite":
            rows = await self.conn.execute_query_dict(f"PRAGMA table_info({self.quote(table)});")
            for row in rows:
                if row["name"] == column:
                    return not row["notnull"]
            return True
        rows = await self.conn.execute_query_dict(
            "SELECT IS_NULLABLE FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s;",
            [table, column],
        )
        return not rows or rows[0]["IS_NULLABLE"] == "YES"

    async def has_index(self, table: str, column: str) -> bool:
        """
        判断指定列上是否已有索引，作为任意索引的首列即算。

        按列而非按索引名判断：新建的库由 ``generate_schemas`` 依模型声明建索引，索引名由 ORM
        生成，与迁移里显式指定的名字不同；按名字判断会为已有索引的库重复建一份。

        :param table: 表名。
        :param column: 列名。
        :return: 是否存在。
        """
        if self.db_type == "sqlite":
            indexes = await self.conn.execute_query_dict(f"PRAGMA index_list({self.quote(table)});")
            for index in indexes:
                columns = await self.conn.execute_query_dict(f"PRAGMA index_info({self.quote(index['name'])});")
                if columns and columns[0]["name"] == column:
                    return True
            return False
        rows = await self.conn.execute_query_dict(
            "SELECT INDEX_NAME FROM information_schema.STATISTICS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s AND SEQ_IN_INDEX = 1;",
            [table, column],
        )
        return bool(rows)

    async def add_column(
        self, table: str, column: str, ddl_type: str, *, null: bool = True, default: str | None = None
    ) -> None:
        """
        增列。

        :param table: 表名。
        :param column: 列名。
        :param ddl_type: 列类型，如 ``VARCHAR(1024)``。
        :param null: 是否允许为空。
        :param default: 默认值表达式；省略时不写 ``DEFAULT``。
        """
        statement = f"ALTER TABLE {self.quote(table)} ADD COLUMN {self.quote(column)} {ddl_type}"
        statement += " NULL" if null else " NOT NULL"
        if default is not None:
            statement += f" DEFAULT {default}"
        await self.execute(statement + ";")

    async def drop_column(self, table: str, column: str) -> None:
        """
        删列。

        :param table: 表名。
        :param column: 列名。
        """
        await self.execute(f"ALTER TABLE {self.quote(table)} DROP COLUMN {self.quote(column)};")

    async def rename_column(self, table: str, old: str, new: str, ddl_type: str) -> None:
        """
        改列名。

        MySQL 的 ``CHANGE COLUMN`` 必须重复列类型，且向下兼容到 8.0 以下版本，故统一走它。

        :param table: 表名。
        :param old: 旧列名。
        :param new: 新列名。
        :param ddl_type: 新列在 MySQL 上的完整类型，如 ``VARCHAR(512) NOT NULL``。
        """
        if self.db_type == "sqlite":
            await self.execute(f"ALTER TABLE {self.quote(table)} RENAME COLUMN {self.quote(old)} TO {self.quote(new)};")
            return
        await self.execute(
            f"ALTER TABLE {self.quote(table)} CHANGE COLUMN {self.quote(old)} {self.quote(new)} {ddl_type};"
        )

    async def rename_table(self, old: str, new: str) -> None:
        """
        改表名。

        :param old: 旧表名。
        :param new: 新表名。
        """
        await self.execute(f"ALTER TABLE {self.quote(old)} RENAME TO {self.quote(new)};")

    async def create_index(self, table: str, columns: list[str], name: str) -> None:
        """
        建索引。

        调用方须先以 :meth:`has_index` 探测：MySQL 不支持 ``CREATE INDEX IF NOT EXISTS``。

        :param table: 表名。
        :param columns: 参与索引的列。
        :param name: 索引名。
        """
        column_sql = ", ".join(self.quote(column) for column in columns)
        await self.execute(f"CREATE INDEX {self.quote(name)} ON {self.quote(table)} ({column_sql});")

    async def generate_schemas(self) -> None:
        """按当前模型补建缺失的表与索引。"""
        await Tortoise.generate_schemas(safe=True)


@dataclass(frozen=True, slots=True)
class MigrationModule:
    """
    一条已加载的迁移。

    :param package: 所属包名。
    :param revision: revision 标识符。
    :param path: 迁移文件路径。
    :param checksum: 文件源码的 sha256。
    :param depends_on: 同包内须先执行的 revision。
    :param upgrade: 升级函数。
    :param downgrade: 回退函数；未声明时为 ``None``。
    """

    package: str
    revision: str
    path: Path
    checksum: str
    depends_on: str | None
    upgrade: Callable[[MigrationContext], Awaitable[None]]
    downgrade: Callable[[MigrationContext], Awaitable[None]] | None = None


def core_migrations_dir() -> Path:
    """core 自身的迁移目录。"""
    return Path(__file__).resolve().parent / MIGRATIONS_DIRNAME


def load_migration(package: str, path: Path) -> MigrationModule:
    """
    加载一个迁移文件。

    按文件路径加载而非按包名导入：包名与目录布局在拆包前后不同，路径是唯一稳定的标识。

    :param package: 所属包名。
    :param path: 迁移文件路径。
    :return: 迁移对象。
    :raises MigrationError: 文件缺少可调用入口或元数据不合法。
    """
    key = (package, str(path))
    cached = _LOADED.get(key)
    if cached is not None:
        return cached

    spec_name = f"akari_migration_{package}_{path.stem}".replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(spec_name, path)
    if spec is None or spec.loader is None:
        raise MigrationError(f"Cannot load migration file {path}.")
    source: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)

    revision = getattr(source, "REVISION", None)
    if not isinstance(revision, str) or not revision:
        raise MigrationError(f"Migration {path} must declare a non-empty REVISION.")
    depends_on = getattr(source, "DEPENDS_ON", None)
    if depends_on is not None and not isinstance(depends_on, str):
        raise MigrationError(f"Migration {path} declares a non-string DEPENDS_ON.")
    upgrade = getattr(source, "upgrade", None)
    if not callable(upgrade):
        raise MigrationError(f"Migration {path} must define an async upgrade().")
    downgrade = getattr(source, "downgrade", None)

    loaded = MigrationModule(
        package=package,
        revision=revision,
        path=path,
        checksum=hashlib.sha256(path.read_bytes()).hexdigest(),
        depends_on=depends_on,
        upgrade=upgrade,
        downgrade=downgrade if callable(downgrade) else None,
    )
    _LOADED[key] = loaded
    return loaded


def order_migrations(package: str, modules: list[MigrationModule]) -> list[MigrationModule]:
    """
    按 ``DEPENDS_ON`` 拓扑排序，未声明依赖时按 revision 字典序。

    :param package: 包名。
    :param modules: 该包的迁移。
    :return: 可依次执行的顺序。
    :raises MigrationError: revision 重名、依赖缺失或成环。
    """
    by_revision: dict[str, MigrationModule] = {}
    for module in modules:
        if module.revision in by_revision:
            raise MigrationError(f"Duplicate revision {module.revision!r} in package {package!r}.")
        by_revision[module.revision] = module

    ordered: list[MigrationModule] = []
    done: set[str] = set()

    def visit(revision: str, chain: tuple[str, ...]) -> None:
        if revision in done:
            return
        if revision in chain:
            raise MigrationError(f"Circular dependency on revision {revision!r} in package {package!r}.")
        module = by_revision.get(revision)
        if module is None:
            # 跨包依赖无法表达，Runner 已固定 core 先于各包执行。
            raise MigrationError(
                f"Revision {revision!r} in package {package!r} depends on an unknown revision; "
                "cross-package dependencies are not supported."
            )
        if module.depends_on is not None:
            visit(module.depends_on, chain + (revision,))
        done.add(revision)
        ordered.append(module)

    for revision in sorted(by_revision):
        visit(revision, ())
    return ordered


class MigrationRunner:
    """迁移的发现、登记与执行。"""

    @classmethod
    async def discover(cls) -> dict[str, list[MigrationModule]]:
        """
        发现 core 与各模块包的迁移。

        模块包不存在时其迁移目录不存在，对应的 revision 不会被发现，其表也不会被触碰。

        :return: 包名到有序迁移列表的映射。
        """
        from core.registry import PackageRegistry

        directories: list[tuple[str, Path]] = [(CORE_PACKAGE, core_migrations_dir())]
        directories.extend(PackageRegistry.migration_dirs())
        discovered: dict[str, list[MigrationModule]] = {}
        for package, directory in directories:
            if not directory.is_dir():
                continue
            modules = [
                load_migration(package, path)
                for path in sorted(directory.glob("*.py"))
                if not path.name.startswith("_")
            ]
            discovered[package] = order_migrations(package, modules)
        return discovered

    @classmethod
    async def _applied(cls) -> dict[tuple[str, str], str | None]:
        """
        取已登记的 revision。

        :return: ``(包名, revision)`` 到 checksum 的映射。
        """
        rows = await SchemaMigration.all()
        return {(row.package, row.revision): row.checksum for row in rows}

    @classmethod
    async def pending(cls) -> dict[str, list[str]]:
        """
        取尚未应用的 revision。

        :return: 包名到待应用 revision 的映射，无待应用项时为空字典。
        """
        discovered = await cls.discover()
        applied = await cls._applied()
        pending: dict[str, list[str]] = {}
        for package, modules in discovered.items():
            revisions = [module.revision for module in modules if (package, module.revision) not in applied]
            if revisions:
                pending[package] = revisions
        return pending

    @classmethod
    def _warn_checksum_drift(cls, discovered: dict[str, list[MigrationModule]], applied: dict) -> None:
        """
        提示已应用的迁移文件被改写。

        只警告不阻断：开发期改动迁移文件是常态，阻断会制造无谓摩擦，但生产环境的静默改动
        值得一条告警。

        :param discovered: 已发现的迁移。
        :param applied: 已登记的 revision。
        """
        for package, modules in discovered.items():
            for module in modules:
                recorded = applied.get((package, module.revision))
                if recorded is not None and recorded != module.checksum:
                    Logger.warning(
                        f"Migration {package}/{module.revision} has changed since it was applied; "
                        "the database keeps the old result."
                    )

    @classmethod
    def _order(cls, discovered: dict[str, list[MigrationModule]], package: str | None) -> list[str]:
        """
        取包的执行顺序。

        core 的全部 revision 先跑完，再按包名依次执行各模块包：模块侧的绑定回填依赖 core 的
        改名与回填已完成，且各包的 revision 无法互相声明依赖。

        :param discovered: 已发现的迁移。
        :param package: 只执行该包；省略时执行全部包。
        :return: 包名列表。
        """
        if package is not None:
            if package not in discovered:
                Logger.warning(f"No migrations discovered for package {package!r}.")
                return []
            return [package]
        return [CORE_PACKAGE] + sorted(name for name in discovered if name != CORE_PACKAGE)

    @classmethod
    async def upgrade(cls, package: str | None = None) -> list[tuple[str, str]]:
        """
        执行待应用的 revision。

        :param package: 只执行该包；省略时执行全部包。
        :return: 已应用的 ``(包名, revision)`` 列表。
        """
        discovered = await cls.discover()
        applied = await cls._applied()
        cls._warn_checksum_drift(discovered, applied)
        results: list[tuple[str, str]] = []
        for name in cls._order(discovered, package):
            for migration in discovered[name]:
                if (name, migration.revision) in applied:
                    continue
                await cls._apply(migration)
                applied[(name, migration.revision)] = migration.checksum
                results.append((name, migration.revision))
        return results

    @classmethod
    async def downgrade(cls, package: str, to: str | None = None) -> list[tuple[str, str]]:
        """
        回退该包已应用的 revision。

        :param package: 包名。
        :param to: 回退到该 revision 为止（保留它）；省略时全部回退。
        :return: 已回退的 ``(包名, revision)`` 列表。
        :raises MigrationError: revision 未声明 ``downgrade``，或 ``to`` 不存在。
        """
        discovered = await cls.discover()
        modules = discovered.get(package)
        if not modules:
            Logger.warning(f"No migrations discovered for package {package!r}.")
            return []
        if to is not None and to not in {module.revision for module in modules}:
            raise MigrationError(f"Unknown target revision {to!r} in package {package!r}.")
        applied = await cls._applied()
        results: list[tuple[str, str]] = []
        for migration in reversed(modules):
            if (package, migration.revision) not in applied:
                continue
            if to is not None and migration.revision == to:
                break
            if migration.downgrade is None:
                raise MigrationError(f"Migration {package}/{migration.revision} has no downgrade().")
            Logger.info(f"Reverting migration {package}/{migration.revision}.")
            await cls._run(migration, migration.downgrade)
            await SchemaMigration.filter(package=package, revision=migration.revision).delete()
            results.append((package, migration.revision))
        return results

    @classmethod
    async def stamp(cls, package: str, revisions: list[str]) -> None:
        """
        标记 revision 为已应用而不执行。

        供旧库版本号转换与显式跳过使用。包不存在时其 revision 不会被发现，此处仍照常登记，
        以便日后装上该包时不再重放这些历史步骤。

        :param package: 包名。
        :param revisions: revision 列表。
        """
        discovered = await cls.discover()
        known = {module.revision: module for module in discovered.get(package, [])}
        applied = await cls._applied()
        for revision in revisions:
            if (package, revision) in applied:
                continue
            module = known.get(revision)
            if module is None and package in discovered:
                Logger.warning(f"Stamping unknown revision {package}/{revision}.")
            await SchemaMigration.create(
                package=package,
                revision=revision,
                checksum=module.checksum if module else None,
            )
            applied[(package, revision)] = module.checksum if module else None

    @classmethod
    async def _apply(cls, migration: MigrationModule) -> None:
        """
        执行并登记一条迁移。

        :param migration: 迁移。
        """
        Logger.info(f"Applying migration {migration.package}/{migration.revision}.")
        await cls._run(migration, migration.upgrade)
        await SchemaMigration.create(
            package=migration.package,
            revision=migration.revision,
            checksum=migration.checksum,
        )

    @classmethod
    async def _run(cls, migration: MigrationModule, entry: Callable) -> None:
        """
        在方言允许时以事务执行迁移入口。

        :param migration: 迁移。
        :param entry: 要执行的 ``upgrade`` 或 ``downgrade``。
        """
        conn = Tortoise.get_connection("default")
        if _dialect(conn) not in TRANSACTIONAL_DIALECTS:
            await entry(MigrationContext(conn))
            return
        # 事务内取到的连接由事务上下文登记，模型查询与裸 SQL 都会走同一连接。
        async with in_transaction("default") as transaction:
            await entry(MigrationContext(transaction))


async def run_startup_migrations() -> None:
    """启动期迁移入口：先转换旧版本号，再执行各包的待应用 revision。"""
    from core.database.legacy import convert_legacy_version

    await convert_legacy_version()
    applied = await MigrationRunner.upgrade()
    if applied:
        Logger.info(f"Applied {len(applied)} database migration(s).")
