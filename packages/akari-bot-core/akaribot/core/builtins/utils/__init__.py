"""内置工具模块，提供命令前缀和确认词等系统级配置。"""

from akaribot.core.config.base import CoreConfig
from akaribot.core.constants.default import (
    confirm_command_default,
    command_prefix_default,
)
from akaribot.core.utils.func import unique_list


# 确认命令列表，包含用户确认操作时可使用的关键词以及默认的圆形符号表情。
# 从配置中加载并去重，默认添加 ⭕ 符号作为万能确认符。
confirm_command = unique_list(filter(str.strip, CoreConfig.confirm_command) or confirm_command_default) + [
    "⭕"
]  # 确认词。

# 命令前缀列表，包含触发命令的前缀符号（如 "/" 或 "~"）。
# 从配置中加载并去重。
command_prefix = unique_list(filter(str.strip, CoreConfig.command_prefix) or command_prefix_default)  # 命令前缀。

__all__ = ["confirm_command", "command_prefix"]
