"""文档目录：从实例取包清单，合并 CLI 自身文档。

目录优先使用 core 的 ``docs list`` 入口；该入口不可用时退回 ``registry`` 的已装包清单，
用 ``<包根>/doc`` 构造最小条目，并把降级原因记入警告。
"""

from __future__ import annotations

import json
import tomllib
from importlib import metadata
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from akaribot.cli import __version__

from .config import default_labels
from .model import DEFAULT_ORDER, DocCatalog, DocPackage, DocPage

CLI_DIST = "akari-bot-cli"
CLI_KEY = "cli"
CLI_DOC_PATH = Path(__file__).resolve().parent.parent / "doc"
SCHEMA_VERSION = 1
GROUP_ORDER = ("core", "builtin", "cli", "testing", "module", "adapter", "asset", "library")
_GROUP_RANK = {name: index for index, name in enumerate(GROUP_ORDER)}
_PAGE_SUFFIXES = (".md",)


def load_catalog(
    instance: Any,
    include_cli: bool = True,
    labels: Mapping[str, str] | None = None,
    locales: Sequence[str] = (),
) -> DocCatalog:
    """读取实例可用的文档目录。

    :param instance: 带 ``root`` 与 ``run_core_capture`` 的实例。
    :param include_cli: 是否合并 CLI 自身文档。
    :param labels: 界面文案，用于首页与开发页的默认标题；缺省取随包默认值。
    :param locales: 非默认语言标签，其目录不进入默认语言的页面清单。
    :return: 已按 ``order`` 排序的目录。
    """
    labels = dict(labels or default_labels())
    tags = tuple(str(tag) for tag in locales)
    warnings: list[str] = []
    packages = _load_remote(instance, warnings, labels, tags)
    if include_cli:
        local = _load_local_cli(labels, tags)
        if local is not None:
            packages = [package for package in packages if package.key != local.key]
            packages.append(local)
    merged: dict[str, DocPackage] = {}
    for package in packages:
        merged.setdefault(package.key, package)
    ordered = tuple(sorted(merged.values(), key=_package_sort_key))
    return DocCatalog(packages=ordered, warnings=tuple(warnings))


def _package_sort_key(package: DocPackage) -> tuple[int, int, str, str]:
    # 分组顺序固定，避免首页与导航随包 key 的字母序把适配器排到模块之前。
    return (_GROUP_RANK.get(package.group, len(GROUP_ORDER)), package.order, package.title, package.key)


def _load_remote(
    instance: Any, warnings: list[str], labels: Mapping[str, str], tags: Sequence[str]
) -> list[DocPackage]:
    payload = _fetch_docs(instance, warnings)
    if payload is not None:
        reported = payload.get("warnings")
        if isinstance(reported, list):
            warnings.extend(text for item in reported if (text := str(item).strip()))
        return _parse_packages(payload, Path(instance.root), labels, tags)
    return _fallback_registry(instance, warnings, labels, tags)


def _fetch_docs(instance: Any, warnings: list[str]) -> Mapping[str, Any] | None:
    try:
        proc = instance.run_core_capture("docs", "list", "--json", timeout=60.0)
    except Exception as exc:  # noqa: BLE001 - 子进程形态由实例实现决定，任何失败都只影响目录来源
        warnings.append(f"docs 入口不可用，已回退 registry：{_reason(exc)}")
        return None
    if proc.returncode != 0:
        warnings.append(f"docs 入口不可用，已回退 registry：{_reason(proc)}")
        return None
    payload = _decode_json(proc.stdout or "")
    if not isinstance(payload, Mapping) or payload.get("schema") != SCHEMA_VERSION:
        warnings.append("docs 入口返回的清单版本不受支持，已回退 registry")
        return None
    if not isinstance(payload.get("packages"), list):
        warnings.append("docs 入口未返回 packages 列表，已回退 registry")
        return None
    return payload


