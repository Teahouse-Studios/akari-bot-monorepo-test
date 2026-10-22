"""tools/check_versions.py 的跳过豁免解析测试。

此处固定两条语义：正文里提到 token 不算声明，只有独立 trailer 才算；豁免绑定到具体分发，
而不是一个标记放行整个区间——否则解释功能的一句话就能关掉整段区间的检查。
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from akaribot.testing import func_case, Tester

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "check_versions.py"
TOKEN = "Skip-Version"
# 曾把整段区间放行的提交：正文里两次提到旧标记，但从未写过独立 trailer。
POISONED_COMMIT = "b337364d3"
# 版本守卫依赖真实历史时会被区间内的豁免声明左右，故用例自建仓库夹具。
FIXTURE_ROOT_PYPROJECT = '[tool.uv.workspace]\nmembers = ["packages/*"]\n'
FIXTURE_MEMBER_PYPROJECT = '[project]\nname = "example"\nversion = "0.1.0"\ndependencies = []\n'

PROSE_WITH_OLD_MARKER = (
    "feat(tools): 变更检测与版本守卫（T6.1/T6.2）\n"
    "\n"
    "提交信息写 [skip-version] 时放行。\n"
    "注意 [skip-version] 只是说明，不是声明。\n"
)


def _tool():
    spec = importlib.util.spec_from_file_location("check_versions_under_test", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _commit_exists(ref: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _test_prose_mention_is_not_an_exemption():
    tool = _tool()
    return tool.parse_exemption(PROSE_WITH_OLD_MARKER, TOKEN) is None


def _test_real_guard_commit_is_not_an_exemption():
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
    tool = _tool()
    named = tool.parse_exemption("fix: x\n\nSkip-Version: akari-bot-core, akari-bot-module-wiki\n", TOKEN)
    hash_form = tool.parse_exemption("fix: x\n\nSkip-Version #akari-bot-core\n", TOKEN)
    return named == ("akari-bot-core", "akari-bot-module-wiki") and hash_form == ("akari-bot-core",)


def _test_empty_exemption_value_is_an_error():
    tool = _tool()
    try:
        tool.parse_exemption("fix: x\n\nSkip-Version:\n", TOKEN)
    except tool.ConfigError:
        return True
    return False


def _init_fixture_repo(root: Path) -> str:
    member = root / "packages" / "example"
    member.mkdir(parents=True)
    (root / "pyproject.toml").write_text(FIXTURE_ROOT_PYPROJECT, encoding="utf-8")
    (member / "pyproject.toml").write_text(FIXTURE_MEMBER_PYPROJECT, encoding="utf-8")
    (member / "example.py").write_text("VALUE = 1\n", encoding="utf-8")
    identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.com", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", *identity, "commit", "-q", "-m", "init"], cwd=root, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.strip()


def _test_guard_reports_unbumped_packages_after_split():
    with tempfile.TemporaryDirectory() as directory:
        tmp_root = Path(directory)
        return _run_fixture_guard(tmp_root)


def _run_fixture_guard(tmp_root: Path) -> bool:
    base = _init_fixture_repo(tmp_root)
    member = tmp_root / "packages" / "example"
    (member / "example.py").write_text("VALUE = 2\n", encoding="utf-8")
    identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.com", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "add", "-A"], cwd=tmp_root, check=True)
    subprocess.run(["git", *identity, "commit", "-q", "-m", "fix: 改源码不升版本"], cwd=tmp_root, check=True)

    tool = _tool()
    received = {}
    original = sys.argv
    original_root = tool.PROJECT_ROOT
    original_pyproject = tool.ROOT_PYPROJECT
    try:
        tool.PROJECT_ROOT = tmp_root
        tool.ROOT_PYPROJECT = tmp_root / "pyproject.toml"
        sys.argv = ["check_versions.py", "--base", base]
        received["violation"] = tool.main()
        (member / "example.py").write_text("VALUE = 3\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=tmp_root, check=True)
        subprocess.run(
            ["git", *identity, "commit", "-q", "-m", "fix: 改源码不升版本\n\nSkip-Version: true"],
            cwd=tmp_root,
            check=True,
        )
        sys.argv = ["check_versions.py", "--base", base]
        received["exempt"] = tool.main()
    finally:
        tool.PROJECT_ROOT = original_root
        tool.ROOT_PYPROJECT = original_pyproject
        sys.argv = original
    return received["violation"] == 1 and received["exempt"] == 0


def _test_new_packages_do_not_count_as_unbumped():
    tool = _tool()
    original = sys.argv
    try:
        sys.argv = ["check_versions.py", "--base", "master"]
        code = tool.main()
    finally:
        sys.argv = original
    return code == 0


def _test_downgrade_is_a_violation():
    tool = _tool()
    member = tool.Member("example", "0.1.0", "packages/example", "packages/example/pyproject.toml")
    with patch.object(tool, "version_at", return_value=(True, "0.2.0")):
        finding = tool.inspect_member(member, ["packages/example/example.py"], "base", False)
    return finding.is_violation


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
    await tester.test(_test_downgrade_is_a_violation, "版本下调不能通过版本守卫")
    return tester
