"""数据库页：浏览表与数据项，改动经二次确认后写回。

数据与写入一律经 ``akaribot db`` 子命令（该命令再经 core 的 ``data`` 入口读写），界面不直接连库：
表名与列名只认 ORM 注册过的模型。左栏是表清单与搜索框，右上数据项，右下编辑区；``s``、``i``、``d``
第一次按只在状态栏问一次，第二次按同一个键才真正写入。
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.instance import default_instance_root
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process

# 一次读取的数据项条数：界面只做浏览与单条改写，分页由 core 侧统一收口。
PAGE_LIMIT = 20
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
        """返回编辑区里的字段名标签，带上类型。"""
        if not self.type:
            return self.name
        return i18n.t("cli.tui.database.field_label", column=self.name, kind=self.type)


@dataclass(frozen=True)
class TableInfo:
    """一张已注册模型对应的表。

    :param name: 表标识，如 ``module_status``。
    :param model: 模型类名。
    :param rows: 表内数据项条数。
    :param package: 声明该表的已装分发包；取不到时为空串。
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
        """返回主键列名，取不到时返回空串。"""
        column = self.pk
        return column.name if column is not None else ""

    def editable_columns(self) -> tuple[ColumnInfo, ...]:
        """返回可编辑的列，主键只能只读展示。"""
        return tuple(column for column in self.columns if not column.pk)


@dataclass(frozen=True)
class RowPage:
    """一页数据项。

    :param table: 表标识。
    :param total: 该表的数据项总数。
    :param rows: 本页数据项，键为列名。
    """

    table: str = ""
    total: int = 0
    rows: tuple[dict[str, Any], ...] = ()


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
        """返回状态栏用的一行说明，列出将改动的列与新旧值。"""
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


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def normalize_columns(payload: Any) -> tuple[ColumnInfo, ...]:
    """把 ``db tables --json`` 里的列数组归一化为列信息。

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
        table=str(payload.get("table") or table), total=int(payload.get("total") or 0), rows=tuple(collected)
    )


class DatabaseSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


@runtime_checkable
class DatabaseSource(Protocol):
    """数据库数据源接口；测试注入替身，生产走子进程。"""

    def tables(self) -> Sequence[TableInfo]:
        """返回实例数据库里已注册模型的表。"""

    def rows(self, table: str, *, limit: int, offset: int) -> RowPage:
        """返回一张表的一页数据项。"""

    def set_values(self, table: str, key: str, values: Mapping[str, str]) -> WriteResult:
        """按主键改写一行的一个或多个列；多列在同一次调用里下发。"""

    def insert_row(self, table: str, values: Mapping[str, str]) -> WriteResult:
        """新建一条数据项。"""

    def delete_row(self, table: str, key: str) -> WriteResult:
        """按主键删除一条数据项。"""


class StaticDatabaseSource:
    """固定数据的替身数据源，供自动化断言与自检使用，不产生任何子进程。

    :param tables: 表清单。
    :param pages: 表名到数据项的映射；缺省时每张表都返回空页。
    :param write_result: 写入返回值；缺省为成功。
    :param delete_result: 删除返回值；缺省为成功。
    :param insert_result: 新建返回值；缺省为成功。
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

    def tables(self) -> Sequence[TableInfo]:
        """见 :meth:`DatabaseSource.tables`。"""
        self.calls["tables"] += 1
        return self._tables

    def rows(self, table: str, *, limit: int, offset: int) -> RowPage:
        """见 :meth:`DatabaseSource.rows`。"""
        self.calls["rows"] += 1
        self.reads.append((table, limit, offset))
        items = self._pages.get(table, [])
        return RowPage(table=table, total=len(items), rows=tuple(items[offset : offset + limit]))

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

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
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
        self.root = Path(root).expanduser().resolve() if root is not None else default_instance_root()
        self.timeout = timeout
        self.calls = {"tables": 0, "rows": 0, "set": 0, "insert": 0, "delete": 0}
        self._runner = runner or subprocess.run

    def tables(self) -> Sequence[TableInfo]:
        """见 :meth:`DatabaseSource.tables`。"""
        self.calls["tables"] += 1
        return normalize_tables(self._invoke("tables"))

    def rows(self, table: str, *, limit: int, offset: int) -> RowPage:
        """见 :meth:`DatabaseSource.rows`。"""
        self.calls["rows"] += 1
        payload = self._invoke("rows", table, "--limit", str(limit), "--offset", str(offset))
        return normalize_page(payload, table)

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
        """见 :meth:`DatabaseSource.delete_row`；界面自己问过，故代为回答 CLI 的确认。"""
        self.calls["delete"] += 1
        return self._write("delete", table, "--key", key, "--yes")

    def _write(self, *args: str) -> WriteResult:
        # 解析失败与退出码非零都如实回报：状态栏要能区分「core 说不行」与「读不懂 core 的输出」。
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
            # 解析失败要把原始输出带上：调用方据此判断是 CLI 坏了还是 core 输出变了。
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
    # 只读文本一律经 render() 取：``Static.renderable`` 在 Textual 8.x 已不再是公开属性。
    return str(widget.render())


