"""数据库连接参数与初始化职责单元测试。"""

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, parse_qsl, urlsplit
from unittest.mock import AsyncMock, patch

import akaribot.core.database as database
import tortoise.context as tortoise_context
from akaribot.core.database.models import JobQueuesTable
from akaribot.core.database.link import prepare_db_link
from akaribot.core.queue.server import JobQueueServer
from akaribot.core.registry import PackageEntry, PackageManifest, PackageRegistry
from akaribot.core.queue.transport import PROTOCOL_VERSION
from akaribot.core.scheduler import Scheduler, SchedulerLifecycle
from akaribot.testing import Tester, func_case
from akaribot.core.types import Module
from akaribot.core.types.module.component_meta import ScheduleMeta
from tortoise.context import TortoiseContext

from apscheduler.triggers.interval import IntervalTrigger


def _query_fields(link: str) -> dict[str, list[str]]:
    return parse_qs(urlsplit(link).query)


def _test_sqlite_defaults_are_added():
    link = prepare_db_link("sqlite://database/save.db")
    fields = _query_fields(link)
    keys = [key for key, _ in parse_qsl(urlsplit(link).query)]
    return (
        fields.get("journal_mode") == ["WAL"]
        and fields.get("busy_timeout") == ["30000"]
        and keys.index("busy_timeout") < keys.index("journal_mode")
    )


def _test_sqlite_explicit_fields_are_preserved():
    link = prepare_db_link("sqlite://database/save.db?journal_mode=DELETE&cache_size=2000&busy_timeout=1000")
    fields = _query_fields(link)
    keys = [key for key, _ in parse_qsl(urlsplit(link).query)]
    return (
        fields.get("busy_timeout") == ["1000"]
        and fields.get("journal_mode") == ["DELETE"]
        and fields.get("cache_size") == ["2000"]
        and keys.index("busy_timeout") < keys.index("journal_mode")
    )


def _test_non_sqlite_link_keeps_existing_behavior():
    link = prepare_db_link("mysql+asyncmy://user:pass@localhost/akari?charset=utf8mb4")
    return link == "mysql://user:pass@localhost/akari?charset=utf8mb4"


def _test_module_database_discovery_follows_file_existence():
    # 清单为空只表示该包没有数据库模型；包内缺少依赖的失败改由 ``init_db()`` 在真正导入
    # 模型时抛出（见下一条用例），不再由发现阶段承担。
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        with_models = root / "with_models"
        (with_models / "database").mkdir(parents=True)
        (with_models / "database" / "models.py").write_text("", encoding="utf-8")
        without_models = root / "without_models"
        (without_models / "database").mkdir(parents=True)
        (without_models / "database" / "__init__.py").write_text("", encoding="utf-8")

        entries = {
            "with_models": PackageEntry(
                kind="module",
                name="with_models",
                dist_name="",
                version="0+local",
                import_path="akaribot.modules.with_models",
                root=with_models,
                manifest=PackageManifest(),
            ),
            "without_models": PackageEntry(
                kind="module",
                name="without_models",
                dist_name="",
                version="0+local",
                import_path="akaribot.modules.without_models",
                root=without_models,
                manifest=PackageManifest(),
            ),
        }
        with patch.object(PackageRegistry, "modules", return_value=entries):
            paths = database.fetch_module_db()
    return paths == ["akaribot.modules.with_models.database.models"]


async def _test_missing_module_dependency_fails_initialization():
    dependency_error = ModuleNotFoundError("No module named 'database_driver'", name="database_driver")
    init = AsyncMock(side_effect=dependency_error)
    old_database_list = database.Temp.data.get("modules_db_list")
    try:
        with (
            patch.object(
                database, "fetch_module_db", return_value=["akaribot.modules.__missing_dependency.database.models"]
            ),
            patch.object(database, "get_db_link", return_value="sqlite://database/save.db"),
            patch.object(database.Tortoise, "init", new=init),
            patch.object(database.Tortoise, "close_connections", new=AsyncMock()),
        ):
            result = await database.init_db()
    finally:
        if old_database_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_database_list
    return result is False and init.await_count == 1


async def _test_runtime_init_does_not_generate_schemas():
    init = AsyncMock()
    generate_schemas = AsyncMock()
    old_database_list = database.Temp.data.get("modules_db_list")
    try:
        with (
            patch.object(database, "fetch_module_db", return_value=["akaribot.modules.example.database.models"]),
            patch.object(database, "get_db_link", return_value="sqlite://database/save.db"),
            patch.object(database.Tortoise, "init", new=init),
            patch.object(database.Tortoise, "generate_schemas", new=generate_schemas),
        ):
            result = await database.init_db()

        config = init.await_args.kwargs["config"]
        return (
            result
            and generate_schemas.await_count == 0
            and config["apps"]["models"]["models"]
            == ["akaribot.core.database.models", "akaribot.modules.example.database.models"]
            and _query_fields(config["connections"]["local"]).get("busy_timeout") == ["30000"]
        )
    finally:
        if old_database_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_database_list


