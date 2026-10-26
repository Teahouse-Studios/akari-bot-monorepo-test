"""文档页：列表与详情、搜索、多选、构建、预览与部署测试。

数据源使用静态替身，预览服务不产生子进程；浏览器调用与子进程无关，按调用参数断言。
"""

import asyncio
import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import PAGE_BLURB, PAGES, TuiApp
from akaribot.cli.tui.docs import (
    DocsPackageRow,
    DocsPageRow,
    DocsView,
    StaticDocsSource,
    ToolchainInfo,
)
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case

PREVIEW_URL = "http://127.0.0.1:43117/"
BUILD_AT = "2026-10-01T12:00:00Z"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _pages() -> tuple[DocsPackageRow, ...]:
    return (
        DocsPackageRow(
            key="core",
            group="cli",
            dist="akari-bot-core",
            version="0.1.0",
            title="核心",
            summary="运行时与公共设施",
            pages=(
                DocsPageRow(path="index.md", title="概览", order=0, description="入口"),
                DocsPageRow(path="api.md", title="API", order=10),
            ),
            doc_path="/tmp/docs/core",
            editable=True,
        ),
        DocsPackageRow(
            key="dice",
            group="module",
            dist="akari-bot-module-dice",
            version="0.2.0",
            title="骰子",
            summary="骰子模块",
            pages=(DocsPageRow(path="index.md", title="概览"),),
            doc_path="/tmp/docs/dice",
        ),
    )


def _view(*, ready: bool = True, build: dict | None = None) -> DocsView:
    return DocsView(
        packages=_pages(),
        toolchain=ToolchainInfo(
            node="/usr/bin/node",
            npm="/usr/bin/npm",
            node_version="v20.11.0",
            npm_version="10.2.4",
            ready=ready,
            detail="" if ready else "未找到 npm",
        ),
        config={"path": "/tmp/inst/docs.toml", "out_dir": "/tmp/inst/cache/docs/site"},
        build=build,
        deploys=({"at": "2026-10-02T08:00:00Z", "target": "vercel:demo", "status": "ok"},),
        warnings=("跳过 akari-bot-module-dice：缺少 index.md",),
    )


BUILT = {"generated_at": BUILD_AT, "packages": ["core"], "fingerprint": "abcdef123456"}


async def _wait_until(predicate, timeout: float = 1.5) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


