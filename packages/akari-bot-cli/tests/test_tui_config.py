"""配置页的未保存更改保护、异步渲染与外部编辑器测试。"""

import asyncio
import os
import shlex
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.config import (
    KIND_BOOL,
    KIND_INT,
    KIND_LIST,
    MODE_FORM,
    MODE_RAW,
    ConfigField,
    ConfigPage,
    StaticConfigSource,
    SubprocessConfigSource,
    editor_argv,
    editor_setting,
)
from akaribot.testing import Tester, func_case

FIELDS = {
    "config": (
        ConfigField(key="count", table="config", kind=KIND_INT, value=3),
        ConfigField(key="enable", table="config", kind=KIND_BOOL, value=True),
    ),
    "module_wiki": (
        ConfigField(key="prefixes", table="module_wiki", kind=KIND_LIST, value=["wiki", "维基"]),
        ConfigField(key="enable", table="module_wiki", kind=KIND_BOOL, value=False),
    ),
    "empty_table": (),
}
RAW = {
    "config": "[config]\ncount = 3\nenable = true\n",
    "module_wiki": '[module_wiki]\nprefixes = ["wiki", "维基"]\nenable = false\n',
    "empty_table": "",
}

FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "config_run.json"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticConfigSource:
    params = {"tables": ("config", "module_wiki", "empty_table"), "fields": FIELDS, "raw": RAW}
    params.update(kwargs)
    return StaticConfigSource(**params)


def _config_file(root: Path, table: str, text: str = "") -> Path:
    target = root / "config" / f"{table}.toml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


@contextmanager
def _editor_env(env: dict[str, str], *, found: str | None = "/usr/bin/editor"):
    # 注入编辑器变量与 PATH，避免测试依赖本机安装状态。
    with mock.patch.dict(os.environ, env):
        with mock.patch("akaribot.cli.tui.config.shutil.which", return_value=found):
            yield


def _recording_suspend(events: list[str]):
    @contextmanager
    def suspend():
        events.append("suspend-enter")
        yield
        events.append("suspend-exit")

    return suspend


