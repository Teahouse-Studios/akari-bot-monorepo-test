from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.instance import INSTANCE_ID_PATTERN
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context
from akaribot.cli.tui.modules import ModuleRecord, OperationResult, SubprocessModuleSource


PEER_ENTRYPOINT = "peers"
PEER_READY_STATE = "ready"

# 文案与列宽随当前语言计算，常量仅保存文案键。
_ALIVE_KEYS = {True: "cli.tui.adapters.online", False: "cli.tui.adapters.offline"}
_ENABLE_KEYS = {True: "cli.tui.adapters.enable_on", False: "cli.tui.adapters.enable_off"}
_ENABLE_MISSING_KEY = "cli.tui.adapters.enable_missing"

# 此值用于解析 CLI 输出；显示文本使用 default_id 文案键。
DEFAULT_ID_LABEL = "（默认）"
EMPTY_CELL = "—"

MIN_FLEX_COLUMN_WIDTH = 8
ID_MAX_WIDTH = 14
CLIENT_MAX_WIDTH = 18
LISTEN_MAX_WIDTH = 24
COLUMN_GAP = 2
ROW_INDENT = 2


def _column_titles() -> tuple[str, ...]:
    return (
        i18n.t("cli.tui.adapters.column_instance"),
        "client_name",
        "enable",
        i18n.t("cli.tui.adapters.column_status"),
        i18n.t("cli.tui.adapters.column_listen"),
        i18n.t("cli.tui.adapters.column_error"),
    )


def _enable_column_width() -> int:
    labels = (i18n.t(_ENABLE_MISSING_KEY), *(i18n.t(key) for key in _ENABLE_KEYS.values()))
    return compat.column_width((_column_titles()[2], *labels))


def _status_column_width() -> int:
    labels = (i18n.t("cli.tui.common.unknown"), *(i18n.t(key) for key in _ALIVE_KEYS.values()))
    return compat.column_width((_column_titles()[3], *labels))


@dataclass(frozen=True)
class AdapterRecord:
    """一个适配器实例。

    :param platform: 平台名（entry point 名），如 ``telegram``。
    :param instance_id: 实例 ID；默认实例为空串。
    :param client_name: 路由用的 ``client_name``，如 ``Telegram-alt``。
    :param table: 配置表名，如 ``bot_telegram-alt``。
    :param config_file: 配置文件路径文本。
    :param enable: ``enable`` 原值；配置缺该键时为 ``None``。
    :param enabled: 是否已启用。
    :param listen: 监听地址的展示文本。
    :param installed: 对应平台的适配器包是否已安装。
    :param legacy_layout: 配置是否采用扁平布局。
    :param client_name_inferred: ``client_name`` 是否为按平台名推断的结果。
    :param issues: ``adapter list`` 给出的备注。
    :param developers: 适配器作者，取自包的 ``pyproject.toml``；仅可安装清单提供。
    """

    platform: str
    instance_id: str = ""
    client_name: str = ""
    table: str = ""
    config_file: str = ""
    enable: bool | None = None
    enabled: bool = False
    listen: tuple[str, ...] = ()
    installed: bool = False
    legacy_layout: bool = False
    client_name_inferred: bool = False
    issues: tuple[str, ...] = ()
    developers: tuple[str, ...] = ()

    @property
    def key(self) -> str:
        """选中项的稳定标识：表名优先，其次 ``client_name``。"""
        return self.table or self.client_name or f"{self.platform}/{self.instance_id}"

    @property
    def display_id(self) -> str:
        """返回实例列文本；未配置实例的平台为空。"""
        if self.installable and not self.configured:
            return EMPTY_CELL
        return self.instance_id or i18n.t("cli.tui.adapters.default_id")

    @property
    def installable(self) -> bool:
        """返回适配器包是否需要安装。"""
        return not self.installed

    @property
    def enable_label(self) -> str:
        """返回启用状态文本；未安装的适配器显示安装状态。"""
        if self.installable:
            return i18n.t("cli.tui.adapters.state_not_installed")
        if self.enable is None:
            return i18n.t(_ENABLE_MISSING_KEY)
        return i18n.t(_ENABLE_KEYS[self.enabled])

    @property
    def configured(self) -> bool:
        """是否已有配置表；由可安装清单合成的记录没有配置。"""
        return bool(self.table)

    @property
    def listen_text(self) -> str:
        """监听地址列的展示文本。"""
        return i18n.t("cli.tui.common.list_separator").join(self.listen) or EMPTY_CELL

    @property
    def issue_text(self) -> str:
        """备注列的展示文本。"""
        return i18n.t("cli.tui.common.error_separator").join(self.issues) or EMPTY_CELL


@dataclass(frozen=True)
class PeerStatus:
    """一个 ``client_name`` 的连接状态，取自 peer 记录。

    :param client_name: 该记录声明的 ``client_name``。
    :param state: peer 的原始状态，如 ``ready``；无记录时为空串。
    :param alive: 是否在线；无法判定时为 ``None``。
    :param error: peer 元数据中的最近错误。
    :param detail: 无法判定或状态异常时的说明。
    """

    client_name: str
    state: str = ""
    alive: bool | None = None
    error: str = ""
    detail: str = ""

    @property
    def label(self) -> str:
        """连接列的展示文本。"""
        if self.alive is None:
            return i18n.t("cli.tui.common.unknown")
        return i18n.t(_ALIVE_KEYS[self.alive])


@dataclass(frozen=True)
class AdapterSnapshot:
    """适配器实例清单快照。

    :param instances: 实例记录，按平台名与实例 ID 排序。
    :param instance_root: 实例根目录文本。
    :param registry_available: 已安装适配器清单是否可用。
    :param registry_note: 清单不可用或形状异常时的说明。
    :param legacy_layout: 是否含扁平布局配置。
    :param errors: 配置文件的解析错误。
    """

    instances: tuple[AdapterRecord, ...] = ()
    instance_root: str = ""
    registry_available: bool = True
    registry_note: str = ""
    legacy_layout: bool = False
    errors: tuple[str, ...] = ()

    def grouped(self) -> tuple[tuple[str, tuple[AdapterRecord, ...]], ...]:
        """按平台名分组，组内保持实例顺序，组间按平台名升序。"""
        groups: dict[str, list[AdapterRecord]] = {}
        for record in self.instances:
            groups.setdefault(record.platform, []).append(record)
        return tuple((platform, tuple(groups[platform])) for platform in sorted(groups))

    def with_available(self, records: Sequence[AdapterRecord]) -> AdapterSnapshot:
        """补充尚无实例记录的可安装平台。"""
        known = {record.platform for record in self.instances}
        extra = [record for record in records if record.platform not in known]
        if not extra:
            return self
        merged = tuple(sorted((*self.instances, *extra), key=lambda item: (item.platform, item.instance_id)))
        return replace(self, instances=merged)


