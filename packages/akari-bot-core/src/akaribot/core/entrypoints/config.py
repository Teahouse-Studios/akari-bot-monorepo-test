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
from typing import Any

PLACEHOLDER_PATTERN = re.compile(r"^<Replace me.*?>$")

# i18n 快照是否已接上：子进程只在需要注释时接一次。
_LOCALE_READY = False

# 注释键前缀：与配置模板写入期使用的 i18n 键一致（core/config/__init__.py 的注释生成路径）。
COMMENT_KEY = "config.comments.{table}.{key}"


def _entry_for_dist(dist: str):
    """按分发名取包条目。

    :param dist: 分发名，如 ``akari-bot-module-wiki``。
    :return: 包条目；未安装时为 ``None``。
    """
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            if entry.dist_name == dist:
                return entry
    return None


def _table_document(table: str) -> dict[str, Any]:
    """取某个配置表在内存副本中的键值。

    :param table: 表名，如 ``module_wiki``。
    :return: 普通键与密钥键的映射。
    :raises KeyError: 该表不存在。
    """
    from akaribot.core.config import CFGManager

    document = CFGManager.values.get(table)
    if document is None:
        raise KeyError(table)
    return dict(document)


def _localized_comment(table: str, key: str, secret: bool) -> str | None:
    """取配置项的本地化注释。

    :param table: 表名。
    :param key: 键名。
    :param secret: 是否来自密钥表。
    :return: 注释文本；未声明时为 ``None``。
    """
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
    """接上 i18n 快照。

    子进程没有 bot 启动期的快照，不接上时 ``Locale.t`` 一律回退为键名（注释会显示成
    ``{I18N:...}`` 标记）。只做一次。
    """
    global _LOCALE_READY
    if _LOCALE_READY:
        return
    from akaribot.core.constants import lang_list
    from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot

    build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")
    _LOCALE_READY = True


def _schema(table: str) -> list[dict]:
    """列出一个配置表的全部键。

    键清单以配置文件为准（模板在生成期已把声明字段全部落盘）；类型取运行期值，
    ``default`` 尽力从配置模板的声明里取，取不到时为 ``None``。

    :param table: 表名。
    :return: 条目列表，按键名排序。
    """
    document = _table_document(table)
    plain = document.get(table) or {}
    secret_table = "secret" if table == "config" else f"{table}_secret"
    secret = document.get(secret_table) or {}

    declared = _declared_defaults(table)
    items: list[dict] = []
    for key in sorted({*plain, *secret}):
        raw = secret[key] if key in secret else plain[key]
        value = raw.unwrap() if hasattr(raw, "unwrap") else raw
        is_secret = key in secret
        meta = declared.get(key, {})
        cfg_type = meta.get("type")
        items.append(
            {
                "key": key,
                "type": getattr(cfg_type, "__name__", None) or type(value).__name__,
                "default": meta.get("default"),
                "secret": is_secret,
                "comment": _localized_comment(table, key, is_secret),
                "value": value,
                "is_placeholder": bool(PLACEHOLDER_PATTERN.match(str(value))),
            }
        )
    return items


def _declared_defaults(table: str) -> dict[str, dict]:
    """从配置模板里取声明默认值，取不到时返回空映射。

    模板声明经 ``@on_module_config`` 在类创建期落盘，字段元数据保存在类的
    ``__config_fields__``；此处只读该映射，不重新生成配置。

    :param table: 表名。
    :return: 键名到 ``{"default": ...}`` 的映射。
    """
    from akaribot.core.registry import PackageRegistry

    PackageRegistry.discover()
    result: dict[str, dict] = {}
    for entries in (PackageRegistry.modules(), PackageRegistry.adapters()):
        for entry in entries.values():
            if entry.manifest.config_table != table:
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


def _resolve_table(table: str) -> str:
    """表名归一化，与 :meth:`CFGManager.get` 的既有约定一致。"""
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

    args = parser.parse_args(argv)

    try:
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

            CFGManager.edit_write(args.key, args.value, table_name=_resolve_table(args.table))
            if args.json:
                json.dump({"key": args.key, "value": args.value}, sys.stdout, ensure_ascii=False)
                sys.stdout.write("\n")
            return 0

        entry = _entry_for_dist(args.package)
        if entry is None:
            print(f"未安装分发包 {args.package!r}。", file=sys.stderr)
            return 2
        importlib.import_module(f"{entry.import_path}.config")
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
