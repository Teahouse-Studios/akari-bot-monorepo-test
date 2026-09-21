"""Run 页：启动 / 停止 / 重启实例，并显示子进程状态表。

数据流：界面只读 :class:`RunSource`；默认实现 :class:`SubprocessRunSource` 以
``akaribot run`` 子进程启停实例（POSIX 下自建进程组，停止时向整组发信号），状态表由本页
启动的 Popen 对象与实例锁文件共同推出。启停走后台任务，状态表刷新只轮询 Popen 与锁文件。
"""

from __future__ import annotations

import asyncio
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat

STATE_RUNNING = "running"
STATE_STOPPED = "stopped"
STATE_EXITED = "exited"
STATE_UNKNOWN = "unknown"

RUN_LABEL = "akaribot run"
CLI_ENV_BIN = "AKARIBOT_CLI_BIN"
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"
LOCK_FILENAME = ".bot.lock"
RUN_LOG_PREFIX = "TuiRun"

# 状态与表头都是按当前语言取的展示标签，故这里只存文案键，取值一律在渲染时进行。
_STATE_KEYS = {
    STATE_RUNNING: "cli.tui.run.state_running",
    STATE_STOPPED: "cli.tui.run.state_stopped",
    STATE_EXITED: "cli.tui.run.state_exited",
    STATE_UNKNOWN: "cli.tui.run.state_unknown",
}
_STATE_MARKS = {STATE_RUNNING: "●", STATE_STOPPED: "○", STATE_EXITED: "◌", STATE_UNKNOWN: "?"}

_TABLE_COLUMNS = (
    "cli.tui.run.col_label",
    "cli.tui.run.col_state",
    "cli.tui.run.col_pid",
    "cli.tui.run.col_started",
    "cli.tui.run.col_exit_code",
    "cli.tui.run.col_detail",
)


@dataclass(frozen=True)
class ProcessRecord:
    """状态表里的一行。

    :param label: 目标名，通常是 ``akaribot run``。
    :param pid: 进程号；未启动或由外部进程持锁时为空。
    :param started_at: 启动时间，展示用本地时间字符串。
    :param exit_code: 退出码；仍在运行或未曾启动时为空。
    :param state: ``running`` / ``stopped`` / ``exited`` / ``unknown``。
    :param origin: 记录来源：``本界面启动`` / ``外部进程`` / ``替身`` 等。
    :param detail: 备注，通常是启动命令或锁文件路径。
    """

    label: str = RUN_LABEL
    pid: int | None = None
    started_at: str = ""
    exit_code: int | None = None
    state: str = STATE_UNKNOWN
    origin: str = ""
    detail: str = ""

    @property
    def state_label(self) -> str:
        """返回带状态标记的本地化状态标签。"""
        key = _STATE_KEYS.get(self.state)
        label = i18n.t(key) if key else self.state
        return f"{_STATE_MARKS.get(self.state, '?')} {label}"

    @property
    def running(self) -> bool:
        """该行是否表示进程正在运行。"""
        return self.state == STATE_RUNNING


@dataclass(frozen=True)
class RunResult:
    """一次启停操作的结果。

    :param ok: 操作是否成功。
    :param message: 一行结论，用于状态栏与通知。
    :param detail: 失败时的补充信息，或成功时的命令与日志路径。
    """

    ok: bool
    message: str
    detail: str = ""


@runtime_checkable
class RunSource(Protocol):
    """运行控制数据源接口；测试注入替身，生产走子进程。"""

    def status(self) -> Sequence[ProcessRecord]:
        """返回状态表，本轮至少一行。"""

    def start(self) -> RunResult:
        """启动实例。"""

    def stop(self) -> RunResult:
        """停止本页启动的实例。"""

    def restart(self) -> RunResult:
        """先停后启。"""


