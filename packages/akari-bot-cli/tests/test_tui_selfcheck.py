"""TUI 自检与无头冒烟：逐页等待页面 worker、检查异常，并区分未执行的产品检查。

逐页切换在读取导航断言前先等该页空闲，页面 worker 异常与页面错误状态都记成失败；环境事实记警告
不影响退出码，产品检查未执行记 ``skip`` 并计入非零退出码。无头冒烟分默认首屏与模块页两段：首屏
要求停在概览页且三个关键控件已挂载，模块页要求数据源实际取数，任一段失败即非零退出码。
"""

import asyncio
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli.commands import tui as tui_cmd
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import app as tui_app_module
from akaribot.cli.tui.adapters import StaticAdapterSource
from akaribot.cli.tui.app import PAGES, TuiApp
from akaribot.cli.tui.config import StaticConfigSource
from akaribot.cli.tui.dashboard import (
    StaticDashboardSource,
    StaticInstanceListSource,
    StaticServiceControl,
    StaticSetupSummarySource,
)
from akaribot.cli.tui.database import StaticDatabaseSource
from akaribot.cli.tui.dev import StaticDevSource
from akaribot.cli.tui.doctor import StaticDoctorSource
from akaribot.cli.tui.environment import StaticEnvironmentSource
from akaribot.cli.tui.logs import StaticLogSource
from akaribot.cli.tui.misc import StaticMiscSource
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.cli.tui.run import StaticRunSource
from akaribot.testing import Tester, func_case

INJECTED_ERROR = "注入的取数异常"
# 杂项页没有预取，替身不会被调用，不参与「取数发生过」的断言。
NO_PREFETCH = ("misc",)
# 模块页在挂载时就取过一次数，那次早于逐页循环，不参与串行断言。
PRELOADED = ("modules",)
FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "tui_selfcheck.json"
_KEEP_ALIVE: list[tempfile.TemporaryDirectory] = []


def _merged_locale_dir() -> Path:
    # 片段里的新键尚未并入 locales：合成一份合并后的语言目录，断言才取到真实渲染结果。
    holder = tempfile.TemporaryDirectory(prefix="akari-selfcheck-locale-")
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
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [str(_merged_locale_dir())], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _static_sources() -> dict:
    return {
        "dashboard": StaticDashboardSource(),
        "environment": StaticEnvironmentSource(),
        "database": StaticDatabaseSource(),
        "modules": StaticModuleSource([]),
        "adapters": StaticAdapterSource(),
        "config": StaticConfigSource(),
        "logs": StaticLogSource(),
        "run": StaticRunSource(),
        "dev": StaticDevSource(),
        "doctor": StaticDoctorSource(),
        "misc": StaticMiscSource(),
    }


class _Counting:
    # 取数返回后才计数：计数非空即说明该页的取数确实跑完过，没等空闲就读断言会拿到空计数。
    def __init__(self, inner, delay: float = 0.05) -> None:
        self._inner = inner
        self._delay = delay
        # 数据源自带的计数沿用同一个字典：生产键名是 list，替身另起的键名会让计数断言落空。
        counts = getattr(inner, "calls", None)
        self.calls: dict[str, int] = counts if isinstance(counts, dict) else {}
        self.first: tuple[float, float] | None = None

    def __getattr__(self, name: str):
        attribute = getattr(self._inner, name)
        if not callable(attribute):
            return attribute

        def _record(*args, **kwargs):
            started = time.monotonic()
            result = attribute(*args, **kwargs)
            time.sleep(self._delay)
            self.calls[name] = self.calls.get(name, 0) + 1
            if self.first is None:
                self.first = (started, time.monotonic())
            return result

        return _record


class _FailingDashboardSource(StaticDashboardSource):
    def snapshot(self):
        raise RuntimeError(INJECTED_ERROR)


class _FakeWorker:
    def __init__(self, error) -> None:
        self.error = error


class _FakePage:
    def __init__(self, *, workers=(), last_error: str = "", raises=None) -> None:
        self.app = SimpleNamespace(workers=list(workers))
        self.last_error = last_error
        self._raises = raises

    async def wait_for_idle(self) -> None:
        if self._raises is not None:
            raise self._raises


class _FakePilot:
    async def pause(self) -> None:
        return None


