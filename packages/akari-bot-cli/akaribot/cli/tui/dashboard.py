from __future__ import annotations

import asyncio
import json
import os
import re
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
CONFIG_DIRNAME = "config"
CONFIG_GLOB = "*.toml"

_PLACEHOLDER_PATTERN = re.compile(r"<Replace me[^>]*>")

# 标签须按当前语言解析，因此常量只保存文案键。
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


# 切换实例会重新挂载页面，操作记录保存在应用上以供新页面读取。
_USE_REQUEST_ATTR = "_dashboard_use_requested"


# 实例创建包含依赖解析与安装，超时须覆盖下载耗时。
INIT_TIMEOUT_SECONDS = 1800.0
SERVICE_CLI_TIMEOUT_SECONDS = 60.0
CLI_WRITE_TIMEOUT_SECONDS = 60.0
SETUP_TIMEOUT_SECONDS = 60.0

SETUP_BUTTONS: tuple[tuple[str, str], ...] = (
    ("config", "goto-config"),
    ("run", "goto-run"),
    ("doctor", "goto-doctor"),
)
"""首次使用行动区的三个按钮：页面键与控件 id，文案键按 ``setup_button_<页面键>`` 派生。"""


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


def _json_object(text: str | None) -> Mapping[str, Any] | None:
    try:
        payload = json.loads(text or "")
    except (json.JSONDecodeError, TypeError):
        return None
    return payload if isinstance(payload, Mapping) else None


def _count_of(value: Any) -> int | None:
    # bool 是 int 的子类，计数字段须显式排除布尔值。
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _missing_text(reason: str) -> str:
    if reason:
        return i18n.t("cli.tui.dashboard.setup_value_missing_reason", reason=reason)
    return i18n.t("cli.tui.dashboard.setup_value_missing")


def _count_placeholders(paths: Sequence[Path]) -> int:
    # 配置模板的占位符包含类型说明，估算时须匹配完整标记。
    total = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        total += len(_PLACEHOLDER_PATTERN.findall(text))
    return total


