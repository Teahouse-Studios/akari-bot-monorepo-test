"""已装包清单入口。

CLI 进程不 import core，一切经本入口的子进程输出获取；故 stdout 只允许出现结果本身，
日志与进度一律走 stderr。``modules`` 取自包清单的 ``provides_modules``，不为此加载模块。
"""

from __future__ import annotations

import argparse
import json
import sys

from akaribot.core.registry import PackageRegistry


def collect() -> dict:
    """收集已发现的模块与适配器包。

    :return: ``{"packages": [...], "incompatible": {...}}``。
    """
    PackageRegistry.discover(force=True)
    packages: list[dict] = []
    for kind, entries in (("module", PackageRegistry.modules()), ("adapter", PackageRegistry.adapters())):
        for name in sorted(entries):
            entry = entries[name]
            packages.append(
                {
                    "name": entry.name,
                    "kind": entry.kind,
                    "dist": entry.dist_name or f"akari-bot-{kind}-{entry.name}",
                    "version": entry.version,
                    "import_path": entry.import_path,
                    "root": str(entry.root),
                    "modules": list(entry.manifest.provides_modules),
                }
            )
    return {"packages": packages, "incompatible": PackageRegistry.incompatible()}


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.registry",
        description="输出已装模块与适配器包清单。",
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 输出，供 CLI 解析")
    args = parser.parse_args(argv)

    data = collect()
    if args.json:
        json.dump(data, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    for item in data["packages"]:
        print(f"{item['name']}\t{item['kind']}\t{item['dist']}\t{item['version']}\t{item['import_path']}")
    for name, reason in data["incompatible"].items():
        print(f"! {name}\t{reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
