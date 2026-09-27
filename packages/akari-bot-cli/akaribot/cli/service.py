"""把本机 CLI 装成常驻服务，并由它守护实例。

服务本体是 ``akaribot service supervise``：由系统服务管理器（macOS 的 launchd、Linux 的 systemd
user unit）常驻拉起，每轮读实例注册表，按记录里的 ``desired`` 与 ``restart_on_crash`` 恢复、重启
或跳过各个实例。注册表只存策略，运行期观测留在守护进程内存里。

单元文件的渲染是纯函数，系统命令经可注入的 runner 与 which 发出：没有对应系统工具的机器上也能
核对生成结果，测试不会真的调用 ``launchctl`` 或 ``systemctl``。
"""

from __future__ import annotations

import os
import plistlib
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from akaribot.cli import i18n
from akaribot.cli.instance import Instance
from akaribot.cli.instances import HOME_ENV, STATE_RUNNING, InstanceRegistry, RegistryError, registry_home
from akaribot.cli.process import pid_alive, wait_until
from akaribot.cli.tui import cli_process

BACKEND_LAUNCHD = "launchd"
BACKEND_SYSTEMD = "systemd"
BACKEND_UNSUPPORTED = "unsupported"

LAUNCHD_LABEL = "se.teahouse.akaribot.service"
LAUNCHD_UNIT_FILENAME = f"{LAUNCHD_LABEL}.plist"
LAUNCHD_TOOL = "launchctl"
SYSTEMD_UNIT_NAME = "akaribot.service"
SYSTEMD_TOOL = "systemctl"
# 单元文件里要执行的子命令；render_unit 只负责拼装，不关心它的含义。
SERVICE_COMMAND = ("service", "supervise")

DEFAULT_INTERVAL = 5.0
DEFAULT_MAX_RESTARTS = 5
DEFAULT_BACKOFF = 2.0

KIND_OBSERVED = "observed"
KIND_RECOVERED = "recovered"
KIND_RESTARTED = "restarted"
KIND_ABANDONED = "abandoned"
KIND_REFUSED = "refused"
KIND_MISSING = "missing"
KIND_NO_AUTOSTART = "no-autostart"
KIND_STRAY = "stray"
KIND_FAILED = "failed"
KIND_REGISTRY = "registry"

LOG_TAIL_CHARS = 800


class ServiceError(RuntimeError):
    """服务托管不可用：平台不受支持、单元文件已存在或系统命令失败。"""


def detect_backend(platform_name: str | None = None) -> str:
    """按平台名判定系统服务管理器。

    :param platform_name: ``sys.platform`` 风格的平台名；缺省用当前平台。
    :return: ``launchd`` / ``systemd`` / ``unsupported``。
    """
    name = platform_name or sys.platform
    if name == "darwin":
        return BACKEND_LAUNCHD
    if name.startswith("linux"):
        return BACKEND_SYSTEMD
    return BACKEND_UNSUPPORTED


def current_uid() -> int:
    """当前用户号；Windows 上没有该概念，返回 0 供展示。"""
    getter = getattr(os, "getuid", None)
    return getter() if getter is not None else 0


def supported_backends() -> tuple[str, str]:
    """返回本模块实现的两种后端名，供提示文案列举。"""
    return (BACKEND_LAUNCHD, BACKEND_SYSTEMD)


def unsupported_detail(platform_name: str | None = None) -> str:
    """平台不受支持时的说明，含可执行的下一步。"""
    head = i18n.t(
        "cli.service.unsupported",
        platform=platform_name or sys.platform,
        backends=i18n.t("cli.common.list_separator").join(supported_backends()),
    )
    return f"{head} {i18n.t('cli.service.unsupported_hint')}"


