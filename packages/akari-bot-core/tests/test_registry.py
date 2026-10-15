"""core.registry 发现层单元测试。"""

import tempfile
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from akaribot.core.registry import ENTRY_POINT_GROUPS, CORE_API_VERSION, PackageEntry, PackageManifest, PackageRegistry
from akaribot.testing import Tester, func_case

MANIFEST_SAMPLE = """schema = 1
requires_core_api = ">=1"
locales = "locales"
config_table = "module_sample"
config_schema_version = 3
provides_modules = ["sample", "sample-extra"]
owned_tables = ["module_sample_record"]
credential_fields = ["sample_token"]
"""


@contextmanager
def _isolated_registry(entries: dict[str, PackageEntry]):
    original_entries = PackageRegistry._entries
    original_index = PackageRegistry._by_import_path
    original_discovered = PackageRegistry._discovered
    try:
        PackageRegistry._entries = dict(entries)
        PackageRegistry._by_import_path = {entry.import_path: entry for entry in entries.values()}
        PackageRegistry._discovered = True
        yield
    finally:
        PackageRegistry._entries = original_entries
        PackageRegistry._by_import_path = original_index
        PackageRegistry._discovered = original_discovered


def _entry(kind: str, name: str, import_path: str, root: Path, **manifest_fields) -> PackageEntry:
    return PackageEntry(
        kind=kind,
        name=name,
        dist_name="",
        version="0+local",
        import_path=import_path,
        root=root,
        manifest=PackageManifest(**manifest_fields),
    )


def _test_by_import_path_uses_longest_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        short = _entry("module", "wiki", "akaribot.modules.wiki", root)
        long = _entry("module", "wikilog", "akaribot.modules.wiki.log", root)
        with _isolated_registry({"module:wiki": short, "module:wikilog": long}):
            exact = PackageRegistry.by_import_path("akaribot.modules.wiki")
            child = PackageRegistry.by_import_path("akaribot.modules.wiki.log.entry")
            unrelated = PackageRegistry.by_import_path("akaribot.modules.other.child")
            boundary = PackageRegistry.by_import_path("akaribot.modules.wikilog")
        return exact is short and child is long and unrelated is None and boundary is None


def _test_by_import_path_handles_nested_and_unknown_paths():
    with tempfile.TemporaryDirectory() as tmp:
        entry = _entry("module", "wiki", "akaribot.modules.wiki", Path(tmp))
        with _isolated_registry({"module:wiki": entry}):
            deep = PackageRegistry.by_import_path("akaribot.modules.wiki.utils.wikilib")
            shallow = PackageRegistry.by_import_path("akaribot.modules.wiki")
            unknown_root = PackageRegistry.by_import_path("os.path")
            empty = PackageRegistry.by_import_path("")
        return deep is entry and shallow is entry and unknown_root is None and empty is None


def _test_modules_and_adapters_are_separated():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        as_module = _entry("module", "web", "akaribot.modules.web", root)
        as_adapter = _entry("adapter", "web", "akaribot.adapters.web", root)
        with _isolated_registry({"module:web": as_module, "adapter:web": as_adapter}):
            modules = PackageRegistry.modules()
            adapters = PackageRegistry.adapters()
            by_adapter_path = PackageRegistry.by_import_path("akaribot.adapters.web.api")
            by_module_path = PackageRegistry.by_import_path("akaribot.modules.web")
        return (
            list(modules) == ["web"]
            and list(adapters) == ["web"]
            and by_adapter_path is as_adapter
            and by_module_path is as_module
        )


def _test_directory_scan_finds_repository_packages():
    # 已安装分发的 entry point 会先于兜底收录条目，故须显式屏蔽该路径：本用例断言的是
    # 兜底本身，结论不应取决于当前环境装没装包。
    try:
        with patch.object(PackageRegistry, "_from_entry_points", return_value=[]):
            PackageRegistry.discover(force=True)
            modules = PackageRegistry.modules()
            adapters = PackageRegistry.adapters()
    finally:
        PackageRegistry.discover(force=True)
    keys_match = all(entry.name == key for key, entry in modules.items()) and all(
        entry.name == key for key, entry in adapters.items()
    )
    scanned = all(not entry.dist_name for entry in list(modules.values()) + list(adapters.values()))
    roots_exist = all(entry.root.is_dir() for entry in list(modules.values()) + list(adapters.values()))
    return len(modules) > 0 and len(adapters) > 0 and keys_match and scanned and roots_exist


