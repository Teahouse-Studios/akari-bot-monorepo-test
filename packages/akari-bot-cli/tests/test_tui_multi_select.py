"""Modules 页的多选与批量操作。

选择模型对齐桌面列表：Ctrl（macOS 的 Control）逐个切换、Shift 扩选一段、普通点击收敛为单选；
键盘上以 Space/Ctrl+Space 切换、Shift+↑/↓ 扩选。批量操作作用于选区，单条操作仍是「没有选区时
按当前项」，两者共用同一条执行路径。批量卸载先确认目标，目标过多时改成输入数量。
"""

import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.modules import ModuleRecord, OperationResult, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORDS = [
    ModuleRecord(name="alpha", dist="akari-bot-module-alpha", version="1.0.0", state="installed"),
    ModuleRecord(name="bravo", dist="akari-bot-module-bravo", version="1.0.0", state="installed"),
    ModuleRecord(name="charlie", dist="akari-bot-module-charlie", version="0.9.0", state="available"),
    ModuleRecord(name="delta", dist="akari-bot-module-delta", version="0.9.0", state="available"),
]


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticModuleSource:
    params = {
        "records": RECORDS,
        "available": RECORDS,
        "stream_lines": ["Resolved 1 package", "Installed 1 package"],
    }
    params.update(kwargs)
    return StaticModuleSource(**params)


async def _with_page(body, source: StaticModuleSource | None = None, *, records=None):
    chosen = source if source is not None else _source()
    app = TuiApp(source=chosen, initial_page="modules", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=(110, 34)) as pilot:
        page = app.modules_page()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _choice_labels(app: TuiApp) -> list[str]:
    return [str(button.label) for button in app.screen.query("#choice-actions Button")]


async def _pick_choice(app: TuiApp, pilot, index: int) -> None:
    # 直接派发按下消息：选项多时按钮可能排到可视区之外，按坐标点击会落空。
    app.screen.query_one(f"#choice-{index}", compat.Button).press()
    await pilot.pause()


def _positions(page) -> list[int]:
    names = [record.dist for record in page.visible_records]
    return sorted(names.index(dist) for dist in page._selected if dist in names)


async def _test_space_toggles_selection():
    async def body(app, page, pilot, source):
        await pilot.press("space")
        await pilot.pause()
        first = _positions(page)
        await pilot.press("space")
        await pilot.pause()
        second = _positions(page)
        await pilot.press("ctrl+space")
        await pilot.pause()
        third = _positions(page)
        await pilot.press("q")
        return first, second, third

    first, second, third = await _with_page(body)
    return first == [0] and second == [] and third == [0]


async def _test_shift_extends_and_replaces_range():
    async def body(app, page, pilot, source):
        await pilot.press("space")  # 锚点落在第 0 行
        await pilot.pause()
        for _ in range(3):
            await pilot.press("down")
            await pilot.pause()
        moved = _positions(page)
        await pilot.press("shift+down")
        await pilot.pause()
        extended = _positions(page)
        await pilot.press("shift+down")
        await pilot.pause()
        further = _positions(page)
        await pilot.press("shift+up")
        await pilot.pause()
        shrunk = _positions(page)
        await pilot.press("q")
        return moved, extended, further, shrunk

    moved, extended, further, shrunk = await _with_page(body)
    return moved == [0] and extended == [0, 1, 2, 3] and further == [0, 1, 2, 3] and shrunk == [0, 1, 2]


async def _test_select_all_and_clear():
    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        all_selected = len(page._selected)
        await pilot.press("slash")
        await pilot.pause()
        page.set_query("a")
        await pilot.pause()
        page.action_clear_selection()
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        filtered = _positions(page)
        visible = len(page.visible_records)
        page.action_clear_selection()
        await pilot.pause()
        cleared = len(page._selected)
        await pilot.press("q")
        return all_selected, visible, filtered, cleared

    all_selected, visible, filtered, cleared = await _with_page(body)
    return all_selected == len(RECORDS) and visible < len(RECORDS) and len(filtered) == visible and cleared == 0