async def _test_pre_init_mode_generates_all_schemas():
    init = AsyncMock()
    generate_schemas = AsyncMock()
    run_migrations = AsyncMock()
    old_database_list = database.Temp.data.get("modules_db_list")
    try:
        with (
            patch.object(database, "fetch_module_db", return_value=["akaribot.modules.example.database.models"]),
            patch.object(database.Tortoise, "init", new=init),
            patch.object(database.Tortoise, "generate_schemas", new=generate_schemas),
            patch.object(database, "run_startup_migrations", new=run_migrations),
        ):
            result = await database.init_db(generate_schemas=True)

        config = init.await_args.kwargs["config"]
        return (
            result
            and generate_schemas.await_count == 1
            and generate_schemas.await_args.kwargs == {"safe": True}
            and run_migrations.await_count == 1
            and "akaribot.modules.example.database.models" in config["apps"]["models"]["models"]
            and config["apps"]["local_models"]["models"] == ["akaribot.core.database.local"]
        )
    finally:
        if old_database_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_database_list


async def _test_failed_init_closes_partial_connections():
    close_connections = AsyncMock()
    old_database_list = database.Temp.data.get("modules_db_list")
    try:
        with (
            patch.object(database, "fetch_module_db", return_value=[]),
            patch.object(database.Tortoise, "init", new=AsyncMock(side_effect=RuntimeError("partial init"))),
            patch.object(database.Tortoise, "close_connections", new=close_connections),
        ):
            result = await database.init_db()
        return result is False and close_connections.await_count == 1
    finally:
        if old_database_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_database_list


async def _test_cancelled_init_closes_partial_connections():
    entered = asyncio.Event()
    close_connections = AsyncMock()

    async def initialize(**kwargs):
        entered.set()
        await asyncio.Event().wait()

    with (
        patch.object(database, "fetch_module_db", return_value=[]),
        patch.object(database.Tortoise, "init", new=initialize),
        patch.object(database.Tortoise, "close_connections", new=close_connections),
    ):
        task = asyncio.create_task(database.init_db())
        await asyncio.wait_for(entered.wait(), timeout=1)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            return close_connections.await_count == 1
    return False


async def _test_init_db_clears_task_local_tortoise_context():
    context = TortoiseContext()
    context.__enter__()
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    try:
        with (
            patch.object(database, "fetch_module_db", return_value=[]),
            patch.object(database.Tortoise, "init", new=AsyncMock(return_value=context)),
        ):
            result = await database.init_db()
        return result and tortoise_context._current_context.get() is None and context._token is None
    finally:
        if context._token is not None:
            context.__exit__(None, None, None)
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


async def _test_activate_db_reload_clears_inherited_old_context():
    old_context = TortoiseContext()
    new_context = TortoiseContext()
    previous_global = tortoise_context._global_context
    token = tortoise_context._current_context.set(old_context)
    prepared = database.PreparedDatabaseReload(
        context=new_context,
        previous_context=old_context,
        database_list=[],
    )
    try:
        database.activate_db_reload(prepared)
        return (
            prepared.activated
            and tortoise_context._global_context is new_context
            and tortoise_context._current_context.get() is None
        )
    finally:
        tortoise_context._global_context = previous_global
        tortoise_context._current_context.reset(token)


async def _test_task_created_after_init_uses_replaceable_global_context():
    old_context = TortoiseContext()
    new_context = TortoiseContext()
    previous_global = tortoise_context._global_context
    token = tortoise_context._current_context.set(None)
    tortoise_context._global_context = old_context
    release = asyncio.Event()
    started = asyncio.Event()

    async def child():
        inherited = tortoise_context._current_context.get()
        started.set()
        await release.wait()
        return inherited, tortoise_context.get_current_context()

    task = asyncio.create_task(child())
    prepared = database.PreparedDatabaseReload(
        context=new_context,
        previous_context=old_context,
        database_list=[],
    )
    try:
        await started.wait()
        database.activate_db_reload(prepared)
        release.set()
        inherited, resolved = await task
        return inherited is None and resolved is new_context
    finally:
        release.set()
        if not task.done():
            task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        tortoise_context._global_context = previous_global
        tortoise_context._current_context.reset(token)