def _run_cli_operation(
    argv: Sequence[str],
    *,
    label: str,
    cwd: Path,
    root: Path,
    timeout: float,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> OperationResult:
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
    """实例概览快照。

    :param instance_root: 实例根目录的绝对路径。
    :param instance_name: ``[instance] name``。
    :param instance_mode: ``installed`` 或 ``workspace``。
    :param locale: 实例默认语言。
    :param core_version: core 版本号；无法获取时为空串。
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
        """将运行状态转换为 :data:`STATE_RUNNING` 等取值。"""
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
    """实例清单记录。

    :param name: 注册名；未登记的当前实例用空串。
    :param root: 实例根目录。
    :param locale: 实例默认语言。
    :param running: 是否在运行；探测失败时为 ``None``。
    :param autostart: 是否在服务启动时自动启动。
    :param restart_on_crash: 崩溃后是否自动重启。
    :param registered: 是否已在注册表中。
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
    :param enabled: 系统是否已注册；无法探测时为 ``None``。
    :param path: 单元文件路径。
    :param detail: 面向用户的简要说明。
    """

    backend: str = ""
    installed: bool = False
    enabled: bool | None = None
    path: Path | None = None
    detail: str = ""


@runtime_checkable
class ServiceControl(Protocol):
    """读取服务状态并执行预览；装卸经 :class:`CliRunner` 执行。"""

    def service_status(self) -> ServiceRow:
        """返回服务单元状态。"""

    def preview_service(self, action: str) -> OperationResult:
        """执行 ``akaribot service <动作> --dry-run``，返回预览输出。

        :param action: ``install`` 或 ``uninstall``。
        """


class SystemServiceControl:
    """通过 CLI 服务模块读取状态并执行预览。

    :param backend: 服务后端；默认按平台探测。
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
        return self._row(self._service().status())

    def preview_service(self, action: str) -> OperationResult:
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
    :param preview_result: ``preview_service`` 的返回值；默认为成功。
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
        self.calls["status"] += 1
        return self._status

    def set_status(self, status: ServiceRow) -> None:
        """替换替身记录的服务状态，模拟单元文件在界面之外出现或消失。"""
        self._status = status

    def preview_service(self, action: str) -> OperationResult:
        self.calls["preview"] += 1
        self.previewed.append(action)
        return self._preview


@runtime_checkable
class CliRunner(Protocol):
    """写操作的执行接口：一次 ``akaribot <子命令>`` 调用。"""

    def run(self, args: Sequence[str], *, label: str) -> OperationResult:
        """执行子命令并返回操作结果。

        :param args: 子命令及其参数，不含解释器与入口。
        :param label: 操作结果使用的名称。
        """


class SubprocessCliRunner:
    """通过 CLI 子进程执行写操作。

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
        :param managed_venv: 是否创建托管 venv；为假时用当前环境。
        :param locale: 实例默认语言。
        """


class SubprocessInitRunner:
    """默认实现：经 ``akaribot init`` 子进程创建实例。

    :param timeout: 子进程超时秒数；包含 core 与适配器的安装时间。
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
        argv = cli_process.cli_argv("init", str(root), "--non-interactive", "--locale", locale)
        if not managed_venv:
            argv.append("--no-venv")
        return _run_cli_operation(
            argv,
            label=i18n.t("cli.tui.dashboard.new_label", root=root),
            # 目标目录由 init 创建，子进程须以父目录作为工作目录。
            cwd=root.parent,
            root=root,
            timeout=self.timeout,
            runner=self._runner,
        )


class StaticInitRunner:
    """固定结果的替身执行器，供自动化断言使用。

    :param result: ``create`` 的返回值；默认为成功。
    """

    def __init__(self, result: OperationResult | None = None) -> None:
        self._result = result or OperationResult(True, i18n.t("cli.tui.dashboard.new_stub_ok"), "stub")
        self.created: list[tuple[str, bool, str]] = []

    def create(self, root: Path, *, managed_venv: bool, locale: str) -> OperationResult:
        self.created.append((str(root), managed_venv, locale))
        return self._result


@runtime_checkable
class InstanceListSource(Protocol):
    """本机实例清单的数据源接口；写操作经 :class:`CliRunner` 交给命令层。"""

    def list_instances(self) -> tuple[InstanceRow, ...]:
        """返回注册表中的实例，附带实时运行状态。"""


class RegistryInstanceListSource:
    """读取本机注册表，逐条探测锁文件。

    :param registry: 注册表；默认用默认位置。
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
            # 当前实例可能尚未登记，清单须包含该实例。
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
        self.calls["list"] += 1
        return tuple(self._rows)


@dataclass(frozen=True)
class SetupSummary:
    """首次使用摘要。

    :param unconfigured_adapters: 已安装但未配置的适配器数量；``None`` 表示未获取。
    :param pending_placeholders: 待填写的占位符数量；``None`` 表示未获取。
    :param doctor_errors: 最近一次诊断的错误级结论数；``None`` 表示未获取。
    :param doctor_warnings: 最近一次诊断的告警级结论数；``None`` 表示未获取。
    :param adapters_reason: 适配器数量未获取的原因；获取成功时为空串。
    :param placeholders_reason: 占位符数量的口径说明；core 返回完整统计时为空串。
    :param doctor_reason: 诊断结论未获取的原因；获取成功时为空串。
    :param placeholders_estimated: 占位符数量是否来自配置文本标记的估算。
    """

    unconfigured_adapters: int | None = None
    pending_placeholders: int | None = None
    doctor_errors: int | None = None
    doctor_warnings: int | None = None
    adapters_reason: str = ""
    placeholders_reason: str = ""
    doctor_reason: str = ""
    placeholders_estimated: bool = False


def _placeholders_text(summary: SetupSummary) -> str:
    if summary.pending_placeholders is None:
        return _missing_text(summary.placeholders_reason)
    if summary.placeholders_reason:
        return i18n.t(
            "cli.tui.dashboard.setup_placeholders_value_note",
            count=summary.pending_placeholders,
            reason=summary.placeholders_reason,
        )
    return i18n.t("cli.tui.dashboard.setup_placeholders_value", count=summary.pending_placeholders)


@runtime_checkable
class SetupSummarySource(Protocol):
    """首次使用摘要的数据源接口；测试注入替身，生产经子进程与本机配置文件。"""

    def summary(self) -> SetupSummary:
        """返回摘要数据。"""


class StaticSetupSummarySource:
    """固定摘要的替身数据源，供自动化断言使用。

    :param summary: ``summary`` 的返回值；默认提供完整的模拟摘要。
    :param error: 指定后每次读取均抛出该异常，用于验证读取失败时的处理。
    """

    def __init__(self, summary: SetupSummary | None = None, *, error: Exception | None = None) -> None:
        self._summary = summary if summary is not None else SetupSummary(0, 0, 0, 0)
        self._error = error
        self.calls = {"summary": 0}

    def summary(self) -> SetupSummary:
        self.calls["summary"] += 1
        if self._error is not None:
            raise self._error
        return self._summary

    def set_summary(self, summary: SetupSummary) -> None:
        """替换替身记录的摘要，模拟配置或诊断结论在界面之外变化。"""
        self._summary = summary


class LocalSetupSummarySource:
    """通过 CLI 获取诊断与占位符统计；占位符命令失败时按配置标记估算并注明原因。

    :param root: 实例根；默认在读取数据时按界面当前实例解析。
    :param timeout: 子进程超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = SETUP_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        self.root = Path(root) if root is not None else None
        self.timeout = timeout
        self._runner = runner
        self.calls = {"summary": 0}
        self.last_argv: tuple[str, ...] = ()

    def summary(self) -> SetupSummary:
        self.calls["summary"] += 1
        root = self.root or resolve_instance_root()
        if root is None:
            reason = i18n.t("cli.tui.dashboard.setup_src_no_instance")
            return SetupSummary(adapters_reason=reason, placeholders_reason=reason, doctor_reason=reason)
        adapters, errors, warnings, adapters_reason, doctor_reason = self._doctor(root)
        placeholders, placeholders_reason, placeholders_estimated = self._placeholders(root)
        return SetupSummary(
            unconfigured_adapters=adapters,
            pending_placeholders=placeholders,
            doctor_errors=errors,
            doctor_warnings=warnings,
            adapters_reason=adapters_reason,
            placeholders_reason=placeholders_reason,
            doctor_reason=doctor_reason,
            placeholders_estimated=placeholders_estimated,
        )

    def _doctor(self, root: Path) -> tuple[int | None, int | None, int | None, str, str]:
        argv = cli_process.cli_argv("doctor", "--json")
        self.last_argv = tuple(argv)
        execute = self._runner or subprocess.run
        try:
            completed = execute(
                list(argv),
                cwd=str(root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=cli_process.cli_env(root),
            )
        except subprocess.TimeoutExpired:
            reason = i18n.t("cli.tui.dashboard.setup_cli_timeout", seconds=f"{self.timeout:g}")
            return None, None, None, reason, reason
        except OSError as error:
            reason = f"{type(error).__name__}: {error}"
            return None, None, None, reason, reason
        # 诊断发现错误时返回非零退出码，但标准输出仍包含有效统计。
        payload = _json_object(completed.stdout)
        if payload is None:
            reason = i18n.t("cli.tui.dashboard.setup_doctor_unreadable", code=completed.returncode)
            tail = _tail(completed.stderr) or _tail(completed.stdout)
            if tail:
                reason = f"{reason}{i18n.t('cli.tui.common.error_separator')}{tail}"
            return None, None, None, reason, reason
        unreadable = i18n.t("cli.tui.dashboard.setup_checks_unreadable")
        checks = payload.get("checks")
        checks = checks if isinstance(checks, Mapping) else {}
        summary = payload.get("summary")
        summary = summary if isinstance(summary, Mapping) else {}
        unconfigured = checks.get("unconfigured_adapters")
        adapters: int | None = None
        adapters_reason = ""
        if payload.get("registry_available") is False:
            adapters_reason = str(payload.get("registry_note") or "").strip() or unreadable
        elif isinstance(unconfigured, Sequence) and not isinstance(unconfigured, (str, bytes)):
            adapters = len(unconfigured)
        else:
            adapters_reason = unreadable
        errors = _count_of(summary.get("error"))
        warnings = _count_of(summary.get("warning"))
        doctor_reason = "" if errors is not None and warnings is not None else unreadable
        return adapters, errors, warnings, adapters_reason, doctor_reason

    def _placeholders(self, root: Path) -> tuple[int | None, str, bool]:
        argv = cli_process.cli_argv("config", "placeholders", "--json")
        execute = self._runner or subprocess.run
        try:
            completed = execute(
                list(argv),
                cwd=str(root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=cli_process.cli_env(root),
            )
        except subprocess.TimeoutExpired:
            detail = i18n.t("cli.tui.dashboard.setup_placeholders_timeout", seconds=f"{self.timeout:g}")
            return self._estimate_placeholders(root, detail)
        except OSError as error:
            return self._estimate_placeholders(root, f"{type(error).__name__}: {error}")
        if completed.returncode != 0:
            failed = i18n.t("cli.tui.dashboard.setup_placeholders_failed", code=completed.returncode)
            detail = _first_line(_tail(completed.stderr) or _tail(completed.stdout)) or failed
            return self._estimate_placeholders(root, detail)
        payload = _json_object(completed.stdout)
        count = _count_of(payload.get("count")) if payload is not None else None
        if count is None:
            reason = i18n.t("cli.tui.dashboard.setup_placeholders_unreadable", code=completed.returncode)
            tail = _first_line(_tail(completed.stderr) or _tail(completed.stdout))
            if tail:
                reason = f"{reason}{i18n.t('cli.tui.common.error_separator')}{tail}"
            return self._estimate_placeholders(root, reason)
        failed_tables = payload.get("failed")
        if isinstance(failed_tables, Mapping) and failed_tables:
            names = "、".join(str(name) for name in failed_tables)
            reason = i18n.t(
                "cli.tui.dashboard.setup_placeholders_partial_reason",
                count=len(failed_tables),
                tables=names,
            )
            return count, reason, False
        return count, "", False

    def _estimate_placeholders(self, root: Path, detail: str) -> tuple[int | None, str, bool]:
        # core 统计不可用时按配置标记估算，摘要须注明估算方式。
        try:
            paths = sorted((root / CONFIG_DIRNAME).rglob(CONFIG_GLOB))
        except OSError as error:
            reason = i18n.t(
                "cli.tui.dashboard.setup_placeholders_estimate_unavailable",
                detail=detail,
                error=f"{type(error).__name__}: {error}",
            )
            return None, reason, True
        reason = i18n.t("cli.tui.dashboard.setup_placeholders_estimated_reason", detail=detail)
        return _count_placeholders(paths), reason, True


def resolve_instance_root(start: Path | None = None) -> Path | None:
    """定位实例根，供概览、运行与日志三页的默认数据源共用。

    依次查询当前实例、起点及其父目录、注册表中的默认实例。

    :param start: 查找起点，默认为当前工作目录。
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
    """探测锁文件是否被排他锁持有，供概览与运行页共用。

    只读打开文件，不截断运行中进程持有的锁；``Instance.is_running()`` 不可用时作为备用实现。

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
    """Dashboard 数据源接口；测试注入替身，运行时通过文件系统与子进程读取。"""

    def snapshot(self) -> DashboardSnapshot:
        """返回完整快照，包括版本查询结果。"""

    def probe_running(self) -> bool | None:
        """只探测运行状态，代价须与读一个锁文件相当。"""


class StaticDashboardSource:
    """固定快照的替身数据源，不产生任何子进程与文件访问。

    :param snapshot: 初始快照；默认提供合成实例。
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
        self.calls["snapshot"] += 1
        return self._snapshot

    def probe_running(self) -> bool | None:
        self.calls["probe"] += 1
        return self._snapshot.running

    def set_running(self, value: bool | None) -> None:
        """改写替身的运行状态，模拟实例启停。"""
        self._snapshot = replace(self._snapshot, running=value)

    def set_snapshot(self, snapshot: DashboardSnapshot) -> None:
        """整份替换替身快照，模拟实例重建或版本变化。"""
        self._snapshot = snapshot


class LocalDashboardSource:
    """通过文件系统与子进程读取实例信息。

    :param root: 实例根；默认按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param start: 向上查找的起点，默认为当前工作目录。
    :param timeout: 子进程超时秒数，仅在需要补取版本时使用。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: 构造 ``Instance`` 的回调，测试可注入。
    :param module_source: 取版本用的模块数据源；默认复用 Modules 页的子进程实现。
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
            return "", i18n.t(
                "cli.tui.dashboard.update_source_probe_no_hint", source=i18n.t("cli.tui.dashboard.update_source_probe")
            )
        return hint, i18n.t("cli.tui.dashboard.update_source_probe")

    def _running_detail(self, root: Path) -> str:
        text = i18n.t("cli.tui.dashboard.running_detail_lock", path=str(root / LOCK_FILENAME))
        if self.last_probe_error:
            text = f"{text}{i18n.t('cli.tui.common.error_separator')}{self.last_probe_error}"
        return text


class DashboardPage(compat.Vertical):
    """概览页控件。

    :param source: 数据源，默认为 :class:`LocalDashboardSource`。
    :param instances: 实例清单数据源，默认读本机注册表。
    :param service_control: 服务状态与预览接口，默认直接用 CLI 侧的 service 模块。
    :param setup: 首次使用摘要的数据源；默认取应用注入的 ``dashboard_setup``，没有时用
        :class:`LocalSetupSummarySource`。
    :param init_runner: 新建实例的执行接口，默认经 ``akaribot init`` 子进程。
    :param cli_runner: 写动作的执行接口，默认经 ``akaribot <子命令>`` 子进程。
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
        height: 6;
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
    DashboardPage.short #instance-list {
        height: 4;
    }
    DashboardPage #service {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DashboardPage #setup {
        height: 2;
        padding: 0 1;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DashboardPage #setup-actions {
        height: auto;
        padding: 0 0 0 1;
    }
    DashboardPage #setup-actions Button, DashboardPage.compact #actions Button {
        height: 1;
        min-height: 1;
        max-width: 100%;
        border: none;
        padding: 0 1;
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
        height: auto;
        padding: 0 0 0 1;
    }
    DashboardPage #status {
        height: 1;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    # 文案在类定义时解析，更改 --lang 后须重启进程。
    # 低频键位通过按钮和帮助提供，避免页脚超出 80 列。
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
        setup: SetupSummarySource | None = None,
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
        self._setup_source = setup
        self._setup = SetupSummary()
        self._setup_rows: tuple[tuple[str, str], ...] = ()
        self._setup_rendered: str = ""
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
        yield compat.Static(i18n.t("cli.tui.dashboard.instances_keys_caption"), id="instances-caption", markup=False)
        yield compat.Static("", id="service", markup=False)
        yield compat.ListView(id="instance-list")
        yield compat.Static("", id="setup", markup=False)
        yield compat.ButtonFlow(
            ("goto-config", i18n.t("cli.tui.dashboard.setup_button_config")),
            ("goto-run", i18n.t("cli.tui.dashboard.setup_button_run")),
            ("goto-doctor", i18n.t("cli.tui.dashboard.setup_button_doctor")),
            id="setup-actions",
        )
        with compat.VerticalScroll(id="fields-pane"):
            yield compat.Static(i18n.t("cli.tui.dashboard.fields_placeholder"), id="fields", markup=False)
        yield compat.ButtonFlow(
            ("switch", i18n.t("cli.tui.dashboard.button_switch")),
            ("new-instance", i18n.t("cli.tui.dashboard.button_new_instance")),
            ("add-instance", i18n.t("cli.tui.dashboard.button_add_instance")),
            ("remove-instance", i18n.t("cli.tui.dashboard.button_remove_instance"), "error"),
            ("autostart", i18n.t("cli.tui.dashboard.button_autostart_off")),
            ("crash-restart", i18n.t("cli.tui.dashboard.button_crash_off")),
            ("service-toggle", i18n.t("cli.tui.dashboard.button_service_install")),
            ("refresh", i18n.t("cli.tui.dashboard.action_refresh"), "primary"),
            breaks=("remove-instance",),
            id="actions",
        )
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        compat.set_text_selection(self, False)
        # CSS 不接受值为零的 line-pad，须通过样式对象设置，确保单行按钮的标签可见。
        for _, button_id in SETUP_BUTTONS:
            self.query_one(f"#{button_id}", compat.Button).styles.line_pad = 0
        self._adapt_height()

    def activate(self) -> None:
        """首次显示时读取快照与首次使用摘要，并按周期探测锁文件。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_snapshot(force=True)
        self.refresh_instances()
        self.refresh_service()
        self.refresh_setup()
        if self.refresh_interval and self.refresh_interval > 0:
            self.set_interval(self.refresh_interval, self._on_tick)

    def focus_primary(self) -> None:
        """聚焦实例清单；为空时聚焦页面。"""
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
        except Exception as error:  # noqa: BLE001 - 注册表不可用仅显示错误提示
            self._instance_rows = ()
            if not polling:
                self.reset_pending()
            self._render_instances()
            self._set_status(i18n.t("cli.tui.dashboard.instances_failed", error=f"{type(error).__name__}: {error}"))
            return
        if not polling and rows != self._instance_rows:
            # 清单变化可能使待确认目标失效，须重新确认。
            self.reset_pending()
        self._instance_rows = rows
        self._render_instances()

    def selected_instance(self) -> InstanceRow | None:
        """返回清单中当前高亮的记录。"""
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
            rows.append(text)
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(row, markup=False)) for row in rows])
        index = self._index_of_active()
        list_view.index = index
        # 重建列表恢复高亮时，不应使确认状态失效。
        self._highlighted_key = self._highlight_key(self._instance_rows[index] if index is not None else None)
        self.query_one("#instances-caption", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.dashboard.instances_keys_caption_with_count", count=len(rows)))
        )
        self._sync_setup_actions()
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
        # 统一解析真实路径，避免将同一目录的符号链接视为不同实例。
        active = context.active_root()
        if active is None:
            return False
        return Path(row.root).expanduser().resolve() == active

    def switch_to_selected(self) -> None:
        """切换到高亮实例，并通过 CLI 设置默认实例。"""
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
                # 切换确认前不得修改默认实例，以免丢失未保存的更改。
                self._set_status(i18n.t("cli.tui.dashboard.switch_deferred"))
                return
        name = row.name or str(row.root)
        separator = i18n.t("cli.tui.common.error_separator")
        self._set_status(
            f"{i18n.t('cli.tui.dashboard.switch_done', name=name)}{separator}{self._request_default_instance(row)}"
        )

    def _request_default_instance(self, row: InstanceRow) -> str:
        # CLI 读取注册表中的默认实例，切换结果须同步写入。
        if not row.registered or not row.name:
            return i18n.t("cli.tui.dashboard.switch_default_skipped")
        app = self.app
        name = row.name
        note = i18n.t("cli.tui.dashboard.use_calling", name=name)
        if getattr(app, _USE_REQUEST_ATTR, "") == name:
            # 同一目标只启动一次注册表写入进程。
            return note
        setattr(app, _USE_REQUEST_ATTR, name)
        label = i18n.t("cli.tui.dashboard.use_label", name=name)
        # 任务由应用持有，避免页面重新挂载时取消注册表写入。
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
        # 页面重新挂载会清除状态栏，因此结果通过应用通知显示。
        if result.ok:
            compat.notify(app, i18n.t("cli.tui.dashboard.switch_default_done"), title=label)
            return
        if getattr(app, _USE_REQUEST_ATTR, "") == name:
            # 写入失败后清除请求记录，允许重试。
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
        """返回最近一次服务预览的完整输出。"""
        return self._service_preview

    def refresh_service(self) -> None:
        """读取并显示服务单元状态。"""
        self._pending_service.reset()
        try:
            self._service = self.service_control.service_status()
        except Exception as error:  # noqa: BLE001 - 服务状态读取失败仅显示错误说明
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
        # 首次激活时布局可能未完成；保留原文，渲染时按当前宽度截断。
        self._service_text = text
        self.query_one("#service", compat.Static).update(
            compat.plain_text(compat.truncate_cells(text, self._inner_width()))
        )
        self._sync_actions()

    def _sync_actions(self) -> None:
        row = self.selected_instance()
        registered = row is not None and row.registered
        self.query_one("#switch", compat.Button).disabled = self._busy or row is None or self._is_active_instance(row)
        for button_id in ("new-instance", "add-instance", "refresh"):
            self.query_one(f"#{button_id}", compat.Button).disabled = self._busy
        self.query_one("#remove-instance", compat.Button).disabled = self._busy or not registered
        self._sync_policy_button("autostart", "autostart", row)
        self._sync_policy_button("crash-restart", "restart_on_crash", row)
        service = self.query_one("#service-toggle", compat.Button)
        # 策略依赖已登记实例；服务操作还须有可用的平台后端。
        service.disabled = self._busy or not registered or self._service.backend == "unsupported"
        service.label = i18n.t(
            "cli.tui.dashboard.button_service_uninstall"
            if self._service.installed
            else "cli.tui.dashboard.button_service_install"
        )
        self.query_one("#actions", compat.ButtonFlow).relayout()

    def _sync_policy_button(self, button_id: str, field_name: str, row: InstanceRow | None) -> None:
        enabled = row is not None and (row.autostart if field_name == "autostart" else row.restart_on_crash)
        state = "on" if enabled else "off"
        prefix = "autostart" if field_name == "autostart" else "crash"
        button = self.query_one(f"#{button_id}", compat.Button)
        button.disabled = self._busy or row is None or not row.registered
        button.label = i18n.t(f"cli.tui.dashboard.button_{prefix}_{state}")
        # 标签变化可能影响按钮宽度，须重新计算布局。
        self.query_one("#actions", compat.ButtonFlow).relayout()

    def request_toggle_service(self) -> None:
        """请求安装或卸载服务，提供执行与预览选项。"""
        action, force = self._service_action()
        if not self._pending_service.accept(f"service:{action}"):
            return
        self._ask_service(action, force=force)

    def _service_action(self) -> tuple[str, bool]:
        if self._service.installed:
            return "uninstall", False
        # 缓存可能过期，确认覆盖前须重新检查单元文件。
        try:
            fresh = self.service_control.service_status()
        except Exception:  # noqa: BLE001 - 刷新失败按缓存状态处理，执行时不带 force
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
        if choice == "dry-run":
            self.preview_service(action)
            return
        if choice != action:
            self._set_status(i18n.t("cli.tui.dashboard.service_cancelled"))
            return
        self._start_service(action, force=force)

    def preview_service(self, action: str) -> None:
        """执行 ``akaribot service <动作> --dry-run``，在状态栏与预览区显示输出。"""
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
        # 串行执行写操作，避免多个子进程同时修改注册表。
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
        except Exception as error:  # noqa: BLE001 - 执行器异常仅显示错误说明
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        if track_busy:
            # 仅由设置忙状态的操作负责清除该状态。
            self._busy = False
            self._sync_actions()
        on_done(result)

    def action_toggle_service(self) -> None:
        self.request_toggle_service()

    def request_add_instance(self) -> None:
        """请求输入实例目录并登记。"""
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
        # 注册名由 CLI 生成；刷新后无法取得时使用目录名。
        wanted = root.expanduser().resolve()
        for row in self._instance_rows:
            if row.root.expanduser().resolve() == wanted:
                return row.name or wanted.name
        return root.name

    def request_new_instance(self) -> None:
        """请求输入新实例目录并选择环境方式。"""
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
        root = resolve_instance_root()
        if root is not None:
            return str(root.parent)
        return str(Path.cwd())

    def on_new_instance_path_entered(self, path: str | None) -> None:
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
        # init 负责实例登记，创建成功后刷新清单。
        self.refresh_instances()
        self._set_status(i18n.t("cli.tui.dashboard.new_done", name=self._registered_name(root), root=root))

    def request_remove_instance(self) -> None:
        """请求确认移除高亮实例的登记，保留实例目录。"""
        row = self.selected_instance()
        if row is None:
            self._set_status(i18n.t("cli.tui.dashboard.switch_no_selection"))
            return
        if not row.registered:
            self._set_status(i18n.t("cli.tui.dashboard.policy_unregistered", root=row.root))
            return
        if not self._pending_remove.accept(row.name or str(row.root)):
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.dashboard.remove_choice_title", name=row.name),
            hint=i18n.t("cli.tui.dashboard.remove_choice_hint"),
            options=(("remove", i18n.t("cli.tui.dashboard.remove_choice_confirm")),),
            cancel_label=i18n.t("cli.tui.dashboard.add_cancel"),
            callback=lambda choice: self.on_remove_choice(row, choice),
        )

    def on_remove_choice(self, row: InstanceRow, choice: str | None) -> None:
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
        self.switch_to_selected()

    def action_toggle_autostart(self) -> None:
        self.toggle_policy("autostart")

    def action_toggle_crash_restart(self) -> None:
        self.toggle_policy("restart_on_crash")

    def action_add_instance(self) -> None:
        self.request_add_instance()

    def action_new_instance(self) -> None:
        self.request_new_instance()

    def action_remove_instance(self) -> None:
        self.request_remove_instance()

    @property
    def snapshot(self) -> DashboardSnapshot:
        """返回缓存中的快照，不重新读取数据。"""
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
    def setup_summary(self) -> SetupSummary:
        """返回缓存中的首次使用摘要，不重新读取数据。"""
        return self._setup

    @property
    def setup_rows(self) -> tuple[tuple[str, str], ...]:
        """返回首次使用摘要最近一次渲染的标签与值，供自动化断言逐项核对。"""
        return self._setup_rows

    @property
    def setup_text(self) -> str:
        """返回首次使用行动区当前渲染出的纯文本。"""
        return self._setup_rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    def cache_age(self) -> float:
        """返回快照自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    def refresh_snapshot(self, *, force: bool = False) -> None:
        """读取快照。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不读取数据。
        """
        # 手动刷新使待确认目标失效，须重新确认。
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
        except Exception as error:  # noqa: BLE001 - 数据源异常都不应中断界面
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
        不启动子进程、不重取版本；探测结果与缓存相同时不重绘。
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

    def refresh_setup(self) -> None:
        """读取首次使用摘要；失败时显示原因。"""
        source = self._resolve_setup_source()
        self.run_worker(self._load_setup(source), group="dashboard-setup", exclusive=True)

    def _resolve_setup_source(self) -> SetupSummarySource:
        if self._setup_source is not None:
            return self._setup_source
        app_sources = getattr(self.app, "sources", None)
        injected = app_sources.get("dashboard_setup") if isinstance(app_sources, Mapping) else None
        self._setup_source = injected if injected is not None else LocalSetupSummarySource()
        return self._setup_source

    async def _load_setup(self, source: SetupSummarySource) -> None:
        try:
            summary = await asyncio.to_thread(source.summary)
        except Exception as error:  # noqa: BLE001 - 取数失败只降级为逐项说明
            reason = f"{type(error).__name__}: {error}"
            summary = SetupSummary(adapters_reason=reason, placeholders_reason=reason, doctor_reason=reason)
        self._setup = summary
        self._render_setup()

    def _render_setup(self) -> None:
        rows = self._setup_rows_for_render()
        self._setup_rows = rows
        # 摘要限高两行，为列表与详情保留空间；原文保留完整取值，由控件按宽度截断。
        cells = [f"{label} {value}" for label, value in rows]
        text = "\n".join("  ".join(cells[index : index + 2]) for index in range(0, len(cells), 2))
        self._setup_rendered = text
        self.query_one("#setup", compat.Static).update(compat.plain_text(text))
        self._sync_setup_actions()

    def _setup_rows_for_render(self) -> tuple[tuple[str, str], ...]:
        state = self._snapshot.state_label if self._loaded_at else _missing_text("")
        return (
            (
                i18n.t("cli.tui.dashboard.setup_adapters_label"),
                _missing_text(self._setup.adapters_reason)
                if self._setup.unconfigured_adapters is None
                else i18n.t("cli.tui.dashboard.setup_adapters_value", count=self._setup.unconfigured_adapters),
            ),
            (
                i18n.t("cli.tui.dashboard.setup_placeholders_label_estimated")
                if self._setup.placeholders_estimated
                else i18n.t("cli.tui.dashboard.setup_placeholders_label"),
                _placeholders_text(self._setup),
            ),
            (i18n.t("cli.tui.dashboard.setup_instance_label"), state),
            (
                i18n.t("cli.tui.dashboard.setup_doctor_label"),
                _missing_text(self._setup.doctor_reason)
                if self._setup.doctor_errors is None or self._setup.doctor_warnings is None
                else i18n.t(
                    "cli.tui.dashboard.setup_doctor_value",
                    errors=self._setup.doctor_errors,
                    warnings=self._setup.doctor_warnings,
                ),
            ),
        )

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
        # 运行状态和可用宽度均可能变化，须同时刷新摘要与按钮。
        self._render_setup()
        self._sync_actions()

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        if outer < 8:
            # 首次激活时宽度可能为零，使用默认宽度并在 resize 时重新布局。
            return 72
        return max(outer - 6, 16)

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        self._adapt_height()
        self._render_fields()
        self._render_service()

    def _adapt_height(self) -> None:
        compact = self.size.height < 28
        self.set_class(compact, "compact")
        self.set_class(self.size.height < 22, "short")
        for button in self.query("#actions Button"):
            button.styles.line_pad = 0 if compact else 1

    def reset_pending(self) -> None:
        """作废本页的待确认状态；切页、刷新与更换选中项后须重新确认。"""
        self._pending_service.reset()
        self._pending_remove.reset()

    @compat.on(compat.ListView.Selected, "#instance-list")
    def _on_instance_selected(self, event: compat.ListView.Selected) -> None:
        self.switch_to_selected()

    @compat.on(compat.ListView.Highlighted, "#instance-list")
    def _on_instance_highlighted(self, event: compat.ListView.Highlighted) -> None:
        # 重建列表也会触发高亮事件，须比较目标以排除显示刷新。
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
            self.refresh_setup()
        else:
            page_key = next((key for key, widget_id in SETUP_BUTTONS if widget_id == button_id), "")
            if page_key:
                self.open_setup_page(page_key)

    def _sync_setup_actions(self) -> None:
        for page_key, button_id in SETUP_BUTTONS:
            label_key, reason = self._setup_button_state(page_key)
            button = self.query_one(f"#{button_id}", compat.Button)
            button.disabled = bool(reason)
            button.label = i18n.t(label_key)
        # 禁用状态可能改变标签宽度，须重新计算布局。
        self.query_one("#setup-actions", compat.ButtonFlow).relayout()

    def _setup_button_state(self, page_key: str) -> tuple[str, str]:
        if not self._setup_has_instance():
            return f"cli.tui.dashboard.setup_button_{page_key}_blocked", i18n.t(
                "cli.tui.dashboard.setup_block_no_instance"
            )
        if page_key == "run" and self._snapshot.running is True:
            return "cli.tui.dashboard.setup_button_run_running", i18n.t("cli.tui.dashboard.setup_block_running")
        return f"cli.tui.dashboard.setup_button_{page_key}", ""

    def _setup_has_instance(self) -> bool:
        return bool(self._instance_rows) or context.active_root() is not None

    def open_setup_page(self, page_key: str) -> None:
        """切到首次使用行动区指向的页面；前提不满足时只在状态栏说明原因。

        :param page_key: 页面键，取自 :data:`SETUP_BUTTONS`。
        """
        _, reason = self._setup_button_state(page_key)
        if reason:
            self._set_status(
                i18n.t(
                    "cli.tui.dashboard.setup_blocked_status",
                    action=i18n.t(f"cli.tui.dashboard.setup_button_{page_key}"),
                    reason=reason,
                )
            )
            return
        self.app.show_page(page_key)

    def action_refresh(self) -> None:
        self.refresh_snapshot(force=True)
        self.refresh_setup()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()


def _mode_text(snapshot: DashboardSnapshot) -> str:
    mode = snapshot.instance_mode or i18n.t("cli.tui.common.unknown")
    if not snapshot.locale:
        return mode
    return i18n.t("cli.tui.dashboard.mode_with_locale", mode=mode, locale=snapshot.locale)
