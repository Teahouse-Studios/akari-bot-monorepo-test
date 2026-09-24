"""测试运行器的命令行选项：筛选、CI 与覆盖率。

CLI 曾把路径、``--case``、``--ci``、``--coverage`` 拼进 ``sys.argv``，而 runner 完全不解析参数：
``--ci`` 仍是非 CI 模式（遇到人工复核用例会挂住等待输入）、``--coverage`` 不启用覆盖率、
path 与 ``--case`` 不筛选。``IS_CI`` / ``ENABLE_COVERAGE`` 在**导入期**读取，所以两个模式开关
必须在那之前就被识别——本文件同时固定「解析结果」与「导入期取值」两层。
"""

import importlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from akaribot.testing import Tester, func_case
from akaribot.testing import runner

REPO_ROOT = Path(__file__).resolve().parents[3]
SAMPLE = REPO_ROOT / "tests" / "unit" / "test_registry_release.py"


def _test_parse_paths_and_cases():
    options = runner.parse_options(["a/b.py", "c/", "--case", "one", "--case", "two"])
    return options.paths == ("a/b.py", "c/") and options.cases == ("one", "two")


def _test_parse_mode_flags():
    plain = runner.parse_options([])
    both = runner.parse_options(["--ci", "--coverage"])
    return plain.ci is False and plain.coverage is False and both.ci is True and both.coverage is True


def _test_prescan_ignores_unrelated_arguments():
    ci, coverage = runner._prescan_mode_flags(["--ci", "--unknown", "some/path"])
    plain, none = runner._prescan_mode_flags(["some/path", "--case", "x"])
    return (ci, coverage) == (True, False) and (plain, none) == (False, False)


def _test_import_time_flags_follow_argv():
    script = (
        "import sys; sys.argv = ['akaribot.testing'] + {argv!r};"
        " from akaribot.testing import runner;"
        " print(runner.IS_CI, runner.ENABLE_COVERAGE)"
    )
    env = {**os.environ, "MPLCONFIGDIR": "/tmp/mplconfig"}
    env.pop("CI", None)
    env.pop("COVERAGE", None)
    results = []
    for argv in ([], ["--ci"], ["--coverage"], ["--ci", "--coverage"]):
        proc = subprocess.run(
            [sys.executable, "-c", script.format(argv=argv)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env=env,
            timeout=180,
        )
        results.append(proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else f"ERR {proc.stderr[-200:]}")
    return results == [
        "False False",
        "True False",
        "False True",
        "True True",
    ]


def _test_explicit_path_selects_single_file():
    files = runner._explicit_test_files.__wrapped__ if hasattr(runner._explicit_test_files, "__wrapped__") else None
    original = runner.OPTIONS
    try:
        runner.OPTIONS = runner.RunOptions(paths=(str(SAMPLE),))
        collected = runner._collect_test_files()
    finally:
        runner.OPTIONS = original
    return files is None and collected == [str(SAMPLE.resolve())]


def _test_directory_path_expands_to_python_files():
    with tempfile.TemporaryDirectory(prefix="akari-testing-opts-") as raw:
        root = Path(raw)
        (root / "nested").mkdir()
        (root / "test_a.py").write_text("", encoding="utf-8")
        (root / "nested" / "test_b.py").write_text("", encoding="utf-8")
        (root / "notes.txt").write_text("", encoding="utf-8")
        original = runner.OPTIONS
        try:
            runner.OPTIONS = runner.RunOptions(paths=(str(root),))
            collected = runner._collect_test_files()
        finally:
            runner.OPTIONS = original
    return len(collected) == 2 and all(path.endswith(".py") for path in collected)


def _test_unmatched_path_yields_nothing():
    original = runner.OPTIONS
    try:
        runner.OPTIONS = runner.RunOptions(paths=("tests/unit/definitely_absent.py",))
        collected = runner._collect_test_files()
    finally:
        runner.OPTIONS = original
    return collected == []


def _test_default_collection_is_unchanged_without_paths():
    original = runner.OPTIONS
    try:
        runner.OPTIONS = runner.RunOptions()
        collected = runner._collect_test_files()
    finally:
        runner.OPTIONS = original
    return len(collected) > 10 and any(path.endswith("test_registry_release.py") for path in collected)


def _test_cli_test_command_passes_modes_as_environment():
    source = (REPO_ROOT / "packages" / "akari-bot-cli" / "akaribot" / "cli" / "commands" / "test.py").read_text(
        encoding="utf-8"
    )
    return 'env["CI"] = "1"' in source and 'env["COVERAGE"] = "1"' in source and "run_module(" in source


def _reload_runner():
    return importlib.reload(runner)


@func_case
async def test_testing_options(tester: Tester):
    """akaribot.testing.runner: 命令行选项与筛选测试"""
    await tester.test(_test_parse_paths_and_cases, "位置参数与 --case 收集")
    await tester.test(_test_parse_mode_flags, "--ci 与 --coverage 各自独立")
    await tester.test(_test_prescan_ignores_unrelated_arguments, "预扫描忽略无关参数")
    await tester.test(_test_import_time_flags_follow_argv, "导入期取值跟随 argv")
    await tester.test(_test_explicit_path_selects_single_file, "文件路径只收该文件")
    await tester.test(_test_directory_path_expands_to_python_files, "目录递归收 *.py")
    await tester.test(_test_unmatched_path_yields_nothing, "不存在的路径收不到文件")
    await tester.test(_test_default_collection_is_unchanged_without_paths, "无位置参数时按默认根收集")
    await tester.test(_test_cli_test_command_passes_modes_as_environment, "CLI 经环境变量传模式")
    return tester
