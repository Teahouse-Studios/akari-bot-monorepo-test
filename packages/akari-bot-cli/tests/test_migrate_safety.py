import json
import sqlite3
import tempfile
import tomllib
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import migrate
from akaribot.cli.instance import CliError, Instance, InstanceMeta
from akaribot.cli.venv import RegistryCatalog, RegistryEntry
from akaribot.testing import Tester, func_case


def _legacy(root: Path, *, database: Path | None = None, link: str | None = None):
    root = root.resolve()
    for name in ("core", "modules", "config", "database"):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "bot.py").touch()
    (root / ".bot.lock").touch()
    database = database or root / "database" / "save.db"
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE module_status (module_name TEXT, load INTEGER)")
        connection.execute("INSERT INTO module_status VALUES ('dice', 1)")
        connection.execute("CREATE TABLE marker (value TEXT)")
        connection.execute("INSERT INTO marker VALUES ('source')")
    config = 'default_locale = "en_us"\nconfig_version = 6\n[config]\n[secret]\n'
    config += "db_path = " + json.dumps(link or f"sqlite://{database}") + "\n"
    (root / "config" / "config.toml").write_text(config, encoding="utf-8")
    return root


def _contents(root: Path):
    return {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def _instance(root: Path):
    Instance.create_dirs(root)
    InstanceMeta.create(root, venv="").save()
    return Instance(root)


def _copy(legacy: migrate.LegacyProject, instance: Instance, *, force: bool = False, dry_run: bool = False):
    log = migrate.MigrationLog()
    migrate._copy_payload(legacy, instance, force=force, dry_run=dry_run, log=log)
    return log


def _target_database(instance: Instance):
    config = tomllib.loads((instance.config_dir / "config.toml").read_text(encoding="utf-8"))
    return migrate._sqlite_database_file(instance.root, config["secret"]["db_path"])


def _catalog():
    entry = RegistryEntry(name="dice", dist="akari-bot-module-dice", kind="module", provides_modules=("dice",))
    return RegistryCatalog(entries={entry.dist: entry})


def _test_top_level_locale_and_secret_database():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        legacy = migrate._inspect(root)
        return legacy.locale == "en_us" and legacy.database_file == root / "database" / "save.db"


def _test_current_data_and_historical_fallback():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        contents = {
            "data/private/default/state.txt": "private",
            "data/filter_words/custom.txt": "filter",
            "data/url_audit/allowlist/user.txt": "current",
            "data/retired/accounts.json": "retired",
            "data/union_merge_logs/log.json": "union",
            "assets/url_audit/allowlist/user.txt": "historical",
            "assets/private/default/extra.txt": "extra",
            "modules/dice/data/state.txt": "module",
            "modules/dice/__init__.py": "",
        }
        for name, value in contents.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
        before = _contents(root)
        instance = _instance(Path(temporary) / "new")
        _copy(migrate._inspect(root), instance, force=True)
        copied = _contents(instance.root)
        return (
            all(copied[Path(name)].decode() == value for name, value in contents.items() if name.startswith("data/"))
            and copied[Path("data/private/default/extra.txt")] == b"extra"
            and copied[Path("data/module/dice/state.txt")] == b"module"
            and before == _contents(root)
        )


def _test_wal_snapshot_keeps_source_files_unchanged():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        database = root / "database" / "save.db"
        with sqlite3.connect(database) as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA wal_autocheckpoint=0")
            connection.execute("INSERT INTO marker VALUES ('wal')")
            connection.commit()
            before = _contents(root)
            instance = _instance(Path(temporary) / "new")
            _copy(migrate._inspect(root), instance)
            with sqlite3.connect(_target_database(instance)) as destination:
                rows = destination.execute("SELECT value FROM marker ORDER BY rowid").fetchall()
            return rows == [("source",), ("wal",)] and before == _contents(root)


def _test_absolute_database_isolated_before_upgrade():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        before = _contents(root)
        instance = _instance(Path(temporary) / "new")
        _copy(migrate._inspect(root), instance)
        completed = instance.run_core_capture(
            "db", "upgrade", "--package", "akari-bot-core", "--json", AKARI_CONFIG_PATH=str(instance.config_dir)
        )
        with sqlite3.connect(_target_database(instance)) as destination:
            migrated = destination.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0]
        return completed.returncode == 0 and migrated > 0 and before == _contents(root)


