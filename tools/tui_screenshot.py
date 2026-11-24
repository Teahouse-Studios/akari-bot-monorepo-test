"""TUI 截图工具，无界面渲染指定页面并导出 SVG 与 PNG。

Textual 的截图沿用 Rich 的 SVG 导出，而 Rich 按字符数计算 ``textLength``。中文等宽字符占
两个单元格，宽度却按一个字符计算，导出后会被横向压扁并与相邻字符重叠。本工具在导出后按
单元格重新排版文字。每段文字拆分为单个字素簇，居中放入所属单元格，并补上中文字体回退。
同一份导出在浏览器中显示为正常的终端画面。本工具一并移除模板中指向 CDN 的字体声明，
断网时既不必等待下载，也不会因为无法获取字体而改变排版。

页面数据默认来自 TUI 自带的自检快照，同一份代码重复截取所得的内容相同。指定 ``--live``
时读取当前实例的真实数据，内容随实例状态变化。

位图由重排后的 SVG 渲染。优先使用 resvg、rsvg-convert 或 cairosvg，三者均不可用时回退至
Chromium 系浏览器的无界面模式。可用环境变量 ``CHROME_PATH`` 指定浏览器路径。

用法：
    uv run python tools/tui_screenshot.py                          # 截取概览页，同时给出 SVG 与 PNG
    uv run python tools/tui_screenshot.py --page modules -o tui-modules.png
    uv run python tools/tui_screenshot.py --all -o docs/public/tui --format png --theme light
"""

from __future__ import annotations

import argparse
import asyncio
import html
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

from rich.cells import get_character_cell_size

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 默认终端尺寸取常见终端的大小，为 110 列 30 行。侧边栏占 20 列后正文仍有足够宽度，各页面无需滚动。
DEFAULT_SIZE = (110, 30)

_TEXT_PATTERN = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)
_ATTRIBUTE_PATTERN = re.compile(r'([\w-]+)="([^"]*)"')
_VIEW_BOX_PATTERN = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')
_FONT_FACE_PATTERN = re.compile(r"\s*@font-face \{[^}]*\}", re.S)

# Rich 的模板仅声明 Fira Code 与 monospace，并且用 @font-face 从 CDN 获取字体。reflow_text
# 会移除字体声明，因此字体仅能取自本机。等宽 ASCII 必须排在中文字体之前，否则西文会按比例
# 字形排布，终端网格随之错位。中文缺字时依次回退至各平台的常见字体。
_MATRIX_FONT = "font-family: Fira Code, monospace;"
_CJK_FONT_STACK = (
    'font-family: "Fira Code", "FiraCode-Regular", "Sarasa Mono SC", "Noto Sans Mono CJK SC", '
    '"Noto Sans CJK SC", "Menlo", "Consolas", "DejaVu Sans Mono", "PingFang SC", "Hiragino Sans GB", '
    '"Microsoft YaHei", monospace;'
)

# 浏览器回退仅使用 Chromium 系，可用 CHROME_PATH 指定安装位置。
_CHROME_ENV = "CHROME_PATH"
_MAC_BROWSERS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Microsoft Edge Beta.app/Contents/MacOS/Microsoft Edge Beta",
)

# 演示用模块列表，名称与发行包来自本仓库，数值固定，默认截取的结果不随实例状态变化。
_DEMO_MODULES = (
    {
        "name": "wiki",
        "dist": "akari-bot-module-wiki",
        "version": "0.2.0",
        "summary": "MediaWiki 查询",
        "state": "installed",
        "kind": "module",
        "provides_modules": ("wiki",),
    },
    {
        "name": "mcmod",
        "dist": "akari-bot-module-mcmod",
        "version": "0.1.1",
        "summary": "MC 百科查询",
        "state": "installed",
        "kind": "module",
        "provides_modules": ("mcmod",),
    },
    {
        "name": "arcaea",
        "dist": "akari-bot-module-arcaea",
        "version": "0.1.3",
        "summary": "Arcaea 查分与信息",
        "state": "installed",
        "kind": "module",
        "provides_modules": ("arcaea", "arcaea-rss"),
    },
    {
        "name": "bilibili",
        "dist": "akari-bot-module-bilibili",
        "version": "0.1.0",
        "summary": "哔哩哔哩动态与直播",
        "state": "installed",
        "kind": "module",
        "provides_modules": ("bilibili",),
    },
)

