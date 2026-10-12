"""模块页的可安装列表、模块操作、确认流程及进度显示测试。"""

import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.modules import (
    ModuleRecord,
    ModuleSourceError,
    ModulesPage,
    OperationResult,
    StaticModuleSource,
    _git_install_args,
    _split_git_address,
)
from akaribot.testing import Tester, func_case

INSTALLED = ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed")
CANDIDATE = ModuleRecord(name="wiki", dist="akari-bot-module-wiki", version="0.2.0", summary="维基", state="available")
ADAPTER = ModuleRecord(
    name="telegram", dist="akari-bot-adapter-telegram", version="0.1.0", summary="", state="available"
)

FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "modules.json"


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
    app = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())
    return app


async def _with_app(source: StaticModuleSource, body, *, size: tuple[int, int] = (100, 30)) -> object:
    app = await _boot(source)
    async with compat.app_test(app, size=size) as pilot:
        page = app.modules_page()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


def _filter_installed(app: TuiApp) -> None:

    checkbox = app.modules_page().query_one("#installed-only", compat.Checkbox)
    checkbox.value = True


async def _test_lists_everything_by_default():
    # 默认同时显示已安装与未安装模块。
    async def body(app, page, pilot):
        rows = tuple(record.dist for record in page.visible_records)
        await pilot.press("q")
        return rows, app.module_source.calls["available"]

    rows, available_calls = await _with_app(_source(), body)
    return (
        rows == ("akari-bot-module-dice", "akari-bot-adapter-telegram", "akari-bot-module-wiki")
        and available_calls == 1
    )


async def _test_refresh_keeps_row_highlighted():
    # 关键回归：重建模块列表后选中行必须仍然亮着——ListView 只在 index 变化时打高亮。
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 1
        await pilot.pause()
        target = list_view.index
        before = [bool(item.highlighted) for item in list_view.children]
        page.refresh_records()
        await page.wait_for_idle()
        await pilot.pause()
        after = (list_view.index, [bool(item.highlighted) for item in list_view.children])
        await pilot.press("q")
        return target, before, after

    target, before, after = await _with_app(_source(), body)

    def only(flags, index):
        return index is not None and flags[index] is True and sum(flags) == 1

    return only(before, target) and after[0] == target and only(after[1], target)


async def _test_toggle_filters_to_installed():
    # 勾选后仅显示已安装模块，取消勾选后显示全部模块。
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
        list_view.index = 2  # 排序为已安装的 dice、适配器 telegram、模块 wiki。
        await pilot.pause()
        selected = page.selected_record
        install_button = page.query_one("#install", compat.Button)
        return (
            selected is not None and selected.dist == "akari-bot-module-wiki",
            install_button.disabled,
        )

    selected_is_wiki, disabled = await _with_app(_source(), body)
    return selected_is_wiki and disabled is False


def _choice_labels(app: TuiApp) -> list[str]:
    return [str(button.label) for button in app.screen.query("#choice-actions Button")]


async def _pick_choice(app: TuiApp, pilot, index: int) -> None:
    assert await pilot.click(f"#choice-{index}")
    await pilot.pause()


async def _test_install_streams_output_to_status():
    # 高亮已安装项时，安装操作通过输入框指定目标并选择来源。
    async def body(app, page, pilot):
        page.request_install()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "akari-bot-module-wiki"
        await pilot.press("enter")
        await pilot.pause()
        labels = _choice_labels(app)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        return labels, page.stream_lines, page.status_text, app.module_source.installed

    labels, lines, status, installed = await _with_app(_source(), body)
    ok = (
        i18n.t("cli.tui.modules.install_from_registry") in labels
        and lines == ("Resolved 2 packages", "Installed 2 packages")
        and status.startswith(i18n.t("cli.tui.modules.stub_install_ok"))
        and installed == ["akari-bot-module-wiki"]
    )
    return ok


async def _test_install_highlighted_record_without_dialog():
    # 未安装的高亮项直接作为安装目标。
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 2
        await pilot.pause()
        page.request_install()
        await page.wait_for_idle()
        await pilot.pause()
        dialog = app.screen is not page.screen
        await pilot.press("q")
        return dialog, app.module_source.installed

    dialog, installed = await _with_app(_source(), body)
    return dialog is False and installed == ["akari-bot-module-wiki"]


