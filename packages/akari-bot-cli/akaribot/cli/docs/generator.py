"""VitePress 站点源文件生成。

生成器只读取目录、配置与各包文档目录，产物全部落在 ``<实例根>/cache/docs/src`` 下；重建前先清空
该目录，且只接受位于 ``<实例根>/cache/docs`` 内的目标路径。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import textwrap
import tomllib
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

from .config import DocsConfig, site_asset_path
from .model import DocCatalog, DocPackage, DocPage, DocsError, page_url
from .theme import ThemeSpec, bundled_theme

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"})
ATTACHMENT_SUFFIXES = frozenset({".txt", ".pdf"})
ALLOWED_SUFFIXES = frozenset({".md"}) | IMAGE_SUFFIXES | ATTACHMENT_SUFFIXES
CONFIG_HEADER = "// 由 akaribot docs 生成，请勿手工修改。"
# 文档里的 ``{{I18N:key}}`` 是机器人模板语法；Vue 会把双花括号当插值，行内代码需显式 v-pre。
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
GROUP_TITLES = {
    "core": "核心",
    "builtin": "内置模块",
    "cli": "命令行",
    "module": "模块",
    "modules": "模块",
    "adapter": "适配器",
    "adapters": "适配器",
    "testing": "测试",
    "assets": "资源",
    "asset": "资源",
    "library": "库",
    "docs": "文档",
}


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
    :param theme: 主题；缺省使用 CLI 内置主题。
    :param link_packages: 用于跨包链接重写的全部包；缺省只用 ``catalog``。子集构建时传入完整目录，
        使指向未选包的源码相对链接仍能折算成站点地址。
    :raises DocsError: 目标路径越界、包 key 非法或源文件经符号链接逃逸。
    """
    spec = theme or bundled_theme()
    source = _checked_source_dir(src_dir, config)
    if source.exists():
        shutil.rmtree(source)
    source.mkdir(parents=True)

    roots = {Path(package.doc_path).resolve(): package for package in (link_packages or catalog.packages)}
    groups = _grouped(catalog.packages)
    _write_index(source, catalog.packages, config)
    for group, packages in groups.items():
        _write_group_page(source, group, packages)
    for package in catalog.packages:
        _copy_package(source, package, roots)
    assets = _prepare_site_assets(source, config)
    _write_vitepress_config(source, catalog.packages, groups, config, spec, assets)
    _write_theme(source, spec)


