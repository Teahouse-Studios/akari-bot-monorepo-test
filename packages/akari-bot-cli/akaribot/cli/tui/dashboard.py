"""Dashboard 页：本机实例清单 + 当前实例的路径 / core 版本 / 运行状态 / 更新提示。

数据流：界面只读 :class:`DashboardSource`（当前实例的快照）与 :class:`InstanceListSource`（注册表
里的其它实例）。默认实现 :class:`LocalDashboardSource` 先读 ``akaribot.toml``，取不到 core 版本时
再经 ``akaribot module list --json`` 子进程补取，运行状态一律探测实例锁文件 ``.bot.lock``；实例清单
直接读本机注册表，不起子进程。在清单里选中一条并回车即切换当前实例，缺省项经 ``akaribot instance
use`` 子进程异步写回，结论以应用级通知报出；各页随后的取数都指向它。``ctrl+n`` 经 ``akaribot init``
子进程新建实例并登记，``ctrl+d`` 弹确认框移除登记。

页底两行按钮是这些动作的主要入口：上行作用于高亮的实例，下行作用于当前实例的策略与服务；键位是
同一批动作的快捷方式，逐条列在 ``?`` 键位一览里。

服务装卸经 :class:`ServiceControl`：安装前重读一次状态，单元文件已存在时确认框里写明覆盖；确认框
里另给 ``--dry-run`` 预演，用户看过将写入的单元文件再决定。

写动作（登记、移除、策略、缺省项、服务装卸、新建实例）一律经 :class:`CliRunner` 起
``akaribot <子命令>`` 子进程，注册表只用于读取。
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
from akaribot.cli.tui import cli_process, context
from akaribot.cli.tui.modules import OperationResult

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


# 切换实例会重挂载本页，最近一次下发 `instance use` 的目标名挂在应用上，新页面才读得到这份记录。
_USE_REQUEST_ATTR = "_dashboard_use_requested"


# 新建实例要解析依赖并装 core 与适配器，耗时可达数分钟，超时按最坏情况给足。
INIT_TIMEOUT_SECONDS = 1800.0
# 服务预演只渲染单元文件并读一次系统工具，正常在数秒内结束。
SERVICE_CLI_TIMEOUT_SECONDS = 60.0
# 注册表与服务单元的写入是秒级操作，超时只用于兜住卡死的子进程。
CLI_WRITE_TIMEOUT_SECONDS = 60.0


def _tail(text: str | None, limit: int = 400) -> str:
    return (text or "").strip()[-limit:]


def _first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _result_summary(result: OperationResult) -> str:
    line = _first_line(result.detail)
    if not line:
        return result.message
    return f"{result.message}{i18n.t('cli.tui.common.error_separator')}{line}"


def _run_cli_operation(
    argv: Sequence[str],
    *,
    label: str,
    cwd: Path,
    root: Path,
    timeout: float,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> OperationResult:
    # 与模块页安装同一条通路：阻塞式子进程，成功取标准输出尾部，失败取标准错误尾部。
    execute = runner or subprocess.run
    try:
        completed = execute(
            list(argv),
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=cli_process.cli_env(root),
        )
    except subprocess.TimeoutExpired:
        return OperationResult(False, i18n.t("cli.tui.dashboard.cli_timeout", label=label, seconds=f"{timeout:g}"), "")
    except OSError as error:
        return OperationResult(
            False,
            i18n.t("cli.tui.common.failed_label", label=label),
            f"{type(error).__name__}: {error}",
        )
    if completed.returncode == 0:
        return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), _tail(completed.stdout))
    return OperationResult(
        False,
        i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
        _tail(completed.stderr) or _tail(completed.stdout),
    )


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
    """服务状态的读取与预演；装卸经 :class:`CliRunner` 交给命令层。"""

    def service_status(self) -> ServiceRow:
        """返回服务单元状态。"""

    def preview_service(self, action: str) -> OperationResult:
        """执行 ``akaribot service <动作> --dry-run``，返回预演输出。

        :param action: ``install`` 或 ``uninstall``。
        """


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

    def preview_service(self, action: str) -> OperationResult:
        """见 :meth:`ServiceControl.preview_service`。"""
        return _run_cli_operation(
            cli_process.cli_argv("service", action, "--dry-run"),
            label=i18n.t(f"cli.tui.dashboard.service_preview_label_{action}"),
            cwd=Path.cwd(),
            root=Path.cwd(),
            timeout=SERVICE_CLI_TIMEOUT_SECONDS,
        )


class StaticServiceControl:
    """固定服务状态的替身，供自动化断言使用。

    :param status: ``service_status`` 的返回值。
    :param preview_result: ``preview_service`` 的返回值；缺省为成功。
    """

    def __init__(
        self,
        status: ServiceRow | None = None,
        *,
        preview_result: OperationResult | None = None,
    ) -> None:
        self._status = status or ServiceRow(backend="launchd", installed=False)
        self._preview = preview_result or OperationResult(
            True, i18n.t("cli.tui.dashboard.service_preview_stub_ok"), "stub"
        )
        self.calls = {"status": 0, "preview": 0}
        self.previewed: list[str] = []

    def service_status(self) -> ServiceRow:
        """见 :meth:`ServiceControl.service_status`。"""
        self.calls["status"] += 1
        return self._status

    def set_status(self, status: ServiceRow) -> None:
        """替换替身记录的服务状态，模拟单元文件在界面之外出现或消失。"""
        self._status = status

    def preview_service(self, action: str) -> OperationResult:
        """见 :meth:`ServiceControl.preview_service`。"""
        self.calls["preview"] += 1
        self.previewed.append(action)
        return self._preview


@runtime_checkable
class CliRunner(Protocol):
    """写操作的执行接口：一次 ``akaribot <子命令>`` 调用。"""

    def run(self, args: Sequence[str], *, label: str) -> OperationResult:
        """执行子命令并返回操作结果。

        :param args: 子命令及其参数，不含解释器与入口。
        :param label: 用于拼装结论的操作名。
        """


class SubprocessCliRunner:
    """默认实现：经子进程执行本 CLI 的写子命令。

    :param timeout: 子进程超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        timeout: float = CLI_WRITE_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        self.timeout = timeout
        self._runner = runner

    def run(self, args: Sequence[str], *, label: str) -> OperationResult:
        """见 :meth:`CliRunner.run`。"""
        root = context.resolve_root()
        return _run_cli_operation(
            cli_process.cli_argv(*args),
            label=label,
            cwd=root,
            root=root,
            timeout=self.timeout,
            runner=self._runner,
        )


