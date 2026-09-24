"""配置迁移设施的端到端用例（合成包，不接启动链）。

``config/migration.py`` 有近四百行从未被任何用例执行过：``ConfigMigrationRunner``、
``iter_config_revisions()``、``stamp_config_versions()`` 在测试目录零引用。风险不是「现在坏了」，
而是首个真实消费者出现时它已经与 registry、扁平配置布局或原子写入路径脱节——那时才发现的代价
要大得多。

按既有裁决**不接启动链**（首个声明 ``config_migrations`` 的包出现时再接），只固化行为：
合成包 → revision 升级 → 版本递增 → 重载后可见 → 二次执行 no-op。
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from akaribot.core.config import migration
from akaribot.core.registry import PackageEntry, PackageManifest, PackageRegistry
from akaribot.testing import Tester, func_case

TABLE = "module_sample"
PACKAGE = "sample"

REVISION_ONE = '''"""把旧键改名。"""


def upgrade(doc, table):
    """就地迁移文档。"""
    doc["renamed"] = doc.pop("legacy_name", "fallback")
'''

REVISION_TWO = '''"""补一个默认值。"""


def upgrade(doc, table):
    """就地迁移文档。"""
    doc["added_by_two"] = table
'''


def _make_package(root: Path, *, schema_version: int = 0) -> PackageEntry:
    (root / "config.py").write_text("", encoding="utf-8")
    revisions = root / "config_migrations"
    revisions.mkdir()
    (revisions / "0001_rename.py").write_text(REVISION_ONE, encoding="utf-8")
    (revisions / "0002_add.py").write_text(REVISION_TWO, encoding="utf-8")
    return PackageEntry(
        kind="module",
        name=PACKAGE,
        dist_name=f"akari-bot-module-{PACKAGE}",
        version="0.1.0",
        import_path=f"akaribot.modules.{PACKAGE}",
        root=root,
        manifest=PackageManifest(
            config_table=TABLE,
            config_migrations="config_migrations",
            config_schema_version=schema_version,
        ),
    )


def _patches(entry: PackageEntry, config_root: Path):
    # ``PackageRegistry.modules()`` 的键是**包名**（不是 ``种类：包名``）：迁移运行器按 ``entry.name``
    # 取回自己的 revision，键写错会让整条链路静默查不到迁移。
    return (
        patch.object(PackageRegistry, "modules", lambda: {PACKAGE: entry}),
        patch.object(PackageRegistry, "adapters", lambda: {}),
        patch.object(migration, "_config_root", lambda: config_root),
        patch.object(migration, "_reload_config_manager", lambda: None),
    )


def _run_with(patches, action):
    with patches[0], patches[1], patches[2], patches[3]:
        return action()


def _write_config(config_root: Path, body: str) -> Path:
    config_root.mkdir(parents=True, exist_ok=True)
    path = config_root / f"{TABLE}.toml"
    path.write_text(body, encoding="utf-8")
    return path


def _test_revisions_are_discovered_in_order():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        patches = _patches(entry, root / "config")
        found = _run_with(patches, migration.iter_config_revisions)
    revisions = found.get(PACKAGE, [])
    return [item.number for item in revisions] == [1, 2] and revisions[0].revision == "0001_rename"


def _test_upgrade_applies_and_bumps_version():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        config_root = root / "config"
        path = _write_config(config_root, 'legacy_name = "old"\n')
        patches = _patches(entry, config_root)
        applied = _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
        text = path.read_text(encoding="utf-8")
    return (
        applied == [(PACKAGE, "0001_rename"), (PACKAGE, "0002_add")]
        and 'renamed = "old"' in text
        and f'added_by_two = "{TABLE}"' in text
        and f"{migration.CONFIG_VERSION_KEY} = 2" in text
    )


def _test_second_run_is_noop():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        config_root = root / "config"
        _write_config(config_root, 'legacy_name = "old"\n')
        patches = _patches(entry, config_root)
        first = _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
        second = _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
        pending = _run_with(patches, migration.ConfigMigrationRunner.pending)
    return len(first) == 2 and second == [] and pending == {}


def _test_pending_lists_unapplied_revisions():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        config_root = root / "config"
        _write_config(config_root, 'legacy_name = "old"\n')
        patches = _patches(entry, config_root)
        before = _run_with(patches, migration.ConfigMigrationRunner.pending)
        _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
        after = _run_with(patches, migration.ConfigMigrationRunner.pending)
    return before == {PACKAGE: ["0001_rename", "0002_add"]} and after == {}


def _test_versionless_file_starts_before_first_revision():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        config_root = root / "config"
        _write_config(config_root, 'legacy_name = "old"\n')
        patches = _patches(entry, config_root)
        applied = _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
    return [revision for _, revision in applied] == ["0001_rename", "0002_add"]


def _test_stamp_writes_schema_version():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root, schema_version=7)
        config_root = root / "config"
        path = _write_config(config_root, 'key = "value"\n')
        patches = _patches(entry, config_root)
        first = _run_with(patches, migration.stamp_config_versions)
        second = _run_with(patches, migration.stamp_config_versions)
        text = path.read_text(encoding="utf-8")
    return first == [TABLE] and second == [] and f"{migration.CONFIG_VERSION_KEY} = 7" in text


def _test_failed_revision_leaves_file_untouched():
    with tempfile.TemporaryDirectory(prefix="akari-config-migration-") as raw:
        root = Path(raw)
        entry = _make_package(root)
        broken = root / "config_migrations" / "0002_add.py"
        broken.write_text('def upgrade(doc, table):\n    raise RuntimeError("boom")\n', encoding="utf-8")
        config_root = root / "config"
        path = _write_config(config_root, 'legacy_name = "old"\n')
        patches = _patches(entry, config_root)
        applied = _run_with(patches, lambda: migration.ConfigMigrationRunner.upgrade(PACKAGE))
        text = path.read_text(encoding="utf-8")
        pending = _run_with(patches, migration.ConfigMigrationRunner.pending)
    return applied == [] and text == 'legacy_name = "old"\n' and pending == {PACKAGE: ["0001_rename", "0002_add"]}


@func_case
async def test_config_migration(tester: Tester):
    """core.config.migration: 配置迁移端到端测试"""
    await tester.test(_test_revisions_are_discovered_in_order, "迁移脚本按号段发现")
    await tester.test(_test_upgrade_applies_and_bumps_version, "应用迁移并推进版本号")
    await tester.test(_test_second_run_is_noop, "二次执行 no-op")
    await tester.test(_test_pending_lists_unapplied_revisions, "pending 列出未应用号段")
    await tester.test(_test_versionless_file_starts_before_first_revision, "无版本号文件从头迁移")
    await tester.test(_test_stamp_writes_schema_version, "stamp 写入表结构版本")
    await tester.test(_test_failed_revision_leaves_file_untouched, "脚本失败时文件保持原样")
    return tester
