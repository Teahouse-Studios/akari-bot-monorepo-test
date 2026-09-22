"""tools/check_test_baseline.py 的失败集合对拍测试。

CI 的第一轮 step 曾经因为 runner 的退出码直接变红，后面的「只读包目录」一轮根本没跑过；而
「失败集合与基线逐名一致」也从来没有被检查。此处固定四种判定：一致才通过，新增、消失、错误
文本变化都必须失败——只比数量会让「修好一个、坏掉一个」蒙混过关。
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

from akaribot.testing import func_case, Tester

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "check_test_baseline.py"

JUNIT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites tests="2" failures="{failures}">
  <testsuite name="Function Tests" tests="2" failures="{failures}">
    <testcase name="test_ok" classname="FunctionTest.1" time="0.1"/>
{body}  </testsuite>
</testsuites>
"""


def _tool():
    """按路径加载工具模块。"""
    spec = importlib.util.spec_from_file_location("check_test_baseline_under_test", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(tmp: Path, failures: list[tuple[str, str, str]]) -> Path:
    """写一份 junit.xml，failures 为 (用例名, 类型, 消息)。"""
    body = "".join(
        f'    <testcase name="{name}" classname="FunctionTest.{index}" time="0.1">\n'
        f'      <{kind} message="{message}">trace</{kind}>\n'
        f"    </testcase>\n"
        for index, (name, kind, message) in enumerate(failures, start=2)
    )
    path = tmp / "junit.xml"
    path.write_text(JUNIT_TEMPLATE.format(failures=len(failures), body=body), encoding="utf-8")
    return path


def _write_baseline(tmp: Path, failures: list[tuple[str, str, str]]) -> Path:
    """写一份基线清单。"""
    path = tmp / "baseline.txt"
    lines = ["# 注释行应被忽略", *(f"{name}\t{kind}\t{message}" for name, kind, message in failures)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _run(junit: Path, baseline: Path, *extra: str) -> int:
    """调用入口并返回退出码。"""
    return _tool().main(["--junit", str(junit), "--baseline", str(baseline), *extra])


def _test_identical_sets_pass():
    """逐名一致时通过，注释行不参与比对。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        failures = [("test_tos", "failure", "Function test failed")]
        code = _run(_write(tmp, failures), _write_baseline(tmp, failures))
    return code == 0


def _test_new_failure_fails():
    """基线之外多出一条失败必须判失败。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        baseline = [("test_tos", "failure", "Function test failed")]
        actual = [*baseline, ("test_new", "failure", "Function test failed")]
        code = _run(_write(tmp, actual), _write_baseline(tmp, baseline))
    return code == 1


def _test_vanished_failure_fails():
    """基线里还留着已经不会失败的条目时必须失败，逼基线同步缩小。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        baseline = [
            ("test_tos", "failure", "Function test failed"),
            ("test_fixed", "failure", "Function test failed"),
        ]
        actual = [("test_tos", "failure", "Function test failed")]
        code = _run(_write(tmp, actual), _write_baseline(tmp, baseline))
    return code == 1


def _test_changed_message_fails_even_when_count_matches():
    """数量没变但错误文本变了同样失败：这正是「只比数量」会漏掉的情形。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        baseline = [("test_tos", "failure", "Subtest raised KeyError")]
        actual = [("test_tos", "failure", "Subtest raised ValueError")]
        code = _run(_write(tmp, actual), _write_baseline(tmp, baseline))
    return code == 1


def _test_kind_change_is_reported_as_changed():
    """同一用例由 failure 变 error 属于文本变化，不能当成新增加消失各一条糊过去。"""
    tool = _tool()
    baseline = [tool.Failure("test_x", "failure", "boom")]
    actual = [tool.Failure("test_x", "error", "boom")]
    vanished, added, changed = tool.compare(baseline, actual)
    return vanished == [] and added == [] and len(changed) == 1


def _test_update_rewrites_baseline():
    """--update 用实际集合重写基线，之后对拍必须通过。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        failures = [("test_new", "error", "boom")]
        junit = _write(tmp, failures)
        baseline = _write_baseline(tmp, [])
        updated = _run(junit, baseline, "--update")
        checked = _run(junit, baseline)
    return updated == 0 and checked == 0


def _test_missing_junit_is_an_input_error():
    """junit.xml 不存在时是输入错误（2），不是「集合不一致」。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        code = _run(tmp / "absent.xml", _write_baseline(tmp, []))
    return code == 2


def _test_malformed_baseline_line_is_an_input_error():
    """基线行不是三段制时报输入错误，不静默跳过。"""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        baseline = tmp / "baseline.txt"
        baseline.write_text("only-one-column\n", encoding="utf-8")
        code = _run(_write(tmp, []), baseline)
    return code == 2


@func_case
async def test_check_test_baseline(tester: Tester):
    """tools.check_test_baseline: 失败集合对拍测试"""
    await tester.test(_test_identical_sets_pass, "逐名一致时通过")
    await tester.test(_test_new_failure_fails, "新增失败判失败")
    await tester.test(_test_vanished_failure_fails, "基线残留判失败")
    await tester.test(_test_changed_message_fails_even_when_count_matches, "数量不变但文本变化判失败")
    await tester.test(_test_kind_change_is_reported_as_changed, "failure 变 error 属文本变化")
    await tester.test(_test_update_rewrites_baseline, "--update 重写基线后可通过对拍")
    await tester.test(_test_missing_junit_is_an_input_error, "缺 junit 报输入错误")
    await tester.test(_test_malformed_baseline_line_is_an_input_error, "基线格式错误报输入错误")
    return tester