def unit_path(backend: str, *, home: Path | None = None) -> Path:
    """单元文件路径。

    :param backend: :func:`detect_backend` 的返回值之一。
    :param home: 家目录；缺省用当前用户的家目录。
    :return: 单元文件的绝对路径。
    :raises ServiceError: 平台不受支持。
    """
    base = Path(home) if home is not None else Path.home()
    if backend == BACKEND_LAUNCHD:
        return base / "Library" / "LaunchAgents" / LAUNCHD_UNIT_FILENAME
    if backend == BACKEND_SYSTEMD:
        return base / ".config" / "systemd" / "user" / SYSTEMD_UNIT_NAME
    raise ServiceError(unsupported_detail())


def default_log_dir(backend: str, *, home: Path | None = None) -> Path:
    """服务进程控制台输出的默认落盘目录。"""
    base = Path(home) if home is not None else Path.home()
    if backend == BACKEND_LAUNCHD:
        return base / "Library" / "Logs" / "akaribot"
    return base / ".local" / "state" / "akaribot"


def default_cli_argv() -> tuple[str, ...]:
    """调用本 CLI 的 argv 前缀，不含子命令。"""
    return tuple(cli_process.cli_argv())


def service_env() -> dict[str, str]:
    """服务进程需要显式带上的环境变量。

    launchd 与 systemd 都不继承登录 shell 的环境：注册表位置若只存在于安装时的 shell 里，守护
    进程会退回 ``~/.akaribot`` 去读另一份注册表，一个实例都恢复不了。安装时把注册表位置写进
    单元，服务读到的注册表与 ``service status`` 读到的就是同一份。
    """
    return {HOME_ENV: str(registry_home())}


def render_unit(
    backend: str,
    *,
    cli_argv: Sequence[str],
    workdir: Path | None = None,
    log_dir: Path,
    env: Mapping[str, str] | None = None,
) -> str:
    """渲染服务单元文件的内容。

    :param backend: :func:`detect_backend` 的返回值之一。
    :param cli_argv: 调用本 CLI 的 argv 前缀；子命令由本函数追加。
    :param workdir: 服务工作目录；``None`` 表示不在单元里声明。
    :param log_dir: 控制台输出的落盘目录。
    :param env: 服务进程的环境变量；``None`` 或空表示不在单元里声明。
    :return: 单元文件的完整文本。
    :raises ServiceError: 平台不受支持。
    """
    command = [*cli_argv, *SERVICE_COMMAND]
    if backend == BACKEND_LAUNCHD:
        return _render_launchd(command, workdir=workdir, log_dir=log_dir, env=env)
    if backend == BACKEND_SYSTEMD:
        return _render_systemd(command, workdir=workdir, log_dir=log_dir, env=env)
    raise ServiceError(unsupported_detail())


def _render_launchd(
    command: Sequence[str], *, workdir: Path | None, log_dir: Path, env: Mapping[str, str] | None = None
) -> str:
    payload: dict[str, Any] = {
        "Label": LAUNCHD_LABEL,
        "ProgramArguments": list(command),
        # 崩溃（非零退出）才拉起：正常退出说明守护循环按信号收工，不该被立刻重启。
        "KeepAlive": {"SuccessfulExit": False},
        "RunAtLoad": True,
        "ProcessType": "Background",
        "StandardOutPath": str(log_dir / "service.log"),
        "StandardErrorPath": str(log_dir / "service.err.log"),
    }
    if workdir is not None:
        payload["WorkingDirectory"] = str(workdir)
    if env:
        payload["EnvironmentVariables"] = dict(sorted(env.items()))
    return plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False).decode("utf-8")


def _render_systemd(
    command: Sequence[str], *, workdir: Path | None, log_dir: Path, env: Mapping[str, str] | None = None
) -> str:
    lines = [
        "[Unit]",
        f"Description={i18n.t('cli.service.unit.description')}",
        "After=network-online.target",
        "Wants=network-online.target",
        "",
        "[Service]",
        "Type=simple",
        f"ExecStart={_systemd_argv(command)}",
        "Restart=on-failure",
        "RestartSec=5",
        f"StandardOutput=append:{log_dir / 'service.log'}",
        f"StandardError=append:{log_dir / 'service.err.log'}",
    ]
    if workdir is not None:
        lines.append(f"WorkingDirectory={workdir}")
    lines += [f"Environment={_systemd_env(name, value)}" for name, value in sorted((env or {}).items())]
    lines += ["", "[Install]", "WantedBy=default.target", ""]
    return "\n".join(lines)