async def _test_reload_activates_prepared_context_before_closing_previous():
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    prepared = object()
    calls = []

    async def prepare(models):
        calls.append(("prepare", models))
        return prepared

    def activate(value):
        calls.append(("activate", value))

    async def close_previous(value):
        calls.append(("close_previous", value))

    try:
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload", new=activate),
            patch.object(database, "close_previous_db_context", new=close_previous),
        ):
            result = await database.reload_db(db_models=["akaribot.modules.example.database.models"])
        return result is True and calls == [
            ("prepare", ["akaribot.modules.example.database.models"]),
            ("activate", prepared),
            ("close_previous", prepared),
        ]
    finally:
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


async def _test_reload_failure_does_not_activate_partial_context():
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    calls = []

    async def prepare(models):
        calls.append(("prepare", models))
        return None

    def activate(value):
        calls.append(("activate", value))

    async def close_previous(value):
        calls.append(("close_previous", value))

    try:
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload", new=activate),
            patch.object(database, "close_previous_db_context", new=close_previous),
        ):
            result = await database.reload_db(db_models=["akaribot.modules.broken.database.models"])
        return result is False and calls == [
            ("prepare", ["akaribot.modules.broken.database.models"]),
        ]
    finally:
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


async def _test_reload_waits_for_other_queue_handlers():
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    started = asyncio.Event()
    release = asyncio.Event()
    prepare_called = asyncio.Event()

    async def handler():
        started.set()
        await release.wait()

    async def prepare(models):
        prepare_called.set()
        return object()

    handler_task = asyncio.create_task(handler(), name="test-database-reload-handler")
    JobQueueServer._process_tasks.add(handler_task)
    await asyncio.wait_for(started.wait(), timeout=1)
    try:
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload"),
            patch.object(database, "close_previous_db_context", new=AsyncMock()),
        ):
            reload_task = asyncio.create_task(database.reload_db())
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            waited = not prepare_called.is_set() and not reload_task.done()
            release.set()
            await handler_task
            result = await asyncio.wait_for(reload_task, timeout=1)
        return waited and result is True and prepare_called.is_set()
    finally:
        release.set()
        if not handler_task.done():
            handler_task.cancel()
        await asyncio.gather(handler_task, return_exceptions=True)
        JobQueueServer._process_tasks.discard(handler_task)
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


async def _test_reload_cancels_scheduler_jobs_before_closing_connections():
    module_name = "__test_database_scheduler_maintenance"
    started = asyncio.Event()
    stopped = asyncio.Event()
    prepare_saw_stopped = []

    async def scheduled():
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            stopped.set()

    async def prepare(models):
        prepare_saw_stopped.append(stopped.is_set())
        return object()

    module = Module.assign(module_name=module_name, alias=None, recommend_modules=None, developers=None)
    module._db_load = True
    module.schedule_list.add(ScheduleMeta(function=scheduled, trigger=IntervalTrigger(hours=1)))
    SchedulerLifecycle.prepare()
    SchedulerLifecycle.reconcile_modules({module_name}, {module_name: module})
    job = Scheduler.get_job(SchedulerLifecycle.module_job_id(module_name, 0))
    task = asyncio.create_task(job.func())
    try:
        await asyncio.wait_for(started.wait(), timeout=1)
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload"),
            patch.object(database, "close_previous_db_context", new=AsyncMock()),
        ):
            result = await database.reload_db()
        return result is True and stopped.is_set() and task.done() and prepare_saw_stopped == [True]
    finally:
        if not task.done():
            task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        SchedulerLifecycle._remove_modules({module_name})


