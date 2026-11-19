"""文档站点部署 provider。

命令层经 :func:`get_provider` 取得实现，只处理 :class:`DeployTarget` 与
:class:`DeployResult`；provider 抛出的 :class:`DocsDeployError` 携带本地化键与参数。
"""

from .base import (
    DeployProvider,
    DeployResult,
    DeployTarget,
    DocsDeployError,
    Reporter,
    get_provider,
)

__all__ = [
    "DeployProvider",
    "DeployResult",
    "DeployTarget",
    "DocsDeployError",
    "Reporter",
    "get_provider",
]
