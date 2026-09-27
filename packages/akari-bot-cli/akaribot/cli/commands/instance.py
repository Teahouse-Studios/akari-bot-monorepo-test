"""管理本机登记过的 AkariBot 实例。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli.instance import console, fail, ok
from akaribot.cli.instances import InstanceEntry, InstanceRegistry, RegistryError, probe_running

app = typer.Typer(help=i18n.t("cli.instance_cmd.help"))


def _registry() -> InstanceRegistry:
    return InstanceRegistry()


def _state_text(entry: InstanceEntry) -> str:
    if not entry.exists:
        return i18n.t("cli.instance_cmd.state_missing")
    running = probe_running(entry.root)
    if running is None:
        return i18n.t("cli.common.unknown")
    return i18n.t("cli.instance_cmd.state_running") if running else i18n.t("cli.instance_cmd.state_stopped")


def _payload(entry: InstanceEntry, *, default: str) -> dict[str, object]:
    return {
        "name": entry.name,
        "root": str(entry.root),
        "locale": entry.locale,
        "added_at": entry.added_at,
        "autostart": entry.autostart,
        "restart_on_crash": entry.restart_on_crash,
        "desired": entry.desired,
        "exists": entry.exists,
        "running": probe_running(entry.root) if entry.exists else False,
        "default": entry.name == default,
    }


@app.command("list", help=i18n.t("cli.instance_cmd.list.help"))
def list_instances(
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
) -> None:
    """列出本机登记过的实例及其运行状态与服务策略。"""
    try:
        registry = _registry()
        entries = registry.load()
        default = registry.default_name()
    except RegistryError as error:
        fail(str(error))
    if as_json:
        console.print_json(json.dumps([_payload(entry, default=default) for entry in entries], ensure_ascii=False))
        return
    if not entries:
        console.print(i18n.t("cli.instance_cmd.list.empty"))
        return
    table = Table(title=i18n.t("cli.instance_cmd.list.table_title", count=len(entries)))
    table.add_column(i18n.t("cli.instance_cmd.column_name"))
    table.add_column(i18n.t("cli.instance_cmd.column_state"))
    table.add_column(i18n.t("cli.instance_cmd.column_autostart"))
    table.add_column(i18n.t("cli.instance_cmd.column_crash"))
    table.add_column(i18n.t("cli.instance_cmd.column_root"))
    for entry in entries:
        marker = i18n.t("cli.instance_cmd.default_mark") if entry.name == default else ""
        table.add_row(
            f"{entry.name}{marker}",
            _state_text(entry),
            _yes_no(entry.autostart),
            _yes_no(entry.restart_on_crash),
            str(entry.root),
        )
    console.print(table)
    console.print(i18n.t("cli.instance_cmd.list.hint"))


def _yes_no(value: bool) -> str:
    return i18n.t("cli.instance_cmd.yes") if value else i18n.t("cli.instance_cmd.no")


@app.command("add", help=i18n.t("cli.instance_cmd.add.help"))
def add_instance(
    path: Annotated[Path, typer.Argument(help=i18n.t("cli.instance_cmd.add.arg_path"))],
    name: Annotated[str | None, typer.Option("--name", help=i18n.t("cli.instance_cmd.add.option_name"))] = None,
    locale: Annotated[str | None, typer.Option("--locale", help=i18n.t("cli.instance_cmd.add.option_locale"))] = None,
) -> None:
    """登记一个已存在的实例目录；只记位置，不动实例本身。"""
    try:
        entry = _registry().add(path, name=name, locale=locale or "")
    except RegistryError as error:
        fail(str(error))
    ok(i18n.t("cli.instance_cmd.add.done", name=entry.name, root=entry.root))


@app.command("remove", help=i18n.t("cli.instance_cmd.remove.help"))
def remove_instance(
    name: Annotated[str, typer.Argument(help=i18n.t("cli.instance_cmd.arg_name"))],
    yes: Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))] = False,
) -> None:
    """删除一条登记；实例目录本身保留。"""
    if not yes:
        typer.confirm(i18n.t("cli.instance_cmd.remove.confirm", name=name), abort=True)
    try:
        removed = _registry().remove(name)
    except RegistryError as error:
        fail(str(error))
    if not removed:
        fail(i18n.t("cli.instance_cmd.unknown", name=name))
    ok(i18n.t("cli.instance_cmd.remove.done", name=name))


@app.command("use", help=i18n.t("cli.instance_cmd.use.help"))
def use_instance(
    name: Annotated[str, typer.Argument(help=i18n.t("cli.instance_cmd.arg_name"))],
) -> None:
    """把某个实例设为缺省：站在实例之外时，命令与界面都按它执行。"""
    try:
        _registry().set_default(name)
    except RegistryError as error:
        fail(str(error))
    ok(i18n.t("cli.instance_cmd.use.done", name=name))


@app.command("policy", help=i18n.t("cli.instance_cmd.policy.help"))
def set_policy(
    name: Annotated[str, typer.Argument(help=i18n.t("cli.instance_cmd.arg_name"))],
    autostart: Annotated[
        bool | None,
        typer.Option("--autostart/--no-autostart", help=i18n.t("cli.instance_cmd.policy.option_autostart")),
    ] = None,
    restart_on_crash: Annotated[
        bool | None,
        typer.Option("--restart-on-crash/--no-restart-on-crash", help=i18n.t("cli.instance_cmd.policy.option_crash")),
    ] = None,
) -> None:
    """设置实例的服务策略：随服务启动而拉起、崩溃后自动重启。"""
    fields: dict[str, object] = {}
    if autostart is not None:
        fields["autostart"] = autostart
    if restart_on_crash is not None:
        fields["restart_on_crash"] = restart_on_crash
    if not fields:
        fail(i18n.t("cli.instance_cmd.policy.nothing"))
    try:
        entry = _registry().update(name, **fields)
    except RegistryError as error:
        fail(str(error))
    ok(
        i18n.t(
            "cli.instance_cmd.policy.done",
            name=entry.name,
            autostart=_yes_no(entry.autostart),
            crash=_yes_no(entry.restart_on_crash),
        )
    )
