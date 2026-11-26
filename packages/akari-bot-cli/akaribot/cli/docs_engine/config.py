"""``docs.toml`` 的读取与默认值。

配置只读不写：站点标题、语言、部署基路径与输出目录都由实例维护者提供，文档引擎不代写。
"""

from __future__ import annotations

import json
import os
import re
import tomllib
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from .model import DocsError

CONFIG_FILENAME = "docs.toml"
DEFAULTS_FILENAME = "defaults.toml"
CORE_CONFIG_FILENAME = "config/config.toml"
_DEFAULTS_PATH = Path(__file__).with_name(DEFAULTS_FILENAME)
DEFAULT_ASSETS_DIR = Path(__file__).with_name("assets")
DEFAULT_THEME_SOURCE = "auto"
BASE_ENV = "AKARIBOT_DOCS_BASE"
_URL_PATTERN = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]+:|//)")
_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
LOCALE_PATTERN = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


@dataclass(frozen=True)
class DocsFooterLink:
    """页脚关于区块的按钮。

    :param text: 按钮文字，同时作为无障碍名称。
    :param link: 按钮指向的地址，可以是 URL 或站内路径。
    :param icon: 内置图标名（``afdian``、``github``）或图片路径。相对路径按实例根解析。
    """

    text: str
    link: str
    icon: str = ""


@dataclass(frozen=True)
class DocsFooterConfig:
    """页脚关于区块。

    :param enabled: 是否显示该区块。
    :param title: 标题。留空时取 ``defaults.toml`` 的 ``[footer] title``。
    :param text: 正文段落。``None`` 取默认段落，空元组不显示正文。
    :param image: 配图。相对路径按实例根解析，也可写 URL 或站点路径。留空时使用角色立绘。
    :param links: 按钮。``None`` 取默认按钮，空元组不显示按钮。
    :param copyright: 版权行。留空时取 ``defaults.toml`` 的 ``[footer] copyright``。
    """

    enabled: bool = True
    title: str = ""
    text: tuple[str, ...] | None = None
    image: str = ""
    links: tuple[DocsFooterLink, ...] | None = None
    copyright: str = ""


@dataclass(frozen=True)
class DocsDefaults:
    """随包分发的默认文案与图标。

    :param labels: 界面文案，键为 ``home``、``overview``、``usage``、``development``。
    :param group_titles: 侧栏分组标题，键为包分组名。
    :param icons: 分组与 ``home`` 的图标名。
    :param category_icons: 分类图标名，键为 ``docs.toml`` 的 ``category``。
    :param assets: 随包站点素材，键为用途，值为 ``assets/`` 下的文件名。
    :param site: 站点展示默认值，目前只有 ``title``。
    :param build: 构建开关的默认值，目前有 ``webp`` 与 ``webp_keep_original``。
    :param locales: 默认语言清单，键为语言标签，值为显示名称。
    """

    labels: Mapping[str, str] = field(default_factory=dict)
    group_titles: Mapping[str, str] = field(default_factory=dict)
    icons: Mapping[str, str] = field(default_factory=dict)
    category_icons: Mapping[str, str] = field(default_factory=dict)
    assets: Mapping[str, str] = field(default_factory=dict)
    site: Mapping[str, str] = field(default_factory=dict)
    build: Mapping[str, bool] = field(default_factory=dict)
    locales: Mapping[str, str] = field(default_factory=dict)
    footer: DocsFooterConfig = field(default_factory=DocsFooterConfig)


@lru_cache(maxsize=1)
def load_defaults() -> DocsDefaults:
    """读取随包分发的 ``defaults.toml``。

    :return: 默认文案与图标。
    :raises DocsError: 文件无法解析，或某段的取值不是非空字符串。
    """
    path = _DEFAULTS_PATH
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=str(exc)) from exc
    return DocsDefaults(
        labels=_string_map(data, path, "labels"),
        group_titles=_string_map(data, path, "group_titles"),
        icons=_string_map(data, path, "icons"),
        category_icons=_string_map(data, path, "category_icons"),
        assets=_string_map(data, path, "assets"),
        site=_string_map(data, path, "site"),
        build=_bool_map(data, path, "build"),
        locales=_locale_labels(data, path),
        footer=_footer_config(data, path),
    )


