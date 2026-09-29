"""Run 页：启动 / 停止 / 重启实例，并显示运行状态。

数据流：界面只读 :class:`RunSource`；默认实现 :class:`SubprocessRunSource` 把状态、启动与停止
全部交给 ``akaribot run`` 子进程。实例由 CLI 以独立会话启动并登记在实例锁里，界面因此不持有
进程句柄：界面退出后实例继续运行，新开的界面能接管并停止由其它控制器启动的实例。启停走后台
任务，状态刷新按周期询问 CLI。
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context

STATE_RUNNING = "running"
STATE_STOPPED = "stopped"
STATE_EXITED = "exited"
STATE_UNKNOWN = "unknown"

RUN_LABEL = "akaribot run"
LOCK_FILENAME = ".bot.lock"
# 交给 CLI 的停止等待秒数；CLI 超时后会强杀，界面只需等它给出结论。
STOP_TIMEOUT_SECONDS = 20.0
_TAIL_CHARS = 400

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

    def start(self, *, adapter: str = "") -> RunResult:
        """启动实例；``adapter`` 非空时只启动该平台的适配器。"""

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
        # 每次启动请求带的适配器名，供自动化断言核对界面确实把平台交给了数据源。
        self.adapters: list[str] = []
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

    def start(self, *, adapter: str = "") -> RunResult:
        """见 :meth:`RunSource.start`。"""
        self.calls["start"] += 1
        self.adapters.append(adapter)
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


class RunSourceError(RuntimeError):
    """数据源无法给出结论：CLI 调用失败或输出不可解析。"""


class SubprocessRunSource:
    """默认数据源：状态与启停全部经 ``akaribot run`` 子进程。

    界面不自己持有实例进程：``akaribot run --detach`` 让实例自建会话，界面退出后实例继续运行；
    状态与进程号取自 ``run --status --json``，停止走 ``run --stop``。因此新开的界面能接管并停止
    由其它控制器（另一个界面、终端、系统服务）启动的实例。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param start: 向上查找的起点，缺省为当前工作目录。
    :param timeout: 单次 CLI 调用的秒数上限。
    :param stop_timeout: 交给 CLI 的停止等待秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        start: Path | str | None = None,
        timeout: float = 60.0,
        stop_timeout: float = STOP_TIMEOUT_SECONDS,
        runner: Callable[..., Any] | None = None,
    ) -> None:
        self.root = Path(root) if root is not None else None
        self.start_dir = Path(start) if start is not None else None
        self.timeout = timeout
        self.stop_timeout = stop_timeout
        self.label = RUN_LABEL
        self.calls = {"status": 0, "start": 0, "stop": 0, "restart": 0}
        self.last_error = ""
        self.last_argv = ""
        self._runner = runner or subprocess.run

    def status(self) -> Sequence[ProcessRecord]:
        """见 :meth:`RunSource.status`。"""
        self.calls["status"] += 1
        return self._records_from(self._state())

    def start(self, *, adapter: str = "") -> RunResult:
        """见 :meth:`RunSource.start`：经 ``run --detach`` 启动，界面不持有进程句柄。"""
        self.calls["start"] += 1
        argv = ["run", "--detach", "--json"]
        if adapter:
            argv += ["--adapter", adapter]
        try:
            payload = self._invoke("start", *argv)
        except RunSourceError as error:
            return self._failed("cli.tui.run.label_start", str(error))
        if not payload.get("started"):
            self.last_error = str(payload.get("detail") or "")
            return RunResult(False, i18n.t("cli.tui.run.msg_start_failed"), self.last_error)
        self.last_error = ""
        return RunResult(
            True,
            i18n.t("cli.tui.run.msg_started", pid=payload.get("pid")),
            i18n.t("cli.tui.run.detail_detached", log=payload.get("log") or ""),
        )

    def stop(self) -> RunResult:
        """见 :meth:`RunSource.stop`：经 ``run --stop`` 停止，能停掉别的控制器启动的实例。"""
        self.calls["stop"] += 1
        try:
            payload = self._invoke("stop", "run", "--stop", "--json", "--timeout", f"{self.stop_timeout:g}")
        except RunSourceError as error:
            return self._failed("cli.tui.run.label_stop", str(error))
        message = str(payload.get("message") or "")
        detail = str(payload.get("detail") or "")
        if not payload.get("stopped"):
            self.last_error = detail or message
            return RunResult(False, message or i18n.t("cli.tui.run.msg_stop_failed"), detail)
        self.last_error = ""
        return RunResult(True, message, detail)

    def restart(self) -> RunResult:
        """见 :meth:`RunSource.restart`：先停后启，停止失败则中止。"""
        self.calls["restart"] += 1
        if self.probe_running():
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
        """探测实例是否在运行；探测失败返回 ``None``。"""
        try:
            state = self._state()
        except RunSourceError as error:
            self.last_error = str(error)
            return None
        return bool(state.get("running"))

    def _failed(self, label_key: str, detail: str) -> RunResult:
        self.last_error = detail
        return RunResult(False, i18n.t("cli.tui.common.failed_label", label=i18n.t(label_key)), detail)

    def _state(self) -> dict[str, Any]:
        return self._invoke("status", "run", "--status", "--json")

    def _records_from(self, state: Mapping[str, Any]) -> tuple[ProcessRecord, ...]:
        if not state.get("running"):
            return (
                ProcessRecord(
                    label=self.label,
                    state=STATE_STOPPED,
                    detail=i18n.t("cli.tui.run.detail_never_started"),
                ),
            )
        argv = state.get("argv") or []
        detail = i18n.t("cli.tui.run.detail_cli_record", log=state.get("console_log") or "")
        if argv:
            detail = i18n.t("cli.tui.common.error_separator").join((detail, " ".join(str(item) for item in argv)))
        return (
            ProcessRecord(
                label=self.label,
                pid=state.get("pid"),
                started_at=_local_time(state.get("started_at")),
                state=STATE_RUNNING,
                origin=i18n.t("cli.tui.run.origin_cli"),
                detail=detail,
            ),
        )

    def _invoke(self, action: str, *args: str) -> dict[str, Any]:
        root = self._root()
        if root is None:
            self.last_error = i18n.t("cli.tui.run.error_no_instance", origin=self._origin_text())
            raise RunSourceError(self.last_error)
        argv = cli_process.cli_argv(*args)
        self.last_argv = " ".join(argv)
        try:
            completed = self._runner(
                list(argv),
                cwd=str(root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=cli_process.cli_env(root),
            )
        except subprocess.TimeoutExpired as error:
            raise RunSourceError(
                i18n.t("cli.tui.run.error_cli_timeout", command=" ".join(args), seconds=f"{self.timeout:g}")
            ) from error
        except OSError as error:
            raise RunSourceError(i18n.t("cli.tui.run.error_cli_failed", command=" ".join(args), error=error)) from error
        payload = _parse_payload(completed.stdout)
        if payload is None:
            tail = (completed.stderr or completed.stdout or "").strip()[-_TAIL_CHARS:]
            raise RunSourceError(
                i18n.t(
                    "cli.tui.run.error_cli_output",
                    command=" ".join(args),
                    code=completed.returncode,
                    tail=tail or i18n.t("cli.tui.common.no_output"),
                )
            )
        return payload

    def _root(self) -> Path | None:
        found = context.active_root()
        if found is not None:
            return found
        if self.root is not None:
            return self.root
        from akaribot.cli.tui.dashboard import resolve_instance_root

        return resolve_instance_root(self.start_dir)

    def _origin_text(self) -> str:
        return str(self.root or self.start_dir or Path.cwd())

    def _lock_path(self) -> Path:
        return (self._root() or Path(self._origin_text())) / LOCK_FILENAME


def _parse_payload(stdout: str | None) -> dict[str, Any] | None:
    # CLI 以 --json 输出单行对象；退出码非零时对象本身带有失败结论，故先解析再看退出码。
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        payload = json.loads(text.splitlines()[-1])
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _local_time(value: Any) -> str:
    text = str(value or "")
    if not text:
        return ""
    try:
        return datetime.fromisoformat(text).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return text


class RunPage(compat.Vertical):
    """Run 页控件。

    启动、停止、重启与「只启动指定适配器」都先弹一次模态确认框，选「执行」后才调用数据源。

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

    # 重启、指定适配器与前台运行在操作行上都有按钮，键位属低频入口，不进页脚。
    BINDINGS = compat.bindings(
        ("s", "start", i18n.t("cli.tui.run.label_start")),
        ("x", "stop", i18n.t("cli.tui.run.label_stop")),
        ("ctrl+r", "restart", i18n.t("cli.tui.run.label_restart"), False),
        ("r", "refresh", i18n.t("cli.tui.run.bind_refresh")),
        ("a", "adapter_start", i18n.t("cli.tui.run.bind_adapter_start"), False),
        ("f", "foreground", i18n.t("cli.tui.run.label_foreground"), False),
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
        self._activated = False
        self.source: RunSource = source if source is not None else SubprocessRunSource()
        self.status_interval = status_interval
        self.last_error: str = ""
        self.last_result: str = ""
        self._records: tuple[ProcessRecord, ...] = ()
        self._busy: bool = False
        self._pending = compat.PendingConfirm()
        self._adapter: str = ""
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
            yield compat.Button(i18n.t("cli.tui.run.label_adapter_start"), id="adapter-start")
            yield compat.Button(i18n.t("cli.tui.run.label_foreground"), id="foreground")
            yield compat.Button(i18n.t("cli.tui.run.label_refresh"), id="refresh")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；取数与周期轮询推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取状态表，并按周期轮询进程与锁文件。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_status()
        if self.status_interval and self.status_interval > 0:
            self.set_interval(self.status_interval, self._on_tick)

    def focus_primary(self) -> None:
        """把焦点交给本页，供上层在页面切换时调用。"""
        compat.focus_now(self)

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

    def refresh_status(self, *, manual: bool = False) -> None:
        """读取状态表并重绘。

        状态经 ``akaribot run --status --json`` 子进程取得，故放到后台任务里执行；同一时刻只保留
        最新一次刷新，响应慢时不会堆积。数据源异常只更新状态栏，不中断界面。

        :param manual: 是否由用户显式刷新；轮询不作废待确认，手动刷新才作废。
        """
        self.run_worker(partial(self._refresh, manual=manual), group="run-status", exclusive=True)

    async def _refresh(self, *, manual: bool = False) -> None:
        # 轮询不作废待确认：确认框开着时，周期刷新不得把它撤掉。
        if manual:
            self._pending.reset()
        try:
            records = tuple(await asyncio.to_thread(self.source.status))
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            # 状态读不到就无法判断语境，待确认随本轮失效。
            self._pending.reset()
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
        if not self.display:
            return
        self.refresh_status()

    def reset_pending(self) -> None:
        """作废待确认状态；切页时由 App 调用。"""
        self._pending.reset()

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
        self._request_start(self._adapter)

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
        self._ask_confirm(
            "stop",
            label=i18n.t("cli.tui.run.label_stop"),
            hint=i18n.t("cli.tui.run.choice_hint_stop"),
            func=self.source.stop,
        )

    def request_restart(self) -> None:
        """发起重启。"""
        self._ask_confirm(
            "restart",
            label=i18n.t("cli.tui.run.label_restart"),
            hint=i18n.t("cli.tui.run.choice_hint_restart"),
            func=self.source.restart,
        )

    def request_adapter_start(self) -> None:
        """发起「只启动指定适配器」；先弹输入框收集平台，确认后才执行。"""
        if self.running:
            compat.notify(
                self.app,
                i18n.t("cli.tui.run.notify_start_running"),
                severity="warning",
                title=i18n.t("cli.tui.run.label_adapter_start"),
            )
            return
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.run.adapter_title"),
            hint=i18n.t("cli.tui.run.adapter_hint"),
            placeholder=i18n.t("cli.tui.run.adapter_placeholder"),
            confirm_label=i18n.t("cli.tui.run.adapter_confirm"),
            cancel_label=i18n.t("cli.tui.run.adapter_cancel"),
            initial=self._adapter,
            callback=self._set_adapter,
        )

    def _set_adapter(self, value: str | None) -> None:
        chosen = (value or "").strip()
        if not chosen:
            self._pending.reset()
            self._set_status(i18n.t("cli.tui.run.adapter_cancelled"))
            return
        self._adapter = chosen
        self._request_start(chosen)

    def _request_start(self, adapter: str) -> None:
        if adapter:
            label = i18n.t("cli.tui.run.label_adapter_start")
            hint = i18n.t("cli.tui.run.choice_hint_start_adapter", platform=adapter)
            func: Callable[[], RunResult] = partial(self.source.start, adapter=adapter)
        else:
            label = i18n.t("cli.tui.run.label_start")
            hint = i18n.t("cli.tui.run.choice_hint_start")
            func = self.source.start
        self._ask_confirm(self._start_key(adapter), label=label, hint=hint, func=func)

    def _start_key(self, adapter: str) -> str:
        return f"start:{adapter}" if adapter else "start"

    def _ask_confirm(self, key: str, *, label: str, hint: str, func: Callable[[], RunResult]) -> None:
        # 模态框就是确认；闸门只挡鼠标双击与键盘连发带来的第二层弹窗。
        if not self._pending.accept(key):
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.run.choice_title", label=label),
            hint=hint,
            options=(("run", i18n.t("cli.tui.run.choice_run")),),
            cancel_label=i18n.t("cli.tui.run.choice_cancel"),
            callback=lambda choice: self._on_confirm_choice(choice, label=label, func=func),
        )

    def _on_confirm_choice(self, choice: str | None, *, label: str, func: Callable[[], RunResult]) -> None:
        self._pending.reset()
        if choice != "run":
            self._set_status(i18n.t("cli.tui.run.choice_cancelled", label=label))
            return
        self._start_operation(label, func)

    def _foreground_command(self) -> str:
        command = f"{RUN_LABEL} --foreground"
        return f"{command} --adapter {self._adapter}" if self._adapter else command

    def _start_operation(self, label: str, func: Callable[[], RunResult]) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.run.notify_busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._pending.reset()
        self._busy = True
        self.last_result = ""
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.run.status_calling", label=label))
        self.run_worker(self._operate(label, func), group="run-op", exclusive=True)

    async def _operate(self, label: str, func: Callable[[], RunResult]) -> None:
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
        width = self._inner_width()
        if width <= 0:
            return len(widths)
        keep = len(widths)
        while keep > 2 and sum(widths[:keep]) + 2 * (keep - 1) > width:
            keep -= 1
        return keep

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        return max(outer - 6, 12)

    def _sync_actions(self) -> None:
        running = self.running
        self.query_one("#start", compat.Button).disabled = self._busy or running
        self.query_one("#stop", compat.Button).disabled = self._busy or not running
        self.query_one("#restart", compat.Button).disabled = self._busy
        self.query_one("#adapter-start", compat.Button).disabled = self._busy or running
        self.query_one("#refresh", compat.Button).disabled = self._busy

    def _set_status(self, text: str) -> None:
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
        button_id = event.button.id
        if button_id == "start":
            self.request_start()
        elif button_id == "stop":
            self.request_stop()
        elif button_id == "restart":
            self.request_restart()
        elif button_id == "adapter-start":
            self.request_adapter_start()
        elif button_id == "foreground":
            self.action_foreground()
        elif button_id == "refresh":
            self.refresh_status(manual=True)

    def action_start(self) -> None:
        """键位动作：启动实例。"""
        self.request_start()

    def action_stop(self) -> None:
        """键位动作：停止实例。"""
        self.request_stop()

    def action_restart(self) -> None:
        """键位动作：重启实例。"""
        self.request_restart()

    def action_adapter_start(self) -> None:
        """键位动作：只启动指定平台的适配器。"""
        self.request_adapter_start()

    def action_foreground(self) -> None:
        """键位动作：给出前台运行的命令与后果，界面内不执行。"""
        text = i18n.t("cli.tui.run.foreground_hint", command=self._foreground_command())
        compat.notify(self.app, text, severity="warning", title=i18n.t("cli.tui.run.label_foreground"))
        self._set_status(text)

    def action_refresh(self) -> None:
        """键位动作：刷新状态表。"""
        self.refresh_status(manual=True)

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
