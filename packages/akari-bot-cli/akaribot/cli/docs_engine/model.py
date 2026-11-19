"""文档引擎的数据类型。

目录、配置与构建结果都是不可变记录：生成器与构建器只读取它们，缓存键也由这些字段推导。
"""

from __future__ import annotations

import json
import tomllib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

DEFAULT_ORDER = 500
DOC_META_GLOBAL_DIR = Path("config") / "global"
DOC_META_GLOBAL_FILES = (DOC_META_GLOBAL_DIR / "docs.global.toml", DOC_META_GLOBAL_DIR / "docs.global.json")
DOC_META_USER_FILES = (Path("config") / "docs.toml", Path("config") / "docs.json")
DOC_META_LEGACY_FILES = (Path("doc.toml"), Path("doc.json"))


def _existing(doc_path: Path, paths: Iterable[Path]) -> tuple[Path, ...]:
    return tuple(path for path in (doc_path / item for item in paths) if path.is_file())


def doc_meta_paths(doc_path: Path) -> tuple[Path, ...]:
    """返回参与合并的文档元数据文件，按全局、用户覆盖、旧布局的顺序。"""
    global_files = _existing(doc_path, DOC_META_GLOBAL_FILES)
    user_files = _existing(doc_path, DOC_META_USER_FILES)
    if global_files or user_files:
        return global_files + user_files
    return _existing(doc_path, DOC_META_LEGACY_FILES)


def doc_meta_path(doc_path: Path) -> Path:
    """返回用于文件指纹与提示的元数据文件；没有文件时返回全局默认路径。"""
    paths = doc_meta_paths(doc_path)
    if paths:
        return paths[-1]
    return doc_path / DOC_META_GLOBAL_FILES[0]


