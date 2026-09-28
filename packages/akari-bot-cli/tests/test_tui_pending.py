"""破坏性动作的二次确认闸门。

各页的「连按两次」确认经 :class:`akaribot.cli.tui._compat.PendingConfirm` 收口：它挡住鼠标双击与
键盘连发（最短间隔），并让放置过久的待确认自动失效（绝对超时），这样「第一次问、第二次做」不会被
穿透，也不会在换过页之后把一句旧提示当成当前语境。用例用注入时钟驱动，不依赖真实等待。
"""

from akaribot.cli.tui import _compat as compat
from akaribot.testing import Tester, func_case

DEBOUNCE = compat.CONFIRM_DEBOUNCE_SECONDS
TIMEOUT = compat.CONFIRM_TIMEOUT_SECONDS


def _test_first_press_only_asks():
    gate = compat.PendingConfirm()
    first = gate.arm("recreate", now=100.0)
    return first is False and gate.pending_key(now=100.0) == "recreate" and gate.armed


def _test_double_press_is_ignored():
    # 鼠标双击与键盘连发：两次请求挨得极近，第二次不算确认。
    gate = compat.PendingConfirm()
    gate.arm("recreate", now=100.0)
    burst = [gate.arm("recreate", now=100.0 + offset) for offset in (0.01, 0.1, DEBOUNCE / 2)]
    return burst == [False, False, False] and gate.pending_key(now=100.0 + DEBOUNCE / 2) == "recreate"


def _test_second_press_after_the_window_executes():
    gate = compat.PendingConfirm()
    gate.arm("recreate", now=100.0)
    confirmed = gate.arm("recreate", now=100.0 + DEBOUNCE + 0.01)
    return confirmed is True and gate.armed is False


def _test_expired_pending_arms_again():
    # 放置过久后第二次按下的语境已经不同，必须重新问一次，而不是直接执行。
    gate = compat.PendingConfirm()
    gate.arm("recreate", now=100.0)
    late = gate.arm("recreate", now=100.0 + TIMEOUT + 0.01)
    return late is False and gate.pending_key(now=100.0 + TIMEOUT + 0.02) == "recreate"


def _test_pending_key_expires_and_other_keys_arm_anew():
    gate = compat.PendingConfirm()
    gate.arm("a", now=100.0)
    expired = gate.pending_key(now=100.0 + TIMEOUT + 0.01)
    other = gate.arm("b", now=200.0)
    reset = gate.arm("b", now=200.0 + DEBOUNCE + 0.01)
    gate.reset()
    return expired == "" and other is False and reset is True and gate.armed is False and gate.pending_key() == ""


def _test_reset_makes_the_next_press_ask_again():
    # 切页、刷新、换选中项都会调 reset：复位之后按同一个键只会重新提问。
    gate = compat.PendingConfirm()
    gate.arm("a", now=100.0)
    gate.reset()
    return gate.arm("a", now=100.0 + DEBOUNCE + 1.0) is False


@func_case
async def test_tui_pending(tester: Tester):
    """cli.tui._compat: 二次确认闸门测试"""
    await tester.test(_test_first_press_only_asks, "首次按键只记下待确认")
    await tester.test(_test_double_press_is_ignored, "双击与连发不算确认")
    await tester.test(_test_second_press_after_the_window_executes, "越过防抖窗口的第二次按键才执行")
    await tester.test(_test_expired_pending_arms_again, "超时后重新提问而不是执行")
    await tester.test(_test_pending_key_expires_and_other_keys_arm_anew, "换目标重新提问，复位后清空")
    await tester.test(_test_reset_makes_the_next_press_ask_again, "复位后按同一个键仍只提问")

    return tester