async def _test_install_search_term_prefills_dialog():
    # 搜索词预填到安装输入框，避免重复输入。
    async def body(app, page, pilot):
        page.set_query("akari-bot-module-unknown")
        await pilot.pause()
        page.request_install()
        await pilot.pause()
        prefill = app.screen.query_one("#prompt-input", compat.Input).value
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return prefill

    prefill = await _with_app(_source(), body)
    return prefill == "akari-bot-module-unknown"


async def _test_install_cancelled_by_empty_spec():
    async def body(app, page, pilot):
        page.request_install()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        status = page.status_text
        installed = list(app.module_source.installed)
        await pilot.press("q")
        return status, installed

    status, installed = await _with_app(_source(), body)
    return installed == [] and status == i18n.t("cli.tui.modules.install_cancelled")


async def _test_install_git_spec_offers_git_source():
    # 仓库地址使用 Git 安装，ref 与 subdirectory 分别传入对应 CLI 选项。
    spec = "git+https://github.com/akari-bot/modules@v1.2#subdirectory=packages/wiki"

    async def body(app, page, pilot):
        page.on_install_spec_entered(spec)
        await pilot.pause()
        labels = _choice_labels(app)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, list(app.module_source.stream_calls)

    labels, calls = await _with_app(_source(), body)
    return labels[:-1] == [i18n.t("cli.tui.modules.install_from_git")] and calls == [
        (
            "install",
            spec,
            ("--git", "git+https://github.com/akari-bot/modules", "--ref", "v1.2", "--subdir", "packages/wiki"),
            False,
        )
    ]


async def _test_install_editable_directory_offers_editable_source():
    with TemporaryDirectory(prefix="akari-editable-") as raw:
        directory = str(Path(raw).resolve())

        async def body(app, page, pilot):
            page.on_install_spec_entered(directory)
            await pilot.pause()
            labels = _choice_labels(app)
            await _pick_choice(app, pilot, 0)
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return labels, list(app.module_source.stream_calls)

        labels, calls = await _with_app(_source(), body)
    return labels[:-1] == [i18n.t("cli.tui.modules.install_editable")] and calls == [
        ("install", directory, ("-e", directory), False)
    ]


async def _test_install_unknown_spec_is_rejected():
    async def body(app, page, pilot):
        page.on_install_spec_entered("不存在的目标！")
        await pilot.pause()
        status = page.status_text
        installed = list(app.module_source.installed)
        await pilot.press("q")
        return status, installed

    status, installed = await _with_app(_source(), body)
    return installed == [] and status == i18n.t("cli.tui.modules.install_unknown_spec", spec="不存在的目标！")


def _test_git_address_split():
    # 地址末段的 @ 分隔 ref；``git@host`` 中的 @ 属于 userinfo。
    return (
        _split_git_address("git+https://github.com/oasis/akari@v2") == ("git+https://github.com/oasis/akari", "v2", "")
        and _split_git_address("git@github.com:oasis/akari.git") == ("git@github.com:oasis/akari.git", "", "")
        and _git_install_args("ssh://git@host/oasis/akari.git#subdirectory=mod")
        == ("--git", "ssh://git@host/oasis/akari.git", "--subdir", "mod")
    )


async def _uninstall_confirmed(app: TuiApp, page, pilot, choice: int = 0) -> str:
    # 卸载需先选择处置方式；交互用例关闭防抖延迟。
    page.request_uninstall()
    await pilot.pause()
    title = str(app.screen.query_one("#choice-title", compat.Static).render())
    await _pick_choice(app, pilot, choice)
    await page.wait_for_idle()
    await pilot.pause()
    return title


async def _test_single_uninstall_opens_options():
    # 单个与批量卸载共用确认流程，标题明确列出目标。
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        title = str(app.screen.query_one("#choice-title", compat.Static).render())
        first = list(app.module_source.uninstalled)
        labels = _choice_labels(app)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return title, first, labels

    title, first, labels = await _with_app(_source(), body)
    return (
        title == i18n.t("cli.tui.modules.uninstall_confirm_one", name="akari-bot-module-dice")
        and first == []
        and labels[:-1]
        == [
            i18n.t("cli.tui.modules.uninstall_keep_data"),
            i18n.t("cli.tui.modules.uninstall_purge_data"),
        ]
    )


async def _test_uninstall_streams_output_to_status():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        title = await _uninstall_confirmed(app, page, pilot)
        return title, page.stream_lines, app.module_source.uninstalled

    title, lines, uninstalled = await _with_app(_source(), body)
    return (
        title == i18n.t("cli.tui.modules.uninstall_confirm_one", name="akari-bot-module-dice")
        and lines == ("Resolved 2 packages", "Installed 2 packages")
        and uninstalled == ["akari-bot-module-dice"]
    )


