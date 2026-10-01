"""Dev 页动作：跑测试与生成脚手架。

包清单本身只读，两个动作各起一次 CLI 子进程：``t`` 跑 ``akaribot test``，``n`` 跑 ``akaribot new``。
断言全部走注入的替身数据源——真实测试套件要跑数分钟，脚手架会写盘，都不适合放进用例。新建表单的类型
是二态按钮，另收 config / database / tests 三个开关。动作输出全部留在可滚动的输出区：行数与跟随状态在
输出区标题行，状态栏只给结论与下一步；新文案键尚未并入 locales 时先从片段合并语言快照。
"""

import asyncio
import json
import shutil
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dev import (
    ACTION_NEW,
    ACTION_TEST,
    TARGET_ADAPTER,
    TARGET_MODULE,
    ActionResult,
    DevPage,
    DevSnapshot,
    StaticDevSource,
    SubprocessDevSource,
)
from akaribot.testing import Tester, func_case

WORKSPACE = "/tmp/akari-dev-workspace"
INSTANCE = "/tmp/akari-dev-instance"
SNAPSHOT = DevSnapshot(instance_root=INSTANCE, workspace_root=WORKSPACE, workspace_exists=True)
TEST_TARGET = "packages/akari-bot-cli/tests/test_tui_dev_actions.py"
TEST_OUTPUT = ("collected 3 items", "3 passed")
FAILED_OUTPUT = ("collected 2 items", "1 failed", "AssertionError: boom")
LONG_OUTPUT = tuple(f"用例行 {index:03d}" for index in range(1, 201))
FOLLOW_OUTPUT = tuple(f"line {index:03d}" for index in range(1, 41))
FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "dev.json"
# 快照放在本文件专用的命名空间：共享命名空间会被其他测试进程按包内 locales 重新发布，
# 连接期间取词随之回退，片段文案读不到。
LOCALE_NAMESPACE = "akaribot-cli-dev-actions"
FORM_CONTROLS = (
    "refresh",
    "run-tests",
    "test-path",
    "new-package",
    "focus-output",
    "new-name",
    "new-kind",
    "new-config",
    "new-database",
    "new-tests",
    "new-dir",
    "new-confirm",
    "new-close",
    "action-output-title",
    "action-output",
    "action-output-text",
)
_KEEP_ALIVE: list[TemporaryDirectory] = []


def _merged_locale_dir() -> Path:
    # 片段里的新键尚未并入 locales：合成一份合并后的语言目录，断言才取到真实渲染结果。
    holder = TemporaryDirectory(prefix="akari-dev-locale-")
    _KEEP_ALIVE.append(holder)
    root = Path(holder.name)
    for path in Path(i18n.locales_dir()).glob("*.json"):
        shutil.copy(path, root / path.name)
    target = root / "zh_cn.json"
    document = json.loads(target.read_text(encoding="utf-8"))
    document.update(json.loads(FRAGMENT.read_text(encoding="utf-8")))
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return root


def _use_cli_locale() -> None:
    # CLI 的首次取文案会用包内 locales 重建快照，把合并目录顶掉；先取一次把它顶过，再建合并快照。
    i18n.t("cli.tui.common.status_ready")
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [str(_merged_locale_dir())], LOCALE_NAMESPACE)
    i18n.connect_locale_snapshot(LOCALE_NAMESPACE)


def _output_pane(page) -> compat.VerticalScroll:
    return page.query_one("#action-output", compat.VerticalScroll)


def _output_widget(page) -> compat.Static:
    return page.query_one("#action-output-text", compat.Static)


def _output_shown(page) -> str:
    return str(_output_widget(page).render())


def _source(**kwargs) -> StaticDevSource:
    params = {
        "snapshot": SNAPSHOT,
        "action_lines": TEST_OUTPUT,
        "action_result": ActionResult(ok=True, message="stub exit=0"),
    }
    params.update(kwargs)
    return StaticDevSource(**params)


