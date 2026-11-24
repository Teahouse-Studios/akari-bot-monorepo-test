"""数据库迁移入口。

供 CLI 在安装/升级/卸载包后以子进程调用。读 ``AKARI_INSTANCE_DIR`` 决定实例，不依赖仓库根作为 cwd。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from packaging.utils import canonicalize_name


class PurgeError(RuntimeError):
    """卸载清理不满足前提（包未包含在发现结果中，或没有可删除的表）。"""


def _is_installed(dist: str) -> bool:
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            if entry.dist_name == dist:
                return True
    return False


def _owned_tables(dist: str) -> tuple[str, ...]:
    # 表名仅从 manifest 读取，**绝不接受调用方传入**，因为 purge 是破坏性操作，各表归属仅能由包自身声明。
    # CLI 即使被改动或由人工直接调用，也无法通过该入口删除未声明的数据表。
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
        # 迁移记录表由创建数据表负责。写入进程同样先执行 generate_schemas 再迁移，
        # 否则全新实例上第一条迁移会因 schema_migrations 不存在而失败。
        from tortoise import Tortoise

        await Tortoise.generate_schemas(safe=True)
        if package is not None:
            discovered = await MigrationRunner.discover()
            # 迁移按包名记录，core 的迁移记录为 "core"，而 CLI 传的是包名 akari-bot-core。
            if package not in discovered and package == "akari-bot-core" and "core" in discovered:
                package = "core"
            if package not in discovered:
                # 缺少迁移目录属于合法状态，本仓库各模块包不创建数据表。仅当成员包未安装时才判定为用户错误。
                if not _is_installed(package):
                    print(f"未安装分发包 {package!r}。", file=sys.stderr)
                    raise SystemExit(2)
                print(f"{package} 没有数据库迁移，无需执行。", file=sys.stderr)
                return {"applied": []}
        # 旧版本号转换与按包执行迁移记录一并处理，旧数据库升级到指定版本后其迁移记录视为已应用。
        await convert_legacy_version()
        applied = await MigrationRunner.upgrade(package)
    finally:
        await close_db()
    return {"applied": [[name, revision] for name, revision in applied]}


async def _purge(package: str) -> dict:
    # 表已不存在时按幂等成功处理，因为本命令的预期目标是“上述数据表不再存在”，重新运行或手工删除后再次运行
    # 均满足该预期，报告失败会导致卸载流程停滞在已经达成的目标上。缺失的表名如实返回，调用方
    # 可明确区分哪些为本次删除项、哪些为原本即不存在的项。
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

    :param argv: 命令行参数。默认取 ``sys.argv[1:]``。
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
        # 失败原因写入 stdout 的 JSON，因为调用方仅解析 stdout，
        # 若仅写入 stderr 则无法获取结构化原因，仅能退回“退出码 1”这一无用信息。
        if getattr(args, "json", False):
            json.dump(
                {"dist": args.package, "error": str(exc), "dropped": [], "missing": []}, sys.stdout, ensure_ascii=False
            )
            sys.stdout.write("\n")
        print(f"清理失败：{exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - 入口层统一捕获异常，错误信息面向调用方展示。
        if getattr(args, "json", False):
            json.dump(
                {"dist": args.package, "error": str(exc), "dropped": [], "missing": []}, sys.stdout, ensure_ascii=False
            )
            sys.stdout.write("\n")
        print(f"迁移执行失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
