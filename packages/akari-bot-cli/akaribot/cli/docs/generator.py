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
from dataclasses import dataclass, replace
from pathlib import Path

from .config import DEFAULT_ASSETS_DIR, DocsConfig, DocsLocaleConfig, site_asset_path
from .model import DocCatalog, DocPackage, DocPage, DocsError, page_url
from .theme import ThemeSpec, bundled_theme

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"})
ATTACHMENT_SUFFIXES = frozenset({".txt", ".pdf"})
ALLOWED_SUFFIXES = frozenset({".md"}) | IMAGE_SUFFIXES | ATTACHMENT_SUFFIXES
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
    tags = [locale.tag for locale in config.locales]
    views: list[_LocaleView] = []
    for locale in config.locales:
        prefix = "" if locale is config.default_locale else f"/{locale.tag}"
        packages = tuple(_locale_package(package, config, locale, tags) for package in catalog.packages)
        target = source if not prefix else source / locale.tag
        target.mkdir(parents=True, exist_ok=True)
        groups = _grouped(packages)
        _write_index(target, packages, config, locale)
        for group, items in groups.items():
            _write_group_page(target, group, items, config, locale)
        for package in packages:
            _copy_package(source, target, package, roots, locale, tags)
        views.append(_LocaleView(locale=locale, prefix=prefix, packages=packages, groups=groups, target=target))
    assets = _prepare_site_assets(source, config, catalog.packages)
    _write_vitepress_config(source, views, config, spec, assets)
    _write_theme(source, spec)


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
    try:
        data = tomllib.loads((doc_dir / "doc.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return "", ""
    locales = data.get("locales")
    if not isinstance(locales, Mapping):
        return "", ""
    entry = locales.get(tag)
    if not isinstance(entry, Mapping):
        return "", ""
    return _text(entry, "title"), _text(entry, "summary")


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
    if "index.md" not in copied:
        page = destination / "index.md"
        page.write_text(f"# {package.title}\n\n{package.summary or package.name}\n", encoding="utf-8")


def _rewrite_links(
    text: str,
    source: Path,
    package: DocPackage,
    roots: dict[Path, DocPackage],
    *,
    prefix: str = "",
) -> str:
    # 文档在源码树里用相对路径互相引用；落到站点后包目录已重排，跨包链接须折算成 URL。
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


def _prefix_for(locale: DocsLocaleConfig, config: DocsConfig) -> str:
    return "" if locale.tag == config.default_locale.tag else f"/{locale.tag}"


def _site_link(prefix: str, key: str, path: str) -> str:
    return f"{prefix}{page_url(key, path)}"


def _write_index(source: Path, packages: Sequence[DocPackage], config: DocsConfig, locale: DocsLocaleConfig) -> None:
    prefix = _prefix_for(locale, config)
    labels = locale.labels
    lines = [f"# {locale.title or config.site.title}", "", labels["index_intro"], ""]
    for group, items in _grouped(packages).items():
        lines.extend([f"## {_group_title(group, locale.group_titles)}", ""])
        for package in items:
            summary = f"：{package.summary}" if package.summary else ""
            lines.append(f"- [{package.title}]({_site_link(prefix, package.key, 'index.md')}){summary}")
        lines.append("")
    (source / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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
    for package in packages:
        lines.extend([f"## [{package.title}]({_site_link(prefix, package.key, 'index.md')})", ""])
        if package.summary:
            lines.extend([package.summary, ""])
        for page in package.pages:
            lines.append(f"- [{page.title}]({_site_link(prefix, package.key, page.path)})")
        lines.append("")
    (directory / f"{group_slug(group)}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _prepare_site_assets(
    source: Path,
    config: DocsConfig,
    packages: Sequence[DocPackage],
) -> tuple[str, str, str]:
    # 顶栏标志与对话头像的优先级：站点配置 > 包声明 > 站点图标。
    favicon = _site_asset_url(source, config, config.site.favicon, "site-favicon")
    if not favicon:
        favicon = _bundled_asset(source, config, "favicon", "site-favicon")
    logo = _site_asset_url(source, config, config.site.logo, "site-logo")
    if not logo:
        logo = _package_asset(source, config, packages, "logo", "site-logo")
    avatar = _site_asset_url(source, config, config.site.avatar, "site-avatar")
    if not avatar:
        avatar = _package_asset(source, config, packages, "avatar", "site-avatar")
    return logo or favicon, favicon, avatar or favicon


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


def _publish_asset(source: Path, config: DocsConfig, path: Path, stem: str) -> str:
    name = f"{stem}{path.suffix.lower()}"
    target = source / "public" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    return f"{config.base}{name}"


def _write_vitepress_config(
    source: Path,
    views: Sequence[_LocaleView],
    config: DocsConfig,
    theme: ThemeSpec,
    assets: tuple[str, str, str],
) -> None:
    directory = source / ".vitepress"
    directory.mkdir(parents=True, exist_ok=True)
    logo, favicon, avatar = assets
    color = config.theme.color
    theme_key = str(theme.config.get("theme_config_key") or "")
    search = theme.config.get("search")
    if not isinstance(search, Mapping):
        search = {"provider": "local"}
    default_view = views[0]
    theme_config = _locale_theme(default_view, config, theme_key, logo, avatar, color, dict(search))
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
            "themeConfig": _locale_theme(view, config, theme_key, logo, avatar, color, dict(search)),
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


def _locale_theme(
    view: _LocaleView,
    config: DocsConfig,
    theme_key: str,
    logo: str,
    avatar: str,
    color: str,
    search: dict[str, object],
) -> dict[str, object]:
    locale = view.locale
    prefix = view.prefix
    nav = [
        {"text": _group_title(group, locale.group_titles), "link": f"{prefix}/{items[0].key}/"}
        for group, items in view.groups.items()
    ]
    sidebar: dict[str, list[dict[str, object]]] = {}
    for package in view.packages:
        items = _native_page_items(package, akari=bool(theme_key), labels=locale.labels, prefix=prefix)
        sidebar[f"{prefix}/{package.key}/"] = [
            {
                "text": package.title,
                "link": f"{prefix}/{package.key}/",
                "collapsed": False,
                "items": items,
            }
        ]
    theme_config: dict[str, object] = {
        "siteTitle": locale.title or config.site.title,
        "nav": nav,
        "sidebar": sidebar,
        "search": search,
    }
    if theme_key:
        app_bar: dict[str, object] = {"title": locale.title or config.site.title}
        if logo:
            app_bar["logo"] = logo
        akari: dict[str, object] = {
            "appBar": app_bar,
            "sidebar": {"items": _akari_sidebar(view.groups, config, locale)},
            "footer": {"message": locale.labels["footer"]},
            "search": {"enabled": True},
        }
        if color:
            akari["settings"] = {"defaults": {"color": color}}
        if config.site.command_prefix:
            akari["commandPrefix"] = config.site.command_prefix
        if avatar:
            akari["chatAvatar"] = avatar
        theme_config[theme_key] = akari
    elif logo:
        theme_config["logo"] = logo
    return theme_config


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


def _akari_sidebar(
    groups: dict[str, list[DocPackage]], config: DocsConfig, locale: DocsLocaleConfig
) -> list[dict[str, object]]:
    prefix = _prefix_for(locale, config)
    result: list[dict[str, object]] = [
        {"text": locale.labels["home"], "link": f"{prefix}/" if prefix else "/", "icon": config.icons.get("home", "")}
    ]
    for group, packages in groups.items():
        item: dict[str, object] = {
            "text": _group_title(group, locale.group_titles),
            "collapsed": False,
            "items": _sidebar_children(packages, config, locale, prefix),
        }
        icon = config.icons.get(group) or config.icons.get(group.lower(), "")
        if icon:
            item["icon"] = icon
        result.append(item)
    return result


def _sidebar_children(
    packages: Sequence[DocPackage], config: DocsConfig, locale: DocsLocaleConfig, prefix: str
) -> list[dict[str, object]]:
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
            "collapsed": False,
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


def _sidebar_package(package: DocPackage, locale: DocsLocaleConfig, prefix: str) -> dict[str, object]:
    if _uses_parallel_tabs(package):
        tabs = _package_tabs(package, locale.labels, prefix)
        return {"text": package.title, "link": tabs[0]["link"], "tabs": tabs}
    items = [{"text": page.title, "link": _site_link(prefix, package.key, page.path)} for page in package.pages]
    if not items:
        items = [{"text": locale.labels["overview"], "link": _site_link(prefix, package.key, "index.md")}]
    return {
        "text": package.title,
        "link": _site_link(prefix, package.key, "index.md"),
        "collapsed": False,
        "items": items,
    }


def _uses_parallel_tabs(package: DocPackage) -> bool:
    # 模块统一使用平行页面；其他包只要提供 development.md 也按同一结构处理。
    if len(package.pages) <= 1:
        return False
    return package.group == "module" or any(Path(page.path).name == "development.md" for page in package.pages)


def _package_tabs(package: DocPackage, labels: Mapping[str, str], prefix: str) -> list[dict[str, object]]:
    tabs = [
        {"text": _page_tab_title(page, labels), "link": _site_link(prefix, package.key, page.path)}
        for page in package.pages
    ]
    if not tabs:
        tabs = [{"text": labels["usage"], "link": _site_link(prefix, package.key, "index.md")}]
    return tabs


def _native_page_items(
    package: DocPackage, *, akari: bool, labels: Mapping[str, str], prefix: str
) -> list[dict[str, object]]:
    pages = list(package.pages)
    parallel = akari and _uses_parallel_tabs(package)
    if parallel:
        # Akari 主题用标签切换开发页，开发页不进入侧栏；其他主题保留全部页面。
        pages = [page for page in pages if Path(page.path).name != "development.md"]
    items = [
        {
            "text": _page_tab_title(page, labels) if parallel else page.title,
            "link": _site_link(prefix, package.key, page.path),
        }
        for page in pages
    ]
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


def _grouped(packages: Iterable[DocPackage]) -> dict[str, list[DocPackage]]:
    grouped: dict[str, list[DocPackage]] = {}
    for package in packages:
        grouped.setdefault(package.group, []).append(package)
    return grouped


def _group_title(group: str, titles: Mapping[str, str]) -> str:
    return titles.get((group or "").lower(), group)
