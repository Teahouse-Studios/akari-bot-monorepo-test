"""环境页：实例用的解释器、venv 托管方式与装了哪些包。

数据经 ``akaribot venv status --json`` 取得，动作经 ``venv adopt/release/recreate`` 执行——界面不直接
改环境。三个动作都会换掉实例正在使用的解释器，因此实例运行期间一律拒绝。
"""

from __future__ import annotations

import asyncio
import json
import signal
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context
from akaribot.cli.tui.modules import OperationResult

# 环境动作的秒数上限：要建 venv、解析依赖、装几十个包，比查询宽松得多。
ACTION_TIMEOUT_SECONDS = 1800.0
QUERY_TIMEOUT_SECONDS = 120.0
MODE_MANAGED = "managed"
MODE_EXTERNAL = "external"


def _signal_name(number: int) -> str:
    # 换不出名字时退回编号文本。
    try:
        return signal.Signals(number).name
    except ValueError:
        return str(number)


@dataclass(frozen=True)
class EnvironmentPackage:
    """环境里的一个已装分发。

    :param dist: 分发名。
    :param version: 版本。
    :param editable: 是否为可编辑安装。
    """

    dist: str
    version: str = ""
    editable: bool = False

    def row_text(self) -> str:
        """返回列表行文本。"""
        mark = i18n.t("cli.tui.environment.editable_mark") if self.editable else ""
        return f"{self.dist} {self.version}{mark}".rstrip()


@dataclass(frozen=True)
class EnvironmentState:
    """一次环境快照。

    :param mode: ``managed``（实例自带 venv）或 ``external``（用当前解释器）。
    :param python: 当前生效的解释器。
    :param venv_dir: 托管 venv 的目标目录。
    :param ready: 解释器是否存在。
    :param packages: 已装分发；探测失败时为 ``None``。
    :param core_version: core 版本号。
    :param error: 读取失败的原因。
    """

    mode: str = ""
    python: str = ""
    venv_dir: str = ""
    ready: bool = False
    packages: tuple[EnvironmentPackage, ...] | None = None
    core_version: str = ""
    error: str = ""

    def mode_text(self) -> str:
        """返回托管方式的说明。"""
        if self.mode == MODE_MANAGED:
            return i18n.t("cli.tui.environment.mode_managed", venv=self.venv_dir or "-")
        if self.mode == MODE_EXTERNAL:
            return i18n.t("cli.tui.environment.mode_external")
        return i18n.t("cli.tui.environment.mode_unknown")

    def package_count(self) -> int:
        """返回已装分发数量；探测失败时为 ``-1``。"""
        return -1 if self.packages is None else len(self.packages)

    def count_text(self) -> str:
        """返回包数量的展示文本。"""
        if self.error:
            return i18n.t("cli.tui.environment.value_unknown")
        if self.packages is None:
            return i18n.t("cli.tui.environment.probe_failed")
        return i18n.t("cli.tui.environment.package_count", count=len(self.packages))


class EnvironmentSourceError(RuntimeError):
    """数据源不可用：子进程缺失、输出不是 JSON 或读取超时。"""


@runtime_checkable
class EnvironmentSource(Protocol):
    """环境数据源接口；测试注入替身，生产走子进程。"""

    def state(self) -> EnvironmentState:
        """返回环境快照。"""

    def running(self) -> bool | None:
        """返回实例是否在运行；探测失败时返回 ``None``。"""

    def action(self, kind: str) -> OperationResult:
        """执行 ``adopt`` / ``release`` / ``recreate``。"""


