"""品牌资产定位：``akari-bot-assets-brand`` 资源包 → 实例 ``assets/`` → 无。

立绘、标志与制作人员名单原先散在仓库根 ``assets/`` 与 core 包内，部署形态下经常取不到；现在由
独立的资源包分发，但**实例目录仍要能覆盖**：部署者换一张自己的标志是合理需求，且旧实例的
``assets/`` 里可能已经放着这些文件。故按上述顺序查找，任一级命中即用，都没有时返回 ``None``
由调用方决定降级方式——``~about`` 少一张图不该让整条命令失败。
"""

from __future__ import annotations

from pathlib import Path

from akaribot.core.paths import Paths

BRAND_PACKAGE = "akaribot.assets.brand"


def _package_brand_dir() -> Path | None:
    """取品牌资源包目录；未安装该资源包时返回 ``None``。"""
    try:
        module = __import__(BRAND_PACKAGE, fromlist=["brand_dir"])
    except ImportError:
        return None
    directory = Path(str(module.brand_dir()))
    return directory if directory.is_dir() else None


def find_brand_asset(name: str) -> Path | None:
    """按「资源包 → 实例 assets」的顺序定位品牌资产。

    :param name: 文件名，如 ``character_marked.png``。
    :return: 存在的文件路径；两处都没有时为 ``None``。
    """
    directory = _package_brand_dir()
    if directory is not None:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    fallback = Paths.assets / name
    return fallback if fallback.is_file() else None
