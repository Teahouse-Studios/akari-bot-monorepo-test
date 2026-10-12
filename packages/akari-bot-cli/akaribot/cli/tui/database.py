"""数据库页：浏览已注册的表和数据项，通过模态框确认写入操作。

数据读取与写入均通过 ``akaribot db`` 子命令执行。
内容区不足 :data:`SIDE_BY_SIDE_MIN_WIDTH` 列时，表清单、数据项与编辑区分为两行显示。
"""

from __future__ import annotations

import asyncio
import json
import re
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context

# 仅加载当前页，避免一次读取大量数据；分页与总数由 core 计算。
PAGE_LIMIT = 50
# 三栏并排所需的最小内容宽度：表清单 26 列、数据项 32 列（四个翻页按钮的自然宽度）、编辑区 34 列。
# 窄屏采用两行布局，为数据项和编辑区保留可读宽度。
SIDE_BY_SIDE_MIN_WIDTH = 92

PAGER_BUTTONS = ("db-first-page", "db-previous-page", "db-next-page", "db-last-page")
# 运算符按长度降序匹配，避免将 != 识别为 =。
FILTER_OPERATORS = ("!=", ">=", "<=", "!~", "~", "^", "$", "=", ">", "<")
# 筛选条件必须包含列名，避免将搜索词中的运算符识别为条件。
CONDITION_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*(?:!=|>=|<=|!~|~|\^|\$|=|>|<)")


def is_condition(text: str) -> bool:
    """判断输入是否为列名与运算符组成的筛选条件，其余输入作为全表搜索词。

    :param text: 用户输入的文本。
    :return: 是条件时为 ``True``。
    """
    return bool(CONDITION_PATTERN.match(text.strip()))


QUERY_TIMEOUT_SECONDS = 120.0
STATUS_TAIL_LIMIT = 300


@dataclass(frozen=True)
class ColumnInfo:
    """一个列的类型信息。

    :param name: 列名，取自模型的字段名。
    :param type: 模型字段的类型名，如 ``CharField``。
    :param null: 是否允许空值。
    :param pk: 是否为主键列。
    :param default: 模型声明的默认值；由模型自行决定时为 ``None``。
    """

    name: str
    type: str = ""
    null: bool = False
    pk: bool = False
    default: Any = None

    @property
    def label(self) -> str:
        """返回包含类型的字段名标签。"""
        if not self.type:
            return self.name
        return i18n.t("cli.tui.database.field_label", column=self.name, kind=self.type)


@dataclass(frozen=True)
class TableInfo:
    """一张已注册模型对应的表。

    :param name: 表标识，如 ``module_status``。
    :param model: 模型类名。
    :param rows: 表内数据项条数。
    :param package: 声明该表的已安装分发包；无法获取时为空串。
    :param columns: 列信息，顺序同模型声明。
    """

    name: str
    model: str = ""
    rows: int | None = 0
    package: str = ""
    columns: tuple[ColumnInfo, ...] = ()

    @property
    def pk(self) -> ColumnInfo | None:
        """返回主键列，模型未声明时返回 ``None``。"""
        for column in self.columns:
            if column.pk:
                return column
        return None

    @property
    def pk_name(self) -> str:
        """返回主键列名，无法获取时返回空串。"""
        column = self.pk
        return column.name if column is not None else ""

    def editable_columns(self) -> tuple[ColumnInfo, ...]:
        """返回可编辑的列，主键只能只读展示。"""
        return tuple(column for column in self.columns if not column.pk)


@dataclass(frozen=True)
class RowQuery:
    """数据项查询的筛选条件与排序。

    :param filters: 筛选条件，形如 ``<列><运算符><值>``；多条之间是 AND。
    :param search: 全表搜索词，在所有文本列上做包含匹配。
    :param order_by: 排序列，可带 ``:asc`` / ``:desc``；空串表示用 core 的默认顺序。
    """

    filters: tuple[str, ...] = ()
    search: str = ""
    order_by: str = ""

    def is_empty(self) -> bool:
        """返回是否没有任何条件。"""
        return not self.filters and not self.search

    def with_filter(self, condition: str) -> RowQuery:
        """追加一条筛选条件；重复的条件不重复添加。"""
        text = condition.strip()
        if not text or text in self.filters:
            return self
        return replace(self, filters=(*self.filters, text))

    def with_search(self, keyword: str) -> RowQuery:
        """设置全表搜索词。"""
        return replace(self, search=keyword.strip())

    def summary(self) -> str:
        """返回状态栏用的一行说明。"""
        separator = i18n.t("cli.common.list_separator")
        parts = list(self.filters)
        if self.search:
            parts.append(i18n.t("cli.tui.database.search_term", keyword=self.search))
        return separator.join(parts)


