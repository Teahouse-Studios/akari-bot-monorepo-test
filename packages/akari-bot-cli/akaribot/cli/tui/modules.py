"""模块页：模块浏览、搜索、安装、卸载与装载管理。

数据通过 :class:`ModuleSource` 读取，渲染与搜索使用页面缓存。
安装或卸载成功后重新加载列表。
"""

from __future__ import annotations

import asyncio
import json
import re
import subprocess
import time
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context

STATE_INSTALLED = "installed"
STATE_AVAILABLE = "available"
STATE_UNKNOWN = "unknown"

# 状态与包类型保存文案键，以便按当前语言解析标签。
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


_OPERATION_SUBCOMMANDS = {
    "install": "add",
    "uninstall": "remove",
    "update": "update",
    "load": "load",
    "unload": "unload",
}
# 界面确认后使用 ``--yes``，避免子进程等待重复的交互确认。
_OPERATION_EXTRA_ARGS = {"update": ("--yes",), "uninstall": ("--yes",)}
# 大批量卸载要求输入目标数量，以确认操作范围。
_UNINSTALL_COUNT_THRESHOLD = 10

_UNINSTALL_MODE_ARGS = {"purge": ("--purge-data",), "cascade": ("--cascade",)}

_UPDATE_SELECTED = "selected"
_UPDATE_ALL = "all"

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
    :param developers: 模块作者，取自包的 ``pyproject.toml``。
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
    developers: tuple[str, ...] = ()
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
    :param install_result: 安装返回值；默认为成功。
    :param uninstall_result: 卸载返回值；默认为成功。
    :param stream_lines: ``stream_operation`` 逐行上报的假输出。
    :param load_states: ``load_states`` 返回的模块装载状态。
    """

    def __init__(
        self,
        records: Sequence[ModuleRecord] = (),
        *,
        available: Sequence[ModuleRecord] = (),
        install_result: OperationResult | None = None,
        uninstall_result: OperationResult | None = None,
        stream_lines: Sequence[str] = (),
        load_states: Mapping[str, bool | None] | None = None,
    ) -> None:
        self._records = tuple(records)
        self._available = tuple(available)
        self._stream_lines = tuple(stream_lines)
        self._load_states: dict[str, bool | None] = dict(load_states or {})
        self._install_result = install_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_install_ok"), "stub"
        )
        self._uninstall_result = uninstall_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_uninstall_ok"), "stub"
        )
        self.calls = {"list": 0, "available": 0, "install": 0, "uninstall": 0, "update": 0, "status": 0}
        self.installed: list[str] = []
        self.uninstalled: list[str] = []
        self.loaded: dict[str, list[str]] = {}
        self.stream_calls: list[tuple[str, str, tuple[str, ...], bool]] = []

    def list_modules(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_modules`。"""
        self.calls["list"] += 1
        return self._records

    def list_available(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_available`。"""
        self.calls["available"] += 1
        return self._available

    def load_states(self) -> Mapping[str, bool | None]:
        """见 :meth:`ModuleSource.load_states`。"""
        self.calls["status"] += 1
        return dict(self._load_states)

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
        self,
        kind: str,
        record: ModuleRecord,
        on_line: Callable[[str], None],
        *,
        extra_args: Sequence[str] = (),
        positional: bool = True,
    ) -> OperationResult:
        """见 :meth:`ModuleSource.stream_operation`；替身直接回放固定输出。"""
        self.stream_calls.append((kind, record.dist or record.name, tuple(extra_args), positional))
        for line in self._stream_lines:
            on_line(line)
        if kind in ("load", "unload"):
            self.calls[kind] = self.calls.get(kind, 0) + 1
            self.loaded.setdefault(kind, []).append(record.dist or record.name)
            return self._install_result
        return self.install(record) if kind == "install" else self.uninstall(record)


@runtime_checkable
class ModuleSource(Protocol):
    """模块数据源接口；测试注入替身，实际运行通过子进程访问。"""

    def list_modules(self) -> Sequence[ModuleRecord]:
        """返回全部模块记录。"""

    def list_available(self) -> Sequence[ModuleRecord]:
        """返回可安装的模块记录，含尚未安装的项。"""

    def load_states(self) -> Mapping[str, bool | None]:
        """返回模块名到全局装载状态的映射；``None`` 表示尚无记录。"""

    def install(self, record: ModuleRecord) -> OperationResult:
        """安装给定记录。"""

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """卸载给定记录。"""

    async def stream_operation(
        self,
        kind: str,
        record: ModuleRecord,
        on_line: Callable[[str], None],
        *,
        extra_args: Sequence[str] = (),
        positional: bool = True,
    ) -> OperationResult:
        """执行安装或卸载，并把子进程输出逐行交给 ``on_line``。

        :param kind: ``install`` 或 ``uninstall``。
        :param record: 目标记录。
        :param on_line: 输出行回调，供界面显示进度。
        :param extra_args: 追加在目标名之后的 CLI 参数，如卸载的 ``--purge-data``。
        :param positional: 是否把记录的分发名作为位置参数；``False`` 表示目标完全由 ``extra_args``
            描述（git 与可编辑安装）。
        :return: 操作结果。
        """


def _operation_action(kind: str) -> str:
    # 安装、卸载、更新的动作名，用于批量汇总与通知标题。
    return i18n.t(f"cli.tui.modules.action_{kind}")


def _is_git_address(text: str) -> bool:
    # ``module add`` 只接受名字或 git 直引用：含协议头的输入一律按仓库地址交给 CLI 的 ``--git``。
    return text.startswith(("git+", "git@", "ssh://", "git://")) or "://" in text


def _split_git_address(text: str) -> tuple[str, str, str]:
    # 拆出地址中的 ref 与 subdirectory 片段，交给 CLI 的同名选项。末段中的 ``@`` 才是 ref
    # ``git@host`` 中的 ``@`` 属于 userinfo，解析规则与引擎一致。
    head, _, fragment = text.partition("#")
    subdir = ""
    for part in fragment.split("&"):
        field, _, value = part.partition("=")
        if field == "subdirectory":
            subdir = value
    if "@" in head.rpartition("/")[2]:
        head, _, ref = head.rpartition("@")
        return head, ref, subdir
    return head, "", subdir


def _git_install_args(text: str) -> tuple[str, ...]:
    address, ref, subdir = _split_git_address(text)
    args = ["--git", address]
    if ref:
        args += ["--ref", ref]
    if subdir:
        args += ["--subdir", subdir]
    return tuple(args)


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
        developers=_as_text_tuple(_pick(info, "developers", "authors", default=())),
        provides_modules=_as_text_tuple(_pick(info, "provides_modules", "modules", default=())),
        owned_tables=_as_text_tuple(_pick(info, "owned_tables", "tables", default=())),
        config_table=_text(_pick(info, "config_table", "config")),
    )


def normalize_records(payload: Any) -> list[ModuleRecord]:
    """把对端 JSON 归一化为记录列表并排序。

    接受三种形态：记录数组、以发行包名为键的映射、``{"modules": [...]}`` 之类的包装对象。
    记录默认视为已安装，与列表命令的输出范围一致。

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
    """通过 CLI 子进程读取模块数据；读取失败时使用实例清单。

    :param root: 实例根目录，默认当前工作目录。
    :param timeout: 单个子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: ``Instance`` 的构造回调，供测试注入替身。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        instance_factory: Callable[[], Any] | None = None,
    ) -> None:
        # 每次读取时解析实例根，确保切换实例后子进程使用当前实例。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"list": 0, "available": 0, "install": 0, "uninstall": 0}
        self._runner = runner or subprocess.run
        self._instance_factory = instance_factory

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

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
        """返回当前实例软件源中的可安装模块及安装状态。"""
        self.calls["available"] += 1
        # 适配器由独立页面管理，模块页仅查询模块。
        argv = self.cli_argv("module", "available", "--json", "--kind", "module")
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
        self,
        kind: str,
        record: ModuleRecord,
        on_line: Callable[[str], None],
        *,
        extra_args: Sequence[str] = (),
        positional: bool = True,
    ) -> OperationResult:
        """执行模块操作，并通过异步读取子进程输出报告进度。"""
        self.calls[kind if kind in self.calls else "install"] += 1
        name = record.dist or record.name
        subcommand = _OPERATION_SUBCOMMANDS[kind]
        target = (name,) if name and positional else ()
        argv = self.cli_argv("module", subcommand, *target, *extra_args, *_OPERATION_EXTRA_ARGS.get(kind, ()))
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
        """构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。"""
        return cli_process.cli_argv(*args)

    def _env(self) -> dict[str, str]:
        return cli_process.cli_env(self.root)

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

    def load_states(self) -> Mapping[str, bool | None]:
        """通过 ``module status --json`` 读取装载状态；实例未运行时仍可读取已有记录。"""
        self.calls["status"] = self.calls.get("status", 0) + 1
        argv = self.cli_argv("module", "status", "--json")
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
        payload = self._parse_json(completed.stdout, "module status --json")
        items = payload.get("modules") if isinstance(payload, Mapping) else payload
        if not isinstance(items, Sequence) or isinstance(items, str | bytes):
            raise ModuleSourceError(i18n.t("cli.tui.modules.src_bad_status", label="module status --json"))
        states: dict[str, bool | None] = {}
        for item in items:
            if not isinstance(item, Mapping):
                continue
            name = item.get("name")
            if not name:
                continue
            loaded = item.get("loaded")
            states[str(name)] = None if loaded is None else bool(loaded)
        return states

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


@dataclass(frozen=True)
class ModuleLayout:
    """模块列表的列宽计划。

    :param name_width: 名称列宽。
    :param version_width: 版本列宽。
    :param load_width: 装载列宽；``0`` 表示本屏没有这一列。
    :param show_summary: 是否显示简介列。
    """

    name_width: int
    version_width: int
    load_width: int
    show_summary: bool


class ModulesPage(compat.Vertical):
    """模块页控件。

    :param source: 数据源，默认为 :class:`SubprocessModuleSource`。
    :param cache_ttl: 缓存有效期秒数；安装/卸载成功后立即失效，与有效期无关。
    """

    # 页面键位仅在本页生效，避免隐藏页响应操作；低频键位由详情区提示以控制页脚宽度。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.modules.action_refresh")),
        ("slash", "focus_search", i18n.t("cli.tui.modules.bind_search")),
        ("i", "install", i18n.t("cli.tui.modules.action_install")),
        ("u", "uninstall", i18n.t("cli.tui.modules.action_uninstall"), False),
        ("U", "update", i18n.t("cli.tui.modules.action_update"), False),
        ("ctrl+u", "update", i18n.t("cli.tui.modules.action_update"), False),
        ("l", "toggle_load", i18n.t("cli.tui.modules.bind_load"), False),
        ("space", "toggle_select", i18n.t("cli.tui.modules.bind_toggle_select")),
        ("ctrl+space", "toggle_select", i18n.t("cli.tui.modules.bind_toggle_select"), False),
        ("shift+up", "extend_up", i18n.t("cli.tui.modules.bind_extend"), False),
        ("shift+down", "extend_down", i18n.t("cli.tui.modules.bind_extend"), False),
        ("a", "select_all", i18n.t("cli.tui.modules.bind_select_all"), False),
        ("ctrl+a", "select_all", i18n.t("cli.tui.modules.bind_select_all"), False),
        ("c", "clear_selection", i18n.t("cli.tui.modules.bind_clear_selection"), False),
        ("escape", "clear_search", i18n.t("cli.tui.modules.bind_clear_search"), False),
    )

    can_focus = True

    DEFAULT_CSS = """
    ModulesPage {
        layout: vertical;
        height: 1fr;
    }
    ModulesPage #search-row {
        height: 3;
        align-vertical: middle;
    }
    ModulesPage #search {
        width: 1fr;
        min-width: 16;
    }
    ModulesPage #installed-only {
        width: auto;
        margin: 0 0 0 1;
    }
    ModulesPage #count {
        width: 1fr;
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    ModulesPage #body {
        height: 1fr;
    }
    ModulesPage #list-pane {
        width: 40%;
        min-width: 24;
    }
    ModulesPage #columns {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    ModulesPage #module-list {
        height: 1fr;
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
        height: auto;
        padding: 0 0 0 1;
    }
    ModulesPage #actions Button {
        min-width: 0;
    }
    ModulesPage #progress {
        height: 1;
    }
    ModulesPage #status {
        height: 1;
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
        # 多选：按分发名记录选区，刷新后只保留仍然存在的项；_anchor 是 Shift 扩选的起点。
        self._selected: set[str] = set()
        self._anchor: str | None = None
        # 确认框使用防抖，避免鼠标双击或键盘连发产生重复弹窗。
        self._confirm = compat.PendingConfirm()
        self._available_error: str = ""
        self._load_states: dict[str, bool | None] = {}
        self._load_error: str = ""
        self._stream_line: str = ""
        self._stream_lines: list[str] = []
        self._detail_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._rendered_rows: tuple[str, ...] = ()
        self._columns_rendered: str = ""

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.modules.search_placeholder"), id="search")
            yield compat.Checkbox(i18n.t("cli.tui.modules.installed_only"), id="installed-only")
        yield compat.Static(i18n.t("cli.tui.modules.status_pending"), id="count", markup=False)
        with compat.Horizontal(id="body"):
            with compat.Vertical(id="list-pane"):
                yield compat.Static("", id="columns", markup=False)
                yield compat.ListView(id="module-list")
            with compat.VerticalScroll(id="detail-pane"):
                yield compat.Static(i18n.t("cli.tui.modules.detail_placeholder"), id="detail", markup=False)
        yield compat.ButtonFlow(
            ("install", i18n.t("cli.tui.modules.action_install"), "primary"),
            ("uninstall", i18n.t("cli.tui.modules.action_uninstall"), "error"),
            ("update", i18n.t("cli.tui.modules.action_update")),
            ("toggle-load", i18n.t("cli.tui.modules.button_load")),
            ("refresh", i18n.t("cli.tui.modules.action_refresh")),
            id="actions",
        )
        yield compat.ProgressBar(total=100.0, show_eta=False, id="progress")
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；读取数据推迟到首次显示。"""
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
    def search_query(self) -> str:
        """返回当前搜索词。"""
        # 名称需避免覆盖 Textual 的 Widget.query()。
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
        """返回最近一次模块操作的子进程输出，供故障排查与自动化验证。"""
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

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不读取数据。
        """
        # 刷新可能改变目标集合，必须清除待确认状态。
        self._confirm.reset()
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
        # 适配器由独立页面管理；保留类型未知的记录，避免隐藏可管理的包。
        records = [record for record in records if record.kind != "adapter"]
        if not self._installed_only:
            records = await self._merge_available(records)
        await self._load_module_states()
        self._records = tuple(sorted(records, key=sort_key))
        # 清除刷新后不存在的选中项，避免批量操作包含不可见的包。
        known = {record.dist for record in self._records}
        self._selected &= known
        if self._anchor not in known:
            self._anchor = None
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = i18n.t("cli.tui.modules.status_loaded", count=len(self._records))
        if self._available_error:
            self.last_result = f"{self.last_result}{self._available_error}"
        if self._load_error:
            self.last_result = f"{self.last_result}{self._load_error}"
        self._render_list()
        self._set_status(self.last_result)
        # 列表加载后恢复列表焦点，仅在焦点仍位于页面容器时执行，避免中断搜索输入。
        if self.display and self.app.focused is self:
            self.focus_primary()
        return True

    async def _load_module_states(self) -> None:
        # 装载状态表可能不存在，读取失败时仍展示安装列表。
        try:
            states = await asyncio.to_thread(self.source.load_states)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都只降级
            self._load_states = {}
            self._load_error = i18n.t("cli.tui.modules.status_load_unavailable", error=error)
            return
        self._load_states = dict(states)
        self._load_error = ""

    def load_state_text(self, record: ModuleRecord) -> str:
        """返回某条记录的装载状态文本，供列表与详情展示。"""
        modules = [name for name in record.provides_modules if name in self._load_states]
        if not modules:
            return i18n.t("cli.tui.modules.load_cell_unknown")
        loaded = sum(1 for name in modules if self._load_states.get(name) is True)
        return i18n.t("cli.tui.modules.load_cell", loaded=loaded, total=len(modules))

    async def _merge_available(self, installed: Sequence[ModuleRecord]) -> list[ModuleRecord]:
        # 已安装记录包含本地版本与依赖信息，合并时优先保留；软件源读取失败不影响已安装列表。
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
        # 数据源返回的适配器记录不参与模块列表合并。
        merged.extend(record for record in available if record.dist not in known and record.kind != "adapter")
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
        layout = self._layout(inner_width)
        rows = [self._row_text(record, layout, inner_width) for record in records]
        self._render_columns(layout, inner_width)
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

    def column_text(self) -> str:
        """返回最近一次渲染出的表头文本。"""
        return self._columns_rendered

    def _render_columns(self, layout: ModuleLayout, inner_width: int) -> None:
        # 表头与数据行共用列宽计划，确保隐藏列后仍保持对齐。
        cells = [
            f"{' ' * 4}{compat.fit_cells(i18n.t('cli.tui.modules.column_name'), layout.name_width)}",
            compat.fit_cells(i18n.t("cli.tui.modules.column_version"), layout.version_width),
        ]
        if layout.load_width:
            cells.append(compat.fit_cells(i18n.t("cli.tui.modules.column_load"), layout.load_width))
        text = " ".join(cells)
        if layout.show_summary:
            text = f"{text} {i18n.t('cli.tui.modules.column_summary')}"
        text = compat.truncate_cells(text, inner_width).rstrip()
        self._columns_rendered = text
        self.query_one("#columns", compat.Static).update(compat.plain_text(text))

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

    def _load_column_width(self) -> int:
        # 仅已安装且声明模块的包具有装载状态。
        texts = [self.load_state_text(record) for record in self._records if self._has_load_column(record)]
        return max((compat.display_width(text) for text in texts), default=0)

    def _layout(self, inner_width: int) -> ModuleLayout:
        # 空间不足时隐藏简介列，优先保证名称可读。
        name_width = self._name_column_width(inner_width)
        version_width = self._version_column_width()
        load_width = self._load_column_width()
        fixed = 4 + version_width + (load_width + 1 if load_width else 0) + 1
        show_summary = inner_width - fixed - name_width - 1 >= 6
        if not show_summary:
            name_width = max(inner_width - fixed, 4)
        # 装载列不足 4 列时隐藏该列，避免显示无法识别的截断状态。
        budget = inner_width - 6 - name_width - version_width
        if load_width and budget < load_width:
            load_width = budget if budget >= 4 else 0
        return ModuleLayout(name_width, version_width, load_width, show_summary)

    @staticmethod
    def _has_load_column(record: ModuleRecord) -> bool:
        return record.installed and bool(record.provides_modules)

    def _row_text(self, record: ModuleRecord, layout: ModuleLayout, inner_width: int) -> str:
        # 首列是选中位：高亮条只表示光标所在，选中集合才是批量操作的操作对象。
        marked = "✓" if record.dist in self._selected else " "
        marker = "●" if record.installed else "○"
        version = compat.fit_cells(record.version or "-", layout.version_width)
        load = self.load_state_text(record) if self._has_load_column(record) else ""
        load_cell = f" {compat.fit_cells(load, layout.load_width)}" if layout.load_width else ""
        name = compat.fit_cells(record.name, layout.name_width)
        row = f"{marked} {marker} {name} {version}{load_cell}"
        if not layout.show_summary:
            return row.rstrip()
        summary_width = inner_width - compat.display_width(row) - 1
        return f"{row} {compat.truncate_cells(record.summary, summary_width)}".rstrip()

    def _load_detail(self, record: ModuleRecord) -> str:
        separator = i18n.t("cli.tui.common.list_separator")
        parts = []
        for name in record.provides_modules:
            if name not in self._load_states:
                parts.append(f"{name}={i18n.t('cli.tui.common.unknown')}")
            elif self._load_states[name]:
                parts.append(f"{name}={i18n.t('cli.module.status.state_loaded')}")
            else:
                parts.append(f"{name}={i18n.t('cli.module.status.state_unloaded')}")
        text = separator.join(parts) or i18n.t("cli.tui.common.none")
        return text if self._load_states else i18n.t("cli.tui.modules.load_state_hint")

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
        if self._selected:
            text = f"{text}{i18n.t('cli.common.clause_separator')}{i18n.t('cli.tui.modules.count_selected', count=len(self._selected))}"
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
        if record.developers:
            rows.append((i18n.t("cli.tui.modules.field_developers"), separator.join(record.developers)))
        if record.provides_modules:
            rows.append((i18n.t("cli.tui.modules.field_provides"), separator.join(record.provides_modules)))
            rows.append((i18n.t("cli.tui.modules.field_load"), self._load_detail(record)))
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
        uninstall_target = self._uninstall_target()
        # 安装按钮允许输入新的目标，不受当前选中包的安装状态限制。
        self.query_one("#install", compat.Button).disabled = self._busy
        self.query_one("#uninstall", compat.Button).disabled = self._busy or uninstall_target is None
        # 更新始终可用：全量更新不依赖光标与选区。
        self.query_one("#update", compat.Button).disabled = self._busy
        self.query_one("#toggle-load", compat.Button).disabled = self._busy or not self._load_targets()

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新读取数据。"""
        if self._records:
            self._render_list()

    # endregion

    # region 交互

    @compat.on(compat.Input.Changed, "#search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        self._confirm.reset()
        self._query = event.value
        self._render_list()

    @compat.on(compat.Checkbox.Changed, "#installed-only")
    def _on_installed_only_changed(self, event: compat.Checkbox.Changed) -> None:
        self._installed_only = bool(event.value)
        self._selected_key = None
        self.refresh_records(force=True)

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        # 待确认的卸载操作必须与当前高亮目标一致。
        self._confirm.reset()
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
        elif button_id == "update":
            self.request_update()
        elif button_id == "toggle-load":
            self.request_toggle_load()
        elif button_id == "refresh":
            self.refresh_records(force=True)

    def set_query(self, value: str) -> None:
        """设置搜索框内容，等价于用户键入。"""
        self.query_one("#search", compat.Input).value = value

    def focus_search(self) -> None:
        """把焦点移到搜索框。"""
        self.query_one("#search", compat.Input).focus()

    def clear_search(self) -> None:
        """清空搜索框；已为空时聚焦列表。"""
        search = self.query_one("#search", compat.Input)
        if search.value:
            search.value = ""
            return
        self.query_one("#module-list", compat.ListView).focus()

    def _install_target(self) -> ModuleRecord | None:
        # 未安装的高亮项可直接作为目标；其他情况使用搜索词预填安装输入框。
        record = self.selected_record
        if record is not None and not record.installed:
            return record
        return None

    def _install_prefill(self) -> str:

        candidate = self._query.strip()
        return candidate if _NAME_PATTERN.match(candidate) else ""

    def _uninstall_target(self) -> ModuleRecord | None:
        record = self.selected_record
        if record is not None and record.installed:
            return record
        return None

    def request_install(self) -> None:
        """安装选区或未安装的高亮项；无可安装目标时打开安装输入框。"""
        targets = self._batch_targets("install")
        if targets:
            self._start_operation("install", targets)
            return
        if self._selected:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.pick_install"),
                severity="warning",
                title=i18n.t("cli.tui.modules.action_install"),
            )
            return
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.modules.install_title"),
            hint=i18n.t("cli.tui.modules.install_hint"),
            placeholder=i18n.t("cli.tui.modules.install_placeholder"),
            initial=self._install_prefill(),
            confirm_label=i18n.t("cli.tui.modules.install_confirm"),
            cancel_label=i18n.t("cli.tui.modules.cancel"),
            callback=self.on_install_spec_entered,
        )

    def on_install_spec_entered(self, spec: str | None) -> None:
        """输入框回调：按输入内容给出可用的安装方式。

        :param spec: 用户输入的模块名、仓库地址或目录；取消时为 ``None``。
        """
        text = (spec or "").strip()
        if not text:
            self._set_status(i18n.t("cli.tui.modules.install_cancelled"))
            return
        options = self._install_options(text)
        if not options:
            self._set_status(i18n.t("cli.tui.modules.install_unknown_spec", spec=text))
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.modules.install_target_title", spec=text),
            hint=i18n.t("cli.tui.modules.install_target_hint"),
            options=options,
            cancel_label=i18n.t("cli.tui.modules.cancel"),
            callback=lambda mode: self.start_install(text, mode),
        )

    def _install_options(self, text: str) -> tuple[tuple[str, str], ...]:

        options: list[tuple[str, str]] = []
        if _NAME_PATTERN.match(text):
            options.append(("registry", i18n.t("cli.tui.modules.install_from_registry")))
        if _is_git_address(text):
            options.append(("git", i18n.t("cli.tui.modules.install_from_git")))
        if self._editable_path(text) is not None:
            options.append(("editable", i18n.t("cli.tui.modules.install_editable")))
        return tuple(options)

    def _editable_path(self, text: str) -> Path | None:
        # 子进程的 cwd 是实例根，相对路径按它解析才能与 CLI 的 -e 取到同一个目录。
        path = Path(text).expanduser()
        if not path.is_absolute():
            path = context.resolve_root() / path
        return path if path.is_dir() else None

    def start_install(self, spec: str, mode: str | None) -> None:
        """按选定的方式安装输入的名字、地址或目录。

        :param spec: 输入框中的内容。
        :param mode: ``registry`` / ``git`` / ``editable``；``None`` 表示取消。
        """
        extra: tuple[str, ...] = ()
        if mode == "git" and _is_git_address(spec):
            extra = _git_install_args(spec)
        elif mode == "editable":
            path = self._editable_path(spec)
            if path is None:
                self._set_status(i18n.t("cli.tui.modules.install_unknown_spec", spec=spec))
                return
            extra = ("-e", str(path))
        elif mode != "registry" or not _NAME_PATTERN.match(spec):
            self._set_status(i18n.t("cli.tui.modules.install_cancelled"))
            return
        # Git 与可编辑安装的目标由选项指定，记录仅提供状态栏中的名称。
        record = ModuleRecord(name=spec, dist=spec, state=STATE_AVAILABLE)
        self._start_operation("install", [record], extra_args=extra, positional=not extra)

    def request_update(self) -> None:
        """发起更新：弹出选择框决定更新选中项还是全部已安装包。"""
        targets = self._batch_targets("update")
        # 防抖用于避免鼠标双击或键盘连发产生重复确认框。
        if not self._confirm.accept(f"update:{','.join(record.dist for record in targets)}"):
            return
        options: list[tuple[str, str]] = []
        if targets:
            options.append((_UPDATE_SELECTED, i18n.t("cli.tui.modules.update_selected")))
        options.append((_UPDATE_ALL, i18n.t("cli.tui.modules.update_all")))
        hint = i18n.t("cli.tui.modules.update_hint")
        if not targets:
            hint = f"{hint}{i18n.t('cli.common.clause_separator')}{i18n.t('cli.tui.modules.update_no_target')}"
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.modules.action_update"),
            hint=hint,
            options=tuple(options),
            cancel_label=i18n.t("cli.tui.modules.cancel"),
            callback=lambda mode: self.start_update(targets, mode),
        )

    def start_update(self, targets: Sequence[ModuleRecord], mode: str | None) -> None:
        """按选定范围更新。

        :param targets: 选区（没有选区时为当前项）中的已安装包；为空表示只能全量更新。
        :param mode: ``selected`` / ``all``；``None`` 表示取消。
        """
        # 关闭确认框后清除防抖记录，允许重新发起操作。
        self._confirm.reset()
        if mode == _UPDATE_SELECTED and targets:
            self._start_operation("update", targets)
            return
        if mode != _UPDATE_ALL:
            self._set_status(i18n.t("cli.tui.modules.update_cancelled"))
            return
        name = i18n.t("cli.tui.modules.update_all_target")
        # 全量更新的目标名仅用于展示，实际目标由 CLI 的 ``--all`` 枚举。
        self._start_operation(
            "update",
            [ModuleRecord(name=name, dist=name, state=STATE_INSTALLED)],
            extra_args=("--all",),
            positional=False,
        )

    def request_uninstall(self) -> None:
        """发起卸载：弹出确认框选择数据与依赖的处置方式。

        大批量操作要求输入目标数量；清理配置与数据表另需输入确认文字。
        """
        targets = self._batch_targets("uninstall")
        if not targets:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.pick_uninstall"),
                severity="warning",
                title=i18n.t("cli.tui.modules.action_uninstall"),
            )
            return
        keys = tuple(record.dist for record in targets)
        if not self._confirm.accept(f"uninstall:{','.join(keys)}"):
            return
        if len(targets) > _UNINSTALL_COUNT_THRESHOLD:
            compat.ask_text(
                self.app,
                title=i18n.t("cli.tui.modules.uninstall_count_title", count=len(targets)),
                hint=i18n.t("cli.tui.modules.uninstall_count_hint", count=len(targets)),
                placeholder=i18n.t("cli.tui.modules.uninstall_count_placeholder"),
                confirm_label=i18n.t("cli.tui.modules.uninstall_count_confirm"),
                cancel_label=i18n.t("cli.tui.modules.cancel"),
                callback=lambda value: self.on_uninstall_count_entered(targets, value),
            )
            return
        self._open_uninstall_options(targets)

    def _uninstall_title(self, targets: Sequence[ModuleRecord]) -> str:
        if len(targets) == 1:
            return i18n.t("cli.tui.modules.uninstall_confirm_one", name=targets[0].dist)
        separator = i18n.t("cli.tui.common.list_separator")
        names = separator.join(record.dist for record in targets)
        return i18n.t("cli.tui.modules.uninstall_confirm_many", count=len(targets), names=names)

    def on_uninstall_count_entered(self, targets: Sequence[ModuleRecord], value: str | None) -> None:
        """数量输入回调：输入与目标数量一致才继续。

        :param targets: 待卸载的目标。
        :param value: 用户输入的数量；取消时为 ``None``。
        """
        self._confirm.reset()
        text = (value or "").strip()
        if not text:
            self._set_status(i18n.t("cli.tui.modules.uninstall_cancelled"))
            return
        if text != str(len(targets)):
            self._set_status(i18n.t("cli.tui.modules.uninstall_count_mismatch", given=text, count=len(targets)))
            return
        self._open_uninstall_options(targets)

    def _open_uninstall_options(self, targets: Sequence[ModuleRecord]) -> None:
        # 反向依赖由 CLI 回报；只有存在依赖时才提供级联卸载。
        options = [
            ("keep", i18n.t("cli.tui.modules.uninstall_keep_data")),
            ("purge", i18n.t("cli.tui.modules.uninstall_purge_data")),
        ]
        hint = i18n.t("cli.tui.modules.uninstall_options_hint")
        dependents = sorted({name for record in targets for name in record.dependents})
        if dependents:
            options.append(("cascade", i18n.t("cli.tui.modules.uninstall_cascade")))
            joined = i18n.t("cli.tui.common.list_separator").join(dependents)
            hint = f"{hint}{i18n.t('cli.common.clause_separator')}{i18n.t('cli.tui.modules.uninstall_cascade_hint', names=joined)}"
        compat.ask_choice(
            self.app,
            title=self._uninstall_title(targets),
            hint=hint,
            options=tuple(options),
            cancel_label=i18n.t("cli.tui.modules.cancel"),
            callback=lambda mode: self.start_uninstall(targets, mode),
        )

    def start_uninstall(self, targets: Sequence[ModuleRecord], mode: str | None) -> None:
        """按选定的处置方式卸载。

        :param targets: 目标记录。
        :param mode: ``keep`` / ``purge`` / ``cascade``；``None`` 表示取消。
        """
        self._confirm.reset()
        if mode != "keep" and mode not in _UNINSTALL_MODE_ARGS:
            self._set_status(i18n.t("cli.tui.modules.uninstall_cancelled"))
            return
        if mode == "purge":
            self._request_purge_confirmation(targets)
            return
        self._start_operation("uninstall", targets, extra_args=_UNINSTALL_MODE_ARGS.get(mode, ()))

    def _request_purge_confirmation(self, targets: Sequence[ModuleRecord]) -> None:
        separator = i18n.t("cli.tui.common.list_separator")
        token = (
            targets[0].dist if len(targets) == 1 else i18n.t("cli.tui.modules.purge_batch_token", count=len(targets))
        )
        files = sorted({f"config/{record.config_table}.toml" for record in targets if record.config_table})
        tables = sorted({table for record in targets for table in record.owned_tables})
        none = i18n.t("cli.tui.common.none")
        compat.ask_text(
            self.app,
            title=i18n.t("cli.tui.modules.purge_title", count=len(targets)),
            hint=i18n.t(
                "cli.tui.modules.purge_hint",
                names=separator.join(record.dist for record in targets),
                files=separator.join(files) or none,
                tables=separator.join(tables) or none,
                token=token,
            ),
            placeholder=i18n.t("cli.tui.modules.purge_placeholder"),
            confirm_label=i18n.t("cli.tui.modules.purge_confirm"),
            cancel_label=i18n.t("cli.tui.modules.cancel"),
            callback=lambda value: self._on_purge_confirmed(targets, token, value),
        )

    def _on_purge_confirmed(self, targets: Sequence[ModuleRecord], token: str, value: str | None) -> None:
        if value is None:
            self._set_status(i18n.t("cli.tui.modules.uninstall_cancelled"))
            return
        if value.strip() != token:
            self._set_status(i18n.t("cli.tui.modules.purge_mismatch"))
            return
        self._start_operation("uninstall", targets, extra_args=_UNINSTALL_MODE_ARGS["purge"])

    def request_toggle_load(self) -> None:
        """装载选中包的模块；全部已装载时取消装载。"""
        targets = self._load_targets()
        if not targets:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.pick_load"),
                severity="warning",
                title=i18n.t("cli.tui.modules.bind_load"),
            )
            return
        modules = [name for record in targets for name in record.provides_modules]
        states = [self._load_states.get(name) for name in modules]
        action = "load" if any(state is not True for state in states) else "unload"
        self._start_operation(action, [ModuleRecord(name=name, dist=name) for name in modules])

    def _load_targets(self) -> list[ModuleRecord]:
        # 装载仅适用于已安装且声明模块的包。
        records = [record for record in self._records if record.dist in self._selected] if self._selected else []
        if not records:
            current = self.selected_record
            records = [current] if current is not None else []
        return [record for record in records if record.installed and record.provides_modules]

    def _batch_targets(self, kind: str) -> list[ModuleRecord]:
        # 批量目标按安装状态筛选，避免对同一选区执行无效操作。
        if not self._selected:
            single = self._install_target() if kind == "install" else self._uninstall_target()
            return [single] if single is not None else []  # 更新与卸载同取已安装项
        wanted = [record for record in self._records if record.dist in self._selected]
        if kind == "install":
            return [record for record in wanted if not record.installed]
        # 卸载与更新都只作用于已安装项。
        return [record for record in wanted if record.installed]

    def action_toggle_select(self) -> None:
        """键位动作：切换当前项的选中状态（对应 Ctrl+点击）。"""
        record = self.selected_record
        if record is None:
            return
        self._anchor = record.dist
        if record.dist in self._selected:
            self._selected.discard(record.dist)
        else:
            self._selected.add(record.dist)
        self._render_list()

    def action_select_all(self) -> None:
        """键位动作：选中当前可见的全部（受搜索与筛选影响）。"""
        visible = self.visible_records
        if not visible:
            return
        self._selected.update(record.dist for record in visible)
        self._anchor = visible[0].dist
        self._render_list()

    def action_clear_selection(self) -> None:
        """键位动作：清空选区。"""
        # 清空选区时同步清除待确认状态。
        self._confirm.reset()
        if not self._selected:
            return
        self._selected.clear()
        self._anchor = None
        self._render_list()

    def action_extend_up(self) -> None:
        """键位动作：光标上移并扩展选区。"""
        self._move_cursor(-1, extend=True)

    def action_extend_down(self) -> None:
        """键位动作：光标下移并扩展选区。"""
        self._move_cursor(1, extend=True)

    def _move_cursor(self, step: int, *, extend: bool) -> None:
        # Shift 扩选替换上次范围，避免反向移动时保留已移出范围的记录。
        records = self.visible_records
        if not records:
            return
        list_view = self.query_one("#module-list", compat.ListView)
        current = compat.highlighted_index(list_view) or 0
        target = max(0, min(current + step, len(records) - 1))
        list_view.index = target
        if not extend:
            return
        if self._anchor is None:
            self._anchor = records[current].dist
        self._select_range(self._anchor, records[target].dist, records)
        # 重绘会按 _selected_key 恢复高亮项，需先同步当前目标。
        self._selected_key = records[target].dist
        self._render_list()

    def _select_range(self, anchor: str, focus: str, records: Sequence[ModuleRecord]) -> None:
        names = [record.dist for record in records]
        if anchor not in names or focus not in names:
            self._selected = {focus}
            return
        start, end = sorted((names.index(anchor), names.index(focus)))
        self._selected = set(names[start : end + 1])

    def on_click(self, event: compat.events.Click) -> None:
        """处理列表选择：普通点击单选，Ctrl 点击切换，Shift 点击扩选。"""
        # 点击事件由 ListItem 冒泡，需检查来源以排除列表外的控件。
        list_view = self.query_one("#module-list", compat.ListView)
        clicked = event.widget
        if clicked is None or list_view not in clicked.ancestors_with_self:
            return
        records = self.visible_records
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(records):
            return
        record = records[index]
        if event.shift and self._anchor is not None:
            self._select_range(self._anchor, record.dist, records)
        elif event.ctrl:
            self._anchor = record.dist
            if record.dist in self._selected:
                self._selected.discard(record.dist)
            else:
                self._selected.add(record.dist)
        else:
            self._anchor = record.dist
            self._selected = {record.dist}
        self._selected_key = record.dist
        self._render_list()

    def _start_operation(
        self,
        kind: str,
        targets: Sequence[ModuleRecord],
        *,
        extra_args: Sequence[str] = (),
        positional: bool = True,
    ) -> None:
        if self._busy:
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.busy"),
                severity="warning",
                title=i18n.t("cli.tui.common.busy_title"),
            )
            return
        self._confirm.reset()
        self._busy = True
        self._stream_line = ""
        self._stream_lines = []
        self._sync_actions()
        compat.progress_phase(self.query_one("#progress", compat.ProgressBar), 1.0, _PROGRESS_PHASES)
        first = targets[0]
        label = i18n.t(f"cli.tui.modules.label_{kind}", name=first.dist)
        if len(targets) > 1:
            label = i18n.t("cli.tui.modules.batch_label", count=len(targets), label=label)
        self._set_status(i18n.t("cli.tui.modules.calling", label=label))
        self.run_worker(
            self._operate_streaming(kind, targets, tuple(extra_args), positional),
            group="modules-op",
            exclusive=True,
        )

    async def _operate_streaming(
        self,
        kind: str,
        targets: Sequence[ModuleRecord],
        extra_args: Sequence[str],
        positional: bool,
    ) -> None:
        # 批量操作中单项失败不影响其余目标，失败结果在全部操作结束后汇总。
        bar = self.query_one("#progress", compat.ProgressBar)
        # 单项操作保留数据源的结果说明，批量操作统一汇总。
        succeeded: list[tuple[str, str]] = []
        failed: list[tuple[str, str]] = []
        total = len(targets)
        for index, record in enumerate(targets, 1):
            label = i18n.t(f"cli.tui.modules.label_{kind}", name=record.dist)
            if total > 1:
                self._set_status(i18n.t("cli.tui.modules.batch_progress", index=index, total=total, label=label))
            try:
                result = await self.source.stream_operation(
                    kind,
                    record,
                    self._on_operation_line,
                    extra_args=extra_args,
                    positional=positional,
                )
            except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
                result = OperationResult(
                    False,
                    i18n.t("cli.tui.common.failed_label", label=label),
                    f"{type(error).__name__}: {error}",
                )
            compat.progress_phase(bar, 1.0 + 2.0 * index / total, _PROGRESS_PHASES)
            if result.ok:
                succeeded.append((record.dist, result.message))
            else:
                failed.append((record.dist, result.detail or result.message))
        await self._finish_operation(kind, targets, succeeded, failed, bar)

    def _on_operation_line(self, line: str) -> None:
        # 回调由工作线程之外的异步读取循环调用，因此只写字段并直接刷新控件，不触发读取数据。
        self._stream_line = line
        self._stream_lines.append(line)
        self._set_status(line)

    async def _finish_operation(
        self,
        kind: str,
        targets: Sequence[ModuleRecord],
        succeeded: list[str],
        failed: list[tuple[str, str]],
        bar: compat.ProgressBar,
    ) -> None:
        compat.progress_phase(bar, 3.0, _PROGRESS_PHASES)
        self._selected_key = targets[0].dist
        if succeeded:
            # 操作成功的目标退出选区，保留失败目标以便重试。
            self._selected.difference_update(name for name, _ in succeeded)
            self._set_status(i18n.t("cli.tui.modules.refreshing", message=""))
            self.invalidate_cache()
            await self._load_records()
        if failed:
            names = i18n.t("cli.tui.common.list_separator").join(name for name, _ in failed)
            self.last_error = failed[0][1]
            self._set_status(
                i18n.t(
                    "cli.tui.modules.batch_failed",
                    ok=len(succeeded),
                    failed=len(failed),
                    names=names,
                    detail=failed[0][1],
                    what=_operation_action(kind),
                )
            )
            compat.progress_reset(bar)
            compat.notify(
                self.app,
                i18n.t("cli.tui.modules.notify_failed", count=len(failed)),
                severity="error",
                title=i18n.t(f"cli.tui.modules.label_{kind}", name=targets[0].dist),
            )
        elif succeeded:
            compat.progress_phase(bar, _PROGRESS_PHASES, _PROGRESS_PHASES)

            message = (
                succeeded[0][1]
                if len(succeeded) == 1
                else i18n.t("cli.tui.modules.batch_done", count=len(succeeded), what=_operation_action(kind))
            )
            self.last_result = message
            self._set_status(message)
            compat.notify(self.app, message, severity="information", title=message)
        self._busy = False
        self._sync_actions()

    def focus_primary(self) -> None:
        """聚焦列表；列表为空时聚焦页面容器，加载后恢复列表焦点。"""
        compat.focus_first(self, "#module-list")

    def reset_pending(self) -> None:
        """作废待确认状态；切页与本页状态变化时调用。"""
        self._confirm.reset()

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

    def action_update(self) -> None:
        """键位动作：更新选中项或全部已安装包。"""
        self.request_update()

    def action_toggle_load(self) -> None:
        """键位动作：装载或卸载选中项声明的模块。"""
        self.request_toggle_load()

    def action_clear_search(self) -> None:
        """键位动作：清空搜索框。"""
        self.clear_search()

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
