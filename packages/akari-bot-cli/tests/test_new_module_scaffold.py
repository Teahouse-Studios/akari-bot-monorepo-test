"""``akaribot new module`` 脚手架渲染。

模板引用的上下文键必须与 :func:`akaribot.cli.commands.new.prepare_commands` 与
:func:`akaribot.cli.commands.new.prepare_test_cases` 产出的键一致。键名不一致时生成过程会在
README 与测试文件处抛出 jinja 未定义错误，本文件固定这两处的渲染结果。
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.commands.new import collect_plan, template_root, write_package
from akaribot.testing import Tester, func_case


def _build(target_root: Path) -> Path:
    plan = collect_plan(
        name="greet",
        desc=None,
        author="tester",
        license=None,
        aliases=[],
        platforms=[],
        excluded_platforms=[],
        components=["command"],
        commands=[],
        has_config=False,
        has_database=False,
        has_assets=False,
        has_data_dir=False,
        with_tests=True,
        non_interactive=True,
    )
    target = target_root / "akari-bot-module-greet"
    write_package(plan, template_root(None), target, False)
    return target


def _test_readme_documents_default_command():
    with TemporaryDirectory() as tmp:
        readme = (_build(Path(tmp)) / "README.md").read_text(encoding="utf-8")
    return "- `~greet`：执行 greet 的默认命令。" in readme


def _test_generated_test_file_calls_module_name():
    with TemporaryDirectory() as tmp:
        source = (_build(Path(tmp)) / "tests" / "test_greet.py").read_text(encoding="utf-8")
    return '"""default 命令返回预期文案。"""' in source and '"~greet",' in source


@func_case
async def test_new_module_scaffold(tester: Tester):
    """new module 脚手架渲染测试"""
    await tester.test(_test_readme_documents_default_command, "README 列出默认命令")
    await tester.test(_test_generated_test_file_calls_module_name, "用例以模块名调用默认命令")
    return tester