class _StubApp:
    # 只提供冒烟断言读到的属性：控件查询、当前页、焦点与数据源计数各自可控。
    def __init__(
        self,
        selectors=(),
        *,
        active_page: str = "dashboard",
        focused: bool = True,
        calls: int = 1,
    ) -> None:
        self._selectors = tuple(selectors)
        self.active_page = active_page
        self.focused = object() if focused else None
        self.module_source = SimpleNamespace(calls={"list": calls})

    def query_one(self, selector: str) -> object:
        if selector in self._selectors:
            return SimpleNamespace()
        raise LookupError(selector)


class _FakeApp:
    # 记录构造参数：第二段冒烟必须显式启动到模块页并带上模块数据源。
    def __init__(self, *args: object, **kwargs: object) -> None:
        self.args = args
        self.kwargs = dict(kwargs)
        self.active_page = str(kwargs.get("initial_page", "dashboard"))
        self.startup_ms = 0.0
        self.first_paint_ms = 0.0
        self.module_source = SimpleNamespace(calls={"list": 1})


MODULE_RECORDS = (
    ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed"),
)


def _first_screen_sources() -> dict:
    # 首次使用摘要的替身必须显式注入：生产实现要起体检子进程，用例不得真的起进程。
    sources = _static_sources()
    sources["dashboard_instances"] = StaticInstanceListSource()
    sources["dashboard_service"] = StaticServiceControl()
    sources["dashboard_setup"] = StaticSetupSummarySource()
    return sources


STYLESHEET_INFO = {"origin": "inline:test", "lines": 1, "sha256": "0" * 8, "bytes": 0}


def _run_headless_with_segments(first: str, modules: tuple[str, int]) -> tuple[int, list[str], list[_FakeApp]]:
    built: list[_FakeApp] = []
    lines: list[str] = []

    def build(*args: object, **kwargs: object) -> _FakeApp:
        app = _FakeApp(*args, **kwargs)
        built.append(app)
        return app

    def collect(message: object = "", **kwargs: object) -> None:
        lines.append(str(message))

    with (
        patch.object(tui_app_module, "TuiApp", build),
        patch.object(tui_app_module, "stylesheet_summary", lambda: dict(STYLESHEET_INFO)),
        # 冻结时钟：总耗时与启动耗时都成了定值，三行输出可以逐字比对。
        patch.object(tui_cmd, "time", SimpleNamespace(monotonic=lambda: 1000.0)),
        patch.object(tui_cmd, "_smoke_first_screen", lambda app: first),
        patch.object(tui_cmd, "_smoke_modules", lambda app: modules),
        patch.object(tui_cmd.typer, "echo", side_effect=collect),
    ):
        return tui_cmd.run_headless(), lines, built


async def _navigate(**kwargs) -> tui_cmd.CheckResult:
    # 自检内部用 asyncio.run()，而用例跑在事件循环里，故放回无循环的线程执行。
    return await asyncio.to_thread(tui_cmd._check_page_navigation, **kwargs)


async def _test_navigation_passes_with_static_sources():
    result = await _navigate(sources=_static_sources())
    return result.level == tui_cmd.LEVEL_OK and str(len(PAGES)) in result.detail


async def _test_navigation_reports_page_source_failure():
    sources = _static_sources()
    sources["dashboard"] = _FailingDashboardSource()
    result = await _navigate(sources=sources)
    return (
        result.level == tui_cmd.LEVEL_FAIL
        and INJECTED_ERROR in result.detail
        and i18n.t("cli.tui.nav.dashboard") in result.detail
    )


async def _test_navigation_waits_for_each_page_load():
    counted = {key: _Counting(source) for key, source in _static_sources().items()}
    result = await _navigate(sources=counted)
    loaded = {key: sum(source.calls.values()) for key, source in counted.items() if key not in NO_PREFETCH}
    # 逐页串行：上一页取数结束后才开始下一页，说明每次切换都等到了页面空闲。
    order = [key for key, _, _ in PAGES if key not in NO_PREFETCH and key not in PRELOADED]
    serial = all(
        counted[order[index]].first[1] <= counted[order[index + 1]].first[0] for index in range(len(order) - 1)
    )
    return result.level == tui_cmd.LEVEL_OK and all(loaded.values()) and serial


async def _test_page_failure_reads_worker_error():
    worker_error = _FakeWorker(RuntimeError("worker 取数失败"))
    observed = (
        await tui_cmd._page_failure(_FakePage(workers=[worker_error]), _FakePilot()),
        await tui_cmd._page_failure(_FakePage(raises=ValueError("页面未挂载")), _FakePilot()),
        await tui_cmd._page_failure(_FakePage(last_error="RuntimeError: 页面自报错误"), _FakePilot()),
        await tui_cmd._page_failure(_FakePage(), _FakePilot()),
    )
    return observed == (
        "RuntimeError: worker 取数失败",
        "ValueError: 页面未挂载",
        "RuntimeError: 页面自报错误",
        "",
    )


