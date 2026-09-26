"""数据库页：表清单、数据项、编辑区与二次确认的写入。

页面只经 ``akaribot db`` 子命令读写，故用例一律注入替身数据源，不起真子进程：写操作必须按两次
同一个键才发生，第一次只把将改动的列与新旧值记在待确认计划里；写入失败后页面仍可继续读取与重试。
"""

import json
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.database import (
    ColumnInfo,
    DatabaseSource,
    StaticDatabaseSource,
    SubprocessDatabaseSource,
    TableInfo,
    WriteResult,
)
from akaribot.testing import Tester, func_case

MODULE_COLUMNS = (ColumnInfo("module_name", "CharField", pk=True), ColumnInfo("load", "BooleanField"))
STORED_COLUMNS = (ColumnInfo("stored_key", "CharField", pk=True), ColumnInfo("value", "JSONField"))
TABLES = (
    TableInfo(name="module_status", model="ModuleStatus", rows=2, package="akari-bot-core", columns=MODULE_COLUMNS),
    TableInfo(name="stored_data", model="StoredData", rows=1, package="", columns=STORED_COLUMNS),
)
ROWS = {
    "module_status": ({"module_name": "dice", "load": True}, {"module_name": "wiki", "load": False}),
    "stored_data": ({"stored_key": "demo", "value": {"a": 1}},),
}


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticDatabaseSource:
    params: dict = {"tables": TABLES, "pages": ROWS}
    params.update(kwargs)
    return StaticDatabaseSource(**params)


async def _with_page(body, source: DatabaseSource | None = None, size=(120, 34)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"database": chosen}, initial_page="database", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("database")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _select_table(pilot, page, name: str) -> None:
    index = next(position for position, table in enumerate(page.visible_tables) if table.name == name)
    page.query_one("#table-list", compat.ListView).index = index
    await pilot.pause()
    await page.wait_for_idle()
    await pilot.pause()


async def _select_row(pilot, page, index: int) -> None:
    page.query_one("#row-list", compat.ListView).index = index
    await pilot.pause()
    await page.wait_for_idle()
    await pilot.pause()


async def _test_lists_tables():
    async def body(app, page, pilot, source):
        rows = page.table_row_texts()
        items = len(page.query_one("#table-list", compat.ListView).children)
        await pilot.press("q")
        return rows, items

    rows, items = await _with_page(body)
    return len(rows) == 2 and items == 2 and "module_status" in rows[0] and "stored_data" in rows[1] and "2" in rows[0]


async def _test_search_narrows_tables():
    async def body(app, page, pilot, source):
        page.set_query("stored")
        await pilot.pause()
        narrowed = page.table_row_texts()
        page.set_query("")
        await pilot.pause()
        restored = len(page.table_row_texts())
        await pilot.press("q")
        return narrowed, restored

    narrowed, restored = await _with_page(body)
    return len(narrowed) == 1 and "stored_data" in narrowed[0] and restored == 2


async def _test_selecting_table_loads_rows():
    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await pilot.pause()
        await pilot.press("q")
        return page.page, page.row_texts(), list(source.reads)

    loaded, texts, reads = await _with_page(body)
    return (
        loaded.table == "module_status"
        and loaded.total == 2
        and len(texts) == 2
        and "dice" in texts[0]
        and "wiki" in texts[1]
        and reads == [("module_status", 20, 0)]
    )


async def _test_selecting_row_fills_editor():
    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 1)
        values = page.editor_values()
        pk_text = page.pk_text()
        fields = [field.column.name for field in page.editor()]
        await pilot.press("q")
        return values, pk_text, fields, page.selected_key

    values, pk_text, fields, key = await _with_page(body)
    return values == {"load": "false"} and fields == ["load"] and bool(pk_text) and key == "wiki"


async def _test_primary_key_is_read_only():
    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "stored_data")
        await _select_row(pilot, page, 0)
        fields = [field.column.name for field in page.editor()]
        pk = page.selected_info.pk_name
        await pilot.press("q")
        return fields, pk

    fields, pk = await _with_page(body)
    return fields == ["value"] and pk == "stored_key"


async def _test_json_values_round_trip_in_editor():
    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "stored_data")
        await _select_row(pilot, page, 0)
        values = page.editor_values()
        await pilot.press("q")
        return values

    values = await _with_page(body)
    return values == {"value": '{"a": 1}'}


async def _test_save_needs_two_presses():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        before = page.status_text
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        asked, pending = list(source.writes), page.pending
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, pending, list(source.writes), page.status_text != before

    asked, pending, written, status_changed = await _with_page(body, source)
    return (
        asked == []
        and pending is not None
        and pending.changes == (("load", "true", "false"),)
        and status_changed
        and written == [("module_status", "dice", "load", "false")]
    )


async def _test_unchanged_editor_writes_nothing():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        await pilot.press("s")
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.writes), page.pending

    written, pending = await _with_page(body, source)
    return written == [] and pending is None


