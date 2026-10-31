"""``akaribot.cli.docs.theme``：主题清单解析、外部模板与内置回退。"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs.config import DocsConfig, DocsThemeConfig
from akaribot.cli.docs.model import DocsError
from akaribot.cli.docs.theme import (
    BUNDLED_SOURCE,
    TEMPLATE_DIR,
    THEME_ENV,
    bundled_theme,
    resolve_theme,
)
from akaribot.testing import Tester, func_case


def _external(root: Path, name: str = "akari-bot-docs-template") -> Path:
    theme_root = root / name
    theme_dir = theme_root / "docs/.vitepress/theme"
    theme_dir.mkdir(parents=True)
    (theme_dir / "index.ts").write_text("export default {}\n", encoding="utf-8")
    (theme_root / "docs-theme.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "name": "akari-docs",
                "version": "1.2.3",
                "theme_dir": "docs/.vitepress/theme",
                "vitepress": "2.0.0-alpha.21",
                "node": ">=22.12.0",
                "install_mode": "install",
                "dependencies": {"vitepress": "2.0.0-alpha.21", "vue": "^3.5.43"},
                "config": {"theme_config_key": "akari"},
            }
        ),
        encoding="utf-8",
    )
    return theme_root


async def _test_theme_digest_tracks_content_changes():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        external = _external(root)
        package = external / "package.json"
        lock = external / "package-lock.json"
        package.write_text('{"name": "theme"}\n', encoding="utf-8")
        lock.write_text('{"lockfileVersion": 3}\n', encoding="utf-8")
        config = DocsConfig(root=root, theme=DocsThemeConfig(source=f"file:{external}"))
        first = resolve_theme(config).digest

        source = external / "docs/.vitepress/theme/index.ts"
        original_source = source.read_text(encoding="utf-8")
        source_stat = source.stat()
        changed_source = original_source.replace("export default {}", "export default []")
        assert len(changed_source) == len(original_source)
        source.write_text(changed_source, encoding="utf-8")
        os.utime(source, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))
        second = resolve_theme(config).digest

        source.write_text(original_source, encoding="utf-8")
        os.utime(source, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))
        original_lock = lock.read_text(encoding="utf-8")
        lock_stat = lock.stat()
        lock.write_text(original_lock.replace("3", "2"), encoding="utf-8")
        os.utime(lock, ns=(lock_stat.st_atime_ns, lock_stat.st_mtime_ns))
        third = resolve_theme(config).digest
    return first != second and first != third


async def _test_bundled_theme():
    theme = bundled_theme()
    return (
        theme.name == "bundled"
        and theme.source == BUNDLED_SOURCE
        and theme.theme_dir == TEMPLATE_DIR / "theme"
        and theme.vitepress_version == "1.6.4"
        and theme.node_major == 18
        and theme.install_mode == "ci"
        and theme.config.get("search") == {"provider": "local"}
    )


async def _test_file_theme():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        external = _external(root)
        config = DocsConfig(root=root, theme=DocsThemeConfig(source=f"file:{external}"))
        theme = resolve_theme(config)
    return (
        theme.name == "akari-docs"
        and theme.version == "1.2.3"
        and theme.vitepress_version == "2.0.0-alpha.21"
        and theme.node_major == 22
        and theme.install_mode == "install"
        and theme.dependencies["vitepress"] == "2.0.0-alpha.21"
        and theme.config["theme_config_key"] == "akari"
    )


async def _test_auto_theme_in_instance():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        external = _external(root)
        theme = resolve_theme(DocsConfig(root=root))
    return theme.source == f"auto:{external}" and theme.name == "akari-docs"


async def _test_environment_overrides_source():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        external = _external(root)
        config = DocsConfig(root=root, theme=DocsThemeConfig(source="bundled"))
        theme = resolve_theme(config, environ={THEME_ENV: f"file:{external}"})
    return theme.name == "akari-docs"


async def _test_missing_theme_is_reported():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        config = DocsConfig(root=root, theme=DocsThemeConfig(source="file:missing"))
        try:
            resolve_theme(config)
        except DocsError as exc:
            error = (str(exc), exc.params.get("source"))
        else:
            error = ("", "")
    return error == ("cli.docs.error.theme_missing", "file:missing")


async def _test_unsupported_source_is_reported():
    with TemporaryDirectory(prefix="akari-docs-theme-") as raw:
        root = Path(raw)
        config = DocsConfig(root=root, theme=DocsThemeConfig(source="npm:other-theme"))
        try:
            resolve_theme(config)
        except DocsError as exc:
            error = (str(exc), exc.params.get("source"))
        else:
            error = ("", "")
    return error == ("cli.docs.error.theme_unsupported", "npm:other-theme")


@func_case
async def test_docs_theme(tester: Tester):
    """cli.docs.theme: 内置回退、外部模板与来源校验"""
    await tester.test(_test_bundled_theme, "内置主题清单")
    await tester.test(_test_theme_digest_tracks_content_changes, "主题摘要按内容变化，不受 mtime 与尺寸影响")
    await tester.test(_test_file_theme, "file 来源读取外部模板")
    await tester.test(_test_auto_theme_in_instance, "auto 在实例根发现模板")
    await tester.test(_test_environment_overrides_source, "环境变量覆盖主题来源")
    await tester.test(_test_missing_theme_is_reported, "缺失主题报错")
    await tester.test(_test_unsupported_source_is_reported, "不支持的主题来源报错")
    return tester