class StaticRunSource:
    """替身数据源：不产生任何子进程，启停只累加调用次数并做状态迁移。

    :param records: 初始状态表；缺省给一行「已停止」。
    :param running_pid: 启动成功后上报的 PID。
    :param stop_exit_code: 停止后上报的退出码。
    :param results: 覆盖 ``start`` / ``stop`` / ``restart`` 的返回值；覆盖时不再迁移状态表。
    """

    def __init__(
        self,
        records: Sequence[ProcessRecord] = (),
        *,
        running_pid: int = 4242,
        stop_exit_code: int = 0,
        results: dict[str, RunResult] | None = None,
    ) -> None:
        self.records: list[ProcessRecord] = list(records) or [
            ProcessRecord(
                label=RUN_LABEL,
                state=STATE_STOPPED,
                origin=i18n.t("cli.tui.run.origin_stub"),
                detail=i18n.t("cli.tui.run.detail_not_started"),
            )
        ]
        self.running_pid = running_pid
        self.stop_exit_code = stop_exit_code
        self.started_at = "2026-01-01 00:00:00"
        self.calls = {"status": 0, "start": 0, "stop": 0, "restart": 0}
        self._results = dict(results or {})

    def set_result(self, action: str, result: RunResult) -> None:
        """覆盖某个动作的返回值；覆盖后该动作不再迁移状态表。

        :param action: ``start`` / ``stop`` / ``restart``。
        :param result: 该动作要返回的结果。
        """
        self._results[action] = result

    def status(self) -> Sequence[ProcessRecord]:
        """见 :meth:`RunSource.status`。"""
        self.calls["status"] += 1
        return tuple(self.records)

    def start(self) -> RunResult:
        """见 :meth:`RunSource.start`。"""
        self.calls["start"] += 1
        override = self._results.get("start")
        if override is not None:
            return override
        self.records = [
            ProcessRecord(
                label=RUN_LABEL,
                pid=self.running_pid,
                started_at=self.started_at,
                state=STATE_RUNNING,
                origin=i18n.t("cli.tui.run.origin_stub"),
                detail="stub run",
            )
        ]
        return RunResult(True, i18n.t("cli.tui.run.msg_started", pid=self.running_pid), "stub run")

    def stop(self) -> RunResult:
        """见 :meth:`RunSource.stop`。"""
        self.calls["stop"] += 1
        override = self._results.get("stop")
        if override is not None:
            return override
        pid = self.records[0].pid if self.records else None
        self.records = [
            ProcessRecord(
                label=RUN_LABEL,
                pid=pid,
                started_at=self.started_at,
                exit_code=self.stop_exit_code,
                state=STATE_EXITED,
                origin=i18n.t("cli.tui.run.origin_stub"),
                detail="stub stop",
            )
        ]
        return RunResult(
            True,
            i18n.t("cli.tui.run.msg_stopped"),
            i18n.t("cli.tui.run.detail_pid_exit", pid=pid, code=self.stop_exit_code),
        )

    def restart(self) -> RunResult:
        """见 :meth:`RunSource.restart`。"""
        self.calls["restart"] += 1
        override = self._results.get("restart")
        if override is not None:
            return override
        self.running_pid += 1
        self.records = [
            ProcessRecord(
                label=RUN_LABEL,
                pid=self.running_pid,
                started_at=self.started_at,
                state=STATE_RUNNING,
                origin=i18n.t("cli.tui.run.origin_stub"),
                detail="stub restart",
            )
        ]
        return RunResult(True, i18n.t("cli.tui.run.msg_restarted", pid=self.running_pid), "stub restart")


