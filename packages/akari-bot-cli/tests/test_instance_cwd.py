"""实例子进程 cwd 锚定测试。

CLI 允许从实例外操作实例（``-I`` 或 ``AKARI_INSTANCE_DIR``）。子进程若继承调用方的 cwd，
实例内的相对路径就会落到调用目录，因此 ``_run`` 与 ``_capture`` 都必须以实例根为 cwd。
"""

import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import akaribot.cli.instance as instance_module
from akaribot.cli.instance import INSTANCE_DIR_ENV, Instance, InstanceMeta, system_python
from akaribot.testing import Tester, func_case


def _make_instance(root: Path) -> Instance:
    return Instance(root, python_override=system_python(), meta=InstanceMeta.create(root))


def _test_call_arguments_anchor_instance_cwd():
    with TemporaryDirectory() as temp:
        root = Path(temp) / "instance"
        root.mkdir()
        instance = _make_instance(root)
        seen = []

        def fake_run(argv, **kwargs):
            seen.append(kwargs)
            return subprocess.CompletedProcess(list(argv), 0, "", "")

        with patch.object(instance_module.subprocess, "run", fake_run):
            code = instance._run(["<python>", "-c", ""])
            captured = instance._capture(["<python>", "-c", ""], timeout=5.0)
        return (
            code == 0
            and captured.returncode == 0
            and len(seen) == 2
            and all(kwargs["cwd"] == str(instance.root) for kwargs in seen)
            and all(kwargs["env"][INSTANCE_DIR_ENV] == str(instance.root) for kwargs in seen)
        )


def _test_captured_child_runs_in_instance_root():
    with TemporaryDirectory() as temp:
        root = Path(temp) / "instance"
        root.mkdir()
        instance = _make_instance(root)
        if str(instance.root) == os.getcwd():
            return False
        completed = instance.run_python_capture("-c", "import os; print(os.getcwd())", timeout=60.0)
        return completed.returncode == 0 and (completed.stdout or "").strip() == str(instance.root)


def _test_run_child_writes_inside_instance_root():
    with TemporaryDirectory() as temp:
        root = Path(temp) / "instance"
        root.mkdir()
        instance = _make_instance(root)
        if str(instance.root) == os.getcwd():
            return False
        probe = instance.root / "child_cwd.txt"
        code = instance._run(
            instance.python_argv(
                "-c",
                "import os, pathlib, sys; pathlib.Path(sys.argv[1]).write_text(os.getcwd())",
                str(probe),
            )
        )
        return code == 0 and probe.is_file() and probe.read_text(encoding="utf-8") == str(instance.root)


@func_case
async def test_instance_process_cwd(tester: Tester):
    """实例子进程一律以实例根为 cwd，从实例外调用也不例外。"""
    await tester.test(_test_call_arguments_anchor_instance_cwd, "子进程调用参数带实例根 cwd")
    await tester.test(_test_captured_child_runs_in_instance_root, "捕获式子进程的 cwd 为实例根")
    await tester.test(_test_run_child_writes_inside_instance_root, "继承标准流的子进程 cwd 为实例根")
    return tester
