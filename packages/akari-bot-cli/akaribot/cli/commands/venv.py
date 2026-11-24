"""实例 venv 托管。"""

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

# 纯仓库地址根据对应的主机名与 .git 后缀判定为 git 直接引用。其余 http(s) 地址作为普通直接引用交由 uv 处理。
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
    """显示当前模式、解释器路径、环境中的包与清单中记录的运行库。"""
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
                    # 界面根据该清单管理运行环境，包括已安装的包、属于 AkariBot 的包以及记录在实例清单中的项。
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
    # 依赖记录均可解析出对应包名。无法解析时返回空字符串，调用方据此保留该记录。
    names = engine.requirement_names([spec])
    return next(iter(names), "")


# 改写清单中记录的运行库，返回改写后的列表。
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


# 补全直接引用，为仓库地址添加 ``git+`` 前缀，其他地址与依赖声明原样沿用。
def _resolve_spec(spec: str) -> str:
    text = spec.strip()
    if text.startswith(("git+", "ssh://", "git@")) or "://" not in text:
        return text
    host = text.split("://", 1)[1].split("/", 1)[0].lower()
    if host in GIT_HOSTS or text.rstrip("/").endswith(".git"):
        return engine.git_spec(text)
    return text


# 将无版本约束的依赖声明补全为 ``名称==已安装版本``，确保清单中的记录具备可复现性。
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


# 将直接引用规范化为可与 ``direct_url`` 比对的形式，移除 git+ 前缀、片段与末尾斜杠。
def _direct_reference(spec: str) -> str:
    text = spec.strip()
    if not text.startswith("git+") and Path(text).expanduser().exists():
        return Path(text).expanduser().resolve().as_uri()
    return text.removeprefix("git+").split("#", 1)[0].rstrip("/")


# 为直接引用补全包名，安装完成后按 ``direct_url`` 反向查找对应的包。
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


# 将已安装的依赖声明规范化为清单中的记录，尽可能确定包名与版本号。
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
    """将运行库安装至实例环境。``--save`` 会同时写入实例清单，环境重建时根据清单补充安装。"""
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
            env=engine.uv_environment(target),
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
    """从实例环境卸载运行库。``--save`` 同时删除清单中的记录。"""
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
                env=engine.uv_environment(target),
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
    """切换为 CLI 托管 venv，先执行安装与验证流程，验证通过后再卸载源环境中的包。"""
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
    """放弃托管，将实例 venv 中的包迁移回当前环境。"""
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
    """重建实例 venv（Python 升级后修复）。在新环境安装并验证通过后再替换旧目录。"""
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
