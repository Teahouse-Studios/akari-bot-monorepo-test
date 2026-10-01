"""交互界面。

``akaribot tui`` 默认进入交互界面；``--self-check`` 用于在冻结产物里验证包内资源与样式表
能否加载（T6.5(a)），``--headless`` 用于没有终端的环境做一次启动冒烟。

Textual 及其应用模块一律在函数内延迟导入：``akaribot --help`` 等普通命令不应为一个
用不到的界面付出导入开销。
"""

from __future__ import annotations

import asyncio
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer

from akaribot.cli import i18n

app = typer.Typer(
    help=i18n.t("cli.tui_cmd.help"),
    no_args_is_help=False,
)

LEVEL_OK = "ok"
LEVEL_WARN = "warn"
LEVEL_SKIP = "skip"
LEVEL_FAIL = "fail"

# 未执行与失败都要退出非零：环境能力不足导致产品检查没跑成的路径，不能用「通过」掩盖。
BLOCKING_LEVELS = (LEVEL_SKIP, LEVEL_FAIL)


@dataclass(frozen=True)
class CheckResult:
    """一条自检结论。

    :param level: ``ok`` / ``warn`` / ``skip`` / ``fail``；``warn`` 只报环境事实，``skip`` 表示产品检查未执行。
    :param name: 检查项名称。
    :param detail: 实测结果说明。
    """

    level: str
    name: str
    detail: str

    def render(self) -> str:
        """返回单行输出文本。"""
        return i18n.t("cli.tui_cmd.result_line", level=f"{self.level:>4}", name=self.name, detail=self.detail)


@app.callback(invoke_without_command=True)
def tui(
    self_check: bool = typer.Option(False, "--self-check", help=i18n.t("cli.tui_cmd.option_self_check")),
    headless: bool = typer.Option(False, "--headless", help=i18n.t("cli.tui_cmd.option_headless")),
    no_mouse: bool = typer.Option(False, "--no-mouse", help=i18n.t("cli.tui_cmd.option_no_mouse")),
) -> None:
    """启动 AkariBot 交互界面。"""
    if self_check:
        raise typer.Exit(code=run_self_check())
    if headless:
        raise typer.Exit(code=run_headless(mouse=not no_mouse))
    run_interactive(mouse=not no_mouse)


def run_interactive(*, mouse: bool = True) -> None:
    """在当前终端启动交互界面，退出后打印耗时摘要。

    :param mouse: 是否请求鼠标追踪。
    """
    from akaribot.cli.tui import _compat as compat

    if not compat.is_interactive_terminal():
        typer.echo(i18n.t("cli.tui_cmd.not_terminal"), err=True)
        raise typer.Exit(code=2)

    from akaribot.cli.tui.app import run_tui

    result = run_tui(mouse=mouse, boot_note=register_active())
    typer.echo(result.summary(), err=True)
    raise typer.Exit(code=result.exit_code)


def register_active() -> str:
    """登记本次界面要管的实例，返回给界面报出的结论文案。

    站在实例目录里则登记它；站在实例之外（例如源码仓库根）而下级目录里恰好有一个实例时，登记并
    切换过去——「项目路径下的那个实例」正是用户要管的对象。下级有多个实例时不猜，只把候选报出来。

    :return: 提示文案；无需登记也无需切换时为空串。
    """
    from akaribot.cli.instance import resolve_instance_root
    from akaribot.cli.instances import InstanceRegistry, child_instances, register_existing
    from akaribot.cli.tui import context

    root = resolve_instance_root()
    adopted = False
    if root is None:
        found = child_instances(Path.cwd(), limit=None)
        if len(found) > 1:
            listing = i18n.t("cli.common.list_separator").join(str(path) for path in found)
            return i18n.t("cli.tui_cmd.discover_ambiguous", count=len(found), found=listing)
        if not found:
            return ""
        root = found[0]
        adopted = True
    # 自动登记失败不该挡住界面：注册表写不进去时照常进入，把原因交给通知。
    try:
        entry = register_existing(root)
    except Exception as error:  # noqa: BLE001
        return i18n.t("cli.tui_cmd.register_auto_failed", error=f"{type(error).__name__}: {error}")
    if adopted:
        context.set_active_root(root)
        # register_existing 只在确实新登记时给记录，已在注册表里的要自己取回来才有名字可显示。
        known = entry if entry is not None else InstanceRegistry().find_by_root(root)
        name = known.name if known is not None else str(root)
        return i18n.t("cli.tui_cmd.discover_done", name=name, root=root, parent=Path.cwd())
    if entry is None:
        return ""
    return i18n.t("cli.tui.dashboard.register_auto", name=entry.name, root=entry.root)


