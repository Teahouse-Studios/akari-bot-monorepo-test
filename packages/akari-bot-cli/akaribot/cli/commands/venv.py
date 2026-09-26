"""实例 venv 托管"""

from __future__ import annotations

import json
from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import CliError, InstancePathOption, console, fail, require_instance

app = typer.Typer(help=i18n.t("cli.venv.help"))

DryRunOption = Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.venv.option_dry_run"))]


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
    """显示当前模式、解释器路径与已装 akaribot 包数量。"""
    target = require_instance(instance)
    state = engine.venv_status(target)
    if as_json:
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
                    # 界面要列出环境里装了什么：分发名、版本与是否可编辑安装。
                    "packages": (
                        [
                            {"dist": info.dist, "version": info.version, "editable": info.editable}
                            for info in sorted(state.packages.values(), key=lambda item: item.dist)
                        ]
                        if state.packages is not None
                        else None
                    ),
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