class StaticEnvironmentSource:
    """固定数据的替身数据源，供自动化断言使用。

    :param state: ``state`` 的返回值。
    :param running: ``running`` 的返回值。
    :param action_result: ``action`` 的返回值；缺省为成功。
    """

    def __init__(
        self,
        state: EnvironmentState | None = None,
        *,
        running: bool | None = False,
        action_result: OperationResult | None = None,
    ) -> None:
        self._state = state or EnvironmentState(
            mode=MODE_MANAGED,
            python="/tmp/inst/.venv/bin/python",
            venv_dir="/tmp/inst/.venv",
            ready=True,
            packages=(
                EnvironmentPackage("akari-bot-core", "0.1.0"),
                EnvironmentPackage("akari-bot-module-wiki", "0.2.0", editable=True),
            ),
            core_version="0.1.0",
        )
        self._running = running
        self._action_result = action_result or OperationResult(
            True, i18n.t("cli.tui.environment.stub_action_ok"), "stub"
        )
        self.calls = {"state": 0, "running": 0, "action": 0}
        self.actions: list[str] = []

    def state(self) -> EnvironmentState:
        """见 :meth:`EnvironmentSource.state`。"""
        self.calls["state"] += 1
        return self._state

    def running(self) -> bool | None:
        """见 :meth:`EnvironmentSource.running`。"""
        self.calls["running"] += 1
        return self._running

    def action(self, kind: str) -> OperationResult:
        """见 :meth:`EnvironmentSource.action`。"""
        self.calls["action"] += 1
        self.actions.append(kind)
        return self._action_result

    def set_state(self, state: EnvironmentState) -> None:
        """替换替身返回的快照。"""
        self._state = state


