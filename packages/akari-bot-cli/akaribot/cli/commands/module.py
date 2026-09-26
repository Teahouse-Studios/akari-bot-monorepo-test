"""模块安装与全局装载。

安装流水线的七步顺序有硬约束（tasks T5.2）：解析 → 兼容性预检 → uv 安装 →
config sync → db upgrade → 热装载 RPC → 报告占位符。第 4 步必须由 CLI 子进程完成，
因为机器人与 server 一律以只读配置运行，写配置会被 ``CFGManager._ensure_writable()`` 拒绝。

``load`` / ``unload`` 是另一条路径：它们不碰分发包，只切换 ``module_status.load``，且必须由
运行中的实例执行，故经 ``akari-bot.core.entrypoints.modules`` 子进程转成 JobQueue RPC。
"""

from __future__ import annotations

import contextlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any, Iterable, Sequence

import typer
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from rich.markup import escape
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import (
    CliError,
    Instance,
    InstancePathOption,
    PackageInfo,
    console,
    err_console,
    explain_process_failure,
    fail,
    ok,
    require_instance,
    split_names,
    step,
    warn,
)

app = typer.Typer(help=i18n.t("cli.module.help"))

OfflineOption = Annotated[bool, typer.Option("--offline", help=i18n.t("cli.module.option_offline"))]
DryRunOption = Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.module.option_dry_run"))]
VerboseOption = Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.module.option_verbose"))]
YesOption = Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))]


def _join_list(items: Iterable[str]) -> str:
    return i18n.t("cli.common.list_separator").join(items)


def _load_catalog(
    instance: Instance, *, offline: bool, needed: bool, ttl: float | None = None
) -> engine.RegistryCatalog | None:
    if not needed:
        return None
    kwargs = {} if ttl is None else {"ttl": ttl}
    try:
        return engine.RegistryCatalog.load(instance.meta.registry_sources, offline=offline, **kwargs)
    except CliError as exc:
        fail(str(exc))


def _describe_installed(packages: Sequence[PackageInfo]) -> str:
    return _join_list(f"{info.display_name} {info.version}".strip() for info in packages)


def _report_placeholders(instance: Instance, snapshot: engine.ConfigSnapshot) -> int:
    changed = snapshot.changed_paths(instance)
    if changed:
        paths = _join_list(str(path.relative_to(instance.root)) for path in changed[:10])
        console.print(i18n.t("cli.module.install.config_changed", paths=paths))
    count = engine.count_placeholders(changed)
    if count:
        console.print(i18n.t("cli.module.install.placeholders_left", count=count))
    else:
        ok(i18n.t("cli.module.install.no_placeholders"))
    return count


def _rollback(instance: Instance, dist: str, snapshot: engine.ConfigSnapshot, runner: engine.CommandRunner) -> None:
    # 第 5 步的数据库迁移不回滚：迁移是幂等且向前的，回滚风险大于收益，报告里如实告知用户表已建。
    warn(i18n.t("cli.module.install.rollback_start"))
    restored = snapshot.restore(instance)
    if restored:
        paths = _join_list(str(path.relative_to(instance.root)) for path in restored[:10])
        console.print(i18n.t("cli.module.install.config_restored", paths=paths))
    try:
        what = i18n.t("cli.venv_engine.what_uninstall_dist", dist=dist)
        runner.run_checked(engine.uninstall_argv(instance.python, [dist]), what=what, stream=True)
    except CliError as exc:
        warn(str(exc))
    instance.invalidate()
    warn(i18n.t("cli.module.install.rollback_migration_kept"))


def _precheck(instance: Instance, target: engine.InstallTarget, *, force: bool) -> None:
    # 冲突说明以「谁要求什么、实际是什么」呈现，不把 uv 解析器的原始报错抛给用户。
    extra_names: list[str] = []
    for text in target.dependencies:
        try:
            extra_names.append(Requirement(text).name)
        except InvalidRequirement:
            continue
    try:
        installed_env = engine.probe_environment(instance.python, names=extra_names)
    except CliError as exc:
        fail(str(exc))

    problems: list[str] = []
    api_version = instance.api_version()
    if api_version is None:
        api_version = engine.probe_api_version(instance.python)
    if target.requires_core_api and api_version is not None:
        try:
            specifier = SpecifierSet(target.requires_core_api)
        except InvalidSpecifier:
            warn(i18n.t("cli.module.precheck.unparsable_api", dist=target.dist, spec=target.requires_core_api))
        else:
            if not specifier.contains(str(api_version)):
                problems.append(
                    i18n.t(
                        "cli.module.precheck.api_mismatch",
                        dist=target.dist,
                        spec=target.requires_core_api,
                        current=api_version,
                    )
                )
    elif target.requires_core_api and api_version is None:
        warn(i18n.t("cli.module.precheck.api_unknown"))

    problems.extend(engine.dependency_conflicts(target, installed_env))
    if problems:
        for problem in problems:
            console.print(f"[red]  × {escape(str(problem))}[/red]")
        related = engine.installed_api_requirements(target, installed_env)
        if related:
            items = i18n.t("cli.common.clause_separator").join(related)
            console.print(i18n.t("cli.module.precheck.installed_requirements", items=items))
        if not force:
            fail(i18n.t("cli.module.precheck.conflict"))
        warn(i18n.t("cli.module.precheck.force"))
    else:
        ok(i18n.t("cli.module.precheck.ok"))


