"""消息正则解析临时关闭功能测试。"""

from unittest.mock import AsyncMock, patch

from akaribot.core.builtins.message.chain import MessageChain
from akaribot.core.builtins.message.internal import Plain
from akaribot.core.builtins.session.info import SessionInfo
from akaribot.core.builtins.session.internal import MessageSession
from akaribot.core.config.base import CoreConfig
from akaribot.core.constants.default import regex_disable_prefix_default
from akaribot.testing import func_case, Tester


async def _production_regex_called(input_: str) -> bool:
    from akaribot.core.builtins.parser.message import parser

    session_info = await SessionInfo.assign(
        target_id="REGEXESCAPE|Group|0",
        target_from="REGEXESCAPE|Group",
        client_name="REGEXESCAPE",
        sender_id="REGEXESCAPE|0",
        messages=MessageChain.assign(Plain(input_)),
        create=True,
    )
    msg = MessageSession(session_info=session_info)
    execute_regex = AsyncMock()
    with patch("akaribot.core.builtins.parser.message._execute_regex", execute_regex):
        await parser(msg)
    return execute_regex.await_count == 1


async def _test_production_parser_skips_markers():
    return not await _production_regex_called(".BV1xx411c7mD") and not await _production_regex_called("。BV1xx411c7mD")


async def _test_production_parser_keeps_normal_regex_parsing():
    return await _production_regex_called("BV1xx411c7mD")


async def _test_production_parser_uses_configured_markers():
    with patch.object(CoreConfig, "regex_disable_prefix", ["!"]):
        return not await _production_regex_called("!BV1xx411c7mD") and await _production_regex_called(".BV1xx411c7mD")


async def _test_production_parser_allows_empty_marker_config():
    with patch.object(CoreConfig, "regex_disable_prefix", []):
        return await _production_regex_called(".BV1xx411c7mD")


def _test_default_from_constants():
    field = CoreConfig.__config_fields__["regex_disable_prefix"]
    return regex_disable_prefix_default == [".", "。"] and field["default"] == regex_disable_prefix_default


@func_case
async def test_regex_escape(tester: Tester):
    await tester.test(_test_production_parser_skips_markers, "生产解析器在正则执行前跳过句号消息")
    await tester.test(_test_production_parser_keeps_normal_regex_parsing, "生产解析器保留普通消息正则解析")
    await tester.test(_test_production_parser_uses_configured_markers, "生产解析器使用配置的正则关闭前缀")
    await tester.test(_test_production_parser_allows_empty_marker_config, "生产解析器允许空正则关闭前缀")
    await tester.test(_test_default_from_constants, "默认前缀由 akaribot.core.constants 提供并绑定至 CoreConfig")
    return tester
