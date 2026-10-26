"""文档页：文档包浏览、构建、预览与部署。

数据通过 :class:`DocsSource` 读取，写操作经 ``akaribot docs ...`` 子进程执行。
预览服务以子进程形式运行，离开页面、卸载或退出时终止。
"""

from __future__ import annotations

import asyncio
import atexit
import json
import subprocess
import time
import webbrowser
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context
from akaribot.cli.tui.modules import OperationResult

QUERY_TIMEOUT_SECONDS = 120.0
ACTION_TIMEOUT_SECONDS = 1800.0
SERVE_READY_SECONDS = 60.0
SERVE_STOP_SECONDS = 10.0
DEFAULT_PREVIEW_URL = "http://127.0.0.1:4173/"
OUTPUT_LIMIT = 600

CHOICE_DRY_RUN = "dry"
CHOICE_DEPLOY = "deploy"


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return str(value).strip()


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _tail(text: str | None, limit: int = OUTPUT_LIMIT) -> str:
    return (text or "").strip()[-limit:]


@dataclass(frozen=True)
class DocsPageRow:
    """文档包中的一个页面。

    :param path: 相对包文档目录的路径。
    :param title: 侧栏标题。
    :param order: 排序权重。
    :param description: 一句话说明。
    """

    path: str
    title: str = ""
    order: int = 500
    description: str = ""

    @property
    def display_title(self) -> str:
        """返回页面标题，缺省时使用路径。"""
        return self.title or self.path


@dataclass(frozen=True)
class DocsPackageRow:
    """一个提供文档的包。

    :param key: URL 与目录使用的唯一短名。
    :param group: 分组。
    :param dist: 分发名。
    :param version: 已装版本。
    :param title: 展示标题。
    :param summary: 一句话简介。
    :param pages: 页面清单。
    :param doc_path: 包内文档目录。
    :param editable: 是否为可编辑安装。
    :param order: 排序权重。
    """

    key: str
    group: str = ""
    dist: str = ""
    version: str = ""
    title: str = ""
    summary: str = ""
    pages: tuple[DocsPageRow, ...] = ()
    doc_path: str = ""
    editable: bool = False
    order: int = 500

    @property
    def display_title(self) -> str:
        """返回展示标题，缺省时使用 key。"""
        return self.title or self.key

    def haystack(self) -> str:
        """返回搜索用的匹配文本，已做大小写折叠。"""
        parts = [self.key, self.group, self.dist, self.title, self.summary, self.version]
        parts.extend(page.title for page in self.pages)
        return " ".join(part for part in parts if part).casefold()

    def matches(self, query: str) -> bool:
        """按空白分词的子串匹配，全部词命中才算匹配。

        :param query: 搜索词。
        :return: 是否命中。
        """
        tokens = query.casefold().split()
        if not tokens:
            return True
        haystack = self.haystack()
        return all(token in haystack for token in tokens)


@dataclass(frozen=True)
class ToolchainInfo:
    """Node.js 与 npm 的探测结果。

    :param node: node 可执行文件路径。
    :param npm: npm 可执行文件路径。
    :param node_version: node 版本。
    :param npm_version: npm 版本。
    :param ready: 是否满足构建要求。
    :param detail: 版本摘要或不可用的原因。
    """

    node: str = ""
    npm: str = ""
    node_version: str = ""
    npm_version: str = ""
    ready: bool = True
    detail: str = ""


@dataclass(frozen=True)
class DocsView:
    """一次文档快照。

    :param packages: 文档包清单。
    :param toolchain: 构建工具链状态。
    :param config: 文档配置摘要。
    :param build: 最近一次构建记录。
    :param deploys: 最近的部署记录。
    :param warnings: 目录构建期间的降级说明。
    """

    packages: tuple[DocsPackageRow, ...] = ()
    toolchain: ToolchainInfo = field(default_factory=ToolchainInfo)
    config: Mapping[str, Any] = field(default_factory=dict)
    build: Mapping[str, Any] | None = None
    deploys: tuple[Mapping[str, Any], ...] = ()
    warnings: tuple[str, ...] = ()


def _page_from(value: Any) -> DocsPageRow:
    if isinstance(value, str):
        return DocsPageRow(path=value)
    info = _mapping(value)
    path = _text(info.get("path"))
    try:
        order = int(info.get("order", 500))
    except (TypeError, ValueError):
        order = 500
    return DocsPageRow(
        path=path,
        title=_text(info.get("title")),
        order=order,
        description=_text(info.get("description")),
    )


def _package_from(value: Any) -> DocsPackageRow:
    info = _mapping(value)
    pages = tuple(_page_from(item) for item in info.get("pages") or () if item)
    try:
        order = int(info.get("order", 500))
    except (TypeError, ValueError):
        order = 500
    editable = info.get("editable")
    return DocsPackageRow(
        key=_text(info.get("key")),
        group=_text(info.get("group")),
        dist=_text(info.get("dist")),
        version=_text(info.get("version")),
        title=_text(info.get("title")),
        summary=_text(info.get("summary")),
        pages=pages,
        doc_path=_text(info.get("doc_path")),
        editable=bool(editable) if isinstance(editable, bool) else _text(editable).casefold() in {"1", "true", "yes"},
        order=order,
    )