def _resolve_git(
    name: str | None,
    *,
    dist: str | None,
    version: str | None,
    editable: Path | None,
    git: str,
    ref: str | None,
    subdir: str | None,
) -> engine.InstallTarget:
    # git 来源在装完之前拿不到 manifest，因此除名字以外的字段留空，由 :func:`_install` 在安装后补齐。
    if editable is not None:
        raise CliError(i18n.t("cli.module.git.editable_conflict"))
    if version:
        raise CliError(i18n.t("cli.module.git.version_conflict"))
    dist_name = (dist or name or "").strip()
    spec = engine.git_spec(git, ref=ref or "", subdir=subdir or "", dist=dist_name)
    return engine.InstallTarget(dist=dist_name, specs=(spec,), source="git")


def _resolve(
    instance: Instance, name: str | None, *, dist, version, editable, extra, kind, offline
) -> engine.InstallTarget:
    workspace_root = instance.workspace_root
    needs_catalog = dist is None and editable is None and workspace_root is None
    catalog = _load_catalog(instance, offline=offline, needed=needs_catalog)
    try:
        return engine.resolve_target(
            name,
            workspace_root=workspace_root,
            catalog=catalog,
            dist=dist,
            version=version,
            editable_path=editable,
            extra=split_names(extra),
            kind=kind,
        )
    except CliError as exc:
        fail(str(exc))


def _refuse_if_installed(instance: Instance, dist: str, *, force: bool) -> None:
    try:
        current = instance.find_package(dist)
    except CliError as exc:
        fail(str(exc))
    if current is None:
        return
    if not force:
        fail(
            i18n.t(
                "cli.module.add.already_installed",
                dist=current.dist,
                version=current.version,
                name=current.display_name,
            )
        )
    warn(i18n.t("cli.module.add.force_reinstall", dist=current.dist, version=current.version))


def _installed_dists(instance: Instance) -> set[str]:
    # git 直引用不预先知道分发名，只能靠安装前后的差集认领新装的那个，故安装前先记一份。
    try:
        return {engine.canonical(dist) for dist in instance.installed(refresh=True)}
    except CliError as exc:
        fail(str(exc))


def _dist_from_git_install(instance: Instance, before: set[str], *, requested: str) -> str:
    try:
        packages = instance.installed(refresh=True)
    except CliError as exc:
        fail(str(exc))
    added = sorted(dist for dist in packages if engine.canonical(dist) not in before)
    if requested:
        for dist in packages.values():
            if engine.canonical(dist.dist) == engine.canonical(requested):
                return dist.dist
    if len(added) == 1:
        return packages[added[0]].dist
    if not added:
        raise CliError(i18n.t("cli.module.git.nothing_added", dist=requested or "-"))
    raise CliError(i18n.t("cli.module.git.ambiguous", names=_join_list(added)))


def _check_git_api(instance: Instance, dist: str, *, runner: engine.CommandRunner) -> None:
    # 预检阶段拿不到 manifest，若把这一步也省掉，不兼容的包会直接装进实例并在运行时才炸。
    package = instance.find_package(dist)
    if package is None or not package.requires_core_api:
        return
    api_version = instance.api_version() or engine.probe_api_version(instance.python)
    if api_version is None:
        warn(i18n.t("cli.module.precheck.api_unknown"))
        return
    try:
        specifier = SpecifierSet(package.requires_core_api)
    except InvalidSpecifier:
        warn(i18n.t("cli.module.precheck.unparsable_api", dist=package.dist, spec=package.requires_core_api))
        return
    if api_version in specifier:
        ok(i18n.t("cli.module.precheck.ok"))
        return
    console.print(
        f"[red]  × "
        f"{escape(i18n.t('cli.module.precheck.api_mismatch', dist=package.dist, spec=package.requires_core_api, current=api_version))}"
        f"[/red]"
    )
    try:
        runner.run_checked(
            engine.uninstall_argv(instance.python, [package.dist]),
            what=i18n.t("cli.venv_engine.what_uninstall_dist", dist=package.dist),
            stream=True,
        )
    except CliError as exc:
        warn(str(exc))
    instance.invalidate()
    fail(i18n.t("cli.module.git.rolled_back", dist=package.dist))