async def _test_headless_first_screen_mounts_default_page():
    app_instance = TuiApp(sources=_first_screen_sources(), boot_started_at=time.monotonic())
    async with compat.app_test(app_instance, size=(80, 24)) as pilot:
        page = app_instance.page(tui_cmd.DASHBOARD_PAGE)
        failure = await tui_cmd._first_screen_failure(app_instance, page, pilot)
        missing = tui_cmd._missing_widgets(app_instance, tui_cmd.FIRST_SCREEN_WIDGETS)
        focused = app_instance.focused is not None
        await pilot.press("q")
    return failure == "" and app_instance.active_page == tui_cmd.DASHBOARD_PAGE and missing == [] and focused


async def _test_headless_first_screen_requires_widgets():
    complete = _StubApp(tui_cmd.FIRST_SCREEN_WIDGETS)
    incomplete = _StubApp(tui_cmd.FIRST_SCREEN_WIDGETS[:-1])
    passed = await tui_cmd._first_screen_failure(complete, _FakePage(), _FakePilot())
    missing = await tui_cmd._first_screen_failure(incomplete, _FakePage(), _FakePilot())
    unfocused = await tui_cmd._first_screen_failure(
        _StubApp(tui_cmd.FIRST_SCREEN_WIDGETS, focused=False), _FakePage(), _FakePilot()
    )
    return (
        passed == ""
        and tui_cmd._missing_widgets(incomplete, tui_cmd.FIRST_SCREEN_WIDGETS) == ["#fields"]
        and missing == i18n.t("cli.tui_cmd.headless_first_widgets_bad", missing="#fields")
        and unfocused == i18n.t("cli.tui_cmd.headless_first_focus_bad")
    )


async def _test_headless_modules_smoke_requires_fetch():
    source = _Counting(StaticModuleSource(list(MODULE_RECORDS)))
    app_instance = TuiApp(source=source, initial_page=tui_cmd.MODULES_PAGE, boot_started_at=time.monotonic())
    async with compat.app_test(app_instance, size=(80, 24)) as pilot:
        page = app_instance.modules_page()
        failure = await tui_cmd._modules_failure(app_instance, page, pilot)
        rows = len(page.visible_records)
        await pilot.press("q")
    # 未取数的数据源必须判失败：计数停在 0 时冒烟不得报成功。
    uncalled = await tui_cmd._modules_failure(
        _StubApp(active_page=tui_cmd.MODULES_PAGE, calls=0), _FakePage(), _FakePilot()
    )
    return (
        failure == ""
        and source.calls.get("list", 0) >= 1
        and rows == len(MODULE_RECORDS)
        and uncalled == i18n.t("cli.tui_cmd.headless_modules_uncalled", calls=0)
    )


def _headless_exit_code_checks() -> bool:
    widgets = i18n.t("cli.common.list_separator").join(tui_cmd.FIRST_SCREEN_WIDGETS)
    # 三行输出各自对应一个键：首行只讲概览页，模块页那行才是取数结果。
    first = i18n.t("cli.tui_cmd.headless_first_ok", page=tui_cmd.DASHBOARD_PAGE, widgets=widgets)
    modules = i18n.t("cli.tui_cmd.headless_modules_ok", rows=2, calls=1)
    summary = i18n.t(
        "cli.tui_cmd.headless_summary",
        origin=STYLESHEET_INFO["origin"],
        lines=STYLESHEET_INFO["lines"],
        sha256=STYLESHEET_INFO["sha256"],
        startup="0",
        first_paint="0",
        ms="0",
    )
    ok_code, ok_lines, ok_apps = _run_headless_with_segments("", ("", 2))
    empty_code, empty_lines, _ = _run_headless_with_segments("", ("", 0))
    first_code, first_lines, _ = _run_headless_with_segments("概览页缺关键控件：#fields", ("", 2))
    modules_code, modules_lines, _ = _run_headless_with_segments("", ("模块页未取数", 0))
    copy = json.loads(FRAGMENT.read_text(encoding="utf-8"))
    return (
        ok_code == 0
        # 第一段不覆盖 initial_page；第二段显式带数据源启动到模块页。
        and ok_apps[0].kwargs.get("initial_page") is None
        and ok_apps[1].kwargs.get("initial_page") == tui_cmd.MODULES_PAGE
        and ok_apps[1].kwargs.get("source") is not None
        and ok_lines[0] == first
        and ok_lines[0] != modules
        and ok_lines[1] == modules
        and ok_lines[2] == summary
        # 0 行同样是通过：文案要写明数据源已经取过数。
        and empty_code == 0
        and empty_lines[1] == i18n.t("cli.tui_cmd.headless_modules_empty", calls=1)
        and first_code == 1
        and any("概览页缺关键控件" in line for line in first_lines)
        and modules_code == 1
        and any("模块页未取数" in line for line in modules_lines)
        # 片段是这批新文案的真源：首屏那句必须点明概览页，模块那句必须点明模块页。
        and "概览页" in copy["cli.tui_cmd.headless_first_ok"]
        and "模块页" in copy["cli.tui_cmd.headless_modules_ok"]
    )


