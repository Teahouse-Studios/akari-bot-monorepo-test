"""TUI 自检：逐页等待页面 worker、检查异常，并区分未执行的产品检查。

逐页切换在读取导航断言前先等该页空闲，页面 worker 异常与页面错误状态都记成失败；环境事实记警告
不影响退出码，产品检查未执行记 ``skip`` 并计入非零退出码。本文件用替身数据源固定这三条。
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
from akaribot.cli.tui.adapters import StaticAdapterSource
from akaribot.cli.tui.app import PAGES
from akaribot.cli.tui.config import StaticConfigSource
from akaribot.cli.tui.dashboard import StaticDashboardSource
from akaribot.cli.tui.database import StaticDatabaseSource
from akaribot.cli.tui.dev import StaticDevSource
from akaribot.cli.tui.doctor import StaticDoctorSource
from akaribot.cli.tui.environment import StaticEnvironmentSource
from akaribot.cli.tui.logs import StaticLogSource
from akaribot.cli.tui.misc import StaticMiscSource
from akaribot.cli.tui.modules import StaticModuleSource
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
    # 合并目录必须显式重建成快照：框架会在用例入口重连语言快照，只靠 _connect() 拿不到新键。
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
        self.calls: dict[str, int] = {}
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
    await tester.test(_test_report_separates_warning_from_skipped, "环境警告不影响退出码、产品检查未执行则非零")
    await tester.test(_test_unreadable_resources_are_not_run, "资源枚举不到时记未执行而非警告")
    return tester
