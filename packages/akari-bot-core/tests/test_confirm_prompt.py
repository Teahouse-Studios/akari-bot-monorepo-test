"""确认提示文案选择单元测试。

快速确认有三条互不相干的途径：按钮随消息键盘下发、表情反应由机器人补加、戳一戳为 QQ 独有。
三者须依各自的能力标志分别判定：把它们嵌在 support_reaction 一个门槛之下时，按钮分支永远
够不着——QQ 官方机器人的 support_reaction 为假，而它恰恰是唯一支持按钮的平台。

按钮不受 quick_confirm 管辖：该配置控制的是表情反应的补加与戳一戳的响应，
而按钮在 akaribot/adapters/qqbot/context.py 中只看 wait_type，配置关闭时照样下发。
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from akaribot.core.builtins.session.internal import MessageSession, confirm_prompt_key
from akaribot.core.queue.contracts import PlatformAPI
from akaribot.testing import func_case, Tester


def _session(support_button: bool = False, support_reaction: bool = False, client_name: str = "TEST"):
    return SimpleNamespace(
        support_button=support_button,
        support_reaction=support_reaction,
        client_name=client_name,
    )


def _test_button_wins_over_reaction():
    key = confirm_prompt_key(_session(support_button=True, support_reaction=True))
    return key == "message.wait.confirm.prompt.button"


def _test_qq_gets_poke_prompt():
    key = confirm_prompt_key(_session(support_reaction=True, client_name="QQ"))
    return key == "message.wait.confirm.prompt.qq"


def _test_other_reaction_client():
    key = confirm_prompt_key(_session(support_reaction=True, client_name="Discord"))
    return key == "message.wait.confirm.prompt.reaction"


def _test_no_quick_path():
    return confirm_prompt_key(_session()) == "message.wait.confirm.prompt"


def _test_quick_confirm_off_disables_reaction():
    with patch("akaribot.core.builtins.session.internal.quick_confirm", False):
        key = confirm_prompt_key(_session(support_reaction=True, client_name="QQ"))
    return key == "message.wait.confirm.prompt"


def _test_quick_confirm_off_keeps_button():
    with patch("akaribot.core.builtins.session.internal.quick_confirm", False):
        key = confirm_prompt_key(_session(support_button=True))
    return key == "message.wait.confirm.prompt.button"


async def _test_qq_instance_uses_face_ids():
    for platform in ("QQ", "QQBot"):
        session = _session(support_reaction=True, client_name=f"{platform}-alt")
        session.platform_name = platform
        fake = SimpleNamespace(session_info=session)
        with patch.object(PlatformAPI, "add_reaction", AsyncMock()) as add:
            await MessageSession._add_confirm_reaction(fake, ["123"])
        if [call.args[-1] for call in add.call_args_list] != ["11093", "10060"]:
            return False
        if platform == "QQ" and confirm_prompt_key(session) != "message.wait.confirm.prompt.qq":
            return False
    return True


@func_case
async def test_confirm_prompt(tester: Tester):
    """core: 确认提示文案的选择"""
    await tester.test(_test_button_wins_over_reaction, "按钮优先于表情反应")
    await tester.test(_test_qq_gets_poke_prompt, "QQ 提示含戳一戳")
    await tester.test(_test_other_reaction_client, "其余平台用表情反应提示")
    await tester.test(_test_no_quick_path, "无快速途径时只提示确认词")
    await tester.test(_test_quick_confirm_off_disables_reaction, "关闭快速确认后不提示表情反应")
    await tester.test(_test_quick_confirm_off_keeps_button, "关闭快速确认不影响按钮提示")
    await tester.test(_test_qq_instance_uses_face_ids, "QQ 后缀实例使用平台表情编号与确认提示")
    return tester
