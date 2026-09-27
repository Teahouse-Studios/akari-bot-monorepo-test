"""杂项页：只放不属于其它页面的一次性操作。

目前只有「迁移项目」：把旧版项目搬成当前实例。页面平时只显示一个按钮，点击后才弹出输入框要路径，
迁移本身仍要经确认——旧目录只读，但会往实例里写配置与数据。
"""

from __future__ import annotations

import asyncio
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context
from akaribot.cli.tui.modules import OperationResult

MIGRATE_TIMEOUT_SECONDS = 1800.0


@runtime_checkable
class MiscSource(Protocol):
    """杂项动作的数据源接口；测试注入替身，生产走子进程。"""

    def migrate_legacy(self, project: str) -> OperationResult:
        """把旧版项目迁移为当前实例。"""


class StaticMiscSource:
    """固定数据的替身数据源，供自动化断言使用。

    :param result: ``migrate_legacy`` 的返回值；缺省为成功。
    """

    def __init__(self, result: OperationResult | None = None) -> None:
        self._result = result or OperationResult(True, i18n.t("cli.tui.misc.stub_migrate_ok"), "stub")
        self.calls = {"migrate": 0}
        self.migrated: list[str] = []

    def migrate_legacy(self, project: str) -> OperationResult:
        """见 :meth:`MiscSource.migrate_legacy`。"""
        self.calls["migrate"] += 1
        self.migrated.append(project)
        return self._result


class SubprocessMiscSource:
    """默认数据源：经 ``akaribot migrate legacy`` 执行，CLI 进程内不 import core。

    :param root: 实例根；缺省按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param timeout: 单个子进程的超时秒数；迁移要搬文件、装包，给足时间。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = MIGRATE_TIMEOUT_SECONDS,
        runner: Callable[..., Any] | None = None,
    ) -> None:
        # 根在取数时解析：界面切换实例后，同一份数据源要指向新实例，不能在构造时定死。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"migrate": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def migrate_legacy(self, project: str) -> OperationResult:
        """见 :meth:`MiscSource.migrate_legacy`。"""
        self.calls["migrate"] += 1
        label = i18n.t("cli.tui.misc.label_migrate")
        argv = cli_process.cli_argv("migrate", "legacy", project)
        try:
            completed = self._runner(
                argv,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=cli_process.cli_env(self.root),
            )
        except subprocess.TimeoutExpired:
            return OperationResult(
                False,
                i18n.t("cli.tui.misc.timeout", label=label, seconds=f"{self.timeout:g}"),
                "",
            )
        except OSError as error:
            return OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        detail = _tail(completed.stderr) or _tail(completed.stdout)
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), detail)
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            detail,
        )


def _tail(text: str | None, limit: int = 400) -> str:
    return (text or "").strip()[-limit:]


class MiscPage(compat.Vertical):
    """杂项页控件。

    :param source: 数据源，缺省为 :class:`SubprocessMiscSource`。
    """

    DEFAULT_CSS = """
    MiscPage {
        layout: vertical;
        height: 1fr;
    }
    MiscPage #misc-hint {
        height: 4;
        padding: 0 1;
        color: $text-muted;
    }
    MiscPage #actions {
        height: 3;
        padding: 0 1;
    }
    MiscPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    BINDINGS = compat.bindings(("m", "migrate", i18n.t("cli.tui.misc.bind_migrate")))

    can_focus = True

    def __init__(self, source: MiscSource | None = None, *, id: str | None = None) -> None:
        super().__init__(id=id)
        self.source: MiscSource = source if source is not None else SubprocessMiscSource()
        self.last_error: str = ""
        self.last_result: str = ""
        self._busy = False
        self._pending_project: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：说明、一个动作按钮与状态栏。"""
        yield compat.Static(i18n.t("cli.tui.misc.hint"), id="misc-hint", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.misc.button_migrate"), id="migrate", variant="primary")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def activate(self) -> None:
        """本页没有需要预取的数据。"""

    def focus_primary(self) -> None:
        """把焦点交给按钮。"""
        compat.focus_first(self, "#migrate")

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def pending_project(self) -> str:
        """返回已输入、等待确认的项目路径。"""
        return self._pending_project

    def action_migrate(self) -> None:
        """键位动作：弹出输入框要项目路径。"""
        self.request_migrate()

    def request_migrate(self) -> None:
        """弹出输入框；已填过路径时改为确认执行。"""
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.common.busy_title"),
                severity="warning",
                title=i18n.t("cli.tui.misc.button_migrate"),
            )
            return
        if self._pending_project:
            project = self._pending_project
            self._pending_project = ""
            self._start_migration(project)
            return
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.misc.dialog_title"),
            hint=i18n.t("cli.tui.misc.dialog_hint"),
            placeholder=i18n.t("cli.tui.misc.dialog_placeholder"),
            confirm_label=i18n.t("cli.tui.misc.dialog_confirm"),
            cancel_label=i18n.t("cli.tui.misc.dialog_cancel"),
            callback=self.on_project_entered,
        )

    def on_project_entered(self, project: str | None) -> None:
        """输入框回调：拿到路径后先问一次再执行。

        :param project: 用户输入的路径；取消时为 ``None``。
        """
        if not project:
            self._set_status(i18n.t("cli.tui.misc.cancelled"))
            return
        self._pending_project = project
        self._set_status(i18n.t("cli.tui.misc.confirm_migrate", project=project))

    def _start_migration(self, project: str) -> None:
        self._busy = True
        self._sync_actions()
        label = i18n.t("cli.tui.misc.label_migrate")
        self._set_status(i18n.t("cli.tui.misc.calling", project=project))
        self.run_worker(self._migrate(project, label), group="misc-migrate", exclusive=True)

    async def _migrate(self, project: str, label: str) -> None:
        try:
            result = await asyncio.to_thread(self.source.migrate_legacy, project)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        if result.ok:
            self.last_result = result.message
            detail = result.detail.splitlines()[-1] if result.detail else ""
            self._set_status(f"{result.message}｜{detail}" if detail else result.message)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.misc.failed_detail", message=result.message, detail=tail))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def _sync_actions(self) -> None:
        self.query_one("#migrate", compat.Button).disabled = self._busy

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "migrate":
            self.request_migrate()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
