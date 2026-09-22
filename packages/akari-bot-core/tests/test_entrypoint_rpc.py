"""包变更 RPC 入口（``entrypoints/rpc.py``）的白名单、真实投递与失败分类。

热装载与热拆卸本身由 core 既有的 ``post_package_install`` / ``post_package_remove`` 实现，本文件
验证 CLI 经该入口把请求投递到运行中的 Server 并拿到可区分的结果：白名单在导入 core 之前生效，
投递走真实契约与真实处理器，端到端用例另起一个真实 Server 进程在隔离实例里做完整热装载与热拆卸。

未覆盖：``ModulesManager.install_package`` 自身失败与取消时的回滚路径。
"""

import asyncio
import io
import json
import os
import shutil
import sys
from contextlib import asynccontextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from akaribot.core.constants import Info
from akaribot.core.entrypoints import rpc
from akaribot.core.loader import ModulesManager
from akaribot.core.paths import Paths
from akaribot.core.queue.base import JobQueueBase
from akaribot.core.queue.memory import InMemoryBroker, InMemoryJobQueueBackend
from akaribot.core.queue.server import JobQueueServer
from akaribot.core.registry import PackageEntry, PackageRegistry
from akaribot.testing import Tester, func_case


def _production_handlers() -> dict:
    """生产 Server 上已绑定的两个包变更处理器（wire 名 → dispatch）。"""
    return {
        "server.post_package_install": JobQueueServer.handlers["server.post_package_install"],
        "server.post_package_remove": JobQueueServer.handlers["server.post_package_remove"],
    }


@asynccontextmanager
async def _stack(*, server: bool = True, handlers: dict | None = None):
    """在共享内存后端上装配「入口的临时 CLI peer + 可选 Server peer」。

    入口按实例配置选择后端；测试改用共享内存后端，并让「是否需要连数据库」的分支落在非 database
    一侧，避免触碰测试进程已初始化的内存库。

    :param server: 是否起一个 service 为 ``Server`` 的 peer（入口按该 service 名定位实例）。
    :param handlers: 该 peer 的 wire 处理器；缺省挂生产 Server 的真实 dispatch。
    """
    from akaribot.core.config.jobqueue import JobQueueConfig
    from akaribot.core.queue import backend as backend_module

    broker = InMemoryBroker()
    had_config_value = "jobqueue_backend" in JobQueueConfig.__dict__
    previous_config_value = JobQueueConfig.__dict__.get("jobqueue_backend")
    previous_factory = backend_module.create_jobqueue_backend
    previous_peer = (Info.peer_id, Info.peer_role)
    peers: list[type[JobQueueBase]] = []
    pollers: list[asyncio.Task] = []

    if server:

        class ServerPeer(JobQueueBase):
            name = f"TEST-SERVER-{uuid4()}"
            POLL_INTERVAL_SECONDS = 0.001
            backend = InMemoryJobQueueBackend(broker)

        ServerPeer.configure_peer(role="server", service="Server", capabilities=["rpc"])
        for method, handler in (handlers if handlers is not None else _production_handlers()).items():
            ServerPeer.register(method, handler)
        peers.append(ServerPeer)

    JobQueueConfig.jobqueue_backend = "memory"
    backend_module.create_jobqueue_backend = lambda *args, **kwargs: InMemoryJobQueueBackend(broker)
    try:
        pollers = [asyncio.create_task(peer.check_job_queue()) for peer in peers]
        await asyncio.gather(*(peer.wait_ready(timeout=1) for peer in peers))
        yield peers[0] if peers else None
    finally:
        backend_module.create_jobqueue_backend = previous_factory
        if had_config_value:
            JobQueueConfig.jobqueue_backend = previous_config_value
        else:
            del JobQueueConfig.jobqueue_backend
        Info.peer_id, Info.peer_role = previous_peer
        await asyncio.gather(*(peer.begin_shutdown() for peer in peers), return_exceptions=True)
        await asyncio.gather(*(peer.cancel_process_tasks() for peer in peers), return_exceptions=True)
        for poller in pollers:
            poller.cancel()
        await asyncio.gather(*pollers, return_exceptions=True)


def _emit(outcome: rpc.Outcome) -> tuple[int, dict, str]:
    """调用入口的写出逻辑并取回退出码、JSON 载荷与 stderr 文本。"""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = rpc._emit(outcome)
    payload = json.loads(out.getvalue().strip().splitlines()[-1])
    return code, payload, err.getvalue()


async def _test_usage_rejects_unknown_remote():
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = rpc.main(["server.post_package_nuke", "akari-bot-module-dice"])
    # 白名单若失效，main 会在运行中的事件循环里调 asyncio.run 而抛错，本用例随之变红。
    direct = await rpc._run("server.post_package_nuke", "akari-bot-module-dice")
    return (
        code == rpc.EXIT_USAGE
        and out.getvalue() == ""
        and "server.post_package_nuke" in err.getvalue()
        and "server.post_package_install" in err.getvalue()
        and direct.status == rpc.STATUS_USAGE
        and direct.exit_code == rpc.EXIT_USAGE
        and direct.result is None
    )