def default_labels() -> dict[str, str]:
    """返回默认界面文案的副本，供目录层在未持有实例配置时使用。"""
    return dict(load_defaults().labels)


@dataclass(frozen=True)
class DocsLocaleConfig:
    """一种语言的站点设置。

    :param tag: 语言标签，同时作为非默认语言的目录名与 URL 前缀。
    :param label: 语言选择器里的显示名称。
    :param title: 该语言的站点标题。留空时取默认语言的标题。
    :param labels: 该语言的界面文案，逐键覆盖默认值。
    :param group_titles: 该语言的侧栏分组标题，逐键覆盖默认值。
    """

    tag: str
    label: str = ""
    title: str = ""
    labels: Mapping[str, str] = field(default_factory=dict)
    group_titles: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DocsThemeConfig:
    """站点主题设置。

    :param source: 主题来源：``auto``、``bundled``、``file:<路径>`` 或实例内的相对路径。
    :param color: M3E 种子色，格式为 ``#rrggbb``。空串使用主题默认值。
    """

    source: str = DEFAULT_THEME_SOURCE
    color: str = ""


@dataclass(frozen=True)
class DocsSiteConfig:
    """站点展示设置。

    :param title: 站点标题。留空时取 ``defaults.toml`` 的 ``[site] title``。
    :param lang: 页面语言标签。留空时取 ``defaults.toml`` 的 ``[site] lang``。
    :param base: 部署基路径。留空时取 ``defaults.toml`` 的 ``[site] base``。
    :param logo: 日间标志。相对路径按实例根解析，也可写 URL 或站点路径。
    :param logo_dark: 夜间标志。留空时使用品牌包或内置资源。
    :param avatar: 对话示例的机器人头像。相对路径按实例根解析，也可写 URL 或站点路径。
    :param character: 角色立绘。留空时使用品牌包或内置资源。
    :param credits: 制作人员名单文件。留空时使用品牌包资源。
    :param favicon: 站点图标。相对路径按实例根解析，也可写 URL 或站点路径。
    :param command_prefix: 命令用法行使用的前缀。留空时取实例核心配置的首个前缀。
    """

    title: str = ""
    lang: str = ""
    base: str = ""
    logo: str = ""
    logo_dark: str = ""
    avatar: str = ""
    character: str = ""
    credits: str = ""
    favicon: str = ""
    command_prefix: str = ""


@dataclass(frozen=True)
class DocsBuildConfig:
    """构建输出设置。

    :param out_dir: 输出目录，相对实例根或绝对路径。留空时取 ``defaults.toml`` 的 ``[site] out_dir``。
    :param webp: 构建时把页面引用的位图转成 WebP。``None`` 时取 ``defaults.toml`` 的 ``[build] webp``。
    :param webp_keep_original: 转换后保留原图。``None`` 时取 ``defaults.toml`` 的 ``[build] webp_keep_original``。
    """

    out_dir: str = ""
    webp: bool | None = None
    webp_keep_original: bool | None = None


