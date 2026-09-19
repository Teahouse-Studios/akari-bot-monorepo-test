"""按包管理的配置版本与配置迁移。

core 只维护 ``config.toml`` 的版本（见 core/config/update.py）；其余配置文件的版本随包走：包把
迁移脚本放在 ``config_migrations/`` 下，脚本文件名以四位号段开头，负责把文件从 ``N-1`` 号升到
``N`` 号，已应用到哪一号记在文件自身的 ``config_version`` 里。

版本记在文件而非数据库，是本设计的前提：配置文件必须能脱离数据库独立迁移。模块可能被单独升级、
降级或移出部署，core 无从知道某个包的表结构经历过哪些改动；已应用号段一旦记在数据库，文件与记录
脱节之后便无法再对齐。

号段约定：``config_version = N`` 表示已应用至第 N 号迁移。新生成的配置由
:func:`stamp_config_versions` 写入 ``manifest.config_schema_version``，因此首个迁移脚本须从
``config_schema_version + 1`` 起编号；号段一经发布不得复用、重排或跳号。
"""

import asyncio
import importlib.util
import inspect
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger
from tomlkit import parse as toml_parser, dumps as toml_dumps

from core.paths import Paths

if TYPE_CHECKING:
    from tomlkit import TOMLDocument

    from core.registry import PackageEntry

CONFIG_VERSION_KEY = "config_version"
CORE_CONFIG_TABLE = "config"
REVISION_FILENAME_PATTERN = re.compile(r"^(?P<number>\d{4})_(?P<slug>[a-z0-9_]+)\.py$")


@dataclass(frozen=True, slots=True)
class ConfigRevision:
    """一条包内配置迁移。

    :param package: 包名，取自发现层。
    :param number: 目标号段，取自文件名前缀；应用后文件的 config_version 即为该值。
    :param revision: 修订标识，取自文件名（含号段、不含扩展名）。
    :param path: 迁移脚本路径。
    """

    package: str
    number: int
    revision: str
    path: Path


def _config_root() -> Path:
    """取配置根目录。

    配置管理器已加载时以它为准：测试与脚本可能已切换过配置路径。

    :return: 配置目录路径。
    """
    module = sys.modules.get("core.config")
    if module is not None:
        return module.CFGManager.config_path
    return Paths.config


def _config_file(table: str) -> Path:
    """由配置表名推出配置文件路径。

    现行扁平布局下非核心表一名一文件；P4.4 的 ConfigLayout 落地后改由
    ConfigLayout.file_for() 提供同一映射。

    :param table: 配置表名，如 "module_wiki"。
    :return: 配置文件路径。
    """
    return _config_root() / f"{table}.toml"


def _config_table(entry: "PackageEntry") -> str:
    """取包配置所在的表名。

    清单未声明 ``config_table`` 时按装饰器的命名规则回推：适配器为 ``bot_<名>``，
    模块为 ``module_<名>``。

    :param entry: 包条目。
    :return: 配置表名。
    """
    if entry.manifest.config_table:
        return entry.manifest.config_table
    prefix = "bot" if entry.kind == "adapter" else "module"
    return f"{prefix}_{entry.name}"


def iter_config_tables() -> list[tuple["PackageEntry", str]]:
    """列出声明了配置模板的包及其配置表名。

    核心配置不出现在结果中：它由 core/config/update.py 单独维护版本。清单的判定与
    ``PackageRegistry.config_template_paths()`` 同源，均以 ``config.py`` 是否存在为准。

    :return: (包条目, 配置表名) 列表，按包名排序。
    """
    from core.registry import PackageRegistry

    result: list[tuple[Any, str]] = []
    for kind in ("adapter", "module"):
        entries = PackageRegistry.adapters() if kind == "adapter" else PackageRegistry.modules()
        for entry in entries.values():
            if not (entry.root / "config.py").is_file():
                continue
            table = _config_table(entry)
            if table == CORE_CONFIG_TABLE:
                continue
            result.append((entry, table))
    return sorted(result, key=lambda item: item[0].name)


