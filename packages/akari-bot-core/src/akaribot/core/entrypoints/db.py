"""数据库迁移入口。

供 CLI 在安装/升级包后以子进程调用；读 ``AKARI_INSTANCE_DIR`` 决定实例，不依赖仓库根作为 cwd。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys


async def _status() -> dict:
    """读取各包的迁移状态。

    :return: ``{"packages": {包名: {"discovered": n, "applied": n, "pending": [...]}}, ...}``。
    """
    from akaribot.core.database import close_db, init_db
    from akaribot.core.database.migration import MigrationRunner
    from akaribot.core.database.models import SchemaMigration

    await init_db(generate_schemas=False)
    try:
        discovered = await MigrationRunner.discover()
        pending = await MigrationRunner.pending()
        rows = await SchemaMigration.all()
    finally:
        await close_db()

    applied_count: dict[str, int] = {}
    for row in rows:
        applied_count[row.package] = applied_count.get(row.package, 0) + 1

    return {
        "packages": {
            package: {
                "discovered": len(modules),
                "applied": applied_count.get(package, 0),
                "pending": pending.get(package, []),
            }
            for package, modules in sorted(discovered.items())
        }
    }


async def _upgrade(package: str | None) -> dict:
    """执行待应用迁移。

    :param package: 限定包名；``None`` 表示全部。
    :return: ``{"applied": [[包名, revision], ...]}``。
    :raises SystemExit: 指定的包没有可发现的迁移目录。
    """
    from akaribot.core.database import close_db, init_db
    from akaribot.core.database.legacy import convert_legacy_version
    from akaribot.core.database.migration import MigrationRunner

    await init_db(generate_schemas=False)
    try:
        if package is not None:
            discovered = await MigrationRunner.discover()
            if package not in discovered:
                print(f"未发现包 {package!r} 的迁移目录。", file=sys.stderr)
                raise SystemExit(2)
        # 旧版本号转换与逐包 revision 一并执行：旧库升到某版本后其 revision 视为已应用。
        await convert_legacy_version()
        applied = await MigrationRunner.upgrade(package)
    finally:
        await close_db()
    return {"applied": [[name, revision] for name, revision in applied]}


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.db",
        description="查看或执行实例数据库迁移。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="查看各包的迁移状态")
    status.add_argument("--json", action="store_true", help="以 JSON 输出")

    upgrade = sub.add_parser("upgrade", help="执行待应用迁移")
    upgrade.add_argument("--package", default=None, help="限定分发名，如 akari-bot-module-wiki")
    upgrade.add_argument("--json", action="store_true", help="以 JSON 输出")

    args = parser.parse_args(argv)

    try:
        if args.command == "status":
            data = asyncio.run(_status())
            if args.json:
                json.dump(data, sys.stdout, ensure_ascii=False)
                sys.stdout.write("\n")
            else:
                for package, info in data["packages"].items():
                    pending = ",".join(info["pending"]) or "-"
                    print(f"{package}\t已应用 {info['applied']}/{info['discovered']}\t待应用 {pending}")
            return 0

        data = asyncio.run(_upgrade(args.package))
        if args.json:
            json.dump(data, sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            print(f"已应用 {len(data['applied'])} 条迁移。")
            for name, revision in data["applied"]:
                print(f"  {name}\t{revision}")
        return 0
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        print(f"迁移执行失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
