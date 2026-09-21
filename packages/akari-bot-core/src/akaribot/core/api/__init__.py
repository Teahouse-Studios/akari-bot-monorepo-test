"""模块作者的公共 API 门面。

模块包依赖本模块，而不是 ``core.builtins.bot`` 这类内部路径：core 内部模块在拆包与后续重构中
可以自由移动，模块侧的 import 保持不变。平台适配器另有 :mod:`core.api.adapters` 收录只有适配器
会用的设施。

具体导入集中在 :mod:`core.api.base`，本模块只做转发。导入期不依赖实例配置：``core.api.base``
的导入块在配置缺失时会整体中断，未绑定的名字由本模块的 ``__getattr__`` 在首次访问时重试，因此
CLI 与发现层可以在配置就绪之前安全地 import 本模块并读取 ``__api_version__``。
"""

from __future__ import annotations

from typing import Any

from akaribot.core.api import base as _base
from akaribot.core.constants.exceptions import ConfigFileNotFound
from akaribot.core.registry import CORE_API_VERSION

# 与发现层共用同一常量：registry 的 requires_core_api 闸门据此校验包兼容性。方向必须是
# core.api 依赖 core.registry —— registry 被 core.component 等模块在导入期引用，反向依赖会成环。
__api_version__ = CORE_API_VERSION

__all__ = ["__api_version__", *_base.__all__]

try:
    # 复制 base 已解析的名字。配置缺失时该导入会在中途中断，其余名字留给 __getattr__。
    from akaribot.core.api.base import *
except ConfigFileNotFound:
    pass


def __getattr__(name: str) -> Any:
    """转发到实现模块，使配置缺失时未绑定的名字在首次访问时重试。

    :param name: 门面名字。
    :return: 名字对应的对象。
    :raises AttributeError: 该名字不在门面承诺的清单内。
    """
    return getattr(_base, name)
