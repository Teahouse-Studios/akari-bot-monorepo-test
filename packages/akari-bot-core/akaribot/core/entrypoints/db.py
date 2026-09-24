"""数据库迁移入口。

供 CLI 在安装/升级/卸载包后以子进程调用；读 ``AKARI_INSTANCE_DIR`` 决定实例，不依赖仓库根作为 cwd。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from packaging.utils import canonicalize_name


class PurgeError(RuntimeError):
    """卸载清理不满足前提：包不在发现结果里，或没有可删的表。"""


def _is_installed(dist: str) -> bool:
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            if entry.dist_name == dist:
                return True
    return False


def _owned_tables(dist: str) -> tuple[str, ...]:
    # 表名只从 manifest 读，**绝不接受调用方传入**：purge 是破坏性操作，谁拥有哪张表只能由包自己
    # 声明。CLI 即使被改坏或被人手工调用，也无法借这个入口删掉未声明的表。
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    wanted = canonicalize_name(dist)
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            name = entry.dist_name or f"akari-bot-{entry.kind}-{entry.name}"
            if canonicalize_name(name) != wanted:
                continue
            declared = tuple(str(table) for table in entry.manifest.owned_tables)
            if not declared:
                raise PurgeError(f"{dist} 的 manifest 未声明 owned_tables，没有可删除的表")
            return declared
    reason = PackageRegistry.incompatible().get(wanted)
    detail = f"（发现层拒绝：{reason}）" if reason else ""
    raise PurgeError(f"未安装分发包 {dist}{detail}")


async def _status() -> dict:
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
    from akaribot.core.database import close_db, init_db
    from akaribot.core.database.legacy import convert_legacy_version
    from akaribot.core.database.migration import MigrationRunner

    await init_db(generate_schemas=False)
    try:
        # 迁移登记表由模型建表负责：写进程的启动路径同样是「先 generate_schemas 再迁移」，
        # 否则全新实例上第一条迁移就会因 schema_migrations 不存在而失败。
        from tortoise import Tortoise

        await Tortoise.generate_schemas(safe=True)
        if package is not None:
            discovered = await MigrationRunner.discover()
            # 迁移按包名登记：core 的迁移登记为 "core"，而 CLI 传的是分发名 akari-bot-core。
            if package not in discovered and package == "akari-bot-core" and "core" in discovered:
                package = "core"
            if package not in discovered:
                # 没有迁移目录是合法状态：本仓库 39 个模块包不建表。只有包根本没装才算用户错误。
                if not _is_installed(package):
                    print(f"未安装分发包 {package!r}。", file=sys.stderr)
                    raise SystemExit(2)
                print(f"{package} 没有数据库迁移，无需执行。", file=sys.stderr)
                return {"applied": []}
        # 旧版本号转换与逐包 revision 一并执行：旧库升到某版本后其 revision 视为已应用。
        await convert_legacy_version()
        applied = await MigrationRunner.upgrade(package)
    finally:
        await close_db()
    return {"applied": [[name, revision] for name, revision in applied]}


async def _purge(package: str) -> dict:
    # 表已不存在时按**幂等成功**处理：本命令的契约是「这些表不再存在」，重跑或手工删过之后再跑
    # 都满足该契约，报成失败只会让卸载流程卡在一个已经达成的目标上。缺失的表名照实回报，操作者
    # 据此判断是不是清单漂移。
    from tortoise import Tortoise

    from akaribot.core.database import close_db, init_db
    from akaribot.core.database.legacy import has_table
    from akaribot.core.database.migration import MigrationContext

    tables = _owned_tables(package)

    await init_db(generate_schemas=False)
    try:
        conn = Tortoise.get_connection("default")
        context = MigrationContext(conn)
        dropped: list[str] = []
        missing: list[str] = []
        for table in tables:
            if not await has_table(conn, table):
                missing.append(table)
                continue
            await context.execute(f"DROP TABLE IF EXISTS {context.quote(table)};")
            dropped.append(table)
    finally:
        await close_db()
    return {"dist": package, "dropped": dropped, "missing": missing}


def _emit_purge(payload: dict, as_json: bool) -> None:
    if as_json:
        json.dump(payload, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return
    print(f"已删除 {len(payload['dropped'])} 张表：{','.join(payload['dropped']) or '-'}")
    if payload["missing"]:
        print(f"以下表本就不存在，按幂等处理：{','.join(payload['missing'])}")


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

    purge = sub.add_parser("purge", help="删除某个分发声明的表（卸载清理用）")
    purge.add_argument("--package", required=True, help="分发名，如 akari-bot-module-wiki")
    purge.add_argument("--json", action="store_true", help="以 JSON 输出")

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

        if args.command == "purge":
            _emit_purge(asyncio.run(_purge(args.package)), args.json)
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
    except PurgeError as exc:
        # --json 时把原因也写进 stdout：调用方（CLI 的 db_purge）解析的是 stdout，
        # 只给 stderr 的话它拿不到结构化原因，只能退回「退出码 1」这种无用信息。
        if getattr(args, "json", False):
            json.dump(
                {"dist": args.package, "error": str(exc), "dropped": [], "missing": []}, sys.stdout, ensure_ascii=False
            )
            sys.stdout.write("\n")
        print(f"清理失败：{exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        if getattr(args, "json", False):
            json.dump(
                {"dist": args.package, "error": str(exc), "dropped": [], "missing": []}, sys.stdout, ensure_ascii=False
            )
            sys.stdout.write("\n")
        print(f"迁移执行失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
