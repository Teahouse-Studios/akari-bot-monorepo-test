"""实例 venv 托管"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated

import typer
from packaging.requirements import InvalidRequirement, Requirement
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import (
    CliError,
    InstancePathOption,
    console,
    fail,
    ok,
    require_instance,
    warn,
)

app = typer.Typer(help=i18n.t("cli.venv.help"))

DryRunOption = Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.venv.option_dry_run"))]

# 裸仓库地址按这些主机名与 .git 后缀判定为 git 直引用；其余 http(s) 地址按普通直引用交给 uv。
GIT_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org", "gitee.com", "git.sr.ht")


def _report(report: engine.HostingReport) -> None:
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row(i18n.t("cli.venv.report.action"), report.action)
    table.add_row(i18n.t("cli.venv.report.source"), str(report.source))
    table.add_row(i18n.t("cli.venv.report.target"), str(report.target))
    separator = i18n.t("cli.common.list_separator")
    none = i18n.t("cli.venv.none")
    table.add_row(i18n.t("cli.venv.report.moved"), separator.join(report.moved) or none)
    table.add_row(i18n.t("cli.venv.report.removed"), separator.join(report.removed_from_source) or none)
    console.print(table)
    if report.detail:
        console.print(report.detail)


@app.command("status", help=i18n.t("cli.venv.status.help"))
def status(
    instance: InstancePathOption = None,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """显示当前模式、解释器路径、环境里的包与清单里记录的运行库。"""
    target = require_instance(instance)
    state = engine.venv_status(target)
    if as_json:
        recorded = engine.requirement_names(state.requirements)
        typer.echo(
            json.dumps(
                {
                    "mode": state.mode,
                    "root": str(target.root),
                    "python": str(state.python),
                    "venv_dir": str(state.venv_dir),
                    "venv": target.meta.venv,
                    "exists": state.exists,
                    "package_count": state.package_count if state.packages is not None else None,
                    "installed_count": state.installed_count,
                    # 界面按这份清单管理环境：装了什么、哪些是 AkariBot 的、哪些记在实例清单里。
                    "installed": (
                        [
                            {
                                "dist": info.dist,
                                "version": info.version,
                                "editable": info.editable,
                                "requires": list(info.requires),
                                "groups": sorted({key.split("|", 1)[0] for key in info.entry_points}),
                                "url": info.url,
                                "akari": engine.is_akari_dist(info),
                                "recorded": info.dist in recorded,
                            }
                            for info in sorted(state.installed.values(), key=lambda item: item.dist)
                        ]
                        if state.installed is not None
                        else None
                    ),
                    "requirements": list(state.requirements),
                    "core_version": state.core_version,
                    "error": state.error,
                },
                ensure_ascii=False,
            )
        )
        return
    table = Table(title=i18n.t("cli.venv.status.title"), show_header=False, padding=(0, 2))
    if state.mode == "managed":
        table.add_row(i18n.t("cli.venv.status.mode"), i18n.t("cli.venv.status.mode_managed", venv=target.meta.venv))
    else:
        table.add_row(i18n.t("cli.venv.status.mode"), i18n.t("cli.venv.status.mode_external"))
    table.add_row(i18n.t("cli.venv.status.root"), str(target.root))
    table.add_row(i18n.t("cli.venv.status.python"), str(state.python))
    table.add_row(i18n.t("cli.venv.status.venv_dir"), str(state.venv_dir))
    if not state.exists:
        table.add_row(i18n.t("cli.venv.status.state"), i18n.t("cli.venv.status.missing"))
    elif state.packages is None:
        table.add_row(i18n.t("cli.venv.status.state"), i18n.t("cli.venv.status.probe_failed", error=state.error))
    else:
        table.add_row(i18n.t("cli.venv.status.packages"), str(state.package_count))
        table.add_row(
            i18n.t("cli.venv.status.core_version"), state.core_version or i18n.t("cli.venv.status.not_installed")
        )
    console.print(table)
    if state.mode == "external":
        console.print(i18n.t("cli.venv.status.adopt_hint"))
    elif not state.exists:
        console.print(i18n.t("cli.venv.status.recreate_hint"))


def _recorded_name(spec: str) -> str:
    # 记录串都能解析出分发名；解析不出时返回空串，调用方据此保留它。
    names = engine.requirement_names([spec])
    return next(iter(names), "")


# 改写清单里记录的运行库，返回改写后的列表。
def _record(instance, specs: Sequence[str], *, drop: bool = False) -> tuple[str, ...]:
    current = list(instance.meta.requirements)
    if drop:
        wanted = {engine.canonical(spec) for spec in specs}
        current = [spec for spec in current if engine.canonical(_recorded_name(spec)) not in wanted]
    else:
        current.extend(specs)
    instance.meta.set_requirements(current)
    instance.meta.save()
    return instance.meta.requirements


# 补全直接引用：仓库地址加 ``git+`` 前缀，其它地址与需求串原样沿用。
def _resolve_spec(spec: str) -> str:
    text = spec.strip()
    if text.startswith(("git+", "ssh://", "git@")) or "://" not in text:
        return text
    host = text.split("://", 1)[1].split("/", 1)[0].lower()
    if host in GIT_HOSTS or text.rstrip("/").endswith(".git"):
        return engine.git_spec(text)
    return text


# 把没有版本约束的需求串补成 ``名字==装到的版本``，让清单里的记录可复现。
def _pin_spec(python: Path, spec: str) -> str:
    try:
        requirement = Requirement(spec)
    except InvalidRequirement:
        return spec
    if requirement.specifier or requirement.url:
        return spec
    try:
        found = engine.probe_environment(python, names=[requirement.name])
    except CliError:
        return spec
    info = found.get(engine.canonical(requirement.name))
    if info is None or not info.version:
        return spec
    extras = f"[{','.join(sorted(requirement.extras))}]" if requirement.extras else ""
    return f"{requirement.name}{extras}=={info.version}"


# 把直接引用规范成可与 ``direct_url`` 比对的形式：去掉 git+ 前缀、片段与末尾斜杠。
def _direct_reference(spec: str) -> str:
    text = spec.strip()
    if not text.startswith("git+") and Path(text).expanduser().exists():
        return Path(text).expanduser().resolve().as_uri()
    return text.removeprefix("git+").split("#", 1)[0].rstrip("/")


# 给直接引用补上分发名：装完之后按 ``direct_url`` 反查是谁装的。
def _named_direct_spec(python: Path, spec: str) -> str:
    address = _direct_reference(spec)
    target = spec if spec.startswith("git+") else address
    try:
        found = engine.probe_environment(python, all_distributions=True)
    except CliError:
        return spec
    for info in found.values():
        url = info.url.removeprefix("git+").split("#", 1)[0].rstrip("/")
        if url and url == address:
            return f"{info.dist} @ {target}"
    return spec


def _is_direct_reference(spec: str) -> bool:
    return spec.startswith("git+") or "://" in spec or Path(spec).expanduser().exists()


# 把装好的需求串规范成清单里的记录：能定名就定名，能定版就定版。
def _recorded_spec(python: Path, spec: str) -> str:
    if _is_direct_reference(spec):
        return _named_direct_spec(python, spec)
    return _pin_spec(python, spec)


@app.command("add", help=i18n.t("cli.venv.add.help"))
def add(
    spec: Annotated[str, typer.Argument(help=i18n.t("cli.venv.add.arg_spec"))],
    instance: InstancePathOption = None,
    save: Annotated[bool, typer.Option("--save/--no-save", help=i18n.t("cli.venv.add.option_save"))] = True,
    upgrade: Annotated[bool, typer.Option("--upgrade", "-U", help=i18n.t("cli.venv.add.option_upgrade"))] = False,
    dry_run: DryRunOption = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.venv.option_verbose"))] = False,
) -> None:
    """把运行库装进实例环境；``--save`` 同时记进实例清单，环境重建时按它补装。"""
    target = require_instance(instance)
    text = _resolve_spec(spec)
    if not text:
        fail(i18n.t("cli.venv.add.empty_spec"))
    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    try:
        runner.run_checked(
            engine.install_argv(target.python, [text], upgrade=upgrade),
            what=i18n.t("cli.venv_engine.what_install_dist", dist=text),
            stream=True,
        )
    except CliError as exc:
        fail(str(exc))
    target.invalidate()
    if dry_run:
        console.print(i18n.t("cli.venv.add.dry_run"))
        return
    if not save:
        console.print(i18n.t("cli.venv.add.not_saved"))
        return
    recorded = _recorded_spec(target.python, text)
    if recorded == text and _is_direct_reference(text):
        warn(i18n.t("cli.venv.add.unnamed_git", spec=text))
        return
    _record(target, [recorded])
    ok(i18n.t("cli.venv.add.saved", spec=recorded))


@app.command("remove", help=i18n.t("cli.venv.remove.help"))
def remove(
    dist: Annotated[str, typer.Argument(help=i18n.t("cli.venv.remove.arg_dist"))],
    instance: InstancePathOption = None,
    save: Annotated[bool, typer.Option("--save/--no-save", help=i18n.t("cli.venv.remove.option_save"))] = True,
    dry_run: DryRunOption = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.venv.option_verbose"))] = False,
) -> None:
    """从实例环境卸载运行库；``--save`` 同时删掉清单里的记录。"""
    target = require_instance(instance)
    name = engine.canonical(dist)
    recorded = engine.requirement_names(target.meta.requirements)
    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    installed = engine.probe_environment(target.python, all_distributions=True)
    if name in installed:
        try:
            runner.run_checked(
                engine.uninstall_argv(target.python, [dist]),
                what=i18n.t("cli.venv_engine.what_uninstall_dist", dist=dist),
                stream=True,
            )
        except CliError as exc:
            fail(str(exc))
        target.invalidate()
    elif name not in recorded:
        fail(i18n.t("cli.venv.remove.absent", dist=dist))
    else:
        console.print(i18n.t("cli.venv.remove.not_installed", dist=dist))
    if dry_run:
        console.print(i18n.t("cli.venv.add.dry_run"))
        return
    if not save:
        if name in recorded:
            console.print(i18n.t("cli.venv.remove.kept_record", spec=recorded[name]))
        return
    if name in recorded:
        _record(target, [name], drop=True)
        ok(i18n.t("cli.venv.remove.record_dropped", spec=recorded[name]))


@app.command("adopt", help=i18n.t("cli.venv.adopt.help"))
def adopt(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))] = False,
    keep_source: Annotated[
        bool, typer.Option("--keep-source", help=i18n.t("cli.venv.adopt.option_keep_source"))
    ] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.venv.adopt.option_force"))] = False,
    python: Annotated[str | None, typer.Option("--python", help=i18n.t("cli.venv.adopt.option_python"))] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.venv.option_verbose"))] = False,
) -> None:
    """切换为 CLI 托管 venv：先装好并验证，最后才卸载源环境的包。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm(i18n.t("cli.venv.adopt.confirm", venv=target.venv_dir), abort=True)
    try:
        report = engine.adopt(
            target,
            runner=engine.CommandRunner(dry_run=dry_run, verbose=verbose),
            keep_source=keep_source,
            force=force,
            python=python,
        )
    except CliError as exc:
        fail(str(exc))
    _report(report)