@dataclass(frozen=True)
class PeerSnapshot:
    """peer 连接状态快照。

    :param statuses: 别名（``client_name`` / ``service`` / 路由前缀）到连接状态的映射。
    :param available: 快照是否可用。
    :param note: 不可用的原因。
    """

    statuses: Mapping[str, PeerStatus] = field(default_factory=dict)
    available: bool = False
    note: str = ""

    def status_for(self, client_name: str) -> PeerStatus:
        """返回指定 ``client_name`` 的连接状态；无记录时返回未知状态与原因。"""
        found = self.statuses.get(client_name)
        if found is not None:
            return found
        if self.available:
            return PeerStatus(client_name=client_name, alive=None, detail=i18n.t("cli.tui.adapters.peer_missing"))
        return PeerStatus(
            client_name=client_name, alive=None, detail=self.note or i18n.t("cli.tui.adapters.peer_unavailable")
        )


class AdapterSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


class StaticAdapterSource:
    """用于测试的静态数据源，不创建子进程。

    :param snapshot: ``list_instances`` 的返回值。
    :param available: ``list_available`` 的返回值。
    :param peers: ``peer_status`` 的返回值；默认表示快照不可用。
    :param toggle_result: ``set_enable`` 的返回值；默认为成功。
    :param instance_result: ``add_instance`` / ``remove_instance`` 的返回值；默认为成功。
    """

    def __init__(
        self,
        snapshot: AdapterSnapshot | None = None,
        *,
        available: Sequence[AdapterRecord] = (),
        peers: PeerSnapshot | None = None,
        toggle_result: OperationResult | None = None,
        install_result: OperationResult | None = None,
        install_lines: Sequence[str] = (),
        instance_result: OperationResult | None = None,
    ) -> None:
        self._snapshot = snapshot or AdapterSnapshot()
        self._available = tuple(available)
        self._install_result = install_result or OperationResult(
            True, i18n.t("cli.tui.adapters.stub_install_ok"), "stub"
        )
        self._install_lines = tuple(install_lines)
        self.installed: list[str] = []
        self._peers = peers or PeerSnapshot(note=i18n.t("cli.tui.adapters.stub_no_peers"))
        self._toggle_result = toggle_result or OperationResult(True, i18n.t("cli.tui.adapters.stub_toggle_ok"), "stub")
        self._instance_result = instance_result or OperationResult(
            True, i18n.t("cli.tui.adapters.stub_instance_ok"), "stub"
        )
        self.calls = {
            "list": 0,
            "available": 0,
            "install": 0,
            "peers": 0,
            "set_enable": 0,
            "add_instance": 0,
            "remove_instance": 0,
        }
        self.toggles: list[tuple[str, bool]] = []
        self.added: list[tuple[str, str]] = []
        self.removed: list[tuple[str, str, bool]] = []

    def list_instances(self) -> AdapterSnapshot:
        """见 :meth:`AdapterSource.list_instances`。"""
        self.calls["list"] += 1
        return self._snapshot

    def list_available(self) -> tuple[AdapterRecord, ...]:
        """见 :meth:`AdapterSource.list_available`。"""
        self.calls["available"] += 1
        return self._available

    async def stream_install(self, record: AdapterRecord, on_line: Callable[[str], None]) -> OperationResult:
        """见 :meth:`AdapterSource.stream_install`；替身直接回放固定输出。"""
        self.calls["install"] += 1
        self.installed.append(record.platform)
        for line in self._install_lines:
            on_line(line)
        return self._install_result

    def peer_status(self) -> PeerSnapshot:
        """见 :meth:`AdapterSource.peer_status`。"""
        self.calls["peers"] += 1
        return self._peers

    def add_instance(self, platform: str, instance_id: str) -> OperationResult:
        """见 :meth:`AdapterSource.add_instance`。"""
        self.calls["add_instance"] += 1
        self.added.append((platform, instance_id))
        return self._instance_result

    def remove_instance(self, record: AdapterRecord) -> OperationResult:
        """见 :meth:`AdapterSource.remove_instance`。"""
        self.calls["remove_instance"] += 1
        self.removed.append((record.platform, record.instance_id))
        return self._instance_result

    def set_enable(self, record: AdapterRecord, enabled: bool) -> OperationResult:
        """见 :meth:`AdapterSource.set_enable`；成功后替换缓存中的该条记录。"""
        self.calls["set_enable"] += 1
        self.toggles.append((record.table or record.client_name, enabled))
        records = [
            replace(item, enable=enabled, enabled=enabled) if item.key == record.key else item
            for item in self._snapshot.instances
        ]
        self._snapshot = replace(self._snapshot, instances=tuple(records))
        return self._toggle_result


@runtime_checkable
class AdapterSource(Protocol):
    """适配器状态与操作的数据源接口。"""

    def list_instances(self) -> AdapterSnapshot:
        """返回实例清单。"""

    def list_available(self) -> tuple[AdapterRecord, ...]:
        """返回可安装的适配器包，含尚未安装的平台。"""

    async def stream_install(self, record: AdapterRecord, on_line: Callable[[str], None]) -> OperationResult:
        """安装适配器包，通过 ``on_line`` 逐行返回输出。"""

    def peer_status(self) -> PeerSnapshot:
        """返回 peer 连接状态快照；不可用时以 ``available=False`` 上报原因，不抛异常。"""

    def set_enable(self, record: AdapterRecord, enabled: bool) -> OperationResult:
        """通过 CLI 设置实例的 ``enable``。"""


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return i18n.t("cli.tui.common.list_separator").join(_text(item) for item in value if _text(item))
    return str(value)


def _pick(source: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if isinstance(source, Mapping) and source.get(name) is not None:
            return source[name]
        value = getattr(source, name, None)
        if value is not None:
            return value
    return default


def _string_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, Sequence):
        return tuple(item for item in (_text(entry) for entry in value) if item)
    return ()


def _flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes", "on"}
    return bool(value)


def available_adapter_records(payload: Any) -> tuple[AdapterRecord, ...]:
    """将可安装清单输出转换为适配器记录。

    :param payload: ``json.loads`` 的结果。
    :return: 适配器记录，包含已安装的平台，由调用方去重。
    """
    records: list[AdapterRecord] = []
    for item in _rows(payload, "packages", "items", "data") or (payload if isinstance(payload, list) else []):
        if not isinstance(item, Mapping):
            continue
        name = _text(_pick(item, "name", "platform", "module", "id"))
        if not name:
            continue
        records.append(
            AdapterRecord(
                platform=name,
                installed=bool(_pick(item, "installed", "is_installed", default=False)),
                developers=tuple(str(value) for value in _pick(item, "developers", "authors", default=()) or ()),
            )
        )
    return tuple(records)


