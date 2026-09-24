"""Modules 页：列表 + 搜索 + 详情 + 安装/卸载 + 进度。

数据流：界面只读 :class:`ModuleSource`，默认实现 :class:`SubprocessModuleSource` 以子进程
方式取数（CLI 进程不 import core）。列表结果缓存在本页内，渲染与搜索一律走缓存；
安装/卸载成功后缓存失效并在同一后台任务里重新读取。
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import time
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.instance import default_instance_root
from akaribot.cli.tui import _compat as compat

STATE_INSTALLED = "installed"
STATE_AVAILABLE = "available"
STATE_UNKNOWN = "unknown"

# 状态与包类型是对端 JSON 的取值，界面按当前语言取标签，故这里只存文案键。
_STATE_KEYS = {
    STATE_INSTALLED: "cli.tui.modules.state_installed",
    STATE_AVAILABLE: "cli.tui.modules.state_available",
    STATE_UNKNOWN: "cli.tui.modules.state_unknown",
}
_KIND_KEYS = {
    "module": "cli.tui.modules.kind_module",
    "adapter": "cli.tui.modules.kind_adapter",
    "core": "cli.tui.modules.kind_core",
    "testing": "cli.tui.modules.kind_testing",
}
_KIND_ALIASES = {"builtin": "module", "builtins": "module", "package": "module", "unknown": ""}
_INSTALLED_MARKERS = ("install", "loaded", "enabled", "active")
_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_CLI_ENV_BIN = "AKARIBOT_CLI_BIN"

# 进度条按阶段推进：解析、执行、重载、完成；阶段内的细粒度进度由子进程输出行承担。
_PROGRESS_PHASES = 4.0
# 实时转发时保留的末尾行数，失败时作为详情展示。
_STREAM_TAIL_LINES = 40


@dataclass(frozen=True)
class ModuleRecord:
    """一条模块记录，字段名按 CLI JSON 契约归一化后的结果。

    :param name: 模块名，即注册名。
    :param dist: 发行包名，安装与卸载以它为目标。
    :param version: 版本号，未知时为空串。
    :param summary: 简介。
    :param state: ``installed`` / ``available`` / ``unknown``。
    :param requires_core_api: 声明的核心 API 版本约束。
    :param dependents: 依赖本模块的发行包名。
    :param origin: 记录来源说明，供详情面板展示。
    :param kind: ``module`` / ``adapter`` / ``core`` / ``testing``，未知时为空串。
    :param provides_modules: 该包注册的模块名。
    :param owned_tables: 该包拥有的数据表。
    :param config_table: 该包在 ``config/`` 下的扁平配置表名；无配置时为空串。
    """

    name: str
    dist: str = ""
    version: str = ""
    summary: str = ""
    state: str = STATE_UNKNOWN
    requires_core_api: str = ""
    dependents: tuple[str, ...] = ()
    origin: str = ""
    kind: str = ""
    provides_modules: tuple[str, ...] = ()
    owned_tables: tuple[str, ...] = ()
    config_table: str = ""

    @property
    def installed(self) -> bool:
        """判断该模块是否已安装。"""
        return self.state == STATE_INSTALLED

    @property
    def state_label(self) -> str:
        """返回状态的本地化标签。"""
        key = _STATE_KEYS.get(self.state)
        return i18n.t(key) if key else self.state

    @property
    def kind_label(self) -> str:
        """返回包类型的本地化标签，未知时给出「未声明」。"""
        key = _KIND_KEYS.get(self.kind)
        return i18n.t(key) if key else i18n.t("cli.tui.common.undeclared")

    def haystack(self) -> str:
        """返回搜索用的匹配文本，已做大小写折叠。"""
        parts = (
            self.name,
            self.dist,
            self.version,
            self.summary,
            self.state_label,
            self.kind_label,
            *self.provides_modules,
        )
        return " ".join(part for part in parts if part).casefold()

    def matches(self, query: str) -> bool:
        """按空白分词的子串匹配，全部词命中才算匹配。

        :param query: 搜索词；中文按子串处理，无需分词。
        :return: 是否命中。
        """
        tokens = query.casefold().split()
        if not tokens:
            return True
        haystack = self.haystack()
        return all(token in haystack for token in tokens)


@dataclass(frozen=True)
class OperationResult:
    """安装或卸载的结果。

    :param ok: 子进程是否成功。
    :param message: 一行结论，用于状态栏与通知。
    :param detail: 失败时的补充信息，通常为子进程输出尾部。
    """

    ok: bool
    message: str
    detail: str = ""


class ModuleSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


class StaticModuleSource:
    """固定数据的替身数据源，供自动化断言与自检使用，不产生任何子进程。

    :param records: ``list_modules`` 直接返回的记录序列。
    :param available: ``list_available`` 直接返回的记录序列。
    :param install_result: 安装返回值；缺省为成功。
    :param uninstall_result: 卸载返回值；缺省为成功。
    :param stream_lines: ``stream_operation`` 逐行上报的假输出。
    """

    def __init__(
        self,
        records: Sequence[ModuleRecord] = (),
        *,
        available: Sequence[ModuleRecord] = (),
        install_result: OperationResult | None = None,
        uninstall_result: OperationResult | None = None,
        stream_lines: Sequence[str] = (),
    ) -> None:
        self._records = tuple(records)
        self._available = tuple(available)
        self._stream_lines = tuple(stream_lines)
        self._install_result = install_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_install_ok"), "stub"
        )
        self._uninstall_result = uninstall_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_uninstall_ok"), "stub"
        )
        self.calls = {"list": 0, "available": 0, "install": 0, "uninstall": 0}
        self.installed: list[str] = []
        self.uninstalled: list[str] = []

    def list_modules(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_modules`。"""
        self.calls["list"] += 1
        return self._records

    def list_available(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_available`。"""
        self.calls["available"] += 1
        return self._available

    def install(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.install`。"""
        self.calls["install"] += 1
        self.installed.append(record.dist or record.name)
        return self._install_result

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.uninstall`。"""
        self.calls["uninstall"] += 1
        self.uninstalled.append(record.dist or record.name)
        return self._uninstall_result

    async def stream_operation(
        self, kind: str, record: ModuleRecord, on_line: Callable[[str], None]
    ) -> OperationResult:
        """见 :meth:`ModuleSource.stream_operation`；替身直接回放固定输出。"""
        for line in self._stream_lines:
            on_line(line)
        return self.install(record) if kind == "install" else self.uninstall(record)


@runtime_checkable
class ModuleSource(Protocol):
    """模块数据源接口；测试注入替身，生产走子进程。"""

    def list_modules(self) -> Sequence[ModuleRecord]:
        """返回全部模块记录。"""

    def list_available(self) -> Sequence[ModuleRecord]:
        """返回可安装的模块记录，含尚未安装的项。"""

    def install(self, record: ModuleRecord) -> OperationResult:
        """安装给定记录。"""

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """卸载给定记录。"""

    async def stream_operation(
        self, kind: str, record: ModuleRecord, on_line: Callable[[str], None]
    ) -> OperationResult:
        """执行安装或卸载，并把子进程输出逐行交给 ``on_line``。

        :param kind: ``install`` 或 ``uninstall``。
        :param record: 目标记录。
        :param on_line: 每读到一行输出就调用一次，供界面显示进度。
        :return: 操作结果。
        """


def sort_key(record: ModuleRecord) -> tuple[bool, str]:
    """列表展示顺序：已安装在前，其次按名称升序（大小写不敏感）。"""
    return (not record.installed, record.name.casefold())


def _pick(source: Any, *names: str, default: Any = "") -> Any:
    for name in names:
        if isinstance(source, Mapping) and source.get(name) is not None:
            return source[name]
        value = getattr(source, name, None)
        if value is not None:
            return value
    return default


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return i18n.t("cli.tui.common.list_separator").join(_text(item) for item in value if _text(item))
    return str(value)


def _as_text_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, (list, tuple, set)):
        return tuple(text for item in value if (text := _text(item)))
    return ()


