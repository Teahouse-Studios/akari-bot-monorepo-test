"""构建编排：目录 → 配置 → 工具链 → 生成 → VitePress。

构建指纹覆盖所选文档内容、模板版本、VitePress 版本与基路径；指纹未变且输出仍在时直接复用，
避免每次预览都重跑一次完整构建。
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable, Sequence

from .catalog import load_catalog
from .config import DocsConfig, load_config
from .generator import collect_files, generate
from .model import BuildResult, DocCatalog, DocsError
from .state import load_state, save_build_state
from .toolchain import TEMPLATE_DIR, VITEPRESS_VERSION, detect, ensure_toolchain, run_build, template_version

Reporter = Callable[[str], None]


def build(
    instance: Any,
    keys: Sequence[str] | None = None,
    force: bool = False,
    offline: bool = False,
    reporter: Reporter | None = None,
) -> BuildResult:
    """构建实例的文档站点。

    :param instance: 带 ``root`` 与 ``run_core_capture`` 的实例。
    :param keys: 只构建这些包；``None`` 表示全部。
    :param force: 为真时忽略指纹与既有输出。
    :param offline: 为真时禁止安装 Node 依赖。
    :param reporter: 阶段回调，参数为 ``toolchain`` / ``generate`` / ``build`` / ``done``。
    :return: 构建结果。
    :raises DocsError: 目录过滤失败、工具链不可用或构建失败。
    """
    started = time.monotonic()
    notify = reporter or _ignore
    catalog = load_catalog(instance)
    full_catalog = catalog
    if keys:
        catalog = catalog.select(keys)
    config = load_config(instance)
    out_dir = config.out_dir
    fingerprint = fingerprint_catalog(catalog, config)

    previous = (load_state(instance).get("build") or {}).get("fingerprint")
    if not force and previous == fingerprint and (out_dir / "index.html").is_file():
        return BuildResult(
            out_dir=out_dir,
            packages=catalog.keys(),
            fingerprint=fingerprint,
            reused=True,
            duration_ms=_elapsed_ms(started),
        )

    toolchain = detect()
    if not toolchain.ready:
        raise DocsError("cli.docs.error.toolchain_missing", detail=toolchain.detail)

    notify("toolchain")
    cache_dir = Path(instance.root) / "cache"
    docs_dir = ensure_toolchain(cache_dir, TEMPLATE_DIR, offline=offline)
    notify("generate")
    src_dir = config.cache_docs_dir / "src"
    generate(catalog, src_dir, config, link_packages=full_catalog.packages)
    notify("build")
    log = run_build(docs_dir, src_dir, out_dir)
    if not (out_dir / "index.html").is_file():
        raise DocsError("cli.docs.error.build_failed", reason="index.html is missing after build", path=str(out_dir))
    save_build_state(
        instance,
        fingerprint=fingerprint,
        packages=catalog.keys(),
        out_dir=out_dir,
        base=config.base,
    )
    notify("done")
    return BuildResult(
        out_dir=out_dir,
        packages=catalog.keys(),
        fingerprint=fingerprint,
        reused=False,
        duration_ms=_elapsed_ms(started),
        log=log,
    )


def fingerprint_catalog(catalog: DocCatalog, config: DocsConfig) -> str:
    """计算构建输入指纹。

    文档文件按内容参与摘要，因此改写页面、增删图片或调整基路径都会触发重建。
    """
    digest = hashlib.sha256()
    head = {
        "schema": 1,
        "template": template_version(TEMPLATE_DIR),
        "vitepress": VITEPRESS_VERSION,
        "base": config.base,
        "title": config.site.title,
        "lang": config.site.lang,
    }
    digest.update(json.dumps(head, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    for package in sorted(catalog.packages, key=lambda item: item.key):
        digest.update(f"package\0{package.key}\0{package.version}\0{package.title}\n".encode("utf-8"))
        meta_path = package.doc_path / "doc.toml"
        if meta_path.is_file():
            digest.update(b"meta\0")
            digest.update(_file_digest(meta_path))
        for relative, path in collect_files(package.doc_path):
            digest.update(f"file\0{relative}\0".encode("utf-8"))
            digest.update(_file_digest(path))
    return digest.hexdigest()


def _file_digest(path: Path) -> bytes:
    try:
        with path.open("rb") as handle:
            return hashlib.file_digest(handle, "sha256").digest()
    except OSError as exc:
        raise DocsError("cli.docs.error.missing_page", path=str(path), reason=str(exc)) from exc


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _ignore(_: str) -> None:
    return None