def _test_entry_points_take_precedence_over_directory_scan():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        scanned = _entry("module", "wiki", "akaribot.modules.wiki", root)
        installed = PackageEntry(
            kind="module",
            name="wiki",
            dist_name="akari-bot-module-wiki",
            version="1.2.3",
            import_path="akaribot.modules.wiki",
            root=root,
            manifest=PackageManifest(),
        )
        entries: dict[str, PackageEntry] = {}
        PackageRegistry._insert(entries, installed, source="entry point")
        PackageRegistry._insert(entries, scanned, source="directory scan")
        with _isolated_registry(entries):
            modules = PackageRegistry.modules()
        return len(modules) == 1 and modules["wiki"] is installed


def _test_manifest_defaults_when_missing():
    with tempfile.TemporaryDirectory() as tmp:
        manifest = PackageRegistry._read_manifest("akaribot.modules.sample", Path(tmp))
    return (
        manifest.schema == 1
        and manifest.requires_core_api == ">=1,<2"
        and manifest.locales == "locales"
        and manifest.assets is None
        and manifest.config_table is None
        and manifest.config_schema_version == 1
        and manifest.provides_modules == ()
        and manifest.owned_tables == ()
    )


def _test_manifest_is_read_from_package_root():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "manifest.toml").write_text(MANIFEST_SAMPLE, encoding="utf-8")
        manifest = PackageRegistry._read_manifest("akaribot.modules.sample", root)
    return (
        manifest.config_table == "module_sample"
        and manifest.config_schema_version == 3
        and manifest.provides_modules == ("sample", "sample-extra")
        and manifest.owned_tables == ("module_sample_record",)
        and manifest.credential_fields == ("sample_token",)
    )


def _test_manifest_ignores_unknown_keys():
    manifest = PackageManifest.from_mapping({"schema": 1, "not_a_field": "x", "config_table": "module_x"})
    return manifest.config_table == "module_x" and not hasattr(manifest, "not_a_field")


def _test_manifest_with_unknown_schema_falls_back_to_defaults():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "manifest.toml").write_text('schema = 99\nconfig_table = "module_x"\n', encoding="utf-8")
        manifest = PackageRegistry._read_manifest("akaribot.modules.sample", root)
    return manifest.config_table == "module_x"


def _test_locales_paths_skip_packages_without_locale_dir():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "locales").mkdir()
        present = _entry("module", "with_locales", "akaribot.modules.with_locales", root)
        absent = _entry("module", "without_locales", "akaribot.modules.without_locales", Path(tmp) / "missing")
        undeclared = _entry("module", "no_locales_field", "akaribot.modules.no_locales", root, locales=None)
        with (
            patch.object(PackageRegistry, "_core_locales_dir", return_value=None),
            _isolated_registry(
                {
                    "module:with_locales": present,
                    "module:without_locales": absent,
                    "module:no_locales_field": undeclared,
                }
            ),
        ):
            paths = PackageRegistry.locales_paths()
    return paths == [str(root / "locales")]


def _test_config_template_paths_follow_file_existence():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "config.py").write_text("", encoding="utf-8")
        has_template = _entry("module", "has_template", "akaribot.modules.has_template", root)
        no_template = _entry("module", "no_template", "akaribot.modules.no_template", Path(tmp) / "other")
        with _isolated_registry({"module:has_template": has_template, "module:no_template": no_template}):
            names = PackageRegistry.config_template_paths()
    return names == ["akaribot.core.config.base", "akaribot.modules.has_template.config"]


def _test_import_roots_cover_registered_packages():
    PackageRegistry.discover(force=True)
    module_roots = PackageRegistry.import_roots("module")
    adapter_roots = PackageRegistry.import_roots("adapter")
    entry_groups_match = set(ENTRY_POINT_GROUPS.values()) == {"akaribot.modules", "akaribot.adapters"}
    return module_roots == {"akaribot.modules"} and adapter_roots == {"akaribot.adapters"} and entry_groups_match


def _test_core_api_version_is_declared():
    return isinstance(CORE_API_VERSION, int) and CORE_API_VERSION >= 1


