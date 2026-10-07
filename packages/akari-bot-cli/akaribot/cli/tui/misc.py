from __future__ import annotations

import asyncio
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context
from akaribot.cli.tui.modules import OperationResult

MIGRATE_TIMEOUT_SECONDS = 1800.0
# 迁移计划通常较长，预览输出使用独立的截断上限。
DRY_RUN_OUTPUT_LIMIT = 4000
OUTPUT_LINES = 6

CHOICE_MIGRATE = "migrate"
CHOICE_DRY_RUN = "dry-run"
# 请求防抖键与项目路径分离，避免同名值覆盖防抖记录。
MIGRATE_REQUEST = "migrate-request"


MIGRATE_SWITCHES = (
    ("--skip-install", "cli.tui.misc.option_skip_install"),
    ("--no-venv", "cli.tui.misc.option_no_venv"),
    ("--force", "cli.tui.misc.option_force"),
    ("--offline", "cli.tui.misc.option_offline"),
)


def _option_id(flag: str) -> str:
    return f"option-{flag.removeprefix('--')}"


@runtime_checkable
class MiscSource(Protocol):
    """项目迁移数据源接口。"""

    def migrate_legacy(self, project: str, *, dry_run: bool = False, flags: Sequence[str] = ()) -> OperationResult:
        """迁移旧版项目到当前实例；``dry_run`` 为真时仅预览，``flags`` 为附加的 CLI 参数。"""


class StaticMiscSource:
    """用于测试的静态数据源。

    :param result: ``migrate_legacy`` 的返回值；默认为成功。
    """

    def __init__(self, result: OperationResult | None = None) -> None:
        self._result = result or OperationResult(True, i18n.t("cli.tui.misc.stub_migrate_ok"), "stub")
        self.calls = {"migrate": 0}
        self.migrated: list[tuple[str, bool, tuple[str, ...]]] = []

    def migrate_legacy(self, project: str, *, dry_run: bool = False, flags: Sequence[str] = ()) -> OperationResult:
        """见 :meth:`MiscSource.migrate_legacy`。"""
        self.calls["migrate"] += 1
        self.migrated.append((project, dry_run, tuple(flags)))
        return self._result


