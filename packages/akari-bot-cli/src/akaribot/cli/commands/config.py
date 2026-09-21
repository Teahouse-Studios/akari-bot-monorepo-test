"""配置读写。

数据与写入一律经子进程调用 ``python -m akaribot.core.entrypoints.config``：CLI 进程不 import
core，且写入必须走 ``CFGManager.edit_write()`` 的原子路径，命令行与 TUI 都不直接改文件。
表单模式与原始文本模式在 TUI 的 Config 页；命令行提供 list / schema / get / set 与外部编辑器。
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

from akaribot.cli.instance import (
    CliError,
    Instance,
    InstancePathOption,
    console,
    fail,
    ok,
    require_instance,
)

app = typer.Typer(help="配置读写：list / schema / get / set / open")

TableOption = Annotated[str, typer.Option("--table", "-t", help="配置表名，如 module_wiki、bot_telegram")]
JsonOption = Annotated[bool, typer.Option("--json", help="以 JSON 输出，供脚本消费")]

# 表名与配置文件一一对应（扁平布局）：config -> config.toml，secret -> secret.toml，其余为 <表名>.toml。
FILE_BY_TABLE = {"config": "config.toml", "secret": "secret.toml"}


def _entrypoint_json(instance: Instance, *args: str) -> object:
    """调用 core 配置入口并解析其 JSON 输出。

    :param instance: 目标实例。
    :param args: 传给入口的参数（本函数会补 ``--json``）。
    :return: 解析后的对象。
    """
    result = instance.run_core_capture("config", *args, "--json")
    if result.returncode != 0:
        detail = [line for line in (result.stderr or "").strip().splitlines() if line]
        fail(detail[-1] if detail else f"配置入口以退出码 {result.returncode} 结束。")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CliError(f"配置入口返回的不是 JSON：{exc}") from exc


def _config_file(instance: Instance, table: str) -> Path:
    """取配置表对应的文件路径。

    :param instance: 目标实例。
    :param table: 表名。
    :return: 配置文件路径（未必存在）。
    """
    name = FILE_BY_TABLE.get(table, f"{table}.toml")
    base = instance.meta.root / "config"
    for candidate in (base / name, base / "modules" / name, base / "adapters" / name):
        if candidate.is_file():
            return candidate
    return base / name


@app.command("list")
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


@app.command("schema")
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
        console.print(f"表 {table} 没有配置项。")
        return
    grid = Table(title=f"{table}（{len(items)} 项）")
    grid.add_column("键")
    grid.add_column("类型")
    grid.add_column("当前值")
    grid.add_column("注释")
    for item in items:
        shown = "******" if item.get("secret") else str(item.get("value"))
        if item.get("is_placeholder"):
            shown = "[yellow]<待填写>[/yellow]"
        grid.add_row(str(item["key"]), str(item["type"]), shown, str(item.get("comment") or "-"))
    console.print(grid)


@app.command("get")
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


@app.command("set")
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
    ok(f"已写入 {table}.{key}")


@app.command("open")
def open_in_editor(
    table: TableOption = "config",
    instance_path: InstancePathOption = None,
) -> None:
    """用外部编辑器打开配置文件（第三种编辑模式）。"""
    instance = require_instance(instance_path)
    target = _config_file(instance, table)
    if not target.is_file():
        fail(f"配置文件不存在：{target}")
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if not editor:
        editor = "notepad" if sys.platform.startswith("win") else ("open" if sys.platform == "darwin" else "xdg-open")
    if shutil.which(editor.split()[0]) is None:
        fail(f"找不到编辑器 {editor!r}，请设置 $EDITOR 或 $VISUAL。")
    console.print(f"打开 {target}")
    completed = subprocess.run([*editor.split(), str(target)], check=False)
    if completed.returncode != 0:
        fail(f"编辑器以退出码 {completed.returncode} 结束。")


@app.command("edit")
def edit_hint(
    table: TableOption = "config",
    instance_path: InstancePathOption = None,
) -> None:
    """提示三种编辑方式（表单与文本模式在 TUI 里）。"""
    instance = require_instance(instance_path)
    console.print(f"配置文件：{_config_file(instance, table)}")
    console.print("表单模式与原始文本模式：akaribot tui → Config 页")
    console.print("外部编辑器：akaribot config open")
    console.print("脚本写入：akaribot config set <键> <值> --table <表名>")
