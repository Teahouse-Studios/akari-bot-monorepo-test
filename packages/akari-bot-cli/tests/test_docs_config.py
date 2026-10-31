"""``akaribot.cli.docs.config``：站点品牌、图标与资源路径。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs.config import DocsConfig, DocsSiteConfig, load_config, site_asset_path
from akaribot.cli.docs.model import DocsError
from akaribot.testing import Tester, func_case


class _Instance:
    def __init__(self, root: Path) -> None:
        self.root = root


async def _test_loads_branding_and_icons():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text(
            "[site]\n"
            'title = "文档"\n'
            'logo = "assets/logo.svg"\n'
            'favicon = "assets/favicon.ico"\n'
            "\n[icons]\n"
            'home = "home"\n'
            'module = "widgets"\n'
            "\n[theme]\n"
            'color = "#D69CDD"\n',
            encoding="utf-8",
        )
        config = load_config(_Instance(root))
    return (
        config.site == DocsSiteConfig(title="文档", logo="assets/logo.svg", favicon="assets/favicon.ico")
        and config.icons == {"home": "home", "module": "widgets"}
        and config.theme.color == "#d69cdd"
    )


async def _test_theme_color_must_be_hex():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text('[theme]\ncolor = "purple"\n', encoding="utf-8")
        try:
            load_config(_Instance(root))
        except DocsError as exc:
            error = (str(exc), exc.params.get("reason"))
        else:
            error = ("", "")
    return error == ("cli.docs.error.bad_config", "theme.color must be #rrggbb")


async def _test_icons_must_be_non_empty_strings():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text("[icons]\ncore = 1\n", encoding="utf-8")
        try:
            load_config(_Instance(root))
        except DocsError as exc:
            error = (str(exc), exc.params.get("reason"))
        else:
            error = ("", "")
    return error[0] == "cli.docs.error.bad_config" and "icons.core" in str(error[1])


async def _test_site_asset_path_resolves_and_rejects_unsafe_files():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        base = Path(raw)
        root = base / "instance"
        root.mkdir()
        (root / "assets").mkdir()
        (root / "assets" / "logo.svg").write_text("<svg/>", encoding="utf-8")
        outside = base / "outside.svg"
        outside.write_text("<svg/>", encoding="utf-8")
        local = site_asset_path(root, "assets/logo.svg")
        remote = site_asset_path(root, "https://example.test/logo.svg")
        site_path = site_asset_path(root, "/assets/logo.svg")
        try:
            site_asset_path(root, "missing.svg")
        except DocsError as exc:
            missing = str(exc)
        else:
            missing = ""
        try:
            site_asset_path(root, "../outside.svg")
        except DocsError as exc:
            unsafe = str(exc)
        else:
            unsafe = ""
        config = DocsConfig(root=root)
    return (
        local == (root / "assets" / "logo.svg").resolve()
        and remote is None
        and site_path is None
        and missing == "cli.docs.error.site_asset_missing"
        and unsafe == "cli.docs.error.unsafe_path"
        and config.icons == {}
        and config.site.logo == ""
        and config.site.favicon == ""
    )


@func_case
async def test_docs_config(tester: Tester):
    """cli.docs.config: 站点品牌、一级图标与资源路径"""
    await tester.test(_test_loads_branding_and_icons, "读取 Logo、favicon 与一级图标")
    await tester.test(_test_theme_color_must_be_hex, "主题色必须是 #rrggbb")
    await tester.test(_test_icons_must_be_non_empty_strings, "图标值必须是非空字符串")
    await tester.test(_test_site_asset_path_resolves_and_rejects_unsafe_files, "本地资源解析与越界拒绝")
    return tester
