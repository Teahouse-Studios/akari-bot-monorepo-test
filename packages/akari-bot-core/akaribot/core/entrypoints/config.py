"""配置读写入口。

供 CLI 以子进程调用：CLI 不 import core，配置的读取、写入与安装后的补全都在这里完成。
JSON 走 stdout，日志与进度走 stderr。写入一律经 ``CFGManager.edit_write()`` 的原子路径。
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from collections.abc import Mapping
from typing import Any

PLACEHOLDER_PATTERN = re.compile(r"^<Replace me.*?>$")

# i18n 快照是否已接上：子进程只在需要注释时接一次。
_LOCALE_READY = False

# 注释键前缀：与配置模板写入期使用的 i18n 键一致（core/config/__init__.py 的注释生成路径）。
COMMENT_KEY = "config.comments.{table}.{key}"


def _entry_for_dist(dist: str):
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            if entry.dist_name == dist:
                return entry
    return None


def _table_document(table: str) -> dict[str, Any]:
    from akaribot.core.config import CFGManager

    document = CFGManager.values.get(table)
    if document is None:
        raise KeyError(table)
    return dict(document)


def _localized_comment(table: str, key: str, secret: bool) -> str | None:
    from akaribot.core.config import CFGManager
    from akaribot.core.i18n import Locale

    _connect_locale()
    locale_name = CFGManager.values.get("config", {}).get("default_locale") or "zh_cn"
    locale = Locale(locale_name)
    candidates = [COMMENT_KEY.format(table=f"{table}_secret" if secret else table, key=key)]
    candidates.append(COMMENT_KEY.format(table=table, key=key))
    for candidate in candidates:
        text = locale.t(candidate, locale_failed_prompt=False)
        if text != candidate:
            return text
    return None


def _connect_locale() -> None:
    # 子进程没有 bot 启动期的快照，不接上时 ``Locale.t`` 一律回退为键名（注释会显示成
    # ``{I18N:...}`` 标记）。只做一次。
    global _LOCALE_READY
    if _LOCALE_READY:
        return
    from akaribot.core.constants import lang_list
    from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot

    build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")
    _LOCALE_READY = True


def _table_values(table: str, document: Mapping[str, Any]) -> list[dict[str, Any]]:
    # 键清单以配置文件为准（模板在生成期已把声明字段全部落盘）；占位判定是 schema 与
    # placeholders 共用的口径，只在这里出现一次。
    plain = document.get(table) or {}
    secret_table = "secret" if table == "config" else f"{table}_secret"
    secret = document.get(secret_table) or {}
    values: list[dict[str, Any]] = []
    for key in sorted({*plain, *secret}):
        raw = secret[key] if key in secret else plain[key]
        value = raw.unwrap() if hasattr(raw, "unwrap") else raw
        values.append(
            {
                "key": key,
                "value": value,
                "secret": key in secret,
                "is_placeholder": bool(PLACEHOLDER_PATTERN.match(str(value))),
            }
        )
    return values


def _schema(table: str) -> list[dict]:
    # 类型取运行期值，``default`` 尽力从配置模板的声明里取，取不到时为 ``None``。
    document = _table_document(table)
    declared = _declared_defaults(table)
    items: list[dict] = []
    for entry in _table_values(table, document):
        meta = declared.get(entry["key"], {})
        cfg_type = meta.get("type")
        items.append(
            {
                "key": entry["key"],
                "type": getattr(cfg_type, "__name__", None) or type(entry["value"]).__name__,
                "default": meta.get("default"),
                "secret": entry["secret"],
                "comment": _localized_comment(table, entry["key"], entry["secret"]),
                "value": entry["value"],
                "is_placeholder": entry["is_placeholder"],
            }
        )
    return items


def _read_table_file(table: str) -> Any:
    # 任一文件损坏都会让 ``CFGManager.load()`` 整体失败，故按表读文件，未读到的表单独归集。
    from tomlkit import parse as toml_parser

    from akaribot.core.paths import Paths

    with open(Paths.config / f"{table}.toml", "r", encoding="utf-8") as handle:
        return toml_parser(handle.read())


def _placeholder_report(tables: str | None) -> dict[str, Any]:
    from akaribot.core.paths import Paths

    if tables is None:
        requested = sorted(path.stem for path in Paths.config.glob("*.toml"))
    else:
        requested = [name.strip() for name in tables.split(",") if name.strip()]

    table_counts: dict[str, dict[str, int]] = {}
    failed: dict[str, str] = {}
    scanned: list[str] = []
    count = 0
    for table in dict.fromkeys(requested):
        # 表名只用于拼接配置目录下的文件名；含分隔符的名字一律拒绝，读不到目录之外。
        if "/" in table or "\\" in table:
            failed[table] = "表名含路径分隔符"
            continue
        try:
            document = _read_table_file(table)
        except (OSError, UnicodeDecodeError) as error:
            failed[table] = f"读取失败：{type(error).__name__}: {error}"
            continue
        except Exception as error:  # noqa: BLE001 - 解析错误类型由 tomlkit 决定，逐表归集后继续
            failed[table] = f"解析失败：{type(error).__name__}: {error}"
            continue
        values = _table_values(table, document)
        placeholder = sum(1 for item in values if item["is_placeholder"])
        table_counts[table] = {"placeholder": placeholder, "total": len(values)}
        scanned.append(table)
        count += placeholder
    return {"tables": table_counts, "count": count, "scanned": scanned, "failed": failed}


def _declared_defaults(table: str) -> dict[str, dict]:
    # 模板声明经 ``@on_module_config`` 在类创建期落盘，字段元数据保存在类的
    # ``__config_fields__``；此处只读该映射，不重新生成配置。
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    result: dict[str, dict] = {}
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            declared_table = entry.manifest.config_table
            # 实例表（bot_telegram-alt）由基表（bot_telegram）的模板派生，按前缀一并匹配。
            if declared_table != table and not table.startswith(f"{declared_table}-"):
                continue
            try:
                module = importlib.import_module(f"{entry.import_path}.config")
            except Exception:  # noqa: BLE001 - 模板不可导入时降级为无默认值
                continue
            for obj in vars(module).values():
                fields = getattr(obj, "__config_fields__", None)
                if not isinstance(fields, dict):
                    continue
                for name, meta in fields.items():
                    if not isinstance(meta, dict):
                        continue
                    result.setdefault(name, {"default": meta.get("default"), "type": meta.get("cfg_type")})
    return result


def _coerce(table: str, key: str, value: str) -> Any:
    # 不做转换会把 `enable` 之类的布尔项写成字符串 ``"true"``：文件里类型不对，读回虽是 ``true``
    # 但任何按布尔取用的代码都会拿到真值字符串。
    cfg_type = _declared_defaults(table).get(key, {}).get("type")
    if cfg_type is bool:
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "on"):
            return True
        if lowered in ("false", "0", "no", "off"):
            return False
        return value
    if cfg_type is int:
        try:
            return int(value)
        except ValueError:
            return value
    if cfg_type is float:
        try:
            return float(value)
        except ValueError:
            return value
    if cfg_type is list:
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


def _resolve_table(table: str) -> str:
    from akaribot.core.config import CFGManager

    return CFGManager._resolve_table(table)


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.config",
        description="读取、写入与补全实例配置。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    schema = sub.add_parser("schema", help="列出某表的全部配置项")
    schema.add_argument("--table", required=True)
    schema.add_argument("--json", action="store_true")

    get = sub.add_parser("get", help="读取单个配置项")
    get.add_argument("key")
    get.add_argument("--table", required=True)
    get.add_argument("--json", action="store_true")

    set_ = sub.add_parser("set", help="写入单个配置项")
    set_.add_argument("key")
    set_.add_argument("value")
    set_.add_argument("--table", required=True)
    set_.add_argument("--json", action="store_true")

    sync = sub.add_parser("sync", help="导入某包的配置模板并补全实例配置")
    sync.add_argument("--package", required=True)
    sync.add_argument("--json", action="store_true")

    placeholders = sub.add_parser("placeholders", help="统计各表的待填写占位符")
    placeholders.add_argument("--tables", help="逗号分隔的表名；缺省统计配置目录下的全部表")
    placeholders.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)

    try:
        if args.command == "placeholders":
            report = _placeholder_report(args.tables)
            if args.json:
                json.dump(report, sys.stdout, ensure_ascii=False, default=str)
                sys.stdout.write("\n")
            else:
                for table, counts in report["tables"].items():
                    print(f"{table}\t{counts['placeholder']}/{counts['total']}")
                print(f"待填写 {report['count']} 项，统计 {len(report['scanned'])} 张表。")
                if report["failed"]:
                    detail = "、".join(f"{name}（{reason}）" for name, reason in report["failed"].items())
                    print(f"未统计 {len(report['failed'])} 张表：{detail}")
            return 0

        if args.command == "schema":
            items = _schema(_resolve_table(args.table))
            if args.json:
                json.dump(items, sys.stdout, ensure_ascii=False, default=str)
                sys.stdout.write("\n")
            else:
                for item in items:
                    flag = "secret" if item["secret"] else item["type"]
                    print(f"{item['key']}\t{flag}\t{item['comment'] or '-'}\t{item['value']!r}")
            return 0

        if args.command == "get":
            from akaribot.core.config import CFGManager

            value = CFGManager.get(args.key, table_name=_resolve_table(args.table))
            if args.json:
                json.dump({"key": args.key, "value": value}, sys.stdout, ensure_ascii=False, default=str)
                sys.stdout.write("\n")
            else:
                print(value)
            return 0

        if args.command == "set":
            from akaribot.core.config import CFGManager

            table = _resolve_table(args.table)
            value = _coerce(table, args.key, args.value)
            CFGManager.edit_write(args.key, value, table_name=table)
            if args.json:
                json.dump({"key": args.key, "value": args.value}, sys.stdout, ensure_ascii=False)
                sys.stdout.write("\n")
            return 0

        entry = _entry_for_dist(args.package)
        if entry is None:
            print(f"未安装分发包 {args.package!r}。", file=sys.stderr)
            return 2
        module_name = f"{entry.import_path}.config"
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            # 包没有模块配置模板（bundled core 即如此，其配置由首次运行扫描生成），不是失败。
            if exc.name != module_name:
                raise
            print(f"{args.package} 没有模块配置模板，无需补写。", file=sys.stderr)
            if args.json:
                json.dump(
                    {"package": args.package, "table": None, "keys": 0, "placeholders": []},
                    sys.stdout,
                    ensure_ascii=False,
                )
                sys.stdout.write("\n")
            return 0
        table = entry.manifest.config_table
        items = _schema(table) if table else []
        placeholders = [item["key"] for item in items if item["is_placeholder"]]
        result = {"package": args.package, "table": table, "keys": len(items), "placeholders": placeholders}
        if args.json:
            json.dump(result, sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            print(f"{args.package}\t表 {table}\t共 {len(items)} 项\t占位 {len(placeholders)} 项")
            for key in placeholders:
                print(f"  待填写：{key}")
        return 0
    except KeyError as exc:
        print(f"配置表不存在：{exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - 入口层兜底，错误信息给操作者看
        print(f"配置操作失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
