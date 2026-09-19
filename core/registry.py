"""模块与适配器的统一发现层。

本模块回答「系统里有哪些模块与适配器」，是全仓唯一的答案来源。发现结果按
「entry point 优先、目录扫描兜底」的顺序合成：

1. 存在 ``core/_frozen_registry.py`` 时直接使用，不再继续（二进制构建产物，尚未生成）；
2. ``importlib.metadata.entry_points()`` 枚举已安装分发的 entry point；
3. 兜底扫描仓库内的 ``modules/`` 与 ``bots/`` 目录，合成 ``dist_name`` 为空的条目；
4. 两者按条目名去重，entry point 胜出，冲突时记录警告。

拆包之前第 3 条是主路径；拆包之后各包以 wheel 安装，第 2 条接管，本模块之外的
代码不需要改动。
"""

from __future__ import annotations

import importlib
import importlib.metadata
import importlib.resources
import sys
import tomllib
from dataclasses import dataclass, fields as dataclass_fields
from pathlib import Path
from typing import Any, Literal

ENTRY_POINT_GROUPS: dict[str, str] = {"module": "akaribot.modules", "adapter": "akaribot.adapters"}

# 二进制构建产物。存在时 discover() 直接采用其中记录的清单，跳过 entry point 与目录扫描。
FROZEN_REGISTRY_MODULE = "core._frozen_registry"

# 包内 manifest 的文件名与版本。
MANIFEST_FILENAME = "manifest.toml"
MANIFEST_SCHEMA = 1

# core 公共 API 的版本。模块与适配器通过 manifest 的 requires_core_api 声明所需区间；
# 该版本的正式发布与校验闸门在公共 API 契约阶段建立。
CORE_API_VERSION = 1

PackageKind = Literal["module", "adapter"]


class RegistryError(RuntimeError):
    """发现层无法产出可用清单时抛出。"""


def _logger():
    """惰性取得日志器。

    不能在模块层导入 core.logger：core.logger 会经 core.config.base 引入整个配置系统，
    而配置系统在导入期校验配置文件存在并执行版本迁移。发现层必须能在配置就绪之前使用
    （locale 目录的收集就发生在配置加载之前），因此把这条依赖推迟到真正要写日志时。
    """
    from core.logger import Logger

    return Logger


@dataclass(frozen=True, slots=True)
class PackageManifest:
    """包的元数据声明。

    全部字段都有默认值：拆包之前没有任何包带 manifest，缺失即等价于现状。

    :param schema: manifest 自身的结构版本。
    :param requires_core_api: 所需的 core 公共 API 区间，PEP 440 描述符。
    :param locales: 包内 locale 目录的相对路径；``None`` 表示该包不提供文案。
    :param assets: 包内只读静态资源的相对路径；``None`` 表示不提供。
    :param migrations: 数据库迁移目录的相对路径；``None`` 表示无迁移。
    :param config_migrations: 配置迁移目录的相对路径；``None`` 表示无配置迁移。
    :param config_table: 配置文件中的表名，如 ``module_wiki``；``None`` 表示无配置。
    :param config_schema_version: 该包配置的表结构版本。核心配置的版本另记于 config.toml。
    :param provides_modules: 该包注册的模块名；空元组表示只有运行时才知道。
    :param owned_tables: 该包拥有的数据表，供数据清理使用。
    :param credential_fields: 该包配置中属于凭据的字段名，供重复凭据检查使用。
    """

    schema: int = MANIFEST_SCHEMA
    requires_core_api: str = ">=1"
    locales: str | None = "locales"
    assets: str | None = None
    migrations: str | None = None
    config_migrations: str | None = None
    config_table: str | None = None
    config_schema_version: int = 1
    provides_modules: tuple[str, ...] = ()
    owned_tables: tuple[str, ...] = ()
    credential_fields: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, data: dict[str, Any], *, source: str = "") -> "PackageManifest":
        """由 manifest 的内容构造，忽略未声明的键。

        :param data: 解析后的 TOML 内容。
        :param source: 出错时用于定位的来源描述。
        :return: 清单对象。
        """
        known = {field.name for field in dataclass_fields(cls)}
        unknown = sorted(set(data) - known)
        if unknown:
            _logger().warning(f"Manifest {source} has unknown keys: {', '.join(unknown)}")
        payload = {key: value for key, value in data.items() if key in known}
        for key in ("provides_modules", "owned_tables", "credential_fields"):
            if key in payload:
                payload[key] = tuple(payload[key])
        return cls(**payload)


