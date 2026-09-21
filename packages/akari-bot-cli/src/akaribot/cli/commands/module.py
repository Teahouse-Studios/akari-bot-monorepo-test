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
from pathlib import Path
from typing import Annotated, Iterable, Sequence

import typer
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
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
    """按当前语言的顿号或逗号拼接展示用列表。"""
    return i18n.t("cli.common.list_separator").join(items)


def _load_catalog(instance: Instance, *, offline: bool, needed: bool) -> engine.RegistryCatalog | None:
    """按需加载 registry；本地路径模式不需要远端 catalog。"""
    if not needed:
        return None
    try:
        return engine.RegistryCatalog.load(instance.meta.registry_sources, offline=offline)
    except CliError as exc:
        fail(str(exc))


def _describe_installed(packages: Sequence[PackageInfo]) -> str:
    """把包列表拼成「名字 版本」的展示串。"""
    return _join_list(f"{info.display_name} {info.version}".strip() for info in packages)


def _report_placeholders(instance: Instance, snapshot: engine.ConfigSnapshot) -> int:
    """第 7 步：报告新增配置项里的 ``<Replace me>`` 占位符数量。"""
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
    """失败回滚：恢复第 4 步写入的配置，并卸载刚装上的分发包。

    第 5 步的数据库迁移不回滚：迁移是幂等且向前的，回滚风险大于收益，报告里如实告知用户表已建。
    """
    warn(i18n.t("cli.module.install.rollback_start"))
    restored = snapshot.restore(instance)
    if restored:
        paths = _join_list(str(path.relative_to(instance.root)) for path in restored[:10])
        console.print(i18n.t("cli.module.install.config_restored", paths=paths))
    try:
        what = i18n.t("cli.venv_engine.what_uninstall_dist", dist=dist)
        runner.run_checked(engine.uninstall_argv(instance.python, [dist]), what=what)
    except CliError as exc:
        warn(str(exc))
    instance.invalidate()
    warn(i18n.t("cli.module.install.rollback_migration_kept"))


def _precheck(instance: Instance, target: engine.InstallTarget, *, force: bool) -> None:
    """第 2 步：core API 兼容性与依赖对称检查。

    冲突说明以「谁要求什么、实际是什么」呈现，不把 uv 解析器的原始报错抛给用户。
    """
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
            console.print(f"[red]  × {problem}[/red]")
        related = engine.installed_api_requirements(target, installed_env)
        if related:
            items = i18n.t("cli.common.clause_separator").join(related)
            console.print(i18n.t("cli.module.precheck.installed_requirements", items=items))
        if not force:
            fail(i18n.t("cli.module.precheck.conflict"))
        warn(i18n.t("cli.module.precheck.force"))
    else:
        ok(i18n.t("cli.module.precheck.ok"))


def _resolve(
    instance: Instance, name: str | None, *, dist, version, editable, extra, kind, offline
) -> engine.InstallTarget:
    """按工作区 / registry / 显式分发名三条路径解析安装目标。"""
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


def _install(
    instance: Instance,
    target: engine.InstallTarget,
    *,
    force: bool,
    dry_run: bool,
    verbose: bool,
    upgrade: bool = False,
) -> int:
    """执行安装流水线，返回占位符数量。"""
    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    step(1, 7, i18n.t("cli.module.install.step_resolve", dist=target.dist, source=target.source))
    console.print(i18n.t("cli.module.install.specs_line", specs=" ".join(target.specs)))
    step(2, 7, i18n.t("cli.module.install.step_precheck"))
    if dry_run:
        console.print(i18n.t("cli.module.dry_run_precheck"))
    else:
        _precheck(instance, target, force=force)

    step(3, 7, i18n.t("cli.module.install.step_install", python=instance.python))
    try:
        # 同上：what 由 venv.py 拼接「完成/失败」，保持原文。
        runner.run_checked(
            engine.install_argv(instance.python, target.specs, upgrade=upgrade),
            what=i18n.t("cli.venv_engine.what_install_dist", dist=target.dist),
        )
    except CliError as exc:
        fail(str(exc))
    if dry_run:
        console.print(i18n.t("cli.module.dry_run_skip_rest"))
        return 0
    instance.invalidate()

    snapshot = engine.ConfigSnapshot.take(instance)
    step(4, 7, i18n.t("cli.module.install.step_config_sync"))
    try:
        engine.config_sync(instance, target.dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, target.dist, snapshot, runner)
        fail(i18n.t("cli.module.install.config_sync_failed", dist=target.dist))

    step(5, 7, i18n.t("cli.module.install.step_db_upgrade"))
    try:
        engine.db_upgrade(instance, target.dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, target.dist, snapshot, runner)
        fail(i18n.t("cli.module.install.db_upgrade_failed", dist=target.dist))

    step(6, 7, i18n.t("cli.module.install.step_notify"))
    notify = instance.notify_package_change("install", target.dist)
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
                "provides_modules": list(info.provides_modules),
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
    table.add_column(i18n.t("cli.module.list.column_source"))
    for info in selected:
        table.add_row(
            info.kind,
            info.display_name,
            info.version,
            info.dist,
            _join_list(info.provides_modules) or "-",
            i18n.t("cli.module.list.source_editable") if info.editable else i18n.t("cli.module.list.source_dist"),
        )
    console.print(table)


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
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.module.add.option_force"))] = False,
    offline: OfflineOption = False,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    instance: InstancePathOption = None,
) -> None:
    """安装模块或适配器：解析 → 预检 → 安装 → 补配置 → 迁移 → 热装载 → 报告。"""
    target_instance = require_instance(instance)
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
    try:
        current = target_instance.find_package(target.dist)
    except CliError as exc:
        fail(str(exc))
    if current is not None and not force:
        fail(
            i18n.t(
                "cli.module.add.already_installed",
                dist=current.dist,
                version=current.version,
                name=current.display_name,
            )
        )
    if current is not None:
        warn(i18n.t("cli.module.add.force_reinstall", dist=current.dist, version=current.version))
    _install(target_instance, target, force=force, dry_run=dry_run, verbose=verbose)
    if not dry_run:
        console.print(i18n.t("cli.module.add.next_steps"))