def _install(
    instance: Instance,
    target: engine.InstallTarget,
    *,
    force: bool,
    dry_run: bool,
    verbose: bool,
    upgrade: bool = False,
) -> int:
    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    # git 直引用可能没有名字，此时用 spec 自身作为展示对象，免得出现「解析 （来源：git）」。
    step(1, 7, i18n.t("cli.module.install.step_resolve", dist=target.dist or target.specs[0], source=target.source))
    console.print(i18n.t("cli.module.install.specs_line", specs=" ".join(target.specs)))
    from_git = target.source == "git"
    step(2, 7, i18n.t("cli.module.install.step_precheck"))
    if dry_run:
        console.print(i18n.t("cli.module.dry_run_precheck"))
    elif from_git:
        # git 直引用要装完才解析出分发名与 manifest，此时无从预检，改为装完后校验 core API。
        console.print(i18n.t("cli.module.install.precheck_git"))
    else:
        _precheck(instance, target, force=force)

    step(3, 7, i18n.t("cli.module.install.step_install", python=instance.python))
    before = _installed_dists(instance) if from_git and not dry_run else None
    try:
        # 同上：what 由 venv.py 拼接「完成/失败」，保持原文。
        runner.run_checked(
            engine.install_argv(instance.python, target.specs, upgrade=upgrade),
            what=i18n.t("cli.venv_engine.what_install_dist", dist=target.dist or target.specs[0]),
            stream=True,
        )
    except CliError as exc:
        fail(str(exc))
    if dry_run:
        console.print(i18n.t("cli.module.dry_run_skip_rest"))
        return 0
    instance.invalidate()
    dist = target.dist
    if before is not None:
        try:
            dist = _dist_from_git_install(instance, before, requested=target.dist)
        except CliError as exc:
            fail(str(exc))
        console.print(i18n.t("cli.module.git.resolved", dist=dist))
        if not force:
            _check_git_api(instance, dist, runner=runner)

    snapshot = engine.ConfigSnapshot.take(instance)
    step(4, 7, i18n.t("cli.module.install.step_config_sync"))
    try:
        engine.config_sync(instance, dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, dist, snapshot, runner)
        fail(i18n.t("cli.module.install.config_sync_failed", dist=dist))

    step(5, 7, i18n.t("cli.module.install.step_db_upgrade"))
    try:
        engine.db_upgrade(instance, dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, dist, snapshot, runner)
        fail(i18n.t("cli.module.install.db_upgrade_failed", dist=dist))

    step(6, 7, i18n.t("cli.module.install.step_notify"))
    notify = instance.notify_package_change("install", dist)
    if notify.attempted and not notify.delivered:
        warn(notify.detail)
        warn(i18n.t("cli.module.install.restart_needed"))
    else:
        console.print("  " + notify.detail)

    step(7, 7, i18n.t("cli.module.install.step_report"))
    return _report_placeholders(instance, snapshot)


