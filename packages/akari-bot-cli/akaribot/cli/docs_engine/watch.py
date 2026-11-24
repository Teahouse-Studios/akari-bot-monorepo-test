"""文档开发模式的文件监听。

各包文档目录、主题目录与站点配置文件都是普通的目录或文件，watchdog 的原生事件源在这些位置上
发现改动。监听器把事件归并为去抖后的批次交给调用方，一次保存只触发一轮重新生成。
"""

from __future__ import annotations

import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

DOCS = "docs"
THEME = "theme"
CONFIG = "config"
MANIFEST = "manifest"

DEFAULT_DEBOUNCE_SECONDS = 0.6
MAX_BATCH_SECONDS = 5.0
IGNORED_DIRECTORIES = frozenset({"node_modules", "__pycache__", ".git"})
IGNORED_NAMES = frozenset({".DS_Store"})
IGNORED_SUFFIXES = (".swp", ".tmp", ".swx", ".orig")

_ACTION_BY_EVENT = {
    "created": "created",
    "deleted": "deleted",
    "modified": "modified",
    "moved": "moved",
}


@dataclass(frozen=True)
class WatchTarget:
    """一个被监听的路径。

    :param path: 目录或文件。
    :param kind: 变更类别，取 ``DOCS``、``THEME``、``CONFIG``、``MANIFEST`` 之一。
    :param recursive: 目录是否递归监听。
    """

    path: Path
    kind: str
    recursive: bool = True


@dataclass(frozen=True)
class Change:
    """单次文件变更。"""

    path: Path
    action: str
    kind: str


class _TargetHandler(FileSystemEventHandler):
    def __init__(self, watcher: PathWatcher, target: WatchTarget) -> None:
        self._watcher = watcher
        self._target = target

    def on_any_event(self, event: FileSystemEvent) -> None:
        self._watcher.report(event, self._target)


class PathWatcher:
    """按目标路径收集文件改动并按批次交付。

    :param targets: 监听目标。
    :param debounce: 最后一次改动之后静默多久算一轮结束。
    """

    def __init__(self, targets: Iterable[WatchTarget], *, debounce: float = DEFAULT_DEBOUNCE_SECONDS) -> None:
        self.targets = tuple(
            WatchTarget(path=target.path.expanduser().resolve(), kind=target.kind, recursive=target.recursive)
            for target in targets
        )
        self.debounce = max(0.05, float(debounce))
        self._lock = threading.Lock()
        self._pending: dict[Path, Change] = {}
        self._last_event = 0.0
        self._ready = threading.Event()
        self._observer: Observer | None = None

    def start(self) -> None:
        """启动观察者。目标路径不存在时跳过。"""
        if self._observer is not None:
            return
        observer = Observer()
        for target in self.targets:
            directory = target.path if target.path.is_dir() else target.path.parent
            if not directory.is_dir():
                continue
            handler = _TargetHandler(self, target)
            observer.schedule(handler, str(directory), recursive=target.recursive and target.path.is_dir())
        observer.start()
        self._observer = observer

    def stop(self) -> None:
        """停止观察者。"""
        observer, self._observer = self._observer, None
        if observer is not None:
            observer.stop()
            observer.join(timeout=5.0)

    def close(self) -> None:
        self.stop()

    def report(self, event: FileSystemEvent, target: WatchTarget) -> None:
        """记录观察者交付的原始事件。"""
        action = _ACTION_BY_EVENT.get(event.event_type)
        if action is None or event.is_directory:
            return
        paths = [Path(event.src_path)]
        destination = getattr(event, "dest_path", "")
        if event.event_type == "moved" and destination:
            paths.append(Path(destination))
        for path in paths:
            if not _relevant(path, target):
                continue
            canonical = _canonical(path)
            with self._lock:
                known = self._pending.get(canonical)
                if known is None or known.action == "modified" or action != "modified":
                    self._pending[canonical] = Change(path=canonical, action=action, kind=target.kind)
                self._last_event = time.monotonic()
            self._ready.set()

    def poll(self, timeout: float = 0.5) -> tuple[Change, ...]:
        """等待批量变更。超时返回空元组。"""
        if not self._ready.wait(max(0.0, float(timeout))):
            return ()
        deadline = time.monotonic() + MAX_BATCH_SECONDS
        while True:
            with self._lock:
                if not self._pending:
                    self._ready.clear()
                    return ()
                quiet = time.monotonic() - self._last_event
            if quiet >= self.debounce or time.monotonic() >= deadline:
                break
            time.sleep(min(0.05, self.debounce))
        with self._lock:
            changes = tuple(sorted(self._pending.values(), key=lambda change: str(change.path)))
            self._pending.clear()
            self._ready.clear()
        return changes

    def wake(self) -> None:
        """让阻塞在 :meth:`poll` 上的调用方立即返回。"""
        self._ready.set()


def _relevant(path: Path, target: WatchTarget) -> bool:
    if not target.recursive and not target.path.is_dir():
        return path == target.path
    relative = _relative(path, target.path)
    if relative is None or not relative.parts:
        return False
    if any(part.startswith(".") or part in IGNORED_DIRECTORIES for part in relative.parts[:-1]):
        return False
    name = relative.name
    if name in IGNORED_NAMES or name.startswith("."):
        return False
    return not name.endswith(IGNORED_SUFFIXES)


def _canonical(path: Path) -> Path:
    try:
        return path.resolve()
    except OSError:
        return path


def _relative(path: Path, root: Path) -> Path | None:
    try:
        return path.relative_to(root)
    except ValueError:
        pass
    try:
        return path.resolve().relative_to(root)
    except (OSError, ValueError):
        return None