@dataclass(frozen=True)
class DocsConfig:
    """实例的文档配置。

    :param root: 实例根目录。
    :param site: 站点展示设置。
    :param build: 构建输出设置。
    :param theme: 主题来源与清单解析设置。
    :param labels: 界面文案，``defaults.toml`` 提供默认值，实例可逐键覆盖。
    :param group_titles: 侧栏分组标题，``defaults.toml`` 提供默认值。
    :param icons: 侧栏一级项的图标名，键为分组或 ``home``。
    :param category_icons: 侧栏分类的图标名，键为 ``docs.toml`` 的 ``category``。
    :param assets: 随包站点素材，``defaults.toml`` 提供默认值。
    :param locales: 站点语言，首项为默认语言。留空时由 ``site.lang`` 推导。
    :param footer: 页脚关于区块，``defaults.toml`` 提供默认文案与按钮。
    :param deploy: 部署设置，由命令层解释，引擎只透传。
    """

    root: Path
    site: DocsSiteConfig = field(default_factory=DocsSiteConfig)
    build: DocsBuildConfig = field(default_factory=DocsBuildConfig)
    theme: DocsThemeConfig = field(default_factory=DocsThemeConfig)
    labels: Mapping[str, str] = field(default_factory=default_labels)
    group_titles: Mapping[str, str] = field(default_factory=lambda: dict(load_defaults().group_titles))
    icons: Mapping[str, str] = field(default_factory=lambda: dict(load_defaults().icons))
    category_icons: Mapping[str, str] = field(default_factory=lambda: dict(load_defaults().category_icons))
    assets: Mapping[str, str] = field(default_factory=lambda: dict(load_defaults().assets))
    locales: tuple[DocsLocaleConfig, ...] = ()
    footer: DocsFooterConfig = field(default_factory=DocsFooterConfig)
    deploy: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        explicit_lang = self.site.lang
        if not self.site.command_prefix:
            object.__setattr__(self, "site", replace(self.site, command_prefix=read_command_prefix(self.root)))
        defaults = load_defaults()
        missing = {
            name: defaults.site[name]
            for name in ("title", "lang", "base")
            if name in defaults.site and not getattr(self.site, name)
        }
        if missing:
            object.__setattr__(self, "site", replace(self.site, **missing))
        build = self.build
        if not build.out_dir and "out_dir" in defaults.site:
            build = replace(build, out_dir=defaults.site["out_dir"])
        if build.webp is None:
            build = replace(build, webp=defaults.build.get("webp", True))
        if build.webp_keep_original is None:
            build = replace(build, webp_keep_original=defaults.build.get("webp_keep_original", True))
        if build != self.build:
            object.__setattr__(self, "build", build)
        object.__setattr__(self, "locales", self._resolved_locales(defaults, explicit_lang))
        object.__setattr__(self, "footer", _merge_footer(self.footer, defaults.footer))
        for name, source in (
            ("labels", defaults.labels),
            ("group_titles", defaults.group_titles),
            ("icons", defaults.icons),
            ("category_icons", defaults.category_icons),
            ("assets", defaults.assets),
        ):
            object.__setattr__(self, name, {**source, **dict(getattr(self, name))})

    def _resolved_locales(self, defaults: DocsDefaults, explicit_lang: str) -> tuple[DocsLocaleConfig, ...]:
        configured = self.locales
        if not configured:
            tag = self.site.lang or next(iter(defaults.locales), "zh-CN")
            configured = (DocsLocaleConfig(tag=tag, label=defaults.locales.get(tag, tag)),)
        if explicit_lang and explicit_lang != configured[0].tag:
            raise DocsError(
                "cli.docs.error.bad_config",
                path=str(self.root / CONFIG_FILENAME),
                reason="site.lang must match the first locale",
            )
        resolved: list[DocsLocaleConfig] = []
        for locale in configured:
            tag = locale.tag.strip()
            if not LOCALE_PATTERN.match(tag):
                raise DocsError(
                    "cli.docs.error.bad_config",
                    path=str(self.root / CONFIG_FILENAME),
                    reason=f"invalid locale tag: {locale.tag}",
                )
            resolved.append(
                replace(
                    locale,
                    tag=tag,
                    label=locale.label or defaults.locales.get(tag, tag),
                    title=locale.title or self.site.title,
                    labels={**defaults.labels, **dict(self.labels), **dict(locale.labels)},
                    group_titles={**defaults.group_titles, **dict(self.group_titles), **dict(locale.group_titles)},
                )
            )
        tags = [locale.tag for locale in resolved]
        if len(set(tags)) != len(tags):
            raise DocsError(
                "cli.docs.error.bad_config",
                path=str(self.root / CONFIG_FILENAME),
                reason="duplicate locale tag",
            )
        object.__setattr__(self, "site", replace(self.site, lang=resolved[0].tag))
        return tuple(resolved)

    @property
    def default_locale(self) -> DocsLocaleConfig:
        """默认语言。"""
        return self.locales[0]

    @property
    def cache_docs_dir(self) -> Path:
        """生成器与工具链共用的缓存目录 ``<实例根目录>/cache/docs``。"""
        return self.root / "cache" / "docs"

    @property
    def out_dir(self) -> Path:
        """输出目录的绝对路径。配置为相对路径时以实例根目录为基准。"""
        configured = Path(self.build.out_dir).expanduser()
        return configured if configured.is_absolute() else self.root / configured

    @property
    def base(self) -> str:
        """当前生效的基础路径，环境变量优先于配置文件。"""
        return normalize_base(os.environ.get(BASE_ENV) or self.site.base)