# 装载状态决定表格中的“装载”列，未提供时显示为未知，因此演示数据一并提供。
_DEMO_LOAD_STATES = {"wiki": True, "mcmod": True, "arcaea": True, "arcaea-rss": False, "bilibili": True}


def parse_size(value: str) -> tuple[int, int]:
    """把 ``110x30`` 形式的尺寸解析为列数与行数。

    :param value: 尺寸文本。
    :return: ``(列, 行)``。
    """
    columns, _, rows = value.lower().partition("x")
    try:
        size = (int(columns), int(rows))
    except ValueError as error:
        raise argparse.ArgumentTypeError("尺寸格式应为 列x行，例如 110x30") from error
    if size[0] < 40 or size[1] < 12:
        raise argparse.ArgumentTypeError("尺寸过小，至少为 40x12")
    return size


def split_clusters(text: str) -> list[str]:
    """把一段文字拆分为不可再分的字素簇。

    组合符与零宽连接符必须跟随前一个字符，单独拆分会让屏幕上显示为两个字形。

    :param text: 待拆分的文字。
    :return: 字素簇序列。
    """
    clusters: list[str] = []
    for character in text:
        width = get_character_cell_size(character)
        joined = bool(clusters) and (width == 0 or character == "\u200d" or clusters[-1].endswith("\u200d"))
        if joined:
            clusters[-1] += character
        else:
            clusters.append(character)
    return clusters


def detect_cell_width(svg: str) -> float:
    """从仅包含窄字符的文字片段推算单元格宽度。

    字符宽度由字体决定，随字体不同而变化。单元格宽度按各片段 ``textLength`` 与单元格数之比
    的中位数推算，避免个别异常片段干扰。

    :param svg: Rich 导出的 SVG 文本。
    :return: 单元格宽度。
    """
    ratios: list[float] = []
    for attributes, content in _iter_text(svg):
        if "textLength" not in attributes:
            continue
        text = html.unescape(content).replace("\u00a0", " ")
        cells = sum(get_character_cell_size(character) for character in text)
        if not text.strip() or cells != len(text):
            continue
        ratios.append(float(attributes["textLength"]) / cells)
    return statistics.median(ratios) if ratios else 12.2


def _iter_text(svg: str) -> list[tuple[dict[str, str], str]]:
    return [(dict(_ATTRIBUTE_PATTERN.findall(match.group(1))), match.group(2)) for match in _TEXT_PATTERN.finditer(svg)]


def _render_cluster(attributes: dict[str, str], cluster: str, center: float, y: str) -> str:
    # 逐字定位不需要 textLength，保留它会让浏览器把单个字符拉伸到整行宽度。
    parts = [f'{name}="{value}"' for name, value in attributes.items() if name not in {"x", "y", "textLength"}]
    parts.append(f'x="{center:g}"')
    parts.append(f'y="{y}"')
    parts.append('text-anchor="middle"')
    escaped = html.escape(cluster, quote=False).replace(" ", "&#160;")
    return f"<text {' '.join(parts)}>{escaped}</text>"


def reflow_text(svg: str) -> str:
    """按单元格重排 SVG 中的文字，补上中文字体回退并移除远端字体。

    标题等不带 ``textLength`` 的文字沿用浏览器的自然排版。

    :param svg: Rich 导出的 SVG 文本。
    :return: 重排后的 SVG 文本。
    """
    cell_width = detect_cell_width(svg)

    def replace(match: re.Match[str]) -> str:
        attributes, content = match.group(1), match.group(2)
        parsed = dict(_ATTRIBUTE_PATTERN.findall(attributes))
        if "textLength" not in parsed:
            return match.group(0)
        text = html.unescape(content).replace("\u00a0", " ")
        if not text or "x" not in parsed or "y" not in parsed:
            return match.group(0)
        origin = float(parsed["x"])
        rendered: list[str] = []
        offset = 0
        for cluster in split_clusters(text):
            cells = max(1, sum(get_character_cell_size(character) for character in cluster))
            # 空格仅占位、不显示，逐字输出时可以直接跳过。
            if cluster.strip():
                center = origin + (offset + cells / 2) * cell_width
                rendered.append(_render_cluster(parsed, cluster, center, parsed["y"]))
            offset += cells
        return "".join(rendered)

    fixed = _TEXT_PATTERN.sub(replace, svg)
    fixed = _FONT_FACE_PATTERN.sub("", fixed)
    return fixed.replace(_MATRIX_FONT, _CJK_FONT_STACK)