@runtime_checkable
class InitRunner(Protocol):
    """新建实例的执行接口；测试注入替身，生产经 ``akaribot init`` 子进程。"""

    def create(self, root: Path, *, managed_venv: bool, locale: str) -> OperationResult:
        """创建实例并返回操作结果。

        :param root: 新实例根目录。
        :param managed_venv: 是否建托管 venv；为假时用当前环境。
        :param locale: 实例默认语言。
        """


class SubprocessInitRunner:
    """默认实现：经 ``akaribot init`` 子进程创建实例。

    :param timeout: 子进程超时秒数；初始化要装 core 与适配器，按最坏情况给足。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        timeout: float = INIT_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        self.timeout = timeout
        self._runner = runner

    def create(self, root: Path, *, managed_venv: bool, locale: str) -> OperationResult:
        """见 :meth:`InitRunner.create`。"""
        argv = cli_process.cli_argv("init", str(root), "--non-interactive", "--locale", locale)
        if not managed_venv:
            argv.append("--no-venv")
        return _run_cli_operation(
            argv,
            label=i18n.t("cli.tui.dashboard.new_label", root=root),
            # 实例目录由 init 自己创建，子进程的工作目录只能取它的父目录。
            cwd=root.parent,
            root=root,
            timeout=self.timeout,
            runner=self._runner,
        )


class StaticInitRunner:
    """固定结果的替身执行器，供自动化断言使用。

    :param result: ``create`` 的返回值；缺省为成功。
    """

    def __init__(self, result: OperationResult | None = None) -> None:
        self._result = result or OperationResult(True, i18n.t("cli.tui.dashboard.new_stub_ok"), "stub")
        self.created: list[tuple[str, bool, str]] = []

    def create(self, root: Path, *, managed_venv: bool, locale: str) -> OperationResult:
        """见 :meth:`InitRunner.create`。"""
        self.created.append((str(root), managed_venv, locale))
        return self._result


@runtime_checkable
class InstanceListSource(Protocol):
    """本机实例清单的数据源接口；写动作经 :class:`CliRunner` 交给命令层。"""

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """返回注册表里的实例，附带实时运行状态。"""


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
        self.calls = {"list": 0}
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


class StaticInstanceListSource:
    """固定清单的替身数据源，供自动化断言使用。

    :param rows: 清单内容。
    """

    def __init__(self, rows: Sequence[InstanceRow] = ()) -> None:
        self._rows = list(rows)
        self.calls = {"list": 0}

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """见 :meth:`InstanceListSource.list_instances`。"""
        self.calls["list"] += 1
        return tuple(self._rows)


def resolve_instance_root(start: Path | None = None) -> Path | None:
    """定位实例根，供概览、运行与日志三页的默认数据源共用。

    顺序与 :func:`akaribot.cli.tui.context.resolve_root` 一致：界面里选中的实例优先，其次自起点
    向上查找，最后是注册表里的缺省实例。区别只在三者都没有时返回 ``None`` 而不是退回当前目录——
    这三页要能区分「没找到实例」并如实说明。

    :param start: 查找起点，缺省为当前工作目录。
    :return: 实例根；未找到时为 ``None``。
    """
    active = context.active_root()
    if active is not None:
        return active
    try:
        from akaribot.cli.instance import find_instance_root, registry_default_root
    except ImportError:
        candidate = Path(os.environ.get(INSTANCE_DIR_ENV) or (start or Path.cwd())).expanduser()
        return candidate.resolve() if (candidate / INSTANCE_META_FILENAME).is_file() else None
    found = find_instance_root(start)
    if found is not None:
        return found.resolve()
    return registry_default_root()


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
    :param instances: 实例清单数据源，缺省读本机注册表。
    :param service_control: 服务状态与预演接口，缺省直接用 CLI 侧的 service 模块。
    :param init_runner: 新建实例的执行接口，缺省经 ``akaribot init`` 子进程。
    :param cli_runner: 写动作的执行接口，缺省经 ``akaribot <子命令>`` 子进程。
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
        height: 6;
        padding: 0 0 0 1;
    }
    DashboardPage #actions Horizontal {
        height: 3;
    }
    DashboardPage #actions Button {
        min-width: 0;
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
    # 页脚只放高频键位：低频动作由页底按钮承载，键位仍可在 ? 键位一览里查到。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.dashboard.bind_refresh")),
        ("s", "switch_instance", i18n.t("cli.tui.dashboard.bind_switch")),
        ("ctrl+n", "new_instance", i18n.t("cli.tui.dashboard.bind_new_instance")),
        ("a", "toggle_autostart", i18n.t("cli.tui.dashboard.bind_autostart"), False),
        ("c", "toggle_crash_restart", i18n.t("cli.tui.dashboard.bind_crash_restart"), False),
        ("n", "add_instance", i18n.t("cli.tui.dashboard.bind_add_instance"), False),
        ("ctrl+d", "remove_instance", i18n.t("cli.tui.dashboard.bind_remove_instance"), False),
        ("i", "toggle_service", i18n.t("cli.tui.dashboard.bind_service"), False),
    )

    can_focus = True

    def __init__(
        self,
        source: DashboardSource | None = None,
        *,
        instances: InstanceListSource | None = None,
        service_control: ServiceControl | None = None,
        init_runner: InitRunner | None = None,
        cli_runner: CliRunner | None = None,
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
        self.init_runner: InitRunner = init_runner if init_runner is not None else SubprocessInitRunner()
        self.cli_runner: CliRunner = cli_runner if cli_runner is not None else SubprocessCliRunner()
        self._service = ServiceRow()
        self._service_text = ""
        self._service_preview = ""
        self._busy = False
        self._pending_service = compat.PendingConfirm()
        self._instance_rows: tuple[InstanceRow, ...] = ()
        self._highlighted_key = ""
        self._pending_remove = compat.PendingConfirm()
        self.cache_ttl = cache_ttl
        self.refresh_interval = refresh_interval
        self.last_error: str = ""
        self._snapshot = DashboardSnapshot()
        self._loaded_at: float = 0.0
        self._rows: tuple[tuple[str, str], ...] = ()
        self._fields_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：实例清单 + 当前实例的字段 + 两行操作按钮与状态栏。"""
        yield compat.Static(i18n.t("cli.tui.dashboard.instances_keys_caption"), id="instances-caption", markup=False)
        yield compat.Static("", id="service", markup=False)
        yield compat.ListView(id="instance-list")
        with compat.VerticalScroll(id="fields-pane"):
            yield compat.Static(i18n.t("cli.tui.dashboard.fields_placeholder"), id="fields", markup=False)
        with compat.Vertical(id="actions"):
            with compat.Horizontal(id="actions-instance"):
                yield compat.Button(i18n.t("cli.tui.dashboard.button_switch"), id="switch")
                yield compat.Button(i18n.t("cli.tui.dashboard.button_new_instance"), id="new-instance")
                yield compat.Button(i18n.t("cli.tui.dashboard.button_add_instance"), id="add-instance")
                yield compat.Button(
                    i18n.t("cli.tui.dashboard.button_remove_instance"), id="remove-instance", variant="error"
                )
            with compat.Horizontal(id="actions-policy"):
                yield compat.Button(i18n.t("cli.tui.dashboard.button_autostart_off"), id="autostart")
                yield compat.Button(i18n.t("cli.tui.dashboard.button_crash_off"), id="crash-restart")
                yield compat.Button(i18n.t("cli.tui.dashboard.button_service_install"), id="service-toggle")
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

    def refresh_instances(self, *, polling: bool = False) -> None:
        """重新读取本机实例清单并重绘。

        :param polling: 周期轮询只刷新显示，不作废待确认。
        """
        try:
            rows = tuple(self.instances.list_instances())
        except Exception as error:  # noqa: BLE001 - 注册表不可用只降级为一句提示
            self._instance_rows = ()
            if not polling:
                self.reset_pending()
            self._render_instances()
            self._set_status(i18n.t("cli.tui.dashboard.instances_failed", error=f"{type(error).__name__}: {error}"))
            return
        if not polling and rows != self._instance_rows:
            # 清单内容变了，待确认的那个实例可能已经不在原位，作废重问。
            self.reset_pending()
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
        index = self._index_of_active()
        list_view.index = index
        # 重建时把高亮拨回当前实例属于显示刷新，不能算用户换了选中项。
        self._highlighted_key = self._highlight_key(self._instance_rows[index] if index is not None else None)
        self.query_one("#instances-caption", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.dashboard.instances_keys_caption_with_count", count=len(rows)))
        )
        self._sync_actions()

    @staticmethod
    def _highlight_key(row: InstanceRow | None) -> str:
        return row.name if row is not None else ""

    def _index_of_active(self) -> int | None:
        active = context.active_root()
        if active is None or not self._instance_rows:
            return 0 if self._instance_rows else None
        for index, row in enumerate(self._instance_rows):
            if row.root == active:
                return index
        return 0

    @staticmethod
    def _is_active_instance(row: InstanceRow) -> bool:
        # 上下文里的根按真实路径保存，比较前同样解析，否则软链接下的临时实例永远判为不同。
        active = context.active_root()
        if active is None:
            return False
        return Path(row.root).expanduser().resolve() == active

    def _instance_width(self, list_view: compat.ListView) -> int:
        try:
            return max(compat.widget_cells(list_view)[0] - 4, 16)
        except Exception:  # noqa: BLE001 - 未完成布局时按保守宽度排版
            return 72

    def switch_to_selected(self) -> None:
        """把当前实例切换为清单里高亮的那条，并把缺省项交给命令层写回。"""
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
        if self._reject_when_busy():
            return
        target = Path(row.root).expanduser().resolve()
        if context.active_root() != target:
            switch(row.root)
            if context.active_root() != target:
                # 别处有未保存改动时切换要先过确认框，确认前不能改写缺省项。
                self._set_status(i18n.t("cli.tui.dashboard.switch_deferred"))
                return
        name = row.name or str(row.root)
        separator = i18n.t("cli.tui.common.error_separator")
        self._set_status(
            f"{i18n.t('cli.tui.dashboard.switch_done', name=name)}{separator}{self._request_default_instance(row)}"
        )

    def _request_default_instance(self, row: InstanceRow) -> str:
        # 命令行读的是注册表缺省项，只切内存态会让界面与 `instance use` 各说各话。
        if not row.registered or not row.name:
            return i18n.t("cli.tui.dashboard.switch_default_skipped")
        app = self.app
        name = row.name
        note = i18n.t("cli.tui.dashboard.use_calling", name=name)
        if getattr(app, _USE_REQUEST_ATTR, "") == name:
            # 同一目标名已经下发过，重复切换不再叠一个改注册表的子进程。
            return note
        setattr(app, _USE_REQUEST_ATTR, name)
        label = i18n.t("cli.tui.dashboard.use_label", name=name)
        # worker 挂在应用上：本页随切换重挂载，挂在本页的 worker 会在卸载时被取消而丢掉结论。
        app.run_worker(
            self._run_action(
                lambda: self.cli_runner.run(("instance", "use", name), label=label),
                label=label,
                on_done=lambda result: self._finish_default_instance(app, name, label, result),
                track_busy=False,
            ),
            group="dashboard-use",
        )
        return note

    def _finish_default_instance(self, app: Any, name: str, label: str, result: OperationResult) -> None:
        # 本页随后被重挂载，结论只能经应用级通知报出；旧页的状态栏已随页面消失。
        if result.ok:
            compat.notify(app, i18n.t("cli.tui.dashboard.switch_default_done"), title=label)
            return
        if getattr(app, _USE_REQUEST_ATTR, "") == name:
            # 写失败即撤掉记录，用户再切一次就能重试。
            setattr(app, _USE_REQUEST_ATTR, "")
        compat.notify(
            app,
            i18n.t("cli.tui.dashboard.switch_default_failed", error=_result_summary(result)),
            severity="error",
            title=label,
        )

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
        if self._reject_when_busy():
            return
        wanted = not (row.autostart if field_name == "autostart" else row.restart_on_crash)
        option = field_name.replace("_", "-")
        args = ("instance", "policy", row.name, f"--{option}" if wanted else f"--no-{option}")
        label = i18n.t("cli.tui.dashboard.policy_label", name=row.name)
        self._set_status(i18n.t("cli.tui.dashboard.policy_calling", name=row.name))
        self._start_action(
            lambda: self.cli_runner.run(args, label=label),
            label=label,
            group="dashboard-instance",
            on_done=lambda result: self._finish_policy(row, field_name, wanted, result),
        )

    def _finish_policy(self, row: InstanceRow, field_name: str, wanted: bool, result: OperationResult) -> None:
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.policy_failed", error=_result_summary(result)))
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

    @property
    def service_preview(self) -> str:
        """返回最近一次服务预演的完整输出。"""
        return self._service_preview

    def refresh_service(self) -> None:
        """读取服务单元状态并重绘那一行。"""
        self._pending_service.reset()
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
        self._sync_actions()

    def _sync_actions(self) -> None:
        # 按钮是主要入口，禁用状态与标签都要跟着清单、策略与服务状态走，免得点下去才被拒绝。
        row = self.selected_instance()
        registered = row is not None and row.registered
        self.query_one("#switch", compat.Button).disabled = self._busy or row is None or self._is_active_instance(row)
        for button_id in ("new-instance", "add-instance", "refresh"):
            self.query_one(f"#{button_id}", compat.Button).disabled = self._busy
        self.query_one("#remove-instance", compat.Button).disabled = self._busy or not registered
        self._sync_policy_button("autostart", "autostart", row)
        self._sync_policy_button("crash-restart", "restart_on_crash", row)
        service = self.query_one("#service-toggle", compat.Button)
        # 策略与服务都写在注册表上，未登记时写不了；平台没有服务后端时也无处可装。
        service.disabled = self._busy or not registered or self._service.backend == "unsupported"
        service.label = i18n.t(
            "cli.tui.dashboard.button_service_uninstall"
            if self._service.installed
            else "cli.tui.dashboard.button_service_install"
        )

    def _sync_policy_button(self, button_id: str, field_name: str, row: InstanceRow | None) -> None:
        enabled = row is not None and (row.autostart if field_name == "autostart" else row.restart_on_crash)
        state = "on" if enabled else "off"
        prefix = "autostart" if field_name == "autostart" else "crash"
        button = self.query_one(f"#{button_id}", compat.Button)
        button.disabled = self._busy or row is None or not row.registered
        button.label = i18n.t(f"cli.tui.dashboard.button_{prefix}_{state}")

    def request_toggle_service(self) -> None:
        """安装或卸载常驻服务：一次触发即弹确认框，框里可选执行或先预演。

        安装会往系统里写一个自启单元，卸载会注销它，故都经模态框确认；框里给出单元文件路径与
        覆盖提示，用户知道到底动了什么。
        """
        action, force = self._service_action()
        if not self._pending_service.accept(f"service:{action}"):
            # 防抖窗口内的重复触发（鼠标双击、键盘连发）直接忽略，避免叠起两层模态框。
            return
        self._ask_service(action, force=force)

    def _service_action(self) -> tuple[str, bool]:
        if self._service.installed:
            return "uninstall", False
        # 缓存的安装状态可能过期：单元文件已存在时安装会覆盖它，确认框据此写提示。
        try:
            fresh = self.service_control.service_status()
        except Exception:  # noqa: BLE001 - 重读失败按缓存状态处理，执行时不带 force
            return "install", False
        self._service = fresh
        self._render_service()
        return "install", fresh.installed

    def _ask_service(self, action: str, *, force: bool) -> None:
        hint = i18n.t("cli.tui.dashboard.service_choice_hint")
        if force:
            hint = i18n.t("cli.tui.dashboard.service_choice_hint_force", path=self._service.path or "-")
        compat.ask_choice(
            self.app,
            title=i18n.t(
                "cli.tui.dashboard.service_choice_title",
                action=i18n.t(f"cli.tui.dashboard.service_action_{action}"),
            ),
            hint=hint,
            options=(
                (action, i18n.t(f"cli.tui.dashboard.service_choice_{action}")),
                ("dry-run", i18n.t("cli.tui.dashboard.service_choice_dry_run")),
            ),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=lambda choice: self.on_service_choice(action, force, choice),
        )

    def on_service_choice(self, action: str, force: bool, choice: str | None) -> None:
        """确认框回调：选执行则装卸服务，选预演则只打印将发生什么。

        :param action: ``install`` 或 ``uninstall``。
        :param force: 是否覆盖已存在的单元文件。
        :param choice: 用户选中的取值；取消时为 ``None``。
        """
        if choice == "dry-run":
            self.preview_service(action)
            return
        if choice != action:
            self._set_status(i18n.t("cli.tui.dashboard.service_cancelled"))
            return
        self._start_service(action, force=force)

    def preview_service(self, action: str) -> None:
        """执行 ``akaribot service <动作> --dry-run``，把输出留在状态栏与预演区。"""
        if self._reject_when_busy():
            return
        self._set_status(
            i18n.t(
                "cli.tui.dashboard.service_calling_preview",
                action=i18n.t(f"cli.tui.dashboard.service_action_{action}"),
            )
        )
        self._service_preview = ""
        self._start_action(
            lambda: self.service_control.preview_service(action),
            label=i18n.t(f"cli.tui.dashboard.service_preview_label_{action}"),
            group="dashboard-service",
            on_done=self._finish_preview,
        )

    def _finish_preview(self, result: OperationResult) -> None:
        self._service_preview = result.detail
        output = _first_line(result.detail) or i18n.t("cli.tui.common.no_output")
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.service_preview_failed", error=_result_summary(result)))
            return
        self._set_status(i18n.t("cli.tui.dashboard.service_preview_done", output=output))

    def _start_service(self, action: str, *, force: bool = False) -> None:
        if self._reject_when_busy():
            return
        args = ["service", action]
        if action == "install" and force:
            args.append("--force")
        label = i18n.t(f"cli.tui.dashboard.service_label_{action}")
        self._set_status(i18n.t(f"cli.tui.dashboard.service_calling_{action}"))
        self._start_action(
            lambda: self.cli_runner.run(tuple(args), label=label),
            label=label,
            group="dashboard-service",
            on_done=lambda result: self._finish_service(action, result),
        )

    def _finish_service(self, action: str, result: OperationResult) -> None:
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.service_failed", error=_result_summary(result)))
            return
        self.refresh_service()
        key = "service_removed" if action == "uninstall" else "service_added"
        self._set_status(i18n.t(f"cli.tui.dashboard.{key}", path=self._service.path or "-"))

    def _reject_when_busy(self) -> bool:
        # 写动作各起一个子进程，连点会让多个进程同时改同一份注册表。
        if not self._busy:
            return False
        self._set_status(i18n.t("cli.tui.dashboard.busy_running"))
        return True

    def _start_action(
        self,
        call: Callable[[], OperationResult],
        *,
        label: str,
        group: str,
        on_done: Callable[[OperationResult], None],
    ) -> None:
        self._busy = True
        self._sync_actions()
        self.run_worker(self._run_action(call, label=label, on_done=on_done), group=group, exclusive=True)

    async def _run_action(
        self,
        call: Callable[[], OperationResult],
        *,
        label: str,
        on_done: Callable[[OperationResult], None],
        track_busy: bool = True,
    ) -> None:
        try:
            result = await asyncio.to_thread(call)
        except Exception as error:  # noqa: BLE001 - 执行器任意异常都只降级为一句说明
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        if track_busy:
            # 未纳管的动作不得清掉别的动作置上的忙标志。
            self._busy = False
            self._sync_actions()
        on_done(result)

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
            initial=str(context.resolve_root()),
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
        if self._reject_when_busy():
            return
        root = Path(path).expanduser()
        label = i18n.t("cli.tui.dashboard.add_label", root=root)
        self._set_status(i18n.t("cli.tui.dashboard.add_calling", root=root))
        self._start_action(
            lambda: self.cli_runner.run(("instance", "add", str(root)), label=label),
            label=label,
            group="dashboard-instance",
            on_done=lambda result: self._finish_add(root, result),
        )

    def _finish_add(self, root: Path, result: OperationResult) -> None:
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.add_failed", error=_result_summary(result)))
            return
        self.refresh_instances()
        self._set_status(i18n.t("cli.tui.dashboard.add_done", name=self._registered_name(root), root=root))

    def _registered_name(self, root: Path) -> str:
        # 注册名由命令层推导，界面从刷新后的清单里取；取不到时退回目录名。
        wanted = root.expanduser().resolve()
        for row in self._instance_rows:
            if row.root.expanduser().resolve() == wanted:
                return row.name or wanted.name
        return root.name

    def request_new_instance(self) -> None:
        """弹出输入框要新实例目录，拿到目录后再问环境方式。"""
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.dashboard.new_title"),
            hint=i18n.t("cli.tui.dashboard.new_hint"),
            placeholder=i18n.t("cli.tui.dashboard.new_placeholder"),
            initial=self._new_instance_default(),
            confirm_label=i18n.t("cli.tui.dashboard.new_confirm"),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=self.on_new_instance_path_entered,
        )

    def _new_instance_default(self) -> str:
        # 新实例多半是当前实例的邻居，预填它的父目录；没有实例时退回当前工作目录。
        root = resolve_instance_root()
        if root is not None:
            return str(root.parent)
        return str(Path.cwd())

    def on_new_instance_path_entered(self, path: str | None) -> None:
        """输入框回调：把目录交给下一步的环境方式选择框。

        :param path: 用户输入的路径；取消时为 ``None``。
        """
        if not path:
            self._set_status(i18n.t("cli.tui.dashboard.new_cancelled"))
            return
        root = Path(path).expanduser()
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.dashboard.new_venv_title", root=root),
            hint=i18n.t("cli.tui.dashboard.new_venv_hint"),
            options=(
                ("managed", i18n.t("cli.tui.dashboard.new_venv_managed")),
                ("current", i18n.t("cli.tui.dashboard.new_venv_current")),
            ),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=lambda choice: self.on_new_instance_venv_chosen(root, choice),
        )

    def on_new_instance_venv_chosen(self, root: Path, choice: str | None) -> None:
        """选择框回调：按所选环境方式执行 ``akaribot init``。

        :param root: 新实例目录。
        :param choice: ``managed`` 建托管 venv，``current`` 装进当前环境；取消时为 ``None``。
        """
        if choice not in ("managed", "current"):
            self._set_status(i18n.t("cli.tui.dashboard.new_cancelled"))
            return
        if self._reject_when_busy():
            return
        locale = i18n.current_locale()
        managed_venv = choice == "managed"
        self._set_status(i18n.t("cli.tui.dashboard.new_calling", root=root))
        self._start_action(
            lambda: self.init_runner.create(root, managed_venv=managed_venv, locale=locale),
            label=i18n.t("cli.tui.dashboard.new_label", root=root),
            group="dashboard-new",
            on_done=lambda result: self._finish_new_instance(root, result),
        )

    def _finish_new_instance(self, root: Path, result: OperationResult) -> None:
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.new_failed", error=_result_summary(result)))
            return
        # init 自己会把新实例登记进注册表，界面只需重读清单。
        self.refresh_instances()
        self._set_status(i18n.t("cli.tui.dashboard.new_done", name=self._registered_name(root), root=root))

    def request_remove_instance(self) -> None:
        """移除清单里高亮实例的登记；一次触发即弹确认框，实例目录本身不动。"""
        row = self.selected_instance()
        if row is None:
            self._set_status(i18n.t("cli.tui.dashboard.switch_no_selection"))
            return
        if not row.registered:
            self._set_status(i18n.t("cli.tui.dashboard.policy_unregistered", root=row.root))
            return
        if not self._pending_remove.accept(row.name or str(row.root)):
            # 防抖窗口内的重复触发（鼠标双击、键盘连发）直接忽略，避免叠起两层模态框。
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.dashboard.remove_label", name=row.name),
            hint=i18n.t("cli.tui.dashboard.remove_choice_hint"),
            options=(("remove", i18n.t("cli.tui.dashboard.remove_choice_confirm")),),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=lambda choice: self.on_remove_choice(row, choice),
        )

    def on_remove_choice(self, row: InstanceRow, choice: str | None) -> None:
        """确认框回调：选中「移除登记」才下发 ``instance remove``。

        :param row: 待移除的记录。
        :param choice: ``remove`` 表示确认；取消时为 ``None``。
        """
        self._pending_remove.reset()
        if choice != "remove":
            self._set_status(i18n.t("cli.tui.dashboard.remove_cancelled"))
            return
        if self._reject_when_busy():
            return
        label = i18n.t("cli.tui.dashboard.remove_label", name=row.name)
        self._set_status(i18n.t("cli.tui.dashboard.remove_calling", name=row.name))
        self._start_action(
            lambda: self.cli_runner.run(("instance", "remove", row.name, "--yes"), label=label),
            label=label,
            group="dashboard-instance",
            on_done=lambda result: self._finish_remove(row, result),
        )

    def _finish_remove(self, row: InstanceRow, result: OperationResult) -> None:
        if not result.ok:
            self._set_status(i18n.t("cli.tui.dashboard.remove_failed", error=_result_summary(result)))
            return
        self.refresh_instances()
        self._set_status(i18n.t("cli.tui.dashboard.remove_done", name=row.name))

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

    def action_new_instance(self) -> None:
        """键位动作：新建实例。"""
        self.request_new_instance()

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
        # 用户主动刷新即视为换了一轮语境，任何待确认动作都要重新问过。
        self.reset_pending()
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
        self.refresh_instances(polling=True)

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
        self._sync_actions()

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

    def reset_pending(self) -> None:
        """作废本页的待确认状态；切页、刷新与换选中项后必须重问。"""
        self._pending_service.reset()
        self._pending_remove.reset()

    @compat.on(compat.ListView.Selected, "#instance-list")
    def _on_instance_selected(self, event: compat.ListView.Selected) -> None:
        self.switch_to_selected()

    @compat.on(compat.ListView.Highlighted, "#instance-list")
    def _on_instance_highlighted(self, event: compat.ListView.Highlighted) -> None:
        # 重建列表会先清高亮再回填，按当前下标比对可避开这类假变化。
        key = self._highlight_key(self.selected_instance())
        if key == self._highlighted_key:
            return
        self._highlighted_key = key
        self.reset_pending()
        self._sync_actions()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "switch":
            self.switch_to_selected()
        elif button_id == "new-instance":
            self.request_new_instance()
        elif button_id == "add-instance":
            self.request_add_instance()
        elif button_id == "remove-instance":
            self.request_remove_instance()
        elif button_id == "autostart":
            self.toggle_policy("autostart")
        elif button_id == "crash-restart":
            self.toggle_policy("restart_on_crash")
        elif button_id == "service-toggle":
            self.request_toggle_service()
        elif button_id == "refresh":
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
