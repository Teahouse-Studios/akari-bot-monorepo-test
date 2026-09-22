"""表外基础配置及历史导入路径兼容层。"""

from akaribot.core.config.decorator import on_base_config
from akaribot.core.constants.default import default_locale as default_locale_default
from akaribot.core.constants.version import config_version as config_version_default


# 位于 config.toml 中任何表之外的顶层键值对。它们在首次运行时由 bot.py 写出骨架，
# 并由 akaribot/core/config/update.py 的版本迁移维护，声明在此仅为提供一个带类型的读取入口。
@on_base_config()
class BaseConfig:
    default_locale: str = default_locale_default
    config_version: int = config_version_default


# 保留既有导入路径
from akaribot.core.config.core import CoreConfig, CoreSecretConfig
from akaribot.core.config.jobqueue import JobQueueConfig, JobQueueSecretConfig
from akaribot.core.config.s3 import S3Config, S3SecretConfig
from akaribot.core.config.smtp import SMTPConfig, SMTPSecretConfig
from akaribot.core.config.webrender import WebRenderConfig

__all__ = [
    "BaseConfig",
    "CoreConfig",
    "CoreSecretConfig",
    "JobQueueConfig",
    "JobQueueSecretConfig",
    "S3Config",
    "S3SecretConfig",
    "SMTPConfig",
    "SMTPSecretConfig",
    "WebRenderConfig",
]
