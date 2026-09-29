"""数据库页：表清单、数据项、编辑区与二次确认的写入。

页面只经 ``akaribot db`` 子命令读写，故用例一律注入替身数据源，不起真子进程：写操作必须按两次
同一个键才发生，第一次只把将改动的列与新旧值记在待确认计划里；写入失败后页面仍可继续读取与重试。
"""

import json
import subprocess
from unittest import mock
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.database import (
    PAGE_LIMIT,
    ColumnInfo,
    DatabaseSource,
    RowQuery,
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


# 点确认框里的「写入」按钮：写入一律经模态确认，第二次按键不再直接执行。
async def _confirm_write(app, pilot) -> None:
    app.screen.query_one("#choice-0", compat.Button).press()
    await pilot.pause()


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
        and reads == [("module_status", PAGE_LIMIT, 0)]
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


async def _test_write_keeps_the_page_and_recounts():
    # 翻到第几页是用户的上下文：改一行、删一行都留在当前页，但条数要重算（写入会改变总数）。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.action_next_page()
        await page.wait_for_idle()
        await pilot.pause()
        await _select_row(pilot, page, 0)
        page.set_editor_value("load", "false")
        await pilot.press("s")
        await pilot.pause()
        await _confirm_write(app, pilot)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return page.offset, [item[2] for item in source.queries], list(source.writes)

    offset, counts, writes = await _with_page(body, source)
    return offset == PAGE_LIMIT and counts[-1] is True and len(writes) == 1


async def _test_failed_rows_load_disables_the_pager():
    source = _source()
    source.rows = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        states = page.pager_states()
        caption = page.caption_text()
        await pilot.press("q")
        return states, caption

    states, caption = await _with_page(body, source)
    # 失败原因写在标题行，且四个翻页按钮全部禁用。
    return all(states.values()) and "boom" in caption


async def _test_save_asks_for_confirmation():
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
        await _confirm_write(app, pilot)
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
        and written == [("module_status", "dice", {"load": "false"})]
    )


async def _test_multi_column_save_is_one_call():
    # 一行多列：改动几列都只发一次写入，各列在同一次 UPDATE 里落库。
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "stored_data")
        await _select_row(pilot, page, 0)
        page.set_editor_value("value", '{"a": 2}')
        await pilot.press("s")
        await pilot.pause()
        pending = page.pending
        await _confirm_write(app, pilot)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return pending, list(source.writes)

    pending, written = await _with_page(body, source)
    return (
        pending is not None
        and len(pending.changes) == 1
        and written == [("stored_data", "demo", {"value": '{"a": 2}'})]
    )


async def _test_unchanged_editor_writes_nothing():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        await pilot.press("s")
        await pilot.pause()
        # 没有改动时连确认框都不该出现：先说明「没有可写的内容」，不打扰用户。
        opened = type(app.screen).__name__
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.writes), page.pending, opened

    written, pending, opened = await _with_page(body, source)
    return written == [] and pending is None and opened == "Screen"


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
            await pilot.pause()
            before = [call for call in calls if "set" in call]
            app.screen.query_one("#choice-0", compat.Button).press()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return before, [call for call in calls if "set" in call]

        before, after = await _with_page(body, source)
    expected = cli_process.cli_argv("db", "set", "module_status", "--key", "dice", "--set", "load=false", "--json")
    return before == [] and after == [expected]


async def _test_insert_asks_for_confirmation():
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
        await _confirm_write(app, pilot)
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
        await _confirm_write(app, pilot)
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
            app.screen.query_one("#choice-0", compat.Button).press()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return [call for call in calls if "insert" in call]

        inserts = await _with_page(body, source)
    expected = cli_process.cli_argv("db", "insert", "module_status", "--set", "load=false", "--json")
    return inserts == [expected]


async def _test_delete_asks_for_confirmation():
    source = _source()

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await _select_row(pilot, page, 0)
        await pilot.press("ctrl+d")
        await pilot.pause()
        asked, pending = list(source.deleted), page.pending
        await _confirm_write(app, pilot)
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
            await pilot.pause()
            app.screen.query_one("#choice-0", compat.Button).press()
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
        # 取消后编辑区退回该行的取值，此时再按 s 只会提示「没有可写的内容」，不会落库。
        await pilot.press("s")
        await pilot.pause()
        reopened = type(app.screen).__name__
        status = page.status_text
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return pending, cleared, restored, list(source.writes), reopened, status

    pending, cleared, restored, written, reopened, status = await _with_page(body, source)
    return (
        pending
        and cleared
        and restored == {"load": "true"}
        and written == []
        and reopened == "Screen"
        and status == i18n.t("cli.tui.database.status_no_changes", table="module_status", pk="module_name")
    )


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
        await pilot.pause()
        await _confirm_write(app, pilot)
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

        def set_values(self, table, key, values):
            self.calls["set"] += 1
            self.writes.append((table, key, dict(values)))
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
        await pilot.pause()
        await _confirm_write(app, pilot)
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
        await pilot.pause()
        await _confirm_write(app, pilot)
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
        and written[1] == ("module_status", "dice", {"load": "false"})
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
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page._offset = PAGE_LIMIT
        await page.reload_rows()
        await pilot.pause()
        await pilot.press("q")
        return list(source.reads)

    reads = await _with_page(body, source)
    return reads == [("module_status", PAGE_LIMIT, 0), ("module_status", PAGE_LIMIT, PAGE_LIMIT)]