def _test_custom_external_sqlite_file_is_copied():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        database = Path(temporary) / "shared" / "custom.sqlite"
        root = _legacy(Path(temporary) / "old", database=database)
        before = database.read_bytes()
        instance = _instance(Path(temporary) / "new")
        _copy(migrate._inspect(root), instance)
        target = _target_database(instance)
        with sqlite3.connect(target) as destination:
            destination.execute("INSERT INTO marker VALUES ('target')")
        return target == instance.root / "database/external/custom.sqlite" and database.read_bytes() == before


def _test_external_backend_rejected_before_writes():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old", link="mysql://user:secret@db.example/source")
        target = Path(temporary) / "new"
        before = _contents(root)
        with patch.object(migrate, "_load_catalog") as catalog, patch.object(migrate, "_install_packages") as install:
            result = CliRunner().invoke(migrate.app, [str(root), "--instance", str(target)])
        return (
            result.exit_code != 0
            and not target.exists()
            and not catalog.called
            and not install.called
            and (before == _contents(root))
        )


def _test_running_source_rejected_before_writes():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        target = Path(temporary) / "new"
        with patch.object(Instance, "is_running", return_value=True), patch.object(migrate, "_load_catalog") as catalog:
            result = CliRunner().invoke(migrate.app, [str(root), "--instance", str(target)])
        return result.exit_code != 0 and not target.exists() and not catalog.called


def _test_skip_install_does_not_upgrade():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        target = Path(temporary) / "new"
        with (
            patch.object(migrate, "_load_catalog", return_value=_catalog()),
            patch.object(migrate, "_convert_database") as upgrade,
            patch.object(migrate, "_install_packages") as install,
        ):
            result = CliRunner().invoke(migrate.app, [str(root), "--instance", str(target), "--skip-install"])
        return (
            result.exit_code == 0
            and not upgrade.called
            and not install.called
            and (_target_database(Instance(target)).is_relative_to(target.resolve()))
        )


def _test_dry_run_is_read_only():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        target = Path(temporary) / "new"
        before = _contents(root)
        with patch.object(migrate, "_load_catalog", return_value=_catalog()):
            result = CliRunner().invoke(migrate.app, [str(root), "--instance", str(target), "--dry-run"])
        return result.exit_code == 0 and not target.exists() and before == _contents(root)


def _test_existing_target_database_is_preserved():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        legacy = migrate._inspect(root)
        instance = _instance(Path(temporary) / "new")
        _copy(legacy, instance)
        database = _target_database(instance)
        with sqlite3.connect(database) as destination:
            destination.execute("INSERT INTO marker VALUES ('target')")
        _copy(legacy, instance)
        with sqlite3.connect(database) as destination:
            rows = destination.execute("SELECT value FROM marker ORDER BY rowid").fetchall()
        return rows == [("source",), ("target",)]


def _test_database_symlink_to_source_is_rejected():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        instance = _instance(Path(temporary) / "new")
        target = instance.root / "database" / "save.db"
        try:
            target.symlink_to(root / "database" / "save.db")
        except OSError:
            return True
        try:
            _copy(migrate._inspect(root), instance)
        except CliError:
            return True
        return False


def _test_source_lock_held_during_snapshot():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        legacy = migrate._inspect(root)
        instance = _instance(Path(temporary) / "new")
        snapshot = migrate._snapshot_database
        held = []

        def observe(*args, **kwargs):
            held.append(Instance.detached(root).is_running())
            return snapshot(*args, **kwargs)

        with patch.object(migrate, "_snapshot_database", side_effect=observe):
            _copy(legacy, instance)
        return held == [True] and not Instance.detached(root).is_running()


