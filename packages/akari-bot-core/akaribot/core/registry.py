"""模块与适配器的统一发现层。

「系统里有哪些模块与适配器」的唯一答案来源，按下列顺序合成：

1. 存在 ``akaribot/core/_frozen_registry.py`` 时直接采用（二进制构建产物，尚未生成）；
2. 枚举已安装分发的 entry point；
3. 兜底扫描命名空间包 ``akaribot.modules`` 与 ``akaribot.adapters``，合成 ``dist_name`` 为空的条目；
4. 按条目名去重，entry point 胜出，冲突时记录警告。

拆包前以第 3 条为主，拆包后各包以 wheel 安装，第 2 条接管，本模块之外的代码无需改动。
"""

from __future__ import annotations

import heapq
import importlib
import importlib.metadata
import importlib.resources
import importlib.util
import sys
import tomllib
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, fields as dataclass_fields
from pathlib import Path
from typing import Any, Literal

ENTRY_POINT_GROUPS: dict[str, str] = {"module": "akaribot.modules", "adapter": "akaribot.adapters"}

# 二进制构建产物。存在时 discover() 直接采用其中记录的清单，跳过 entry point 与目录扫描。
FROZEN_REGISTRY_MODULE = "akaribot.core._frozen_registry"

# 包内 manifest 的文件名与版本。
MANIFEST_FILENAME = "manifest.toml"
MANIFEST_SCHEMA = 1

# core 公共 API 的版本。模块与适配器以 manifest 的 requires_core_api 声明所需区间，不满足者由
# reject_incompatible() 拒绝注册。本常量是单一真源，core.api 取其值；此处不得反向导入 core.api。
CORE_API_VERSION = 1

# 参与运行时依赖图的分发名前缀。其余 Requires-Dist 是普通 PyPI 依赖，由安装器负责解析。
DEPENDENCY_PREFIXES = ("akari-bot-module-", "akari-bot-adapter-")

PackageKind = Literal["module", "adapter"]


class RegistryError(RuntimeError):
    """发现层无法产出可用清单时抛出。"""


class CircularDependencyError(RegistryError):
    """包声明依赖成环时抛出。

    :param cycles: 每个环的完整路径，首尾为同一个包。
    """

    def __init__(self, cycles: tuple[tuple[str, ...], ...]):
        self.cycles = cycles
        detail = "; ".join(" -> ".join(cycle) for cycle in cycles)
        super().__init__(f"Circular dependency detected: {detail}")


def _logger():
    """惰性取得日志器。

    不能在模块层导入 core.logger：core.logger 会经 core.config.base 引入整个配置系统，
    而配置系统在导入期校验配置文件存在并执行版本迁移。发现层必须能在配置就绪之前使用
    （locale 目录的收集就发生在配置加载之前），因此把这条依赖推迟到真正要写日志时。
    """
    from akaribot.core.logger import Logger

    return Logger


def _canonicalize(name: str) -> str:
    """分发名的规范化形式。

    依赖声明的写法允许大小写与下划线差异，比较前统归一形式，等价名字才能命中同一个包。

    :param name: 分发名或包名。
    :return: 规范化后的名字。
    """
    from packaging.utils import canonicalize_name

    return canonicalize_name(name)


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
    :param import_path: 导入路径，如 ``akaribot.modules.wiki``。
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


@dataclass(frozen=True, slots=True)
class PackageDependency:
    """一个包在分发 metadata 里声明的模块包依赖。

    :param dist_name: 依赖的分发名，已规范化为小写连字符形式。
    :param specifier: 版本描述符，如 ``>=1.0,<2.0``；未限定版本时为空串。
    :param satisfied: 已装版本是否满足描述符。
    :param installed_version: 已装版本；未安装时为 ``None``。
    """

    dist_name: str
    specifier: str
    satisfied: bool
    installed_version: str | None