def _big_rows(count: int = 130) -> tuple[dict[str, object], ...]:
    return tuple({"module_name": f"mod-{index:03d}", "load": index % 2 == 0} for index in range(count))


async def _test_paging_walks_pages():
    # 线上表很大，界面一次只取一页：翻页改的是偏移，条数与页码由服务端回传的总数算。
    pages = {"module_status": _big_rows()}
    source = _source(pages=pages)

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        first = (page.page.page_number, page.page.pages, len(page.row_texts()), page.pager_states())
        await pilot.press("n")
        await page.wait_for_idle()
        await pilot.pause()
        second = (page.page.page_number, page.offset, len(page.row_texts()))
        await pilot.press("G")
        await page.wait_for_idle()
        await pilot.pause()
        last = (page.page.page_number, page.offset, len(page.row_texts()), page.pager_states())
        await pilot.press("g")
        await page.wait_for_idle()
        await pilot.pause()
        back = (page.page.page_number, page.offset)
        await pilot.press("q")
        return first, second, last, back, list(source.reads)

    first, second, last, back, reads = await _with_page(body, source)
    return (
        first[0] == 1
        and first[1] == 3
        and first[2] == PAGE_LIMIT
        and first[3]["db-previous-page"] is True
        and first[3]["db-next-page"] is False
        and second == (2, PAGE_LIMIT, PAGE_LIMIT)
        and last[0] == 3
        and last[1] == 2 * PAGE_LIMIT
        and last[2] == 30
        and last[3]["db-next-page"] is True
        and last[3]["db-last-page"] is True
        and back == (1, 0)
        and reads
        == [
            ("module_status", PAGE_LIMIT, 0),
            ("module_status", PAGE_LIMIT, PAGE_LIMIT),
            ("module_status", PAGE_LIMIT, 2 * PAGE_LIMIT),
            ("module_status", PAGE_LIMIT, 0),
        ]
    )


async def _test_page_turns_skip_the_count():
    # 纯翻页不再重算总数：大表上一次 COUNT 就是一次全表扫描，条数沿用上一页的。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await pilot.press("n")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("n")
        await page.wait_for_idle()
        await pilot.pause()
        caption = page.caption_text()
        await pilot.press("q")
        return list(source.queries), caption, page.page.rows_total

    queries, caption, total = await _with_page(body, source)
    # 末页只剩 30 条，条数沿用上一页统计出来的 130。
    return (
        [item[2] for item in queries] == [True, False, False]
        and total == 130
        and i18n.t("cli.tui.database.rows_caption", table="module_status", total=130, count=30, page=3, pages=3)
        == caption
    )


async def _test_paging_stops_at_last_page():
    # 已在末页时不再重复取数，只在状态栏说明。
    source = _source(pages={"module_status": _big_rows(10)})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        before = len(source.reads)
        await pilot.press("n")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return before, len(source.reads), status, page.pager_states()

    before, after, status, states = await _with_page(body, source)
    return (
        before == 1
        and after == 1
        and status == i18n.t("cli.tui.database.status_page_same", page=1, pages=1)
        and states["db-next-page"] is True
    )


async def _test_filter_narrows_rows():
    # 按条件筛选：条件下发到数据源，列表收窄，总数与页码随之重算，偏移回到第一页。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        await pilot.press("n")
        await page.wait_for_idle()
        await pilot.pause()
        page.action_add_filter()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "load=false"
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return page.row_query, page.offset, page.page, status, list(source.queries)

    query, offset, page_info, status, queries = await _with_page(body, source)
    return (
        query.filters == ("load=false",)
        and offset == 0
        and page_info.total == 65
        and len(page_info.rows) == PAGE_LIMIT
        and all(row["load"] is False for row in page_info.rows)
        and status == i18n.t("cli.tui.database.status_filter_added", condition="load=false")
        and queries[-1][1].filters == ("load=false",)
        and queries[-1][2] is True
    )


