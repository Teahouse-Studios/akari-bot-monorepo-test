"""构造会话术语作用域。"""

from __future__ import annotations

import re

from akaribot.core.i18n import derive_term_candidates

# 场景前缀来自各适配器，格式由平台方确定。无法作为键名或占位符语法的字符一律剔除。
_UNSAFE_TOKEN_CHARS = re.compile(r"[^0-9a-z_]+")


def _normalize_token(part: str) -> str:
    return _UNSAFE_TOKEN_CHARS.sub("", part.strip().lower())


def build_term_candidates(target_from: str | None, is_private: bool) -> tuple[str, ...]:
    """把场景前缀与私聊标志转换为术语候选链。

    :param target_from: 场景前缀，如 ``Discord|DM|Channel``。
    :param is_private: 该会话是否为私聊。
    :return: 候选链，最具体在前。无法解析时返回空元组，改用基础术语。
    """
    if not target_from:
        return ()
    tokens = tuple(_normalize_token(part) for part in target_from.split("|"))
    if not all(tokens):
        return ()
    try:
        return derive_term_candidates(tokens, shared=("private",) if is_private else ())
    except ValueError:
        # 前缀由平台方声明，外部适配器可能提供不合规的格式。此时回退至基础术语，而不中断消息处理流程。
        return ()
