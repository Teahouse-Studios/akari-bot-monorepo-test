"""Dev 页：workspace 路径、各包来源与 editable 状态，附跑测试与生成脚手架的入口。

包清单经 ``akaribot module list --json`` 子进程取数，CLI 进程内不 import core；``[dev] workspace_root``
与 ``[instance] mode`` 出自实例的 ``akaribot.toml``，由 CLI 自己的 ``InstanceMeta`` 读取——
``akaribot dev status --json``（上位文档 §3.2.2）尚未实现，工作区成员索引因此在本进程内扫描。
包清单本身只读：不提供 use / link / unlink，也不写实例配置；两个动作各起一次 ``akaribot`` 子进程，
``t`` 跑测试（``akaribot test``），``n`` 生成脚手架（``akaribot new module|adapter``），输出逐行回显。
"""

from __future__ import annotations

import asyncio
import json
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

SOURCE_WORKSPACE = "workspace"
SOURCE_EDITABLE = "editable"
SOURCE_REGISTRY = "registry"
SOURCE_UNKNOWN = "unknown"

# 来源、包类型与模式取自对端 JSON，界面按当前语言取标签，故这里只存文案键。
_SOURCE_KEYS = {
    SOURCE_WORKSPACE: "cli.tui.dev.source_workspace",
    SOURCE_EDITABLE: "cli.tui.dev.source_editable",
    SOURCE_REGISTRY: "cli.tui.dev.source_registry",
    SOURCE_UNKNOWN: "cli.tui.dev.source_unknown",
}
_KIND_KEYS = {
    "module": "cli.tui.dev.kind_module",
    "adapter": "cli.tui.dev.kind_adapter",
    "core": "cli.tui.dev.kind_core",
    "testing": "cli.tui.dev.kind_testing",
}
_MODE_KEYS = {"workspace": "cli.tui.dev.mode_workspace", "installed": "cli.tui.dev.mode_installed"}

EMPTY_CELL = "—"

NAME_MAX_WIDTH = 18
KIND_WIDTH = 8
VERSION_MAX_WIDTH = 10
EDITABLE_WIDTH = 8
SOURCE_MAX_WIDTH = 14
MIN_PATH_WIDTH = 10
COLUMN_GAP = 2
ROW_INDENT = 2

ACTION_TEST = "test"
ACTION_NEW = "new"

TARGET_MODULE = "module"
TARGET_ADAPTER = "adapter"

# 输出区只回显尾部若干行；完整序列留在 ``action_lines()``，供断言与失败详情使用。
ACTION_OUTPUT_LINES = 4
ACTION_TAIL_LINES = 40
STATUS_DETAIL_LIMIT = 400

# 列标题在渲染时按当前语言取；editable 是数据字段名，两种语言写法一致，故不入键表。
_COLUMN_KEYS: tuple[str | None, ...] = (
    "cli.tui.dev.col_package",
    "cli.tui.dev.col_kind",
    "cli.tui.dev.col_version",
    None,
    "cli.tui.dev.col_source",
    "cli.tui.dev.col_path",
)


def _column_titles() -> tuple[str, ...]:
    return tuple(i18n.t(key) if key else "editable" for key in _COLUMN_KEYS)


def _canonical_dist(name: str) -> str:
    return name.strip().lower().replace("_", "-").replace(".", "-")


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


def _action_label(kind: str) -> str:
    return i18n.t("cli.tui.dev.action_label_test" if kind == ACTION_TEST else "cli.tui.dev.action_label_new")


def _name_rejection(name: str) -> str:
    # 页面只拦下显然无法成包的名字；其余校验（长度、首字符、关键字）交给 CLI 报错。
    if not name:
        return i18n.t("cli.tui.dev.new_name_required")
    if any(char.isspace() for char in name) or "/" in name or "\\" in name:
        return i18n.t("cli.tui.dev.new_name_invalid")
    return ""


def _one_line(text: str, limit: int = STATUS_DETAIL_LIMIT) -> str:
    return " ".join(text.split())[-limit:]


@dataclass(frozen=True)
class DevPackage:
    """一个已装包的来源与 editable 状态。

    :param dist: 分发名，如 ``akari-bot-module-wiki``。
    :param name: 短名，如 ``wiki``。
    :param kind: ``module`` / ``adapter`` / ``core`` / ``testing``。
    :param version: 已装版本。
    :param editable: ``module list --json`` 回传的 editable 标记。
    :param source: ``workspace`` / ``editable`` / ``registry`` / ``unknown``。
    :param path: 本地路径；仅工作区成员有值。
    :param requires_core_api: 声明的 core API 区间。
    :param provides_modules: 该包注册的模块名。
    :param summary: 一句话简介。
    """

    dist: str
    name: str = ""
    kind: str = ""
    version: str = ""
    editable: bool = False
    source: str = SOURCE_UNKNOWN
    path: str = ""
    requires_core_api: str = ""
    provides_modules: tuple[str, ...] = ()
    summary: str = ""

    @property
    def display_name(self) -> str:
        """包名列的展示文本。"""
        return self.name or self.dist or i18n.t("cli.tui.dev.unnamed")

    @property
    def kind_label(self) -> str:
        """类型列的展示文本。"""
        key = _KIND_KEYS.get(self.kind)
        return i18n.t(key) if key else self.kind or i18n.t("cli.tui.common.undeclared")

    @property
    def editable_label(self) -> str:
        """editable 列的展示文本。"""
        return i18n.t("cli.tui.dev.yes") if self.editable else i18n.t("cli.tui.dev.no")

    @property
    def source_label(self) -> str:
        """来源列的展示文本。"""
        return i18n.t(_SOURCE_KEYS.get(self.source, _SOURCE_KEYS[SOURCE_UNKNOWN]))

    @property
    def path_text(self) -> str:
        """本地路径列的展示文本。"""
        return self.path or EMPTY_CELL

    @property
    def key(self) -> str:
        """选中项的稳定标识。"""
        return self.dist or self.name