async def _test_save_passes_argv_to_cli():
    calls: list[list[str]] = []
    payloads = {
        "rows": {"table": "module_status", "total": 1, "rows": [{"module_name": "dice", "load": True}]},
        "set": {"table": "module_status", "key": "dice", "column": "load", "updated": 1},
        "tables": [],
    }

    def runner(argv, **kwargs):
        calls.append(list(argv))
        command = argv[argv.index("db") + 1]
        return subprocess.CompletedProcess(argv, 0, json.dumps(payloads[command], ensure_ascii=False), "")

    with TemporaryDirectory(prefix="akari-db-") as raw:
        source = SubprocessDatabaseSource(root=Path(raw), timeout=10.0, runner=runner)

        async def body(app, page, pilot, source):
            # 表清单直接写进页面，只让写路径经子进程，argv 才能被逐段核对。
            page._tables = TABLES
            page._loaded_at = time.monotonic()
            await page.select_table("module_status")
            await _select_row(pilot, page, 0)
            page.set_editor_value("load", "false")
            page.request_save()
            await page.wait_for_idle()
            await pilot.pause()
            before = [call for call in calls if "set" in call]
            page.request_save()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return before, [call for call in calls if "set" in call]

        before, after = await _with_page(body, source)
    expected = cli_process.cli_argv(
        "db", "set", "module_status", "--key", "dice", "--column", "load", "--value", "false", "--json"
    )
    return before == [] and after == [expected]


async def _test_insert_needs_two_presses():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        await pilot.press("i")
        await pilot.pause()
        mode = page.insert_mode
        empty = page.editor_values()
        key = page.selected_key
        page.set_editor_value("load", "true")
        await pilot.press("i")
        await pilot.pause()
        asked = list(source.inserted)
        await pilot.press("i")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return mode, empty, key, asked, list(source.inserted)

    mode, empty, key, asked, inserted = await _with_page(body, source)
    return (
        mode
        and empty == {"load": ""}
        and key == ""
        and asked == []
        and inserted == [("module_status", {"load": "true"})]
    )


async def _test_insert_can_set_primary_key():
    # 主键非自增且必填的表（如 module_status.module_name）必须能填主键，否则这类表建不了数据项。
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await pilot.press("i")
        await pilot.pause()
        pk_input = page.query_one("#editor-pk-input", compat.Input)
        editable = pk_input.display
        readonly = page.query_one("#editor-pk", compat.Static).display
        pk_input.value = "wordle"
        page.set_editor_value("load", "true")
        await pilot.press("i")
        await pilot.pause()
        await pilot.press("i")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return editable, readonly, list(source.inserted)

    editable, readonly, inserted = await _with_page(body, source)
    return editable and not readonly and inserted == [("module_status", {"module_name": "wordle", "load": "true"})]


async def _test_insert_passes_argv_to_cli():
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(
            argv, 0, json.dumps({"table": "module_status", "inserted": 1, "key": "dice"}), ""
        )

    with TemporaryDirectory(prefix="akari-db-") as raw:
        source = SubprocessDatabaseSource(root=Path(raw), timeout=10.0, runner=runner)

        async def body(app, page, pilot, source):
            page._tables = TABLES
            page._loaded_at = time.monotonic()
            await page.select_table("module_status")
            await _select_row(pilot, page, 0)
            page.request_insert()
            await pilot.pause()
            page.set_editor_value("load", "false")
            page.request_insert()
            await pilot.pause()
            page.request_insert()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return [call for call in calls if "insert" in call]

        inserts = await _with_page(body, source)
    expected = cli_process.cli_argv("db", "insert", "module_status", "--set", "load=false", "--json")
    return inserts == [expected]


async def _test_delete_needs_two_presses():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        await pilot.press("d")
        await pilot.pause()
        asked, pending = list(source.deleted), page.pending
        await pilot.press("d")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, pending, list(source.deleted)

    asked, pending, deleted = await _with_page(body, source)
    return (
        asked == []
        and pending is not None
        and pending.kind == "delete"
        and pending.key == "dice"
        and deleted == [("module_status", "dice")]
    )


async def _test_delete_passes_argv_to_cli():
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(list(argv))
        payloads = {
            "rows": {"table": "module_status", "total": 1, "rows": [{"module_name": "dice", "load": True}]},
            "delete": {"table": "module_status", "key": "dice", "deleted": 1},
            "tables": [],
        }
        command = argv[argv.index("db") + 1]
        return subprocess.CompletedProcess(argv, 0, json.dumps(payloads[command]), "")

    with TemporaryDirectory(prefix="akari-db-") as raw:
        source = SubprocessDatabaseSource(root=Path(raw), timeout=10.0, runner=runner)

        async def body(app, page, pilot, source):
            page._tables = TABLES
            page._loaded_at = time.monotonic()
            await page.select_table("module_status")
            await _select_row(pilot, page, 0)
            page.request_delete()
            await page.wait_for_idle()
            await pilot.pause()
            page.request_delete()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return [call for call in calls if "delete" in call]

        deletes = await _with_page(body, source)
    expected = cli_process.cli_argv("db", "delete", "module_status", "--key", "dice", "--yes", "--json")
    return deletes == [expected]


