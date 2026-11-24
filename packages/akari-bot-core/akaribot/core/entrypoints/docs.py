"""包文档清单入口。

CLI 以子进程调用本模块列出各包 ``docs/`` 目录与页面。包发现只按 entry point 的导入路径定位包目录，
不导入目标包：导入会执行包内配置模板与其它导入期副作用。
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import inspect
import json
import re
import sys
import tomllib
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from packaging.requirements import InvalidRequirement, Requirement
from urllib.parse import urlparse
from urllib.request import url2pathname

from akaribot.core.constants.default import lang_list


DOCS_GROUP = "akaribot.docs"
DOCS_DIR = "docs"
DOC_META_DIR = "config"
DOC_META_GLOBAL_DIR = "global"
DOC_META_GLOBAL_FILES = ("docs.global.toml", "docs.global.json")
DOC_META_USER_FILES = ("docs.toml", "docs.json")
LEGACY_DOC_META_FILES = ("doc.toml", "doc.json")
DOC_META_DISPLAY = f"{DOC_META_DIR}/{DOC_META_GLOBAL_DIR}/docs.global.toml"
DOC_META_SCHEMA = 1
DEFAULT_ORDER = 500
DEFAULT_VERSION = "0+local"
SCHEMA = 1
GROUP_ORDER = ("core", "builtin", "cli", "testing", "module", "adapter", "asset", "library")
_GROUP_RANK = {name: index for index, name in enumerate(GROUP_ORDER)}
_KEY_GROUPS = {"core": "core", "builtin": "builtin", "cli": "cli", "testing": "testing"}
_KEY_PREFIX_GROUPS = (("module-", "module"), ("adapter-", "adapter"), ("assets-", "asset"))
_FRONT_MATTER_KEYS = frozenset({"title", "order", "description", "submenu"})
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


def _as_category(value: Any, label: str, warnings: list[str]) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        warnings.append(f"{label}: category 必须是单个字符串，已忽略。")
        return ""
    return value.strip()


def _dist_from_path(import_path: str) -> str:
    parts = import_path.split(".")
    if parts[:2] == ["akaribot", "modules"] and len(parts) >= 3:
        # 内置模块与核心运行时属于同一成员包，不按模块成员包命名规则命名。
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
        except Exception:  # noqa: BLE001 - 元数据残缺时按导入路径推导。
            name = ""
        if name:
            return name
    return _dist_from_path(import_path)


def _dist_version(dist: Any) -> str:
    if dist is None:
        return DEFAULT_VERSION
    try:
        return str(dist.version)
    except Exception:  # noqa: BLE001 - 元数据残缺时按源码克隆方式处理。
        return DEFAULT_VERSION


def _dist_summary(dist: Any) -> str:
    try:
        metadata = getattr(dist, "metadata", None)
        return str(metadata.get("Summary", "") or "") if metadata is not None else ""
    except Exception:  # noqa: BLE001 - Summary 缺失不影响清单。
        return ""


_SPECIFIER_ORDER = {"===": 0, "==": 1, "~=": 2, ">=": 3, ">": 4, "<=": 5, "<": 6, "!=": 7}


# 按项目声明顺序显示依赖，忽略 extra 声明的可选依赖。
def _format_dependency(text: str) -> str:
    ""
    try:
        requirement = Requirement(text)
    except InvalidRequirement:
        return text
    if requirement.marker is not None and "extra" in str(requirement.marker):
        return ""
    base = requirement.name
    if requirement.extras:
        base += f"[{','.join(sorted(requirement.extras))}]"
    specifiers = sorted(
        requirement.specifier,
        key=lambda specifier: (_SPECIFIER_ORDER.get(specifier.operator, 99), specifier.version),
    )
    rendered = ",".join(str(specifier) for specifier in specifiers)
    if rendered:
        base += rendered
    elif requirement.url:
        return f"{base} @ {requirement.url}"
    if requirement.marker is not None:
        base += f"; {requirement.marker}"
    return base


# 读取运行依赖，忽略 extra 声明的可选依赖。
def _dist_dependencies(dist: Any) -> list[str]:
    ""
    try:
        requires = getattr(dist, "requires", None) or []
    except Exception:  # noqa: BLE001 - 元数据残缺时按无依赖处理。
        return []
    dependencies: list[str] = []
    for item in requires:
        dependency = _format_dependency(str(item).strip())
        if dependency:
            dependencies.append(dependency)
    return dependencies


def _dist_dependencies_by_name(name: str) -> list[str]:
    try:
        dist = importlib.metadata.distribution(name)
    except importlib.metadata.PackageNotFoundError:
        return []
    return _dist_dependencies(dist)


def _is_editable(dist: Any) -> bool:
    if dist is None:
        return True
    try:
        raw = dist.read_text("direct_url.json")
    except Exception:  # noqa: BLE001 - 无法读取安装记录时按普通安装处理。
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


# 依次返回全局、用户覆盖与迁移兼容的文档元数据文件。
def _doc_meta_paths(doc_dir: Path) -> tuple[Path, ...]:
    ""
    global_files = tuple(
        path
        for path in (doc_dir / DOC_META_DIR / DOC_META_GLOBAL_DIR / name for name in DOC_META_GLOBAL_FILES)
        if path.is_file()
    )
    user_files = tuple(
        path for path in (doc_dir / DOC_META_DIR / name for name in DOC_META_USER_FILES) if path.is_file()
    )
    if global_files or user_files:
        return global_files + user_files
    return tuple(path for path in (doc_dir / name for name in LEGACY_DOC_META_FILES) if path.is_file())


def _merge_meta(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = _merge_meta(current, value)
        else:
            merged[key] = value
    return merged


def _read_doc_meta(doc_dir: Path, label: str, warnings: list[str]) -> dict[str, Any]:
    paths = _doc_meta_paths(doc_dir)
    if not paths:
        return {}
    merged: dict[str, Any] = {}
    for path in paths:
        display = path.relative_to(doc_dir).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            data = json.loads(text) if path.suffix.lower() == ".json" else tomllib.loads(text)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
            warnings.append(f"{label}: 无法解析 {display}（{exc}），已忽略该文件。")
            continue
        if not isinstance(data, Mapping):
            warnings.append(f"{label}: {display} 不是对象，已忽略该文件。")
            continue
        schema = data.get("schema", DOC_META_SCHEMA)
        if schema != DOC_META_SCHEMA:
            warnings.append(f"{label}: {display} 的 schema 为 {schema}，当前为 {DOC_META_SCHEMA}，已忽略该文件。")
            continue
        merged = _merge_meta(merged, data)
    return {
        name: merged[name]
        for name in (
            "title",
            "summary",
            "order",
            "hidden",
            "kind",
            "category",
            "category_order",
            "logo",
            "logo_dark",
            "avatar",
            "character",
            "credits",
            "brand",
            "overview",
        )
        if name in merged
    }


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
        "submenu": _as_text(front.get("submenu")),
    }


def _page_sort_key(page: dict[str, Any]) -> tuple[int, int, str]:
    name = Path(page["path"]).name
    role = 0 if name == "index.md" else 2 if name == "development.md" else 1
    return (role, int(page["order"]), str(page["path"]))


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


def _doc_asset(
    doc_dir: Path,
    meta: Mapping[str, Any],
    field: str,
    label: str,
    warnings: list[str],
) -> Path | None:
    value = meta.get(field)
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        warnings.append(f"{label}: {DOC_META_DISPLAY} 的 {field} 必须是相对路径字符串，已忽略。")
        return None
    package_dir = doc_dir.parent.resolve()
    candidate = (package_dir / value.strip()).resolve()
    if not candidate.is_relative_to(package_dir):
        warnings.append(f"{label}: {DOC_META_DISPLAY} 的 {field} 指向包目录之外，已忽略。")
        return None
    if not candidate.is_file():
        warnings.append(f"{label}: {DOC_META_DISPLAY} 声明的 {field} 不存在（{candidate}），已忽略。")
        return None
    return candidate


_PARAM_LINE = re.compile(r"^\s*:param\s+(?P<name>[^:]+):\s*(?P<text>.*)$")


def _doc_summary(obj: Any) -> str:
    text = inspect.getdoc(obj) or ""
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def _doc_params(obj: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    text = inspect.getdoc(obj) or ""
    current: str | None = None
    for line in text.splitlines():
        match = _PARAM_LINE.match(line)
        if match:
            current = match.group("name").strip()
            segment = re.split(r"\s*:(?:returns?|rtype|raises)\b", match.group("text"), maxsplit=1)[0]
            result[current] = segment.strip()
        elif current and line.strip():
            if re.match(r"\s*:(?:returns?|rtype|raises)\b", line):
                current = None
                continue
            result[current] = f"{result[current]} {line.strip()}".strip()
        elif current and not line.strip():
            current = None
    return result


def _annotation(value: Any) -> str:
    if value is inspect.Parameter.empty:
        return ""
    if isinstance(value, type):
        return value.__name__
    text = str(value).replace("typing.", "").replace("NoneType", "None")
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        text = text[1:-1]
    return re.sub(r"(['\"])([^'\"]*)\1", r"\2", text)


def _default(value: Any) -> str:
    if value is inspect.Parameter.empty:
        return ""
    text = repr(value)
    return text if len(text) <= 40 else text[:37] + "..."


def _parameter_payload(obj: Any) -> list[dict[str, str]]:
    try:
        signature = inspect.signature(obj)
    except (TypeError, ValueError):
        return []
    descriptions = _doc_params(obj)
    result: list[dict[str, str]] = []
    for parameter in signature.parameters.values():
        if parameter.name in {"self", "cls"}:
            continue
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            name = f"*{parameter.name}"
        elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
            name = f"**{parameter.name}"
        else:
            name = parameter.name
        result.append(
            {
                "name": name,
                "type": _annotation(parameter.annotation),
                "default": _default(parameter.default),
                "description": descriptions.get(parameter.name, ""),
            }
        )
    return result


def _source_name(obj: Any) -> str:
    module = getattr(obj, "__module__", "")
    return "core" if module.startswith("akaribot.") else "external"


def _callable_payload(name: str, obj: Any, kind: str) -> dict[str, Any]:
    try:
        signature = _annotation(str(inspect.signature(obj)))
    except (TypeError, ValueError):
        signature = ""
    return {
        "name": name,
        "kind": kind,
        "source": _source_name(obj),
        "module": str(getattr(obj, "__module__", "") or ""),
        "description": _doc_summary(obj),
        "signature": signature,
        "parameters": _parameter_payload(obj),
    }


def _class_payload(name: str, cls: type) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    nested: list[dict[str, Any]] = []
    try:
        members = inspect.getmembers(cls)
    except Exception:  # noqa: BLE001 - 单个类不可内省时仍保留类说明。
        members = []
    for member_name, member in members:
        if member_name.startswith("_"):
            continue
        if isinstance(member, property):
            source = _source_name(member.fget) if member.fget else "external"
            description = _doc_summary(member.fget) if member.fget else ""
            methods.append(
                {
                    "name": member_name,
                    "kind": "property",
                    "source": source,
                    "description": description,
                    "signature": "",
                    "parameters": [],
                }
            )
        elif inspect.isfunction(member) or inspect.ismethod(member):
            qualname = getattr(member, "__qualname__", "")
            owner = qualname.split(".", 1)[0]
            if owner in {"BaseModel", "dict", "Mapping", "MutableMapping", "Sequence"}:
                continue
            methods.append(_callable_payload(member_name, member, "method"))
        elif inspect.isclass(member) and member is not cls:
            qualname = getattr(member, "__qualname__", "")
            if qualname.startswith(f"{cls.__qualname__}."):
                nested.append(_class_payload(f"{name}.{member_name}", member))
    try:
        signature = _annotation(str(inspect.signature(cls)))
    except (TypeError, ValueError):
        signature = ""
    return {
        "name": name,
        "kind": "class",
        "source": _source_name(cls),
        "module": str(getattr(cls, "__module__", "") or ""),
        "description": _doc_summary(cls),
        "signature": signature,
        "parameters": _parameter_payload(cls),
        "methods": methods,
        "nested": nested,
    }


def _api_catalog() -> dict[str, Any]:
    try:
        from akaribot.core import api
        from akaribot.core.api import adapters
    except Exception:
        return {}
    groups: list[dict[str, Any]] = []
    for title, module in (("akaribot.core.api", api), ("akaribot.core.api.adapters", adapters)):
        entries: list[dict[str, Any]] = []
        for name in getattr(module, "__all__", ()):  # noqa: B007 - 仅遍历公开承诺接口。
            try:
                obj = getattr(module, name)
            except Exception:
                continue
            if inspect.isclass(obj):
                entries.append(_class_payload(name, obj))
            elif inspect.isfunction(obj) or inspect.ismethod(obj):
                entries.append(_callable_payload(name, obj, "function"))
            else:
                entries.append(
                    {
                        "name": name,
                        "kind": "constant",
                        "source": _source_name(obj),
                        "module": str(getattr(obj, "__module__", "") or ""),
                        "description": _doc_summary(obj),
                        "signature": "",
                        "parameters": [],
                    }
                )
        groups.append({"name": title, "entries": entries})
    return {"groups": groups}


def _build_package(
    key: str,
    import_path: str,
    *,
    dist_name: str,
    version: str,
    summary: str,
    dependencies: list[str],
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
    assets = {
        field: _doc_asset(doc_dir, meta, field, key, warnings) if meta else None
        for field in ("logo", "logo_dark", "avatar", "character", "credits")
    }
    return {
        "key": key,
        "dist": dist_name,
        "name": name,
        "group": _as_text(meta.get("kind")) or _group_of(key),
        "version": version,
        "dependencies": list(dependencies),
        "languages": dict(lang_list) if key == "core" else {},
        "api_catalog": _api_catalog() if key == "core" else {},
        "title": _as_text(meta.get("title")) or name,
        "summary": _as_text(meta.get("summary")) or summary,
        "order": _as_order(meta.get("order", DEFAULT_ORDER), key, warnings),
        "category": _as_category(meta.get("category"), key, warnings),
        "category_order": _as_order(meta.get("category_order", DEFAULT_ORDER), f"{key}.category_order", warnings),
        "doc_path": str(doc_dir),
        **{field: str(value) if value is not None else "" for field, value in assets.items()},
        "brand": meta.get("brand") is True,
        "editable": editable,
        "overview": meta.get("overview", True) is not False,
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
        dependencies=_dist_dependencies(dist),
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


def _editable_source(dist: Any) -> Path | None:
    try:
        payload = json.loads(dist.read_text("direct_url.json") or "{}")
    except Exception:  # noqa: BLE001 - 安装记录缺失或损坏时视为非可编辑安装。
        return None
    if not payload.get("dir_info", {}).get("editable"):
        return None
    url = urlparse(str(payload.get("url") or ""))
    return Path(url2pathname(url.path)) if url.scheme == "file" else None


def _stale_docs_entries() -> Iterable[Any]:
    # 可编辑安装的入口仅在安装时写入元数据，源码 pyproject 之后新增的 akaribot.docs 声明需要重新安装才能生效。
    for dist in importlib.metadata.distributions():
        try:
            if any(entry.group == DOCS_GROUP for entry in dist.entry_points):
                continue
        except Exception:  # noqa: BLE001 - 元数据残缺的包不参与补入。
            continue
        source = _editable_source(dist)
        if source is None:
            continue
        try:
            project = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8")).get("project", {})
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
            continue
        declared = project.get("entry-points", {}).get(DOCS_GROUP, {}) if isinstance(project, dict) else {}
        if not isinstance(declared, dict):
            continue
        for name, value in declared.items():
            yield SimpleNamespace(name=str(name), value=str(value), dist=dist)


def _package_sort_key(item: dict[str, Any]) -> tuple[int, int, str, str]:
    return (_GROUP_RANK.get(item["group"], len(GROUP_ORDER)), item["order"], item["title"], item["key"])


def collect(
    entry_points: Callable[[], Iterable[Any]] | None = None,
    find_spec: Callable[[str], Any] | None = None,
    stale_entries: Callable[[], Iterable[Any]] | None = None,
) -> dict[str, Any]:
    """收集各包的文档清单。

    :param entry_points: 返回 ``akaribot.docs`` 条目的可调用对象。默认读取已安装元数据。
    :param find_spec: 按导入路径定位包的可调用对象。默认使用 :func:`importlib.util.find_spec`。
    :param stale_entries: 返回“源码已声明、可编辑安装元数据未记录”条目的可调用对象。默认在读取
        已安装元数据时扫描可编辑安装，注入 ``entry_points`` 时不扫描。
    :return: ``{"schema": 1, "packages": [...], "warnings": [...]}``。
    """
    locate = find_spec or importlib.util.find_spec
    load = entry_points or _docs_entry_points
    stale = stale_entries or (_stale_docs_entries if entry_points is None else None)
    warnings: list[str] = []
    try:
        discovered = sorted(load(), key=lambda item: str(getattr(item, "name", "")))
    except Exception as exc:  # noqa: BLE001 - 元数据损坏时改用目录扫描，仍返回可用结果。
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
        refreshed: list[str] = []
        for entry_point in stale() if stale is not None else ():
            if entry_point.name in seen:
                continue
            item = _package_from_entry_point(entry_point, locate, warnings)
            if item is None:
                continue
            seen.add(item["key"])
            packages.append(item)
            refreshed.append(item["key"])
        if refreshed:
            warnings.append(
                f"{'、'.join(sorted(refreshed))}: 源码已声明 {DOCS_GROUP} 入口，但可编辑安装的元数据未记录，"
                "已按源码声明补入；重新安装这些包以刷新元数据（工作区实例可执行 akaribot module update --all）。"
            )
    else:
        for key, import_path in _scan_sources(locate):
            item = _build_package(
                key,
                import_path,
                dist_name=_dist_from_path(import_path),
                version=DEFAULT_VERSION,
                summary="",
                dependencies=_dist_dependencies_by_name(_dist_from_path(import_path)),
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

    :param argv: 命令行参数。默认取 ``sys.argv[1:]``。
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
