"""akaribot.core.utils.cooldown 冷却系统单元测试。"""

import time

from akaribot.core.utils.cooldown import CoolDown, _cd_dict
from akaribot.testing import func_case, Tester
from akaribot.testing.mock.session import MockMessageSession


async def _test_cooldown_init():
    try:
        msg = MockMessageSession("~test")
        await msg.async_init("~test")
        cd = CoolDown("test_cmd", msg, delay=60)
        # 场景维度按消息通道、用户维度按 union，确保切换平台账号仍然受同一份冷却约束，
        # 但仅共享 union 而通道编号不同的场景不应互相牵连。
        return (
            cd.key == "test_cmd"
            and cd.delay == 60
            and cd.whole_target is False
            and cd.channel_key == msg.session_info.channel_key
            and cd.sender_union_id == msg.session_info.sender_union_id
        )
    except Exception:
        return False


async def _test_cooldown_check_no_cooldown():
    try:
        _cd_dict.clear()
        msg = MockMessageSession("~test")
        await msg.async_init("~test")
        cd = CoolDown("fresh_cmd_xyz", msg, delay=60)
        remaining = cd.check()
        return remaining == 0
    except Exception:
        return False


async def _test_cooldown_reset():
    try:
        _cd_dict.clear()
        msg = MockMessageSession("~test")
        await msg.async_init("~test")
        cd = CoolDown("reset_cmd_xyz", msg, delay=60)
        if cd.check() != 0:
            return False
        cd.reset()
        # 模块每次执行命令均会创建新的 CoolDown 实例，冷却限制必须跨实例生效。
        remaining = CoolDown("reset_cmd_xyz", msg, delay=60).check()
        # 重置后应恰好保留完整冷却时长，模块正是通过此非 0 值实现对重复调用的拦截。
        return 0 < remaining <= 60
    except Exception:
        return False


async def _test_cooldown_expired():
    try:
        _cd_dict.clear()
        msg = MockMessageSession("~test")
        await msg.async_init("~test")
        CoolDown("expired_cmd_xyz", msg, delay=60).reset()
        # 将记录的时间戳调整至冷却时长之前，模拟冷却已经结束。
        CoolDown("expired_cmd_xyz", msg, delay=60)._get_cd_dict().ts = time.time() - 61
        return CoolDown("expired_cmd_xyz", msg, delay=60).check() == 0
    except Exception:
        return False


async def _test_cooldown_check_readonly():
    try:
        _cd_dict.clear()
        msg = MockMessageSession("~test")
        await msg.async_init("~test")
        if CoolDown("readonly_cmd_xyz", msg, delay=60).check() != 0:
            return False
        return len(_cd_dict) == 0
    except Exception:
        return False


@func_case
async def test_cooldown(tester: Tester):
    """akaribot.core.utils.cooldown 的 CoolDown 冷却系统测试"""
    await tester.test(_test_cooldown_init, "CoolDown 初始化测试")
    await tester.test(_test_cooldown_check_no_cooldown, "CoolDown 无冷却时 check 测试")
    await tester.test(_test_cooldown_reset, "CoolDown reset 计时测试")
    await tester.test(_test_cooldown_expired, "CoolDown 冷却结束测试")
    await tester.test(_test_cooldown_check_readonly, "CoolDown check 只读测试")
    return tester
