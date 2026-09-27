"""Dashboard 页：本机实例清单 + 当前实例的路径 / core 版本 / 运行状态 / 更新提示。

数据流：界面只读 :class:`DashboardSource`（当前实例的快照）与 :class:`InstanceListSource`（注册表
里的其它实例）。默认实现 :class:`LocalDashboardSource` 先读 ``akaribot.toml``，取不到 core 版本时
再经 ``akaribot module list --json`` 子进程补取，运行状态一律探测实例锁文件 ``.bot.lock``；实例清单
直接读本机注册表，不起子进程。在清单里选中一条并回车即切换当前实例，各页随后的取数都指向它。
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.instances import InstanceRegistry, probe_running
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context

STATE_RUNNING = "running"
STATE_STOPPED = "stopped"
STATE_UNKNOWN = "unknown"

INSTANCE_META_FILENAME = "akaribot.toml"
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"
LOCK_FILENAME = ".bot.lock"

# 状态取值来自锁文件探测，界面按当前语言取标签，故这里只存文案键。
_STATE_KEYS = {
    STATE_RUNNING: "cli.tui.dashboard.state_running",
    STATE_STOPPED: "cli.tui.dashboard.state_stopped",
    STATE_UNKNOWN: "cli.tui.dashboard.state_unknown",
}
_STATE_MARKS = {STATE_RUNNING: "●", STATE_STOPPED: "○", STATE_UNKNOWN: "?"}

CORE_DIST_CANDIDATES = ("akari-bot-core", "akaribot-core", "akaribot", "core")
"""``module list --json`` 中 core 的候选分发名与模块名，比较时大小写不敏感。"""

UPDATE_SOURCE_PENDING_KEY = "cli.tui.dashboard.update_source_pending"
"""更新提示的占位来源说明文案键：探测回调未注入时该行留空并显示本说明。"""


def _pending_update_source() -> str:
    return i18n.t(UPDATE_SOURCE_PENDING_KEY)


@dataclass(frozen=True)
class DashboardSnapshot:
    """Dashboard 的一次快照。

    :param instance_root: 实例根目录的绝对路径。
    :param instance_name: ``[instance] name``。
    :param instance_mode: ``installed`` 或 ``workspace``。
    :param locale: 实例默认语言。
    :param core_version: core 版本号；取不到时为空串。
    :param core_origin: core 版本的来源说明（``akaribot.toml`` 或 ``module list --json``）。
    :param running: 运行状态；``None`` 表示锁文件探测不可用。
    :param running_detail: 运行状态的判据说明，含锁文件路径与降级原因。
    :param update_hint: 更新提示；空串表示无更新提示。
    :param update_source: 更新提示的来源说明。
    :param error: 读取过程中的非致命错误，供界面在末行展示。
    """

    instance_root: str = ""
    instance_name: str = ""
    instance_mode: str = ""
    locale: str = ""
    core_version: str = ""
    core_origin: str = ""
    running: bool | None = None
    running_detail: str = ""
    update_hint: str = ""
    update_source: str = field(default_factory=_pending_update_source)
    error: str = ""

    @property
    def state(self) -> str:
        """把三态运行状态归一到 :data:`STATE_RUNNING` 等取值。"""
        if self.running is None:
            return STATE_UNKNOWN
        return STATE_RUNNING if self.running else STATE_STOPPED

    @property
    def state_label(self) -> str:
        """返回运行状态的本地化标签，带状态标记。"""
        key = _STATE_KEYS.get(self.state)
        return f"{_STATE_MARKS[self.state]} {i18n.t(key) if key else self.state}"


@dataclass(frozen=True)
class InstanceRow:
    """实例清单里的一行。

    :param name: 注册名；未登记的当前实例用空串。
    :param root: 实例根目录。
    :param locale: 实例默认语言。
    :param running: 是否在运行；探测失败时为 ``None``。
    :param autostart: 是否随服务启动而拉起。
    :param restart_on_crash: 崩溃后是否自动重启。
    :param registered: 是否已在注册表里。
    """

    name: str
    root: Path
    locale: str = ""
    running: bool | None = False
    autostart: bool = False
    restart_on_crash: bool = False
    registered: bool = True

    @property
    def state_label(self) -> str:
        """返回运行状态的本地化标签。"""
        key = _STATE_KEYS.get(STATE_RUNNING if self.running else STATE_STOPPED)
        mark = _STATE_MARKS[STATE_RUNNING if self.running else STATE_STOPPED]
        return f"{mark} {i18n.t(key) if key else ''}".strip()

    def marks(self) -> str:
        """返回策略标记：自启与崩溃重启。"""
        marks: list[str] = []
        if self.autostart:
            marks.append(i18n.t("cli.tui.dashboard.mark_autostart"))
        if self.restart_on_crash:
            marks.append(i18n.t("cli.tui.dashboard.mark_crash_restart"))
        return " ".join(marks)


@dataclass(frozen=True)
class ServiceRow:
    """服务状态的一行摘要。

    :param backend: ``launchd`` / ``systemd`` / ``unsupported``。
    :param installed: 单元文件是否存在。
    :param enabled: 系统是否已注册；探测不到时为 ``None``。
    :param path: 单元文件路径。
    :param detail: 面向用户的一句话说明。
    """

    backend: str = ""
    installed: bool = False
    enabled: bool | None = None
    path: Path | None = None
    detail: str = ""


@runtime_checkable
class ServiceControl(Protocol):
    """服务安装状态与装卸动作。"""

    def service_status(self) -> ServiceRow:
        """返回服务单元状态。"""

    def install_service(self) -> ServiceRow:
        """安装并注册服务。"""

    def uninstall_service(self) -> ServiceRow:
        """注销并删除服务单元。"""


class SystemServiceControl:
    """默认实现：直接用 CLI 侧的 service 模块，界面不自己拼单元文件。

    :param backend: 服务后端；缺省按平台探测。
    """

    def __init__(self, backend: Any | None = None) -> None:
        self._backend = backend

    def _service(self) -> Any:
        if self._backend is not None:
            return self._backend
        from akaribot.cli import service

        return service.ServiceBackend()

    @staticmethod
    def _row(status: Any) -> ServiceRow:
        return ServiceRow(
            backend=str(status.backend),
            installed=bool(status.installed),
            enabled=status.enabled,
            path=status.path,
            detail=str(status.detail),
        )

    def service_status(self) -> ServiceRow:
        """见 :meth:`ServiceControl.service_status`。"""
        return self._row(self._service().status())

    def install_service(self) -> ServiceRow:
        """见 :meth:`ServiceControl.install_service`。"""
        return self._row(self._service().install(force=True))

    def uninstall_service(self) -> ServiceRow:
        """见 :meth:`ServiceControl.uninstall_service`。"""
        return self._row(self._service().uninstall())


class StaticServiceControl:
    """固定服务状态的替身，供自动化断言使用。

    :param status: ``service_status`` 的返回值。
    :param result: 安装 / 卸载后的返回值；缺省按动作推出一个合理状态。
    """

    def __init__(self, status: ServiceRow | None = None, *, result: ServiceRow | None = None) -> None:
        self._status = status or ServiceRow(backend="launchd", installed=False)
        self._result = result
        self.calls = {"status": 0, "install": 0, "uninstall": 0}

    def service_status(self) -> ServiceRow:
        """见 :meth:`ServiceControl.service_status`。"""
        self.calls["status"] += 1
        return self._status

    def install_service(self) -> ServiceRow:
        """见 :meth:`ServiceControl.install_service`。"""
        self.calls["install"] += 1
        self._status = self._result or replace(self._status, installed=True, enabled=True, path=Path("/tmp/agent"))
        return self._status

    def uninstall_service(self) -> ServiceRow:
        """见 :meth:`ServiceControl.uninstall_service`。"""
        self.calls["uninstall"] += 1
        self._status = self._result or replace(self._status, installed=False, enabled=False)
        return self._status


@runtime_checkable
class InstanceListSource(Protocol):
    """本机实例清单的数据源接口。"""

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """返回注册表里的实例，附带实时运行状态。"""

    def add_instance(self, root: Path, *, name: str | None = None) -> InstanceRow:
        """登记一个实例。"""

    def remove_instance(self, name: str) -> bool:
        """删除一条登记。"""

    def set_policy(self, name: str, **fields: object) -> InstanceRow:
        """改写实例策略（自启 / 崩溃重启）。"""


class RegistryInstanceListSource:
    """默认实现：读本机注册表，逐条探测锁文件。

    :param registry: 注册表；缺省用默认位置。
    :param probe: 探测运行状态的函数 ``(root) -> bool | None``，测试可注入。
    """

    def __init__(
        self,
        registry: Any | None = None,
        *,
        probe: Callable[[Path], bool | None] | None = None,
    ) -> None:
        self.registry = registry if registry is not None else InstanceRegistry()
        self.calls = {"list": 0, "add": 0, "remove": 0, "policy": 0}
        self._probe = probe or probe_running

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """见 :meth:`InstanceListSource.list_instances`。"""
        self.calls["list"] += 1
        rows: list[InstanceRow] = []
        for entry in self.registry.load():
            rows.append(
                InstanceRow(
                    name=entry.name,
                    root=entry.root,
                    locale=entry.locale,
                    running=self._probe(entry.root),
                    autostart=entry.autostart,
                    restart_on_crash=entry.restart_on_crash,
                )
            )
        active = context.active_root()
        if active is not None and self.registry.find_by_root(active) is None:
            # 正在管理的实例可能没登记过（比如站在实例目录里直接启动界面），也要出现在清单里。
            rows.append(InstanceRow(name="", root=active, running=self._probe(active), registered=False))
        return tuple(rows)

    def add_instance(self, root: Path, *, name: str | None = None) -> InstanceRow:
        """见 :meth:`InstanceListSource.add_instance`。"""
        self.calls["add"] += 1
        entry = self.registry.add(root, name=name)
        return InstanceRow(
            name=entry.name,
            root=entry.root,
            locale=entry.locale,
            running=self._probe(entry.root),
            autostart=entry.autostart,
            restart_on_crash=entry.restart_on_crash,
        )

    def remove_instance(self, name: str) -> bool:
        """见 :meth:`InstanceListSource.remove_instance`。"""
        self.calls["remove"] += 1
        return self.registry.remove(name)

    def set_policy(self, name: str, **fields: object) -> InstanceRow:
        """见 :meth:`InstanceListSource.set_policy`。"""
        self.calls["policy"] += 1
        entry = self.registry.update(name, **fields)
        return InstanceRow(
            name=entry.name,
            root=entry.root,
            locale=entry.locale,
            running=self._probe(entry.root),
            autostart=entry.autostart,
            restart_on_crash=entry.restart_on_crash,
        )


class StaticInstanceListSource:
    """固定清单的替身数据源，供自动化断言使用。

    :param rows: 清单内容。
    """

    def __init__(self, rows: Sequence[InstanceRow] = ()) -> None:
        self._rows = list(rows)
        self.calls = {"list": 0, "add": 0, "remove": 0, "policy": 0}
        self.added: list[str] = []
        self.removed: list[str] = []
        self.policies: list[tuple[str, dict[str, object]]] = []

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """见 :meth:`InstanceListSource.list_instances`。"""
        self.calls["list"] += 1
        return tuple(self._rows)

    def add_instance(self, root: Path, *, name: str | None = None) -> InstanceRow:
        """见 :meth:`InstanceListSource.add_instance`。"""
        self.calls["add"] += 1
        self.added.append(str(root))
        row = InstanceRow(name=name or "added", root=Path(root), registered=True)
        self._rows.append(row)
        return row

    def remove_instance(self, name: str) -> bool:
        """见 :meth:`InstanceListSource.remove_instance`。"""
        self.calls["remove"] += 1
        self.removed.append(name)
        self._rows = [row for row in self._rows if row.name != name]
        return True

    def set_policy(self, name: str, **fields: object) -> InstanceRow:
        """见 :meth:`InstanceListSource.set_policy`。"""
        self.calls["policy"] += 1
        self.policies.append((name, dict(fields)))
        updated: list[InstanceRow] = []
        result: InstanceRow | None = None
        for row in self._rows:
            if row.name == name:
                row = replace(row, **fields)  # type: ignore[arg-type]
                result = row
            updated.append(row)
        self._rows = updated
        return result or InstanceRow(name=name, root=Path("/tmp"), registered=False)


def resolve_instance_root(start: Path | None = None) -> Path | None:
    """定位实例根，供三页的默认数据源共用。

    :param start: 查找起点，缺省为当前工作目录。
    :return: 含 ``akaribot.toml`` 的实例根；未找到时为 ``None``。
    """
    try:
        from akaribot.cli.instance import find_instance_root
    except ImportError:
        candidate = Path(os.environ.get(INSTANCE_DIR_ENV) or (start or Path.cwd())).expanduser()
        return candidate.resolve() if (candidate / INSTANCE_META_FILENAME).is_file() else None
    return find_instance_root(start)


def lock_held(lock_path: Path) -> bool | None:
    """探测锁文件是否被排他锁持有，供 Dashboard 与 Run 两页共用。

    只读打开文件，不截断运行中进程持有的锁；``Instance.is_running()`` 不可用时作为兜底实现。

    :param lock_path: 锁文件路径，通常是 ``<实例根>/.bot.lock``。
    :return: ``True`` 运行中、``False`` 未运行、``None`` 平台或权限不支持探测。
    """
    if not lock_path.exists():
        return False
    try:
        handle = lock_path.open("rb")
    except OSError:
        return None
    with handle:
        try:
            if os.name == "nt":
                import msvcrt

                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError:
                    return True
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                return False
            import fcntl

            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False
        except Exception:  # noqa: BLE001 - 探测失败按未知处理，不应中断界面
            return None


def meta_core_version(doc: Any) -> str:
    """从 ``akaribot.toml`` 的候选位置取 core 版本，缺失时返回空串。"""
    for section, key in (("core", "version"), ("instance", "core_version"), ("runtime", "core_version")):
        table = doc.get(section) if isinstance(doc, Mapping) else None
        if isinstance(table, Mapping):
            value = table.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


@runtime_checkable
class DashboardSource(Protocol):
    """Dashboard 数据源接口；测试注入替身，生产走文件系统与子进程。"""

    def snapshot(self) -> DashboardSnapshot:
        """返回一次完整快照（含较贵的版本查询）。"""

    def probe_running(self) -> bool | None:
        """只探测运行状态，代价须与读一个锁文件相当。"""


class StaticDashboardSource:
    """固定快照的替身数据源，不产生任何子进程与文件访问。

    :param snapshot: 初始快照；缺省给一份合成实例。
    :param running: 初始运行状态；为 ``None`` 时沿用快照自身的取值，构造后可经
        :meth:`set_running` 改成 ``True`` / ``False`` / ``None`` 以断言界面随之变化。
    """

    def __init__(
        self,
        snapshot: DashboardSnapshot | None = None,
        *,
        running: bool | None = None,
    ) -> None:
        base = snapshot or DashboardSnapshot(
            instance_root="/tmp/fake-instance",
            instance_name="fake",
            instance_mode="installed",
            locale="zh_cn",
            core_version="9.9.9",
            core_origin="stub",
            running=False,
            update_hint="",
        )
        self._snapshot = replace(base, running=base.running if running is None else running)
        self.calls = {"snapshot": 0, "probe": 0}

    def snapshot(self) -> DashboardSnapshot:
        """见 :meth:`DashboardSource.snapshot`。"""
        self.calls["snapshot"] += 1
        return self._snapshot

    def probe_running(self) -> bool | None:
        """见 :meth:`DashboardSource.probe_running`。"""
        self.calls["probe"] += 1
        return self._snapshot.running

    def set_running(self, value: bool | None) -> None:
        """改写替身的运行状态，模拟实例启停。"""
        self._snapshot = replace(self._snapshot, running=value)

    def set_snapshot(self, snapshot: DashboardSnapshot) -> None:
        """整份替换替身快照，模拟实例重建或版本变化。"""
        self._snapshot = snapshot


class LocalDashboardSource:
    """默认数据源：文件系统 + 子进程，CLI 进程内不 import core。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param start: 向上查找的起点，缺省为当前工作目录。
    :param timeout: 子进程超时秒数，仅在需要补取版本时使用。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: 构造 ``Instance`` 的回调，测试可注入以避开 T5.1 的实现。
    :param module_source: 取版本用的模块数据源；缺省复用 Modules 页的子进程实现。
    :param update_probe: 返回更新提示的回调；未注入时更新提示留空。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        start: Path | str | None = None,
        timeout: float = 60.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        instance_factory: Callable[[Path], Any] | None = None,
        module_source: Any | None = None,
        update_probe: Callable[[], str] | None = None,
    ) -> None:
        self.root = Path(root) if root is not None else None
        self.start = Path(start) if start is not None else None
        self.timeout = timeout
        self.calls = {"snapshot": 0, "probe": 0}
        self.last_error = ""
        self.last_probe_error = ""
        self._runner = runner
        self._instance_factory = instance_factory
        self._module_source = module_source
        self._update_probe = update_probe

    def snapshot(self) -> DashboardSnapshot:
        """见 :meth:`DashboardSource.snapshot`。"""
        self.calls["snapshot"] += 1
        root = self._root()
        if root is None:
            self.last_error = i18n.t(
                "cli.tui.dashboard.src_no_instance",
                path=self._origin_text(),
                meta=INSTANCE_META_FILENAME,
            )
            return DashboardSnapshot(instance_root=self._origin_text(), error=self.last_error)
        fields, meta_error = self._read_meta(root)
        version = fields.pop("core_version", "")
        origin = INSTANCE_META_FILENAME if version else ""
        if not version:
            version, origin = self._version_from_cli(root)
        hint, hint_source = self._update_hint()
        self.last_error = meta_error
        return DashboardSnapshot(
            instance_root=str(root),
            instance_name=fields.get("name", ""),
            instance_mode=fields.get("mode", ""),
            locale=fields.get("locale", ""),
            core_version=version,
            core_origin=origin,
            running=self.probe_running(),
            running_detail=self._running_detail(root),
            update_hint=hint,
            update_source=hint_source,
            error=meta_error,
        )

    def probe_running(self) -> bool | None:
        """见 :meth:`DashboardSource.probe_running`：只读锁文件，不起子进程。"""
        self.calls["probe"] += 1
        self.last_probe_error = ""
        root = self._root()
        if root is None:
            self.last_probe_error = i18n.t("cli.tui.dashboard.src_root_unknown")
            return None
        instance = self._instance(root)
        if instance is not None:
            try:
                return bool(instance.is_running())
            except Exception as error:  # noqa: BLE001 - 降级到本地锁探测，不中断界面
                self.last_probe_error = i18n.t(
                    "cli.tui.dashboard.src_probe_failed", kind=type(error).__name__, error=error
                )
        return lock_held(root / LOCK_FILENAME)

    def _root(self) -> Path | None:
        if self.root is not None:
            return self.root
        return resolve_instance_root(self.start)

    def _origin_text(self) -> str:
        return str(self.root or self.start or Path.cwd())

    def _instance(self, root: Path) -> Any | None:
        if self._instance_factory is not None:
            try:
                return self._instance_factory(root)
            except Exception as error:  # noqa: BLE001 - 替身失败同样只降级
                self.last_probe_error = i18n.t(
                    "cli.tui.dashboard.src_stub_failed", kind=type(error).__name__, error=error
                )
                return None
        try:
            from akaribot.cli.instance import Instance
        except ImportError as error:
            self.last_probe_error = i18n.t("cli.tui.dashboard.src_instance_unavailable", error=error)
            return None
        try:
            return Instance(root)
        except Exception as error:  # noqa: BLE001 - 实例构造失败只作为降级原因
            self.last_probe_error = i18n.t(
                "cli.tui.dashboard.src_instance_failed", kind=type(error).__name__, error=error
            )
            return None

    def _read_meta(self, root: Path) -> tuple[dict[str, str], str]:
        try:
            from akaribot.cli.instance import InstanceMeta
        except ImportError as error:
            return {}, i18n.t("cli.tui.dashboard.src_instance_unavailable", error=error)
        try:
            meta = InstanceMeta.load(root)
        except Exception as error:  # noqa: BLE001 - 元数据失败不应让整页空白
            return {}, i18n.t(
                "cli.tui.dashboard.src_meta_read_failed",
                file=INSTANCE_META_FILENAME,
                kind=type(error).__name__,
                error=error,
            )
        return {
            "name": meta.name,
            "mode": meta.mode,
            "locale": meta.locale,
            "core_version": meta_core_version(meta.doc),
        }, ""

    def _version_from_cli(self, root: Path) -> tuple[str, str]:
        source = self._resolve_module_source(root)
        if source is None:
            return "", i18n.t("cli.tui.dashboard.src_modules_unavailable")
        try:
            records = source.list_modules()
        except Exception as error:  # noqa: BLE001 - 失败只写入来源说明
            return "", i18n.t("cli.tui.dashboard.src_list_failed", kind=type(error).__name__, error=error)
        candidates = {name.casefold() for name in CORE_DIST_CANDIDATES}
        for record in records:
            names = {record.name.casefold(), record.dist.casefold()}
            if names & candidates:
                return record.version or "", "module list --json"
        return "", i18n.t("cli.tui.dashboard.src_no_core_record")

    def _resolve_module_source(self, root: Path) -> Any | None:
        if self._module_source is not None:
            return self._module_source
        try:
            from akaribot.cli.tui.modules import SubprocessModuleSource
        except ImportError:
            return None
        return SubprocessModuleSource(
            root=root,
            timeout=self.timeout,
            runner=self._runner,
            instance_factory=(lambda: self._instance_factory(root)) if self._instance_factory else None,
        )

    def _update_hint(self) -> tuple[str, str]:
        if self._update_probe is None:
            return "", _pending_update_source()
        try:
            hint = str(self._update_probe() or "").strip()
        except Exception as error:  # noqa: BLE001 - 探测失败不影响其余字段
            return "", i18n.t("cli.tui.dashboard.src_probe_callback_failed", kind=type(error).__name__, error=error)
        if not hint:
            return "", i18n.t("cli.tui.dashboard.update_source_probe_no_hint", source=_pending_update_source())
        return hint, i18n.t("cli.tui.dashboard.update_source_probe")

    def _running_detail(self, root: Path) -> str:
        text = i18n.t("cli.tui.dashboard.running_detail_lock", path=str(root / LOCK_FILENAME))
        if self.last_probe_error:
            text = f"{text}{i18n.t('cli.tui.common.error_separator')}{self.last_probe_error}"
        return text