def _rows(payload: Any, *keys: str) -> list[Any]:
    if isinstance(payload, Mapping):
        for key in keys:
            nested = payload.get(key)
            if isinstance(nested, Sequence) and not isinstance(nested, (str, bytes)):
                return list(nested)
        return []
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
        return list(payload)
    return []


def normalize_snapshot(payload: Any) -> AdapterSnapshot:
    """将适配器清单输出转换为 :class:`AdapterSnapshot`。

    :param payload: ``json.loads`` 的结果；支持对象与数组。
    :return: 按平台名与实例 ID 排序的实例快照。
    """
    records: list[AdapterRecord] = []
    for entry in _rows(payload, "instances", "items", "adapters", "data"):
        if not isinstance(entry, Mapping):
            continue
        enable_raw = _pick(entry, "enable")
        enable = None if enable_raw is None else _flag(enable_raw)
        platform = _text(_pick(entry, "platform", "platform_name", "adapter"))
        instance_id = _text(_pick(entry, "instance_id", "instance", "id"))
        table = _text(_pick(entry, "table", "config_table"))
        client_name = _text(_pick(entry, "client_name", "client", "service"))
        records.append(
            AdapterRecord(
                platform=platform,
                instance_id="" if instance_id == DEFAULT_ID_LABEL else instance_id,
                client_name=client_name,
                table=table,
                config_file=_text(_pick(entry, "config_file", "path", "file")),
                enable=enable,
                enabled=_flag(_pick(entry, "enabled", default=enable)) if enable is not None else False,
                listen=_string_tuple(_pick(entry, "listen", "listen_addresses", "endpoints", default=())),
                installed=_flag(_pick(entry, "installed", default=False)),
                legacy_layout=_flag(_pick(entry, "legacy_layout", default=False)),
                client_name_inferred=_flag(_pick(entry, "client_name_inferred", default=False)),
                issues=_string_tuple(_pick(entry, "issues", "warnings", "notes", default=())),
            )
        )
    records.sort(key=lambda item: (item.platform, item.instance_id))
    if not isinstance(payload, Mapping):
        return AdapterSnapshot(instances=tuple(records))
    return AdapterSnapshot(
        instances=tuple(records),
        instance_root=_text(payload.get("instance_root")),
        registry_available=_flag(payload.get("registry_available", True)),
        registry_note=_text(payload.get("registry_note")),
        legacy_layout=_flag(payload.get("legacy_layout", False)),
        errors=_string_tuple(payload.get("errors")),
    )


def _lease_expired(value: Any, now: float) -> bool | None:
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) <= now
    text = _text(value)
    if not text:
        return None
    try:
        return float(text) <= now
    except ValueError:
        pass
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.timestamp() <= now


def _peer_aliases(entry: Mapping[str, Any], peer_id: str) -> tuple[str, set[str]]:
    # 平台显示名可能与默认实例的 client_name 相同，不能用作其他实例的状态别名。
    primary = _text(_pick(entry, "client_name")) or _text(_pick(entry, "service")) or peer_id
    aliases = {primary, _text(_pick(entry, "service")), _text(_pick(entry, "client_name"))}
    metadata = _pick(entry, "metadata", default={})
    if isinstance(metadata, Mapping):
        aliases.add(_text(metadata.get("client_name")))
        for key in ("target_prefix_list", "sender_prefix_list"):
            for prefix in _string_tuple(metadata.get(key)):
                aliases.add(prefix.split("|", 1)[0].strip())
    return primary, {alias for alias in aliases if alias}


def normalize_peer_snapshot(payload: Any, now: float | None = None) -> PeerSnapshot:
    """将 core 的 peer 快照转换为 :class:`PeerSnapshot`。

    :param payload: ``json.loads`` 的结果。
    :param now: 判定租约用的当前时刻，默认取 :func:`time.time`。
    :return: 连接状态快照；状态为 ready 且租约有效时判定为在线。
    """
    if not isinstance(payload, Mapping):
        return PeerSnapshot(available=False, note=i18n.t("cli.tui.adapters.peer_not_object"))
    available = payload.get("available")
    if not isinstance(available, bool):
        return PeerSnapshot(available=False, note=i18n.t("cli.tui.adapters.peer_missing_field", field="available"))
    rows = payload.get("peers")
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        return PeerSnapshot(available=False, note=i18n.t("cli.tui.adapters.peer_missing_field", field="peers"))
    note = _text(payload.get("note"))
    if not available:
        return PeerSnapshot(available=False, note=note or i18n.t("cli.tui.adapters.peer_unavailable"))
    moment = time.time() if now is None else now
    statuses: dict[str, PeerStatus] = {}
    seen: set[str] = set()
    for entry in rows:
        if not isinstance(entry, Mapping):
            continue
        peer_id = _text(_pick(entry, "peer_id", "id"))
        if peer_id in seen:
            continue
        seen.add(peer_id)
        state = _text(_pick(entry, "state", "status"))
        metadata = _pick(entry, "metadata", default={})
        error = ""
        if isinstance(metadata, Mapping):
            error = _text(_pick(metadata, "last_error", "error", "last_exception"))
        expired = _lease_expired(_pick(entry, "lease_until", "lease"), moment)
        if not state:
            alive: bool | None = None
            detail = i18n.t("cli.tui.adapters.peer_no_state")
        elif state != PEER_READY_STATE:
            alive = False
            detail = i18n.t("cli.tui.adapters.peer_state", state=state)
        elif expired is None:
            alive = None
            detail = i18n.t("cli.tui.adapters.peer_no_lease")
        elif expired:
            alive = False
            detail = i18n.t("cli.tui.adapters.peer_lease_expired")
        else:
            alive = True
            detail = ""
        primary, aliases = _peer_aliases(entry, peer_id)
        status = PeerStatus(client_name=primary, state=state, alive=alive, error=error, detail=detail)
        for alias in aliases or {peer_id}:
            statuses.setdefault(alias, status)
    return PeerSnapshot(statuses=statuses, available=True, note=note)