def _systemd_env(name: str, value: str) -> str:
    # Environment= 按空白切分赋值，值里含空白或引号时整个赋值要加引号并转义。
    assignment = f"{name}={value}"
    if value and not any(char in assignment for char in " \t\"'\\"):
        return assignment
    escaped = assignment.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _systemd_argv(command: Sequence[str]) -> str:
    return " ".join(_systemd_quote(argument) for argument in command)


def _systemd_quote(argument: str) -> str:
    # systemd 会展开未转义的 ``$``，含空格或特殊字符的参数必须加引号并逐项转义。
    if argument and not any(char in argument for char in " \t\"'\\$"):
        return argument
    escaped = argument.replace("\\", "\\\\").replace('"', '\\"').replace("$", "$$")
    return f'"{escaped}"'


def system_runner(argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
    """默认的系统命令执行器：捕获输出，不因非零退出抛异常。

    :param argv: 命令行参数。
    :return: 已完成的子进程。
    """
    return subprocess.run(list(argv), capture_output=True, text=True, check=False)  # noqa: S603 - 参数由本模块拼装


CommandRunner = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]
WhichFn = Callable[[str], str | None]


@dataclass(frozen=True)
class ServiceStatus:
    """服务单元的状态。

    :param backend: ``launchd`` / ``systemd`` / ``unsupported``。
    :param installed: 单元文件是否存在。
    :param enabled: 系统是否已注册该服务；探测不到时为 ``None``。
    :param path: 单元文件路径；平台不受支持时为 ``None``。
    :param detail: 面向用户的一句话说明。
    """

    backend: str
    installed: bool
    enabled: bool | None
    path: Path | None = None
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        """转为 ``--json`` 输出用的字典。"""
        return {
            "backend": self.backend,
            "installed": self.installed,
            "enabled": self.enabled,
            "path": str(self.path) if self.path is not None else "",
            "detail": self.detail,
        }