@dataclass(frozen=True)
class DevSnapshot:
    """一次 Dev 取数的结果。

    :param instance_root: 实例根目录文本。
    :param meta_path: ``akaribot.toml`` 路径文本。
    :param mode: ``workspace`` / ``installed``；读不到时为空串。
    :param workspace_root: ``[dev] workspace_root`` 原值。
    :param workspace_exists: 工作区根是否为存在的目录。
    :param registry_sources: ``[registry] sources``。
    :param packages: 已装包记录。
    :param errors: 取数错误。
    :param notes: 其他说明，如工作区未配置。
    """

    instance_root: str = ""
    meta_path: str = ""
    mode: str = ""
    workspace_root: str = ""
    workspace_exists: bool = False
    registry_sources: tuple[str, ...] = ()
    packages: tuple[DevPackage, ...] = ()
    errors: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def mode_label(self) -> str:
        """模式列的展示文本。"""
        key = _MODE_KEYS.get(self.mode)
        return i18n.t(key) if key else self.mode or i18n.t("cli.tui.dev.mode_unknown")

    @property
    def workspace_label(self) -> str:
        """工作区路径的展示文本。"""
        if not self.workspace_root:
            return i18n.t("cli.tui.dev.workspace_unset")
        key = "cli.tui.dev.workspace_exists" if self.workspace_exists else "cli.tui.dev.workspace_missing"
        return i18n.t(key, path=self.workspace_root)

    def source_counts(self) -> dict[str, int]:
        """按来源统计包数。"""
        counts: dict[str, int] = {}
        for package in self.packages:
            counts[package.source] = counts.get(package.source, 0) + 1
        return counts


@dataclass(frozen=True)
class ActionResult:
    """一次动作的结局。

    :param ok: 子进程是否以退出码 0 结束。
    :param returncode: 子进程退出码；被终止时为信号值。
    :param message: 状态栏显示的一行结论，由数据源按动作与结果生成。
    :param detail: 输出尾部，失败时并入状态栏。
    :param cancelled: 是否由终止请求结束。
    """

    ok: bool = False
    returncode: int = 0
    message: str = ""
    detail: str = ""
    cancelled: bool = False


class StaticDevSource:
    """固定数据的替身数据源，供自动化断言使用，不产生任何子进程。

    :param snapshot: ``load_snapshot`` 的返回值。
    :param action_lines: 动作逐行回放的固定输出。
    :param action_result: 动作的返回值；``hold`` 为真时先等 :attr:`gate` 放行。
    :param hold: 为真时 ``stream_action`` 停在 :attr:`gate` 上，供「运行中」断言使用。
    """

    def __init__(
        self,
        snapshot: DevSnapshot | None = None,
        *,
        action_lines: Sequence[str] = (),
        action_result: ActionResult | None = None,
        hold: bool = False,
    ) -> None:
        self._snapshot = snapshot or DevSnapshot()
        self._action_lines = tuple(action_lines)
        self._action_result = action_result or ActionResult(ok=True, message="stub action done")
        self._hold = hold
        self.gate = asyncio.Event()
        self.calls = {"load": 0, "action": 0, "cancel": 0}
        self.actions: list[tuple[str, dict[str, Any]]] = []
        self.cancelled: list[str] = []

    def load_snapshot(self) -> DevSnapshot:
        """见 :meth:`DevSource.load_snapshot`。"""
        self.calls["load"] += 1
        return self._snapshot

    async def stream_action(self, kind: str, params: Mapping[str, Any], on_line: Callable[[str], None]) -> ActionResult:
        """见 :meth:`DevSource.stream_action`；替身回放固定输出，不产生子进程。"""
        self.calls["action"] += 1
        self.actions.append((kind, dict(params)))
        if self._hold:
            await self.gate.wait()
        if kind in self.cancelled:
            return ActionResult(
                ok=False,
                returncode=-15,
                message=i18n.t("cli.tui.dev.action_cancelled", label=_action_label(kind)),
                cancelled=True,
            )
        for line in self._action_lines:
            on_line(line)
        return self._action_result

    def cancel_action(self, kind: str) -> bool:
        """见 :meth:`DevSource.cancel_action`；替身记录请求并放行被挂起的动作。"""
        self.calls["cancel"] += 1
        self.cancelled.append(kind)
        self.gate.set()
        return True


@runtime_checkable
class DevSource(Protocol):
    """Dev 数据源接口；测试注入替身，生产走子进程。"""

    def load_snapshot(self) -> DevSnapshot:
        """返回 workspace 配置与已装包清单；错误记入快照而不抛出。"""

    async def stream_action(self, kind: str, params: Mapping[str, Any], on_line: Callable[[str], None]) -> ActionResult:
        """执行一次耗时的 CLI 动作，并把子进程输出逐行交给 ``on_line``。

        :param kind: :data:`ACTION_TEST` 或 :data:`ACTION_NEW`。
        :param params: 动作参数——``test`` 取 ``args``（追加到 ``test`` 之后的参数）与 ``cwd``；
            ``new`` 取 ``name`` / ``target`` / ``directory`` 与 ``cwd``。
        :param on_line: 每读到一行输出就调用一次，供界面回显进度。
        :return: 动作结果。
        """

    def cancel_action(self, kind: str) -> bool:
        """请求终止正在执行的动作，返回是否发出了终止请求。"""


