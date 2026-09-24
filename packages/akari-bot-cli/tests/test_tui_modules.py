"""Modules 页的可安装列表与安装进度。

本文件固定两条链路：列表默认给出全部（已装与未装同列，未装项可直接选中安装），开关只用于收窄到
已装；安装与卸载把子进程输出逐行显示到状态栏，完整序列留在 ``stream_lines``，失败时输出尾部作为详情。
"""

import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.modules import ModuleRecord, ModuleSourceError, OperationResult, StaticModuleSource
from akaribot.testing import Tester, func_case

INSTALLED = ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed")
CANDIDATE = ModuleRecord(name="wiki", dist="akari-bot-module-wiki", version="0.2.0", summary="维基", state="available")
ADAPTER = ModuleRecord(
    name="telegram", dist="akari-bot-adapter-telegram", version="0.1.0", summary="", state="available"
)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticModuleSource:
    params = {
        "records": [INSTALLED],
        "available": [INSTALLED, CANDIDATE, ADAPTER],
        "stream_lines": ["Resolved 2 packages", "Installed 2 packages"],
    }
    params.update(kwargs)
    return StaticModuleSource(**params)


async def _boot(source: StaticModuleSource):
    app = TuiApp(source=source, boot_started_at=time.monotonic())
    return app


async def _with_app(source: StaticModuleSource, body) -> object:
    app = await _boot(source)
    async with compat.app_test(app, size=(100, 30)) as pilot:
        page = app.modules_page()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


def _filter_installed(app: TuiApp) -> None:
    # 勾选「只看已安装」。
    checkbox = app.modules_page().query_one("#installed-only", compat.Checkbox)
    checkbox.value = True


async def _test_lists_everything_by_default():
    # 默认列出全部：已装与未装同列，用户不必先知道名字再搜索。
    async def body(app, page, pilot):
        rows = tuple(record.dist for record in page.visible_records)
        await pilot.press("q")
        return rows, app.module_source.calls["available"]

    rows, available_calls = await _with_app(_source(), body)
    return (
        rows == ("akari-bot-module-dice", "akari-bot-adapter-telegram", "akari-bot-module-wiki")
        and available_calls == 1
    )


async def _test_toggle_filters_to_installed():
    # 勾选后收窄到已装，取消勾选后恢复全部。
    async def body(app, page, pilot):
        all_rows = tuple(record.dist for record in page.visible_records)
        _filter_installed(app)
        await page.wait_for_idle()
        await pilot.pause()
        filtered = tuple(record.dist for record in page.visible_records)
        page.query_one("#installed-only", compat.Checkbox).value = False
        await page.wait_for_idle()
        await pilot.pause()
        restored = tuple(record.dist for record in page.visible_records)
        await pilot.press("q")
        return all_rows, filtered, restored

    all_rows, filtered, restored = await _with_app(_source(), body)
    return len(all_rows) == 3 and filtered == ("akari-bot-module-dice",) and restored == all_rows


async def _test_uninstalled_record_is_installable():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 2  # 排序为：已装 dice、适配器 telegram、模块 wiki
        await pilot.pause()
        selected = page.selected_record
        install_button = page.query_one("#install", compat.Button)
        return (
            selected is not None and selected.dist == "akari-bot-module-wiki",
            install_button.disabled,
        )

    selected_is_wiki, disabled = await _with_app(_source(), body)
    return selected_is_wiki and disabled is False


async def _test_install_streams_output_to_status():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 2
        await pilot.pause()
        page.request_install()
        await page.wait_for_idle()
        await pilot.pause()
        return page.stream_lines, page.status_text, app.module_source.installed

    lines, status, installed = await _with_app(_source(), body)
    ok = (
        lines == ("Resolved 2 packages", "Installed 2 packages")
        and status.startswith(i18n.t("cli.tui.modules.stub_install_ok"))
        and installed == ["akari-bot-module-wiki"]
    )
    return ok