async def _with_page(body, source: StaticDevSource | None = None, size: tuple[int, int] = (120, 44)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"dev": chosen}, initial_page="dev", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("dev")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _wait_until(predicate, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


def _set_input(page, selector: str, value: str) -> None:
    page.query_one(selector, compat.Input).value = value


async def _test_keys_and_controls_are_present():
    async def body(app, page, pilot, source):
        keys = {binding.key for binding in DevPage.BINDINGS}
        shown = {binding.key for binding in DevPage.BINDINGS if binding.show}
        missing = [name for name in FORM_CONTROLS if len(page.query(f"#{name}")) != 1]
        active = set(app.screen.active_bindings)
        await pilot.press("q")
        return keys, shown, missing, active

    keys, shown, missing, active = await _with_page(body)
    # 终止是低频动作，不进页脚；刷新、测试、新建与输出四条常驻。
    return (
        {"t", "n", "escape", "r", "o"} <= keys
        and {"t", "n", "r", "o"} <= shown
        and "escape" not in shown
        and not missing
        and {"t", "n", "o"} <= active
    )


async def _test_run_tests_streams_output():
    async def body(app, page, pilot, source):
        _set_input(page, "#test-path", TEST_TARGET)
        await pilot.press("t")
        await page.wait_for_idle()
        await pilot.pause()
        actions = source.actions
        lines = page.action_lines()
        output = page.action_output_text
        shown = _output_shown(page)
        title = page.output_title_text
        status = page.status_text
        result = page.action_result
        await pilot.press("q")
        return actions, lines, output, shown, title, status, result

    actions, lines, output, shown, title, status, result = await _with_page(body)
    return (
        actions == [(ACTION_TEST, {"args": (TEST_TARGET,), "cwd": WORKSPACE})]
        and lines == TEST_OUTPUT
        and output == "\n".join(TEST_OUTPUT)
        and shown == output
        and title == i18n.t("cli.tui.dev.output_title", count=len(TEST_OUTPUT))
        and result is not None
        and result.returncode == 0
        and "exit=0" in status
        and i18n.t("cli.tui.dev.status_next_step") in status
        and all(line not in status for line in TEST_OUTPUT)
    )


async def _test_second_press_while_running_is_ignored():
    source = _source(hold=True)

    async def body(app, page, pilot, chosen):
        await pilot.press("t")
        started = await _wait_until(lambda: chosen.calls["action"] == 1)
        await pilot.press("t")
        await pilot.press("n")
        await pilot.pause()
        during = (chosen.calls["action"], page.action_kind, page.new_form_open)
        chosen.gate.set()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return started, during, page.action_kind

    started, during, after = await _with_page(body, source)
    return started and during == (1, ACTION_TEST, False) and after == ""


async def _test_failed_status_is_conclusion_only():
    source = _source(
        action_lines=FAILED_OUTPUT,
        action_result=ActionResult(ok=False, returncode=7, detail="\n".join(FAILED_OUTPUT)),
    )

    async def body(app, page, pilot, chosen):
        await pilot.press("t")
        await page.wait_for_idle()
        await pilot.pause()
        result = page.action_result
        lines = page.action_lines()
        status = page.status_text
        title = page.output_title_text
        shown = _output_shown(page)
        await pilot.press("q")
        return result, lines, status, title, shown

    result, lines, status, title, shown = await _with_page(body, source)
    # 失败结论只有动作、退出码与下一步；输出整段留在输出区，不塞进状态栏。
    return (
        result is not None
        and not result.ok
        and result.returncode == 7
        and lines == FAILED_OUTPUT
        and result.detail == "\n".join(FAILED_OUTPUT)
        and status
        == i18n.t("cli.tui.dev.status_separator").join(
            (i18n.t("cli.tui.dev.status_action_failed", code=7), i18n.t("cli.tui.dev.status_next_step"))
        )
        and "失败" in status
        and "7" in status
        and all(line not in status for line in FAILED_OUTPUT)
        and title == i18n.t("cli.tui.dev.output_title", count=len(FAILED_OUTPUT))
        and shown == "\n".join(FAILED_OUTPUT)
    )


async def _test_long_output_is_fully_kept_and_scrollable():
    source = _source(action_lines=LONG_OUTPUT)

    async def body(app, page, pilot, chosen):
        await pilot.press("t")
        await page.wait_for_idle()
        await pilot.pause()
        pane = _output_pane(page)
        widget = _output_widget(page)
        kept = len(page.action_lines())
        rendered = _output_shown(page).split("\n")
        rows = widget.virtual_size.height
        pane_rows = pane.virtual_size.height
        await pilot.press("o")
        await pilot.pause()
        focused = pane.has_focus
        await pilot.press("home")
        await pilot.pause()
        top = pane.scroll_offset.y
        first_visible = pane.region.contains(widget.region.x, widget.region.y)
        tail_visible_at_top = pane.region.contains(widget.region.x, widget.region.bottom)
        first_row = widget.render_line(0).text.rstrip()
        await pilot.press("pagedown")
        await pilot.pause()
        paged = pane.scroll_offset.y
        await pilot.press("end")
        await pilot.pause()
        bottom = pane.is_vertical_scroll_end
        bottom_offset = pane.scroll_offset.y
        tail_visible = pane.region.contains(widget.region.x, widget.region.bottom)
        first_visible_at_end = pane.region.contains(widget.region.x, widget.region.y)
        last_row = widget.render_line(widget.region.height - 1).text.rstrip()
        await pilot.press("q")
        return (
            kept,
            rendered,
            rows,
            pane_rows,
            focused,
            top,
            first_visible,
            tail_visible_at_top,
            first_row,
            paged,
            bottom,
            bottom_offset,
            tail_visible,
            first_visible_at_end,
            last_row,
        )

    values = await _with_page(body, source)
    (
        kept,
        rendered,
        rows,
        pane_rows,
        focused,
        top,
        first_visible,
        tail_visible_at_top,
        first_row,
        paged,
        bottom,
        bottom_offset,
        tail_visible,
        first_visible_at_end,
        last_row,
    ) = values
    return (
        kept == 200
        and len(rendered) == 200
        and rendered[0] == LONG_OUTPUT[0]
        and rendered[-1] == LONG_OUTPUT[-1]
        and rows == 200
        and pane_rows >= 200
        and focused
        and top == 0
        and first_visible
        and not tail_visible_at_top
        and first_row == LONG_OUTPUT[0]
        and paged > 0
        and bottom
        and bottom_offset > 0
        and tail_visible
        and not first_visible_at_end
        and last_row == LONG_OUTPUT[-1]
    )


async def _test_follow_pauses_on_scroll_back_and_resumes():
    source = _source(action_lines=(), hold=True)

    async def body(app, page, pilot, chosen):
        await pilot.press("t")
        started = await _wait_until(lambda: chosen.calls["action"] == 1)
        for line in FOLLOW_OUTPUT:
            chosen.emit(line)
        pane = _output_pane(page)
        widget = _output_widget(page)
        pinned = await _wait_until(lambda: pane.is_vertical_scroll_end)
        pinned_tail = pane.region.contains(widget.region.x, widget.region.bottom)
        await pilot.press("o")
        await pilot.pause()
        entered = pane.has_focus
        await pilot.press("home")
        await pilot.pause()
        detached = not pane.is_vertical_scroll_end
        chosen.emit("line 041")
        await pilot.pause()
        held_offset = pane.scroll_offset.y
        paused_title = i18n.t("cli.tui.dev.status_separator").join(
            (i18n.t("cli.tui.dev.output_title", count=len(FOLLOW_OUTPUT) + 1), i18n.t("cli.tui.dev.output_paused"))
        )
        announced = page.output_title_text == paused_title
        await pilot.press("end")
        await pilot.pause()
        chosen.emit("line 042")
        following = await _wait_until(
            lambda: pane.is_vertical_scroll_end and pane.region.contains(widget.region.x, widget.region.bottom)
        )
        resumed_title = page.output_title_text
        chosen.gate.set()
        await page.wait_for_idle()
        await pilot.pause()
        finished_title = page.output_title_text
        await pilot.press("q")
        return (
            started,
            pinned,
            pinned_tail,
            entered,
            detached,
            held_offset,
            announced,
            following,
            resumed_title,
            finished_title,
        )

    values = await _with_page(body, source)
    started, pinned, pinned_tail, entered, detached, held_offset = values[:6]
    announced, following, resumed_title, finished_title = values[6:]
    counted = i18n.t("cli.tui.dev.output_title", count=len(FOLLOW_OUTPUT) + 2)
    # 上滚后新行不再把视口拽回底部，标题改报暂停与恢复方式；按 End 回到末尾后继续跟。
    return (
        started
        and pinned
        and pinned_tail
        and entered
        and detached
        and held_offset == 0
        and announced
        and following
        and resumed_title == counted
        and finished_title == counted
    )


def _test_fragment_texts_are_active():
    document = json.loads(FRAGMENT.read_text(encoding="utf-8"))
    # 片段里的键尚未并入 locales：合并快照就位后，逐键取到的文本必须与片段一致。
    return all(i18n.t(key) == value for key, value in document.items())


async def _test_empty_output_hint():
    async def body(app, page, pilot, source):
        pane = _output_pane(page)
        hidden = not pane.display
        hint_at_mount = _output_shown(page)
        page.query_one("#focus-output", compat.Button).press()
        await pilot.pause()
        shown = pane.display
        focused = pane.has_focus
        hint = _output_shown(page)
        title = page.output_title_text
        await pilot.press("q")
        return hidden, hint_at_mount, shown, focused, hint, title

    hidden, hint_at_mount, shown, focused, hint, title = await _with_page(body)
    # 没有动作时输出区收起；键位与按钮打开它后，区内说明本次动作还没有输出。
    return (
        hidden
        and hint_at_mount == i18n.t("cli.tui.dev.output_empty")
        and shown
        and focused
        and hint == i18n.t("cli.tui.dev.output_empty")
        and title == i18n.t("cli.tui.dev.output_title", count=0)
    )


class _FakeStdout:
    # 子进程标准输出的替身：异步逐行产出字节，与 asyncio 子进程的读取方式一致。
    def __init__(self, lines: tuple[str, ...]) -> None:
        self._lines = lines

    def __aiter__(self):
        return self._iterate()

    async def _iterate(self):
        for line in self._lines:
            yield f"{line}\n".encode()


class _FakeProcess:
    def __init__(self, lines: tuple[str, ...]) -> None:
        self.stdout = _FakeStdout(lines)

    async def wait(self) -> int:
        return 0


async def _test_stream_detail_keeps_full_output():
    lines = tuple(f"line {index:03d}" for index in range(1, 61))
    received: list[str] = []
    detail: list[str] = []
    returncode = await SubprocessDevSource._pump(_FakeProcess(lines), received.append, detail)
    return returncode == 0 and received == list(lines) and detail == list(lines) and len(detail) > 40


async def _test_new_form_rejects_invalid_names():
    async def body(app, page, pilot, source):
        await pilot.press("n")
        await pilot.pause()
        opened = page.new_form_open
        rejected = []
        for candidate in ("", "bad name", "bad/name", "bad\\name"):
            _set_input(page, "#new-name", candidate)
            await pilot.press("enter")
            await pilot.pause()
            rejected.append((bool(page.new_hint_text), page.new_form_open))
        await pilot.press("q")
        return opened, rejected, source.calls["action"], source.actions

    opened, rejected, action_calls, actions = await _with_page(body)
    return opened and all(hint and still_open for hint, still_open in rejected) and action_calls == 0 and actions == []


async def _test_new_form_shows_skeleton_hint():
    async def body(app, page, pilot, source):
        await pilot.press("n")
        await pilot.pause()
        hint = page.new_hint_text
        label = str(page.query_one("#new-kind", compat.Button).label)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return hint, label

    hint, label = await _with_page(body)
    return (
        hint == i18n.t("cli.tui.dev.new_skeleton_hint")
        and "${" not in hint
        and label == i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t("cli.tui.dev.new_kind_module"))
    )