async def _test_cancel_clears_pending():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await pilot.pause()
        pending = page.pending is not None
        await pilot.press("escape")
        await pilot.pause()
        cleared = page.pending is None
        restored = page.editor_values()
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return pending, cleared, restored, list(source.writes)

    pending, cleared, restored, written = await _with_page(body, source)
    return pending and cleared and restored == {"load": "true"} and written == []


async def _test_write_failure_reports_reason():
    source = _source(
        write_result=WriteResult(False, "列 load 无法写入", "UNIQUE constraint failed: module_status.load")
    )

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        before = page.status_text
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return page.status_text, page.last_error, before

    status, last_error, before = await _with_page(body, source)
    return (
        "列 load 无法写入" in status
        and "UNIQUE constraint failed" in status
        and status != before
        and "UNIQUE constraint failed" in last_error
    )


async def _test_page_still_usable_after_failure():
    class FlakySource(StaticDatabaseSource):
        # 第一次写入失败、之后成功：验证失败后仍能重新读取并完成写入。
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.remaining_failures = 1

        def set_value(self, table, key, column, value):
            self.calls["set"] += 1
            self.writes.append((table, key, column, value))
            if self.remaining_failures:
                self.remaining_failures -= 1
                return WriteResult(False, "写入被拒绝", "写入被拒绝：唯一约束冲突")
            return WriteResult(True, "写入成功", "")

    source = FlakySource(tables=TABLES, pages=ROWS)

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        failed = page.status_text
        await pilot.press("r")
        await page.wait_for_idle()
        await pilot.pause()
        reloaded = page.table_row_texts()
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        filled = page.editor_values()
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return failed, reloaded, filled, list(source.writes), page.status_text

    failed, reloaded, filled, written, status = await _with_page(body, source)
    return (
        "写入被拒绝" in failed
        and len(reloaded) == 2
        and filled == {"load": "true"}
        and len(written) == 2
        and written[1] == ("module_status", "dice", "load", "false")
        and "写入被拒绝" not in status
    )


async def _test_broken_json_is_reported():
    def runner(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, "not json at all", "")

    with TemporaryDirectory(prefix="akari-db-") as raw:
        source = SubprocessDatabaseSource(root=Path(raw), timeout=10.0, runner=runner)
        try:
            source.rows("module_status", limit=20, offset=0)
        except Exception as error:  # noqa: BLE001 - 用例只核对失败原因是否如实转述
            return "not json at all" in str(error)
    return False


async def _test_broken_json_reaches_status():
    def runner(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, "not json at all", "")

    with TemporaryDirectory(prefix="akari-db-") as raw:
        source = SubprocessDatabaseSource(root=Path(raw), timeout=10.0, runner=runner)

        async def body(app, page, pilot, source):
            page._tables = TABLES
            page._loaded_at = time.monotonic()
            page._selected = "module_status"
            page.set_editor_value("load", "false")
            await page.reload_rows()
            await pilot.pause()
            await pilot.press("q")
            return page.status_text

        status = await _with_page(body, source)
    return "not json at all" in status


async def _test_row_page_expands_offset():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page._offset = 20
        await page.reload_rows()
        await pilot.pause()
        await pilot.press("q")
        return list(source.reads)

    reads = await _with_page(body, source)
    return reads == [("module_status", 20, 0), ("module_status", 20, 20)]


@func_case
async def test_tui_database(tester: Tester):
    """cli.tui.database: 数据库页的表清单、数据项与写入确认测试"""
    _use_cli_locale()
    await tester.test(_test_lists_tables, "渲染表清单")
    await tester.test(_test_search_narrows_tables, "搜索收窄表清单")
    await tester.test(_test_selecting_table_loads_rows, "选中表加载数据项")
    await tester.test(_test_selecting_row_fills_editor, "选中数据项填充编辑区")
    await tester.test(_test_primary_key_is_read_only, "主键只读不进编辑字段")
    await tester.test(_test_json_values_round_trip_in_editor, "JSON 值按 JSON 文本回填")
    await tester.test(_test_save_needs_two_presses, "保存需两次确认")
    await tester.test(_test_unchanged_editor_writes_nothing, "未改动不写入")
    await tester.test(_test_save_passes_argv_to_cli, "保存以正确 argv 调用 CLI")
    await tester.test(_test_insert_needs_two_presses, "新建走 insert")
    await tester.test(_test_insert_can_set_primary_key, "新建时可填非自增主键")
    await tester.test(_test_insert_passes_argv_to_cli, "新建以正确 argv 调用 CLI")
    await tester.test(_test_delete_needs_two_presses, "删除需两次确认")
    await tester.test(_test_delete_passes_argv_to_cli, "删除以正确 argv 调用 CLI")
    await tester.test(_test_cancel_clears_pending, "Esc 清空待确认")
    await tester.test(_test_write_failure_reports_reason, "写失败在状态栏给出原因")
    await tester.test(_test_page_still_usable_after_failure, "失败后界面仍可用")
    await tester.test(_test_broken_json_is_reported, "JSON 解析失败如实上报")
    await tester.test(_test_broken_json_reaches_status, "解析失败进状态栏")
    await tester.test(_test_row_page_expands_offset, "重新读取沿用当前偏移")
    return tester