async def _test_failed_install_reports_detail():
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        await _uninstall_confirmed(app, page, pilot)
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
        async def stream_operation(self, kind, record, on_line, **kwargs):
            raise RuntimeError("子进程炸了")

    async def body(app, page, pilot):
        await _uninstall_confirmed(app, page, pilot)
        return page.status_text

    source = _Exploding(records=[INSTALLED])
    status = await _with_app(source, body)
    return "RuntimeError" in status and "子进程炸了" in status


# AKARIBOT_CLI_BIN 必须为可执行文件路径，因此替身脚本包含 shebang。
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
    # 记录操作类型与目标，验证更新调用 update。
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.streamed: list[tuple[str, str]] = []

    async def stream_operation(self, kind, record, on_line, **kwargs):
        self.streamed.append((kind, record.dist))
        return await super().stream_operation(kind, record, on_line, **kwargs)


def _update_source() -> _RecordingUpdate:
    records = [UPDATE_INSTALLED, UPDATE_SECOND, UPDATE_PENDING]
    return _RecordingUpdate(records=records, available=records, stream_lines=["Updated 1 package"])


async def _test_update_covers_installed_selection():
    # 更新选中项时逐个调用 update，目标仅包含已安装包。
    source = _update_source()

    async def body(app, page, pilot):
        await pilot.press("a")
        await pilot.pause()
        await pilot.press("U")
        await pilot.pause()
        labels = _choice_labels(app)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        return labels, list(source.streamed), page.status_text

    labels, streamed, status = await _with_app(source, body)
    return (
        labels[:-1]
        == [
            i18n.t("cli.tui.modules.update_selected"),
            i18n.t("cli.tui.modules.update_all"),
        ]
        and streamed == [("update", "akari-bot-module-alpha"), ("update", "akari-bot-module-bravo")]
        and i18n.t("cli.tui.modules.batch_done", count=2, what=i18n.t("cli.tui.modules.action_update")) in status
    )


async def _test_update_only_targets_installed():
    # 更新目标仅包含已安装包。
    source = _update_source()

    async def body(app, page, pilot):
        await pilot.press("a")
        await pilot.pause()
        page.request_update()
        await pilot.pause()
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        return [dist for _, dist in source.streamed]

    streamed = await _with_app(source, body)
    return streamed == ["akari-bot-module-alpha", "akari-bot-module-bravo"]


async def _test_update_entry_points_open_choice():
    # U、ctrl+u 与按钮共用范围选择流程。
    async def body(app, page, pilot):
        seen: list[list[str]] = []
        for trigger in ("U", "ctrl+u"):
            await pilot.press(trigger)
            await pilot.pause()
            seen.append(_choice_labels(app))
            await pilot.press("escape")
            await pilot.pause()
        page.query_one("#update", compat.Button).press()
        await pilot.pause()
        seen.append(_choice_labels(app))
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return seen

    seen = await _with_app(_update_source(), body)
    expected = [
        i18n.t("cli.tui.modules.update_selected"),
        i18n.t("cli.tui.modules.update_all"),
        i18n.t("cli.tui.modules.cancel"),
    ]
    return seen == [expected, expected, expected]


async def _test_update_all_dispatches_all_flag():
    # 全部更新通过 --all 枚举已安装包，不传递位置参数。
    source = _update_source()

    async def body(app, page, pilot):
        page.request_update()
        await pilot.pause()
        await _pick_choice(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.stream_calls)

    calls = await _with_app(source, body)
    return calls == [("update", i18n.t("cli.tui.modules.update_all_target"), ("--all",), False)]


async def _test_update_hint_warns_and_cancel_changes_nothing():
    # 提示明确全部更新的范围，取消后不执行操作。
    async def body(app, page, pilot):
        page.request_update()
        await pilot.pause()
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await pilot.press("escape")
        await pilot.pause()
        status = page.status_text
        calls = list(app.module_source.stream_calls)
        await pilot.press("q")
        return hint, status, calls

    hint, status, calls = await _with_app(_update_source(), body)
    return (
        hint == i18n.t("cli.tui.modules.update_hint")
        and status == i18n.t("cli.tui.modules.update_cancelled")
        and calls == []
    )