class PackageRegistry:
    """模块与适配器的发现结果缓存。

    发现结果在进程内缓存一次，``discover(force=True)`` 用于安装或卸载包之后重建。
    """

    _entries: dict[str, PackageEntry] = {}
    _by_import_path: dict[str, PackageEntry] = {}
    _discovered: bool = False
    # core API 不兼容的包：展示用标签到原因。
    _incompatible: dict[str, str] = {}
    # 同一批包：规范化分发名到原因，供依赖校验把「依赖被 API 门槛拒绝的包」判为不可用。
    _api_refused: dict[str, str] = {}
    _dependency_rejected: dict[str, str] = {}

    @classmethod
    def discover(cls, *, force: bool = False) -> None:
        """建立发现结果。

        收尾依次校验 core API 兼容性与声明依赖（缺失、版本不满足、成环、依赖了被 API 门槛拒绝的
        包），两道都通过的包才注册。顺序不可颠倒：依赖校验须知道哪些包已被 API 门槛拒绝，否则
        依赖它们的包会以「发行版已安装」为由留下，直到导入期才失败。原因经 :meth:`incompatible`
        与 :meth:`report_lines` 报出。

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
            known = {entry.import_path for entry in entries.values()}
            for entry in cls._from_directory_scan():
                # 目录扫描是兜底：entry point 已提供的包不再重复登记，也不产生冲突告警。
                if entry.import_path in known:
                    continue
                cls._insert(entries, entry, source="directory scan")

        entries, api_rejected, api_refused = cls._reject_core_api_incompatible(entries)
        entries, rejected = cls._reject_unsatisfied_dependencies(entries, refused=api_refused)
        cls._entries = entries
        cls._incompatible = api_rejected
        cls._api_refused = api_refused
        cls._dependency_rejected = rejected
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
        return f"{entry.kind}:{entry.name}"

    @classmethod
    def incompatible(cls) -> dict[str, str]:
        """不能注册的包及其原因。

        收录两类：core 公共 API 不兼容的包，与声明依赖不满足的包。仅覆盖已发现的包；
        被拒绝注册的包不进入 :meth:`modules` 与 :meth:`adapters`，但在此可见，供启动
        提示与 ``~module list`` 展示。

        :return: 包标识到原因的映射。
        """
        cls.discover()
        return {**cls._dependency_rejected, **cls._incompatible}

    @staticmethod
    def _package_label(entry: PackageEntry) -> str:
        return entry.dist_name or entry.name

    @classmethod
    def reject_incompatible(cls) -> dict[str, str]:
        """``requires_core_api`` 与当前 core API 版本不兼容的包及其原因。

        该检查已是 :meth:`discover` 的一环：依赖校验必须知道哪些包被它拒绝，才能级联剔除
        依赖它们的包。本方法保留为公开入口，对直接注入注册表的条目（测试与工具）补做一次，
        并返回同源的结果。

        :return: 包标识到原因的映射。
        """
        cls.discover()
        kept, rejected, refused = cls._reject_core_api_incompatible(cls._entries)
        if len(kept) == len(cls._entries):
            # 发现阶段已闸过一遍，此时覆盖会丢掉已记录的原因（被拒的包已不在 _entries 里）
            return dict(cls._incompatible)
        cls._entries = kept
        cls._by_import_path = {entry.import_path: entry for entry in kept.values()}
        cls._incompatible = rejected
        cls._api_refused = refused
        return dict(rejected)

    @classmethod
    def _reject_core_api_incompatible(
        cls, entries: dict[str, PackageEntry]
    ) -> tuple[dict[str, PackageEntry], dict[str, str], dict[str, str]]:
        """按 ``requires_core_api`` 分出与当前 core API 版本不兼容的包。

        结果分两份：展示用标签到原因，供 :meth:`incompatible` / :meth:`report_lines` 报出；
        规范化分发名到原因，供依赖校验把「依赖一个已被拒绝的包」判为不可用。本方法不改动
        类状态，由调用方决定如何登记。

        :param entries: 本次发现的全部条目。
        :return: 三元组——保留的条目；标签到原因；规范化分发名到原因。
        """
        from packaging.specifiers import InvalidSpecifier, SpecifierSet
        from packaging.version import InvalidVersion, Version

        rejected: dict[str, str] = {}
        refused: dict[str, str] = {}
        keep: dict[str, PackageEntry] = {}
        for key, entry in entries.items():
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
            for dist_name in cls._distribution_names(entry):
                refused[_canonicalize(dist_name)] = reason
            _logger().warning(f"Skipped {cls._package_label(entry)}: {reason}.")
        return keep, rejected, refused

    @classmethod
    def report_lines(cls) -> list[str]:
        """不兼容包的一行式说明，供启动提示与 loader 缓存展示。"""
        return [f"{name}: {reason}" for name, reason in sorted(cls.incompatible().items())]

    @classmethod
    def _load_frozen(cls) -> dict[str, PackageEntry] | None:
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

        只按 spec 定位包目录，不导入包本身。导入会执行包内 ``config.py``，使配置模板在 i18n
        快照接上之前写盘，新实例生成的配置注释全部退化为空。

        :param kind: 包种类。
        :param entry_point: ``importlib.metadata.EntryPoint`` 实例。
        :return: 条目。
        :raises RegistryError: entry point 指向的不是包，或无法定位其目录。
        """
        import_path = entry_point.value
        root = cls._root_of(import_path)
        distribution = importlib.metadata.distribution(entry_point.dist.name) if entry_point.dist else None
        version = distribution.version if distribution else "0+local"
        manifest = cls._read_manifest(import_path, root)
        return PackageEntry(
            kind=kind,
            name=entry_point.name,
            dist_name=distribution.metadata["Name"] if distribution else "",
            version=version,
            import_path=import_path,
            root=root,
            manifest=manifest,
            editable=cls._is_editable(distribution),
        )

    @staticmethod
    def _root_of(import_path: str) -> Path:
        """按导入路径定位包根目录，不导入该包。

        :param import_path: 包导入路径，如 ``akaribot.modules.wiki``。
        :return: 包根目录。
        :raises RegistryError: 该路径无法定位，或不是包。
        """
        spec = importlib.util.find_spec(import_path)
        if spec is None:
            raise RegistryError(f"{import_path} cannot be located")
        locations = list(spec.submodule_search_locations or ())
        if locations:
            return Path(locations[0]).resolve()
        if spec.origin:
            return Path(spec.origin).resolve().parent
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
        """扫描命名空间包 ``akaribot.modules`` 与 ``akaribot.adapters``。

        未安装分发的源码检出依赖这条路径，因此扫描对象是真实存在的包目录，而非硬编码的路径常量。

        :return: 条目列表，按 ``(kind, name)`` 排序。
        """
        entries: list[PackageEntry] = []
        for kind, package_name in (("module", "akaribot.modules"), ("adapter", "akaribot.adapters")):
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
        try:
            return importlib.import_module(name)
        except ImportError:
            return None

    @classmethod
    def _entry_from_directory(cls, kind: str, package_name: str, root: Path) -> PackageEntry:
        """由目录扫描结果构造条目。

        条目根取**导入包目录**而非分发包目录：manifest、locales、assets、migrations 都相对它
        解析，entry point 路径下两者同为导入包目录，此处对齐。源码布局为 ``src`` 时按导入路径
        下推；不是该布局时退回传入目录。

        :param kind: 包种类。
        :param package_name: 命名空间前缀，``akaribot.modules`` 或 ``akaribot.adapters``。
        :param root: 分发包目录。
        :return: 条目。
        """
        import_path = f"{package_name}.{root.name}"
        package_root = root / "src" / Path(*import_path.split("."))
        if not package_root.is_dir():
            package_root = root
        return PackageEntry(
            kind=kind,
            name=root.name,
            dist_name="",
            version="0+local",
            import_path=import_path,
            root=package_root.resolve(),
            manifest=cls._read_manifest(import_path, package_root),
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

        ``'akaribot.modules.wiki.utils.wikilib'`` 解析为 ``wiki`` 包的条目。

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
        """某一类包所属的命名空间前缀。

        包导入路径形如 ``akaribot.modules.wiki``，命名空间是去掉包名那一段。该前缀是 loader
        归约导入路径的界：取「命名空间 + 包名」三段。2 段布局时代的顶层段语义不再成立。

        :param kind: 包种类。
        :return: 命名空间前缀集合；该类无包时为空集。
        """
        cls.discover()
        # 命名空间与 entry point 组同名（见 ENTRY_POINT_GROUPS），但取值仍由条目导出：
        # 该类无包时返回空集，调用方据此判断是否存在可依赖的包。
        roots = {entry.import_path.rpartition(".")[0] for entry in cls._entries.values() if entry.kind == kind}
        roots.discard("")
        return roots

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
        try:
            core = importlib.import_module("akaribot.core")
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

        按包名排序以固定生成顺序，避免同一批配置项反复改写配置文件。以文件是否存在判断模板有无，
        不导入包：捕获 ``ModuleNotFoundError`` 无法区分「未提供 config.py」与「模板自身缺依赖」，
        后者会被静默跳过形成漏键；``find_spec()`` 为取 ``__path__`` 会导入父包，失去叶子模块的优势。

        :return: 配置模板的模块名列表。
        """
        cls.discover()
        names = ["akaribot.core.config.base"]
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

        与配置模板同理，以文件是否存在判断而不导入包。``models.py`` 内部缺依赖时，错误在
        ``init_db()`` 真正导入它时抛出，不会在此被静默跳过。

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
    def migration_dirs(cls) -> list[tuple[str, Path]]:
        """全部模块包的数据库迁移目录。

        键取分发名：迁移记录长期存放，包名在拆包前后会变化而分发名不变，用裸包名会让旧库已登记的
        revision 在拆包后重新变为待应用。目录以 ``manifest.migrations`` 为准，未声明时回落包内
        ``migrations/``，否则拆包前没有任何包带 manifest，迁移目录会全部不可见。

        :return: ``(包名, 目录)`` 列表，按包名排序。
        """
        cls.discover()
        directories: list[tuple[str, Path]] = []
        modules = cls.modules()
        for name in sorted(modules):
            entry = modules[name]
            relative = entry.manifest.migrations or "migrations"
            directory = entry.root / relative
            if not directory.is_dir():
                continue
            directories.append((entry.dist_name or f"akari-bot-module-{entry.name}", directory))
        return directories

    @classmethod
    def package_data(cls, name_or_entry: str | PackageEntry) -> Path:
        """包在实例内的可写数据目录。

        运行时下载、索引与用户配置写在此处，不写回包目录：包目录在只读挂载与 wheel
        安装两种形态下都不可写。目录须由调用方经 :meth:`Paths.ensure` 创建。

        :param name_or_entry: 包名或条目。
        :return: 数据目录路径。
        :raises KeyError: 该名称不是已发现的包。
        """
        entry = cls._resolve(name_or_entry)
        return cls._instance_data_root() / entry.kind / entry.name

    @classmethod
    def package_assets(cls, name_or_entry: str | PackageEntry) -> Path:
        """包内只读静态资源目录。

        安装为 wheel 后该目录位于 site-packages 内，只可读取。声明了 ``manifest.assets``
        时取该相对路径，否则取包根目录。

        :param name_or_entry: 包名或条目。
        :return: 资源目录路径。
        :raises KeyError: 该名称不是已发现的包。
        """
        entry = cls._resolve(name_or_entry)
        relative = entry.manifest.assets
        return entry.root / relative if relative else entry.root

    @staticmethod
    def _instance_data_root() -> Path:
        """实例数据根目录。

        取实例的可写 data 目录，而非顶层只读的 assets：包的可写数据不属于随仓库分发的
        内容，放在 assets 下会在只读挂载与 wheel 安装两种形态下同时失败。
        """
        from akaribot.core.paths import Paths

        return Paths.data

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

    @classmethod
    def dependencies(cls, entry: PackageEntry) -> tuple[PackageDependency, ...]:
        """包在分发 metadata 里声明的模块包依赖。

        只收录 ``akari-bot-module-`` 与 ``akari-bot-adapter-`` 前缀的 ``Requires-Dist``；其余是
        普通 PyPI 依赖，由安装器负责。目录扫描兜底时无分发 metadata，返回空元组。带 extra 标记的
        条目按「该 extra 已装」判断（见 :meth:`_installed_extras`），未装 extra 的依赖不计入。

        :param entry: 待查询的包。
        :return: 依赖元组，按分发名排序。
        """
        if not entry.dist_name:
            return ()
        try:
            distribution = importlib.metadata.distribution(entry.dist_name)
        except importlib.metadata.PackageNotFoundError:
            return ()
        try:
            requirements = cls._parsed_requirements(distribution, entry.dist_name)
        except Exception:
            _logger().exception(f"Failed to read dependency metadata of {entry.dist_name!r}.")
            return ()
        extras = cls._installed_extras(distribution, requirements)
        found: dict[str, PackageDependency] = {}
        for requirement in requirements:
            name = _canonicalize(requirement.name)
            if not name.startswith(DEPENDENCY_PREFIXES):
                continue
            if not cls._marker_applies(requirement.marker, extras):
                continue
            installed = cls._installed_version(name)
            found[name] = PackageDependency(
                dist_name=name,
                specifier=str(requirement.specifier),
                satisfied=cls._requirement_satisfied(installed, requirement, name),
                installed_version=installed,
            )
        return tuple(found[key] for key in sorted(found))

    @classmethod
    def dependents(cls, entry: PackageEntry) -> tuple[PackageEntry, ...]:
        """反向依赖：声明依赖 ``entry`` 的全部包，供卸载保护使用。

        匹配按分发名的规范化形式进行；条目没有分发名时按 ``akari-bot-<种类>-<包名>``
        合成，与 :meth:`migration_dirs` 同一约定，使依赖声明在拆包前后指向同一个包。

        :param entry: 目标包。
        :return: 依赖它的包，按注册表键排序。
        """
        cls.discover()
        names = {_canonicalize(name) for name in cls._distribution_names(entry)}
        own = cls._key(entry)
        found = [
            candidate
            for key, candidate in cls._entries.items()
            if key != own
            and names & {_canonicalize(dependency.dist_name) for dependency in cls.dependencies(candidate)}
        ]
        return tuple(sorted(found, key=cls._key))

    @classmethod
    def resolved_dependencies(cls, entry: PackageEntry) -> tuple[PackageEntry, ...]:
        """声明依赖中已注册为本进程包的那些。

        依赖已装但未注册（例如装入的是普通 PyPI 包）时不出现在结果中。

        :param entry: 待查询的包。
        :return: 依赖条目，按注册表键排序。
        """
        cls.discover()
        index = {
            _canonicalize(name): key
            for key, candidate in cls._entries.items()
            for name in cls._distribution_names(candidate)
        }
        own = cls._key(entry)
        found = set()
        for dependency in cls.dependencies(entry):
            target = index.get(_canonicalize(dependency.dist_name))
            if target is not None and target != own:
                found.add(target)
        return tuple(cls._entries[key] for key in sorted(found))

    @classmethod
    def load_order(cls) -> list[PackageEntry]:
        """全部包的拓扑序，被依赖者在前。

        同层按注册表键排序，使同一批包在多次运行间的顺序一致。返回值覆盖全部已注册包，
        与 :meth:`all` 等长，不遗漏任何包。

        :return: 条目列表。
        :raises CircularDependencyError: 声明依赖存在环。成环的包在 :meth:`discover`
            阶段已被拒绝注册，此异常只在直接调用本方法时出现。
        """
        cls.discover()
        edges = cls._dependency_edges()
        cycles = cls._cycles(edges)
        if cycles:
            paths = tuple(cls._cycle_path(cycle, edges) for cycle in cycles)
            raise CircularDependencyError(cls._cycle_labels(paths, cls._entries))
        dependents: dict[str, set[str]] = {key: set() for key in edges}
        degree = {key: len(dependencies) for key, dependencies in edges.items()}
        for key, dependencies in edges.items():
            for dependency in dependencies:
                dependents[dependency].add(key)
        ready = [key for key, count in degree.items() if not count]
        heapq.heapify(ready)
        ordered: list[str] = []
        while ready:
            key = heapq.heappop(ready)
            ordered.append(key)
            for dependent in sorted(dependents[key]):
                degree[dependent] -= 1
                if not degree[dependent]:
                    heapq.heappush(ready, dependent)
        if len(ordered) != len(edges):
            # 环检测已在上方拦截，此处只作兜底：宁可报错，也不静默少加载包。
            remaining = tuple(sorted(set(edges) - set(ordered)))
            raise CircularDependencyError((cls._cycle_path(remaining, edges),))
        return [cls._entries[key] for key in ordered]

    @classmethod
    def _record_rejection(
        cls, entry: PackageEntry, reason: str, rejected: dict[str, str], refused: dict[str, str]
    ) -> None:
        """
        登记一次拒绝。

        :param entry: 被拒绝的包。
        :param reason: 拒绝原因。
        :param rejected: 展示用标签到原因的映射，就地写入。
        :param refused: 规范化分发名到原因的映射，供依赖级联判分，就地写入。
        """
        label = cls._package_label(entry)
        rejected[label] = reason
        for dist_name in cls._distribution_names(entry):
            refused[_canonicalize(dist_name)] = reason
        _logger().warning(f"Skipped {label}: {reason}.")

    @classmethod
    def _reject_unsatisfied_dependencies(
        cls, entries: dict[str, PackageEntry], *, refused: dict[str, str] | None = None
    ) -> tuple[dict[str, PackageEntry], dict[str, str]]:
        """剔除声明依赖缺失、版本不满足或成环的包，并级联剔除依赖它们的包。

        :param entries: 本次发现中已通过 core API 校验的条目。
        :param refused: 已确定不可用的依赖（规范化分发名到原因），由 core API 校验登记。
        :return: 二元组——保留的条目；被拒绝包的标识到原因的映射。
        """
        refused = dict(refused or {})
        kept: dict[str, PackageEntry] = {}
        rejected: dict[str, str] = {}
        for key, entry in entries.items():
            reason = cls._dependency_reason(entry, refused)
            if reason is None:
                kept[key] = entry
                continue
            cls._record_rejection(entry, reason, rejected, refused)
        edges = cls._edges_of(kept)
        for cycle in cls._cycles(edges):
            path = cls._cycle_path(cycle, edges)
            labels = " -> ".join(cls._package_label(kept[key]) for key in path)
            for key in cycle:
                cls._record_rejection(kept[key], f"circular dependency {labels}", rejected, refused)
                del kept[key]
            _logger().warning(f"Skipped {len(cycle)} package(s): circular dependency {labels}.")

        # 级联：依赖一个已被拒绝的包与依赖一个未安装的包同样注定失败，只按 metadata 判断会让
        # 依赖方以「依赖已安装」为由留下，最终在导入期抛出与配置无关的错误。逐个剔除至不动点。
        declared = {key: cls.dependencies(entry) for key, entry in kept.items()}
        while True:
            cascade: list[tuple[str, PackageEntry, str]] = []
            for key, dependencies in declared.items():
                reasons = [
                    f"depends on {dependency.dist_name}, which was refused: "
                    f"{refused[_canonicalize(dependency.dist_name)]}"
                    for dependency in dependencies
                    if _canonicalize(dependency.dist_name) in refused
                ]
                if reasons:
                    cascade.append((key, kept[key], "; ".join(reasons)))
            if not cascade:
                break
            for key, entry, reason in cascade:
                del kept[key]
                declared.pop(key, None)
                cls._record_rejection(entry, reason, rejected, refused)
        return kept, rejected

    @classmethod
    def _dependency_reason(cls, entry: PackageEntry, refused: dict[str, str] | None = None) -> str | None:
        """声明依赖不满足时的原因；全部满足时为 ``None``。

        :param entry: 待查询的包。
        :param refused: 已被拒绝的依赖（规范化分发名到原因）。命中的依赖按不可用处理：
            它可能仍装在环境里，但不会完成注册。
        """
        refused = refused or {}
        reasons = []
        for dependency in cls.dependencies(entry):
            refusal = refused.get(_canonicalize(dependency.dist_name))
            if refusal is not None:
                reasons.append(f"depends on {dependency.dist_name}, which was refused: {refusal}")
            elif dependency.installed_version is None:
                reasons.append(f"missing dependency {dependency.dist_name}")
            elif not dependency.satisfied:
                reasons.append(
                    f"{dependency.dist_name} {dependency.installed_version} does not satisfy {dependency.specifier}"
                )
        return "; ".join(reasons) or None

    @staticmethod
    def _distribution_names(entry: PackageEntry) -> tuple[str, ...]:
        """条目可被依赖声明引用的分发名。

        目录扫描的包没有分发名，按 ``akari-bot-<种类>-<包名>`` 合成：该名字与拆包后的
        分发名一致，依赖声明因此不必区分包来自 entry point 还是目录扫描。

        :param entry: 包。
        :return: 分发名元组。
        """
        if entry.dist_name:
            return (entry.dist_name,)
        return (f"akari-bot-{entry.kind}-{entry.name}",)

    @staticmethod
    def _installed_version(dist_name: str) -> str | None:
        try:
            return importlib.metadata.version(dist_name)
        except importlib.metadata.PackageNotFoundError:
            return None

    @staticmethod
    def _requirement_satisfied(installed: str | None, requirement: Any, dist_name: str) -> bool:
        """已装版本是否满足依赖描述符。版本号不可解析时视为不满足。"""
        from packaging.version import InvalidVersion, Version

        if installed is None:
            return False
        try:
            return Version(installed) in requirement.specifier
        except InvalidVersion:
            _logger().warning(f"Installed {dist_name} has unparsable version {installed!r}.")
            return False

    @staticmethod
    def _parsed_requirements(distribution: Any, dist_name: str) -> tuple[Any, ...]:
        """解析分发 metadata 的 ``Requires-Dist``。

        单行不可解析时跳过该行：一条写错的依赖不应让整个包从注册表中消失。

        :param distribution: ``importlib.metadata`` 的分发对象。
        :param dist_name: 分发名，用于日志。
        :return: ``Requirement`` 元组。
        """
        from packaging.requirements import InvalidRequirement, Requirement

        parsed = []
        for line in distribution.metadata.get_all("Requires-Dist") or []:
            try:
                parsed.append(Requirement(line))
            except InvalidRequirement:
                _logger().warning(f"Ignoring unparsable Requires-Dist {line!r} of {dist_name}.")
        return tuple(parsed)

    @classmethod
    def _installed_extras(cls, distribution: Any, requirements: tuple[Any, ...]) -> frozenset[str]:
        """该分发声明且已装的 extra。

        分发 metadata 不记录装包时选中了哪些 extra，故任何实现都是启发式。此处取「该 extra 下属
        的依赖都能解析为已装分发」为已装判据。已知边界：手工装齐某个未选中 extra 的全部依赖时会被
        误判为已装，代价是多记一条依赖边。既有测试固化此判据。

        :param distribution: 分发对象。
        :param requirements: 已解析的 ``Requires-Dist``。
        :return: 已装 extra 的规范化名字集合。
        """
        declared = {_canonicalize(name) for name in distribution.metadata.get_all("Provides-Extra") or []}
        installed = set()
        for extra in declared:
            guarded = [item for item in requirements if cls._marker_applies(item.marker, (extra,))]
            if guarded and all(cls._installed_version(item.name) is not None for item in guarded):
                installed.add(extra)
        return frozenset(installed)

    @classmethod
    def _marker_applies(cls, marker: Any, extras: frozenset[str] | tuple[str, ...]) -> bool:
        """环境标记是否成立。

        extra 未指定时 packaging 代入空串，带 ``extra`` 子句的标记因此先判为假，再逐个
        代入候选 extra 重判；只有已装 extra 的子句才算成立。标记无法求值时按成立处理：
        依赖是真实存在的耦合，宁可多记一条边，也不静默丢弃。

        :param marker: ``packaging.markers.Marker``；``None`` 表示无条件。
        :param extras: 参与判定的已装 extra。
        :return: 标记是否成立。
        """
        if marker is None:
            return True
        try:
            if marker.evaluate():
                return True
            return any(marker.evaluate({"extra": extra}) for extra in extras)
        except Exception:
            _logger().exception(f"Failed to evaluate marker {marker!s}, treating it as applicable.")
            return True

    @classmethod
    def _edges_of(cls, entries: dict[str, PackageEntry]) -> dict[str, tuple[str, ...]]:
        """给定条目集合内的声明依赖边。

        :param entries: 条目映射，键为注册表键。
        :return: 注册表键到其依赖键的映射，值为排序后的元组。
        """
        index = {
            _canonicalize(name): key
            for key, candidate in entries.items()
            for name in cls._distribution_names(candidate)
        }
        edges: dict[str, tuple[str, ...]] = {}
        for key, entry in entries.items():
            targets = set()
            for dependency in cls.dependencies(entry):
                target = index.get(_canonicalize(dependency.dist_name))
                if target is not None and target != key:
                    targets.add(target)
            edges[key] = tuple(sorted(targets))
        return edges

    @classmethod
    def _dependency_edges(cls) -> dict[str, tuple[str, ...]]:
        cls.discover()
        return cls._edges_of(cls._entries)

    @classmethod
    def _cycle_labels(
        cls, cycles: tuple[tuple[str, ...], ...], entries: dict[str, PackageEntry]
    ) -> tuple[tuple[str, ...], ...]:
        """把环的注册表键路径换成展示名路径。"""
        return tuple(tuple(cls._package_label(entries[key]) for key in cycle) for cycle in cycles)

    @staticmethod
    def _cycles(edges: dict[str, tuple[str, ...]]) -> tuple[tuple[str, ...], ...]:
        """依赖图中的全部环。

        以 Tarjan 算法求强连通分量：成员多于一个的分量即为环。返回的是分量成员而非
        某一条回路，调用方用 :meth:`_cycle_path` 还原完整路径；这样两个互不相交的环
        都会被发现，不会被只找首个环的写法漏掉。

        :param edges: 注册表键到其依赖键的映射。
        :return: 每个环的成员键，按最小键排序。
        """
        index: dict[str, int] = {}
        low: dict[str, int] = {}
        stack: list[str] = []
        on_stack: set[str] = set()
        counter = 0
        components: list[tuple[str, ...]] = []
        for root in sorted(edges):
            if root in index:
                continue
            index[root] = low[root] = counter
            counter += 1
            stack.append(root)
            on_stack.add(root)
            work: list[tuple[str, Iterator[str]]] = [(root, iter(edges[root]))]
            while work:
                node, successors = work[-1]
                advanced = False
                for successor in successors:
                    if successor not in index:
                        index[successor] = low[successor] = counter
                        counter += 1
                        stack.append(successor)
                        on_stack.add(successor)
                        work.append((successor, iter(edges.get(successor, ()))))
                        advanced = True
                        break
                    if successor in on_stack:
                        low[node] = min(low[node], index[successor])
                if advanced:
                    continue
                work.pop()
                if low[node] == index[node]:
                    component = []
                    while True:
                        member = stack.pop()
                        on_stack.discard(member)
                        component.append(member)
                        if member == node:
                            break
                    if len(component) > 1:
                        components.append(tuple(sorted(component)))
                if work:
                    parent = work[-1][0]
                    low[parent] = min(low[parent], low[node])
        return tuple(sorted(components))

    @staticmethod
    def _cycle_path(component: tuple[str, ...], edges: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
        """从强连通分量中还原一条完整回路，首尾为同一个包。

        :param component: 分量内的节点键。
        :param edges: 依赖图。
        :return: 回路路径，宽度优先取最短的一条。
        """
        members = set(component)
        start = min(component)
        queue: deque[tuple[str, ...]] = deque([(start,)])
        while queue:
            path = queue.popleft()
            for successor in edges.get(path[-1], ()):
                if successor == start:
                    return (*path, start)
                if successor in members and successor not in path:
                    queue.append((*path, successor))
        return (*component, start)