@dataclass
class ServiceBackend:
    """一个系统服务管理器后端。

    :param kind: ``launchd`` / ``systemd`` / ``unsupported``。
    :param home: 家目录，单元文件与默认日志目录都相对它定位。
    :param workdir: 服务的工作目录；缺省用注册表目录，``None`` 表示不在单元里声明。
    :param env: 服务进程的环境变量；缺省带上当前注册表位置。
    :param runner: 系统命令执行器，测试注入替身后不会真的调用系统工具。
    :param which: 系统工具查找器。
    :param cli_argv: 调用本 CLI 的 argv 前缀。
    :param uid: launchd 域里的用户号。
    """

    kind: str = field(default_factory=detect_backend)
    home: Path = field(default_factory=Path.home)
    # 缺省工作目录取注册表目录：界面与命令行走同一个缺省，装出来的单元才一致。
    workdir: Path | None = field(default_factory=registry_home)
    env: Mapping[str, str] = field(default_factory=service_env)
    runner: CommandRunner = system_runner
    which: WhichFn = shutil.which
    cli_argv: tuple[str, ...] = field(default_factory=default_cli_argv)
    uid: int = field(default_factory=current_uid)

    def tool(self) -> str:
        """本后端要用的系统工具名。"""
        return LAUNCHD_TOOL if self.kind == BACKEND_LAUNCHD else SYSTEMD_TOOL

    def path(self) -> Path:
        """单元文件路径。

        :raises ServiceError: 平台不受支持。
        """
        return unit_path(self.kind, home=self.home)

    def log_dir(self) -> Path:
        """服务进程控制台输出的落盘目录。"""
        return default_log_dir(self.kind, home=self.home)

    def render(self) -> str:
        """渲染单元文件内容。

        :raises ServiceError: 平台不受支持。
        """
        return render_unit(
            self.kind, cli_argv=self.cli_argv, workdir=self.workdir, log_dir=self.log_dir(), env=self.env
        )

    def install(self, *, dry_run: bool = False, force: bool = False) -> ServiceStatus:
        """写入单元文件并注册服务。

        :param dry_run: 只生成内容，不落盘也不调用系统工具。
        :param force: 单元文件已存在时覆盖它。
        :return: 安装后的状态；``enabled`` 为 ``None`` 表示系统工具不可用、尚未注册。
        :raises ServiceError: 平台不受支持，或单元文件已存在而未指定 ``force``。
        """
        self._require_supported()
        path = self.path()
        if path.exists() and not force and not dry_run:
            raise ServiceError(
                i18n.t("cli.service.install.exists", path=path, hint=i18n.t("cli.service.install.exists_hint"))
            )
        if dry_run:
            key = "cli.service.install.dry_run_exists" if path.exists() else "cli.service.install.dry_run"
            detail = i18n.t(key, path=path, tool=self.tool())
            return ServiceStatus(self.kind, path.exists(), None, path, detail)
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.workdir is not None:
            self.workdir.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(), encoding="utf-8")
        enabled, detail = self._register(path)
        return ServiceStatus(self.kind, True, enabled, path, detail)

    def uninstall(self, *, dry_run: bool = False) -> ServiceStatus:
        """注销服务并删除单元文件。

        :param dry_run: 只报告将要做什么，不注销也不删除。
        :return: 卸载后的状态；本来就没装时 ``installed`` 为假且不视为失败。
        :raises ServiceError: 平台不受支持。
        """
        self._require_supported()
        path = self.path()
        if not path.exists():
            return ServiceStatus(self.kind, False, None, path, i18n.t("cli.service.uninstall.absent", path=path))
        if dry_run:
            return ServiceStatus(
                self.kind, True, None, path, i18n.t("cli.service.uninstall.dry_run", path=path, tool=self.tool())
            )
        enabled, detail = self._unregister(path)
        try:
            path.unlink()
        except OSError as error:
            return ServiceStatus(
                self.kind, True, enabled, path, i18n.t("cli.service.uninstall.remove_failed", path=path, error=error)
            )
        return ServiceStatus(self.kind, False, enabled, path, detail)

    def status(self) -> ServiceStatus:
        """读取服务状态，只用只读命令探测是否已注册。"""
        if self.kind == BACKEND_UNSUPPORTED:
            return ServiceStatus(BACKEND_UNSUPPORTED, False, None, None, unsupported_detail())
        path = self.path()
        enabled, detail = self._probe()
        return ServiceStatus(self.kind, path.exists(), enabled, path, detail)

    def _require_supported(self) -> None:
        if self.kind == BACKEND_UNSUPPORTED:
            raise ServiceError(unsupported_detail())

    def _call(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str] | None:
        try:
            return self.runner(list(argv))
        except OSError:
            return None

    def _register(self, path: Path) -> tuple[bool | None, str]:
        tool = self.tool()
        if not self.which(tool):
            return None, i18n.t("cli.service.install.tool_missing", tool=tool, path=path)
        if self.kind == BACKEND_LAUNCHD:
            domain = f"gui/{self.uid}"
            first = self._call([LAUNCHD_TOOL, "bootstrap", domain, str(path)])
            if first is not None and first.returncode == 0:
                return True, i18n.t("cli.service.install.registered", tool=tool)
            # 部分 macOS 版本的 launchctl 只实现 load；bootstrap 失败时退回它，两者语义一致。
            second = self._call([LAUNCHD_TOOL, "load", "-w", str(path)])
            if second is not None and second.returncode == 0:
                return True, i18n.t("cli.service.install.registered", tool=tool)
            return False, _failure_detail("cli.service.install.register_failed", tool, second or first)
        reloaded = self._call([SYSTEMD_TOOL, "--user", "daemon-reload"])
        if reloaded is None or reloaded.returncode != 0:
            return False, _failure_detail("cli.service.install.register_failed", tool, reloaded)
        enabled = self._call([SYSTEMD_TOOL, "--user", "enable", "--now", SYSTEMD_UNIT_NAME])
        if enabled is not None and enabled.returncode == 0:
            return True, i18n.t("cli.service.install.registered", tool=tool)
        return False, _failure_detail("cli.service.install.register_failed", tool, enabled)

    def _unregister(self, path: Path) -> tuple[bool | None, str]:
        tool = self.tool()
        if not self.which(tool):
            return None, i18n.t("cli.service.uninstall.tool_missing", tool=tool, path=path)
        if self.kind == BACKEND_LAUNCHD:
            first = self._call([LAUNCHD_TOOL, "bootout", f"gui/{self.uid}/{LAUNCHD_LABEL}"])
            if first is not None and first.returncode == 0:
                return False, i18n.t("cli.service.uninstall.done", tool=tool, path=path)
            second = self._call([LAUNCHD_TOOL, "unload", "-w", str(path)])
            if second is not None and second.returncode == 0:
                return False, i18n.t("cli.service.uninstall.done", tool=tool, path=path)
            return False, _failure_detail("cli.service.uninstall.unregister_failed", tool, second or first)
        disabled = self._call([SYSTEMD_TOOL, "--user", "disable", "--now", SYSTEMD_UNIT_NAME])
        if disabled is None or disabled.returncode != 0:
            return False, _failure_detail("cli.service.uninstall.unregister_failed", tool, disabled)
        return False, i18n.t("cli.service.uninstall.done", tool=tool, path=path)

    def _probe(self) -> tuple[bool | None, str]:
        tool = self.tool()
        if not self.which(tool):
            return None, i18n.t("cli.service.status.tool_missing", tool=tool)
        if self.kind == BACKEND_LAUNCHD:
            argv = [LAUNCHD_TOOL, "print", f"gui/{self.uid}/{LAUNCHD_LABEL}"]
        else:
            argv = [SYSTEMD_TOOL, "--user", "is-enabled", SYSTEMD_UNIT_NAME]
        result = self._call(argv)
        if result is None:
            return None, i18n.t("cli.service.status.probe_failed", tool=tool)
        if result.returncode == 0:
            return True, i18n.t("cli.service.status.registered", tool=tool)
        return False, i18n.t("cli.service.status.unregistered", tool=tool)


