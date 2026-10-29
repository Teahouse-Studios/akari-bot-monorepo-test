"""akaribot.modules.core.su_tools.analytics 单元测试 - 折线图数值标注的排版与缺依赖降级。"""

import subprocess
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from akaribot.core.i18n import Locale
from akaribot.testing import func_case, Tester
from akaribot.modules.core.su_tools.analytics import annotate_points

FIGSIZES = ((6.4, 4.8), (4, 3), (12, 8))
CASES = (
    [0] * 20 + [3, 5, 2, 8, 4, 1, 6, 9, 12, 7],
    [0] * 29 + [999],  # 峰值出现在末尾
    [0] * 30,  # 全零，此时不该反过来压缩坐标区
    [5, 3, 8, 2, 9, 1, 7, 4, 6, 11, 0, 2],  # year 分支的 12 个点
)


def _max_overflow(data_y: list[int], figsize: tuple[float, float]) -> float:
    # 按 analytics 折线图的画法出图，返回标注顶端超出坐标区上沿的最大像素数。
    data_x = [str(i) for i in range(1, len(data_y) + 1)]
    figure = plt.figure(figsize=figsize)
    try:
        plt.plot(data_x, data_y, "-o")
        plt.plot(data_x[-1], data_y[-1], "-ro")
        plt.tick_params(axis="x", labelrotation=45, which="major", labelsize=10)
        plt.gca().yaxis.get_major_locator().set_params(integer=True)
        annotate_points(plt, data_x, data_y)

        ax = plt.gca()
        figure.canvas.draw()
        return max(text.get_window_extent().y1 for text in ax.texts) - ax.get_window_extent().y1
    finally:
        plt.close(figure)


def _test_annotation_stays_inside_axes():
    try:
        # 标注按像素偏移放置，不参与坐标轴自动缩放，因此要覆盖不同数据量级与图幅。
        return all(_max_overflow(data_y, figsize) < 0 for data_y in CASES for figsize in FIGSIZES)

    except Exception:
        return False


def _test_module_imports_without_matplotlib():
    # 子进程里把 matplotlib 置为缺席：核心包不得因可选依赖缺席而在导入期失败，
    # 否则整个 bundled 模块会随之一并消失。
    code = (
        "import sys; sys.modules['matplotlib'] = None; sys.modules['matplotlib.pyplot'] = None; "
        "import akaribot.modules.core.su_tools.analytics as analytics; "
        "assert analytics._pyplot() is None, 'pyplot 未被判定为缺席'"
    )
    try:
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=90, check=False)
        return result.returncode == 0
    except Exception:
        return False


def _test_missing_dependency_message_resolves():
    key = "core.message.analytics.missing_matplotlib"
    return Locale("zh_cn").t(key) != key


@func_case
async def test_analytics_plot(tester: Tester):
    """akaribot.modules.core.su_tools.analytics: 折线图标注排版与缺依赖降级测试"""
    await tester.test(_test_annotation_stays_inside_axes, "数值标注不超出坐标区测试")
    await tester.test(_test_module_imports_without_matplotlib, "缺 matplotlib 时仍可导入测试")
    await tester.test(_test_missing_dependency_message_resolves, "缺依赖提示文案可解析测试")

    return tester