async def _test_subprocess_entry_contract():
    async def run(*args: str) -> tuple[int, str, str]:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "akaribot.core.entrypoints.rpc",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await asyncio.wait_for(process.communicate(), timeout=60)
        return process.returncode, out.decode(), err.decode()

    help_code, help_out, _ = await run("--help")
    unknown_code, unknown_out, unknown_err = await run("server.post_package_nuke", "x")
    return (
        help_code == 0
        and "server.post_package_install" in help_out
        and unknown_code == rpc.EXIT_USAGE
        and unknown_out.strip() == ""
        and "未知的 remote" in unknown_err
    )


async def _test_not_running_without_server_peer():
    async with _stack(server=False):
        outcome = await rpc._run("server.post_package_install", "akari-bot-module-dice", timeout=2)
        code, payload, _ = _emit(outcome)
    return (
        outcome.status == rpc.STATUS_NOT_RUNNING
        and outcome.exit_code == rpc.EXIT_NOT_RUNNING
        and code == rpc.EXIT_NOT_RUNNING
        and payload["ok"] is False
        and payload["result"] is None
        and payload["remote"] == "server.post_package_install"
        and payload["dist"] == "akari-bot-module-dice"
    )


async def _test_delivered_to_production_handlers():
    calls: list[tuple[str, str]] = []
    originals = (ModulesManager.install_package, ModulesManager.remove_package)

    async def fake_install(entry):
        calls.append(("install", entry.dist_name))
        return True

    async def fake_remove(entry):
        calls.append(("remove", entry.dist_name))
        return True

    ModulesManager.install_package = fake_install
    ModulesManager.remove_package = fake_remove
    try:
        PackageRegistry.discover(force=True)
        entry = next(item for item in PackageRegistry.modules().values() if item.dist_name)
        async with _stack():
            install = await rpc._run("server.post_package_install", entry.dist_name, timeout=5)
            install_code, install_payload, _ = _emit(install)
            remove = await rpc._run("server.post_package_remove", entry.dist_name, timeout=5)
            remove_code, remove_payload, _ = _emit(remove)
    finally:
        ModulesManager.install_package, ModulesManager.remove_package = originals

    # 断言处理器收到的是调用方给的分发，而不是把 dist 丢在路上的空结果。
    return (
        install.status == rpc.STATUS_DELIVERED
        and install.result is True
        and install_code == rpc.EXIT_OK
        and install_payload["ok"] is True
        and remove.status == rpc.STATUS_DELIVERED
        and remove.result is True
        and remove_code == rpc.EXIT_OK
        and remove_payload["status"] == rpc.STATUS_DELIVERED
        and calls == [("install", entry.dist_name), ("remove", entry.dist_name)]
    )


async def _test_rejected_when_package_not_registered():
    async with _stack():
        outcome = await rpc._run("server.post_package_install", "akari-bot-module-definitely-absent", timeout=5)
        code, payload, _ = _emit(outcome)
    return (
        outcome.status == rpc.STATUS_REJECTED
        and outcome.result is False
        and outcome.exit_code == rpc.EXIT_REJECTED
        and code == rpc.EXIT_REJECTED
        and payload["ok"] is False
        and payload["result"] is False
    )


async def _test_timeout_is_distinct():
    async def slow(_payload):
        await asyncio.sleep(5)
        return True

    async with _stack(handlers={"server.post_package_install": slow}):
        outcome = await rpc._run("server.post_package_install", "akari-bot-module-dice", timeout=0.3)
        code, payload, _ = _emit(outcome)
    return (
        outcome.status == rpc.STATUS_TIMEOUT
        and outcome.result is None
        and outcome.exit_code == rpc.EXIT_TIMEOUT
        and code == rpc.EXIT_TIMEOUT
        and payload["ok"] is False
        and payload["result"] is None
    )


def _pick_hot_install_target() -> PackageEntry | None:
    """挑一个用于端到端热装载的已装模块包。

    优先 arcaea_rss：它声明了一个计划任务，能一并验证 Scheduler 的注册与拆除；缺失时退回任意
    声明了 ``provides_modules`` 的模块包，用例对包名保持无关。
    """
    PackageRegistry.discover(force=True)
    candidates = [
        entry for entry in PackageRegistry.modules().values() if entry.dist_name and entry.manifest.provides_modules
    ]
    preferred = [entry for entry in candidates if entry.dist_name == "akari-bot-module-arcaea_rss"]
    return (preferred or sorted(candidates, key=lambda entry: entry.dist_name))[0] if candidates else None