class SubprocessMiscSource:
    """通过 ``akaribot migrate legacy`` 执行项目迁移。

    :param root: 实例根；默认按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param timeout: 迁移子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = MIGRATE_TIMEOUT_SECONDS,
        runner: Callable[..., Any] | None = None,
    ) -> None:
        # 每次请求均解析当前实例，避免切换实例后继续访问旧路径。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"migrate": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """返回实例根目录，依次采用显式路径、当前实例或自动定位结果。"""
        return context.resolve_root(self._root_override)

    def migrate_legacy(self, project: str, *, dry_run: bool = False, flags: Sequence[str] = ()) -> OperationResult:
        """见 :meth:`MiscSource.migrate_legacy`。"""
        self.calls["migrate"] += 1
        label = i18n.t("cli.tui.misc.label_dry_run" if dry_run else "cli.tui.misc.label_migrate")
        # 必须显式指定 --instance，确保迁移目标为界面当前实例。
        argv = cli_process.cli_argv("migrate", "legacy", project, "--instance", str(self.root))
        if dry_run:
            argv.append("--dry-run")
        argv.extend(flags)
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
        limit = DRY_RUN_OUTPUT_LIMIT if dry_run else 400
        detail = _tail(completed.stderr, limit) or _tail(completed.stdout, limit)
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

    :param source: 数据源，默认为 :class:`SubprocessMiscSource`。
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
    MiscPage #migrate-options {
        height: 1;
        padding: 0 0 0 1;
    }
    MiscPage #migrate-options Checkbox {
        width: auto;
        height: 1;
        border: none;
        padding: 0;
        margin: 0 1 0 0;
    }
    MiscPage #actions {
        height: 3;
        padding: 0 1;
    }
    MiscPage #migrate-output {
        height: 8;
        border: round $primary;
        padding: 0 1;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    MiscPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    BINDINGS = compat.bindings(
        ("m", "migrate", i18n.t("cli.tui.misc.bind_migrate")),
        ("p", "dry_run", i18n.t("cli.tui.misc.bind_dry_run"), False),
    )

    can_focus = True

    def __init__(self, source: MiscSource | None = None, *, id: str | None = None) -> None:
        super().__init__(id=id)
        self.source: MiscSource = source if source is not None else SubprocessMiscSource()
        self.last_error: str = ""
        self.last_result: str = ""
        self._busy = False
        self._confirm = compat.PendingConfirm()
        self._pending_project: str = ""
        self._output_lines: tuple[str, ...] = ()
        self._output_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:

        yield compat.Static(i18n.t("cli.tui.misc.hint"), id="misc-hint", markup=False)
        with compat.Horizontal(id="migrate-options"):
            for flag, label_key in MIGRATE_SWITCHES:
                yield compat.Checkbox(i18n.t(label_key), id=_option_id(flag))
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.misc.button_migrate"), id="migrate", variant="primary")
        yield compat.Static("", id="migrate-output", markup=False)
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:

        compat.set_text_selection(self, False)
        self._sync_output()

    def activate(self) -> None:
        """本页没有需要预取的数据。"""

    def focus_primary(self) -> None:
        """聚焦按钮。"""
        compat.focus_first(self, "#migrate")

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def pending_project(self) -> str:
        """返回已输入、等待确认的项目路径。"""
        return self._pending_project

    @property
    def output_text(self) -> str:
        """返回输出区当前显示的文本。"""
        return self._output_rendered

    @property
    def selected_flags(self) -> tuple[str, ...]:
        """返回当前勾选的开关，顺序与界面一致。"""
        chosen: list[str] = []
        for flag, _ in MIGRATE_SWITCHES:
            widget = self._action_widget(f"#{_option_id(flag)}")
            if isinstance(widget, compat.Checkbox) and widget.value:
                chosen.append(flag)
        return tuple(chosen)

    def reset_pending(self) -> None:
        """作废待确认的迁移；切页时由 :meth:`TuiApp.show_page` 调用。"""
        self._confirm.reset()
        self._pending_project = ""

    def action_migrate(self) -> None:

        self.request_migrate()

    def action_dry_run(self) -> None:

        if self._busy:
            self._notify_busy()
            return
        if not self._pending_project:
            self._set_status(i18n.t("cli.tui.misc.dry_run_need_path"))
            return
        self._start_migration(self._pending_project, dry_run=True)

    def request_migrate(self) -> None:
        """请求迁移；未指定路径时先请求输入，再显示确认框。"""
        if self._busy:
            self._notify_busy()
            return
        # 防抖窗口内忽略重复请求，避免叠加确认框。
        if not self._confirm.accept(MIGRATE_REQUEST):
            return
        project = self._pending_project
        if project:
            self._open_choice(project)
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

        if not project:
            self._set_status(i18n.t("cli.tui.misc.cancelled"))
            return
        self._pending_project = project
        # 输入框与确认框均响应回车，记录提交时刻以防止连续按键误确认。
        self._confirm.reset()
        self._confirm.accept(project)
        self._open_choice(project)

    def _open_choice(self, project: str) -> None:
        self._set_status(i18n.t("cli.tui.misc.confirm_migrate_pending", project=project))
        # 确认框必须列明即将传递给 CLI 的参数。
        chosen = self.selected_flags
        options = " ".join(chosen) if chosen else i18n.t("cli.tui.misc.choice_options_none")
        hint = "\n".join(
            (
                i18n.t("cli.tui.misc.choice_hint", project=project),
                i18n.t("cli.tui.misc.choice_options", options=options),
            )
        )
        # 默认聚焦只读预览选项，避免连续回车直接执行迁移。
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.misc.dialog_title"),
            hint=hint,
            options=(
                (CHOICE_DRY_RUN, i18n.t("cli.tui.misc.choice_dry_run")),
                (CHOICE_MIGRATE, i18n.t("cli.tui.misc.choice_migrate")),
            ),
            cancel_label=i18n.t("cli.tui.misc.dialog_cancel"),
            callback=self.on_migration_choice,
        )

    def on_migration_choice(self, choice: str | None) -> None:

        project = self._pending_project
        if not project or not choice:
            self.reset_pending()
            self._set_status(i18n.t("cli.tui.misc.cancelled"))
            return
        if choice == CHOICE_DRY_RUN:
            # 预览不写入数据，无需执行确认防抖检查。
            self._start_migration(project, dry_run=True)
            return
        # 防抖检查避免提交路径后的连续回车直接确认迁移。
        if not self._confirm.accept(project):
            self._set_status(i18n.t("cli.tui.misc.confirm_migrate_again", project=project))
            return
        self._start_migration(project, dry_run=False)

    def _notify_busy(self) -> None:
        compat.notify(
            self.app,
            i18n.t("cli.tui.common.busy_title"),
            severity="warning",
            title=i18n.t("cli.tui.misc.button_migrate"),
        )

    def _start_migration(self, project: str, *, dry_run: bool) -> None:
        self._busy = True
        self._sync_actions()
        label = i18n.t("cli.tui.misc.label_dry_run" if dry_run else "cli.tui.misc.label_migrate")
        key = "cli.tui.misc.calling_dry_run" if dry_run else "cli.tui.misc.calling"
        self._set_status(i18n.t(key, project=project))
        # 在操作开始时固定参数，避免后台任务执行期间读取变化中的表单状态。
        flags = self.selected_flags
        self.run_worker(
            self._migrate(project, label, dry_run=dry_run, flags=flags), group="misc-migrate", exclusive=True
        )

    async def _migrate(self, project: str, label: str, *, dry_run: bool, flags: tuple[str, ...]) -> None:
        try:
            result = await asyncio.to_thread(self.source.migrate_legacy, project, dry_run=dry_run, flags=flags)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        self._render_output(result.detail)
        if result.ok:
            self.last_result = result.message
            detail = result.detail.splitlines()[-1] if result.detail else ""
            self._set_status(f"{result.message}｜{detail}" if detail else result.message)
            compat.notify(self.app, result.message, severity="information", title=label)
            if not dry_run:
                # 迁移成功后清除路径，避免后续操作复用已完成的目标。
                self.reset_pending()
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.misc.failed_detail", message=result.message, detail=tail))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def _sync_actions(self) -> None:
        self.query_one("#migrate", compat.Button).disabled = self._busy

    def _sync_output(self) -> None:
        widget = self._action_widget("#migrate-output")
        if widget is None:
            return
        widget.display = bool(self._output_lines)
        text = "\n".join(self._fit_page_width(line) for line in self._output_lines)
        self._output_rendered = text
        widget.update(compat.plain_text(text))

    def _render_output(self, detail: str) -> None:
        lines = [line for line in detail.splitlines() if line.strip()]
        self._output_lines = tuple(lines[-OUTPUT_LINES:])
        self._sync_output()

    def _fit_page_width(self, text: str) -> str:
        try:
            width = compat.widget_cells(self)[0] - 2
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            width = 78
        return compat.truncate_cells(text, max(width, 8))

    def _action_widget(self, selector: str) -> compat.Widget | None:
        try:
            return self.query_one(selector)
        except Exception:  # noqa: BLE001 - 未挂载时按无控件处理
            return None

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(self._fit_page_width(text)))

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "migrate":
            self.request_migrate()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