def _normalize_state(source: Any, fallback: str) -> str:
    raw = _text(_pick(source, "state", "status", "load_state", "install_state"))
    if raw:
        lowered = raw.casefold()
        if lowered in (STATE_INSTALLED, STATE_AVAILABLE, STATE_UNKNOWN):
            return lowered
        if any(marker in lowered for marker in _INSTALLED_MARKERS):
            return STATE_INSTALLED
        return STATE_AVAILABLE
    flag = _pick(source, "installed", "is_installed", "loadable", default=None)
    if isinstance(flag, bool):
        return STATE_INSTALLED if flag else STATE_AVAILABLE
    return fallback


def _normalize_kind(value: Any) -> str:
    raw = _text(value).casefold()
    if not raw:
        return ""
    raw = _KIND_ALIASES.get(raw, raw)
    return raw if raw in _KIND_KEYS else ""


def _record_from_mapping(dist: str, info: Any) -> ModuleRecord:
    if isinstance(info, str):
        info = {"version": info}
    dist_name = _text(_pick(info, "dist", "distribution", "package", "dist_name")) or dist
    name = _text(_pick(info, "name", "module", "module_name", "import_name", "id")) or dist_name
    dependents = _pick(info, "dependents", "required_by", "reverse_dependencies", default=())
    if isinstance(dependents, str):
        dependents = (dependents,) if dependents else ()
    return ModuleRecord(
        name=name,
        dist=dist_name or name,
        version=_text(_pick(info, "version", "ver", "dist_version")),
        summary=_text(_pick(info, "summary", "description", "desc", "doc")),
        state=_normalize_state(info, STATE_INSTALLED),
        requires_core_api=_text(_pick(info, "requires_core_api", "core_api", "api_version")),
        dependents=tuple(_text(item) for item in dependents),
        origin=_text(_pick(info, "origin", "path", "location", "dist_info")),
        kind=_normalize_kind(_pick(info, "kind", "type", "category")),
        provides_modules=_as_text_tuple(_pick(info, "provides_modules", "modules", default=())),
        owned_tables=_as_text_tuple(_pick(info, "owned_tables", "tables", default=())),
        config_table=_text(_pick(info, "config_table", "config")),
    )


