"""``data`` 入口的单元测试。

入口只按主键读写，表名与列名只认已注册模型声明过的标识：未知表、未知列、缺必填字段、改动主键列都
必须在入口层被拒，用户错误一律退出码 2。另有一次 sqlite 上的最小 round-trip，覆盖新建、读取、
改写、删除与重复删除，并核对读回的值是 JSON 安全的。
"""

import asyncio
import io
import json
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tortoise import Tortoise

from akaribot.core.database import close_db, init_db
from akaribot.core.database import link as db_link_module
from akaribot.core.database import local as db_local_module
from akaribot.core.entrypoints import data
from akaribot.testing import Tester, func_case

TABLE = "module_status"
# 多列改写的用例需要一张有两个以上普通列的表。
WIDE_TABLE = "module_wiki_bot_account_list"
PROBE_KEY = "probe-entry"


@contextmanager
def _temp_instance():
    # 库链接在 init_db() 调用时读取模块级变量，故把两个连接都指到临时目录：用例绝不碰仓库实例的库。
    with TemporaryDirectory(prefix="akari-data-") as raw:
        root = Path(raw)
        (root / "database").mkdir(parents=True, exist_ok=True)
        with (
            patch.object(db_link_module, "db_link", f"sqlite://{(root / 'database' / 'save.db').as_posix()}"),
            patch.object(db_local_module, "DB_LINK", f"sqlite://{(root / 'database' / 'local.db').as_posix()}"),
        ):
            yield root


def _run(args: list[str]) -> tuple[int, object]:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = data.main(args)
    text = stdout.getvalue().strip()
    return code, json.loads(text) if text else None


async def _call(*args: str) -> tuple[int, object]:
    # 入口内部用 asyncio.run()，而用例跑在事件循环里，故放回无循环的线程执行。
    return await asyncio.to_thread(_run, list(args))


async def _create_schema() -> None:
    await init_db(generate_schemas=False)
    try:
        await Tortoise.generate_schemas(safe=True)
    finally:
        await close_db()


def _error(payload: object) -> str:
    return str(payload.get("error") or "") if isinstance(payload, dict) else ""


async def _test_unknown_table_is_rejected():
    with _temp_instance():
        code, payload = await _call("rows", "no_such_table", "--limit", "1")
    return code == 2 and "no_such_table" in _error(payload)


async def _test_unknown_column_is_rejected():
    with _temp_instance():
        code, payload = await _call("set", TABLE, "--key", "dice", "--set", "no_such_column=1")
        order_code, order_payload = await _call("rows", TABLE, "--order-by", "no_such_column")
        filter_code, filter_payload = await _call("rows", TABLE, "--filter", "no_such_column=1")
    return (
        code == 2
        and "no_such_column" in _error(payload)
        and order_code == 2
        and "no_such_column" in _error(order_payload)
        and filter_code == 2
        and "no_such_column" in _error(filter_payload)
    )


async def _test_missing_required_field_is_rejected():
    with _temp_instance():
        code, payload = await _call("insert", TABLE, "--set", "load=true")
    return code == 2 and "module_name" in _error(payload)


async def _test_primary_key_cannot_be_changed():
    with _temp_instance():
        code, payload = await _call("set", TABLE, "--key", "dice", "--set", "module_name=other")
    return code == 2 and "module_name" in _error(payload)


async def _test_unparsable_value_is_rejected():
    with _temp_instance():
        code, payload = await _call("insert", TABLE, "--set", "module_name=x", "--set", "load=maybe")
    return code == 2 and "load" in _error(payload)


async def _test_negative_paging_is_rejected():
    with _temp_instance():
        limit_code, _ = await _call("rows", TABLE, "--limit", "-1")
        offset_code, _ = await _call("rows", TABLE, "--offset", "-5")
    return limit_code == 2 and offset_code == 2


async def _test_missing_key_is_rejected():
    with _temp_instance():
        await _create_schema()
        code, payload = await _call("set", TABLE, "--key", "absent", "--set", "load=true")
        delete_code, delete_payload = await _call("delete", TABLE, "--key", "absent")
    return code == 2 and delete_code == 2 and "absent" in _error(payload) and "absent" in _error(delete_payload)


async def _test_multi_column_set_is_one_update():
    # 一行多列：一次 set 改写整行的若干列，回读后各列都已生效。
    with _temp_instance():
        await _create_schema()
        await _call(
            "insert",
            WIDE_TABLE,
            "--set",
            f"api_link={PROBE_KEY}",
            "--set",
            "bot_account=old",
            "--set",
            "bot_password=secret",
        )
        code, updated = await _call(
            "set", WIDE_TABLE, "--key", PROBE_KEY, "--set", "bot_account=new", "--set", "bot_password=rotated"
        )
        _, page = await _call("rows", WIDE_TABLE, "--filter", f"api_link={PROBE_KEY}")
        rows = page.get("rows") if isinstance(page, dict) else None
    return (
        code == 0
        and updated.get("updated") == 1
        and updated.get("columns") == ["bot_account", "bot_password"]
        and rows == [{"api_link": PROBE_KEY, "bot_account": "new", "bot_password": "rotated"}]
    )


