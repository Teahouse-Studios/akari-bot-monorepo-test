"""文档开发模式：生成到暂存目录、差分同步到镜像目录，并在镜像上运行 VitePress dev。

生成器每次都会清空目标目录并重写全部文件，直接把生成结果写进 dev 服务器正在读取的镜像会让 Vite
每一轮都重建整站。开发模式因此先生成到 ``cache/docs/.dev-staging``，再按文件内容把差异写进
``cache/docs/dev``：只有真正变化的文件才会更新，VitePress 的模块热替换与页面滚动位置得以保留。
"""

from __future__ import annotations

import filecmp
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil

from .catalog import load_catalog
from .config import CONFIG_FILENAME, DocsConfig, load_config, site_asset_path
from .generator import HOME_DIR, generate
from .model import DocCatalog, DocsError
from .theme import THEME_FILENAME, ThemeSpec, resolve_theme
from .toolchain import VITEPRESS_BIN, LogSink, detect, ensure_toolchain
from .watch import CONFIG, DOCS, MANIFEST, THEME, Change, PathWatcher, WatchTarget

DEFAULT_DEV_PORT = 5173
DEV_DIR_NAME = "dev"
STAGING_DIR_NAME = ".dev-staging"
LOCK_FILENAME = ".dev.lock"
DEBOUNCE_SECONDS = 0.6
STOP_TIMEOUT_SECONDS = 8.0
READY_TIMEOUT_SECONDS = 180.0
PORT_ATTEMPTS = 3
LOG_TAIL_LINES = 40

STRUCTURE = "structure"
CONTENT = "content"
STRUCTURE_NAMES = frozenset({"docs.toml", "docs.json", "docs.global.toml", "docs.global.json", "doc.toml", "doc.json"})
# VitePress dev 在镜像里写依赖预构建与输出缓存，同步时既不同步也不清理。
SKIPPED_SYNC_PATHS = frozenset({"node_modules", ".vitepress/cache", ".vitepress/dist"})
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
_LAST_SYNC_PATH = ".vitepress/config.mts"
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")

Emitter = Callable[[Mapping[str, Any]], None]


@dataclass(frozen=True)
class SyncResult:
    """一次镜像同步的结果。"""

    written: tuple[str, ...]
    removed: tuple[str, ...]
    duration_ms: int


@dataclass(frozen=True)
class DevLock:
    """开发模式的运行锁内容。"""

    pid: int
    host: str
    port: int
    base: str
    started_at: float


def lock_file(config: DocsConfig) -> Path:
    """返回实例的开发模式运行锁路径。"""
    return config.cache_docs_dir / LOCK_FILENAME


def read_lock(config: DocsConfig) -> DevLock | None:
    """读取实例的运行锁；文件缺失或内容损坏时返回 ``None``。"""
    return read_lock_at(lock_file(config))


def read_lock_at(path: Path) -> DevLock | None:
    """读取指定路径的运行锁；文件缺失或内容损坏时返回 ``None``。"""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    try:
        return DevLock(
            pid=int(payload["pid"]),
            host=str(payload.get("host", "")),
            port=int(payload.get("port", 0)),
            base=str(payload.get("base", "/")),
            started_at=float(payload.get("started_at", 0.0)),
        )
    except (KeyError, TypeError, ValueError):
        return None


def lock_active(lock: DevLock | None) -> bool:
    """判断持有运行锁的进程是否仍在运行。"""
    if lock is None:
        return False
    try:
        return psutil.pid_exists(lock.pid)
    except (psutil.Error, OSError):
        return False