def normalize_view(payload: Any) -> DocsView:
    """把 ``docs list --json`` 的输出归一化为视图。

    :param payload: ``json.loads`` 的结果。
    :return: 归一化后的视图。
    """
    info = _mapping(payload)
    toolchain = _mapping(info.get("toolchain"))
    packages = tuple(_package_from(item) for item in info.get("packages") or () if item)
    builds = info.get("build")
    deploys = tuple(_mapping(item) for item in info.get("deploys") or () if isinstance(item, Mapping))
    warnings = tuple(text for item in info.get("warnings") or () if (text := _text(item)))
    return DocsView(
        packages=packages,
        toolchain=ToolchainInfo(
            node=_text(toolchain.get("node")),
            npm=_text(toolchain.get("npm")),
            node_version=_text(toolchain.get("node_version")),
            npm_version=_text(toolchain.get("npm_version")),
            ready=bool(toolchain.get("ready")),
            detail=_text(toolchain.get("detail")),
        ),
        config=_mapping(info.get("config")),
        build=_mapping(builds) if isinstance(builds, Mapping) else None,
        deploys=deploys,
        warnings=warnings,
    )


class DocsSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


@runtime_checkable
class DocsSource(Protocol):
    """文档数据源接口；测试注入替身，实际运行通过子进程访问。"""

    def load(self) -> DocsView:
        """返回文档包、工具链与最近状态。"""

    def build(self, keys: Sequence[str]) -> OperationResult:
        """构建指定包；``keys`` 为空时构建全部。"""

    async def start_server(self) -> str:
        """启动预览服务并返回站点 URL。"""

    async def stop_server(self) -> None:
        """停止预览服务。"""

    def deploy(self, provider: str | None, dry_run: bool) -> OperationResult:
        """部署站点；``dry_run`` 为真时只统计将更改的文件。"""


class StaticDocsSource:
    """固定数据的替身数据源，供自动化断言与自检使用，不产生任何子进程。

    :param view: ``load`` 直接返回的视图。
    :param build_result: 构建返回值；默认按包数量返回成功。
    :param deploy_result: 部署返回值；默认按部署方式返回成功。
    :param url: 预览服务返回的地址。
    :param serve_error: 非空时 ``start_server`` 抛出该错误。
    """

    def __init__(
        self,
        view: DocsView | None = None,
        *,
        build_result: OperationResult | None = None,
        deploy_result: OperationResult | None = None,
        url: str = DEFAULT_PREVIEW_URL,
        serve_error: str = "",
    ) -> None:
        self._view = view or DocsView()
        self._build_result = build_result
        self._deploy_result = deploy_result
        self.url = url
        self.serve_error = serve_error
        self.calls = {"load": 0, "build": 0, "serve": 0, "stop": 0, "deploy": 0}
        self.build_keys: list[tuple[str, ...]] = []
        self.deploys: list[tuple[str | None, bool]] = []
        self.serving = False

    @property
    def server_running(self) -> bool:
        """返回预览服务是否处于运行状态。"""
        return self.serving

    def set_view(self, view: DocsView) -> None:
        """替换替身返回的视图。"""
        self._view = view

    def load(self) -> DocsView:
        """见 :meth:`DocsSource.load`。"""
        self.calls["load"] += 1
        return self._view

    def build(self, keys: Sequence[str]) -> OperationResult:
        """见 :meth:`DocsSource.build`。"""
        self.calls["build"] += 1
        self.build_keys.append(tuple(keys))
        if self._build_result is not None:
            return self._build_result
        count = len(keys) or len(self._view.packages)
        return OperationResult(True, i18n.t("cli.tui.docs.build_done", count=count, duration=0), "stub")

    async def start_server(self) -> str:
        """见 :meth:`DocsSource.start_server`。"""
        self.calls["serve"] += 1
        if self.serve_error:
            raise DocsSourceError(self.serve_error)
        self.serving = True
        return self.url

    async def stop_server(self) -> None:
        """见 :meth:`DocsSource.stop_server`。"""
        self.calls["stop"] += 1
        self.serving = False

    def deploy(self, provider: str | None, dry_run: bool) -> OperationResult:
        """见 :meth:`DocsSource.deploy`。"""
        self.calls["deploy"] += 1
        self.deploys.append((provider, dry_run))
        if self._deploy_result is not None:
            return self._deploy_result
        if dry_run:
            message = i18n.t("cli.docs.deploy.dry_run", uploaded=0, deleted=0, skipped=0)
            return OperationResult(True, message, "stub")
        return OperationResult(True, i18n.t("cli.tui.docs.deploy_done", detail=self.url), "stub")


