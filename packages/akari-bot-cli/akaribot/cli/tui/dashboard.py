"""Dashboard 页：实例路径 / core 版本 / 运行状态 / 更新提示。

数据流：界面只读 :class:`DashboardSource`；默认实现 :class:`LocalDashboardSource` 先读
``akaribot.toml``，取不到 core 版本时再经 ``akaribot module list --json`` 子进程补取，
运行状态一律探测实例锁文件 ``.bot.lock``。快照按 TTL 缓存，周期刷新只探测锁文件，不重复取数。
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat

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
    )

    can_focus = True

    def __init__(
        self,
        source: DashboardSource | None = None,
        *,
        cache_ttl: float = 5.0,
        refresh_interval: float = 2.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DashboardSource = source if source is not None else LocalDashboardSource()
        self.cache_ttl = cache_ttl
        self.refresh_interval = refresh_interval
        self.last_error: str = ""
        self._snapshot = DashboardSnapshot()
        self._loaded_at: float = 0.0
        self._rows: tuple[tuple[str, str], ...] = ()
        self._fields_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
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
        if self.refresh_interval and self.refresh_interval > 0:
            self.set_interval(self.refresh_interval, self._on_tick)

    def focus_primary(self) -> None:
        """把焦点交给本页，供上层在页面切换时调用。"""
        compat.focus_now(self)

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
        return max(outer - 6, 16)

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        self._render_fields()

    # endregion

    # region 交互

    @compat.on(compat.Button.Pressed)
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