class EditorField(compat.Vertical):
    """编辑区里的一列：字段名标签与非主键输入框。

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
        """返回输入框里的当前文本。"""
        return self.query_one(compat.Input).value

    def set_value(self, text: str) -> None:
        """设置输入框文本，等价于用户键入。"""
        self.query_one(compat.Input).value = text


class DatabasePage(compat.Vertical):
    """数据库页控件。

    :param source: 数据源，缺省为 :class:`SubprocessDatabaseSource`。
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
        width: 32;
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
        height: 1fr;
    }
    DatabasePage #rows-caption {
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
    DatabasePage #row-list > ListItem {
        padding: 0 1;
    }
    DatabasePage #row-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DatabasePage #editor-pane {
        width: 42;
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
        min-width: 8;
    }
    DatabasePage #database-status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    can_focus = True

    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.database.bind_refresh")),
        ("s", "save", i18n.t("cli.tui.database.bind_save")),
        ("i", "insert", i18n.t("cli.tui.database.bind_insert")),
        ("d", "delete", i18n.t("cli.tui.database.bind_delete")),
        ("slash", "focus_search", i18n.t("cli.tui.database.bind_search")),
        ("escape", "cancel", i18n.t("cli.tui.database.bind_cancel")),
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
        self._row_index: int | None = None
        self._row_key: str = ""
        self._original: dict[str, Any] = {}
        self._insert_mode = False
        self._pending: WritePlan | None = None
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
                yield compat.ListView(id="row-list")
            with compat.VerticalScroll(id="editor-pane"):
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
                yield compat.Vertical(id="editor-fields")
                with compat.Horizontal(id="editor-actions"):
                    yield compat.Button(i18n.t("cli.tui.database.button_save"), id="db-save", variant="success")
                    yield compat.Button(i18n.t("cli.tui.database.button_insert"), id="db-insert")
                    yield compat.Button(i18n.t("cli.tui.database.button_delete"), id="db-delete", variant="warning")
                    yield compat.Button(i18n.t("cli.tui.database.button_refresh"), id="db-refresh")
        yield compat.Static(
            compat.plain_text(i18n.t("cli.tui.common.status_ready")), id="database-status", markup=False
        )

    def on_mount(self) -> None:
        """挂载后只装配控件；取数推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取表清单。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_tables(force=True)

    def focus_primary(self) -> None:
        """把焦点交给表清单；列表为空时退到页面容器，页级键位仍然生效。"""
        compat.focus_first(self, "#table-list")

    def _adopt_focus(self) -> None:
        # 表清单由后台任务填充：首帧时它还是空的，焦点只能落在页面容器上，数据到位后再补交给列表。
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
        """返回编辑区里的字段控件。"""
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

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不取数。
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
        self._selected = table
        info = self.selected_info
        if info is None:
            self._set_status(i18n.t("cli.tui.database.status_unknown_table", table=table))
            return False
        await self._rebuild_editor(info)
        self._insert_mode = False
        self._pending = None
        ok = await self.reload_rows(reset_offset=True)
        if ok:
            self._set_status(i18n.t("cli.tui.database.status_table_loaded", table=table, rows=self._page.total))
        return ok

    async def reload_rows(self, *, reset_offset: bool = False) -> bool:
        """读取当前表的数据项并重绘列表。

        :param reset_offset: 为 ``True`` 时回到第一页。
        :return: 是否成功。
        """
        if self._selected is None:
            return False
        offset = 0 if reset_offset else self._offset
        try:
            page = await asyncio.to_thread(self.source.rows, self._selected, limit=PAGE_LIMIT, offset=offset)
        except Exception as error:  # noqa: BLE001 - 取数失败只影响本页展示
            self.last_error = f"{type(error).__name__}: {error}"
            await self._clear_rows(i18n.t("cli.tui.database.rows_load_failed", error=error))
            self._set_status(
                i18n.t("cli.tui.common.error_separator").join(
                    [i18n.t("cli.tui.database.status_rows_failed", table=self._selected), self.last_error]
                )
            )
            return False
        self._page = page
        self._offset = offset
        self.last_error = ""
        self._render_rows()
        self._select_row(0 if reset_offset else self._row_index)
        return True

    async def _clear_rows(self, hint: str) -> None:
        self._page = RowPage(table=self._selected or "")
        self._row_index = None
        self._row_key = ""
        self._original = {}
        list_view = self.query_one("#row-list", compat.ListView)
        list_view.clear()
        self._row_texts = ()
        self.query_one("#rows-caption", compat.Static).update(compat.plain_text(hint))
        await self._clear_editor()

    async def _clear_editor(self) -> None:
        pane = self.query_one("#editor-fields", compat.Vertical)
        await pane.remove_children()
        self.query_one("#editor-pk", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.database.editor_pk_empty"))
        )
        self.query_one("#editor-caption", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.database.editor_caption_empty"))
        )

    async def _rebuild_editor(self, info: TableInfo) -> None:
        pane = self.query_one("#editor-fields", compat.Vertical)
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
        # 编辑区只读缓存里的数据项：渲染路径不得起子进程。
        info = self.selected_info
        if info is None:
            return
        if self._insert_mode:
            # 新建时主键可填：自增主键留空由数据库生成，非自增主键（如 module_status.module_name）
            # 必须由用户给出，只读展示会让这类表根本建不了数据项。
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
        list_view = self.query_one("#table-list", compat.ListView)
        width = self._list_width(list_view)
        # 行文本由表名与行数直接拼出：这两项都是数据，交给模板插值反而让列表读不出表名。
        rows = tuple(
            compat.fit_cells(f"{table.name}（{table.rows if table.rows is not None else '-'}）", width)
            for table in self.visible_tables
        )
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(compat.plain_text(row), markup=False)) for row in rows])
        index = self._table_index()
        if compat.highlighted_index(list_view) != index:
            list_view.index = index
        self._table_rows = rows
        self._adopt_focus()

    def _render_rows(self) -> None:
        info = self.selected_info
        list_view = self.query_one("#row-list", compat.ListView)
        width = self._list_width(list_view)
        separator = i18n.t("cli.tui.common.list_separator")
        rows: list[str] = []
        if info is not None:
            for row in self._page.rows:
                summary = separator.join(f"{name}={_text(value)}" for name, value in row.items())
                rows.append(compat.fit_cells(summary, width))
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(compat.plain_text(row), markup=False)) for row in rows])
            list_view.index = self._row_index if self._row_index is not None and self._row_index < len(rows) else 0
        else:
            list_view.index = None
        self._row_texts = tuple(rows)
        caption = (
            i18n.t("cli.tui.database.rows_caption", table=info.name, total=self._page.total, count=len(rows))
            if info is not None
            else i18n.t("cli.tui.database.rows_caption_empty")
        )
        self.query_one("#rows-caption", compat.Static).update(compat.plain_text(caption))

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
        self.query_one("#database-status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        if self._tables:
            self._render_tables()
        if self._page.rows:
            self._render_rows()

    # endregion

    # region 写入

    def action_refresh(self) -> None:
        """键位动作：作废缓存并重新读取表与数据项。"""
        self._pending = None
        self.refresh_tables(force=True)

    def action_save(self) -> None:
        """键位动作：保存编辑区的改动；新建模式下等价于写入新数据项。"""
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
        """键位动作：把焦点交给搜索框。"""
        self.query_one("#database-search", compat.Input).focus()

    def request_save(self) -> None:
        """保存编辑区的改动；第一次按只在状态栏问一次，第二次按同一个键才写。"""
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
        """进入新建模式；已在新建模式时按同一个键两次才写入。"""
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
        """删除当前数据项；第一次按只在状态栏问一次，第二次按同一个键才删。"""
        info = self.selected_info
        if info is None or self._row_index is None or not self._row_key:
            self._set_status(i18n.t("cli.tui.database.status_no_row"))
            return
        self._request(WritePlan(kind="delete", table=info.name, key=self._row_key))

    def cancel_edit(self) -> None:
        """退出新建模式、清空待确认状态并把编辑区还原为当前数据项。"""
        cancelled = self._pending is not None or self._insert_mode
        self._pending = None
        self._insert_mode = False
        self._sync_editor()
        self._set_status(
            i18n.t("cli.tui.database.status_cancelled") if cancelled else i18n.t("cli.tui.database.status_ready")
        )

    def _request(self, plan: WritePlan) -> None:
        if self._busy:
            self._set_status(i18n.t("cli.tui.common.busy_title"))
            return
        if self._pending != plan:
            self._pending = plan
            self._set_status(plan.summary())
            return
        self._pending = None
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
                # 一行一次调用：多列在同一次 UPDATE 里落库，不会出现改了一半的行。
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
        """写入成功后重新读取当前表的数据项，并尽量停在原来的主键上。"""
        previous = self._row_key
        self._loaded_at = 0.0
        await self.reload_rows(reset_offset=True)
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
        self._pending = None
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

    # endregion