async def _test_headless_exit_code_covers_both_segments():
    # 两段冒烟在此被替身替换，run_headless 不再起事件循环，故直接在用例循环里跑。
    return _headless_exit_code_checks()


def _report(results: list[tui_cmd.CheckResult]) -> tuple[int, list[tuple[str, object]]]:
    with patch.object(tui_cmd.typer, "echo") as echo:
        code = tui_cmd._report_self_check(results)
    return code, [(str(call.args[0]), call.kwargs.get("file")) for call in echo.call_args_list]


def _test_report_separates_warning_from_skipped():
    warn_only = [tui_cmd.CheckResult(tui_cmd.LEVEL_WARN, "交互终端", "stdin.isatty=False")]
    skipped = [
        tui_cmd.CheckResult(tui_cmd.LEVEL_OK, "样式表解析", "Textual 解析通过"),
        tui_cmd.CheckResult(tui_cmd.LEVEL_SKIP, "包内资源枚举", "未枚举到可读资源"),
        tui_cmd.CheckResult(tui_cmd.LEVEL_WARN, "tmux", "不在 tmux 内"),
    ]
    failed = [tui_cmd.CheckResult(tui_cmd.LEVEL_FAIL, "品牌主题", "主题未生效")]
    warn_code, warn_lines = _report(warn_only)
    skip_code, skip_lines = _report(skipped)
    fail_code, fail_lines = _report(failed)
    return (
        warn_code == 0
        and all(line[1] in (None, sys.stdout) for line in warn_lines)
        and skip_code == 1
        and skip_lines[1][0].startswith("[skip]")
        and skip_lines[1][1] is sys.stderr
        and i18n.t("cli.tui_cmd.self_check_blocked", failures=0, skipped=1, warnings=1) in skip_lines[-1][0]
        and fail_code == 1
        and i18n.t("cli.tui_cmd.self_check_failed", failures=1, warnings=0) in fail_lines[-1][0]
    )


def _test_unreadable_resources_are_not_run():
    with patch.object(compat, "resource_inventory", lambda package: []):
        results = tui_cmd._check_resources()
    skipped, stylesheet = results[0], results[1]
    return (
        skipped.level == tui_cmd.LEVEL_SKIP
        and skipped.detail == i18n.t("cli.tui_cmd.check_resources_missing", package="akaribot.cli.tui")
        and stylesheet.level == tui_cmd.LEVEL_WARN
    )


@func_case
async def test_tui_selfcheck(tester: Tester):
    """cli.tui 自检: 逐页 worker 等待与异常、未执行的产品检查"""
    _use_cli_locale()
    await tester.test(_test_navigation_passes_with_static_sources, "逐页切换等待取数后仍通过")
    await tester.test(_test_navigation_reports_page_source_failure, "页面数据源抛异常时导航检查失败")
    await tester.test(_test_navigation_waits_for_each_page_load, "逐页切换串行等到每页取数完成")
    await tester.test(_test_page_failure_reads_worker_error, "页面异常取 worker 错误、等待异常与页面错误状态")
    await tester.test(_test_headless_first_screen_mounts_default_page, "无头冒烟默认首屏停在概览页且三个关键控件已挂载")
    await tester.test(_test_headless_first_screen_requires_widgets, "首屏缺关键控件或焦点为空即判失败")
    await tester.test(_test_headless_modules_smoke_requires_fetch, "模块页冒烟要求数据源实际取数")
    await tester.test(_test_headless_exit_code_covers_both_segments, "无头冒烟任一段失败即非零退出码")
    await tester.test(_test_report_separates_warning_from_skipped, "环境警告不影响退出码、产品检查未执行则非零")
    await tester.test(_test_unreadable_resources_are_not_run, "资源枚举不到时记未执行而非警告")
    return tester