class SubprocessDocsSource:
    """通过 ``akaribot docs ...`` 子进程读取状态并执行操作。

    :param root: 实例根；默认按 ``AKARI_INSTANCE_DIR`` 与向上查找定位。
    :param query_timeout: 查询类调用的秒数上限。
    :param action_timeout: 构建与部署的秒数上限。
    :param serve_timeout: 等待预览服务就绪的秒数上限。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        query_timeout: float = QUERY_TIMEOUT_SECONDS,
        action_timeout: float = ACTION_TIMEOUT_SECONDS,
        serve_timeout: float = SERVE_READY_SECONDS,
        runner: Any | None = None,
    ) -> None:
        # 每次请求都解析当前实例，确保切换实例后子进程使用新目录。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.query_timeout = query_timeout
        self.action_timeout = action_timeout
        self.serve_timeout = serve_timeout
        self.calls = {"load": 0, "build": 0, "serve": 0, "stop": 0, "deploy": 0}
        self._runner = runner or subprocess.run
        self._process: asyncio.subprocess.Process | None = None
        self._atexit_registered = False

    @property
    def root(self) -> Path:
        """返回实例根目录，依次采用显式路径、当前实例或自动定位结果。"""
        return context.resolve_root(self._root_override)

    @property
    def server_running(self) -> bool:
        """返回预览服务子进程是否仍在运行。"""
        process = self._process
        return process is not None and process.returncode is None

    def load(self) -> DocsView:
        """见 :meth:`DocsSource.load`。"""
        self.calls["load"] += 1
        payload = self._invoke(("docs", "list", "--json"), timeout=self.query_timeout)
        return normalize_view(payload)

    def build(self, keys: Sequence[str]) -> OperationResult:
        """见 :meth:`DocsSource.build`；``--json`` 输出构建摘要。"""
        self.calls["build"] += 1
        argv = ["docs", "build", "--json"]
        for key in keys:
            argv += ["--package", str(key)]
        return self._action(argv, self.action_timeout, "build")

    def deploy(self, provider: str | None, dry_run: bool) -> OperationResult:
        """见 :meth:`DocsSource.deploy`；界面已确认，子进程带 ``--yes``。"""
        self.calls["deploy"] += 1
        argv = ["docs", "deploy", "--json", "--yes"]
        if provider:
            argv += ["--provider", provider]
        if dry_run:
            argv.append("--dry-run")
        return self._action(argv, self.action_timeout, "deploy")

    async def start_server(self) -> str:
        """启动 ``docs serve --json --no-build`` 并等待首行就绪事件。"""
        argv = cli_process.cli_argv("docs", "serve", "--json", "--no-build", "--port", "0")
        self.calls["serve"] += 1
        try:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(self.root),
                stdin=subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_exe_missing", path=argv[0], error=error)) from error
        except OSError as error:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_oserror", cmd=" ".join(argv), error=error)) from error
        self._process = process
        self._register_exit_hook()
        stream = process.stdout
        try:
            raw = await asyncio.wait_for(
                stream.readline() if stream is not None else _empty(), timeout=self.serve_timeout
            )
        except TimeoutError:
            await self._terminate(process)
            self._process = None
            raise DocsSourceError(i18n.t("cli.tui.docs.src_serve_timeout", seconds=f"{self.serve_timeout:g}")) from None
        line = raw.decode("utf-8", errors="replace").strip()
        url = ""
        if line:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                event = None
            if isinstance(event, Mapping) and event.get("event") == "ready":
                url = _text(event.get("url"))
        if not url:
            detail = await self._drain_stderr(process)
            code = await process.wait()
            self._process = None
            raise DocsSourceError(
                i18n.t(
                    "cli.tui.docs.src_serve_exit",
                    code=code,
                    detail=detail or line or i18n.t("cli.tui.common.no_output"),
                )
            )
        return url

    async def stop_server(self) -> None:
        """见 :meth:`DocsSource.stop_server`；先终止，超时后强制结束。"""
        self.calls["stop"] += 1
        process = self._process
        self._process = None
        if process is None or process.returncode is not None:
            return
        await self._terminate(process)

    def _register_exit_hook(self) -> None:
        # 界面异常退出时事件循环可能先关闭，进程必须在解释器退出前终止。
        if self._atexit_registered:
            return
        self._atexit_registered = True
        atexit.register(self._terminate_at_exit)

    def _terminate_at_exit(self) -> None:
        process = self._process
        if process is not None and process.returncode is None:
            process.terminate()

    async def _terminate(self, process: asyncio.subprocess.Process) -> None:
        if process.returncode is not None:
            return
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=SERVE_STOP_SECONDS)
        except TimeoutError:
            process.kill()
            await process.wait()

    @staticmethod
    async def _drain_stderr(process: asyncio.subprocess.Process) -> str:
        stream = process.stderr
        if stream is None:
            return ""
        try:
            raw = await asyncio.wait_for(stream.read(), timeout=5.0)
        except TimeoutError:
            return ""
        return _tail(raw.decode("utf-8", errors="replace"))

    def _invoke(self, args: Sequence[str], *, timeout: float) -> Mapping[str, Any]:
        argv = cli_process.cli_argv(*args)
        try:
            completed = self._runner(
                list(argv),
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=self._env(),
            )
        except FileNotFoundError as error:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise DocsSourceError(
                i18n.t("cli.tui.docs.src_timeout", cmd=" ".join(args), seconds=f"{timeout:g}")
            ) from error
        except OSError as error:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_oserror", cmd=" ".join(args), error=error)) from error
        if completed.returncode != 0:
            raise DocsSourceError(
                i18n.t(
                    "cli.tui.docs.src_exit_code",
                    cmd=" ".join(args),
                    code=completed.returncode,
                    tail=_tail(completed.stderr),
                )
            )
        payload = self._parse(completed.stdout, " ".join(args))
        return payload

    def _action(self, args: Sequence[str], timeout: float, kind: str) -> OperationResult:
        argv = cli_process.cli_argv(*args)
        fail_key = "cli.tui.docs.build_failed" if kind == "build" else "cli.tui.docs.deploy_failed"
        try:
            completed = self._runner(
                list(argv),
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=self._env(),
            )
        except subprocess.TimeoutExpired:
            return OperationResult(
                False,
                i18n.t(fail_key, detail=i18n.t("cli.tui.docs.src_timeout", cmd=" ".join(args), seconds=f"{timeout:g}")),
            )
        except OSError as error:
            return OperationResult(
                False,
                i18n.t(fail_key, detail=f"{type(error).__name__}: {error}"),
            )
        if completed.returncode != 0:
            detail = _tail(completed.stderr) or _tail(completed.stdout) or i18n.t("cli.tui.common.no_output")
            return OperationResult(False, i18n.t(fail_key, detail=detail), detail)
        try:
            payload = self._parse(completed.stdout, " ".join(args))
        except DocsSourceError as error:
            return OperationResult(False, i18n.t(fail_key, detail=str(error)), str(error))
        if kind == "build":
            packages = payload.get("packages")
            count = len(packages) if isinstance(packages, (list, tuple)) else 0
            try:
                duration = int(payload.get("duration_ms") or 0)
            except (TypeError, ValueError):
                duration = 0
            return OperationResult(
                True,
                i18n.t("cli.tui.docs.build_done", count=count, duration=duration),
                _tail(_text(payload.get("log"))),
            )
        if bool(payload.get("dry_run")):
            message = i18n.t(
                "cli.docs.deploy.dry_run",
                uploaded=payload.get("uploaded", 0),
                deleted=payload.get("deleted", 0),
                skipped=payload.get("skipped", 0),
            )
            return OperationResult(True, message, _tail(_text(payload.get("detail"))))
        detail = _text(payload.get("url")) or _text(payload.get("detail")) or payload.get("provider", "")
        return OperationResult(
            True, i18n.t("cli.tui.docs.deploy_done", detail=detail), _tail(_text(payload.get("detail")))
        )

    def _parse(self, stdout: str, label: str) -> Mapping[str, Any]:
        text = (stdout or "").strip()
        if not text:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_empty_output", label=label))
        try:
            payload = json.loads(text.splitlines()[-1])
        except json.JSONDecodeError as error:
            raise DocsSourceError(i18n.t("cli.tui.docs.src_bad_json", label=label, error=error)) from error
        if not isinstance(payload, Mapping):
            raise DocsSourceError(i18n.t("cli.tui.docs.src_bad_json", label=label, error="not an object"))
        return payload

    def _env(self) -> dict[str, str]:
        return cli_process.cli_env(self.root)


async def _empty() -> bytes:
    return b""


@dataclass(frozen=True)
class DocsLayout:
    """文档列表的列宽计划。

    :param key_width: key 列宽。
    :param version_width: 版本列宽。
    :param title_width: 标题列宽。
    :param group_width: 分组列宽；``0`` 表示本屏没有这一列。
    """

    key_width: int
    version_width: int
    title_width: int
    group_width: int


class DocsPage(compat.Vertical):
    """文档页控件。

    :param source: 数据源，默认为 :class:`SubprocessDocsSource`。
    :param cache_ttl: 缓存有效期秒数；构建成功后立即标记站点可用。
    """

    # 页脚只保留高频键；部署与打开浏览器等低频动作由按钮与详情提示承载。
    BINDINGS = compat.bindings(
        ("r", "refresh", i18n.t("cli.tui.docs.action_refresh")),
        ("slash", "focus_search", i18n.t("cli.tui.docs.bind_search")),
        ("space", "toggle_select", i18n.t("cli.tui.docs.bind_toggle")),
        ("b", "build", i18n.t("cli.tui.docs.action_build")),
        ("s", "serve", i18n.t("cli.tui.docs.action_serve")),
        ("o", "open", i18n.t("cli.tui.docs.action_open"), False),
        ("a", "select_all", i18n.t("cli.tui.docs.bind_select_all"), False),
        ("c", "clear_selection", i18n.t("cli.tui.docs.bind_clear"), False),
        ("ctrl+p", "deploy", i18n.t("cli.tui.docs.action_deploy"), False),
        ("escape", "clear_search", i18n.t("cli.tui.docs.bind_clear_search"), False),
    )

    can_focus = True

    DEFAULT_CSS = """
    DocsPage {
        layout: vertical;
        height: 1fr;
    }
    DocsPage #search-row {
        height: 3;
        align-vertical: middle;
    }
    DocsPage #search {
        width: 1fr;
        min-width: 16;
    }
    DocsPage #count {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DocsPage #body {
        height: 1fr;
    }
    DocsPage #list-pane {
        width: 44%;
        min-width: 28;
    }
    DocsPage #columns {
        height: 1;
        padding: 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DocsPage #docs-list {
        height: 1fr;
        border: round $primary;
    }
    DocsPage #docs-list > ListItem {
        padding: 0 1;
    }
    DocsPage #docs-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    DocsPage #detail-pane {
        width: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    DocsPage #detail {
        width: 1fr;
    }
    DocsPage #actions {
        height: auto;
        padding: 0 0 0 1;
    }
    DocsPage #actions Button {
        min-width: 0;
    }
    DocsPage #status {
        height: 1;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    def __init__(
        self,
        source: DocsSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: DocsSource = source if source is not None else SubprocessDocsSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = ""
        self._view: DocsView | None = None
        self._loaded_at: float = 0.0
        self._query: str = ""
        self._selected_key: str | None = None
        self._selected: set[str] = set()
        self._busy = False
        self._serving = False
        self._url = ""
        self._built = False
        self._confirm = compat.PendingConfirm()
        self._rendered_rows: tuple[str, ...] = ()
        self._columns_rendered: str = ""
        self._detail_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.docs.status_ready")

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树。"""
        with compat.Horizontal(id="search-row"):
            yield compat.Input(placeholder=i18n.t("cli.tui.docs.search_placeholder"), id="search")
        yield compat.Static(i18n.t("cli.tui.docs.status_loading"), id="count", markup=False)
        with compat.Horizontal(id="body"):
            with compat.Vertical(id="list-pane"):
                yield compat.Static("", id="columns", markup=False)
                yield compat.ListView(id="docs-list")
            with compat.VerticalScroll(id="detail-pane"):
                yield compat.Static(i18n.t("cli.tui.docs.detail_placeholder"), id="detail", markup=False)
        yield compat.ButtonFlow(
            ("build", i18n.t("cli.tui.docs.action_build"), "primary"),
            ("serve", i18n.t("cli.tui.docs.action_serve")),
            ("stop", i18n.t("cli.tui.docs.action_stop")),
            ("open", i18n.t("cli.tui.docs.action_open")),
            ("deploy", i18n.t("cli.tui.docs.action_deploy")),
            ("refresh", i18n.t("cli.tui.docs.action_refresh")),
            breaks=("stop",),
            id="actions",
        )
        yield compat.Static(i18n.t("cli.tui.docs.status_ready"), id="status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；读取数据推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取文档目录。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_view(force=True)

    def focus_primary(self) -> None:
        """聚焦包列表；列表为空时聚焦页面容器，以保留全局键位。"""
        compat.focus_first(self, "#docs-list")

    # region 状态读取（供测试与 App 使用）

    @property
    def view(self) -> DocsView | None:
        """返回最近一次读取的视图，不触发子进程。"""
        return self._view

    @property
    def packages(self) -> tuple[DocsPackageRow, ...]:
        """返回缓存中的全部文档包。"""
        return self._view.packages if self._view else ()

    @property
    def visible_packages(self) -> tuple[DocsPackageRow, ...]:
        """返回应用当前搜索词后的文档包。"""
        packages = self.packages
        if not self._query.strip():
            return packages
        return tuple(package for package in packages if package.matches(self._query))

    @property
    def selected_package(self) -> DocsPackageRow | None:
        """返回列表当前高亮项对应的文档包。"""
        packages = self.visible_packages
        if not packages:
            return None
        try:
            list_view = self.query_one("#docs-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时按无选中处理
            return None
        index = compat.highlighted_index(list_view)
        if index is None or index >= len(packages):
            return None
        return packages[index]

    @property
    def selected_keys(self) -> tuple[str, ...]:
        """返回当前选中的包 key，按视图顺序排列。"""
        return tuple(package.key for package in self.packages if package.key in self._selected)

    @property
    def search_query(self) -> str:
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
    def preview_url(self) -> str:
        """返回运行中的预览服务地址；未运行时为空串。"""
        return self._url if self._serving else ""

    @property
    def server_running(self) -> bool:
        """返回预览服务是否处于运行状态。"""
        return self._serving

    def row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的列表行文本，供自动化断言核对宽度。"""
        return self._rendered_rows

    def column_text(self) -> str:
        """返回最近一次渲染出的表头文本。"""
        return self._columns_rendered

    # endregion

    # region 数据读取

    def refresh_view(self, *, force: bool = False) -> None:
        """读取文档目录。

        :param force: 为 ``True`` 时忽略缓存。
        """
        # 刷新可能改变目标集合，必须清除待确认状态。
        self._confirm.reset()
        if not force and self._view is not None and self._cache_age() < self.cache_ttl:
            self._render_list()
            self._set_status(i18n.t("cli.tui.docs.status_cached", age=f"{self._cache_age():.1f}"))
            return
        self._set_status(i18n.t("cli.tui.docs.status_loading"))
        self.run_worker(self._load(), group="docs-load", exclusive=True)

    def _cache_age(self) -> float:
        if not self._loaded_at:
            return float("inf")
        return max(0.0, time.monotonic() - self._loaded_at)

    async def _load(self) -> bool:
        try:
            view = await asyncio.to_thread(self.source.load)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._view = None
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_list()
            self._set_status(i18n.t("cli.tui.docs.status_load_failed", error=self.last_error))
            self._sync_actions()
            return False
        self._view = view
        self._loaded_at = time.monotonic()
        self.last_error = ""
        known = {package.key for package in view.packages}
        self._selected &= known
        if self._selected_key not in known:
            self._selected_key = None
        # 构建记录存在即视为已有可预览站点；本会话内的成功构建另由 _built 标记。
        self._built = self._built or view.build is not None
        self.last_result = i18n.t("cli.tui.docs.status_loaded", count=len(view.packages))
        self._render_list()
        self._set_status(self.last_result)
        if self.display and self.app.focused is self:
            self.focus_primary()
        return True

    def _is_built(self) -> bool:
        build = self._view.build if self._view else None
        return self._built or build is not None

    # endregion

    # region 渲染（只读缓存）

    def _list_inner_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 36
        return max(outer - 4, 8)

    def _layout(self, inner_width: int) -> DocsLayout:
        packages = self.visible_packages
        key_width = max(min(compat.column_width(package.key for package in packages), 18, inner_width - 16), 6)
        version_width = min(max(compat.column_width(package.version or "-" for package in packages), 5), 8)
        group_width = min(compat.column_width(package.group for package in packages), 10)
        fixed = 2 + key_width + 1 + version_width + 1 + 4 + 1
        title_width = max(inner_width - fixed, 0)
        if group_width and title_width - group_width - 1 >= 8:
            title_width -= group_width + 1
        else:
            group_width = 0
        if title_width < 6:
            key_width = max(inner_width - (2 + version_width + 1 + 4 + 1 + 1), 4)
            fixed = 2 + key_width + 1 + version_width + 1 + 4 + 1
            title_width = max(inner_width - fixed, 0)
        return DocsLayout(key_width, version_width, title_width, group_width)

    def _row_text(self, package: DocsPackageRow, layout: DocsLayout) -> str:
        marked = "✓" if package.key in self._selected else " "
        version = compat.fit_cells(package.version or "-", layout.version_width)
        pages_cell = f"{len(package.pages):>3}"
        title = compat.truncate_cells(package.display_title, layout.title_width)
        key = compat.fit_cells(package.key, layout.key_width)
        row = f"{marked} {key} {version} {pages_cell} {title}"
        if layout.group_width:
            row = f"{row} {compat.fit_cells(package.group or '-', layout.group_width)}"
        return row.rstrip()

    def _render_list(self) -> None:
        packages = self.visible_packages
        try:
            list_view = self.query_one("#docs-list", compat.ListView)
        except Exception:  # noqa: BLE001 - 未挂载时跳过渲染
            return
        inner_width = self._list_inner_width(list_view)
        layout = self._layout(inner_width)
        rows = [self._row_text(package, layout) for package in packages]
        self._render_columns(layout, inner_width)
        compat.rebuild_rows(list_view, rows, self._index_for_key(packages))
        self._rendered_rows = tuple(rows)
        self._sync_count(packages)
        self._sync_detail()
        self._sync_actions()

    def _render_columns(self, layout: DocsLayout, inner_width: int) -> None:
        # 表头与数据行共用列宽计划，保证窄屏隐藏分组列后仍对齐。
        cells = [
            f"  {compat.fit_cells(i18n.t('cli.tui.docs.column_key'), layout.key_width)}",
            compat.fit_cells(i18n.t("cli.tui.docs.column_version"), layout.version_width),
            f"{i18n.t('cli.tui.docs.column_pages'):>3}",
            compat.fit_cells(i18n.t("cli.tui.docs.column_title"), layout.title_width),
        ]
        if layout.group_width:
            cells.append(compat.fit_cells(i18n.t("cli.tui.docs.column_group"), layout.group_width))
        text = compat.truncate_cells(" ".join(cells), inner_width).rstrip()
        self._columns_rendered = text
        self.query_one("#columns", compat.Static).update(compat.plain_text(text))

    def _index_for_key(self, packages: Sequence[DocsPackageRow]) -> int:
        if not packages:
            return 0
        if self._selected_key is not None:
            for index, package in enumerate(packages):
                if package.key == self._selected_key:
                    return index
        return 0

    def _sync_count(self, packages: Sequence[DocsPackageRow]) -> None:
        text = i18n.t("cli.tui.docs.count", shown=len(packages), total=len(self.packages))
        if self._selected:
            text = f"{text}{i18n.t('cli.common.clause_separator')}{i18n.t('cli.tui.docs.selected', count=len(self._selected))}"
        self.query_one("#count", compat.Static).update(compat.plain_text(text))

    def _build_text(self) -> str:
        build = self._view.build if self._view else None
        if not build:
            return i18n.t("cli.tui.common.none")
        at = _text(build.get("generated_at")) or i18n.t("cli.tui.common.unknown")
        packages = build.get("packages")
        count = len(packages) if isinstance(packages, (list, tuple)) else 0
        return i18n.t("cli.tui.docs.build_value", at=at, count=count)

    def _deploy_text(self) -> str:
        deploys = self._view.deploys if self._view else ()
        if not deploys:
            return i18n.t("cli.tui.common.none")
        latest = deploys[-1]
        at = _text(latest.get("at")) or i18n.t("cli.tui.common.unknown")
        target = _text(latest.get("target")) or "-"
        status = _text(latest.get("status")) or "-"
        return i18n.t("cli.tui.docs.deploy_value", at=at, target=target, status=status)

    def _toolchain_text(self) -> str:
        info = self._view.toolchain if self._view else None
        if info is None:
            return i18n.t("cli.tui.common.unknown")
        if not info.ready:
            return i18n.t("cli.tui.docs.toolchain_missing", detail=info.detail or info.node or "-")
        return i18n.t("cli.tui.docs.toolchain_ready", node=info.node_version or "-", npm=info.npm_version or "-")

    def _sync_detail(self) -> None:
        package = self.selected_package
        if package is None:
            if not self.packages:
                hint = i18n.t("cli.tui.docs.empty")
            elif not self.visible_packages:
                hint = i18n.t("cli.tui.docs.no_match")
            else:
                hint = i18n.t("cli.tui.docs.detail_placeholder")
            self._detail_rendered = hint
            self.query_one("#detail", compat.Static).update(compat.plain_text(hint))
            return
        self._selected_key = package.key
        none = i18n.t("cli.tui.common.none")
        rows = [
            (i18n.t("cli.tui.docs.field_title"), package.display_title),
            (i18n.t("cli.tui.docs.field_summary"), package.summary or none),
            (i18n.t("cli.tui.docs.field_dist"), package.dist or none),
            (i18n.t("cli.tui.docs.version"), package.version or i18n.t("cli.tui.common.unknown")),
            (i18n.t("cli.tui.docs.group"), package.group or i18n.t("cli.tui.common.undeclared")),
            (i18n.t("cli.tui.docs.pages"), i18n.t("cli.tui.docs.page_count", count=len(package.pages))),
            (i18n.t("cli.tui.docs.doc_path"), package.doc_path or none),
            (
                i18n.t("cli.tui.docs.editable"),
                i18n.t("cli.tui.docs.yes") if package.editable else i18n.t("cli.tui.docs.no"),
            ),
            (i18n.t("cli.tui.docs.build_state"), self._build_text()),
            (i18n.t("cli.tui.docs.deploy_state"), self._deploy_text()),
            (i18n.t("cli.tui.docs.toolchain"), self._toolchain_text()),
        ]
        lines = compat.align_rows(rows, gap=2)
        lines.append("")
        if package.pages:
            lines.append(i18n.t("cli.tui.docs.pages_list", count=len(package.pages)))
            for page in package.pages:
                lines.append("  " + i18n.t("cli.tui.docs.page_line", title=page.display_title, path=page.path))
        else:
            lines.append(i18n.t("cli.tui.docs.no_pages"))
        warnings = self._view.warnings if self._view else ()
        if warnings:
            lines.append("")
            lines.extend(i18n.t("cli.tui.docs.warning", message=message) for message in warnings)
        lines.append("")
        lines.append(i18n.t("cli.tui.docs.detail_keys"))
        text = "\n".join(lines)
        self._detail_rendered = text
        self.query_one("#detail", compat.Static).update(compat.plain_text(text))

    def _sync_actions(self) -> None:
        try:
            for button_id in ("build", "serve", "deploy", "refresh"):
                self.query_one(f"#{button_id}", compat.Button).disabled = self._busy
            self.query_one("#stop", compat.Button).disabled = self._busy or not self._serving
            self.query_one("#open", compat.Button).disabled = self._busy or not self._serving
            self.query_one("#actions", compat.ButtonFlow).relayout()
        except Exception:  # noqa: BLE001 - 尚未挂载时没有按钮可更新
            return

    def _set_status(self, text: str) -> None:
        self._status_rendered = text
        self.last_result = text
        self.query_one("#status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排，不重新读取数据。"""
        if self._view is not None:
            self._render_list()

    # endregion

    # region 交互

    @compat.on(compat.Input.Changed, "#search")
    def _on_search_changed(self, event: compat.Input.Changed) -> None:
        self._confirm.reset()
        self._query = event.value
        self._render_list()

    @compat.on(compat.ListView.Highlighted)
    def _on_highlighted(self, event: compat.ListView.Highlighted) -> None:
        # 待确认的部署必须与当前选择无关，换选中项时仍应复位以防误触。
        self._confirm.reset()
        self._sync_detail()

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "build":
            self.request_build()
        elif button_id == "serve":
            self.toggle_serve()
        elif button_id == "stop":
            self.stop_preview()
        elif button_id == "open":
            self.open_preview()
        elif button_id == "deploy":
            self.request_deploy()
        elif button_id == "refresh":
            self.refresh_view(force=True)

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
        self.query_one("#docs-list", compat.ListView).focus()

    def _notify_busy(self) -> None:
        compat.notify(
            self.app,
            i18n.t("cli.tui.common.busy_title"),
            severity="warning",
            title=i18n.t("cli.tui.docs.title"),
        )

    def _toolchain_blocker(self) -> str:
        view = self._view
        if view is None:
            return i18n.t("cli.tui.docs.status_loading")
        if view.toolchain.ready:
            return ""
        detail = view.toolchain.detail or view.toolchain.node or "-"
        return i18n.t("cli.tui.docs.toolchain_missing", detail=detail)

    def request_build(self) -> None:
        """构建选区中的包；没有选区时构建全部。"""
        if self._busy:
            self._notify_busy()
            return
        reason = self._toolchain_blocker()
        if reason:
            self._set_status(reason)
            compat.notify(self.app, reason, severity="warning", title=i18n.t("cli.tui.docs.action_build"))
            return
        keys = self.selected_keys
        label = i18n.t("cli.tui.common.list_separator").join(keys) or i18n.t("cli.tui.docs.all_packages")
        self._confirm.reset()
        self._busy = True
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.docs.build_started", label=label))
        self.run_worker(self._build(keys), group="docs-build", exclusive=True)

    async def _build(self, keys: tuple[str, ...]) -> None:
        try:
            result = await asyncio.to_thread(self.source.build, keys)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False,
                i18n.t("cli.tui.docs.build_failed", detail=f"{type(error).__name__}: {error}"),
                "",
            )
        if result.ok:
            self._built = True
            self.last_result = result.message
            self._set_status(result.message)
            compat.notify(self.app, result.message, severity="information", title=i18n.t("cli.tui.docs.action_build"))
        else:
            self.last_error = result.detail or result.message
            self._set_status(i18n.t("cli.tui.docs.build_failed", detail=result.detail or result.message))
            compat.notify(self.app, result.message, severity="error", title=i18n.t("cli.tui.docs.action_build"))
        self._busy = False
        self._sync_actions()

    def toggle_serve(self) -> None:
        """启动或停止预览服务。"""
        if self._busy:
            self._notify_busy()
            return
        if self._serving:
            self.stop_preview()
            return
        reason = self._toolchain_blocker()
        if reason:
            self._set_status(reason)
            compat.notify(self.app, reason, severity="warning", title=i18n.t("cli.tui.docs.action_serve"))
            return
        if not self._is_built():
            self._set_status(i18n.t("cli.tui.docs.need_build"))
            compat.notify(
                self.app,
                i18n.t("cli.tui.docs.need_build"),
                severity="warning",
                title=i18n.t("cli.tui.docs.action_serve"),
            )
            return
        self._busy = True
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.docs.serve_starting"))
        self.run_worker(self._start_server(), group="docs-serve", exclusive=True)

    async def _start_server(self) -> None:
        try:
            url = await self.source.start_server()
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            self._serving = False
            self._url = ""
            self.last_error = f"{type(error).__name__}: {error}"
            message = i18n.t("cli.tui.docs.serve_failed", detail=error)
            self._set_status(message)
            compat.notify(self.app, message, severity="error", title=i18n.t("cli.tui.docs.action_serve"))
        else:
            self._serving = True
            self._url = url
            # 启动期间页面可能已切走，此时立即停止，避免留下无人管理的服务。
            if not self.display:
                await self._quiet_stop()
                self._serving = False
                self._url = ""
            else:
                message = i18n.t("cli.tui.docs.serve_ready", url=url)
                self._set_status(message)
                compat.notify(self.app, message, severity="information", title=i18n.t("cli.tui.docs.action_serve"))
        self._busy = False
        self._sync_detail()
        self._sync_actions()

    def stop_preview(self) -> None:
        """停止预览服务；未运行时只更新状态。"""
        if self._busy:
            self._notify_busy()
            return
        if not self._serving:
            self._set_status(i18n.t("cli.tui.docs.server_stopped"))
            self._sync_actions()
            return
        self._busy = True
        self._sync_actions()
        self.run_worker(self._stop_server(), group="docs-serve", exclusive=True)

    async def _stop_server(self) -> None:
        try:
            await self.source.stop_server()
        except Exception as error:  # noqa: BLE001 - 停止失败仍需复位界面状态
            self.last_error = f"{type(error).__name__}: {error}"
        self._serving = False
        self._url = ""
        self._busy = False
        self._set_status(i18n.t("cli.tui.docs.server_stopped"))
        self._sync_detail()
        self._sync_actions()

    def open_preview(self) -> None:
        """在运行中的预览服务上打开浏览器。"""
        if not self._serving or not self._url:
            self._set_status(i18n.t("cli.tui.docs.need_serve"))
            return
        try:
            opened = webbrowser.open(self._url)
        except Exception as error:  # noqa: BLE001 - 浏览器调用失败只作为状态展示
            opened = False
            self.last_error = f"{type(error).__name__}: {error}"
        if opened:
            self._set_status(i18n.t("cli.tui.docs.server_running", url=self._url))
            return
        self._set_status(i18n.t("cli.tui.docs.open_failed", detail=self.last_error or self._url))

    def request_deploy(self) -> None:
        """弹出部署方式选择框；默认聚焦只读的试运行。"""
        if self._busy:
            self._notify_busy()
            return
        # 防抖窗口内忽略重复请求，避免叠加确认框。
        if not self._confirm.accept("deploy"):
            return
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.docs.deploy_title"),
            hint=i18n.t("cli.tui.docs.deploy_hint"),
            options=(
                (CHOICE_DRY_RUN, i18n.t("cli.tui.docs.deploy_dry_run")),
                (CHOICE_DEPLOY, i18n.t("cli.tui.docs.deploy_real")),
            ),
            cancel_label=i18n.t("cli.tui.docs.cancelled"),
            callback=self.start_deploy,
        )

    def start_deploy(self, choice: str | None) -> None:
        """按选择执行试运行或真实部署。

        :param choice: ``dry`` 只统计，``deploy`` 发布；``None`` 表示取消。
        """
        # 关闭确认框后清除防抖记录，允许重新发起操作。
        self._confirm.reset()
        if choice not in (CHOICE_DRY_RUN, CHOICE_DEPLOY):
            self._set_status(i18n.t("cli.tui.docs.cancelled"))
            return
        if self._busy:
            self._notify_busy()
            return
        dry_run = choice == CHOICE_DRY_RUN
        label = i18n.t("cli.tui.docs.deploy_dry_run" if dry_run else "cli.tui.docs.deploy_real")
        self._busy = True
        self._sync_actions()
        self._set_status(i18n.t("cli.tui.docs.deploy_started", label=label))
        self.run_worker(self._deploy(dry_run), group="docs-deploy", exclusive=True)

    async def _deploy(self, dry_run: bool) -> None:
        label = i18n.t("cli.tui.docs.deploy_dry_run" if dry_run else "cli.tui.docs.deploy_real")
        try:
            result = await asyncio.to_thread(self.source.deploy, None, dry_run)
        except Exception as error:  # noqa: BLE001 - 数据源异常转换为操作结果
            result = OperationResult(
                False,
                i18n.t("cli.tui.docs.deploy_failed", detail=f"{type(error).__name__}: {error}"),
                "",
            )
        if result.ok:
            self.last_result = result.message
            self._set_status(result.message)
            compat.notify(self.app, result.message, severity="information", title=label)
        else:
            self.last_error = result.detail or result.message
            self._set_status(i18n.t("cli.tui.docs.deploy_failed", detail=result.detail or result.message))
            compat.notify(self.app, result.message, severity="error", title=label)
        self._busy = False
        self._sync_actions()

    def reset_pending(self) -> None:
        """作废待确认状态；切页与本页状态变化时调用。"""
        self._confirm.reset()

    def dirty_note(self) -> str:
        """返回未结束的预览服务摘要，供退出与切换实例确认。"""
        if not self._serving:
            return ""
        return i18n.t("cli.tui.docs.dirty_note", url=self._url or "-")

    def on_hide(self, event: compat.events.Hide) -> None:
        """离开页面时停止预览服务，避免后台子进程残留。"""
        self._stop_in_background()

    def on_unmount(self) -> None:
        """卸载页面时停止预览服务。"""
        self._stop_in_background()

    def _stop_in_background(self) -> None:
        if not self._serving:
            return
        self._serving = False
        self._url = ""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        loop.create_task(self._quiet_stop())

    async def _quiet_stop(self) -> None:
        try:
            await self.source.stop_server()
        except Exception:  # noqa: BLE001 - 退出路径上不再报告停止失败
            return

    def action_refresh(self) -> None:
        """键位动作：强制重新读取文档目录。"""
        self.refresh_view(force=True)

    def action_focus_search(self) -> None:
        """键位动作：聚焦搜索框。"""
        self.focus_search()

    def action_toggle_select(self) -> None:
        """键位动作：切换当前项的选中状态。"""
        package = self.selected_package
        if package is None:
            return
        self._confirm.reset()
        if package.key in self._selected:
            self._selected.discard(package.key)
        else:
            self._selected.add(package.key)
        self._render_list()

    def action_select_all(self) -> None:
        """键位动作：选中当前可见的全部文档包。"""
        visible = self.visible_packages
        if not visible:
            return
        self._confirm.reset()
        self._selected.update(package.key for package in visible)
        self._render_list()

    def action_clear_selection(self) -> None:
        """键位动作：清空选区。"""
        self._confirm.reset()
        if not self._selected:
            return
        self._selected.clear()
        self._render_list()

    def action_build(self) -> None:
        """键位动作：构建选中包或全部包。"""
        self.request_build()

    def action_serve(self) -> None:
        """键位动作：启动或停止预览服务。"""
        self.toggle_serve()

    def action_open(self) -> None:
        """键位动作：在浏览器中打开预览地址。"""
        self.open_preview()

    def action_deploy(self) -> None:
        """键位动作：请求部署确认。"""
        self.request_deploy()

    def action_clear_search(self) -> None:
        """键位动作：清空搜索框。"""
        self.clear_search()

    # endregion

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await compat.wait_for_idle(self.app, lambda: self._busy)