async def _test_kind_toggle_switches_label():
    async def body(app, page, pilot, source):
        await pilot.press("n")
        await pilot.pause()
        module_label = str(page.query_one("#new-kind", compat.Button).label)
        page.query_one("#new-kind", compat.Button).press()
        await pilot.pause()
        adapter_label = str(page.query_one("#new-kind", compat.Button).label)
        adapter_disabled = page.query_one("#new-database", compat.Checkbox).disabled
        page.query_one("#new-kind", compat.Button).press()
        await pilot.pause()
        back = str(page.query_one("#new-kind", compat.Button).label)
        module_disabled = page.query_one("#new-database", compat.Checkbox).disabled
        await pilot.press("q")
        return module_label, adapter_label, adapter_disabled, back, module_disabled

    module_label, adapter_label, adapter_disabled, back, module_disabled = await _with_page(body)
    return (
        module_label == i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t("cli.tui.dev.new_kind_module"))
        and adapter_label == i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t("cli.tui.dev.new_kind_adapter"))
        and adapter_disabled is True
        and back == module_label
        and module_disabled is False
    )


async def _test_new_form_submits_adapter():
    async def body(app, page, pilot, source):
        await pilot.press("n")
        await pilot.pause()
        _set_input(page, "#new-name", "demo")
        page.query_one("#new-kind", compat.Button).press()
        await pilot.pause()
        adapter_label = str(page.query_one("#new-kind", compat.Button).label)
        # 按下按钮后焦点在按钮上，回车会再切一次类型；交回名称输入框再提交。
        compat.focus_now(page.query_one("#new-name", compat.Input))
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        actions = source.actions
        form_open = page.new_form_open
        focused = app.focused
        hidden_focus = focused is None or page.query_one("#new-form") in focused.ancestors_with_self
        await pilot.press("q")
        return actions, adapter_label, form_open, hidden_focus

    actions, adapter_label, form_open, hidden_focus = await _with_page(body)
    return (
        actions
        == [
            (
                ACTION_NEW,
                {
                    "name": "demo",
                    "target": TARGET_ADAPTER,
                    "directory": "",
                    "config": False,
                    "database": False,
                    "tests": True,
                    "cwd": WORKSPACE,
                },
            )
        ]
        and adapter_label == i18n.t("cli.tui.dev.new_kind_toggle", kind=i18n.t("cli.tui.dev.new_kind_adapter"))
        and form_open is False
        and not hidden_focus
    )