async def capture(page_key: str, *, size: tuple[int, int], theme: str, live: bool) -> str:
    """无界面运行 TUI 并导出指定页面的 SVG。

    :param page_key: 页面键，取值参见 :data:`akaribot.cli.tui.app.PAGES`。
    :param size: 虚拟终端尺寸。
    :param theme: ``dark`` 或 ``light``。
    :param live: 为 True 时读取当前实例的真实数据，否则使用自检快照。
    :return: SVG 文本。
    """
    from akaribot.cli import i18n
    from akaribot.cli.tui import _compat as compat, context
    from akaribot.cli.tui.app import PAGES, TuiApp

    title_key = next((title for key, title, _ in PAGES if key == page_key), "cli.tui.app.title")
    if not live:
        from akaribot.cli.commands.tui import _self_check_sources
        from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource

        sources = _self_check_sources()
        module_source = StaticModuleSource(
            [ModuleRecord(**record) for record in _DEMO_MODULES],
            load_states=_DEMO_LOAD_STATES,
        )
    else:
        # 命令行入口在启动界面前记录了当前实例，直接构造应用实例时补上这一步，
        # 否则标题栏没有实例名，与正常启动的界面不一致。
        from akaribot.cli.instance import default_instance_root

        context.set_active_root(default_instance_root())
        sources = {}
        module_source = None

    app = TuiApp(source=module_source, sources=sources, initial_page=page_key)
    async with compat.app_test(app, size=size) as pilot:
        await pilot.pause()
        page = app.page(page_key)
        await page.wait_for_idle()
        await pilot.pause()
        if theme == "light":
            app.theme = compat.AKARI_THEME_LIGHT
            await pilot.pause()
        return reflow_text(app.export_screenshot(title=f"{TuiApp.TITLE} — {i18n.t(title_key)}"))


def _svg_size(svg: str) -> tuple[int, int]:
    # 位图按画布尺寸设置视口，既不会裁掉边缘，也不会多出留白。
    match = _VIEW_BOX_PATTERN.search(svg)
    if match is None:
        raise SystemExit("SVG 缺少 viewBox，无法渲染位图")
    return math.ceil(float(match.group(1))), math.ceil(float(match.group(2)))


def _browser_binary() -> str | None:
    # 仅接受 Chromium 系浏览器。这些浏览器的截图参数一致，也不必额外安装依赖。
    override = os.environ.get(_CHROME_ENV)
    if override and Path(override).exists():
        return override
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return found
    for path in _MAC_BROWSERS:
        if Path(path).exists():
            return path
    return None


def _render_cairosvg(svg_path: Path, png_path: Path, *, scale: int) -> bool:
    # cairosvg 依赖本机 cairo，缺失时导入即失败，按不可用处理。
    try:
        import cairosvg
    except (ImportError, OSError):
        return False
    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=scale)
    except Exception:
        return False
    return png_path.exists() and png_path.stat().st_size > 0


def _rasterize(svg_path: Path, png_path: Path, *, scale: int) -> str:
    # 视口按 viewBox 尺寸设置，再用 scale 放大像素比，各后端生成的像素尺寸一致。
    # 渲染依赖本机字体，优先使用仅渲染 SVG 的渲染器，减少与浏览器默认样式的相互干扰。
    # 返回值是后端名，写入输出便于排查字体差异。
    width, height = _svg_size(svg_path.read_text(encoding="utf-8"))
    png_path.parent.mkdir(parents=True, exist_ok=True)
    browser = _browser_binary()
    profile = Path(tempfile.mkdtemp(prefix="tui-screenshot-")) if browser else None
    attempts: list[tuple[str, list[str] | None]] = []
    if shutil.which("resvg"):
        attempts.append(("resvg", ["resvg", "--zoom", str(scale), str(svg_path), str(png_path)]))
    if shutil.which("rsvg-convert"):
        attempts.append(("rsvg-convert", ["rsvg-convert", "-z", str(scale), "-o", str(png_path), str(svg_path)]))
    attempts.append(("cairosvg", None))
    if browser is not None and profile is not None:
        attempts.append(
            (
                "chromium",
                [
                    browser,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-breakpad",
                    "--disable-crash-reporter",
                    "--hide-scrollbars",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=8000",
                    f"--user-data-dir={profile}",
                    f"--force-device-scale-factor={scale}",
                    f"--window-size={width},{height}",
                    f"--screenshot={png_path}",
                    svg_path.as_uri(),
                ],
            )
        )
    failures: list[str] = []
    try:
        for name, command in attempts:
            if png_path.exists():
                png_path.unlink()
            if command is None:
                if _render_cairosvg(svg_path, png_path, scale=scale):
                    return name
                failures.append(f"{name}: 不可用")
                continue
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            if png_path.exists() and png_path.stat().st_size > 0:
                return name
            detail = (result.stderr.strip().splitlines() or [str(result.returncode)])[-1]
            failures.append(f"{name}: {detail}")
    finally:
        if profile is not None:
            shutil.rmtree(profile, ignore_errors=True)
    raise SystemExit(
        "找不到可用的位图渲染器，请安装 resvg、rsvg-convert 或 cairosvg，"
        f"或用 {_CHROME_ENV} 指定 Chromium 系浏览器。已尝试：{'；'.join(failures)}"
    )