@app.command("list", help=i18n.t("cli.module.list.help"))
def list_packages(
    instance: InstancePathOption = None,
    kind: Annotated[str | None, typer.Option("--kind", help=i18n.t("cli.module.list.option_kind"))] = None,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """列出已安装的模块与适配器。"""
    target = require_instance(instance)
    try:
        packages = target.installed()
    except CliError as exc:
        fail(str(exc))
    selected = [info for info in packages.values() if kind is None or info.kind == kind]
    selected.sort(key=lambda info: (info.kind, info.dist))
    if as_json:
        payload = [
            {
                "dist": info.dist,
                "name": info.name,
                "kind": info.kind,
                "version": info.version,
                "editable": info.editable,
                "requires_core_api": info.requires_core_api,
                "summary": info.summary,
                "developers": list(info.developers),
                "provides_modules": list(info.provides_modules),
                # manifest 的其余字段：TUI 详情与 --purge-data 都要看，缺了只能显示「未声明」。
                "owned_tables": list(info.owned_tables),
                "config_table": info.config_table,
                "dependencies": [
                    f"{dep.dist}{dep.specifier}" if dep.specifier else dep.dist for dep in info.dependencies
                ],
            }
            for info in selected
        ]
        console.print_json(json.dumps(payload, ensure_ascii=False))
        return
    table = Table(title=i18n.t("cli.module.list.table_title", count=len(selected)))
    table.add_column(i18n.t("cli.module.list.column_kind"))
    table.add_column(i18n.t("cli.module.list.column_name"))
    table.add_column(i18n.t("cli.module.list.column_version"))
    table.add_column(i18n.t("cli.module.list.column_dist"))
    table.add_column(i18n.t("cli.module.list.column_provides"))
    table.add_column(i18n.t("cli.module.list.column_developers"))
    table.add_column(i18n.t("cli.module.list.column_source"))
    for info in selected:
        table.add_row(
            info.kind,
            info.display_name,
            info.version,
            info.dist,
            _join_list(info.provides_modules) or "-",
            _join_list(info.developers) or "-",
            i18n.t("cli.module.list.source_editable") if info.editable else i18n.t("cli.module.list.source_dist"),
        )
    console.print(table)


@dataclass(frozen=True)
class AvailablePackage:
    """一条「可安装」记录，工作区与 registry 两个来源共用同一形状。

    :param kind: ``module`` 或 ``adapter``。
    :param name: 短名；工作区来源取 entry point 名。
    :param dist: 分发名。
    :param version: 可安装的版本。
    :param detail: 补充信息：registry 来源是一句话简介，工作区来源是包路径。
    :param provides: 提供的模块名（适配器为 entry point 名）。
    :param developers: 模块作者，取自包的 ``pyproject.toml``。
    """

    kind: str
    name: str
    dist: str
    version: str
    detail: str
    provides: tuple[str, ...]
    developers: tuple[str, ...] = ()

    def search_text(self) -> str:
        """拼出可搜索文本。"""
        return " ".join((self.name, self.dist, self.detail, *self.provides)).casefold()


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _workspace_available(root: Path) -> list[AvailablePackage]:
    # 工作区模式下安装一律取本地源码（``resolve_target`` 的优先级如此），此时 registry 并不是
    # 「能装什么」的答案来源；把本地成员列出来才是。
    index = engine.workspace_index(root)
    found: list[AvailablePackage] = []
    for package in index.values():
        if engine.canonical(package.dist) == engine.CORE_DIST:
            continue
        if package.adapter_names:
            kind, names = "adapter", package.adapter_names
        elif package.module_names:
            kind, names = "module", package.module_names
        else:
            continue
        found.append(
            AvailablePackage(
                kind=kind,
                name=names[0],
                dist=package.dist,
                version=package.version,
                detail=_relative_path(package.path, root),
                provides=package.provides_modules or package.module_names,
                developers=engine.package_authors(package.path),
            )
        )
    return found


def _registry_available(catalog: engine.RegistryCatalog) -> list[AvailablePackage]:
    return [
        AvailablePackage(
            kind=entry.kind,
            name=entry.name,
            dist=entry.dist,
            version=entry.latest,
            detail=_summary_text(entry),
            provides=entry.provides_modules,
            developers=entry.developers,
        )
        for entry in catalog.entries.values()
        if entry.kind != "core"
    ]


def _summary_text(entry: engine.RegistryEntry) -> str:
    preferred = i18n.current_locale()
    if text := entry.summary.get(preferred):
        return text
    return next((text for text in entry.summary.values() if text), "")


@app.command("available", help=i18n.t("cli.module.available.help"))
def available(
    instance: InstancePathOption = None,
    kind: Annotated[str | None, typer.Option("--kind", help=i18n.t("cli.module.available.option_kind"))] = None,
    search: Annotated[str | None, typer.Option("--search", help=i18n.t("cli.module.available.option_search"))] = None,
    refresh: Annotated[bool, typer.Option("--refresh", help=i18n.t("cli.module.available.option_refresh"))] = False,
    offline: OfflineOption = False,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """列出可安装的模块与适配器，并标出哪些已装。

    ``add`` 只认名字，而名字从哪来看不到；本命令把可安装集合连同「是否已装」一并列出。
    工作区模式下集合来自本地工作区成员，否则来自实例配置的 registry 来源。
    """
    target = require_instance(instance)
    workspace_root = Path(target.meta.workspace_root) if target.meta.workspace_root else None
    workspace_mode = workspace_root is not None and (workspace_root / "packages").is_dir()
    catalog: engine.RegistryCatalog | None = None
    if workspace_mode:
        candidates = _workspace_available(workspace_root)
        source = i18n.t("cli.module.available.source_workspace", root=workspace_root)
    else:
        catalog = _load_catalog(target, offline=offline, needed=True, ttl=0.0 if refresh and not offline else None)
        if catalog is None:
            return
        candidates = _registry_available(catalog)
        source = catalog.source or "-"
    try:
        installed = {engine.canonical(info.dist) for info in target.installed().values()}
    except CliError as exc:
        fail(str(exc))
    needle = (search or "").strip().casefold()
    selected = [
        item
        for item in candidates
        if (kind is None or item.kind == kind) and (not needle or needle in item.search_text())
    ]
    selected.sort(key=lambda item: (item.kind, item.dist))
    if as_json:
        payload = [
            {
                "dist": item.dist,
                "name": item.name,
                "kind": item.kind,
                # 键名与 `module list --json` 对齐：TUI 的 normalize_records 按 version 取值。
                "version": item.version,
                "installed": engine.canonical(item.dist) in installed,
                "provides_modules": list(item.provides),
                "developers": list(item.developers),
                "summary": "" if workspace_mode else item.detail,
                # 工作区来源的 detail 是包路径；放进 origin，消费方（TUI、脚本）据此定位源码。
                "origin": item.detail if workspace_mode else "",
            }
            for item in selected
        ]
        console.print_json(json.dumps(payload, ensure_ascii=False))
        return
    console.print(i18n.t("cli.module.available.source_line", source=source))
    if not selected:
        console.print(i18n.t("cli.module.available.none", search=search or ""))
        console.print(i18n.t("cli.module.available.none_hint"))
        return
    table = Table(title=i18n.t("cli.module.available.table_title", count=len(selected)))
    table.add_column(i18n.t("cli.module.available.column_kind"))
    table.add_column(i18n.t("cli.module.available.column_name"))
    table.add_column(i18n.t("cli.module.available.column_dist"))
    table.add_column(i18n.t("cli.module.available.column_latest"))
    table.add_column(i18n.t("cli.module.available.column_state"))
    table.add_column(i18n.t("cli.module.available.column_developers"))
    table.add_column(
        i18n.t("cli.module.available.column_path" if workspace_mode else "cli.module.available.column_summary")
    )
    for item in selected:
        table.add_row(
            item.kind,
            item.name,
            item.dist,
            item.version or "-",
            i18n.t("cli.module.available.state_installed")
            if engine.canonical(item.dist) in installed
            else i18n.t("cli.module.available.state_available"),
            _join_list(item.developers) or "-",
            item.detail or "-",
        )
    console.print(table)
    console.print(i18n.t("cli.module.available.install_hint"))
    if catalog is not None and catalog.from_cache:
        console.print(i18n.t("cli.module.available.cached_hint"))


@app.command("add", help=i18n.t("cli.module.add.help"))
def add(
    name: Annotated[str | None, typer.Argument(help=i18n.t("cli.module.add.arg_name"))] = None,
    dist: Annotated[str | None, typer.Option("--dist", help=i18n.t("cli.module.add.option_dist"))] = None,
    version: Annotated[str | None, typer.Option("--version", help=i18n.t("cli.module.add.option_version"))] = None,
    editable: Annotated[
        Path | None, typer.Option("-e", "--editable", help=i18n.t("cli.module.add.option_editable"))
    ] = None,
    extra: Annotated[list[str] | None, typer.Option("--extra", help=i18n.t("cli.module.add.option_extra"))] = None,
    kind: Annotated[str | None, typer.Option("--kind", help=i18n.t("cli.module.add.option_kind"))] = None,
    git: Annotated[str | None, typer.Option("--git", help=i18n.t("cli.module.add.option_git"))] = None,
    ref: Annotated[str | None, typer.Option("--ref", help=i18n.t("cli.module.add.option_ref"))] = None,
    subdir: Annotated[str | None, typer.Option("--subdir", help=i18n.t("cli.module.add.option_subdir"))] = None,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.module.add.option_force"))] = False,
    offline: OfflineOption = False,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    instance: InstancePathOption = None,
) -> None:
    """安装模块或适配器：解析 → 预检 → 安装 → 补配置 → 迁移 → 热装载 → 报告。"""
    target_instance = require_instance(instance)
    if git is not None:
        try:
            target = _resolve_git(name, dist=dist, version=version, editable=editable, git=git, ref=ref, subdir=subdir)
        except CliError as exc:
            fail(str(exc))
        # 给了名字才可能提前查重；不给名字时无从查起，只能装完再由差集认领。
        if target.dist:
            _refuse_if_installed(target_instance, target.dist, force=force)
        _install(target_instance, target, force=force, dry_run=dry_run, verbose=verbose)
        if not dry_run:
            console.print(i18n.t("cli.module.add.next_steps"))
        return
    if ref is not None or subdir is not None:
        fail(i18n.t("cli.module.add.ref_without_git"))
    target = _resolve(
        target_instance,
        name,
        dist=dist,
        version=version,
        editable=editable,
        extra=extra,
        kind=kind,
        offline=offline,
    )
    _refuse_if_installed(target_instance, target.dist, force=force)
    _install(target_instance, target, force=force, dry_run=dry_run, verbose=verbose)
    if not dry_run:
        console.print(i18n.t("cli.module.add.next_steps"))


def _cascade_order(instance: Instance, root: PackageInfo) -> list[PackageInfo]:
    ordered: list[PackageInfo] = []
    seen: set[str] = set()

    def visit(package: PackageInfo) -> None:
        key = package.dist.lower().replace("_", "-")
        if key in seen:
            return
        seen.add(key)
        for dependent in instance.dependents_of(package.dist):
            visit(dependent)
        ordered.append(package)

    visit(root)
    return ordered


def _config_files(instance: Instance, package: PackageInfo) -> tuple[list[Path], list[Path]]:
    # 基表取 ``manifest.config_table`` 的扁平路径：``CFGManager.load()`` 只扫描 ``config/*.toml``，
    # 按 ``provides_modules`` 拼出的路径不在扫描范围内。适配器实例表名由基表派生，只能按前缀匹配。
    if not package.config_table:
        return [], []
    base = instance.config_dir / f"{package.config_table}.toml"
    files = [base] if base.is_file() else []
    if package.kind != "adapter":
        return files, []
    prefix = f"{package.config_table}-"
    instances = sorted(
        path for path in instance.config_dir.glob("*.toml") if path.name.startswith(prefix) and path != base
    )
    return files, instances


def _purge(
    instance: Instance,
    packages: Sequence[PackageInfo],
    *,
    yes: bool,
    dry_run: bool,
    purge_instances: bool,
) -> bool:
    # 必须在 uv uninstall **之前**调用：清单随分发一起被删，卸载后再也解析不出 ``owned_tables``
    # 与 ``config_table``，那时连该删什么都不知道。任一步失败即返回 ``False``，由命令层决定中止
    # 卸载还是按 ``--force`` 接受残留——静默返回成功会让用户以为数据已清干净。
    tables = sorted({table for package in packages for table in package.owned_tables})
    base_files: list[Path] = []
    instance_files: list[Path] = []
    for package in packages:
        base, instances = _config_files(instance, package)
        base_files.extend(base)
        if purge_instances:
            instance_files.extend(instances)
        elif instances:
            console.print(i18n.t("cli.module.purge.instance_kept", count=len(instances), dist=package.dist))
    tables_text = _join_list(tables) if tables else i18n.t("cli.module.purge.none_tables")
    console.print(i18n.t("cli.module.purge.tables", tables=tables_text))
    files = base_files + instance_files
    if files:
        files_text = _join_list(str(path.relative_to(instance.root)) for path in files)
    else:
        files_text = i18n.t("cli.module.purge.none")
    console.print(i18n.t("cli.module.purge.files", files=files_text))
    if dry_run:
        return True
    if not yes:
        typer.confirm(i18n.t("cli.module.purge.confirm"), abort=True)

    failures: list[str] = []
    purged = 0
    for package in packages:
        if not package.owned_tables:
            continue
        if engine.db_purge(instance, package.dist):
            purged += 1
        else:
            failures.append(i18n.t("cli.module.purge.failed_tables", dist=package.dist))
    removed = 0
    for path in files:
        try:
            path.unlink()
        except OSError as exc:
            failures.append(i18n.t("cli.module.purge.failed_file", path=path.name, error=exc))
        else:
            removed += 1
    if removed:
        ok(i18n.t("cli.module.purge.removed_files", count=removed))
    if failures:
        warn(i18n.t("cli.module.purge.partial", reasons=_join_list(failures)))
        return False
    if purged:
        ok(i18n.t("cli.module.purge.done", count=purged))
    return True


@app.command("remove", help=i18n.t("cli.module.remove.help"))
def remove(
    name: Annotated[str, typer.Argument(help=i18n.t("cli.module.remove.arg_name"))],
    cascade: Annotated[bool, typer.Option("--cascade", help=i18n.t("cli.module.remove.option_cascade"))] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.module.remove.option_force"))] = False,
    purge_data: Annotated[
        bool, typer.Option("--purge-data", help=i18n.t("cli.module.remove.option_purge_data"))
    ] = False,
    yes: YesOption = False,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    instance: InstancePathOption = None,
) -> None:
    """卸载模块或适配器；默认保留配置与数据，并做反向依赖检查。"""
    target = require_instance(instance)
    try:
        package = target.find_package(name)
    except CliError as exc:
        fail(str(exc))
    if package is None:
        fail(i18n.t("cli.module.not_installed", name=name))
    dependents = target.dependents_of(package.dist)
    if dependents and not (cascade or force):
        fail(
            i18n.t(
                "cli.module.remove.dependents",
                name=package.display_name,
                packages=_describe_installed(dependents),
            )
        )
    order = _cascade_order(target, package) if cascade else [package]
    if cascade and dependents:
        console.print(i18n.t("cli.module.remove.cascade_list", packages=_describe_installed(order)))
        if not dry_run and not yes:
            typer.confirm(i18n.t("cli.module.remove.cascade_confirm", count=len(order)), abort=True)
    if force and dependents:
        warn(i18n.t("cli.module.remove.force_warning", packages=_describe_installed(dependents)))

    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    blocked: list[str] = []
    for item in order:
        if dry_run:
            continue
        notify = target.notify_package_change("remove", item.dist)
        console.print(i18n.t("cli.module.remove.notify_line", dist=item.dist, detail=notify.detail))
        # 先拆后卸：确认热拆卸失败时必须停手，否则运行中的实例会继续持有已删分发的模块与库 context。
        if notify.blocks_uninstall:
            blocked.append(i18n.t("cli.module.remove.detach_blocked", dist=item.dist, detail=notify.detail))
    if blocked:
        fail(i18n.t("cli.module.remove.detach_failed", reasons=_join_list(blocked)))
    if purge_data:
        # 先清理再卸载：清单随分发一起消失，卸载后再也解析不出 owned_tables 与 config_table。
        purge_instances = yes or dry_run
        if not purge_instances:
            instances = sum(len(_config_files(target, item)[1]) for item in order)
            if instances:
                purge_instances = typer.confirm(i18n.t("cli.module.remove.purge_instances_confirm", count=instances))
        if not _purge(target, order, yes=yes, dry_run=dry_run, purge_instances=purge_instances):
            if not force:
                fail(i18n.t("cli.module.remove.purge_failed"))
            warn(i18n.t("cli.module.remove.purge_failed_forced"))
    try:
        # 同上：what 由 venv.py 拼接「完成/失败」，保持原文。
        what = i18n.t("cli.venv_engine.what_uninstall_packages")
        runner.run_checked(engine.uninstall_argv(target.python, [item.dist for item in order]), what=what, stream=True)
    except CliError as exc:
        fail(str(exc))
    target.invalidate()
    if not purge_data:
        console.print(i18n.t("cli.module.remove.keep_data"))


def _update_payload(
    *,
    updated: Sequence[str],
    plans: Sequence[engine.InstallTarget],
    failed: Sequence[tuple[str, str]],
    skipped: Sequence[tuple[str, str, str]],
    notified: Sequence[tuple[str, str, bool]],
    dry_run: bool,
) -> dict:
    # ``updated`` / ``failed`` / ``skipped`` 保持纯名字列表以兼容既有消费者，明细另置
    # ``*_details``；``reload_pending`` 与 ``restart_required`` 供机器人内的 ``~update``
    # 判断要不要提示 ``~restart``。
    delivered = {dist: ok_ for dist, _, ok_ in notified}
    reload_pending = [dist for dist in updated if not delivered.get(dist, False)]
    return {
        "updated": list(updated),
        "failed": [dist for dist, _ in failed],
        "skipped": [dist for dist, _, _ in skipped],
        "planned": [plan.dist for plan in plans],
        "failed_details": [{"dist": dist, "reason": reason} for dist, reason in failed],
        "skipped_details": [{"dist": dist, "reason": reason} for dist, reason, _ in skipped],
        "notified": [{"dist": dist, "detail": detail, "delivered": ok_} for dist, detail, ok_ in notified],
        "reload_pending": reload_pending,
        "restart_required": bool(reload_pending),
        "dry_run": dry_run,
    }


def _perform_update(
    instance_path: Path | None,
    requested: Sequence[str],
    *,
    all_packages: bool,
    offline: bool,
    force: bool,
    assume_yes: bool,
    dry_run: bool,
    verbose: bool,
    json_mode: bool,
) -> tuple[int, dict]:
    # ``--json`` 的 stdout 改道由调用方完成，本函数照常把人类可读输出写到当前 stdout；
    # ``json_mode`` 只影响整体失败时报错还是回传载荷。
    target_instance = require_instance(instance_path)
    try:
        installed = target_instance.installed()
    except CliError as exc:
        fail(str(exc))
    if not requested and not all_packages:
        fail(i18n.t("cli.module.update.no_names"))
    selected: list[PackageInfo] = []
    for item in requested:
        found = target_instance.find_package(item)
        if found is None:
            fail(i18n.t("cli.module.not_installed", name=item))
        selected.append(found)
    if all_packages:
        selected = [info for info in installed.values() if engine.canonical(info.dist) != engine.CLI_DIST]
    selected = list({info.dist: info for info in selected}.values())

    workspace_root = target_instance.workspace_root
    catalog = _load_catalog(target_instance, offline=offline, needed=workspace_root is None)
    plans: list[engine.InstallTarget] = []
    skipped: list[tuple[str, str, str]] = []
    for info in selected:
        if workspace_root is not None:
            resolved = engine.workspace_target(workspace_root, info.dist)
            if resolved is None:
                # 三元组的第二项是 --json 载荷里的 reason，属机器可读契约，保持原文；第三项只供打印。
                skipped.append((info.dist, "工作区里没有该包", i18n.t("cli.module.update.skip_no_workspace")))
                continue
            plans.append(resolved)
            continue
        latest = catalog.latest(info.dist) if catalog else None
        if not latest:
            skipped.append((info.dist, "registry 里没有该分发", i18n.t("cli.module.update.skip_no_registry")))
            continue
        if latest == info.version and not force:
            skipped.append(
                (info.dist, f"已是最新（{latest}）", i18n.t("cli.module.update.skip_up_to_date", version=latest))
            )
            continue
        plans.append(
            engine.InstallTarget(dist=info.dist, version=latest, specs=(f"{info.dist}=={latest}",), source="registry")
        )

    if not plans:
        for dist, _, printable in skipped:
            console.print(i18n.t("cli.module.update.skip_line", dist=dist, reason=printable))
        ok(i18n.t("cli.module.update.nothing_to_do"))
        return 0, _update_payload(updated=[], plans=[], failed=[], skipped=skipped, notified=[], dry_run=dry_run)

    argv = engine.install_argv(target_instance.python, [spec for plan in plans for spec in plan.specs], upgrade=True)
    targets = _join_list(f"{plan.dist}→{plan.version or i18n.t('cli.module.update.local_source')}" for plan in plans)
    console.print(i18n.t("cli.module.update.will_update", targets=targets))
    if dry_run:
        console.print(f"[dim]$ {escape(' '.join(argv))}[/dim]")
        console.print(i18n.t("cli.module.dry_run_skip_rest"))
        return 0, _update_payload(updated=[], plans=plans, failed=[], skipped=skipped, notified=[], dry_run=True)
    if not assume_yes:
        typer.confirm(i18n.t("cli.module.update.confirm", count=len(plans)), abort=True)

    completed = engine.CommandRunner(verbose=verbose).run(argv)
    if completed.returncode != 0:
        summary = engine.summarize_uv_error(completed.stderr or completed.stdout or "")
        # failed_details[].reason 是 --json 契约的一部分，保持原文；人类可读提示另行本地化。
        failures = [(plan.dist, f"更新包失败：{summary}") for plan in plans]
        payload = _update_payload(updated=[], plans=plans, failed=failures, skipped=skipped, notified=[], dry_run=False)
        message = i18n.t("cli.module.update.failed", detail=summary)
        if not json_mode:
            fail(message)
        warn(message)
        return 1, payload
    ok(i18n.t("cli.module.update.ok"))
    target_instance.invalidate()

    failed: list[tuple[str, str]] = []
    notified: list[tuple[str, str, bool]] = []
    kinds = {engine.canonical(info.dist): info.kind for info in selected}
    for plan in plans:
        try:
            engine.config_sync(target_instance, plan.dist)
            engine.db_upgrade(target_instance, plan.dist)
        except CliError as exc:
            failed.append((plan.dist, str(exc)))
            warn(str(exc))
        if kinds.get(engine.canonical(plan.dist)) == "module":
            # 代码已在磁盘上换新，但运行中的实例仍注册着旧代际，直接热装载会被判「已注册」；
            # 先热拆卸再热装载才能换到新代码。适配器不支持整包热换，沿用重启提示。
            detach = target_instance.notify_package_change("remove", plan.dist)
            if detach.blocks_uninstall:
                warn(i18n.t("cli.module.update.detach_failed", dist=plan.dist, detail=detach.detail))
                notified.append((plan.dist, detach.detail, False))
                continue
            if detach.delivered:
                console.print(i18n.t("cli.module.update.detach_line", dist=plan.dist))
        notify = target_instance.notify_package_change("install", plan.dist)
        notified.append((plan.dist, notify.detail, notify.delivered))
        if notify.attempted and not notify.delivered:
            warn(notify.detail)
    for dist, _, printable in skipped:
        console.print(i18n.t("cli.module.update.skip_line", dist=dist, reason=printable))
    failed_names = [dist for dist, _ in failed]
    updated = [plan.dist for plan in plans if plan.dist not in failed_names]
    payload = _update_payload(
        updated=updated, plans=plans, failed=failed, skipped=skipped, notified=notified, dry_run=False
    )
    if failed:
        warn(i18n.t("cli.module.update.partial", count=len(updated)))
        return 1, payload
    suffix = i18n.t("cli.module.update.notified_suffix") if updated else ""
    ok(i18n.t("cli.module.update.done", count=len(updated)) + suffix)
    return 0, payload


@app.command("update", help=i18n.t("cli.module.update.help"))
def update(
    name: Annotated[list[str] | None, typer.Argument(help=i18n.t("cli.module.update.arg_name"))] = None,
    all_packages: Annotated[bool, typer.Option("--all", help=i18n.t("cli.module.update.option_all"))] = False,
    offline: OfflineOption = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.module.update.option_force"))] = False,
    yes: YesOption = False,
    non_interactive: Annotated[
        bool, typer.Option("--non-interactive", help=i18n.t("cli.module.update.option_non_interactive"))
    ] = False,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.module.update.option_json"))] = False,
    instance: InstancePathOption = None,
) -> None:
    """更新已安装的包；工作区模式下等价于按本地源码重装。

    ``--json`` 的契约：stdout 只出现一行结果 JSON（``updated`` / ``failed`` / ``skipped`` /
    ``failed_details`` / ``skipped_details`` / ``reload_pending`` / ``restart_required``），
    进度与警告一律走 stderr，退出码 1 表示有包未更新成功。
    """
    if as_json:
        if verbose:
            err_console.print(i18n.t("cli.module.update.verbose_ignored"))
        # 结果 JSON 之外的一切输出先改道 stderr，改道块结束后才写出唯一的那一行。
        stream = sys.stdout
        with contextlib.redirect_stdout(sys.stderr):
            code, payload = _perform_update(
                instance,
                split_names(name),
                all_packages=all_packages,
                offline=offline,
                force=force,
                assume_yes=yes or non_interactive,
                dry_run=dry_run,
                verbose=False,
                json_mode=True,
            )
        print(json.dumps(payload, ensure_ascii=False), file=stream)
        raise typer.Exit(code)
    code, _ = _perform_update(
        instance,
        split_names(name),
        all_packages=all_packages,
        offline=offline,
        force=force,
        assume_yes=yes or non_interactive,
        dry_run=dry_run,
        verbose=verbose,
        json_mode=False,
    )
    if code != 0:
        raise typer.Exit(code)


@app.command("status", help=i18n.t("cli.module.status.help"))
def module_status(
    instance_path: InstancePathOption = None,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """列出各模块的全局装载状态（``module_status.load``）。

    状态表由实例的数据库提供，实例未运行时读到的可能是上次退出前的记录，故不加运行校验；
    ``loaded`` 为 ``null`` 表示该模块尚无记录（实例未完成过一次启动）。
    """
    instance = require_instance(instance_path)
    completed = instance.run_core_capture("modules", "list", "--json", timeout=60.0)
    if completed.returncode != 0:
        fail(explain_process_failure(completed, i18n.t("cli.module.status.failed")))
    try:
        payload = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as error:
        fail(i18n.t("cli.module.status.bad_json", error=error))
    items = [item for item in payload if isinstance(item, dict)]
    note = (completed.stderr or "").strip()
    if as_json:
        console.print_json(json.dumps({"modules": items, "note": note}, ensure_ascii=False))
        return
    table = Table(title=i18n.t("cli.module.status.table_title", count=len(items)))
    table.add_column(i18n.t("cli.module.status.column_module"))
    table.add_column(i18n.t("cli.module.status.column_state"))
    table.add_column(i18n.t("cli.module.status.column_dist"))
    for item in items:
        table.add_row(
            str(item.get("name") or ""),
            _load_state_label(item.get("loaded")),
            str(item.get("installed_dist") or "-"),
        )
    console.print(table)
    if note:
        warn(note)


def _load_state_label(loaded: Any) -> str:
    if loaded is None:
        return i18n.t("cli.module.status.state_unknown")
    return i18n.t("cli.module.status.state_loaded") if loaded else i18n.t("cli.module.status.state_unloaded")


# 三级「启用」语义（附录 B）：安装看 venv、全局装载看 ModuleStatus.load、场景启用看
# target_union_info.modules。本命令只管第二级，故用 load/unload 而非场景级的 enable/disable。
@app.command("load", help=i18n.t("cli.module.load.help"))
def load_module(
    name: str,
    instance_path: InstancePathOption = None,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """全局装载模块：让它参与命令匹配（与安装、场景启用是两回事）。

    实例 ID 一旦使用请勿更改这条约束**不适用于本命令**：它只改全局装载状态，不触碰任何配置。
    """
    instance = require_instance(instance_path)
    # 实例未运行时 core 侧要等 websocket 连接超时（实测 15.6 秒）才回报，故先用锁文件短路；
    # 为真时仍走子进程，由 core 判定 Server 是否在线。
    if not instance.is_running():
        fail(i18n.t("cli.warn.instance_not_running_load"))
    code = instance.run_core("modules", "load", name)
    if as_json:
        console.print_json(json.dumps({"module": name, "action": "load", "returncode": code}, ensure_ascii=False))
    elif code == 0:
        ok(i18n.t("cli.ok.loaded", module=name))
    if code != 0:
        raise typer.Exit(code)


@app.command("unload", help=i18n.t("cli.module.unload.help"))
def unload_module(
    name: str,
    instance_path: InstancePathOption = None,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """全局卸载模块：让它退出命令匹配；代码与配置都保留。

    实例 ID 一旦使用请勿更改这条约束**不适用于本命令**：它只改全局装载状态，不触碰任何配置。
    """
    instance = require_instance(instance_path)
    if not instance.is_running():
        fail(i18n.t("cli.warn.instance_not_running_unload"))
    code = instance.run_core("modules", "unload", name)
    if as_json:
        console.print_json(json.dumps({"module": name, "action": "unload", "returncode": code}, ensure_ascii=False))
    elif code == 0:
        ok(i18n.t("cli.ok.unloaded", module=name))
    if code != 0:
        raise typer.Exit(code)