def run_headless(*, mouse: bool = False) -> int:
    """无头启动一次界面并立即退出，返回进程退出码。

    :param mouse: 是否请求鼠标追踪，无头模式下无实际作用，保留以便与交互路径参数对齐。
    :return: 0 表示启动与退出均成功。
    """
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp, stylesheet_summary

    del mouse
    started = time.monotonic()
    app_instance = TuiApp(boot_started_at=started)

    async def smoke() -> int:
        async with compat.app_test(app_instance, size=(80, 24)) as pilot:
            page = app_instance.modules_page()
            await page.wait_for_idle()
            await pilot.pause()
            rows = len(page.visible_records)
            await pilot.press("q")
            return rows

    try:
        rows = asyncio.run(smoke())
    except Exception as error:  # noqa: BLE001 - 冒烟失败必须转成非零退出码
        typer.echo(i18n.t("cli.tui_cmd.headless_failed", error=f"{type(error).__name__}: {error}"), err=True)
        return 1
    elapsed_ms = (time.monotonic() - started) * 1000.0
    sheet = stylesheet_summary()
    typer.echo(
        i18n.t(
            "cli.tui_cmd.headless_ok",
            rows=rows,
            ms=f"{elapsed_ms:.0f}",
            origin=sheet["origin"],
            lines=sheet["lines"],
            sha256=sheet["sha256"],
        )
    )
    typer.echo(
        i18n.t(
            "cli.tui_cmd.headless_timing",
            startup=f"{app_instance.startup_ms:.0f}",
            first_paint=f"{app_instance.first_paint_ms:.0f}",
            calls=_source_calls(app_instance),
        )
    )
    return 0


def _source_calls(app_instance: object) -> int:
    source = getattr(app_instance, "module_source", None)
    calls = getattr(source, "calls", None)
    if isinstance(calls, dict):
        return int(calls.get("list", 0))
    return -1


def run_self_check() -> int:
    """执行自检并返回进程退出码，非零表示存在硬失败或未执行的产品检查。

    :return: 0 表示全部硬性检查通过；1 表示存在 ``fail`` 项或 ``skip`` 项。
    """
    results: list[CheckResult] = []
    results.extend(_check_environment())
    results.extend(_check_stylesheet())
    results.extend(_check_resources())
    results.extend(_check_width())
    results.append(_check_boot())
    results.append(_check_available_and_progress())
    results.append(_check_page_navigation())
    results.append(_check_multi_select())
    results.append(_check_adapter_install())
    results.append(_check_theme())
    return _report_self_check(results)


def _report_self_check(results: list[CheckResult]) -> int:
    for result in results:
        stream = sys.stderr if result.level in BLOCKING_LEVELS else sys.stdout
        typer.echo(result.render(), file=stream)
    failures = [result for result in results if result.level == LEVEL_FAIL]
    skipped = [result for result in results if result.level == LEVEL_SKIP]
    warnings = [result for result in results if result.level == LEVEL_WARN]
    if skipped:
        typer.echo(
            i18n.t(
                "cli.tui_cmd.self_check_blocked",
                failures=len(failures),
                skipped=len(skipped),
                warnings=len(warnings),
            ),
            err=True,
        )
        return 1
    if failures:
        typer.echo(i18n.t("cli.tui_cmd.self_check_failed", failures=len(failures), warnings=len(warnings)), err=True)
        return 1
    typer.echo(i18n.t("cli.tui_cmd.self_check_ok", passed=len(results) - len(warnings), warnings=len(warnings)))
    return 0


