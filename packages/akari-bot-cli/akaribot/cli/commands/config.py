"""配置读写。

数据与写入一律经子进程调用 ``python -m akaribot.core.entrypoints.config``：CLI 进程不 import
core，且写入必须走 ``CFGManager.edit_write()`` 的原子路径，命令行与 TUI 都不直接改文件。
表单模式与原始文本模式在 TUI 的 Config 页；命令行提供 list / schema / placeholders / get / set
与外部编辑器。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli.instance import (
    CliError,
    Instance,
    InstancePathOption,
    console,
    fail,
    ok,
    require_instance,
)

app = typer.Typer(help=i18n.t("cli.config.help"))

TableOption = Annotated[str, typer.Option("--table", "-t", help=i18n.t("cli.common.table_option"))]
JsonOption = Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))]

# 表名与配置文件一一对应（扁平布局）：config -> config.toml，secret -> secret.toml，其余为 <表名>.toml。
FILE_BY_TABLE = {"config": "config.toml", "secret": "secret.toml"}


def _entrypoint_json(instance: Instance, *args: str) -> object:
    result = instance.run_core_capture("config", *args, "--json")
    if result.returncode != 0:
        detail = [line for line in (result.stderr or "").strip().splitlines() if line]
        fail(detail[-1] if detail else i18n.t("cli.config.entry_failed", code=result.returncode))
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CliError(i18n.t("cli.config.entry_not_json", error=exc)) from exc


def _config_file(instance: Instance, table: str) -> Path:
    name = FILE_BY_TABLE.get(table, f"{table}.toml")
    base = instance.meta.root / "config"
    for candidate in (base / name, base / "modules" / name, base / "adapters" / name):
        if candidate.is_file():
            return candidate
    return base / name


@app.command("list", help=i18n.t("cli.config.list.help"))
def list_tables(
    instance_path: InstancePathOption = None,
    json_out: JsonOption = False,
) -> None:
    """列出实例已有的配置表。"""
    instance = require_instance(instance_path)
    tables = sorted(path.stem for path in (instance.meta.root / "config").rglob("*.toml"))
    if json_out:
        console.print_json(json.dumps(tables, ensure_ascii=False))
        return
    for table in tables:
        console.print(table)


@app.command("schema", help=i18n.t("cli.config.schema.help"))
def show_schema(
    table: TableOption,
    instance_path: InstancePathOption = None,
    json_out: JsonOption = False,
) -> None:
    """列出某表的全部配置项（类型、默认值、注释、是否占位）。"""
    instance = require_instance(instance_path)
    items = _entrypoint_json(instance, "schema", "--table", table)
    if json_out:
        console.print_json(json.dumps(items, ensure_ascii=False, default=str))
        return
    assert isinstance(items, list)
    if not items:
        console.print(i18n.t("cli.config.schema.no_items", table=table))
        return
    grid = Table(title=i18n.t("cli.config.schema.table_title", table=table, count=len(items)))
    grid.add_column(i18n.t("cli.config.schema.column_key"))
    grid.add_column(i18n.t("cli.config.schema.column_type"))
    grid.add_column(i18n.t("cli.config.schema.column_value"))
    grid.add_column(i18n.t("cli.config.schema.column_comment"))
    for item in items:
        shown = "******" if item.get("secret") else str(item.get("value"))
        if item.get("is_placeholder"):
            shown = i18n.t("cli.config.schema.placeholder")
        grid.add_row(str(item["key"]), str(item["type"]), shown, str(item.get("comment") or "-"))
    console.print(grid)


@app.command("placeholders", help=i18n.t("cli.config.placeholders.help"))
def show_placeholders(
    instance_path: InstancePathOption = None,
    json_out: JsonOption = False,
) -> None:
    """统计各表的待填写占位符（core 的占位符判定）。"""
    instance = require_instance(instance_path)
    tables = sorted({path.stem for path in (instance.meta.root / "config").rglob("*.toml")})
    args = ["placeholders", "--tables", ",".join(tables)] if tables else ["placeholders"]
    payload = _entrypoint_json(instance, *args)
    if json_out:
        # 界面按行解析 stdout，故 JSON 保持单行原样，不做二次排版。
        print(json.dumps(payload, ensure_ascii=False))
        return
    assert isinstance(payload, dict)
    rows = payload.get("tables") if isinstance(payload.get("tables"), dict) else {}
    failed = payload.get("failed") if isinstance(payload.get("failed"), dict) else {}
    if not rows and not failed:
        console.print(i18n.t("cli.config.placeholders.none"))
        return
    grid = Table(title=i18n.t("cli.config.placeholders.table_title", count=payload.get("count") or 0, tables=len(rows)))
    grid.add_column(i18n.t("cli.config.placeholders.column_table"))
    grid.add_column(i18n.t("cli.config.placeholders.column_placeholder"))
    grid.add_column(i18n.t("cli.config.placeholders.column_total"))
    for table, counts in rows.items():
        detail = counts if isinstance(counts, dict) else {}
        grid.add_row(table, str(detail.get("placeholder")), str(detail.get("total")))
    console.print(grid)
    if failed:
        detail = "、".join(f"{name}（{reason}）" for name, reason in failed.items())
        console.print(i18n.t("cli.config.placeholders.failed_line", count=len(failed), detail=detail))


@app.command("get", help=i18n.t("cli.config.get.help"))
def get_value(
    key: str,
    table: TableOption,
    instance_path: InstancePathOption = None,
    json_out: JsonOption = False,
) -> None:
    """读取单个配置项。"""
    instance = require_instance(instance_path)
    data = _entrypoint_json(instance, "get", key, "--table", table)
    if json_out:
        console.print_json(json.dumps(data, ensure_ascii=False, default=str))
        return
    assert isinstance(data, dict)
    console.print(data.get("value"))


@app.command("set", help=i18n.t("cli.config.set.help"))
def set_value(
    key: str,
    value: str,
    table: TableOption,
    instance_path: InstancePathOption = None,
) -> None:
    """写入单个配置项（经 core 的原子写入路径）。"""
    instance = require_instance(instance_path)
    code = instance.run_core("config", "set", key, value, "--table", table)
    if code != 0:
        raise typer.Exit(code)
    ok(i18n.t("cli.ok.written", table=table, name=key))


@app.command("open", help=i18n.t("cli.config.open.help"))
def open_in_editor(
    table: TableOption = "config",
    instance_path: InstancePathOption = None,
) -> None:
    """用外部编辑器打开配置文件（第三种编辑模式）。"""
    instance = require_instance(instance_path)
    target = _config_file(instance, table)
    if not target.is_file():
        fail(i18n.t("cli.config.open.missing", target=target))
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if not editor:
        editor = "notepad" if sys.platform.startswith("win") else ("open" if sys.platform == "darwin" else "xdg-open")
    if shutil.which(editor.split()[0]) is None:
        fail(i18n.t("cli.config.open.no_editor", editor=repr(editor)))
    console.print(i18n.t("cli.config.open.opening", target=target))
    completed = subprocess.run([*editor.split(), str(target)], check=False)
    if completed.returncode != 0:
        fail(i18n.t("cli.config.open.editor_failed", code=completed.returncode))


@app.command("edit", help=i18n.t("cli.config.edit.help"))
def edit_hint(
    table: TableOption = "config",
    instance_path: InstancePathOption = None,
) -> None:
    """提示三种编辑方式（表单与文本模式在 TUI 里）。"""
    instance = require_instance(instance_path)
    console.print(i18n.t("cli.config.edit.config_file", path=_config_file(instance, table)))
    console.print(i18n.t("cli.config.edit.tui"))
    console.print(i18n.t("cli.config.edit.external"))
    console.print(i18n.t("cli.config.edit.script"))