def _failure_detail(key: str, tool: str, result: subprocess.CompletedProcess[str] | None) -> str:
    code = result.returncode if result is not None else -1
    return i18n.t(key, tool=tool, code=code, detail=_tail(result))


def _tail(result: subprocess.CompletedProcess[str] | None) -> str:
    # 系统工具的失败原因写在 stderr，取尾部供排障。
    if result is None:
        return ""
    text = (result.stderr or result.stdout or "").strip()
    return text[-LOG_TAIL_CHARS:]


@dataclass(frozen=True)
class SuperviseEvent:
    """守护循环里的一处状态变化。

    :param kind: 事件类型，见 ``KIND_*``。
    :param name: 实例注册名；注册表读取失败时为空串。
    :param message: 面向用户的一句话说明。
    """

    kind: str
    name: str
    message: str


@dataclass(frozen=True)
class SuperviseRound:
    """一轮守护的结论。

    :param events: 本轮发生的变化；状态没变时为空。
    :param checked: 本轮检查的实例数。
    :param running: 观察到正在运行的实例数。
    :param started: 恢复拉起的实例数。
    :param restarted: 自动重启的实例数。
    :param failed: 拉起失败的实例数。
    :param abandoned: 放弃守护的实例数（达到重启上限，或策略禁止重启）。
    :param skipped: 跳过的实例数（目录不存在，或期望停止却在跑）。
    """

    events: tuple[SuperviseEvent, ...] = ()
    checked: int = 0
    running: int = 0
    started: int = 0
    restarted: int = 0
    failed: int = 0
    abandoned: int = 0
    skipped: int = 0


@dataclass
class _Watch:
    seen_running: bool = False
    recovery_done: bool = False
    restarts: int = 0
    next_restart_at: float = 0.0
    abandoned: bool = False
    label: str = ""