def _cascade_order(instance: Instance, root: PackageInfo) -> list[PackageInfo]:
    """按「依赖者先、被依赖者后」的顺序展开连带卸载清单。"""
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


def _purge(instance: Instance, packages: Sequence[PackageInfo], *, yes: bool, dry_run: bool) -> None:
    """删除这些包拥有的数据表与配置文件（``--purge-data``）。"""
    tables = sorted({table for package in packages for table in package.owned_tables})
    files: list[Path] = []
    for package in packages:
        names = list(package.provides_modules) or ([package.name] if package.name else [])
        subdir = "adapters" if package.kind == "adapter" else "modules"
        for module_name in names:
            candidate = instance.config_dir / subdir / f"{module_name}.toml"
            if candidate.exists():
                files.append(candidate)
    tables_text = _join_list(tables) if tables else i18n.t("cli.module.purge.none_tables")
    console.print(i18n.t("cli.module.purge.tables", tables=tables_text))
    if files:
        files_text = _join_list(str(path.relative_to(instance.root)) for path in files)
    else:
        files_text = i18n.t("cli.module.purge.none")
    console.print(i18n.t("cli.module.purge.files", files=files_text))
    if dry_run:
        return
    if not yes:
        typer.confirm(i18n.t("cli.module.purge.confirm"), abort=True)
    for package in packages:
        if package.owned_tables:
            engine.db_purge(instance, package.dist)
    for path in files:
        path.unlink()
    if files:
        ok(i18n.t("cli.module.purge.removed_files", count=len(files)))


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
    for item in order:
        notify = target.notify_package_change("remove", item.dist) if not dry_run else None
        if notify is not None:
            console.print(i18n.t("cli.module.remove.notify_line", dist=item.dist, detail=notify.detail))
    try:
        # 同上：what 由 venv.py 拼接「完成/失败」，保持原文。
        what = i18n.t("cli.venv_engine.what_uninstall_packages")
        runner.run_checked(engine.uninstall_argv(target.python, [item.dist for item in order]), what=what)
    except CliError as exc:
        fail(str(exc))
    target.invalidate()
    if purge_data:
        _purge(target, order, yes=yes, dry_run=dry_run)
    else:
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
    """整理更新结果的 JSON 载荷。

    ``updated`` / ``failed`` / ``skipped`` 保持纯名字列表以兼容既有消费者，明细另置
    ``*_details``；``reload_pending`` 与 ``restart_required`` 供机器人内的 ``~update``
    判断要不要提示 ``~restart``。

    :param updated: 更新成功的分发名。
    :param plans: 本次计划更新的目标。
    :param failed: 分发名与失败原因的二元组。
    :param skipped: 分发名、跳过原因、人类可读跳过文案的三元组；前两项进 JSON 契约，末项只供打印。
    :param notified: 分发名、通知详情、是否送达的三元组。
    :param dry_run: 是否为演练模式。
    :return: JSON 可序列化的载荷。
    """
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
    """执行更新主体，返回退出码与 JSON 载荷。

    ``--json`` 的 stdout 改道由调用方完成，本函数照常把人类可读输出写到当前 stdout；
    ``json_mode`` 只影响整体失败时报错还是回传载荷。

    :return: 二元组——退出码（1 表示有包失败）；结果载荷。
    """
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
        console.print(f"[dim]$ {' '.join(argv)}[/dim]")
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
    for plan in plans:
        try:
            engine.config_sync(target_instance, plan.dist)
            engine.db_upgrade(target_instance, plan.dist)
        except CliError as exc:
            failed.append((plan.dist, str(exc)))
            warn(str(exc))
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