def group_display(records: Sequence[AdapterRecord], registry_available: bool) -> str:
    """返回平台分组标题的状态后缀。

    :param records: 该平台下的实例。
    :param registry_available: 已安装适配器清单是否可用。
    :return: 平台显示名或清单状态。
    """
    for record in records:
        if not record.installed:
            continue
        suffix = f"-{record.instance_id}" if record.instance_id else ""
        if suffix and record.client_name.endswith(suffix):
            return record.client_name[: -len(suffix)]
        if not suffix and record.client_name:
            return record.client_name
    return (
        i18n.t("cli.tui.adapters.group_not_installed")
        if registry_available
        else i18n.t("cli.tui.adapters.group_registry_unavailable")
    )


class SubprocessAdapterSource:
    """通过子进程读取适配器状态并执行操作。

    :param root: 实例根目录；默认取当前实例。
    :param timeout: 单个子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: ``Instance`` 的构造回调，测试可注入以避开实例发现。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        instance_factory: Callable[[], Any] | None = None,
    ) -> None:
        # 实例根在每次请求时解析，使子进程目录与 AKARI_INSTANCE_DIR 跟随当前实例。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"list": 0, "available": 0, "install": 0, "peers": 0, "set_enable": 0}
        self._runner = runner or subprocess.run
        self._instance_factory = instance_factory

    @property
    def root(self) -> Path:
        """返回实例根目录，依次采用显式路径、当前实例或自动定位结果。"""
        return context.resolve_root(self._root_override)

    def list_instances(self) -> AdapterSnapshot:
        """见 :meth:`AdapterSource.list_instances`。"""
        self.calls["list"] += 1
        argv = self.cli_argv("adapter", "list", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise AdapterSourceError(
                i18n.t(
                    "cli.tui.adapters.src_exit_code",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return normalize_snapshot(self._parse_json(completed.stdout, "adapter list --json"))

    def list_available(self) -> tuple[AdapterRecord, ...]:
        """见 :meth:`AdapterSource.list_available`；复用 ``module available`` 的可安装集合。"""
        self.calls["available"] += 1
        argv = self.cli_argv("module", "available", "--json", "--kind", "adapter")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise AdapterSourceError(
                i18n.t(
                    "cli.tui.adapters.src_exit_code",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return available_adapter_records(self._parse_json(completed.stdout, "module available --json"))

    async def stream_install(self, record: AdapterRecord, on_line: Callable[[str], None]) -> OperationResult:
        """通过模块数据源安装适配器，并逐行返回进度。"""
        self.calls["install"] += 1
        installer = SubprocessModuleSource(root=self.root, timeout=self.timeout)
        return await installer.stream_operation("install", ModuleRecord(name=record.platform), on_line)

    def peer_status(self) -> PeerSnapshot:
        """返回 peer 连接状态；入口不可用时返回原因。"""
        self.calls["peers"] += 1
        argv = self.peer_argv()
        try:
            completed = self._run(argv)
        except AdapterSourceError as error:
            return PeerSnapshot(available=False, note=str(error))
        if completed.returncode != 0:
            tail = self._tail(completed.stderr) or i18n.t("cli.tui.common.no_output")
            return PeerSnapshot(
                available=False,
                note=i18n.t(
                    "cli.tui.adapters.peer_entrypoint_unavailable",
                    entry=PEER_ENTRYPOINT,
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=tail,
                ),
            )
        try:
            payload = self._parse_json(completed.stdout, f"core {PEER_ENTRYPOINT} --json")
        except AdapterSourceError as error:
            return PeerSnapshot(available=False, note=str(error))
        return normalize_peer_snapshot(payload)

    def set_enable(self, record: AdapterRecord, enabled: bool) -> OperationResult:
        """见 :meth:`AdapterSource.set_enable`；经 ``akaribot config set`` 写入。"""
        self.calls["set_enable"] += 1
        table = record.table or f"bot_{record.platform}" + (f"-{record.instance_id}" if record.instance_id else "")
        label = i18n.t(
            "cli.tui.adapters.label_enable" if enabled else "cli.tui.adapters.label_disable",
            name=record.client_name or table,
        )
        argv = self.cli_argv("config", "set", "enable", "true" if enabled else "false", "--table", table)
        completed = self._run(argv)
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), self._tail(completed.stdout))
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            self._tail(completed.stderr),
        )

    def add_instance(self, platform: str, instance_id: str) -> OperationResult:
        """见 :meth:`AdapterSource.add_instance`；经 ``akaribot adapter instance add`` 新建。"""
        self.calls["add_instance"] += 1
        label = i18n.t("cli.tui.adapters.label_instance_add", name=self._instance_display(platform, instance_id))
        args = ["adapter", "instance", "add", platform]
        if instance_id:
            args.append(instance_id)
        completed = self._run(self.cli_argv(*args))
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), self._tail(completed.stdout))
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            self._tail(completed.stderr) or self._tail(completed.stdout),
        )

    def remove_instance(self, record: AdapterRecord) -> OperationResult:
        """通过 CLI 移除适配器配置，保留实例数据。"""
        self.calls["remove_instance"] += 1
        label = i18n.t(
            "cli.tui.adapters.label_instance_remove",
            name=self._instance_display(record.platform, record.instance_id),
        )
        args = ["adapter", "instance", "remove", record.platform]
        if record.instance_id:
            args.append(record.instance_id)
        completed = self._run(self.cli_argv(*args))
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), self._tail(completed.stdout))
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            self._tail(completed.stderr) or self._tail(completed.stdout),
        )

    @staticmethod
    def _instance_display(platform: str, instance_id: str) -> str:
        return f"{platform}/{instance_id}" if instance_id else i18n.t("cli.tui.adapters.default_id")

    def cli_argv(self, *args: str) -> list[str]:
        """构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。"""
        return cli_process.cli_argv(*args)

    def peer_argv(self) -> list[str]:
        """构造使用实例解释器读取 peer 快照的命令参数。"""
        return [str(self._instance_python()), "-m", f"akaribot.core.entrypoints.{PEER_ENTRYPOINT}", "--json"]

    def _instance_python(self) -> Path:
        try:
            instance = self._instance()
        except AdapterSourceError:
            return Path(sys.executable)
        candidate = Path(_pick(instance, "python", default=sys.executable) or sys.executable)
        return candidate if candidate.exists() else Path(sys.executable)

    def _instance(self) -> Any:
        if self._instance_factory is not None:
            return self._instance_factory()
        try:
            from akaribot.cli.instance import Instance, find_instance_root
        except ImportError as error:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_instance_missing")) from error
        root = find_instance_root(self.root)
        if root is None:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_not_instance", root=self.root))
        return Instance(root)

    def _env(self) -> dict[str, str]:
        return cli_process.cli_env(self.root)

    def _run(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        try:
            return self._runner(
                list(argv),
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise AdapterSourceError(
                i18n.t("cli.tui.adapters.src_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from error
        except OSError as error:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_oserror", cmd=" ".join(argv), error=error)) from error

    def _parse_json(self, stdout: str, label: str) -> Any:
        text = stdout.strip()
        if not text:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_empty_output", label=label))
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise AdapterSourceError(i18n.t("cli.tui.adapters.src_bad_json", label=label, error=error)) from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        return (text or "").strip()[-limit:]


@dataclass(frozen=True)
class ColumnLayout:
    """列表列宽，单位终端列；宽度为 0 的列不渲染。

    :param id_width: 实例列。
    :param client_width: ``client_name`` 列。
    :param enable_width: enable 列。
    :param status_width: 连接列。
    :param listen_width: 监听地址列。
    :param error_width: 最近错误列。
    """

    id_width: int
    client_width: int
    enable_width: int
    status_width: int
    listen_width: int
    error_width: int

    def widths(self) -> tuple[int, ...]:
        """按列序返回宽度。"""
        return (
            self.id_width,
            self.client_width,
            self.enable_width,
            self.status_width,
            self.listen_width,
            self.error_width,
        )


class AdaptersPage(compat.Vertical):
    """适配器页面。

    :param source: 数据源，默认为 :class:`SubprocessAdapterSource`。
    :param cache_ttl: 缓存有效期秒数；enable 切换成功后立即失效，与有效期无关。
    """

    can_focus = True

    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.adapters.action_refresh")),
        ("e", "toggle_enable", i18n.t("cli.tui.adapters.bind_toggle_enable"), False),
        ("i", "install", i18n.t("cli.tui.adapters.action_install")),
        ("a", "add_instance", i18n.t("cli.tui.adapters.bind_add_instance"), False),
        ("ctrl+d", "remove_instance", i18n.t("cli.tui.adapters.bind_remove_instance"), False),
    )

    DEFAULT_CSS = """
    AdaptersPage {
        layout: vertical;
        height: 1fr;
    }
    AdaptersPage #summary {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    AdaptersPage #columns {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    AdaptersPage #adapter-list {
        height: 1fr;
        border: round $primary;
    }
    AdaptersPage #adapter-list > ListItem {
        padding: 0;
    }
    AdaptersPage #adapter-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    AdaptersPage #adapter-list > ListItem.group-header {
        color: $accent;
    }
    AdaptersPage #instance-row {
        height: 3;
        padding: 0 0 0 1;
    }
    AdaptersPage #new-instance {
        width: 1fr;
    }
    AdaptersPage #actions {
        height: auto;
        padding: 0 0 0 1;
    }
    AdaptersPage #detail {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    AdaptersPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(
        self,
        source: AdapterSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: AdapterSource = source if source is not None else SubprocessAdapterSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._snapshot = AdapterSnapshot()
        self._peers = PeerSnapshot()
        self._loaded_at: float = 0.0
        self._selected_key: str | None = None
        self._busy: bool = False
        self._gate = compat.PendingConfirm()
        self._available_error: str = ""
        self._stream_lines: list[str] = []
        self._layout = ColumnLayout(6, 8, _enable_column_width(), _status_column_width(), MIN_FLEX_COLUMN_WIDTH, 0)
        self._row_texts: tuple[str, ...] = ()
        self._row_kinds: tuple[str, ...] = ()
        self._instance_rows: tuple[tuple[str, ...], ...] = ()
        self._group_titles: tuple[str, ...] = ()
        self._header_text: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._summary_rendered: str = ""
        self._detail_rendered: str = ""

    def compose(self) -> compat.ComposeResult:

        yield compat.Static(i18n.t("cli.tui.adapters.summary_pending"), id="summary", markup=False)
        yield compat.Static("", id="columns", markup=False)
        yield compat.ListView(id="adapter-list")
        with compat.Horizontal(id="instance-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.adapters.instance_placeholder"), id="new-instance")
        yield compat.ButtonFlow(
            ("toggle", i18n.t("cli.tui.adapters.action_toggle"), "primary"),
            ("add-instance", i18n.t("cli.tui.adapters.action_add_instance")),
            ("remove-instance", i18n.t("cli.tui.adapters.action_remove_instance"), "error"),
            ("refresh", i18n.t("cli.tui.adapters.action_refresh")),
            id="actions",
        )
        yield compat.Static(i18n.t("cli.tui.adapters.detail_placeholder"), id="detail", markup=False)
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:

        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取适配器实例。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_instances()

    @property
    def records(self) -> tuple[AdapterRecord, ...]:
        """返回缓存中的全部实例，不触发子进程。"""
        return self._snapshot.instances

    @property
    def snapshot(self) -> AdapterSnapshot:
        """返回最近一次实例清单快照。"""
        return self._snapshot

    @property
    def peers(self) -> PeerSnapshot:
        """返回最近一次 peer 快照。"""
        return self._peers

    @property
    def peer_note(self) -> str:
        """返回 peer 快照不可用的原因，可用时为空串。"""
        return "" if self._peers.available else self._peers.note

    @property
    def selected_record(self) -> AdapterRecord | None:
        """返回列表当前高亮项对应的记录；停在分组标题上时为 ``None``。"""
        records = self._records_in_row_order()
        if not records:
            return None
        try:
            list_view = self.query_one("#adapter-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None:
            return None
        row = self._row_kinds[index] if 0 <= index < len(self._row_kinds) else ""
        if row != "instance":
            return None
        position = sum(1 for kind in self._row_kinds[:index] if kind == "instance")
        return records[position] if position < len(records) else None

    @property
    def header_text(self) -> str:
        """返回列标题行当前文本。"""
        return self._header_text

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def summary_text(self) -> str:
        """返回顶部摘要当前文本。"""
        return self._summary_rendered

    @property
    def detail_text(self) -> str:
        """返回详情栏当前文本。"""
        return self._detail_rendered

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的全部行文本，包含分组标题行。"""
        return self._row_texts

    def group_titles(self) -> tuple[str, ...]:
        """返回最近一次渲染出的分组标题行文本。"""
        return self._group_titles

    def instance_cells(self) -> tuple[tuple[str, ...], ...]:
        """返回最近一次渲染出的实例行各列取值，顺序与列表一致。"""
        return self._instance_rows

    def cache_age(self) -> float:
        """返回缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    def refresh_instances(self, *, force: bool = False) -> None:
        """读取实例清单与 peer 快照。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不读取数据。
        """
        self.reset_pending()
        if not force and self._snapshot.instances and self.cache_age() < self.cache_ttl:
            self._render_all()
            self._set_status(
                i18n.t(
                    "cli.tui.adapters.status_cached",
                    age=f"{self.cache_age():.1f}",
                    count=len(self._snapshot.instances),
                )
            )
            return
        self._set_status(i18n.t("cli.tui.adapters.status_loading"))
        self.run_worker(self._load(), group="adapters-load", exclusive=True)

    async def _load(self) -> bool:
        try:
            snapshot = await asyncio.to_thread(self.source.list_instances)
        except AdapterSourceError as error:
            self._snapshot = AdapterSnapshot()
            self._peers = PeerSnapshot()
            self._loaded_at = time.monotonic()
            self.last_error = str(error)
            self._render_all()
            self._set_status(i18n.t("cli.tui.adapters.status_load_failed", error=error))
            return False
        except Exception as error:  # noqa: BLE001 - 数据源异常不应中断界面
            self._snapshot = AdapterSnapshot()
            self._peers = PeerSnapshot()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_all()
            self._set_status(i18n.t("cli.tui.adapters.status_load_failed", error=self.last_error))
            return False
        self._peers = await self._load_peers()
        self._snapshot = await self._with_available(snapshot)
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = i18n.t("cli.tui.adapters.status_loaded", count=len(snapshot.instances))
        self._render_all()
        self._set_status(self.last_result)
        return True

    async def _with_available(self, snapshot: AdapterSnapshot) -> AdapterSnapshot:
        # 可安装清单读取失败时，仍保留实例配置与启用状态。
        self._available_error = ""
        try:
            records = await asyncio.to_thread(self.source.list_available)
        except AdapterSourceError as error:
            self._available_error = i18n.t("cli.tui.adapters.available_failed", error=error)
            return snapshot
        except Exception as error:  # noqa: BLE001 - 数据源异常不应中断界面
            self._available_error = i18n.t(
                "cli.tui.adapters.available_failed", error=f"{type(error).__name__}: {error}"
            )
            return snapshot
        return snapshot.with_available(records)

    async def _load_peers(self) -> PeerSnapshot:
        try:
            return await asyncio.to_thread(self.source.peer_status)
        except Exception as error:  # noqa: BLE001 - 连接状态读取失败不应中断页面
            return PeerSnapshot(available=False, note=f"{type(error).__name__}: {error}")

    def invalidate_cache(self) -> None:
        """清除缓存有效期，使下次请求重新读取数据。"""
        self._loaded_at = 0.0
        self._snapshot = AdapterSnapshot()

    def _records_in_row_order(self) -> tuple[AdapterRecord, ...]:
        return tuple(record for _, group in self._snapshot.grouped() for record in group)

    def _render_all(self) -> None:
        list_view = self.query_one("#adapter-list", compat.ListView)
        inner_width = self._list_inner_width(list_view)
        self._layout = self._build_layout(inner_width)
        self._header_text = self._header_row(self._layout)
        self.query_one("#columns", compat.Static).update(compat.plain_text(self._header_text))
        lines: list[str] = []
        kinds: list[str] = []
        cells: list[tuple[str, ...]] = []
        titles: list[str] = []
        for platform, group in self._snapshot.grouped():
            title = self._group_row(platform, group, inner_width)
            lines.append(title)
            kinds.append("header")
            titles.append(title)
            for record in group:
                row_cells = self._record_cells(record)
                lines.append(self._compose_row(row_cells, self._layout))
                kinds.append("instance")
                cells.append(row_cells)
        self._row_texts = tuple(lines)
        self._row_kinds = tuple(kinds)
        self._instance_rows = tuple(cells)
        self._group_titles = tuple(titles)
        list_view.clear()
        if lines:
            items = [
                compat.ListItem(
                    compat.Static(line, markup=False),
                    disabled=kind == "header",
                    classes="group-header" if kind == "header" else "",
                )
                for line, kind in zip(lines, kinds)
            ]
            list_view.extend(items)
        list_view.index = self._index_for_key()
        self._sync_summary()
        self._sync_detail()
        self._sync_actions()

    def _list_inner_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 76
        return max(outer - 4, 8)

    def _build_layout(self, inner_width: int) -> ColumnLayout:
        records = self._snapshot.instances
        titles = _column_titles()
        id_width = min(
            max(compat.column_width(record.display_id for record in records), compat.display_width(titles[0]), 6),
            ID_MAX_WIDTH,
        )
        client_width = min(
            max(compat.column_width(record.client_name or "-" for record in records), 8), CLIENT_MAX_WIDTH
        )
        enable_width = _enable_column_width()
        status_width = _status_column_width()
        fixed = ROW_INDENT + id_width + client_width + enable_width + status_width + COLUMN_GAP * 3
        remaining = inner_width - fixed - COLUMN_GAP * 2
        if remaining < 0:
            budget = max(inner_width - ROW_INDENT - enable_width - status_width - COLUMN_GAP * 3, 8)
            id_width = max(budget // 2, 4)
            client_width = max(budget - id_width, 4)
            remaining = 0
        listen_need = min(
            max(compat.column_width(record.listen_text for record in records) + 1, MIN_FLEX_COLUMN_WIDTH),
            LISTEN_MAX_WIDTH,
        )
        if remaining >= MIN_FLEX_COLUMN_WIDTH * 2 + COLUMN_GAP:
            listen_width = min(listen_need, remaining - COLUMN_GAP - MIN_FLEX_COLUMN_WIDTH)
            error_width = remaining - COLUMN_GAP - listen_width
        elif remaining >= MIN_FLEX_COLUMN_WIDTH:
            listen_width, error_width = remaining, 0
        else:
            listen_width, error_width = 0, 0
        return ColumnLayout(
            id_width=id_width,
            client_width=client_width,
            enable_width=enable_width,
            status_width=status_width,
            listen_width=listen_width,
            error_width=error_width,
        )

    def _header_row(self, layout: ColumnLayout) -> str:
        return self._compose_row(_column_titles(), layout)

    def _record_cells(self, record: AdapterRecord) -> tuple[str, ...]:
        status = self._peers.status_for(record.client_name)
        error = record.issue_text
        if error == EMPTY_CELL and status.error:
            error = status.error
        return (
            record.display_id,
            record.client_name or EMPTY_CELL,
            record.enable_label,
            status.label,
            record.listen_text,
            error,
        )

    def _compose_row(self, cells: Sequence[str], layout: ColumnLayout) -> str:
        parts = [compat.fit_cells(value, width) for value, width in zip(cells, layout.widths()) if width > 0]
        return (" " * ROW_INDENT + (" " * COLUMN_GAP).join(parts)).rstrip()

    def _group_row(self, platform: str, group: Sequence[AdapterRecord], inner_width: int) -> str:
        suffix = group_display(group, self._snapshot.registry_available)
        return compat.truncate_cells(
            i18n.t("cli.tui.adapters.group_row", platform=platform, suffix=suffix), inner_width
        )

    def _index_for_key(self) -> int:
        records = self._records_in_row_order()
        target = self._selected_key
        if target is not None:
            for position, record in enumerate(records):
                if record.key != target:
                    continue
                seen = 0
                for index, kind in enumerate(self._row_kinds):
                    if kind != "instance":
                        continue
                    if seen == position:
                        return index
                    seen += 1
        return next((index for index, kind in enumerate(self._row_kinds) if kind == "instance"), 0)

    def _sync_summary(self) -> None:
        snapshot = self._snapshot
        # 可安装平台记录不代表已配置实例，不计入实例总数。
        instances = tuple(record for record in snapshot.instances if not record.installable)
        enabled = sum(1 for record in instances if record.enabled)
        parts = [
            i18n.t(
                "cli.tui.adapters.summary_root",
                root=snapshot.instance_root or i18n.t("cli.tui.common.unknown"),
            ),
            i18n.t(
                "cli.tui.adapters.summary_counts",
                total=len(instances),
                enabled=enabled,
                platforms=len({record.platform for record in instances}),
            ),
        ]
        if not snapshot.registry_available:
            parts.append(
                i18n.t(
                    "cli.tui.adapters.summary_registry_unavailable",
                    note=snapshot.registry_note or i18n.t("cli.tui.adapters.reason_unknown"),
                )
            )
        elif snapshot.registry_note:
            parts.append(snapshot.registry_note)
        if snapshot.legacy_layout:
            parts.append(i18n.t("cli.tui.adapters.summary_legacy_layout"))
        if any(record.installed and record.client_name_inferred for record in snapshot.instances):
            parts.append(i18n.t("cli.tui.adapters.summary_inferred_client_name"))
        if self._peers.available:
            parts.append(i18n.t("cli.tui.adapters.peer_count", count=len(self._peers.statuses)))
        else:
            parts.append(
                i18n.t(
                    "cli.tui.adapters.peer_status_unknown",
                    note=self._peers.note or i18n.t("cli.tui.adapters.peer_unavailable"),
                )
            )

            parts.append(i18n.t("cli.tui.adapters.peer_status_unknown_hint"))
        installable = sum(1 for record in snapshot.instances if record.installable)
        if installable:
            parts.append(i18n.t("cli.tui.adapters.summary_installable", count=installable))
        if self._available_error:
            parts.append(self._available_error)
        for error in snapshot.errors:
            parts.append(error)
        text = i18n.t("cli.tui.common.error_separator").join(parts)
        self._summary_rendered = text
        self.query_one("#summary", compat.Static).update(compat.plain_text(self._fit_page_width(text)))

    def _fit_page_width(self, text: str) -> str:
        try:
            width = compat.widget_cells(self)[0] - 2
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            width = 78
        return compat.truncate_cells(text, max(width, 8))

    def _sync_detail(self) -> None:
        record = self.selected_record
        if record is None:
            text = (
                i18n.t("cli.tui.adapters.detail_hint")
                if self._snapshot.instances
                else i18n.t("cli.tui.adapters.detail_empty")
            )
            self._detail_rendered = text
            self.query_one("#detail", compat.Static).update(compat.plain_text(text))
            return
        self._selected_key = record.key
        if record.installable:
            parts = [i18n.t("cli.tui.adapters.detail_not_installed", platform=record.platform)]
            if record.developers:
                parts.append(
                    i18n.t(
                        "cli.tui.adapters.detail_developers",
                        names=i18n.t("cli.tui.common.list_separator").join(record.developers),
                    )
                )
            parts.append(i18n.t("cli.tui.adapters.detail_install_hint"))
            text = i18n.t("cli.tui.common.error_separator").join(parts)
            self._detail_rendered = self._fit_page_width(text)
            self.query_one("#detail", compat.Static).update(compat.plain_text(self._detail_rendered))
            return
        status = self._peers.status_for(record.client_name)
        notes = [item for item in (status.detail, status.error) if item]
        if record.enable is None:
            notes.append(i18n.t("cli.tui.adapters.note_enable_missing"))
        first = i18n.t(
            "cli.tui.adapters.detail_config",
            table=record.table or i18n.t("cli.tui.common.unknown"),
            file=record.config_file or i18n.t("cli.tui.adapters.path_unknown"),
        )
        parts = [
            i18n.t(
                "cli.tui.adapters.detail_status",
                label=status.label,
                state=status.state or i18n.t("cli.tui.adapters.peer_no_record"),
            ),
            *notes,
        ]
        if record.legacy_layout:
            parts.append(i18n.t("cli.tui.adapters.detail_legacy_layout"))
        if record.client_name_inferred:
            parts.append(i18n.t("cli.tui.adapters.detail_client_name_inferred"))
        second = i18n.t("cli.tui.common.error_separator").join(parts)
        text = f"{self._fit_page_width(first)}\n{self._fit_page_width(second)}"
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _sync_actions(self) -> None:
        toggle = self.query_one("#toggle", compat.Button)
        toggle.disabled = self._busy or self.selected_record is None
        record = self.selected_record
        self.query_one("#add-instance", compat.Button).disabled = self._busy or record is None
        self.query_one("#remove-instance", compat.Button).disabled = (
            self._busy or record is None or not record.configured
        )
        if record is None:
            toggle.label = i18n.t("cli.tui.adapters.action_toggle")
        elif record.installable:
            toggle.label = i18n.t("cli.tui.adapters.action_install")
        else:
            toggle.label = i18n.t(
                "cli.tui.adapters.action_disable" if record.enabled else "cli.tui.adapters.action_enable"
            )
        self.query_one("#actions", compat.ButtonFlow).relayout()

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:

        if self._snapshot.instances:
            self._render_all()

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        self.reset_pending()
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.ListView.Selected)
    def _on_selected(self, event: compat.ListView.Selected) -> None:
        self.reset_pending()
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "toggle":
            self.request_toggle()
        elif event.button.id == "add-instance":
            self.request_add_instance()
        elif event.button.id == "remove-instance":
            self.request_remove_instance()
        elif event.button.id == "refresh":
            self.refresh_instances(force=True)

    def request_add_instance(self) -> None:
        """使用输入的实例 ID，为所选平台创建实例。"""
        record = self.selected_record
        if record is None:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.pick_platform"),
                severity="warning",
                title=i18n.t("cli.tui.adapters.action_add_instance"),
            )
            return
        # 实例 ID 参与 target_id 前缀，必须由用户指定，创建后不可更改。
        instance_id = self.query_one("#new-instance", compat.Input).value.strip()
        if not instance_id:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.instance_id_required"),
                severity="warning",
                title=i18n.t("cli.tui.adapters.action_add_instance"),
            )
            return
        if not INSTANCE_ID_PATTERN.fullmatch(instance_id):
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.instance_id_invalid", instance_id=instance_id),
                severity="warning",
                title=i18n.t("cli.tui.adapters.action_add_instance"),
            )
            return
        self._start_instance_op(
            i18n.t("cli.tui.adapters.label_instance_add", name=f"{record.platform}/{instance_id}"),
            lambda: self.source.add_instance(record.platform, instance_id),
            clear_input=True,
        )

    def request_remove_instance(self) -> None:
        """请求确认移除实例配置，忽略防抖窗口内的重复请求。"""
        record = self._removal_target()
        if record is None:
            return
        if not self._gate.accept(f"remove:{record.key}"):
            return
        name = self._instance_display(record)
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.adapters.remove_choice_title", name=name),
            hint=i18n.t("cli.tui.adapters.remove_only_hint", name=name),
            options=(("remove", i18n.t("cli.tui.adapters.remove_choice_plain")),),
            cancel_label=i18n.t("cli.tui.adapters.cancel"),
            callback=lambda choice: self.on_remove_chosen(record, choice),
        )

    def on_remove_chosen(self, record: AdapterRecord, choice: str | None) -> None:

        self.reset_pending()
        if choice != "remove":
            self._set_status(i18n.t("cli.tui.adapters.remove_cancelled"))
            return
        self._start_remove(record)

    def reset_pending(self) -> None:
        """作废待确认的移除；切页、刷新与换选中项时调用。"""
        self._gate.reset()

    def _removal_target(self) -> AdapterRecord | None:
        record = self.selected_record
        if record is not None and record.configured:
            return record
        compat.notify(
            self.app,
            i18n.t("cli.tui.adapters.pick_instance"),
            severity="warning",
            title=i18n.t("cli.tui.adapters.action_remove_instance"),
        )
        return None

    def _start_remove(self, record: AdapterRecord) -> None:
        name = self._instance_display(record)
        label = i18n.t("cli.tui.adapters.label_instance_remove", name=name)
        kept = i18n.t("cli.tui.adapters.remove_kept", name=name)

        def remove() -> OperationResult:
            result = self.source.remove_instance(record)
            return replace(result, message=kept) if result.ok else result

        self._start_instance_op(label, remove, clear_input=False)

    def _instance_display(self, record: AdapterRecord) -> str:
        return (
            f"{record.platform}/{record.instance_id}" if record.instance_id else i18n.t("cli.tui.adapters.default_id")
        )

    def _start_instance_op(self, label: str, func: Callable[[], OperationResult], *, clear_input: bool) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._busy = True
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.adapters.calling", label=label))
        self.run_worker(self._instance_op(label, func, clear_input), group="adapters-instance", exclusive=True)

    async def _instance_op(self, label: str, func: Callable[[], OperationResult], clear_input: bool) -> None:
        try:
            result = await asyncio.to_thread(func)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        if result.ok:
            if clear_input:
                self.query_one("#new-instance", compat.Input).value = ""
            self._set_status(i18n.t("cli.tui.adapters.refreshing", message=result.message))
            self.invalidate_cache()
            await self._load()
            self.last_result = result.message
            self._set_status(self.last_result)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.adapters.failed_detail", message=result.message, detail=tail))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def request_toggle(self) -> None:
        """切换所选实例的启用状态；无选中项时显示提示。"""
        record = self.selected_record
        if record is None:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.pick_toggle"),
                severity="warning",
                title="enable",
            )
            return
        if record.installable:
            # 未安装的适配器必须先安装，才能设置启用状态。
            self.request_install()
            return
        self._start_toggle(record, not record.enabled)

    def request_install(self) -> None:
        """安装所选平台的适配器；已安装或无选中项时显示提示。"""
        record = self.selected_record
        if record is None or not record.installable:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.pick_install"),
                severity="warning",
                title=i18n.t("cli.tui.adapters.action_install"),
            )
            return
        self._start_install(record)

    def _start_install(self, record: AdapterRecord) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._busy = True
        self._selected_key = record.key
        self._stream_lines = []
        self._sync_actions()
        label = i18n.t("cli.tui.adapters.label_install", name=record.platform)
        self._set_status(i18n.t("cli.tui.adapters.calling", label=label))
        self.run_worker(self._install(record, label), group="adapters-install", exclusive=True)

    async def _install(self, record: AdapterRecord, label: str) -> None:
        try:
            result = await self.source.stream_install(record, self._on_install_line)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        if result.ok:
            self._set_status(i18n.t("cli.tui.adapters.refreshing", message=result.message))
            self.invalidate_cache()
            await self._load()
            self.last_result = result.message
            self._set_status(self.last_result)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.adapters.failed_detail", message=result.message, detail=tail))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def _on_install_line(self, line: str) -> None:
        # 安装耗时较长，通过实时输出提供进度反馈。
        self._stream_lines.append(line)
        self._set_status(line)

    def _start_toggle(self, record: AdapterRecord, enabled: bool) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.adapters.busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._busy = True
        self._selected_key = record.key
        self._sync_actions()
        label = i18n.t(
            "cli.tui.adapters.label_enable" if enabled else "cli.tui.adapters.label_disable",
            name=record.client_name or record.table,
        )
        self._set_status(i18n.t("cli.tui.adapters.calling", label=label))
        self.run_worker(self._toggle(record, enabled, label), group="adapters-toggle", exclusive=True)

    async def _toggle(self, record: AdapterRecord, enabled: bool, label: str) -> None:
        try:
            result = await asyncio.to_thread(self.source.set_enable, record, enabled)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        if result.ok:
            self._set_status(i18n.t("cli.tui.adapters.refreshing", message=result.message))
            self.invalidate_cache()
            await self._load()
            detail = (
                i18n.t("cli.tui.adapters.detail_wrap", detail=result.detail.splitlines()[-1]) if result.detail else ""
            )
            self.last_result = f"{result.message}{detail}"
            self._set_status(self.last_result)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.adapters.failed_detail", message=result.message, detail=tail))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def focus_primary(self) -> None:
        """聚焦适配器列表；列表为空时聚焦页面容器。"""
        compat.focus_first(self, "#adapter-list")

    def action_refresh(self) -> None:

        self.refresh_instances(force=True)

    def action_install(self) -> None:

        self.request_install()

    def action_add_instance(self) -> None:

        self.request_add_instance()

    def action_remove_instance(self) -> None:

        self.request_remove_instance()

    def action_toggle_enable(self) -> None:

        self.request_toggle()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