def _check_multi_select() -> CheckResult:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

    records = [
        ModuleRecord(name="alpha", dist="akari-bot-module-alpha", version="1.0.0", state="installed"),
        ModuleRecord(name="bravo", dist="akari-bot-module-bravo", version="0.9.0", state="available"),
        ModuleRecord(name="charlie", dist="akari-bot-module-charlie", version="0.9.0", state="available"),
    ]
    source = StaticModuleSource(
        records=records, available=records, stream_lines=["Resolved 1 package", "Installed 1 package"]
    )
    app_instance = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())

    async def probe() -> tuple[int, int, list[str]]:
        async with compat.app_test(app_instance, size=(100, 30)) as pilot:
            page = app_instance.modules_page()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("space")
            await pilot.pause()
            await pilot.press("shift+down")
            await pilot.pause()
            await pilot.press("shift+down")
            await pilot.pause()
            selected = len(page._selected)
            page.request_install()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return selected, len(page.visible_records), list(source.installed)

    try:
        selected, total, installed = asyncio.run(probe())
    except Exception as error:  # noqa: BLE001 - 自检失败需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_multi_select"), f"{type(error).__name__}: {error}")
    if selected != 3 or installed != ["akari-bot-module-bravo", "akari-bot-module-charlie"]:
        return CheckResult(
            LEVEL_FAIL,
            i18n.t("cli.tui_cmd.check_multi_select"),
            i18n.t(
                "cli.tui_cmd.check_multi_select_bad",
                selected=selected,
                total=total,
                installed=i18n.t("cli.common.list_separator").join(installed) or "-",
            ),
        )
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_multi_select"),
        i18n.t("cli.tui_cmd.check_multi_select_detail", total=total, installed=len(installed)),
    )


def _check_page_navigation(sources: dict[str, Any] | None = None) -> CheckResult:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import PAGES, TuiApp, _nav_position
    from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

    source = StaticModuleSource(
        [ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed")]
    )
    app_instance = TuiApp(source=source, sources=sources, initial_page="modules", boot_started_at=time.monotonic())

    async def probe() -> tuple[list[str], list[str], list[str]]:
        mismatched: list[str] = []
        unfocused: list[str] = []
        broken: list[str] = []
        async with compat.app_test(app_instance, size=(100, 30)) as pilot:
            await pilot.pause()
            for key, title_key, _ in PAGES:
                app_instance.show_page(key)
                await pilot.pause()
                failure = await _page_failure(app_instance.page(key), pilot)
                if failure:
                    broken.append(f"{i18n.t(title_key)}：{failure}")
                nav = app_instance.query_one("#nav", compat.ListView)
                visible = app_instance.query_one(f"#page-{key}").display
                # 侧栏混排了分组标题，高亮下标要按 app 自己的折算读，不能直接用 PAGES 下标。
                if (
                    app_instance.active_page != key
                    or compat.highlighted_index(nav) != _nav_position(key)
                    or not visible
                ):
                    mismatched.append(key)
                if app_instance.focused is None:
                    unfocused.append(key)
            await pilot.press("q")
        return mismatched, unfocused, broken

    try:
        mismatched, unfocused, broken = asyncio.run(probe())
    except Exception as error:  # noqa: BLE001 - 自检失败需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_navigation"), f"{type(error).__name__}: {error}")
    problems: list[str] = []
    if mismatched or unfocused:
        problems.append(
            i18n.t(
                "cli.tui_cmd.check_navigation_bad",
                count=len(PAGES),
                mismatched=i18n.t("cli.common.list_separator").join(mismatched) or "-",
                unfocused=i18n.t("cli.common.list_separator").join(unfocused) or "-",
            )
        )
    if broken:
        problems.append(i18n.t("cli.common.list_separator").join(broken))
    if problems:
        return CheckResult(
            LEVEL_FAIL,
            i18n.t("cli.tui_cmd.check_navigation"),
            i18n.t("cli.tui.common.error_separator").join(problems),
        )
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_navigation"),
        i18n.t("cli.tui_cmd.check_navigation_detail", count=len(PAGES)),
    )


