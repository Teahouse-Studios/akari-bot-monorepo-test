"""模块安装与卸载。

安装流水线的七步顺序有硬约束（tasks T5.2）：解析 → 兼容性预检 → uv 安装 →
config sync → db upgrade → 热装载 RPC → 报告占位符。第 4 步必须由 CLI 子进程完成，
因为机器人与 server 一律以只读配置运行，写配置会被 ``CFGManager._ensure_writable()`` 拒绝。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Sequence

import typer
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from rich.table import Table

from akaribot.cli import venv as engine
from akaribot.cli.instance import (
    CliError,
    Instance,
    InstancePathOption,
    PackageInfo,
    console,
    fail,
    ok,
    require_instance,
    split_names,
    step,
    warn,
)

app = typer.Typer(help="模块安装与卸载：list / add / remove / update")

OfflineOption = Annotated[bool, typer.Option("--offline", help="registry 只用本地缓存，不联网")]
DryRunOption = Annotated[bool, typer.Option("--dry-run", help="只打印将执行的命令，不修改任何文件")]
VerboseOption = Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")]
YesOption = Annotated[bool, typer.Option("--yes", "-y", help="不询问，直接执行")]


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
    return "、".join(f"{info.display_name} {info.version}".strip() for info in packages)


def _report_placeholders(instance: Instance, snapshot: engine.ConfigSnapshot) -> int:
    """第 7 步：报告新增配置项里的 ``<Replace me>`` 占位符数量。"""
    changed = snapshot.changed_paths(instance)
    if changed:
        console.print("  配置文件变更：" + "、".join(str(path.relative_to(instance.root)) for path in changed[:10]))
    count = engine.count_placeholders(changed)
    if count:
        console.print(f"[yellow]有 {count} 项仍是 <Replace me> 占位符，运行 `akaribot config edit` 填写。[/yellow]")
    else:
        ok("没有待填的占位符")
    return count


def _rollback(instance: Instance, dist: str, snapshot: engine.ConfigSnapshot, runner: engine.CommandRunner) -> None:
    """失败回滚：恢复第 4 步写入的配置，并卸载刚装上的分发包。

    第 5 步的数据库迁移不回滚：迁移是幂等且向前的，回滚风险大于收益，报告里如实告知用户表已建。
    """
    warn("开始回滚安装")
    restored = snapshot.restore(instance)
    if restored:
        console.print("  已恢复配置文件：" + "、".join(str(path.relative_to(instance.root)) for path in restored[:10]))
    try:
        runner.run_checked(engine.uninstall_argv(instance.python, [dist]), what=f"卸载 {dist}")
    except CliError as exc:
        warn(str(exc))
    instance.invalidate()
    warn("数据库迁移不回滚：已建的表保留，属幂等且向前的变更。")


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
            warn(f"{target.dist} 的 requires_core_api 无法解析：{target.requires_core_api}")
        else:
            if not specifier.contains(str(api_version)):
                problems.append(f"{target.dist} 要求 core API {target.requires_core_api}，当前为 {api_version}")
    elif target.requires_core_api and api_version is None:
        warn("未能读到已装 core 的 API 版本，跳过 core API 兼容性检查。")

    problems.extend(engine.dependency_conflicts(target, installed_env))
    if problems:
        for problem in problems:
            console.print(f"[red]  × {problem}[/red]")
        related = engine.installed_api_requirements(target, installed_env)
        if related:
            console.print("  已装包对它的要求：" + "；".join(related))
        if not force:
            fail("依赖冲突（见上）。修正版本约束后重试，或确认无碍后加 --force。")
        warn("--force：忽略上述冲突继续安装，机器人可能无法启动。")
    else:
        ok("兼容性预检通过")


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
    step(1, 7, f"解析 {target.dist}（来源：{target.source}）")
    console.print("  安装参数：" + " ".join(target.specs))
    step(2, 7, "兼容性预检")
    if dry_run:
        console.print("[dim]dry-run：跳过预检[/dim]")
    else:
        _precheck(instance, target, force=force)

    step(3, 7, f"下载并安装（{instance.python}）")
    try:
        runner.run_checked(
            engine.install_argv(instance.python, target.specs, upgrade=upgrade), what=f"安装 {target.dist}"
        )
    except CliError as exc:
        fail(str(exc))
    if dry_run:
        console.print("[dim]dry-run：跳过 config sync、db upgrade 与热装载通知[/dim]")
        return 0
    instance.invalidate()

    snapshot = engine.ConfigSnapshot.take(instance)
    step(4, 7, "补写配置（config sync）")
    try:
        engine.config_sync(instance, target.dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, target.dist, snapshot, runner)
        fail(f"{target.dist} 的配置补写失败，安装已回滚。")

    step(5, 7, "应用数据库迁移（db upgrade）")
    try:
        engine.db_upgrade(instance, target.dist)
    except CliError as exc:
        warn(str(exc))
        _rollback(instance, target.dist, snapshot, runner)
        fail(f"{target.dist} 的数据库迁移失败，安装已回滚。")

    step(6, 7, "通知运行中的实例")
    notify = instance.notify_package_change("install", target.dist)
    if notify.attempted and not notify.delivered:
        warn(notify.detail)
        warn("模块已装好，但需要 `~restart` 或重启进程后才会装载。")
    else:
        console.print("  " + notify.detail)

    step(7, 7, "报告配置项")
    return _report_placeholders(instance, snapshot)


@app.command("list")
def list_packages(
    instance: InstancePathOption = None,
    kind: Annotated[str | None, typer.Option("--kind", help="只看 module 或 adapter")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="输出 JSON，便于脚本消费")] = False,
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
    table = Table(title=f"已装 akaribot 包（{len(selected)}）")
    table.add_column("种类")
    table.add_column("名字")
    table.add_column("版本")
    table.add_column("分发名")
    table.add_column("提供模块")
    table.add_column("来源")
    for info in selected:
        table.add_row(
            info.kind,
            info.display_name,
            info.version,
            info.dist,
            "、".join(info.provides_modules) or "-",
            "可编辑" if info.editable else "发行版",
        )
    console.print(table)


@app.command("add")
def add(
    name: Annotated[str | None, typer.Argument(help="模块名、适配器名或分发名；用 -e 时可省略")] = None,
    dist: Annotated[str | None, typer.Option("--dist", help="直接指定分发名，跳过 registry 查名")] = None,
    version: Annotated[str | None, typer.Option("--version", help="版本或版本区间，如 1.2.3 或 '>=1,<2'")] = None,
    editable: Annotated[Path | None, typer.Option("-e", "--editable", help="以可编辑方式安装该本地目录")] = None,
    extra: Annotated[list[str] | None, typer.Option("--extra", help="要一并安装的 extra，可重复")] = None,
    kind: Annotated[str | None, typer.Option("--kind", help="限定包种类：module 或 adapter")] = None,
    force: Annotated[bool, typer.Option("--force", help="预检发现冲突时仍然继续安装")] = False,
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
            f"{current.dist} 已安装（{current.version}）。升级请用 `akaribot module update {current.display_name}`，重装加 --force。"
        )
    if current is not None:
        warn(f"{current.dist} 已安装（{current.version}），--force 将覆盖重装。")
    _install(target_instance, target, force=force, dry_run=dry_run, verbose=verbose)
    if not dry_run:
        console.print("\n下一步：`akaribot config edit` 填写占位符，运行中可用 `~reload` 让改动生效。")


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
    console.print("  将删除数据表：" + ("、".join(tables) if tables else "无（manifest 未声明 owned_tables）"))
    console.print(
        "  将删除配置文件：" + ("、".join(str(path.relative_to(instance.root)) for path in files) if files else "无")
    )
    if dry_run:
        return
    if not yes:
        typer.confirm("确认删除上述数据表与配置文件（不可恢复）", abort=True)
    for package in packages:
        if package.owned_tables:
            engine.db_purge(instance, package.dist)
    for path in files:
        path.unlink()
    if files:
        ok(f"已删除 {len(files)} 个配置文件")


@app.command("remove")
def remove(
    name: Annotated[str, typer.Argument(help="已安装的模块名、适配器名或分发名")],
    cascade: Annotated[bool, typer.Option("--cascade", help="连带卸载依赖它的包，先列清单再二次确认")] = False,
    force: Annotated[bool, typer.Option("--force", help="无视反向依赖强行卸载并告警")] = False,
    purge_data: Annotated[bool, typer.Option("--purge-data", help="同时删除该包的数据表与配置文件")] = False,
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
        fail(f"{name} 未安装。用 `akaribot module list` 查看已装包。")
    dependents = target.dependents_of(package.dist)
    if dependents and not (cascade or force):
        fail(
            f"{package.display_name} 被以下包依赖：{_describe_installed(dependents)}。"
            "默认拒绝卸载；确认连带卸载加 --cascade，确认破坏依赖加 --force。"
        )
    order = _cascade_order(target, package) if cascade else [package]
    if cascade and dependents:
        console.print("连带卸载清单：" + _describe_installed(order))
        if not dry_run and not yes:
            typer.confirm(f"将卸载 {len(order)} 个包，继续", abort=True)
    if force and dependents:
        warn(f"--force：{_describe_installed(dependents)} 将因缺依赖在 discover() 时不再注册（可恢复，不是数据损坏）。")

    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    for item in order:
        notify = target.notify_package_change("remove", item.dist) if not dry_run else None
        if notify is not None:
            console.print(f"  {item.dist}：{notify.detail}")
    try:
        runner.run_checked(engine.uninstall_argv(target.python, [item.dist for item in order]), what="卸载")
    except CliError as exc:
        fail(str(exc))
    target.invalidate()
    if purge_data:
        _purge(target, order, yes=yes, dry_run=dry_run)
    else:
        console.print("配置与数据默认保留；要一并清理请加 --purge-data。")


@app.command("update")
def update(
    name: Annotated[list[str] | None, typer.Argument(help="要更新的包名，可给多个；缺省配合 --all")] = None,
    all_packages: Annotated[bool, typer.Option("--all", help="更新全部已装包（含 core）")] = False,
    offline: OfflineOption = False,
    force: Annotated[bool, typer.Option("--force", help="已是最新版本时也重装")] = False,
    yes: YesOption = False,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    as_json: Annotated[bool, typer.Option("--json", help="输出 JSON，便于脚本消费")] = False,
    instance: InstancePathOption = None,
) -> None:
    """更新已安装的包；工作区模式下等价于按本地源码重装。"""
    target_instance = require_instance(instance)
    try:
        installed = target_instance.installed()
    except CliError as exc:
        fail(str(exc))
    requested = split_names(name)
    if not requested and not all_packages:
        fail("请给出要更新的包名，或用 `akaribot module update --all` 更新全部。")
    selected: list[PackageInfo] = []
    for item in requested:
        found = target_instance.find_package(item)
        if found is None:
            fail(f"{item} 未安装。用 `akaribot module list` 查看已装包。")
        selected.append(found)
    if all_packages:
        selected = [info for info in installed.values() if engine.canonical(info.dist) != engine.CLI_DIST]
    selected = list({info.dist: info for info in selected}.values())

    workspace_root = target_instance.workspace_root
    catalog = _load_catalog(target_instance, offline=offline, needed=workspace_root is None)
    plans: list[engine.InstallTarget] = []
    skipped: list[tuple[str, str]] = []
    for info in selected:
        if workspace_root is not None:
            resolved = engine.workspace_target(workspace_root, info.dist)
            if resolved is None:
                skipped.append((info.dist, "工作区里没有该包"))
                continue
            plans.append(resolved)
            continue
        latest = catalog.latest(info.dist) if catalog else None
        if not latest:
            skipped.append((info.dist, "registry 里没有该分发"))
            continue
        if latest == info.version and not force:
            skipped.append((info.dist, f"已是最新（{latest}）"))
            continue
        plans.append(
            engine.InstallTarget(dist=info.dist, version=latest, specs=(f"{info.dist}=={latest}",), source="registry")
        )

    if not plans:
        for dist, reason in skipped:
            console.print(f"  跳过 {dist}：{reason}")
        if as_json:
            console.print_json(
                json.dumps({"updated": [], "skipped": [dist for dist, _ in skipped]}, ensure_ascii=False)
            )
        else:
            ok("没有需要更新的包")
        return

    console.print("将更新：" + "、".join(f"{plan.dist}→{plan.version or '本地源码'}" for plan in plans))
    if not dry_run and not yes:
        typer.confirm(f"更新 {len(plans)} 个包", abort=True)
    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    failed: list[str] = []
    try:
        runner.run_checked(
            engine.install_argv(target_instance.python, [spec for plan in plans for spec in plan.specs], upgrade=True),
            what="更新包",
        )
    except CliError as exc:
        fail(str(exc))
    if dry_run:
        console.print("[dim]dry-run：跳过 config sync、db upgrade 与热装载通知[/dim]")
        return
    target_instance.invalidate()
    for plan in plans:
        try:
            engine.config_sync(target_instance, plan.dist)
            engine.db_upgrade(target_instance, plan.dist)
        except CliError as exc:
            failed.append(plan.dist)
            warn(str(exc))
        notify = target_instance.notify_package_change("install", plan.dist)
        if notify.attempted and not notify.delivered:
            warn(notify.detail)
    for dist, reason in skipped:
        console.print(f"  跳过 {dist}：{reason}")
    if failed:
        warn(f"以下包更新后处理失败，需手动重试：{'、'.join(failed)}")
    updated = [plan.dist for plan in plans if plan.dist not in failed]
    if as_json:
        console.print_json(
            json.dumps(
                {"updated": updated, "failed": failed, "skipped": [dist for dist, _ in skipped]}, ensure_ascii=False
            )
        )
    elif failed:
        warn(f"仅 {len(updated)} 个包更新成功；请检查上面的错误后重试。")
    else:
        ok(f"已更新 {len(updated)} 个包" + ("；运行中的实例已收到热装载通知" if updated else ""))