def sync_tree(source: Path, target: Path) -> SyncResult:
    """按内容把 ``source`` 同步到 ``target``。

    只写内容不同的文件，先写临时文件再原子替换；``target`` 中不在 ``source`` 里的文件会被删除，
    ``node_modules`` 目录保持不变。
    """
    started = time.monotonic()
    source = Path(source)
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    removed: list[str] = []
    staged = set()
    for relative, path in _staged_files(source):
        staged.add(relative)
        destination = target / relative
        if _same_content(path, destination):
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f"{destination.name}.tmp")
        shutil.copyfile(path, temporary)
        os.replace(temporary, destination)
        written.append(relative)
    for relative in _mirrored_files(target):
        if relative in staged:
            continue
        (target / relative).unlink(missing_ok=True)
        removed.append(relative)
    _prune_directories(target)
    return SyncResult(written=tuple(written), removed=tuple(removed), duration_ms=_elapsed_ms(started))


def classify(changes: Sequence[Change]) -> str:
    """把一批改动归类成一次同步的触发原因。

    ``manifest`` 需要重装依赖，``config`` 需要重读站点配置，``theme`` 与 ``structure`` 需要重新生成，
    其余都属于正文内容变化。
    """
    kinds = {change.kind for change in changes}
    if MANIFEST in kinds:
        return MANIFEST
    if CONFIG in kinds:
        return CONFIG
    if THEME in kinds:
        return THEME
    for change in changes:
        if change.kind != DOCS:
            continue
        if change.action in {"created", "deleted", "moved"}:
            return STRUCTURE
        if change.path.name in STRUCTURE_NAMES:
            return STRUCTURE
    return CONTENT


