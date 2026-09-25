"""命令页：CLI 命令面的导出、参数收集与执行。

本文件固定三条链路：命令清单直接从 CLI 的命令树导出（CLI 加子命令后界面自动跟上），参数按
声明类型收集成 argv，执行仍是 ``akaribot <子命令>`` 子进程。
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.commands import (
    KIND_ARGUMENT,
    KIND_FLAG,
    KIND_OPTION,
    CommandEntry,
    CommandParam,
    StaticCommandCatalog,
    StaticCommandSource,
    build_catalog,
)
from akaribot.testing import Tester, func_case

# 界面必须能到达的命令。CLI 增删子命令时这里先失败，避免命令面悄悄缺一块。
REQUIRED_COMMANDS = (
    "init",
    "run",
    "test",
    "doctor",
    "tui",
    "migrate legacy",
    "new module",
    "new adapter",
    "module list",
    "module available",
    "module add",
    "module remove",
    "module update",
    "module load",
    "module unload",
    "config list",
    "config schema",
    "config get",
    "config set",
    "config open",
    "adapter list",
    "adapter instance add",
    "adapter instance remove",
    "venv status",
    "venv adopt",
    "venv release",
    "venv recreate",
)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _param(name: str, kind: str, **kwargs) -> CommandParam:
    return CommandParam(name=name, kind=kind, **kwargs)


CATALOG = StaticCommandCatalog(
    [
        CommandEntry(path=("venv", "status"), summary="查看 venv 托管状态"),
        CommandEntry(
            path=("module", "remove"),
            summary="卸载模块",
            params=(
                _param("name", KIND_ARGUMENT, required=True),
                _param("purge_data", KIND_FLAG, flags=("--purge-data",)),
                _param("yes", KIND_FLAG, flags=("--yes", "-y"), secondary=("--no-yes",)),
                _param("extra", KIND_OPTION, flags=("--extra",), multiple=True),
            ),
        ),
        CommandEntry(
            path=("config", "get"),
            summary="读取配置项",
            params=(
                _param("key", KIND_ARGUMENT, required=True),
                _param("table", KIND_OPTION, flags=("--table", "-t"), required=True),
            ),
        ),
    ]
)


async def _with_page(source, body, catalog=CATALOG):
    app = TuiApp(sources={"commands": source, "commands_catalog": catalog}, initial_page="commands")
    async with compat.app_test(app, size=(110, 34)) as pilot:
        page = app.query_one("#page-commands")
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


def _rows(page) -> tuple[str, ...]:
    return page.row_texts()


def _select(page, name: str) -> None:
    page._selected = name
    page._render_rows()


def _fill(page, name: str, value: str) -> None:
    control = page.query_one(f"#param-{name}", compat.Input)
    control.value = value


def _toggle(page, name: str) -> None:
    control = page.query_one(f"#param-{name}", compat.Checkbox)
    control.value = not control.value


async def _test_catalog_covers_cli_surface():
    # 命令清单从 CLI 自身导出，界面因此不会漏掉任何已注册的子命令。
    catalog = build_catalog()
    names = {entry.name() for entry in catalog}
    missing = [name for name in REQUIRED_COMMANDS if name not in names]
    return not missing and all(entry.path for entry in catalog)


async def _test_catalog_reads_params_from_cli():
    # 参数种类、必填与默认值都取自 CLI 声明，不在界面里另写一份。
    catalog = {entry.name(): entry for entry in build_catalog()}
    remove = {param.name: param for param in catalog["module remove"].params}
    get = {param.name: param for param in catalog["config get"].params}
    run = {param.name: param for param in catalog["run"].params}
    return (
        remove["purge_data"].kind == KIND_FLAG
        and not remove["purge_data"].required
        and remove["name"].required
        and get["table"].required
        and "-t" in get["table"].flags
        # 透传分组补一个自由输入，未识别参数才有地方填。
        and "extra" in run
        and run["extra"].multiple
    )


async def _test_catalog_skips_framework_params():
    # 帮助与实例根由框架处理：实例根经环境变量钉住，界面不该再暴露一次。
    catalog = build_catalog()
    for entry in catalog:
        labels = {param.label() for param in entry.params}
        if "--help" in labels or "--instance" in labels:
            return False
    return True


async def _test_page_lists_every_command():
    async def body(app, page, pilot):
        rows = _rows(page)
        await pilot.press("q")
        return len(rows), len(CATALOG.commands())

    listed, total = await _with_page(StaticCommandSource(), body)
    return listed == total


async def _test_search_narrows_list():
    async def body(app, page, pilot):
        page.set_query("venv")
        await pilot.pause()
        narrowed = _rows(page)
        page.set_query("")
        await pilot.pause()
        restored = _rows(page)
        await pilot.press("q")
        return len(narrowed), len(restored)

    narrowed, restored = await _with_page(StaticCommandSource(), body)
    return narrowed == 1 and restored == 3


async def _test_run_collects_arguments():
    source = StaticCommandSource(lines=["ok"])

    async def body(app, page, pilot):
        _select(page, "config get")
        await pilot.pause()
        _fill(page, "key", "enable")
        _fill(page, "table", "module_wiki")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return list(source.calls), page.status_text

    calls, status = await _with_page(source, body)
    return calls == [("config", "get", "enable", "--table", "module_wiki")] and "config get" in status


async def _test_required_param_blocks_run():
    source = StaticCommandSource()

    async def body(app, page, pilot):
        _select(page, "config get")
        await pilot.pause()
        _fill(page, "key", "enable")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return list(source.calls), page.status_text

    calls, status = await _with_page(source, body)
    return calls == [] and "必填" in status


async def _test_flags_and_repeats_expand_to_argv():
    source = StaticCommandSource()

    async def body(app, page, pilot):
        _select(page, "module remove")
        await pilot.pause()
        _fill(page, "name", "wiki")
        _fill(page, "extra", "alpha beta")
        _toggle(page, "yes")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return list(source.calls)

    calls = await _with_page(source, body)
    # 展开顺序即命令声明顺序：位置参数在前，其余按声明逐个展开。
    return calls == [("module", "remove", "wiki", "--yes", "--extra", "alpha", "--extra", "beta")]


async def _test_default_on_flag_can_be_negated():
    # 默认开启的开关取消勾选时要显式取反，否则子进程仍按默认值执行。
    source = StaticCommandSource()
    catalog = StaticCommandCatalog(
        [
            CommandEntry(
                path=("module", "update"),
                params=(_param("yes", KIND_FLAG, flags=("--yes",), secondary=("--no-yes",), default=True),),
            )
        ]
    )

    async def body(app, page, pilot):
        _select(page, "module update")
        await pilot.pause()
        _toggle(page, "yes")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return list(source.calls)

    calls = await _with_page(source, body, catalog)
    return calls == [("module", "update", "--no-yes")]


async def _test_failure_reports_exit_code():
    source = StaticCommandSource(lines=["boom"], code=3)

    async def body(app, page, pilot):
        _select(page, "venv status")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return page.status_text, page.output_text

    status, output = await _with_page(source, body)
    return "3" in status and "boom" in output


async def _test_output_keeps_tail():
    lines = [f"line-{index}" for index in range(60)]
    source = StaticCommandSource(lines=lines)

    async def body(app, page, pilot):
        _select(page, "venv status")
        await pilot.pause()
        page.run_selected()
        await page.wait_for_idle()
        await pilot.pause()
        return page.output_text

    output = await _with_page(source, body)
    return output.splitlines() == lines


async def _test_stop_asks_source_to_terminate():
    source = StaticCommandSource()

    async def body(app, page, pilot):
        page._busy = True
        page.action_stop()
        await pilot.pause()
        page._busy = False
        return source.stopped, page.status_text

    stopped, status = await _with_page(source, body)
    return stopped == 1 and status


FAKE_CLI_ECHO_ARGV = """#!/usr/bin/env python3
import sys

