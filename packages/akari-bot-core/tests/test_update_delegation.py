import asyncio
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import psutil

from akaribot.testing import Tester, func_case

update = importlib.import_module("akaribot.modules.core.su_tools.update")


async def _test_chat_update_defers_runtime_and_reports_restart():
    outcome = {
        "updated": ["akari-bot-module-dice"],
        "failed": [],
        "skipped": [],
        "reload_pending": ["akari-bot-module-dice"],
        "restart_required": True,
    }
    captured = []

    async def run(path, argv):
        captured.extend(argv)
        return 0, json.dumps(outcome), "", False

    with (
        patch.object(update, "locate_cli", return_value=update.CliLocation("akaribot")),
        patch.object(update, "_run_cli", run),
    ):
        result = await update.delegate_update()
    return "--defer-runtime" in captured and "~restart" in update.format_update_report(result)


async def _test_cancelled_update_reaps_cli_subprocess():
    created = asyncio.Event()
    processes = []
    create = asyncio.create_subprocess_exec

    async def capture(*args, **kwargs):
        process = await create(*args, **kwargs)
        processes.append(process)
        created.set()
        return process

    with tempfile.TemporaryDirectory(prefix="akari-update-process-") as raw:
        marker = Path(raw) / "child.pid"
        script = (
            "import subprocess,sys,time;from pathlib import Path;"
            "child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);"
            "Path(sys.argv[1]).write_text(str(child.pid));time.sleep(30)"
        )
        with patch.object(asyncio, "create_subprocess_exec", capture):
            task = asyncio.create_task(update._run_cli(sys.executable, ["-c", script, str(marker)]))
            try:
                async with asyncio.timeout(10):
                    await created.wait()
                    while not marker.exists():
                        await asyncio.sleep(0.01)
                child = psutil.Process(int(marker.read_text()))
            finally:
                task.cancel()
                result = await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 10)
        try:
            child_stopped = not child.is_running() or child.status() == psutil.STATUS_ZOMBIE
        except psutil.Error:
            child_stopped = True
    return isinstance(result[0], asyncio.CancelledError) and processes[0].returncode is not None and child_stopped


async def _test_cli_output_uses_utf8():
    script = "import json;print(json.dumps({'message':'更新完成'},ensure_ascii=False))"
    with patch.dict(os.environ, {"PYTHONIOENCODING": "ascii"}):
        code, stdout, _, timed_out = await update._run_cli(sys.executable, ["-c", script])
    return code == 0 and not timed_out and json.loads(stdout) == {"message": "更新完成"}


@func_case
async def test_update_delegation(tester: Tester):
    await tester.test(_test_chat_update_defers_runtime_and_reports_restart, "聊天内更新延迟维护并回报重启")
    await tester.test(_test_cancelled_update_reaps_cli_subprocess, "取消更新委托时清收 CLI 子进程")
    await tester.test(_test_cli_output_uses_utf8, "更新子进程与结果解析统一使用 UTF-8")
    return tester