async def _with_page(body, source=None, *, size=(120, 34)):
    chosen = source or StaticDocsSource(_view(build=BUILT), url=PREVIEW_URL)
    app = TuiApp(sources={"docs": chosen}, initial_page="docs", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("docs")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _test_page_registered_in_navigation():
    async def body(app, page, pilot, source):
        nav = app.query_one("#nav", compat.ListView)
        ids = [child.id for child in nav.children]
        await pilot.press("q")
        return app.active_page, "nav-docs" in ids

    active, listed = await _with_page(body)
    return (
        any(key == "docs" for key, _, _ in PAGES)
        and PAGE_BLURB.get("docs") == "cli.tui.nav.blurb.docs"
        and active == "docs"
        and listed
    )


async def _test_list_and_detail_show_package_fields():
    async def body(app, page, pilot, source):
        rows = page.row_texts()
        columns = page.column_text()
        detail = page.detail_text
        status = page.status_text
        await pilot.press("q")
        return rows, columns, detail, status

    rows, columns, detail, status = await _with_page(body)
    return (
        len(rows) == 2
        and "core" in rows[0]
        and "核心" in rows[0]
        and "0.1.0" in rows[0]
        and "cli" in rows[0]
        and i18n.t("cli.tui.docs.column_key") in columns
        and i18n.t("cli.tui.docs.field_dist") in detail
        and "akari-bot-core" in detail
        and "/tmp/docs/core" in detail
        and i18n.t("cli.tui.docs.version") in detail
        and "v20.11.0" in detail
        and "API" in detail
        and i18n.t("cli.tui.docs.status_loaded", count=2) == status
    )


async def _test_search_filters_and_escape_clears():
    async def body(app, page, pilot, source):
        page.set_query("dice")
        await pilot.pause()
        filtered = page.visible_packages
        rows = page.row_texts()
        page.query_one("#docs-list", compat.ListView).focus()
        await pilot.press("escape")
        await pilot.pause()
        cleared = page.visible_packages
        query = page.search_query
        await pilot.press("q")
        return filtered, rows, cleared, query

    filtered, rows, cleared, query = await _with_page(body)
    return (
        [package.key for package in filtered] == ["dice"]
        and len(rows) == 1
        and "dice" in rows[0]
        and [package.key for package in cleared] == ["core", "dice"]
        and query == ""
    )


async def _test_space_select_all_and_clear():
    async def body(app, page, pilot, source):
        await pilot.press("space")
        await pilot.pause()
        one = page.selected_keys
        await pilot.press("a")
        await pilot.pause()
        every = page.selected_keys
        marked_rows = [row for row in page.row_texts() if row.startswith("✓")]
        await pilot.press("c")
        await pilot.pause()
        none = page.selected_keys
        await pilot.press("q")
        return one, every, len(marked_rows), none

    one, every, marked, none = await _with_page(body)
    return one == ("core",) and every == ("core", "dice") and marked == 2 and none == ()


async def _test_build_passes_selected_keys_or_none():
    async def body(app, page, pilot, source):
        await pilot.press("space")
        await pilot.pause()
        await pilot.press("b")
        await page.wait_for_idle()
        await pilot.pause()
        first = list(source.build_keys)
        selected_status = page.status_text
        await pilot.press("c")
        await pilot.pause()
        await pilot.press("b")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return first, source.build_keys, selected_status, page.status_text

    first, calls, selected_status, all_status = await _with_page(body)
    return (
        first == [("core",)]
        and calls == [("core",), ()]
        and i18n.t("cli.tui.docs.build_done", count=1, duration=0) == selected_status
        and i18n.t("cli.tui.docs.build_done", count=2, duration=0) == all_status
    )


async def _test_preview_start_stop_and_open():
    async def body(app, page, pilot, source):
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        running = page.server_running
        status = page.status_text
        url = page.preview_url
        with mock.patch("akaribot.cli.tui.docs.webbrowser.open", return_value=True) as opener:
            await pilot.press("o")
            await pilot.pause()
            opened = list(opener.call_args_list)
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        stopped = page.server_running
        await pilot.press("q")
        return running, status, url, opened, stopped, source.calls

    running, status, url, opened, stopped, calls = await _with_page(body)
    return (
        running
        and status == i18n.t("cli.tui.docs.serve_ready", url=PREVIEW_URL)
        and url == PREVIEW_URL
        and [call.args for call in opened] == [(PREVIEW_URL,)]
        and not stopped
        and calls["serve"] == 1
        and calls["stop"] == 1
    )


async def _test_preview_requires_build_first():
    source = StaticDocsSource(_view(build=None), url=PREVIEW_URL)

    async def body(app, page, pilot, chosen):
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        blocked = (page.status_text, chosen.calls["serve"], page.server_running)
        await pilot.press("b")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        served = (page.status_text, chosen.calls["serve"], page.server_running)
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.press("q")
        return blocked, served

    blocked, served = await _with_page(body, source)
    return (
        blocked[0] == i18n.t("cli.tui.docs.need_build")
        and blocked[1] == 0
        and not blocked[2]
        and served[1] == 1
        and served[2]
        and PREVIEW_URL in served[0]
    )


async def _test_missing_toolchain_blocks_build_and_preview():
    source = StaticDocsSource(_view(ready=False, build=BUILT), url=PREVIEW_URL)

    async def body(app, page, pilot, chosen):
        await pilot.press("b")
        await page.wait_for_idle()
        await pilot.pause()
        build_status = page.status_text
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        serve_status = page.status_text
        await pilot.press("q")
        return build_status, serve_status, dict(chosen.calls)

    build_status, serve_status, calls = await _with_page(body, source)
    reason = i18n.t("cli.tui.docs.toolchain_missing", detail="未找到 npm")
    return build_status == reason and serve_status == reason and calls["build"] == 0 and calls["serve"] == 0


async def _test_deploy_modal_defaults_to_dry_run():
    async def body(app, page, pilot, source):
        await pilot.press("ctrl+p")
        await pilot.pause()
        screen = app.screen
        opened = type(screen).__name__
        labels = [str(screen.query_one(f"#choice-{index}", compat.Button).label) for index in range(2)]
        focused = getattr(app.focused, "id", "")
        screen.query_one("#choice-0", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        dry_calls = list(source.deploys)
        dry_status = page.status_text
        page.request_deploy()
        await _wait_until(lambda: bool(app.screen.query("#choice-1")))
        await pilot.pause()
        app.screen.query_one("#choice-1", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, labels, focused, dry_calls, dry_status, list(source.deploys), page.status_text

    opened, labels, focused, dry_calls, dry_status, deploys, real_status = await _with_page(body)
    return (
        opened == "ChoiceScreen"
        and labels == [i18n.t("cli.tui.docs.deploy_dry_run"), i18n.t("cli.tui.docs.deploy_real")]
        and focused == "choice-0"
        and dry_calls == [(None, True)]
        and dry_status == i18n.t("cli.docs.deploy.dry_run", uploaded=0, deleted=0, skipped=0)
        and deploys == [(None, True), (None, False)]
        and PREVIEW_URL in real_status
    )


async def _test_deploy_failure_keeps_page_usable():
    source = StaticDocsSource(
        _view(build=BUILT),
        deploy_result=OperationResult(False, i18n.t("cli.tui.docs.deploy_failed", detail="远端拒绝"), "boom"),
    )

    async def body(app, page, pilot, chosen):
        page.request_deploy()
        await _wait_until(lambda: bool(app.screen.query("#choice-0")))
        app.screen.query_one("#choice-0", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        page.request_deploy()
        await _wait_until(lambda: bool(app.screen.query("#choice-0")))
        reopened = bool(app.screen.query("#choice-0"))
        await pilot.press("escape")
        await pilot.press("q")
        return status, reopened, list(chosen.deploys)

    status, reopened, deploys = await _with_page(body, source)
    return "boom" in status and reopened and deploys == [(None, True)]


async def _test_leaving_page_stops_preview():
    async def body(app, page, pilot, source):
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        note = page.dirty_note()
        app.show_page("dashboard")
        stopped = await _wait_until(lambda: source.calls["stop"] >= 1)
        await pilot.pause()
        await pilot.press("q")
        return note, stopped, page.server_running, source.calls["stop"]

    note, stopped, running, stops = await _with_page(body)
    return note != "" and stopped and not running and stops >= 1


async def _test_reset_pending_reopens_modal():
    async def body(app, page, pilot, source):
        with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
            page._confirm.accept("deploy")
            page.request_deploy()
            await pilot.pause()
            blocked = len(app.screen_stack) == 1
            page.reset_pending()
            page.request_deploy()
        await _wait_until(lambda: bool(app.screen.query("#choice-0")))
        opened = bool(app.screen.query("#choice-0"))
        await pilot.press("escape")
        await pilot.press("q")
        return blocked, opened

    blocked, opened = await _with_page(body)
    return blocked and opened


async def _test_preview_start_failure_is_reported():
    source = StaticDocsSource(_view(build=BUILT), serve_error="端口被占用")

    async def body(app, page, pilot, chosen):
        await pilot.press("s")
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        running = page.server_running
        await pilot.press("q")
        return status, running

    status, running = await _with_page(body, source)
    return i18n.t("cli.tui.docs.serve_failed", detail="端口被占用") == status and not running


async def _test_footer_fits_eighty_columns():
    async def body(app, page, pilot, source):
        footer = app.query_one(compat.Footer)
        keys = [child for child in footer.children if getattr(child, "action", "")]
        inside = bool(keys) and all(footer.region.contains_region(child.region) for child in keys)
        descriptions = {getattr(child, "description", "") for child in keys}
        await pilot.press("q")
        return inside, descriptions

    inside, descriptions = await _with_page(body, size=(80, 24))
    return inside and {i18n.t("cli.tui.app.bind_quit"), i18n.t("cli.tui.app.bind_help")} <= descriptions


@func_case
async def test_tui_docs(tester: Tester):
    """cli.tui.docs: 文档包的列表、构建、预览与部署测试"""
    _use_cli_locale()
    await tester.test(_test_page_registered_in_navigation, "文档页注册进侧栏与页面清单")
    await tester.test(_test_list_and_detail_show_package_fields, "列表与详情展示包字段")
    await tester.test(_test_search_filters_and_escape_clears, "搜索过滤与 Esc 清空")
    await tester.test(_test_space_select_all_and_clear, "空格选择、全选与清空")
    await tester.test(_test_build_passes_selected_keys_or_none, "构建只传选中 key，无选中时构建全部")
    await tester.test(_test_preview_start_stop_and_open, "预览启停、URL 与浏览器打开")
    await tester.test(_test_preview_requires_build_first, "未构建时先提示构建")
    await tester.test(_test_missing_toolchain_blocks_build_and_preview, "Node 不可用时阻止构建与预览")
    await tester.test(_test_deploy_modal_defaults_to_dry_run, "部署模态默认试运行并区分真实部署")
    await tester.test(_test_deploy_failure_keeps_page_usable, "部署失败后界面仍可用")
    await tester.test(_test_leaving_page_stops_preview, "离开页面停止预览服务")
    await tester.test(_test_reset_pending_reopens_modal, "reset_pending 清除防抖状态")
    await tester.test(_test_preview_start_failure_is_reported, "预览启动失败写入状态栏")
    await tester.test(_test_footer_fits_eighty_columns, "80 列下页脚不溢出")
    return tester