async def _test_new_form_carries_switches():
    async def body(app, page, pilot, source):
        await pilot.press("n")
        await pilot.pause()
        _set_input(page, "#new-name", "demo")
        page.query_one("#new-config", compat.Checkbox).value = True
        page.query_one("#new-database", compat.Checkbox).value = True
        page.query_one("#new-tests", compat.Checkbox).value = False
        await pilot.pause()
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        actions = source.actions
        await pilot.press("q")
        return actions

    actions = await _with_page(body)
    return actions == [
        (
            ACTION_NEW,
            {
                "name": "demo",
                "target": TARGET_MODULE,
                "directory": "",
                "config": True,
                "database": True,
                "tests": False,
                "cwd": WORKSPACE,
            },
        )
    ]


def _test_production_source_builds_argv():
    source = SubprocessDevSource(root=INSTANCE, timeout=5.0)
    module_params = {
        "name": "demo",
        "target": TARGET_MODULE,
        "directory": "packages/modules",
        "config": True,
        "database": True,
        "tests": True,
    }
    adapter_params = {"name": "demo", "target": TARGET_ADAPTER, "directory": "", "config": False}
    return (
        source._action_argv(ACTION_TEST, {"args": (TEST_TARGET, "--ci")})
        == cli_process.cli_argv("test", TEST_TARGET, "--ci")
        and source._action_argv(ACTION_TEST, {"args": ()}) == cli_process.cli_argv("test")
        # --non-interactive 是必需的：子进程与界面共用终端，缺了它会把问卷打进输出区并抢键盘。
        # 三个开关显式给值，未勾选时用 --no-* 覆盖 CLI 自己的缺省。
        and source._action_argv(ACTION_NEW, module_params)
        == cli_process.cli_argv(
            "new",
            "module",
            "demo",
            "--non-interactive",
            "--config",
            "--database",
            "--tests",
            "--dir",
            "packages/modules",
        )
        # new adapter 没有 database 与 tests 选项，多给的开关会被 typer 当成未知选项拒绝。
        and source._action_argv(ACTION_NEW, adapter_params)
        == cli_process.cli_argv("new", "adapter", "demo", "--non-interactive", "--no-config")
        and source._action_cwd({"cwd": WORKSPACE}) == WORKSPACE
        and source._action_cwd({}) == str(source.root)
    )


