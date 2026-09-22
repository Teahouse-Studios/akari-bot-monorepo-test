"""emotes 资源包：``assets/emotes/`` 的包内落点，只暴露 :func:`emotes_dir` 定位函数。

``akaribot/assets/`` 是 PEP 420 命名空间目录，不得放 ``__init__.py``：fonts 等资源分发共用此前缀。
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

__all__ = ["emotes_dir"]


def emotes_dir() -> Path:
    """取 emotes 根目录（``common`` / ``captcha_held`` / ``typing`` 在其下）。"""
    return Path(str(files(__package__)))