async def _test_uninstall_streams_output_to_status():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_uninstall()
        await page.wait_for_idle()
        await pilot.pause()
        return page.stream_lines, app.module_source.uninstalled

    lines, uninstalled = await _with_app(_source(), body)
    return lines == ("Resolved 2 packages", "Installed 2 packages") and uninstalled == ["akari-bot-module-dice"]


async def _test_failed_install_reports_detail():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_uninstall()
        await page.wait_for_idle()
        await pilot.pause()
        return page.status_text, page.last_error

    source = _source(
        uninstall_result=OperationResult(False, "卸载 akari-bot-module-dice失败", "boom: 依赖冲突"),
        stream_lines=["Resolved 1 package", "boom: 依赖冲突"],
    )
    status, last_error = await _with_app(source, body)
    return "boom: 依赖冲突" in status and last_error == "boom: 依赖冲突"


async def _test_available_failure_keeps_installed_list():
    class _BrokenAvailable(StaticModuleSource):
        def list_available(self):
            raise ModuleSourceError("registry 不可用")

    async def body(app, page, pilot):
        rows = tuple(record.dist for record in page.visible_records)
        return rows, page.status_text

    source = _BrokenAvailable(records=[INSTALLED], available=[CANDIDATE])
    rows, status = await _with_app(source, body)
    return (
        rows == ("akari-bot-module-dice",)
        and i18n.t("cli.tui.modules.available_failed", error="registry 不可用") in status
    )


async def _test_stream_operation_failure_becomes_result():
    class _Exploding(StaticModuleSource):
        async def stream_operation(self, kind, record, on_line):
            raise RuntimeError("子进程炸了")

    async def body(app, page, pilot):
        page.request_uninstall()
        await page.wait_for_idle()
        await pilot.pause()
        return page.status_text

    source = _Exploding(records=[INSTALLED])
    status = await _with_app(source, body)
    return "RuntimeError" in status and "子进程炸了" in status


# 假 CLI 写成带 shebang 的可执行文件：AKARIBOT_CLI_BIN 是单一路径，不按空格拆解释器与脚本。
FAKE_CLI_OK = """#!/usr/bin/env python3
import sys

for line in ("Resolved 2 packages", "Installed 2 packages"):
    print(line)
sys.exit(0)
"""

FAKE_CLI_FAIL = """#!/usr/bin/env python3
import sys

print("Resolved 1 package")
print("boom: 依赖冲突")
sys.exit(3)
"""

FAKE_CLI_SLOW = """#!/usr/bin/env python3
import time

time.sleep(30)
"""


def _fake_cli(root: Path, name: str, body: str) -> str:
    path = root / name
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return str(path)


async def _test_subprocess_source_streams_and_reports():
    # 用 AKARIBOT_CLI_BIN 指向一个假 CLI，既走完整的 spawn/读取/等待路径，又不必真的装包。
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-tui-src-") as raw:
        root = Path(raw)
        ok_cli = _fake_cli(root, "fake_ok", FAKE_CLI_OK)
        fail_cli = _fake_cli(root, "fake_fail", FAKE_CLI_FAIL)
        record = ModuleRecord(name="wiki", dist="akari-bot-module-wiki")
        collected: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": ok_cli}):
            ok_source = SubprocessModuleSource(root=root, timeout=30.0)
            ok_result = await ok_source.stream_operation("install", record, collected.append)
        failed: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fail_cli}):
            fail_source = SubprocessModuleSource(root=root, timeout=30.0)
            fail_result = await fail_source.stream_operation("install", record, failed.append)
    return (
        ok_result.ok
        and ok_result.message == i18n.t("cli.tui.modules.operation_done", label="安装 akari-bot-module-wiki")
        and collected == ["Resolved 2 packages", "Installed 2 packages"]
        and not fail_result.ok
        and "boom: 依赖冲突" in fail_result.detail
        and failed == ["Resolved 1 package", "boom: 依赖冲突"]
    )


