"""JobQueue peer 快照入口。

供 CLI 与 TUI 以子进程调用：连接状态的权威来源是数据库表 ``job_queue_peers`` 的租约，
``Alive`` 只是进程内缓存。取不到数据属于可降级状态（输出 ``available: false`` 与原因、
以 0 退出），不是错误——调用方据此显示「未知」。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime


async def _snapshot() -> dict:
    # 导入本身就可能在实例配置缺失时抛错（core 的配置在导入期加载），故一并纳入降级路径。
    try:
        from akaribot.core.database import close_db, init_db
        from akaribot.core.database.models import JobQueuePeersTable

        await init_db(generate_schemas=False)
    except Exception as exc:  # noqa: BLE001 - 数据库不可用属可降级状态
        return {"peers": [], "available": False, "note": f"数据库不可用：{exc}"}

    try:
        rows = await JobQueuePeersTable.all()
    except Exception as exc:  # noqa: BLE001 - 表不存在时同样降级
        return {"peers": [], "available": False, "note": f"peer 表不可读：{exc}"}
    finally:
        await close_db()

    now = datetime.now(UTC)
    peers = []
    for row in rows:
        lease = row.lease_until
        # 租约是唯一事实来源：已过期的记录仍在表里，但不算在线。
        expired = lease is not None and lease.replace(tzinfo=lease.tzinfo or UTC) <= now
        peers.append(
            {
                "peer_id": row.peer_id,
                "service": row.service,
                "role": row.role,
                "state": "expired" if expired else row.state,
                "online": not expired and row.state == "ready",
                "lease_until": lease.isoformat() if lease else None,
                "metadata": row.metadata or {},
            }
        )
    return {"peers": peers, "available": True, "note": ""}


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.peers",
        description="输出 JobQueue peer 快照（连接状态的权威来源）。",
    )
    # 默认即 JSON；--json 显式写法与 TUI 数据源的调用一致，必须接受。
    parser.add_argument("--json", action="store_true", help="以 JSON 输出（默认）")
    parser.add_argument("--text", action="store_true", help="以人类可读文本输出")
    args = parser.parse_args(argv)

    data = asyncio.run(_snapshot())
    if not args.text:
        json.dump(data, sys.stdout, ensure_ascii=False, default=str)
        sys.stdout.write("\n")
        return 0

    for peer in data["peers"]:
        mark = "在线" if peer["online"] else "离线"
        print(f"{peer['peer_id']}\t{peer['service']}\t{peer['state']}\t{mark}")
    if not data["available"]:
        print(f"不可用：{data['note']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
