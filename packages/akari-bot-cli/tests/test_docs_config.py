"""``akaribot.cli.docs.config``：站点品牌、分组与分类图标、资源路径。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs.config import DocsConfig, load_config, site_asset_path
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
            "\n[category_icons]\n"
            '"音游查询" = "music_note"\n'
            '"实用工具" = "handyman"\n'
            "\n[theme]\n"
            'color = "#D69CDD"\n',
            encoding="utf-8",
        )
        config = load_config(_Instance(root))
    return (
        config.site.title == "文档"
        and config.site.logo == "assets/logo.svg"
        and config.site.favicon == "assets/favicon.ico"
        and config.site.lang == "zh-CN"
        and config.site.base == "/"
        and config.icons["home"] == "home"
        and config.icons["module"] == "widgets"
        and config.icons["core"] == "dashboard"
        and config.category_icons["音游查询"] == "music_note"
        and config.category_icons["实用工具"] == "handyman"
        and config.category_icons["群组管理"] == "groups"
        and config.assets["favicon"] == "favicon.ico"
        and config.theme.color == "#d69cdd"
    )


async def _test_assets_are_overridable():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text('[assets]\nfavicon = "custom.ico"\n', encoding="utf-8")
        config = load_config(_Instance(root))
    return config.assets["favicon"] == "custom.ico"


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
        reasons: list[str | None] = []
        for table, key in (("icons", "core"), ("category_icons", "音游查询")):
            (root / "docs.toml").write_text(f'[{table}]\n"{key}" = 1\n', encoding="utf-8")
            try:
                load_config(_Instance(root))
            except DocsError as exc:
                reasons.append(exc.params.get("reason"))
            else:
                reasons.append(None)
    return reasons == [
        "icons.core is not a non-empty string",
        "category_icons.音游查询 is not a non-empty string",
    ]


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
        and config.icons["home"] == "home"
        and config.labels["overview"] == "概览"
        and config.site.logo == ""
        and config.site.favicon == ""
        and config.site.title == "小可 · 文档"
    )


async def _test_labels_and_group_titles_override():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text(
            '[labels]\nhome = "主页"\n\n[group_titles]\nmodule = "功能模块"\n',
            encoding="utf-8",
        )
        config = load_config(_Instance(root))
    return (
        config.labels["home"] == "主页"
        and config.labels["overview"] == "概览"
        and config.group_titles["module"] == "功能模块"
        and config.group_titles["core"] == "核心"
    )


async def _test_labels_must_be_non_empty_strings():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text('[labels]\nhome = ""\n', encoding="utf-8")
        try:
            load_config(_Instance(root))
        except DocsError as exc:
            error = (str(exc), exc.params.get("reason"))
        else:
            error = ("", "")
    return error == ("cli.docs.error.bad_config", "labels.home is not a non-empty string")


async def _test_command_prefix_comes_from_instance_config():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        (root / "config" / "config.toml").write_text(
            '[config]\ncommand_prefix = ["!", "！"]\n',
            encoding="utf-8",
        )
        resolved = load_config(_Instance(root))
        direct = DocsConfig(root=root)
    return resolved.site.command_prefix == "!" and direct.site.command_prefix == "!"


async def _test_command_prefix_override_and_missing_config():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "docs.toml").write_text('[site]\ncommand_prefix = "%"\n', encoding="utf-8")
        overridden = load_config(_Instance(root))
        (root / "config").mkdir()
        (root / "config" / "config.toml").write_text("[config]\ncommand_prefix = []\n", encoding="utf-8")
        (root / "docs.toml").unlink()
        empty = load_config(_Instance(root))
    return overridden.site.command_prefix == "%" and empty.site.command_prefix == ""


async def _test_site_title_defaults_and_override():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        default = DocsConfig(root=root)
        (root / "docs.toml").write_text('[site]\ntitle = "实例文档"\n', encoding="utf-8")
        overridden = load_config(_Instance(root))
    return default.site.title == "小可 · 文档" and overridden.site.title == "实例文档"


async def _test_site_defaults_cover_lang_base_and_out_dir():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        default = DocsConfig(root=root)
        (root / "docs.toml").write_text(
            '[site]\nlang = "en-US"\nbase = "/docs/"\n\n[build]\nout_dir = "out"\n',
            encoding="utf-8",
        )
        overridden = load_config(_Instance(root))
    return (
        default.site.lang == "zh-CN"
        and default.site.base == "/"
        and default.build.out_dir == "cache/docs/site"
        and overridden.site.lang == "en-US"
        and overridden.site.base == "/docs/"
        and overridden.build.out_dir == "out"
    )


async def _test_locales_declare_languages_and_inherit_defaults():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        (root / "config" / "config.toml").write_text('[config]\ncommand_prefix = ["~"]\n', encoding="utf-8")
        (root / "docs.toml").write_text(
            "[site]\n"
            'locales = ["zh-CN", "en-US"]\n'
            "\n[locales.en-US]\n"
            'label = "English"\n'
            'title = "Docs"\n'
            "\n[locales.en-US.labels]\n"
            'home = "Home"\n'
            "\n[locales.en-US.group_titles]\n"
            'module = "Modules"\n',
            encoding="utf-8",
        )
        config = load_config(_Instance(root))
        (root / "docs.toml").write_text(
            '[site]\nlocales = ["en-US"]\n\n[locales.en-US]\nlabel = "English"\n', encoding="utf-8"
        )
        english = load_config(_Instance(root))
    return (
        tuple(locale.tag for locale in config.locales) == ("zh-CN", "en-US")
        and tuple(locale.tag for locale in english.locales) == ("en-US",)
        and english.site.lang == "en-US"
        and config.default_locale.tag == "zh-CN"
        and config.site.lang == "zh-CN"
        and config.locales[0].label == "简体中文"
        and config.locales[1].label == "English"
        and config.locales[1].title == "Docs"
        and config.locales[1].labels["home"] == "Home"
        and config.locales[1].labels["usage"] == "使用方法"
        and config.locales[1].group_titles["module"] == "Modules"
        and config.locales[1].group_titles["core"] == "核心"
    )


async def _test_locales_reject_undefined_and_invalid_tags():
    with TemporaryDirectory(prefix="akari-docs-config-") as raw:
        root = Path(raw)
        missing = invalid = None
        (root / "docs.toml").write_text('[site]\nlocales = ["zh-CN", "en-US"]\n', encoding="utf-8")
        try:
            load_config(_Instance(root))
        except DocsError as error:
            missing = error
        (root / "docs.toml").write_text(
            '[site]\nlocales = ["zh-CN"]\n\n[locales.zh-CN]\nlabel = "简体中文"\n',
            encoding="utf-8",
        )
        good = load_config(_Instance(root))
        (root / "docs.toml").write_text(
            '[site]\nlocales = ["中文"]\n\n[locales."中文"]\nlabel = "中文"\n',
            encoding="utf-8",
        )
        try:
            load_config(_Instance(root))
        except DocsError as error:
            invalid = error
    return (
        missing is not None
        and "locales." in str(missing.params.get("reason", ""))
        and invalid is not None
        and good.default_locale.label == "简体中文"
    )


@func_case
async def test_docs_config(tester: Tester):
    """cli.docs.config: 站点品牌、分组与分类图标、资源路径"""
    await tester.test(_test_loads_branding_and_icons, "读取 Logo、favicon、一级图标与分类图标")
    await tester.test(_test_theme_color_must_be_hex, "主题色必须是 #rrggbb")
    await tester.test(_test_icons_must_be_non_empty_strings, "图标值必须是非空字符串，错误指出所在表")
    await tester.test(_test_site_asset_path_resolves_and_rejects_unsafe_files, "本地资源解析与越界拒绝")
    await tester.test(_test_labels_and_group_titles_override, "文案与分组标题可由 docs.toml 覆盖，未覆盖项沿用默认值")
    await tester.test(_test_labels_must_be_non_empty_strings, "文案值必须是非空字符串，错误指出所在表")
    await tester.test(_test_assets_are_overridable, "站点素材可由 docs.toml 覆盖")
    await tester.test(_test_command_prefix_comes_from_instance_config, "命令前缀取自实例核心配置")
    await tester.test(_test_command_prefix_override_and_missing_config, "站点配置覆盖前缀，缺失时为空")
    await tester.test(_test_site_title_defaults_and_override, "站点标题默认取自随包默认值，可由 docs.toml 覆盖")
    await tester.test(_test_site_defaults_cover_lang_base_and_out_dir, "语言、基路径与输出目录的默认值同样来自随包配置")
    await tester.test(_test_locales_declare_languages_and_inherit_defaults, "语言清单声明语言并继承默认文案")
    await tester.test(_test_locales_reject_undefined_and_invalid_tags, "语言缺少配置或标签非法时报错")
    return tester
