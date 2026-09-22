"""tools/check_versions.py 的跳过豁免解析测试。

这道闸曾经被自己的一次提交说明关掉：工具引入提交在正文里解释功能时写了两次旧标记，于是
整个区间的版本守卫静默放行，之后一百多个提交的重构等于没有检查。故此处固定「正文提到不算、
独立 trailer 才算」以及「豁免绑定到具体分发」两条语义。
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

from akaribot.testing import func_case, Tester

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "check_versions.py"
TOKEN = "Skip-Version"
# 曾把整段区间放行的提交：正文里两次提到旧标记，但从未写过独立 trailer。
POISONED_COMMIT = "b337364d3"
# 拆分之后的区间基准：此时各包已存在，未升版本必须被抓出来。
MID_BRANCH_BASE = "b337364d3"

PROSE_WITH_OLD_MARKER = (
    "feat(tools): 变更检测与版本守卫（T6.1/T6.2）\n"
    "\n"
    "提交信息写 [skip-version] 时放行。\n"
    "注意 [skip-version] 只是说明，不是声明。\n"
)


def _tool():
    """按路径加载工具模块；dataclass 需要模块先进 sys.modules。"""
    spec = importlib.util.spec_from_file_location("check_versions_under_test", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _commit_exists(ref: str) -> bool:
    """提交是否存在于当前仓库；历史被改写时相关用例退化为通过。"""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _test_prose_mention_is_not_an_exemption():
    """正文里提到 token 不算声明——这是把整段区间放行的那次事故的复现。"""
    tool = _tool()
    return tool.parse_exemption(PROSE_WITH_OLD_MARKER, TOKEN) is None


def _test_real_guard_commit_is_not_an_exemption():
    """真实的那次提交正文含旧标记两次，解析结果必须是「没有声明」。"""
    if not _commit_exists(POISONED_COMMIT):
        return True
    message = subprocess.run(
        ["git", "log", "-1", "--format=%B", POISONED_COMMIT],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return "[skip-version]" in message and _tool().parse_exemption(message, TOKEN) is None


def _test_only_last_paragraph_counts():
    """trailer 段之后的正文会让声明失效：与 git 的 trailer 约定一致。"""
    tool = _tool()
    trailing = "fix: x\n\nSkip-Version: true\n\n后面还有正文。\n"
    proper = "fix: x\n\n说明文字。\n\nSkip-Version: true\n"
    indented = "fix: x\n\n示例：\n\n    Skip-Version: true\n\n说明。\n"
    return (
        tool.parse_exemption(trailing, TOKEN) is None
        and tool.parse_exemption(proper, TOKEN) == ()
        and tool.parse_exemption(indented, TOKEN) is None
    )


def _test_exemption_can_name_packages():
    """逗号分隔的分发名只豁免列出的成员，不再一个标记放行全部。"""
    tool = _tool()
    named = tool.parse_exemption("fix: x\n\nSkip-Version: akari-bot-core, akari-bot-module-wiki\n", TOKEN)
    hash_form = tool.parse_exemption("fix: x\n\nSkip-Version #akari-bot-core\n", TOKEN)
    return named == ("akari-bot-core", "akari-bot-module-wiki") and hash_form == ("akari-bot-core",)


def _test_empty_exemption_value_is_an_error():
    """写了 trailer 却没给取值时必须报错，不能静默当作没有声明。"""
    tool = _tool()
    try:
        tool.parse_exemption("fix: x\n\nSkip-Version:\n", TOKEN)
    except tool.ConfigError:
        return True
    return False


def _test_guard_reports_unbumped_packages_after_split():
    """拆分之后的区间里，未升版本的包必须被抓出来——豁免不再放行整个区间。"""
    if not _commit_exists(MID_BRANCH_BASE):
        return True
    tool = _tool()
    original = sys.argv
    try:
        sys.argv = ["check_versions.py", "--base", MID_BRANCH_BASE]
        code = tool.main()
    finally:
        sys.argv = original
    return code == 1


def _test_new_packages_do_not_count_as_unbumped():
    """相对 master 各包都是新建的，没有旧版本可比，不应报成未升版本。"""
    tool = _tool()
    original = sys.argv
    try:
        sys.argv = ["check_versions.py", "--base", "master"]
        code = tool.main()
    finally:
        sys.argv = original
    return code == 0


@func_case
async def test_check_versions(tester: Tester):
    """tools.check_versions: 版本守卫豁免解析测试"""
    await tester.test(_test_prose_mention_is_not_an_exemption, "正文提到 token 不算声明")
    await tester.test(_test_real_guard_commit_is_not_an_exemption, "真实事故提交不再放行区间")
    await tester.test(_test_only_last_paragraph_counts, "只认最后一段的 trailer")
    await tester.test(_test_exemption_can_name_packages, "豁免可绑定到具体分发")
    await tester.test(_test_empty_exemption_value_is_an_error, "trailer 无取值时报错")
    await tester.test(_test_guard_reports_unbumped_packages_after_split, "拆分后区间仍能抓出未升版本包")
    await tester.test(_test_new_packages_do_not_count_as_unbumped, "新建包不报未升版本")
    return tester
