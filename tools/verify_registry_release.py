"""发布后核对 registry.json 里本次分发的版本。

publish 与 registry 是两个 job：包已上 PyPI、索引却仍旧的部分成功状态最难排查，因为它同时
「看起来成功」又「用户装不到」。索引生成之后、push 到 gh-pages 之前，必须确认本次发布的分发在
索引里的 ``latest`` 就是刚发布的版本，否则宁可让 job 失败，也不要推一份指向旧版本的索引。

工具只读文件、不 import akaribot，未配置的实例与裸 CI 环境都能运行。

用法：
    python tools/verify_registry_release.py --registry registry.json \\
        --dist akari-bot-module-wiki --version 0.2.0

退出码：0 一致；2 索引里找不到该分发、或 latest 与本次版本不符。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from packaging.utils import canonicalize_name

CORE_DIST = "akari-bot-core"
SECTIONS = ("modules", "adapters")


class VerifyError(RuntimeError):
    """索引内容与本次发布不符。"""


def load_registry(path: Path) -> dict[str, Any]:
    """读取 registry.json。

    :param path: 索引文件路径。
    :return: 解析后的索引。
    :raises VerifyError: 文件缺失、不可读或不是 JSON 对象。
    """
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise VerifyError(f"索引文件不存在：{path}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise VerifyError(f"索引文件无法解析：{path}：{error}") from error
    if not isinstance(payload, dict):
        raise VerifyError(f"索引顶层不是对象：{path}")
    return payload


def find_entry(registry: dict[str, Any], dist: str) -> tuple[str, dict[str, Any]]:
    """在索引里定位分发。

    core 段只承载分发名、版本与 API 版本，条目段才有 ``latest`` 之外的字段，故两处分别找。

    :param registry: 索引内容。
    :param dist: 分发名。
    :return: 二元组——所在段名与该段内容。
    :raises VerifyError: 索引里没有该分发。
    """
    wanted = canonicalize_name(dist)
    core = registry.get("core")
    if isinstance(core, dict) and canonicalize_name(str(core.get("dist") or "")) == wanted:
        return "core", core
    for section in SECTIONS:
        entries = registry.get(section) or []
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and canonicalize_name(str(entry.get("dist") or "")) == wanted:
                return section, entry
    raise VerifyError(f"索引里没有分发 {dist}（比对的分发名：{wanted}）")


def verify(registry: dict[str, Any], dist: str, version: str) -> str:
    """核对索引里该分发的 ``latest`` 是否为本次发布的版本。

    :param registry: 索引内容。
    :param dist: 分发名。
    :param version: 本次发布的版本。
    :return: 供日志输出的一行结论。
    :raises VerifyError: 版本不一致，或条目缺少 ``latest``。
    """
    section, entry = find_entry(registry, dist)
    latest = str(entry.get("latest") or "")
    if not latest:
        raise VerifyError(f"索引里 {dist}（{section} 段）没有 latest，无法确认本次版本")
    if latest != version:
        raise VerifyError(f"索引里 {dist} 的 latest 是 {latest}，与本次发布的 {version} 不符；拒绝推送旧索引")
    return f"索引核对通过：{section} 段的 {dist} latest = {latest}"


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(description="核对 registry.json 里本次发布分发的版本")
    parser.add_argument("--registry", metavar="PATH", type=Path, default=Path("registry.json"), help="索引文件路径")
    parser.add_argument("--dist", metavar="NAME", required=True, help="本次发布的分发名")
    parser.add_argument("--version", metavar="VER", required=True, help="本次发布的版本")
    return parser


def main(argv: list[str] | None = None) -> int:
    """入口。返回进程退出码，0 表示索引与本次发布一致。"""
    args = build_parser().parse_args(argv)
    try:
        print(verify(load_registry(args.registry), args.dist, args.version))
    except VerifyError as error:
        print(f"索引核对失败：{error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
