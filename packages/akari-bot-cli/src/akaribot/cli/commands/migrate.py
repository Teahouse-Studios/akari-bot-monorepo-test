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

app = typer.Typer(help="旧项目迁移：把旧版布局的项目搬进实例目录（migrate legacy）", no_args_is_help=True)

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
        raise CliError(f"旧项目目录不存在：{root}")
    if not root.is_dir():
        raise CliError(f"旧项目路径不是目录：{root}")
    missing = [name for name in REQUIRED_ENTRIES if not (root / name).exists()]
    if not (root / OLD_CONFIG_FILE).is_file():
        missing.append(OLD_CONFIG_FILE)
    if missing:
        raise CliError(
            f"{root} 不像是旧版 AkariBot 项目，缺少：{'、'.join(missing)}。"
            "旧项目须同时含 bot.py、core/、modules/ 与 config/config.toml。"
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
            raise CliError(f"{path} 无法解析：{exc}") from exc
        return engine.RegistryCatalog.from_payload(payload, source=str(path))
    try:
        return engine.RegistryCatalog.load(offline=offline)
    except CliError as exc:
        raise CliError(
            f"无法加载 registry（{exc}）。用 --workspace-root 指向含 registry.json 的工作区根，或联网后重试。"
        ) from exc


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
            sources.append("目录")
        if name in legacy.enabled_modules:
            sources.append("数据库")
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
            raise CliError(f"{root} 的机器人正在运行。先停机再迁移。")
        console.print(f"  复用已有实例：{root}")
        return instance
    if root.exists() and any(root.iterdir()) and not force:
        raise CliError(f"{root} 非空且不是 AkariBot 实例。换一个空目录，或确认可写入后加 --force。")
    created = Instance.create_dirs(root)
    meta = InstanceMeta.create(
        root,
        locale=legacy.locale,
        mode="workspace" if workspace_root else "installed",
        venv=DEFAULT_VENV if managed else "",
        workspace_root=str(workspace_root) if workspace_root else "",
    )
    meta.save()
    ok(f"已建实例 {root}（新建目录 {len(created)} 个，语言 {legacy.locale}）")
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
    config = CopyTally("配置文件")
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

    database = CopyTally("数据库文件")
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

    runtime = CopyTally("运行期资源")
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
        raise CliError(f"无法解析 {name}：{exc}") from exc


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
            warn(f"{dist} 解析失败：{exc}")
            continue
        try:
            if not force and instance.find_package(target.dist) is not None:
                log.install_skipped.append(f"{target.dist}（已安装）")
                ok(f"{target.dist} 已安装，跳过")
                continue
        except CliError:
            pass
        try:
            install_package(instance, target, force=force, dry_run=dry_run, verbose=verbose)
            log.installed.append(target.dist)
        except typer.Exit as exc:
            # 安装流水线失败时自行回滚并以退出码结束；迁移继续，失败项交报告提示人工重试。
            log.install_failed.append((target.dist, f"安装流水线以退出码 {exc.exit_code} 结束"))
            warn(f"{target.dist} 安装失败，已记入报告；可重跑本命令或手动 `akaribot module add {target.dist}`。")


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
        "# 旧项目迁移报告",
        "",
        f"- 生成时间：{now_iso()}",
        f"- 旧项目：`{legacy.root}`（只读，迁移全程未修改）",
        f"- 新实例：`{instance.root}`",
        f"- 运行模式：{'dry-run（未写入任何文件）' if dry_run else '正式执行'}",
        "",
        "## 复制结果",
        "",
        "| 类别 | 复制 | 内容一致 | 保留现有 | 旧项目缺失 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for tally in log.tallies:
        lines.append(
            f"| {tally.name} | {len(tally.copied)} | {len(tally.unchanged)} | {len(tally.kept)} | {len(tally.missing)} |"
        )
    lines += ["", "## 模块映射", ""]
    if plan.modules:
        lines += ["| 旧模块名 | 新分发名 | 名字来源 |", "| --- | --- | --- |"]
        for name, dist, source in plan.modules:
            lines.append(f"| `{name}` | `{dist}` | {source} |")
        lines += ["", "映射取 registry 的 `legacy_module_map`；多个旧模块名可指向同一分发（如 wiki 家族）。"]
    else:
        lines.append("旧项目里没有可映射的模块。")
    lines += ["", "## 适配器", ""]
    if plan.adapters:
        for dist in plan.adapters:
            note = "（registry 中无此适配器包）" if dist in plan.missing_adapters else ""
            lines.append(f"- `{dist}`{note}")
    else:
        lines.append("旧配置里没有 `enable = true` 的适配器基表。")
    lines += ["", "## 安装结果", ""]
    if log.installed:
        lines.append("- 本次安装：" + "、".join(f"`{dist}`" for dist in log.installed))
    if log.install_skipped:
        lines.append("- 已装跳过：" + "、".join(f"`{item}`" for item in log.install_skipped))
    if log.install_failed:
        for dist, reason in log.install_failed:
            lines.append(f"- 安装失败：`{dist}`——{reason}")
    if not (log.installed or log.install_skipped or log.install_failed):
        lines.append("- 未安装任何包（`--skip-install` 或 dry-run）。")
    lines += ["", f"- 数据库版本转换：{log.db_result}", "", "## 需人工处理", ""]
    manual: list[str] = []
    if plan.unmapped:
        manual.append(
            "无法映射的旧模块："
            + "、".join(f"`{name}`" for name in plan.unmapped)
            + "。多为自写模块，打包后用 `akaribot module add -e <模块目录>` 安装。"
        )
    if plan.missing_adapters:
        manual.append(
            "registry 中没有对应条目，需先发布或改用 `akaribot module add -e`："
            + "、".join(f"`{dist}`" for dist in plan.missing_adapters)
        )
    if log.install_failed:
        manual.append(
            "安装失败的包："
            + "、".join(f"`{dist}`" for dist, _ in log.install_failed)
            + "。重跑本命令可续装，或逐个执行 `akaribot module add`。"
        )
    if log.credential_files:
        manual.append(
            "缺凭据的适配器（配置里仍是占位符）："
            + "、".join(f"`config/{name}`" for name in log.credential_files)
            + "。运行 `akaribot config edit` 填写。"
        )
    if log.placeholders:
        total = sum(count for _, count in log.placeholders)
        manual.append(f"未填占位符共 {total} 项，分布在：" + "、".join(f"`{path}`" for path, _ in log.placeholders))
    if legacy.config_failures:
        manual.append(
            "以下旧配置无法解析，需人工检查并手工复制：" + "、".join(f"`{name}`" for name in legacy.config_failures)
        )
    if log.database_note:
        manual.append(log.database_note)
    if log.db_result.startswith(("失败", "跳过")):
        manual.append(f"数据库版本转换：{log.db_result}")
    if manual:
        lines += [f"- [ ] {item}" for item in manual]
    else:
        lines.append("无需人工处理。")
    lines += [
        "",
        "## 多实例",
        "",
        "迁移一律生成默认实例（实例 ID 为空，`client_name` 与旧项目相同），因此 `target_id` 前缀不变，",
        "全部场景数据原样可用，无需改写数据库。如需第二个账号，用",
        "`akaribot adapter instance add <平台> <实例 ID>` 新建实例后再填其凭据。",
        "",
    ]
    return "\n".join(lines)


def _print_plan(legacy: LegacyProject, target: Path, plan: MigrationPlan) -> None:
    """打印迁移计划，供执行前确认。"""
    table = Table(title="迁移计划", show_header=False, padding=(0, 2))
    table.add_row("旧项目", str(legacy.root))
    table.add_row("新实例", str(target))
    table.add_row("适配器", "、".join(plan.adapters) or "无")
    table.add_row("模块", "、".join(plan.module_dists) or "无")
    table.add_row("无法映射", "、".join(plan.unmapped) or "无")
    console.print(table)


@app.command("legacy")
def legacy(
    project: Annotated[Path, typer.Argument(help="旧项目根目录：须含 bot.py、core/、modules/、config/config.toml")],
    instance: Annotated[
        Path | None,
        typer.Option("--instance", "-I", help="新实例根目录；缺省为旧项目同级的 <旧项目名>-instance"),
    ] = None,
    workspace_root: Annotated[
        Path | None,
        typer.Option(
            "--workspace-root", "--dev", help="monorepo 工作区根：从本地源码安装，并读其中的 registry.json 做映射"
        ),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="只输出迁移报告，不写任何文件")] = False,
    skip_install: Annotated[bool, typer.Option("--skip-install", help="不安装 core、适配器与模块，只搬文件")] = False,
    no_venv: Annotated[bool, typer.Option("--no-venv", help="不托管 venv，装到当前环境")] = False,
    force: Annotated[bool, typer.Option("--force", help="覆盖目标已存在的同名文件，并允许写入非空目录")] = False,
    offline: Annotated[bool, typer.Option("--offline", help="registry 只用本地缓存，不联网")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")] = False,
) -> None:
    """把旧版项目迁移为新实例：搬配置与数据、装映射到的适配器与模块、转换数据库版本。

    旧目录只读；迁移可重复执行，已完成的步骤不会重复施加。报告写到新实例根的 migration-report.md。
    """
    root = project.expanduser().resolve()
    step(1, 6, "校验旧项目")
    try:
        legacy_project = _inspect(root)
    except CliError as exc:
        fail(str(exc))
    ok(
        f"旧项目 {root}：配置 {len(legacy_project.config_files)} 个、数据库 {len(legacy_project.database_files)} 个、"
        f"模块目录 {len(legacy_project.module_dirs)} 个、启用模块记录 {len(legacy_project.enabled_modules)} 条"
    )
    for failure in legacy_project.config_failures:
        warn(f"旧配置无法解析：{failure}")

    target = _target_root(root, instance)
    if target == root or target.is_relative_to(root):
        fail(f"新实例根不能位于旧项目目录内：{target}。迁移期间旧项目只读。")
    if workspace_root is not None:
        workspace_root = workspace_root.expanduser().resolve()
        if not (workspace_root / "packages").is_dir():
            fail(f"{workspace_root} 下没有 packages 目录，不像是 monorepo 工作区根。")

    step(2, 6, "解析模块映射")
    try:
        catalog = _load_catalog(workspace_root, offline=offline)
    except CliError as exc:
        fail(str(exc))
    index = _legacy_index(catalog)
    if not index:
        fail(
            "registry 里没有任何 legacy_module_map，无法确定旧模块名到新分发包的映射。"
            "用 --workspace-root 指向含 registry.json 的工作区根，或联网后重试。"
        )
    plan = _plan_migration(legacy_project, index, catalog)
    _print_plan(legacy_project, target, plan)
    if plan.unmapped:
        warn("无法映射的模块（记入报告的人工清单）：" + "、".join(plan.unmapped))

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
        console.print(f"[dim]dry-run：将创建实例 {target}[/dim]")
    else:
        step(3, 6, "创建新实例")
        try:
            instance = _prepare_instance(
                target, legacy_project, workspace_root=workspace_root, managed=managed, force=force
            )
        except CliError as exc:
            fail(str(exc))

    step(4, 6, "复制配置与数据")
    _copy_payload(legacy_project, instance, force=force, dry_run=dry_run, log=log)
    for tally in log.tallies:
        console.print(f"  {tally.name}：复制 {len(tally.copied)}、一致 {len(tally.unchanged)}、保留 {len(tally.kept)}")

    step(5, 6, "安装适配器与模块")
    targets: list[tuple[str, str]] = [("core", "akari-bot-core")]
    targets.extend(("adapter", dist) for dist in plan.adapters)
    targets.extend(("module", dist) for dist in plan.module_dists)
    if dry_run or skip_install:
        reason = "dry-run" if dry_run else "--skip-install"
        console.print(f"[dim]{reason}：跳过 {len(targets)} 个包的安装[/dim]")
        log.install_skipped.extend(dist for _, dist in targets)
    else:
        if managed and not instance.venv_dir.exists():
            runner = engine.CommandRunner(dry_run=False, verbose=verbose)
            try:
                runner.run_checked(
                    engine.create_venv_argv(instance.venv_dir, python=str(system_python())),
                    what="创建实例 venv",
                )
            except CliError as exc:
                fail(f"{exc}。本机没有 uv 时可装好后重跑，或用 --no-venv 装到当前环境。")
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
    step(6, 6, "写出迁移报告")
    if dry_run:
        console.print(Markdown(report))
        console.print("[dim]dry-run：未写入任何文件[/dim]")
        return
    report_path = instance.root / "migration-report.md"
    report_path.write_text(report, encoding="utf-8")
    ok(f"已写出 {report_path}")
    if log.install_failed or plan.unmapped:
        console.print("下一步：查看报告的「需人工处理」小节，处理完再运行 `akaribot run`。")
    else:
        console.print(f"下一步：cd {instance.root} && akaribot run")