def _collect_revisions(package: str, directory: Path) -> list[ConfigRevision]:
    """收集一个包内的迁移脚本，按号段升序排列。

    :param package: 包名。
    :param directory: 迁移脚本目录。
    :raises ValueError: 号段重复。
    :return: 迁移脚本列表。
    """
    revisions: list[ConfigRevision] = []
    numbers: set[int] = set()
    for path in sorted(directory.glob("*.py")):
        match = REVISION_FILENAME_PATTERN.match(path.name)
        if match is None:
            if path.name != "__init__.py":
                logger.warning(f"[Config] Ignored config migration with invalid name: {path}")
            continue
        number = int(match.group("number"))
        if number in numbers:
            raise ValueError(f"Duplicate config migration number {number} in {directory}")
        numbers.add(number)
        revisions.append(ConfigRevision(package=package, number=number, revision=path.stem, path=path))
    return sorted(revisions, key=lambda revision: revision.number)


def iter_config_revisions() -> dict[str, list[ConfigRevision]]:
    """列出各包声明的配置迁移。

    只认清单 ``config_migrations`` 字段显式声明的目录：``None`` 表示该包不提供配置迁移。

    :return: 包名到迁移脚本列表的映射，无迁移的包不出现在结果中。
    """
    from core.registry import PackageRegistry

    result: dict[str, list[ConfigRevision]] = {}
    for kind in ("adapter", "module"):
        entries = PackageRegistry.adapters() if kind == "adapter" else PackageRegistry.modules()
        for name, entry in entries.items():
            relative = entry.manifest.config_migrations
            if not relative:
                continue
            directory = entry.root / relative
            if not directory.is_dir():
                logger.warning(f"[Config] Config migration directory not found: {directory}")
                continue
            revisions = _collect_revisions(name, directory)
            if revisions:
                result[name] = revisions
    return result


def _document_version(document: "TOMLDocument") -> int | None:
    """读文件自身声明的配置版本号。

    :param document: 解析后的配置文档。
    :return: 版本号；缺失或类型非法时为 ``None``。
    """
    value = document.get(CONFIG_VERSION_KEY)
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _baseline_version(entry: "PackageEntry", revisions: list[ConfigRevision]) -> int:
    """未写版本号的文件所处的版本。

    这类文件生成于本机制落地之前，其内容等价于该包首个迁移之前的状态；包尚无迁移脚本时，
    直接取清单声明的表结构版本。

    :param entry: 包条目。
    :param revisions: 该包的全部迁移脚本，按号段升序。
    :return: 基准版本号。
    """
    if revisions:
        return revisions[0].number - 1
    return entry.manifest.config_schema_version


def _file_version(path: Path, entry: "PackageEntry", revisions: list[ConfigRevision]) -> int:
    """读配置文件当前的配置版本，缺失时回退至基准版本。

    :param path: 配置文件路径。
    :param entry: 包条目。
    :param revisions: 该包的全部迁移脚本。
    :return: 当前版本号。
    """
    version = _document_version(toml_parser(path.read_text(encoding="utf-8")))
    return _baseline_version(entry, revisions) if version is None else version