class DevSession:
    """一次文档开发模式的完整生命周期。

    :param instance: 带 ``root`` 与 ``run_core_capture`` 的实例。
    :param host: 绑定地址。
    :param port: 首选端口，``0`` 表示每轮都由系统分配。
    :param open_browser: 就绪后打开浏览器。
    :param offline: 为真时禁止安装 Node 依赖。
    :param keys: 只监听这些包；``None`` 表示全部。
    :param debounce: 改动静默多久后开始同步。
    :param emit: 结构化事件回调。
    :param log: 子进程输出行回调。
    :param ready_timeout: 等待 dev 服务器可用的秒数。
    :param opener: 打开浏览器的函数，供测试替换。
    """

    def __init__(
        self,
        instance: Any,
        *,
        host: str = "127.0.0.1",
        port: int = DEFAULT_DEV_PORT,
        open_browser: bool = False,
        offline: bool = False,
        keys: Sequence[str] | None = None,
        debounce: float = DEBOUNCE_SECONDS,
        emit: Emitter | None = None,
        log: LogSink | None = None,
        ready_timeout: float = READY_TIMEOUT_SECONDS,
        opener: Callable[[str], Any] | None = None,
    ) -> None:
        self._instance = instance
        self._host = host or "127.0.0.1"
        self._port = int(port)
        self._open_browser = open_browser
        self._offline = offline
        self._keys = tuple(keys) if keys else None
        self._debounce = debounce
        self._emit_callback = emit or _ignore_event
        self._log_callback = log or _ignore_line
        self._ready_timeout = float(ready_timeout)
        self._opener = opener or webbrowser.open
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._watcher: PathWatcher | None = None
        self._process: subprocess.Popen[str] | None = None
        self._tail: deque[str] = deque(maxlen=LOG_TAIL_LINES)
        self._url = ""
        self._config: DocsConfig | None = None
        self._theme: ThemeSpec | None = None
        self._catalog: DocCatalog | None = None
        self._full: DocCatalog | None = None
        self._docs_dir: Path | None = None
        self._lock_path: Path | None = None

    @property
    def url(self) -> str:
        """当前 dev 服务器地址；未就绪时为空字符串。"""
        return self._url

    def run(self) -> None:
        """启动同步与 dev 服务器，阻塞到收到停止信号。"""
        self._install_signal_handlers()
        try:
            self._prepare()
            self._sync(initial=True)
            self._start_server()
            self._loop()
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown()

    def stop(self) -> None:
        """请求停止；可从其他线程调用。"""
        self._stop.set()
        watcher, self._watcher = self._watcher, None
        if watcher is not None:
            watcher.wake()
            watcher.stop()

    def _prepare(self) -> None:
        config = load_config(self._instance)
        active = read_lock(config)
        if lock_active(active):
            raise DocsError("cli.docs.error.dev_locked", pid=active.pid, port=active.port)
        self._config = config
        self._write_lock(config)
        theme = resolve_theme(config)
        toolchain = detect(theme.node_major)
        if not toolchain.ready:
            raise DocsError("cli.docs.error.toolchain_missing", detail=toolchain.detail)
        self._theme = theme
        self._emit({"event": "stage", "stage": "toolchain"})
        cache_dir = Path(self._instance.root) / "cache"
        self._docs_dir = ensure_toolchain(cache_dir, offline=self._offline, theme=theme, log=self._log)
        self._reload_catalog(config)
        self._watch()

    def _write_lock(self, config: DocsConfig) -> None:
        path = lock_file(config)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = DevLock(
            pid=os.getpid(),
            host=self._host,
            port=self._port,
            base=config.base,
            started_at=time.time(),
        )
        path.write_text(
            json.dumps(
                {
                    "pid": payload.pid,
                    "host": payload.host,
                    "port": payload.port,
                    "base": payload.base,
                    "started_at": payload.started_at,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        self._lock_path = path

    def _reload_catalog(self, config: DocsConfig) -> None:
        full = load_catalog(
            self._instance,
            labels=config.labels,
            locales=[locale.tag for locale in config.locales],
        )
        selected = full.select(self._keys) if self._keys else full
        self._full = full
        self._catalog = selected

    def _watch(self) -> None:
        targets = self._targets()
        previous, self._watcher = self._watcher, PathWatcher(targets, debounce=self._debounce)
        if previous is not None:
            previous.stop()
        self._watcher.start()

    def _targets(self) -> tuple[WatchTarget, ...]:
        config = self._config
        theme = self._theme
        catalog = self._catalog
        if config is None or theme is None or catalog is None:
            return ()
        targets: list[WatchTarget] = []
        for package in catalog.packages:
            targets.append(WatchTarget(path=package.doc_path, kind=DOCS))
        targets.append(WatchTarget(path=theme.theme_dir, kind=THEME))
        targets.append(WatchTarget(path=theme.root / THEME_FILENAME, kind=MANIFEST, recursive=False))
        targets.append(WatchTarget(path=config.root / CONFIG_FILENAME, kind=CONFIG, recursive=False))
        targets.append(WatchTarget(path=HOME_DIR, kind=CONFIG))
        targets.append(WatchTarget(path=ASSETS_DIR, kind=CONFIG))
        for asset in _site_assets(config):
            targets.append(WatchTarget(path=asset, kind=CONFIG, recursive=False))
        for package in catalog.packages:
            for field in ("logo", "logo_dark", "avatar", "character", "credits"):
                asset = Path(str(getattr(package, field, "") or ""))
                if asset.is_file():
                    targets.append(WatchTarget(path=asset, kind=CONFIG, recursive=False))
        return tuple(target for target in targets if target.path.exists())

    def _sync(self, *, initial: bool = False) -> SyncResult:
        config = self._config
        theme = self._theme
        catalog = self._catalog
        full = self._full
        if config is None or theme is None or catalog is None or full is None:
            raise DocsError("cli.docs.error.bad_config", detail="dev session is not prepared")
        staging = config.cache_docs_dir / STAGING_DIR_NAME
        mirror = config.cache_docs_dir / DEV_DIR_NAME
        self._emit({"event": "stage", "stage": "generate"})
        generate(catalog, staging, config, theme=theme, link_packages=full.packages)
        result = sync_tree(staging, mirror)
        self._emit(
            {
                "event": "sync",
                "initial": initial,
                "written": len(result.written),
                "removed": len(result.removed),
                "duration_ms": result.duration_ms,
                "files": list(result.written[:20]),
                "removed_files": list(result.removed[:20]),
            }
        )
        return result

    def _start_server(self) -> str:
        docs_dir = self._docs_dir
        config = self._config
        if docs_dir is None or config is None:
            raise DocsError("cli.docs.error.bad_config", detail="dev session is not prepared")
        node = shutil.which("node")
        if node is None:
            raise DocsError("cli.docs.error.toolchain_missing", detail="node is not on PATH")
        script = docs_dir / VITEPRESS_BIN
        if not script.is_file():
            raise DocsError("cli.docs.error.toolchain_missing", detail=str(script))
        self._emit({"event": "stage", "stage": "server"})
        last = ""
        for attempt in range(PORT_ATTEMPTS):
            port = self._port if attempt == 0 and self._port else _free_port(self._host)
            argv = [
                node,
                str(script),
                "dev",
                str(config.cache_docs_dir / DEV_DIR_NAME),
                "--host",
                self._host,
                "--port",
                str(port),
                "--strictPort",
            ]
            options: dict[str, Any] = {}
            if os.name != "nt":
                options["start_new_session"] = True
            process = subprocess.Popen(  # noqa: S603 - argv 由固定组件拼成
                argv,
                cwd=str(docs_dir),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env={**os.environ, "NO_COLOR": "1", "FORCE_COLOR": "0"},
                **options,
            )
            self._process = process
            threading.Thread(target=self._pump, args=(process,), name="akaribot-docs-dev", daemon=True).start()
            url = self._wait_ready(process, port)
            if url:
                self._port = port
                self._url = url
                return url
            last = "\n".join(self._tail)
            self._stop_server()
            if self._stop.is_set():
                break
        raise DocsError(
            "cli.docs.error.dev_failed",
            reason=last or "vitepress dev did not become ready",
            path=str(config.cache_docs_dir / DEV_DIR_NAME),
        )

    def _wait_ready(self, process: subprocess.Popen[str], port: int) -> str:
        config = self._config
        if config is None:
            return ""
        url = f"http://{_display_host(self._host)}:{port}{config.base}"
        deadline = time.monotonic() + self._ready_timeout
        while time.monotonic() < deadline and not self._stop.is_set():
            if process.poll() is not None:
                return ""
            try:
                with urllib.request.urlopen(url, timeout=1.0) as response:
                    if response.status == 200:
                        return url
            except (OSError, urllib.error.URLError):
                pass
            self._stop.wait(0.2)
        return ""

    def _pump(self, process: subprocess.Popen[str]) -> None:
        stream = process.stdout
        if stream is None:
            return
        for raw in stream:
            line = _ANSI_ESCAPE.sub("", raw).rstrip()
            if not line:
                continue
            with self._lock:
                self._tail.append(line)
            self._log(line)

    def _loop(self) -> None:
        self._emit({"event": "ready", "url": self._url, "mode": "dev", "packages": list(self._catalog.keys())})
        if self._open_browser:
            try:
                self._opener(self._url)
            except (OSError, webbrowser.Error):
                pass
        while not self._stop.is_set():
            watcher = self._watcher
            if watcher is None:
                self._stop.wait(0.2)
                continue
            changes = watcher.poll(0.5)
            if not changes:
                continue
            try:
                self._apply(changes)
            except DocsError as error:
                self._emit({"event": "error", "error": {"key": error.key, "params": dict(error.params)}})

    def _apply(self, changes: Sequence[Change]) -> None:
        kind = classify(changes)
        config = self._config
        if config is None:
            return
        if kind == MANIFEST:
            self._emit({"event": "warn", "code": "theme_manifest", "path": str(changes[0].path)})
            return
        restart = False
        if kind == CONFIG:
            updated = load_config(self._instance)
            theme = resolve_theme(updated)
            if (theme.root, theme.name, theme.vitepress_version) != (
                self._theme.root,
                self._theme.name,
                self._theme.vitepress_version,
            ):
                self._emit({"event": "warn", "code": "theme_manifest", "path": str(theme.root)})
                return
            restart = updated.base != config.base
            self._config = updated
            self._theme = theme
            self._reload_catalog(updated)
            self._watch()
        elif kind == STRUCTURE:
            self._reload_catalog(config)
            self._watch()
        elif kind == THEME:
            self._theme = resolve_theme(config)
            self._watch()
        self._sync()
        if restart:
            self._stop_server()
            self._start_server()
            self._emit(
                {
                    "event": "ready",
                    "url": self._url,
                    "mode": "dev",
                    "packages": list(self._catalog.keys()),
                }
            )

    def _stop_server(self) -> None:
        process, self._process = self._process, None
        if process is None:
            return
        if process.poll() is not None:
            return
        try:
            parent = psutil.Process(process.pid)
            children = parent.children(recursive=True)
        except (psutil.Error, OSError):
            parent, children = None, []
        for child in children:
            _quietly(child.terminate)
        _quietly(process.terminate)
        try:
            process.wait(timeout=STOP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            for child in children:
                _quietly(child.kill)
            _quietly(process.kill)
            try:
                process.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                pass

    def _shutdown(self) -> None:
        self.stop()
        self._stop_server()
        if self._lock_path is not None:
            self._lock_path.unlink(missing_ok=True)
            self._lock_path = None
        self._emit({"event": "stopped"})

    def _install_signal_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            return
        for name in ("SIGINT", "SIGTERM"):
            number = getattr(signal, name, None)
            if number is None:
                continue
            try:
                signal.signal(number, self._on_signal)
            except (OSError, ValueError, RuntimeError):
                continue

    def _on_signal(self, _signum: int, _frame: Any) -> None:
        self.stop()

    def _emit(self, event: Mapping[str, Any]) -> None:
        self._emit_callback(event)

    def _log(self, line: str) -> None:
        self._log_callback(line)


def _staged_files(source: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    for current, directories, files in os.walk(source):
        directories.sort()
        base = Path(current).relative_to(source)
        for name in files:
            entries.append(((base / name).as_posix(), Path(current) / name))
    entries.sort(key=lambda item: (item[0] == _LAST_SYNC_PATH, item[0]))
    return entries


def _mirrored_files(target: Path) -> list[str]:
    entries: list[str] = []
    for current, directories, files in os.walk(target):
        base = Path(current).relative_to(target)
        directories[:] = sorted(name for name in directories if not _skipped_directory(base / name))
        for name in files:
            entries.append((base / name).as_posix())
    return sorted(entries)


def _skipped_directory(relative: Path) -> bool:
    return relative.as_posix() in SKIPPED_SYNC_PATHS


def _same_content(source: Path, target: Path) -> bool:
    try:
        return target.is_file() and filecmp.cmp(source, target, shallow=False)
    except OSError:
        return False


def _prune_directories(root: Path) -> None:
    for current, directories, _files in os.walk(root, topdown=False):
        path = Path(current)
        if path == root or _skipped_directory(path.relative_to(root)):
            continue
        try:
            path.rmdir()
        except OSError:
            continue


def _site_assets(config: DocsConfig) -> list[Path]:
    assets: list[Path] = []
    for field in ("logo", "logo_dark", "avatar", "character", "credits", "favicon"):
        try:
            asset = site_asset_path(config.root, getattr(config.site, field, ""))
        except DocsError:
            continue
        if asset is not None:
            assets.append(asset)
    return assets


def _free_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host if host not in {"0.0.0.0", "::"} else "", 0))
        return int(sock.getsockname()[1])


def _display_host(host: str) -> str:
    return "127.0.0.1" if host in {"0.0.0.0", "::", ""} else host


def _quietly(call: Callable[[], Any]) -> None:
    try:
        call()
    except (OSError, psutil.Error):
        return


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _ignore_event(_event: Mapping[str, Any]) -> None:
    return None


def _ignore_line(_line: str) -> None:
    return None
