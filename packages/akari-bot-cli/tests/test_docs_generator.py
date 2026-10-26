"""``akaribot.cli.docs.generator``：站点源文件、侧栏与路径约束。"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli.docs.config import DocsConfig
from akaribot.cli.docs.generator import generate
from akaribot.cli.docs.model import DocCatalog, DocPackage, DocPage, DocsError
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
    base: Path, files: dict[str, bytes | str], *, pages: tuple[DocPage, ...] = (), key: str = "demo"
) -> DocPackage:
    doc_path = base / f"doc-{key}"
    doc_path.mkdir(parents=True, exist_ok=True)
    _write(doc_path, files)
    return DocPackage(
        key=key,
        group="module",
        dist=f"akari-bot-module-{key}",
        name=key,
        version="1.0.0",
        title="Demo",
        summary="示例包",
        doc_path=doc_path,
        pages=pages,
    )


def _docs(root: Path) -> DocsConfig:
    return DocsConfig(root=root)


async def _test_generate_site_layout():
    with TemporaryDirectory(prefix="akari-docs-gen-") as raw:
        root = Path(raw)
        files = {
            "index.md": "# Demo\n",
            "guide/setup.md": "# 安装\n",
            "images/logo.png": b"\x89PNG\r\n",
            "notes.txt": "说明\n",
            "manual.pdf": b"%PDF-1.4",
            "payload.bin": b"\x00\x01",
        }
        pages = (DocPage("index.md", "概览", 0), DocPage("guide/setup.md", "安装", 10))
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
        and '"text": "Demo"' in config
        and "# AkariBot 文档" in index
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
    return tester