def collect_files(doc_path: Path) -> list[tuple[str, Path]]:
    """列出包文档目录下允许发布的文件。

    :param doc_path: 包文档目录。
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
    """把分组名折算成文件名与 URL 片段。"""
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


def _copy_package(source: Path, package: DocPackage, roots: dict[Path, DocPackage]) -> None:
    key = _checked_key(package.key)
    destination = source / key
    destination.mkdir(parents=True, exist_ok=True)
    copied: set[str] = set()
    for relative, path in collect_files(package.doc_path):
        suffix = path.suffix.lower()
        if suffix in ATTACHMENT_SUFFIXES:
            target = source / "public" / key / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.add(relative)
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if suffix == ".md":
            text = path.read_text(encoding="utf-8")
            text = _rewrite_links(text, path, package, roots)
            if relative == "index.md":
                text = _inject_module_meta(text, package.doc_path)
            target.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, target)
        copied.add(relative)
    if "index.md" not in copied:
        text = f"# {package.title}\n\n{package.summary or package.name}\n"
        (destination / "index.md").write_text(text, encoding="utf-8")


def _rewrite_links(text: str, source: Path, package: DocPackage, roots: dict[Path, DocPackage]) -> str:
    # 文档在源码树里用相对路径互相引用；落到站点后包目录已重排，跨包链接须折算成 URL。
    lines = text.splitlines(keepends=True)
    fenced = False
    for index, line in enumerate(lines):
        if FENCE_PATTERN.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        lines[index] = LINK_PATTERN.sub(lambda match: _rewrite_link(match, source, package, roots), line)
    return "".join(lines)


def _rewrite_link(match: re.Match[str], source: Path, package: DocPackage, roots: dict[Path, DocPackage]) -> str:
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
        return f"{match.group('open')}{url}{suffix}{match.group('close')}"
    return match.group(0)


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
    try:
        data = tomllib.loads((Path(doc_path) / "doc.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return []
    meta = data.get("meta")
    if not isinstance(meta, Mapping):
        return []
    modules = meta.get("modules")
    if not isinstance(modules, list):
        return []
    return [dict(item) for item in modules if isinstance(item, Mapping) and item.get("name")]


def _write_index(source: Path, packages: Sequence[DocPackage], config: DocsConfig) -> None:
    lines = [f"# {config.site.title}", "", "本页汇总当前实例中已安装包的文档。", ""]
    for group, items in _grouped(packages).items():
        lines.extend([f"## {_group_title(group)}", ""])
        for package in items:
            summary = f"：{package.summary}" if package.summary else ""
            lines.append(f"- [{package.title}]({page_url(package.key, 'index.md')}){summary}")
        lines.append("")
    (source / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_group_page(source: Path, group: str, packages: Sequence[DocPackage]) -> None:
    directory = source / "groups"
    directory.mkdir(parents=True, exist_ok=True)
    lines = [f"# {_group_title(group)}", ""]
    for package in packages:
        lines.extend([f"## [{package.title}]({page_url(package.key, 'index.md')})", ""])
        if package.summary:
            lines.extend([package.summary, ""])
        for page in package.pages:
            lines.append(f"- [{page.title}]({page_url(package.key, page.path)})")
        lines.append("")
    (directory / f"{group_slug(group)}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _prepare_site_assets(source: Path, config: DocsConfig) -> tuple[str, str]:
    return (
        _site_asset_url(source, config, config.site.logo, "site-logo"),
        _site_asset_url(source, config, config.site.favicon, "site-favicon"),
    )


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
    name = f"{stem}{path.suffix.lower()}"
    target = source / "public" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    return f"{config.base}{name}"


def _write_vitepress_config(
    source: Path,
    packages: Sequence[DocPackage],
    groups: dict[str, list[DocPackage]],
    config: DocsConfig,
    theme: ThemeSpec,
    assets: tuple[str, str],
) -> None:
    directory = source / ".vitepress"
    directory.mkdir(parents=True, exist_ok=True)
    logo, favicon = assets
    color = config.theme.color
    nav = [{"text": _group_title(group), "link": page_url(items[0].key, "index.md")} for group, items in groups.items()]
    theme_key = str(theme.config.get("theme_config_key") or "")
    sidebar: dict[str, list[dict[str, object]]] = {}
    for package in packages:
        items = _native_page_items(package, akari=bool(theme_key))
        sidebar[f"/{package.key}/"] = [
            {
                "text": package.title,
                "link": page_url(package.key, "index.md"),
                "collapsed": False,
                "items": items,
            }
        ]
    search = theme.config.get("search")
    if not isinstance(search, Mapping):
        search = {"provider": "local"}
    theme_config: dict[str, object] = {
        "nav": nav,
        "sidebar": sidebar,
        "search": dict(search),
    }
    if theme_key:
        app_bar: dict[str, object] = {"title": config.site.title}
        if logo:
            app_bar["logo"] = logo
        akari: dict[str, object] = {
            "appBar": app_bar,
            "sidebar": {"items": _akari_sidebar(groups, config)},
            "footer": {"message": "由 AkariBot 文档引擎生成"},
            "search": {"enabled": True},
        }
        if color:
            akari["settings"] = {"defaults": {"color": color}}
        theme_config[theme_key] = akari
    elif logo:
        theme_config["logo"] = logo
    head_tags: list[list[object]] = []
    if favicon:
        head_tags.append(["link", {"rel": "icon", "href": favicon}])
    if color and not theme_key:
        head_tags.append(["style", {}, _brand_css(color)])
    payload: dict[str, object] = {
        "title": config.site.title,
        "description": config.site.title,
        "lang": config.site.lang,
        "base": config.base,
        "cleanUrls": bool(theme.config.get("clean_urls", True)),
        "lastUpdated": False,
        "ignoreDeadLinks": True,
        "themeConfig": theme_config,
    }
    if "appearance" in theme.config:
        payload["appearance"] = bool(theme.config["appearance"])

    imports = ['import { defineConfig } from "vitepress"']
    head_export = _theme_module(theme, "head", imports)
    markdown_export = _theme_module(theme, "markdown", imports)
    parts = [
        CONFIG_HEADER,
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
    if markdown_export:
        parts.append(_markdown_block(markdown_export))
    else:
        parts.append(MARKDOWN_CONFIG)
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


def _akari_sidebar(groups: dict[str, list[DocPackage]], config: DocsConfig) -> list[dict[str, object]]:
    result: list[dict[str, object]] = [{"text": "首页", "link": "/", "icon": config.icons.get("home") or "home"}]
    for group, packages in groups.items():
        item: dict[str, object] = {
            "text": _group_title(group),
            "collapsed": False,
            "items": _sidebar_children(packages),
        }
        icon = config.icons.get(group)
        if icon:
            item["icon"] = icon
        result.append(item)
    return result


def _sidebar_children(packages: Sequence[DocPackage]) -> list[dict[str, object]]:
    categorized: dict[str, list[DocPackage]] = {}
    direct: list[DocPackage] = []
    for package in packages:
        if package.category:
            categorized.setdefault(package.category, []).append(package)
        else:
            direct.append(package)
    children = [
        {
            "text": category,
            "collapsed": False,
            "items": [_sidebar_package(package) for package in items],
        }
        for category, items in sorted(categorized.items(), key=_category_sort_key)
    ]
    children.extend(_sidebar_package(package) for package in direct)
    return children


def _category_sort_key(item: tuple[str, list[DocPackage]]) -> tuple[int, str]:
    category, packages = item
    return (min(package.category_order for package in packages), category)


def _sidebar_package(package: DocPackage) -> dict[str, object]:
    if _uses_parallel_tabs(package):
        tabs = _package_tabs(package)
        return {"text": package.title, "link": tabs[0]["link"], "tabs": tabs}
    items = [{"text": page.title, "link": page_url(package.key, page.path)} for page in package.pages]
    if not items:
        items = [{"text": "概览", "link": page_url(package.key, "index.md")}]
    return {
        "text": package.title,
        "link": page_url(package.key, "index.md"),
        "collapsed": False,
        "items": items,
    }


def _uses_parallel_tabs(package: DocPackage) -> bool:
    # 模块统一使用平行页面；其他包只要提供 development.md 也按同一结构处理。
    if len(package.pages) <= 1:
        return False
    return package.group == "module" or any(Path(page.path).name == "development.md" for page in package.pages)


def _package_tabs(package: DocPackage) -> list[dict[str, object]]:
    tabs = [{"text": _page_tab_title(page), "link": page_url(package.key, page.path)} for page in package.pages]
    if not tabs:
        tabs = [{"text": "使用方法", "link": page_url(package.key, "index.md")}]
    return tabs


def _native_page_items(package: DocPackage, *, akari: bool) -> list[dict[str, object]]:
    pages = list(package.pages)
    parallel = akari and _uses_parallel_tabs(package)
    if parallel:
        # Akari 主题用标签切换开发页，开发页不进入侧栏；其他主题保留全部页面。
        pages = [page for page in pages if Path(page.path).name != "development.md"]
    items = [
        {
            "text": _page_tab_title(page) if parallel else page.title,
            "link": page_url(package.key, page.path),
        }
        for page in pages
    ]
    if not items:
        label = "使用方法" if parallel else "概览"
        items = [{"text": label, "link": page_url(package.key, "index.md")}]
    return items


def _page_tab_title(page: DocPage) -> str:
    path = Path(page.path)
    if path.name == "index.md":
        return "使用方法"
    if path.name == "development.md":
        return "安装与开发"
    return page.title or path.stem


def _write_theme(source: Path, theme: ThemeSpec) -> None:
    directory = source / ".vitepress" / "theme"
    shutil.copytree(theme.theme_dir, directory, dirs_exist_ok=True)


def _grouped(packages: Iterable[DocPackage]) -> dict[str, list[DocPackage]]:
    grouped: dict[str, list[DocPackage]] = {}
    for package in packages:
        grouped.setdefault(package.group, []).append(package)
    return grouped


def _group_title(group: str) -> str:
    return GROUP_TITLES.get((group or "").lower(), group or "其它")