async def _test_reload_keeps_pumping_remote_results():
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    old_is_running = JobQueueServer.is_running
    result_task_id = await JobQueuesTable.add_task("QUEUE-REMOTE", "reload-result", {})
    result_task_id = str(result_task_id)
    await JobQueuesTable.filter(task_id=result_task_id).update(
        status="done", result={"rpc": PROTOCOL_VERSION, "value": {"ready": True}}
    )
    handler_done = asyncio.Event()

    waiter = asyncio.get_running_loop().create_future()
    JobQueueServer._pending[result_task_id] = waiter

    async def handler():
        result = await waiter
        if result.envelope == {"rpc": PROTOCOL_VERSION, "value": {"ready": True}}:
            handler_done.set()

    async def prepare(models):
        return object()

    handler_task = asyncio.create_task(handler(), name="test-database-reload-remote-waiter")
    JobQueueServer._process_tasks.add(handler_task)

    reload_task = None
    poller_task = None
    try:
        JobQueueServer.is_running = False
        JobQueueServer.pause_event.set()
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload"),
            patch.object(database, "close_previous_db_context", new=AsyncMock()),
        ):
            reload_task = asyncio.create_task(database.reload_db())
            while JobQueueServer.pause_event.is_set() and not reload_task.done():
                await asyncio.sleep(0)
            if reload_task.done():
                return False

            poller_task = asyncio.create_task(
                JobQueueServer.check_job_queue(),
                name="test-database-reload-result-poller",
            )
            result = await asyncio.wait_for(reload_task, timeout=1)
            await asyncio.wait_for(handler_done.wait(), timeout=1)
            return result is True and handler_task.done()
    finally:
        if reload_task is not None and not reload_task.done():
            reload_task.cancel()
        if poller_task is not None and not poller_task.done():
            poller_task.cancel()
        await asyncio.gather(
            *(task for task in (reload_task, poller_task, handler_task) if task is not None),
            return_exceptions=True,
        )
        JobQueueServer._process_tasks.discard(handler_task)
        JobQueueServer._pending.pop(result_task_id, None)
        await JobQueuesTable.filter(task_id=result_task_id).delete()
        JobQueueServer.pause_event.set()
        JobQueueServer.is_running = old_is_running
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


async def _test_cancelled_reload_does_not_publish_partial_context():
    old_modules_db_list = database.Temp.data.get("modules_db_list")
    entered = asyncio.Event()
    calls = []

    async def prepare(models):
        calls.append(("prepare", models))
        entered.set()
        await asyncio.Event().wait()

    def activate(value):
        calls.append(("activate", value))

    async def close_previous(value):
        calls.append(("close_previous", value))

    try:
        with (
            patch.object(database, "prepare_db_reload", new=prepare),
            patch.object(database, "activate_db_reload", new=activate),
            patch.object(database, "close_previous_db_context", new=close_previous),
        ):
            task = asyncio.create_task(database.reload_db(db_models=["akaribot.modules.cancelled.database.models"]))
            await asyncio.wait_for(entered.wait(), timeout=1)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                cancelled = True
            else:
                cancelled = False

        return (
            cancelled
            and calls
            == [
                ("prepare", ["akaribot.modules.cancelled.database.models"]),
            ]
            and JobQueueServer.pause_event.is_set()
        )
    finally:
        if old_modules_db_list is None:
            database.Temp.data.pop("modules_db_list", None)
        else:
            database.Temp.data["modules_db_list"] = old_modules_db_list


@func_case
async def test_database_init(tester: Tester):
    """SQLite 参数自动补全，且仅 pre-init 模式执行建表。"""
    await tester.test(_test_sqlite_defaults_are_added, "SQLite 缺失参数自动补全")
    await tester.test(_test_sqlite_explicit_fields_are_preserved, "SQLite 显式参数保持不变")
    await tester.test(_test_non_sqlite_link_keeps_existing_behavior, "非 SQLite 连接保持现有行为")
    await tester.test(_test_module_database_discovery_follows_file_existence, "模块数据库发现按 models.py 是否存在")
    await tester.test(_test_missing_module_dependency_fails_initialization, "模块模型缺依赖时初始化失败")
    await tester.test(_test_runtime_init_does_not_generate_schemas, "运行期初始化不执行建表")
    await tester.test(_test_pre_init_mode_generates_all_schemas, "pre-init 建立核心、local 与模块表")
    await tester.test(_test_failed_init_closes_partial_connections, "数据库初始化失败清理部分连接")
    await tester.test(_test_cancelled_init_closes_partial_connections, "数据库初始化取消清理部分连接")
    await tester.test(_test_init_db_clears_task_local_tortoise_context, "数据库初始化清理任务级 context")
    await tester.test(
        _test_activate_db_reload_clears_inherited_old_context,
        "数据库切换不继承旧任务级 context",
    )
    await tester.test(
        _test_task_created_after_init_uses_replaceable_global_context,
        "初始化后任务使用可替换 global context",
    )
    await tester.test(
        _test_reload_activates_prepared_context_before_closing_previous,
        "热重载先准备新 context 再原子切换",
    )
    await tester.test(_test_reload_failure_does_not_activate_partial_context, "热重载失败不发布半成品 context")
    await tester.test(_test_reload_waits_for_other_queue_handlers, "热重载等待其它队列处理器")
    await tester.test(_test_reload_cancels_scheduler_jobs_before_closing_connections, "热重载先排空计划任务")
    await tester.test(_test_reload_keeps_pumping_remote_results, "热重载暂停时继续回收远端结果")
    await tester.test(
        _test_cancelled_reload_does_not_publish_partial_context,
        "数据库热重载取消不发布半成品 context",
    )
    return tester