class SubprocessRunSource:
    """默认数据源：以 ``akaribot run`` 子进程启停实例，CLI 进程内不 import core。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param start: 向上查找的起点，缺省为当前工作目录。
    :param timeout: 停止时等待退出的秒数，超时后向进程组发强杀信号。
    :param popen: 子进程构造器，签名同 :func:`subprocess.Popen`，测试可注入替身。
    :param kill: 向进程组发信号的函数 ``(pid, force) -> 是否已发送``，测试可注入。
    :param instance_factory: 构造 ``Instance`` 的回调，测试可注入以避开 T5.1 的实现。
    :param log_path: 子进程标准输出的落盘路径；缺省为 ``<实例根>/logs/TuiRun_<日期>.log``。
    :param now: 返回展示用时间字符串的回调，测试可注入固定值。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        start: Path | str | None = None,
        timeout: float = 10.0,
        popen: Callable[..., Any] | None = None,
        kill: Callable[[int, bool], bool] | None = None,
        instance_factory: Callable[[Path], Any] | None = None,
        log_path: Path | str | None = None,
        now: Callable[[], str] | None = None,
    ) -> None:
        self.root = Path(root) if root is not None else None
        self.start_dir = Path(start) if start is not None else None
        self.timeout = timeout
        self.label = RUN_LABEL
        self.calls = {"status": 0, "start": 0, "stop": 0, "restart": 0}
        self.last_error = ""
        self._popen = popen or subprocess.Popen
        self._kill = kill or default_kill
        self._instance_factory = instance_factory
        self._log_path = Path(log_path) if log_path is not None else None
        self._now = now or (lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._process: Any | None = None
        self._log_handle: Any | None = None
        self._started_at = ""
        self._argv_text = ""
        self._history: ProcessRecord | None = None

    def status(self) -> Sequence[ProcessRecord]:
        """见 :meth:`RunSource.status`：本界面启动的进程优先，其次报告外部持锁进程。"""
        self.calls["status"] += 1
        process = self._process
        if process is not None:
            code = process.poll()
            if code is None:
                return (
                    ProcessRecord(
                        label=self.label,
                        pid=getattr(process, "pid", None),
                        started_at=self._started_at,
                        state=STATE_RUNNING,
                        origin=i18n.t("cli.tui.run.origin_ui"),
                        detail=self._argv_text,
                    ),
                )
            self._history = ProcessRecord(
                label=self.label,
                pid=getattr(process, "pid", None),
                started_at=self._started_at,
                exit_code=int(code),
                state=STATE_EXITED,
                origin=i18n.t("cli.tui.run.origin_ui"),
                detail=self._argv_text,
            )
            self._process = None
            self._close_log()
        running = self.probe_running()
        if running:
            return (
                ProcessRecord(
                    label=self.label,
                    state=STATE_RUNNING,
                    origin=i18n.t("cli.tui.run.origin_external"),
                    detail=i18n.t("cli.tui.run.detail_lock_held", path=self._lock_path()),
                ),
            )
        if running is None:
            return (
                ProcessRecord(
                    label=self.label,
                    state=STATE_UNKNOWN,
                    origin=i18n.t("cli.tui.run.origin_probe_failed"),
                    detail=self.last_error,
                ),
            )
        if self._history is not None:
            return (self._history,)
        return (
            ProcessRecord(
                label=self.label,
                state=STATE_STOPPED,
                origin="",
                detail=i18n.t("cli.tui.run.detail_never_started"),
            ),
        )

    def start(self) -> RunResult:
        """见 :meth:`RunSource.start`：执行 ``akaribot run``，标准输出落盘到日志文件。"""
        self.calls["start"] += 1
        if self._process is not None and self._process.poll() is None:
            return RunResult(
                False,
                i18n.t("cli.tui.run.msg_already_running"),
                f"PID {getattr(self._process, 'pid', None)}",
            )
        root = self._root()
        if root is None:
            self.last_error = i18n.t("cli.tui.run.error_no_instance", origin=self._origin_text())
            return RunResult(False, i18n.t("cli.tui.run.msg_no_instance"), self.last_error)
        argv = self.cli_argv("run")
        log_file = self._log_path or (root / "logs" / f"{RUN_LOG_PREFIX}_{datetime.now().strftime('%Y-%m-%d')}.log")
        handle: Any | None = None
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handle = log_file.open("ab")
            process = self._popen(argv, **self._popen_kwargs(root, handle))
        except (OSError, ValueError) as error:
            if handle is not None:
                handle.close()
            self.last_error = f"{type(error).__name__}: {error}"
            return RunResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=i18n.t("cli.tui.run.label_start")),
                self.last_error,
            )
        self._process = process
        self._log_handle = handle
        self._history = None
        self._started_at = self._now()
        self._argv_text = " ".join(argv)
        self.last_error = ""
        return RunResult(
            True,
            i18n.t("cli.tui.run.msg_started", pid=getattr(process, "pid", None)),
            i18n.t("cli.tui.run.detail_start_output", cmd=self._argv_text, path=log_file),
        )

    def stop(self) -> RunResult:
        """见 :meth:`RunSource.stop`：先温和终止进程组，超时后强杀。"""
        self.calls["stop"] += 1
        process = self._process
        if process is None or process.poll() is not None:
            if self.probe_running():
                return RunResult(
                    False,
                    i18n.t("cli.tui.run.msg_stop_external"),
                    i18n.t("cli.tui.run.detail_lock_held", path=self._lock_path()),
                )
            return RunResult(False, i18n.t("cli.tui.run.msg_not_running"), "")
        pid = getattr(process, "pid", None)
        forced = False
        self._request_stop(process, force=False)
        try:
            process.wait(timeout=self.timeout)
        except Exception:  # noqa: BLE001 - 超时或替身不支持等待，转为强杀
            forced = True
            self._request_stop(process, force=True)
            try:
                process.wait(timeout=self.timeout)
            except Exception as error:  # noqa: BLE001 - 强杀后仍等待失败，如实上报
                self.last_error = f"{type(error).__name__}: {error}"
                return RunResult(False, i18n.t("cli.tui.run.msg_stop_failed_pid", pid=pid), self.last_error)
        code = process.poll()
        return RunResult(
            True,
            i18n.t("cli.tui.run.msg_stopped_forced") if forced else i18n.t("cli.tui.run.msg_stopped"),
            i18n.t(
                "cli.tui.run.detail_pid_exit",
                pid=pid,
                code=i18n.t("cli.tui.common.unknown") if code is None else code,
            ),
        )

    def restart(self) -> RunResult:
        """见 :meth:`RunSource.restart`：先停后启，停止失败则中止。"""
        self.calls["restart"] += 1
        if self._process is not None and self._process.poll() is None:
            stopped = self.stop()
            if not stopped.ok:
                return RunResult(
                    False,
                    i18n.t("cli.tui.run.msg_restart_aborted", message=stopped.message),
                    stopped.detail,
                )
        started = self.start()
        if not started.ok:
            return RunResult(
                False,
                i18n.t("cli.tui.run.msg_restart_failed", message=started.message),
                started.detail,
            )
        return RunResult(True, i18n.t("cli.tui.run.msg_restarted_with", message=started.message), started.detail)

    def probe_running(self) -> bool | None:
        """探测实例是否在运行：优先询问 ``Instance.is_running()``，失败时直接读锁文件。"""
        self.last_error = ""
        root = self._root()
        if root is None:
            self.last_error = i18n.t("cli.tui.run.error_root_unknown", origin=self._origin_text())
            return None
        instance = self._instance(root)
        if instance is not None:
            try:
                return bool(instance.is_running())
            except Exception as error:  # noqa: BLE001 - 降级到本地锁探测
                self.last_error = i18n.t(
                    "cli.tui.run.error_probe_failed",
                    kind=type(error).__name__,
                    error=error,
                )
        from akaribot.cli.tui.dashboard import lock_held

        return lock_held(root / LOCK_FILENAME)

    def cli_argv(self, *args: str) -> list[str]:
        """构造调用本 CLI 的 argv，规则与 Modules 页的子进程数据源一致。

        :param args: 子命令及其参数。
        :return: 可直接交给 :mod:`subprocess` 的参数列表。
        """
        override = os.environ.get(CLI_ENV_BIN)
        if override:
            return [override, *args]
        frozen = bool(getattr(sys, "frozen", False)) or hasattr(sys, "__compiled__")
        if frozen:
            return [sys.executable, *args]
        return [sys.executable, "-m", "akaribot.cli.main", *args]

    def _root(self) -> Path | None:
        """返回实例根，显式给定者优先。"""
        if self.root is not None:
            return self.root
        from akaribot.cli.tui.dashboard import resolve_instance_root

        return resolve_instance_root(self.start_dir)

    def _origin_text(self) -> str:
        """定位失败时用于展示的候选路径。"""
        return str(self.root or self.start_dir or Path.cwd())

    def _lock_path(self) -> Path:
        """返回锁文件路径，实例根未知时给出候选路径拼接结果。"""
        root = self._root() or Path(self._origin_text())
        return root / LOCK_FILENAME

    def _instance(self, root: Path) -> Any | None:
        """构造 ``Instance``；不可用时返回 ``None``。"""
        if self._instance_factory is not None:
            try:
                return self._instance_factory(root)
            except Exception as error:  # noqa: BLE001 - 替身失败只降级
                self.last_error = i18n.t(
                    "cli.tui.run.error_stub_failed",
                    kind=type(error).__name__,
                    error=error,
                )
                return None
        try:
            from akaribot.cli.instance import Instance
        except ImportError as error:
            self.last_error = i18n.t("cli.tui.run.error_instance_unavailable", error=error)
            return None
        try:
            return Instance(root)
        except Exception as error:  # noqa: BLE001 - 构造失败只作为降级原因
            self.last_error = i18n.t(
                "cli.tui.run.error_instance_failed",
                kind=type(error).__name__,
                error=error,
            )
            return None

    def _popen_kwargs(self, root: Path, handle: Any) -> dict[str, Any]:
        """构造 Popen 关键字参数：注入实例目录、UTF-8 输出与独立进程组。"""
        env = dict(os.environ)
        env[INSTANCE_DIR_ENV] = str(root)
        env["PYTHONIOENCODING"] = "utf-8"
        kwargs: dict[str, Any] = {
            "cwd": str(root),
            "env": env,
            "stdin": subprocess.DEVNULL,
            "stdout": handle,
            "stderr": subprocess.STDOUT,
        }
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        else:
            kwargs["start_new_session"] = True
        return kwargs

    def _request_stop(self, process: Any, *, force: bool) -> None:
        """请求停止：优先向进程组发信号，不可用时退回 ``Popen.terminate()``。"""
        pid = getattr(process, "pid", None)
        if pid is not None and self._kill(int(pid), force):
            return
        terminate = getattr(process, "terminate", None)
        if callable(terminate):
            try:
                terminate()
            except OSError:
                return

    def _close_log(self) -> None:
        """关闭子进程标准输出的落盘句柄。"""
        handle = self._log_handle
        self._log_handle = None
        if handle is None:
            return
        try:
            handle.close()
        except OSError:
            return


def default_kill(pid: int, force: bool) -> bool:
    """向进程组发送停止信号，返回是否已发送。

    :param pid: 进程号；取其进程组并向整组发信号，以覆盖 ``akaribot run`` 拉起的子进程。
    :param force: 为 ``True`` 时发强杀信号，否则发温和终止信号。
    :return: 是否成功发送；Windows 下返回 ``False``，由 ``Popen.terminate()`` 兜底。
    """
    if os.name == "nt":
        return False
    try:
        os.killpg(os.getpgid(pid), signal.SIGKILL if force else signal.SIGTERM)
    except (OSError, ProcessLookupError):
        return False
    return True


class RunPage(compat.Vertical):
    """Run 页控件。

    :param source: 数据源，缺省为 :class:`SubprocessRunSource`。
    :param status_interval: 状态表刷新周期（秒）；``None`` 或非正数表示只手动刷新。
    """

    DEFAULT_CSS = """
    RunPage {
        layout: vertical;
        height: 1fr;
    }
    RunPage #table-pane {
        height: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    RunPage #table {
        width: 1fr;
    }
    RunPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    RunPage #status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    BINDINGS = compat.bindings(
        ("s", "start", i18n.t("cli.tui.run.label_start")),
        ("x", "stop", i18n.t("cli.tui.run.label_stop")),
        ("ctrl+r", "restart", i18n.t("cli.tui.run.label_restart")),
        ("r", "refresh", i18n.t("cli.tui.run.bind_refresh")),
    )

    can_focus = True

    def __init__(
        self,
        source: RunSource | None = None,
        *,
        status_interval: float | None = 2.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.source: RunSource = source if source is not None else SubprocessRunSource()
        self.status_interval = status_interval
        self.last_error: str = ""
        self.last_result: str = ""
        self._records: tuple[ProcessRecord, ...] = ()
        self._busy: bool = False
        self._table_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：状态表、操作按钮与状态栏。"""
        with compat.VerticalScroll(id="table-pane"):
            yield compat.Static(i18n.t("cli.tui.run.table_loading"), id="table", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.run.label_start"), id="start", variant="primary")
            yield compat.Button(i18n.t("cli.tui.run.label_stop"), id="stop", variant="error")
            yield compat.Button(i18n.t("cli.tui.run.label_restart"), id="restart", variant="warning")
            yield compat.Button(i18n.t("cli.tui.run.label_refresh"), id="refresh")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后读取一次状态表，并按周期轮询进程与锁文件。"""
        compat.set_text_selection(self, False)
        self.refresh_status()
        if self.status_interval and self.status_interval > 0:
            self.set_interval(self.status_interval, self._on_tick)

    def focus_primary(self) -> None:
        """把焦点交给本页，供上层在页面切换时调用。"""
        self.focus()

    # region 状态读取（供测试与上层使用）

    @property
    def records(self) -> tuple[ProcessRecord, ...]:
        """返回缓存中的状态表，不触发取数。"""
        return self._records

    @property
    def running(self) -> bool:
        """状态表里是否存在运行中的进程。"""
        return any(record.running for record in self._records)

    @property
    def table_text(self) -> str:
        """返回状态表当前渲染出的纯文本。"""
        return self._table_rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    # endregion

    # region 数据读取与操作

    def refresh_status(self) -> None:
        """读取状态表并重绘。

        只轮询已有的 Popen 对象与实例锁文件，不起子进程、不取版本，故同步执行；
        数据源异常只更新状态栏，不中断界面。
        """
        try:
            records = tuple(self.source.status())
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self.last_error = f"{type(error).__name__}: {error}"
            self._records = ()
            self._render_table()
            self._set_status(i18n.t("cli.tui.run.status_read_failed", error=self.last_error))
            self._sync_actions()
            return
        self._records = records
        self.last_error = ""
        self._render_table()
        self._sync_actions()
        self._set_status(self.last_result or self._summary())

    def _on_tick(self) -> None:
        """定时回调：重新轮询状态表；页面被隐藏时跳过，避免无谓轮询。"""
        if not self.display:
            return
        self.refresh_status()

    def request_start(self) -> None:
        """发起启动；已有进程在运行时给出提示而不动作。"""
        if self.running:
            compat.notify(
                self.app,
                i18n.t("cli.tui.run.notify_start_running"),
                severity="warning",
                title=i18n.t("cli.tui.run.label_start"),
            )
            return
        self._start_operation(i18n.t("cli.tui.run.label_start"), self.source.start)

    def request_stop(self) -> None:
        """发起停止；没有本页启动的进程时给出提示而不动作。"""
        if not self.running:
            compat.notify(
                self.app,
                i18n.t("cli.tui.run.msg_not_running"),
                severity="warning",
                title=i18n.t("cli.tui.run.label_stop"),
            )
            return
        self._start_operation(i18n.t("cli.tui.run.label_stop"), self.source.stop)

    def request_restart(self) -> None:
        """发起重启。"""
        self._start_operation(i18n.t("cli.tui.run.label_restart"), self.source.restart)

    def _start_operation(self, label: str, func: Callable[[], RunResult]) -> None:
        """在后台任务里执行启停操作。"""
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.run.notify_busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._busy = True
        self.last_result = ""
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.run.status_calling", label=label))
        self.run_worker(self._operate(label, func), group="run-op", exclusive=True)

    async def _operate(self, label: str, func: Callable[[], RunResult]) -> None:
        """执行启停子进程操作，结束后刷新状态表。"""
        try:
            result = await asyncio.to_thread(func)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = RunResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        self._busy = False
        failure = ""
        if result.ok:
            self.last_result = i18n.t(
                "cli.tui.run.timestamp_wrap",
                message=result.message,
                time=time.strftime("%H:%M:%S"),
            )
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            self.last_result = ""
            failure = i18n.t(
                "cli.tui.run.failed_detail",
                message=result.message,
                detail=result.detail or i18n.t("cli.tui.common.no_output"),
            )
            compat.notify(self.app, failure, severity="error", title=label)
        self.refresh_status()
        if result.ok:
            if result.detail:
                separator = i18n.t("cli.tui.common.error_separator")
                self._set_status(f"{self.last_result}{separator}{result.detail}")
        else:
            self._set_status(failure)

    def _summary(self) -> str:
        """构造状态表的一句话摘要。"""
        if not self._records:
            return i18n.t("cli.tui.run.summary_empty")
        parts = [
            i18n.t("cli.tui.run.summary_entry", label=record.label, state=record.state_label)
            for record in self._records
        ]
        pids = [str(record.pid) for record in self._records if record.pid is not None]
        if pids:
            parts.append("PID " + i18n.t("cli.tui.common.list_separator").join(pids))
        if self.status_interval:
            parts.append(i18n.t("cli.tui.run.summary_poll", seconds=f"{self.status_interval:g}"))
        else:
            parts.append(i18n.t("cli.tui.run.summary_manual"))
        return i18n.t("cli.tui.common.error_separator").join(parts)

    # endregion

    # region 渲染（只读缓存）

    def _render_table(self) -> None:
        """按缓存状态表重绘表格，列宽按终端列数计算，窄屏依次丢弃尾列。"""
        columns = [i18n.t(key) for key in _TABLE_COLUMNS]
        rows = [
            (
                record.label,
                record.state_label,
                "-" if record.pid is None else str(record.pid),
                record.started_at or "-",
                "-" if record.exit_code is None else str(record.exit_code),
                record.detail or record.origin,
            )
            for record in self._records
        ]
        lines: list[str] = []
        if not rows:
            lines.append(i18n.t("cli.tui.run.table_empty"))
        else:
            widths = [compat.column_width([columns[index], *(row[index] for row in rows)]) for index in range(6)]
            keep = self._fit_columns(widths)
            header = "  ".join(compat.fit_cells(columns[index], widths[index]) for index in range(keep)).rstrip()
            lines.append(header)
            for row in rows:
                line = "  ".join(compat.fit_cells(row[index], widths[index]) for index in range(keep)).rstrip()
                lines.append(line)
        width = self._inner_width()
        if width > 0:
            lines = [compat.truncate_cells(line, width) for line in lines]
        text = "\n".join(lines)
        self._table_rendered = text
        self.query_one("#table", compat.Static).update(compat.plain_text(text))

    def _fit_columns(self, widths: Sequence[int]) -> int:
        """按可用宽度决定保留几列：至少保留目标与状态两列。"""
        width = self._inner_width()
        if width <= 0:
            return len(widths)
        keep = len(widths)
        while keep > 2 and sum(widths[:keep]) + 2 * (keep - 1) > width:
            keep -= 1
        return keep

    def _inner_width(self) -> int:
        """返回表格可用内容宽度：控件宽减去边框与左右内边距。"""
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        return max(outer - 6, 12)

    def _sync_actions(self) -> None:
        """按运行状态与忙碌状态更新按钮可用性。"""
        running = self.running
        self.query_one("#start", compat.Button).disabled = self._busy or running
        self.query_one("#stop", compat.Button).disabled = self._busy or not running
        self.query_one("#restart", compat.Button).disabled = self._busy
        self.query_one("#refresh", compat.Button).disabled = self._busy

    def _set_status(self, text: str) -> None:
        """更新状态栏，按控件宽度截断。"""
        width = self._inner_width()
        clipped = compat.truncate_cells(text, width) if width > 0 else text
        self._status_rendered = clipped
        self.query_one("#status", compat.Static).update(compat.plain_text(clipped))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        self._render_table()

    # endregion

    # region 交互

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        """按钮回调：启动、停止、重启、刷新。"""
        button_id = event.button.id
        if button_id == "start":
            self.request_start()
        elif button_id == "stop":
            self.request_stop()
        elif button_id == "restart":
            self.request_restart()
        elif button_id == "refresh":
            self.refresh_status()

    def action_start(self) -> None:
        """键位动作：启动实例。"""
        self.request_start()

    def action_stop(self) -> None:
        """键位动作：停止实例。"""
        self.request_stop()

    def action_restart(self) -> None:
        """键位动作：重启实例。"""
        self.request_restart()

    def action_refresh(self) -> None:
        """键位动作：刷新状态表。"""
        self.refresh_status()

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