async def _test_new_success_reloads_packages():
    async def body(app, page, pilot, source):
        await _wait_until(lambda: source.calls["load"] >= 1)
        before = source.calls["load"]
        await pilot.press("n")
        await pilot.pause()
        _set_input(page, "#new-name", "demo")
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        after = source.calls["load"]
        result = page.action_result
        await pilot.press("q")
        return before, after, result

    before, after, result = await _with_page(body)
    return after == before + 1 and result is not None and result.ok


async def _test_new_failure_keeps_cache():
    source = _source(action_result=ActionResult(ok=False, returncode=1, message="stub exit=1"))

    async def body(app, page, pilot, chosen):
        await _wait_until(lambda: chosen.calls["load"] >= 1)
        before = chosen.calls["load"]
        await pilot.press("n")
        await pilot.pause()
        _set_input(page, "#new-name", "demo")
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        after = chosen.calls["load"]
        await pilot.press("q")
        return before, after

    before, after = await _with_page(body, source)
    return after == before


async def _test_escape_cancels_running_action():
    source = _source(hold=True)

    async def body(app, page, pilot, chosen):
        await pilot.press("t")
        started = await _wait_until(lambda: chosen.calls["action"] == 1)
        await pilot.press("escape")
        await page.wait_for_idle()
        await pilot.pause()
        result = page.action_result
        await pilot.press("q")
        return started, chosen.cancelled, chosen.calls["cancel"], result, page.action_kind

    started, cancelled, cancel_calls, result, kind = await _with_page(body, source)
    return (
        started
        and cancelled == [ACTION_TEST]
        and cancel_calls == 1
        and result is not None
        and result.cancelled
        and not result.ok
        and kind == ""
    )