async def _test_mouse_modifiers():
    async def body(app, page, pilot, source):
        list_view = page.query_one("#module-list", compat.ListView)

        async def click(index: int, **modifiers):
            await pilot.click(list(list_view.children)[index], **modifiers)
            await pilot.pause()

        await click(1)
        single = _positions(page)
        await click(3, control=True)
        added = _positions(page)
        await click(0, shift=True)
        ranged = _positions(page)
        await click(2)
        collapsed = _positions(page)
        await pilot.press("q")
        return single, added, ranged, collapsed

    single, added, ranged, collapsed = await _with_page(body)
    # Shift+点击从锚点（最后一次点击的 #3）扩到 #0，故是 0..3。
    return single == [1] and added == [1, 3] and ranged == [0, 1, 2, 3] and collapsed == [2]


async def _test_batch_install_covers_selection():
    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        page.request_install()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.installed, page.stream_lines

    installed, lines = await _with_page(body)
    return installed == ["akari-bot-module-charlie", "akari-bot-module-delta"] and len(lines) == 4


async def _test_batch_uninstall_needs_confirmation():
    # 一次按键即弹出处置方式，标题列出全部目标；选完才执行。
    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        asked = list(source.uninstalled)
        title = str(app.screen.query_one("#choice-title", compat.Static).render())
        labels = _choice_labels(app)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, title, labels, list(source.uninstalled)

    asked, title, labels, uninstalled = await _with_page(body)
    return (
        asked == []
        and title
        == i18n.t(
            "cli.tui.modules.uninstall_confirm_many",
            count=2,
            names="akari-bot-module-alpha、akari-bot-module-bravo",
        )
        and i18n.t("cli.tui.modules.uninstall_keep_data") in labels
        and i18n.t("cli.tui.modules.uninstall_purge_data") in labels
        and uninstalled == ["akari-bot-module-alpha", "akari-bot-module-bravo"]
    )


async def _test_batch_uninstall_can_purge_data():
    # 「连数据一起清」把 --purge-data 交给 CLI；界面已确认过，故同时带 --yes。
    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        await _pick_choice(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.stream_calls)

    calls = await _with_page(body)
    return calls == [
        ("uninstall", "akari-bot-module-alpha", ("--purge-data",), True),
        ("uninstall", "akari-bot-module-bravo", ("--purge-data",), True),
    ]


async def _test_batch_uninstall_offers_cascade_for_dependents():
    # 有反向依赖时模态框里多出 --cascade 一项，并把依赖列表展开给用户看。
    dependent = ModuleRecord(
        name="alpha",
        dist="akari-bot-module-alpha",
        version="1.0.0",
        state="installed",
        dependents=("akari-bot-module-bravo",),
    )
    source = StaticModuleSource(records=[dependent], available=[dependent])
    hint = (
        f"{i18n.t('cli.tui.modules.uninstall_options_hint')}{i18n.t('cli.common.clause_separator')}"
        f"{i18n.t('cli.tui.modules.uninstall_cascade_hint', names='akari-bot-module-bravo')}"
    )

    async def body(app, page, pilot, chosen):
        await pilot.press("space")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        labels = _choice_labels(app)
        shown = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await _pick_choice(app, pilot, 2)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, shown, list(chosen.stream_calls)

    labels, shown, calls = await _with_page(body, source)
    return (
        labels[2] == i18n.t("cli.tui.modules.uninstall_cascade")
        and shown == hint
        and calls == [("uninstall", "akari-bot-module-alpha", ("--cascade",), True)]
    )


MANY = [
    ModuleRecord(name=f"pkg{index:02d}", dist=f"akari-bot-module-pkg{index:02d}", version="1.0.0", state="installed")
    for index in range(12)
]


async def _test_large_batch_requires_target_count():
    # 目标超过阈值时状态栏列不下全部名字，改为输入目标数量；输入不符即取消。
    source = StaticModuleSource(records=MANY, available=MANY)

    async def body(app, page, pilot, chosen):
        await pilot.press("a")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "3"
        await pilot.press("enter")
        await pilot.pause()
        mismatch = page.status_text
        rejected = list(chosen.uninstalled)
        page.request_uninstall()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "12"
        await pilot.press("enter")
        await pilot.pause()
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return mismatch, rejected, list(chosen.uninstalled)

    mismatch, rejected, uninstalled = await _with_page(body, source)
    return (
        mismatch == i18n.t("cli.tui.modules.uninstall_count_mismatch", given="3", count=12)
        and rejected == []
        and len(uninstalled) == 12
    )