def _test_frozen_registry_takes_precedence():
    frozen = {
        "module:frozen": PackageEntry(
            kind="module",
            name="frozen",
            dist_name="akari-bot-module-frozen",
            version="1.0.0",
            import_path="akaribot.modules.frozen",
            root=Path("."),
            manifest=PackageManifest(),
        )
    }
    with patch.object(PackageRegistry, "_load_frozen", return_value=frozen):
        PackageRegistry.discover(force=True)
        modules = PackageRegistry.modules()
    PackageRegistry.discover(force=True)
    return list(modules) == ["frozen"]


def _test_package_data_is_per_kind_and_name():
    with tempfile.TemporaryDirectory() as tmp:
        entry = _entry("module", "sample", "akaribot.modules.sample", Path(tmp))
        with patch.object(PackageRegistry, "_instance_data_root", return_value=Path("/instance/data")):
            directory = PackageRegistry.package_data(entry)
    return directory == Path("/instance/data/module/sample")


def _test_package_data_uses_instance_data_root():
    from akaribot.core.paths import Paths

    with tempfile.TemporaryDirectory() as tmp:
        entry = _entry("module", "sample", "akaribot.modules.sample", Path(tmp))
        directory = PackageRegistry.package_data(entry)
    return directory == Paths.data / "module" / "sample" and Paths.data.name == "data"


def _test_package_assets_follows_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        declared = _entry("module", "declared", "akaribot.modules.declared", root, assets="assets")
        undeclared = _entry("module", "undeclared", "akaribot.modules.undeclared", root)
        with _isolated_registry({"module:declared": declared, "module:undeclared": undeclared}):
            with_manifest = PackageRegistry.package_assets("declared")
            without_manifest = PackageRegistry.package_assets(undeclared)
    return with_manifest == root / "assets" and without_manifest == root


def _test_incompatible_packages_are_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        compatible = _entry("module", "compatible", "akaribot.modules.compatible", root, requires_core_api=">=1")
        incompatible = _entry("module", "incompatible", "akaribot.modules.incompatible", root, requires_core_api=">=99")
        original = PackageRegistry._incompatible
        try:
            with _isolated_registry({"module:compatible": compatible, "module:incompatible": incompatible}):
                rejected = PackageRegistry.reject_incompatible()
                remaining = PackageRegistry.modules()
                unresolved = PackageRegistry.by_import_path("akaribot.modules.incompatible.sub")
                reported = PackageRegistry.report_lines()
        finally:
            PackageRegistry._incompatible = original
    return (
        list(rejected) == ["incompatible"]
        and list(remaining) == ["compatible"]
        and unresolved is None
        and reported == [f"incompatible: {rejected['incompatible']}"]
    )


def _test_unparsable_api_specifier_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        broken = _entry("module", "broken", "akaribot.modules.broken", Path(tmp), requires_core_api="not a specifier")
        original = PackageRegistry._incompatible
        try:
            with _isolated_registry({"module:broken": broken}):
                rejected = PackageRegistry.reject_incompatible()
        finally:
            PackageRegistry._incompatible = original
    return list(rejected) == ["broken"] and "unparsable" in rejected["broken"]


def _test_compatible_packages_are_kept():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        entries = {
            "module:any": _entry("module", "any", "akaribot.modules.any", root, requires_core_api=">=1,<2"),
            "module:default": _entry("module", "default", "akaribot.modules.default", root),
        }
        original = PackageRegistry._incompatible
        try:
            with _isolated_registry(entries):
                rejected = PackageRegistry.reject_incompatible()
                remaining = sorted(PackageRegistry.modules())
        finally:
            PackageRegistry._incompatible = original
    return not rejected and remaining == ["any", "default"]


def _test_import_index_is_order_independent():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        scanned = _entry("module", "sample", "akaribot.modules.sample", root)
        installed = replace(
            _entry("module", "sample-alias", "akaribot.modules.sample", root),
            dist_name="akari-bot-module-sample",
        )
        original_index = PackageRegistry._by_import_path
        winners = []
        try:
            for ordered in ({"a": scanned, "b": installed}, {"a": installed, "b": scanned}):
                PackageRegistry._rebuild_import_index(ordered)
                winners.append(PackageRegistry._by_import_path["akaribot.modules.sample"])
        finally:
            # 重建写的是全局索引，不还原会让同进程后续用例（如 test_rpc_contracts 依赖的
            # by_import_path("…wiki")）拿到残缺注册表，报出与本次改动无关的失败。
            PackageRegistry._by_import_path = original_index
    return winners == [installed, installed]


