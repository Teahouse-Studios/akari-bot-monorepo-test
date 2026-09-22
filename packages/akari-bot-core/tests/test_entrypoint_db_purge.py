"""``db purge`` 入口的单元测试。

``--purge-data`` 是破坏性操作，两条边界必须由 core 自己守住：表名只能来自包 manifest（调用方
传不进来），以及只删声明的表（未声明的表即使存在也不动）。表已不存在时按幂等成功处理，否则
重跑一次卸载就会卡在一个已经达成的目标上。

入口内部用 ``asyncio.run``，而用例本身跑在事件循环里，故涉及 ``main()`` 的断言一律经
``asyncio.to_thread`` 放回无循环的线程执行，与真实子进程调用同形态。
"""

import asyncio
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import AsyncMock, patch

from akaribot.core.entrypoints import db
from akaribot.core.registry import PackageEntry, PackageManifest, PackageRegistry
from akaribot.testing import Tester, func_case

KNOWN_DIST = "akari-bot-module-purgeable"
UNKNOWN_DIST = "akari-bot-module-absent"


def _entry(dist: str, tables: tuple[str, ...]) -> PackageEntry:
    """构造一个声明了 owned_tables 的模块条目。"""
    return PackageEntry(
        kind="module",
        name="purgeable",
        dist_name=dist,
        version="0.1.0",
        import_path="akaribot.modules.purgeable",
        root=Path("."),
        manifest=PackageManifest(owned_tables=tables),
    )


def _with_registry(entry: PackageEntry):
    """把发现结果替换成单个条目，退出时还原。"""
    return patch.multiple(
        PackageRegistry,
        discover=lambda **kwargs: None,
        modules=lambda: {"module:purgeable": entry},
        adapters=lambda: {},
        incompatible=lambda: {},
    )


def _purge_patches(existing: list[bool], executed: list[str]):
    """把数据库侧换成可观察的桩：init/close、表存在性、连接与 DDL 执行。"""

    class _Context:
        def __init__(self, conn, db_type=None) -> None:
            self.conn = conn

        def quote(self, ident: str) -> str:
            return f'"{ident}"'

        async def execute(self, sql: str, params=None) -> None:
            executed.append(sql)

    return (
        patch("akaribot.core.database.init_db", AsyncMock()),
        patch("akaribot.core.database.close_db", AsyncMock()),
        patch("akaribot.core.database.legacy.has_table", AsyncMock(side_effect=existing)),
        patch("akaribot.core.database.migration.MigrationContext", _Context),
        patch("tortoise.Tortoise.get_connection", return_value=object()),
    )


def _test_declared_tables_come_from_manifest():
    """表名只从 manifest 读，调用方无从注入别的表名。"""
    with _with_registry(_entry(KNOWN_DIST, ("module_purgeable_a", "module_purgeable_b"))):
        tables = db._owned_tables(KNOWN_DIST)
    return tables == ("module_purgeable_a", "module_purgeable_b")


def _test_unknown_distribution_is_rejected():
    """未安装的分发必须报错，而不是返回空表名悄悄成功。"""
    with _with_registry(_entry(KNOWN_DIST, ("module_purgeable_a",))):
        try:
            db._owned_tables(UNKNOWN_DIST)
        except db.PurgeError as error:
            return UNKNOWN_DIST in str(error)
    return False


def _test_package_without_declared_tables_is_rejected():
    """清单没声明任何表时报错，避免把「无表可删」误当成「已清理干净」。"""
    with _with_registry(_entry(KNOWN_DIST, ())):
        try:
            db._owned_tables(KNOWN_DIST)
        except db.PurgeError as error:
            return "owned_tables" in str(error)
    return False


async def _test_purge_drops_only_existing_declared_tables():
    """只对存在的声明表发 DROP，缺失的表记入 missing 而不是发语句。"""
    executed: list[str] = []
    patches = _purge_patches([True, False], executed)
    with (
        patches[0],
        patches[1],
        patches[2],
        patches[3],
        patches[4],
        patch.object(db, "_owned_tables", return_value=("module_present", "module_absent")),
    ):
        result = await db._purge(KNOWN_DIST)
    return result == {
        "dist": KNOWN_DIST,
        "dropped": ["module_present"],
        "missing": ["module_absent"],
    } and executed == ['DROP TABLE IF EXISTS "module_present";']


async def _test_missing_tables_are_idempotent_success():
    """全部表都不存在时仍以 0 退出：契约是「这些表不再存在」，已经达成。"""
    stdout = io.StringIO()
    patches = _purge_patches([False], [])
    with (
        patches[0],
        patches[1],
        patches[2],
        patches[3],
        patches[4],
        patch.object(db, "_owned_tables", return_value=("module_gone",)),
        redirect_stdout(stdout),
    ):
        code = await asyncio.to_thread(db.main, ["purge", "--package", KNOWN_DIST, "--json"])
    payload = json.loads(stdout.getvalue())
    return code == 0 and payload["dropped"] == [] and payload["missing"] == ["module_gone"]


async def _test_failure_still_emits_structured_reason_on_stdout():
    """--json 下失败原因也要进 stdout：调用方解析的是 stdout，只给 stderr 它拿不到原因。"""
    stdout = io.StringIO()
    with _with_registry(_entry(KNOWN_DIST, ("module_purgeable_a",))), redirect_stdout(stdout):
        code = await asyncio.to_thread(db.main, ["purge", "--package", UNKNOWN_DIST, "--json"])
    payload = json.loads(stdout.getvalue())
    return code == 2 and UNKNOWN_DIST in payload["error"] and payload["dropped"] == []


def _test_human_output_reports_missing_tables():
    """非 JSON 输出要把「本就不存在」讲清楚，不能只说删了 0 张。"""
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        db._emit_purge({"dist": KNOWN_DIST, "dropped": ["a"], "missing": ["b"]}, False)
    text = stdout.getvalue()
    return "已删除 1 张表" in text and "b" in text


@func_case
async def test_entrypoint_db_purge(tester: Tester):
    """core.entrypoints.db: 卸载清理入口测试"""
    await tester.test(_test_declared_tables_come_from_manifest, "表名只来自 manifest")
    await tester.test(_test_unknown_distribution_is_rejected, "未安装分发被拒绝")
    await tester.test(_test_package_without_declared_tables_is_rejected, "未声明表的包被拒绝")
    await tester.test(_test_purge_drops_only_existing_declared_tables, "只删存在的声明表")
    await tester.test(_test_missing_tables_are_idempotent_success, "表已不存在时幂等成功")
    await tester.test(_test_failure_still_emits_structured_reason_on_stdout, "失败原因进 stdout")
    await tester.test(_test_human_output_reports_missing_tables, "人类可读输出说明缺失表")
    return tester