async def _page_failure(page: Any, pilot: Any) -> str:
    # worker 一完成即从 app.workers 移除，故先取句柄再等；错误状态在句柄上仍可读。
    workers = list(page.app.workers)
    failure = ""
    try:
        await page.wait_for_idle()
    except Exception as error:  # noqa: BLE001 - 自检要把异常原文带进结论
        failure = f"{type(error).__name__}: {error}"
    await pilot.pause()
    if not failure:
        for worker in workers:
            if worker.error is not None:
                failure = f"{type(worker.error).__name__}: {worker.error}"
                break
    if not failure:
        failure = str(getattr(page, "last_error", ""))
    # 页面错误常带子进程输出的多行尾巴，压成单行才不破坏一条结论一行的格式。
    return " ".join(failure.split())


def _check_available_and_progress() -> CheckResult:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

    installed = ModuleRecord(
        name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed"
    )
    candidate = ModuleRecord(
        name="wiki", dist="akari-bot-module-wiki", version="0.2.0", summary="维基", state="available"
    )
    source = StaticModuleSource(
        records=[installed],
        available=[installed, candidate],
        stream_lines=["Resolved 2 packages", "Installed 2 packages"],
    )
    app_instance = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())

    async def probe() -> tuple[int, int, tuple[str, ...], str]:
        async with compat.app_test(app_instance, size=(100, 30)) as pilot:
            page = app_instance.modules_page()
            await page.wait_for_idle()
            await pilot.pause()
            # 默认列全部：已装的 dice 与未装的 wiki 同时在列。
            before = len(page.visible_records)
            list_view = page.query_one("#module-list", compat.ListView)
            list_view.index = next(index for index, record in enumerate(page.visible_records) if not record.installed)
            await pilot.pause()
            page.request_install()
            await page.wait_for_idle()
            await pilot.pause()
            lines = page.stream_lines
            status = page.status_text
            page.query_one("#installed-only", compat.Checkbox).value = True
            await page.wait_for_idle()
            await pilot.pause()
            after = len(page.visible_records)
            await pilot.press("q")
            return before, after, lines, status

    try:
        before, after, lines, status = asyncio.run(probe())
    except Exception as error:  # noqa: BLE001 - 自检失败需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_available"), f"{type(error).__name__}: {error}")
    if after >= before or len(lines) < 2:
        return CheckResult(
            LEVEL_FAIL,
            i18n.t("cli.tui_cmd.check_available"),
            i18n.t("cli.tui_cmd.check_available_bad", before=before, after=after, lines=len(lines)),
        )
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_available"),
        i18n.t(
            "cli.tui_cmd.check_available_detail",
            before=before,
            after=after,
            lines=len(lines),
            last=lines[-1],
            status=status,
        ),
    )


def _check_theme() -> CheckResult:
    from akaribot.cli.tui import _compat as compat

    try:
        app_instance = compat.App()
        compat.install_akari_themes(app_instance)
        variables = app_instance.get_css_variables()
    except Exception as error:  # noqa: BLE001 - 自检失败需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_theme"), f"{type(error).__name__}: {error}")
    primary = str(variables.get("primary", "")).lower()
    expected = compat.AKARI_DARK_PALETTE["primary"].lower()
    if app_instance.theme != compat.AKARI_THEME_DARK or primary != expected:
        return CheckResult(
            LEVEL_FAIL,
            i18n.t("cli.tui_cmd.check_theme"),
            i18n.t("cli.tui_cmd.check_theme_bad", name=app_instance.theme, primary=primary),
        )
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_theme"),
        i18n.t("cli.tui_cmd.check_theme_detail", name=app_instance.theme, primary=primary),
    )


