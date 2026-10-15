from types import SimpleNamespace
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from akaribot.cli import process
from akaribot.cli.instance import Instance
from akaribot.testing import Tester, func_case


def _test_windows_detach_uses_subprocess_flags():
    with (
        patch.object(process, "is_windows", return_value=True),
        patch.object(process.subprocess, "DETACHED_PROCESS", 8, create=True),
        patch.object(process.subprocess, "CREATE_NEW_PROCESS_GROUP", 512, create=True),
    ):
        return process.detach_kwargs() == {"creationflags": 520}


def _test_windows_stop_waits_for_children():
    child = Mock()
    child.children.return_value = []
    child.is_running.return_value = True
    child.kill.side_effect = lambda: setattr(child.is_running, "return_value", False)
    parent = Mock()
    parent.children.return_value = [child]
    parent.is_running.return_value = True

    def request(_):
        parent.is_running.return_value = False
        return True

    control = process.SystemProcessControl()
    with (
        patch.object(process, "is_windows", return_value=True),
        patch.object(process.psutil, "Process", return_value=parent),
        patch("akaribot.cli.windows.request_stop", side_effect=request) as graceful,
        patch.object(process.os, "kill", side_effect=AssertionError("unsafe Windows signal")),
    ):
        outcome = process.stop_process(pid=42, running=parent.is_running, timeout=0, reap_grace=0, control=control)
    return (
        outcome.ok
        and outcome.forced
        and graceful.call_args.args == (42,)
        and child.kill.call_count == 1
        and parent.kill.call_count == 0
    )


def _test_process_tree_failure_is_not_success():
    control = SimpleNamespace(
        process_group=lambda _: 42,
        terminate=lambda *_, **__: True,
        terminate_group=lambda *_, **__: False,
        group_alive=lambda _: True,
        sleep=lambda _: None,
    )
    outcome = process.stop_process(pid=42, running=lambda: False, timeout=0, reap_grace=0, control=control)
    return not outcome.ok and outcome.forced


def _test_windows_force_uses_saved_process_identity():
    parent = Mock()
    parent.children.return_value = []
    parent.is_running.return_value = False
    control = process.SystemProcessControl()
    with patch.object(process, "is_windows", return_value=True):
        with patch.object(process.psutil, "Process", return_value=parent):
            control.process_group(42)
        with patch.object(process.psutil, "Process", side_effect=AssertionError("PID reused")):
            result = control.terminate(42, force=True)
    return result and not parent.kill.called


def _test_core_environment_binds_target_configuration():
    target = Instance.detached(Path("/tmp/akari-target").resolve())
    with patch.dict(os.environ, {"AKARI_CONFIG_PATH": "/tmp/source/config", "AKARI_CONFIG_READONLY": "1"}):
        environment = target.core_env()
        explicit = target.core_env(AKARI_CONFIG_PATH="/tmp/explicit/config", AKARI_CONFIG_READONLY="1")
    from akaribot.cli.tui.cli_process import cli_env

    with patch.dict(os.environ, {"AKARI_CONFIG_PATH": "/tmp/source/config", "AKARI_CONFIG_READONLY": "1"}):
        cli_environment = cli_env(target.root)
    return (
        environment["AKARI_CONFIG_PATH"] == str(target.config_dir)
        and "AKARI_CONFIG_READONLY" not in environment
        and explicit["AKARI_CONFIG_PATH"] == "/tmp/explicit/config"
        and explicit["AKARI_CONFIG_READONLY"] == "1"
        and cli_environment["AKARI_CONFIG_PATH"] == str(target.config_dir)
        and "AKARI_CONFIG_READONLY" not in cli_environment
    )


def _test_windows_record_avoids_locked_byte():
    with TemporaryDirectory(prefix="akari-windows-record-") as raw:
        path = Path(raw) / ".bot.lock"
        path.write_bytes(b'\n{"pid":42,"argv":[]}')
        with patch.object(process, "is_windows", return_value=True):
            record = process.read_lock_record(path)
            path.write_bytes(b'{"pid":42,"argv":[]}')
            legacy = process.read_lock_record(path)
    return record is not None and record.pid == 42 and legacy is None


def _test_windows_force_discovers_new_children():
    parent, child, grandchild = Mock(), Mock(), Mock()
    for process_mock in (parent, child, grandchild):
        process_mock.is_running.return_value = True
        process_mock.kill.side_effect = lambda item=process_mock: setattr(item.is_running, "return_value", False)
        process_mock.children.return_value = []
    control = process.SystemProcessControl()
    with patch.object(process, "is_windows", return_value=True):
        with patch.object(process.psutil, "Process", return_value=parent):
            control.process_group(42)
        parent.children.return_value = [child]
        child.suspend.side_effect = lambda: setattr(child.children, "return_value", [grandchild])
        result = control.terminate_group(42, force=True)
    return result and all(item.suspend.called and item.kill.called for item in (parent, child, grandchild))


@func_case
async def test_process_control(tester: Tester):
    await tester.test(_test_windows_detach_uses_subprocess_flags, "Windows 后台启动使用有效进程标志")
    await tester.test(_test_windows_stop_waits_for_children, "Windows 正常停止后收拢残留子进程")
    await tester.test(_test_process_tree_failure_is_not_success, "残留进程无法清理时停止失败")
    await tester.test(_test_windows_force_uses_saved_process_identity, "强制停止不重新认领复用的 PID")
    await tester.test(_test_core_environment_binds_target_configuration, "实例子进程使用目标配置且只读状态不泄漏")
    await tester.test(_test_windows_record_avoids_locked_byte, "Windows 记录读取避开首字节锁并拒绝旧记录")
    await tester.test(_test_windows_force_discovers_new_children, "强制停止冻结并清理等待期间的新后代")
    return tester
