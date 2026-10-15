"""实例进程的定位与终止。

运行中的实例在 ``<实例根>/.bot.lock`` 上持锁，锁文件里写有进程号与启动时间。控制器据此找到
进程：先向主进程发温和信号，让它按自身顺序收拢适配器与 Server；主进程退出后再清掉它自建的
进程组里可能残留的子进程。由终端前台启动的实例与控制器同组，此时只按进程号发信号，不对整组
发信号——那会连控制器自己一起终止。
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import psutil

from akaribot.cli import i18n

# 等待主进程退出的默认秒数，以及主进程退出后清收子进程的宽限秒数。
DEFAULT_STOP_TIMEOUT = 20.0
DEFAULT_REAP_GRACE = 3.0
POLL_INTERVAL = 0.1


def is_windows() -> bool:
    """当前平台是否为 Windows。"""
    return os.name == "nt"


@dataclass(frozen=True)
class LockRecord:
    """锁文件里记录的持锁进程信息。

    :param pid: 进程号。
    :param started_at: 启动时间，ISO 8601 字符串。
    :param argv: 启动参数，供展示与排障。
    """

    pid: int
    started_at: str = ""
    argv: tuple[str, ...] = ()

    @classmethod
    def parse(cls, text: str) -> LockRecord | None:
        """解析锁文件内容；内容缺失或不是本模块写下的记录时返回 ``None``。"""
        raw = text.strip()
        if not raw:
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(data, Mapping):
            return None
        try:
            pid = int(data.get("pid"))
        except (TypeError, ValueError):
            return None
        if pid <= 0:
            return None
        argv = data.get("argv")
        return cls(
            pid=pid,
            started_at=str(data.get("started_at") or ""),
            argv=tuple(str(item) for item in argv) if isinstance(argv, list) else (),
        )


def pid_alive(pid: int) -> bool:
    """进程是否仍存在。

    Windows 通过进程查询探测，避免使用具有终止语义的 ``os.kill``。

    :param pid: 进程号。
    :return: 进程是否存活。
    """
    if is_windows():
        return psutil.pid_exists(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def read_lock_record(path: Path) -> LockRecord | None:
    """读取锁文件里的进程记录；文件不存在或不可读时返回 ``None``。"""
    try:
        with path.open("rb", buffering=0) as handle:
            # Windows 的首字节被排他锁保护，记录读取须避开锁区。
            if is_windows():
                handle.seek(1)
            return LockRecord.parse(handle.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError):
        return None


@dataclass(frozen=True)
class StopOutcome:
    """一次停止尝试的结果。

    :param ok: 实例是否已停下。
    :param message: 面向用户的一句话结论。
    :param detail: 补充说明，失败时用于排障。
    :param forced: 是否动用了强杀信号。
    """

    ok: bool
    message: str
    detail: str = ""
    forced: bool = False


@runtime_checkable
class ProcessControl(Protocol):
    """进程控制原语，测试可注入替身。"""

    def process_group(self, pid: int) -> int | None:
        """返回进程所在进程组，且仅当该进程是组长时；否则返回 ``None``。"""
        ...

    def group_alive(self, pgid: int) -> bool:
        """进程组内是否仍有进程。"""
        ...

    def terminate(self, pid: int, *, force: bool) -> bool:
        """向单个进程发终止信号。"""
        ...

    def terminate_group(self, pgid: int, *, force: bool) -> bool:
        """向整个进程组发终止信号。"""
        ...

    def sleep(self, seconds: float) -> None:
        """等待若干秒。"""
        ...


class SystemProcessControl:
    """通过平台信号或 Windows 停止事件控制实例进程。"""

    def __init__(self) -> None:
        self._trees: dict[int, list[psutil.Process]] = {}

    def process_group(self, pid: int) -> int | None:
        """见 :meth:`ProcessControl.process_group`。"""
        if is_windows():
            if pid == os.getpid():
                return None
            try:
                parent = psutil.Process(pid)
                self._trees[pid] = [parent, *parent.children(recursive=True)]
            except psutil.Error:
                return None
            return pid
        try:
            pgid = os.getpgid(pid)
        except OSError:
            return None
        if pgid == pid:
            return pgid
        # 与控制器同组的实例只能按进程号处理：对整组发信号会连控制器一起终止。
        try:
            if pgid == os.getpgid(0):
                return None
        except OSError:
            return None
        return pgid

    def group_alive(self, pgid: int) -> bool:
        """见 :meth:`ProcessControl.group_alive`。"""
        if is_windows():
            self._refresh_tree(pgid)
            return any(process.is_running() for process in self._trees.get(pgid, ()))
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            # macOS 对已退出但尚未回收的组长可返回 EPERM，须继续核对可运行成员。
            pass
        except OSError:
            return False
        for process in psutil.process_iter(("pid", "status")):
            if process.info["status"] in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD):
                continue
            try:
                if os.getpgid(process.pid) == pgid:
                    return True
            except ProcessLookupError:
                continue
            except PermissionError:
                continue
        return False

    def terminate(self, pid: int, *, force: bool) -> bool:
        """见 :meth:`ProcessControl.terminate`。"""
        if is_windows():
            if not force:
                from akaribot.cli.windows import request_stop

                return request_stop(pid)
            try:
                process = self._trees[pid][0] if pid in self._trees else psutil.Process(pid)
                if process.is_running():
                    process.kill()
            except psutil.NoSuchProcess:
                return True
            except psutil.Error:
                return False
            return True
        try:
            os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
        except OSError:
            return False
        return True

    def terminate_group(self, pgid: int, *, force: bool) -> bool:
        """见 :meth:`ProcessControl.terminate_group`。"""
        if is_windows():
            if not force:
                return False
            ok = True
            suspended: list[psutil.Process] = []
            try:
                while True:
                    self._refresh_tree(pgid)
                    pending = [process for process in self._trees.get(pgid, ()) if process not in suspended]
                    if not pending:
                        break
                    for process in pending:
                        try:
                            if process.is_running():
                                process.suspend()
                            suspended.append(process)
                        except psutil.NoSuchProcess:
                            suspended.append(process)
                        except psutil.Error:
                            return False
                for process in reversed(suspended):
                    try:
                        if process.is_running():
                            process.kill()
                    except psutil.NoSuchProcess:
                        continue
                    except psutil.Error:
                        ok = False
            finally:
                for process in suspended:
                    try:
                        if process.is_running():
                            process.resume()
                    except psutil.Error:
                        continue
            return ok
        try:
            os.killpg(pgid, signal.SIGKILL if force else signal.SIGTERM)
        except OSError:
            return False
        return True

    def _refresh_tree(self, pid: int) -> None:
        processes = self._trees.get(pid, [])
        known = set(processes)
        for process in tuple(processes):
            try:
                if not process.is_running():
                    continue
                for child in process.children(recursive=True):
                    if child not in known:
                        processes.append(child)
                        known.add(child)
            except psutil.Error:
                continue

    def sleep(self, seconds: float) -> None:
        """见 :meth:`ProcessControl.sleep`。"""
        time.sleep(seconds)


SYSTEM_CONTROL = SystemProcessControl()


def wait_until(predicate: Callable[[], bool], *, timeout: float, control: ProcessControl | None = None) -> bool:
    """轮询等待条件成立。

    :param predicate: 条件。
    :param timeout: 最长等待秒数。
    :param control: 进程控制原语，提供等待实现；缺省用系统实现。
    :return: 条件是否在超时前成立。
    """
    worker = control or SYSTEM_CONTROL
    deadline = time.monotonic() + max(0.0, timeout)
    while True:
        if predicate():
            return True
        if time.monotonic() >= deadline:
            return False
        worker.sleep(POLL_INTERVAL)


def stop_process(
    *,
    pid: int,
    running: Callable[[], bool],
    timeout: float = DEFAULT_STOP_TIMEOUT,
    reap_grace: float = DEFAULT_REAP_GRACE,
    control: ProcessControl | None = None,
) -> StopOutcome:
    """停止实例进程：先温和终止主进程，再清收它自建的进程组。

    :param pid: 主进程号，取自锁文件记录。
    :param running: 返回实例是否仍在运行的探测函数（通常是锁是否仍被持有）。
    :param timeout: 等待主进程退出的秒数。
    :param reap_grace: 主进程退出后清收子进程的宽限秒数。
    :param control: 进程控制原语，缺省用系统实现。
    :return: 停止结果。
    """
    worker = control or SYSTEM_CONTROL
    pgid = worker.process_group(pid)
    worker.terminate(pid, force=False)
    forced = False

    def stopped():
        if pgid is not None:
            worker.group_alive(pgid)
        return not running()

    if not wait_until(stopped, timeout=timeout, control=worker):
        if pgid is not None:
            worker.terminate_group(pgid, force=True)
        worker.terminate(pid, force=True)
        forced = True
        if not wait_until(lambda: not running(), timeout=timeout, control=worker):
            return StopOutcome(
                False,
                i18n.t("cli.run.stop_failed", pid=pid),
                i18n.t("cli.run.stop_failed_detail", seconds=f"{timeout:.0f}"),
                forced=True,
            )
    if pgid is not None:
        reaped, reap_forced = _reap_group(pgid, grace=reap_grace, control=worker)
        forced = forced or reap_forced
        if not reaped:
            return StopOutcome(
                False,
                i18n.t("cli.run.stop_failed", pid=pid),
                i18n.t("cli.run.stop_failed_detail", seconds=f"{reap_grace:.0f}"),
                forced=True,
            )
    key = "cli.run.stop_forced" if forced else "cli.run.stop_done"
    return StopOutcome(True, i18n.t(key, pid=pid), forced=forced)


def _reap_group(pgid: int, *, grace: float, control: ProcessControl) -> tuple[bool, bool]:
    # 主进程已按自身顺序收拢过子进程，这里只处理残留：先温和，宽限期内没退干净再强杀。
    if not control.group_alive(pgid):
        return True, False
    control.terminate_group(pgid, force=False)
    if wait_until(lambda: not control.group_alive(pgid), timeout=grace, control=control):
        return True, False
    control.terminate_group(pgid, force=True)
    return wait_until(lambda: not control.group_alive(pgid), timeout=grace, control=control), True


def detach_kwargs() -> dict[str, Any]:
    """返回让子进程脱离当前会话的 :mod:`subprocess` 参数。"""
    if is_windows():
        return {
            "creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        }
    return {"start_new_session": True}