def _output_paths(output: Path | None, page_key: str, fmt: str, single: bool) -> dict[str, Path]:
    # -o 指定带后缀的文件名时按该文件名输出，另一格式在相同目录下使用同名文件。其余情况一律视为目录。
    formats = ["svg", "png"] if fmt == "both" else [fmt]
    if output is not None and single and output.suffix.lower() in {".svg", ".png"}:
        explicit = output.suffix.lower().lstrip(".")
        requested = [explicit, *(name for name in formats if name != explicit)]
        return {name: output if name == explicit else output.with_suffix(f".{name}") for name in requested}
    base = output or Path()
    return {name: base / f"tui-{page_key}.{name}" for name in formats}


def _write(target: Path, svg: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg, encoding="utf-8")


async def _run(args: argparse.Namespace) -> int:
    from akaribot.cli.i18n import SUPPORTED_LOCALES, set_locale
    from akaribot.cli.tui.app import PAGES

    page_keys = [key for key, _, _ in PAGES]
    if args.page not in page_keys:
        raise SystemExit(f"未知页面 {args.page}，可选：{', '.join(page_keys)}")
    if args.lang not in SUPPORTED_LOCALES:
        raise SystemExit(f"未知语言 {args.lang}，可选：{', '.join(SUPPORTED_LOCALES)}")
    set_locale(args.lang)

    selected = page_keys if args.all else [args.page]
    output = Path(args.out).expanduser() if args.out else None
    single = len(selected) == 1
    for page_key in selected:
        svg = await capture(page_key, size=args.size, theme=args.theme, live=args.live)
        targets = _output_paths(output, page_key, args.format, single)
        if "svg" in targets:
            source = targets["svg"]
        else:
            source = Path(tempfile.mkdtemp(prefix="tui-svg-")) / f"tui-{page_key}.svg"
        _write(source, svg)
        if "svg" in targets:
            print(source.resolve())
        if "png" in targets:
            backend = _rasterize(source, targets["png"], scale=args.scale)
            print(f"{targets['png'].resolve()}  [{backend}]")
        if "svg" not in targets:
            source.unlink(missing_ok=True)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="无界面截取 AkariBot TUI 页面并导出 SVG 与 PNG")
    parser.add_argument("--page", default="dashboard", help="页面键，默认 dashboard")
    parser.add_argument("--all", action="store_true", help="截取全部页面，此时 --out 视为目录")
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE, help="终端尺寸，默认 110x30")
    parser.add_argument("--theme", choices=("dark", "light"), default="dark", help="主题，默认 dark")
    parser.add_argument("--lang", default="zh_cn", help="界面语言，默认 zh_cn")
    parser.add_argument("--live", action="store_true", help="读取当前实例的真实数据，默认使用自检快照")
    parser.add_argument("--format", choices=("svg", "png", "both"), default="both", help="输出格式，默认 both")
    parser.add_argument("--scale", type=int, default=2, help="位图像素倍数，默认 2")
    parser.add_argument("-o", "--out", default=None, help="输出文件或目录，文件后缀决定格式，默认 tui-<页面>")
    return parser


def main(argv: list[str] | None = None) -> int:
    """命令行入口。"""
    return asyncio.run(_run(_parser().parse_args(argv)))


if __name__ == "__main__":
    sys.exit(main())