async def _test_search_uses_text_columns():
    # 只写一个词时按全表搜索下发，而不是当成条件。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.action_add_filter()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "mod-01"
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return page.row_query, page.page.total, page.row_texts(), page.filter_text()

    query, total, rows, bar = await _with_page(body, source)
    return (
        query.search == "mod-01"
        and query.filters == ()
        and total == 10
        and len(rows) == 10
        and i18n.t("cli.tui.database.search_term", keyword="mod-01") in bar
    )


async def _test_search_word_with_operator_chars_stays_search():
    # 搜索词里带 ~、= 之类字符时不能误判成条件：只有「列名 + 运算符」才算条件。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.on_filter_entered("~mod-01")
        await page.wait_for_idle()
        await pilot.pause()
        searches = page.row_query
        page.on_filter_entered("mod-012")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return searches, page.row_query

    searches, word = await _with_page(body, source)
    return searches.filters == () and searches.search == "~mod-01" and word.filters == () and word.search == "mod-012"


async def _test_conditions_are_anded_and_clearable():
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.on_filter_entered("load=true")
        await page.wait_for_idle()
        await pilot.pause()
        page.on_filter_entered("module_name~mod-0")
        await page.wait_for_idle()
        await pilot.pause()
        anded = (page.row_query, page.page.total, page.offset)
        await pilot.press("ctrl+f")
        await page.wait_for_idle()
        await pilot.pause()
        cleared = (page.row_query, page.page.total, page.filter_text())
        await pilot.press("q")
        return anded, cleared

    anded, cleared = await _with_page(body, source)
    return (
        anded[0].filters == ("load=true", "module_name~mod-0")
        and anded[1] == 50
        and anded[2] == 0
        and cleared[0].is_empty()
        and cleared[1] == 130
        and cleared[2].startswith(i18n.t("cli.tui.database.filter_none"))
    )


async def _test_sort_dialog_sets_order():
    # 排序也下推到 core：界面只报「列:方向」，改排序后回到第一页。
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.action_next_page()
        await page.wait_for_idle()
        await pilot.pause()
        page.action_set_order()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "module_name:asc"
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        sorts = (page.offset, page.row_query.order_by, page.filter_text())
        await pilot.press("q")
        return sorts, status, list(source.queries)

    (offset, order, line), status, queries = await _with_page(body, source)
    return (
        offset == 0
        and order == "module_name:asc"
        and queries[-1][1].order_by == "module_name:asc"
        and status == i18n.t("cli.tui.database.status_order_set", order="module_name:asc")
        and "module_name:asc" in line
    )


async def _test_empty_order_falls_back_to_default():
    source = _source(pages={"module_status": _big_rows()})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.on_order_entered("units:desc")
        await page.wait_for_idle()
        await pilot.pause()
        page.on_order_entered("   ")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        default_line = page.filter_text()
        await pilot.press("q")
        return status, default_line, page.row_query.order_by, list(source.queries)

    status, default_line, order, queries = await _with_page(body, source)
    return (
        order == ""
        and queries[-1][1].order_by == ""
        and status == i18n.t("cli.tui.database.status_order_reset")
        and i18n.t("cli.tui.database.order_default", column="-module_name") in default_line
    )


async def _test_switching_table_clears_filters():
    # 条件里的列名只对原表成立，换表即清空。
    source = _source(pages={"module_status": _big_rows(), "stored_data": ROWS["stored_data"]})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page.on_filter_entered("load=false")
        await page.wait_for_idle()
        await pilot.pause()
        filtered = page.row_query
        await _select_table(pilot, page, "stored_data")
        await pilot.press("q")
        return filtered, page.row_query

    filtered, after = await _with_page(body, source)
    return filtered.filters == ("load=false",) and after.is_empty()


async def _test_subprocess_source_passes_query_argv():
    # 界面把条件、搜索与排序拼成 ``db rows`` 的 argv，core 侧才认得出这些参数。
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append([str(item) for item in argv])
        return subprocess.CompletedProcess(
            list(argv), 0, stdout=json.dumps({"table": "t", "total": 0, "rows": []}), stderr=""
        )

    source = SubprocessDatabaseSource(runner=runner)
    source.rows(
        "module_status",
        limit=PAGE_LIMIT,
        offset=PAGE_LIMIT,
        query=RowQuery(filters=("load=false", "module_name~w"), search="wik", order_by="module_name:asc"),
    )
    argv = calls[0]
    tail = argv[argv.index("db") :]
    return tail == [
        "db",
        "rows",
        "module_status",
        "--limit",
        str(PAGE_LIMIT),
        "--offset",
        str(PAGE_LIMIT),
        "--filter",
        "load=false",
        "--filter",
        "module_name~w",
        "--search",
        "wik",
        "--order-by",
        "module_name:asc",
        "--json",
    ]


