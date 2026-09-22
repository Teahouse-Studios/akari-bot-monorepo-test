"""适配器作者的公共 API 面。

收录只有平台适配器会用、且不属于模块面的设施：模块包 import 本模块，通常意味着它做了本应交给
适配器的事。模块面 API 见 :mod:`core.api`，两者共享的名称（``Bot``、``SessionInfo``、消息元素等）
只在 :mod:`core.api` 导出，适配器同时依赖两个门面。

与 :mod:`core.api` 相同，导入期不依赖实例配置，未绑定的名字由 ``__getattr__`` 在首次访问时重试。
``core.utils.s3`` 依赖可选的 boto3，故导入块额外容忍 ``ImportError``：单个可选依赖缺失不应使整个
适配器面不可用，真实错误在访问对应名字时抛出。
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from akaribot.core.constants.exceptions import ConfigFileNotFound

# 本面对外承诺的全部名字。新增导出须同时更新 __all__ 与 LAZY_MODULES。
__all__ = [
    "BUTTON_TOKEN_PREFIX",
    "BotState",
    "ButtonConsumeResult",
    "ButtonConsumeStatus",
    "ButtonState",
    "ContextManager",
    "Features",
    "PlatformAPI",
    "RegisteredButton",
    "S3Storage",
    "S3StorageAPI",
    "Temp",
    "check_queue",
    "client_cleanup",
    "client_init",
    "compress_audio_video",
    "compress_image",
    "compress_media_chain",
    "consume_button",
    "image_split",
    "normalize_button_payload",
    "register_button_rows",
    "resolve_media_base64",
    "resolve_media_path",
]

try:
    # 不依赖配置系统的名字：能力声明、机器人状态与进程内临时存储。
    from akaribot.core.builtins.session.bot_state import BotState
    from akaribot.core.builtins.session.features import Features
    from akaribot.core.builtins.temp import Temp

    # 会话契约：适配器实现 ContextManager，并据此注册自身能力。
    from akaribot.core.builtins.session.context import ContextManager

    # 客户端生命周期：适配器启动与退出时初始化、清理平台资源。
    from akaribot.core.client.init import check_queue, client_cleanup, client_init

    # 队列契约：适配器实现 PlatformAPI，供服务端跨进程调用平台动作。
    from akaribot.core.queue.contracts import PlatformAPI

    # 按钮与媒体：平台侧按钮注册、媒体压缩与长图分片。
    from akaribot.core.utils.button_runtime import (
        BUTTON_TOKEN_PREFIX,
        ButtonConsumeResult,
        ButtonConsumeStatus,
        ButtonState,
        RegisteredButton,
        consume_button,
        normalize_button_payload,
        register_button_rows,
    )
    from akaribot.core.utils.image_split import image_split
    from akaribot.core.utils.media import (
        compress_audio_video,
        compress_image,
        compress_media_chain,
        resolve_media_base64,
        resolve_media_path,
    )

    # 对象存储依赖可选的 boto3，放在导入块末尾：缺失时只影响这两个名字。
    # S3Storage 是 core 配置构造好的单例，S3StorageAPI 供适配器自建客户端（构造缺依赖时给出安装指引）。
    from akaribot.core.utils.s3 import S3Storage, S3StorageAPI
except (ConfigFileNotFound, ImportError):
    # 配置或可选依赖缺失时保留未导入的名字，由 __getattr__ 在首次访问时重试。
    pass

# 名称到来源模块的映射。仅在导入块中断时使用。
LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "akaribot.core.builtins.session.bot_state": ("BotState",),
    "akaribot.core.builtins.session.context": ("ContextManager",),
    "akaribot.core.builtins.session.features": ("Features",),
    "akaribot.core.builtins.temp": ("Temp",),
    "akaribot.core.client.init": ("check_queue", "client_cleanup", "client_init"),
    "akaribot.core.queue.contracts": ("PlatformAPI",),
    "akaribot.core.utils.button_runtime": (
        "BUTTON_TOKEN_PREFIX",
        "ButtonConsumeResult",
        "ButtonConsumeStatus",
        "ButtonState",
        "RegisteredButton",
        "consume_button",
        "normalize_button_payload",
        "register_button_rows",
    ),
    "akaribot.core.utils.image_split": ("image_split",),
    "akaribot.core.utils.media": (
        "compress_audio_video",
        "compress_image",
        "compress_media_chain",
        "resolve_media_base64",
        "resolve_media_path",
    ),
    "akaribot.core.utils.s3": ("S3Storage", "S3StorageAPI"),
}

_LAZY_INDEX: dict[str, str] = {name: path for path, names in LAZY_MODULES.items() for name in names}


def __getattr__(name: str) -> Any:
    """按来源索引导入单个适配器面名字。

    导入块中断时未绑定的名字在此重试；重试仍失败则原样抛出来源错误，让调用方看到真实原因。
    解析结果写回模块命名空间，后续访问不再经过本函数。

    :param name: 适配器面名字。
    :return: 名字对应的对象。
    :raises AttributeError: 该名字不在本面承诺的清单内。
    """
    module_path = _LAZY_INDEX.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module_path), name)
    globals()[name] = value
    return value