@dataclass(frozen=True)
class RowPage:
    """一页数据项。

    :param table: 表标识。
    :param total: 满足当前条件的数据项总数；未统计时为 ``None``（调用方沿用上次的值）。
    :param rows: 本页数据项，键为列名。
    :param offset: 本页起始偏移。
    :param limit: 本页条数上限。
    """

    table: str = ""
    total: int | None = 0
    rows: tuple[dict[str, Any], ...] = ()
    offset: int = 0
    limit: int = PAGE_LIMIT

    @property
    def rows_total(self) -> int:
        """返回已知的总条数；未统计时按 0 处理。"""
        return int(self.total or 0)

    @property
    def pages(self) -> int:
        """返回总页数，至少为 1。"""
        return max(1, -(-self.rows_total // max(self.limit, 1)))

    @property
    def page_number(self) -> int:
        """返回当前页码，从 1 开始。"""
        return self.offset // max(self.limit, 1) + 1

    @property
    def last_offset(self) -> int:
        """返回末页的起始偏移。"""
        return max(0, (self.pages - 1) * max(self.limit, 1))


@dataclass(frozen=True)
class WriteResult:
    """一次写入的结果。

    :param ok: 子进程是否成功。
    :param message: 一行结论，用于状态栏与通知。
    :param detail: 失败时的补充信息，通常为子进程输出或错误原因。
    """

    ok: bool
    message: str
    detail: str = ""


@dataclass(frozen=True)
class WritePlan:
    """待确认的一次写入。

    :param kind: ``set`` / ``insert`` / ``delete``。
    :param table: 表标识。
    :param key: 主键值；新建时为空串。
    :param changes: ``set`` 的 ``(列, 旧值, 新值)`` 序列。
    :param values: ``insert`` 的 ``(列, 值)`` 序列。
    """

    kind: str
    table: str
    key: str = ""
    changes: tuple[tuple[str, str, str], ...] = ()
    values: tuple[tuple[str, str], ...] = ()

    def summary(self) -> str:
        """返回状态栏用的一行说明，列出将更改的列与新旧值。"""
        if self.kind == "delete":
            return i18n.t("cli.tui.database.confirm_delete", table=self.table, pk=self.key)
        if self.kind == "insert":
            values = i18n.t("cli.tui.database.list_separator").join(
                i18n.t("cli.tui.database.value_item", column=column, value=value) for column, value in self.values
            )
            return i18n.t("cli.tui.database.confirm_insert", table=self.table, values=values)
        changes = i18n.t("cli.tui.database.list_separator").join(
            i18n.t("cli.tui.database.change_item", column=column, before=before, after=after)
            for column, before, after in self.changes
        )
        return i18n.t("cli.tui.database.confirm_set", table=self.table, pk=self.key, changes=changes)


# 替身数据源使用与 core 一致的筛选运算符，使测试能够验证筛选后的记录。
def _matches(row: Mapping[str, Any], query: RowQuery) -> bool:
    text = _text
    for condition in query.filters:
        column, operator, value = _split_filter(condition)
        if not column or column not in row:
            return False
        current = text(row.get(column))
        wanted = value.strip()
        if wanted.casefold() in ("null", "none"):
            hit = not current
        elif operator == "~":
            hit = wanted.casefold() in current.casefold()
        elif operator == "!~":
            hit = wanted.casefold() not in current.casefold()
        elif operator == "^":
            hit = current.casefold().startswith(wanted.casefold())
        elif operator == "$":
            hit = current.casefold().endswith(wanted.casefold())
        elif operator == "!=":
            hit = current != wanted
        elif operator == ">":
            hit = _compare(current, wanted) > 0
        elif operator == ">=":
            hit = _compare(current, wanted) >= 0
        elif operator == "<":
            hit = _compare(current, wanted) < 0
        elif operator == "<=":
            hit = _compare(current, wanted) <= 0
        else:
            hit = current == wanted
        if not hit:
            return False
    if query.search:
        needle = query.search.casefold()
        if not any(needle in text(value).casefold() for key, value in row.items() if key != "__none__"):
            return False
    return True


# 拆分 ``<列><运算符><值>``；只有列名时按「非空」处理。
def _split_filter(condition: str) -> tuple[str, str, str]:
    text = condition.strip()
    for operator in FILTER_OPERATORS:
        column, found, value = text.partition(operator)
        if found:
            return column.strip(), operator, value
    return text, "!=", "null"


def _compare(current: str, wanted: str) -> int:
    # 数值优先按数值比较，其他值按文本比较。
    try:
        left, right = float(current), float(wanted)
    except ValueError:
        return (current > wanted) - (current < wanted)
    return (left > right) - (left < right)


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def normalize_columns(payload: Any) -> tuple[ColumnInfo, ...]:
    """把 ``db tables --json`` 中的列数组归一化为列信息。

    :param payload: ``columns`` 字段的内容。
    :return: 列信息元组，无法识别的条目跳过。
    """
    if not isinstance(payload, Sequence) or isinstance(payload, (str, bytes)):
        return ()
    columns: list[ColumnInfo] = []
    for item in payload:
        if not isinstance(item, Mapping):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        columns.append(
            ColumnInfo(
                name=name,
                type=str(item.get("type") or ""),
                null=bool(item.get("null")),
                pk=bool(item.get("pk")),
                default=item.get("default"),
            )
        )
    return tuple(columns)


def normalize_tables(payload: Any) -> tuple[TableInfo, ...]:
    """把 ``db tables --json`` 的输出归一化为表清单。

    :param payload: ``json.loads`` 的结果，接受数组与 ``{"tables": [...]}`` 两种形态。
    :return: 按表名排序的表信息元组。
    """
    if isinstance(payload, Mapping):
        for key in ("tables", "items", "data"):
            nested = payload.get(key)
            if isinstance(nested, Sequence) and not isinstance(nested, (str, bytes)):
                return normalize_tables(nested)
        return ()
    if not isinstance(payload, Sequence) or isinstance(payload, (str, bytes)):
        return ()
    tables: list[TableInfo] = []
    for item in payload:
        if not isinstance(item, Mapping):
            continue
        name = str(item.get("table") or "").strip()
        if not name:
            continue
        tables.append(
            TableInfo(
                name=name,
                model=str(item.get("model") or ""),
                rows=int(item["rows"]) if isinstance(item.get("rows"), int) else None,
                package=str(item.get("package") or ""),
                columns=normalize_columns(item.get("columns")),
            )
        )
    return tuple(sorted(tables, key=lambda table: table.name))


def normalize_page(payload: Any, table: str) -> RowPage:
    """把 ``db rows --json`` 的输出归一化为一页数据项。"""
    if not isinstance(payload, Mapping):
        return RowPage(table=table)
    rows = payload.get("rows")
    collected: list[dict[str, Any]] = []
    if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
        collected = [dict(row) for row in rows if isinstance(row, Mapping)]
    return RowPage(
        table=str(payload.get("table") or table),
        total=int(payload["total"]) if isinstance(payload.get("total"), int) else None,
        rows=tuple(collected),
        offset=int(payload.get("offset") or 0),
        limit=int(payload.get("limit") or PAGE_LIMIT),
    )


class DatabaseSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


@runtime_checkable
class DatabaseSource(Protocol):
    """数据库数据源接口；测试注入替身，实际运行通过子进程访问。"""

    def tables(self) -> Sequence[TableInfo]:
        """返回实例数据库中已注册模型的表。"""

    def rows(
        self, table: str, *, limit: int, offset: int, query: RowQuery | None = None, count: bool = True
    ) -> RowPage:
        """返回一张表的一页数据项；``query`` 给筛选条件与排序，``count`` 为假时不重算总条数。"""

    def set_values(self, table: str, key: str, values: Mapping[str, str]) -> WriteResult:
        """按主键更新数据项的指定列；多列更改通过一次调用提交。"""

    def insert_row(self, table: str, values: Mapping[str, str]) -> WriteResult:
        """新建一条数据项。"""

    def delete_row(self, table: str, key: str) -> WriteResult:
        """按主键删除一条数据项。"""


class StaticDatabaseSource:
    """固定数据的替身数据源，供自动化断言与自检使用，不产生任何子进程。

    :param tables: 表清单。
    :param pages: 表名到数据项的映射；未指定时返回空页。
    :param write_result: 写入返回值；默认为成功。
    :param delete_result: 删除返回值；默认为成功。
    :param insert_result: 新建返回值；默认为成功。
    """

    def __init__(
        self,
        tables: Sequence[TableInfo] = (),
        pages: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
        *,
        write_result: WriteResult | None = None,
        delete_result: WriteResult | None = None,
        insert_result: WriteResult | None = None,
    ) -> None:
        self._tables = tuple(tables)
        self._pages = {name: [dict(row) for row in rows] for name, rows in (pages or {}).items()}
        self._write_result = write_result or WriteResult(True, i18n.t("cli.tui.database.stub_write_ok"), "stub")
        self._delete_result = delete_result or WriteResult(True, i18n.t("cli.tui.database.stub_delete_ok"), "stub")
        self._insert_result = insert_result or WriteResult(True, i18n.t("cli.tui.database.stub_insert_ok"), "stub")
        self.calls = {"tables": 0, "rows": 0, "set": 0, "insert": 0, "delete": 0}
        self.writes: list[tuple[str, str, str, str]] = []
        self.inserted: list[tuple[str, dict[str, str]]] = []
        self.deleted: list[tuple[str, str]] = []
        self.reads: list[tuple[str, int, int]] = []
        self.queries: list[tuple[str, RowQuery, bool]] = []

    def tables(self) -> Sequence[TableInfo]:
        """见 :meth:`DatabaseSource.tables`。"""
        self.calls["tables"] += 1
        return self._tables

    def rows(
        self, table: str, *, limit: int, offset: int, query: RowQuery | None = None, count: bool = True
    ) -> RowPage:
        """返回按条件筛选并分页的数据项，筛选规则与 core 一致。"""
        self.calls["rows"] += 1
        self.reads.append((table, limit, offset))
        self.queries.append((table, query or RowQuery(), count))
        items = [row for row in self._pages.get(table, []) if _matches(row, query or RowQuery())]
        return RowPage(
            table=table,
            total=len(items) if count else None,
            rows=tuple(items[offset : offset + limit]),
            offset=offset,
            limit=limit,
        )

    def set_values(self, table: str, key: str, values: Mapping[str, str]) -> WriteResult:
        """见 :meth:`DatabaseSource.set_values`。"""
        self.calls["set"] += 1
        self.writes.append((table, key, dict(values)))
        return self._write_result

    def insert_row(self, table: str, values: Mapping[str, str]) -> WriteResult:
        """见 :meth:`DatabaseSource.insert_row`。"""
        self.calls["insert"] += 1
        self.inserted.append((table, dict(values)))
        return self._insert_result

    def delete_row(self, table: str, key: str) -> WriteResult:
        """见 :meth:`DatabaseSource.delete_row`。"""
        self.calls["delete"] += 1
        self.deleted.append((table, key))
        return self._delete_result


class SubprocessDatabaseSource:
    """默认数据源：一律经 ``akaribot db`` 子进程，CLI 进程内不 import core。

    :param root: 实例根；默认按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param timeout: 单个子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = QUERY_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        # 每次读取时解析实例根，确保切换实例后使用当前实例。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"tables": 0, "rows": 0, "set": 0, "insert": 0, "delete": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def tables(self) -> Sequence[TableInfo]:
        """见 :meth:`DatabaseSource.tables`。"""
        self.calls["tables"] += 1
        return normalize_tables(self._invoke("tables"))

    def rows(
        self, table: str, *, limit: int, offset: int, query: RowQuery | None = None, count: bool = True
    ) -> RowPage:
        """见 :meth:`DatabaseSource.rows`：条件、搜索与排序都交给 ``db rows``。"""
        self.calls["rows"] += 1
        condition = query or RowQuery()
        args = ["rows", table, "--limit", str(limit), "--offset", str(offset)]
        for item in condition.filters:
            args += ["--filter", item]
        if condition.search:
            args += ["--search", condition.search]
        if condition.order_by:
            args += ["--order-by", condition.order_by]
        if not count:
            args += ["--no-count"]
        return normalize_page(self._invoke(*args), table)

    def set_values(self, table: str, key: str, values: Mapping[str, str]) -> WriteResult:
        """见 :meth:`DatabaseSource.set_values`：一行一次 CLI 调用，各列经重复的 ``--set`` 下发。"""
        self.calls["set"] += 1
        args = ["set", table, "--key", key]
        for column, value in values.items():
            args.extend(["--set", f"{column}={value}"])
        return self._write(*args)

    def insert_row(self, table: str, values: Mapping[str, str]) -> WriteResult:
        """见 :meth:`DatabaseSource.insert_row`。"""
        self.calls["insert"] += 1
        args = ["insert", table]
        for column, value in values.items():
            args.extend(["--set", f"{column}={value}"])
        return self._write(*args)

    def delete_row(self, table: str, key: str) -> WriteResult:
        """删除数据项，使用 ``--yes`` 传递界面的确认结果。"""
        self.calls["delete"] += 1
        return self._write("delete", table, "--key", key, "--yes")

    def _write(self, *args: str) -> WriteResult:
        # 分别报告执行失败和输出解析失败，便于定位错误。
        try:
            payload = self._invoke(*args)
        except DatabaseSourceError as error:
            return WriteResult(False, str(error), "")
        if not isinstance(payload, Mapping):
            return WriteResult(False, i18n.t("cli.tui.database.err_bad_payload"), _tail(str(payload)))
        message = str(payload.get("error") or "")
        if message:
            return WriteResult(False, message, "")
        return WriteResult(True, i18n.t("cli.tui.database.write_ok", table=str(payload.get("table") or "")), "")

    def _invoke(self, *args: str) -> Any:
        argv = cli_process.cli_argv("db", *args, "--json")
        try:
            completed = self._runner(
                argv,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=cli_process.cli_env(self.root),
            )
        except subprocess.TimeoutExpired as error:
            raise DatabaseSourceError(
                i18n.t("cli.tui.database.err_timeout", cmd=" ".join(args), seconds=f"{self.timeout:g}")
            ) from error
        except OSError as error:
            raise DatabaseSourceError(i18n.t("cli.tui.database.err_exec", cmd=" ".join(args), error=error)) from error
        stdout = (completed.stdout or "").strip()
        payload = _parse_json(stdout)
        if completed.returncode != 0:
            reason = str(payload.get("error") or "") if isinstance(payload, Mapping) else ""
            detail = reason or _tail(completed.stderr) or _tail(stdout)
            raise DatabaseSourceError(
                i18n.t("cli.tui.common.error_separator").join(
                    [
                        i18n.t("cli.tui.database.err_exit", cmd=" ".join(args), code=completed.returncode),
                        detail,
                    ]
                )
            )
        if payload is None:
            # 解析失败时保留原始输出，供调用方诊断。
            raise DatabaseSourceError(
                i18n.t("cli.tui.common.error_separator").join(
                    [i18n.t("cli.tui.database.err_bad_json", cmd=" ".join(args)), _tail(stdout)]
                )
            )
        return payload


def _parse_json(text: str) -> Any:
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _tail(text: str | None, limit: int = STATUS_TAIL_LIMIT) -> str:
    return (text or "").strip()[-limit:]


def _static_text(widget: compat.Static) -> str:
    # 通过公开的 render() 读取文本，避免依赖 Textual 的内部属性。
    return str(widget.render())


class EditorField(compat.Vertical):
    """编辑区中的一列：字段名标签与非主键输入框。

    :param column: 列信息。
    """

    def __init__(self, column: ColumnInfo, *, id: str | None = None) -> None:
        super().__init__(id=id)
        self.column = column
        self.initial = ""
        self.hint = ""

    def compose(self) -> compat.ComposeResult:
        """装配标签与输入框。"""
        yield compat.Static(compat.plain_text(self.column.label), classes="editor-label", markup=False)
        yield compat.Input(self.initial, placeholder=self.hint, classes="editor-input")

    @property
    def value(self) -> str:
        """返回输入框中的当前文本。"""
        return self.query_one(compat.Input).value

    def set_value(self, text: str) -> None:
        """设置输入框文本，等价于用户键入。"""
        self.query_one(compat.Input).value = text


class DatabasePage(compat.Vertical):
    """数据库页控件。

    :param source: 数据源，默认为 :class:`SubprocessDatabaseSource`。
    :param cache_ttl: 表清单缓存有效期秒数；重新读取与写入成功后立即失效。
    """

    DEFAULT_CSS = """
    DatabasePage {
        layout: vertical;
        height: 1fr;
    }
    DatabasePage #database-body {
        height: 1fr;
    }
    DatabasePage #tables-pane {
        width: 26;
        min-width: 20;
    }
    DatabasePage #database-search {
        height: 3;
    }
    DatabasePage #table-list {
        height: 1fr;
        border: round $primary;
    }
    DatabasePage #table-list > ListItem {
        padding: 0 1;
    }
    DatabasePage #table-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #rows-pane {
        width: 1fr;
        min-width: 24;
        height: 1fr;
    }
    DatabasePage #rows-caption {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #filter-bar {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #row-list {
        height: 1fr;
        border: round $panel;
    }
    DatabasePage #pager {
        height: 3;
    }
    DatabasePage #pager Button {
        width: 1fr;
        min-width: 0;
    }
    DatabasePage #row-list > ListItem {
        padding: 0 1;
    }
    DatabasePage #row-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #editor-pane {
        width: 34;
        min-width: 24;
        border: round $primary;
        padding: 0 1;
    }
    DatabasePage #editor-caption {
        height: auto;
        text-style: bold;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #editor-pk-row {
        height: auto;
    }
    DatabasePage #editor-pk-input {
        display: none;
        width: 1fr;
    }
    DatabasePage #editor-pk {
        height: auto;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #editor-fields {
        height: 1fr;
    }
    DatabasePage EditorField {
        height: auto;
        margin: 0 0 1 0;
    }
    DatabasePage .editor-label {
        height: auto;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage .editor-input {
        width: 1fr;
    }
    DatabasePage #editor-actions {
        height: 3;
    }
    DatabasePage #editor-actions Button {
        width: 1fr;
        min-width: 0;
    }
    DatabasePage #database-status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #database-body.narrow {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
    }
    DatabasePage #database-body.narrow #tables-pane {
        width: 100%;
        height: 100%;
        min-width: 0;
    }
    DatabasePage #database-body.narrow #rows-pane {
        width: 100%;
        height: 100%;
        min-width: 0;
    }
    DatabasePage #database-body.narrow #editor-pane {
        column-span: 2;
        width: 100%;
        height: 100%;
        min-width: 0;
    }
    DatabasePage #database-body.narrow #rows-caption, DatabasePage #database-body.narrow #filter-bar {
        height: 1;
    }
    DatabasePage #database-body.narrow #pager {
        height: 1;
    }
    DatabasePage #database-body.narrow #pager Button {
        height: 1;
        border: none;
    }
    /* 窄屏保留前后翻页按钮；首末页通过 g / G 跳转。 */
    DatabasePage #database-body.narrow #db-first-page, DatabasePage #database-body.narrow #db-last-page {
        display: none;
    }
    """

    can_focus = True

    # 删除使用组合键；分页与筛选键位由页内控件提示，为全局键位保留页脚空间。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.database.bind_refresh")),
        ("s", "save", i18n.t("cli.tui.database.bind_save")),
        ("i", "insert", i18n.t("cli.tui.database.bind_insert"), False),
        ("ctrl+d", "delete", i18n.t("cli.tui.database.bind_delete"), False),
        ("slash", "focus_search", i18n.t("cli.tui.database.bind_search")),
        ("f", "add_filter", i18n.t("cli.tui.database.bind_filter"), False),
        ("escape", "cancel", i18n.t("cli.tui.database.bind_cancel"), False),
        ("o", "set_order", i18n.t("cli.tui.database.bind_order"), False),
        ("ctrl+f", "clear_filters", i18n.t("cli.tui.database.bind_clear_filters"), False),
        ("n", "next_page", i18n.t("cli.tui.database.bind_next_page"), False),
        ("p", "previous_page", i18n.t("cli.tui.database.bind_previous_page"), False),
        ("g", "first_page", i18n.t("cli.tui.database.bind_first_page"), False),
        ("G", "last_page", i18n.t("cli.tui.database.bind_last_page"), False),
    )

    def __init__(
        self,
        source: DatabaseSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DatabaseSource = source if source is not None else SubprocessDatabaseSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = i18n.t("cli.tui.common.status_ready")
        self._tables: tuple[TableInfo, ...] = ()
        self._query = ""
        self._selected: str | None = None
        self._page = RowPage()
        self._offset = 0
        self._row_query = RowQuery()
        self._row_index: int | None = None
        self._row_key: str = ""
        self._original: dict[str, Any] = {}
        self._insert_mode = False
        self._pending: WritePlan | None = None
        self._gate = compat.PendingConfirm()
        self._busy = False
        self._loaded_at = 0.0
        self._table_rows: tuple[str, ...] = ()
        self._row_texts: tuple[str, ...] = ()
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：表清单、数据项、编辑区与状态栏。"""
        with compat.Horizontal(id="database-body"):
            with compat.Vertical(id="tables-pane"):
                yield compat.Input(placeholder=i18n.t("cli.tui.database.search_placeholder"), id="database-search")
                yield compat.ListView(id="table-list")
            with compat.Vertical(id="rows-pane"):
                yield compat.Static(
                    compat.plain_text(i18n.t("cli.tui.database.rows_caption_empty")), id="rows-caption", markup=False
                )
                yield compat.Static(
                    compat.plain_text(i18n.t("cli.tui.database.filter_none")), id="filter-bar", markup=False
                )
                yield compat.ListView(id="row-list")
                with compat.Horizontal(id="pager"):
                    yield compat.Button(i18n.t("cli.tui.database.button_first_page"), id="db-first-page")
                    yield compat.Button(i18n.t("cli.tui.database.button_previous_page"), id="db-previous-page")
                    yield compat.Button(i18n.t("cli.tui.database.button_next_page"), id="db-next-page")
                    yield compat.Button(i18n.t("cli.tui.database.button_last_page"), id="db-last-page")
            with compat.Vertical(id="editor-pane"):
                yield compat.Static(
                    compat.plain_text(i18n.t("cli.tui.database.editor_caption_empty")),
                    id="editor-caption",
                    markup=False,
                )
                with compat.Horizontal(id="editor-pk-row"):
                    yield compat.Static(
                        compat.plain_text(i18n.t("cli.tui.database.editor_pk_empty")), id="editor-pk", markup=False
                    )
                    yield compat.Input(
                        placeholder=i18n.t("cli.tui.database.editor_pk_placeholder"), id="editor-pk-input"
                    )
                # 字段单独放进滚动容器：字段多时只有它滚动，编辑区底部的按钮始终留在原地。
                yield compat.VerticalScroll(id="editor-fields")
                with compat.Horizontal(id="editor-actions"):
                    yield compat.Button(i18n.t("cli.tui.database.button_save"), id="db-save", variant="success")
                    yield compat.Button(i18n.t("cli.tui.database.button_insert"), id="db-insert")
                    yield compat.Button(i18n.t("cli.tui.database.button_delete"), id="db-delete", variant="warning")
                    yield compat.Button(i18n.t("cli.tui.database.button_refresh"), id="db-refresh")
        yield compat.Static(
            compat.plain_text(i18n.t("cli.tui.common.status_ready")), id="database-status", markup=False
        )

    def on_mount(self) -> None:
        """挂载后只装配控件；读取数据推迟到首次显示。"""
        compat.set_text_selection(self, False)
        self._sync_layout(self.size.width)
        # 加载前禁用不可用的分页操作，避免首帧出现无效按钮。
        self._sync_pager()

    def _sync_layout(self, width: int) -> None:
        # 切换的是容器上的类，三栏的构成与控件 id 都不变；并排所需宽度见 SIDE_BY_SIDE_MIN_WIDTH。
        if width <= 0:
            return
        body = self.query_one("#database-body", compat.Horizontal)
        body.set_class(width < SIDE_BY_SIDE_MIN_WIDTH, "narrow")

    def activate(self) -> None:
        """首次显示时读取表清单。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_tables(force=True)

    def focus_primary(self) -> None:
        """聚焦表清单；列表为空时聚焦页面容器，保持页面键位可用。"""
        compat.focus_first(self, "#table-list")

    def _adopt_focus(self) -> None:
        # 列表加载后仅在焦点仍位于页面容器时恢复列表焦点，避免中断用户输入。
        if self.display and getattr(self.app, "focused", None) is self:
            compat.focus_first(self, "#table-list")

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)

    # region 状态读取（供测试与 App 使用）

    @property
    def tables(self) -> tuple[TableInfo, ...]:
        """返回缓存中的表清单，不触发子进程。"""
        return self._tables

    @property
    def visible_tables(self) -> tuple[TableInfo, ...]:
        """返回应用当前搜索词后的表清单。"""
        if not self._query.strip():
            return self._tables
        needle = self._query.strip().casefold()
        return tuple(table for table in self._tables if needle in table.name.casefold())

    @property
    def selected_table(self) -> str | None:
        """返回当前表名。"""
        return self._selected

    @property
    def selected_info(self) -> TableInfo | None:
        """返回当前表的表信息。"""
        for table in self._tables:
            if table.name == self._selected:
                return table
        return None

    @property
    def page(self) -> RowPage:
        """返回最近一次读取的数据项，不触发子进程。"""
        return self._page

    @property
    def row_query(self) -> RowQuery:
        """返回当前生效的筛选条件与搜索词。"""
        # 名称需避免覆盖 Textual 的 Widget.query()。
        return self._row_query

    @property
    def offset(self) -> int:
        """返回当前页的起始偏移。"""
        return self._offset

    @property
    def insert_mode(self) -> bool:
        """返回是否处于新建模式。"""
        return self._insert_mode

    @property
    def selected_key(self) -> str:
        """返回当前数据项的主键值文本；未选中时为空串。"""
        return self._row_key

    @property
    def pending(self) -> WritePlan | None:
        """返回待确认的写入计划，没有待确认时为空。"""
        return self._pending

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    def table_row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的表清单行文本。"""
        return self._table_rows

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的数据项行文本。"""
        return self._row_texts

    def editor(self) -> tuple[EditorField, ...]:
        """返回编辑区中的字段控件。"""
        return tuple(self.query(EditorField))

    def editor_values(self) -> dict[str, str]:
        """返回编辑区各列的当前文本。"""
        return {field.column.name: field.value for field in self.editor()}

    def set_editor_value(self, column: str, text: str) -> None:
        """设置某一列的编辑文本，等价于用户键入。"""
        for field in self.editor():
            if field.column.name == column:
                field.set_value(text)
                return

    def set_query(self, value: str) -> None:
        """设置表名搜索词，等价于用户键入。"""
        self.query_one("#database-search", compat.Input).value = value

    def caption_text(self) -> str:
        """返回数据项列表上方的摘要文本。"""
        return _static_text(self.query_one("#rows-caption", compat.Static))

    def filter_text(self) -> str:
        """返回条件行的当前文本。"""
        return _static_text(self.query_one("#filter-bar", compat.Static))

    def pager_states(self) -> dict[str, bool]:
        """返回四个翻页按钮的禁用状态，供自动化断言。"""
        return {button_id: bool(self.query_one(f"#{button_id}", compat.Button).disabled) for button_id in PAGER_BUTTONS}

    def editor_caption(self) -> str:
        """返回编辑区上方的摘要文本。"""
        return _static_text(self.query_one("#editor-caption", compat.Static))

    def pk_text(self) -> str:
        """返回主键的只读展示文本。"""
        return _static_text(self.query_one("#editor-pk", compat.Static))

    # endregion

    # region 读取与渲染

    def refresh_tables(self, *, force: bool = False) -> None:
        """读取表清单。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不读取数据。
        """
        if not force and self._tables and self.cache_age() < self.cache_ttl:
            self._render_tables()
            self._set_status(i18n.t("cli.tui.database.status_cached", count=len(self._tables)))
            return
        self._set_status(i18n.t("cli.tui.database.status_loading"))
        self.run_worker(self.reload_tables(), group="database-tables", exclusive=True)

    def cache_age(self) -> float:
        """返回表清单缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    async def reload_tables(self) -> bool:
        """后台读取表清单并载入当前表，返回是否成功。"""
        try:
            tables = await asyncio.to_thread(self.source.tables)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._tables = ()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_tables()
            await self._clear_rows(i18n.t("cli.tui.database.rows_load_failed", error=error))
            self._set_status(
                i18n.t("cli.tui.common.error_separator").join(
                    [i18n.t("cli.tui.database.status_load_failed"), self.last_error]
                )
            )
            return False
        self._tables = tuple(tables)
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = i18n.t("cli.tui.database.status_loaded", count=len(self._tables))
        self._render_tables()
        target = self._selected if any(table.name == self._selected for table in self._tables) else None
        if target is None and self.visible_tables:
            target = self.visible_tables[0].name
        if target is None:
            self._selected = None
            await self._clear_rows(i18n.t("cli.tui.database.rows_no_table"))
            self._set_status(i18n.t("cli.tui.database.status_no_tables"))
            return True
        await self.select_table(target)
        return True

    async def select_table(self, table: str | None, *, force: bool = False) -> bool:
        """切换当前表并加载第一页数据项。

        :param table: 目标表名；``None`` 表示清空。
        :param force: 为 ``True`` 时忽略缓存重新读取。
        :return: 是否成功。
        """
        if table is None:
            self._selected = None
            await self._clear_rows(i18n.t("cli.tui.database.rows_no_table"))
            self._set_status(i18n.t("cli.tui.database.status_no_tables"))
            return False
        if table != self._selected:
            # 筛选列属于当前表，切换表时清空条件，避免引用不存在的列。
            self._row_query = RowQuery()
        self._selected = table
        info = self.selected_info
        if info is None:
            self._set_status(i18n.t("cli.tui.database.status_unknown_table", table=table))
            return False
        await self._rebuild_editor(info)
        self._insert_mode = False
        self.reset_pending()
        ok = await self.reload_rows(reset_offset=True)
        if ok:
            self._set_status(i18n.t("cli.tui.database.status_table_loaded", table=table, rows=self._page.rows_total))
        return ok

    async def reload_rows(self, *, reset_offset: bool = False, count: bool | None = None) -> bool:
        """读取当前表的数据项并重绘列表。

        :param reset_offset: 为 ``True`` 时恢复为第一页。
        :param count: 是否重算总条数；``None`` 表示按需决定（换页不数，其余都数）。
        :return: 是否成功。
        """
        if self._selected is None:
            return False
        offset = 0 if reset_offset else self._offset
        # 翻页复用记录总数，避免对大表重复执行全表统计。
        if count is None:
            count = reset_offset or self._page.total is None
        try:
            page = await asyncio.to_thread(
                self.source.rows,
                self._selected,
                limit=PAGE_LIMIT,
                offset=offset,
                query=self._row_query,
                count=count,
            )
        except Exception as error:  # noqa: BLE001 - 读取数据失败只影响本页展示
            self.last_error = f"{type(error).__name__}: {error}"
            await self._clear_rows(i18n.t("cli.tui.database.rows_load_failed", error=error))
            self._set_status(
                i18n.t("cli.tui.common.error_separator").join(
                    [i18n.t("cli.tui.database.status_rows_failed", table=self._selected), self.last_error]
                )
            )
            return False
        if page.total is None:
            # 未重新统计时保留总数，用于页码和末页定位。
            page = replace(page, total=self._page.total)
        self._page = page
        # 记录减少可能使偏移超出末页，修正偏移以避免空白页。
        if page.rows_total and offset > page.last_offset:
            self._offset = page.last_offset
            return await self.reload_rows()
        self._offset = offset
        self.last_error = ""
        self._render_rows()
        self._select_row(0 if reset_offset else self._row_index)
        return True

    async def _clear_rows(self, hint: str) -> None:
        self._page = RowPage(table=self._selected or "", limit=PAGE_LIMIT)
        self._row_index = None
        self._row_key = ""
        self._original = {}
        list_view = self.query_one("#row-list", compat.ListView)
        list_view.clear()
        self._row_texts = ()
        self.query_one("#rows-caption", compat.Static).update(compat.plain_text(hint))
        self._sync_pager()
        await self._clear_editor()

    async def _clear_editor(self) -> None:
        pane = self.query_one("#editor-fields", compat.VerticalScroll)
        await pane.remove_children()
        self.query_one("#editor-pk", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.database.editor_pk_empty"))
        )
        self.query_one("#editor-caption", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.database.editor_caption_empty"))
        )

    async def _rebuild_editor(self, info: TableInfo) -> None:
        pane = self.query_one("#editor-fields", compat.VerticalScroll)
        await pane.remove_children()
        fields = [EditorField(column, id=f"editor-{column.name}") for column in info.editable_columns()]
        if fields:
            await pane.mount(*fields)
            return
        await pane.mount(compat.Static(compat.plain_text(i18n.t("cli.tui.database.editor_no_fields")), markup=False))

    def _select_row(self, index: int | None) -> None:
        rows = self._page.rows
        if index is None or index < 0 or index >= len(rows):
            self._row_index = None
            self._row_key = ""
            self._original = {}
            self._sync_editor()
            return
        self._row_index = index
        self._original = dict(rows[index])
        info = self.selected_info
        self._row_key = _text(self._original.get(info.pk_name)) if info is not None else ""
        self._sync_editor()

    def _sync_editor(self) -> None:
        # 编辑区只读缓存中的数据项：渲染路径不得起子进程。
        info = self.selected_info
        if info is None:
            return
        if self._insert_mode:
            # 新建时允许输入主键，以支持 module_status.module_name 等非自增主键。
            self._row_key = ""
            self._original = {}
            for field_ in self.editor():
                field_.set_value("")
            self.query_one("#editor-pk", compat.Static).display = False
            pk_input = self.query_one("#editor-pk-input", compat.Input)
            pk_input.display = True
            pk_input.value = ""
            self.query_one("#editor-caption", compat.Static).update(
                compat.plain_text(i18n.t("cli.tui.database.editor_caption_insert", table=info.name))
            )
            return
        self.query_one("#editor-pk-input", compat.Input).display = False
        self.query_one("#editor-pk", compat.Static).display = True
        for field_ in self.editor():
            field_.set_value(_text(self._original.get(field_.column.name)))
        caption = (
            i18n.t("cli.tui.database.editor_caption_edit", table=info.name, pk=info.pk_name, value=self._row_key)
            if self._row_index is not None
            else i18n.t("cli.tui.database.editor_caption_no_row", table=info.name)
        )
        self.query_one("#editor-caption", compat.Static).update(compat.plain_text(caption))
        self.query_one("#editor-pk", compat.Static).update(
            compat.plain_text(
                i18n.t("cli.tui.database.editor_pk_edit", column=info.pk_name, pk=self._row_key)
                if self._row_index is not None
                else i18n.t("cli.tui.database.editor_pk_empty")
            )
        )

    def _render_tables(self) -> None:
        if not compat.mounted(self):
            return
        list_view = self.query_one("#table-list", compat.ListView)
        width = self._list_width(list_view)
        rows = tuple(
            compat.fit_cells(f"{table.name}（{table.rows if table.rows is not None else '-'}）", width)
            for table in self.visible_tables
        )
        compat.rebuild_rows(list_view, rows, self._table_index())
        self._table_rows = rows
        self._adopt_focus()

    def _render_rows(self) -> None:
        if not compat.mounted(self):
            return
        info = self.selected_info
        list_view = self.query_one("#row-list", compat.ListView)
        width = self._list_width(list_view)
        separator = i18n.t("cli.tui.common.list_separator")
        rows: list[str] = []
        if info is not None:
            for row in self._page.rows:
                summary = separator.join(f"{name}={_text(value)}" for name, value in row.items())
                rows.append(compat.fit_cells(summary, width))
        index = self._row_index if self._row_index is not None and self._row_index < len(rows) else 0
        compat.rebuild_rows(list_view, rows, index if rows else None)
        self._row_texts = tuple(rows)
        caption = (
            i18n.t(
                "cli.tui.database.rows_caption",
                table=info.name,
                total=self._page.rows_total,
                count=len(rows),
                page=self._page.page_number,
                pages=self._page.pages,
            )
            if info is not None
            else i18n.t("cli.tui.database.rows_caption_empty")
        )
        self.query_one("#rows-caption", compat.Static).update(compat.plain_text(caption))
        filters = self._filter_text()
        self.query_one("#filter-bar", compat.Static).update(compat.plain_text(filters))
        self._sync_pager()

    def _filter_text(self) -> str:
        if self._row_query.is_empty():
            line = i18n.t("cli.tui.database.filter_none")
        else:
            line = i18n.t("cli.tui.database.filter_line", conditions=self._row_query.summary())
        return i18n.t("cli.tui.database.filter_with_order", line=line, order=self.sort_text())

    def sort_text(self) -> str:
        """返回当前排序的展示文本。"""
        return self._row_query.order_by or i18n.t("cli.tui.database.order_default", column=self._default_order_label())

    def _sync_pager(self) -> None:
        # 首末页禁用对应的翻页操作，避免进入空白页。
        page = self._page
        first = page.offset <= 0
        last = page.offset >= page.last_offset
        # 后台读取可能在页面卸载后完成，此时跳过控件更新。
        if not compat.mounted(self):
            return
        buttons = {name: self.query_one(f"#{name}", compat.Button) for name in PAGER_BUTTONS}
        for button_id, disabled in (
            ("db-first-page", first),
            ("db-previous-page", first),
            ("db-next-page", last),
            ("db-last-page", last),
        ):
            buttons[button_id].disabled = disabled or self._selected is None

    def action_add_filter(self) -> None:
        """键位动作：添加筛选条件或搜索词。"""
        if self._selected is None:
            self._set_status(i18n.t("cli.tui.database.status_no_tables"))
            return
        info = self.selected_info
        columns = i18n.t("cli.common.list_separator").join(column.name for column in (info.columns if info else ()))
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.database.filter_title", table=self._selected),
            hint=i18n.t("cli.tui.database.filter_hint", columns=columns),
            placeholder=i18n.t("cli.tui.database.filter_placeholder"),
            confirm_label=i18n.t("cli.tui.database.filter_confirm"),
            cancel_label=i18n.t("cli.tui.database.cancel"),
            callback=self.on_filter_entered,
        )

    def on_filter_entered(self, text: str | None) -> None:
        """输入框回调：带运算符的按条件下发，只写一个词的按全表搜索下发。

        :param text: 用户输入的文本；取消时为 ``None``。
        """
        value = (text or "").strip()
        if not value:
            self._set_status(i18n.t("cli.tui.database.filter_cancelled"))
            return
        if is_condition(value):
            self._row_query = self._row_query.with_filter(value)
            message = i18n.t("cli.tui.database.status_filter_added", condition=value)
        else:
            self._row_query = self._row_query.with_search(value)
            message = i18n.t("cli.tui.database.status_search_set", keyword=value)
        self._set_status(message)
        self.refresh_rows(reset_offset=True)

    def action_clear_filters(self) -> None:
        """键位动作：清空全部条件与搜索词。"""
        if self._row_query.is_empty():
            self._set_status(i18n.t("cli.tui.database.filter_none"))
            return
        # 清空筛选条件不影响排序。
        self._row_query = RowQuery(order_by=self._row_query.order_by)
        self._set_status(i18n.t("cli.tui.database.status_filters_cleared"))
        self.refresh_rows(reset_offset=True)

    def action_set_order(self) -> None:
        """键位动作：改排序方式。"""
        if self._selected is None:
            self._set_status(i18n.t("cli.tui.database.status_no_tables"))
            return
        info = self.selected_info
        columns = i18n.t("cli.common.list_separator").join(column.name for column in (info.columns if info else ()))
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.database.order_title", table=self._selected),
            hint=i18n.t("cli.tui.database.order_hint", columns=columns),
            placeholder=i18n.t("cli.tui.database.order_placeholder"),
            initial=self._row_query.order_by,
            confirm_label=i18n.t("cli.tui.database.order_confirm"),
            cancel_label=i18n.t("cli.tui.database.cancel"),
            callback=self.on_order_entered,
        )

    def on_order_entered(self, text: str | None) -> None:
        """输入框回调：设定排序；空输入恢复为默认（主键倒序）。

        :param text: 用户输入的排序方式；取消时为 ``None``。
        """
        if text is None:
            self._set_status(i18n.t("cli.tui.database.order_cancelled"))
            return
        value = text.strip()
        self._row_query = replace(self._row_query, order_by=value)
        self._set_status(
            i18n.t("cli.tui.database.status_order_set", order=self.sort_text())
            if value
            else i18n.t("cli.tui.database.status_order_reset")
        )
        self.refresh_rows(reset_offset=True)

    def _default_order_label(self) -> str:
        info = self.selected_info
        return f"-{info.pk_name}" if info is not None and info.pk_name else "-"

    def refresh_rows(self, *, reset_offset: bool = False) -> None:
        """按当前条件重新加载数据项。

        :param reset_offset: 为 ``True`` 时恢复为第一页。
        """
        self.run_worker(self.reload_rows(reset_offset=reset_offset), group="database-rows", exclusive=True)

    def action_next_page(self) -> None:
        """键位动作：下一页。"""
        self.goto_offset(self._page.offset + PAGE_LIMIT)

    def action_previous_page(self) -> None:
        """键位动作：上一页。"""
        self.goto_offset(self._page.offset - PAGE_LIMIT)

    def action_first_page(self) -> None:
        """键位动作：第一页。"""
        self.goto_offset(0)

    def action_last_page(self) -> None:
        """键位动作：最后一页。"""
        self.goto_offset(self._page.last_offset)

    def goto_offset(self, offset: int) -> None:
        """跳到指定偏移所在的那一页。

        :param offset: 目标偏移，会被夹到 ``0`` 与末页之间。
        """
        if self._selected is None:
            self._set_status(i18n.t("cli.tui.database.status_no_tables"))
            return
        bounded = max(0, min(offset, self._page.last_offset))
        if bounded == self._page.offset:
            self._set_status(
                i18n.t("cli.tui.database.status_page_same", page=self._page.page_number, pages=self._page.pages)
            )
            return
        self._set_status(i18n.t("cli.tui.database.status_page_loading"))
        self.run_worker(self._goto_offset(bounded), group="database-rows", exclusive=True)

    async def _goto_offset(self, offset: int) -> None:
        self._offset = offset
        if await self.reload_rows():
            self._set_status(
                i18n.t("cli.tui.database.status_page_loaded", page=self._page.page_number, pages=self._page.pages)
            )

    def _list_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 40
        return max(outer - 4, 8)

    def _table_index(self) -> int:
        if self._selected is not None:
            for index, table in enumerate(self.visible_tables):
                if table.name == self._selected:
                    return index
        return 0

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        if not compat.mounted(self):
            return
        self.query_one("#database-status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时切换布局并按缓存重排，不重新读取数据。"""
        self._sync_layout(event.size.width)
        if self._tables:
            self._render_tables()
        if self._page.rows:
            self._render_rows()

    # endregion

    # region 写入

    def action_refresh(self) -> None:
        """键位动作：作废缓存并重新读取表与数据项。"""
        self.reset_pending()
        self.refresh_tables(force=True)

    def action_save(self) -> None:
        """键位动作：保存编辑区的更改；新建模式下等价于写入新数据项。"""
        self.request_save()

    def action_insert(self) -> None:
        """键位动作：进入新建模式或写入新数据项。"""
        self.request_insert()

    def action_delete(self) -> None:
        """键位动作：删除当前数据项。"""
        self.request_delete()

    def action_cancel(self) -> None:
        """键位动作：退出新建模式并清空待确认状态；焦点在搜索框时先清空搜索。"""
        search = self.query_one("#database-search", compat.Input)
        if getattr(self.app, "focused", None) is search:
            if search.value:
                search.value = ""
                return
            compat.focus_first(self, "#table-list")
            return
        self.cancel_edit()

    def action_focus_search(self) -> None:
        """键位动作：聚焦搜索框。"""
        self.query_one("#database-search", compat.Input).focus()

    def request_save(self) -> None:
        """通过模态框确认并保存编辑区的更改。"""
        info = self.selected_info
        if info is None or self._insert_mode:
            self.request_insert()
            return
        if self._row_index is None:
            self._set_status(i18n.t("cli.tui.database.status_no_row"))
            return
        changes = tuple(
            (name, _text(self._original.get(name)), _text(value))
            for name, value in self.editor_values().items()
            if _text(value) != _text(self._original.get(name))
        )
        if not changes:
            self._pending = None
            self._set_status(i18n.t("cli.tui.database.status_no_changes", table=info.name, pk=info.pk_name))
            return
        self._request(WritePlan(kind="set", table=info.name, key=self._row_key, changes=changes))

    def request_insert(self) -> None:
        """进入新建模式；已处于新建模式时打开写入确认框。"""
        info = self.selected_info
        if info is None:
            self._set_status(i18n.t("cli.tui.database.status_no_table"))
            return
        if not self._insert_mode:
            self._insert_mode = True
            self._pending = None
            self._sync_editor()
            self._set_status(i18n.t("cli.tui.database.status_insert_mode", table=info.name))
            return
        values = [(name, text) for name, text in self.editor_values().items() if text != ""]
        pk_input = self.query_one("#editor-pk-input", compat.Input).value.strip()
        if pk_input and info.pk_name and all(name != info.pk_name for name, _ in values):
            values.insert(0, (info.pk_name, pk_input))
        self._request(WritePlan(kind="insert", table=info.name, values=tuple(values)))

    def request_delete(self) -> None:
        """通过模态框确认并删除当前数据项。"""
        info = self.selected_info
        if info is None or self._row_index is None or not self._row_key:
            self._set_status(i18n.t("cli.tui.database.status_no_row"))
            return
        self._request(WritePlan(kind="delete", table=info.name, key=self._row_key))

    def reset_pending(self) -> None:
        """作废待确认的写入；切页、刷新、换表与换行时调用。"""
        self._gate.reset()
        self._pending = None

    def dirty_note(self) -> str:
        """返回未保存更改的说明；没有更改时返回空字符串。"""
        if self._insert_mode:
            filled = [name for name, text in self.editor_values().items() if text != ""]
            if filled:
                return i18n.t("cli.tui.database.dirty_insert", count=len(filled))
            return ""
        if self._row_index is None:
            return ""
        changed = [
            name for name, value in self.editor_values().items() if _text(value) != _text(self._original.get(name))
        ]
        if not changed:
            return ""
        return i18n.t("cli.tui.database.dirty_edit", count=len(changed), pk=self._row_key)

    def cancel_edit(self) -> None:
        """退出新建模式、清空待确认状态并把编辑区还原为当前数据项。"""
        cancelled = self._pending is not None or self._insert_mode
        self._pending = None
        self._gate.reset()
        self._insert_mode = False
        self._sync_editor()
        self._set_status(
            i18n.t("cli.tui.database.status_cancelled") if cancelled else i18n.t("cli.tui.database.status_ready")
        )

    def _request(self, plan: WritePlan) -> None:
        # 写入前通过模态框展示操作范围，并防止连续触发重复确认。
        if self._busy:
            self._set_status(i18n.t("cli.tui.common.busy_title"))
            return
        if not self._gate.accept(f"{plan.kind}:{plan.table}:{plan.key}"):
            return
        self._pending = plan
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.database.write_title", table=plan.table),
            hint=plan.summary(),
            options=(("write", i18n.t("cli.tui.database.write_confirm")),),
            cancel_label=i18n.t("cli.tui.database.cancel"),
            callback=lambda choice, target=plan: self.start_write(target, choice),
        )

    def start_write(self, plan: WritePlan, choice: str | None) -> None:
        """按确认结果执行写入。

        :param plan: 待写入的计划。
        :param choice: ``write`` 表示确认，``None`` 表示取消。
        """
        self._pending = None
        if choice != "write":
            self._set_status(i18n.t("cli.tui.database.write_cancelled"))
            return
        self._set_status(i18n.t("cli.tui.database.status_writing", table=plan.table))
        self.run_worker(self._apply(plan), group="database-write", exclusive=True)

    async def _apply(self, plan: WritePlan) -> bool:
        self._busy = True
        try:
            results = await self._dispatch(plan)
        finally:
            self._busy = False
        failures = [result for result in results if not result.ok]
        if failures:
            first = failures[0]
            self.last_error = first.detail or first.message
            tail = first.detail.splitlines()[-1] if first.detail else i18n.t("cli.tui.common.no_output")
            # 原因与输出尾部是 CLI 给出的可变文本，按分隔符拼接而不是写进模板。
            self._set_status(
                i18n.t("cli.tui.common.error_separator").join(
                    [i18n.t("cli.tui.database.status_write_failed", table=plan.table), first.message, tail]
                )
            )
            compat.notify(self.app, first.message, severity="error", title=plan.table)
            return False
        self._insert_mode = False
        await self.reload_tables_after_write(plan)
        self._set_status(
            i18n.t("cli.tui.database.status_written", count=len(results), table=plan.table, action=plan.kind)
        )
        compat.notify(
            self.app,
            i18n.t("cli.tui.database.status_written", count=len(results), table=plan.table, action=plan.kind),
            severity="information",
            title=plan.table,
        )
        return True

    async def _dispatch(self, plan: WritePlan) -> list[WriteResult]:
        try:
            if plan.kind == "set":
                # 同一数据项的多列更改通过一次 UPDATE 写入，避免部分列更新。
                changed = {column: after for column, _, after in plan.changes}
                return [await asyncio.to_thread(self.source.set_values, plan.table, plan.key, changed)]
            if plan.kind == "insert":
                result = await asyncio.to_thread(self.source.insert_row, plan.table, dict(plan.values))
                return [result]
            result = await asyncio.to_thread(self.source.delete_row, plan.table, plan.key)
            return [result]
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成失败项展示
            return [WriteResult(False, f"{type(error).__name__}: {error}", "")]

    async def reload_tables_after_write(self, plan: WritePlan) -> None:
        """写入后重新加载数据项和记录总数；编辑与删除保留当前页，新建返回第一页。"""
        previous = self._row_key
        self._loaded_at = 0.0
        await self.reload_rows(reset_offset=plan.kind == "insert", count=True)
        if plan.kind == "delete" or previous == self._row_key:
            return
        for index, row in enumerate(self._page.rows):
            info = self.selected_info
            if info is not None and _text(row.get(info.pk_name)) == previous:
                self._select_row(index)
                return

    # endregion

    # region 交互

    @compat.on(compat.Input.Changed, "#database-search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        self._query = event.value
        self._render_tables()

    @compat.on(compat.ListView.Highlighted, "#table-list")
    def _on_table_highlighted(self, event: compat.ListView.Highlighted) -> None:
        index = compat.highlighted_index(self.query_one("#table-list", compat.ListView))
        visible = self.visible_tables
        if index is None or index >= len(visible):
            return
        table = visible[index].name
        if table != self._selected:
            self._pending = None
            self.run_worker(self.select_table(table), group="database-select", exclusive=True)

    @compat.on(compat.ListView.Highlighted, "#row-list")
    def _on_row_highlighted(self, event: compat.ListView.Highlighted) -> None:
        index = compat.highlighted_index(self.query_one("#row-list", compat.ListView))
        if index is None or index >= len(self._page.rows):
            return
        self._insert_mode = False
        self.reset_pending()
        self._select_row(index)

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "db-save":
            self.request_save()
        elif button_id == "db-insert":
            self.request_insert()
        elif button_id == "db-delete":
            self.request_delete()
        elif button_id == "db-refresh":
            self.action_refresh()
        elif button_id == "db-first-page":
            self.action_first_page()
        elif button_id == "db-previous-page":
            self.action_previous_page()
        elif button_id == "db-next-page":
            self.action_next_page()
        elif button_id == "db-last-page":
            self.action_last_page()

    # endregion