@app.command("release", help=i18n.t("cli.venv.release.help"))
def release(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))] = False,
    keep_source: Annotated[
        bool, typer.Option("--keep-source", help=i18n.t("cli.venv.release.option_keep_source"))
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.venv.option_verbose"))] = False,
) -> None:
    """放弃托管：把实例 venv 的包迁回当前环境。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm(i18n.t("cli.venv.release.confirm"), abort=True)
    try:
        report = engine.release(
            target,
            runner=engine.CommandRunner(dry_run=dry_run, verbose=verbose),
            keep_source=keep_source,
        )
    except CliError as exc:
        fail(str(exc))
    _report(report)


@app.command("recreate", help=i18n.t("cli.venv.recreate.help"))
def recreate(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.venv.recreate.option_force"))] = False,
    python: Annotated[str | None, typer.Option("--python", help=i18n.t("cli.venv.recreate.option_python"))] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.venv.option_verbose"))] = False,
) -> None:
    """重建实例 venv（Python 升级后修复）。新环境装好并验证通过后才与旧目录换位。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm(i18n.t("cli.venv.recreate.confirm"), abort=True)
    try:
        report = engine.recreate(
            target,
            runner=engine.CommandRunner(dry_run=dry_run, verbose=verbose),
            python=python,
            force=force,
        )
    except CliError as exc:
        fail(str(exc))
    _report(report)
