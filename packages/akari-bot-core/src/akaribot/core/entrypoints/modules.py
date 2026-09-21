"""模块全局装载入口。

供 CLI 与 TUI 以子进程调用：``list`` 读 ``module_status``；``load`` / ``unload`` 经 JobQueue RPC
交给运行中的 Server 执行 ``ModulesManager.load_module()`` / ``unload_module()``。这两个函数要在
队列与调度器的维护窗口内改本进程的模块索引，独立进程里索引为空，直接调用只会返回 False。
stdout 只放结果，提示与日志走 stderr；退出码 0 成功、1 运行期失败、2 用户错误。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

# 等 Server 确认的秒数上限。热装载要排空队列并让出调度器窗口，故高于普通查询。
RPC_TIMEOUT_SECONDS = 60

# peer 注册与就绪的秒数上限；超时说明实例的 JobQueue 不可达。
PEER_READY_TIMEOUT_SECONDS = 15

# 实例未运行时的统一提示，与 CLI 侧同文案，避免两处说法不一致。
INSTANCE_STOPPED_HINT = "实例未运行，无法热装载；下次启动会自动装载。"


class InstanceUnreachable(RuntimeError):
    """运行中的 Server 实例不可达。"""


async def _status() -> dict[str, bool]:
    """读取 ``module_status`` 表。

    表缺席表示实例尚未完成过一次启动，与状态为空对操作者是同一件事，故一并返回空映射。

    :return: 模块名到 ``module_status.load`` 的映射。
    """
    from akaribot.core.database import close_db, init_db
    from akaribot.core.database.models import ModuleStatus

    await init_db(load_module_db=False, generate_schemas=False)
    try:
        try:
            return dict(await ModuleStatus.all().values_list("module_name", "load"))
        except Exception as exc:  # noqa: BLE001 - 状态表不可读时降级为「无记录」，原因照实输出
            print(f"模块状态表不可读（{exc}），只列出发现层声明的模块。", file=sys.stderr)
            return {}
    finally:
        await close_db()


def _declared() -> dict[str, str]:
    """取发现层声明的模块名及其分发名。

    清单里的 ``provides_modules`` 覆盖 bundled 模块与已装模块包；它声明为空的包只有运行期才
    知道注册名，这类包不产生条目，其模块名由状态表补上，分发名留空。

    :return: 模块名到分发名的映射。
    """
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    declared: dict[str, str] = {}
    for entry in PackageRegistry.modules().values():
        dist = entry.dist_name or f"akari-bot-module-{entry.name}"
        for name in entry.manifest.provides_modules:
            declared.setdefault(name, dist)
    return declared


def collect() -> tuple[list[dict], str]:
    """汇总各注册模块的全局装载状态。

    模块名取「发现层声明」与「状态表已有记录」的并集：前者覆盖已装模块包，后者覆盖 bundled
    模块；``loaded`` 只在状态表有记录时才是布尔值，无记录用 ``null`` 表示尚未初始化。

    :return: 二元组——按名字排序的 ``{name, loaded, installed_dist}`` 列表；需要提示给操作者的说明。
    """
    declared = _declared()
    status = asyncio.run(_status())
    # 下划线开头的是框架内部注册（解析器策略、错误处理等），不是用户可装载的模块，列出只会成为噪声。
    names = sorted(name for name in set(declared) | set(status) if not name.startswith("_"))
    items = [
        {"name": name, "loaded": status.get(name), "installed_dist": declared.get(name, "")} for name in names
    ]
    note = "" if status else "状态表暂无记录：实例尚未完成过一次启动，下次启动按默认装载。"
    return items, note


async def _connect_database_if_needed() -> bool:
    """数据库后端与运行中的实例共用队列表，须先接上库连接。

    :return: 是否已建立连接（调用方据此决定收尾时是否关闭）。
    """
    from akaribot.core.config.jobqueue import JobQueueConfig

    if JobQueueConfig.jobqueue_backend.strip().lower() != "database":
        return False
    from akaribot.core.database import init_db

    await init_db(load_module_db=False, generate_schemas=False)
    return True


async def _notify_server(module: str, action: str) -> bool:
    """把全局装载动作交给运行中的 Server 执行。

    本进程只做一次 RPC：注册为临时 peer 以便收结果，不改任何模块索引，也不写状态表。

    :param module: 模块名。
    :param action: ``load`` 或 ``unload``。
    :return: Server 报告的结果。
    :raises InstanceUnreachable: JobQueue 不可达，或注册表里没有在线的 Server 实例。
    """
    from akaribot.core.queue.backend import create_jobqueue_backend
    from akaribot.core.queue.base import JobQueueBase
    from akaribot.core.queue.contracts import ServerAPI
    from akaribot.core.queue.peer import PeerSelector

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
        return bool(
            await ServerAPI.post_module_action.using(CliPeer).with_timeout(RPC_TIMEOUT_SECONDS)(
                module=module, action=action
            )
        )
    finally:
        if poller is not None:
            poller.cancel()
            await asyncio.gather(poller, return_exceptions=True)
        if database_connected:
            from akaribot.core.database import close_db

            await close_db()


def _known_modules() -> tuple[set[str], bool]:
    """收集可用于校验模块名的名字集合。

    :return: 二元组——名字集合；状态表是否已有记录（据此判断运行期注册名是否已收录）。
    """
    declared = set(_declared())
    try:
        status = asyncio.run(_status())
    except Exception as exc:  # noqa: BLE001 - 校验只是提前拦截笔误，读不到状态表不应阻断操作
        print(f"无法读取模块状态表（{exc}），跳过模块名校验。", file=sys.stderr)
        return declared, False
    return declared | set(status), bool(status)


def _load_or_unload(module: str, action: str) -> int:
    """执行一次全局装载或卸载。

    :param module: 模块名。
    :param action: ``load`` 或 ``unload``。
    :return: 进程退出码。
    """
    known, status_seen = _known_modules()
    if module not in known:
        hedge = "" if status_seen else "；若该模块由未声明 provides_modules 的包在运行期注册，请先启动一次实例再试"
        print(f"未知模块 {module!r}：状态表与已装包都没有它。用 `akaribot module list` 核对已装包{hedge}。", file=sys.stderr)
        return 2

    from akaribot.core.queue.errors import RpcError, RpcTimeoutError

    try:
        changed = asyncio.run(_notify_server(module, action))
    except InstanceUnreachable as exc:
        print(f"{INSTANCE_STOPPED_HINT}（{exc}）", file=sys.stderr)
        return 1
    except RpcTimeoutError as exc:
        print(f"已发出请求，但 {RPC_TIMEOUT_SECONDS} 秒内未收到实例确认：{exc}", file=sys.stderr)
        print("模块状态可能已改变，请用本入口的 list 子命令复核，不要直接重试。", file=sys.stderr)
        return 1
    except RpcError as exc:
        print(f"热装载通知失败：{exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        print(f"热装载通知失败：{exc}", file=sys.stderr)
        return 1

    if not changed:
        print(f"实例拒绝{action}模块 {module}：模块未注册，或状态切换未完成。", file=sys.stderr)
        return 1
    state = "true" if action == "load" else "false"
    print(f"已全局{'装载' if action == 'load' else '卸载'}模块 {module}（module_status.load = {state}）")
    return 0


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.modules",
        description="查看或切换模块的全局装载状态（module_status.load）。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="列出各注册模块的全局装载状态")
    listing.add_argument("--json", action="store_true", help="以 JSON 输出，供 CLI 解析")

    load = sub.add_parser("load", help="全局装载模块：让它参与命令匹配")
    load.add_argument("module", help="模块名，如 wiki")

    unload = sub.add_parser("unload", help="全局卸载模块：让它退出命令匹配")
    unload.add_argument("module", help="模块名，如 wiki")

    args = parser.parse_args(argv)

    if args.command == "list":
        try:
            items, note = collect()
        except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
            print(f"读取模块状态失败：{exc}", file=sys.stderr)
            return 1
        if note:
            print(note, file=sys.stderr)
        if args.json:
            json.dump(items, sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
            return 0
        for item in items:
            loaded = item["loaded"]
            state = "unknown" if loaded is None else ("loaded" if loaded else "unloaded")
            print(f"{item['name']}\t{state}\t{item['installed_dist'] or '-'}")
        return 0

    return _load_or_unload(args.module, args.command)


if __name__ == "__main__":
    sys.exit(main())
