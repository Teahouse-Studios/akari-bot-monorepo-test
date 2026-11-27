"""``akaribot.cli.docs_engine.facts`` 的命令自省与失败降级测试。"""

from unittest.mock import patch

from akaribot.cli.docs_engine import facts
from akaribot.testing import Tester, func_case


async def _test_collects_known_commands():
    commands = facts.collect_cli_commands()
    return {"module add", "module remove", "docs build"} <= set(commands)


async def _test_module_add_options():
    entry = facts.collect_cli_commands().get("module add", {})
    options = entry.get("options") or []
    names = {name for option in options for name in option.get("names", [])}
    return (
        "--dist" in names
        and "--save" not in names
        and "module add" in str(entry.get("usage", ""))
        and bool(options)
        and all(option.get("names") for option in options)
    )


async def _test_entry_shape():
    entry = facts.collect_cli_commands().get("module add", {})
    arguments = entry.get("arguments") or []
    options = entry.get("options") or []
    return (
        bool(entry.get("summary"))
        and any(argument.get("name") == "name" and argument.get("required") is False for argument in arguments)
        and all(isinstance(option.get("isFlag"), bool) for option in options)
        and any(option.get("isFlag") and option.get("default") == "false" for option in options)
    )


async def _test_failure_returns_empty():
    with patch("typer.main.get_command", side_effect=RuntimeError("boom")):
        return facts.collect_cli_commands() == {}


@func_case
async def test_docs_facts(tester: Tester):
    """cli.docs_engine.facts 命令自省测试"""
    await tester.test(_test_collects_known_commands, "采集模块与文档子命令")
    await tester.test(_test_module_add_options, "module add 的选项、用法与名称")
    await tester.test(_test_entry_shape, "参数与选项字段结构")
    await tester.test(_test_failure_returns_empty, "自省失败时返回空映射")
    return tester
