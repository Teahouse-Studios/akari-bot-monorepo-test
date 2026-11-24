"""配置模板与既有导入路径。

配置项的存取实现位于 :mod:`akaribot.core.builtins.config`。本模块保留模板类与
``akaribot.core.config`` 下的导入路径，并在导入时完成配置加载，使既有调用方无须关心
初始化顺序。新增代码应直接使用 ``akaribot.core.builtins.config``。
"""

from akaribot.core.builtins.config import (
    ALLOWED_TYPES,
    CONFIG_READONLY,
    CFGManager,
    Config,
    ConfigManager,
    ConfigSource,
    get_source,
    set_source,
    use_source,
)
from akaribot.core.builtins.config.bootstrap import bootstrap_config
from akaribot.core.exports import add_export
from akaribot.core.utils.func import format_url

# 模板在类创建时注册字段并补充缺失键，因此加载与迁移必须先于此处的模板导入完成。
bootstrap_config()

from akaribot.core.config.base import (  # noqa: E402
    BaseConfig,
    CoreConfig,
    CoreSecretConfig,
    JobQueueConfig,
    JobQueueSecretConfig,
    S3Config,
    S3SecretConfig,
    SMTPConfig,
    SMTPSecretConfig,
    WebRenderConfig,
)

add_export(Config)
add_export(CFGManager)

__all__ = [
    "ALLOWED_TYPES",
    "BaseConfig",
    "CFGManager",
    "CONFIG_READONLY",
    "Config",
    "ConfigManager",
    "ConfigSource",
    "CoreConfig",
    "CoreSecretConfig",
    "JobQueueConfig",
    "JobQueueSecretConfig",
    "S3Config",
    "S3SecretConfig",
    "SMTPConfig",
    "SMTPSecretConfig",
    "WebRenderConfig",
    "bootstrap_config",
    "format_url",
    "get_source",
    "set_source",
    "use_source",
]
