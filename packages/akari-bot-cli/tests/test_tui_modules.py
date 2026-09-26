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


FAKE_CLI_ECHO_ARGV = """#!/usr/bin/env python3
import sys

print(" ".join(sys.argv[1:]))
sys.exit(0)
"""


UPDATE_INSTALLED = ModuleRecord(name="alpha", dist="akari-bot-module-alpha", version="1.0.0", state="installed")
UPDATE_SECOND = ModuleRecord(name="bravo", dist="akari-bot-module-bravo", version="1.0.0", state="installed")
UPDATE_PENDING = ModuleRecord(name="charlie", dist="akari-bot-module-charlie", version="0.9.0", state="available")


class _RecordingUpdate(StaticModuleSource):
    # 记录每次流式操作的种类与目标，用于断言更新确实走了 update 通道。
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.streamed: list[tuple[str, str]] = []

    async def stream_operation(self, kind, record, on_line):
        self.streamed.append((kind, record.dist))
        return await super().stream_operation(kind, record, on_line)


def _update_source() -> _RecordingUpdate:
    records = [UPDATE_INSTALLED, UPDATE_SECOND, UPDATE_PENDING]
    return _RecordingUpdate(records=records, available=records, stream_lines=["Updated 1 package"])


async def _test_update_covers_installed_selection():
    # 按 U 更新选中的已装项，走的是 update 而非重装。
    source = _update_source()

    async def body(app, page, pilot):
        await pilot.press("a")
        await pilot.pause()
        page.request_update()
        await page.wait_for_idle()
        await pilot.pause()
        return list(source.streamed), page.status_text

    streamed, status = await _with_app(source, body)
    return (
        streamed == [("update", "akari-bot-module-alpha"), ("update", "akari-bot-module-bravo")]
        and i18n.t("cli.tui.modules.batch_done", count=2, what=i18n.t("cli.tui.modules.action_update")) in status
    )


async def _test_update_only_targets_installed():
    # 未装项不进更新目标：更新只对已装包有意义。
    source = _update_source()

    async def body(app, page, pilot):
        await pilot.press("a")
        await pilot.pause()
        page.request_update()
        await page.wait_for_idle()
        await pilot.pause()
        return [dist for _, dist in source.streamed]

    streamed = await _with_app(source, body)
    return streamed == ["akari-bot-module-alpha", "akari-bot-module-bravo"]


async def _test_update_argv_passes_yes():
    # 真源按 ``module update <分发名> --yes`` 调用：界面里已经确认过，不该再被 CLI 追问。
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-update-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_update", FAKE_CLI_ECHO_ARGV)
        record = ModuleRecord(name="alpha", dist="akari-bot-module-alpha")
        lines: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            source = SubprocessModuleSource(root=root, timeout=30.0)
            result = await source.stream_operation("update", record, lines.append)
    return result.ok and lines == ["module update akari-bot-module-alpha --yes"]


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


LOADED_PKG = ModuleRecord(
    name="wiki",
    dist="akari-bot-module-wiki",
    version="1.0.0",
    state="installed",
    provides_modules=("wiki", "ab"),
)
PARTIAL_PKG = ModuleRecord(
    name="arcaea",
    dist="akari-bot-module-arcaea",
    version="1.0.0",
    state="installed",
    provides_modules=("arcaea", "arcaea-rss"),
)


def _select_package(page, dist: str) -> None:
    # 列表按「已装在前、其次按名」排序，选中项由页面自己维护，这里直接指定以固定用例目标。
    page._selected_key = dist
    page._selected = {dist}
    page._render_list()


PENDING_PKG = ModuleRecord(
    name="cytoid",
    dist="akari-bot-module-cytoid",
    version="0.3.0",
    state="available",
    provides_modules=("cytoid",),
)


def _load_source(states) -> StaticModuleSource:
    records = [LOADED_PKG, PARTIAL_PKG, PENDING_PKG]
    return StaticModuleSource(
        records=records,
        available=records,
        load_states=states,
        stream_lines=["已全局装载模块 wiki"],
    )


async def _test_load_cell_counts_loaded_modules():
    # 装载与安装是两回事：列表按包声明逐个数出已装载的模块。
    source = _load_source({"wiki": True, "ab": True, "arcaea": True, "arcaea-rss": False})

    async def body(app, page, pilot):
        rows = page.row_texts()
        await pilot.press("q")
        return rows

    rows = await _with_app(source, body)
    # 排序为「已装在前、其次按名」：arcaea 在 wiki 之前。
    return (
        i18n.t("cli.tui.modules.load_cell", loaded=1, total=2) in rows[0]
        and i18n.t("cli.tui.modules.load_cell", loaded=2, total=2) in rows[1]
    )