@dataclass(frozen=True, slots=True)
class PackageEntry:
    """一个已发现的模块包或适配器包。

    :param kind: 包的种类。
    :param name: 包名，取自 entry point 名或目录名，如 ``wiki`` / ``qqbot``。
    :param dist_name: 分发名，如 ``akari-bot-module-wiki``；目录扫描兜底时为空串。
    :param version: 已安装分发的版本；目录扫描兜底时为 ``0+local``。
    :param import_path: 导入路径，如 ``modules.wiki``；拆包后为 ``akaribot.modules.wiki``。
    :param root: 包根目录。
    :param manifest: 包元数据。
    :param editable: 是否为可编辑安装。
    """

    kind: PackageKind
    name: str
    dist_name: str
    version: str
    import_path: str
    root: Path
    manifest: PackageManifest
    editable: bool = False

    @property
    def stem(self) -> str:
        """包名。目录扫描与 entry point 两条路径下取值一致。"""
        return self.name


class PackageRegistry:
    """模块与适配器的发现结果缓存。

    发现结果在进程内缓存一次，``discover(force=True)`` 用于安装或卸载包之后重建。
    """

    _entries: dict[str, PackageEntry] = {}
    _by_import_path: dict[str, PackageEntry] = {}
    _discovered: bool = False
    _incompatible: dict[str, str] = {}

    @classmethod
    def discover(cls, *, force: bool = False) -> None:
        """建立发现结果。

        :param force: 为真时忽略缓存并重新发现。
        """
        if cls._discovered and not force:
            return

        entries: dict[str, PackageEntry] = {}
        frozen = cls._load_frozen()
        if frozen is not None:
            entries = frozen
        else:
            for kind, group in ENTRY_POINT_GROUPS.items():
                for entry in cls._from_entry_points(kind, group):
                    cls._insert(entries, entry, source="entry point")
            for entry in cls._from_directory_scan():
                cls._insert(entries, entry, source="directory scan")

        cls._entries = entries
        cls._by_import_path = {}
        for entry in entries.values():
            current = cls._by_import_path.get(entry.import_path)
            if current is None or cls._is_more_specific(entry, current):
                cls._by_import_path[entry.import_path] = entry
        cls._discovered = True

    @staticmethod
    def _is_more_specific(candidate: PackageEntry, current: PackageEntry) -> bool:
        """同名导入路径冲突时，取 dist_name 非空者。"""
        return bool(candidate.dist_name) and not current.dist_name

    @classmethod
    def _insert(cls, entries: dict[str, PackageEntry], entry: PackageEntry, *, source: str) -> None:
        """按键写入条目，已存在时保留先写入者并记录冲突。

        :param entries: 待填充的映射。
        :param entry: 新条目。
        :param source: 冲突信息中用于指明来源的描述。
        """
        key = cls._key(entry)
        existing = entries.get(key)
        if existing is None:
            entries[key] = entry
            return
        if existing.dist_name == entry.dist_name and existing.import_path == entry.import_path:
            return
        _logger().warning(
            f"Duplicate package {key!r} from {source}: keeping {existing.import_path!r}, "
            f"ignoring {entry.import_path!r}."
        )

    @staticmethod
    def _key(entry: PackageEntry) -> str:
        """条目在注册表中的唯一键。模块与适配器可能同名，需带种类区分。"""
        return f"{entry.kind}:{entry.name}"

    @classmethod
    def incompatible(cls) -> dict[str, str]:
        """core 公共 API 不兼容的包。

        仅收录已发现的包；被拒绝注册的包不进入 :meth:`modules` 与 :meth:`adapters`，
        但在此可见，供启动提示与 ``~module list`` 展示。

        :return: 包标识到原因的映射。
        """
        cls.discover()
        return dict(cls._incompatible)

    @staticmethod
    def _package_label(entry: PackageEntry) -> str:
        """包的展示名，优先用分发名。"""
        return entry.dist_name or entry.name

    @classmethod
    def reject_incompatible(cls) -> dict[str, str]:
        """剔除 requires_core_api 与当前 core API 版本不兼容的包。

        在 ``load_modules()`` 之前调用：此时配置系统已就绪，可安全写日志。

        :return: 包标识到原因的映射。
        """
        from packaging.specifiers import InvalidSpecifier, SpecifierSet
        from packaging.version import InvalidVersion, Version

        cls.discover()
        rejected: dict[str, str] = {}
        keep: dict[str, PackageEntry] = {}
        for key, entry in cls._entries.items():
            specifier = entry.manifest.requires_core_api
            try:
                satisfied = Version(str(CORE_API_VERSION)) in SpecifierSet(specifier)
            except (InvalidSpecifier, InvalidVersion):
                reason = f"declares an unparsable requires_core_api {specifier!r}"
                satisfied = False
            else:
                reason = f"requires core API {specifier}, current is {CORE_API_VERSION}"
            if satisfied:
                keep[key] = entry
                continue
            rejected[cls._package_label(entry)] = reason
            _logger().warning(f"Skipped {cls._package_label(entry)}: {reason}.")

        if rejected:
            cls._entries = keep
            cls._by_import_path = {entry.import_path: entry for entry in keep.values()}
        cls._incompatible = rejected
        return dict(rejected)

    @classmethod
    def report_lines(cls) -> list[str]:
        """不兼容包的一行式说明，供启动提示与 loader 缓存展示。"""
        return [f"{name}: {reason}" for name, reason in sorted(cls.incompatible().items())]

    @classmethod
    def _load_frozen(cls) -> dict[str, PackageEntry] | None:
        """读取二进制构建产物中的清单；不存在时返回 ``None``。"""
        try:
            module = importlib.import_module(FROZEN_REGISTRY_MODULE)
        except ModuleNotFoundError:
            return None
        try:
            return dict(getattr(module, "PACKAGES"))
        except AttributeError as error:
            raise RegistryError(f"{FROZEN_REGISTRY_MODULE} does not define PACKAGES") from error

    @classmethod
    def _from_entry_points(cls, kind: str, group: str) -> list[PackageEntry]:
        """枚举某个 entry point 组的条目。

        :param kind: 包种类。
        :param group: entry point 组名。
        :return: 条目列表；单个条目失败时记录错误并跳过。
        """
        try:
            discovered = importlib.metadata.entry_points(group=group)
        except TypeError:
            discovered = importlib.metadata.entry_points().get(group, ())
        entries: list[PackageEntry] = []
        for entry_point in discovered:
            try:
                entries.append(cls._entry_from_entry_point(kind, entry_point))
            except Exception:
                _logger().exception(f"Failed to resolve {kind} entry point {entry_point.name!r}, skipped.")
        return entries

    @classmethod
    def _entry_from_entry_point(cls, kind: str, entry_point: Any) -> PackageEntry:
        """把单个 entry point 解析为条目。

        :param kind: 包种类。
        :param entry_point: ``importlib.metadata.EntryPoint`` 实例。
        :return: 条目。
        :raises RegistryError: entry point 指向的不是包，或无法定位其目录。
        """
        module = importlib.import_module(entry_point.value)
        root = cls._root_of(module, entry_point.value)
        distribution = importlib.metadata.distribution(entry_point.dist.name) if entry_point.dist else None
        version = distribution.version if distribution else "0+local"
        manifest = cls._read_manifest(module.__name__, root)
        return PackageEntry(
            kind=kind,
            name=entry_point.name,
            dist_name=distribution.metadata["Name"] if distribution else "",
            version=version,
            import_path=module.__name__,
            root=root,
            manifest=manifest,
            editable=cls._is_editable(distribution),
        )

    @staticmethod
    def _root_of(module: Any, import_path: str) -> Path:
        """定位包根目录。

        :param module: 已导入的包。
        :param import_path: 包导入路径，用于报错。
        :return: 包根目录。
        :raises RegistryError: 该模块不是包。
        """
        paths = list(getattr(module, "__path__", ()))
        if paths:
            return Path(paths[0]).resolve()
        module_file = getattr(module, "__file__", None)
        if module_file:
            return Path(module_file).resolve().parent
        raise RegistryError(f"{import_path} is not a package")

    @staticmethod
    def _is_editable(distribution: Any) -> bool:
        """判断已安装分发是否为可编辑安装。"""
        if distribution is None:
            return True
        direct_url = distribution.read_text("direct_url.json")
        if not direct_url:
            return False
        try:
            import json

            payload = json.loads(direct_url)
        except ValueError:
            return False
        return bool(payload.get("dir_info", {}).get("editable"))

    @classmethod
    def _from_directory_scan(cls) -> list[PackageEntry]:
        """扫描仓库内的 ``modules/`` 与 ``bots/``。

        拆包之前这是主路径，因此扫描对象是真实存在的包目录，而非硬编码的路径常量。

        :return: 条目列表，按 ``(kind, name)`` 排序。
        """
        entries: list[PackageEntry] = []
        for kind, package_name in (("module", "modules"), ("adapter", "bots")):
            package = sys.modules.get(package_name) or cls._import_optional(package_name)
            if package is None:
                _logger().warning(f"Package {package_name!r} not importable, skip {kind} discovery.")
                continue
            for root in getattr(package, "__path__", ()):
                for child in sorted(Path(root).iterdir()):
                    if not child.is_dir() or child.name.startswith((".", "_")):
                        continue
                    if not (child / "__init__.py").is_file():
                        continue
                    entries.append(cls._entry_from_directory(kind, package_name, child))
        return entries

    @staticmethod
    def _import_optional(name: str) -> Any | None:
        """导入包；不存在时返回 ``None``。"""
        try:
            return importlib.import_module(name)
        except ImportError:
            return None

    @classmethod
    def _entry_from_directory(cls, kind: str, package_name: str, root: Path) -> PackageEntry:
        """由目录扫描结果构造条目。

        :param kind: 包种类。
        :param package_name: 顶层包名，``modules`` 或 ``bots``。
        :param root: 包目录。
        :return: 条目。
        """
        import_path = f"{package_name}.{root.name}"
        return PackageEntry(
            kind=kind,
            name=root.name,
            dist_name="",
            version="0+local",
            import_path=import_path,
            root=root.resolve(),
            manifest=cls._read_manifest(import_path, root),
        )

    @classmethod
    def _read_manifest(cls, import_path: str, root: Path) -> PackageManifest:
        """读取包内 manifest；不存在或结构版本不认识时返回默认清单。

        :param import_path: 包导入路径，用于日志。
        :param root: 包根目录。
        :return: 清单对象。
        """
        path = root / MANIFEST_FILENAME
        if not path.is_file():
            return PackageManifest()
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            _logger().exception(f"Failed to read manifest of {import_path}, using defaults.")
            return PackageManifest()
        schema = data.get("schema", MANIFEST_SCHEMA)
        if schema != MANIFEST_SCHEMA:
            _logger().warning(f"Manifest of {import_path} declares schema {schema}, current is {MANIFEST_SCHEMA}.")
        return PackageManifest.from_mapping(data, source=import_path)

    @classmethod
    def modules(cls) -> dict[str, PackageEntry]:
        """全部模块包，键为包名。"""
        cls.discover()
        return {entry.name: entry for entry in cls._entries.values() if entry.kind == "module"}

    @classmethod
    def adapters(cls) -> dict[str, PackageEntry]:
        """全部适配器包，键为包名。"""
        cls.discover()
        return {entry.name: entry for entry in cls._entries.values() if entry.kind == "adapter"}

    @classmethod
    def all(cls) -> dict[str, PackageEntry]:
        """全部包，键为 ``种类:包名``。"""
        cls.discover()
        return dict(cls._entries)

    @classmethod
    def get(cls, kind: PackageKind, name: str) -> PackageEntry | None:
        """按键取单个包。

        :param kind: 包种类。
        :param name: 包名。
        :return: 条目；不存在时为 ``None``。
        """
        cls.discover()
        return cls._entries.get(f"{kind}:{name}")

    @classmethod
    def by_import_path(cls, path: str) -> PackageEntry | None:
        """按导入路径查包，取最长前缀匹配。

        ``'modules.wiki.utils.wikilib'`` 解析为 ``wiki`` 包的条目。

        :param path: 导入路径。
        :return: 条目；无任何包的导入路径是其前缀时为 ``None``。
        """
        cls.discover()
        candidate = path
        while candidate:
            entry = cls._by_import_path.get(candidate)
            if entry is not None:
                return entry
            candidate = candidate.rpartition(".")[0]
        return None

    @classmethod
    def import_roots(cls, kind: PackageKind) -> set[str]:
        """某一类包导入路径的顶层段。

        :param kind: 包种类。
        :return: 顶层段集合；该类无包时为空集。
        """
        cls.discover()
        return {entry.import_path.split(".")[0] for entry in cls._entries.values() if entry.kind == kind}

    @classmethod
    def locales_paths(cls) -> list[str]:
        """全部现存的 locale 目录，核心的 locale 目录排在最前。"""
        cls.discover()
        paths: list[str] = []
        core_locales = cls._core_locales_dir()
        if core_locales is not None:
            paths.append(str(core_locales))
        for entry in cls._entries.values():
            relative = entry.manifest.locales
            if not relative:
                continue
            directory = entry.root / relative
            if directory.is_dir():
                paths.append(str(directory))
        return paths

    @staticmethod
    def _core_locales_dir() -> Path | None:
        """core 自身的 locale 目录。"""
        try:
            core = importlib.import_module("core")
        except ImportError:
            return None
        paths = list(getattr(core, "__path__", ()))
        if not paths:
            return None
        directory = Path(paths[0]) / "locales"
        return directory if directory.is_dir() else None

    @classmethod
    def config_template_paths(cls) -> list[str]:
        """全部配置模板的模块名，核心配置排在最前。

        清单按包名排序，以固定生成顺序，避免同一批配置项在多次生成间换序而反复改写
        配置文件。

        以文件是否存在判断模板有无，而非在导入时捕获 ``ModuleNotFoundError``：后者无法
        区分「该包未提供 config.py」与「模板自身导入了不存在的依赖」，后一种会被静默跳过，
        形成漏键。亦不使用 ``importlib.util.find_spec()``：该函数为取得 ``__path__`` 会
        导入父包，使配置模板作为叶子模块的优势不复存在。

        :return: 配置模板的模块名列表。
        """
        cls.discover()
        names = ["core.config.base"]
        for kind in ("adapter", "module"):
            candidates = sorted(
                (entry for entry in cls._entries.values() if entry.kind == kind),
                key=lambda entry: entry.name,
            )
            for entry in candidates:
                if not (entry.root / "config.py").is_file():
                    continue
                if not (entry.root / "__init__.py").is_file():
                    # 目录形式的命名空间包仍可导入，配置照常补全；但其它按包枚举的代码
                    # 看不见它，故仅告警，提示补上空的 __init__.py 以恢复常规包。
                    _logger().warning(
                        f"[Config] {entry.import_path} provides config.py without __init__.py; "
                        "its configuration is generated, but an empty __init__.py is required for it "
                        "to be visible to package-based enumeration."
                    )
                names.append(f"{entry.import_path}.config")
        return names

    @classmethod
    def db_model_paths(cls) -> list[str]:
        """全部模块的数据库模型模块名。

        与配置模板同一条理由：以文件是否存在判断，不导入包。``models.py`` 内部缺少依赖
        时，错误会在 ``init_db()`` 真正导入它时抛出，不会在此被静默跳过。

        :return: 模型模块名列表，按包名排序。
        """
        cls.discover()
        modules = cls.modules()
        return [
            f"{modules[name].import_path}.database.models"
            for name in sorted(modules)
            if (modules[name].root / "database" / "models.py").is_file()
        ]

    @classmethod
    def data_dir(cls, name_or_entry: str | PackageEntry) -> Path:
        """包在实例内的可写数据目录。

        :param name_or_entry: 包名或条目。
        :return: 数据目录路径；调用方负责创建。
        :raises KeyError: 该名称不是已发现的包。
        """
        entry = cls._resolve(name_or_entry)
        return cls._instance_data_root() / entry.kind / entry.name

    @staticmethod
    def _instance_data_root() -> Path:
        """实例数据根目录。"""
        from core.constants.path import assets_path

        return assets_path / "data"

    @classmethod
    def _resolve(cls, name_or_entry: str | PackageEntry) -> PackageEntry:
        """把包名解析为条目。

        :param name_or_entry: 包名或条目。
        :return: 条目。
        :raises KeyError: 无法解析。
        """
        if isinstance(name_or_entry, PackageEntry):
            return name_or_entry
        cls.discover()
        for entry in cls._entries.values():
            if entry.name == name_or_entry:
                return entry
        raise KeyError(f"Unknown package {name_or_entry!r}")