async def _test_escape_on_idle_page_leaves_source_alone():
    async def body(app, page, pilot, source):
        await pilot.press("escape")
        await pilot.pause()
        idle_calls = source.calls["cancel"]
        await pilot.press("n")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return idle_calls, source.calls["cancel"], page.new_form_open

    idle_calls, total_calls, form_open = await _with_page(body)
    return idle_calls == 0 and total_calls == 0 and form_open is False


@func_case
async def test_tui_dev_actions(tester: Tester):
    """cli.tui.dev: 跑测试与生成脚手架的动作测试"""
    _use_cli_locale()
    await tester.test(_test_keys_and_controls_are_present, "键位与按钮齐备且在页脚生效")
    await tester.test(_test_run_tests_streams_output, "按 t 跑测试并逐行回显输出")
    await tester.test(_test_second_press_while_running_is_ignored, "运行中再按 t 不重复启动")
    await tester.test(_test_failed_status_is_conclusion_only, "失败时状态栏只给结论，整段输出留在输出区")
    await tester.test(_test_long_output_is_fully_kept_and_scrollable, "200 行输出全部保留且可滚到首末行")
    await tester.test(_test_follow_pauses_on_scroll_back_and_resumes, "运行中贴底跟随，上滚暂停，按 End 恢复")
    await tester.test(_test_empty_output_hint, "输出为空时区内说明本次动作还没有输出")
    await tester.test(_test_fragment_texts_are_active, "新增文案键写在片段文件里并已生效")
    await tester.test(_test_stream_detail_keeps_full_output, "生产数据源的详情保留完整输出")
    await tester.test(_test_new_form_rejects_invalid_names, "名称非法只提示不执行")
    await tester.test(_test_new_form_shows_skeleton_hint, "表单提示位写明只生成最小骨架")
    await tester.test(_test_kind_toggle_switches_label, "类型按钮在模块与适配器之间切换")
    await tester.test(_test_new_form_submits_adapter, "表单选适配器后提交")
    await tester.test(_test_new_form_carries_switches, "三个开关进入生成参数")
    await tester.test(_test_production_source_builds_argv, "生产数据源的 argv 形态")
    await tester.test(_test_new_success_reloads_packages, "新建成功后刷新包清单")
    await tester.test(_test_new_failure_keeps_cache, "新建失败不刷新包清单")
    await tester.test(_test_escape_cancels_running_action, "Esc 终止运行中的测试")
    await tester.test(_test_escape_on_idle_page_leaves_source_alone, "空闲时 Esc 不触碰数据源")
    return tester
