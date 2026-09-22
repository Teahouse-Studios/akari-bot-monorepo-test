"""brand 资源包：``assets/brand/`` 的包内落点，只暴露 :func:`brand_dir` 定位函数。

``akaribot/assets/`` 是 PEP 420 命名空间目录，不得放 ``__init__.py``：fonts、emotes 等资源分发
共用此前缀。

本包放的是**不可再生成的品牌资产**：角色立绘 ``character_marked.png``、标志
``akaribot_logo.png``、制作人员名单 ``credits.txt``。它们由画师提供并保留全部权利（见同目录
LICENSE），既不属于可重新导出的构建产物，也不得为压体积而重新编码——立绘被降采样过一次，
用户一眼就看出糊了。需要控制体积时应当调整使用侧（如展示宽度），而不是改这些文件本身。
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

__all__ = ["brand_dir"]


def brand_dir() -> Path:
    """取 brand 资源根目录（立绘、标志、名单都在其下）。"""
    return Path(str(files(__package__)))
