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
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
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

# 子进程式安装拿不到字节级进度，进度条按阶段推进：解析、执行、重载、完成。
_PROGRESS_PHASES = 4.0


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
        parts = (self.name, self.dist, self.version, self.summary, self.state_label, self.kind_label)
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

    :param records: 直接返回的记录序列。
    :param install_result: 安装返回值；缺省为成功。
    :param uninstall_result: 卸载返回值；缺省为成功。
    """

    def __init__(
        self,
        records: Sequence[ModuleRecord] = (),
        *,
        install_result: OperationResult | None = None,
        uninstall_result: OperationResult | None = None,
    ) -> None:
        self._records = tuple(records)
        self._install_result = install_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_install_ok"), "stub"
        )
        self._uninstall_result = uninstall_result or OperationResult(
            True, i18n.t("cli.tui.modules.stub_uninstall_ok"), "stub"
        )
        self.calls = {"list": 0, "install": 0, "uninstall": 0}
        self.installed: list[str] = []
        self.uninstalled: list[str] = []

    def list_modules(self) -> Sequence[ModuleRecord]:
        """见 :meth:`ModuleSource.list_modules`。"""
        self.calls["list"] += 1
        return self._records

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


@runtime_checkable
class ModuleSource(Protocol):
    """模块数据源接口；测试注入替身，生产走子进程。"""

    def list_modules(self) -> Sequence[ModuleRecord]:
        """返回全部模块记录。"""

    def install(self, record: ModuleRecord) -> OperationResult:
        """安装给定记录。"""

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """卸载给定记录。"""


def sort_key(record: ModuleRecord) -> tuple[bool, str]:
    """列表展示顺序：已安装在前，其次按名称升序（大小写不敏感）。"""
    return (not record.installed, record.name.casefold())


def _pick(source: Any, *names: str, default: Any = "") -> Any:
    """从字典或对象上按候选名取值，兼容对端契约未冻结时的字段别名。

    :param source: 字典或带属性的对象。
    :param names: 候选字段名，按顺序取第一个非 ``None`` 值。
    :param default: 全部缺失时的返回值。
    :return: 取到的原始值。
    """
    for name in names:
        if isinstance(source, Mapping) and source.get(name) is not None:
            return source[name]
        value = getattr(source, name, None)
        if value is not None:
            return value
    return default


def _text(value: Any) -> str:
    """把任意标量转为用于展示的字符串。"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return "、".join(_text(item) for item in value if _text(item))
    return str(value)


def _normalize_state(source: Any, fallback: str) -> str:
    """把对端的状态字段归一到三种取值。"""
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
    """把包类型归一到四种取值，未识别的类型返回空串。"""
    raw = _text(value).casefold()
    if not raw:
        return ""
    raw = _KIND_ALIASES.get(raw, raw)
    return raw if raw in _KIND_KEYS else ""