def _parse_packages(
    payload: Mapping[str, Any], root: Path, labels: Mapping[str, str], tags: Sequence[str]
) -> list[DocPackage]:
    packages: list[DocPackage] = []
    for item in payload.get("packages", []):
        if not isinstance(item, Mapping):
            continue
        key = _text(item, "key", "name")
        if not key:
            continue
        dist = _text(item, "dist", "distribution") or key
        doc_path = _path_value(item, root)
        pages = _parse_pages(item.get("pages"), labels, tags)
        packages.append(
            DocPackage(
                key=key,
                group=_text(item, "group", "kind") or "module",
                dist=dist,
                name=_text(item, "name") or key,
                version=_text(item, "version"),
                title=_text(item, "title") or _text(item, "name") or key,
                summary=_text(item, "summary", "description"),
                doc_path=doc_path,
                pages=pages,
                logo=_text(item, "logo"),
                avatar=_text(item, "avatar"),
                order=_int_value(item.get("order")),
                editable=bool(item.get("editable", False)),
                category=_text(item, "category"),
                category_order=_int_value(item.get("category_order")),
                overview=bool(item.get("overview", True)),
            )
        )
    return packages


def _parse_pages(value: Any, labels: Mapping[str, str], tags: Sequence[str]) -> tuple[DocPage, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    pages: list[DocPage] = []
    for entry in value:
        if isinstance(entry, str):
            if not _locale_page(entry, tags):
                pages.append(DocPage(path=entry, title=_page_title_from_path(entry, labels)))
            continue
        if not isinstance(entry, Mapping):
            continue
        path = _text(entry, "path", "file")
        if not path or _locale_page(path, tags):
            continue
        pages.append(
            DocPage(
                path=path,
                title=_text(entry, "title") or _page_title_from_path(path, labels),
                order=_int_value(entry.get("order")),
                description=_text(entry, "description", "summary"),
                submenu=_text(entry, "submenu"),
            )
        )
    return tuple(sorted(pages, key=_page_sort_key))


def _locale_page(path: str, tags: Sequence[str]) -> bool:
    first = Path(path).parts[0] if Path(path).parts else ""
    return first in tags


def _fallback_registry(
    instance: Any, warnings: list[str], labels: Mapping[str, str], tags: Sequence[str]
) -> list[DocPackage]:
    try:
        proc = instance.run_core_capture("registry", "--json")
    except Exception as exc:  # noqa: BLE001 - 回退本身失败时目录为空，由警告说明原因
        warnings.append(f"registry 入口也不可用：{_reason(exc)}")
        return []
    if proc.returncode != 0:
        warnings.append(f"registry 入口返回非零退出码：{_reason(proc)}")
        return []
    payload = _decode_json(proc.stdout or "")
    packages: list[DocPackage] = []
    for item in _iter_package_items(payload):
        root_text = _text(item, "root")
        if not root_text:
            continue
        doc_path = Path(root_text) / "doc"
        if not doc_path.is_dir():
            continue
        key = _text(item, "name") or _short_name(_text(item, "dist", "package"))
        if not key:
            continue
        pages = _scan_pages(doc_path, labels, tags)
        meta = _read_local_meta(doc_path)
        packages.append(
            DocPackage(
                key=key,
                group=_text(item, "kind", "type") or "module",
                dist=_text(item, "dist", "distribution") or key,
                name=key,
                version=_text(item, "version"),
                title=_text(meta, "title") or key,
                summary=_text(item, "summary"),
                doc_path=doc_path,
                pages=pages,
                logo=_local_asset(doc_path, meta, "logo"),
                avatar=_local_asset(doc_path, meta, "avatar"),
                editable=bool(item.get("editable", False)),
                category=_text(meta, "category"),
                category_order=_int_value(meta.get("category_order")),
                overview=meta.get("overview", True) is not False,
            )
        )
    return packages


def _local_asset(doc_path: Path, meta: Mapping[str, Any], field: str) -> str:
    value = _text(meta, field)
    if not value:
        return ""
    candidate = (doc_path.parent / value).resolve()
    return str(candidate) if candidate.is_file() else ""


def _iter_package_items(payload: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, Mapping)]
    if not isinstance(payload, Mapping):
        return []
    items: list[Mapping[str, Any]] = []
    for name in ("packages", "entries", "installed", "items"):
        value = payload.get(name)
        if isinstance(value, list):
            items.extend(item for item in value if isinstance(item, Mapping))
        elif isinstance(value, Mapping):
            items.extend(item for item in value.values() if isinstance(item, Mapping))
    if payload.get("root"):
        items.append(payload)
    return items