class DashboardPage(compat.Vertical):
    """Dashboard 页控件。

    :param source: 数据源，缺省为 :class:`LocalDashboardSource`。
    :param cache_ttl: 快照缓存有效期（秒）；缓存内刷新只重绘，不取版本。
    :param refresh_interval: 锁文件探测周期（秒）；自动化断言可调大以避免定时刷新干扰。
    """

    DEFAULT_CSS = """
    DashboardPage {
        layout: vertical;
        height: 1fr;
    }
    DashboardPage #instances-caption {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DashboardPage #instance-list {
        height: 8;
        min-height: 4;
        border: round $panel;
    }
    DashboardPage #instance-list > ListItem {
        padding: 0 1;
    }
    DashboardPage #instance-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DashboardPage #service {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DashboardPage #fields-pane {
        height: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    DashboardPage #fields {
        width: 1fr;
    }
    DashboardPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    DashboardPage #status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    # 文案在类创建时取值：main.py 的 --lang 早于界面模块导入，改语言需重启进程。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.dashboard.bind_refresh")),
        ("s", "switch_instance", i18n.t("cli.tui.dashboard.bind_switch")),
        ("a", "toggle_autostart", i18n.t("cli.tui.dashboard.bind_autostart")),
        ("c", "toggle_crash_restart", i18n.t("cli.tui.dashboard.bind_crash_restart")),
        ("n", "add_instance", i18n.t("cli.tui.dashboard.bind_add_instance")),
        ("d", "remove_instance", i18n.t("cli.tui.dashboard.bind_remove_instance")),
        ("i", "toggle_service", i18n.t("cli.tui.dashboard.bind_service")),
    )

    can_focus = True

    def __init__(
        self,
        source: DashboardSource | None = None,
        *,
        instances: InstanceListSource | None = None,
        service_control: ServiceControl | None = None,
        cache_ttl: float = 5.0,
        refresh_interval: float = 2.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DashboardSource = source if source is not None else LocalDashboardSource()
        self.instances: InstanceListSource = instances if instances is not None else RegistryInstanceListSource()
        self.service_control: ServiceControl = (
            service_control if service_control is not None else SystemServiceControl()
        )
        self._service = ServiceRow()
        self._service_text = ""
        self._pending_service = ""
        self._instance_rows: tuple[InstanceRow, ...] = ()
        self._pending_remove: str = ""
        self.cache_ttl = cache_ttl
        self.refresh_interval = refresh_interval
        self.last_error: str = ""
        self._snapshot = DashboardSnapshot()
        self._loaded_at: float = 0.0
        self._rows: tuple[tuple[str, str], ...] = ()
        self._fields_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：实例清单 + 当前实例的字段 + 操作与状态栏。"""
        yield compat.Static(i18n.t("cli.tui.dashboard.instances_caption"), id="instances-caption", markup=False)
        yield compat.Static("", id="service", markup=False)
        yield compat.ListView(id="instance-list")
        with compat.VerticalScroll(id="fields-pane"):
            yield compat.Static(i18n.t("cli.tui.dashboard.fields_placeholder"), id="fields", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.dashboard.action_refresh"), id="refresh", variant="primary")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；取数与周期探测推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取快照，并按周期探测锁文件。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_snapshot(force=True)
        self.refresh_instances()
        self.refresh_service()
        if self.refresh_interval and self.refresh_interval > 0:
            self.set_interval(self.refresh_interval, self._on_tick)

    def focus_primary(self) -> None:
        """把焦点交给实例清单；清单为空时退到页面容器。"""
        compat.focus_first(self, "#instance-list")

    @property
    def instance_rows(self) -> tuple[InstanceRow, ...]:
        """返回最近一次读取到的实例清单。"""
        return self._instance_rows

    def refresh_instances(self) -> None:
        """重新读取本机实例清单并重绘。"""
        try:
            rows = tuple(self.instances.list_instances())
        except Exception as error:  # noqa: BLE001 - 注册表不可用只降级为一句提示
            self._instance_rows = ()
            self._render_instances()
            self._set_status(i18n.t("cli.tui.dashboard.instances_failed", error=f"{type(error).__name__}: {error}"))
            return
        self._instance_rows = rows
        self._render_instances()

    def selected_instance(self) -> InstanceRow | None:
        """返回清单里当前高亮的那条记录。"""
        if not self._instance_rows:
            return None
        try:
            list_view = self.query_one("#instance-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(self._instance_rows):
            return None
        return self._instance_rows[index]

    def _render_instances(self) -> None:
        list_view = self.query_one("#instance-list", compat.ListView)
        active = context.active_root()
        rows: list[str] = []
        for row in self._instance_rows:
            current = "▸" if active is not None and row.root == active else " "
            name = row.name or i18n.t("cli.tui.dashboard.instance_unregistered")
            marks = row.marks()
            text = f"{current} {name}  {row.state_label}  {row.root}"
            if marks:
                text = f"{text}  {marks}"
            if not (row.root / INSTANCE_META_FILENAME).is_file():
                text = f"{text}  {i18n.t('cli.tui.dashboard.instance_missing')}"
            rows.append(compat.fit_cells(text, self._instance_width(list_view)))
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(row, markup=False)) for row in rows])
        list_view.index = self._index_of_active()
        self.query_one("#instances-caption", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.dashboard.instances_caption_with_count", count=len(rows)))
        )

    def _index_of_active(self) -> int | None:
        active = context.active_root()
        if active is None or not self._instance_rows:
            return 0 if self._instance_rows else None
        for index, row in enumerate(self._instance_rows):
            if row.root == active:
                return index
        return 0

    def _instance_width(self, list_view: compat.ListView) -> int:
        try:
            return max(compat.widget_cells(list_view)[0] - 4, 16)
        except Exception:  # noqa: BLE001 - 未完成布局时按保守宽度排版
            return 72

    def switch_to_selected(self) -> None:
        """把当前实例切换为清单里高亮的那条。"""
        row = self.selected_instance()
        if row is None:
            self._set_status(i18n.t("cli.tui.dashboard.switch_no_selection"))
            return
        if not (row.root / INSTANCE_META_FILENAME).is_file():
            self._set_status(i18n.t("cli.tui.dashboard.switch_missing", root=row.root))
            return
        switch = getattr(self.app, "switch_instance", None)
        if not callable(switch):
            self._set_status(i18n.t("cli.tui.dashboard.switch_unsupported"))
            return
        switch(row.root)
        self._set_status(i18n.t("cli.tui.dashboard.switch_done", name=row.name or str(row.root)))

    def toggle_policy(self, field_name: str) -> None:
        """翻转当前实例的自启 / 崩溃重启策略。

        :param field_name: ``autostart`` 或 ``restart_on_crash``。
        """
        row = self.selected_instance()
        if row is None:
            self._set_status(i18n.t("cli.tui.dashboard.switch_no_selection"))
            return
        if not row.registered:
            self._set_status(i18n.t("cli.tui.dashboard.policy_unregistered", root=row.root))
            return
        wanted = not (row.autostart if field_name == "autostart" else row.restart_on_crash)
        try:
            self.instances.set_policy(row.name, **{field_name: wanted})
        except Exception as error:  # noqa: BLE001 - 策略写入失败只报错，不改界面状态
            self._set_status(i18n.t("cli.tui.dashboard.policy_failed", error=f"{type(error).__name__}: {error}"))
            return
        self.refresh_instances()
        key = "policy_autostart_on" if wanted else "policy_autostart_off"
        if field_name != "autostart":
            key = "policy_crash_on" if wanted else "policy_crash_off"
        self._set_status(i18n.t(f"cli.tui.dashboard.{key}", name=row.name))

    @property
    def service_row(self) -> ServiceRow:
        """返回最近一次读到的服务状态。"""
        return self._service

    def refresh_service(self) -> None:
        """读取服务单元状态并重绘那一行。"""
        try:
            self._service = self.service_control.service_status()
        except Exception as error:  # noqa: BLE001 - 服务状态读不到只降级为一句说明
            self._service = ServiceRow(detail=f"{type(error).__name__}: {error}")
        self._render_service()

    def _render_service(self) -> None:
        row = self._service
        if row.backend == "unsupported":
            text = i18n.t("cli.tui.dashboard.service_unsupported", detail=row.detail)
        elif row.installed:
            state = (
                i18n.t("cli.tui.dashboard.service_enabled")
                if row.enabled
                else i18n.t("cli.tui.dashboard.service_registered_unknown")
                if row.enabled is None
                else i18n.t("cli.tui.dashboard.service_disabled")
            )
            text = i18n.t(
                "cli.tui.dashboard.service_installed",
                backend=row.backend,
                state=state,
                path=row.path or "-",
            )
        else:
            text = i18n.t("cli.tui.dashboard.service_missing", backend=row.backend)
        # 首次激活时页面还没完成布局，宽度取不到；这里只存原文，截断按当前宽度在重绘时进行。
        self._service_text = text
        self.query_one("#service", compat.Static).update(
            compat.plain_text(compat.truncate_cells(text, self._inner_width()))
        )

    def request_toggle_service(self) -> None:
        """安装或卸载常驻服务；连按两次同一个动作才执行。

        安装会往系统里写一个自启单元，卸载会注销它，故都要求再按一次确认；确认文案里带上单元
        文件路径，用户知道到底动了什么。
        """
        row = self._service
        action = "uninstall" if row.installed else "install"
        if self._pending_service != action:
            self._pending_service = action
            key = "cli.tui.dashboard.service_confirm_remove" if action == "uninstall" else "service_confirm_add"
            self._set_status(i18n.t(f"cli.tui.dashboard.{key}", path=row.path or "-"))
            return
        self._pending_service = ""
        self._start_service(action)

    def _start_service(self, action: str) -> None:
        self._set_status(i18n.t(f"cli.tui.dashboard.service_calling_{action}"))
        self.run_worker(self._service_op(action), group="dashboard-service", exclusive=True)

    async def _service_op(self, action: str) -> None:
        call = self.service_control.uninstall_service if action == "uninstall" else self.service_control.install_service
        try:
            row = await asyncio.to_thread(call)
        except Exception as error:  # noqa: BLE001 - 装卸失败只报错，不改界面状态
            self._set_status(i18n.t("cli.tui.dashboard.service_failed", error=f"{type(error).__name__}: {error}"))
            return
        self._service = row
        self._render_service()
        key = "service_removed" if action == "uninstall" else "service_added"
        self._set_status(i18n.t(f"cli.tui.dashboard.{key}", path=row.path or "-"))

    def action_toggle_service(self) -> None:
        """键位动作：安装或卸载常驻服务。"""
        self.request_toggle_service()

    def request_add_instance(self) -> None:
        """弹出输入框要实例目录，登记进本机注册表。"""
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.dashboard.add_title"),
            hint=i18n.t("cli.tui.dashboard.add_hint"),
            placeholder=i18n.t("cli.tui.dashboard.add_placeholder"),
            confirm_label=i18n.t("cli.tui.dashboard.add_confirm"),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=self.on_instance_path_entered,
        )

    def on_instance_path_entered(self, path: str | None) -> None:
        """输入框回调：登记用户填写的实例目录。

        :param path: 用户输入的路径；取消时为 ``None``。
        """
        if not path:
            self._set_status(i18n.t("cli.tui.dashboard.add_cancelled"))
            return
        try:
            row = self.instances.add_instance(Path(path).expanduser())
        except Exception as error:  # noqa: BLE001 - 目录不是实例等原因照实展示
            self._set_status(i18n.t("cli.tui.dashboard.add_failed", error=error))
            return
        self.refresh_instances()
        self._set_status(i18n.t("cli.tui.dashboard.add_done", name=row.name, root=row.root))

    def request_remove_instance(self) -> None:
        """移除清单里高亮实例的登记；连按两次才执行，实例目录本身不动。"""
        row = self.selected_instance()
        if row is None:
            self._set_status(i18n.t("cli.tui.dashboard.switch_no_selection"))
            return
        if not row.registered:
            self._set_status(i18n.t("cli.tui.dashboard.policy_unregistered", root=row.root))
            return
        if self._pending_remove != row.name:
            self._pending_remove = row.name
            self._set_status(i18n.t("cli.tui.dashboard.remove_confirm", name=row.name, root=row.root))
            return
        self._pending_remove = ""
        try:
            removed = self.instances.remove_instance(row.name)
        except Exception as error:  # noqa: BLE001 - 移除失败只报错
            self._set_status(i18n.t("cli.tui.dashboard.remove_failed", error=f"{type(error).__name__}: {error}"))
            return
        self.refresh_instances()
        self._set_status(
            i18n.t("cli.tui.dashboard.remove_done", name=row.name)
            if removed
            else i18n.t("cli.tui.dashboard.remove_missing", name=row.name)
        )

    def action_switch_instance(self) -> None:
        """键位动作：切换到清单里高亮的实例。"""
        self.switch_to_selected()

    def action_toggle_autostart(self) -> None:
        """键位动作：翻转开机自启。"""
        self.toggle_policy("autostart")

    def action_toggle_crash_restart(self) -> None:
        """键位动作：翻转崩溃重启。"""
        self.toggle_policy("restart_on_crash")

    def action_add_instance(self) -> None:
        """键位动作：登记一个实例目录。"""
        self.request_add_instance()

    def action_remove_instance(self) -> None:
        """键位动作：移除实例登记。"""
        self.request_remove_instance()

    # region 状态读取（供测试与上层使用）

    @property
    def snapshot(self) -> DashboardSnapshot:
        """返回缓存中的快照，不触发取数。"""
        return self._snapshot

    @property
    def rows(self) -> tuple[tuple[str, str], ...]:
        """返回最近一次渲染使用的标签与值，供自动化断言逐字段核对。"""
        return self._rows

    @property
    def fields_text(self) -> str:
        """返回信息面板当前渲染出的纯文本。"""
        return self._fields_rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    def cache_age(self) -> float:
        """返回快照自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    # endregion

    # region 数据读取

    def refresh_snapshot(self, *, force: bool = False) -> None:
        """读取快照。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不取数。
        """
        if not force and self._loaded_at and self.cache_age() < self.cache_ttl:
            self._render_fields()
            self._set_status(i18n.t("cli.tui.dashboard.status_cached", age=f"{self.cache_age():.1f}"))
            return
        self._set_status(i18n.t("cli.tui.dashboard.status_loading"))
        self.run_worker(self._load_snapshot(), group="dashboard-load", exclusive=True)

    async def _load_snapshot(self) -> bool:
        try:
            snapshot = await asyncio.to_thread(self.source.snapshot)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._snapshot = DashboardSnapshot(error=self.last_error)
            self._render_fields()
            self._set_status(i18n.t("cli.tui.dashboard.status_load_failed", error=self.last_error))
            return False
        self._snapshot = snapshot
        self._loaded_at = time.monotonic()
        self.last_error = snapshot.error
        self._render_fields()
        if snapshot.error:
            self._set_status(i18n.t("cli.tui.dashboard.status_partial_failed", error=snapshot.error))
        else:
            self._set_status(i18n.t("cli.tui.dashboard.status_updated", time=time.strftime("%H:%M:%S")))
        return True

    def refresh_running(self) -> bool | None:
        """只探测运行状态并就地更新该行，返回探测结果。

        判据与 :meth:`DashboardSource.probe_running` 一致：读锁文件或询问实例对象，
        不起子进程、不重取版本；探测结果与缓存相同时不重绘。
        """
        try:
            value = self.source.probe_running()
        except Exception as error:  # noqa: BLE001 - 探测失败按未知展示
            self.last_error = f"{type(error).__name__}: {error}"
            self._set_status(i18n.t("cli.tui.dashboard.status_probe_failed", error=self.last_error))
            return None
        if value != self._snapshot.running:
            self._snapshot = replace(self._snapshot, running=value)
            self._render_fields()
        detail = self._snapshot.running_detail or i18n.t("cli.tui.dashboard.running_detail_fallback")
        self._set_status(i18n.t("cli.tui.dashboard.status_running", state=self._snapshot.state_label, detail=detail))
        return value

    def _on_tick(self) -> None:
        if not self.display:
            return
        self.refresh_running()
        self.refresh_instances()

    # endregion

    # region 渲染（只读缓存）

    def _render_fields(self) -> None:
        snapshot = self._snapshot
        rows = [
            (
                i18n.t("cli.tui.dashboard.field_instance_root"),
                snapshot.instance_root or i18n.t("cli.tui.common.unknown"),
            ),
            (
                i18n.t("cli.tui.dashboard.field_instance_name"),
                snapshot.instance_name or i18n.t("cli.tui.common.unknown"),
            ),
            (i18n.t("cli.tui.dashboard.field_mode"), _mode_text(snapshot)),
            (
                i18n.t("cli.tui.dashboard.field_core_version"),
                snapshot.core_version or i18n.t("cli.tui.dashboard.value_version_missing"),
            ),
            (i18n.t("cli.tui.dashboard.field_core_origin"), snapshot.core_origin or i18n.t("cli.tui.common.unknown")),
            (i18n.t("cli.tui.dashboard.field_state"), snapshot.state_label),
            (
                i18n.t("cli.tui.dashboard.field_running_detail"),
                snapshot.running_detail or i18n.t("cli.tui.common.unknown"),
            ),
            (
                i18n.t("cli.tui.dashboard.field_update_hint"),
                snapshot.update_hint or i18n.t("cli.tui.dashboard.value_no_hint"),
            ),
        ]
        self._rows = tuple(rows)
        lines = compat.align_rows(rows, gap=2)
        lines.append("")
        lines.append(i18n.t("cli.tui.dashboard.update_source_line", source=snapshot.update_source))
        if snapshot.error:
            lines.append(i18n.t("cli.tui.dashboard.warning_line", error=snapshot.error))
        lines.append(
            i18n.t(
                "cli.tui.dashboard.fields_hint",
                refresh=i18n.t("cli.tui.dashboard.bind_refresh"),
            )
        )
        width = self._inner_width()
        if width > 0:
            lines = [compat.truncate_cells(line, width) for line in lines]
        text = "\n".join(lines)
        self._fields_rendered = text
        self.query_one("#fields", compat.Static).update(compat.plain_text(text))

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        if outer < 8:
            # 首次激活时页面尚未布局，宽度还是 0；按保守值排版，布局完成后的 resize 会重排。
            return 72
        return max(outer - 6, 16)

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        self._render_fields()
        self._render_service()

    # endregion

    # region 交互

    @compat.on(compat.Button.Pressed)
    @compat.on(compat.ListView.Selected, "#instance-list")
    def _on_instance_selected(self, event: compat.ListView.Selected) -> None:
        self.switch_to_selected()

    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "refresh":
            self.refresh_snapshot(force=True)

    def action_refresh(self) -> None:
        """键位动作：强制重新读取快照。"""
        self.refresh_snapshot(force=True)

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()


def _mode_text(snapshot: DashboardSnapshot) -> str:
    mode = snapshot.instance_mode or i18n.t("cli.tui.common.unknown")
    if not snapshot.locale:
        return mode
    return i18n.t("cli.tui.dashboard.mode_with_locale", mode=mode, locale=snapshot.locale)
