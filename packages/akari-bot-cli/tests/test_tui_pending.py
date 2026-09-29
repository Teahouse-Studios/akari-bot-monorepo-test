"""确认框的连发闸门。

每次弹确认框之前页面都过一次 :class:`akaribot.cli.tui._compat.PendingConfirm`：鼠标双击与键盘连发
会在几十毫秒内送来同一个动作的两次请求，闸门在防抖窗口内只放行一次，第二次不开第二层模态框。
换目标立即放行；切页、刷新、换选中项时复位。用例用注入时钟驱动，不依赖真实等待。
"""

from akaribot.cli.tui import _compat as compat
from akaribot.testing import Tester, func_case

DEBOUNCE = compat.CONFIRM_DEBOUNCE_SECONDS


def _test_first_trigger_is_accepted():
    gate = compat.PendingConfirm()
    return gate.accept("recreate", now=100.0) is True


def _test_double_trigger_is_ignored():
    # 鼠标双击与键盘连发：两次请求挨得极近，第二次不开第二层确认框。
    gate = compat.PendingConfirm()
    gate.accept("recreate", now=100.0)
    burst = [gate.accept("recreate", now=100.0 + offset) for offset in (0.01, 0.1, DEBOUNCE / 2)]
    return burst == [False, False, False]


def _test_trigger_after_the_window_is_accepted():
    gate = compat.PendingConfirm()
    gate.accept("recreate", now=100.0)
    return gate.accept("recreate", now=100.0 + DEBOUNCE + 0.01) is True


def _test_other_target_is_accepted():
    # 换目标就是另一次动作：立即放行，不受上一个目标的防抖窗口影响。
    gate = compat.PendingConfirm()
    gate.accept("recreate", now=100.0)
    return gate.accept("release", now=100.01) is True


def _test_reset_accepts_immediately():
    # 切页、刷新、换选中项会复位：复位后同一个目标立即放行。
    gate = compat.PendingConfirm()
    gate.accept("recreate", now=100.0)
    gate.reset()
    return gate.accept("recreate", now=100.01) is True


@func_case
async def test_tui_pending(tester: Tester):
    """cli.tui._compat: 确认框连发闸门测试"""
    await tester.test(_test_first_trigger_is_accepted, "首次触发放行")
    await tester.test(_test_double_trigger_is_ignored, "双击与连发被忽略")
    await tester.test(_test_trigger_after_the_window_is_accepted, "越过防抖窗口后放行")
    await tester.test(_test_other_target_is_accepted, "换目标立即放行")
    await tester.test(_test_reset_accepts_immediately, "复位后立即放行")

    return tester
