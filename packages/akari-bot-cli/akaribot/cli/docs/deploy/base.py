"""文档站点部署 provider 的公共契约。

部署分两步：先给出目标摘要供命令层确认，再按站点目录同步。失败一律抛
:class:`DocsDeployError`，由命令层把键与参数渲染成文案；凭据只从环境变量读取，
不进入命令行、日志或异常消息。
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from ..model import DocsError

Reporter = Callable[[str], None]


class DocsDeployError(DocsError):
    """部署失败；``str()`` 返回本地化键。"""


@dataclass(frozen=True)
class DeployTarget:
    """一次部署的目标摘要。

    :param provider: provider 名称。
    :param label: 展示用名称。
    :param detail: 目标说明，例如项目 ID、存储桶与前缀。
    :param destructive: 部署是否会改动或删除远端既有内容。
    """

    provider: str
    label: str
    detail: str
    destructive: bool = False


@dataclass(frozen=True)
class DeployResult:
    """一次部署的结果。

    :param ok: 是否成功。
    :param provider: provider 名称。
    :param url: 站点地址，未知时为空串。
    :param detail: 目标说明，供部署历史记录。
    :param uploaded: 上传的对象数；试运行时为计划上传数。
    :param deleted: 删除的对象数；试运行时为计划删除数。
    :param skipped: 内容未变而跳过的对象数。
    :param dry_run: 是否为试运行。
    """

    ok: bool
    provider: str
    url: str = ""
    detail: str = ""
    uploaded: int = 0
    deleted: int = 0
    skipped: int = 0
    dry_run: bool = False


class DeployProvider(Protocol):
    """部署 provider 的接口。"""

    name: str

    def plan(self, site_dir: Path) -> DeployTarget:
        """返回目标摘要，不产生任何远端写入。"""
        ...

    def deploy(
        self,
        site_dir: Path,
        *,
        dry_run: bool = False,
        delete: bool = False,
        reporter: Reporter | None = None,
    ) -> DeployResult:
        """把站点目录同步到远端。

        :param site_dir: 已构建的站点目录。
        :param dry_run: 只统计计划动作，不写入远端。
        :param delete: 删除远端在目标前缀下多余的对象。
        :param reporter: 阶段回调，取值为 ``list`` / ``link`` / ``upload`` / ``delete`` / ``deploy`` / ``done``。
        :return: 部署结果。
        :raises DocsDeployError: 凭据、配置或远端操作失败。
        """
        ...


def get_provider(
    name: str,
    config: Mapping[str, Any],
    *,
    instance_root: Path,
    runner: Any = None,
    transport: Any = None,
) -> DeployProvider:
    """按名称创建部署 provider。

    :param name: provider 名称，支持 ``vercel`` 与 ``s3``。
    :param config: ``docs.toml`` 的 ``[deploy]`` 表或对应 provider 的子表。
    :param instance_root: 实例根目录。
    :param runner: Vercel 子进程执行器，测试可注入。
    :param transport: S3 的 httpx transport，测试可注入。
    :return: 对应的 provider。
    :raises DocsDeployError: provider 名称未知。
    """
    provider = str(name or "").strip().lower()
    if provider not in {"vercel", "s3"}:
        raise DocsDeployError("cli.docs.deploy.unknown_provider", provider=name)
    table = _provider_table(config, provider)
    if provider == "vercel":
        from .vercel import VercelProvider

        return VercelProvider(table, instance_root=instance_root, runner=runner)
    from .s3 import S3Provider

    return S3Provider(table, instance_root=instance_root, transport=transport)


def _provider_table(config: Mapping[str, Any], provider: str) -> Mapping[str, Any]:
    # 命令层可以传整个 [deploy] 表，也可以只传对应子表。
    nested = config.get(provider)
    return nested if isinstance(nested, Mapping) else config