def _record_from_mapping(dist: str, info: Any) -> ModuleRecord:
    """把一条对端记录归一化为 :class:`ModuleRecord`。"""
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
        self.root = Path(root) if root is not None else Path.cwd()
        self.timeout = timeout
        self.calls = {"list": 0, "install": 0, "uninstall": 0}
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
        raise ModuleSourceError("；".join(errors))

    def install(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.install`。"""
        self.calls["install"] += 1
        return self._run_cli(("module", "add", record.dist or record.name), f"安装 {record.dist or record.name}")

    def uninstall(self, record: ModuleRecord) -> OperationResult:
        """见 :meth:`ModuleSource.uninstall`。"""
        self.calls["uninstall"] += 1
        return self._run_cli(("module", "remove", record.dist or record.name), f"卸载 {record.dist or record.name}")

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
        """构造子进程环境：注入实例目录，并把子进程标准流固定为 UTF-8。

        理由：子进程输出含中文与 JSON，Windows 控制台默认代码页可能是 GBK，
        读写编码不一致会得到乱码或解析失败，故两侧都显式声明 UTF-8。
        """
        env = dict(os.environ)
        env["AKARI_INSTANCE_DIR"] = str(self.root)
        env["PYTHONIOENCODING"] = "utf-8"
        return env

    def _run(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        """执行子进程并把常见失败转成 :class:`ModuleSourceError`。"""
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
            raise ModuleSourceError(f"找不到可执行文件：{argv[0]}（{error}）") from error
        except subprocess.TimeoutExpired as error:
            raise ModuleSourceError(f"`{' '.join(argv)}` 超过 {self.timeout:.0f} 秒未返回") from error
        except OSError as error:
            raise ModuleSourceError(f"`{' '.join(argv)}` 执行失败：{error}") from error

    def _list_from_cli_json(self) -> list[ModuleRecord]:
        """经 ``akaribot module list --json`` 取数。"""
        argv = self.cli_argv("module", "list", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise ModuleSourceError(f"`{' '.join(argv)}` 退出码 {completed.returncode}：{self._tail(completed.stderr)}")
        return normalize_records(self._parse_json(completed.stdout, "module list --json"))

    def _list_from_instance(self) -> list[ModuleRecord]:
        """退回 ``Instance.installed()`` 取数，该接口由 T5.1 提供。"""
        instance = self._instance()
        installed = getattr(instance, "installed", None)
        if not callable(installed):
            raise ModuleSourceError("akaribot.cli.instance.Instance 未提供 installed()，无法取数")
        try:
            payload = installed()
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的错误
            raise ModuleSourceError(f"Instance.installed() 失败：{type(error).__name__}: {error}") from error
        return normalize_records(payload)

    def _instance(self) -> Any:
        """构造实例对象；模块缺失、实例不存在或构造失败时给出可读原因。"""
        if self._instance_factory is not None:
            return self._instance_factory()
        try:
            from akaribot.cli.instance import Instance, find_instance_root
        except ImportError as error:
            raise ModuleSourceError("尚未提供 akaribot.cli.instance（T5.1），无法取数") from error
        try:
            root = find_instance_root(self.root)
            if root is None:
                raise ModuleSourceError(
                    f"{self.root} 不是 AkariBot 实例（未找到 akaribot.toml）；"
                    "先运行 `akaribot init`，或用 AKARI_INSTANCE_DIR 指定实例根"
                )
            return Instance(root)
        except ModuleSourceError:
            raise
        except Exception as error:  # noqa: BLE001 - 实例构造失败同样只作为降级原因上报
            raise ModuleSourceError(f"构造 Instance 失败：{type(error).__name__}: {error}") from error

    def _run_cli(self, args: Sequence[str], label: str) -> OperationResult:
        """执行安装或卸载子命令并包装结果。"""
        argv = self.cli_argv(*args)
        completed = self._run(argv)
        if completed.returncode == 0:
            return OperationResult(True, f"{label}成功", self._tail(completed.stdout))
        return OperationResult(False, f"{label}失败（退出码 {completed.returncode}）", self._tail(completed.stderr))

    def _parse_json(self, stdout: str, label: str) -> Any:
        """解析子进程 JSON 输出。"""
        text = stdout.strip()
        if not text:
            raise ModuleSourceError(f"`{label}` 没有输出")
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ModuleSourceError(f"`{label}` 输出不是 JSON：{error}") from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        """截取子进程输出的尾部，供状态栏展示。"""
        cleaned = (text or "").strip()
        return cleaned[-limit:]


class ModulesPage(compat.Vertical):
    """Modules 页控件。

    :param source: 数据源，缺省为 :class:`SubprocessModuleSource`。
    :param cache_ttl: 缓存有效期秒数；安装/卸载成功后立即失效，与有效期无关。
    """

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
        self.source: ModuleSource = source if source is not None else SubprocessModuleSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._records: tuple[ModuleRecord, ...] = ()
        self._loaded_at: float = 0.0
        self._query: str = ""
        self._selected_key: str | None = None
        self._busy: bool = False
        self._detail_rendered: str = ""
        self._status_rendered: str = "就绪"
        self._rendered_rows: tuple[str, ...] = ()

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder="搜索模块名 / 发行包 / 简介，空格分词", id="search")
            yield compat.Static("尚未读取", id="count")
        with compat.Horizontal(id="body"):
            yield compat.ListView(id="module-list")
            with compat.VerticalScroll(id="detail-pane"):
                yield compat.Static("选择一个模块查看详情", id="detail", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button("安装", id="install", variant="primary")
            yield compat.Button("卸载", id="uninstall", variant="error")
            yield compat.Button("刷新", id="refresh")
        yield compat.ProgressBar(total=100.0, show_eta=False, id="progress")
        yield compat.Static("就绪", id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后读取一次数据，并把焦点交给列表，使键位立即可用。"""
        compat.set_text_selection(self, False)
        self.query_one("#module-list", compat.ListView).focus()
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
            self._set_status(f"使用 {age:.1f} 秒前的缓存，共 {len(self._records)} 个模块")
            return
        self._set_status("正在读取模块列表…")
        self.run_worker(self._load_records(), group="modules-load", exclusive=True)

    async def _load_records(self) -> bool:
        """后台读取记录并刷新界面，返回是否成功。"""
        try:
            records = await asyncio.to_thread(self.source.list_modules)
        except ModuleSourceError as error:
            self._records = ()
            self._loaded_at = time.monotonic()
            self.last_error = str(error)
            self._render_list()
            self._set_status(f"读取失败：{error}")
            return False
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._records = ()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_list()
            self._set_status(f"读取失败：{self.last_error}")
            return False
        self._records = tuple(sorted(records, key=sort_key))
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = f"已读取 {len(self._records)} 个模块"
        self._render_list()
        self._set_status(self.last_result)
        return True

    def invalidate_cache(self) -> None:
        """使缓存立即失效，下一次读取必定走数据源。"""
        self._loaded_at = 0.0
        self._records = ()

    # endregion

    # region 渲染（只读缓存）

    def _render_list(self) -> None:
        """按缓存与搜索词重绘列表、计数、详情与按钮状态。"""
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
        """返回列表可用内容宽度：外框宽减去边框与左右内边距。"""
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 36
        return max(outer - 4, 8)

    def _name_column_width(self, inner_width: int) -> int:
        """计算名称列宽度：取最长名称，但不挤掉简介列。"""
        longest = compat.column_width(record.name for record in self._records)
        return max(min(max(longest, 6), 20, inner_width - 14), 4)

    def _version_column_width(self) -> int:
        """计算版本列宽度：同一屏内定宽，保证各行版本左对齐。"""
        longest = compat.column_width(record.version or "-" for record in self._records)
        return min(max(longest, 5), 8)

    def _row_text(self, record: ModuleRecord, name_width: int, version_width: int, inner_width: int) -> str:
        """渲染列表行；列宽按终端列数计算，中文与英文混排仍对齐。

        :param record: 记录。
        :param name_width: 名称列宽度，单位终端列。
        :param version_width: 版本列宽度，单位终端列。
        :param inner_width: 行可用的终端列数。
        :return: 显示宽度不超过 ``inner_width`` 的定宽行文本。
        """
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
        """定位要恢复的高亮项，找不到时回到首项。"""
        if not records:
            return 0
        if self._selected_key is not None:
            for index, record in enumerate(records):
                if record.dist == self._selected_key:
                    return index
        return 0

    def _sync_count(self, records: Sequence[ModuleRecord]) -> None:
        """更新计数标签。"""
        installed = sum(1 for record in self._records if record.installed)
        text = f"显示 {len(records)} / 共 {len(self._records)} 个模块，其中已安装 {installed} 个"
        self.query_one("#count", compat.Static).update(compat.plain_text(text))

    def _sync_detail(self) -> None:
        """按当前选中项更新详情面板。"""
        record = self.selected_record
        if record is None:
            if not self._records:
                hint = "列表为空：先按 r 重新读取，或用搜索框输入模块名后按 i 安装"
            elif not self.visible_records:
                hint = "没有匹配的模块：按 esc 清空搜索"
            else:
                hint = "选择左侧模块查看详情"
            self._detail_rendered = hint
            self.query_one("#detail", compat.Static).update(compat.plain_text(hint))
            return
        self._selected_key = record.dist
        rows = [
            ("名称", record.name),
            ("发行包", record.dist),
            ("类型", record.kind_label),
            ("版本", record.version or "未知"),
            ("状态", record.state_label),
            ("核心 API", record.requires_core_api or "未声明"),
            ("简介", record.summary or "无"),
        ]
        if record.dependents:
            rows.append(("被依赖", "、".join(record.dependents)))
        if record.origin:
            rows.append(("来源", record.origin))
        lines = compat.align_rows(rows, gap=2)
        lines.append("")
        lines.append("Enter 选中；i 安装；u 卸载；r 刷新")
        text = "\n".join(lines)
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _sync_actions(self) -> None:
        """按当前选中项与忙碌状态更新按钮可用性。"""
        install_target = self._install_target()
        uninstall_target = self._uninstall_target()
        self.query_one("#install", compat.Button).disabled = self._busy or install_target is None
        self.query_one("#uninstall", compat.Button).disabled = self._busy or uninstall_target is None

    def _set_status(self, text: str) -> None:
        """更新状态栏。"""
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
        """搜索词变化时只过滤缓存。"""
        self._query = event.value
        self._render_list()

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        """高亮项变化时更新详情与按钮。"""
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.ListView.Selected)
    def _on_selected(self, event: compat.ListView.Selected) -> None:
        """回车选中时刷新详情。"""
        self._sync_detail()
        self._sync_actions()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        """按钮回调：安装、卸载、刷新。"""
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
        """确定安装目标：优先未安装的选中项，其次搜索框里的模块名。"""
        record = self.selected_record
        if record is not None and not record.installed:
            return record
        candidate = self._query.strip()
        if _NAME_PATTERN.match(candidate) and (record is None or record.dist != candidate):
            return ModuleRecord(name=candidate, dist=candidate, state=STATE_AVAILABLE)
        return None

    def _uninstall_target(self) -> ModuleRecord | None:
        """确定卸载目标：当前选中的已安装项。"""
        record = self.selected_record
        if record is not None and record.installed:
            return record
        return None

    def request_install(self) -> None:
        """发起安装；无目标时给出提示而不动作。"""
        target = self._install_target()
        if target is None:
            compat.notify(self.app, "先选中未安装的模块，或在搜索框输入模块名", severity="warning", title="安装")
            return
        self._start_operation("install", f"安装 {target.dist}", target, self.source.install)

    def request_uninstall(self) -> None:
        """发起卸载；无目标时给出提示而不动作。"""
        target = self._uninstall_target()
        if target is None:
            compat.notify(self.app, "先选中一个已安装的模块", severity="warning", title="卸载")
            return
        self._start_operation("uninstall", f"卸载 {target.dist}", target, self.source.uninstall)

    def _start_operation(
        self,
        kind: str,
        label: str,
        record: ModuleRecord,
        func: Callable[[ModuleRecord], OperationResult],
    ) -> None:
        """在后台任务里执行安装或卸载，并按阶段推进进度。"""
        if self._busy:
            compat.notify(self.app, "已有安装或卸载在进行", severity="warning", title="请稍候")
            return
        self._busy = True
        self._sync_actions()
        compat.progress_phase(self.query_one("#progress", compat.ProgressBar), 1.0, _PROGRESS_PHASES)
        self._set_status(f"{label}：调用子进程…")
        self.run_worker(self._operate(kind, label, record, func), group="modules-op", exclusive=True)

    async def _operate(
        self,
        kind: str,
        label: str,
        record: ModuleRecord,
        func: Callable[[ModuleRecord], OperationResult],
    ) -> None:
        """执行子进程操作；成功后缓存失效并重新读取列表。"""
        bar = self.query_one("#progress", compat.ProgressBar)
        try:
            result = await asyncio.to_thread(func, record)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成结果展示
            result = OperationResult(False, f"{label}失败", f"{type(error).__name__}: {error}")
        compat.progress_phase(bar, 3.0, _PROGRESS_PHASES)
        self._selected_key = record.dist
        if result.ok:
            self._set_status(f"{result.message}，正在刷新列表…")
            self.invalidate_cache()
            await self._load_records()
            compat.progress_phase(bar, _PROGRESS_PHASES, _PROGRESS_PHASES)
            detail = f"（{result.detail.splitlines()[-1]}）" if result.detail else ""
            self.last_result = f"{result.message}{detail}"
            self._set_status(self.last_result)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            self._set_status(f"{result.message}：{result.detail.splitlines()[-1] if result.detail else '无输出'}")
            compat.progress_reset(bar)
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def action_refresh(self) -> None:
        """键位动作：强制重新读取列表。"""
        self.refresh_records(force=True)

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()