async def _test_multi_column_set_rejects_before_writing():
    # 多列里有一处取值非法时整行不动：转换全部通过才下发 UPDATE，不会留下改了一半的行。
    with _temp_instance():
        await _create_schema()
        await _call(
            "insert",
            WIDE_TABLE,
            "--set",
            f"api_link={PROBE_KEY}",
            "--set",
            "bot_account=old",
            "--set",
            "bot_password=secret",
        )
        code, payload = await _call(
            "set", WIDE_TABLE, "--key", PROBE_KEY, "--set", "bot_account=changed", "--set", "no_such_column=1"
        )
        _, page = await _call("rows", WIDE_TABLE, "--filter", f"api_link={PROBE_KEY}")
        rows = page.get("rows") if isinstance(page, dict) else None
    return (
        code == 2
        and "no_such_column" in _error(payload)
        and rows == [{"api_link": PROBE_KEY, "bot_account": "old", "bot_password": "secret"}]
    )


async def _test_set_without_assignment_is_rejected():
    with _temp_instance():
        code, payload = await _call("set", TABLE, "--key", "dice")
    return code == 2 and "set" in _error(payload)


async def _test_sqlite_round_trip():
    with _temp_instance():
        await _create_schema()
        insert_code, inserted = await _call("insert", TABLE, "--set", f"module_name={PROBE_KEY}", "--set", "load=yes")
        read_code, page = await _call("rows", TABLE, "--filter", f"module_name={PROBE_KEY}")
        set_code, updated = await _call("set", TABLE, "--key", PROBE_KEY, "--set", "load=false")
        _, after = await _call("rows", TABLE, "--filter", f"module_name={PROBE_KEY}")
        delete_code, deleted = await _call("delete", TABLE, "--key", PROBE_KEY)
        repeat_code, _ = await _call("delete", TABLE, "--key", PROBE_KEY)
    return (
        insert_code == 0
        and inserted.get("inserted") == 1
        and inserted.get("key") == PROBE_KEY
        and read_code == 0
        and page.get("total") == 1
        and page.get("rows") == [{"module_name": PROBE_KEY, "load": True}]
        and set_code == 0
        and updated.get("updated") == 1
        and after.get("rows") == [{"module_name": PROBE_KEY, "load": False}]
        and delete_code == 0
        and deleted.get("deleted") == 1
        and repeat_code == 2
    )


async def _test_tables_payload_shape():
    with _temp_instance():
        # 尚未建表时也要给得出清单：条数按未知回报，而不是整份清单失败。
        empty_code, empty_payload = await _call("tables", "--json")
        await _create_schema()
        code, payload = await _call("tables", "--json")
    if code != 0 or not isinstance(payload, list) or not isinstance(empty_payload, list):
        return False
    missing = next((item for item in empty_payload if item.get("table") == TABLE), None)
    found = next((item for item in payload if item.get("table") == TABLE), None)
    if not isinstance(found, dict) or not isinstance(missing, dict):
        return False
    columns = {column["name"]: column for column in found.get("columns") or []}
    return (
        empty_code == 0
        and missing.get("rows") is None
        and found.get("model") == "ModuleStatus"
        and found.get("rows") == 0
        and columns["module_name"]["pk"] is True
        and columns["load"]["pk"] is False
        and columns["load"]["null"] is False
        and columns["load"]["type"] == "BooleanField"
    )


async def _test_values_are_json_safe():
    with _temp_instance():
        await _create_schema()
        code, _ = await _call(
            "insert",
            "analytics_data",
            "--set",
            "module_name=probe",
            "--set",
            "module_type=entry",
            "--set",
            "target_id=target",
            "--set",
            "command=probe",
            "--set",
            "timestamp=2026-01-02T03:04:05",
        )
        _, page = await _call("rows", "analytics_data", "--filter", "module_name=probe")
    rows = page.get("rows") or []
    if code != 0 or len(rows) != 1:
        return False
    timestamp = rows[0].get("timestamp")
    return isinstance(timestamp, str) and timestamp.startswith("2026-01-02T03:04:05")


async def _test_plain_output_is_json():
    with _temp_instance():
        await _create_schema()
        await _call("insert", TABLE, "--set", f"module_name={PROBE_KEY}", "--set", "load=true")
        plain_code, plain = await _call("rows", TABLE, "--filter", f"module_name={PROBE_KEY}")
        json_code, as_json = await _call("rows", TABLE, "--filter", f"module_name={PROBE_KEY}", "--json")
        await _call("delete", TABLE, "--key", PROBE_KEY)
    return plain_code == 0 and json_code == 0 and plain == as_json


@func_case
async def test_data_entrypoint(tester: Tester):
    """core.entrypoints.data: 数据浏览与写入入口测试"""
    await tester.test(_test_unknown_table_is_rejected, "未知表名被拒")
    await tester.test(_test_unknown_column_is_rejected, "未知列名被拒")
    await tester.test(_test_missing_required_field_is_rejected, "缺必填字段被拒")
    await tester.test(_test_primary_key_cannot_be_changed, "主键列不可改写")
    await tester.test(_test_unparsable_value_is_rejected, "值无法按列类型解析被拒")
    await tester.test(_test_negative_paging_is_rejected, "负分页参数被拒")
    await tester.test(_test_missing_key_is_rejected, "主键不存在被拒")
    await tester.test(_test_multi_column_set_is_one_update, "一次改写多列并回读")
    await tester.test(_test_multi_column_set_rejects_before_writing, "一处取值非法则整行不动")
    await tester.test(_test_set_without_assignment_is_rejected, "缺少列赋值被拒")
    await tester.test(_test_sqlite_round_trip, "sqlite 上的最小读写闭环")
    await tester.test(_test_tables_payload_shape, "表清单载荷形状")
    await tester.test(_test_values_are_json_safe, "时间值以 ISO 文本回传")
    await tester.test(_test_plain_output_is_json, "缺省输出与 --json 一致")
    return tester
