"""端到端热装载用例的 Server 侧进程：真实 ``JobQueueServer`` 与真实包变更处理器。

父用例经 stdin 逐行下达 ``snapshot`` / ``quit``；每条 ``snapshot`` 输出一行 ``STATE`` JSON。实例根
由父用例注入 ``AKARI_INSTANCE_DIR``，数据库因此落在临时实例内，不触碰仓库或调用方的实例。

本文件会被测试运行器当作测试文件导入，故模块级不得读 ``sys.argv``（与 ``tests/helpers`` 下的
worker 同一约定），全部逻辑收在 ``main()`` 里。
"""

import asyncio
import json
import os
import sys
from pathlib import Path


async def _snapshot(import_path: str) -> None:
    from akaribot.core.database.models import ModuleStatus
    from akaribot.core.loader import ModulesManager
    from akaribot.core.registry import PackageRegistry
    from akaribot.core.scheduler import SchedulerLifecycle

    entry = PackageRegistry.by_import_path(import_path)
    provided = sorted(entry.manifest.provides_modules) if entry is not None else []
    state = {
        "provided": provided,
        "registered": sorted(name for name in provided if name in ModulesManager.modules),
        "declared_jobs": {
            name: len(ModulesManager.modules[name].schedule_list.set)
            for name in provided
            if name in ModulesManager.modules
        },
        "scheduler_jobs": {name: len(specs) for name, specs in SchedulerLifecycle.snapshot_modules(provided).items()},
        "sys_modules": sorted(
            name for name in sys.modules if name == import_path or name.startswith(f"{import_path}.")
        ),
        "module_status": dict(await ModuleStatus.filter(module_name__in=provided).values_list("module_name", "load")),
    }
    print("STATE " + json.dumps(state, ensure_ascii=False), flush=True)


async def main(instance: Path, import_path: str) -> None:
    os.environ["AKARI_INSTANCE_DIR"] = str(instance)

    from akaribot.core.database import close_db, init_db
    from akaribot.core.queue.backend import create_jobqueue_backend
    from akaribot.core.queue.server import JobQueueServer
    from akaribot.core.registry import PackageRegistry
    from akaribot.core.scheduler import SchedulerLifecycle

    await init_db(load_module_db=True, generate_schemas=True)
    SchedulerLifecycle.prepare()
    JobQueueServer.configure_backend(create_jobqueue_backend())
    JobQueueServer.configure_peer(
        role="server", service="Server", capabilities=["rpc", "signals", "modules", "scheduler"]
    )
    poller = asyncio.create_task(JobQueueServer.check_job_queue())
    await JobQueueServer.wait_ready(timeout=30)
    PackageRegistry.discover(force=True)
    print("READY", flush=True)
    try:
        while True:
            command = (await asyncio.to_thread(sys.stdin.readline)).strip()
            if command == "snapshot":
                await _snapshot(import_path)
            elif command == "quit":
                break
    finally:
        poller.cancel()
        await asyncio.gather(poller, return_exceptions=True)
        await close_db()


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]), sys.argv[2]))
