"""实例 venv 托管"""

from __future__ import annotations

from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import venv as engine
from akaribot.cli.instance import CliError, InstancePathOption, console, fail, require_instance

app = typer.Typer(help="实例 venv 托管：status / adopt / release / recreate")

DryRunOption = Annotated[bool, typer.Option("--dry-run", help="只打印将执行的命令，不修改任何文件")]


def _report(report: engine.HostingReport) -> None:
    """打印托管动作的结果。"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("动作", report.action)
    table.add_row("源环境", str(report.source))
    table.add_row("目标环境", str(report.target))
    table.add_row("迁移的包", "、".join(report.moved) or "无")
    table.add_row("源环境已卸载", "、".join(report.removed_from_source) or "无")
    console.print(table)
    if report.detail:
        console.print(report.detail)


@app.command("status")
def status(instance: InstancePathOption = None) -> None:
    """显示当前模式、解释器路径与已装 akaribot 包数量。"""
    target = require_instance(instance)
    state = engine.venv_status(target)
    table = Table(title="实例 venv 状态", show_header=False, padding=(0, 2))
    if state.mode == "managed":
        table.add_row("模式", f"托管（runtime.venv = {target.meta.venv}）")
    else:
        table.add_row("模式", "非托管（使用当前环境）")
    table.add_row("实例根", str(target.root))
    table.add_row("解释器", str(state.python))
    table.add_row("venv 目录", str(state.venv_dir))
    if not state.exists:
        table.add_row("状态", "[red]解释器不存在[/red]")
    elif state.packages is None:
        table.add_row("状态", f"[red]探测失败：{state.error}[/red]")
    else:
        table.add_row("已装 akaribot 包", str(state.package_count))
        table.add_row("core 版本", state.core_version or "[yellow]未安装[/yellow]")
    console.print(table)
    if state.mode == "external":
        console.print("运行 `akaribot venv adopt` 可切换为 CLI 托管。")
    elif not state.exists:
        console.print("运行 `akaribot venv recreate` 重建实例 venv。")


@app.command("adopt")
def adopt(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="不询问，直接执行")] = False,
    keep_source: Annotated[bool, typer.Option("--keep-source", help="不卸载源环境的包，只做迁移副本")] = False,
    force: Annotated[bool, typer.Option("--force", help="目标 venv 已存在且非空时覆盖重建")] = False,
    python: Annotated[str | None, typer.Option("--python", help="建 venv 用的解释器；缺省与当前解释器一致")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")] = False,
) -> None:
    """切换为 CLI 托管 venv：先装好并验证，最后才卸载源环境的包。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm(f"将把当前环境的 akaribot 包迁入 {target.venv_dir}，随后从源环境卸载。继续", abort=True)
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


@app.command("release")
def release(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="不询问，直接执行")] = False,
    keep_source: Annotated[bool, typer.Option("--keep-source", help="保留实例 venv 里的包，只做迁移副本")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")] = False,
) -> None:
    """放弃托管：把实例 venv 的包迁回当前环境。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm("将把实例 venv 的包装入当前环境，随后从实例 venv 卸载。继续", abort=True)
    try:
        report = engine.release(
            target,
            runner=engine.CommandRunner(dry_run=dry_run, verbose=verbose),
            keep_source=keep_source,
        )
    except CliError as exc:
        fail(str(exc))
    _report(report)


@app.command("recreate")
def recreate(
    instance: InstancePathOption = None,
    dry_run: DryRunOption = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="不询问，直接执行")] = False,
    force: Annotated[bool, typer.Option("--force", help="暂存目录已存在时覆盖")] = False,
    python: Annotated[str | None, typer.Option("--python", help="新 venv 用的解释器；缺省为当前解释器")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")] = False,
) -> None:
    """重建实例 venv（Python 升级后修复）。新环境装好并验证通过后才与旧目录换位。"""
    target = require_instance(instance)
    if not dry_run and not yes:
        typer.confirm("将重建实例 venv，旧的 venv 在新环境验证通过后删除。继续", abort=True)
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
