"""自检。

``akaribot doctor`` 的多实例三查：端口冲突、凭据重复、孤立配置（T5.7、上位文档 §3.6）。

与 T1B.4 的 daemon 前置检查共用同一份实现：优先调用 core 的 ``config conflicts`` 入口，该入口应由
``bot.py`` 的启动前检查与 CLI 同时调用，判据只有一份；入口不可用时回退到本模块的本地实现，并在输出
中标注实际使用的实现，避免两处判据悄悄分叉。推荐的 core 侧接口：

    python -m akaribot.core.entrypoints.config conflicts --json
    → {"conflicts": [{"kind": "port" | "credential" | "orphan" | "config",
                      "level": "error" | "warning",
                      "platform": "telegram",
                      "instances": ["bot_telegram", "bot_telegram-alt"],
                      "message": "…",
                      "detail": {…}}]}

本地判据与 core 一致：只比较已启用实例；凭据比较限定同平台、由 manifest 的 ``credential_fields``
声明，并豁免空值与 ``<Replace me>`` 占位符；孤立配置只告警不报错。已装包清单不可用时，孤立配置检查
跳过，凭据检查保守地覆盖全部密钥字段。

环境诊断的其余项（Python 版本、venv、缺失配置、迁移未应用、字体）不在本任务范围内。
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import json
from typing import Any

import typer
from rich.console import Console
from rich.markup import escape

from akaribot.cli.commands.adapter import (
    AdapterInstanceConfig,
    AdapterRegistry,
    AdapterScan,
    CoreCallError,
    InstanceLike,
    InstalledAdapter,
    ListenEndpoint,
    client_name_for,
    config_root,
    fetch_adapters,
    hosts_overlap,
    is_placeholder,
    listen_endpoints,
    open_instance,
    scan_adapter_instances,
    spawn_core,
)

CONFLICT_KINDS = frozenset({"port", "credential", "orphan", "config"})
DEFAULT_LEVELS = {"port": "error", "credential": "error", "orphan": "warning", "config": "error"}
# 凭据比对不看这些键：它们不是账号凭据，取值相同属于正常。
CREDENTIAL_EXCLUDED_KEYS = frozenset({"enable"})
CORE_CONFLICTS_ARGS = ("config", "conflicts", "--json")


@dataclass(frozen=True)
class Conflict:
    """一项检查结论。

    :param kind: ``port`` / ``credential`` / ``orphan`` / ``config``。
    :param level: ``error`` 会以非零码退出，``warning`` 只提示。
    :param message: 面向用户的一句话结论。
    :param platform: 相关平台名；跨平台时为多个平台。
    :param instances: 相关表名。
    :param detail: 结构化细节，供 ``--json`` 输出。
    """

    kind: str
    level: str
    message: str
    platform: str = ""
    instances: tuple[str, ...] = ()
    detail: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """转为可序列化的字典。"""
        return {
            "kind": self.kind,
            "level": self.level,
            "platform": self.platform,
            "instances": list(self.instances),
            "message": self.message,
            "detail": dict(self.detail),
        }


def _label(config: AdapterInstanceConfig, registry: AdapterRegistry) -> str:
    """实例在结论中的称呼。

    :param config: 实例配置。
    :param registry: 已装适配器清单。
    :return: 形如 ``bot_telegram-alt（Telegram-alt）`` 的文本。
    """
    client_name, inferred = client_name_for(config, registry)
    suffix = "（推断）" if inferred else ""
    return f"{config.table}（{client_name}{suffix}）"


def _check_ports(scan: AdapterScan, registry: AdapterRegistry) -> list[Conflict]:
    """端口冲突：全部已启用实例的监听地址两两比对。

    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :return: 结论列表。
    """
    observations: list[tuple[ListenEndpoint, AdapterInstanceConfig]] = []
    for config in scan.instances:
        adapter = registry.adapters.get(config.platform)
        declared = adapter.listen_fields if adapter else ()
        for endpoint in listen_endpoints(config.values, declared):
            if not endpoint.local or not endpoint.port:
                continue
            observations.append((endpoint, config))
    conflicts: list[Conflict] = []
    for index, (endpoint, config) in enumerate(observations):
        for other_endpoint, other in observations[index + 1 :]:
            if config.table == other.table or endpoint.port != other_endpoint.port:
                continue
            if not hosts_overlap(endpoint.host, other_endpoint.host):
                continue
            both_enabled = config.enabled and other.enabled
            note = "" if both_enabled else "（相关实例未全部启用，启用后即会冲突）"
            conflicts.append(
                Conflict(
                    kind="port",
                    level="error" if both_enabled else "warning",
                    platform=config.platform if config.platform == other.platform else "",
                    message=(
                        f"端口冲突：{endpoint.display()} 与 {other_endpoint.display()} 同时被 "
                        f"{_label(config, registry)} 与 {_label(other, registry)} 声明{note}"
                    ),
                    instances=(config.table, other.table),
                    detail={
                        "address": endpoint.display(),
                        "other_address": other_endpoint.display(),
                        "port": endpoint.port,
                    },
                )
            )
    return conflicts


def _credential_items(
    config: AdapterInstanceConfig, adapter: InstalledAdapter | None, registry: AdapterRegistry
) -> list[tuple[str, str]]:
    """列出实例参与重复检查的凭据项。

    :param config: 实例配置。
    :param adapter: 该平台的已装适配器；未安装时为 ``None``。
    :param registry: 已装适配器清单。
    :return: 二元组列表——字段名与取值的规范化串（取值只用于比对，不进入输出）。
    """
    if not registry.available:
        fields: Sequence[str] = tuple(config.secrets)
    elif adapter is None:
        fields = ()
    else:
        fields = adapter.credential_fields
    items: list[tuple[str, str]] = []
    for name in fields:
        if name in CREDENTIAL_EXCLUDED_KEYS:
            continue
        # 凭据字段可能落在非密钥表：qqbot 的 qq_bot_appid 就在明文表中
        value = config.secrets.get(name, config.values.get(name))
        if value is None or is_placeholder(value):
            continue
        if isinstance(value, str):
            if not value.strip():
                continue
        elif isinstance(value, (list, tuple, dict, set)) and not value:
            continue
        items.append((name, json.dumps(value, sort_keys=True, default=str)))
    return items


def _check_credentials(scan: AdapterScan, registry: AdapterRegistry) -> list[Conflict]:
    """凭据重复：同平台不同实例配了相同的 token / appid。

    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :return: 结论列表。
    """
    groups: dict[tuple[str, str, str], list[AdapterInstanceConfig]] = defaultdict(list)
    for config in scan.instances:
        adapter = registry.adapters.get(config.platform)
        for name, normalized in _credential_items(config, adapter, registry):
            groups[(config.platform, name, normalized)].append(config)
    conflicts: list[Conflict] = []
    for (platform, name, normalized), members in sorted(groups.items()):
        if len(members) < 2:
            continue
        all_enabled = all(member.enabled for member in members)
        note = "" if all_enabled else "（相关实例未全部启用，启用后即会冲突）"
        labels = "、".join(_label(member, registry) for member in members)
        conflicts.append(
            Conflict(
                kind="credential",
                level="error" if all_enabled else "warning",
                platform=platform,
                message=(
                    f"凭据重复：{labels}的 {name} 取值相同（已隐藏，长度 {len(normalized)}）{note}"
                    "；两个进程会争抢同一账号的消息。"
                ),
                instances=tuple(member.table for member in members),
                detail={"field": name, "length": len(normalized), "tables": [member.table for member in members]},
            )
        )
    return conflicts


def _check_orphans(scan: AdapterScan, registry: AdapterRegistry) -> list[Conflict]:
    """孤立配置：有实例配置文件，但对应平台的适配器包未安装。

    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :return: 结论列表。
    """
    if not registry.available:
        return []
    conflicts: list[Conflict] = []
    for config in scan.instances:
        if config.platform in registry.adapters:
            continue
        conflicts.append(
            Conflict(
                kind="orphan",
                level="warning",
                platform=config.platform,
                message=(
                    f"孤立配置：{config.path} 定义了 {config.table}，但平台 {config.platform} 的适配器包"
                    "未安装；守护进程会跳过该实例。"
                ),
                instances=(config.table,),
                detail={"config_file": str(config.path), "table": config.table},
            )
        )
    return conflicts


def local_conflicts(scan: AdapterScan, registry: AdapterRegistry) -> list[Conflict]:
    """本地实现的多实例三查。

    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :return: 结论列表，按种类与表名排序。
    """
    conflicts = [*_check_ports(scan, registry), *_check_credentials(scan, registry), *_check_orphans(scan, registry)]
    return sorted(conflicts, key=lambda item: (item.kind, item.instances))


def fetch_core_conflicts(instance: InstanceLike) -> list[Conflict] | None:
    """调用 core 的 ``config conflicts`` 入口。

    :param instance: 目标实例。
    :return: 结论列表；入口不可用、退出码非零或输出结构不符时返回 ``None``，由调用方回退到本地实现。
    """
    try:
        call = spawn_core(instance, *CORE_CONFLICTS_ARGS)
    except CoreCallError:
        return None
    if call.returncode != 0:
        return None
    try:
        payload = call.json()
    except CoreCallError:
        return None
    raw_entries = payload.get("conflicts") if isinstance(payload, Mapping) else payload
    if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
        return None
    conflicts: list[Conflict] = []
    for entry in raw_entries:
        if not isinstance(entry, Mapping):
            return None
        kind = str(entry.get("kind") or "").strip().lower()
        if kind not in CONFLICT_KINDS:
            return None
        conflicts.append(
            Conflict(
                kind=kind,
                level=str(entry.get("level") or DEFAULT_LEVELS[kind]).strip().lower(),
                message=str(entry.get("message") or "").strip() or f"{kind} 冲突",
                platform=str(entry.get("platform") or ""),
                instances=tuple(str(item) for item in entry.get("instances") or ()),
                detail=entry.get("detail") if isinstance(entry.get("detail"), Mapping) else {},
            )
        )
    return conflicts


app = typer.Typer(help="自检：多实例的端口冲突、凭据重复与孤立配置", no_args_is_help=False)


@app.callback(invoke_without_command=True)
def run_checks(
    json_output: bool = typer.Option(False, "--json", help="以 JSON 输出，供 CI 与脚本使用。"),
    strict: bool = typer.Option(False, "--strict", help="告警也按失败处理。"),
) -> None:
    """检查多实例部署的三类冲突：端口冲突、凭据重复、孤立配置。

    判据优先来自 core 的 ``config conflicts`` 入口（与 daemon 启动前检查共用同一份实现）；入口不可用时
    使用 CLI 本地实现，输出中会标注实际使用的实现。存在 error 级结论时以非零码退出。
    """
    instance = open_instance()
    scan = scan_adapter_instances(instance)
    registry = fetch_adapters(instance)
    conflicts = fetch_core_conflicts(instance)
    implementation = "core（config conflicts）" if conflicts is not None else "CLI 本地（core 入口不可用）"
    if conflicts is None:
        conflicts = local_conflicts(scan, registry)
    conflicts.extend(
        Conflict(
            kind="config",
            level="error",
            message=f"配置文件无法解析：{error}",
            detail={"error": error},
        )
        for error in scan.errors
    )
    errors = [item for item in conflicts if item.level == "error"]
    warnings = [item for item in conflicts if item.level != "error"]

    if json_output:
        payload = {
            "instance_root": str(instance.root),
            "config_root": str(config_root(instance)),
            "implementation": implementation,
            "registry_available": registry.available,
            "registry_note": registry.note,
            "conflicts": [item.as_dict() for item in conflicts],
            "summary": {"error": len(errors), "warning": len(warnings)},
            "checks": _check_summary(scan, registry),
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        _print_report(instance, scan, registry, conflicts, implementation, errors, warnings)

    if errors or (strict and warnings):
        raise typer.Exit(1)


def _check_summary(scan: AdapterScan, registry: AdapterRegistry) -> dict[str, Any]:
    """各项检查的执行情况，供 JSON 输出与报告尾注使用。

    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :return: 检查项与结论。
    """
    configured = {config.platform for config in scan.instances}
    unconfigured = sorted(set(registry.adapters) - configured)
    return {
        "instances": len(scan.instances),
        "installed_adapters": sorted(registry.adapters),
        "unconfigured_adapters": unconfigured,
        "orphan_check": "ran" if registry.available else "skipped",
        "credential_scope": "manifest credential_fields" if registry.available else "全部密钥字段",
    }


def _print_report(
    instance: InstanceLike,
    scan: AdapterScan,
    registry: AdapterRegistry,
    conflicts: Sequence[Conflict],
    implementation: str,
    errors: Sequence[Conflict],
    warnings: Sequence[Conflict],
) -> None:
    """打印可读的检查报告。

    :param instance: 目标实例。
    :param scan: 配置扫描结果。
    :param registry: 已装适配器清单。
    :param conflicts: 全部结论。
    :param implementation: 本次使用的检查实现。
    :param errors: error 级结论。
    :param warnings: warning 级结论。
    """
    console = Console()
    summary = _check_summary(scan, registry)
    # 路径与消息里可能出现方括号（IPv6 监听地址、TOML 表名），故经 escape 再进入 rich 标记解析
    console.print(f"实例根：{escape(str(instance.root))}")
    console.print(f"配置根：{escape(str(config_root(instance)))}")
    installed = "、".join(summary["installed_adapters"]) or "（无）"
    console.print(f"实例 {summary['instances']} 个；已装适配器：{escape(installed)}")
    if summary["unconfigured_adapters"]:
        console.print(f"已装但尚无配置的适配器：{escape('、'.join(summary['unconfigured_adapters']))}")
    if not registry.available:
        console.print(f"[yellow]已装包清单不可用：{escape(registry.note)}[/yellow]")
        console.print("[yellow]孤立配置检查跳过；凭据检查退化为全部密钥字段。[/yellow]")
    for item in conflicts:
        style = "red" if item.level == "error" else "yellow"
        console.print(f"[{style}]{escape(item.message)}[/{style}]")
    console.print(f"共 {len(conflicts)} 项：error {len(errors)}，warning {len(warnings)}")
    console.print(f"冲突检查实现：{escape(implementation)}")
    if implementation.startswith("CLI"):
        console.print("注：core 提供 config conflicts 入口后，本命令与 daemon 前置检查将自动共用同一份判据。")
