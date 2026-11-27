"""消息链原地修改的归一化单元测试。

values 的声明类型是 list[MessageElement]。append 一类原地修改的方法直接写入入参，因此裸字符串
能一路进到 JobQueue 的序列化阶段，直到 cattrs 内部才以“'str' object is not a mapping”暴露，
调用栈已难以追溯来源。

assign() 会把字符串转作文本元素，原地修改的方法不会。两者行为不一致：以
MessageChain.create() 起手、随后 append 裸字符串的写法（如 akaribot/modules/wiki/wiki.py 与
akaribot/modules/idlist）由此出错。
"""

from akaribot.core.builtins.converter import converter
from akaribot.core.builtins.message.chain import MessageChain, MessageNodes
from akaribot.core.builtins.message.elements import PlainElement
from akaribot.core.builtins.message.internal import Plain
from akaribot.core.logger import Logger
from akaribot.testing import func_case, Tester


async def _test_append_normalizes_str():
    try:
        chain = MessageChain.create()
        chain.append("裸字符串")
        if len(chain.values) != 1 or not isinstance(chain.values[0], PlainElement):
            Logger.error(f"append should normalise str, got: {chain.values!r}")
            return False
        return chain.values[0].text == "裸字符串"

    except Exception:
        return False


async def _test_appended_chain_is_serialisable():
    # 此用例复现线上异常场景。finish() 若接收到 MessageChain，get_message_chain()
    # 则直接原样返回并跳过 assign 规范化，导致字符串类型透传至 cattrs 并引发异常：
    # TypeError: 'str' object is not a mapping。
    try:
        chain = MessageChain.create()
        chain.append("裸字符串")
        converter.unstructure(chain, MessageChain | MessageNodes)
        return True

    except Exception:
        Logger.exception()
        return False


async def _test_iadd_list_normalizes_str():
    try:
        chain = MessageChain.create()
        chain += [Plain("甲"), "乙"]
        return len(chain.values) == 2 and all(isinstance(v, PlainElement) for v in chain.values)

    except Exception:
        return False


async def _test_append_skips_empty_and_none():
    try:
        chain = MessageChain.create()
        chain.append("")
        chain.append(None)
        return len(chain.values) == 0

    except Exception:
        return False


@func_case
async def test_chain_normalize(tester: Tester):
    """消息链原地修改的规范化测试"""
    await tester.test(_test_append_normalizes_str, "append 归一化字符串测试")
    await tester.test(_test_appended_chain_is_serialisable, "append 后可序列化测试")
    await tester.test(_test_iadd_list_normalizes_str, "+= 列表归一化测试")
    await tester.test(_test_append_skips_empty_and_none, "空值跳过测试")

    return tester