class SubprocessEnvironmentSource:
    """默认数据源：一律经 ``akaribot`` 子进程，CLI 进程内不 import core。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param query_timeout: 查询类调用的秒数上限。
    :param action_timeout: 环境动作的秒数上限。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        query_timeout: float = QUERY_TIMEOUT_SECONDS,
        action_timeout: float = ACTION_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        # 根在取数时解析：界面切换实例后，同一份数据源要指向新实例，不能在构造时定死。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.query_timeout = query_timeout
        self.action_timeout = action_timeout
        self.calls = {"state": 0, "running": 0, "action": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def state(self) -> EnvironmentState:
        """见 :meth:`EnvironmentSource.state`。"""
        self.calls["state"] += 1
        payload = self._invoke(("venv", "status", "--json"), timeout=self.query_timeout)
        packages = payload.get("packages")
        parsed: tuple[EnvironmentPackage, ...] | None = None
        if isinstance(packages, Sequence) and not isinstance(packages, str | bytes):
            parsed = tuple(
                EnvironmentPackage(
                    dist=str(item.get("dist") or ""),
                    version=str(item.get("version") or ""),
                    editable=bool(item.get("editable")),
                )
                for item in packages
                if isinstance(item, Mapping) and item.get("dist")
            )
        return EnvironmentState(
            mode=str(payload.get("mode") or ""),
            python=str(payload.get("python") or ""),
            venv_dir=str(payload.get("venv_dir") or ""),
            ready=bool(payload.get("exists")),
            packages=parsed,
            core_version=str(payload.get("core_version") or ""),
            error=str(payload.get("error") or ""),
        )

    def running(self) -> bool | None:
        """见 :meth:`EnvironmentSource.running`：读锁文件记录，不起实例进程。"""
        self.calls["running"] = self.calls.get("running", 0) + 1
        try:
            payload = self._invoke(("run", "--status", "--json"), timeout=self.query_timeout)
        except EnvironmentSourceError:
            return None
        return bool(payload.get("running"))

    def action(self, kind: str) -> OperationResult:
        """见 :meth:`EnvironmentSource.action`；``--yes`` 由界面代答。"""
        self.calls["action"] = self.calls.get("action", 0) + 1
        label = i18n.t(f"cli.tui.environment.label_{kind}")
        argv = cli_process.cli_argv("venv", kind, "--yes")
        try:
            completed = self._runner(
                argv,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.action_timeout,
                env=cli_process.cli_env(self.root),
            )
        except subprocess.TimeoutExpired:
            return OperationResult(
                False,
                i18n.t("cli.tui.environment.action_timeout", label=label, seconds=f"{self.action_timeout:g}"),
                "",
            )
        except OSError as error:
            return OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        detail = _tail(completed.stderr) or _tail(completed.stdout)
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), detail)
        if completed.returncode < 0:
            # 子进程被信号终止时退出码是负数，只报数字看不出所以然。
            return OperationResult(
                False,
                i18n.t("cli.tui.environment.action_signalled", label=label, signal=_signal_name(-completed.returncode)),
                detail,
            )
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            detail,
        )

    def _invoke(self, args: Sequence[str], *, timeout: float) -> dict[str, Any]:
        argv = cli_process.cli_argv(*args)
        try:
            completed = self._runner(
                argv,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=cli_process.cli_env(self.root),
            )
        except subprocess.TimeoutExpired as error:
            raise EnvironmentSourceError(
                i18n.t("cli.tui.environment.src_timeout", cmd=" ".join(args), seconds=f"{timeout:g}")
            ) from error
        except OSError as error:
            raise EnvironmentSourceError(
                i18n.t("cli.tui.environment.src_oserror", cmd=" ".join(args), error=error)
            ) from error
        text = (completed.stdout or "").strip()
        if not text:
            raise EnvironmentSourceError(
                i18n.t("cli.tui.environment.src_exit_code", cmd=" ".join(args), code=completed.returncode)
            )
        try:
            payload = json.loads(text.splitlines()[-1])
        except json.JSONDecodeError as error:
            raise EnvironmentSourceError(i18n.t("cli.tui.environment.src_bad_json", error=error)) from error
        if not isinstance(payload, dict):
            raise EnvironmentSourceError(i18n.t("cli.tui.environment.src_bad_payload"))
        return payload


def _tail(text: str | None, limit: int = 400) -> str:
    return (text or "").strip()[-limit:]


class EnvironmentPage(compat.Vertical):
    """环境页控件。

    :param source: 数据源，缺省为 :class:`SubprocessEnvironmentSource`。
    :param cache_ttl: 快照缓存有效期（秒）。
    """

    DEFAULT_CSS = """
    EnvironmentPage {
        layout: vertical;
        height: 1fr;
    }
    EnvironmentPage #fields-pane {
        height: 7;
        border: round $primary;
        padding: 0 1;
    }
    EnvironmentPage #fields {
        width: 1fr;
    }
    EnvironmentPage #package-search {
        height: 3;
    }
    EnvironmentPage #package-list {
        height: 1fr;
        border: round $panel;
    }
    EnvironmentPage #package-list > ListItem {
        padding: 0 1;
    }
    EnvironmentPage #package-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    EnvironmentPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    EnvironmentPage #status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.environment.bind_refresh")),
        ("slash", "focus_search", i18n.t("cli.tui.environment.bind_search")),
        ("a", "adopt", i18n.t("cli.tui.environment.bind_adopt")),
        ("x", "release", i18n.t("cli.tui.environment.bind_release")),
        ("ctrl+n", "recreate", i18n.t("cli.tui.environment.bind_recreate")),
    )

    can_focus = True

    def __init__(
        self,
        source: EnvironmentSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: EnvironmentSource = source if source is not None else SubprocessEnvironmentSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._state = EnvironmentState()
        self._query = ""
        self._busy = False
        self._running: bool | None = False
        self._pending: str = ""
        self._pending_status: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._loaded_at: float = 0.0
        self._rows: tuple[str, ...] = ()

    @property
    def rows(self) -> tuple[str, ...]:
        """返回最近一次渲染出的包列表行。"""
        return self._rows

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.VerticalScroll(id="fields-pane"):
            yield compat.Static(i18n.t("cli.tui.environment.fields_placeholder"), id="fields", markup=False)
        yield compat.Input(placeholder=i18n.t("cli.tui.environment.search_placeholder"), id="package-search")
        yield compat.ListView(id="package-list")
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.environment.button_adopt"), id="adopt", variant="warning")
            yield compat.Button(i18n.t("cli.tui.environment.button_release"), id="release", variant="warning")
            yield compat.Button(i18n.t("cli.tui.environment.button_recreate"), id="recreate", variant="warning")
            yield compat.Button(i18n.t("cli.tui.environment.button_refresh"), id="refresh")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；取数推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取环境快照。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_state(force=True)

    def focus_primary(self) -> None:
        """把焦点交给包列表；列表为空时退到页面容器。"""
        compat.focus_first(self, "#package-list")

    @property
    def state(self) -> EnvironmentState:
        """返回缓存中的环境快照，不触发取数。"""
        return self._state

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def running(self) -> bool | None:
        """返回最近一次运行状态探测结果。"""
        return self._running

    @property
    def visible_packages(self) -> tuple[EnvironmentPackage, ...]:
        """返回应用当前搜索词后的分发包。"""
        packages = self._state.packages or ()
        if not self._query.strip():
            return packages
        needle = self._query.strip().casefold()
        return tuple(package for package in packages if needle in package.dist.casefold())

    def action_refresh(self) -> None:
        """键位动作：强制重新读取。"""
        self._pending_status = ""
        self.refresh_state(force=True)

    def action_focus_search(self) -> None:
        """键位动作：把焦点交给搜索框。"""
        self.query_one("#package-search", compat.Input).focus()

    def action_adopt(self) -> None:
        """键位动作：改用托管 venv。"""
        self.request_action("adopt")

    def action_release(self) -> None:
        """键位动作：改用系统解释器。"""
        self.request_action("release")

    def action_recreate(self) -> None:
        """键位动作：重建实例 venv。"""
        self.request_action("recreate")

    def set_query(self, value: str) -> None:
        """设置搜索词，等价于用户键入。"""
        self.query_one("#package-search", compat.Input).value = value

    def refresh_state(self, *, force: bool = False) -> None:
        """读取环境快照与运行状态。

        :param force: 为 ``True`` 时忽略缓存。
        """
        if not force and self._state.mode and self._cache_age() < self.cache_ttl:
            self._render_all()
            self._set_status(i18n.t("cli.tui.environment.status_cached", age=f"{self._cache_age():.1f}"))
            return
        self._set_status(i18n.t("cli.tui.environment.status_loading"))
        self.run_worker(self._load, group="environment-load", exclusive=True)

    async def _load(self) -> bool:
        try:
            state = await asyncio.to_thread(self.source.state)
            running = await asyncio.to_thread(self.source.running)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._state = EnvironmentState(error=self.last_error)
            self._running = None
            self._render_all()
            self._set_status(i18n.t("cli.tui.environment.status_load_failed", error=self.last_error))
            self._sync_actions()
            return False
        self._state = state
        self._running = running
        self._loaded_at = time.monotonic()
        self.last_error = state.error
        self.last_result = i18n.t("cli.tui.environment.status_loaded", count=max(state.package_count(), 0))
        self._render_all()
        # 动作刚失败时保留那句结论：紧接着的重读不该把「为什么失败」冲掉。
        self._set_status(self._pending_status or self.last_result)
        self._sync_actions()
        return True

    def _cache_age(self) -> float:
        return max(0.0, time.monotonic() - self._loaded_at)

    def request_action(self, kind: str) -> None:
        """执行环境动作；连按两次同一个动作才真正执行。

        三个动作都会换掉实例正在使用的解释器，因此实例运行期间一律拒绝；动作不适用于当前模式时
        也不动作，只说明为什么。
        """
        reason = self._blocker(kind)
        if reason:
            compat.notify(self.app, reason, severity="warning", title=i18n.t(f"cli.tui.environment.label_{kind}"))
            return
        if self._pending != kind:
            self._pending = kind
            self._set_status(i18n.t(f"cli.tui.environment.confirm_{kind}"))
            return
        self._pending = ""
        label = i18n.t(f"cli.tui.environment.label_{kind}")
        self._set_status(i18n.t("cli.tui.environment.calling", label=label))
        self.run_worker(self._operate(kind, label), group="environment-action", exclusive=True)

    def _blocker(self, kind: str) -> str:
        # 可以执行时返回空串。
        if self._busy:
            return i18n.t("cli.tui.common.busy_title")
        if self._running:
            return i18n.t("cli.tui.environment.running_blocked")
        mode = self._state.mode
        if mode not in (MODE_MANAGED, MODE_EXTERNAL):
            return i18n.t("cli.tui.environment.mode_missing")
        if kind == "adopt" and mode == MODE_MANAGED:
            return i18n.t("cli.tui.environment.already_managed")
        if kind in ("release", "recreate") and mode != MODE_MANAGED:
            return i18n.t("cli.tui.environment.not_managed")
        return ""

    async def _operate(self, kind: str, label: str) -> None:
        self._busy = True
        self._sync_actions()
        try:
            result = await asyncio.to_thread(self.source.action, kind)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        if result.ok:
            self.last_result = result.message
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._pending_status = i18n.t("cli.tui.environment.action_failed", message=result.message, detail=tail)
            self._set_status(self._pending_status)
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self.refresh_state(force=True)

    def _render_all(self) -> None:
        self._render_fields()
        self._render_packages()

    def _render_fields(self) -> None:
        state = self._state
        rows = [
            (i18n.t("cli.tui.environment.field_mode"), state.mode_text()),
            (
                i18n.t("cli.tui.environment.field_python"),
                state.python or i18n.t("cli.tui.common.unknown"),
            ),
            (
                i18n.t("cli.tui.environment.field_core"),
                state.core_version or i18n.t("cli.tui.common.unknown"),
            ),
            (i18n.t("cli.tui.environment.field_packages"), state.count_text()),
            (
                i18n.t("cli.tui.environment.field_state"),
                i18n.t("cli.tui.environment.state_running")
                if self._running
                else i18n.t("cli.tui.environment.state_stopped")
                if self._running is False
                else i18n.t("cli.tui.common.unknown"),
            ),
        ]
        if state.error:
            rows.append((i18n.t("cli.tui.environment.field_error"), state.error))
        lines = compat.align_rows(rows, gap=2)
        width = self._inner_width()
        if width > 0:
            lines = [compat.truncate_cells(line, width) for line in lines]
        text = "\n".join(lines)
        self.query_one("#fields", compat.Static).update(compat.plain_text(text))

    def _render_packages(self) -> None:
        list_view = self.query_one("#package-list", compat.ListView)
        packages = self.visible_packages
        rows = tuple(package.row_text() for package in packages)
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(row, markup=False)) for row in rows])
        list_view.index = 0 if rows else None
        self._rows = rows

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        return max(outer - 6, 16)

    def _sync_actions(self) -> None:
        # 只显示当前模式下有意义的动作：托管实例给「改用系统解释器」与「重建」，外部实例只给
        # 「改用托管 venv」。点不到的按钮不会让人去猜它是干什么的。
        mode = self._state.mode
        visible = {
            "adopt": mode == MODE_EXTERNAL,
            "release": mode == MODE_MANAGED,
            "recreate": mode == MODE_MANAGED,
        }
        for kind, shown in visible.items():
            button = self.query_one(f"#{kind}", compat.Button)
            button.display = shown
            button.disabled = self._busy

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.last_result = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        self._render_all()

    @compat.on(compat.Input.Changed, "#package-search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        self._query = event.value
        self._render_packages()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id in ("adopt", "release", "recreate"):
            self.request_action(str(button_id))
        elif button_id == "refresh":
            self.refresh_state(force=True)

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
