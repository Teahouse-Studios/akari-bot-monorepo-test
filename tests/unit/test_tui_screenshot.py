"""tools/tui_screenshot.py 的 SVG 文字重排与输出路径测试。

中文粘连的根因是 Rich 按字符数写入 ``textLength``，一个汉字仅分到半个单元格的宽度。这里固定
三项行为。

- 宽字符按单元格逐个输出。
- 单元格宽度由导出自身的窄字符片段推算。
- 标题一类自然排版的文字保持原样。

空格不产生文字元素，否则会在单元格中间留下可见的空白块。

远端字体声明必须移除，否则断网时浏览器仍会尝试下载字体，排版随字体是否可用而变化。
"""

import importlib.util
import re
import sys
from pathlib import Path

from akaribot.testing import func_case, Tester

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "tui_screenshot.py"

FONT_RULE = ".terminal-1-matrix { font-family: Fira Code, monospace; }"


def _tool():
    spec = importlib.util.spec_from_file_location("tui_screenshot_under_test", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _svg(body: str) -> str:
    return f"<svg><style>{FONT_RULE}</style>{body}</svg>"


def _texts(svg: str) -> list[tuple[dict[str, str], str]]:
    return [
        (dict(re.findall(r'([\w-]+)="([^"]*)"', attributes)), content)
        for attributes, content in re.findall(r"<text\b([^>]*)>(.*?)</text>", svg, re.S)
    ]


def _test_wide_run_is_split_per_cell():
    # 122 是 Rich 按 10 个字符计算的错误宽度。四个汉字实际占八个单元格。
    svg = _svg(
        '<text class="r2" x="10" y="20" textLength="122" clip-path="url(#l)">实例管理</text>'
        '<text class="r2" x="10" y="44" textLength="12.2">a</text>'
    )
    fixed = _tool().reflow_text(svg)
    texts = _texts(fixed)
    chars = [content for _, content in texts]
    centers = [float(attributes["x"]) for attributes, _ in texts]
    return (
        chars == ["实", "例", "管", "理", "a"]
        and centers[:2] == [22.2, 46.6]
        and all(attributes.get("text-anchor") == "middle" for attributes, _ in texts)
        and "textLength" not in fixed
    )


def _test_narrow_run_keeps_ascii_cells():
    fixed = _tool().reflow_text(_svg('<text x="0" y="10" textLength="36.6">abc</text>'))
    return [float(attributes["x"]) for attributes, _ in _texts(fixed)] == [6.1, 18.3, 30.5]


def _test_spaces_do_not_become_glyphs():
    fixed = _tool().reflow_text(_svg('<text x="0" y="10" textLength="36.6">a b</text>'))
    texts = _texts(fixed)
    return [content for _, content in texts] == ["a", "b"] and float(texts[1][0]["x"]) == 30.5


def _test_title_is_not_rewritten():
    title = '<text class="r1-title" fill="#c5c8c6" text-anchor="middle" x="679" y="27">AkariBot — 概览</text>'
    fixed = _tool().reflow_text(_svg(title))
    return title in fixed


def _test_cell_width_falls_back_when_only_wide_text():
    # 没有窄字符片段可参照时沿用 20 px 字号下的等宽估算，避免除零或 0 宽度。
    return _tool().detect_cell_width(_svg('<text x="0" y="10" textLength="122">实例</text>')) == 12.2


def _test_combining_marks_stay_with_base():
    tool = _tool()
    return tool.split_clusters("e\u0301") == ["e\u0301"] and tool.split_clusters("👩\u200d💻") == ["👩\u200d💻"]


def _test_font_stack_gains_cjk_fallback():
    fixed = _tool().reflow_text(_svg('<text x="0" y="10" textLength="12.2">a</text>'))
    return '"PingFang SC"' in fixed and "font-family: Fira Code, monospace;" not in fixed


def _test_remote_font_face_is_removed():
    # Rich 模板从 cdnjs 加载 Fira Code，断网时浏览器会等待下载后再回退，同一份导出会呈现两种排版。
    svg = (
        '<svg><style>@font-face { font-family: "Fira Code"; '
        'src: url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/FiraCode-Regular.woff2") format("woff2"); }'
        f"{FONT_RULE}</style></svg>"
    )
    fixed = _tool().reflow_text(svg)
    return "@font-face" not in fixed and "cdnjs" not in fixed and '"PingFang SC"' in fixed


def _test_output_paths_pair_formats():
    tool = _tool()
    return tool._output_paths(None, "dashboard", "both", True) == {
        "svg": Path("tui-dashboard.svg"),
        "png": Path("tui-dashboard.png"),
    }


def _test_output_paths_honour_explicit_suffix():
    # 指定文件名时按该文件名输出，另一份在相同目录下使用同名文件，以免两份截图分散在两个目录。
    tool = _tool()
    return tool._output_paths(Path("shots/hero.png"), "dashboard", "svg", True) == {
        "png": Path("shots/hero.png"),
        "svg": Path("shots/hero.svg"),
    }


def _test_output_paths_use_directory_for_batches():
    tool = _tool()
    return tool._output_paths(Path("shots"), "logs", "png", False) == {"png": Path("shots/tui-logs.png")}


def _test_viewbox_size_is_ceiled():
    tool = _tool()
    return tool._svg_size('<svg viewBox="0 0 1360 782.5">') == (1360, 783)


def _test_parse_keys_splits_and_trims():
    tool = _tool()
    return tool.parse_keys(" n, enter ,f ") == ("n", "enter", "f")


def _test_parse_keys_drops_empty_segments():
    # 逗号结尾或连续逗号常见于手动输入的命令，空片段传给 pilot 会抛出异常。
    tool = _tool()
    return tool.parse_keys("f,,  ,") == ("f",) and tool.parse_keys("") == ()


@func_case
async def test_tui_screenshot(tester: Tester):
    """tools.tui_screenshot 的 SVG 文字重排与输出路径测试。"""
    await tester.test(_test_wide_run_is_split_per_cell, "宽字符按单元格逐个输出")
    await tester.test(_test_narrow_run_keeps_ascii_cells, "窄字符保持单单元格")
    await tester.test(_test_spaces_do_not_become_glyphs, "空格不生成文字元素")
    await tester.test(_test_title_is_not_rewritten, "标题保持自然排版")
    await tester.test(_test_cell_width_falls_back_when_only_wide_text, "缺少窄字符时回退默认宽度")
    await tester.test(_test_combining_marks_stay_with_base, "组合符跟随基字符")
    await tester.test(_test_font_stack_gains_cjk_fallback, "字体栈补上中文回退")
    await tester.test(_test_remote_font_face_is_removed, "移除远端字体声明")
    await tester.test(_test_output_paths_pair_formats, "默认同时输出 SVG 与 PNG")
    await tester.test(_test_output_paths_honour_explicit_suffix, "指定文件名时补同名兄弟文件")
    await tester.test(_test_output_paths_use_directory_for_batches, "批量输出按页面名命名")
    await tester.test(_test_viewbox_size_is_ceiled, "画布尺寸向上取整")
    await tester.test(_test_parse_keys_splits_and_trims, "按键序列按逗号拆分")
    await tester.test(_test_parse_keys_drops_empty_segments, "按键序列忽略空片段")
    return tester