@dataclass
class _Tally:
    checked: int = 0
    running: int = 0
    started: int = 0
    restarted: int = 0
    failed: int = 0
    abandoned: int = 0
    skipped: int = 0


def default_spawn(controller: Instance) -> int:
    """拉起实例并等它取到锁。

    :param controller: 目标实例。
    :return: 实例进程号。
    :raises ServiceError: 进程未在就绪时限内取到锁。
    """
    # 就绪时限与控制台日志路径都以 run --detach 为准，故就地取用它的实现，避免两处判据分叉。
    from akaribot.cli.commands.run import READY_TIMEOUT_SECONDS, console_log_path

    log_path = console_log_path(controller.root)
    launched = controller.spawn_detached(log_path=log_path)
    ready = wait_until(lambda: controller.is_running() or not pid_alive(launched.pid), timeout=READY_TIMEOUT_SECONDS)
    if ready and controller.is_running():
        return launched.pid
    raise ServiceError(
        i18n.t(
            "cli.service.supervise.start_failed",
            pid=launched.pid,
            log=launched.log_path,
            tail=_log_tail(launched.log_path),
        )
    )


def _log_tail(path: Path, limit: int = LOG_TAIL_CHARS) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return text.strip()[-limit:] or i18n.t("cli.common.no_output")


