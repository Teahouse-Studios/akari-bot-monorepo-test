"""旧项目迁移：把旧版 AkariBot 项目搬进实例目录。

CLI 进程不 import core：旧配置用 ``tomllib`` 读、旧库用 ``sqlite3`` 以只读方式直读，数据库
版本号转换交给既有的 ``akaribot.core.entrypoints.db`` 子进程。旧项目目录全程只读。
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Any, Mapping

import typer
from rich.markdown import Markdown
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands.module import _install as install_package
from akaribot.cli.instance import (
    DEFAULT_LOCALE,
    DEFAULT_VENV,
    INSTANCE_META_FILENAME,
    CliError,
    Instance,
    InstanceMeta,
    console,
    explain_process_failure,
    extract_json,
    fail,
    now_iso,
    ok,
    step,
    system_python,
    warn,
)

app = typer.Typer(help=i18n.t("cli.migrate.help"), no_args_is_help=True)

# 旧项目的判定条件：四者同时存在（monorepo_refactor_plan.md §3.5）。
REQUIRED_ENTRIES = ("bot.py", "core", "modules")
OLD_CONFIG_FILE = "config/config.toml"
OLD_CONFIG_DIR = "config"
OLD_DATABASE_DIR = "database"
OLD_MODULES_DIR = "modules"
CORE_MODULE_DIR = "core"
ADAPTER_DIST_PREFIX = "akari-bot-adapter-"

# 旧 assets 布局到新实例 data 布局的对照，与 core/scripts/migrate_assets_to_data.py 的 MOVES 一致。
ASSET_MOVES = (
    ("assets/i18n_cache", "data/i18n_cache"),
    ("assets/private", "data/private"),
    ("assets/union_merge_logs", "data/union_merge_logs"),
    ("assets/bad_words", "data/filter_words"),
    ("assets/retired", "data/retired"),
    ("assets/url_audit/allowlist/user.txt", "data/url_audit/allowlist/user.txt"),
    ("assets/url_audit/blocklist/user.txt", "data/url_audit/blocklist/user.txt"),
)


@dataclass
class LegacyProject:
    """旧项目的只读视图。

    :param root: 旧项目根目录。
    :param config_files: ``config/*.toml``。
    :param database_files: ``database/*.db`` 及其 ``-wal`` / ``-shm``。
    :param module_dirs: ``modules/`` 下的模块目录名。
    :param enabled_modules: 旧库 ``module_status`` 里 ``load = 1`` 的模块名。
    :param adapters: 旧配置里 ``enable = true`` 的平台名。
    :param locale: 旧配置的 ``default_locale``。
    :param db_path: 旧配置的 ``db_path``。
    :param config_failures: 解析失败的配置文件说明。
    """

    root: Path
    config_files: tuple[Path, ...] = ()
    database_files: tuple[Path, ...] = ()
    module_dirs: tuple[str, ...] = ()
    enabled_modules: tuple[str, ...] = ()
    adapters: tuple[str, ...] = ()
    locale: str = DEFAULT_LOCALE
    db_path: str = ""
    config_failures: tuple[str, ...] = ()


@dataclass
class MigrationPlan:
    """迁移计划：模块映射结果与要安装的包。

    :param modules: ``(旧模块名, 新分发名, 名字来源)`` 三元组。
    :param unmapped: 没有对应分发包的旧模块名。
    :param adapters: 由旧配置推导出的适配器分发名。
    :param missing_adapters: registry 中没有对应条目的适配器分发名。
    """

    modules: list[tuple[str, str, str]] = field(default_factory=list)
    unmapped: list[str] = field(default_factory=list)
    adapters: list[str] = field(default_factory=list)
    missing_adapters: list[str] = field(default_factory=list)

    @property
    def module_dists(self) -> list[str]:
        """去重后的模块分发名，保持首次出现顺序。"""
        return list(dict.fromkeys(dist for _, dist, _ in self.modules))


@dataclass
class CopyTally:
    """一类内容的复制结果，供报告计数。

    :param name: 类别名，如「配置文件」。
    :param copied: 本次复制或计划复制的相对路径。
    :param unchanged: 目标已存在且内容一致、无需复制的相对路径。
    :param kept: 目标已存在且内容不同、保留目标的相对路径。
    :param missing: 旧项目里找不到的条目。
    """

    name: str
    copied: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


@dataclass
class MigrationLog:
    """迁移过程记录，报告由它生成。"""

    tallies: list[CopyTally] = field(default_factory=list)
    installed: list[str] = field(default_factory=list)
    install_skipped: list[str] = field(default_factory=list)
    install_failed: list[tuple[str, str]] = field(default_factory=list)
    placeholders: list[tuple[str, int]] = field(default_factory=list)
    credential_files: list[str] = field(default_factory=list)
    database_note: str = ""
    db_result: str = "未执行"


def _legacy_key(name: str) -> str:
    """旧模块名归一：小写并把连字符换成下划线（registry 的映射键即此口径）。"""
    return name.strip().lower().replace("-", "_")


def _inspect(root: Path) -> LegacyProject:
    """校验旧项目结构并读出迁移所需的事实。

    :param root: 旧项目根目录。
    :return: 只读视图。
    :raises CliError: 目录不存在或缺少旧项目的判定文件。
    """
    if not root.exists():
        raise CliError(i18n.t("cli.migrate.error.project_missing", path=root))
    if not root.is_dir():
        raise CliError(i18n.t("cli.migrate.error.project_not_dir", path=root))
    missing = [name for name in REQUIRED_ENTRIES if not (root / name).exists()]
    if not (root / OLD_CONFIG_FILE).is_file():
        missing.append(OLD_CONFIG_FILE)
    if missing:
        raise CliError(
            i18n.t(
                "cli.migrate.error.not_legacy",
                path=root,
                missing=i18n.t("cli.common.list_separator").join(missing),
            )
        )

    library = _read_config_facts(root)
    database_dir = root / OLD_DATABASE_DIR
    database_files = tuple(sorted(path for path in database_dir.glob("*.db*") if path.is_file()))
    return LegacyProject(
        root=root,
        config_files=library.config_files,
        database_files=database_files,
        module_dirs=_module_dirs(root / OLD_MODULES_DIR),
        enabled_modules=_enabled_modules(database_files),
        adapters=library.adapters,
        locale=library.locale,
        db_path=library.db_path,
        config_failures=library.failures,
    )


@dataclass
class _ConfigFacts:
    """旧配置读取结果的中间结构。"""

    config_files: tuple[Path, ...]
    adapters: tuple[str, ...]
    locale: str
    db_path: str
    failures: tuple[str, ...]


def _read_config_facts(root: Path) -> _ConfigFacts:
    """读 ``config/*.toml``：汇总表名、启用平台、默认语言与数据库连接串。"""
    config_files = tuple(sorted(path for path in (root / OLD_CONFIG_DIR).glob("*.toml") if path.is_file()))
    tables: dict[str, Mapping[str, Any]] = {}
    failures: list[str] = []
    for path in config_files:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            failures.append(f"{path.relative_to(root)}：{exc}")
            continue
        for table, value in data.items():
            if isinstance(value, Mapping):
                tables[table] = value
    core = tables.get("config") or {}
    adapters: list[str] = []
    for table, value in tables.items():
        if not table.startswith("bot_"):
            continue
        platform = table[len("bot_") :]
        # 带实例 ID 的表（bot_telegram-alt）是派生物，迁移只认基表。
        if platform and "-" not in platform and value.get("enable") is True:
            adapters.append(platform)
    return _ConfigFacts(
        config_files=config_files,
        adapters=tuple(sorted(adapters)),
        locale=str(core.get("default_locale") or DEFAULT_LOCALE),
        db_path=str(core.get("db_path") or ""),
        failures=tuple(failures),
    )


def _module_dirs(modules_root: Path) -> tuple[str, ...]:
    """列出旧 ``modules/`` 下带 ``__init__.py`` 的模块目录名；``core`` 属核心，不计入。"""
    if not modules_root.is_dir():
        return ()
    names: list[str] = []
    for child in sorted(modules_root.iterdir()):
        if not child.is_dir() or child.name.startswith((".", "_")) or child.name == CORE_MODULE_DIR:
            continue
        if (child / "__init__.py").is_file():
            names.append(child.name)
    return tuple(names)


def _enabled_modules(database_files: tuple[Path, ...]) -> tuple[str, ...]:
    """从旧 SQLite 库的 ``module_status`` 读启用过的模块名；库不可读时返回空元组。"""
    names: list[str] = []
    for path in database_files:
        if not path.name.endswith(".db"):
            continue
        try:
            with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as conn:
                rows = conn.execute("SELECT module_name FROM module_status WHERE load = 1").fetchall()
        except sqlite3.Error:
            continue
        names.extend(str(row[0]) for row in rows if row and row[0])
    return tuple(dict.fromkeys(names))


def _target_root(project_root: Path, instance: Path | None) -> Path:
    """解析新实例根：显式 ``--instance`` 优先，缺省为旧项目同级的 ``<旧项目名>-instance``。"""
    if instance is not None:
        return instance.expanduser().resolve()
    return (project_root.parent / f"{project_root.name}-instance").resolve()


def _load_catalog(workspace_root: Path | None, *, offline: bool) -> engine.RegistryCatalog:
    """加载 registry：工作区里有 ``registry.json`` 时优先本地文件，保证映射可离线复现。"""
    roots: list[Path] = []
    if workspace_root is not None:
        roots.append(workspace_root)
    else:
        detected = engine.find_workspace_root(Path.cwd())
        if detected is not None:
            roots.append(detected)
    for root in roots:
        path = root / "registry.json"
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CliError(i18n.t("cli.migrate.error.registry_parse", path=path, error=exc)) from exc
        return engine.RegistryCatalog.from_payload(payload, source=str(path))
    try:
        return engine.RegistryCatalog.load(offline=offline)
    except CliError as exc:
        raise CliError(i18n.t("cli.migrate.error.registry_load", error=exc)) from exc


def _legacy_index(catalog: engine.RegistryCatalog) -> dict[str, str]:
    """旧模块名到新分发名的索引；``provides_modules`` 与 ``legacy_module_map`` 一并收录。"""
    index: dict[str, str] = {}
    for entry in catalog.entries.values():
        if entry.kind != "module":
            continue
        for name in (*entry.provides_modules, *entry.legacy_module_map):
            key = _legacy_key(name)
            if key and key not in index:
                index[key] = entry.dist
    return index


def _plan_migration(legacy: LegacyProject, index: dict[str, str], catalog: engine.RegistryCatalog) -> MigrationPlan:
    """由旧项目事实与 registry 映射算出迁移计划。"""
    known_adapters = {engine.canonical(entry.dist) for entry in catalog.entries.values() if entry.kind == "adapter"}
    plan = MigrationPlan()
    for platform in legacy.adapters:
        dist = f"{ADAPTER_DIST_PREFIX}{platform}"
        plan.adapters.append(dist)
        if engine.canonical(dist) not in known_adapters:
            plan.missing_adapters.append(dist)
    candidates = sorted(set(legacy.module_dirs) | set(legacy.enabled_modules))
    for name in candidates:
        sources: list[str] = []
        if name in legacy.module_dirs:
            sources.append(i18n.t("cli.migrate.source.dir"))
        if name in legacy.enabled_modules:
            sources.append(i18n.t("cli.migrate.source.database"))
        dist = index.get(_legacy_key(name))
        if dist:
            plan.modules.append((name, dist, "＋".join(sources)))
        else:
            plan.unmapped.append(name)
    return plan


def _prepare_instance(
    root: Path, legacy: LegacyProject, *, workspace_root: Path | None, managed: bool, force: bool
) -> Instance:
    """创建或复用实例；目录与 ``akaribot.toml`` 均走 ``akaribot init`` 的既有路径。

    :raises CliError: 目标非空且不是实例，或实例正在运行。
    """
    if (root / INSTANCE_META_FILENAME).is_file():
        instance = Instance(root)
        if instance.is_running():
            raise CliError(i18n.t("cli.migrate.error.running", path=root))
        console.print(i18n.t("cli.migrate.reuse_instance", path=root))
        return instance
    if root.exists() and any(root.iterdir()) and not force:
        raise CliError(i18n.t("cli.migrate.error.target_not_empty", path=root))
    created = Instance.create_dirs(root)
    meta = InstanceMeta.create(
        root,
        locale=legacy.locale,
        mode="workspace" if workspace_root else "installed",
        venv=DEFAULT_VENV if managed else "",
        workspace_root=str(workspace_root) if workspace_root else "",
    )
    meta.save()
    ok(i18n.t("cli.migrate.instance_created", root=root, count=len(created), locale=legacy.locale))
    return Instance(root)


def _copy_file(
    source: Path,
    target: Path,
    *,
    force: bool,
    dry_run: bool,
    tally: CopyTally,
    rel: str,
    compare: bool = True,
) -> None:
    """复制单个文件；内容一致则跳过，不同则默认保留目标，``--force`` 时覆盖。

    :param compare: 为假时只按目标是否存在判断（大文件与数据库文件用）。
    """
    if target.is_file():
        if compare and not force and target.read_bytes() == source.read_bytes():
            tally.unchanged.append(rel)
            return
        if not force:
            tally.kept.append(rel)
            return
    if dry_run:
        tally.copied.append(rel)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    tally.copied.append(rel)


def _copy_tree(source: Path, target: Path, *, force: bool, dry_run: bool, tally: CopyTally, rel: str) -> None:
    """递归复制目录，逐文件套用 :func:`_copy_file` 的重入规则。"""
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source).as_posix()
        _copy_file(
            path,
            target / relative,
            force=force,
            dry_run=dry_run,
            tally=tally,
            rel=f"{rel}/{relative}",
        )


def _copy_payload(legacy: LegacyProject, instance: Instance, *, force: bool, dry_run: bool, log: MigrationLog) -> None:
    """复制配置、数据库、旧 assets 与模块的部署者数据，并记录结果。"""
    config = CopyTally(i18n.t("cli.migrate.tally.config"))
    log.tallies.append(config)
    for path in legacy.config_files:
        _copy_file(
            path,
            instance.config_dir / path.name,
            force=force,
            dry_run=dry_run,
            tally=config,
            rel=f"config/{path.name}",
        )

    database = CopyTally(i18n.t("cli.migrate.tally.database"))
    log.tallies.append(database)
    for path in legacy.database_files:
        _copy_file(
            path,
            instance.root / OLD_DATABASE_DIR / path.name,
            force=force,
            dry_run=dry_run,
            tally=database,
            rel=f"database/{path.name}",
            compare=False,
        )

    runtime = CopyTally(i18n.t("cli.migrate.tally.runtime"))
    log.tallies.append(runtime)
    for source_rel, target_rel in ASSET_MOVES:
        source = legacy.root / source_rel
        if not source.exists():
            runtime.missing.append(source_rel)
            continue
        target = instance.root / target_rel
        if source.is_dir():
            _copy_tree(source, target, force=force, dry_run=dry_run, tally=runtime, rel=target_rel)
        else:
            _copy_file(source, target, force=force, dry_run=dry_run, tally=runtime, rel=target_rel)

    for name in legacy.module_dirs:
        source = legacy.root / OLD_MODULES_DIR / name / "data"
        if source.is_dir():
            target_rel = f"data/module/{name}"
            _copy_tree(source, instance.root / target_rel, force=force, dry_run=dry_run, tally=runtime, rel=target_rel)


def _resolve_target(name: str, *, kind: str, workspace_root: Path | None) -> engine.InstallTarget:
    """解析安装目标：工作区模式取本地源码，否则按分发名安装。"""
    try:
        return engine.resolve_target(name, workspace_root=workspace_root, dist=name, kind=kind)
    except CliError as exc:
        raise CliError(i18n.t("cli.migrate.error.resolve", name=name, error=exc)) from exc


def _install_packages(
    instance: Instance,
    targets: list[tuple[str, str]],
    *,
    workspace_root: Path | None,
    force: bool,
    dry_run: bool,
    verbose: bool,
    log: MigrationLog,
) -> None:
    """按 core、适配器、模块的顺序安装；单个包失败只记入报告，不中断整体迁移。"""
    for kind, dist in targets:
        try:
            target = _resolve_target(dist, kind=kind, workspace_root=workspace_root)
        except CliError as exc:
            log.install_failed.append((dist, str(exc)))
            warn(i18n.t("cli.migrate.resolve_failed", dist=dist, error=exc))
            continue
        try:
            if not force and instance.find_package(target.dist) is not None:
                # install_skipped 会写进迁移报告，属报告取值，保持原文。
                log.install_skipped.append(f"{target.dist}（已安装）")
                ok(i18n.t("cli.migrate.already_installed", dist=target.dist))
                continue
        except CliError:
            pass
        try:
            install_package(instance, target, force=force, dry_run=dry_run, verbose=verbose)
            log.installed.append(target.dist)
        except typer.Exit as exc:
            # 安装流水线失败时自行回滚并以退出码结束；迁移继续，失败项交报告提示人工重试。
            log.install_failed.append((target.dist, f"安装流水线以退出码 {exc.exit_code} 结束"))
            warn(i18n.t("cli.migrate.install_failed", dist=target.dist))


def _convert_database(instance: Instance, legacy: LegacyProject, *, log: MigrationLog) -> None:
    """在副本上执行旧版本号转换：复用 core 的 db 入口，不重写版本逻辑。"""
    if legacy.db_path and not legacy.db_path.startswith("sqlite"):
        log.db_result = f"跳过：旧配置使用非 SQLite 数据库（{legacy.db_path}），数据须自行 dump 后导入。"
        return
    if not instance.python_exists:
        log.db_result = "跳过：实例解释器不存在（--skip-install 或 venv 未建），装好 core 后重跑本命令即可补做。"
        return
    try:
        proc = instance.run_core_capture("db", "upgrade", "--package", "akari-bot-core", "--json", timeout=None)
    except CliError as exc:
        log.db_result = f"跳过：{exc}"
        return
    if proc.returncode != 0:
        log.db_result = explain_process_failure(proc, "数据库版本转换失败")
        warn(log.db_result)
        return
    applied = 0
    try:
        payload = extract_json(proc.stdout or "")
    except CliError:
        payload = None
    if isinstance(payload, Mapping) and isinstance(payload.get("applied"), list):
        applied = len(payload["applied"])
    log.db_result = f"完成：已登记 {applied} 项迁移；旧版本号转换由 core 的 convert_legacy_version() 完成。"
    ok(log.db_result)


def _scan_placeholders(instance: Instance, log: MigrationLog) -> None:
    """统计复制后配置里的 ``<Replace me>``，并单独标出待填凭据的适配器文件。"""
    counts: dict[str, int] = {}
    for path in sorted(instance.config_dir.glob("*.toml")):
        count = engine.count_placeholders([path])
        if count:
            counts[path.name] = count
            log.placeholders.append((f"config/{path.name}", count))
    log.credential_files = sorted(name for name in counts if name.startswith("bot_"))


def _render_report(
    legacy: LegacyProject, instance: Instance, plan: MigrationPlan, log: MigrationLog, *, dry_run: bool
) -> str:
    """生成 Markdown 迁移报告全文。"""
    lines: list[str] = [
        i18n.t("cli.migrate.report.title"),
        "",
        i18n.t("cli.migrate.report.generated_at", time=now_iso()),
        i18n.t("cli.migrate.report.old_project", path=legacy.root),
        i18n.t("cli.migrate.report.new_instance", path=instance.root),
        i18n.t("cli.migrate.report.mode", mode=i18n.t(f"cli.migrate.report.mode_{'dry_run' if dry_run else 'real'}")),
        "",
        i18n.t("cli.migrate.report.copy_heading"),
        "",
        i18n.t("cli.migrate.report.copy_header"),
        i18n.t("cli.migrate.report.copy_sep"),
    ]
    for tally in log.tallies:
        lines.append(
            i18n.t(
                "cli.migrate.report.copy_row",
                name=tally.name,
                copied=len(tally.copied),
                unchanged=len(tally.unchanged),
                kept=len(tally.kept),
                missing=len(tally.missing),
            )
        )
    lines += ["", i18n.t("cli.migrate.report.modules_heading"), ""]
    if plan.modules:
        lines += [i18n.t("cli.migrate.report.modules_header"), i18n.t("cli.migrate.report.modules_sep")]
        for name, dist, source in plan.modules:
            lines.append(i18n.t("cli.migrate.report.modules_row", name=name, dist=dist, source=source))
        lines += ["", i18n.t("cli.migrate.report.modules_note")]
    else:
        lines.append(i18n.t("cli.migrate.report.no_modules"))
    lines += ["", i18n.t("cli.migrate.report.adapters_heading"), ""]
    if plan.adapters:
        for dist in plan.adapters:
            note = i18n.t("cli.migrate.report.adapter_missing") if dist in plan.missing_adapters else ""
            lines.append(i18n.t("cli.migrate.report.adapter_item", dist=dist, note=note))
    else:
        lines.append(i18n.t("cli.migrate.report.no_adapters"))
    lines += ["", i18n.t("cli.migrate.report.install_heading"), ""]
    if log.installed:
        items = i18n.t("cli.common.list_separator").join(f"`{dist}`" for dist in log.installed)
        lines.append(i18n.t("cli.migrate.report.installed", items=items))
    if log.install_skipped:
        items = i18n.t("cli.common.list_separator").join(f"`{item}`" for item in log.install_skipped)
        lines.append(i18n.t("cli.migrate.report.install_skipped", items=items))
    if log.install_failed:
        for dist, reason in log.install_failed:
            lines.append(i18n.t("cli.migrate.report.install_failed_item", dist=dist, reason=reason))
    if not (log.installed or log.install_skipped or log.install_failed):
        lines.append(i18n.t("cli.migrate.report.nothing_installed"))
    lines += [
        "",
        i18n.t("cli.migrate.report.db_result", result=log.db_result),
        "",
        i18n.t("cli.migrate.report.manual_heading"),
        "",
    ]
    manual: list[str] = []
    if plan.unmapped:
        items = i18n.t("cli.common.list_separator").join(f"`{name}`" for name in plan.unmapped)
        manual.append(i18n.t("cli.migrate.report.manual_unmapped", items=items))
    if plan.missing_adapters:
        items = i18n.t("cli.common.list_separator").join(f"`{dist}`" for dist in plan.missing_adapters)
        manual.append(i18n.t("cli.migrate.report.manual_missing_adapters", items=items))
    if log.install_failed:
        items = i18n.t("cli.common.list_separator").join(f"`{dist}`" for dist, _ in log.install_failed)
        manual.append(i18n.t("cli.migrate.report.manual_install_failed", items=items))
    if log.credential_files:
        items = i18n.t("cli.common.list_separator").join(f"`config/{name}`" for name in log.credential_files)
        manual.append(i18n.t("cli.migrate.report.manual_credentials", items=items))
    if log.placeholders:
        total = sum(count for _, count in log.placeholders)
        items = i18n.t("cli.common.list_separator").join(f"`{path}`" for path, _ in log.placeholders)
        manual.append(i18n.t("cli.migrate.report.manual_placeholders", total=total, items=items))
    if legacy.config_failures:
        items = i18n.t("cli.common.list_separator").join(f"`{name}`" for name in legacy.config_failures)
        manual.append(i18n.t("cli.migrate.report.manual_config_failures", items=items))
    if log.database_note:
        manual.append(log.database_note)
    # db_result 是报告里的取值（且被 startswith 用作状态判断），保持原文；此处只判断状态。
    if log.db_result.startswith(("失败", "跳过")):
        manual.append(i18n.t("cli.migrate.report.manual_db_result", result=log.db_result))
    if manual:
        lines += [i18n.t("cli.migrate.report.manual_item", item=item) for item in manual]
    else:
        lines.append(i18n.t("cli.migrate.report.manual_none"))
    lines += [
        "",
        i18n.t("cli.migrate.report.multi_heading"),
        "",
        i18n.t("cli.migrate.report.multi_note"),
        "",
    ]
    return "\n".join(lines)


def _print_plan(legacy: LegacyProject, target: Path, plan: MigrationPlan) -> None:
    """打印迁移计划，供执行前确认。"""
    table = Table(title=i18n.t("cli.migrate.plan.title"), show_header=False, padding=(0, 2))
    table.add_row(i18n.t("cli.migrate.plan.old"), str(legacy.root))
    table.add_row(i18n.t("cli.migrate.plan.new"), str(target))
    separator = i18n.t("cli.common.list_separator")
    none = i18n.t("cli.migrate.none")
    table.add_row(i18n.t("cli.migrate.plan.adapters"), separator.join(plan.adapters) or none)
    table.add_row(i18n.t("cli.migrate.plan.modules"), separator.join(plan.module_dists) or none)
    table.add_row(i18n.t("cli.migrate.plan.unmapped"), separator.join(plan.unmapped) or none)
    console.print(table)


@app.command("legacy", help=i18n.t("cli.migrate.legacy.help"))
def legacy(
    project: Annotated[Path, typer.Argument(help=i18n.t("cli.migrate.legacy.arg_project"))],
    instance: Annotated[
        Path | None,
        typer.Option("--instance", "-I", help=i18n.t("cli.migrate.legacy.option_instance")),
    ] = None,
    workspace_root: Annotated[
        Path | None,
        typer.Option("--workspace-root", "--dev", help=i18n.t("cli.migrate.legacy.option_workspace_root")),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.migrate.legacy.option_dry_run"))] = False,
    skip_install: Annotated[
        bool, typer.Option("--skip-install", help=i18n.t("cli.migrate.legacy.option_skip_install"))
    ] = False,
    no_venv: Annotated[bool, typer.Option("--no-venv", help=i18n.t("cli.migrate.legacy.option_no_venv"))] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.migrate.legacy.option_force"))] = False,
    offline: Annotated[bool, typer.Option("--offline", help=i18n.t("cli.migrate.legacy.option_offline"))] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.migrate.legacy.option_verbose"))] = False,
) -> None:
    """把旧版项目迁移为新实例：搬配置与数据、装映射到的适配器与模块、转换数据库版本。

    旧目录只读；迁移可重复执行，已完成的步骤不会重复施加。报告写到新实例根的 migration-report.md。
    """
    root = project.expanduser().resolve()
    step(1, 6, i18n.t("cli.migrate.step.inspect"))
    try:
        legacy_project = _inspect(root)
    except CliError as exc:
        fail(str(exc))
    ok(
        i18n.t(
            "cli.migrate.inspected",
            root=root,
            configs=len(legacy_project.config_files),
            databases=len(legacy_project.database_files),
            modules=len(legacy_project.module_dirs),
            enabled=len(legacy_project.enabled_modules),
        )
    )
    for failure in legacy_project.config_failures:
        warn(i18n.t("cli.migrate.config_failure", error=failure))

    target = _target_root(root, instance)
    if target == root or target.is_relative_to(root):
        fail(i18n.t("cli.migrate.error.target_inside", path=target))
    if workspace_root is not None:
        workspace_root = workspace_root.expanduser().resolve()
        if not (workspace_root / "packages").is_dir():
            fail(i18n.t("cli.migrate.error.not_workspace", path=workspace_root))

    step(2, 6, i18n.t("cli.migrate.step.mapping"))
    try:
        catalog = _load_catalog(workspace_root, offline=offline)
    except CliError as exc:
        fail(str(exc))
    index = _legacy_index(catalog)
    if not index:
        fail(i18n.t("cli.migrate.error.no_mapping"))
    plan = _plan_migration(legacy_project, index, catalog)
    _print_plan(legacy_project, target, plan)
    if plan.unmapped:
        unmapped = i18n.t("cli.common.list_separator").join(plan.unmapped)
        warn(i18n.t("cli.migrate.unmapped", modules=unmapped))

    managed = not no_venv
    log = MigrationLog()
    if dry_run:
        instance = Instance.detached(
            target,
            locale=legacy_project.locale,
            venv=DEFAULT_VENV if managed else "",
            workspace_root=str(workspace_root) if workspace_root else "",
            mode="workspace" if workspace_root else "installed",
        )
        console.print(i18n.t("cli.migrate.dry_run_create", path=target))
    else:
        step(3, 6, i18n.t("cli.migrate.step.create"))
        try:
            instance = _prepare_instance(
                target, legacy_project, workspace_root=workspace_root, managed=managed, force=force
            )
        except CliError as exc:
            fail(str(exc))

    step(4, 6, i18n.t("cli.migrate.step.copy"))
    _copy_payload(legacy_project, instance, force=force, dry_run=dry_run, log=log)
    for tally in log.tallies:
        console.print(
            i18n.t(
                "cli.migrate.copy_line",
                name=tally.name,
                copied=len(tally.copied),
                unchanged=len(tally.unchanged),
                kept=len(tally.kept),
            )
        )

    step(5, 6, i18n.t("cli.migrate.step.install"))
    targets: list[tuple[str, str]] = [("core", "akari-bot-core")]
    targets.extend(("adapter", dist) for dist in plan.adapters)
    targets.extend(("module", dist) for dist in plan.module_dists)
    if dry_run or skip_install:
        reason = "dry-run" if dry_run else "--skip-install"
        console.print(i18n.t("cli.migrate.skip_install", reason=reason, count=len(targets)))
        log.install_skipped.extend(dist for _, dist in targets)
    else:
        if managed and not instance.venv_dir.exists():
            runner = engine.CommandRunner(dry_run=False, verbose=verbose)
            try:
                # what 会被 venv.py 拼成「{what}完成/失败」，该层不在本次范围内，保持原文。
                runner.run_checked(
                    engine.create_venv_argv(instance.venv_dir, python=str(system_python())),
                    what="创建实例 venv",
                )
            except CliError as exc:
                fail(i18n.t("cli.migrate.venv_failed", error=exc))
        _install_packages(
            instance,
            targets,
            workspace_root=workspace_root,
            force=force,
            dry_run=False,
            verbose=verbose,
            log=log,
        )

    if dry_run:
        log.db_result = "未执行（dry-run）"
    else:
        _convert_database(instance, legacy_project, log=log)
        _scan_placeholders(instance, log)

    report = _render_report(legacy_project, instance, plan, log, dry_run=dry_run)
    step(6, 6, i18n.t("cli.migrate.step.report"))
    if dry_run:
        console.print(Markdown(report))
        console.print(i18n.t("cli.migrate.dry_run_no_write"))
        return
    report_path = instance.root / "migration-report.md"
    report_path.write_text(report, encoding="utf-8")
    ok(i18n.t("cli.migrate.report_written", path=report_path))
    if log.install_failed or plan.unmapped:
        console.print(i18n.t("cli.migrate.next_steps_manual"))
    else:
        console.print(i18n.t("cli.migrate.next_steps", path=instance.root))
