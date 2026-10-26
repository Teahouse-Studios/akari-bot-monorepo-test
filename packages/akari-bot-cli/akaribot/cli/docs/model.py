"""文档引擎的数据类型。

目录、配置与构建结果都是不可变记录：生成器与构建器只读取它们，缓存键也由这些字段推导。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

DEFAULT_ORDER = 500


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
    """

    path: str
    title: str
    order: int = DEFAULT_ORDER
    description: str = ""


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
    :param pages: 页面清单。
    :param order: 排序权重，自小到大。
    :param editable: 是否为可编辑安装。
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
    order: int = DEFAULT_ORDER
    editable: bool = False


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