async def _test_large_batch_cancelled_by_count_dialog():
    # 取消数量输入不执行任何卸载。
    source = StaticModuleSource(records=MANY, available=MANY)

    async def body(app, page, pilot, chosen):
        await pilot.press("a")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status, list(chosen.uninstalled)

    status, uninstalled = await _with_page(body, source)
    return status == i18n.t("cli.tui.modules.uninstall_cancelled") and uninstalled == []


async def _test_batch_continues_after_failure():
    class _Flaky(StaticModuleSource):
        def __init__(self):
            super().__init__(records=RECORDS, available=RECORDS, stream_lines=["boom"])
            self.seen: list[str] = []

        def install(self, record):
            self.seen.append(record.dist)
            if record.name == "charlie":
                return OperationResult(False, "安装失败", "boom: 依赖冲突")
            return OperationResult(True, "安装成功", "stub")

    source = _Flaky()

    async def body(app, page, pilot, chosen):
        await pilot.press("a")
        await pilot.pause()
        page.request_install()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return source.seen, page.status_text

    seen, status = await _with_page(body, source)
    expected = i18n.t(
        "cli.tui.modules.batch_failed",
        what=i18n.t("cli.tui.modules.action_install"),
        ok=1,
        failed=1,
        names="akari-bot-module-charlie",
        detail="boom: 依赖冲突",
    )
    return seen == ["akari-bot-module-charlie", "akari-bot-module-delta"] and status == expected


async def _test_selection_pruned_on_refresh():
    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        before = len(page._selected)
        page.invalidate_cache()
        source._records = (RECORDS[0],)
        source._available = (RECORDS[0],)
        await page._load_records()
        await pilot.pause()
        after = sorted(page._selected)
        await pilot.press("q")
        return before, after

    before, after = await _with_page(body)
    return before == len(RECORDS) and after == ["akari-bot-module-alpha"]


async def _test_rows_show_selection_marker():
    async def body(app, page, pilot, source):
        await pilot.press("space")
        await pilot.pause()
        rows = page.row_texts()
        count = str(page.query_one("#count", compat.Static).render())
        await pilot.press("q")
        return rows[0], rows[1], count

    first, second, count = await _with_page(body)
    return (
        first.startswith("✓") and second.startswith(" ") and i18n.t("cli.tui.modules.count_selected", count=1) in count
    )


@func_case
async def test_tui_multi_select(tester: Tester):
    """cli.tui.modules: 多选与批量操作测试"""
    _use_cli_locale()
    # 用例里的两次按键几乎同时发生，压缩防抖窗口，免得每条确认都等 0.4 秒。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_space_toggles_selection, "Space/Ctrl+Space 切换选中")
        await tester.test(_test_shift_extends_and_replaces_range, "Shift+↑/↓ 扩选且重算范围")
        await tester.test(_test_select_all_and_clear, "全选可见与清空")
        await tester.test(_test_mouse_modifiers, "鼠标 Ctrl/Shift/普通点击")
        await tester.test(_test_batch_install_covers_selection, "批量安装按选区执行")
        await tester.test(_test_batch_uninstall_needs_confirmation, "批量卸载需确认并选处置方式")
        await tester.test(_test_batch_uninstall_can_purge_data, "批量卸载可连数据一起清")
        await tester.test(_test_batch_uninstall_offers_cascade_for_dependents, "有反向依赖时给出连同依赖卸载")
        await tester.test(_test_large_batch_requires_target_count, "超过阈值时按目标数量确认")
        await tester.test(_test_large_batch_cancelled_by_count_dialog, "数量输入取消后不卸载")
        await tester.test(_test_batch_continues_after_failure, "批量中单条失败不中断")
        await tester.test(_test_selection_pruned_on_refresh, "刷新后剪掉失效选区")
        await tester.test(_test_rows_show_selection_marker, "选中行显示勾选标记")
    return tester
