"""包文档清单入口。

CLI 以子进程调用本模块列出各包 ``doc/`` 目录与页面。发现只按 entry point 的导入路径定位包目录，
不导入目标包：导入会执行包内配置模板与其它导入期副作用。
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import re
import sys
import tomllib
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

DOCS_GROUP = "akaribot.docs"
DOCS_DIR = "doc"
DOC_META_FILE = "doc.toml"
DOC_META_SCHEMA = 1
DEFAULT_ORDER = 500
DEFAULT_VERSION = "0+local"
SCHEMA = 1
GROUP_ORDER = ("core", "builtin", "cli", "testing", "module", "adapter", "asset", "library")
_GROUP_RANK = {name: index for index, name in enumerate(GROUP_ORDER)}
_KEY_GROUPS = {"core": "core", "builtin": "builtin", "cli": "cli", "testing": "testing"}
_KEY_PREFIX_GROUPS = (("module-", "module"), ("adapter-", "adapter"), ("assets-", "asset"))
_FRONT_MATTER_KEYS = frozenset({"title", "order", "description"})
_HEADING = re.compile(r"^#\s+(?P<title>.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(?:```|~~~)")
_NAMESPACES = (("akaribot.modules", "module"), ("akaribot.adapters", "adapter"))


def _group_of(key: str) -> str:
    if key in _KEY_GROUPS:
        return _KEY_GROUPS[key]
    for prefix, group in _KEY_PREFIX_GROUPS:
        if key.startswith(prefix):
            return group
    return "library"


def _as_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _as_order(value: Any, label: str, warnings: list[str]) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        warnings.append(f"{label}: 排序值 {value!r} 不是整数，按 {DEFAULT_ORDER} 处理。")
        return DEFAULT_ORDER


def _dist_from_path(import_path: str) -> str:
    parts = import_path.split(".")
    if parts[:2] == ["akaribot", "modules"] and len(parts) >= 3:
        # 内置模块与核心运行时同属一个分发，不按模块分发命名。
        return "akari-bot-core" if parts[2] == "core" else f"akari-bot-module-{parts[2]}"
    if parts[:2] == ["akaribot", "adapters"] and len(parts) >= 3:
        return f"akari-bot-adapter-{parts[2]}"
    if parts[:2] == ["akaribot", "assets"] and len(parts) >= 3:
        return f"akari-bot-assets-{parts[2]}"
    fixed = {
        "akaribot.core": "akari-bot-core",
        "akaribot.cli": "akari-bot-cli",
        "akaribot.testing": "akari-bot-testing",
    }
    if import_path in fixed:
        return fixed[import_path]
    if parts and parts[0] == "akaribot":
        parts = parts[1:]
    return "-".join(("akari-bot", *parts)) if parts else "akari-bot"


def _dist_name(dist: Any, import_path: str) -> str:
    if dist is not None:
        try:
            name = str(dist.name or "")
        except Exception:  # noqa: BLE001 - 元数据残缺时按导入路径推导
            name = ""
        if name:
            return name
    return _dist_from_path(import_path)


def _dist_version(dist: Any) -> str:
    if dist is None:
        return DEFAULT_VERSION
    try:
        return str(dist.version)
    except Exception:  # noqa: BLE001 - 元数据残缺时按源码检出处理
        return DEFAULT_VERSION


def _dist_summary(dist: Any) -> str:
    try:
        metadata = getattr(dist, "metadata", None)
        return str(metadata.get("Summary", "") or "") if metadata is not None else ""
    except Exception:  # noqa: BLE001 - Summary 缺失不影响清单
        return ""


def _is_editable(dist: Any) -> bool:
    if dist is None:
        return True
    try:
        raw = dist.read_text("direct_url.json")
    except Exception:  # noqa: BLE001 - 无法读取安装记录时按普通安装处理
        return False
    if not raw:
        return False
    try:
        payload = json.loads(raw)
    except ValueError:
        return False
    return bool(payload.get("dir_info", {}).get("editable"))


def _locate_doc_dir(import_path: str, find_spec: Callable[[str], Any]) -> Path:
    spec = find_spec(import_path)
    if spec is None:
        raise LookupError(import_path)
    locations = list(getattr(spec, "submodule_search_locations", None) or ())
    if locations:
        root = Path(locations[0])
    elif getattr(spec, "origin", None):
        root = Path(spec.origin).parent
    else:
        raise LookupError(import_path)
    return (root / DOCS_DIR).resolve()


def _read_doc_meta(doc_dir: Path, label: str, warnings: list[str]) -> dict[str, Any]:
    path = doc_dir / DOC_META_FILE
    if not path.is_file():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        warnings.append(f"{label}: 无法解析 {DOC_META_FILE}（{exc}），按缺省元数据处理。")
        return {}
    schema = data.get("schema", DOC_META_SCHEMA)
    if schema != DOC_META_SCHEMA:
        warnings.append(f"{label}: {DOC_META_FILE} 的 schema 为 {schema}，当前为 {DOC_META_SCHEMA}，已忽略该文件。")
        return {}
    return {name: data[name] for name in ("title", "summary", "order", "hidden", "kind") if name in data}


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.removeprefix("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "\n".join(lines)
    for index in range(1, len(lines)):
        if lines[index].strip() != "---":
            continue
        meta: dict[str, str] = {}
        for line in lines[1:index]:
            name, separator, value = line.partition(":")
            name = name.strip()
            if separator and name in _FRONT_MATTER_KEYS:
                meta[name] = _scalar(value.strip())
        return meta, "\n".join(lines[index + 1 :])
    return {}, "\n".join(lines)


def _scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _first_heading(body: str) -> str:
    fenced = False
    for line in body.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = _HEADING.match(line)
        if match:
            title = match.group("title").strip()
            if title:
                return title
    return ""


def _read_page(path: Path, relative: Path, label: str, warnings: list[str]) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        warnings.append(f"{label}: 无法读取文档 {relative.as_posix()}（{exc}），已跳过。")
        return None
    front, body = _split_front_matter(text)
    title = _as_text(front.get("title")) or _first_heading(body) or path.stem
    order = _as_order(front.get("order", DEFAULT_ORDER), f"{label}/{relative.as_posix()}", warnings)
    return {
        "title": title,
        "path": relative.as_posix(),
        "order": order,
        "summary": _as_text(front.get("description")),
    }


def _page_sort_key(page: dict[str, Any]) -> tuple[int, int, str]:
    return (0 if Path(page["path"]).name == "index.md" else 1, int(page["order"]), str(page["path"]))


def _collect_pages(doc_dir: Path, label: str, warnings: list[str]) -> list[dict[str, Any]]:
    root = doc_dir.resolve()
    pages: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            warnings.append(f"{label}: 文档 {relative.as_posix()} 指向文档目录之外，已跳过。")
            continue
        page = _read_page(resolved, relative, label, warnings)
        if page is not None:
            pages.append(page)
    pages.sort(key=_page_sort_key)
    return pages


def _build_package(
    key: str,
    import_path: str,
    *,
    dist_name: str,
    version: str,
    summary: str,
    editable: bool,
    find_spec: Callable[[str], Any],
    warnings: list[str],
) -> dict[str, Any] | None:
    try:
        doc_dir = _locate_doc_dir(import_path, find_spec)
    except (LookupError, ImportError, ValueError):
        warnings.append(f"{key}: 无法定位导入路径 {import_path}，已跳过。")
        return None
    meta = _read_doc_meta(doc_dir, key, warnings) if doc_dir.is_dir() else {}
    if meta.get("hidden") is True:
        return None
    pages = _collect_pages(doc_dir, key, warnings) if doc_dir.is_dir() else []
    if not pages:
        warnings.append(f"{key}: {doc_dir} 下没有 Markdown 文档，已跳过。")
        return None
    name = import_path.rpartition(".")[2] or import_path
    return {
        "key": key,
        "dist": dist_name,
        "name": name,
        "group": _as_text(meta.get("kind")) or _group_of(key),
        "version": version,
        "title": _as_text(meta.get("title")) or name,
        "summary": _as_text(meta.get("summary")) or summary,
        "order": _as_order(meta.get("order", DEFAULT_ORDER), key, warnings),
        "doc_path": str(doc_dir),
        "editable": editable,
        "pages": pages,
    }


def _package_from_entry_point(
    entry_point: Any, find_spec: Callable[[str], Any], warnings: list[str]
) -> dict[str, Any] | None:
    key = str(getattr(entry_point, "name", "") or "")
    value = str(getattr(entry_point, "value", "") or "")
    import_path = value.partition(":")[0].strip()
    if not key or not import_path:
        warnings.append(f"{key or value or '?'}: entry point 缺少名称或导入路径，已跳过。")
        return None
    dist = getattr(entry_point, "dist", None)
    return _build_package(
        key,
        import_path,
        dist_name=_dist_name(dist, import_path),
        version=_dist_version(dist),
        summary=_dist_summary(dist),
        editable=_is_editable(dist),
        find_spec=find_spec,
        warnings=warnings,
    )


def _namespace_sources(namespace: str, prefix: str, find_spec: Callable[[str], Any]) -> list[tuple[str, str]]:
    try:
        spec = find_spec(namespace)
    except (ImportError, ValueError):
        return []
    if spec is None:
        return []
    sources: list[tuple[str, str]] = []
    for location in getattr(spec, "submodule_search_locations", None) or ():
        root = Path(location)
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir() or child.name.startswith((".", "_")):
                continue
            if not (child / DOCS_DIR).is_dir():
                continue
            sources.append((f"{prefix}-{child.name}", f"{namespace}.{child.name}"))
    return sources


def _scan_sources(find_spec: Callable[[str], Any]) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = [("core", "akaribot.core"), ("builtin", "akaribot.modules.core")]
    for namespace, prefix in _NAMESPACES:
        sources.extend(_namespace_sources(namespace, prefix, find_spec))
    unique: dict[str, str] = {}
    seen_paths: set[str] = set()
    for key, import_path in sources:
        if import_path in seen_paths:
            continue
        seen_paths.add(import_path)
        unique.setdefault(key, import_path)
    return sorted(unique.items())


def _docs_entry_points() -> Iterable[Any]:
    return importlib.metadata.entry_points(group=DOCS_GROUP)


def _package_sort_key(item: dict[str, Any]) -> tuple[int, int, str, str]:
    return (_GROUP_RANK.get(item["group"], len(GROUP_ORDER)), item["order"], item["title"], item["key"])


def collect(
    entry_points: Callable[[], Iterable[Any]] | None = None,
    find_spec: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """收集各包的文档清单。

    :param entry_points: 返回 ``akaribot.docs`` 条目的可调用对象；缺省读取已安装元数据。
    :param find_spec: 按导入路径定位包的可调用对象；缺省使用 :func:`importlib.util.find_spec`。
    :return: ``{"schema": 1, "packages": [...], "warnings": [...]}``。
    """
    locate = find_spec or importlib.util.find_spec
    load = entry_points or _docs_entry_points
    warnings: list[str] = []
    try:
        discovered = sorted(load(), key=lambda item: str(getattr(item, "name", "")))
    except Exception as exc:  # noqa: BLE001 - 元数据损坏时退回目录扫描，仍给出可用结果
        warnings.append(f"读取 {DOCS_GROUP} entry point 失败（{exc}），改用目录扫描。")
        discovered = []
    packages: list[dict[str, Any]] = []
    seen: set[str] = set()
    if discovered:
        for entry_point in discovered:
            item = _package_from_entry_point(entry_point, locate, warnings)
            if item is None:
                continue
            if item["key"] in seen:
                warnings.append(f"{item['key']}: entry point 重复，已忽略后出现的条目。")
                continue
            seen.add(item["key"])
            packages.append(item)
    else:
        for key, import_path in _scan_sources(locate):
            item = _build_package(
                key,
                import_path,
                dist_name=_dist_from_path(import_path),
                version=DEFAULT_VERSION,
                summary="",
                editable=True,
                find_spec=locate,
                warnings=warnings,
            )
            if item is not None:
                packages.append(item)
    packages.sort(key=_package_sort_key)
    return {"schema": SCHEMA, "packages": packages, "warnings": warnings}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m akaribot.core.entrypoints.docs",
        description="列出各包的文档目录与页面。",
    )
    parser.add_argument("command", nargs="?", default="list", choices=("list",), help="子命令，目前只有 list")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出，供 CLI 解析")
    return parser


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码，0 成功、2 参数错误。
    """
    args = _build_parser().parse_args(argv)
    data = collect()
    if args.json:
        json.dump(data, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    for item in data["packages"]:
        print(f"{item['key']}\t{item['group']}\t{item['title']}\t{len(item['pages'])}\t{item['doc_path']}")
    for warning in data["warnings"]:
        print(f"! {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