async def _test_update_without_target_offers_all_only():
    # 选区没有已安装包时，仅提供全部更新并说明原因。
    source = _RecordingUpdate(records=[UPDATE_PENDING], available=[UPDATE_PENDING], stream_lines=["Updated 1 package"])

    async def body(app, page, pilot):
        page.request_update()
        await pilot.pause()
        labels = _choice_labels(app)
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, hint, list(source.stream_calls)

    labels, hint, calls = await _with_app(source, body)
    expected_hint = (
        f"{i18n.t('cli.tui.modules.update_hint')}{i18n.t('cli.common.clause_separator')}"
        f"{i18n.t('cli.tui.modules.update_no_target')}"
    )
    return (
        labels[:-1] == [i18n.t("cli.tui.modules.update_all")]
        and hint == expected_hint
        and calls == [("update", i18n.t("cli.tui.modules.update_all_target"), ("--all",), False)]
    )


async def _test_update_all_argv_passes_all_and_yes():
    # 界面确认后通过 ``module update --all --yes`` 执行，避免重复交互。
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-update-all-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_update_all", FAKE_CLI_ECHO_ARGV)
        record = ModuleRecord(name="alpha", dist="akari-bot-module-alpha")
        lines: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            source = SubprocessModuleSource(root=root, timeout=30.0)
            result = await source.stream_operation(
                "update", record, lines.append, extra_args=("--all",), positional=False
            )
    return result.ok and lines == ["module update --all --yes"]


async def _test_update_argv_passes_yes():
    # 界面确认后通过 ``module update <分发名> --yes`` 执行，避免重复交互。
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
    # CLI 替身覆盖进程启动、输出读取与退出等待，避免实际安装包。
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
    # 实例根同时作为 cwd 和 AKARI_INSTANCE_DIR，必须使用绝对路径以避免重复拼接。
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
    # 模块记录必须保留 manifest 元数据，以准确显示核心 API 与模块声明。

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
    app = TuiApp(source=StaticModuleSource([record]), initial_page="modules", boot_started_at=time.monotonic())
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
    # 直接指定选中项，以独立于页面的默认选择策略验证目标记录。
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
    # 装载状态按包声明的模块统计，与包的安装状态独立。
    source = _load_source({"wiki": True, "ab": True, "arcaea": True, "arcaea-rss": False})

    async def body(app, page, pilot):
        rows = page.row_texts()
        await pilot.press("q")
        return rows

    rows = await _with_app(source, body)
    # 已安装包优先，其次按名称排序；arcaea 先于 wiki。
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
    # 表头与数据行的版本列、装载列必须对齐。
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


async def _test_action_buttons_fit_narrow_screen():
    for size in ((80, 24), (60, 20)):
        app = TuiApp(source=_update_source(), initial_page="modules", boot_started_at=time.monotonic())
        async with compat.app_test(app, size=size) as pilot:
            page = app.modules_page()
            await page.wait_for_idle()
            await pilot.pause()
            actions = page.query_one("#actions").region
            buttons = [
                page.query_one(f"#{name}", compat.Button)
                for name in ("install", "uninstall", "update", "toggle-load", "refresh")
            ]
            if not all(
                button.region.width >= compat.button_width(button)
                and actions.contains_region(button.region)
                and page.content_region.contains_region(button.region)
                for button in buttons
            ):
                return False
    return True


async def _test_search_remains_visible_with_full_catalog():
    records = [
        ModuleRecord(name=f"module-{index:02}", dist=f"akari-bot-module-{index:02}", state="installed")
        for index in range(43)
    ]
    for size in ((80, 24), (60, 20)):
        source = StaticModuleSource(records=records, available=records)
        app = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())
        async with compat.app_test(app, size=size) as pilot:
            page = app.modules_page()
            await page.wait_for_idle()
            page.action_select_all()
            await pilot.pause()
            row = page.query_one("#search-row").region
            search = page.query_one("#search", compat.Input)
            toggle = page.query_one("#installed-only", compat.Checkbox)
            count = page.query_one("#count").region
            layout_ok = (
                search.content_size.width >= 10
                and row.contains_region(search.region)
                and row.contains_region(toggle.region)
                and search.region.right <= toggle.region.x
                and count.y == row.bottom
                and page.query_one("#module-list").content_size.height >= 3
            )
            await pilot.press("slash", "0", "1")
            await pilot.pause()
            if not (
                layout_ok
                and search.content_size.width >= 10
                and search.has_focus
                and page.search_query == "01"
                and [record.name for record in page.visible_records] == ["module-01"]
            ):
                return False
    return True