def _test_reject_incompatible_rebuilds_index_with_same_rule():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        installed = replace(
            _entry("module", "sample", "akaribot.modules.sample", root),
            dist_name="akari-bot-module-sample",
        )
        scanned = _entry("module", "sample-alias", "akaribot.modules.sample", root)
        outdated = _entry("module", "outdated", "akaribot.modules.outdated", root, requires_core_api=">=99")
        entries = {"module:sample": installed, "module:sample-alias": scanned, "module:outdated": outdated}
        original = PackageRegistry._incompatible
        try:
            with _isolated_registry(entries):
                PackageRegistry.reject_incompatible()
                winner = PackageRegistry._by_import_path["akaribot.modules.sample"]
        finally:
            PackageRegistry._incompatible = original
    return winner is installed


def _test_locales_paths_are_order_independent():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name in ("zulu", "alpha", "mike"):
            (root / name / "locales").mkdir(parents=True)
        entries = {
            "module:zulu": _entry("module", "zulu", "akaribot.modules.zulu", root / "zulu"),
            "module:alpha": _entry("module", "alpha", "akaribot.modules.alpha", root / "alpha"),
            "adapter:mike": _entry("adapter", "mike", "akaribot.adapters.mike", root / "mike"),
        }
        orders = [
            entries,
            {key: entries[key] for key in reversed(list(entries))},
            {key: entries[key] for key in ("module:alpha", "adapter:mike", "module:zulu")},
        ]
        results = []
        with patch.object(PackageRegistry, "_core_locales_dir", return_value=None):
            for ordered in orders:
                with _isolated_registry(ordered):
                    results.append(PackageRegistry.locales_paths())
    expected = [str(root / "mike" / "locales"), str(root / "alpha" / "locales"), str(root / "zulu" / "locales")]
    return results == [expected, expected, expected]


@func_case
async def test_registry(tester: Tester):
    """core.registry: 发现层测试"""
    await tester.test(_test_by_import_path_uses_longest_prefix, "前缀匹配取最长者")
    await tester.test(_test_by_import_path_handles_nested_and_unknown_paths, "嵌套路径与未知路径解析")
    await tester.test(_test_modules_and_adapters_are_separated, "同名模块与适配器按种类区分")
    await tester.test(_test_directory_scan_finds_repository_packages, "目录扫描找出仓库内的包")
    await tester.test(_test_entry_points_take_precedence_over_directory_scan, "entry point 优先于目录扫描")
    await tester.test(_test_manifest_defaults_when_missing, "无 manifest 时取默认清单")
    await tester.test(_test_manifest_is_read_from_package_root, "manifest 按字段读取")
    await tester.test(_test_manifest_ignores_unknown_keys, "manifest 未知键被忽略")
    await tester.test(_test_manifest_with_unknown_schema_falls_back_to_defaults, "manifest 结构版本不认识时降级")
    await tester.test(_test_locales_paths_skip_packages_without_locale_dir, "缺 locale 目录的包不收录路径")
    await tester.test(_test_config_template_paths_follow_file_existence, "配置模板按文件存在判断")
    await tester.test(_test_import_roots_cover_registered_packages, "顶层段覆盖已注册包")
    await tester.test(_test_core_api_version_is_declared, "公共 API 版本已声明")
    await tester.test(_test_frozen_registry_takes_precedence, "frozen registry 优先")
    await tester.test(_test_package_data_is_per_kind_and_name, "包数据目录按种类与包名分层")
    await tester.test(_test_package_data_uses_instance_data_root, "包数据目录取实例 data")
    await tester.test(_test_package_assets_follows_manifest, "包静态资源目录取 manifest.assets")
    await tester.test(_test_incompatible_packages_are_rejected, "API 不兼容的包被拒绝注册")
    await tester.test(_test_unparsable_api_specifier_is_rejected, "描述符不可解析时拒绝注册")
    await tester.test(_test_compatible_packages_are_kept, "API 兼容的包保留注册")
    await tester.test(_test_import_index_is_order_independent, "导入路径索引与条目顺序无关")
    await tester.test(_test_reject_incompatible_rebuilds_index_with_same_rule, "API 门槛补做后按同规则重建索引")
    await tester.test(_test_locales_paths_are_order_independent, "locale 搜索路径与条目顺序无关")
    return tester
