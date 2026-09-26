"""实例数据浏览与按主键写入入口。

供 CLI 的 ``db`` 子命令与 TUI 的数据库页以子进程调用；读 ``AKARI_INSTANCE_DIR`` 决定实例。
表与列只认 Tortoise 已注册模型声明过的标识：不接受原始 SQL，也不接受调用方给出的任意表名。
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import sys
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

DEFAULT_LIMIT = 20
MAX_LIMIT = 200

_INT_FIELDS = frozenset({"IntField", "BigIntField", "SmallIntField"})
_TRUE_WORDS = frozenset({"true", "1", "yes", "y", "on"})
_FALSE_WORDS = frozenset({"false", "0", "no", "n", "off"})


class DataError(RuntimeError):
    """用户错误：未知表或列、缺必填字段、主键不存在、值无法按列类型转换。"""


def _registered_tables() -> list[tuple[str, Any]]:
    from tortoise import Tortoise

    found: dict[str, Any] = {}
    for models in Tortoise.apps.values():
        for model in models.values():
            found.setdefault(model._meta.db_table, model)
    return sorted(found.items())


def _fields(model: Any) -> dict[str, Any]:
    meta = model._meta
    return {name: meta.fields_map[name] for name in meta.fields_db_projection if name in meta.fields_map}


def _pk_name(model: Any) -> str:
    return str(model._meta.pk_attr)


def _table_or_fail(name: str) -> tuple[str, Any]:
    for table, model in _registered_tables():
        if table == name:
            return table, model
    raise DataError(f"未注册的表 {name!r}；请先执行 tables 查看可用表。")


def _column_or_fail(fields: Mapping[str, Any], table: str, name: str) -> Any:
    field = fields.get(name)
    if field is None:
        declared = ", ".join(fields) or "-"
        raise DataError(f"表 {table} 没有列 {name!r}；该表声明的列为：{declared}。")
    return field


def _table_owners() -> dict[str, str]:
    from akaribot.core.registry import PackageRegistry

    try:
        PackageRegistry.discover()
        entries = list(PackageRegistry.modules().values()) + list(PackageRegistry.adapters().values())
    except Exception:  # noqa: BLE001 - 清单读取失败只让 package 一栏留空，不应阻断浏览
        return {}
    owners: dict[str, str] = {}
    for entry in entries:
        dist = entry.dist_name or f"akari-bot-{entry.kind}-{entry.name}"
        for table in entry.manifest.owned_tables:
            owners.setdefault(str(table), dist)
    return owners


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dt.datetime | dt.date | dt.time):
        return value.isoformat()
    if isinstance(value, bytes | bytearray | memoryview):
        return bytes(value).hex()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set | frozenset):
        return [_json_safe(item) for item in value]
    return str(value)


def _default_text(value: Any) -> Any:
    # 可调用默认值（uuid4、list 等）要运行期才知道结果，用 null 表示「由模型自行决定」。
    return None if callable(value) else _json_safe(value)


def _is_required(field: Any) -> bool:
    if field.null or field.generated or field.default is not None:
        return False
    return not (getattr(field, "auto_now", False) or getattr(field, "auto_now_add", False))


def _coerce_bool(text: str) -> bool:
    lowered = text.strip().casefold()
    if lowered in _TRUE_WORDS:
        return True
    if lowered in _FALSE_WORDS:
        return False
    raise ValueError(f"布尔取值应为 true 或 false，实际为 {text!r}")


def _coerce(field: Any, text: str, *, table: str, column: str) -> Any:
    kind = type(field).__name__
    try:
        if kind in _INT_FIELDS:
            return int(text)
        if kind == "FloatField":
            return float(text)
        if kind == "DecimalField":
            return Decimal(text)
        if kind == "BooleanField":
            return _coerce_bool(text)
        if kind == "DatetimeField":
            return dt.datetime.fromisoformat(text)
        if kind == "DateField":
            return dt.date.fromisoformat(text)
        if kind == "TimeField":
            return dt.time.fromisoformat(text)
        if kind == "UUIDField":
            return UUID(text)
        if kind == "JSONField":
            return json.loads(text)
        if kind == "BinaryField":
            return bytes.fromhex(text)
    except (ValueError, TypeError, InvalidOperation) as exc:
        raise DataError(f"表 {table} 的列 {column} 无法按 {kind} 解析 {text!r}：{exc}") from exc
    return text


def _parse_assignment(raw: str, *, table: str) -> tuple[str, str]:
    column, separator, value = raw.partition("=")
    column = column.strip()
    if not separator or not column:
        raise DataError(f"表 {table} 的赋值 {raw!r} 不是 <列>=<值> 形式。")
    return column, value


def _order_terms(fields: Mapping[str, Any], table: str, pk_name: str, order_by: str | None) -> list[str]:
    if not order_by:
        return [f"-{pk_name}"]
    column, _, direction = order_by.partition(":")
    column = column.strip()
    _column_or_fail(fields, table, column)
    keyword = direction.strip().casefold()
    if keyword in ("", "asc"):
        term = column
    elif keyword in ("desc", "d"):
        term = f"-{column}"
    else:
        raise DataError(f"排序方向 {direction!r} 不是 asc 或 desc。")
    # 主键作次级排序键：分页时同值行之间才有稳定顺序，翻页不会重复或漏行。
    return [term] if column == pk_name else [term, f"-{pk_name}"]


def _row_payload(fields: Mapping[str, Any], row: Mapping[str, Any]) -> dict[str, Any]:
    return {name: _json_safe(row.get(name)) for name in fields}


async def _write(coro: Any, table: str) -> Any:
    # 唯一约束、外键约束这类拒绝由数据库给出，属调用方给错了值，按用户错误上报。
    from tortoise.exceptions import IntegrityError

    try:
        return await coro
    except IntegrityError as exc:
        raise DataError(f"表 {table} 的写入被数据库拒绝：{exc}") from exc


async def _table_rows(model: Any) -> int | None:
    # 包已装但实例尚未建出该表时读不到条数；此时保留表并如实回报「未知」，不让一张表拖垮整份清单。
    try:
        return await model.all().count()
    except Exception:  # noqa: BLE001 - 不同后端的缺表报错类型不同，统一按未知处理
        return None


async def _tables() -> list[dict[str, Any]]:
    owners = _table_owners()
    payload: list[dict[str, Any]] = []
    for table, model in _registered_tables():
        fields = _fields(model)
        payload.append(
            {
                "table": table,
                "model": model.__name__,
                "rows": await _table_rows(model),
                "package": owners.get(table, ""),
                "columns": [
                    {
                        "name": name,
                        "type": type(field).__name__,
                        "null": bool(field.null),
                        "pk": bool(field.pk),
                        "default": _default_text(field.default),
                    }
                    for name, field in fields.items()
                ],
            }
        )
    return payload


async def _rows(
    table_name: str,
    *,
    limit: int,
    offset: int,
    order_by: str | None,
    filters: Sequence[str],
) -> dict[str, Any]:
    table, model = _table_or_fail(table_name)
    fields = _fields(model)
    # 用户错误先判完再碰库：未知列与非法取值不该先撞上一条数据库报错。
    terms = _order_terms(fields, table, _pk_name(model), order_by)
    conditions: dict[str, Any] = {}
    for raw in filters:
        column, value = _parse_assignment(raw, table=table)
        field = _column_or_fail(fields, table, column)
        conditions[column] = _coerce(field, value, table=table, column=column)
    query = model.filter(**conditions)
    total = await query.count()
    rows = await query.order_by(*terms).limit(limit).offset(offset).values(*fields)
    return {"table": table, "total": total, "rows": [_row_payload(fields, row) for row in rows]}


async def _set(table_name: str, *, key: str, column: str, value: str) -> dict[str, Any]:
    table, model = _table_or_fail(table_name)
    fields = _fields(model)
    pk_name = _pk_name(model)
    if column == pk_name:
        raise DataError(f"列 {column!r} 是表 {table} 的主键，主键不可修改；如需更换请删除后新建。")
    field = _column_or_fail(fields, table, column)
    converted_key = _coerce(_column_or_fail(fields, table, pk_name), key, table=table, column=pk_name)
    converted = _coerce(field, value, table=table, column=column)
    updated = await _write(model.filter(**{pk_name: converted_key}).update(**{column: converted}), table)
    if not updated:
        raise DataError(f"表 {table} 中不存在主键 {pk_name}={key!r} 的数据项。")
    return {"table": table, "key": key, "column": column, "updated": updated}


async def _insert(table_name: str, assignments: Sequence[str]) -> dict[str, Any]:
    table, model = _table_or_fail(table_name)
    fields = _fields(model)
    values: dict[str, Any] = {}
    for raw in assignments:
        column, value = _parse_assignment(raw, table=table)
        field = _column_or_fail(fields, table, column)
        if column in values:
            raise DataError(f"表 {table} 的列 {column!r} 被重复赋值。")
        values[column] = _coerce(field, value, table=table, column=column)
    missing = [name for name, field in fields.items() if _is_required(field) and name not in values]
    if missing:
        raise DataError(f"表 {table} 缺少必填字段：{', '.join(missing)}。")
    created = await _write(model.create(**values), table)
    pk_name = _pk_name(model)
    return {"table": table, "inserted": 1, "key": _json_safe(getattr(created, pk_name, None))}


async def _delete(table_name: str, *, key: str) -> dict[str, Any]:
    table, model = _table_or_fail(table_name)
    fields = _fields(model)
    pk_name = _pk_name(model)
    converted_key = _coerce(_column_or_fail(fields, table, pk_name), key, table=table, column=pk_name)
    deleted = await model.filter(**{pk_name: converted_key}).delete()
    if not deleted:
        raise DataError(f"表 {table} 中不存在主键 {pk_name}={key!r} 的数据项。")
    return {"table": table, "key": key, "deleted": deleted}


async def _dispatch(args: argparse.Namespace) -> Any:
    from akaribot.core.database import close_db, init_db

    await init_db(generate_schemas=False)
    try:
        if args.command == "tables":
            return await _tables()
        if args.command == "rows":
            if args.limit < 0 or args.offset < 0:
                raise DataError("limit 与 offset 不可为负数。")
            return await _rows(
                args.table,
                limit=min(args.limit, MAX_LIMIT),
                offset=args.offset,
                order_by=args.order_by,
                filters=tuple(args.filter or ()),
            )
        if args.command == "set":
            return await _set(args.table, key=args.key, column=args.column, value=args.value)
        if args.command == "insert":
            return await _insert(args.table, tuple(args.set or ()))
        return await _delete(args.table, key=args.key)
    finally:
        await close_db()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.data",
        description="浏览实例数据库的表与数据项，并按主键写入。",
    )
    # 输出恒为 JSON，``--json`` 只为与其它入口的命令行形态保持一致。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="兼容开关，输出恒为 JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("tables", parents=[common], help="列出已注册模型对应的表与列")

    rows = sub.add_parser("rows", parents=[common], help="按表名分页读取数据项")
    rows.add_argument("table", help="表标识，取自 tables 的 table 字段")
    rows.add_argument(
        "--limit", type=int, default=DEFAULT_LIMIT, help=f"每页条数，默认 {DEFAULT_LIMIT}，上限 {MAX_LIMIT}"
    )
    rows.add_argument("--offset", type=int, default=0, help="起始偏移，默认 0")
    rows.add_argument("--order-by", default=None, help="排序列，可带 :asc 或 :desc 后缀；缺省按主键倒序")
    rows.add_argument("--filter", action="append", default=[], help="等值筛选，形如 <列>=<值>，可重复")

    setter = sub.add_parser("set", parents=[common], help="按主键改写单个列")
    setter.add_argument("table", help="表标识")
    setter.add_argument("--key", required=True, help="主键值")
    setter.add_argument("--column", required=True, help="列名，主键列不可修改")
    setter.add_argument("--value", required=True, help="按列类型解析后的新值")

    insert = sub.add_parser("insert", parents=[common], help="新建一条数据项")
    insert.add_argument("table", help="表标识")
    insert.add_argument("--set", action="append", default=[], help="列赋值，形如 <列>=<值>，可重复")

    delete = sub.add_parser("delete", parents=[common], help="按主键删除数据项")
    delete.add_argument("table", help="表标识")
    delete.add_argument("--key", required=True, help="主键值")
    return parser


def _emit(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


def _fail(message: str, code: int) -> int:
    # 失败原因同时进 stdout 的 JSON：调用方（CLI 与界面）只解析 stdout，仅给 stderr 拿不到结构化原因。
    _emit({"error": message})
    print(f"数据操作失败：{message}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码，0 成功、1 运行期失败、2 用户错误。
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        payload = asyncio.run(_dispatch(args))
    except DataError as exc:
        return _fail(str(exc), 2)
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        return _fail(f"{type(exc).__name__}: {exc}", 1)
    _emit(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
