"""模块包热装载与热拆卸的 RPC 入口。

供 CLI 以子进程调用：``python -m akaribot.core.entrypoints.rpc <remote> <dist>``。``remote`` 只接受
``server.post_package_install`` 与 ``server.post_package_remove``，即 ``ServerAPI`` 上已有的两个固定
契约；方法名由本模块的白名单给出，不接受调用方拼接任意 RPC 名。

热装载与热拆卸都必须在运行中的 Server 内执行（独立进程里没有模块索引、调度器与数据库 context），
故本进程只做一次 RPC 并等待确认。stdout 只放一行结果 JSON，说明与日志走 stderr。

退出码：0 成功、1 投递或后端失败、2 用法错误、3 实例未运行、4 远端拒绝、5 超时。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass

# 等 Server 确认的秒数上限。契约声明的是 7200 秒（热装载要导入依赖并重挂数据库 context），但
# Server 掉线而租约未过期时无人认领消息，按契约等下去会把 CLI 挂住两小时，故在此收紧。
RPC_TIMEOUT_SECONDS = 300

# peer 注册与就绪的秒数上限；超时说明实例的 JobQueue 不可达。
PEER_READY_TIMEOUT_SECONDS = 15

# 白名单：remote 到固定契约的对应关系。新增包变更动作时必须在此登记，不得由调用方拼方法名。
REMOTE_METHODS = {
    "server.post_package_install": "install",
    "server.post_package_remove": "remove",
}

STATUS_DELIVERED = "delivered"
STATUS_REJECTED = "rejected"
STATUS_NOT_RUNNING = "not_running"
STATUS_TIMEOUT = "timeout"
STATUS_USAGE = "usage"
STATUS_ERROR = "error"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_NOT_RUNNING = 3
EXIT_REJECTED = 4
EXIT_TIMEOUT = 5

_EXIT_CODES = {
    STATUS_DELIVERED: EXIT_OK,
    STATUS_REJECTED: EXIT_REJECTED,
    STATUS_NOT_RUNNING: EXIT_NOT_RUNNING,
    STATUS_TIMEOUT: EXIT_TIMEOUT,
    STATUS_USAGE: EXIT_USAGE,
    STATUS_ERROR: EXIT_FAILED,
}


class InstanceUnreachable(RuntimeError):
    """运行中的 Server 实例不可达。"""


@dataclass(frozen=True, slots=True)
class Outcome:
    """一次包变更 RPC 的结果，同时决定 JSON 载荷与退出码。

    :param remote: 契约名。
    :param dist: 分发名。
    :param status: :data:`STATUS_DELIVERED` 等状态之一。
    :param result: 远端返回值；未取得结果时为 ``None``。
    :param detail: 面向调用者的原因说明。
    """

    remote: str
    dist: str
    status: str
    result: bool | None
    detail: str

    @property
    def exit_code(self) -> int:
        """本结果对应的进程退出码。"""
        return _EXIT_CODES[self.status]

    def payload(self) -> dict:
        """结果 JSON 载荷。"""
        return {
            "ok": self.status == STATUS_DELIVERED,
            "status": self.status,
            "remote": self.remote,
            "dist": self.dist,
            "result": self.result,
            "detail": self.detail,
        }


async def _connect_database_if_needed() -> bool:
    from akaribot.core.config.jobqueue import JobQueueConfig

    if JobQueueConfig.jobqueue_backend.strip().lower() != "database":
        return False
    from akaribot.core.database import init_db

    await init_db(load_module_db=False, generate_schemas=False)
    return True


async def _deliver(remote: str, dist: str, timeout: float) -> bool:
    from akaribot.core.queue.backend import create_jobqueue_backend
    from akaribot.core.queue.base import JobQueueBase
    from akaribot.core.queue.contracts import ServerAPI
    from akaribot.core.queue.peer import PeerSelector

    endpoints = {
        "server.post_package_install": ServerAPI.post_package_install,
        "server.post_package_remove": ServerAPI.post_package_remove,
    }

    class CliPeer(JobQueueBase):
        """一次性 RPC 调用方；只发一次请求，不绑定任何远端处理器。"""

    poller = None
    database_connected = False
    try:
        try:
            # 后端与 peer 的装配失败与「连不上」对操作者是同一件事：实例的 JobQueue 用不了。
            database_connected = await _connect_database_if_needed()
            CliPeer.configure_backend(create_jobqueue_backend())
            CliPeer.configure_peer(role="cli", service="CLI", capabilities=["rpc"])
        except Exception as exc:  # noqa: BLE001 - 配置未生成或后端不可用，实例同样不可达
            raise InstanceUnreachable(f"JobQueue 后端不可用：{exc}") from exc
        poller = asyncio.create_task(CliPeer.check_job_queue())
        try:
            await CliPeer.wait_ready(timeout=PEER_READY_TIMEOUT_SECONDS)
            servers = await CliPeer.registry.resolve(PeerSelector.service("Server"))
        except Exception as exc:  # noqa: BLE001 - 连不上 JobQueue 与实例未运行对操作者是同一件事
            raise InstanceUnreachable(str(exc) or exc.__class__.__name__) from exc
        if not servers:
            raise InstanceUnreachable("JobQueue 注册表里没有在线的 Server 实例")
        return bool(await endpoints[remote].using(CliPeer).with_timeout(timeout)(dist=dist))
    finally:
        if poller is not None:
            poller.cancel()
            await asyncio.gather(poller, return_exceptions=True)
        if database_connected:
            from akaribot.core.database import close_db

            await close_db()


async def _run(remote: str, dist: str, *, timeout: float = RPC_TIMEOUT_SECONDS) -> Outcome:
    if remote not in REMOTE_METHODS:
        return Outcome(remote, dist, STATUS_USAGE, None, f"未知的 remote：{remote!r}，不在固定白名单内。")

    from akaribot.core.queue.errors import RpcError, RpcTimeoutError

    try:
        result = await _deliver(remote, dist, timeout)
    except InstanceUnreachable as exc:
        return Outcome(remote, dist, STATUS_NOT_RUNNING, None, f"实例未运行：{exc}")
    except RpcTimeoutError as exc:
        # 超时是「结果未知」：远端可能已经改了状态，调用方不得当作未发生。
        return Outcome(remote, dist, STATUS_TIMEOUT, None, f"已投递，但 {timeout:g} 秒内未收到实例确认：{exc}")
    except RpcError as exc:
        return Outcome(remote, dist, STATUS_ERROR, None, f"投递失败：{exc}")
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        return Outcome(remote, dist, STATUS_ERROR, None, f"投递失败：{exc.__class__.__name__}: {exc}")

    if not result:
        return Outcome(remote, dist, STATUS_REJECTED, False, "实例拒绝本次变更：包未注册，或另有热重载正在进行。")
    return Outcome(remote, dist, STATUS_DELIVERED, True, "实例已确认完成本次变更。")


def _emit(outcome: Outcome) -> int:
    json.dump(outcome.payload(), sys.stdout, ensure_ascii=False, default=str)
    sys.stdout.write("\n")
    print(outcome.detail, file=sys.stderr)
    return outcome.exit_code


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.rpc",
        description="把模块包的安装或卸载事件交给运行中的 Server 热装载/热拆卸。",
    )
    parser.add_argument("remote", help="固定契约名：server.post_package_install 或 server.post_package_remove")
    parser.add_argument("dist", help="分发名，如 akari-bot-module-wiki")
    args = parser.parse_args(argv)

    # 白名单在导入 core 之前判：既避免为一次误用拉起整套运行时，也不给拼接方法名留入口。
    if args.remote not in REMOTE_METHODS:
        accepted = "、".join(sorted(REMOTE_METHODS))
        print(f"未知的 remote {args.remote!r}：只接受 {accepted}。", file=sys.stderr)
        return EXIT_USAGE

    return _emit(asyncio.run(_run(args.remote, args.dist)))


if __name__ == "__main__":
    sys.exit(main())