def _read_file(path: Path) -> Mapping[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
    else:
        payload = tomllib.loads(text)
    return payload if isinstance(payload, Mapping) else {}


def _merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = _merge(current, value)
        else:
            merged[key] = value
    return merged


def read_doc_meta(doc_path: Path) -> Mapping[str, Any]:
    """读取并合并全局默认与用户覆盖；解析失败时跳过对应文件。"""
    merged: dict[str, Any] = {}
    for path in doc_meta_paths(doc_path):
        try:
            payload = _read_file(path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
            continue
        merged = _merge(merged, payload)
    return merged


class DocsError(Exception):
    """面向用户的文档引擎失败。

    :param key: 本地化键，由命令层渲染成文案。
    :param params: 文案插值参数。
    """

    def __init__(self, key: str, /, **params: Any) -> None:
        super().__init__(key)
        self.key = key
        self.params: dict[str, Any] = params

    def __str__(self) -> str:
        return self.key


@dataclass(frozen=True)
class DocPage:
    """一个文档页面。

    :param path: 相对包文档目录的路径，以 ``.md`` 结尾。
    :param title: 侧栏与索引里显示的标题。
    :param order: 排序权重，自小到大。
    :param description: 一句话说明，可为空。
    :param submenu: 侧栏子菜单名，空串表示直接列在包下。
    """

    path: str
    title: str
    order: int = DEFAULT_ORDER
    description: str = ""
    submenu: str = ""


@dataclass(frozen=True)
class DocPackage:
    """一个提供文档的已装包。

    :param key: URL 与目录名使用的唯一短名。
    :param group: 分组，决定导航与分组页面。
    :param dist: 分发名。
    :param name: 包短名。
    :param version: 已装版本。
    :param title: 展示标题。
    :param summary: 一句话简介。
    :param doc_path: 包内文档目录。
    :param logo: 该包声明给文档站点使用的日间标志文件，未声明时为空串。
    :param logo_dark: 该包声明给文档站点使用的夜间标志文件，未声明时为空串。
    :param avatar: 该包声明给对话示例使用的机器人头像，未声明时为空串。
    :param character: 该包声明的角色立绘，未声明时为空串。
    :param credits: 该包声明的制作人员名单文件，未声明时为空串。
    :param brand: 是否为品牌资源提供者；构建时只取第一个提供者。
    :param pages: 页面清单。
    :param order: 排序权重，自小到大。
    :param editable: 是否为可编辑安装。
    :param category: 侧栏分类，空串表示不分类。
    :param category_order: 分类在侧栏中的排序权重，自小到大。
    :param overview: 是否生成包级概览页；为假时包只作为页面容器。
    """

    key: str
    group: str
    dist: str
    name: str
    version: str
    title: str
    summary: str
    doc_path: Path
    pages: tuple[DocPage, ...]
    logo: str = ""
    logo_dark: str = ""
    avatar: str = ""
    character: str = ""
    credits: str = ""
    brand: bool = False
    order: int = DEFAULT_ORDER
    editable: bool = False
    category: str = ""
    category_order: int = DEFAULT_ORDER
    overview: bool = True


@dataclass(frozen=True)
class DocCatalog:
    """一次文档构建可用的全部包。

    :param packages: 已排序的包清单。
    :param warnings: 目录构建期间的降级说明，供命令层原样展示。
    """

    packages: tuple[DocPackage, ...]
    warnings: tuple[str, ...] = ()

    def keys(self) -> tuple[str, ...]:
        """返回全部包的 key，顺序与 :attr:`packages` 一致。"""
        return tuple(package.key for package in self.packages)

    def select(self, keys: Sequence[str] | None) -> DocCatalog:
        """按 key 过滤目录，保持目录原有顺序。

        :param keys: 需要的 key；``None`` 或空序列表示全选。
        :return: 过滤后的目录，警告原样保留。
        :raises DocsError: ``keys`` 含目录里没有的 key。
        """
        if not keys:
            return self
        wanted = [str(key).strip() for key in keys if str(key).strip()]
        known = {package.key for package in self.packages}
        missing = [key for key in wanted if key not in known]
        if missing:
            raise DocsError("cli.docs.error.unknown_key", key=missing[0], keys=", ".join(missing))
        selected = set(wanted)
        return DocCatalog(
            packages=tuple(package for package in self.packages if package.key in selected), warnings=self.warnings
        )


@dataclass(frozen=True)
class ToolchainInfo:
    """Node 与 npm 的探测结果。

    :param node: node 可执行文件路径，找不到时为空串。
    :param npm: npm 可执行文件路径，找不到时为空串。
    :param node_version: node 版本，找不到时为空串。
    :param npm_version: npm 版本，找不到时为空串。
    :param ready: 是否满足构建要求。
    :param detail: 版本摘要或不可用的原因。
    """

    node: str
    npm: str
    node_version: str
    npm_version: str
    ready: bool
    detail: str = ""


@dataclass(frozen=True)
class BuildResult:
    """一次构建的结果。

    :param out_dir: 站点输出目录。
    :param packages: 参与构建的包 key。
    :param fingerprint: 输入指纹，相同指纹可直接复用输出。
    :param reused: 是否复用了上一次输出。
    :param duration_ms: 本次耗时，毫秒。
    :param log: 构建器输出尾部，复用时为空串。
    """

    out_dir: Path
    packages: tuple[str, ...]
    fingerprint: str
    reused: bool
    duration_ms: int
    log: str = ""


def page_url(key: str, path: str) -> str:
    """把包内页面路径折算成站点 URL。

    站点开启 ``cleanUrls``，页面文件 ``a.md`` 对应 ``/a``；``index.md`` 对应包的目录首页。
    """
    normalized = path.replace("\\", "/").strip("/")
    if normalized == "index.md":
        return f"/{key}/"
    if normalized.endswith("/index.md"):
        return f"/{key}/{normalized[: -len('/index.md')]}/"
    stem = normalized[:-3] if normalized.endswith(".md") else normalized
    return f"/{key}/{stem}"


def as_mapping(value: Any) -> Mapping[str, Any]:
    """把任意 JSON 值收窄成映射，非映射返回空字典。"""
    return value if isinstance(value, Mapping) else {}