async def _test_purge_requires_typed_confirmation():
    record = ModuleRecord(
        name="dice",
        dist=INSTALLED.dist,
        state="installed",
        config_table="module_dice",
        owned_tables=("dice_history",),
    )
    source = StaticModuleSource(records=[record], available=[record])

    async def body(app, page, pilot):
        for value in ("", "dice", record.dist):
            page.request_uninstall()
            await pilot.pause()
            await _pick_choice(app, pilot, 1)
            prompt = app.screen
            if not (
                isinstance(prompt, compat.TextPromptScreen)
                and record.dist in prompt.prompt_hint
                and "config/module_dice.toml" in prompt.prompt_hint
                and "dice_history" in prompt.prompt_hint
                and prompt.query_one("#prompt-input", compat.Input).value == ""
                and source.stream_calls == []
            ):
                return False
            prompt.query_one("#prompt-input", compat.Input).value = value
            await pilot.press("enter" if value else "escape")
            await page.wait_for_idle()
            await pilot.pause()
            if value != record.dist and source.stream_calls:
                return False
        return source.stream_calls == [("uninstall", record.dist, ("--purge-data",), True)]

    return await _with_app(source, body, size=(80, 24))


async def _test_uninstall_argv_passes_data_options():
    # CLI 参数包含选定的卸载方式和 --yes，避免重复交互。
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-remove-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_remove", FAKE_CLI_ECHO_ARGV)
        record = ModuleRecord(name="dice", dist="akari-bot-module-dice")
        lines: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            source = SubprocessModuleSource(root=root, timeout=30.0)
            result = await source.stream_operation("uninstall", record, lines.append, extra_args=("--purge-data",))
    return result.ok and lines == ["module remove akari-bot-module-dice --purge-data --yes"]


async def _test_install_argv_for_git_and_editable():
    from akaribot.cli.tui.modules import SubprocessModuleSource

    with TemporaryDirectory(prefix="akari-add-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_add", FAKE_CLI_ECHO_ARGV)
        record = ModuleRecord(name="wiki", dist="wiki")
        lines: list[str] = []
        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            source = SubprocessModuleSource(root=root, timeout=30.0)
            await source.stream_operation(
                "install",
                record,
                lines.append,
                extra_args=("--git", "git+https://github.com/oasis/akari", "--ref", "v2"),
                positional=False,
            )
            await source.stream_operation(
                "install", record, lines.append, extra_args=("-e", str(root)), positional=False
            )
    return lines == [
        "module add --git git+https://github.com/oasis/akari --ref v2",
        f"module add -e {root}",
    ]


def _test_low_frequency_bindings_stay_out_of_footer():
    # 80 列下页脚只留高频键位；其余键位仍可用，只是不占页脚。
    shown = {binding.key for binding in ModulesPage.BINDINGS if binding.show}
    hidden = {binding.key for binding in ModulesPage.BINDINGS if not binding.show}
    return shown == {"r", "slash", "i", "space"} and hidden == {
        "a",
        "u",
        "U",
        "ctrl+u",
        "l",
        "ctrl+space",
        "shift+up",
        "shift+down",
        "ctrl+a",
        "c",
        "escape",
    }


def _test_pending_confirm_gate():
    # 防抖窗口内忽略同一目标的重复请求，其他目标和超时请求正常处理。
    gate = compat.PendingConfirm()
    first = gate.accept("x", now=100.0)
    burst = gate.accept("x", now=100.1)
    again = gate.accept("x", now=101.0)
    other = gate.accept("y", now=200.0)
    return first is True and burst is False and again is True and other is True


