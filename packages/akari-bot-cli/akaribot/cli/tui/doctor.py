from __future__ import annotations

import asyncio
import json
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context

SOURCE_LABEL = "doctor --json"


STRICT_FLAG = "--strict"


LEVEL_ERROR = "error"
LEVEL_WARNING = "warning"

IMPLEMENTATION_CORE = "core"
IMPLEMENTATION_LOCAL = "cli"
IMPLEMENTATION_UNKNOWN = "unknown"

ORPHAN_RAN = "ran"
ORPHAN_SKIPPED = "skipped"

# 文案随当前语言解析，常量仅保存文案键。
_LEVEL_KEYS = {LEVEL_ERROR: "cli.tui.doctor.level_error", LEVEL_WARNING: "cli.tui.doctor.level_warning"}
_LEVEL_MARKS = {LEVEL_ERROR: "✖", LEVEL_WARNING: "!"}
_IMPLEMENTATION_KEYS = {
    IMPLEMENTATION_CORE: "cli.tui.doctor.impl_core",
    IMPLEMENTATION_LOCAL: "cli.tui.doctor.impl_local",
    IMPLEMENTATION_UNKNOWN: "cli.tui.doctor.impl_unknown",
}
_ORPHAN_KEYS = {ORPHAN_RAN: "cli.tui.doctor.orphan_ran", ORPHAN_SKIPPED: "cli.tui.doctor.orphan_skipped"}
# 结论默认级别与 CLI 侧判据一致：端口与凭据重复报错，孤立配置只告警。
_DEFAULT_LEVELS = {"port": LEVEL_ERROR, "credential": LEVEL_ERROR, "orphan": LEVEL_WARNING, "config": LEVEL_ERROR}

PAGE_DASHBOARD = "dashboard"
PAGE_ADAPTERS = "adapters"

_PAGE_BY_KIND = {
    "module": "modules",
    "modules": "modules",
    "adapter": PAGE_ADAPTERS,
    "adapters": PAGE_ADAPTERS,
    "platform": PAGE_ADAPTERS,
    "config": "config",
    "configuration": "config",
    "environment": "environment",
    "interpreter": "environment",
    "venv": "environment",
    "database": "database",
    "db": "database",
}


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return i18n.t("cli.tui.common.list_separator").join(item for item in (_text(entry) for entry in value) if item)
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