def _check_adapter_install() -> CheckResult:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.adapters import AdapterRecord, AdapterSnapshot, StaticAdapterSource
    from akaribot.cli.tui.app import TuiApp

    installed = AdapterRecord(
        platform="telegram",
        client_name="Telegram",
        table="bot_telegram",
        enable=True,
        enabled=True,
        installed=True,
    )
    source = StaticAdapterSource(
        snapshot=AdapterSnapshot(instances=(installed,), instance_root="/tmp/inst"),
        available=(
            AdapterRecord(platform="discord", installed=False),
            AdapterRecord(platform="telegram", installed=True),
        ),
        install_lines=["Resolved 1 package", "Installed 1 package"],
    )
    app_instance = TuiApp(sources={"adapters": source}, initial_page="adapters", boot_started_at=time.monotonic())

    async def probe() -> tuple[list[str], str, list[str]]:
        async with compat.app_test(app_instance, size=(120, 34)) as pilot:
            page = app_instance.page("adapters")
            await page.wait_for_idle()
            await pilot.pause()
            order = page._records_in_row_order()
            rows = [index for index, kind in enumerate(page._row_kinds) if kind == "instance"]
            page.query_one("#adapter-list", compat.ListView).index = rows[
                next(index for index, record in enumerate(order) if record.platform == "discord")
            ]
            await pilot.pause()
            label = str(page.query_one("#toggle", compat.Button).label)
            await pilot.press("i")
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return [record.platform for record in order], label, list(source.installed)

    try:
        platforms, label, installed_now = asyncio.run(probe())
    except Exception as error:  # noqa: BLE001 - 自检失败需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_adapter_install"), f"{type(error).__name__}: {error}")
    if platforms != ["discord", "telegram"] or installed_now != ["discord"]:
        return CheckResult(
            LEVEL_FAIL,
            i18n.t("cli.tui_cmd.check_adapter_install"),
            i18n.t(
                "cli.tui_cmd.check_adapter_install_bad",
                platforms=i18n.t("cli.common.list_separator").join(platforms) or "-",
                label=label,
                installed=i18n.t("cli.common.list_separator").join(installed_now) or "-",
            ),
        )
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_adapter_install"),
        i18n.t("cli.tui_cmd.check_adapter_install_detail", count=len(platforms), installed=len(installed_now)),
    )


def _check_environment() -> list[CheckResult]:
    from akaribot.cli.tui import _compat as compat

    results: list[CheckResult] = []
    pinned, message = compat.check_textual_version()
    name = i18n.t("cli.tui_cmd.check_textual_version")
    # compat 给的消息自带一次「<检查项名>：」前缀，去掉它以免与检查项名重复。
    detail = message.removeprefix(f"{name}：").removeprefix(f"{name}: ")
    results.append(
        CheckResult(
            LEVEL_OK if pinned else LEVEL_FAIL,
            name,
            i18n.t("cli.tui_cmd.check_textual_version_detail", message=detail, pin=compat.TEXTUAL_PIN),
        )
    )
    for capability in compat.terminal_capabilities():
        results.append(
            CheckResult(LEVEL_OK if capability.available else LEVEL_WARN, capability.name, capability.detail)
        )
    return results


def _check_stylesheet() -> list[CheckResult]:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import STYLESHEET, stylesheet_summary

    sheet = stylesheet_summary()
    results = [
        CheckResult(
            LEVEL_OK,
            i18n.t("cli.tui_cmd.check_stylesheet_source"),
            i18n.t(
                "cli.tui_cmd.check_stylesheet_source_detail",
                origin=sheet["origin"],
                lines=sheet["lines"],
                size=sheet["bytes"],
                sha256=sheet["sha256"],
            ),
        )
    ]
    try:
        probe = compat.App()
        compat.install_akari_themes(probe)
        compat.parse_stylesheet(STYLESHEET, "<akaribot-tui>", app=probe)
    except Exception as error:  # noqa: BLE001 - 解析失败即硬失败，需报出原文
        results.append(
            CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_stylesheet_parse"), f"{type(error).__name__}: {error}")
        )
    else:
        results.append(
            CheckResult(
                LEVEL_OK,
                i18n.t("cli.tui_cmd.check_stylesheet_parse"),
                i18n.t("cli.tui_cmd.check_stylesheet_parse_ok"),
            )
        )
    return results


