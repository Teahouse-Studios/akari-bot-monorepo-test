"""core.registry 发现层单元测试。"""

import tempfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from core.registry import ENTRY_POINT_GROUPS, CORE_API_VERSION, PackageEntry, PackageManifest, PackageRegistry
from core.tester import Tester, func_case

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
    """以给定条目替换发现结果，退出时还原。

    :param entries: 新的条目映射，键为 ``种类:包名``。
    :return: 上下文管理器。
    """
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
    """构造测试用条目。

    :param kind: 包种类。
    :param name: 包名。
    :param import_path: 导入路径。
    :param root: 包根目录。
    :param manifest_fields: 清单字段覆盖项。
    :return: 条目。
    """
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
    """前缀匹配须取最长者，而非先命中者。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        short = _entry("module", "wiki", "modules.wiki", root)
        long = _entry("module", "wikilog", "modules.wiki.log", root)
        with _isolated_registry({"module:wiki": short, "module:wikilog": long}):
            exact = PackageRegistry.by_import_path("modules.wiki")
            child = PackageRegistry.by_import_path("modules.wiki.log.entry")
            unrelated = PackageRegistry.by_import_path("modules.other.child")
            boundary = PackageRegistry.by_import_path("modules.wikilog")
        return exact is short and child is long and unrelated is None and boundary is None


def _test_by_import_path_handles_nested_and_unknown_paths():
    """嵌套模块解析到所属包，未知路径返回 None。"""
    with tempfile.TemporaryDirectory() as tmp:
        entry = _entry("module", "wiki", "modules.wiki", Path(tmp))
        with _isolated_registry({"module:wiki": entry}):
            deep = PackageRegistry.by_import_path("modules.wiki.utils.wikilib")
            shallow = PackageRegistry.by_import_path("modules.wiki")
            unknown_root = PackageRegistry.by_import_path("os.path")
            empty = PackageRegistry.by_import_path("")
        return deep is entry and shallow is entry and unknown_root is None and empty is None


def _test_modules_and_adapters_are_separated():
    """同名包按种类区分，互不覆盖。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        as_module = _entry("module", "web", "modules.web", root)
        as_adapter = _entry("adapter", "web", "bots.web", root)
        with _isolated_registry({"module:web": as_module, "adapter:web": as_adapter}):
            modules = PackageRegistry.modules()
            adapters = PackageRegistry.adapters()
            by_adapter_path = PackageRegistry.by_import_path("bots.web.api")
            by_module_path = PackageRegistry.by_import_path("modules.web")
        return (
            list(modules) == ["web"]
            and list(adapters) == ["web"]
            and by_adapter_path is as_adapter
            and by_module_path is as_module
        )


def _test_directory_scan_finds_repository_packages():
    """目录扫描兜底须找出仓库内的全部模块与适配器，且键与包名一致。"""
    PackageRegistry.discover(force=True)
    modules = PackageRegistry.modules()
    adapters = PackageRegistry.adapters()
    keys_match = all(entry.name == key for key, entry in modules.items()) and all(
        entry.name == key for key, entry in adapters.items()
    )
    scanned = all(not entry.dist_name for entry in list(modules.values()) + list(adapters.values()))
    roots_exist = all(entry.root.is_dir() for entry in list(modules.values()) + list(adapters.values()))
    return len(modules) > 0 and len(adapters) > 0 and keys_match and scanned and roots_exist


def _test_entry_points_take_precedence_over_directory_scan():
    """同一包同时来自 entry point 与目录扫描时，entry point 胜出且不重复计数。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        scanned = _entry("module", "wiki", "modules.wiki", root)
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
    """包内无 manifest 时取全默认值，与拆包前的现状等价。"""
    with tempfile.TemporaryDirectory() as tmp:
        manifest = PackageRegistry._read_manifest("modules.sample", Path(tmp))
    return (
        manifest.schema == 1
        and manifest.requires_core_api == ">=1"
        and manifest.locales == "locales"
        and manifest.assets is None
        and manifest.config_table is None
        and manifest.config_schema_version == 1
        and manifest.provides_modules == ()
        and manifest.owned_tables == ()
    )


def _test_manifest_is_read_from_package_root():
    """manifest 存在时按字段读取，序列字段转为元组。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "manifest.toml").write_text(MANIFEST_SAMPLE, encoding="utf-8")
        manifest = PackageRegistry._read_manifest("modules.sample", root)
    return (
        manifest.config_table == "module_sample"
        and manifest.config_schema_version == 3
        and manifest.provides_modules == ("sample", "sample-extra")
        and manifest.owned_tables == ("module_sample_record",)
        and manifest.credential_fields == ("sample_token",)
    )


def _test_manifest_ignores_unknown_keys():
    """未知键不得进入清单，也不得使读取失败。"""
    manifest = PackageManifest.from_mapping({"schema": 1, "not_a_field": "x", "config_table": "module_x"})
    return manifest.config_table == "module_x" and not hasattr(manifest, "not_a_field")


def _test_manifest_with_unknown_schema_falls_back_to_defaults():
    """结构版本不认识时仍走默认清单，不抛异常。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "manifest.toml").write_text('schema = 99\nconfig_table = "module_x"\n', encoding="utf-8")
        manifest = PackageRegistry._read_manifest("modules.sample", root)
    return manifest.config_table == "module_x"


def _test_locales_paths_skip_packages_without_locale_dir():
    """manifest 声明了 locales 但目录不存在时不收录该路径。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "locales").mkdir()
        present = _entry("module", "with_locales", "modules.with_locales", root)
        absent = _entry("module", "without_locales", "modules.without_locales", Path(tmp) / "missing")
        undeclared = _entry("module", "no_locales_field", "modules.no_locales", root, locales=None)
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
    """配置模板按文件是否存在判断，不导入包。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "config.py").write_text("", encoding="utf-8")
        has_template = _entry("module", "has_template", "modules.has_template", root)
        no_template = _entry("module", "no_template", "modules.no_template", Path(tmp) / "other")
        with _isolated_registry({"module:has_template": has_template, "module:no_template": no_template}):
            names = PackageRegistry.config_template_paths()
    return names == ["core.config.base", "modules.has_template.config"]


def _test_import_roots_cover_registered_packages():
    """顶层段由已注册包导出，供裸包导入的展开使用。"""
    PackageRegistry.discover(force=True)
    module_roots = PackageRegistry.import_roots("module")
    adapter_roots = PackageRegistry.import_roots("adapter")
    entry_groups_match = set(ENTRY_POINT_GROUPS.values()) == {"akaribot.modules", "akaribot.adapters"}
    return module_roots == {"modules"} and adapter_roots == {"bots"} and entry_groups_match


def _test_core_api_version_is_declared():
    """公共 API 版本已声明，供 manifest 的兼容性校验使用。"""
    return isinstance(CORE_API_VERSION, int) and CORE_API_VERSION >= 1


def _test_frozen_registry_takes_precedence():
    """存在 frozen registry 时直接采用其中清单，不再做 entry point 与目录扫描。"""
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


def _test_data_dir_is_per_kind_and_name():
    """数据目录按种类与包名分层。"""
    with tempfile.TemporaryDirectory() as tmp:
        entry = _entry("module", "sample", "modules.sample", Path(tmp))
        with patch.object(PackageRegistry, "_instance_data_root", return_value=Path("/instance/data")):
            directory = PackageRegistry.data_dir(entry)
    return directory == Path("/instance/data/module/sample")


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
    await tester.test(_test_data_dir_is_per_kind_and_name, "数据目录按种类与包名分层")
    return tester