def normalize_base(value: str) -> str:
    """将基础路径规范为以 ``/`` 开头并结尾的形式。"""
    text = (value or "").strip()
    if not text or text == "/":
        return "/"
    if not text.startswith("/"):
        text = "/" + text
    if not text.endswith("/"):
        text += "/"
    return text


def load_config(instance: Any) -> DocsConfig:
    """读取实例的 ``docs.toml``，缺失时使用默认值。

    :param instance: 带 ``root`` 属性的实例。
    :return: 解析后的配置。
    :raises DocsError: 文件不是合法 TOML，或站点与构建段不是表。
    """
    root = Path(instance.root)
    path = root / CONFIG_FILENAME
    if not path.is_file():
        return DocsConfig(root=root)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=str(exc)) from exc

    site = _table(data, "site", path)
    build = _table(data, "build", path)
    locales = _locale_config(data, path)
    theme = _table(data, "theme", path)
    deploy = _table(data, "deploy", path)
    return DocsConfig(
        root=root,
        site=DocsSiteConfig(
            title=_text(site, "title", ""),
            lang=_text(site, "lang", ""),
            base=_text(site, "base", ""),
            logo=_text(site, "logo", ""),
            logo_dark=_text(site, "logo_dark", ""),
            avatar=_text(site, "avatar", ""),
            character=_text(site, "character", ""),
            credits=_text(site, "credits", ""),
            favicon=_text(site, "favicon", ""),
            command_prefix=_text(site, "command_prefix", "").strip() or read_command_prefix(root),
        ),
        build=DocsBuildConfig(
            out_dir=_text(build, "out_dir", ""),
            webp=_build_flag(build, "webp", path),
            webp_keep_original=_build_flag(build, "webp_keep_original", path),
        ),
        theme=DocsThemeConfig(
            source=_text(theme, "source", DEFAULT_THEME_SOURCE),
            color=_theme_color(theme, path),
        ),
        labels=_string_map(data, path, "labels"),
        group_titles=_string_map(data, path, "group_titles"),
        icons=_string_map(data, path, "icons"),
        category_icons=_string_map(data, path, "category_icons"),
        assets=_string_map(data, path, "assets"),
        locales=locales,
        footer=_footer_config(data, path),
        deploy=dict(deploy),
    )