async def _test_pending_invalidated_by_refresh_and_selection():
    # 刷新、高亮切换及清空选区后应清除防抖状态。
    async def body(app, page, pilot):
        list_view = page.query_one("#module-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        with mock.patch.object(compat.PendingConfirm, "debounce", 30.0), mock.patch.object(compat, "ask_choice") as ask:
            page.request_update()
            await pilot.pause()
            page.request_update()
            await pilot.pause()
            swallowed = ask.call_count
            page.action_clear_selection()
            await pilot.pause()
            page.request_update()
            await pilot.pause()
            cleared = ask.call_count
            list_view.index = 1
            await pilot.pause()
            page.request_update()
            await pilot.pause()
            highlighted = ask.call_count
            page.refresh_records(force=True)
            await page.wait_for_idle()
            await pilot.pause()
            page.request_update()
            await pilot.pause()
            refreshed = ask.call_count
        await pilot.press("q")
        return swallowed, cleared, highlighted, refreshed, list(app.module_source.uninstalled)

    swallowed, cleared, highlighted, refreshed, uninstalled = await _with_app(_source(), body)
    return swallowed == 1 and cleared == 2 and highlighted == 3 and refreshed == 4 and uninstalled == []


async def _test_reset_pending_hook_clears_gate():
    async def body(app, page, pilot):
        with mock.patch.object(compat.PendingConfirm, "debounce", 30.0), mock.patch.object(compat, "ask_choice") as ask:
            page.request_update()
            await pilot.pause()
            page.request_update()
            await pilot.pause()
            first = ask.call_count
            page.reset_pending()
            page.request_update()
            await pilot.pause()
            after = ask.call_count
        await pilot.press("q")
        return first, after

    first, after = await _with_app(_source(), body)
    return first == 1 and after == 2


@func_case
async def test_tui_modules_available(tester: Tester):
    """cli.tui.modules: 可安装列表与安装进度测试"""
    _use_cli_locale()
    # 防抖专项用例使用实际窗口，与关闭延迟的交互用例分开运行。
    await tester.test(_test_pending_confirm_gate, "确认闸门忽略连发并在窗口外放行")
    # 关闭防抖延迟，使交互用例无需等待；防抖行为由专项用例验证。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_lists_everything_by_default, "默认列出已装与未装")
        await tester.test(_test_refresh_keeps_row_highlighted, "刷新后选中行仍然高亮")
        await tester.test(_test_toggle_filters_to_installed, "开关在全部与只看已装之间切换")
        await tester.test(_test_uninstalled_record_is_installable, "未装项可安装")
        await tester.test(_test_install_streams_output_to_status, "安装先问名字再选来源并逐行回显")
        await tester.test(_test_install_highlighted_record_without_dialog, "光标停在未装项上直接安装")
        await tester.test(_test_install_search_term_prefills_dialog, "搜索词预填安装输入框")
        await tester.test(_test_install_cancelled_by_empty_spec, "安装输入框取消后不动列表")
        await tester.test(_test_install_git_spec_offers_git_source, "仓库地址只给 git 来源")
        await tester.test(_test_install_editable_directory_offers_editable_source, "本地目录给可编辑安装")
        await tester.test(_test_install_unknown_spec_is_rejected, "无法识别的安装目标直接拒绝")
        await tester.test(_test_git_address_split, "仓库地址拆出 ref 与 subdirectory")
        await tester.test(_test_single_uninstall_opens_options, "单个卸载一次按键即弹处置方式")
        await tester.test(_test_uninstall_streams_output_to_status, "卸载确认后输出逐行显示到状态栏")
        await tester.test(_test_failed_install_reports_detail, "失败时展示输出尾部")
        await tester.test(_test_available_failure_keeps_installed_list, "可安装集合失败不清空列表")
        await tester.test(_test_stream_operation_failure_becomes_result, "数据源异常转成结果展示")
        await tester.test(_test_update_entry_points_open_choice, "U、ctrl+u 与按钮都弹出更新范围选择")
        await tester.test(_test_update_covers_installed_selection, "选「更新选中项」逐个更新已装项")
        await tester.test(_test_update_only_targets_installed, "更新只作用于已装项")
        await tester.test(_test_update_all_dispatches_all_flag, "选「更新全部」下发 --all")
        await tester.test(_test_update_without_target_offers_all_only, "没有可更新目标时只给全量更新")
        await tester.test(_test_update_hint_warns_and_cancel_changes_nothing, "提示写明全量更新耗时且取消无副作用")
        await tester.test(_test_update_argv_passes_yes, "更新带 --yes 调用 CLI")
        await tester.test(_test_update_all_argv_passes_all_and_yes, "全量更新按 update --all --yes 调用 CLI")
        await tester.test(_test_uninstall_argv_passes_data_options, "卸载把 --purge-data 拼进 argv")
        await tester.test(_test_install_argv_for_git_and_editable, "git 与可编辑安装拼出对应 argv")
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
        await tester.test(_test_action_buttons_fit_narrow_screen, "80 列下五个动作按钮都在页内")
        await tester.test(_test_search_remains_visible_with_full_catalog, "完整模块列表在窄屏下可输入搜索")
        await tester.test(_test_purge_requires_typed_confirmation, "清理配置与数据需输入分发名确认")
        await tester.test(_test_low_frequency_bindings_stay_out_of_footer, "低频键位不进页脚")
        await tester.test(_test_pending_invalidated_by_refresh_and_selection, "刷新、换选中项与清选区作废防抖记录")
        await tester.test(_test_reset_pending_hook_clears_gate, "切页钩子清掉防抖记录")
    return tester