def normalize_packages(payload: Any, members: Mapping[str, str] | None = None) -> tuple[DevPackage, ...]:
    """把 ``module list --json`` 的负载归一化为包记录。

    来源判定按优先级降级：分发名命中工作区成员索引时记为本地工作区并带路径；否则按
    ``editable`` 区分本地可编辑安装与远端发行版。``editable`` 单独不足以判定来源——
    工作区成员经 ``uv sync`` 装进来时该标记为假，却在磁盘上有本地源码。

    :param payload: ``json.loads`` 的结果；接受包装对象与裸数组。
    :param members: 规范化分发名到本地路径的映射。
    :return: 按类型与分发名排序的包记录。
    """
    index = dict(members or {})
    if isinstance(payload, Mapping):
        raw: Any = None
        for key in ("packages", "items", "installed", "data"):
            candidate = payload.get(key)
            if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes)):
                raw = candidate
                break
        entries = list(raw) if raw is not None else []
    elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
        entries = list(payload)
    else:
        entries = []
    packages: list[DevPackage] = []
    for entry in entries:
        if isinstance(entry, str):
            entry = {"dist": entry}
        if not isinstance(entry, Mapping):
            continue
        dist = _text(_pick(entry, "dist", "dist_name", "distribution", "package"))
        name = _text(_pick(entry, "name", "module", "short_name"))
        editable = _flag(_pick(entry, "editable", default=False))
        path = index.get(_canonical_dist(dist or name), "")
        if path:
            source = SOURCE_WORKSPACE
        elif editable:
            source = SOURCE_EDITABLE
        elif dist or name:
            source = SOURCE_REGISTRY
        else:
            source = SOURCE_UNKNOWN
        packages.append(
            DevPackage(
                dist=dist or name,
                name=name,
                kind=_text(_pick(entry, "kind", "type", "category")),
                version=_text(_pick(entry, "version", "installed_version")),
                editable=editable,
                source=source,
                path=path,
                requires_core_api=_text(_pick(entry, "requires_core_api", "core_api")),
                provides_modules=_string_tuple(_pick(entry, "provides_modules", default=())),
                summary=_text(_pick(entry, "summary", "description")),
            )
        )
    packages.sort(key=lambda item: (item.kind, item.dist))
    return tuple(packages)


class DevSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