def _read_config_document(path: Path) -> dict[str, Any]:
    try:
        if path.suffix.lower() == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _merge_config(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(base.get(key), Mapping):
            base[key] = _merge_config(dict(base[key]), value)
        else:
            base[key] = value
    return base


def read_command_prefix(root: Path) -> str:
    """读取实例核心配置里的首个命令前缀。

    核心配置缺失、无法解析或没有可用的前缀时返回空串：文档站点照常构建，用法行不带前缀。
    先读 ``config/global`` 中的默认层，再由 ``config/config.toml`` 覆盖。

    :param root: 实例根。
    :return: 首个命令前缀。
    """
    directory = Path(root) / "config"
    data: dict[str, Any] = {}
    for path in (directory / "global" / "config.global.toml", directory / "global" / "config.global.json"):
        data = _merge_config(data, _read_config_document(path))
    data = _merge_config(data, _read_config_document(Path(root) / CORE_CONFIG_FILENAME))
    core = data.get("config")
    if not isinstance(core, Mapping):
        return ""
    prefixes = core.get("command_prefix")
    if not isinstance(prefixes, list):
        return ""
    for prefix in prefixes:
        if isinstance(prefix, str) and prefix.strip():
            return prefix.strip()
    return ""


def _footer_config(data: Mapping[str, Any], path: Path) -> DocsFooterConfig:
    section = data.get("footer")
    if section is None:
        return DocsFooterConfig()
    if not isinstance(section, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason="[footer] is not a table")
    return DocsFooterConfig(
        enabled=_footer_bool(section, "enabled", path),
        title=_text(section, "title", "").strip(),
        text=_footer_text(section, path),
        image=_text(section, "image", "").strip(),
        links=_footer_links(section, path),
        copyright=_text(section, "copyright", "").strip(),
    )


def _merge_footer(configured: DocsFooterConfig, defaults: DocsFooterConfig) -> DocsFooterConfig:
    # 正文与按钮区分“未配置”和“配置为空”，空元组表示有意不显示该类内容。
    return DocsFooterConfig(
        enabled=configured.enabled,
        title=configured.title or defaults.title,
        text=defaults.text if configured.text is None else configured.text,
        image=configured.image or defaults.image,
        links=defaults.links if configured.links is None else configured.links,
        copyright=configured.copyright or defaults.copyright,
    )


def _footer_bool(data: Mapping[str, Any], name: str, path: Path) -> bool:
    value = data.get(name)
    if value is None:
        return True
    if not isinstance(value, bool):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"[footer] {name} must be a boolean")
    return value


def _footer_text(data: Mapping[str, Any], path: Path) -> tuple[str, ...] | None:
    value = data.get("text")
    if value is None:
        return None
    if isinstance(value, str):
        return (value.strip(),) if value.strip() else ()
    if not isinstance(value, list) or not all(isinstance(line, str) for line in value):
        raise DocsError(
            "cli.docs.error.bad_config",
            path=str(path),
            reason="[footer] text must be a string or an array of strings",
        )
    return tuple(line.strip() for line in value if line.strip())


def _footer_links(data: Mapping[str, Any], path: Path) -> tuple[DocsFooterLink, ...] | None:
    value = data.get("links")
    if value is None:
        return None
    if not isinstance(value, list):
        raise DocsError(
            "cli.docs.error.bad_config",
            path=str(path),
            reason="[footer] links must be an array of tables",
        )
    links: list[DocsFooterLink] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise DocsError(
                "cli.docs.error.bad_config",
                path=str(path),
                reason="[[footer.links]] must be a table",
            )
        link = _text(item, "link", "").strip()
        if not link:
            raise DocsError(
                "cli.docs.error.bad_config",
                path=str(path),
                reason="[[footer.links]] is missing link",
            )
        links.append(
            DocsFooterLink(
                text=_text(item, "text", "").strip() or link,
                link=link,
                icon=_text(item, "icon", "").strip(),
            )
        )
    return tuple(links)


def _theme_color(data: Mapping[str, Any], path: Path) -> str:
    value = _text(data, "color", "").strip()
    if value and not _COLOR_PATTERN.match(value):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason="theme.color must be #rrggbb")
    return value.lower()


def _locale_labels(data: Mapping[str, Any], path: Path) -> dict[str, str]:
    section = data.get("locales", {})
    if not isinstance(section, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason="locales is not a table")
    labels: dict[str, str] = {}
    for tag, value in section.items():
        if isinstance(value, str) and value.strip():
            labels[str(tag)] = value.strip()
            continue
        if not isinstance(value, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"locales.{tag} is not a table")
        label = value.get("label")
        if isinstance(label, str) and label.strip():
            labels[str(tag)] = label.strip()
    return labels


