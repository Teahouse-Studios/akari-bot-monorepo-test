"""VitePress 站点源文件生成。

生成器只读取目录、配置与各包文档目录，产物全部落在 ``<实例根>/cache/docs/src`` 下；重建前先清空
该目录，且只接受位于 ``<实例根>/cache/docs`` 内的目标路径。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tomllib
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

from .config import DocsConfig
from .model import DocCatalog, DocPackage, DocsError, page_url

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"})
ATTACHMENT_SUFFIXES = frozenset({".txt", ".pdf"})
ALLOWED_SUFFIXES = frozenset({".md"}) | IMAGE_SUFFIXES | ATTACHMENT_SUFFIXES
TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
CONFIG_HEADER = "// 由 akaribot docs 生成，请勿手工修改。"
# 文档里的 ``{{I18N:key}}`` 是机器人模板语法；Vue 会把双花括号当插值，行内代码需显式 v-pre。
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
    link_packages: Iterable[DocPackage] | None = None,
) -> None:
    """按目录与配置生成整个站点源目录。

    :param catalog: 参与构建的文档目录。
    :param src_dir: 目标源目录，必须位于实例的 ``cache/docs`` 下。
    :param config: 实例文档配置。
    :param link_packages: 用于跨包链接重写的全部包；缺省只用 ``catalog``。子集构建时传入完整目录，
        使指向未选包的源码相对链接仍能折算成站点地址。
    :raises DocsError: 目标路径越界、包 key 非法或源文件经符号链接逃逸。
    """
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
    _write_vitepress_config(source, catalog.packages, groups, config)
    _write_theme(source)


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


def _write_vitepress_config(
    source: Path, packages: Sequence[DocPackage], groups: dict[str, list[DocPackage]], config: DocsConfig
) -> None:
    directory = source / ".vitepress"
    directory.mkdir(parents=True, exist_ok=True)
    nav = [{"text": _group_title(group), "link": page_url(items[0].key, "index.md")} for group, items in groups.items()]
    sidebar: dict[str, list[dict[str, object]]] = {}
    for package in packages:
        items = [{"text": page.title, "link": page_url(package.key, page.path)} for page in package.pages]
        if not items:
            items = [{"text": "概览", "link": page_url(package.key, "index.md")}]
        sidebar[f"/{package.key}/"] = [{"text": package.title, "collapsed": False, "items": items}]
    payload = {
        "title": config.site.title,
        "description": config.site.title,
        "lang": config.site.lang,
        "base": config.base,
        "cleanUrls": True,
        "lastUpdated": False,
        "ignoreDeadLinks": True,
        "themeConfig": {
            "nav": nav,
            "sidebar": sidebar,
            "search": {"provider": "local"},
        },
    }
    text = (
        f"{CONFIG_HEADER}\n"
        'import { defineConfig } from "vitepress"\n\n'
        "export default defineConfig({\n"
        f"  ...{json.dumps(payload, ensure_ascii=False, indent=2)},\n"
        f"{MARKDOWN_CONFIG}\n"
        "})\n"
    )
    (directory / "config.mts").write_text(text, encoding="utf-8")


def _write_theme(source: Path) -> None:
    directory = source / ".vitepress" / "theme"
    template = TEMPLATE_DIR / "theme"
    if template.is_dir():
        shutil.copytree(template, directory, dirs_exist_ok=True)
        return
    directory.mkdir(parents=True, exist_ok=True)
    for name in ("index.ts", "custom.css"):
        (directory / name).write_text("", encoding="utf-8")


def _grouped(packages: Iterable[DocPackage]) -> dict[str, list[DocPackage]]:
    grouped: dict[str, list[DocPackage]] = {}
    for package in packages:
        grouped.setdefault(package.group, []).append(package)
    return grouped


def _group_title(group: str) -> str:
    return GROUP_TITLES.get((group or "").lower(), group or "其它")