def _test_missing_source_lock_does_not_create_files():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        (root / ".bot.lock").unlink()
        before = _contents(root)
        target = Path(temporary) / "new"
        result = CliRunner().invoke(migrate.app, [str(root), "--instance", str(target)])
        return result.exit_code != 0 and not target.exists() and before == _contents(root)


def _test_target_configuration_database_preserved():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        legacy = migrate._inspect(root)
        instance = _instance(Path(temporary) / "new")
        _copy(legacy, instance)
        config = instance.config_dir / "config.toml"
        before = config.read_bytes()
        _copy(legacy, instance)
        return config.read_bytes() == before


def _test_conflicting_target_database_rejected_before_copy():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        legacy = migrate._inspect(root)
        instance = _instance(Path(temporary) / "new")
        (instance.config_dir / "config.toml").write_text(
            '[secret]\ndb_path = "sqlite://database/custom.db"\n', encoding="utf-8"
        )
        before = _contents(instance.root)
        try:
            _copy(legacy, instance)
        except CliError:
            return before == _contents(instance.root)
        return False


def _test_target_data_symlink_cannot_write_source():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        path = root / "data" / "private" / "state.txt"
        path.parent.mkdir(parents=True)
        path.write_text("source", encoding="utf-8")
        legacy = migrate._inspect(root)
        instance = _instance(Path(temporary) / "new")
        try:
            (instance.root / "data" / "private").symlink_to(path.parent, target_is_directory=True)
        except OSError:
            return True
        before = _contents(root)
        try:
            _copy(legacy, instance, force=True)
        except CliError:
            return before == _contents(root)
        return False


def _test_target_database_hardlink_cannot_modify_source():
    with tempfile.TemporaryDirectory(prefix="akari-migrate-") as temporary:
        root = _legacy(Path(temporary) / "old")
        instance = _instance(Path(temporary) / "new")
        source = root / "database" / "save.db"
        target = instance.root / "database" / "save.db"
        try:
            target.hardlink_to(source)
        except OSError:
            return True
        before = _contents(root)
        try:
            _copy(migrate._inspect(root), instance)
        except CliError:
            return before == _contents(root)
        return False


@func_case
async def test_migrate_safety(tester: Tester):
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")
    await tester.test(_test_top_level_locale_and_secret_database, "读取顶层语言与密钥数据库地址")
    await tester.test(_test_current_data_and_historical_fallback, "迁移现行 data 与历史回退资源且保留源文件")
    await tester.test(_test_wal_snapshot_keeps_source_files_unchanged, "SQLite 快照包含 WAL 且源文件不变")
    await tester.test(_test_absolute_database_isolated_before_upgrade, "绝对数据库地址隔离后升级仅作用于副本")
    await tester.test(_test_custom_external_sqlite_file_is_copied, "外部 SQLite 文件复制到目标实例")
    await tester.test(_test_external_backend_rejected_before_writes, "外部数据库在写入与安装前被拒绝")
    await tester.test(_test_running_source_rejected_before_writes, "运行中的源项目在写入前被拒绝")
    await tester.test(_test_skip_install_does_not_upgrade, "只搬文件时不安装或升级数据库")
    await tester.test(_test_dry_run_is_read_only, "迁移预演不修改源或目标")
    await tester.test(_test_existing_target_database_is_preserved, "重复迁移保留目标数据库")
    await tester.test(_test_database_symlink_to_source_is_rejected, "目标数据库指向源库时拒绝迁移")
    await tester.test(_test_source_lock_held_during_snapshot, "数据库快照期间持有源项目排他锁")
    await tester.test(_test_missing_source_lock_does_not_create_files, "缺少源锁时拒绝迁移且不创建文件")
    await tester.test(_test_target_configuration_database_preserved, "重复迁移不改目标数据库配置")
    await tester.test(_test_conflicting_target_database_rejected_before_copy, "目标数据库冲突在复制前被拒绝")
    await tester.test(_test_target_data_symlink_cannot_write_source, "目标数据符号链接无法写入源项目")
    await tester.test(_test_target_database_hardlink_cannot_modify_source, "目标数据库硬链接无法修改源数据库")
    return tester