def normalize_records(payload: Any) -> list[ModuleRecord]:
    """把对端 JSON 归一化为记录列表并排序。

    接受三种形态：记录数组、以发行包名为键的映射、``{"modules": [...]}`` 之类的包装对象。
    记录默认视为已安装，因为列表命令输出的就是实例内已装的包。

    :param payload: ``json.loads`` 的结果。
    :return: 按「已安装在前、名称升序」排序的记录列表。
    """
    if payload is None:
        return []
    if isinstance(payload, Mapping):
        for key in ("modules", "packages", "installed", "items", "data"):
            nested = payload.get(key)
            if isinstance(nested, (list, tuple, Mapping)) and not isinstance(nested, str):
                return normalize_records(nested)
        records = [_record_from_mapping(_text(key), value) for key, value in payload.items()]
    elif isinstance(payload, (list, tuple)):
        records = []
        for item in payload:
            if isinstance(item, str):
                records.append(ModuleRecord(name=item, dist=item, state=STATE_INSTALLED))
            elif isinstance(item, Mapping) or hasattr(item, "name"):
                records.append(_record_from_mapping("", item))
    else:
        return []
    return sorted(records, key=sort_key)


class SubprocessModuleSource:
    """默认数据源：一律经子进程取数，CLI 进程内不 import core。

    取数按优先级降级：先调 ``akaribot module list --json``；该命令未实现或失败时，
    退回 :class:`akaribot.cli.instance.Instance` 的 ``installed()``。失败原因全部汇总上报。

    :param root: 实例根目录，默认当前工作目录。
    :param timeout: 单个子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: ``Instance`` 的构造回调，测试可注入以避开 T5.1 的实现。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        instance_factory: Callable[[], Any] | None = None,
    ) -> None:
        # 实例根同时是子进程的 cwd 与 AKARI_INSTANCE_DIR；相对值会在子进程里二次拼接而失效，
        # 只认 cwd 则会忽略 AKARI_INSTANCE_DIR。
        self.root = Path(root).expanduser().resolve() if root is not None else default_instance_root()
        self.timeout = timeout
        self.calls = {"list": 0, "available": 0, "install": 0, "uninstall": 0}
        self._runner = runner or subprocess.run
        self._instance_factory = instance_factory

    def list_modules(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_modules`。"""
        self.calls["list"] += 1
        errors: list[str] = []
        for strategy in (self._list_from_cli_json, self._list_from_instance):
            try:
                return strategy()
            except ModuleSourceError as error:
                errors.append(str(error))
        raise ModuleSourceError(i18n.t("cli.tui.common.error_separator").join(errors))

    def list_available(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_available`。

        ``module available`` 自己就区分了已装与未装，因此这里不做二次过滤，全部交给界面按
        ``state`` 展示；该命令需要实例上下文（registry 来源写在实例配置里），故必带实例目录。
        """
        self.calls["available"] += 1
        argv = self.cli_argv("module", "available", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise ModuleSourceError(
                i18n.t(
                    "cli.tui.modules.src_exit_code",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return normalize_records(self._parse_json(completed.stdout, "module available --json"))

    def install(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.install`。"""
        self.calls["install"] += 1
        name = record.dist or record.name
        return self._run_cli(("module", "add", name), i18n.t("cli.tui.modules.label_install", name=name))

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.uninstall`。"""
        self.calls["uninstall"] += 1
        name = record.dist or record.name
        return self._run_cli(("module", "remove", name), i18n.t("cli.tui.modules.label_uninstall", name=name))

    async def stream_operation(
        self, kind: str, record: ModuleRecord, on_line: Callable[[str], None]
    ) -> OperationResult:
        """见 :meth:`ModuleSource.stream_operation`。

        安装要解析依赖、下载 wheel、写 venv，可能跑上几分钟；沿用 ``subprocess.run`` 时这段时间
        界面只能空转。改为异步起进程并逐行读输出，界面据此显示进度。
        """
        self.calls["install" if kind == "install" else "uninstall"] += 1
        name = record.dist or record.name
        subcommand = "add" if kind == "install" else "remove"
        argv = self.cli_argv("module", subcommand, name)
        label = i18n.t(f"cli.tui.modules.label_{kind}", name=name)
        try:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(self.root),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_exe_missing", path=argv[0], error=error)) from error
        except OSError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_oserror", cmd=" ".join(argv), error=error)) from error
        tail: deque[str] = deque(maxlen=_STREAM_TAIL_LINES)
        try:
            returncode = await asyncio.wait_for(self._pump(process, on_line, tail), timeout=self.timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            raise ModuleSourceError(
                i18n.t("cli.tui.modules.src_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from None
        detail = "\n".join(tail)
        if returncode != 0:
            return OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                self._tail(detail) or i18n.t("cli.tui.common.no_output"),
            )
        return OperationResult(True, i18n.t("cli.tui.modules.operation_done", label=label), detail)

    @staticmethod
    async def _pump(process: asyncio.subprocess.Process, on_line: Callable[[str], None], tail: deque[str]) -> int:
        stream = process.stdout
        if stream is not None:
            async for raw in stream:
                line = raw.decode("utf-8", errors="replace").rstrip()
                if not line:
                    continue
                tail.append(line)
                on_line(line)
        return await process.wait()

    def cli_argv(self, *args: str) -> list[str]:
        """构造调用本 CLI 的 argv。

        冻结产物（Nuitka onefile）里 ``sys.executable`` 就是 CLI 本体，不能再加 ``-m``；
        可用环境变量 ``AKARIBOT_CLI_BIN`` 显式指定 CLI 入口。

        :param args: 子命令及其参数。
        :return: 可直接交给 :mod:`subprocess` 的参数列表。
        """
        override = os.environ.get(_CLI_ENV_BIN)
        if override:
            return [override, *args]
        frozen = bool(getattr(sys, "frozen", False)) or hasattr(sys, "__compiled__")
        if frozen:
            return [sys.executable, *args]
        return [sys.executable, "-m", "akaribot.cli.main", *args]

    def _env(self) -> dict[str, str]:
        # 理由：子进程输出含中文与 JSON，Windows 控制台默认代码页可能是 GBK，
        # 读写编码不一致会得到乱码或解析失败，故两侧都显式声明 UTF-8。
        env = dict(os.environ)
        env["AKARI_INSTANCE_DIR"] = str(self.root)
        env["PYTHONIOENCODING"] = "utf-8"
        return env

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
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise ModuleSourceError(
                i18n.t("cli.tui.modules.src_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from error
        except OSError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_oserror", cmd=" ".join(argv), error=error)) from error

    def _list_from_cli_json(self) -> list[ModuleRecord]:
        argv = self.cli_argv("module", "list", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise ModuleSourceError(
                i18n.t(
                    "cli.tui.modules.src_exit_code",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return normalize_records(self._parse_json(completed.stdout, "module list --json"))

    def _list_from_instance(self) -> list[ModuleRecord]:
        instance = self._instance()
        installed = getattr(instance, "installed", None)
        if not callable(installed):
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_no_installed"))
        try:
            payload = installed()
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的错误
            raise ModuleSourceError(
                i18n.t("cli.tui.modules.src_installed_failed", kind=type(error).__name__, error=error)
            ) from error
        return normalize_records(payload)

    def _instance(self) -> Any:
        if self._instance_factory is not None:
            return self._instance_factory()
        try:
            from akaribot.cli.instance import Instance, find_instance_root
        except ImportError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_instance_missing")) from error
        try:
            root = find_instance_root(self.root)
            if root is None:
                raise ModuleSourceError(i18n.t("cli.tui.modules.src_not_instance", root=self.root))
            return Instance(root)
        except ModuleSourceError:
            raise
        except Exception as error:  # noqa: BLE001 - 实例构造失败同样只作为降级原因上报
            raise ModuleSourceError(
                i18n.t("cli.tui.modules.src_instance_failed", kind=type(error).__name__, error=error)
            ) from error

    def _run_cli(self, args: Sequence[str], label: str) -> OperationResult:
        argv = self.cli_argv(*args)
        completed = self._run(argv)
        if completed.returncode == 0:
            return OperationResult(True, i18n.t("cli.tui.common.op_ok", label=label), self._tail(completed.stdout))
        return OperationResult(
            False,
            i18n.t("cli.tui.common.op_failed", label=label, code=completed.returncode),
            self._tail(completed.stderr),
        )

    def _parse_json(self, stdout: str, label: str) -> Any:
        text = stdout.strip()
        if not text:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_empty_output", label=label))
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_bad_json", label=label, error=error)) from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        cleaned = (text or "").strip()
        return cleaned[-limit:]


class ModulesPage(compat.Vertical):
    """Modules 页控件。

    :param source: 数据源，缺省为 :class:`SubprocessModuleSource`。
    :param cache_ttl: 缓存有效期秒数；安装/卸载成功后立即失效，与有效期无关。
    """

    # 页面键位由页面自己声明：注册在 App 上会作用于隐藏页（停在配置页按 u 曾会卸载模块）。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.modules.action_refresh")),
        ("slash", "focus_search", i18n.t("cli.tui.modules.bind_search")),
        ("i", "install", i18n.t("cli.tui.modules.action_install")),
        ("u", "uninstall", i18n.t("cli.tui.modules.action_uninstall")),
        ("escape", "clear_search", i18n.t("cli.tui.modules.bind_clear_search")),
    )

    can_focus = True

    DEFAULT_CSS = """
    ModulesPage {
        layout: vertical;
        height: 1fr;
    }
    ModulesPage #search-row {
        height: 3;
    }
    ModulesPage #search {
        width: 1fr;
    }
    ModulesPage #installed-only {
        width: auto;
        padding: 1 0 0 1;
    }
    ModulesPage #count {
        width: auto;
        padding: 1 1 0 1;
        color: $text-muted;
    }
    ModulesPage #body {
        height: 1fr;
    }
    ModulesPage #module-list {
        width: 40%;
        min-width: 24;
        border: round $primary;
    }
    ModulesPage #module-list > ListItem {
        padding: 0 1;
    }
    ModulesPage #module-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    ModulesPage #detail-pane {
        width: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    ModulesPage #detail {
        width: 1fr;
    }
    ModulesPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    ModulesPage #progress {
        height: 1;
    }
    ModulesPage #status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(
        self,
        source: ModuleSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: ModuleSource = source if source is not None else SubprocessModuleSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._records: tuple[ModuleRecord, ...] = ()
        self._loaded_at: float = 0.0
        self._query: str = ""
        self._selected_key: str | None = None
        self._busy: bool = False
        self._installed_only: bool = False
        self._available_error: str = ""
        self._stream_line: str = ""
        self._stream_lines: list[str] = []
        self._detail_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._rendered_rows: tuple[str, ...] = ()

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.modules.search_placeholder"), id="search")
            yield compat.Checkbox(i18n.t("cli.tui.modules.installed_only"), id="installed-only")
            yield compat.Static(i18n.t("cli.tui.modules.status_pending"), id="count")
        with compat.Horizontal(id="body"):
            yield compat.ListView(id="module-list")
            with compat.VerticalScroll(id="detail-pane"):
                yield compat.Static(i18n.t("cli.tui.modules.detail_placeholder"), id="detail", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.modules.action_install"), id="install", variant="primary")
            yield compat.Button(i18n.t("cli.tui.modules.action_uninstall"), id="uninstall", variant="error")
            yield compat.Button(i18n.t("cli.tui.modules.action_refresh"), id="refresh")
        yield compat.ProgressBar(total=100.0, show_eta=False, id="progress")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；取数推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取模块列表。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_records()

    # region 状态读取（供测试与 App 使用）

    @property
    def records(self) -> tuple[ModuleRecord, ...]:
        """返回缓存中的全部记录，不触发子进程。"""
        return self._records

    @property
    def visible_records(self) -> tuple[ModuleRecord, ...]:
        """返回应用当前搜索词后的记录。"""
        if not self._query.strip():
            return self._records
        return tuple(record for record in self._records if record.matches(self._query))

    @property
    def selected_record(self) -> ModuleRecord | None:
        """返回列表当前高亮项对应的记录。"""
        records = self.visible_records
        if not records:
            return None
        try:
            list_view = self.query_one("#module-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(records):
            return None
        return records[index]

    @property
    def query(self) -> str:
        """返回当前搜索词。"""
        return self._query

    @property
    def detail_text(self) -> str:
        """返回详情面板当前渲染出的纯文本。"""
        return self._detail_rendered

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def stream_lines(self) -> tuple[str, ...]:
        """返回最近一次安装或卸载收到的子进程输出行。

        状态栏只留最后一行，操作结束后又会被结论覆盖；完整序列留在这里，供失败排查与自动化断言。
        """
        return tuple(self._stream_lines)

    def cache_age(self) -> float:
        """返回缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    # endregion

    # region 数据读取

    def refresh_records(self, *, force: bool = False) -> None:
        """读取模块列表。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不取数。
        """
        if not force and self._records and self.cache_age() < self.cache_ttl:
            age = self.cache_age()
            self._render_list()
            self._set_status(i18n.t("cli.tui.modules.status_cached", age=f"{age:.1f}", count=len(self._records)))
            return
        self._set_status(i18n.t("cli.tui.modules.status_loading"))
        self.run_worker(self._load_records(), group="modules-load", exclusive=True)

    async def _load_records(self) -> bool:
        try:
            records = await asyncio.to_thread(self.source.list_modules)
        except ModuleSourceError as error:
            self._records = ()
            self._loaded_at = time.monotonic()
            self.last_error = str(error)
            self._render_list()
            self._set_status(i18n.t("cli.tui.modules.status_load_failed", error=error))
            return False
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._records = ()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_list()
            self._set_status(i18n.t("cli.tui.modules.status_load_failed", error=self.last_error))
            return False
        # 默认展示全部：已装与未装同列，用户不必先知道名字再搜索。开关只用于收窄到已装。
        if not self._installed_only:
            records = await self._merge_available(records)
        self._records = tuple(sorted(records, key=sort_key))
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = i18n.t("cli.tui.modules.status_loaded", count=len(self._records))
        if self._available_error:
            self.last_result = f"{self.last_result}{self._available_error}"
        self._render_list()
        self._set_status(self.last_result)
        return True

    async def _merge_available(self, installed: Sequence[ModuleRecord]) -> list[ModuleRecord]:
        # 以分发名为键去重：两边都有的项保留已装那条（它带着本地版本与依赖信息），只把尚未安装的
        # 项补进来。取不到可安装集合时保留已装列表并记下原因，不让一次子进程失败清空整页。
        self._available_error = ""
        try:
            available = await asyncio.to_thread(self.source.list_available)
        except ModuleSourceError as error:
            self._available_error = i18n.t("cli.tui.modules.available_failed", error=error)
            return list(installed)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._available_error = i18n.t("cli.tui.modules.available_failed", error=f"{type(error).__name__}: {error}")
            return list(installed)
        known = {record.dist for record in installed}
        merged = list(installed)
        merged.extend(record for record in available if record.dist not in known)
        return merged

    def invalidate_cache(self) -> None:
        """使缓存立即失效，下一次读取必定走数据源。"""
        self._loaded_at = 0.0
        self._records = ()

    # endregion

    # region 渲染（只读缓存）

    def _render_list(self) -> None:
        records = self.visible_records
        list_view = self.query_one("#module-list", compat.ListView)
        inner_width = self._list_inner_width(list_view)
        name_width = self._name_column_width(inner_width)
        version_width = self._version_column_width()
        rows = [self._row_text(record, name_width, version_width, inner_width) for record in records]
        list_view.clear()
        items = [compat.ListItem(compat.Static(row, markup=False)) for row in rows]
        if items:
            list_view.extend(items)
        list_view.index = self._index_for_key(records)
        self._rendered_rows = tuple(rows)
        self._sync_count(records)
        self._sync_detail()
        self._sync_actions()

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的列表行文本，供自动化断言核对宽度。"""
        return self._rendered_rows

    def _list_inner_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 36
        return max(outer - 4, 8)

    def _name_column_width(self, inner_width: int) -> int:
        longest = compat.column_width(record.name for record in self._records)
        return max(min(max(longest, 6), 20, inner_width - 14), 4)

    def _version_column_width(self) -> int:
        longest = compat.column_width(record.version or "-" for record in self._records)
        return min(max(longest, 5), 8)

    def _row_text(self, record: ModuleRecord, name_width: int, version_width: int, inner_width: int) -> str:
        marker = "●" if record.installed else "○"
        version = compat.fit_cells(record.version or "-", version_width)
        fixed = compat.display_width(marker) + 2 + version_width
        summary_width = inner_width - fixed - name_width - 1
        if summary_width < 6:
            name_width = max(inner_width - fixed, 4)
            return f"{marker} {compat.fit_cells(record.name, name_width)} {version}".rstrip()
        name = compat.fit_cells(record.name, name_width)
        summary = compat.truncate_cells(record.summary, summary_width)
        return f"{marker} {name} {version} {summary}".rstrip()

    def _index_for_key(self, records: Sequence[ModuleRecord]) -> int:
        if not records:
            return 0
        if self._selected_key is not None:
            for index, record in enumerate(records):
                if record.dist == self._selected_key:
                    return index
        return 0

    def _sync_count(self, records: Sequence[ModuleRecord]) -> None:
        installed = sum(1 for record in self._records if record.installed)
        text = i18n.t(
            "cli.tui.modules.count",
            shown=len(records),
            total=len(self._records),
            installed=installed,
        )
        self.query_one("#count", compat.Static).update(compat.plain_text(text))

    def _sync_detail(self) -> None:
        record = self.selected_record
        if record is None:
            if not self._records:
                hint = i18n.t("cli.tui.modules.hint_empty")
            elif not self.visible_records:
                hint = i18n.t("cli.tui.modules.hint_no_match")
            else:
                hint = i18n.t("cli.tui.modules.hint_select")
            self._detail_rendered = hint
            self.query_one("#detail", compat.Static).update(compat.plain_text(hint))
            return
        self._selected_key = record.dist
        rows = [
            (i18n.t("cli.tui.modules.field_name"), record.name),
            (i18n.t("cli.tui.modules.field_dist"), record.dist),
            (i18n.t("cli.tui.modules.field_kind"), record.kind_label),
            (i18n.t("cli.tui.modules.field_version"), record.version or i18n.t("cli.tui.common.unknown")),
            (i18n.t("cli.tui.modules.field_state"), record.state_label),
            (i18n.t("cli.tui.modules.field_core_api"), record.requires_core_api or i18n.t("cli.tui.common.undeclared")),
            (i18n.t("cli.tui.modules.field_summary"), record.summary or i18n.t("cli.tui.common.none")),
        ]
        separator = i18n.t("cli.tui.common.list_separator")
        if record.provides_modules:
            rows.append((i18n.t("cli.tui.modules.field_provides"), separator.join(record.provides_modules)))
        if record.config_table:
            rows.append((i18n.t("cli.tui.modules.field_config_table"), record.config_table))
        if record.owned_tables:
            rows.append((i18n.t("cli.tui.modules.field_tables"), separator.join(record.owned_tables)))
        if record.dependents:
            rows.append(
                (
                    i18n.t("cli.tui.modules.field_dependents"),
                    i18n.t("cli.tui.common.list_separator").join(record.dependents),
                )
            )
        if record.origin:
            rows.append((i18n.t("cli.tui.modules.field_origin"), record.origin))
        lines = compat.align_rows(rows, gap=2)
        lines.append("")
        lines.append(i18n.t("cli.tui.modules.detail_keys"))
        text = "\n".join(lines)
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _sync_actions(self) -> None:
        install_target = self._install_target()
        uninstall_target = self._uninstall_target()
        self.query_one("#install", compat.Button).disabled = self._busy or install_target is None
        self.query_one("#uninstall", compat.Button).disabled = self._busy or uninstall_target is None

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        if self._records:
            self._render_list()

    # endregion

    # region 交互

    @compat.on(compat.Input.Changed, "#search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        self._query = event.value
        self._render_list()

    @compat.on(compat.Checkbox.Changed, "#installed-only")
    def _on_installed_only_changed(self, event: compat.Checkbox.Changed) -> None:
        self._installed_only = bool(event.value)
        self._selected_key = None
        self.refresh_records(force=True)

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.ListView.Selected)
    def _on_selected(self, event: compat.ListView.Selected) -> None:
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "install":
            self.request_install()
        elif button_id == "uninstall":
            self.request_uninstall()
        elif button_id == "refresh":
            self.refresh_records(force=True)

    def set_query(self, value: str) -> None:
        """设置搜索框内容，等价于用户键入。"""
        self.query_one("#search", compat.Input).value = value

    def focus_search(self) -> None:
        """把焦点移到搜索框。"""
        self.query_one("#search", compat.Input).focus()

    def clear_search(self) -> None:
        """清空搜索框；已为空时把焦点交给列表。"""
        search = self.query_one("#search", compat.Input)
        if search.value:
            search.value = ""
            return
        self.query_one("#module-list", compat.ListView).focus()

    def _install_target(self) -> ModuleRecord | None:
        record = self.selected_record
        if record is not None and not record.installed:
            return record
        candidate = self._query.strip()
        if _NAME_PATTERN.match(candidate) and (record is None or record.dist != candidate):
            return ModuleRecord(name=candidate, dist=candidate, state=STATE_AVAILABLE)
        return None

    def _uninstall_target(self) -> ModuleRecord | None:
        record = self.selected_record
        if record is not None and record.installed:
            return record
        return None

    def request_install(self) -> None:
        """发起安装；无目标时给出提示而不动作。"""
        target = self._install_target()
        if target is None:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.pick_install"),
                severity="warning",
                title=i18n.t("cli.tui.modules.action_install"),
            )
            return
        label = i18n.t("cli.tui.modules.label_install", name=target.dist)
        self._start_operation("install", label, target)

    def request_uninstall(self) -> None:
        """发起卸载；无目标时给出提示而不动作。"""
        target = self._uninstall_target()
        if target is None:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.pick_uninstall"),
                severity="warning",
                title=i18n.t("cli.tui.modules.action_uninstall"),
            )
            return
        label = i18n.t("cli.tui.modules.label_uninstall", name=target.dist)
        self._start_operation("uninstall", label, target)

    def _start_operation(self, kind: str, label: str, record: ModuleRecord) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._busy = True
        self._stream_line = ""
        self._stream_lines = []
        self._sync_actions()
        compat.progress_phase(self.query_one("#progress", compat.ProgressBar), 1.0, _PROGRESS_PHASES)
        self._set_status(i18n.t("cli.tui.modules.calling", label=label))
        self.run_worker(self._operate_streaming(kind, label, record), group="modules-op", exclusive=True)

    async def _operate_streaming(self, kind: str, label: str, record: ModuleRecord) -> None:
        # 安装期间子进程会打印 ``Resolved … / Installed …`` 这类进度行；把它们显示出来，操作者才能
        # 区分「正在装」与「卡住了」。状态栏只留最后一行，完整尾部在失败时作为详情给出。
        bar = self.query_one("#progress", compat.ProgressBar)
        try:
            result = await self.source.stream_operation(kind, record, self._on_operation_line)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(
                False,
                i18n.t("cli.tui.common.failed_label", label=label),
                f"{type(error).__name__}: {error}",
            )
        await self._finish_operation(label, record, result, bar)

    def _on_operation_line(self, line: str) -> None:
        # 回调由工作线程之外的异步读取循环调用，因此只写字段并直接刷新控件，不触发取数。
        self._stream_line = line
        self._stream_lines.append(line)
        self._set_status(line)

    async def _finish_operation(
        self, label: str, record: ModuleRecord, result: OperationResult, bar: compat.ProgressBar
    ) -> None:
        compat.progress_phase(bar, 3.0, _PROGRESS_PHASES)
        self._selected_key = record.dist
        if result.ok:
            self._set_status(i18n.t("cli.tui.modules.refreshing", message=result.message))
            self.invalidate_cache()
            await self._load_records()
            compat.progress_phase(bar, _PROGRESS_PHASES, _PROGRESS_PHASES)
            detail = (
                i18n.t("cli.tui.modules.detail_wrap", detail=result.detail.splitlines()[-1]) if result.detail else ""
            )
            self.last_result = f"{result.message}{detail}"
            self._set_status(self.last_result)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            detail = result.detail.splitlines()[-1] if result.detail else i18n.t("cli.tui.common.no_output")
            self._set_status(i18n.t("cli.tui.modules.failed_detail", message=result.message, detail=detail))
            compat.progress_reset(bar)
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def focus_primary(self) -> None:
        """把焦点交给列表；列表为空时退到搜索框。"""
        compat.focus_first(self, "#module-list", "#search")

    def action_refresh(self) -> None:
        """键位动作：强制重新读取列表。"""
        self.refresh_records(force=True)

    def action_focus_search(self) -> None:
        """键位动作：聚焦搜索框。"""
        self.focus_search()

    def action_install(self) -> None:
        """键位动作：安装当前目标。"""
        self.request_install()

    def action_uninstall(self) -> None:
        """键位动作：卸载当前目标。"""
        self.request_uninstall()

    def action_clear_search(self) -> None:
        """键位动作：清空搜索框。"""
        self.clear_search()

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
