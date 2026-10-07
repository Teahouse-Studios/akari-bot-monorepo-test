"""按钮区的宽度适配、语义分组与动态重排测试。"""

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import PAGES, TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

RECORD = ModuleRecord(name="coin", dist="akari-bot-module-coin", version="0.1.0", state="installed")

# 每个标签四个汉字（八格）加两格内边距，故每个按钮十格；八个按钮一行需要 80 格。
SPECS = tuple((f"b{index}", "切换实例") for index in range(8))
MIXED_SPECS = (
    ("b0", "安装"),
    ("b1", "卸载"),
    ("b2", "刷新"),
    ("b3", "更新选中的模块"),
    ("b4", "更新所有已安装模块版本"),
)


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
    def __init__(self, *, specs=SPECS, breaks=("b3",), id=None):
        super().__init__(id=id)
        self._specs = specs
        self._breaks = breaks

    def compose(self) -> compat.ComposeResult:
        """装配按钮区。"""
        yield compat.ButtonFlow(*self._specs, breaks=self._breaks, id="flow")


async def _measure(body, *, size, specs=SPECS, breaks=("b3",)):
    app = TuiApp(source=StaticModuleSource([RECORD]), initial_page="modules", boot_started_at=0.0)
    async with compat.app_test(app, size=size) as pilot:
        page = _FlowPage(specs=specs, breaks=breaks, id="page-flow")
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
    # 窄屏按 breaks 指定的分组折行，每行四个按钮。
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
    # 页面挂载后需要立即按 id 更新按钮标签和禁用状态。
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        labels = [str(flow.query_one(f"#b{index}", compat.Button).label) for index in range(len(SPECS))]
        await pilot.press("q")
        return labels

    labels = await _measure(body, size=(80, 24))
    return labels == ["切换实例"] * len(SPECS)


async def _test_longer_label_repacks():
    # 标签宽度变化后需重新排布，避免后续按钮越界。
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


def _visible_buttons_fit(flow: compat.ButtonFlow) -> bool:
    bounds = flow.content_region
    boxes = [button.region for button in flow.query(compat.Button) if button.display]
    return (
        bool(boxes)
        and all(box.width > 0 and bounds.x <= box.x < box.right <= bounds.right for box in boxes)
        and all(not first.overlaps(second) for index, first in enumerate(boxes) for second in boxes[index + 1 :])
    )


async def _test_mixed_labels_fit_after_resize():
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        flow.styles.padding = (0, 1)
        await pilot.pause()
        row_counts = []
        for size in ((60, 24), (140, 30), (80, 24), (60, 24), (140, 30)):
            await pilot.resize_terminal(*size)
            await pilot.pause()
            if not _visible_buttons_fit(flow):
                return False
            row_counts.append(len(_rows(flow)))
        return row_counts[0] > 1 and row_counts[1] == row_counts[-1] == 1 and row_counts[0] == row_counts[3]

    return await _measure(body, size=(60, 24), specs=MIXED_SPECS, breaks=())


async def _test_hidden_mixed_buttons_repack():
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        flow.styles.padding = (0, 1)
        await pilot.pause()
        before = len(_rows(flow))
        hidden = [flow.query_one(f"#{name}", compat.Button) for name in ("b1", "b3")]
        for button in hidden:
            button.display = False
        flow.relayout()
        await pilot.pause()
        visible = [button for button in flow.query(compat.Button) if button.display]
        compact = _visible_buttons_fit(flow) and len({button.region.y for button in visible}) == 1
        for button in hidden:
            button.display = True
        flow.relayout()
        await pilot.pause()
        return before > 1 and compact and _visible_buttons_fit(flow) and len(_rows(flow)) == before

    return await _measure(body, size=(60, 24), specs=MIXED_SPECS, breaks=())


async def _test_dynamic_mixed_labels_keep_controls_visible():
    async def body(app, page, pilot):
        flow = page.query_one("#flow", compat.ButtonFlow)
        original_buttons = list(flow.query(compat.Button))
        target = flow.query_one("#b0", compat.Button)
        for label in ("安装选中的模块", "更新所有已安装模块并同步数据库配置" * 4, "安装"):
            target.label = label
            flow.relayout()
            await pilot.pause()
            if not _visible_buttons_fit(flow) or list(flow.query(compat.Button)) != original_buttons:
                return False
        return len(_rows(flow)) == 1 and str(target.label) == "安装"

    return await _measure(body, size=(140, 30), specs=MIXED_SPECS, breaks=())


async def _test_navigation_still_reports_eleven_pages():

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
    await tester.test(_test_mixed_labels_fit_after_resize, "长短标签在窄宽往返缩放时无越界或重叠")
    await tester.test(_test_hidden_mixed_buttons_repack, "隐藏与恢复按钮后按可见按钮重排")
    await tester.test(_test_dynamic_mixed_labels_keep_controls_visible, "动态长标签与超宽标签不挤出控件")
    await tester.test(_test_navigation_still_reports_eleven_pages, "页面清单不变")

    return tester