class SubprocessDevSource:
    """默认数据源：包清单经子进程取数，实例元数据在 CLI 进程内读取。

    实例元数据不经子进程的理由：``akaribot dev status --json`` 尚未实现，而 ``akaribot.toml``
    属 CLI 自己的契约；工作区成员索引按 ``pyproject.toml`` 扫描，同样不触碰 core。

    :param root: 实例根目录，默认当前工作目录。
    :param timeout: 子进程的超时秒数。
    :param action_timeout: 单次动作的超时秒数；测试套件可能跑数分钟。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param meta_reader: 实例元数据读取回调，缺省读 ``akaribot.toml``，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        action_timeout: float = 1800.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        meta_reader: Callable[[], Mapping[str, Any]] | None = None,
    ) -> None:
        # 实例根同时是子进程的 cwd 与 AKARI_INSTANCE_DIR；只认 cwd 会忽略环境变量，
        # 在仓库根运行 TUI 时静默读到另一个实例的配置与日志。
        # 根在取数时解析：界面切换实例后，同一份数据源要指向新实例，不能在构造时定死。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.action_timeout = action_timeout
        self.calls = {"load": 0}
        self._runner = runner or subprocess.run
        self._meta_reader = meta_reader
        self._action_process: asyncio.subprocess.Process | None = None
        self._action_cancelled = False

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def load_snapshot(self) -> DevSnapshot:
        """见 :meth:`DevSource.load_snapshot`。"""
        self.calls["load"] += 1
        meta, errors = self._read_meta()
        notes: list[str] = []
        workspace_root = _text(meta.get("workspace_root"))
        members: dict[str, str] = {}
        if workspace_root:
            members, member_errors = self._workspace_members(workspace_root)
            errors.extend(member_errors)
        else:
            notes.append(i18n.t("cli.tui.dev.note_no_workspace"))
        packages: tuple[DevPackage, ...] = ()
        payload, list_error = self._list_packages()
        if list_error:
            errors.append(list_error)
        else:
            packages = normalize_packages(payload, members)
        return DevSnapshot(
            instance_root=_text(meta.get("instance_root")) or str(self.root),
            meta_path=_text(meta.get("meta_path")),
            mode=_text(meta.get("mode")),
            workspace_root=workspace_root,
            workspace_exists=bool(workspace_root) and Path(workspace_root).expanduser().is_dir(),
            registry_sources=_string_tuple(meta.get("registry_sources")),
            packages=packages,
            errors=tuple(errors),
            notes=tuple(notes),
        )

    async def stream_action(self, kind: str, params: Mapping[str, Any], on_line: Callable[[str], None]) -> ActionResult:
        """见 :meth:`DevSource.stream_action`。

        测试套件与脚手架都可能跑上数分钟，沿用 ``subprocess.run`` 时这段时间界面只能空转；
        改为异步起进程并逐行读输出，界面据此显示进度，``Esc`` 也能终止进程。
        """
        argv = self._action_argv(kind, params)
        self._action_cancelled = False
        try:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=self._action_cwd(params),
                # 标准输入指向空设备：动作子进程不该读界面这一侧的终端，需要输入的选项已在 argv 里给全。
                stdin=subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise DevSourceError(i18n.t("cli.tui.dev.src_exe_missing", path=argv[0], error=error)) from error
        except OSError as error:
            raise DevSourceError(i18n.t("cli.tui.dev.src_oserror", cmd=" ".join(argv), error=error)) from error
        self._action_process = process
        tail: deque[str] = deque(maxlen=ACTION_TAIL_LINES)
        try:
            returncode = await asyncio.wait_for(self._pump(process, on_line, tail), timeout=self.action_timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            raise DevSourceError(
                i18n.t("cli.tui.dev.src_timeout", cmd=" ".join(argv), seconds=f"{self.action_timeout:.0f}")
            ) from None
        except asyncio.CancelledError:
            process.kill()
            raise
        finally:
            self._action_process = None
        detail = "\n".join(tail)
        if self._action_cancelled:
            return ActionResult(
                ok=False,
                returncode=returncode,
                message=i18n.t("cli.tui.dev.action_cancelled", label=_action_label(kind)),
                detail=detail,
                cancelled=True,
            )
        ok = returncode == 0
        suffix = "ok" if ok else "failed"
        return ActionResult(
            ok=ok,
            returncode=returncode,
            message=i18n.t(f"cli.tui.dev.action_{kind}_{suffix}", code=returncode),
            detail=detail,
        )

    def cancel_action(self, kind: str) -> bool:
        """见 :meth:`DevSource.cancel_action`；向动作子进程发终止信号。"""
        process = self._action_process
        if process is None or process.returncode is not None:
            return False
        self._action_cancelled = True
        process.terminate()
        return True

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

    def _action_argv(self, kind: str, params: Mapping[str, Any]) -> list[str]:
        if kind == ACTION_NEW:
            # --non-interactive：表单没收集的选项取默认值。缺了它，子进程会把问卷打进输出区并
            # 与界面争抢键盘——它继承的是同一个终端。
            target = _text(params.get("target")) or TARGET_MODULE
            args = [
                "new",
                target,
                _text(params.get("name")),
                "--non-interactive",
                # 三个开关一律显式给值：不给时 CLI 取自己的缺省（tests 默认为真），与表单显示不符。
                "--config" if _flag(params.get("config")) else "--no-config",
            ]
            if target != TARGET_ADAPTER:
                # new adapter 只声明了 --config，多给的开关会被 typer 当成未知选项拒绝。
                args.append("--database" if _flag(params.get("database")) else "--no-database")
                args.append("--tests" if _flag(params.get("tests")) else "--no-tests")
            directory = _text(params.get("directory"))
            if directory:
                args += ["--dir", directory]
            return self.cli_argv(*args)
        return self.cli_argv(ACTION_TEST, *_string_tuple(params.get("args")))

    def _action_cwd(self, params: Mapping[str, Any]) -> str:
        # 动作在工作区根执行：测试路径与新建包的目录都相对它解析；工作区未配置时退回实例根。
        return _text(params.get("cwd")) or str(self.root)

    def _read_meta(self) -> tuple[dict[str, Any], list[str]]:
        if self._meta_reader is not None:
            try:
                return dict(self._meta_reader()), []
            except Exception as error:  # noqa: BLE001 - 替身读取失败只作为错误上报
                return {}, [i18n.t("cli.tui.dev.meta_read_failed", kind=type(error).__name__, error=error)]
        try:
            from akaribot.cli.instance import InstanceMeta, find_instance_root
        except ImportError as error:
            return {}, [i18n.t("cli.tui.dev.meta_module_missing", error=error)]
        root = find_instance_root(self.root)
        if root is None:
            return {}, [i18n.t("cli.tui.dev.not_instance", root=self.root)]
        try:
            meta = InstanceMeta.load(root)
        except Exception as error:  # noqa: BLE001 - 元数据损坏不应中断页面
            return {"instance_root": str(root)}, [
                i18n.t("cli.tui.dev.meta_parse_failed", kind=type(error).__name__, error=error)
            ]
        return {
            "instance_root": str(root),
            "meta_path": str(meta.path),
            "mode": meta.mode,
            "workspace_root": meta.workspace_root,
            "registry_sources": meta.registry_sources,
        }, []

    def _workspace_members(self, workspace_root: str) -> tuple[dict[str, str], list[str]]:
        path = Path(workspace_root).expanduser()
        if not path.is_dir():
            return {}, [i18n.t("cli.tui.dev.workspace_dir_missing", path=path)]
        try:
            from akaribot.cli.venv import workspace_index
        except ImportError as error:
            return {}, [i18n.t("cli.tui.dev.venv_module_missing", error=error)]
        try:
            index = workspace_index(path)
        except Exception as error:  # noqa: BLE001 - 工作区扫描失败只降级来源判定
            return {}, [i18n.t("cli.tui.dev.scan_failed", kind=type(error).__name__, error=error)]
        return {_canonical_dist(dist): str(member.path) for dist, member in index.items()}, []

    def _list_packages(self) -> tuple[Any, str]:
        argv = self.cli_argv("module", "list", "--json")
        try:
            completed = self._run(argv)
        except DevSourceError as error:
            return None, str(error)
        if completed.returncode != 0:
            return None, i18n.t(
                "cli.tui.dev.src_exit_code",
                cmd=" ".join(argv),
                code=completed.returncode,
                tail=self._tail(completed.stderr),
            )
        try:
            return self._parse_json(completed.stdout, "module list --json"), ""
        except DevSourceError as error:
            return None, str(error)

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
            raise DevSourceError(i18n.t("cli.tui.dev.src_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise DevSourceError(
                i18n.t("cli.tui.dev.src_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from error
        except OSError as error:
            raise DevSourceError(i18n.t("cli.tui.dev.src_oserror", cmd=" ".join(argv), error=error)) from error

    def _parse_json(self, stdout: str, label: str) -> Any:
        text = stdout.strip()
        if not text:
            raise DevSourceError(i18n.t("cli.tui.dev.src_empty_output", label=label))
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise DevSourceError(i18n.t("cli.tui.dev.src_bad_json", label=label, error=error)) from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        return (text or "").strip()[-limit:]


@dataclass(frozen=True)
class PackageLayout:
    """包列表列宽，单位终端列；宽度为 0 的列不渲染。

    :param name_width: 包名列。
    :param kind_width: 类型列。
    :param version_width: 版本列。
    :param editable_width: editable 列。
    :param source_width: 来源列。
    :param path_width: 本地路径列。
    """

    name_width: int
    kind_width: int
    version_width: int
    editable_width: int
    source_width: int
    path_width: int

    def widths(self) -> tuple[int, ...]:
        """按列序返回宽度。"""
        return (
            self.name_width,
            self.kind_width,
            self.version_width,
            self.editable_width,
            self.source_width,
            self.path_width,
        )


class DevPage(compat.Vertical):
    """Dev 页控件：包清单只读，跑测试与生成脚手架经数据源起子进程。

    :param source: 数据源，缺省为 :class:`SubprocessDevSource`。
    :param cache_ttl: 缓存有效期秒数；超期后按 ``r`` 重新取数。
    """

    can_focus = True

    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.dev.action_refresh")),
        ("t", "run_tests", i18n.t("cli.tui.dev.action_run_tests")),
        ("n", "new_package", i18n.t("cli.tui.dev.action_new_package")),
        # 终止是低频动作，页脚留给刷新、测试与新建三条。
        ("escape", "cancel_action", i18n.t("cli.tui.dev.action_cancel"), False),
    )

    DEFAULT_CSS = """
    DevPage {
        layout: vertical;
        height: 1fr;
    }
    DevPage #workspace {
        height: 4;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #columns {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #package-list {
        height: 1fr;
        border: round $primary;
    }
    DevPage #package-list > ListItem {
        padding: 0;
    }
    DevPage #package-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #actions {
        height: 3;
        padding: 0 0 0 1;
    }
    DevPage #test-path {
        width: 1fr;
    }
    DevPage #action-panel {
        height: auto;
    }
    DevPage #new-form {
        height: auto;
    }
    DevPage #new-fields, DevPage #new-switches, DevPage #new-buttons {
        height: 3;
        padding: 0 0 0 1;
    }
    DevPage #new-name, DevPage #new-dir {
        width: 1fr;
    }
    DevPage #new-kind {
        width: auto;
        margin: 0 0 0 1;
    }
    DevPage #new-config, DevPage #new-database, DevPage #new-tests {
        width: auto;
        padding: 1 0 0 1;
    }
    DevPage #new-hint {
        width: 1fr;
        padding: 1 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #action-output {
        height: 6;
        border: round $primary;
        padding: 0 1;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #detail {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DevPage #status {
        height: 2;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(
        self,
        source: DevSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DevSource = source if source is not None else SubprocessDevSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._snapshot = DevSnapshot()
        self._loaded_at: float = 0.0
        self._selected_key: str | None = None
        self._busy: bool = False
        self._row_texts: tuple[str, ...] = ()
        self._package_rows: tuple[tuple[str, ...], ...] = ()
        self._header_text: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        self._workspace_rendered: str = ""
        self._detail_rendered: str = ""
        self._action_kind: str = ""
        self._action_lines: list[str] = []
        self._action_rendered: str = ""
        self._action_result: ActionResult | None = None
        self._cancel_requested: bool = False
        self._new_form_open: bool = False
        self._new_kind: str = TARGET_MODULE
        self._new_hint: str = ""

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：包清单、动作表单与输出区，动作由键位与按钮触发。"""
        yield compat.Static(i18n.t("cli.tui.dev.workspace_pending"), id="workspace", markup=False)
        yield compat.Static("", id="columns", markup=False)
        yield compat.ListView(id="package-list")
        with compat.Vertical(id="action-panel"):
            with compat.Vertical(id="new-form"):
                with compat.Horizontal(id="new-fields"):
                    yield compat.Input(placeholder=i18n.t("cli.tui.dev.new_name_placeholder"), id="new-name")
                    yield compat.Button(
                        i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t("cli.tui.dev.new_kind_module")),
                        id="new-kind",
                    )
                    yield compat.Input(placeholder=i18n.t("cli.tui.dev.new_dir_placeholder"), id="new-dir")
                with compat.Horizontal(id="new-switches"):
                    yield compat.Checkbox(i18n.t("cli.tui.dev.new_config"), id="new-config")
                    yield compat.Checkbox(i18n.t("cli.tui.dev.new_database"), id="new-database")
                    yield compat.Checkbox(i18n.t("cli.tui.dev.new_tests"), value=True, id="new-tests")
                with compat.Horizontal(id="new-buttons"):
                    yield compat.Button(i18n.t("cli.tui.dev.new_confirm"), id="new-confirm", variant="primary")
                    yield compat.Button(i18n.t("cli.tui.dev.new_close"), id="new-close")
                    yield compat.Static("", id="new-hint", markup=False)
            yield compat.Static("", id="action-output", markup=False)
        with compat.Horizontal(id="actions"):
            yield compat.Button(i18n.t("cli.tui.dev.action_refresh"), id="refresh")
            yield compat.Button(i18n.t("cli.tui.dev.action_run_tests"), id="run-tests")
            yield compat.Input(placeholder=i18n.t("cli.tui.dev.test_path_placeholder"), id="test-path")
            yield compat.Button(i18n.t("cli.tui.dev.action_new_package"), id="new-package")
        yield compat.Static(i18n.t("cli.tui.dev.detail_placeholder"), id="detail", markup=False)
        yield compat.Static(i18n.t("cli.tui.common.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；取数推迟到首次显示。"""
        compat.set_text_selection(self, False)
        self._render_action_panel()

    def activate(self) -> None:
        """首次显示时读取工作区快照。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_snapshot()

    # region 状态读取（供测试与 App 使用）

    @property
    def snapshot(self) -> DevSnapshot:
        """返回最近一次取到的快照，不触发子进程。"""
        return self._snapshot

    @property
    def packages(self) -> tuple[DevPackage, ...]:
        """返回缓存中的包记录。"""
        return self._snapshot.packages

    @property
    def selected_package(self) -> DevPackage | None:
        """返回列表当前高亮项对应的包。"""
        packages = self._snapshot.packages
        if not packages:
            return None
        try:
            list_view = self.query_one("#package-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(packages):
            return None
        return packages[index]

    @property
    def workspace_text(self) -> str:
        """返回顶部 workspace 面板当前文本。"""
        return self._workspace_rendered

    @property
    def header_text(self) -> str:
        """返回列标题行当前文本。"""
        return self._header_text

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def detail_text(self) -> str:
        """返回详情栏当前文本。"""
        return self._detail_rendered

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的包行文本。"""
        return self._row_texts

    def package_cells(self) -> tuple[tuple[str, ...], ...]:
        """返回最近一次渲染出的包行各列取值，顺序与列表一致。"""
        return self._package_rows

    def cache_age(self) -> float:
        """返回缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    @property
    def action_kind(self) -> str:
        """返回正在运行的动作名；空闲时为空串。"""
        return self._action_kind

    @property
    def action_result(self) -> ActionResult | None:
        """返回最近一次动作的结局；从未执行时为 ``None``。"""
        return self._action_result

    @property
    def action_output_text(self) -> str:
        """返回输出区当前显示的文本。"""
        return self._action_rendered

    @property
    def new_form_open(self) -> bool:
        """返回新建包表单是否展开。"""
        return self._new_form_open

    @property
    def new_hint_text(self) -> str:
        """返回新建包表单的校验提示。"""
        return self._new_hint

    def action_lines(self) -> tuple[str, ...]:
        """返回最近一次动作的完整输出行。"""
        return tuple(self._action_lines)

    def test_args(self) -> tuple[str, ...]:
        """返回测试输入框里的参数，按空白拆分。"""
        return self._split_args(self._input_text("#test-path"))

    # endregion

    # region 数据读取

    def refresh_snapshot(self, *, force: bool = False) -> None:
        """读取 workspace 配置与包清单。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不取数。
        """
        if not force and self._loaded_at and self.cache_age() < self.cache_ttl:
            self._render_all()
            self._set_status(
                i18n.t(
                    "cli.tui.dev.status_cached",
                    age=f"{self.cache_age():.1f}",
                    total=len(self._snapshot.packages),
                )
            )
            return
        self._set_status(i18n.t("cli.tui.dev.status_loading"))
        self.run_worker(self._load(), group="dev-load", exclusive=True)

    async def _load(self) -> bool:
        try:
            snapshot = await asyncio.to_thread(self.source.load_snapshot)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._snapshot = DevSnapshot()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_all()
            self._set_status(i18n.t("cli.tui.dev.status_load_failed", error=self.last_error))
            return False
        self._snapshot = snapshot
        self._loaded_at = time.monotonic()
        self.last_error = i18n.t("cli.tui.common.error_separator").join(snapshot.errors)
        self.last_result = self._result_line(len(snapshot.packages))
        self._render_all()
        if snapshot.errors:
            self._set_status(i18n.t("cli.tui.common.error_separator").join((self.last_result, self.last_error)))
        else:
            self._set_status(self.last_result)
        return True

    def _result_line(self, count: int) -> str:
        counts = self._snapshot.source_counts()
        detail = i18n.t("cli.tui.dev.status_separator").join(
            i18n.t("cli.tui.dev.source_count", label=i18n.t(_SOURCE_KEYS[key]), count=counts[key])
            for key in (SOURCE_WORKSPACE, SOURCE_EDITABLE, SOURCE_REGISTRY)
            if counts.get(key)
        )
        if not detail:
            return i18n.t("cli.tui.dev.status_loaded", total=count)
        return i18n.t("cli.tui.dev.status_loaded_detail", total=count, detail=detail)

    def invalidate_cache(self) -> None:
        """使缓存立即失效，下一次读取必定走数据源。"""
        self._loaded_at = 0.0
        self._snapshot = DevSnapshot()

    # endregion

    # region 动作（t / n / Esc）

    def run_tests(self, args: Sequence[str] | None = None) -> None:
        """跑一次 ``akaribot test``；已有动作时不重复启动。

        :param args: 追加到 ``test`` 之后的参数；缺省取输入框内容，留空表示不带参数。
        """
        if not self._action_ready():
            return
        tokens = tuple(args) if args is not None else self.test_args()
        self._start_action(ACTION_TEST, {"args": tokens, "cwd": self._snapshot.workspace_root})

    def open_new_form(self) -> None:
        """展开新建包表单，并把焦点交给名称输入框；动作运行期间不展开。"""
        if self._action_kind:
            self._set_status(i18n.t("cli.tui.dev.status_action_busy", label=_action_label(self._action_kind)))
            return
        self._new_form_open = True
        self._sync_new_kind()
        self._show_new_hint(i18n.t("cli.tui.dev.new_skeleton_hint"))
        self._render_action_panel()
        compat.focus_now(self.query_one("#new-name", compat.Input))

    def close_new_form(self) -> None:
        """收起新建包表单，放弃未提交的输入。"""
        if not self._new_form_open:
            return
        self._new_form_open = False
        self._clear_new_hint()
        self._render_action_panel()
        self.focus_primary()

    def submit_new_form(self) -> None:
        """校验表单后启动 ``akaribot new``；名称非法时只提示，不执行。"""
        if not self._action_ready():
            return
        name = self._input_text("#new-name")
        rejection = _name_rejection(name)
        if rejection:
            self._show_new_hint(rejection, warning=True)
            return
        self._new_form_open = False
        self._clear_new_hint()
        self._start_action(
            ACTION_NEW,
            {
                "name": name,
                "target": self._new_kind,
                "directory": self._input_text("#new-dir"),
                "config": self._switch_value("#new-config"),
                "database": self._switch_value("#new-database"),
                "tests": self._switch_value("#new-tests"),
                "cwd": self._snapshot.workspace_root,
            },
        )
        # 收起表单会把焦点留给隐藏控件，回车或空格随即落到不可见的控件上；交回列表。
        self.focus_primary()

    def toggle_new_kind(self) -> None:
        """在模块与适配器之间切换生成类型；类型二选一，故用二态按钮而不是两个复选框。"""
        self._new_kind = TARGET_ADAPTER if self._new_kind == TARGET_MODULE else TARGET_MODULE
        self._sync_new_kind()

    def _sync_new_kind(self) -> None:
        label_key = (
            "cli.tui.dev.new_kind_adapter" if self._new_kind == TARGET_ADAPTER else "cli.tui.dev.new_kind_module"
        )
        self.query_one("#new-kind", compat.Button).label = i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t(label_key))
        # 适配器脚手架没有 database 与 tests 选项，关掉这两项，免得生成参数被 CLI 拒绝。
        adapter = self._new_kind == TARGET_ADAPTER
        for selector in ("#new-database", "#new-tests"):
            self.query_one(selector, compat.Checkbox).disabled = adapter

    def _switch_value(self, selector: str) -> bool:
        try:
            return bool(self.query_one(selector, compat.Checkbox).value)
        except Exception:  # noqa: BLE001 - 控件缺失时按未勾选处理
            return False

    def cancel_running_action(self) -> None:
        """请求终止正在运行的动作；空闲时不触碰数据源。"""
        if not self._action_kind:
            return
        if self._cancel_requested:
            return
        cancel = getattr(self.source, "cancel_action", None)
        if not callable(cancel):
            self._set_status(i18n.t("cli.tui.dev.status_cancel_unsupported"))
            return
        if not cancel(self._action_kind):
            self._set_status(i18n.t("cli.tui.dev.status_cancel_none"))
            return
        self._cancel_requested = True
        self._set_status(i18n.t("cli.tui.dev.status_cancel_requested", label=_action_label(self._action_kind)))

    def _action_ready(self) -> bool:
        if self._action_kind:
            self._set_status(i18n.t("cli.tui.dev.status_action_busy", label=_action_label(self._action_kind)))
            return False
        if not callable(getattr(self.source, "stream_action", None)):
            self._set_status(i18n.t("cli.tui.dev.status_action_unsupported"))
            return False
        return True

    def _start_action(self, kind: str, params: Mapping[str, Any]) -> None:
        self._action_kind = kind
        self._action_lines = []
        self._action_result = None
        self._cancel_requested = False
        self._render_action_panel()
        self._set_status(self._running_text())
        self.run_worker(self._run_action(kind, dict(params)), group="dev-action", exclusive=True)

    async def _run_action(self, kind: str, params: Mapping[str, Any]) -> None:
        try:
            result = await self.source.stream_action(kind, params, self._on_action_line)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            result = ActionResult(
                message=i18n.t("cli.tui.dev.status_action_error", error=f"{type(error).__name__}: {error}")
            )
        status = self._conclusion_text(kind, result)
        if result.ok and kind == ACTION_NEW:
            # 新包已经落盘，刷新包清单让它出现在列表里；状态栏最后写结论，不被重载覆盖。
            self.invalidate_cache()
            await self._load()
        self._action_kind = ""
        self._action_result = result
        self._set_status(status)
        self._render_action_panel()

    def _on_action_line(self, line: str) -> None:
        self._action_lines.append(line)
        self._render_action_output()
        if self._action_kind:
            self._set_status(self._running_text())

    def _running_text(self) -> str:
        key = (
            "cli.tui.dev.status_test_running" if self._action_kind == ACTION_TEST else "cli.tui.dev.status_new_running"
        )
        return i18n.t(key, count=len(self._action_lines))

    def _conclusion_text(self, kind: str, result: ActionResult) -> str:
        if result.message:
            conclusion = result.message
        elif result.cancelled:
            conclusion = i18n.t("cli.tui.dev.action_cancelled", label=_action_label(kind))
        else:
            key = "cli.tui.dev.status_action_done" if result.ok else "cli.tui.dev.status_action_failed"
            conclusion = i18n.t(key, code=result.returncode)
        if result.ok or not result.detail:
            return conclusion
        return i18n.t("cli.tui.common.error_separator").join((conclusion, _one_line(result.detail)))

    def _show_new_hint(self, message: str, *, warning: bool = False) -> None:
        self._new_hint = message
        style = "bold red" if warning else "dim"
        self.query_one("#new-hint", compat.Static).update(compat.plain_text(message, style=style))
        if warning:
            self._set_status(message)

    def _clear_new_hint(self) -> None:
        self._new_hint = ""
        hint = self._action_widget("#new-hint")
        if hint is not None:
            hint.update(compat.plain_text(""))

    def _input_text(self, selector: str) -> str:
        try:
            return str(self.query_one(selector, compat.Input).value).strip()
        except Exception:  # noqa: BLE001 - 控件缺失时按空输入处理
            return ""

    @staticmethod
    def _split_args(text: str) -> tuple[str, ...]:
        return tuple(text.split())

    # endregion

    # region 渲染（只读缓存）

    def _render_all(self) -> None:
        if not compat.mounted(self):
            return
        list_view = self.query_one("#package-list", compat.ListView)
        inner_width = self._list_inner_width(list_view)
        layout = self._build_layout(inner_width)
        self._header_text = self._compose_row(_column_titles(), layout)
        self.query_one("#columns", compat.Static).update(compat.plain_text(self._header_text))
        cells = [self._row_cells(package) for package in self._snapshot.packages]
        self._package_rows = tuple(cells)
        self._row_texts = tuple(self._compose_row(row, layout) for row in cells)
        list_view.clear()
        if self._row_texts:
            items = [compat.ListItem(compat.Static(text, markup=False)) for text in self._row_texts]
            list_view.extend(items)
        list_view.index = self._index_for_key()
        self._sync_workspace()
        self._sync_detail()
        self._sync_actions()

    def _list_inner_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 76
        return max(outer - 4, 8)

    def _build_layout(self, inner_width: int) -> PackageLayout:
        packages = self._snapshot.packages
        titles = _column_titles()
        name_width = min(
            max(compat.column_width([package.display_name for package in packages] + [titles[0]]), 10),
            NAME_MAX_WIDTH,
        )
        version_width = min(
            max(compat.column_width([package.version or "-" for package in packages] + [titles[2]]), 6),
            VERSION_MAX_WIDTH,
        )
        kind_width = max(KIND_WIDTH, compat.display_width(titles[1]))
        editable_width = max(EDITABLE_WIDTH, compat.display_width(titles[3]))
        source_width = min(
            max(compat.column_width([package.source_label for package in packages] + [titles[4]]), 6),
            SOURCE_MAX_WIDTH,
        )
        for keep_source, keep_path in ((True, True), (True, False), (False, False)):
            widths = [name_width, kind_width, version_width, editable_width]
            if keep_source:
                widths.append(source_width)
            remaining = inner_width - ROW_INDENT - sum(widths) - COLUMN_GAP * len(widths)
            if keep_path and remaining >= MIN_PATH_WIDTH:
                return PackageLayout(name_width, kind_width, version_width, editable_width, source_width, remaining)
            if not keep_path and remaining >= 0:
                return PackageLayout(
                    name_width,
                    kind_width,
                    version_width,
                    editable_width,
                    source_width if keep_source else 0,
                    0,
                )
        budget = max(inner_width - ROW_INDENT - kind_width - editable_width - COLUMN_GAP * 3, 8)
        version_width = min(version_width, 4)
        name_width = max(budget - version_width, 4)
        return PackageLayout(name_width, kind_width, version_width, editable_width, 0, 0)

    def _row_cells(self, package: DevPackage) -> tuple[str, ...]:
        return (
            package.display_name,
            package.kind_label,
            package.version or EMPTY_CELL,
            package.editable_label,
            package.source_label,
            package.path_text,
        )

    def _compose_row(self, cells: Sequence[str], layout: PackageLayout) -> str:
        parts = [compat.fit_cells(value, width) for value, width in zip(cells, layout.widths()) if width > 0]
        return (" " * ROW_INDENT + (" " * COLUMN_GAP).join(parts)).rstrip()

    def _index_for_key(self) -> int:
        if self._selected_key is not None:
            for index, package in enumerate(self._snapshot.packages):
                if package.key == self._selected_key:
                    return index
        return 0

    def _sync_workspace(self) -> None:
        snapshot = self._snapshot
        sources = i18n.t("cli.tui.common.list_separator").join(snapshot.registry_sources) or i18n.t(
            "cli.tui.dev.sources_unset"
        )
        lines = [
            i18n.t(
                "cli.tui.dev.instance_line",
                root=snapshot.instance_root or i18n.t("cli.tui.common.unknown"),
                mode=snapshot.mode_label,
            ),
            i18n.t("cli.tui.dev.workspace_line", workspace=snapshot.workspace_label),
            i18n.t("cli.tui.dev.sources_line", sources=sources),
        ]
        notes = [*snapshot.notes, *snapshot.errors]
        summary = (
            i18n.t("cli.tui.common.error_separator").join(notes)
            if notes
            else i18n.t("cli.tui.dev.packages_installed", total=len(snapshot.packages))
        )
        lines.append(i18n.t("cli.tui.dev.notes_line", notes=summary))
        text = "\n".join(self._fit_page_width(line) for line in lines)
        self._workspace_rendered = text
        self.query_one("#workspace", compat.Static).update(compat.plain_text(text))

    def _fit_page_width(self, text: str) -> str:
        try:
            width = compat.widget_cells(self)[0] - 2
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            width = 78
        return compat.truncate_cells(text, max(width, 8))

    def _sync_detail(self) -> None:
        package = self.selected_package
        if package is None:
            key = "cli.tui.dev.detail_hint_select" if self._snapshot.packages else "cli.tui.dev.detail_empty"
            text = i18n.t(key)
            self._detail_rendered = text
            self.query_one("#detail", compat.Static).update(compat.plain_text(text))
            return
        self._selected_key = package.key
        first = i18n.t(
            "cli.tui.dev.detail_first",
            dist=package.dist,
            source=package.source_label,
            path=package.path or i18n.t("cli.tui.dev.path_outside_workspace"),
        )
        provides = i18n.t("cli.tui.common.list_separator").join(package.provides_modules) or i18n.t(
            "cli.tui.common.none"
        )
        second = i18n.t(
            "cli.tui.dev.detail_second",
            version=package.version or i18n.t("cli.tui.common.unknown"),
            editable=package.editable_label,
            core_api=package.requires_core_api or i18n.t("cli.tui.common.undeclared"),
            provides=provides,
        )
        text = f"{self._fit_page_width(first)}\n{self._fit_page_width(second)}"
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _sync_actions(self) -> None:
        running = bool(self._action_kind)
        self.query_one("#refresh", compat.Button).disabled = self._busy
        self.query_one("#run-tests", compat.Button).disabled = running
        self.query_one("#new-package", compat.Button).disabled = running

    def _render_action_panel(self) -> None:
        # 表单与输出区互斥：表单占位时收起输出，动作跑起来后表单已经关闭。
        form = self._action_widget("#new-form")
        if form is not None:
            form.display = self._new_form_open
        output = self._action_widget("#action-output")
        if output is not None:
            output.display = bool(self._action_kind or self._action_lines)
        self._render_action_output()
        self._sync_actions()

    def _render_action_output(self) -> None:
        self._action_rendered = "\n".join(self._action_lines[-ACTION_OUTPUT_LINES:])
        output = self._action_widget("#action-output")
        if output is None:
            return
        lines = self._action_rendered.split("\n") if self._action_rendered else [i18n.t("cli.tui.dev.output_waiting")]
        output.update(compat.plain_text("\n".join(self._fit_page_width(line) for line in lines)))

    def _action_widget(self, selector: str) -> compat.Widget | None:
        try:
            return self.query_one(selector)
        except Exception:  # noqa: BLE001 - 未挂载时按无控件处理
            return None

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        self.query_one("#status", compat.Static).update(compat.plain_text(self._fit_page_width(text)))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新取数。"""
        if self._snapshot.packages or self._loaded_at:
            self._render_all()

    # endregion

    # region 交互

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        self._sync_detail()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "refresh":
            self.refresh_snapshot(force=True)
        elif button_id == "run-tests":
            self.run_tests()
        elif button_id == "new-package":
            self.open_new_form()
        elif button_id == "new-kind":
            self.toggle_new_kind()
        elif button_id == "new-confirm":
            self.submit_new_form()
        elif button_id == "new-close":
            self.close_new_form()

    @compat.on(compat.Input.Submitted, "#new-name")
    def _on_new_name_submitted(self, event: compat.Input.Submitted) -> None:
        self.submit_new_form()

    @compat.on(compat.Input.Submitted, "#test-path")
    def _on_test_path_submitted(self, event: compat.Input.Submitted) -> None:
        self.run_tests()

    def focus_primary(self) -> None:
        """把焦点交给包列表；列表为空时退到页面容器。"""
        compat.focus_first(self, "#package-list")

    def action_refresh(self) -> None:
        """键位动作：强制重新读取。"""
        self.refresh_snapshot(force=True)

    def action_run_tests(self) -> None:
        """键位动作：运行测试。"""
        self.run_tests()

    def action_new_package(self) -> None:
        """键位动作：展开新建包表单，已展开时把焦点交回名称输入框。"""
        self.open_new_form()

    def action_cancel_action(self) -> None:
        """键位动作：终止运行中的动作；空闲时收起新建包表单。"""
        if self._action_kind:
            self.cancel_running_action()
        elif self._new_form_open:
            self.close_new_form()

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: bool(self._action_kind))
