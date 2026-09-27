"""数据库浏览与按主键写入。

数据与写入一律经子进程调用 ``python -m akaribot.core.entrypoints.data``：CLI 进程不 import core，
表名与列名只由 core 侧已注册的模型判定。删除在终端里问一次（``--yes`` 跳过），界面自行确认后用
``--yes`` 调用同一条路径。
"""

from __future__ import annotations

import json
from typing import Annotated, Any

import typer
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli.instance import (
    CliError,
    CoreInvocationError,
    Instance,
    InstancePathOption,
    console,
    fail,
    ok,
    require_instance,
)

app = typer.Typer(help=i18n.t("cli.db.help"))

JsonOption = Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))]
YesOption = Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))]
TableArgument = Annotated[str, typer.Argument(metavar="TABLE", help=i18n.t("cli.db.table_argument"))]

# 与 core 入口的默认值保持一致；上限由 core 侧收窄，这里只做展示。
DEFAULT_LIMIT = 20


def _call(instance: Instance, *args: str) -> Any:
    # core 把失败原因也写进 stdout 的 JSON，故先解析再按退出码判定；解析不了就按原始输出报错。
    completed = instance.run_core_capture("data", *args, "--json")
    payload = _parse(completed.stdout)
    if completed.returncode == 0:
        if payload is None:
            raise CliError(i18n.t("cli.db.entry_not_json", output=_tail(completed.stdout)))
        return payload
    reason = ""
    if isinstance(payload, dict):
        reason = str(payload.get("error") or "")
    raise CoreInvocationError(
        reason or i18n.t("cli.db.entry_failed", code=completed.returncode, detail=_tail(completed.stderr)),
        returncode=completed.returncode,
        stderr=completed.stderr or "",
    )


def _parse(stdout: str | None) -> Any:
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _tail(text: str | None, limit: int = 400) -> str:
    return (text or "").strip()[-limit:]


def _guard(action) -> Any:
    # 用户错误在 core 侧是退出码 2，CLI 保持同一个码，脚本才能区分「用错」与「运行失败」。
    try:
        return action()
    except CliError as exc:
        fail(str(exc), code=getattr(exc, "returncode", None) or 1)


def _emit_json(payload: Any) -> None:
    # 界面按行解析 stdout，故 JSON 必须是单行且不被终端宽度折行。
    print(json.dumps(payload, ensure_ascii=False))


def _cell(value: Any) -> str:
    if value is None:
        return i18n.t("cli.db.cell_null")
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


@app.command("tables", help=i18n.t("cli.db.tables.help"))
def list_tables(
    instance_path: InstancePathOption = None,
    as_json: JsonOption = False,
) -> None:
    """列出实例数据库里已注册模型对应的表。"""
    instance = require_instance(instance_path)
    payload = _guard(lambda: _call(instance, "tables"))
    if as_json:
        _emit_json(payload)
        return
    table = Table(title=i18n.t("cli.db.tables.table_title", count=len(payload)))
    table.add_column(i18n.t("cli.db.tables.column_table"))
    table.add_column(i18n.t("cli.db.tables.column_model"))
    table.add_column(i18n.t("cli.db.tables.column_rows"))
    table.add_column(i18n.t("cli.db.tables.column_columns"))
    table.add_column(i18n.t("cli.db.tables.column_package"))
    for item in payload:
        table.add_row(
            str(item.get("table") or ""),
            str(item.get("model") or ""),
            "-" if item.get("rows") is None else str(item.get("rows")),
            str(len(item.get("columns") or ())),
            str(item.get("package") or i18n.t("cli.db.unknown_package")),
        )
    console.print(table)


@app.command("rows", help=i18n.t("cli.db.rows.help"))
def list_rows(
    table_name: TableArgument,
    limit: Annotated[int, typer.Option("--limit", help=i18n.t("cli.db.rows.option_limit"))] = DEFAULT_LIMIT,
    offset: Annotated[int, typer.Option("--offset", help=i18n.t("cli.db.rows.option_offset"))] = 0,
    as_json: JsonOption = False,
    instance_path: InstancePathOption = None,
) -> None:
    """按主键倒序分页读取一张表的数据项。"""
    instance = require_instance(instance_path)
    payload = _guard(lambda: _call(instance, "rows", table_name, "--limit", str(limit), "--offset", str(offset)))
    if as_json:
        _emit_json(payload)
        return
    rows = payload.get("rows") or []
    columns = list(rows[0]) if rows else []
    console.print(i18n.t("cli.db.rows.table_title", table=table_name, total=payload.get("total") or 0, count=len(rows)))
    if not columns:
        console.print(i18n.t("cli.db.rows.empty"))
        return
    table = Table()
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*[_cell(row.get(column)) for column in columns])
    console.print(table)


@app.command("set", help=i18n.t("cli.db.set.help"))
def set_values(
    table_name: TableArgument,
    key: Annotated[str, typer.Option("--key", help=i18n.t("cli.db.option_key"))],
    assignments: Annotated[list[str], typer.Option("--set", help=i18n.t("cli.db.set.option_set"))] = [],
    as_json: JsonOption = False,
    instance_path: InstancePathOption = None,
) -> None:
    """按主键改写一行的若干列；各列在同一次 UPDATE 里下发，主键列不可修改。"""
    instance = require_instance(instance_path)
    args = ["set", table_name, "--key", key]
    for assignment in assignments:
        args += ["--set", assignment]
    payload = _guard(lambda: _call(instance, *args))
    if as_json:
        _emit_json(payload)
        return
    ok(
        i18n.t(
            "cli.db.set.done",
            table=table_name,
            pk=key,
            columns=i18n.t("cli.common.list_separator").join(str(name) for name in payload.get("columns") or ()),
            count=payload.get("updated") or 0,
        )
    )


@app.command("insert", help=i18n.t("cli.db.insert.help"))
def insert_row(
    table_name: TableArgument,
    assignment: Annotated[list[str] | None, typer.Option("--set", help=i18n.t("cli.db.insert.option_set"))] = None,
    as_json: JsonOption = False,
    instance_path: InstancePathOption = None,
) -> None:
    """新建一条数据项；必填字段由 core 侧的模型声明判定。"""
    instance = require_instance(instance_path)
    args = ["insert", table_name]
    for item in assignment or []:
        args.extend(["--set", item])
    payload = _guard(lambda: _call(instance, *args))
    if as_json:
        _emit_json(payload)
        return
    ok(i18n.t("cli.db.insert.done", table=table_name, pk=_cell(payload.get("key"))))


@app.command("delete", help=i18n.t("cli.db.delete.help"))
def delete_row(
    table_name: TableArgument,
    key: Annotated[str, typer.Option("--key", help=i18n.t("cli.db.option_key"))],
    yes: YesOption = False,
    as_json: JsonOption = False,
    instance_path: InstancePathOption = None,
) -> None:
    """按主键删除一条数据项。"""
    instance = require_instance(instance_path)
    if not yes:
        typer.confirm(i18n.t("cli.db.delete.confirm", table=table_name, pk=key), abort=True)
    payload = _guard(lambda: _call(instance, "delete", table_name, "--key", key))
    if as_json:
        _emit_json(payload)
        return
    ok(i18n.t("cli.db.delete.done", table=table_name, pk=key, count=payload.get("deleted") or 0))