print(" ".join(sys.argv[1:]))
sys.exit(0)
"""


async def _test_subprocess_source_prefixes_language():
    # 语言随界面走：子进程在导入期读 --lang，不传就会用默认语言输出。
    from akaribot.cli.tui.commands import SubprocessCommandSource

    with TemporaryDirectory(prefix="akari-commands-") as raw:
        root = Path(raw)
        fake = root / "fake_cli"
        fake.write_text(FAKE_CLI_ECHO_ARGV, encoding="utf-8")
        fake.chmod(0o755)
        lines: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": str(fake)}):
            source = SubprocessCommandSource(root=root, timeout=30.0)
            result = await source.run(("venv", "status"), lines.append)
    return result.ok and lines == ["--lang zh_cn venv status"]


@func_case
async def test_tui_commands(tester: Tester):
    """cli.tui.commands: 命令面导出、参数收集与执行测试"""
    _use_cli_locale()
    await tester.test(_test_catalog_covers_cli_surface, "命令清单覆盖 CLI 全部子命令")
    await tester.test(_test_catalog_reads_params_from_cli, "参数种类与必填取自 CLI 声明")
    await tester.test(_test_catalog_skips_framework_params, "帮助与实例根不进参数表单")
    await tester.test(_test_page_lists_every_command, "列表展示全部命令")
    await tester.test(_test_search_narrows_list, "搜索收窄命令列表")
    await tester.test(_test_run_collects_arguments, "按表单收集位置参数与选项")
    await tester.test(_test_required_param_blocks_run, "必填缺失时不执行")
    await tester.test(_test_flags_and_repeats_expand_to_argv, "开关与可重复选项展开成 argv")
    await tester.test(_test_default_on_flag_can_be_negated, "默认开启的开关取消时显式取反")
    await tester.test(_test_failure_reports_exit_code, "失败时回报退出码与输出")
    await tester.test(_test_output_keeps_tail, "输出面板保留完整输出")
    await tester.test(_test_stop_asks_source_to_terminate, "Esc 终止正在跑的命令")
    await tester.test(_test_subprocess_source_prefixes_language, "真源按界面语言传 --lang")
    return tester