class _ServerProcess:
    """隔离实例里的真实 Server peer 子进程，经 stdin 请求状态快照。"""

    def __init__(self, process: asyncio.subprocess.Process) -> None:
        self.process = process

    @classmethod
    async def start(cls, instance: Path, import_path: str) -> "_ServerProcess":
        worker = Path(__file__).parent / "helpers" / "rpc_server_worker.py"
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            str(worker),
            str(instance),
            import_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "AKARI_INSTANCE_DIR": str(instance), "PYTHONIOENCODING": "UTF-8"},
        )
        server = cls(process)
        line = await asyncio.wait_for(process.stdout.readline(), timeout=90)
        if line.strip() != b"READY":
            raise AssertionError(f"Server peer 未就绪：{line!r} {await process.stderr.read()!r}")
        return server

    async def snapshot(self) -> dict:
        self.process.stdin.write(b"snapshot\n")
        await self.process.stdin.drain()
        while True:
            line = await asyncio.wait_for(self.process.stdout.readline(), timeout=60)
            if not line:
                raise AssertionError(f"Server peer 提前退出：{await self.process.stderr.read()!r}")
            if line.startswith(b"STATE "):
                return json.loads(line[6:])

    async def close(self) -> None:
        if self.process.returncode is None:
            try:
                self.process.stdin.write(b"quit\n")
                await self.process.stdin.drain()
            except (BrokenPipeError, ConnectionResetError):
                pass
            try:
                await asyncio.wait_for(self.process.wait(), timeout=30)
            except TimeoutError:
                self.process.kill()
                await self.process.wait()
        await self.process.stderr.read()


async def _call_entry(instance: Path, remote: str, dist: str) -> tuple[int, dict, str]:
    """以真实子进程调用入口，返回退出码、结果 JSON 与 stderr。"""
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "akaribot.core.entrypoints.rpc",
        remote,
        dist,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "AKARI_INSTANCE_DIR": str(instance), "PYTHONIOENCODING": "UTF-8"},
    )
    out, err = await asyncio.wait_for(process.communicate(), timeout=120)
    return process.returncode, json.loads(out.decode().strip().splitlines()[-1]), err.decode()


async def _test_end_to_end_hot_install_and_remove():
    entry = _pick_hot_install_target()
    source_config = Paths.instance / "config"
    if entry is None or not source_config.is_dir():
        # 环境缺少已装模块包或仓库实例配置时无法搭建隔离实例，明确告警而不是假装通过。
        print("跳过端到端热装载用例：缺少已装模块包或仓库 config/ 目录。", file=sys.stderr)
        return True

    with TemporaryDirectory(prefix="akari-rpc-e2e-") as directory:
        instance = Path(directory)
        shutil.copytree(source_config, instance / "config")
        for name in ("data", "logs", "cache", "database"):
            (instance / name).mkdir()
        server = await _ServerProcess.start(instance, entry.import_path)
        try:
            before = await server.snapshot()
            install_code, install_payload, _ = await _call_entry(
                instance, "server.post_package_install", entry.dist_name
            )
            loaded = await server.snapshot()
            remove_code, remove_payload, _ = await _call_entry(instance, "server.post_package_remove", entry.dist_name)
            unloaded = await server.snapshot()
        finally:
            await server.close()

    # 安装后注册表、sys.modules、Scheduler 与 module_status 必须与包声明一致；拆除后必须全部复原。
    return (
        before["registered"] == []
        and before["sys_modules"] == []
        and install_code == 0
        and install_payload["status"] == rpc.STATUS_DELIVERED
        and install_payload["result"] is True
        and loaded["provided"] == list(entry.manifest.provides_modules)
        and loaded["registered"] == sorted(entry.manifest.provides_modules)
        and loaded["sys_modules"]
        and loaded["scheduler_jobs"] == loaded["declared_jobs"]
        and set(loaded["module_status"]) == set(entry.manifest.provides_modules)
        and all(loaded["module_status"].values())
        and remove_code == 0
        and remove_payload["status"] == rpc.STATUS_DELIVERED
        and unloaded["registered"] == []
        and unloaded["sys_modules"] == []
        and unloaded["module_status"] == {}
        and not any(unloaded["scheduler_jobs"].values())
    )


@func_case
async def test_entrypoint_rpc(tester: Tester):
    """包变更 RPC 入口的白名单、真实投递与失败分类。"""
    await tester.test(_test_usage_rejects_unknown_remote, "未知 remote 被白名单拒绝，且不触发投递")
    await tester.test(_test_subprocess_entry_contract, "真实子进程入口的 --help 与未知 remote 退出码")
    await tester.test(_test_not_running_without_server_peer, "没有在线 Server peer 时判为实例未运行")
    await tester.test(_test_delivered_to_production_handlers, "经真实契约投递到生产处理器并回传结果")
    await tester.test(_test_rejected_when_package_not_registered, "包未注册时远端返回 False")
    await tester.test(_test_timeout_is_distinct, "超时与未运行、远端拒绝可区分")
    await tester.test(_test_end_to_end_hot_install_and_remove, "真实 Server 进程的热装载与热拆卸改到运行态")
    return tester
