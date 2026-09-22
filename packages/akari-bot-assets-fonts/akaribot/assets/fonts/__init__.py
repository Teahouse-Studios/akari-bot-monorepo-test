"""fonts 资源包：``assets/fonts/`` 的包内落点，只暴露 :func:`fonts_dir` 定位函数。

``akaribot/assets/`` 是 PEP 420 命名空间目录，不得放 ``__init__.py``：emotes 等资源分发共用此前缀。
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

__all__ = ["fonts_dir"]


def fonts_dir() -> Path:
    """取字体目录（Noto Sans CJK 与 Noto Sans Symbols2 在其下）。"""
    return Path(str(files(__package__)))