def _load_revision_hook(revision: ConfigRevision):
    """按文件路径加载迁移脚本的 ``upgrade`` 钩子。

    不经 ``importlib.import_module`` 加载：以号段开头的模块名不是合法标识符，且重复加载会在
    ``sys.modules`` 留下同名残留。脚本声明的 ``REVISION`` 与文件名不一致时立即报错。

    :param revision: 迁移脚本。
    :raises ImportError: 无法加载脚本。
    :raises ValueError: 脚本声明的修订标识与文件名不一致。
    :raises AttributeError: 脚本未提供可调用的 ``upgrade``。
    :return: ``upgrade`` 可调用对象。
    """
    spec = importlib.util.spec_from_file_location(f"akari_config_migration_{revision.revision}", revision.path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load config migration {revision.path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    declared = getattr(module, "REVISION", revision.revision)
    if declared != revision.revision:
        raise ValueError(f"Config migration {revision.path} declares REVISION {declared!r}")
    hook = getattr(module, "upgrade", None)
    if not callable(hook):
        raise AttributeError(f"Config migration {revision.path} has no callable upgrade()")
    return hook


def _run_awaitable(awaitable) -> None:
    """驱动迁移脚本返回的可等待对象。

    调用方可能是同步的启动流程，也可能处在事件循环内；后者不能再执行 ``asyncio.run``，
    故另起线程驱动。

    :param awaitable: 脚本返回的可等待对象。
    """

    async def _drive():
        return await awaitable

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(_drive())
        return
    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.submit(asyncio.run, _drive()).result()


def _run_revision(revision: ConfigRevision, document: "TOMLDocument", table: str) -> None:
    """执行单条迁移脚本。

    :param revision: 迁移脚本。
    :param document: 待迁移的文档，脚本就地修改。
    :param table: 配置表名。
    """
    result = _load_revision_hook(revision)(document, table)
    if inspect.isawaitable(result):
        _run_awaitable(result)


def _write_document(path: Path, document: "TOMLDocument") -> None:
    """原子地写回配置文件。

    :param path: 目标文件路径。
    :param document: 迁移后的文档。
    """
    tmp_path = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        tmp_path.write_text(toml_dumps(document), encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _reload_config_manager() -> None:
    """让已加载的配置管理器丢弃内存副本，避免其随后以迁移前的副本覆盖磁盘。"""
    module = sys.modules.get("core.config")
    if module is not None:
        module.CFGManager.load()


def _upgrade_package(
    entry: "PackageEntry", table: str, path: Path, revisions: list[ConfigRevision]
) -> list[tuple[str, str]]:
    """应用单个包的待办迁移，全部成功后才写回文件。

    :param entry: 包条目。
    :param table: 配置表名。
    :param path: 配置文件路径。
    :param revisions: 该包的全部迁移脚本，按号段升序。
    :return: 实际应用的 (包名, 修订标识) 列表。
    """
    document = toml_parser(path.read_text(encoding="utf-8"))
    version = _document_version(document)
    if version is None:
        version = _baseline_version(entry, revisions)
    todo = [revision for revision in revisions if revision.number > version]
    if not todo:
        return []

    applied: list[tuple[str, str]] = []
    for revision in todo:
        _run_revision(revision, document, table)
        document[CONFIG_VERSION_KEY] = revision.number
        applied.append((entry.name, revision.revision))
    _write_document(path, document)
    return applied


class ConfigMigrationRunner:
    """按包应用配置迁移。

    迁移脚本的 ``upgrade(doc, table)`` 可以是同步函数或协程。整包的号段全部应用成功后才写回
    文件，单条脚本失败不会留下迁移了一半的文件，下一次调用从同一号段重试。
    """

    @classmethod
    def pending(cls) -> dict[str, list[str]]:
        """列出尚未应用的迁移。

        :return: 包名到待应用修订标识列表的映射，无待办时为空字典。
        """
        revisions_by_package = iter_config_revisions()
        result: dict[str, list[str]] = {}
        for entry, table in iter_config_tables():
            revisions = revisions_by_package.get(entry.name)
            path = _config_file(table)
            if not revisions or not path.is_file():
                continue
            version = _file_version(path, entry, revisions)
            todo = [revision.revision for revision in revisions if revision.number > version]
            if todo:
                result[entry.name] = todo
        return result

    @classmethod
    def upgrade(cls, package: str | None = None) -> list[tuple[str, str]]:
        """应用待办的配置迁移。

        单个包失败时记录异常并跳过该包，其余包继续处理；失败包的文件保持原样，
        ``pending()`` 会在下一次调用时重新列出它。

        :param package: 限定包名；``None`` 表示全部包。
        :return: 实际写入磁盘的 (包名, 修订标识) 列表。
        """
        revisions_by_package = iter_config_revisions()
        applied: list[tuple[str, str]] = []
        for entry, table in iter_config_tables():
            if package is not None and entry.name != package:
                continue
            revisions = revisions_by_package.get(entry.name)
            path = _config_file(table)
            if not revisions or not path.is_file():
                continue
            try:
                applied.extend(_upgrade_package(entry, table, path, revisions))
            except Exception:
                logger.exception(f"[Config] Failed to migrate the config of package {entry.name!r}: ")
        if applied:
            _reload_config_manager()
        return applied


def stamp_config_versions() -> list[str]:
    """把包清单声明的表结构版本写入各自的配置文件。

    生成阶段在模板扫描之后调用：先由扫描建立缺失的配置文件，再写入版本号，迁移运行器才能
    判断某个文件已走到哪一号段。核心配置不出现在结果中，其版本由 core/config/update.py 维护。

    :return: 被写入或更新的配置表名列表。
    """
    stamped: list[str] = []
    for entry, table in iter_config_tables():
        path = _config_file(table)
        if not path.is_file():
            continue
        target = entry.manifest.config_schema_version
        document = toml_parser(path.read_text(encoding="utf-8"))
        if _document_version(document) == target:
            continue
        document[CONFIG_VERSION_KEY] = target
        _write_document(path, document)
        stamped.append(table)
    if stamped:
        _reload_config_manager()
    return stamped