async def _wait_until(predicate, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


def _screen_title(app: TuiApp) -> str:

    return str(getattr(app.screen, "choice_title", ""))


async def _with_page(body, source=None, size=(110, 32)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"config": chosen}, initial_page="config", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("config")
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _test_worker_marks_stop_after_unmount():
    # 页面卸载后 worker 仍可能完成，异步渲染入口须在访问控件前检查挂载状态。
    async def body(app, page, pilot, source):
        content = app.query_one("#content", compat.Vertical)
        await content.remove_children()
        await pilot.pause()
        outcomes = []
        for call in (
            page.reload_tables,
            lambda: page.select_table("config"),
            lambda: page._rebuild_form(()),
            lambda: page._show_form_hint("卸载后的提示"),
        ):
            try:
                outcomes.append(await call())
            except Exception as error:  # noqa: BLE001 - 验证异常是否向外传播
                outcomes.append(f"{type(error).__name__}: {error}")
        return outcomes

    outcomes = await _with_page(body)
    return all(outcome in (False, None) for outcome in outcomes)


async def _test_refresh_keeps_table_highlighted():
    # 关键回归：重建表清单后选中行必须仍然亮着——ListView 只在 index 变化时打高亮。
    async def body(app, page, pilot, source):
        table_list = page.query_one("#table-list", compat.ListView)
        table_list.index = 1
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        target = table_list.index
        before = [bool(item.highlighted) for item in table_list.children]
        page.refresh_tables()
        await page.wait_for_idle()
        await pilot.pause()
        after = (table_list.index, [bool(item.highlighted) for item in table_list.children])
        selected = page.selected_table
        await pilot.press("q")
        return target, before, after, selected

    target, before, after, selected = await _with_page(body)

    def only(flags, index):
        return index is not None and flags[index] is True and sum(flags) == 1

    return selected == "module_wiki" and only(before, target) and after[0] == target and only(after[1], target)


async def _test_dirty_note_tracks_edits():

    async def body(app, page, pilot, source):
        clean = (page.is_dirty(), page.dirty_note())
        page.row_for("count").set_text("9")
        await pilot.pause()
        dirty = (page.is_dirty(), page.dirty_note())
        expected = i18n.t("cli.tui.config.dirty_note", table="config")
        await pilot.press("q")
        return clean, dirty, expected

    clean, dirty, expected = await _with_page(body)
    return clean == (False, "") and dirty[0] is True and dirty[1] == expected


async def _test_table_switch_keeps_edits():

    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        table_list = page.query_one("#table-list", compat.ListView)
        table_list.index = 1
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        title = _screen_title(app)
        await pilot.press("escape")
        await pilot.pause()
        kept = (
            page.selected_table,
            page.row_for("count").text,
            page.is_dirty(),
            compat.highlighted_index(table_list),
        )
        await pilot.press("q")
        return opened, title, kept

    opened, title, kept = await _with_page(body)
    return opened and title == i18n.t("cli.tui.config.dirty_title") and kept == ("config", "9", True, 0)


async def _test_table_switch_discards_edits():

    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        table_list = page.query_one("#table-list", compat.ListView)
        table_list.index = 1
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        table = page.selected_table
        fields = sorted(row.field.key for row in page.field_rows())
        dirty = page.is_dirty()
        await pilot.press("q")
        return table, fields, dirty

    table, fields, dirty = await _with_page(body)
    return table == "module_wiki" and fields == ["enable", "prefixes"] and dirty is False


async def _test_reload_asks_before_rereading():
    # 取消重新加载时须保留编辑内容，且不得调用数据源。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        before = dict(source.calls)
        page.action_reload()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        kept = (dict(source.calls) == before, page.is_dirty())
        page.action_reload()
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        text = page.row_for("count").text
        await pilot.press("q")
        return opened, kept, dict(source.calls), text

    opened, kept, calls, text = await _with_page(body)
    return opened and kept == (True, True) and calls["list"] > 0 and calls["schema"] > 0 and text == "3"


async def _test_forced_refresh_asks():
    # 强制刷新也会重建编辑区，必须保留未保存更改检查。
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        before = dict(source.calls)
        page.refresh_tables(force=True)
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        untouched = dict(source.calls) == before
        text = page.row_for("count").text
        await pilot.press("q")
        return opened, untouched, text

    opened, untouched, text = await _with_page(body)
    return opened and untouched and text == "9"


async def _test_mode_switch_asks_before_switching():
    async def body(app, page, pilot, source):
        page.row_for("count").set_text("9")
        await pilot.pause()
        page.action_mode_raw()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        kept = (page.mode, page.is_dirty())
        page.action_mode_raw()
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        switched = (page.mode, page.row_for("count").text)
        await pilot.press("q")
        return opened, kept, switched

    opened, kept, switched = await _with_page(body)
    return opened and kept == (MODE_FORM, True) and switched == (MODE_RAW, "3")


async def _test_raw_edits_count_as_dirty():

    async def body(app, page, pilot, source):
        await page.set_mode(MODE_RAW)
        await pilot.pause()
        loaded = page.is_dirty()
        await page.raw_editor().load_text(RAW["config"] + "count = 9\n")
        await pilot.pause()
        dirty = page.is_dirty()
        note = page.dirty_note()
        await pilot.press("q")
        return loaded, dirty, note

    loaded, dirty, note = await _with_page(body)
    return loaded is False and dirty is True and note == i18n.t("cli.tui.config.dirty_note", table="config")


async def _test_form_hint_reads_widget_text():

    async def body(app, page, pilot, source):
        page.query_one("#table-list", compat.ListView).index = 2
        await page.wait_for_idle()
        await pilot.pause()
        hint = page.form_hint()
        await pilot.press("q")
        return hint

    hint = await _with_page(body)
    return hint == i18n.t("cli.tui.config.hint_table_empty")


async def _test_low_frequency_bindings_stay_out_of_footer():
    # 工具栏操作从页脚隐藏，为 80 列终端保留全局快捷键空间。
    async def body(app, page, pilot, source):
        footer = app.query_one(compat.Footer)
        actions = {"save", "mode_form", "mode_raw", "open_editor", "reload", "focus_tables"}
        keys = [child for child in footer.children if getattr(child, "action", "") in actions]
        width = sum(compat.widget_cells(child)[0] for child in keys)
        buttons = sorted(child.id for child in page.query(compat.Button) if child.id)
        await pilot.press("q")
        return len(keys), width, buttons

    count, width, buttons = await _with_page(body, size=(80, 24))
    visible = tuple(binding.key for binding in ConfigPage.BINDINGS if binding.show)
    hidden = tuple(binding.key for binding in ConfigPage.BINDINGS if not binding.show)
    return (
        count == 1
        and width <= 80
        and "open-editor" in buttons
        and visible == ("s",)
        and hidden == ("o", "f", "t", "ctrl+r", "escape")
    )


def _test_editor_command_resolution():
    # 编辑器解析须与 config open 一致：VISUAL 优先于 EDITOR，命令按 shell 规则拆分。
    default = "notepad" if sys.platform.startswith("win") else ("open" if sys.platform == "darwin" else "xdg-open")
    with mock.patch("akaribot.cli.tui.config.shutil.which", return_value="/usr/bin/editor"):
        visual = editor_argv({"VISUAL": "code -w", "EDITOR": "vi"})
        fallback = editor_argv({"EDITOR": "nano"})
        quoted = editor_argv({"VISUAL": "'my editor' -w"})
        platform_default = editor_setting({})
        unresolved = editor_argv({})
    with mock.patch("akaribot.cli.tui.config.shutil.which", return_value=None):
        missing = editor_argv({"VISUAL": "code"})
    return (
        visual == ["code", "-w"]
        and fallback == ["nano"]
        and quoted == ["my editor", "-w"]
        and platform_default == default
        and unresolved == [default]
        and missing is None
    )


def _test_derived_instance_table_keeps_its_own_file():
    # 派生实例表按完整表名定位文件，文件缺失时仍返回候选路径。
    with TemporaryDirectory(prefix="akari-config-file-") as raw:
        root = Path(raw).resolve()
        (root / "akaribot.toml").write_text("", encoding="utf-8")
        derived = _config_file(root, "bot_telegram-alt", "[bot_telegram-alt]\n")
        shared = _config_file(root, "config", RAW["config"])
        source = SubprocessConfigSource(root=root)
        # 清除 AKARI_INSTANCE_DIR，隔离本机当前实例对路径解析的影响。
        with mock.patch.dict(os.environ):
            os.environ.pop("AKARI_INSTANCE_DIR", None)
            instance = source.config_file("bot_telegram-alt")
            secret = source.config_file("secret")
            absent = source.config_file("bot_qq")
    return instance == derived and secret == shared and absent == root / "config" / "bot_qq.toml"


async def _test_editor_button_reports_command_outside_terminal():
    # 非交互终端仅提供路径与命令，不挂起界面或启动编辑器。
    with TemporaryDirectory(prefix="akari-editor-") as raw:
        target = _config_file(Path(raw).resolve(), "config", RAW["config"])
        source = _source(files={"config": target})
        notes: list[str] = []
        seen: list[list[str]] = []

        async def body(app, page, pilot, source):
            page._stdin_isatty = lambda: False
            page._editor_runner = lambda argv, **kwargs: seen.append(list(argv))
            before = dict(source.calls)
            with _editor_env({"VISUAL": "code -w"}):
                with mock.patch.object(compat, "notify", lambda app, message, **kwargs: notes.append(message)):
                    page.query_one("#open-editor", compat.Button).press()
                    await _wait_until(lambda: bool(notes))
                    await page.wait_for_idle()
                    await pilot.pause()
            status = page.status_text
            calls = dict(source.calls)
            await pilot.press("q")
            return status, calls, before

        status, calls, before = await _with_page(body, source)
    expected = i18n.t(
        "cli.tui.config.editor_noninteractive",
        path=str(target),
        command=shlex.join(["code", "-w", str(target)]),
    )
    return notes == [expected] and seen == [] and calls == before and status == expected


async def _test_editor_action_suspends_and_rereads():
    # 交互编辑须先挂起界面，编辑器退出后再重新加载配置。
    with TemporaryDirectory(prefix="akari-editor-") as raw:
        target = _config_file(Path(raw).resolve(), "config", RAW["config"])
        source = _source(files={"config": target})

        async def body(app, page, pilot, source):
            events: list[str] = []
            codes = [0, 7]
            seen: list[tuple[list[str], int]] = []

            def runner(argv, **kwargs):
                # 记录编辑器启动前的读取次数，用于验证重新加载发生在编辑器退出后。
                seen.append((list(argv), source.calls["schema"]))
                events.append("run")
                return subprocess.CompletedProcess(list(argv), codes.pop(0))

            page._stdin_isatty = lambda: True
            page._editor_runner = runner
            page._suspend = _recording_suspend(events)
            before = source.calls["schema"]
            with _editor_env({"VISUAL": "code -w"}):
                await pilot.press("o")
                await _wait_until(lambda: len(seen) == 1)
                await page.wait_for_idle()
                await pilot.pause()
                first = page.status_text
                await pilot.press("o")
                await _wait_until(lambda: len(seen) == 2)
                await page.wait_for_idle()
                await pilot.pause()
                second = page.status_text
            after = source.calls["schema"]
            await pilot.press("q")
            return events, seen, before, after, first, second

        events, seen, before, after, first, second = await _with_page(body, source)
    argv = ["code", "-w", str(target)]
    return (
        seen == [(argv, before), (argv, before + 1)]
        and after == before + 2
        and events == ["suspend-enter", "run", "suspend-exit"] * 2
        and first == i18n.t("cli.tui.config.status_editor_done", table="config", code=0)
        and second == i18n.t("cli.tui.config.status_editor_done", table="config", code=7)
    )


async def _test_editor_action_reports_missing_table_or_file():

    with TemporaryDirectory(prefix="akari-editor-") as raw:
        target = _config_file(Path(raw).resolve(), "config", RAW["config"])
        source = _source(files={"config": target})

        async def body(app, page, pilot, source):
            page._stdin_isatty = lambda: True
            seen: list[list[str]] = []
            notes: list[str] = []
            page._editor_runner = lambda argv, **kwargs: seen.append(list(argv))
            with mock.patch.object(compat, "notify", lambda app, message, **kwargs: notes.append(message)):
                page.query_one("#table-list", compat.ListView).index = 1
                await page.wait_for_idle()
                await pilot.pause()
                await page.open_in_editor()
                no_file = page.status_text
                await page.select_table(None)
                await pilot.pause()
                await page.open_in_editor()
                no_selection = page.status_text
            await pilot.press("q")
            return no_file, no_selection, seen, notes

        no_file, no_selection, seen, notes = await _with_page(body, source)
    return (
        no_file == i18n.t("cli.tui.config.status_editor_no_file", table="module_wiki")
        and no_selection == i18n.t("cli.tui.config.status_editor_no_selection")
        and seen == []
        and notes == []
    )


async def _test_editor_action_reports_unusable_editor():

    with TemporaryDirectory(prefix="akari-editor-") as raw:
        target = _config_file(Path(raw).resolve(), "config", RAW["config"])
        source = _source(files={"config": target})

        async def body(app, page, pilot, source):
            page._stdin_isatty = lambda: True
            seen: list[list[str]] = []
            events: list[str] = []
            page._editor_runner = lambda argv, **kwargs: seen.append(list(argv))
            page._suspend = _recording_suspend(events)
            with _editor_env({"VISUAL": "code -w"}, found=None):
                await page.open_in_editor()
            status = page.status_text
            await pilot.press("q")
            return status, seen, events

        status, seen, events = await _with_page(body, source)
    return status == i18n.t("cli.tui.config.status_editor_missing", editor="code -w") and seen == [] and events == []


async def _test_editor_action_asks_before_discarding_edits():
    # 外部编辑器会触发配置重新加载，启动前必须确认未保存更改。
    with TemporaryDirectory(prefix="akari-editor-") as raw:
        target = _config_file(Path(raw).resolve(), "config", RAW["config"])
        source = _source(files={"config": target})

        async def body(app, page, pilot, source):
            seen: list[list[str]] = []
            events: list[str] = []

            def runner(argv, **kwargs):
                seen.append(list(argv))
                return subprocess.CompletedProcess(list(argv), 0)

            page._stdin_isatty = lambda: True
            page._editor_runner = runner
            page._suspend = _recording_suspend(events)
            page.row_for("count").set_text("9")
            await pilot.pause()
            with _editor_env({"VISUAL": "code -w"}):
                await pilot.press("o")
                await pilot.pause()
                opened = len(app.screen_stack) > 1
                await pilot.press("escape")
                await pilot.pause()
                kept = (page.is_dirty(), page.row_for("count").text, list(seen))
                await pilot.press("o")
                await pilot.pause()
                await pilot.press("enter")
                await _wait_until(lambda: bool(seen))
                await page.wait_for_idle()
                await pilot.pause()
                status = page.status_text
            await pilot.press("q")
            return opened, kept, status, seen, page.is_dirty(), page.row_for("count").text

        opened, kept, status, seen, dirty, text = await _with_page(body, source)
    return (
        opened
        and kept == (True, "9", [])
        and seen == [["code", "-w", str(target)]]
        and status == i18n.t("cli.tui.config.status_editor_done", table="config", code=0)
        and dirty is False
        and text == "3"
    )


@func_case
async def test_tui_config(tester: Tester):
    """cli.tui.config: 未保存更改的拦截与外部编辑器动作"""
    _use_cli_locale()
    # 缩短防抖窗口，避免功能测试依赖实际按键间隔。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_worker_marks_stop_after_unmount, "页面卸载后异步渲染入口安全返回")
        await tester.test(_test_refresh_keeps_table_highlighted, "刷新后选中表仍然高亮")
        await tester.test(_test_dirty_note_tracks_edits, "脏值说明随编辑出现")
        await tester.test(_test_table_switch_keeps_edits, "换表选择保留则不切换")
        await tester.test(_test_table_switch_discards_edits, "换表选择放弃才切换")
        await tester.test(_test_reload_asks_before_rereading, "重读前先问")
        await tester.test(_test_forced_refresh_asks, "强制刷新前先问")
        await tester.test(_test_mode_switch_asks_before_switching, "切模式前先问")
        await tester.test(_test_raw_edits_count_as_dirty, "原始文本的编辑也算脏值")
        await tester.test(_test_form_hint_reads_widget_text, "表单区提示可按纯文本读回")
        await tester.test(_test_low_frequency_bindings_stay_out_of_footer, "低频键位不进页脚")
        await tester.test(_test_editor_command_resolution, "编辑器命令按 VISUAL 与 EDITOR 解析")
        await tester.test(_test_derived_instance_table_keeps_its_own_file, "实例表按派生表名定位文件")
        await tester.test(_test_editor_button_reports_command_outside_terminal, "非交互终端只报路径与命令")
        await tester.test(_test_editor_action_suspends_and_rereads, "交互终端下挂起界面并重读")
        await tester.test(_test_editor_action_reports_missing_table_or_file, "拿不到表或文件只说状态栏")
        await tester.test(_test_editor_action_reports_unusable_editor, "编辑器不可用时只说状态栏")
        await tester.test(_test_editor_action_asks_before_discarding_edits, "未保存改动前先问")
    return tester
