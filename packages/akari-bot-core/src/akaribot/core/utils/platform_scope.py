"""平台匹配的四元组判据。

模块、命令、正则与 hook 的 ``available_for`` / ``exclude_from`` 按四段判据判分：
``target_from``（场景前缀）、``client_name``（客户端身份，含实例后缀）、``platform_from``
（平台级场景前缀）、``platform_name``（平台展示名）。

默认实例下后两段分别等于前两段，判据退化为改造前的两段。``target_from`` 为空表示平台未知，
判为允许——改造前整段跳过平台判分，此语义须保持。
"""

from typing import Iterable

from core.constants.info import Info


def resolve_platform_identity(
    target_from: str | None,
    client_name: str | None = None,
    platform_name: str | None = None,
    platform_from: str | None = None,
) -> tuple[str, str]:
    """补齐会话的平台两段。

    入站会话在平台进程内构造，此时 ``Info.platform_name`` 由 ``bot.py`` 的 ``go()`` 置位；
    出站会话与跨进程反序列化的旧消息取不到它，退回 ``client_name`` / ``target_from``，
    即旧的两段判据，不会因缺字段而误伤。

    :param target_from: 场景前缀。
    :param client_name: 客户端身份。
    :param platform_name: 已有的平台展示名；缺省时按上述规则推导。
    :param platform_from: 已有的平台场景前缀；缺省时由 ``target_from`` 的客户端段替换而来。
    :return: ``(platform_name, platform_from)``。
    """
    if not client_name and target_from:
        client_name = target_from.split("|", 1)[0]
    if not platform_name:
        platform_name = Info.platform_name or client_name or ""
    if not platform_from and target_from:
        if (
            client_name
            and target_from.startswith(client_name)
            and (len(target_from) == len(client_name) or target_from[len(client_name)] == "|")
        ):
            platform_from = f"{platform_name}{target_from[len(client_name) :]}"
        else:
            platform_from = target_from
    return platform_name, platform_from or ""


def platform_fields(session_info) -> tuple[str | None, str | None, str | None, str | None]:
    """按 ``(target_from, client_name, platform_from, platform_name)`` 取会话字段。

    会话对象可能来自核心之外：测试替身只提供它真正用到的字段，跨进程反序列化的旧结构也
    可能缺少平台两段。缺字段按 None 处理（平台未知），由 :func:`platform_scope` 与
    :func:`scope_allows` 判为允许，与改造前整段跳过平台判分的行为一致。

    :param session_info: 会话信息对象。
    :return: 四段字段，缺失者为 None。
    """
    return (
        getattr(session_info, "target_from", None),
        getattr(session_info, "client_name", None),
        getattr(session_info, "platform_from", None),
        getattr(session_info, "platform_name", None),
    )


def scope_of(session_info) -> set[str]:
    """从会话信息取出平台判据；缺字段时判据为空，即平台未知。

    :param session_info: 会话信息对象。
    :return: 判据集合。
    """
    return platform_scope(*platform_fields(session_info))


def platform_scope(
    target_from: str | None,
    client_name: str | None = None,
    platform_from: str | None = None,
    platform_name: str | None = None,
) -> set[str]:
    """构造平台匹配的判据集合。

    :param target_from: 场景前缀。
    :param client_name: 客户端身份；缺省时取 ``target_from`` 的首段。
    :param platform_from: 平台场景前缀。
    :param platform_name: 平台展示名。
    :return: 判据集合，已剔除空值。
    """
    scope = {value for value in (target_from, client_name, platform_from, platform_name) if value}
    if not client_name and target_from:
        scope.add(target_from.split("|", 1)[0])
    return scope


def scope_allows(scope: set[str], available_for: Iterable[str], exclude_from: Iterable[str]) -> bool:
    """按判据集合判分一组 ``available_for`` / ``exclude_from`` 声明。

    排除优先于包含：``exclude_from`` 命中即拒绝，随后才看 ``available_for`` 是否命中或为 ``*``。
    判据为空表示平台未知，此时返回真，见模块 docstring。

    :param scope: 由 :func:`platform_scope` 构造的判据集合。
    :param available_for: 允许的平台声明。
    :param exclude_from: 排除的平台声明。
    :return: 是否允许。
    """
    if not scope:
        return True
    if scope & set(exclude_from):
        return False
    return "*" in available_for or bool(scope & set(available_for))
