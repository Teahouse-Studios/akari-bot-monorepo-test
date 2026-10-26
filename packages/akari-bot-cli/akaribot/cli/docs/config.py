"""``docs.toml`` 的读取与默认值。

配置只读不写：站点标题、语言、部署基路径与输出目录都由实例维护者提供，文档引擎不代写。
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .model import DocsError

CONFIG_FILENAME = "docs.toml"
DEFAULT_TITLE = "AkariBot 文档"
DEFAULT_LANG = "zh-CN"
DEFAULT_BASE = "/"
DEFAULT_OUT_DIR = "cache/docs/site"
BASE_ENV = "AKARIBOT_DOCS_BASE"


@dataclass(frozen=True)
class DocsSiteConfig:
    """站点展示设置。

    :param title: 站点标题。
    :param lang: 页面语言标签。
    :param base: 部署基路径。
    """

    title: str = DEFAULT_TITLE
    lang: str = DEFAULT_LANG
    base: str = DEFAULT_BASE


@dataclass(frozen=True)
class DocsBuildConfig:
    """构建输出设置。

    :param out_dir: 输出目录，相对实例根或绝对路径。
    """

    out_dir: str = DEFAULT_OUT_DIR


@dataclass(frozen=True)
class DocsConfig:
    """实例的文档配置。

    :param root: 实例根目录。
    :param site: 站点展示设置。
    :param build: 构建输出设置。
    :param deploy: 部署设置，由命令层解释，引擎只透传。
    """

    root: Path
    site: DocsSiteConfig = field(default_factory=DocsSiteConfig)
    build: DocsBuildConfig = field(default_factory=DocsBuildConfig)
    deploy: Mapping[str, Any] = field(default_factory=dict)

    @property
    def cache_docs_dir(self) -> Path:
        """生成器与工具链共用的缓存目录 ``<实例根>/cache/docs``。"""
        return self.root / "cache" / "docs"

    @property
    def out_dir(self) -> Path:
        """输出目录的绝对路径；配置为相对路径时锚定实例根。"""
        configured = Path(self.build.out_dir).expanduser()
        return configured if configured.is_absolute() else self.root / configured

    @property
    def base(self) -> str:
        """当前生效的基路径，环境变量优先于配置文件。"""
        return normalize_base(os.environ.get(BASE_ENV) or self.site.base)


def normalize_base(value: str) -> str:
    """把基路径规范成以 ``/`` 开头并结尾的形式。"""
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
    deploy = _table(data, "deploy", path)
    return DocsConfig(
        root=root,
        site=DocsSiteConfig(
            title=_text(site, "title", DEFAULT_TITLE),
            lang=_text(site, "lang", DEFAULT_LANG),
            base=_text(site, "base", DEFAULT_BASE),
        ),
        build=DocsBuildConfig(out_dir=_text(build, "out_dir", DEFAULT_OUT_DIR)),
        deploy=dict(deploy),
    )


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
