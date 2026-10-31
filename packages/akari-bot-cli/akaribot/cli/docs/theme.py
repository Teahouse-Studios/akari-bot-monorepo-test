"""文档主题清单与解析。

引擎只读取主题清单、复制主题目录并生成 VitePress 配置，不导入主题代码。主题可以是 CLI 内置的
最小主题，也可以是与项目解耦的外部模板；两者都通过根目录的 ``docs-theme.json`` 描述依赖、入口与
VitePress 版本。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import DocsConfig
from .model import DocsError

THEME_FILENAME = "docs-theme.json"
TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
THEME_ENV = "AKARIBOT_DOCS_THEME"
BUNDLED_SOURCE = "bundled"
AUTO_SOURCE = "auto"
DEFAULT_NODE_MAJOR = 18
DEFAULT_VITEPRESS_VERSION = "1.6.4"
DEFAULT_THEME_DIR = "theme"
EXTERNAL_THEME_DIR = "docs/.vitepress/theme"
_NODE_MAJOR_PATTERN = re.compile(r"(\d+)")
_THEME_DEPS = ("vitepress", "vue", "markdown-it-image-size", "minisearch")


@dataclass(frozen=True)
class ThemeSpec:
    """一个可用于生成站点的主题。

    :param name: 主题名。
    :param version: 主题版本，用于构建指纹。
    :param source: 解析来源，``bundled``、``file:…`` 或 ``auto:…``。
    :param root: 主题所在目录；内置主题为 CLI 模板目录。
    :param theme_dir: 复制到生成站点 ``.vitepress/theme`` 的目录。
    :param package_dir: 含 ``package.json`` 与 ``package-lock.json`` 的目录；外部主题可为 ``None``。
    :param vitepress_version: 该主题要求的 VitePress 版本。
    :param node_major: 运行该主题所需的 Node 主版本。
    :param dependencies: 外部主题需要安装的 npm 依赖。
    :param install_mode: ``ci`` 或 ``install``。
    :param config: 生成配置时使用的主题声明。
    :param digest: 主题版本、依赖与目录内容的摘要。
    """

    name: str
    version: str
    source: str
    root: Path
    theme_dir: Path
    package_dir: Path | None
    vitepress_version: str
    node_major: int
    dependencies: Mapping[str, str] = field(default_factory=dict)
    install_mode: str = "install"
    config: Mapping[str, Any] = field(default_factory=dict)
    digest: str = ""

    @property
    def is_bundled(self) -> bool:
        """是否为 CLI 内置主题。"""
        return self.install_mode == "ci" and self.source == BUNDLED_SOURCE


def resolve_theme(config: DocsConfig, *, environ: Mapping[str, str] | None = None) -> ThemeSpec:
    """按配置、环境变量与实例目录解析主题。

    解析顺序：``AKARIBOT_DOCS_THEME`` > ``docs.toml`` 的 ``[theme].source``。``auto`` 在实例根查找
    ``akari-bot-docs-template``、``vendor/akari-bot-docs-template`` 与 ``docs-theme``；从仓库源码
    运行时还会查找仓库内的 ``vendor/akari-bot-docs-template`` submodule。都找不到时使用内置主题。

    :param config: 实例文档配置。
    :param environ: 环境变量；缺省读取进程环境。
    :return: 解析后的主题。
    :raises DocsError: 外部主题路径不存在或清单无效。
    """
    source = str((environ or os.environ).get(THEME_ENV) or config.theme.source or AUTO_SOURCE).strip()
    if source == BUNDLED_SOURCE:
        return bundled_theme()
    if source == AUTO_SOURCE:
        for candidate in _auto_candidates(config.root):
            if _looks_like_theme(candidate):
                return _external_theme(candidate, source=f"auto:{candidate}")
        return bundled_theme()
    if source.startswith("file:"):
        path = Path(source[len("file:") :]).expanduser()
        if not path.is_absolute():
            path = config.root / path
        return _external_theme(path, source=source)
    if "://" in source:
        raise DocsError("cli.docs.error.theme_unsupported", source=source)
    if source.startswith(("/", "./", "../", "~")) or os.sep in source or (os.altsep and os.altsep in source):
        path = Path(source).expanduser()
        if not path.is_absolute():
            path = config.root / path
        return _external_theme(path, source=source)
    candidate = config.root / source
    if _looks_like_theme(candidate):
        return _external_theme(candidate, source=source)
    raise DocsError("cli.docs.error.theme_unsupported", source=source)


def bundled_theme(root: Path = TEMPLATE_DIR) -> ThemeSpec:
    """读取 CLI 内置主题清单；清单缺失时使用默认值。

    :param root: 内置模板目录。
    :return: 内置主题。
    """
    return _theme_from_root(Path(root), source=BUNDLED_SOURCE, bundled=True)


def _auto_candidates(root: Path) -> list[Path]:
    # 实例根优先；从源码检出运行 CLI 时，再找仓库内 vendor/ 下的模板 submodule。
    candidates = [
        root / "akari-bot-docs-template",
        root / "vendor" / "akari-bot-docs-template",
        root / "docs-theme",
    ]
    for parent in Path(__file__).resolve().parents:
        if (parent / "packages" / "akari-bot-cli" / "pyproject.toml").is_file():
            candidates.append(parent / "vendor" / "akari-bot-docs-template")
            candidates.append(parent / "akari-bot-docs-template")
            break
    return [candidate.expanduser() for candidate in candidates]


def _looks_like_theme(root: Path) -> bool:
    return (root / THEME_FILENAME).is_file() or (
        (root / "package.json").is_file()
        and ((root / EXTERNAL_THEME_DIR).is_dir() or (root / DEFAULT_THEME_DIR).is_dir())
    )


def _external_theme(root: Path, *, source: str) -> ThemeSpec:
    root = Path(root).expanduser().resolve()
    if not root.is_dir() or not _looks_like_theme(root):
        raise DocsError("cli.docs.error.theme_missing", source=source, path=str(root))
    return _theme_from_root(root, source=source, bundled=False)


def _theme_from_root(root: Path, *, source: str, bundled: bool) -> ThemeSpec:
    manifest = _load_manifest(root, bundled=bundled)
    theme_dir = _inside(root, str(manifest.get("theme_dir") or (DEFAULT_THEME_DIR if bundled else EXTERNAL_THEME_DIR)))
    if not theme_dir.is_dir():
        raise DocsError("cli.docs.error.theme_invalid", source=source, path=str(theme_dir), reason="theme_dir")
    package_dir = _inside(root, str(manifest.get("package_dir") or "."))
    vitepress_version = str(manifest.get("vitepress") or DEFAULT_VITEPRESS_VERSION)
    node_major = _node_major(str(manifest.get("node") or f">={DEFAULT_NODE_MAJOR}"))
    dependencies = dict(manifest.get("dependencies") or {})
    dependencies.setdefault("vitepress", vitepress_version)
    install_mode = str(manifest.get("install_mode") or ("ci" if bundled else "install"))
    config = dict(manifest.get("config") or {})
    version = str(manifest.get("version") or "")
    digest = _theme_digest(root, theme_dir, manifest)
    return ThemeSpec(
        name=str(manifest.get("name") or ("bundled" if bundled else root.name)),
        version=version,
        source=source,
        root=root,
        theme_dir=theme_dir,
        package_dir=package_dir if package_dir.is_dir() else None,
        vitepress_version=vitepress_version,
        node_major=node_major,
        dependencies=dependencies,
        install_mode=install_mode,
        config=config,
        digest=digest,
    )


def _load_manifest(root: Path, *, bundled: bool) -> dict[str, Any]:
    path = root / THEME_FILENAME
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DocsError("cli.docs.error.theme_invalid", source=str(root), path=str(path), reason=str(exc)) from exc
        if not isinstance(data, Mapping):
            raise DocsError("cli.docs.error.theme_invalid", source=str(root), path=str(path), reason="manifest")
        if data.get("schema") != 1:
            raise DocsError(
                "cli.docs.error.theme_invalid",
                source=str(root),
                path=str(path),
                reason=f"schema {data.get('schema')}",
            )
        return dict(data)
    package_path = root / "package.json"
    if not package_path.is_file():
        if bundled:
            return {
                "name": "bundled",
                "version": "1.0.0",
                "theme_dir": DEFAULT_THEME_DIR,
                "package_dir": ".",
                "vitepress": DEFAULT_VITEPRESS_VERSION,
                "node": f">={DEFAULT_NODE_MAJOR}",
                "install_mode": "ci",
                "config": {"search": {"provider": "local"}},
            }
        raise DocsError("cli.docs.error.theme_missing", source=str(root), path=str(root))
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DocsError(
            "cli.docs.error.theme_invalid", source=str(root), path=str(package_path), reason=str(exc)
        ) from exc
    if not isinstance(package, Mapping):
        raise DocsError("cli.docs.error.theme_invalid", source=str(root), path=str(package_path), reason="package")
    dependencies = {}
    for table_name in ("dependencies", "devDependencies"):
        table = package.get(table_name)
        if isinstance(table, Mapping):
            for name, version in table.items():
                if name in _THEME_DEPS:
                    dependencies[str(name)] = str(version)
    return {
        "name": package.get("name"),
        "version": package.get("version"),
        "theme_dir": DEFAULT_THEME_DIR if bundled else EXTERNAL_THEME_DIR,
        "package_dir": ".",
        "vitepress": (package.get("devDependencies") or {}).get("vitepress")
        or (package.get("dependencies") or {}).get("vitepress")
        or DEFAULT_VITEPRESS_VERSION,
        "node": (package.get("engines") or {}).get("node") or f">={DEFAULT_NODE_MAJOR}",
        "install_mode": "ci" if bundled else "install",
        "dependencies": dependencies,
        "config": {} if not bundled else {"search": {"provider": "local"}},
    }


def _inside(root: Path, relative: str) -> Path:
    path = (root / relative).expanduser().resolve()
    if path != root and not path.is_relative_to(root):
        raise DocsError("cli.docs.error.theme_invalid", source=str(root), path=str(path), reason="outside theme root")
    return path


def _node_major(requirement: str) -> int:
    match = _NODE_MAJOR_PATTERN.search(requirement or "")
    return int(match.group(1)) if match else DEFAULT_NODE_MAJOR


def _theme_digest(root: Path, theme_dir: Path, manifest: Mapping[str, Any]) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(dict(manifest), ensure_ascii=False, sort_keys=True).encode("utf-8"))
    for path in sorted(theme_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        digest.update(f"{relative}\0".encode("utf-8"))
        digest.update(_file_digest(path))
    for name in ("package.json", "package-lock.json"):
        path = root / name
        if path.is_file():
            digest.update(f"{name}\0".encode("utf-8"))
            digest.update(_file_digest(path))
    return digest.hexdigest()


def _file_digest(path: Path) -> bytes:
    try:
        with path.open("rb") as handle:
            return hashlib.file_digest(handle, "sha256").digest()
    except OSError:
        return b"\0unreadable"