def _locale_config(data: Mapping[str, Any], path: Path) -> tuple[DocsLocaleConfig, ...]:
    site = _table(data, "site", path)
    tags = site.get("locales")
    configured: list[str] = []
    if tags is not None:
        if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
            raise DocsError(
                "cli.docs.error.bad_config", path=str(path), reason="site.locales must be a list of strings"
            )
        configured = [tag.strip() for tag in tags]
    tables = _table(data, "locales", path)
    known = load_defaults().locales
    missing = [tag for tag in configured if tag not in tables and tag not in known]
    if missing:
        raise DocsError(
            "cli.docs.error.bad_config",
            path=str(path),
            reason=f"locales.{missing[0]} is not defined",
        )
    entries: list[DocsLocaleConfig] = []
    for tag, value in tables.items():
        if not isinstance(value, Mapping):
            raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"locales.{tag} is not a table")
        entries.append(
            DocsLocaleConfig(
                tag=str(tag),
                label=_text(value, "label", "").strip(),
                title=_text(value, "title", "").strip(),
                labels=_string_table(value, path, "labels"),
                group_titles=_string_table(value, path, "group_titles"),
            )
        )
    if not configured:
        return ()
    by_tag = {entry.tag: entry for entry in entries}
    return tuple(by_tag.get(tag) or DocsLocaleConfig(tag=tag, label=known.get(tag, "")) for tag in configured)


def _string_table(data: Mapping[str, Any], path: Path, table: str) -> dict[str, str]:
    section = data.get(table, {})
    if not isinstance(section, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"{table} is not a table")
    values: dict[str, str] = {}
    for key, value in section.items():
        if not isinstance(value, str) or not value.strip():
            raise DocsError(
                "cli.docs.error.bad_config", path=str(path), reason=f"{table}.{key} is not a non-empty string"
            )
        values[str(key)] = value.strip()
    return values


def _string_map(data: Mapping[str, Any], path: Path, table: str) -> dict[str, str]:
    section = data.get(table, {})
    if not isinstance(section, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"{table} is not a table")
    icons: dict[str, str] = {}
    for key, value in section.items():
        if not isinstance(value, str) or not value.strip():
            raise DocsError(
                "cli.docs.error.bad_config", path=str(path), reason=f"{table}.{key} is not a non-empty string"
            )
        icons[str(key)] = value.strip()
    return icons


def _bool_map(data: Mapping[str, Any], path: Path, table: str) -> dict[str, bool]:
    section = _table(data, table, path)
    flags: dict[str, bool] = {}
    for key, value in section.items():
        if not isinstance(value, bool):
            raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"{table}.{key} is not a boolean")
        flags[str(key)] = value
    return flags


def _build_flag(data: Mapping[str, Any], name: str, path: Path) -> bool | None:
    value = data.get(name)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"[build] {name} must be a boolean")
    return value


def site_asset_path(root: Path, value: str) -> Path | None:
    """把 ``site.logo`` / ``site.favicon`` 解析成本地文件。

    URL 与站点绝对路径（``/`` 开头）返回 ``None``。相对路径必须位于实例根内且文件存在。

    :param root: 实例根。
    :param value: 配置值。
    :return: 本地文件路径，或 ``None``。
    :raises DocsError: 相对路径越出实例根或文件不存在。
    """
    text = (value or "").strip()
    if not text or _URL_PATTERN.match(text) or text.startswith("/"):
        return None
    root = Path(root).expanduser().resolve()
    path = (root / text).expanduser()
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise DocsError("cli.docs.error.unsafe_path", path=str(path))
    if not resolved.is_file():
        raise DocsError("cli.docs.error.site_asset_missing", path=str(resolved))
    return resolved


def _table(data: Mapping[str, Any], name: str, path: Path) -> Mapping[str, Any]:
    value = data.get(name)
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise DocsError("cli.docs.error.bad_config", path=str(path), reason=f"[{name}] is not a table")
    return value


def _text(data: Mapping[str, Any], name: str, default: str) -> str:
    value = data.get(name)
    return default if value is None else str(value)
