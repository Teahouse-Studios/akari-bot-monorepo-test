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

import typer

app = typer.Typer(
    help="交互界面",
    no_args_is_help=False,
)

LEVEL_OK = "ok"
LEVEL_WARN = "warn"
LEVEL_FAIL = "fail"


@dataclass(frozen=True)
class CheckResult:
    """一条自检结论。

    :param level: ``ok`` / ``warn`` / ``fail``。
    :param name: 检查项名称。
    :param detail: 实测结果说明。
    """

    level: str
    name: str
    detail: str

    def render(self) -> str:
        """返回单行输出文本。"""
        return f"[{self.level:>4}] {self.name}：{self.detail}"


@app.callback(invoke_without_command=True)
def tui(
    self_check: bool = typer.Option(False, "--self-check", help="无头自检：加载包内资源与样式表并启动一次后退出"),
    headless: bool = typer.Option(False, "--headless", help="无头冒烟运行：启动、读取一次、立即退出并打印耗时"),
    no_mouse: bool = typer.Option(False, "--no-mouse", help="不请求鼠标追踪，供哑终端或 tmux 使用"),
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
        typer.echo(
            "当前标准输入输出不是终端，交互界面无法启动；"
            "请在真实终端中运行，或改用 `akaribot tui --self-check` / `akaribot tui --headless`。",
            err=True,
        )
        raise typer.Exit(code=2)

    from akaribot.cli.tui.app import run_tui

    result = run_tui(mouse=mouse)
    typer.echo(result.summary(), err=True)
    raise typer.Exit(code=result.exit_code)


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
        typer.echo(f"无头冒烟失败：{type(error).__name__}: {error}", err=True)
        return 1
    elapsed_ms = (time.monotonic() - started) * 1000.0
    sheet = stylesheet_summary()
    typer.echo(
        f"无头冒烟通过：80×24 下渲染 {rows} 行模块记录，{elapsed_ms:.0f} ms 内退出；"
        f"样式表来源 {sheet['origin']}，{sheet['lines']} 行，sha256 {sheet['sha256']}"
    )
    typer.echo(
        f"启动 {app_instance.startup_ms:.0f} ms，首帧 {app_instance.first_paint_ms:.0f} ms，"
        f"模块数据源调用 {_source_calls(app_instance)} 次"
    )
    return 0


def _source_calls(app_instance: object) -> int:
    """读取数据源的取数次数，供冒烟输出展示缓存是否生效。"""
    source = getattr(app_instance, "module_source", None)
    calls = getattr(source, "calls", None)
    if isinstance(calls, dict):
        return int(calls.get("list", 0))
    return -1


def run_self_check() -> int:
    """执行自检并返回进程退出码，非零表示存在硬失败。

    :return: 0 表示全部硬性检查通过；1 表示存在 ``fail`` 项。
    """
    results: list[CheckResult] = []
    results.extend(_check_environment())
    results.extend(_check_stylesheet())
    results.extend(_check_resources())
    results.extend(_check_width())
    results.append(_check_boot())

    for result in results:
        stream = sys.stderr if result.level == LEVEL_FAIL else sys.stdout
        typer.echo(result.render(), file=stream)
    failures = [result for result in results if result.level == LEVEL_FAIL]
    warnings = [result for result in results if result.level == LEVEL_WARN]
    if failures:
        typer.echo(f"自检失败：{len(failures)} 项失败，{len(warnings)} 项警告", err=True)
        return 1
    typer.echo(f"自检通过：{len(results) - len(warnings)} 项通过，{len(warnings)} 项警告")
    return 0


def _check_environment() -> list[CheckResult]:
    """检查 Textual 版本与终端能力。"""
    from akaribot.cli.tui import _compat as compat

    results: list[CheckResult] = []
    pinned, message = compat.check_textual_version()
    results.append(
        CheckResult(LEVEL_OK if pinned else LEVEL_FAIL, "textual 版本", f"{message}；紧钉值 {compat.TEXTUAL_PIN}")
    )
    for capability in compat.terminal_capabilities():
        results.append(
            CheckResult(LEVEL_OK if capability.available else LEVEL_WARN, capability.name, capability.detail)
        )
    return results


def _check_stylesheet() -> list[CheckResult]:
    """检查样式表来源与语法。"""
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import STYLESHEET, stylesheet_summary

    sheet = stylesheet_summary()
    results = [
        CheckResult(
            LEVEL_OK,
            "样式表来源",
            f"{sheet['origin']}，{sheet['lines']} 行，{sheet['bytes']} 字节，sha256 {sheet['sha256']}",
        )
    ]
    try:
        compat.parse_stylesheet(STYLESHEET, "<akaribot-tui>", app=compat.App())
    except Exception as error:  # noqa: BLE001 - 解析失败即硬失败，需报出原文
        results.append(CheckResult(LEVEL_FAIL, "样式表解析", f"{type(error).__name__}: {error}"))
    else:
        results.append(CheckResult(LEVEL_OK, "样式表解析", "Textual 解析通过"))
    return results


def _check_resources() -> list[CheckResult]:
    """检查包内资源能否读取，这一项在冻结产物里最容易失败。"""
    from akaribot.cli.tui import _compat as compat

    results: list[CheckResult] = []
    package = "akaribot.cli.tui"
    inventory = compat.resource_inventory(package)
    if inventory:
        results.append(CheckResult(LEVEL_OK, "包内资源枚举", f"{package}：{'、'.join(inventory)}"))
    else:
        results.append(
            CheckResult(
                LEVEL_WARN,
                "包内资源枚举",
                f"{package} 未枚举到可读资源；冻结产物以编译形式存放模块时属预期，"
                "需靠 --include-package-data 带上数据文件",
            )
        )
    probe = compat.read_resource_text(package, "app.tcss")
    results.append(
        CheckResult(
            LEVEL_OK if probe is not None else LEVEL_WARN,
            "样式表资源 app.tcss",
            f"读到 {len(probe)} 字符" if probe is not None else "不存在，样式表由内联常量提供（见 tui/README.md）",
        )
    )
    return results


def _check_width() -> list[CheckResult]:
    """检查中文宽字符的宽度计算。"""
    from akaribot.cli.tui import _compat as compat

    sample = "安装骰子"
    computed = compat.display_width(sample)
    truncated = compat.truncate_cells("安装骰子模块", 7)
    detail = (
        f"display_width({sample!r})={computed}（期望 8，len={len(sample)}）；"
        f"截断到 7 列得到 {truncated!r}，宽度 {compat.display_width(truncated)}"
    )
    level = LEVEL_OK if computed == 8 and compat.display_width(truncated) <= 7 else LEVEL_FAIL
    return [CheckResult(level, "中文宽度计算", detail)]


def _check_boot() -> CheckResult:
    """在 80×24 无头终端里启动一次界面，验证控件树与样式表可用。"""
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

    source = StaticModuleSource(
        [
            ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", summary="骰子", state="installed"),
            ModuleRecord(name="wiki", dist="akari-bot-module-wiki", version="0.2.0", summary="维基查询"),
        ]
    )
    app_instance = TuiApp(source=source, boot_started_at=time.monotonic())

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
        return CheckResult(LEVEL_FAIL, "界面启动 80×24", f"{type(error).__name__}: {error}")
    return CheckResult(
        LEVEL_OK,
        "界面启动 80×24",
        f"列表 {rows} 行，详情首行 {detail!r}，页面尺寸 {size[0]}×{size[1]}，"
        f"启动 {app_instance.startup_ms:.0f} ms、首帧 {first_paint:.0f} ms",
    )