async def _test_subprocess_source_timeout():
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-tui-src-") as raw:
        root = Path(raw)
        slow = _fake_cli(root, "fake_slow", FAKE_CLI_SLOW)
        record = ModuleRecord(name="wiki", dist="akari-bot-module-wiki")
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": slow}):
            source = SubprocessModuleSource(root=root, timeout=0.5)
            try:
                await source.stream_operation("install", record, lambda line: None)
            except ModuleSourceError as error:
                return "0" in str(error) or "超时" in str(error)
    return False


def _test_relative_root_is_resolved():
    # 实例根是子进程的 cwd 又写进 AKARI_INSTANCE_DIR，相对值会二次拼接（test/test）而找不到实例。
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-tui-root-") as raw:
        root = Path(raw)
        (root / "inst").mkdir()
        source = SubprocessModuleSource(root=Path(raw) / "inst" / ".." / "inst")
        relative = os.path.relpath(root / "inst", Path.cwd())
        relative_source = SubprocessModuleSource(root=relative)
    return (
        source.root.is_absolute()
        and source.root == (root / "inst").resolve()
        and relative_source.root.is_absolute()
        and relative_source.root == (root / "inst").resolve()
    )


async def _test_detail_shows_manifest_metadata():
    # 这些值来自 registry --json：`module list --json` 曾丢掉它们，界面因此对已装包显示「核心 API
    # 未声明」、提供模块为空，与 manifest 实际内容不符。
    record = ModuleRecord(
        name="wiki",
        dist="akari-bot-module-wiki",
        version="0.1.0",
        state="installed",
        kind="module",
        requires_core_api=">=1",
        provides_modules=("wiki", "wikilog"),
        owned_tables=("module_wiki_site_info",),
        config_table="module_wiki",
    )

    async def body(app, page, pilot):
        page.query_one("#module-list", compat.ListView).index = 0
        await pilot.pause()
        text = page.detail_text
        await pilot.press("q")
        return text

    detail = await _detail_of(record, body)
    return (
        ">=1" in detail
        and "wiki、wikilog" in detail
        and "module_wiki" in detail
        and "module_wiki_site_info" in detail
        and i18n.t("cli.tui.common.undeclared") not in detail
    )


async def _test_detail_falls_back_when_manifest_missing():
    record = ModuleRecord(name="plain", dist="akari-bot-module-plain", state="installed")

    async def body(app, page, pilot):
        page.query_one("#module-list", compat.ListView).index = 0
        await pilot.pause()
        text = page.detail_text
        await pilot.press("q")
        return text

    detail = await _detail_of(record, body)
    return i18n.t("cli.tui.common.undeclared") in detail


async def _detail_of(record, body):
    app = TuiApp(source=StaticModuleSource([record]), boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(100, 30)) as pilot:
        page = app.modules_page()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


@func_case
async def test_tui_modules_available(tester: Tester):
    """cli.tui.modules: 可安装列表与安装进度测试"""
    _use_cli_locale()
    await tester.test(_test_lists_everything_by_default, "默认列出已装与未装")
    await tester.test(_test_toggle_filters_to_installed, "开关在全部与只看已装之间切换")
    await tester.test(_test_uninstalled_record_is_installable, "未装项可安装")
    await tester.test(_test_install_streams_output_to_status, "安装输出逐行显示到状态栏")
    await tester.test(_test_uninstall_streams_output_to_status, "卸载输出逐行显示到状态栏")
    await tester.test(_test_failed_install_reports_detail, "失败时展示输出尾部")
    await tester.test(_test_available_failure_keeps_installed_list, "可安装集合失败不清空列表")
    await tester.test(_test_stream_operation_failure_becomes_result, "数据源异常转成结果展示")
    await tester.test(_test_subprocess_source_streams_and_reports, "真源逐行回调并给出结论")
    await tester.test(_test_subprocess_source_timeout, "真源超时按数据源错误上报")
    await tester.test(_test_relative_root_is_resolved, "相对实例根解析为绝对路径")
    await tester.test(_test_detail_shows_manifest_metadata, "详情展示 manifest 元数据")
    await tester.test(_test_detail_falls_back_when_manifest_missing, "manifest 缺失才显示未声明")
    return tester
