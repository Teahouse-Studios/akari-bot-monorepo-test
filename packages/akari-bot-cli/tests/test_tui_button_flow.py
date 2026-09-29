"""按宽度自动折行的按钮区。

页底一组动作在宽终端下一行放得下，固定按两行摆放会空出整行高度与右侧大片空白；窄终端下又必须
折行。``ButtonFlow`` 负责这件事：按按钮自然宽度装箱，放不下才折行，并优先在语义分组处断开。
"""

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import PAGES, TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORD = ModuleRecord(name="coin", dist="akari-bot-module-coin", version="0.1.0", state="installed")

# 每个标签四个汉字（八格）加两格内边距，故每个按钮十格；八个按钮一行需要 80 格。
SPECS = tuple((f"b{index}", "切换实例") for index in range(8))


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _rows(flow: compat.ButtonFlow) -> list[list[str]]:
    # 按渲染出来的行坐标分组：按钮始终挂在同一层，行由列数决定。
    rows: dict[int, list[str]] = {}
    for button in flow.query(compat.Button):
        rows.setdefault(button.region.y, []).append(str(button.id))
    return [rows[key] for key in sorted(rows)]


# 只放一个按钮区的测试页面。
class _FlowPage(compat.Vertical):
    def compose(self) -> compat.ComposeResult:
        """装配按钮区。"""
        yield compat.ButtonFlow(*SPECS, breaks=("b3",), id="flow")


async def _measure(body, *, size):
    app = TuiApp(source=StaticModuleSource([RECORD]), initial_page="modules", boot_started_at=0.0)
    async with compat.app_test(app, size=size) as pilot:
        page = _FlowPage(id="page-flow")
        await app.query_one("#content", compat.Vertical).mount(page)
        await pilot.pause()
        return await body(app, page, pilot)


async def _test_wide_screen_keeps_one_row():
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        rows = _rows(flow)
        boxes = [button.region for button in flow.query(compat.Button)]
        await pilot.press("q")
        return rows, boxes, page.region

    rows, boxes, region = await _measure(body, size=(140, 30))
    return (
        len(rows) == 1
        and len(rows[0]) == len(SPECS)
        and all(box.x >= region.x and box.right <= region.right for box in boxes)
    )


async def _test_narrow_screen_breaks_at_group():
    # 80 格放不下八个按钮，按 breaks 指定的分组断成 4 + 4，而不是一路塞到放不下为止。
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        rows = _rows(flow)
        boxes = [button.region for button in flow.query(compat.Button)]
        await pilot.press("q")
        return rows, boxes, page.region

    rows, boxes, region = await _measure(body, size=(80, 24))
    return (
        len(rows) == 2
        and [len(row) for row in rows] == [4, 4]
        and rows[0][-1] == "b3"
        and all(box.x >= region.x and box.right <= region.right for box in boxes)
    )


async def _test_buttons_exist_before_first_layout():
    # 按钮在挂载时就建好：页面挂载后立刻按 id 取用（改写标签、同步禁用）不能落空。
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        labels = [str(flow.query_one(f"#b{index}", compat.Button).label) for index in range(len(SPECS))]
        await pilot.press("q")
        return labels

    labels = await _measure(body, size=(80, 24))
    return labels == ["切换实例"] * len(SPECS)


async def _test_longer_label_repacks():
    # 标签变长会把后面的按钮挤出去，改完标签要重新装箱。
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        before = _rows(flow)
        for index in range(len(SPECS)):
            flow.query_one(f"#b{index}", compat.Button).label = "把所有已安装的包更新到最新版本"
        flow.relayout()
        await pilot.pause()
        after = _rows(flow)
        width = app.size.width
        boxes = [button.region for button in flow.query(compat.Button)]
        await pilot.press("q")
        return before, after, boxes, width

    before, after, boxes, width = await _measure(body, size=(80, 24))
    return len(before) == 2 and len(after) > len(before) and all(box.x >= 0 and box.right <= width for box in boxes)


async def _test_navigation_still_reports_eleven_pages():
    # 页面清单没有因为按钮区改造而变化。
    return [key for key, _, _ in PAGES] == [
        "dashboard",
        "environment",
        "database",
        "modules",
        "adapters",
        "config",
        "logs",
        "run",
        "dev",
        "doctor",
        "misc",
    ]


@func_case
async def test_tui_button_flow(tester: Tester):
    """cli.tui._compat: 按钮区按宽度折行测试"""
    _use_cli_locale()
    await tester.test(_test_wide_screen_keeps_one_row, "宽终端下一行放完")
    await tester.test(_test_narrow_screen_breaks_at_group, "窄终端在语义分组处折行")
    await tester.test(_test_buttons_exist_before_first_layout, "挂载即可按 id 取到按钮")
    await tester.test(_test_longer_label_repacks, "标签变长后重新装箱且不溢出")
    await tester.test(_test_navigation_still_reports_eleven_pages, "页面清单不变")

    return tester