def _count(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _implementation_kind(value: str) -> str:
    text = value.strip().casefold()
    if text.startswith(IMPLEMENTATION_LOCAL):
        return IMPLEMENTATION_LOCAL
    if text.startswith(IMPLEMENTATION_CORE):
        return IMPLEMENTATION_CORE
    return IMPLEMENTATION_UNKNOWN


def _scalar_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return json.dumps(dict(value), ensure_ascii=False, sort_keys=True, default=str)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        separator = i18n.t("cli.tui.common.list_separator")
        return separator.join(item for item in (_text(entry) for entry in value) if item)
    return str(value)


def _detail_text(detail: Mapping[str, Any]) -> str:
    if not detail:
        return i18n.t("cli.tui.common.none")
    separator = i18n.t("cli.tui.common.list_separator")
    return separator.join(f"{name}={_scalar_text(detail[name])}" for name in sorted(detail))


@dataclass(frozen=True)
class DoctorConflict:
    """一项诊断结论。

    :param kind: ``port`` / ``credential`` / ``orphan`` / ``config``。
    :param level: ``error`` 或 ``warning``。
    :param message: 面向用户的诊断结论。
    :param platform: 相关平台名；跨平台时为空串。
    :param instances: 相关表名。
    :param detail: CLI 返回的结构化详情。
    """

    kind: str
    level: str
    message: str
    platform: str = ""
    instances: tuple[str, ...] = ()
    detail: Mapping[str, Any] = field(default_factory=dict)

    @property
    def mark(self) -> str:
        """级别标记；未知级别用问号。"""
        return _LEVEL_MARKS.get(self.level, "?")

    @property
    def level_label(self) -> str:
        """级别的本地化标签；未知级别直接显示原值。"""
        key = _LEVEL_KEYS.get(self.level)
        return i18n.t(key) if key else self.level

    @property
    def target_page(self) -> str:
        """返回处理页面键；无专用页面时按平台信息选择适配器页或概览页。"""
        page = _PAGE_BY_KIND.get(self.kind.strip().casefold())
        if page:
            return page
        return PAGE_ADAPTERS if self.platform else PAGE_DASHBOARD

    @property
    def target_page_label(self) -> str:
        """处理页面的本地化名称。"""
        return i18n.t(f"cli.tui.nav.{self.target_page}")

    @property
    def next_step(self) -> str:
        """返回处理页面或 CLI 命令提示。"""
        if _PAGE_BY_KIND.get(self.kind.strip().casefold()) or self.platform:
            return i18n.t("cli.tui.doctor.next_step_page", page=self.target_page_label)
        return i18n.t("cli.tui.doctor.next_step_cli")


@dataclass(frozen=True)
class DoctorChecks:
    """``doctor --json`` 的 ``checks`` 段。

    :param instances: 扫描到的适配器实例数。
    :param installed_adapters: 已安装适配器的平台名。
    :param unconfigured_adapters: 已安装但未配置实例的平台名。
    :param orphan_check: 孤立配置检查的执行状态，``ran`` 或 ``skipped``。
    :param credential_scope: CLI 返回的凭据比较字段范围。
    """

    instances: int = 0
    installed_adapters: tuple[str, ...] = ()
    unconfigured_adapters: tuple[str, ...] = ()
    orphan_check: str = ""
    credential_scope: str = ""

    @property
    def orphan_label(self) -> str:
        """孤立配置检查执行状态的本地化标签。"""
        key = _ORPHAN_KEYS.get(self.orphan_check)
        return i18n.t(key) if key else i18n.t("cli.tui.doctor.orphan_unknown")


@dataclass(frozen=True)
class DoctorSnapshot:
    """诊断结果快照。

    :param instance_root: 实例根目录文本。
    :param config_root: 配置目录文本。
    :param implementation: CLI 返回的实现来源。
    :param registry_available: 已安装适配器清单是否可用。
    :param registry_note: 清单不可用时的原因。
    :param conflicts: 结论列表，顺序与 CLI 输出一致。
    :param error_count: error 级结论数。
    :param warning_count: warning 级结论数。
    :param checks: 检查项统计。
    :param errors: 数据读取错误；有值时结论不完整。
    """

    instance_root: str = ""
    config_root: str = ""
    implementation: str = ""
    registry_available: bool = False
    registry_note: str = ""
    conflicts: tuple[DoctorConflict, ...] = ()
    error_count: int = 0
    warning_count: int = 0
    checks: DoctorChecks = field(default_factory=DoctorChecks)
    errors: tuple[str, ...] = ()

    @property
    def implementation_kind(self) -> str:
        """返回诊断结果的实现来源。"""
        return _implementation_kind(self.implementation)

    @property
    def implementation_label(self) -> str:
        """实现来源的本地化标签。"""
        kind = self.implementation_kind
        if kind == IMPLEMENTATION_UNKNOWN and self.implementation:
            return i18n.t("cli.tui.doctor.impl_other", value=self.implementation)
        return i18n.t(_IMPLEMENTATION_KEYS[kind])

    @property
    def passed(self) -> bool:
        """返回诊断是否完成且未发现问题。"""
        return not self.errors and not self.conflicts


def normalize_snapshot(payload: Any) -> DoctorSnapshot:
    """将 ``doctor --json`` 输出转换为诊断快照。

    :param payload: ``json.loads`` 的结果。
    :return: 诊断快照；缺字段按默认值处理。
    :raises DoctorSourceError: 负载不是 JSON 对象。
    """
    if not isinstance(payload, Mapping):
        raise DoctorSourceError(i18n.t("cli.tui.doctor.src_bad_payload", label=SOURCE_LABEL))
    raw_conflicts = payload.get("conflicts")
    entries = (
        list(raw_conflicts)
        if isinstance(raw_conflicts, Sequence) and not isinstance(raw_conflicts, (str, bytes))
        else []
    )
    conflicts: list[DoctorConflict] = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        kind = _text(_pick(entry, "kind", "type"))
        detail = entry.get("detail")
        conflicts.append(
            DoctorConflict(
                kind=kind,
                level=_text(_pick(entry, "level")).casefold() or _DEFAULT_LEVELS.get(kind, LEVEL_WARNING),
                message=_text(_pick(entry, "message", "summary")),
                platform=_text(_pick(entry, "platform")),
                instances=_string_tuple(_pick(entry, "instances", "tables")),
                detail=detail if isinstance(detail, Mapping) else {},
            )
        )
    summary = payload.get("summary")
    summary = summary if isinstance(summary, Mapping) else {}
    error_count = _count(summary.get("error"))
    warning_count = _count(summary.get("warning"))
    if error_count is None:
        error_count = sum(1 for item in conflicts if item.level == LEVEL_ERROR)
    if warning_count is None:
        warning_count = sum(1 for item in conflicts if item.level != LEVEL_ERROR)
    return DoctorSnapshot(
        instance_root=_text(payload.get("instance_root")),
        config_root=_text(payload.get("config_root")),
        implementation=_text(payload.get("implementation")),
        registry_available=_flag(payload.get("registry_available")),
        registry_note=_text(payload.get("registry_note")),
        conflicts=tuple(conflicts),
        error_count=error_count,
        warning_count=warning_count,
        checks=_checks(payload.get("checks")),
    )


def _checks(payload: Any) -> DoctorChecks:
    source = payload if isinstance(payload, Mapping) else {}
    count = _count(_pick(source, "instances", "instance_count"))
    return DoctorChecks(
        instances=count if count is not None else 0,
        installed_adapters=_string_tuple(_pick(source, "installed_adapters", default=())),
        unconfigured_adapters=_string_tuple(_pick(source, "unconfigured_adapters", default=())),
        orphan_check=_text(_pick(source, "orphan_check")).casefold(),
        credential_scope=_text(_pick(source, "credential_scope")),
    )


class DoctorSourceError(RuntimeError):
    """数据源不可用：子进程缺失、输出不是 JSON 或结构不符。"""


@runtime_checkable
class DoctorSource(Protocol):
    """诊断数据源接口。"""

    def load_snapshot(self, *, strict: bool = False) -> DoctorSnapshot:
        """返回诊断结果；严格模式下警告视为失败，读取错误记录在快照的 ``errors`` 中。"""


class StaticDoctorSource:
    """用于测试的静态数据源，不创建子进程。

    :param snapshot: ``load_snapshot`` 的返回值。
    :param error: 设定后 ``load_snapshot`` 抛出该异常，用于验证失败路径。
    """

    def __init__(self, snapshot: DoctorSnapshot | None = None, error: Exception | None = None) -> None:
        self._snapshot = snapshot if snapshot is not None else DoctorSnapshot()
        self._error = error
        self.calls = {"load": 0, "strict": 0}

    def load_snapshot(self, *, strict: bool = False) -> DoctorSnapshot:
        """见 :meth:`DoctorSource.load_snapshot`。"""
        self.calls["load"] += 1
        if strict:
            self.calls["strict"] += 1
        if self._error is not None:
            raise self._error
        return self._snapshot


class SubprocessDoctorSource:
    """通过 ``akaribot doctor --json`` 子进程读取诊断结果。

    :param root: 实例根目录，默认取当前实例。
    :param timeout: 子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        # 实例根在每次请求时解析，使子进程目录与 AKARI_INSTANCE_DIR 跟随当前实例。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"load": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """返回实例根目录，依次采用显式路径、当前实例或自动定位结果。"""
        return context.resolve_root(self._root_override)

    def load_snapshot(self, *, strict: bool = False) -> DoctorSnapshot:
        """见 :meth:`DoctorSource.load_snapshot`。"""
        self.calls["load"] += 1
        args = SOURCE_LABEL.split()
        if strict:
            args.insert(1, STRICT_FLAG)
        label = " ".join(args)
        argv = cli_process.cli_argv(*args)
        try:
            completed = self._run(argv)
        except DoctorSourceError as error:
            return DoctorSnapshot(errors=(str(error),))
        # 非零退出码可能表示诊断发现问题，完整的 JSON 结果仍须展示。
        try:
            payload = self._parse_json(completed.stdout, label)
        except DoctorSourceError as error:
            if completed.returncode != 0:
                tail = self._tail(completed.stderr) or i18n.t("cli.tui.common.no_output")
                exit_error = i18n.t(
                    "cli.tui.doctor.src_exit_code",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=tail,
                )
                return DoctorSnapshot(errors=(exit_error, str(error)))
            return DoctorSnapshot(errors=(str(error),))
        try:
            return normalize_snapshot(payload)
        except DoctorSourceError as error:
            return DoctorSnapshot(errors=(str(error),))

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
                env=cli_process.cli_env(self.root),
            )
        except FileNotFoundError as error:
            raise DoctorSourceError(i18n.t("cli.tui.doctor.src_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise DoctorSourceError(
                i18n.t("cli.tui.doctor.src_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from error
        except OSError as error:
            raise DoctorSourceError(i18n.t("cli.tui.doctor.src_oserror", cmd=" ".join(argv), error=error)) from error

    def _parse_json(self, stdout: str, label: str) -> Any:
        text = stdout.strip()
        if not text:
            raise DoctorSourceError(i18n.t("cli.tui.doctor.src_empty_output", label=label))
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise DoctorSourceError(i18n.t("cli.tui.doctor.src_bad_json", label=label, error=error)) from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        return (text or "").strip()[-limit:]


class _ConflictListView(compat.ListView):
    # 回车与单击均产生 Selected 消息，需单独绑定回车，才能保留单击查看详情的行为。
    BINDINGS = [compat.bind("enter", "open_conflict", i18n.t("cli.tui.doctor.bind_open"))]

    def action_open_conflict(self) -> None:
        self.screen.query_one(DoctorPage).open_selected_conflict()


class DoctorPage(compat.Vertical):
    """诊断页控件。

    :param source: 数据源，默认为 :class:`SubprocessDoctorSource`。
    """

    can_focus = True

    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.doctor.bind_refresh")),
        ("enter", "open_conflict", i18n.t("cli.tui.doctor.bind_open")),
    )

    DEFAULT_CSS = """
    DoctorPage {
        layout: vertical;
        height: 1fr;
    }
    DoctorPage #summary {
        height: 7;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DoctorPage #verdict {
        height: 1;
        padding: 0 1;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DoctorPage #conflict-list {
        height: 1fr;
        min-height: 4;
        border: round $primary;
    }
    DoctorPage #conflict-list > ListItem {
        padding: 0;
    }
    DoctorPage #conflict-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DoctorPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    DoctorPage #actions Button {
        min-width: 0;
    }
    DoctorPage #strict {
        width: auto;
        margin: 0 0 0 2;
    }
    DoctorPage #detail {
        height: 1fr;
        max-height: 6;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DoctorPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(self, source: DoctorSource | None = None, *, id: str | None = None) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DoctorSource = source if source is not None else SubprocessDoctorSource()
        self.last_error: str = ""
        self._snapshot = DoctorSnapshot()
        self._loaded_at: float = 0.0
        self._busy: bool = False
        self._strict: bool = False
        self._selected_index: int = 0
        self._summary_rendered: str = ""
        self._verdict_rendered: str = ""
        self._detail_rendered: str = ""
        self._row_texts: tuple[str, ...] = ()
        self._conflict_rows: tuple[tuple[str, str, str], ...] = ()
        self._status_key: str = "cli.tui.common.status_ready"
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:

        yield compat.Static(i18n.t("cli.tui.doctor.summary_pending"), id="summary", markup=False)
        yield compat.Static(i18n.t("cli.tui.doctor.verdict_pending"), id="verdict", markup=False)
        yield _ConflictListView(id="conflict-list")
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.doctor.action_refresh"), id="refresh", variant="primary")
            yield compat.Button(i18n.t("cli.tui.doctor.action_open"), id="open-conflict")
            yield compat.Checkbox(i18n.t("cli.tui.doctor.strict_option"), id="strict")
        yield compat.Static(i18n.t("cli.tui.doctor.detail_placeholder"), id="detail", markup=False)
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:

        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取一次诊断结果。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_report()

    def focus_primary(self) -> None:
        """聚焦冲突列表；列表为空时聚焦页面容器。"""
        compat.focus_first(self, "#conflict-list")

    @property
    def snapshot(self) -> DoctorSnapshot:
        """返回缓存快照，不启动子进程。"""
        return self._snapshot

    @property
    def conflicts(self) -> tuple[DoctorConflict, ...]:
        """返回缓存中的结论列表。"""
        return self._snapshot.conflicts

    @property
    def selected_conflict(self) -> DoctorConflict | None:
        """返回列表当前高亮项对应的结论。"""
        conflicts = self._snapshot.conflicts
        if not conflicts:
            return None
        # 后台请求可能在页面卸载后完成，访问控件前需检查挂载状态。
        if not compat.mounted(self):
            return None
        list_view = self.query_one("#conflict-list", compat.ListView)
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(conflicts):
            return None
        return conflicts[index]

    @property
    def summary_text(self) -> str:
        """返回统计面板当前渲染出的文本。"""
        return self._summary_rendered

    @property
    def verdict_text(self) -> str:
        """返回结论行当前渲染出的文本。"""
        return self._verdict_rendered

    @property
    def detail_text(self) -> str:
        """返回详情区当前渲染出的文本。"""
        return self._detail_rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def status_key(self) -> str:
        """返回状态栏当前文案键。"""
        return self._status_key

    @property
    def strict(self) -> bool:
        """返回严格模式开关的当前取值。"""
        return self._strict

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的冲突行文本。"""
        return self._row_texts

    def row_cells(self) -> tuple[tuple[str, str, str], ...]:
        """返回冲突行的级别标记、级别与结论，顺序与列表一致。"""
        return self._conflict_rows

    def refresh_report(self) -> None:
        """执行诊断并更新页面；读取期间禁用刷新按钮。"""
        if self._busy:
            return
        self._start_load()

    def _start_load(self) -> None:
        self._set_busy(True)
        self._set_status("cli.tui.doctor.status_loading")
        self.run_worker(self._load(self._strict), group="doctor-load", exclusive=True)

    async def _load(self, strict: bool) -> bool:
        try:
            snapshot = await asyncio.to_thread(self.source.load_snapshot, strict=strict)
        except Exception as error:  # noqa: BLE001 - 数据源异常不应中断界面
            self._snapshot = DoctorSnapshot(errors=(f"{type(error).__name__}: {error}",))
            self._loaded_at = time.monotonic()
            self.last_error = self._snapshot.errors[0]
            self._render_report()
            self._set_status("cli.tui.doctor.status_failed", error=self.last_error)
            self._set_busy(False)
            return False
        self._snapshot = snapshot
        self._loaded_at = time.monotonic()
        self.last_error = i18n.t("cli.tui.common.error_separator").join(snapshot.errors)
        self._render_report()
        if self.last_error:
            self._set_status("cli.tui.doctor.status_failed", error=self.last_error)
        else:
            self._set_status(
                "cli.tui.doctor.status_loaded",
                errors=snapshot.error_count,
                warnings=snapshot.warning_count,
                implementation=snapshot.implementation_label,
            )
        self._set_busy(False)
        return True

    def _set_busy(self, value: bool) -> None:
        self._busy = value
        self.query_one("#refresh", compat.Button).disabled = value

    def _render_report(self) -> None:
        if not compat.mounted(self):
            return
        self._render_summary()
        self._render_verdict()
        self._render_rows()
        self._render_detail()

    def _render_summary(self) -> None:
        # 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
        if not compat.mounted(self):
            return
        snapshot = self._snapshot
        checks = snapshot.checks
        separator = i18n.t("cli.tui.common.list_separator")
        installed = separator.join(checks.installed_adapters) or i18n.t("cli.tui.common.none")
        unconfigured = separator.join(checks.unconfigured_adapters) or i18n.t("cli.tui.common.none")
        scope = checks.credential_scope or i18n.t("cli.tui.common.unknown")
        if snapshot.registry_available:
            checks_line = i18n.t("cli.tui.doctor.checks_line", orphan=checks.orphan_label, scope=scope)
        else:
            checks_line = i18n.t(
                "cli.tui.doctor.checks_degraded",
                orphan=checks.orphan_label,
                scope=scope,
                note=snapshot.registry_note or i18n.t("cli.tui.common.unknown"),
            )
        unknown = i18n.t("cli.tui.common.unknown")
        strict_state = i18n.t("cli.tui.doctor.strict_on" if self._strict else "cli.tui.doctor.strict_off")
        rows = [
            (i18n.t("cli.tui.doctor.field_instance_root"), snapshot.instance_root or unknown),
            (i18n.t("cli.tui.doctor.field_config_root"), snapshot.config_root or unknown),
            (i18n.t("cli.tui.doctor.field_instance_count"), str(checks.instances)),
            (i18n.t("cli.tui.doctor.field_installed_adapters"), installed),
            (i18n.t("cli.tui.doctor.field_unconfigured_adapters"), unconfigured),
            (i18n.t("cli.tui.doctor.field_checks"), checks_line),
            (i18n.t("cli.tui.doctor.field_strict"), strict_state),
        ]
        text = "\n".join(self._fit_page_width(line) for line in compat.align_rows(rows))
        self._summary_rendered = text
        self.query_one("#summary", compat.Static).update(compat.plain_text(text))

    def _render_verdict(self) -> None:
        # 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
        if not compat.mounted(self):
            return
        text = self._verdict_line()
        self._verdict_rendered = text
        self.query_one("#verdict", compat.Static).update(compat.plain_text(self._fit_page_width(text)))

    def _verdict_line(self) -> str:
        if not self._loaded_at:
            return i18n.t("cli.tui.doctor.verdict_pending")
        if self._snapshot.errors:
            return i18n.t("cli.tui.doctor.verdict_failed")
        if not self._snapshot.conflicts:
            return i18n.t("cli.tui.doctor.verdict_passed")
        return i18n.t(
            "cli.tui.doctor.verdict_conflicts",
            errors=self._snapshot.error_count,
            warnings=self._snapshot.warning_count,
        )

    def _render_rows(self) -> None:
        list_view = self.query_one("#conflict-list", compat.ListView)
        conflicts = self._snapshot.conflicts
        self._conflict_rows = tuple((item.mark, item.level, item.message) for item in conflicts)
        self._row_texts = tuple(self._compose_row(item) for item in conflicts)
        compat.rebuild_rows(list_view, self._row_texts, self._restore_index())

    def _compose_row(self, conflict: DoctorConflict) -> str:
        return f"{conflict.mark} {conflict.level_label}  {conflict.message}"

    def _restore_index(self) -> int:
        if self._selected_index and 0 <= self._selected_index < len(self._snapshot.conflicts):
            return self._selected_index
        return 0

    def _render_detail(self) -> None:
        # 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
        if not compat.mounted(self):
            return
        text = "\n".join(self._fit_page_width(line) for line in self._detail_lines())
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _detail_lines(self) -> list[str]:
        conflict = self.selected_conflict
        if conflict is None:
            return [self._empty_detail_line()]
        # 短屏优先显示结论与处理步骤，定位信息与详情按需滚动查看。
        kind = conflict.kind or i18n.t("cli.tui.common.unknown")
        rows: list[tuple[str, str]] = [
            (i18n.t("cli.tui.doctor.field_message"), conflict.message),
            (i18n.t("cli.tui.doctor.field_next"), conflict.next_step),
            (i18n.t("cli.tui.doctor.field_level_kind"), f"{conflict.mark} {conflict.level_label} · {kind}"),
        ]
        if conflict.platform:
            rows.append((i18n.t("cli.tui.doctor.field_platform"), conflict.platform))
        if conflict.instances:
            separator = i18n.t("cli.tui.common.list_separator")
            rows.append((i18n.t("cli.tui.doctor.field_instances"), separator.join(conflict.instances)))
        rows.append((i18n.t("cli.tui.doctor.field_detail"), _detail_text(conflict.detail)))
        return compat.align_rows(rows)

    def _empty_detail_line(self) -> str:
        if not self._loaded_at:
            return i18n.t("cli.tui.doctor.detail_placeholder")
        if self._snapshot.errors:
            return i18n.t("cli.tui.doctor.detail_failed")
        if not self._snapshot.conflicts:
            return i18n.t("cli.tui.doctor.detail_passed")
        return i18n.t("cli.tui.doctor.detail_hint_select")

    def _fit_page_width(self, text: str) -> str:
        try:
            width = compat.widget_cells(self)[0] - 2
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            width = 78
        return compat.truncate_cells(text, max(width, 8))

    def _set_status(self, key: str, **params: Any) -> None:
        # 后台请求可能在页面卸载后完成，更新状态栏前需检查挂载状态。
        if not compat.mounted(self):
            return
        self._status_key = key
        self._status_rendered = i18n.t(key, **params)
        self.query_one("#status", compat.Static).update(compat.plain_text(self._fit_page_width(self._status_rendered)))

    def on_resize(self, event: compat.events.Resize) -> None:

        if self._loaded_at:
            self._render_report()

    @compat.on(compat.ListView.Highlighted, "#conflict-list")
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        index = compat.highlighted_index(event.list_view)
        if index is not None:
            self._selected_index = index
        self._render_detail()

    @compat.on(compat.Checkbox.Changed, "#strict")
    def _on_strict_changed(self, event: compat.Checkbox.Changed) -> None:
        self._strict = bool(event.value)
        if self._loaded_at:
            self._render_summary()
        # 选项变化后，旧请求的结果无效，需取消旧请求并重新诊断。
        self._start_load()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        if event.button.id == "refresh":
            self.refresh_report()
        elif event.button.id == "open-conflict":
            self.open_selected_conflict()

    def action_refresh(self) -> None:

        self.refresh_report()

    def action_open_conflict(self) -> None:

        self.open_selected_conflict()

    def open_selected_conflict(self) -> None:
        """打开当前结论对应的处理页面，并显示切换结果。"""
        conflict = self.selected_conflict
        if conflict is None:
            self._set_status("cli.tui.doctor.status_nothing")
            return
        self.app.show_page(conflict.target_page)
        self._set_status("cli.tui.doctor.status_jumped", page=conflict.target_page_label)
        # 切页后当前状态栏不可见，使用通知显示跳转结果。
        compat.notify(self.app, self._status_rendered, title=i18n.t("cli.tui.doctor.bind_open"))

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
