"""配置装饰器的既有导入路径。

实现位于 :mod:`akaribot.core.builtins.config.decorator`。本模块保留
``akaribot.core.config.decorator`` 下的名称，供既有调用方使用。
"""

from akaribot.core.builtins.config.decorator import (
    ConfigMeta,
    on_base_config,
    on_bot_config,
    on_config,
    on_module_config,
    process_config_class,
)

_process_class = process_config_class

__all__ = [
    "ConfigMeta",
    "_process_class",
    "on_base_config",
    "on_bot_config",
    "on_config",
    "on_module_config",
    "process_config_class",
]