def _check_resources() -> list[CheckResult]:
    from akaribot.cli.tui import _compat as compat

    results: list[CheckResult] = []
    package = "akaribot.cli.tui"
    inventory = compat.resource_inventory(package)
    if inventory:
        items = i18n.t("cli.common.list_separator").join(inventory)
        results.append(
            CheckResult(
                LEVEL_OK,
                i18n.t("cli.tui_cmd.check_resources"),
                i18n.t("cli.tui_cmd.check_resources_detail", package=package, items=items),
            )
        )
    else:
        # 枚举不到可读资源即这项产品检查没跑成（冻结产物未带包数据），故记未执行而不是警告。
        results.append(
            CheckResult(
                LEVEL_SKIP,
                i18n.t("cli.tui_cmd.check_resources"),
                i18n.t("cli.tui_cmd.check_resources_missing", package=package),
            )
        )
    probe = compat.read_resource_text(package, "app.tcss")
    results.append(
        CheckResult(
            LEVEL_OK if probe is not None else LEVEL_WARN,
            i18n.t("cli.tui_cmd.check_stylesheet_resource"),
            i18n.t("cli.tui_cmd.check_stylesheet_read", count=len(probe))
            if probe is not None
            else i18n.t("cli.tui_cmd.check_stylesheet_absent"),
        )
    )
    return results


def _check_width() -> list[CheckResult]:
    from akaribot.cli.tui import _compat as compat

    sample = "安装骰子"
    computed = compat.display_width(sample)
    truncated = compat.truncate_cells("安装骰子模块", 7)
    detail = i18n.t(
        "cli.tui_cmd.check_cjk_width_detail",
        sample=repr(sample),
        computed=computed,
        length=len(sample),
        truncated=repr(truncated),
        width=compat.display_width(truncated),
    )
    level = LEVEL_OK if computed == 8 and compat.display_width(truncated) <= 7 else LEVEL_FAIL
    return [CheckResult(level, i18n.t("cli.tui_cmd.check_cjk_width"), detail)]


def _check_boot() -> CheckResult:
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

    source = StaticModuleSource(
        [
            ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed"),
            ModuleRecord(name="wiki", dist="akari-bot-module-wiki", version="0.2.0", summary="维基查询"),
        ]
    )
    app_instance = TuiApp(source=source, initial_page="modules", boot_started_at=time.monotonic())

    async def boot() -> tuple[int, str, tuple[int, int], float]:
        async with compat.app_test(app_instance, size=(80, 24)) as pilot:
            page = app_instance.modules_page()
            await page.wait_for_idle()
            await pilot.pause()
            width, height = compat.widget_cells(page)
            detail = page.detail_text.splitlines()[0] if page.detail_text else ""
            rows = len(page.visible_records)
            first_paint = app_instance.first_paint_ms
            await pilot.press("q")
            return rows, detail, (width, height), first_paint

    try:
        rows, detail, size, first_paint = asyncio.run(boot())
    except Exception as error:  # noqa: BLE001 - 启动失败即硬失败，需报出原文
        return CheckResult(LEVEL_FAIL, i18n.t("cli.tui_cmd.check_boot"), f"{type(error).__name__}: {error}")
    return CheckResult(
        LEVEL_OK,
        i18n.t("cli.tui_cmd.check_boot"),
        i18n.t(
            "cli.tui_cmd.check_boot_detail",
            rows=rows,
            detail=repr(detail),
            width=size[0],
            height=size[1],
            startup=f"{app_instance.startup_ms:.0f}",
            first_paint=f"{first_paint:.0f}",
        ),
    )