async def _test_offset_clamps_to_last_page():
    # 总数变小后偏移可能落到末页之外：夹回末页，而不是把用户留在空白页。
    source = _source(pages={"module_status": _big_rows(10)})

    async def body(app, page, pilot, source):
        await _select_table(pilot, page, "module_status")
        page._offset = 5 * PAGE_LIMIT
        await page.reload_rows()
        await pilot.pause()
        await pilot.press("q")
        return page.page.page_number, page.offset, list(source.reads)

    number, offset, reads = await _with_page(body, source)
    # 三次读取：载入表、按越界偏移取一次、夹回末页再取一次。
    return (
        number == 1
        and offset == 0
        and reads
        == [
            ("module_status", PAGE_LIMIT, 0),
            ("module_status", PAGE_LIMIT, 5 * PAGE_LIMIT),
            ("module_status", PAGE_LIMIT, 0),
        ]
    )


@func_case
async def test_tui_database(tester: Tester):
    """cli.tui.database: 数据库页的表清单、数据项与写入确认测试"""
    _use_cli_locale()
    # 用例里的两次按键几乎同时发生，压缩防抖窗口，免得每条确认都等 0.4 秒。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_lists_tables, "渲染表清单")
        await tester.test(_test_search_narrows_tables, "搜索收窄表清单")
        await tester.test(_test_selecting_table_loads_rows, "选中表加载数据项")
        await tester.test(_test_selecting_row_fills_editor, "选中数据项填充编辑区")
        await tester.test(_test_primary_key_is_read_only, "主键只读不进编辑字段")
        await tester.test(_test_json_values_round_trip_in_editor, "JSON 值按 JSON 文本回填")
        await tester.test(_test_save_asks_for_confirmation, "保存先弹确认框")
        await tester.test(_test_write_keeps_the_page_and_recounts, "写入留在当前页并重算条数")
        await tester.test(_test_failed_rows_load_disables_the_pager, "取数失败时禁用翻页按钮")
        await tester.test(_test_multi_column_save_is_one_call, "多列改动合并成一次写入")
        await tester.test(_test_unchanged_editor_writes_nothing, "未改动不写入")
        await tester.test(_test_save_passes_argv_to_cli, "保存以正确 argv 调用 CLI")
        await tester.test(_test_insert_asks_for_confirmation, "新建先弹确认框再 insert")
        await tester.test(_test_insert_can_set_primary_key, "新建时可填非自增主键")
        await tester.test(_test_insert_passes_argv_to_cli, "新建以正确 argv 调用 CLI")
        await tester.test(_test_delete_asks_for_confirmation, "删除先弹确认框")
        await tester.test(_test_delete_passes_argv_to_cli, "删除以正确 argv 调用 CLI")
        await tester.test(_test_cancel_clears_pending, "Esc 清空待确认")
        await tester.test(_test_write_failure_reports_reason, "写失败在状态栏给出原因")
        await tester.test(_test_page_still_usable_after_failure, "失败后界面仍可用")
        await tester.test(_test_broken_json_is_reported, "JSON 解析失败如实上报")
        await tester.test(_test_broken_json_reaches_status, "解析失败进状态栏")
        await tester.test(_test_row_page_expands_offset, "重新读取沿用当前偏移")
        await tester.test(_test_offset_clamps_to_last_page, "偏移超出末页时夹回末页")
        await tester.test(_test_paging_walks_pages, "分页翻页：下一页、末页、首页")
        await tester.test(_test_page_turns_skip_the_count, "纯翻页跳过总数统计")
        await tester.test(_test_paging_stops_at_last_page, "末页不再重复取数")
        await tester.test(_test_filter_narrows_rows, "按条件筛选并重算总数")
        await tester.test(_test_search_uses_text_columns, "单词输入走全表搜索")
        await tester.test(_test_search_word_with_operator_chars_stays_search, "带运算符字符的搜索词仍是搜索")
        await tester.test(_test_conditions_are_anded_and_clearable, "多条条件是 AND 且可一键清空")
        await tester.test(_test_sort_dialog_sets_order, "排序对话框把列与方向下推")
        await tester.test(_test_empty_order_falls_back_to_default, "清空排序回到缺省主键倒序")
        await tester.test(_test_switching_table_clears_filters, "换表清空条件")
        await tester.test(_test_subprocess_source_passes_query_argv, "条件与排序拼成 db rows 的 argv")
        return tester
