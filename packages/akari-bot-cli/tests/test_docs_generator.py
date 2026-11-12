"""``akaribot.cli.docs.generator``：站点源文件、侧栏与路径约束。"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli.docs.config import DocsConfig, DocsLocaleConfig, DocsSiteConfig, DocsThemeConfig
from akaribot.cli.docs.generator import generate
from akaribot.cli.docs.model import DocCatalog, DocPackage, DocPage, DocsError
from akaribot.cli.docs.theme import ThemeSpec
from akaribot.testing import Tester, func_case


def _write(directory: Path, files: dict[str, bytes | str]) -> None:
    for relative, content in files.items():
        target = directory / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")


def _package(
    base: Path,
    files: dict[str, bytes | str],
    *,
    pages: tuple[DocPage, ...] = (),
    key: str = "demo",
    group: str = "module",
    title: str = "Demo",
    category: str = "",
    category_order: int = 500,
    logo: str = "",
) -> DocPackage:
    doc_path = base / f"doc-{key}"
    doc_path.mkdir(parents=True, exist_ok=True)
    _write(doc_path, files)
    return DocPackage(
        key=key,
        group=group,
        dist=f"akari-bot-module-{key}",
        name=key,
        version="1.0.0",
        title=title,
        summary="示例包",
        doc_path=doc_path,
        pages=pages,
        category=category,
        category_order=category_order,
        logo=logo,
    )


def _docs(root: Path) -> DocsConfig:
    return DocsConfig(root=root)


async def _test_generate_site_layout():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        files = {
            "index.md": "# Demo\n",
            "guide/setup.md": "# 安装\n",
            "development.md": "# 安装与开发\n",
            "images/logo.png": b"\x89PNG\r\n",
            "notes.txt": "说明\n",
            "manual.pdf": b"%PDF-1.4",
            "payload.bin": b"\x00\x01",
        }
        pages = (
            DocPage("index.md", "概览", 0),
            DocPage("guide/setup.md", "安装", 10),
            DocPage("development.md", "安装与开发", 20),
        )
        package = _package(root, files, pages=pages)
        source = root / "cache" / "docs" / "src"
        source.mkdir(parents=True)
        (source / "stale.md").write_text("旧产物\n", encoding="utf-8")
        generate(DocCatalog(packages=(package,)), source, _docs(root))

        config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        index = (source / "index.md").read_text(encoding="utf-8")
        group = (source / "groups" / "module.md").read_text(encoding="utf-8")
        theme = (source / ".vitepress" / "theme" / "index.ts").read_text(encoding="utf-8")
        copied = {
            "index": (source / "demo" / "index.md").is_file(),
            "guide": (source / "demo" / "guide" / "setup.md").is_file(),
            "image": (source / "demo" / "images" / "logo.png").is_file(),
            "text": (source / "public" / "demo" / "notes.txt").is_file(),
            "pdf": (source / "public" / "demo" / "manual.pdf").is_file(),
            "binary": (source / "demo" / "payload.bin").exists(),
            "stale": (source / "stale.md").exists(),
            "custom_css": (source / ".vitepress" / "theme" / "custom.css").is_file(),
            "components": all(
                (source / ".vitepress" / "theme" / "components" / name).is_file()
                for name in ("ModuleMeta.vue", "NoticeBox.vue", "CommandUsage.vue")
            ),
        }
    return (
        copied
        == {
            "index": True,
            "guide": True,
            "image": True,
            "text": True,
            "pdf": True,
            "binary": False,
            "stale": False,
            "custom_css": True,
            "components": True,
        }
        and config.startswith("// 由 akaribot docs 生成，请勿手工修改。")
        and '"cleanUrls": true' in config
        and '"provider": "local"' in config
        and '"base": "/"' in config
        and '"/demo/guide/setup"' in config
        and '"/demo/development"' in config
        and '"text": "Demo"' in config
        and "# 小可 · 文档" in index
        and "[Demo](/demo/)" in index
        and "示例包" in group
        and "DefaultTheme" in theme
        and all(name in theme for name in ("ModuleMeta", "NoticeBox", "CommandUsage"))
    )


async def _test_base_env_override():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        source = root / "cache" / "docs" / "src"
        with patch.dict(os.environ, {"AKARIBOT_DOCS_BASE": "/sub"}):
            generate(DocCatalog(packages=(package,)), source, _docs(root))
        config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
    return '"base": "/sub/"' in config


async def _test_generate_rejects_source_outside_cache():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        outside = root / "elsewhere" / "src"
        try:
            generate(DocCatalog(packages=(package,)), outside, _docs(root))
        except DocsError as exc:
            error = (str(exc), outside.exists())
        else:
            error = ("", outside.exists())
    return error == ("cli.docs.error.unsafe_path", False)


async def _test_generate_rejects_symlink_escape():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        secret = root / "secret.md"
        secret.write_text("机密\n", encoding="utf-8")
        os.symlink(secret, package.doc_path / "leak.md")
        source = root / "cache" / "docs" / "src"
        try:
            generate(DocCatalog(packages=(package,)), source, _docs(root))
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return error == "cli.docs.error.unsafe_path"


async def _test_package_without_pages_gets_placeholder():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {})
        source = root / "cache" / "docs" / "src"
        generate(DocCatalog(packages=(package,)), source, _docs(root))
        text = (source / "demo" / "index.md").read_text(encoding="utf-8")
        config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
    return text.startswith("# Demo") and '"/demo/"' in config


async def _test_unsafe_package_key_is_rejected():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        unsafe = DocPackage(
            key="../escape",
            group="module",
            dist="x",
            name="x",
            version="",
            title="X",
            summary="",
            doc_path=package.doc_path,
            pages=package.pages,
        )
        source = root / "cache" / "docs" / "src"
        try:
            generate(DocCatalog(packages=(unsafe,)), source, _docs(root))
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return error == "cli.docs.error.unsafe_path" and not (root / "cache" / "docs" / "escape").exists()


async def _test_cross_package_links_are_rewritten():
    def _package_at(key: str, files: dict[str, bytes | str]) -> DocPackage:
        doc_path = root / key / "doc"
        _write(doc_path, files)
        return DocPackage(
            key=key,
            group="module",
            dist=f"akari-bot-module-{key}",
            name=key,
            version="1.0.0",
            title=key.upper(),
            summary="",
            doc_path=doc_path,
            pages=(DocPage("index.md", "概览", 0),),
        )

    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package_a = _package_at(
            "a",
            {
                "index.md": (
                    "# A\n"
                    "[B 首页](../../b/doc/index.md)\n"
                    "[B 子页](../../b/doc/guide.md#start)\n"
                    "[B 子目录](../../b/doc/sub/index.md)\n"
                    "[B 资源](../../b/doc/files/manual.pdf)\n"
                    "[同包](guide.md)\n"
                    "[外链](https://example.com/x.md)\n"
                    "[绝对](/b/guide)\n"
                    "```\n[B 代码](../../b/doc/guide.md)\n```\n"
                ),
                "guide.md": "# A 指南\n",
            },
        )
        package_b = _package_at(
            "b",
            {"index.md": "# B\n", "guide.md": "# B 指南\n", "sub/index.md": "# 子目录\n", "files/manual.pdf": b"%PDF"},
        )
        source = root / "cache" / "docs" / "src"
        generate(
            DocCatalog(packages=(package_a,)),
            source,
            _docs(root),
            link_packages=(package_a, package_b),
        )
        text = (source / "a" / "index.md").read_text(encoding="utf-8")
    return (
        "[B 首页](/b/)" in text
        and "[B 子页](/b/guide#start)" in text
        and "[B 子目录](/b/sub/)" in text
        and "[B 资源](/b/files/manual.pdf)" in text
        and "[同包](guide.md)" in text
        and "[外链](https://example.com/x.md)" in text
        and "[绝对](/b/guide)" in text
        and "[B 代码](../../b/doc/guide.md)" in text
    )


async def _test_module_meta_is_injected_from_doc_toml():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(
            root,
            {
                "index.md": "# Demo\n\n简介。\n",
                "doc.toml": (
                    "schema = 1\n"
                    'title = "Demo"\n'
                    "[[meta.modules]]\n"
                    'name = "demo"\n'
                    'aliases = ["d"]\n'
                    'type = ["command"]\n'
                    'permission = "admin"\n'
                    "forced = true\n"
                ),
            },
            pages=(DocPage("index.md", "概览", 0),),
        )
        source = root / "cache" / "docs" / "src"
        generate(DocCatalog(packages=(package,)), source, _docs(root))
        text = (source / "demo" / "index.md").read_text(encoding="utf-8")
        component = (source / ".vitepress" / "theme" / "components" / "ModuleMeta.vue").is_file()
    return (
        component
        and "# Demo" in text
        and text.index("# Demo") < text.index("<ModuleMeta")
        and '"name":"demo"' in text
        and '"permission":"admin"' in text
        and '"forced":true' in text
    )


async def _test_package_without_meta_has_no_component():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        source = root / "cache" / "docs" / "src"
        generate(DocCatalog(packages=(package,)), source, _docs(root))
        text = (source / "demo" / "index.md").read_text(encoding="utf-8")
    return "<ModuleMeta" not in text


async def _test_module_categories_and_parallel_tabs():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        alpha = _package(
            root,
            {"index.md": "# alpha\n", "expressions.md": "# 表达式详解\n", "development.md": "# 安装与开发\n"},
            pages=(
                DocPage("index.md", "alpha", 0),
                DocPage("expressions.md", "表达式详解", 10),
                DocPage("development.md", "安装与开发", 20),
            ),
            key="alpha",
            title="alpha",
            category="音游查询",
            category_order=100,
        )
        beta = _package(
            root,
            {"index.md": "# beta\n", "development.md": "# 安装与开发\n"},
            pages=(DocPage("index.md", "beta", 0), DocPage("development.md", "安装与开发", 10)),
            key="beta",
            title="beta",
            category="音游查询",
            category_order=100,
        )
        gamma = _package(
            root,
            {"index.md": "# gamma\n", "development.md": "# 安装与开发\n"},
            pages=(DocPage("index.md", "gamma", 0), DocPage("development.md", "安装与开发", 10)),
            key="gamma",
            title="gamma",
            category="实用工具",
            category_order=200,
        )
        core = _package(
            root,
            {"index.md": "# core\n", "guide.md": "# 指南\n"},
            pages=(DocPage("index.md", "概览", 0), DocPage("guide.md", "指南", 10)),
            key="core",
            group="core",
            title="core",
        )
        source = root / "cache" / "docs" / "src"
        theme_dir = root / "theme"
        theme_dir.mkdir()
        theme = ThemeSpec(
            name="test",
            version="1.0.0",
            source="file:test",
            root=root,
            theme_dir=theme_dir,
            package_dir=root,
            vitepress_version="1.6.4",
            node_major=18,
            config={"theme_config_key": "akari"},
        )
        generate(
            DocCatalog(packages=(alpha, beta, gamma, core)),
            source,
            DocsConfig(root=root, category_icons={"实用工具": "casino"}),
            theme=theme,
        )
        config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = config.index('"themeConfig": {')
        theme_config, _ = json.JSONDecoder().raw_decode(config[config.index("{", start) :])

    modules = next(item for item in theme_config["akari"]["sidebar"]["items"] if item["text"] == "模块")
    gaming, tools = modules["items"]
    core_group = next(item for item in theme_config["akari"]["sidebar"]["items"] if item["text"] == "核心")
    alpha_item = gaming["items"][0]
    native = theme_config["sidebar"]["/alpha/"][0]["items"]
    return (
        [category["text"] for category in modules["items"]] == ["音游查询", "实用工具"]
        and [package["text"] for package in gaming["items"]] == ["alpha", "beta"]
        and alpha_item["link"] == "/alpha/"
        and alpha_item["tabs"]
        == [
            {"text": "使用方法", "link": "/alpha/"},
            {"text": "表达式详解", "link": "/alpha/expressions"},
            {"text": "安装与开发", "link": "/alpha/development"},
        ]
        and [item["text"] for item in native] == ["使用方法", "表达式详解"]
        and all(item["link"] != "/alpha/development" for item in native)
        and gaming["icon"] == "music_note"
        and tools["icon"] == "casino"
        and "tabs" not in core_group["items"][0]
        and [item["text"] for item in core_group["items"][0]["items"]] == ["概览", "指南"]
        and tools["items"][0]["text"] == "gamma"
    )


async def _test_site_branding_home_and_group_icons():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        (root / "assets").mkdir()
        (root / "assets" / "logo.svg").write_text("<svg>logo</svg>\n", encoding="utf-8")
        (root / "assets" / "favicon.ico").write_bytes(b"icon")
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        source = root / "cache" / "docs" / "src"
        theme_dir = root / "theme"
        theme_dir.mkdir()
        theme = ThemeSpec(
            name="test",
            version="1.0.0",
            source="file:test",
            root=root,
            theme_dir=theme_dir,
            package_dir=root,
            vitepress_version="1.6.4",
            node_major=18,
            config={"theme_config_key": "akari"},
        )
        config = DocsConfig(
            root=root,
            site=DocsSiteConfig(base="/docs/", logo="assets/logo.svg", favicon="assets/favicon.ico"),
            theme=DocsThemeConfig(color="#d69cdd"),
            icons={"home": "dashboard", "module": "widgets"},
        )
        generate(DocCatalog(packages=(package,)), source, config, theme=theme)
        generated = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = generated.index('"themeConfig": {')
        theme_config, _ = json.JSONDecoder().raw_decode(generated[generated.index("{", start) :])
        sidebar = theme_config["akari"]["sidebar"]["items"]
        logo = (source / "public" / "site-logo.svg").read_text(encoding="utf-8")
        favicon = (source / "public" / "site-favicon.ico").read_bytes()
    return (
        logo == "<svg>logo</svg>\n"
        and favicon == b"icon"
        and theme_config["akari"]["appBar"]["logo"] == "/docs/site-logo.svg"
        and theme_config["akari"]["settings"]["defaults"]["color"] == "#d69cdd"
        and '"href": "/docs/site-favicon.ico"' in generated
        and sidebar[0] == {"text": "首页", "link": "/", "icon": "dashboard"}
        and next(item for item in sidebar if item["text"] == "模块")["icon"] == "widgets"
    )


async def _test_bundled_theme_color_injects_css():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        source = root / "cache" / "docs" / "src"
        config = DocsConfig(root=root, theme=DocsThemeConfig(color="#112233"))
        generate(DocCatalog(packages=(package,)), source, config)
        generated = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
    return '"style"' in generated and "--vp-c-brand-1:#112233" in generated


async def _test_external_theme_config():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        theme_dir = root / "theme"
        theme_dir.mkdir()
        (theme_dir / "head.ts").write_text("export function akariHead() { return [] }\n", encoding="utf-8")
        (theme_dir / "markdown.ts").write_text("export function akariMarkdown() {}\n", encoding="utf-8")
        theme = ThemeSpec(
            name="akari-docs",
            version="1.2.3",
            source="file:template",
            root=root,
            theme_dir=theme_dir,
            package_dir=root,
            vitepress_version="2.0.0-alpha.21",
            node_major=22,
            dependencies={"vitepress": "2.0.0-alpha.21"},
            install_mode="install",
            config={
                "appearance": False,
                "clean_urls": True,
                "custom_element_prefixes": ["m3e-"],
                "head_module": "head.ts",
                "head_export": "akariHead",
                "markdown_module": "markdown.ts",
                "markdown_export": "akariMarkdown",
                "theme_config_key": "akari",
                "search": {"provider": "local"},
            },
            digest="theme-digest",
        )
        package = _package(root, {"index.md": "# Demo\n"}, pages=(DocPage("index.md", "概览", 0),))
        source = root / "cache" / "docs" / "src"
        generate(DocCatalog(packages=(package,)), source, _docs(root), theme=theme)
        config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        copied = (source / ".vitepress" / "theme" / "head.ts").is_file()
    return (
        copied
        and 'import { akariHead } from "./theme/head.ts"' in config
        and 'import { akariMarkdown } from "./theme/markdown.ts"' in config
        and "head: [...akariHead(), ..." in config
        and '"rel": "icon"' in config
        and "akariMarkdown(md)" in config
        and '"akari":' in config
        and '"appBar"' in config
        and '"items"' in config
        and "isCustomElement" in config
        and '"appearance": false' in config
    )


async def _test_site_favicon_and_logo_defaults():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        brand_logo = root / "brand-logo.png"
        brand_logo.write_bytes(b"\x89PNG\r\n")
        package = _package(
            root,
            {"index.md": "# 用法\n"},
            pages=(DocPage("index.md", "用法", 0),),
            logo=str(brand_logo),
        )
        source = root / "cache" / "docs" / "src"
        generate(DocCatalog(packages=(package,)), source, DocsConfig(root=root))
        favicon_copied = (source / "public" / "site-favicon.ico").is_file()
        logo_copied = (source / "public" / "site-logo.png").is_file()
        theme_config = _theme_config(source)
        plain = _package(root, {"index.md": "# 用法\n"}, key="plain", pages=(DocPage("index.md", "用法", 0),))
        generate(DocCatalog(packages=(plain,)), source, DocsConfig(root=root))
        fallback = _theme_config(source)
        generate(
            DocCatalog(packages=(package,)),
            source,
            DocsConfig(root=root, site=DocsSiteConfig(logo="brand-logo.png", favicon="/static/icon.svg")),
        )
        override = _theme_config(source)
        head = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
    return (
        favicon_copied
        and logo_copied
        and theme_config["logo"] == "/site-logo.png"
        and fallback["logo"] == "/site-favicon.ico"
        and override["logo"] == "/site-logo.png"
        and "/static/icon.svg" in head
    )


def _theme_config(source: Path) -> dict:
    raw = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
    start = raw.index('"themeConfig": {')
    value, _ = json.JSONDecoder().raw_decode(raw[raw.index("{", start) :])
    return value


async def _test_labels_come_from_config():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(
            root,
            {"index.md": "# 用法\n", "development.md": "# 开发\n"},
            pages=(DocPage("index.md", "用法", 0), DocPage("development.md", "开发", 20)),
            group="module",
        )
        source = root / "cache" / "docs" / "src"
        config = DocsConfig(
            root=root,
            labels={"home": "主页", "overview": "总览", "usage": "用法", "development": "开发"},
            group_titles={"module": "功能"},
        )
        generate(DocCatalog(packages=(package,)), source, config)
        raw = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = raw.index('"themeConfig": {')
        theme_config, _ = json.JSONDecoder().raw_decode(raw[raw.index("{", start) :])
        native = theme_config["sidebar"]["/demo/"][0]["items"]
        index_text = (source / "index.md").read_text(encoding="utf-8")
    return native[0]["text"] == "用法" and theme_config["nav"][0]["text"] == "功能" and "## 功能" in index_text


async def _test_command_prefix_reaches_theme_config():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        package = _package(root, {"index.md": "# 用法\n"}, pages=(DocPage("index.md", "用法", 0),))
        source = root / "cache" / "docs" / "src"
        theme_dir = root / "theme"
        theme_dir.mkdir()
        theme = ThemeSpec(
            name="test",
            version="1.0.0",
            source="file:test",
            root=root,
            theme_dir=theme_dir,
            package_dir=root,
            vitepress_version="2.0.0-alpha.21",
            node_major=22,
            config={"theme_config_key": "akari"},
        )
        config = DocsConfig(root=root, site=DocsSiteConfig(command_prefix="!"))
        generate(DocCatalog(packages=(package,)), source, config, theme=theme)
        raw = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = raw.index('"themeConfig": {')
        theme_config, _ = json.JSONDecoder().raw_decode(raw[raw.index("{", start) :])
        prefix = theme_config["akari"]["commandPrefix"]
        plain = DocsConfig(root=root)
        generate(DocCatalog(packages=(package,)), source, plain, theme=theme)
        raw = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = raw.index('"themeConfig": {')
        absent, _ = json.JSONDecoder().raw_decode(raw[raw.index("{", start) :])
    return prefix == "!" and "commandPrefix" not in absent["akari"]


async def _test_locales_generate_translated_tree_and_links():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        files = {
            "index.md": "# Demo\n",
            "development.md": "# 开发\n",
            "en-US/index.md": "# Docs\n\nSee [development](development.md).\n",
        }
        pages = (
            DocPage("index.md", "概览", 0),
            DocPage("development.md", "开发", 20),
            DocPage("en-US/index.md", "Docs", 0),
        )
        package = _package(root, files, pages=pages)
        source = root / "cache" / "docs" / "src"
        config = DocsConfig(
            root=root,
            site=DocsSiteConfig(title="站"),
            locales=(
                DocsLocaleConfig(tag="zh-CN", label="简体中文"),
                DocsLocaleConfig(tag="en-US", label="English", title="Docs"),
            ),
        )
        generate(DocCatalog(packages=(package,)), source, config)
        raw_config = (source / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        start = raw_config.index('"locales": {')
        locales, _ = json.JSONDecoder().raw_decode(raw_config[raw_config.index("{", start) :])
        default = (source / "index.md").read_text(encoding="utf-8")
        localized = (source / "en-US" / "demo" / "index.md").read_text(encoding="utf-8")
        generated = {
            "default_page": (source / "demo" / "index.md").is_file(),
            "locale_dir_excluded": not (source / "demo" / "en-US").exists(),
            "localized_page": (source / "en-US" / "demo" / "index.md").is_file(),
            "fallback_page": (source / "en-US" / "demo" / "development.md").is_file(),
            "localized_index": (source / "en-US" / "index.md").is_file(),
        }
        translated = locales["en-US"]["themeConfig"]
    return (
        generated
        == {
            "default_page": True,
            "locale_dir_excluded": True,
            "localized_page": True,
            "fallback_page": True,
            "localized_index": True,
        }
        and locales["root"]["lang"] == "zh-CN"
        and locales["en-US"]["link"] == "/en-US/"
        and locales["en-US"]["label"] == "English"
        and translated["nav"][0]["link"] == "/en-US/demo/"
        and "/en-US/demo/" in translated["sidebar"]
        and default.startswith("# 站")
        and "en-US" not in default
        and localized.startswith("# Docs")
    )


@func_case
async def test_docs_generator(tester: Tester):
    """cli.docs.generator: 站点生成与路径约束"""
    await tester.test(_test_generate_site_layout, "生成索引、分组、侧栏与页面副本")
    await tester.test(_test_base_env_override, "环境变量覆盖 base")
    await tester.test(_test_generate_rejects_source_outside_cache, "拒绝 cache/docs 之外的源目录")
    await tester.test(_test_generate_rejects_symlink_escape, "拒绝符号链接逃逸")
    await tester.test(_test_package_without_pages_gets_placeholder, "无页面时生成占位首页")
    await tester.test(_test_unsafe_package_key_is_rejected, "拒绝含路径片段的包 key")
    await tester.test(_test_cross_package_links_are_rewritten, "跨包相对链接折算为站点 URL")
    await tester.test(_test_module_meta_is_injected_from_doc_toml, "doc.toml 元数据注入模块属性卡")
    await tester.test(_test_package_without_meta_has_no_component, "无元数据的包不注入属性卡")
    await tester.test(_test_module_categories_and_parallel_tabs, "模块分类、分类图标与平行页面侧栏")
    await tester.test(_test_site_branding_home_and_group_icons, "站点 Logo、favicon、首页与一级图标")
    await tester.test(_test_bundled_theme_color_injects_css, "内置主题注入主题色变量")
    await tester.test(_test_external_theme_config, "外部主题生成 head、markdown 与侧栏配置")
    await tester.test(_test_labels_come_from_config, "侧栏与导航文案取自配置")
    await tester.test(_test_command_prefix_reaches_theme_config, "命令前缀写入主题配置，缺失时不写")
    await tester.test(_test_site_favicon_and_logo_defaults, "站点图标取随包素材，顶栏标志取包声明并可回退")
    await tester.test(_test_locales_generate_translated_tree_and_links, "多语言生成独立目录、回退页与带前缀链接")
    return tester