async def _test_toggle_load_loads_when_partly_unloaded():
    source = _load_source({"wiki": True, "ab": False, "arcaea": True, "arcaea-rss": True})

    async def body(app, page, pilot):
        _select_package(page, LOADED_PKG.dist)
        await pilot.pause()
        await pilot.press("l")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.loaded.get("load", [])), page.status_text

    loaded, status = await _with_app(source, body)
    return loaded == ["wiki", "ab"] and status


async def _test_toggle_load_unloads_when_all_loaded():
    source = _load_source({"wiki": True, "ab": True, "arcaea": True, "arcaea-rss": True})

    async def body(app, page, pilot):
        _select_package(page, LOADED_PKG.dist)
        await pilot.pause()
        await pilot.press("l")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.loaded.get("unload", []))

    unloaded = await _with_app(source, body)
    return unloaded == ["wiki", "ab"]


async def _test_toggle_load_ignores_uninstalled():
    source = _load_source({"wiki": True, "ab": True, "arcaea": True, "arcaea-rss": True})

    async def body(app, page, pilot):
        _select_package(page, PENDING_PKG.dist)
        await pilot.pause()
        page.request_toggle_load()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return dict(source.loaded), page.status_text

    loaded, status = await _with_app(source, body)
    return loaded == {} and status


async def _test_columns_header_aligns_with_rows():
    # 表头与行用同一套列宽：版本列与装载列在两者中的起始列必须一致。
    source = _load_source({"wiki": True, "ab": True, "arcaea": True, "arcaea-rss": False})

    async def body(app, page, pilot):
        header = page.column_text()
        rows = page.row_texts()
        await pilot.press("q")
        return header, rows

    header, rows = await _with_app(source, body)
    for key in ("column_name", "column_version", "column_load"):
        if i18n.t(f"cli.tui.modules.{key}") not in header:
            return False
    version_col = compat.display_width(header[: header.index(i18n.t("cli.tui.modules.column_version"))])
    load_col = compat.display_width(header[: header.index(i18n.t("cli.tui.modules.column_load"))])
    version_ok = all(
        compat.display_width(row[: row.index(version)]) == version_col
        for row, version in zip(rows, ("1.0.0", "1.0.0", "0.3.0"), strict=False)
    )
    load_positions = [compat.display_width(row[: row.index("装载")]) for row in rows if "装载" in row]
    return version_ok and len(load_positions) == 2 and all(position == load_col for position in load_positions)


async def _test_toggle_row_is_centered():
    # 「只看已安装」独立成一行并水平居中；放在搜索行里会被输入框挤到边缘。
    source = _load_source({"wiki": True, "ab": True})

    async def body(app, page, pilot):
        row = page.query_one("#toggle-row")
        toggle = page.query_one("#installed-only")
        await pilot.press("q")
        return row.region, toggle.region

    row, toggle = await _with_app(source, body)
    row_center = row.x + row.width / 2
    toggle_center = toggle.x + toggle.width / 2
    return abs(row_center - toggle_center) <= 1.0


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
    await tester.test(_test_update_covers_installed_selection, "按 U 更新选中的已装项")
    await tester.test(_test_update_only_targets_installed, "更新只作用于已装项")
    await tester.test(_test_update_argv_passes_yes, "更新带 --yes 调用 CLI")
    await tester.test(_test_subprocess_source_streams_and_reports, "真源逐行回调并给出结论")
    await tester.test(_test_subprocess_source_timeout, "真源超时按数据源错误上报")
    await tester.test(_test_relative_root_is_resolved, "相对实例根解析为绝对路径")
    await tester.test(_test_detail_shows_manifest_metadata, "详情展示 manifest 元数据")
    await tester.test(_test_detail_falls_back_when_manifest_missing, "manifest 缺失才显示未声明")
    await tester.test(_test_load_cell_counts_loaded_modules, "列表按模块数展示装载状态")
    await tester.test(_test_toggle_load_loads_when_partly_unloaded, "有未装载模块时按 l 装载整包")
    await tester.test(_test_toggle_load_unloads_when_all_loaded, "全部已装载时按 l 卸载整包")
    await tester.test(_test_toggle_load_ignores_uninstalled, "未装项不参与装载")
    await tester.test(_test_columns_header_aligns_with_rows, "列表表头与行对齐")
    await tester.test(_test_toggle_row_is_centered, "只看已安装水平居中")
    return tester
