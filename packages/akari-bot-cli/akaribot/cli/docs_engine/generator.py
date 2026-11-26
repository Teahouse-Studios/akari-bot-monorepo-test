"""VitePress 站点源文件生成。

生成器只读取目录、配置与各包文档目录，产物全部放在 ``<实例根>/cache/docs/src`` 下。重建前先清空
该目录，且只接受位于 ``<实例根>/cache/docs`` 内的目标路径。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import textwrap
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

from .config import DEFAULT_ASSETS_DIR, DocsConfig, DocsLocaleConfig, site_asset_path
from .model import DocCatalog, DocPackage, DocPage, DocsError, page_url, read_doc_meta
from .theme import ThemeSpec, bundled_theme

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"})
ATTACHMENT_SUFFIXES = frozenset({".txt", ".pdf"})
ALLOWED_SUFFIXES = frozenset({".md"}) | IMAGE_SUFFIXES | ATTACHMENT_SUFFIXES
# 文档中的 ``{{I18N:key}}`` 为机器人模板语法。Vue 会将双花括号视为插值，行内代码需要显式设置 v-pre。
V_PRE_RULE = """const render = md.renderer.rules.code_inline
if (!render) return
md.renderer.rules.code_inline = (tokens, idx, options, env, self) => {
  const html = render(tokens, idx, options, env, self)
  return tokens[idx].content.includes("{{") ? html.replace("<code", "<code v-pre") : html
}"""
MARKDOWN_CONFIG = """  markdown: {
    config(md) {
      const render = md.renderer.rules.code_inline
      if (!render) return
      md.renderer.rules.code_inline = (tokens, idx, options, env, self) => {
        const html = render(tokens, idx, options, env, self)
        return tokens[idx].content.includes("{{") ? html.replace("<code", "<code v-pre") : html
      }
    }
  }"""
KEY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SLUG_PATTERN = re.compile(r"[^a-z0-9_-]+")
LINK_PATTERN = re.compile(r"(?P<open>!?\[[^\]]*\]\()(?P<target>[^)\s]+)(?P<close>(?:\s+\"[^\"]*\")?\))")
SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FENCE_PATTERN = re.compile(r"^\s*(?:```|~~~)")
HOME_DIR = Path(__file__).resolve().parent / "home"
HOME_CONFIG = HOME_DIR / "home.json"
FOOTER_DIR = Path(__file__).resolve().parent / "footer"
SNIPPETS_DIR = Path(__file__).resolve().parent / "snippets"


def generate(
    catalog: DocCatalog,
    src_dir: Path,
    config: DocsConfig,
    *,
    theme: ThemeSpec | None = None,
    link_packages: Iterable[DocPackage] | None = None,
) -> None:
    """按目录与配置生成整个站点源目录。

    :param catalog: 参与构建的文档目录。
    :param src_dir: 目标源目录，必须位于实例的 ``cache/docs`` 下。
    :param config: 实例文档配置。
    :param theme: 主题。默认使用 CLI 内置主题。
    :param link_packages: 用于跨包链接重写的全部包。默认只用 ``catalog``。子集构建时传入完整目录，
        使指向未选包的源码相对链接仍能折算成站点地址。
    :raises DocsError: 目标路径越界、包 key 非法或源文件经符号链接逃逸。
    """
    spec = theme or bundled_theme()
    source = _checked_source_dir(src_dir, config)
    if source.exists():
        shutil.rmtree(source)
    source.mkdir(parents=True)

    roots = {Path(package.doc_path).resolve(): package for package in (link_packages or catalog.packages)}
    tags = [locale.tag for locale in config.locales]
    views: list[_LocaleView] = []
    for locale in config.locales:
        prefix = "" if locale is config.default_locale else f"/{locale.tag}"
        packages = tuple(_locale_package(package, config, locale, tags) for package in catalog.packages)
        target = source if not prefix else source / locale.tag
        target.mkdir(parents=True, exist_ok=True)
        groups = _grouped(packages)
        _write_index(target, packages, config, locale, theme=spec)
        for group, items in groups.items():
            _write_group_page(target, group, items, config, locale)
        for package in packages:
            _copy_package(source, target, package, roots, locale, tags)
        views.append(_LocaleView(locale=locale, prefix=prefix, packages=packages, groups=groups, target=target))
    assets = _prepare_site_assets(source, config, catalog.packages)
    _copy_theme_public(source, spec)
    _write_vitepress_config(source, views, config, spec, assets)
    _write_theme(source, spec)
    _write_home(source, spec)


def collect_files(doc_path: Path, *, exclude: Sequence[str] = ()) -> list[tuple[str, Path]]:
    """列出包文档目录下允许发布的文件。

    :param doc_path: 包文档目录。
    :param exclude: 不进入的顶层目录名，用于跳过语言子目录。
    :return: ``(相对路径, 已解析的源文件)`` 列表，按相对路径排序。
    :raises DocsError: 文件或目录符号链接指向文档目录之外。
    """
    root = Path(doc_path).expanduser().resolve()
    if not root.is_dir():
        return []
    found: list[tuple[str, Path]] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        kept: list[str] = []
        for name in sorted(dirs):
            if Path(current) == root and name in exclude:
                continue
            candidate = Path(current) / name
            if candidate.is_symlink():
                if not candidate.resolve().is_relative_to(root):
                    raise DocsError("cli.docs.error.unsafe_path", path=str(candidate))
                continue
            kept.append(name)
        dirs[:] = kept
        for name in sorted(files):
            path = Path(current) / name
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                raise DocsError("cli.docs.error.unsafe_path", path=str(path))
            if resolved.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            found.append((resolved.relative_to(root).as_posix(), resolved))
    return sorted(found)


def group_slug(group: str) -> str:
    """将分组名称转换为文件名与 URL 片段。"""
    slug = SLUG_PATTERN.sub("-", (group or "").lower()).strip("-")
    return slug or "other"


def _checked_source_dir(src_dir: Path, config: DocsConfig) -> Path:
    allowed = config.cache_docs_dir.resolve()
    source = Path(src_dir).expanduser().resolve()
    if source == allowed or not source.is_relative_to(allowed):
        raise DocsError("cli.docs.error.unsafe_path", path=str(src_dir))
    return source


def _checked_key(key: str) -> str:
    if not KEY_PATTERN.match(key or ""):
        raise DocsError("cli.docs.error.unsafe_path", path=key)
    return key


@dataclass(frozen=True)
class _LocaleView:
    locale: DocsLocaleConfig
    prefix: str
    packages: tuple[DocPackage, ...]
    groups: dict[str, list[DocPackage]]
    target: Path


def _locale_package(
    package: DocPackage, config: DocsConfig, locale: DocsLocaleConfig, tags: Sequence[str]
) -> DocPackage:
    doc_dir = Path(package.doc_path)
    default = locale is config.default_locale or locale.tag == config.default_locale.tag
    title, summary = _locale_meta(doc_dir, locale.tag) if not default else (package.title, package.summary)
    if default:
        pages = [page for page in package.pages if not _locale_page(page.path, tags)]
    else:
        lang_dir = doc_dir / locale.tag
        pages = _scan_locale_pages(lang_dir) if lang_dir.is_dir() else list(package.pages)
    if package.key == "core" and package.api_catalog:
        existing = {page.path for page in pages}
        pages = list(pages) + [page for page in _api_doc_pages(package.api_catalog) if page.path not in existing]
    return replace(package, title=title or package.title, summary=summary or package.summary, pages=pages)


def _locale_page(path: str, tags: Sequence[str]) -> bool:
    first = Path(path).parts[0] if Path(path).parts else ""
    return first in tags


def _scan_locale_pages(directory: Path) -> list[DocPage]:
    pages: list[DocPage] = []
    for relative, path in collect_files(directory):
        if path.suffix.lower() != ".md":
            continue
        pages.append(DocPage(path=relative, title=_first_heading(path), order=0, description=""))
    pages.sort(
        key=lambda page: (Path(page.path).name == "development.md", Path(page.path).name != "index.md", page.path)
    )
    return pages


def _first_heading(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return path.stem


def _locale_meta(doc_dir: Path, tag: str) -> tuple[str, str]:
    data = read_doc_meta(doc_dir)
    locales = data.get("locales")
    if not isinstance(locales, Mapping):
        return "", ""
    entry = locales.get(tag)
    if not isinstance(entry, Mapping):
        return "", ""
    return _text(entry, "title"), _text(entry, "summary")


def _package_entry(package: DocPackage) -> str:
    # 未提供概览页的包以第一页作为入口，供首页、分组页与顶栏链接复用。
    if package.overview:
        return "index.md"
    return package.pages[0].path if package.pages else "index.md"


API_CATALOG_PLACEHOLDER = "<!-- API_CATALOG -->"
API_CATALOG_SUBMENU = "完整 API 导出清单"
API_CATALOG_INDEX = "api-reference.md"
API_CATALOG_DIR = "api"
API_CATALOG_OTHERS = "api/functions-and-constants.md"


def _api_page_specs(
    catalog: Mapping[str, object],
) -> tuple[list[dict[str, object]], dict[str, str]]:
    classes: list[tuple[str, Mapping[str, object]]] = []
    others: list[tuple[str, Mapping[str, object]]] = []
    groups = catalog.get("groups", [])
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, Mapping):
                continue
            group_name = str(group.get("name", "")).strip()
            entries = group.get("entries", [])
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, Mapping):
                    continue
                name = str(entry.get("name", "")).strip()
                if not name:
                    continue
                item = (group_name, entry)
                if entry.get("kind") == "class":
                    classes.append(item)
                else:
                    others.append(item)
    specs: list[dict[str, object]] = [
        {
            "path": API_CATALOG_INDEX,
            "title": "API 导出索引",
            "submenu": "",
            "entries": [],
            "kind": "index",
        }
    ]
    used = {API_CATALOG_INDEX}
    page_by_name: dict[str, str] = {}

    def register(entry: Mapping[str, object], page: str, prefix: str = "") -> None:
        name = str(entry.get("name", "")).strip()
        if not name:
            return
        full = name if not prefix or name.startswith(f"{prefix}.") else f"{prefix}.{name}"
        page_by_name[full] = page
        methods = entry.get("methods", [])
        if isinstance(methods, list):
            for method in methods:
                if isinstance(method, Mapping):
                    method_name = str(method.get("name", "")).strip()
                    if method_name:
                        page_by_name[f"{full}.{method_name}"] = page
        nested = entry.get("nested", [])
        if isinstance(nested, list):
            for child in nested:
                if isinstance(child, Mapping):
                    register(child, page, full)

    for group_name, entry in classes:
        module_name = str(entry.get("module") or group_name).strip()
        name = str(entry.get("name", "")).strip()
        slug = _api_anchor(name) or "class"
        path = f"{API_CATALOG_DIR}/{slug}.md"
        suffix = 2
        while path in used:
            path = f"{API_CATALOG_DIR}/{slug}-{suffix}.md"
            suffix += 1
        used.add(path)
        specs.append(
            {
                "path": path,
                "title": name,
                "submenu": module_name,
                "group": module_name or group_name,
                "entries": [entry],
                "kind": "class",
            }
        )
        register(entry, path)
    other_groups: dict[str, list[Mapping[str, object]]] = {}
    for group_name, entry in others:
        module_name = str(entry.get("module") or group_name).strip()
        other_groups.setdefault(module_name or group_name, []).append(entry)
    for group_name, entries in other_groups.items():
        relative = group_name.removeprefix("akaribot.core.api").strip(".")
        suffix = f"{_api_anchor(relative) or 'other'}-functions-and-constants"
        path = API_CATALOG_OTHERS if relative == "" else f"{API_CATALOG_DIR}/{suffix}.md"
        specs.append(
            {
                "path": path,
                "title": "函数与常量",
                "submenu": group_name,
                "group": group_name,
                "entries": list(entries),
                "kind": "others",
            }
        )
        for entry in entries:
            name = str(entry.get("name", "")).strip()
            if name:
                page_by_name[name] = path
    return specs, page_by_name


def _api_body_lines(entry: Mapping[str, object], level: int, *, prefix: str = "") -> list[str]:
    name = str(entry.get("name", "")).strip()
    full = name if not prefix or name.startswith(f"{prefix}.") else f"{prefix}.{name}"
    kind = str(entry.get("kind", ""))
    labels = {"class": "类", "function": "函数", "constant": "常量"}
    lines = [f"{'#' * level} `{full}`", "", labels.get(kind, kind) + "。", ""]
    description = str(entry.get("description", "")).strip()
    lines.append(description or "暂无对应描述。")
    signature = str(entry.get("signature", "")).strip()
    if signature:
        lines.extend(["", f"签名：`{signature}`"])
    parameters = entry.get("parameters", [])
    if isinstance(parameters, list) and parameters:
        lines.extend(["", "参数："])
        lines.extend(_api_parameter_lines(parameters))
    methods = entry.get("methods", [])
    if isinstance(methods, list):
        for method in methods:
            if isinstance(method, Mapping):
                lines.extend([""] + _api_method_lines(method, full, level + 1))
    nested = entry.get("nested", [])
    if isinstance(nested, list):
        for child in nested:
            if isinstance(child, Mapping):
                lines.extend([""] + _api_body_lines(child, level + 1, prefix=full))
    return lines


def _api_method_lines(entry: Mapping[str, object], class_name: str, level: int) -> list[str]:
    name = str(entry.get("name", "")).strip()
    full = f"{class_name}.{name}"
    lines = [f"{'#' * level} `{full}`", ""]
    description = str(entry.get("description", "")).strip()
    lines.append(description or "暂无对应描述。")
    signature = str(entry.get("signature", "")).strip()
    if signature:
        lines.extend(["", f"签名：`{signature}`"])
    parameters = entry.get("parameters", [])
    if isinstance(parameters, list) and parameters:
        lines.extend(["", "参数："])
        lines.extend(_api_parameter_lines(parameters))
    return lines


def _api_landing_markdown(specs: Sequence[Mapping[str, object]]) -> str:
    groups: dict[str, list[Mapping[str, object]]] = {}
    for spec in specs:
        if spec.get("kind") == "index":
            continue
        group_name = str(spec.get("group", "") or "其他")
        groups.setdefault(group_name, []).append(spec)
    lines = ["", "按导出名拆成独立页面。" if groups else "当前构建没有生成 API 目录。", ""]
    for group_name, group_specs in groups.items():
        lines.extend([f"## {group_name}", ""])
        for spec in group_specs:
            if spec.get("kind") == "others":
                lines.append(f"- [函数与常量]({spec.get('path')})")
                continue
            name = str(spec.get("title", ""))
            path = str(spec.get("path", ""))
            lines.append(f"- [`{name}`]({path})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _api_page_markdown(spec: Mapping[str, object]) -> str:
    if spec.get("kind") == "others":
        lines = ["# 函数与常量", ""]
        for entry in spec.get("entries", []):
            if isinstance(entry, Mapping):
                lines.extend(_api_body_lines(entry, 2))
                lines.append("")
        return "\n".join(lines).rstrip() + "\n"
    entry = next((item for item in spec.get("entries", []) if isinstance(item, Mapping)), {})
    return "\n".join(_api_body_lines(entry, 1)).rstrip() + "\n"


def _api_doc_pages(catalog: Mapping[str, object]) -> list[DocPage]:
    specs, _ = _api_page_specs(catalog)
    pages: list[DocPage] = []
    for index, spec in enumerate(specs):
        path = str(spec.get("path", ""))
        if path == API_CATALOG_INDEX or not path:
            continue
        pages.append(
            DocPage(
                path=path,
                title=str(spec.get("title", "")),
                order=901 + index,
                submenu=str(spec.get("submenu") or API_CATALOG_SUBMENU),
            )
        )
    return pages


def _write_api_pages(destination: Path, catalog: Mapping[str, object]) -> None:
    specs, _ = _api_page_specs(catalog)
    for spec in specs:
        if spec.get("kind") == "index":
            continue
        path = destination / str(spec.get("path", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_api_page_markdown(spec), encoding="utf-8")
    index = destination / API_CATALOG_INDEX
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        landing = _api_landing_markdown(specs)
        if API_CATALOG_PLACEHOLDER in text:
            text = text.replace(API_CATALOG_PLACEHOLDER, landing)
        else:
            text = text.rstrip() + "\n" + landing
        index.write_text(text, encoding="utf-8")


def _api_anchor(name: str) -> str:
    text = name.lower().replace(".", "-").replace("_", "-")
    return re.sub(r"[^a-z0-9-]+", "", text).strip("-")


def _api_link_table(catalog: Mapping[str, object]) -> tuple[dict[str, str], dict[str, str], set[str]]:
    exact: dict[str, str] = {}
    unqualified: dict[str, str] = {}
    classes: set[str] = set()
    candidates: dict[str, list[str]] = {}
    _, page_by_name = _api_page_specs(catalog)

    def add(name: str, anchor: str) -> None:
        page = page_by_name.get(name)
        target = f"{page}#{anchor}" if page else f"#{anchor}"
        exact[name] = target
        if "." not in name:
            method_names = candidates.setdefault(name, [])
            if target not in method_names:
                method_names.append(target)

    def visit(entry: Mapping[str, object], prefix: str = "") -> None:
        name = str(entry.get("name", "")).strip()
        if not name:
            return
        full = name if not prefix or name.startswith(f"{prefix}.") else f"{prefix}.{name}"
        anchor = _api_anchor(full)
        add(full, anchor)
        if entry.get("kind") == "class":
            classes.add(full)
            methods = entry.get("methods", [])
            if isinstance(methods, list):
                for method in methods:
                    if isinstance(method, Mapping):
                        method_name = str(method.get("name", "")).strip()
                        if method_name:
                            add(f"{full}.{method_name}", _api_anchor(f"{full}.{method_name}"))
            nested = entry.get("nested", [])
            if isinstance(nested, list):
                for child in nested:
                    if isinstance(child, Mapping):
                        visit(child, full)

    groups = catalog.get("groups", [])
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, Mapping):
                continue
            entries = group.get("entries", [])
            if isinstance(entries, list):
                for entry in entries:
                    if isinstance(entry, Mapping):
                        visit(entry)
    for name, anchors in candidates.items():
        unique = {anchor for anchor in anchors}
        if len(unique) == 1:
            unqualified[name] = next(iter(unique))
    return exact, unqualified, classes


CODE_SPAN_PATTERN = re.compile(r"`([^`\n]+)`")
HEADING_PATTERN = re.compile(r"^(#{2,3})\s+(.+)$")
API_LINK_PATTERN = re.compile(r"\[[^\]]*\]\([^)]*\)")


def _api_heading_context(line: str) -> tuple[bool, str | None]:
    match = HEADING_PATTERN.match(line)
    if not match:
        return False, None
    text = match.group(2).strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").strip()
    text = re.sub(r"\(\)$", "", text)
    return True, text


def _link_api_code(segment: str, context: str, exact: Mapping[str, str], unqualified: Mapping[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        content = match.group(1).strip()
        if not content or " " in content:
            return match.group(0)
        bare = content[:-2] if content.endswith("()") else content
        anchor = exact.get(bare)
        if anchor is None and context:
            anchor = exact.get(f"{context}.{bare}")
        if anchor is None and "." not in bare:
            anchor = unqualified.get(bare)
        if anchor is None:
            return match.group(0)
        return f"[`{content}`]({anchor})"

    return CODE_SPAN_PATTERN.sub(replace, segment)


def _link_api_references(text: str, catalog: Mapping[str, object]) -> str:
    exact, unqualified, classes = _api_link_table(catalog)
    if not exact:
        return text
    lines = text.splitlines()
    result: list[str] = []
    context = ""
    in_fence = False
    in_frontmatter = False
    for index, line in enumerate(lines):
        if index == 0 and line.strip() == "---":
            in_frontmatter = True
            result.append(line)
            continue
        if in_frontmatter:
            result.append(line)
            if line.strip() == "---":
                in_frontmatter = False
            continue
        if FENCE_PATTERN.match(line):
            in_fence = not in_fence
            result.append(line)
            continue
        if in_fence:
            result.append(line)
            continue
        is_heading, heading = _api_heading_context(line)
        if is_heading:
            if heading in classes:
                context = heading
            elif line.startswith("## "):
                context = ""
        parts: list[str] = []
        cursor = 0
        for link in API_LINK_PATTERN.finditer(line):
            parts.append(_link_api_code(line[cursor : link.start()], context, exact, unqualified))
            parts.append(link.group(0))
            cursor = link.end()
        parts.append(_link_api_code(line[cursor:], context, exact, unqualified))
        result.append("".join(parts))
    return "\n".join(result) + ("\n" if text.endswith("\n") else "")


def _api_catalog_markdown(catalog: Mapping[str, object]) -> str:
    groups = catalog.get("groups", [])
    if not isinstance(groups, list) or not groups:
        return "当前构建没有生成 API 目录。\n"
    lines: list[str] = []
    kind_labels = {"class": "类", "function": "函数", "constant": "常量"}
    for group in groups:
        if not isinstance(group, Mapping):
            continue
        lines.append(f"## {group.get('name', '')}")
        lines.append("")
        entries = group.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, Mapping):
                continue
            name = str(entry.get("name", ""))
            kind = str(entry.get("kind", ""))
            lines.append(f"### `{name}`")
            lines.append("")
            lines.append(kind_labels.get(kind, kind) + "。")
            description = str(entry.get("description", "")).strip()
            lines.append("")
            lines.append(description or "暂无对应描述。")
            signature = str(entry.get("signature", "")).strip()
            if signature:
                lines.append("")
                lines.append(f"签名：`{signature}`")
            parameters = entry.get("parameters", [])
            if isinstance(parameters, list) and parameters:
                lines.append("")
                lines.append("参数：")
                lines.extend(_api_parameter_lines(parameters))
            methods = entry.get("methods", [])
            if isinstance(methods, list) and methods:
                for method in methods:
                    if not isinstance(method, Mapping):
                        continue
                    method_name = str(method.get("name", ""))
                    lines.append("")
                    lines.append(f"#### `{name}.{method_name}`")
                    lines.append("")
                    method_description = str(method.get("description", "")).strip()
                    lines.append(method_description or "暂无对应描述。")
                    lines.append("")
                    method_signature = str(method.get("signature", "")).strip()
                    if method_signature:
                        lines.append(f"签名：`{method_signature}`")
                        lines.append("")
                    method_parameters = method.get("parameters", [])
                    if isinstance(method_parameters, list) and method_parameters:
                        lines.append("参数：")
                        lines.extend(_api_parameter_lines(method_parameters))
            nested_entries = entry.get("nested", [])
            if isinstance(nested_entries, list) and nested_entries:
                for nested in nested_entries:
                    if not isinstance(nested, Mapping):
                        continue
                    nested_name = str(nested.get("name", ""))
                    lines.append("")
                    lines.append(f'<a id="{_api_anchor(nested_name)}"></a>')
                    lines.append(f"### `{nested_name}`")
                    lines.append("")
                    nested_description = str(nested.get("description", "")).strip()
                    lines.append(nested_description or "暂无对应描述。")
                    nested_methods = nested.get("methods", [])
                    if isinstance(nested_methods, list):
                        for method in nested_methods:
                            if not isinstance(method, Mapping):
                                continue
                            method_name = str(method.get("name", ""))
                            anchor = _api_anchor(f"{nested_name}.{method_name}")
                            lines.append("")
                            lines.append(f'<a id="{anchor}"></a>')
                            lines.append(f"#### `{nested_name}.{method_name}`")
                            lines.append("")
                            method_description = str(method.get("description", "")).strip()
                            lines.append(method_description or "暂无对应描述。")
                            lines.append("")
                            method_signature = str(method.get("signature", "")).strip()
                            if method_signature:
                                lines.append(f"签名：`{method_signature}`")
                                lines.append("")
                            method_parameters = method.get("parameters", [])
                            if isinstance(method_parameters, list) and method_parameters:
                                lines.append("参数：")
                                lines.extend(_api_parameter_lines(method_parameters))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _api_parameter_lines(parameters: Iterable[object]) -> list[str]:
    lines: list[str] = []
    for parameter in parameters:
        if not isinstance(parameter, Mapping):
            continue
        name = str(parameter.get("name", ""))
        type_name = str(parameter.get("type", "")).strip()
        default = str(parameter.get("default", "")).strip()
        description = str(parameter.get("description", "")).strip()
        detail = ""
        if type_name:
            detail += f"`{type_name}`"
        if default:
            detail += ("，" if detail else "") + f"默认 `{default}`"
        suffix = f"（{detail}）" if detail else ""
        line = f"- `{name}`{suffix}"
        if description:
            line += f"：{description}"
        lines.append(line)
    return lines


def _copy_package(
    source: Path,
    target: Path,
    package: DocPackage,
    roots: dict[Path, DocPackage],
    locale: DocsLocaleConfig,
    tags: Sequence[str],
) -> None:
    key = _checked_key(package.key)
    doc_dir = Path(package.doc_path)
    if target != source:
        lang_dir = doc_dir / locale.tag
        if lang_dir.is_dir():
            doc_dir = lang_dir
    destination = target / key
    destination.mkdir(parents=True, exist_ok=True)
    exclude = tags if doc_dir == Path(package.doc_path) else ()
    copied: set[str] = set()
    for relative, path in collect_files(doc_dir, exclude=exclude):
        suffix = path.suffix.lower()
        if suffix in ATTACHMENT_SUFFIXES or suffix in IMAGE_SUFFIXES:
            if target == source:
                attachment = source / "public" / key / relative
            else:
                attachment = source / "public" / locale.tag / key / relative
            attachment.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, attachment)
            if suffix in ATTACHMENT_SUFFIXES:
                copied.add(relative)
                continue
        page = destination / relative
        page.parent.mkdir(parents=True, exist_ok=True)
        if suffix == ".md":
            text = path.read_text(encoding="utf-8")
            text = _rewrite_links(text, path, package, roots, prefix="" if target == source else f"/{locale.tag}")
            if relative == "index.md" and doc_dir == Path(package.doc_path):
                text = _inject_module_meta(text, package.doc_path)
            if package.key == "core" and relative != "api-reference.md":
                text = _link_api_references(text, package.api_catalog)
            page.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, page)
        copied.add(relative)
    if target != source and doc_dir != Path(package.doc_path):
        for relative, path in collect_files(package.doc_path, exclude=tags):
            if relative in copied or path.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            if path.suffix.lower() in ATTACHMENT_SUFFIXES or path.suffix.lower() in IMAGE_SUFFIXES:
                attachment = source / "public" / locale.tag / key / relative
                attachment.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, attachment)
                if path.suffix.lower() in ATTACHMENT_SUFFIXES:
                    continue
            page = destination / relative
            page.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix.lower() == ".md":
                text = _rewrite_links(path.read_text(encoding="utf-8"), path, package, roots, prefix=f"/{locale.tag}")
                page.write_text(text, encoding="utf-8")
            else:
                shutil.copy2(path, page)
    if package.overview and "index.md" not in copied:
        page = destination / "index.md"
        page.write_text(f"# {package.title}\n\n{package.summary or package.name}\n", encoding="utf-8")
    if package.key == "core" and package.api_catalog:
        _write_api_pages(destination, package.api_catalog)


def _rewrite_links(
    text: str,
    source: Path,
    package: DocPackage,
    roots: dict[Path, DocPackage],
    *,
    prefix: str = "",
) -> str:
    # 文档在源码树中使用相对路径互相引用。生成站点时包目录已重新排列，跨包链接需要转换为 URL。
    lines = text.splitlines(keepends=True)
    fenced = False
    for index, line in enumerate(lines):
        if FENCE_PATTERN.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        lines[index] = LINK_PATTERN.sub(lambda match: _rewrite_link(match, source, package, roots, prefix), line)
    return "".join(lines)


def _rewrite_link(
    match: re.Match[str], source: Path, package: DocPackage, roots: dict[Path, DocPackage], prefix: str
) -> str:
    target = match.group("target")
    if not target or target.startswith(("/", "#")) or SCHEME_PATTERN.match(target):
        return match.group(0)
    path_part, hash_mark, anchor = target.partition("#")
    path_part, query_mark, query = path_part.partition("?")
    resolved = (source.parent / path_part).resolve()
    for root, other in roots.items():
        if not resolved.is_relative_to(root):
            continue
        if other.key == package.key:
            return match.group(0)
        relative = resolved.relative_to(root).as_posix()
        url = page_url(other.key, relative) if relative.endswith(".md") else f"/{other.key}/{relative}"
        suffix = f"{query_mark}{query}" if query_mark else ""
        suffix += f"{hash_mark}{anchor}" if hash_mark else ""
        return f"{match.group('open')}{prefix}{url}{suffix}{match.group('close')}"
    return match.group(0)


def _text(data: Mapping[str, object], key: str) -> str:
    value = data.get(key)
    return str(value).strip() if isinstance(value, str) else ""


def _inject_module_meta(text: str, doc_path: Path) -> str:
    modules = _read_meta_modules(doc_path)
    if not modules:
        return text
    payload = json.dumps(modules, ensure_ascii=False, separators=(",", ":")).replace("'", "&#39;")
    block = f"<ModuleMeta :modules='{payload}' />\n\n"
    lines = text.splitlines(keepends=True)
    start = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                start = index + 1
                break
    for index in range(start, len(lines)):
        if lines[index].startswith("# "):
            return "".join(lines[: index + 1]) + "\n" + block + "".join(lines[index + 1 :])
    return block + text


def _read_meta_modules(doc_path: Path) -> list[dict[str, object]]:
    data = read_doc_meta(Path(doc_path))
    meta = data.get("meta")
    if not isinstance(meta, Mapping):
        return []
    modules = meta.get("modules")
    if not isinstance(modules, list):
        return []
    return [dict(item) for item in modules if isinstance(item, Mapping) and item.get("name")]


def _prefix_for(locale: DocsLocaleConfig, config: DocsConfig) -> str:
    return "" if locale.tag == config.default_locale.tag else f"/{locale.tag}"


def _site_link(prefix: str, key: str, path: str) -> str:
    return f"{prefix}{page_url(key, path)}"


def _write_index(
    source: Path,
    packages: Sequence[DocPackage],
    config: DocsConfig,
    locale: DocsLocaleConfig,
    *,
    theme: ThemeSpec | None = None,
) -> None:
    component = str((theme.config if theme else {}).get("home_component") or "").strip()
    if component:
        _write_home_index(source, packages, config, locale, component)
        return
    prefix = _prefix_for(locale, config)
    labels = locale.labels
    lines = [f"# {locale.title or config.site.title}", "", labels["index_intro"], ""]
    for group, items in _grouped(packages).items():
        lines.extend([f"## {_group_title(group, locale.group_titles)}", ""])
        for package in items:
            summary = f"：{package.summary}" if package.summary else ""
            lines.append(f"- [{package.title}]({_site_link(prefix, package.key, _package_entry(package))}){summary}")
        lines.append("")
    (source / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_home_index(
    source: Path,
    packages: Sequence[DocPackage],
    config: DocsConfig,
    locale: DocsLocaleConfig,
    component: str,
) -> None:
    title = locale.title or config.site.title
    payload = json.dumps(_home_payload(packages, config, locale), ensure_ascii=False, separators=(",", ":"))
    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        "toc: false",
        "outline: false",
        f"home: {json.dumps(payload, ensure_ascii=False)}",
        "---",
        "",
        f"<{component} />",
        "",
    ]
    (source / "index.md").write_text("\n".join(lines), encoding="utf-8")


def _load_home_config() -> dict[str, object]:
    try:
        payload = json.loads(HOME_CONFIG.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason=str(exc)) from exc
    if not isinstance(payload, dict) or payload.get("schema") != 1:
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="schema must be 1")
    return payload


def _home_payload(
    packages: Sequence[DocPackage],
    config: DocsConfig,
    locale: DocsLocaleConfig,
) -> dict[str, object]:
    prefix = _prefix_for(locale, config)
    by_key = {package.key: package for package in packages}
    grouped = _grouped(packages)

    def package_href(key: str, path: str | None = None) -> str:
        package = by_key.get(key)
        if package is None:
            return f"{prefix}/"
        return _site_link(prefix, key, path or _package_entry(package))

    def group_href(group: str) -> str:
        return f"{prefix}/groups/{group_slug(group)}/"

    def link(value: Mapping[str, object]) -> str:
        if "url" in value:
            return str(value["url"])
        if "group" in value:
            return group_href(str(value["group"]))
        if "package" in value:
            page = value.get("page")
            return package_href(str(value["package"]), str(page) if page else None)
        if "href" in value:
            return str(value["href"])
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="link has no target")

    def links(value: object) -> list[dict[str, str]]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="links must be a list")
        result: list[dict[str, str]] = []
        for entry in value:
            if not isinstance(entry, Mapping):
                raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="link must be a table")
            result.append(
                {
                    "label": str(entry.get("label") or ""),
                    "href": link(entry),
                    "icon": str(entry.get("icon") or ""),
                }
            )
        return result

    total_pages = sum(len(package.pages) for package in packages)
    module_count = sum(len(grouped.get(name, [])) for name in ("module", "modules"))
    adapter_count = sum(len(grouped.get(name, [])) for name in ("adapter", "adapters"))
    core_package = by_key.get("core")
    values = {
        "core_version": core_package.version if core_package is not None else "—",
        "total_pages": str(total_pages),
        "module_count": str(module_count),
        "adapter_count": str(adapter_count),
    }
    data = _load_home_config()

    raw_sections = data.get("sections")
    if not isinstance(raw_sections, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="sections must be a table")
    for name in ("start", "topics"):
        if not isinstance(raw_sections.get(name), Mapping):
            raise DocsError(
                "cli.docs.error.bad_config", path=str(HOME_CONFIG), reason=f"sections.{name} must be a table"
            )
    sections = {
        "searchPlaceholder": str(raw_sections.get("searchPlaceholder") or ""),
        "statsLabel": str(raw_sections.get("statsLabel") or ""),
        "start": {
            "eyebrow": str(raw_sections["start"].get("eyebrow") or ""),
            "title": str(raw_sections["start"].get("title") or ""),
        },
        "topics": {
            "eyebrow": str(raw_sections["topics"].get("eyebrow") or ""),
            "title": str(raw_sections["topics"].get("title") or ""),
        },
        "contributeLabel": str(raw_sections.get("contributeLabel") or ""),
    }

    actions: list[dict[str, str]] = []
    raw_actions = data.get("actions")
    if not isinstance(raw_actions, list):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="actions must be a list")
    for entry in raw_actions:
        if not isinstance(entry, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="action must be a table")
        actions.append(
            {
                "label": str(entry.get("label") or ""),
                "href": link(entry),
                "icon": str(entry.get("icon") or ""),
                "tone": str(entry.get("tone") or "text"),
            }
        )

    stats: list[dict[str, str]] = []
    raw_stats = data.get("stats")
    if not isinstance(raw_stats, list):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="stats must be a list")
    for entry in raw_stats:
        if not isinstance(entry, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="stat must be a table")
        source = str(entry.get("source") or "")
        if source not in values:
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason=f"unknown stat source: {source}")
        stats.append(
            {"value": values[source], "label": str(entry.get("label") or ""), "icon": str(entry.get("icon") or "")}
        )

    roles: list[dict[str, object]] = []
    raw_roles = data.get("roles")
    if not isinstance(raw_roles, list):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="roles must be a list")
    for entry in raw_roles:
        if not isinstance(entry, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="role must be a table")
        roles.append(
            {
                "eyebrow": str(entry.get("eyebrow") or ""),
                "title": str(entry.get("title") or ""),
                "description": str(entry.get("description") or ""),
                "href": link(entry),
                "icon": str(entry.get("icon") or ""),
                "links": links(entry.get("links")),
            }
        )

    topics: list[dict[str, str]] = []
    raw_topics = data.get("topics")
    if not isinstance(raw_topics, list):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="topics must be a list")
    for entry in raw_topics:
        if not isinstance(entry, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="topic must be a table")
        topics.append(
            {
                "tag": str(entry.get("tag") or ""),
                "title": str(entry.get("title") or ""),
                "description": str(entry.get("description") or ""),
                "href": link(entry),
                "image": str(entry.get("image") or ""),
            }
        )

    contribute = data.get("contribute")
    if not isinstance(contribute, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="contribute must be a table")
    raw_cards = contribute.get("cards")
    if not isinstance(raw_cards, list):
        raise DocsError("cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="contribute.cards must be a list")
    cards: list[dict[str, object]] = []
    for entry in raw_cards:
        if not isinstance(entry, Mapping):
            raise DocsError(
                "cli.docs.error.bad_config", path=str(HOME_CONFIG), reason="contribute card must be a table"
            )
        card: dict[str, object] = {
            "title": str(entry.get("title") or ""),
            "description": str(entry.get("description") or ""),
            "icon": str(entry.get("icon") or ""),
            "links": links(entry.get("links")),
        }
        if entry.get("logo"):
            card["logo"] = str(entry["logo"])
        cards.append(card)

    return {
        "title": str(data.get("title") or ""),
        "lead": str(data.get("lead") or ""),
        "sections": sections,
        "actions": actions,
        "stats": stats,
        "roles": roles,
        "topics": topics,
        "contribute": {"cards": cards},
    }


def _write_group_page(
    source: Path,
    group: str,
    packages: Sequence[DocPackage],
    config: DocsConfig,
    locale: DocsLocaleConfig,
) -> None:
    directory = source / "groups"
    directory.mkdir(parents=True, exist_ok=True)
    prefix = _prefix_for(locale, config)
    lines = [f"# {_group_title(group, locale.group_titles)}", ""]
    flattened = len(packages) == 1 and not packages[0].overview
    for package in packages:
        if package.overview:
            lines.extend([f"## [{package.title}]({_site_link(prefix, package.key, _package_entry(package))})", ""])
        elif not flattened:
            lines.extend([f"## {package.title}", ""])
        if package.summary:
            lines.extend([package.summary, ""])
        for page in package.pages:
            lines.append(f"- [{page.title}]({_site_link(prefix, package.key, page.path)})")
        lines.append("")
    (directory / f"{group_slug(group)}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


@dataclass(frozen=True)
class _BrandAssets:
    logo: str = ""
    logo_dark: str = ""
    avatar: str = ""
    character: str = ""
    credits: str = ""


def _brand_provider(packages: Sequence[DocPackage]) -> DocPackage | None:
    for package in packages:
        if package.brand:
            return package
    # 兼容仍使用旧字段声明站点标志的包。显式 brand 提供者始终优先。
    for package in packages:
        if package.logo or package.avatar:
            return package
    return None


def _brand_site_url(source: Path, config: DocsConfig, value: str, stem: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    path = site_asset_path(config.root, text)
    if path is None:
        return text
    return _publish_asset(source, config, path, stem, prefix=False)


def _brand_asset(
    source: Path,
    config: DocsConfig,
    provider: DocPackage | None,
    field: str,
    site_value: str,
    stem: str,
    fallback: str,
) -> str:
    site = _brand_site_url(source, config, site_value, stem)
    if site:
        return site
    if provider is not None:
        value = str(getattr(provider, field, "") or "").strip()
        path = Path(value)
        if value and path.is_file():
            return _publish_asset(source, config, path, stem, prefix=False)
    path = HOME_DIR / "assets" / fallback if fallback else None
    if path is not None and path.is_file():
        return _publish_asset(source, config, path, stem, prefix=False)
    return ""


def _prepare_site_assets(
    source: Path,
    config: DocsConfig,
    packages: Sequence[DocPackage],
) -> tuple[str, _BrandAssets]:
    # 品牌插槽的优先级依次为站点配置 > 品牌包声明 > 内置资源。
    favicon = _site_asset_url(source, config, config.site.favicon, "site-favicon")
    if not favicon:
        favicon = _bundled_asset(source, config, "favicon", "site-favicon")
    provider = _brand_provider(packages)
    brand = _BrandAssets(
        logo=_brand_asset(source, config, provider, "logo", config.site.logo, "brand-logo", "logo.png"),
        logo_dark=_brand_asset(
            source, config, provider, "logo_dark", config.site.logo_dark, "brand-logo-dark", "logo-night.png"
        ),
        avatar=_brand_asset(source, config, provider, "avatar", config.site.avatar, "brand-avatar", "logo.png"),
        character=_brand_asset(
            source, config, provider, "character", config.site.character, "brand-character", "placeholder.png"
        ),
        credits=_brand_asset(source, config, provider, "credits", config.site.credits, "brand-credits", ""),
    )
    return favicon, brand


def _theme_public_dir(theme: ThemeSpec) -> Path | None:
    for candidate in (theme.root / "docs" / "public", theme.root / "public"):
        if candidate.is_dir():
            return candidate
    return None


def _copy_theme_public(source: Path, theme: ThemeSpec) -> None:
    entries = theme.config.get("public_assets")
    public = _theme_public_dir(theme)
    if not isinstance(entries, list) or public is None:
        return
    for value in entries:
        relative = Path(str(value))
        if relative.is_absolute() or ".." in relative.parts:
            continue
        path = public / relative
        if not path.is_file():
            continue
        target = source / "public" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def _bundled_asset(source: Path, config: DocsConfig, key: str, stem: str) -> str:
    name = str(config.assets.get(key) or "").strip()
    if not name:
        return ""
    path = DEFAULT_ASSETS_DIR / name
    return _publish_asset(source, config, path, stem) if path.is_file() else ""


def _package_asset(
    source: Path,
    config: DocsConfig,
    packages: Sequence[DocPackage],
    field: str,
    stem: str,
) -> str:
    for package in packages:
        text = str(getattr(package, field, "") or "").strip()
        if not text:
            continue
        path = Path(text)
        if path.is_file():
            return _publish_asset(source, config, path, stem)
    return ""


def _site_asset_url(source: Path, config: DocsConfig, value: str, stem: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    path = site_asset_path(config.root, text)
    if path is None:
        if text.startswith("/"):
            base = config.base
            if base == "/" or text.startswith(base):
                return text
            return f"{base.rstrip('/')}{text}"
        return text
    return _publish_asset(source, config, path, stem)


def _publish_asset(
    source: Path,
    config: DocsConfig,
    path: Path,
    stem: str,
    *,
    prefix: bool = True,
) -> str:
    name = f"{stem}{path.suffix.lower()}"
    target = source / "public" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    return f"{config.base}{name}" if prefix else f"/{name}"


def _write_vitepress_config(
    source: Path,
    views: Sequence[_LocaleView],
    config: DocsConfig,
    theme: ThemeSpec,
    assets: tuple[str, _BrandAssets],
) -> None:
    directory = source / ".vitepress"
    directory.mkdir(parents=True, exist_ok=True)
    snippets = source / "_snippets"
    snippets.mkdir(parents=True, exist_ok=True)
    for item in SNIPPETS_DIR.iterdir():
        if item.is_file():
            shutil.copy2(item, snippets / item.name)
    favicon, brand = assets
    color = config.theme.color
    theme_key = str(theme.config.get("theme_config_key") or "")
    search = theme.config.get("search")
    if not isinstance(search, Mapping):
        search = {"provider": "local"}
    default_view = views[0]
    theme_config = _locale_theme(default_view, config, theme_key, brand, color, dict(search), source)
    head_tags: list[list[object]] = []
    if favicon:
        head_tags.append(["link", {"rel": "icon", "href": favicon}])
    if color and not theme_key:
        head_tags.append(["style", {}, _brand_css(color)])
    locales: dict[str, object] = {"root": {"label": default_view.locale.label, "lang": default_view.locale.tag}}
    for view in views[1:]:
        locales[view.locale.tag] = {
            "label": view.locale.label,
            "lang": view.locale.tag,
            "link": f"/{view.locale.tag}/",
            "themeConfig": _locale_theme(view, config, theme_key, brand, color, dict(search), source),
        }
    payload: dict[str, object] = {
        "title": default_view.locale.title or config.site.title,
        "description": default_view.locale.title or config.site.title,
        "lang": default_view.locale.tag,
        "base": config.base,
        "cleanUrls": bool(theme.config.get("clean_urls", True)),
        "lastUpdated": False,
        "ignoreDeadLinks": True,
        "locales": locales,
        "themeConfig": theme_config,
    }
    if "appearance" in theme.config:
        payload["appearance"] = bool(theme.config["appearance"])

    imports = ['import { defineConfig } from "vitepress"']
    head_export = _theme_module(theme, "head", imports)
    markdown_export = _theme_module(theme, "markdown", imports)
    vite_export = _theme_module(theme, "vite", imports)
    hooks_module = str(theme.config.get("hooks_module") or "").strip()
    boot_export = str(theme.config.get("boot_export") or "").strip()
    build_export = str(theme.config.get("build_export") or "").strip()
    postcss_export = str(theme.config.get("postcss_export") or "").strip()
    if hooks_module:
        for name in (boot_export, build_export, postcss_export):
            if name:
                imports.append(f'import {{ {name} }} from "./theme/{hooks_module}"')
    parts = [
        config.labels["generated_header"],
        *imports,
        "",
        "export default defineConfig({",
        f"  ...{json.dumps(payload, ensure_ascii=False, indent=2)},",
    ]
    if head_export and head_tags:
        parts.append(f"  head: [...{head_export}(), ...{json.dumps(head_tags, ensure_ascii=False)}],")
    elif head_export:
        parts.append(f"  head: {head_export}(),")
    elif head_tags:
        parts.append(f"  head: [...{json.dumps(head_tags, ensure_ascii=False)}],")
    if boot_export:
        parts.append(f"  transformHtml: {boot_export},")
    if markdown_export:
        parts.append(_markdown_block(markdown_export))
    else:
        parts.append(MARKDOWN_CONFIG)
    if vite_export or postcss_export:
        parts.append(
            _vite_block(
                vite_export,
                postcss_export=postcss_export,
                seed=color,
            )
        )
    if build_export:
        webp = "true" if config.build.webp else "false"
        keep = "true" if config.build.webp_keep_original else "false"
        parts.append(f"  buildEnd: {build_export}({{ webp: {webp}, keepOriginal: {keep} }}),")
    prefixes = theme.config.get("custom_element_prefixes")
    if isinstance(prefixes, list) and prefixes:
        prefix_json = json.dumps([str(prefix) for prefix in prefixes], ensure_ascii=False)
        parts.append(
            "  vue: {\n"
            "    template: { compilerOptions: { isCustomElement: (tag) => "
            f"{prefix_json}.some((prefix) => tag.startsWith(prefix)) }} }},\n"
            "  },"
        )
    parts.append("})")
    (directory / "config.mts").write_text("\n".join(parts) + "\n", encoding="utf-8")


def _locale_theme(
    view: _LocaleView,
    config: DocsConfig,
    theme_key: str,
    brand: _BrandAssets,
    color: str,
    search: dict[str, object],
    source: Path,
) -> dict[str, object]:
    locale = view.locale
    prefix = view.prefix
    nav = [
        {
            "text": _group_title(group, locale.group_titles),
            "link": _site_link(prefix, items[0].key, _package_entry(items[0])),
        }
        for group, items in view.groups.items()
    ]
    sidebar: dict[str, list[dict[str, object]]] = {}
    for package in view.packages:
        items = _native_page_items(package, akari=bool(theme_key), labels=locale.labels, prefix=prefix)
        entry: dict[str, object] = {
            "text": package.title,
            "collapsed": False,
            "items": items,
        }
        if package.overview:
            entry["link"] = f"{prefix}/{package.key}/"
        sidebar[f"{prefix}/{package.key}/"] = [entry]
    dependencies: dict[str, list[str]] = {}
    for package in view.packages:
        if not package.dependencies:
            continue
        values = list(package.dependencies)
        dependencies[package.key] = values
        dependencies[package.dist] = values
    languages: dict[str, str] = {}
    for package in view.packages:
        if package.languages:
            languages = dict(package.languages)
            break
    api_catalog: dict[str, object] = {}
    for package in view.packages:
        if package.api_catalog:
            api_catalog = dict(package.api_catalog)
            break
    theme_config: dict[str, object] = {
        "siteTitle": locale.title or config.site.title,
        "nav": nav,
        "sidebar": sidebar,
        "search": search,
    }
    if theme_key:
        app_bar: dict[str, object] = {"title": locale.title or config.site.title}
        if brand.logo:
            app_bar["logo"] = brand.logo
        if brand.logo_dark:
            app_bar["logoDark"] = brand.logo_dark
        akari: dict[str, object] = {
            "appBar": app_bar,
            "brand": {
                "logo": brand.logo,
                "logoDark": brand.logo_dark,
                "avatar": brand.avatar,
                "character": brand.character,
                "credits": brand.credits,
            },
            "sidebar": {"items": _akari_sidebar(view.groups, config, locale)},
            "footer": _footer_section(source, config, brand, locale),
            "search": {"enabled": True},
        }
        if dependencies:
            akari["dependencies"] = dependencies
        if languages:
            akari["supportedLanguages"] = languages
        if api_catalog:
            akari["apiCatalog"] = api_catalog
        if color:
            akari["settings"] = {"defaults": {"color": color}}
        if config.site.command_prefix:
            akari["commandPrefix"] = config.site.command_prefix
        if brand.avatar:
            akari["chatAvatar"] = brand.avatar
        theme_config[theme_key] = akari
    else:
        if brand.logo:
            theme_config["logo"] = brand.logo
        if dependencies:
            theme_config["akari"] = {"dependencies": dependencies}
    return theme_config


BUILTIN_FOOTER_ICONS = frozenset({"afdian", "github"})


def _footer_icon(source: Path, config: DocsConfig, value: str, stem: str) -> str:
    text = (value or "").strip()
    if not text or text in BUILTIN_FOOTER_ICONS:
        return text
    return _brand_site_url(source, config, text, stem)


def _footer_section(
    source: Path,
    config: DocsConfig,
    brand: _BrandAssets,
    locale: DocsLocaleConfig,
) -> dict[str, object]:
    footer = config.footer
    section: dict[str, object] = {"message": locale.labels["footer"]}
    if footer.copyright:
        section["copyright"] = footer.copyright
    if not footer.enabled:
        return section
    about: dict[str, object] = {}
    if footer.title:
        about["title"] = footer.title
    if footer.text:
        about["text"] = list(footer.text)
    image = _brand_site_url(source, config, footer.image, "footer-image") if footer.image else ""
    # 未单独配置配图时使用角色立绘，品牌包缺失时由引擎预置的占位图代替。
    if image or brand.character:
        about["image"] = image or brand.character
    if footer.links:
        about["actions"] = [
            {
                "text": link.text,
                "link": link.link,
                **({"icon": _footer_icon(source, config, link.icon, f"footer-icon-{index}")} if link.icon else {}),
            }
            for index, link in enumerate(footer.links, start=1)
        ]
    if about:
        section["about"] = about
    return section


def _brand_css(color: str) -> str:

    return (
        ":root{"
        f"--vp-c-brand-1:{color};--vp-c-brand-2:{color};--vp-c-brand-3:{color};"
        f"--vp-c-brand-soft:color-mix(in srgb,{color} 16%,transparent)"
        "}"
    )


def _theme_module(theme: ThemeSpec, kind: str, imports: list[str]) -> str:
    module = str(theme.config.get(f"{kind}_module") or "").strip()
    export = str(theme.config.get(f"{kind}_export") or "").strip()
    if not module or not export:
        return ""
    imports.append(f'import {{ {export} }} from "./theme/{module}"')
    return export


def _markdown_block(export: str) -> str:
    rule = textwrap.indent(V_PRE_RULE, " " * 8)
    return (
        "  markdown: {\n"
        '    theme: { light: "github-light", dark: "github-dark" },\n'
        "    headers: { level: [2, 3] },\n"
        "    config: (md) => {\n"
        f"      {export}(md)\n"
        f"{rule}\n"
        "    },\n"
        "  },"
    )


def _vite_block(export: str, *, postcss_export: str = "", seed: str = "") -> str:
    lines = ["  vite: {"]
    if export:
        lines.append(f"    plugins: [...{export}()],")
    if postcss_export:
        argument = json.dumps(seed, ensure_ascii=False) if seed else ""
        lines.append("    css: {")
        lines.append("      postcss: {")
        lines.append(f"        plugins: [...{postcss_export}({argument})],")
        lines.append("      },")
        lines.append("    },")
    lines.append("  },")
    return "\n".join(lines)


def _is_api_page(page: DocPage) -> bool:
    return page.path == API_CATALOG_INDEX or page.path.startswith(f"{API_CATALOG_DIR}/")


def _api_pages(packages: Sequence[DocPackage]) -> list[DocPage]:
    for package in packages:
        if package.key == "core":
            return [page for page in package.pages if _is_api_page(page)]
    return []


def _api_sidebar_group(
    pages: Sequence[DocPage], config: DocsConfig, locale: DocsLocaleConfig, prefix: str
) -> dict[str, object]:
    def page_item(page: DocPage) -> dict[str, object]:
        return {"text": page.title, "link": _site_link(prefix, "core", page.path)}

    normalized = [replace(page, submenu="") if page.path == API_CATALOG_INDEX else page for page in pages]
    item: dict[str, object] = {
        "text": "API",
        "collapsed": True,
        "items": _page_menu_items(normalized, page_item),
    }
    icon = config.icons.get("api", "")
    if icon:
        item["icon"] = icon
    return item


def _akari_sidebar(
    groups: dict[str, list[DocPackage]], config: DocsConfig, locale: DocsLocaleConfig
) -> list[dict[str, object]]:
    prefix = _prefix_for(locale, config)
    result: list[dict[str, object]] = [
        {"text": locale.labels["home"], "link": f"{prefix}/" if prefix else "/", "icon": config.icons.get("home", "")}
    ]
    for group, packages in groups.items():
        visible = packages
        if group == "core":
            visible = [
                replace(package, pages=tuple(page for page in package.pages if not _is_api_page(page)))
                for package in packages
            ]
        item: dict[str, object] = {
            "text": _group_title(group, locale.group_titles),
            "collapsed": True,
            "items": _sidebar_children(visible, config, locale, prefix),
        }
        icon = config.icons.get(group) or config.icons.get(group.lower(), "")
        if icon:
            item["icon"] = icon
        result.append(item)
        if group == "core":
            pages = _api_pages(packages)
            if pages:
                result.append(_api_sidebar_group(pages, config, locale, prefix))
    return result


def _sidebar_children(
    packages: Sequence[DocPackage], config: DocsConfig, locale: DocsLocaleConfig, prefix: str
) -> list[dict[str, object]]:
    if len(packages) == 1 and packages[0].key in {"core", "cli"}:
        entry = _sidebar_package(packages[0], locale, prefix)
        items = entry.get("items")
        if isinstance(items, list):
            link = entry.get("link")
            if isinstance(link, str) and not any(item.get("link") == link for item in items):
                return [{"text": entry["text"], "link": link}, *items]
            return list(items)
    if len(packages) == 1 and not packages[0].overview and not packages[0].category:
        return list(_sidebar_package(packages[0], locale, prefix).get("items", []))
    categorized: dict[str, list[DocPackage]] = {}
    direct: list[DocPackage] = []
    for package in packages:
        if package.category:
            categorized.setdefault(package.category, []).append(package)
        else:
            direct.append(package)
    children = []
    for category, items in sorted(categorized.items(), key=_category_sort_key):
        child: dict[str, object] = {
            "text": category,
            "collapsed": True,
            "items": [_sidebar_package(package, locale, prefix) for package in items],
        }
        icon = config.category_icons.get(category, "")
        if icon:
            child["icon"] = icon
        children.append(child)
    children.extend(_sidebar_package(package, locale, prefix) for package in direct)
    return children


def _category_sort_key(item: tuple[str, list[DocPackage]]) -> tuple[int, str]:
    category, packages = item
    return (min(package.category_order for package in packages), category)


def _page_menu_items(
    pages: Sequence[DocPage], make_item: Callable[[DocPage], dict[str, object]]
) -> list[dict[str, object]]:
    direct: list[dict[str, object]] = []
    roots: dict[str, dict[str, object]] = {}
    for page in pages:
        item = make_item(page)
        parts = [part.strip() for part in (page.submenu or "").split("/") if part.strip()]
        if not parts:
            direct.append(item)
            continue
        node = None
        for part in parts:
            if node is None:
                node = roots.setdefault(part, {"text": part, "children": {}, "items": []})
            else:
                children = node["children"]
                assert isinstance(children, dict)
                node = children.setdefault(part, {"text": part, "children": {}, "items": []})
        items = node["items"]
        assert isinstance(items, list)
        items.append(item)

    def render(node: dict[str, object]) -> list[dict[str, object]]:
        result: list[dict[str, object]] = []
        items = node.get("items")
        if isinstance(items, list):
            result.extend(items)
        children = node.get("children")
        if isinstance(children, dict):
            for child in children.values():
                assert isinstance(child, dict)
                result.append({"text": child["text"], "collapsed": True, "items": render(child)})
        return result

    for root in roots.values():
        direct.append({"text": root["text"], "collapsed": True, "items": render(root)})
    return direct


def _sidebar_package(package: DocPackage, locale: DocsLocaleConfig, prefix: str) -> dict[str, object]:
    def page_item(page: DocPage) -> dict[str, object]:
        return {"text": page.title, "link": _site_link(prefix, package.key, page.path)}

    if not package.overview:
        return {
            "text": package.title,
            "collapsed": True,
            "items": _page_menu_items(package.pages, page_item),
        }
    if _uses_parallel_tabs(package):
        tabs = _package_tabs(package, locale.labels, prefix)
        return {"text": package.title, "link": tabs[0]["link"], "tabs": tabs}
    items = _page_menu_items(package.pages, page_item)
    if not items:
        items = [{"text": locale.labels["overview"], "link": _site_link(prefix, package.key, "index.md")}]
    return {
        "text": package.title,
        "link": _site_link(prefix, package.key, "index.md"),
        "collapsed": True,
        "items": items,
    }


def _uses_parallel_tabs(package: DocPackage) -> bool:
    # 模块统一使用同级页面。其他包若提供 development.md 也按同一结构处理。
    if not package.overview or len(package.pages) <= 1:
        return False
    return package.group == "module" or any(Path(page.path).name == "development.md" for page in package.pages)


def _package_tabs(package: DocPackage, labels: Mapping[str, str], prefix: str) -> list[dict[str, object]]:
    tabs = [
        {"text": _page_tab_title(page, labels), "link": _site_link(prefix, package.key, page.path)}
        for page in package.pages
    ]
    if not tabs:
        tabs = [{"text": labels["usage"], "link": _site_link(prefix, package.key, _package_entry(package))}]
    return tabs


def _native_page_items(
    package: DocPackage, *, akari: bool, labels: Mapping[str, str], prefix: str
) -> list[dict[str, object]]:
    pages = list(package.pages)
    parallel = akari and _uses_parallel_tabs(package)
    if parallel:
        # Akari 主题用标签切换开发页，开发页不进入侧边栏。其他主题保留全部页面。
        pages = [page for page in pages if Path(page.path).name != "development.md"]

    def page_item(page: DocPage) -> dict[str, object]:
        return {
            "text": _page_tab_title(page, labels) if parallel else page.title,
            "link": _site_link(prefix, package.key, page.path),
        }

    items = _page_menu_items(pages, page_item)
    if not items:
        label = labels["usage"] if parallel else labels["overview"]
        items = [{"text": label, "link": _site_link(prefix, package.key, "index.md")}]
    return items


def _page_tab_title(page: DocPage, labels: Mapping[str, str]) -> str:
    path = Path(page.path)
    if path.name == "index.md":
        return labels["usage"]
    if path.name == "development.md":
        return labels["development"]
    return page.title or path.stem


def _write_theme(source: Path, theme: ThemeSpec) -> None:
    directory = source / ".vitepress" / "theme"
    shutil.copytree(theme.theme_dir, directory, dirs_exist_ok=True)
    if str(theme.config.get("theme_config_key") or "") == "akari":
        _write_footer_theme(directory)


def _write_footer_theme(directory: Path) -> None:
    entry = directory / "index.ts"
    if not (entry.is_file() and (directory / "composables" / "useAkariConfig.ts").is_file()):
        return
    target = directory / "footer"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("DocsFooter.vue", "FooterIcon.vue"):
        shutil.copy2(FOOTER_DIR / name, target / name)
    entry.replace(directory / "theme-entry.ts")
    shutil.copy2(FOOTER_DIR / "site-entry.ts", entry)


def _write_home(source: Path, theme: ThemeSpec) -> None:
    component = str(theme.config.get("home_component") or "").strip()
    if not component:
        return
    path = HOME_DIR / f"{component}.vue"
    if path.is_file():
        target = source / ".vitepress" / "theme" / "components" / "content" / f"{component}.vue"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    assets = HOME_DIR / "assets"
    if assets.is_dir():
        shutil.copytree(assets, source / "public" / "home", dirs_exist_ok=True)


def home_digest() -> str:
    digest = hashlib.sha256()
    if not HOME_DIR.is_dir():
        return digest.hexdigest()
    for path in sorted(HOME_DIR.rglob("*")):
        if not path.is_file():
            continue
        digest.update(f"{path.relative_to(HOME_DIR).as_posix()}\0".encode("utf-8"))
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _grouped(packages: Iterable[DocPackage]) -> dict[str, list[DocPackage]]:
    grouped: dict[str, list[DocPackage]] = {}
    for package in packages:
        grouped.setdefault(package.group, []).append(package)
    return grouped


def _group_title(group: str, titles: Mapping[str, str]) -> str:
    return titles.get((group or "").lower(), group)
