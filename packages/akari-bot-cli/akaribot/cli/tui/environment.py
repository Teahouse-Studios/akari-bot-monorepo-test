"""环境页：实例用的解释器、环境里装了什么，以及往环境里装／卸运行库。

这一页是 uv 的薄封装：数据经 ``akaribot venv status --json`` 取得，动作经 ``venv add`` /
``venv remove`` / ``venv adopt`` / ``venv release`` / ``venv recreate`` 执行——界面不直接改环境。
装运行库有两种去处：**记进实例清单**（``akaribot.toml`` 的 ``runtime.requirements``，环境重建时
按它补装）与**只装进当前环境**（重建后不保留）；卸载与之一一对应。

三个解释器动作都会换掉实例正在使用的解释器，因此实例运行期间一律拒绝；装卸包只动 site-packages，
运行期间允许，但要提示重启后才生效。
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

# 标记列：● 表示清单里记着这个分发，○ 表示只存在于当前环境。
MARK_RECORDED = "●"
MARK_PLAIN = "○"

# 装卸的去处：与 ``venv add`` / ``venv remove`` 的 ``--save`` 一一对应。
SAVE_MODES = ("save", "once")
# 预演的执行记录加这个后缀，日志与断言一眼能分出「真做了」与「只预演」。
DRY_RUN_SUFFIX = ":dry-run"

GROUP_MODULE = "akaribot.modules"
GROUP_ADAPTER = "akaribot.adapters"


def _signal_name(number: int) -> str:
    # 换不出名字时退回编号文本。
    try:
        return signal.Signals(number).name
    except ValueError:
        return str(number)


@dataclass(frozen=True)
class EnvironmentPackage:
    """环境里的一个已装分发，或清单里一条尚未装上的记录。

    :param dist: 分发名。
    :param version: 版本。
    :param editable: 是否为可编辑安装。
    :param recorded: 是否记在实例清单里。
    :param akari: 是否属于 AkariBot（名字带前缀，或提供模块／适配器入口点）。
    :param groups: 该分发提供的入口点分组。
    :param requires: metadata 里的依赖串。
    :param url: 直引用的来源地址。
    :param installed: 是否真的装在环境里；``False`` 表示只有清单记录。
    """

    dist: str
    version: str = ""
    editable: bool = False
    recorded: bool = False
    akari: bool = False
    groups: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    url: str = ""
    installed: bool = True

    @property
    def tag_keys(self) -> tuple[str, ...]:
        """返回这一行要显示的标记文案键，按固定顺序。"""
        keys: list[str] = []
        if GROUP_MODULE in self.groups:
            keys.append("cli.tui.environment.tag_module")
        if GROUP_ADAPTER in self.groups:
            keys.append("cli.tui.environment.tag_adapter")
        if self.akari and not keys:
            keys.append("cli.tui.environment.tag_akari")
        if not self.installed:
            keys.append("cli.tui.environment.tag_missing")
        if self.editable:
            keys.append("cli.tui.environment.tag_editable")
        return tuple(keys)

    @property
    def tags_text(self) -> str:
        """返回标记列的文本。"""
        separator = i18n.t("cli.common.list_separator")
        return separator.join(i18n.t(key) for key in self.tag_keys)

    def row_text(self, layout: EnvironmentLayout) -> str:
        """返回列表行文本。

        :param layout: 列宽计划；表头与行共用同一份，列宽因此永远对得上。
        """
        mark = MARK_RECORDED if self.recorded else MARK_PLAIN
        name = compat.fit_cells(self.dist, layout.name_width)
        version = compat.fit_cells(self.version or "-", layout.version_width)
        row = f"{mark} {name} {version}"
        if not layout.tag_width:
            return row.rstrip()
        return f"{row} {compat.fit_cells(self.tags_text, layout.tag_width)}".rstrip()


@dataclass(frozen=True)
class EnvironmentLayout:
    """包列表的列宽计划。

    :param name_width: 名称列宽。
    :param version_width: 版本列宽。
    :param tag_width: 标记列宽；``0`` 表示放不下，这一列整体不显示。
    """

    name_width: int
    version_width: int
    tag_width: int


@dataclass(frozen=True)
class EnvironmentState:
    """一次环境快照。

    :param mode: ``managed``（实例自带 venv）或 ``external``（用当前解释器）。
    :param python: 当前生效的解释器。
    :param venv_dir: 托管 venv 的目标目录。
    :param ready: 解释器是否存在。
    :param packages: 环境里装的分发；探测失败时为 ``None``。
    :param core_version: core 版本号。
    :param error: 读取失败的原因。
    :param requirements: 实例清单里记录的运行库需求串。
    """

    mode: str = ""
    python: str = ""
    venv_dir: str = ""
    ready: bool = False
    packages: tuple[EnvironmentPackage, ...] | None = None
    core_version: str = ""
    error: str = ""
    requirements: tuple[str, ...] = ()

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

    def requirement_text(self) -> str:
        """返回清单记录的运行库说明。"""
        if not self.requirements:
            return i18n.t("cli.tui.environment.requirements_none")
        return i18n.t("cli.tui.environment.requirement_count", count=len(self.requirements))

    def rows(self) -> tuple[EnvironmentPackage, ...]:
        """返回清单与环境的并集：装了的分发，加上只在清单里的记录。"""
        packages = list(self.packages or ())
        known = {package.dist.casefold() for package in packages}
        for spec in self.requirements:
            name = recorded_name(spec)
            if not name or name.casefold() in known:
                continue
            packages.append(EnvironmentPackage(dist=name, version=spec, recorded=True, installed=False))
        return tuple(sorted(packages, key=lambda package: package.dist))


def recorded_name(spec: str) -> str:
    """从清单记录里取分发名；取不出名字的记录返回空串。

    记录一律写成 ``名字[extras]==版本`` 或 ``名字 @ 地址``，故取 ``@`` 之前、版本操作符之前的部分。
    """
    text = str(spec).split(" @ ", 1)[0].strip()
    for separator in ("==", ">=", "<=", "!=", "~=", ">", "<", "["):
        text = text.split(separator, 1)[0]
    text = text.strip()
    return "" if not text or "://" in text else text


def requirement_matches(spec: str, name: str) -> bool:
    """判断一条记录是否指向某个分发。"""
    wanted = name.strip().casefold()
    return bool(wanted) and recorded_name(spec).casefold() == wanted

    # 从依赖串里取分发名；``httpx>=0.27; extra == "x"`` 这类写法也认得。


def _needs_dist(requirement: str) -> str:
    text = requirement.split(";", 1)[0]
    for separator in ("==", ">=", "<=", "!=", "~=", ">", "<", "[", "(", " "):
        text = text.split(separator, 1)[0]
    return text.strip().casefold()


class EnvironmentSourceError(RuntimeError):
    """数据源不可用：子进程缺失、输出不是 JSON 或读取超时。"""


@runtime_checkable
class EnvironmentSource(Protocol):
    """环境数据源接口；测试注入替身，生产走子进程。"""

    def state(self) -> EnvironmentState:
        """返回环境快照。"""

    def running(self) -> bool | None:
        """返回实例是否在运行；探测失败时返回 ``None``。"""

    def action(self, kind: str, *, dry_run: bool = False) -> OperationResult:
        """执行 ``adopt`` / ``release`` / ``recreate``；``dry_run`` 为真时只预演。"""

    def add_package(self, spec: str, *, save: bool, upgrade: bool = False) -> OperationResult:
        """安装运行库；``save`` 为真时同时记进实例清单。"""

    def remove_package(self, dist: str, *, save: bool) -> OperationResult:
        """卸载运行库；``save`` 为真时同时删掉清单里的记录。"""


@dataclass(frozen=True)
class PackageCall:
    """替身记录的一次装卸调用。

    :param kind: ``add`` 或 ``remove``。
    :param target: 需求串或分发名。
    :param save: 是否写实例清单。
    :param upgrade: 是否允许升级已装版本。
    """

    kind: str
    target: str
    save: bool
    upgrade: bool = False


class StaticEnvironmentSource:
    """固定数据的替身数据源，供自动化断言使用。

    :param state: ``state`` 的返回值。
    :param running: ``running`` 的返回值。
    :param action_result: ``action`` 的返回值；缺省为成功。
    :param package_result: ``add_package`` / ``remove_package`` 的返回值；缺省为成功。
    """

    def __init__(
        self,
        state: EnvironmentState | None = None,
        *,
        running: bool | None = False,
        action_result: OperationResult | None = None,
        package_result: OperationResult | None = None,
    ) -> None:
        self._state = state or EnvironmentState(
            mode=MODE_MANAGED,
            python="/tmp/inst/.venv/bin/python",
            venv_dir="/tmp/inst/.venv",
            ready=True,
            packages=(
                EnvironmentPackage("akari-bot-core", "0.1.0", akari=True),
                EnvironmentPackage("akari-bot-module-wiki", "0.2.0", editable=True, akari=True),
                EnvironmentPackage("httpx", "0.28.1"),
                EnvironmentPackage("certifi", "2025.1.31"),
            ),
            core_version="0.1.0",
        )
        self._running = running
        self._action_result = action_result or OperationResult(
            True, i18n.t("cli.tui.environment.stub_action_ok"), "stub"
        )
        self._package_result = package_result or OperationResult(
            True, i18n.t("cli.tui.environment.stub_action_ok"), "stub"
        )
        self.calls = {"state": 0, "running": 0, "action": 0, "package": 0}
        self.actions: list[str] = []
        self.package_calls: list[PackageCall] = []

    def state(self) -> EnvironmentState:
        """见 :meth:`EnvironmentSource.state`。"""
        self.calls["state"] += 1
        return self._state

    def running(self) -> bool | None:
        """见 :meth:`EnvironmentSource.running`。"""
        self.calls["running"] += 1
        return self._running

    def action(self, kind: str, *, dry_run: bool = False) -> OperationResult:
        """见 :meth:`EnvironmentSource.action`。"""
        self.calls["action"] += 1
        self.actions.append(f"{kind}{DRY_RUN_SUFFIX}" if dry_run else kind)
        return self._action_result

    def add_package(self, spec: str, *, save: bool, upgrade: bool = False) -> OperationResult:
        """见 :meth:`EnvironmentSource.add_package`。"""
        self.calls["package"] += 1
        self.package_calls.append(PackageCall("add", spec, save, upgrade))
        return self._package_result

    def remove_package(self, dist: str, *, save: bool) -> OperationResult:
        """见 :meth:`EnvironmentSource.remove_package`。"""
        self.calls["package"] += 1
        self.package_calls.append(PackageCall("remove", dist, save))
        return self._package_result

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
        self.calls = {"state": 0, "running": 0, "action": 0, "package": 0}
        self._runner = runner or subprocess.run

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def state(self) -> EnvironmentState:
        """见 :meth:`EnvironmentSource.state`。"""
        self.calls["state"] += 1
        payload = self._invoke(("venv", "status", "--json"), timeout=self.query_timeout)
        packages = payload.get("installed")
        parsed: tuple[EnvironmentPackage, ...] | None = None
        if isinstance(packages, Sequence) and not isinstance(packages, str | bytes):
            parsed = tuple(
                EnvironmentPackage(
                    dist=str(item.get("dist") or ""),
                    version=str(item.get("version") or ""),
                    editable=bool(item.get("editable")),
                    recorded=bool(item.get("recorded")),
                    akari=bool(item.get("akari")),
                    groups=tuple(str(group) for group in item.get("groups") or ()),
                    requires=tuple(str(need) for need in item.get("requires") or ()),
                    url=str(item.get("url") or ""),
                )
                for item in packages
                if isinstance(item, Mapping) and item.get("dist")
            )
        requirements = payload.get("requirements")
        return EnvironmentState(
            mode=str(payload.get("mode") or ""),
            python=str(payload.get("python") or ""),
            venv_dir=str(payload.get("venv_dir") or ""),
            ready=bool(payload.get("exists")),
            packages=parsed,
            core_version=str(payload.get("core_version") or ""),
            error=str(payload.get("error") or ""),
            requirements=tuple(str(spec) for spec in requirements) if isinstance(requirements, list) else (),
        )

    def running(self) -> bool | None:
        """见 :meth:`EnvironmentSource.running`：读锁文件记录，不起实例进程。"""
        self.calls["running"] = self.calls.get("running", 0) + 1
        try:
            payload = self._invoke(("run", "--status", "--json"), timeout=self.query_timeout)
        except EnvironmentSourceError:
            return None
        return bool(payload.get("running"))

    def action(self, kind: str, *, dry_run: bool = False) -> OperationResult:
        """见 :meth:`EnvironmentSource.action`；``--yes`` 由界面代答。"""
        self.calls["action"] = self.calls.get("action", 0) + 1
        label = i18n.t(f"cli.tui.environment.label_{kind}")
        argv = ["venv", kind, "--yes"]
        if dry_run:
            argv.insert(2, "--dry-run")
        return self._run(cli_process.cli_argv(*argv), label=label)

    def add_package(self, spec: str, *, save: bool, upgrade: bool = False) -> OperationResult:
        """见 :meth:`EnvironmentSource.add_package`。"""
        self.calls["package"] = self.calls.get("package", 0) + 1
        label = i18n.t("cli.tui.environment.label_add_package", spec=spec)
        argv = ["venv", "add", spec, "--save" if save else "--no-save"]
        if upgrade:
            argv.append("--upgrade")
        return self._run(cli_process.cli_argv(*argv), label=label)

    def remove_package(self, dist: str, *, save: bool) -> OperationResult:
        """见 :meth:`EnvironmentSource.remove_package`。"""
        self.calls["package"] = self.calls.get("package", 0) + 1
        label = i18n.t("cli.tui.environment.label_remove_package", dist=dist)
        argv = cli_process.cli_argv("venv", "remove", dist, "--save" if save else "--no-save")
        return self._run(argv, label=label)

    def _run(self, argv: Sequence[str], *, label: str) -> OperationResult:
        try:
            completed = self._runner(
                list(argv),
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
        height: 10;
        border: round $primary;
        padding: 0 1;
    }
    EnvironmentPage #fields {
        width: 1fr;
    }
    EnvironmentPage #search-row {
        height: 3;
        align-vertical: middle;
    }
    EnvironmentPage #package-search {
        width: 1fr;
    }
    EnvironmentPage #recorded-only {
        width: auto;
        margin: 0 0 0 1;
    }
    EnvironmentPage #count {
        width: auto;
        height: 3;
        content-align-vertical: middle;
        margin: 0 1 0 1;
        color: $text-muted;
    }
    EnvironmentPage #columns {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
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
        height: auto;
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
        ("i", "install_package", i18n.t("cli.tui.environment.bind_install")),
        ("u", "uninstall_package", i18n.t("cli.tui.environment.bind_uninstall")),
        ("a", "adopt", i18n.t("cli.tui.environment.bind_adopt"), False),
        ("x", "release", i18n.t("cli.tui.environment.bind_release"), False),
        ("ctrl+n", "recreate", i18n.t("cli.tui.environment.bind_recreate"), False),
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
        self._recorded_only = False
        self._busy = False
        self._running: bool | None = False
        self._gate = compat.PendingConfirm()
        self._pending_status: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._loaded_at: float = 0.0
        self._rows: tuple[str, ...] = ()
        self._packages: tuple[EnvironmentPackage, ...] = ()
        self._columns_rendered: str = ""

    @property
    def rows(self) -> tuple[str, ...]:
        """返回最近一次渲染出的包列表行。"""
        return self._rows

    @property
    def column_text(self) -> str:
        """返回最近一次渲染出的表头行。"""
        return self._columns_rendered

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：环境概览、包清单、包装卸与解释器动作。"""
        with compat.VerticalScroll(id="fields-pane"):
            yield compat.Static(i18n.t("cli.tui.environment.fields_placeholder"), id="fields", markup=False)
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.environment.search_placeholder"), id="package-search")
            yield compat.Checkbox(i18n.t("cli.tui.environment.recorded_only"), id="recorded-only")
            yield compat.Static("", id="count", markup=False)
        yield compat.Static("", id="columns", markup=False)
        yield compat.ListView(id="package-list")
        # 装卸与解释器动作各成一组：宽终端下一行放完，放不下时在两组之间折行。
        yield compat.ButtonFlow(
            ("install", i18n.t("cli.tui.environment.button_install"), "primary"),
            ("uninstall", i18n.t("cli.tui.environment.button_uninstall"), "error"),
            ("refresh", i18n.t("cli.tui.environment.button_refresh")),
            ("adopt", i18n.t("cli.tui.environment.button_adopt"), "warning"),
            ("release", i18n.t("cli.tui.environment.button_release"), "warning"),
            ("recreate", i18n.t("cli.tui.environment.button_recreate"), "warning"),
            breaks=("refresh",),
            id="actions",
        )
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
        """返回应用搜索词与过滤后的分发。"""
        packages = self._packages
        if self._recorded_only:
            packages = tuple(package for package in packages if package.recorded)
        needle = self._query.strip().casefold()
        if not needle:
            return packages
        return tuple(
            package for package in packages if needle in package.dist.casefold() or needle in package.url.casefold()
        )

    def selected_package(self) -> EnvironmentPackage | None:
        """返回清单里高亮的那条记录。"""
        visible = self.visible_packages
        if not visible:
            return None
        try:
            list_view = self.query_one("#package-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(visible):
            return None
        return visible[index]

    def action_refresh(self) -> None:
        """键位动作：强制重新读取。"""
        self.reset_pending()
        self._pending_status = ""
        self.refresh_state(force=True)

    def action_focus_search(self) -> None:
        """键位动作：把焦点交给搜索框。"""
        self.query_one("#package-search", compat.Input).focus()

    def action_install_package(self) -> None:
        """键位动作：安装运行库。"""
        self.request_install()

    def action_uninstall_package(self) -> None:
        """键位动作：卸载选中的包。"""
        self.request_uninstall()

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

    def set_recorded_only(self, value: bool) -> None:
        """设置「只看清单里的」，等价于用户勾选。"""
        self.query_one("#recorded-only", compat.Checkbox).value = value

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
        """执行解释器动作：先弹一次选择框，可选直接执行或先预演。

        三个动作都会换掉实例正在使用的解释器，因此实例运行期间一律拒绝；动作不适用于当前模式时
        也不动作，只说明为什么。选择框代替「再按一次」：既挡住鼠标双击与键盘连发，也让用户在动手
        之前能先看一眼将要发生什么。
        """
        reason = self._blocker(kind)
        if reason:
            compat.notify(self.app, reason, severity="warning", title=i18n.t(f"cli.tui.environment.label_{kind}"))
            return
        label = i18n.t(f"cli.tui.environment.label_{kind}")
        gate_key = f"{kind}:{self._state.mode}"
        if not self._gate.accept(gate_key):
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.environment.confirm_title", label=label),
            hint=i18n.t(f"cli.tui.environment.confirm_{kind}"),
            options=(
                ("run", i18n.t("cli.tui.environment.confirm_run")),
                ("dry", i18n.t("cli.tui.environment.confirm_dry_run")),
            ),
            cancel_label=i18n.t("cli.tui.environment.cancel"),
            callback=lambda choice, target=kind: self.start_action(target, choice),
        )

    def start_action(self, kind: str, choice: str | None) -> None:
        """按选择执行解释器动作。

        :param kind: ``adopt`` / ``release`` / ``recreate``。
        :param choice: ``run`` 直接执行，``dry`` 只预演，``None`` 表示取消。
        """
        self._gate.reset()
        if choice not in ("run", "dry"):
            self._set_status(i18n.t("cli.tui.environment.action_cancelled"))
            return
        label = i18n.t(f"cli.tui.environment.label_{kind}")
        if choice == "dry":
            label = i18n.t("cli.tui.environment.label_dry_run", label=label)
        self._set_status(i18n.t("cli.tui.environment.calling", label=label))
        self.run_worker(self._operate(kind, label, dry_run=choice == "dry"), group="environment-action", exclusive=True)

    def reset_pending(self) -> None:
        """作废待确认的解释器动作；切页时由 :meth:`TuiApp.show_page` 调用。"""
        self._gate.reset()

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

    async def _operate(self, kind: str, label: str, *, dry_run: bool = False) -> None:
        self._busy = True
        self._sync_actions()
        try:
            result = await asyncio.to_thread(self.source.action, kind, dry_run=dry_run)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        self._finish(result, label)

    def request_install(self) -> None:
        """弹出输入框要需求串，再问装到哪里。"""
        reason = self._package_blocker()
        if reason:
            compat.notify(
                self.app, reason, severity="warning", title=i18n.t("cli.tui.environment.label_install_package")
            )
            return
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.environment.install_title"),
            hint=i18n.t("cli.tui.environment.install_hint"),
            placeholder=i18n.t("cli.tui.environment.install_placeholder"),
            confirm_label=i18n.t("cli.tui.environment.install_confirm"),
            cancel_label=i18n.t("cli.tui.environment.cancel"),
            callback=self.on_install_spec_entered,
        )

    def on_install_spec_entered(self, spec: str | None) -> None:
        """输入框回调：拿到需求串后再让用户选去处。

        :param spec: 用户输入的需求串；取消时为 ``None``。
        """
        text = (spec or "").strip()
        if not text:
            self._set_status(i18n.t("cli.tui.environment.install_cancelled"))
            return
        options: list[tuple[str, str]] = [
            ("save", i18n.t("cli.tui.environment.install_to_manifest")),
            ("once", i18n.t("cli.tui.environment.install_to_env")),
        ]
        if self._installed_named(text):
            # 名字已经装过时多给一条升级路径：升级只能靠写版本区间，这里直接给 -U。
            options.append(("upgrade", i18n.t("cli.tui.environment.install_upgrade")))
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.environment.install_target_title", spec=text),
            hint=i18n.t("cli.tui.environment.install_target_hint"),
            options=tuple(options),
            cancel_label=i18n.t("cli.tui.environment.cancel"),
            callback=lambda mode: self.start_install(text, mode),
        )

    def _installed_named(self, spec: str) -> bool:
        # 需求串里的分发名与环境里的已装包比对；写地址或带版本区间时不必猜，直接按名字取前缀。
        name = recorded_name(spec)
        if not name:
            return False
        wanted = name.casefold()
        return any(package.dist.casefold() == wanted for package in self._packages)

    def start_install(self, spec: str, mode: str | None) -> None:
        """按选定的去处安装运行库。

        :param spec: 需求串。
        :param mode: ``save`` 记进清单，``once`` 只装进环境；``None`` 表示取消。
        """
        if mode not in (*SAVE_MODES, "upgrade"):
            self._set_status(i18n.t("cli.tui.environment.install_cancelled"))
            return
        upgrade = mode == "upgrade"
        label = i18n.t("cli.tui.environment.label_add_package", spec=spec)
        self._set_status(i18n.t("cli.tui.environment.calling", label=label))
        self.run_worker(
            self._package_operate("add", spec, mode != "once", label, upgrade=upgrade),
            group="environment-package",
            exclusive=True,
        )

    def request_uninstall(self) -> None:
        """卸载选中的包；记在清单里的要选去处，其余连按两次确认。"""
        reason = self._package_blocker()
        if reason:
            compat.notify(
                self.app, reason, severity="warning", title=i18n.t("cli.tui.environment.label_uninstall_package")
            )
            return
        package = self.selected_package()
        if package is None:
            self._set_status(i18n.t("cli.tui.environment.no_selection"))
            return
        if package.recorded:
            options: list[tuple[str, str]] = []
            if package.installed:
                options.append(("once", i18n.t("cli.tui.environment.uninstall_keep_record")))
            options.append(("save", i18n.t("cli.tui.environment.uninstall_drop_record")))
            compat.ask_choice(
                self.app,
                title=i18n.t("cli.tui.environment.uninstall_title", dist=package.dist),
                hint=i18n.t("cli.tui.environment.uninstall_hint"),
                options=tuple(options),
                cancel_label=i18n.t("cli.tui.environment.cancel"),
                callback=lambda mode: self.start_uninstall(package, mode),
            )
            return
        # 未记进清单的包没有去处可选，但仍要弹一次确认框：卸载会动到环境，状态栏连按两次不叫确认。
        if not self._gate.accept(f"uninstall:{package.dist}"):
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.environment.uninstall_title", dist=package.dist),
            hint=i18n.t("cli.tui.environment.uninstall_confirm", dist=package.dist),
            options=(("once", i18n.t("cli.tui.environment.uninstall_confirm_action")),),
            cancel_label=i18n.t("cli.tui.environment.cancel"),
            callback=lambda mode, target=package: self.start_uninstall(target, mode),
        )

    def start_uninstall(self, package: EnvironmentPackage, mode: str | None) -> None:
        """按选定的去处卸载。

        :param package: 目标记录。
        :param mode: ``save`` 同时删掉清单记录，``once`` 只从环境卸载；``None`` 表示取消。
        """
        if mode not in SAVE_MODES:
            self._set_status(i18n.t("cli.tui.environment.uninstall_cancelled"))
            return
        label = i18n.t("cli.tui.environment.label_remove_package", dist=package.dist)
        self._set_status(i18n.t("cli.tui.environment.calling", label=label))
        self.run_worker(
            self._package_operate("remove", package.dist, mode == "save", label),
            group="environment-package",
            exclusive=True,
        )

    def _package_blocker(self) -> str:
        # 装卸包只动 site-packages，实例运行期间允许；这里只挡正在忙与没有可用解释器两种情况。
        if self._busy:
            return i18n.t("cli.tui.common.busy_title")
        if self._state.mode not in (MODE_MANAGED, MODE_EXTERNAL) or not self._state.ready:
            reason = self._state.error or i18n.t("cli.tui.environment.probe_failed")
            return i18n.t("cli.tui.environment.package_blocked", reason=reason)
        return ""

    async def _package_operate(self, kind: str, target: str, save: bool, label: str, *, upgrade: bool = False) -> None:
        self._busy = True
        self._sync_actions()
        try:
            if kind == "add":
                result = await asyncio.to_thread(self.source.add_package, target, save=save, upgrade=upgrade)
            else:
                result = await asyncio.to_thread(self.source.remove_package, target, save=save)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(
                False, i18n.t("cli.tui.common.failed_label", label=label), f"{type(error).__name__}: {error}"
            )
        self._finish(result, label)

    def _finish(self, result: OperationResult, label: str) -> None:
        self._busy = False
        if result.ok:
            self.last_result = result.message
            compat.notify(self.app, result.message, severity="information", title=label)
            if self._running:
                # 已经 import 过的模块不会因为环境变了就换版本，改完要重启实例才生效。
                self._pending_status = i18n.t("cli.tui.environment.restart_needed", label=label)
        else:
            self.last_error = result.detail or result.message
            tail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._pending_status = i18n.t("cli.tui.environment.action_failed", message=result.message, detail=tail)
            compat.notify(self.app, result.message, severity="error", title=label)
        self.refresh_state(force=True)

    def _render_all(self) -> None:
        self._packages = self._state.rows()
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
            (i18n.t("cli.tui.environment.field_requirements"), state.requirement_text()),
            (
                i18n.t("cli.tui.environment.field_state"),
                i18n.t("cli.tui.environment.state_running")
                if self._running
                else i18n.t("cli.tui.environment.state_stopped")
                if self._running is False
                else i18n.t("cli.tui.common.unknown"),
            ),
            (i18n.t("cli.tui.environment.field_selected"), self._selected_text()),
        ]
        if state.error:
            rows.append((i18n.t("cli.tui.environment.field_error"), state.error))
        lines = compat.align_rows(rows, gap=2)
        width = self._inner_width()
        if width > 0:
            lines = [compat.truncate_cells(line, width) for line in lines]
        text = "\n".join(lines)
        self.query_one("#fields", compat.Static).update(compat.plain_text(text))

    def _selected_text(self) -> str:
        package = self.selected_package()
        if package is None:
            return i18n.t("cli.tui.environment.selected_none")
        parts = [f"{package.dist} {package.version}".strip()]
        dependents = self._dependents_of(package.dist)
        if dependents:
            separator = i18n.t("cli.common.list_separator")
            parts.append(i18n.t("cli.tui.environment.selected_depended_by", names=separator.join(dependents)))
        if package.url:
            parts.append(i18n.t("cli.tui.environment.selected_url", url=package.url))
        separator = i18n.t("cli.common.clause_separator")
        return separator.join(parts)

    def _dependents_of(self, dist: str) -> tuple[str, ...]:
        # 返回依赖该分发的已装 AkariBot 包名。
        wanted = dist.strip().casefold()
        if not wanted:
            return ()
        found: list[str] = []
        for package in self._packages:
            if not package.akari or package.dist.strip().casefold() == wanted:
                continue
            if any(_needs_dist(need) == wanted for need in package.requires):
                found.append(package.dist)
        return tuple(found)

    def _layout(self, inner_width: int) -> EnvironmentLayout:
        packages = self.visible_packages
        name_width = max(min(compat.column_width(package.dist for package in packages), 32, inner_width - 18), 8)
        version_width = min(max(compat.column_width(package.version or "-" for package in packages), 5), 12)
        tag_width = min(compat.column_width(package.tags_text for package in packages), 24)
        # 放不下时先丢标记列：把名字挤成省略号比少一列标签更难用。
        if tag_width and name_width + version_width + tag_width + 5 > inner_width:
            tag_width = 0
        return EnvironmentLayout(name_width, version_width, tag_width)

    def _render_packages(self) -> None:
        list_view = self.query_one("#package-list", compat.ListView)
        packages = self.visible_packages
        inner_width = self._inner_width()
        layout = self._layout(inner_width)
        rows = tuple(package.row_text(layout) for package in packages)
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(row, markup=False)) for row in rows])
        list_view.index = 0 if rows else None
        self._rows = rows
        self._render_columns(layout, inner_width)
        self.query_one("#count", compat.Static).update(
            compat.plain_text(i18n.t("cli.tui.environment.status_pending", shown=len(rows), total=len(self._packages)))
        )
        self._render_fields()

    def _render_columns(self, layout: EnvironmentLayout, inner_width: int) -> None:
        # 表头与行共用同一份列宽计划：行里放不下标记列时，表头也必须照做。
        cells = [
            f"  {compat.fit_cells(i18n.t('cli.tui.environment.column_name'), layout.name_width)}",
            compat.fit_cells(i18n.t("cli.tui.environment.column_version"), layout.version_width),
        ]
        if layout.tag_width:
            cells.append(compat.fit_cells(i18n.t("cli.tui.environment.column_tags"), layout.tag_width))
        text = compat.truncate_cells(" ".join(cells), inner_width).rstrip()
        self._columns_rendered = text
        self.query_one("#columns", compat.Static).update(compat.plain_text(text))

    def _inner_width(self) -> int:
        try:
            outer = compat.widget_cells(self)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 72
        return max(outer - 6, 16)

    def _sync_actions(self) -> None:
        # 只显示当前模式下有意义的解释器动作：托管实例给「改用系统解释器」与「重建」，外部实例只给
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
        for kind in ("install", "uninstall", "refresh"):
            self.query_one(f"#{kind}", compat.Button).disabled = self._busy
        # 显示状态变了，按钮区的可用宽度跟着变（隐藏的按钮不占位置），重新算一次列数。
        self.query_one("#actions", compat.ButtonFlow).relayout()

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

    @compat.on(compat.Checkbox.Changed, "#recorded-only")
    def _on_recorded_only_changed(self, event: compat.Checkbox.Changed) -> None:
        self._recorded_only = bool(event.value)
        self._render_packages()

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        self._render_fields()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id in ("adopt", "release", "recreate"):
            self.request_action(str(button_id))
        elif button_id == "install":
            self.request_install()
        elif button_id == "uninstall":
            self.request_uninstall()
        elif button_id == "refresh":
            self.refresh_state(force=True)

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
