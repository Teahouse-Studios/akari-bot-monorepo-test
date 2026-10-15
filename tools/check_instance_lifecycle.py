"""在本机验证后台实例停止协议和进程树清理。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import psutil

from akaribot.cli.instance import Instance, InstanceMeta
from akaribot.cli.process import wait_until

FIXTURE = r"""
import json, os, signal, subprocess, sys, time
from contextlib import nullcontext
from pathlib import Path

root = Path(os.environ["AKARI_INSTANCE_DIR"])
handle = (root / ".bot.lock").open("w+")
handle.write(" ")
handle.flush()
handle.seek(0)
if os.name == "nt":
    import msvcrt
    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
else:
    import fcntl
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0)
if os.name == "nt":
    handle.write("\n")
    handle.seek(1)
handle.write(json.dumps({"pid": os.getpid(), "started_at": "fixture", "argv": sys.argv[1:]}))
handle.truncate()
handle.flush()
ignore = "--ignore-stop" in sys.argv
if not ignore and os.name == "nt":
    from akaribot.core.utils.process_control import listen_for_windows_stop
    listener = listen_for_windows_stop()
else:
    listener = nullcontext()
if os.name != "nt":
    signal.signal(signal.SIGTERM, signal.SIG_IGN if ignore else lambda *_: sys.exit(0))
child = None
try:
    with listener:
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)"])
        (root / "children.json").write_text(json.dumps([child.pid]))
        while True:
            time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    if child is not None:
        child.terminate()
        child.wait(timeout=10)
    handle.close()
"""


def _case(root: Path, *, forced: bool, foreign: bool = False) -> None:
    Instance.create_dirs(root)
    InstanceMeta.create(root, venv="").save()
    fixture = root / "fixture.py"
    fixture.write_text(FIXTURE, encoding="utf-8")
    instance = Instance(root, python_override=Path(sys.executable))
    args = [str(fixture), *(["--ignore-stop"] if forced else [])]
    instance.core_argv = lambda *unused: instance.python_argv(*args)
    owned = None
    if foreign:
        owned = subprocess.Popen(
            instance.python_argv(*args), env=instance.core_env(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        pid = owned.pid
    else:
        pid = instance.spawn_detached(log_path=root / "console.log").pid
    parent = psutil.Process(pid)
    descendants = []
    try:
        ready = wait_until(lambda: (root / "children.json").is_file() and instance.is_running(), timeout=10)
        if not ready:
            raise RuntimeError(f"实例没有启动：{root}")
        descendants = [psutil.Process(pid) for pid in json.loads((root / "children.json").read_text())]
        outcome = instance.stop_running(timeout=0.5 if forced else 10, reap_grace=2)
        if owned is not None:
            owned.wait(timeout=10)
        stopped = wait_until(
            lambda: all(
                not process.is_running() or process.status() == psutil.STATUS_ZOMBIE for process in descendants
            ),
            timeout=5,
        )
        if not outcome.ok or not stopped or instance.is_running() or outcome.forced != forced:
            raise RuntimeError(f"实例停止结果不完整：{outcome}, children_stopped={stopped}")
        print(json.dumps({"forced": forced, "foreign": foreign, "stopped": True, "children_stopped": True}))
    finally:
        for process in [*reversed(descendants), parent]:
            try:
                if process.is_running():
                    process.kill()
            except psutil.NoSuchProcess:
                pass
        if owned is not None:
            owned.wait(timeout=10)


def main() -> int:
    """验证正常停止、强制停止和接管外部启动的实例。"""
    with tempfile.TemporaryDirectory(prefix="akari-process-lifecycle-") as tmp:
        root = Path(tmp)
        _case(root / "normal", forced=False)
        _case(root / "forced", forced=True)
        _case(root / "foreign", forced=False, foreign=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
