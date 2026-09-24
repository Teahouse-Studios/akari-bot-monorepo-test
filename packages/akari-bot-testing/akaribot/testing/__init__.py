"""测试框架的公开面。

本模块刻意不静态导入任何 core 模块：测试配置与合并日志目录的隔离发生在
:mod:`akaribot.testing.runner` 的导入期，而 ``python -m akaribot.testing`` 会先执行本模块。
若这里直接导入 ``.tester``（它依赖 ``core.logger``），core 会抢在隔离环境变量就位之前被导入，
``core.constants.path`` 便把合并日志等路径固化到仓库目录。故公开名一律在首次访问时解析。

本模块自身的辅助名一律以下划线开头：公开名由子模块并入，命名冲突会静默遮住框架的公开 API
（例如 ``typing.Any`` 遮住 ``expectations.Any`` 匹配器）。
"""

from __future__ import annotations

from importlib import import_module as _import_module
from importlib.util import find_spec as _find_spec
from typing import Any as _Any

_SUBMODULES = ("decorator", "expectations", "tester", "timing")


def _load() -> None:
    for name in _SUBMODULES:
        module = _import_module(f"{__name__}.{name}")
        exported = getattr(module, "__all__", None) or [key for key in vars(module) if not key.startswith("_")]
        for key in exported:
            globals()[key] = getattr(module, key)


def __getattr__(name: str) -> _Any:
    """
    首次访问时解析公开名。

        子模块名直接返回子模块本身，避免为取 ``runner`` 而先加载 ``tester``（后者依赖 core，
        会把路径固化在隔离环境变量就位之前）。

        :param name: 属性名。
        :return: 对应的对象。
        :raises AttributeError: 该名字不在任何子模块的公开面内。
    """
    # 子模块名直接返回子模块本身，避免为取 ``runner`` 而先加载 ``tester``（后者依赖 core，
    # 会把路径固化在隔离环境变量就位之前）。
    if not name.startswith("_") and _find_spec(f"{__name__}.{name}") is not None:
        return _import_module(f"{__name__}.{name}")
    _load()
    try:
        return globals()[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def __dir__() -> list[str]:
    """
    列出公开名，供交互式补全与文档工具使用。
    """
    _load()
    return sorted(key for key in globals() if not key.startswith("_"))