def _load_local_cli(labels: Mapping[str, str], tags: Sequence[str]) -> DocPackage | None:
    if not CLI_DOC_PATH.is_dir():
        return None
    meta = _read_local_meta(CLI_DOC_PATH)
    if meta.get("hidden") is True:
        return None
    try:
        version = metadata.version(CLI_DIST)
    except Exception:  # noqa: BLE001 - 冻结产物可能没有 metadata，版本回退到包内常量
        version = __version__
    return DocPackage(
        key=CLI_KEY,
        group="cli",
        dist=CLI_DIST,
        name=CLI_KEY,
        version=version,
        title=_text(meta, "title") or CLI_KEY,
        summary=_text(meta, "summary"),
        doc_path=CLI_DOC_PATH,
        pages=_scan_pages(CLI_DOC_PATH, labels, tags),
        order=_int_value(meta.get("order")),
        category=_text(meta, "category"),
        category_order=_int_value(meta.get("category_order")),
        overview=meta.get("overview", True) is not False,
    )


def _read_local_meta(doc_path: Path) -> Mapping[str, Any]:
    try:
        payload = tomllib.loads((doc_path / "doc.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return {}
    return payload if isinstance(payload, Mapping) else {}


def _scan_pages(doc_path: Path, labels: Mapping[str, str], tags: Sequence[str]) -> tuple[DocPage, ...]:
    pages: list[DocPage] = []
    for path in sorted(doc_path.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _PAGE_SUFFIXES:
            continue
        relative = path.relative_to(doc_path)
        if any(part.startswith(".") for part in relative.parts) or _locale_page(relative.as_posix(), tags):
            continue
        pages.append(
            DocPage(
                path=relative.as_posix(),
                title=_read_title(path, relative.as_posix(), labels),
                order=0 if relative.as_posix() == "index.md" else DEFAULT_ORDER,
                submenu=_read_submenu(path),
            )
        )
    return tuple(sorted(pages, key=_page_sort_key))


def _read_title(path: Path, relative: str, labels: Mapping[str, str]) -> str:
    if relative == "index.md":
        return labels["overview"]
    try:
        with path.open(encoding="utf-8") as handle:
            for _ in range(20):
                line = handle.readline()
                if not line:
                    break
                if line.startswith("# "):
                    return line[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return _page_title_from_path(relative, labels)


def _read_submenu(path: Path) -> str:
    """读取页面 front matter 的 ``submenu``，用于侧栏二级分组。"""
    try:
        with path.open(encoding="utf-8") as handle:
            if handle.readline().strip() != "---":
                return ""
            for _ in range(40):
                line = handle.readline()
                if not line or line.strip() == "---":
                    break
                name, separator, value = line.partition(":")
                if separator and name.strip() == "submenu":
                    text = value.strip()
                    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
                        text = text[1:-1]
                    return text
    except (OSError, UnicodeDecodeError):
        pass
    return ""


def _page_sort_key(page: DocPage) -> tuple[int, int, str]:
    # 首页与开发页固定首尾，其余页面按 order 与路径排序，侧栏标签顺序才稳定。
    name = Path(page.path).name
    role = 0 if name == "index.md" else 2 if name == "development.md" else 1
    return (role, page.order, page.path)


def _page_title_from_path(relative: str, labels: Mapping[str, str]) -> str:
    stem = Path(relative).stem
    return labels["overview"] if stem == "index" else stem.replace("-", " ").replace("_", " ")


def _path_value(item: Mapping[str, Any], root: Path) -> Path:
    value = _text(item, "doc_path", "doc")
    if not value:
        return root / "doc"
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def _short_name(dist: str) -> str:
    text = dist or ""
    for prefix in ("akari-bot-module-", "akari-bot-adapter-", "akari-bot-"):
        if text.startswith(prefix):
            return text[len(prefix) :]
    return text


def _decode_json(text: str) -> Any:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        return value
    return None


def _reason(value: Any) -> str:
    stderr = getattr(value, "stderr", "") or ""
    if stderr.strip():
        return stderr.strip().splitlines()[-1][:200]
    text = str(value).strip()
    return text[:200] if text else type(value).__name__


def _text(item: Mapping[str, Any], *names: str) -> str:
    for name in names:
        value = item.get(name)
        if value is not None and not isinstance(value, (dict, list, tuple)):
            text = str(value).strip()
            if text:
                return text
    return ""


def _int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_ORDER


__all__ = [
    "CLI_DIST",
    "CLI_DOC_PATH",
    "CLI_KEY",
    "load_catalog",
]