class Supervisor:
    """按注册表里的策略守护本机实例。

    :param registry: 实例注册表。
    :param open_instance: 由实例根构造控制器；测试可注入替身。
    :param spawn: 拉起实例并返回进程号；测试可注入替身。
    :param clock: 单调时钟，退避判定与用例时间推进都用它。
    :param max_restarts: 单个实例允许的自动重启次数上限。
    :param backoff: 指数退避的基数秒数。
    """

    def __init__(
        self,
        *,
        registry: InstanceRegistry | None = None,
        open_instance: Callable[[Path], Any] = Instance,
        spawn: Callable[[Any], int] = default_spawn,
        clock: Callable[[], float] = time.monotonic,
        max_restarts: int = DEFAULT_MAX_RESTARTS,
        backoff: float = DEFAULT_BACKOFF,
    ) -> None:
        self.registry = registry if registry is not None else InstanceRegistry()
        self.open_instance = open_instance
        self.spawn = spawn
        self.clock = clock
        self.max_restarts = max(0, max_restarts)
        self.backoff = max(0.0, backoff)
        self._watch: dict[str, _Watch] = {}
        self._registry_error = ""

    def run_once(self) -> SuperviseRound:
        """跑一轮守护并返回本轮结论。

        观测表只活在进程内：注册表存策略，重启计数与「见过它在跑」都是本次服务运行期的判断依据。
        """
        now = self.clock()
        events: list[SuperviseEvent] = []
        tally = _Tally()
        try:
            entries = self.registry.load()
        except RegistryError as error:
            self._note_registry_error(events, str(error))
            return SuperviseRound(events=tuple(events))
        self._registry_error = ""
        for entry in entries:
            self._visit(entry, now, events, tally)
        return SuperviseRound(events=tuple(events), **vars(tally))

    def _visit(self, entry: Any, now: float, events: list[SuperviseEvent], tally: _Tally) -> None:
        watch = self._watch.setdefault(entry.name, _Watch())
        tally.checked += 1
        if not entry.exists:
            tally.skipped += 1
            self._note(
                events,
                watch,
                entry.name,
                KIND_MISSING,
                i18n.t("cli.service.supervise.missing", name=entry.name, root=entry.root),
            )
            return
        controller = self.open_instance(entry.root)
        running = bool(controller.is_running())
        if entry.desired != STATE_RUNNING:
            if running:
                # 用户可能正在前台跑着，守护循环不动它，只说明现状。
                tally.skipped += 1
                state = controller.run_state()
                self._note(
                    events,
                    watch,
                    entry.name,
                    KIND_STRAY,
                    i18n.t("cli.service.supervise.stray", name=entry.name, pid=state.pid or 0),
                )
            else:
                watch.label = ""
            return
        if running:
            watch.seen_running = True
            tally.running += 1
            state = controller.run_state()
            self._note(
                events,
                watch,
                entry.name,
                KIND_OBSERVED,
                i18n.t("cli.service.supervise.observed", name=entry.name, pid=state.pid or 0),
            )
            return
        self._handle_down(entry, watch, controller, now, events, tally)

    def _handle_down(
        self, entry: Any, watch: _Watch, controller: Any, now: float, events: list[SuperviseEvent], tally: _Tally
    ) -> None:
        # 本次服务启动后还没见过它运行，说明是掉电或退出后的恢复：只有开了开机自启的实例才恢复，
        # 「上次在跑」本身不构成自启的理由。见过它运行过的才按崩溃处理。
        if not watch.seen_running and not watch.recovery_done:
            watch.recovery_done = True
            if not entry.autostart:
                watch.abandoned = True
                tally.skipped += 1
                self._note(
                    events,
                    watch,
                    entry.name,
                    KIND_NO_AUTOSTART,
                    i18n.t("cli.service.supervise.no_autostart", name=entry.name),
                )
                return
            self._launch(entry, watch, controller, events, tally, recovered=True)
            return
        if watch.abandoned:
            return
        if not entry.restart_on_crash:
            watch.abandoned = True
            tally.abandoned += 1
            self._note(
                events,
                watch,
                entry.name,
                KIND_REFUSED,
                i18n.t("cli.service.supervise.refused", name=entry.name),
            )
            return
        if watch.restarts >= self.max_restarts:
            watch.abandoned = True
            tally.abandoned += 1
            self._note(
                events,
                watch,
                entry.name,
                KIND_ABANDONED,
                i18n.t(
                    "cli.service.supervise.abandoned",
                    name=entry.name,
                    count=watch.restarts,
                    max=self.max_restarts,
                ),
            )
            return
        if watch.next_restart_at == 0.0:
            watch.next_restart_at = now + self.backoff * (2**watch.restarts)
        if now < watch.next_restart_at:
            return
        self._launch(entry, watch, controller, events, tally, recovered=False)

    def _launch(
        self,
        entry: Any,
        watch: _Watch,
        controller: Any,
        events: list[SuperviseEvent],
        tally: _Tally,
        *,
        recovered: bool,
    ) -> None:
        if not recovered:
            watch.restarts += 1
        try:
            pid = self.spawn(controller)
        except Exception as error:  # noqa: BLE001 - 拉起失败的原因照实上报，守护循环不因此中断
            tally.failed += 1
            watch.next_restart_at = 0.0
            label = f"{KIND_FAILED}:{watch.restarts}" if not recovered else KIND_FAILED
            self._note(
                events,
                watch,
                entry.name,
                label,
                i18n.t("cli.service.supervise.failed", name=entry.name, error=error),
            )
            return
        watch.seen_running = True
        watch.recovery_done = True
        watch.next_restart_at = 0.0
        if recovered:
            tally.started += 1
            self._note(
                events,
                watch,
                entry.name,
                KIND_RECOVERED,
                i18n.t("cli.service.supervise.recovered", name=entry.name, pid=pid),
            )
            return
        tally.restarted += 1
        self._note(
            events,
            watch,
            entry.name,
            f"{KIND_RESTARTED}:{watch.restarts}",
            i18n.t(
                "cli.service.supervise.restarted",
                name=entry.name,
                count=watch.restarts,
                max=self.max_restarts,
            ),
        )

    def _note(self, events: list[SuperviseEvent], watch: _Watch, name: str, label: str, message: str) -> None:
        # 每轮只在状态变化时输出：标签不变就不再重复同一件事。
        if watch.label == label:
            return
        watch.label = label
        events.append(SuperviseEvent(label.split(":", 1)[0], name, message))

    def _note_registry_error(self, events: list[SuperviseEvent], message: str) -> None:
        if self._registry_error == message:
            return
        self._registry_error = message
        events.append(SuperviseEvent(KIND_REGISTRY, "", message))
