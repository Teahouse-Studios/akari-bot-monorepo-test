"""模块面公共 API 的实现模块。

门面把「模块可以依赖什么」与实现位置解耦：模块包只 import ``akaribot.core.api``，core 内部
模块的移动与改名不再波及模块。全部具体 import 集中在本模块，``akaribot/core/api/__init__.py`` 只做转发。

导入分两层。不依赖配置系统的名字在模块层直接导入；其余名字记录在 ``LAZY_MODULES`` 中，由
``__getattr__`` 在首次访问时导入。原因是 ``akaribot.core.config`` 会在导入期校验配置文件存在并执行版本
迁移，而门面必须能在配置就绪之前导入：CLI 读取 API 版本、发现层收集 locale 目录都发生在配置
加载之前。``__all__`` 是门面承诺的完整清单，与 ``LAZY_MODULES`` 收录的名字一致。
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from akaribot.core.constants.exceptions import ConfigFileNotFound

# 门面对外承诺的全部名字。新增导出须同时更新 __all__ 与 LAZY_MODULES。
__all__ = [
    "AbuseWarning",
    "ActionText",
    "ActionTextElement",
    "Alive",
    "AnalyticsData",
    "AndTrigger",
    "ArgumentPattern",
    "Audio",
    "AudioElement",
    "BaseConfig",
    "BaseElement",
    "Bind",
    "Bot",
    "Button",
    "ButtonElement",
    "ButtonFrame",
    "ButtonFrameElement",
    "ButtonPayload",
    "ButtonPermission",
    "ButtonRows",
    "CFGManager",
    "Chainable",
    "CommandMeta",
    "CommandParser",
    "ConfigValueError",
    "CoolDown",
    "CoreConfig",
    "CoreSecretConfig",
    "CronTrigger",
    "DBModel",
    "DateTrigger",
    "ElementScreenshotOptions",
    "Embed",
    "EmbedElement",
    "EmbedField",
    "EmbedFieldElement",
    "EventInfo",
    "ExecutionLockList",
    "ExpiringTempDict",
    "ExternalException",
    "FetchedMessageSession",
    "FinishedSession",
    "FormattedTime",
    "FormattedTimeElement",
    "GAME_EXPIRED",
    "GlobalURLAllowlist",
    "GlobalURLBlocklist",
    "Handled",
    "HookPoint",
    "I18NContext",
    "I18NContextElement",
    "I18NMessageChain",
    "Image",
    "ImageElement",
    "ImageTable",
    "Info",
    "InlineMention",
    "IntervalTrigger",
    "InvalidHelpDocTypeError",
    "JobQueuesTable",
    "LegacyScreenshotOptions",
    "Locale",
    "Logger",
    "MaliciousLoginRecords",
    "Markdown",
    "MarkdownElement",
    "Mention",
    "MentionElement",
    "MessageChain",
    "MessageNodes",
    "MessageSession",
    "MigrationContext",
    "Module",
    "ModuleRuntimeManager",
    "ModuleStatus",
    "ModulesManager",
    "NoReportException",
    "OrTrigger",
    "PageScreenshotOptions",
    "Param",
    "Plain",
    "PlainElement",
    "PlatformMessageChain",
    "PlayState",
    "RETIRED_SOURCES",
    "RETIRED_TARGETS",
    "Random",
    "Raw",
    "RawElement",
    "RawOptions",
    "RecoveryProposal",
    "RpcError",
    "Secret",
    "SectionScreenshotOptions",
    "SecureRandom",
    "SendMessageFailed",
    "SenderUnionBind",
    "SenderUnionInfo",
    "StoredData",
    "ServerAPI",
    "SessionContextUnavailable",
    "SessionFinished",
    "SessionInfo",
    "SourceOptions",
    "Stop",
    "StopScope",
    "TargetUnionBind",
    "TargetUnionInfo",
    "Template",
    "TestException",
    "TokenBucket",
    "UNION_SCOPE_SENDER",
    "UNION_SCOPE_TARGET",
    "URLElement",
    "URLRule",
    "URLRuleError",
    "UnfriendlyActionRecords",
    "UnionDeleteBlocked",
    "Url",
    "Video",
    "VideoElement",
    "WaitCancelException",
    "arrange_buttons",
    "build_button_rows",
    "cb64imglst",
    "check",
    "check_bool",
    "check_web_render_status",
    "chunk_list",
    "close_web_render",
    "collect_locale_paths",
    "command_prefix",
    "config_filename",
    "confirm_command",
    "confirm_command_default",
    "confirm_prompt_key",
    "converter",
    "cost_petal",
    "delete_url",
    "dev_mode",
    "download",
    "enqueue_notice",
    "escape_special_char",
    "escape_table_cell",
    "evaluate_url_policy",
    "fetch_module_db",
    "format_table_code",
    "gained_petal",
    "get_available_locales",
    "get_fontsize",
    "get_message_chain",
    "get_model_fields",
    "get_model_names",
    "get_stored_list",
    "get_url",
    "image_table_render",
    "init_web_render",
    "is_float",
    "is_int",
    "is_merge_route_allowed",
    "is_module_allowed_when_retired",
    "is_retired_client",
    "is_retired_target",
    "iter_at_code",
    "lang_list",
    "lost_petal",
    "markdown_to_plain_text",
    "match_kecode",
    "matrix_homeserver_default",
    "matrix_user_default",
    "module",
    "msgchain2image",
    "normalize_button_click_limit",
    "on_bot_config",
    "on_module_config",
    "parse_time_string",
    "patch_url",
    "post_url",
    "proxy",
    "put_url",
    "qq_host_default",
    "random_cache_path",
    "render_at_code",
    "request_url",
    "resolve_table_columns",
    "restart",
    "rickroll",
    "run_sys_command",
    "send_report",
    "settle_petals",
    "should_yield_channel",
    "sign_get_petal",
    "svg_render",
    "templates_to_str",
    "truncate_text",
    "union_mutation",
    "update_stored_list",
    "url_pattern",
    "web_render",
    "weblate_lang_codes",
    "wiki_allowlist_url_default",
    "wrap_sender_id",
]

try:
    # 不依赖配置系统的名字：CLI 与发现层在配置就绪之前即可使用。
    from akaribot.core.builtins.message.mention import InlineMention, iter_at_code, render_at_code, wrap_sender_id
    from akaribot.core.builtins.parser.args import ArgumentPattern, Template, templates_to_str
    from akaribot.core.constants import config_filename, dev_mode
    from akaribot.core.constants.default import (
        confirm_command_default,
        lang_list,
        matrix_homeserver_default,
        matrix_user_default,
        qq_host_default,
        weblate_lang_codes,
        wiki_allowlist_url_default,
    )
    from akaribot.core.constants.exceptions import (
        AbuseWarning,
        ConfigValueError,
        ExternalException,
        InvalidHelpDocTypeError,
        NoReportException,
        SendMessageFailed,
        SessionContextUnavailable,
        SessionFinished,
        TestException,
        WaitCancelException,
    )
    from akaribot.core.constants.info import Info, Secret
    from akaribot.core.i18n import Locale, collect_locale_paths, get_available_locales
    from akaribot.core.queue.errors import RpcError
    from akaribot.core.utils.bash import run_sys_command
    from akaribot.core.utils.cache import random_cache_path
    from akaribot.core.utils.container import ExpiringTempDict, TokenBucket
    from akaribot.core.utils.func import chunk_list, is_float, is_int, parse_time_string, truncate_text
    from akaribot.core.utils.table import escape_table_cell, format_table_code, resolve_table_columns

    # 机器人与会话：模块函数的入参与运行环境。
    from akaribot.core.alive import Alive
    from akaribot.core.builtins.bot import Bot
    from akaribot.core.builtins.session.info import EventInfo, SessionInfo
    from akaribot.core.builtins.session.internal import (
        FetchedMessageSession,
        FinishedSession,
        MessageSession,
        confirm_prompt_key,
    )
    from akaribot.core.builtins.session.lock import ExecutionLockList
    from akaribot.core.builtins.utils import command_prefix, confirm_command

    # 消息元素与消息链：模块回给用户的内容构造块。
    from akaribot.core.builtins.message.chain import (
        Chainable,
        I18NMessageChain,
        MessageChain,
        MessageNodes,
        PlatformMessageChain,
        escape_special_char,
        get_message_chain,
        match_kecode,
    )
    from akaribot.core.builtins.message.elements import (
        ActionTextElement,
        AudioElement,
        BaseElement,
        ButtonElement,
        ButtonFrameElement,
        ButtonPayload,
        ButtonPermission,
        ButtonRows,
        EmbedElement,
        EmbedFieldElement,
        FormattedTimeElement,
        I18NContextElement,
        ImageElement,
        MarkdownElement,
        MentionElement,
        PlainElement,
        RawElement,
        URLElement,
        VideoElement,
        markdown_to_plain_text,
        normalize_button_click_limit,
    )
    from akaribot.core.builtins.message.internal import (
        ActionText,
        Audio,
        Button,
        ButtonFrame,
        Embed,
        EmbedField,
        FormattedTime,
        I18NContext,
        Image,
        Markdown,
        Mention,
        Plain,
        Raw,
        Url,
        Video,
    )

    # 模块注册与解析：声明模块、命令模板与解析钩子。
    from akaribot.core.builtins.parser.command import CommandParser
    from akaribot.core.builtins.parser.hooks import Handled, HookPoint, RecoveryProposal, Stop, StopScope
    from akaribot.core.component import Bind, module
    from akaribot.core.loader import ModulesManager
    from akaribot.core.module_runtime import ModuleRuntimeManager
    from akaribot.core.types import Module, Param
    from akaribot.core.types.module.component_meta import CommandMeta

    # 配置：读取核心配置、声明模块自身配置项。
    from akaribot.core.builtins.converter import converter
    from akaribot.core.config import CFGManager
    from akaribot.core.config.base import BaseConfig, CoreConfig, CoreSecretConfig
    from akaribot.core.config.decorator import on_bot_config, on_module_config

    # 数据库：定义模块模型、声明包内迁移与使用核心数据表。
    from akaribot.core.database import fetch_module_db, get_model_fields, get_model_names
    from akaribot.core.database.base import DBModel
    from akaribot.core.database.migration import MigrationContext
    from akaribot.core.database.models import (
        UNION_SCOPE_SENDER,
        UNION_SCOPE_TARGET,
        AnalyticsData,
        JobQueuesTable,
        MaliciousLoginRecords,
        ModuleStatus,
        SenderUnionBind,
        SenderUnionInfo,
        StoredData,
        TargetUnionBind,
        TargetUnionInfo,
        UnfriendlyActionRecords,
        UnionDeleteBlocked,
        union_mutation,
    )

    # 日志与调度：记录运行信息、注册定时任务。
    from akaribot.core.logger import Logger
    from akaribot.core.scheduler import AndTrigger, CronTrigger, DateTrigger, IntervalTrigger, OrTrigger

    # 进程与队列：跨进程调用服务端动作、上报错误、重启进程。
    from akaribot.core.queue.contracts import ServerAPI
    from akaribot.core.server.terminate import restart
    from akaribot.core.smtp import send_report

    # 工具：网络、随机、缓存、图像、表格、按钮、游戏、经济与 URL 审计。
    from akaribot.core.utils.button import arrange_buttons, build_button_rows
    from akaribot.core.utils.cooldown import CoolDown
    from akaribot.core.utils.dirty_check import check, check_bool, rickroll
    from akaribot.core.utils.game import GAME_EXPIRED, PlayState
    from akaribot.core.utils.http import (
        delete_url,
        download,
        get_url,
        patch_url,
        post_url,
        proxy,
        put_url,
        request_url,
        url_pattern,
    )
    from akaribot.core.utils.image import cb64imglst, get_fontsize, msgchain2image, svg_render
    from akaribot.core.utils.image_table import ImageTable, image_table_render
    from akaribot.core.utils.petal import cost_petal, gained_petal, lost_petal, settle_petals, sign_get_petal
    from akaribot.core.utils.random import Random, SecureRandom
    from akaribot.core.utils.retired import (
        RETIRED_SOURCES,
        RETIRED_TARGETS,
        enqueue_notice,
        is_merge_route_allowed,
        is_module_allowed_when_retired,
        is_retired_client,
        is_retired_target,
        should_yield_channel,
    )
    from akaribot.core.utils.storedata import get_stored_list, update_stored_list
    from akaribot.core.utils.url_audit import (
        GlobalURLAllowlist,
        GlobalURLBlocklist,
        URLRule,
        URLRuleError,
        evaluate_url_policy,
    )
    from akaribot.core.utils.web_render import (
        ElementScreenshotOptions,
        LegacyScreenshotOptions,
        PageScreenshotOptions,
        RawOptions,
        SectionScreenshotOptions,
        SourceOptions,
        check_web_render_status,
        close_web_render,
        init_web_render,
        web_render,
    )
except ConfigFileNotFound:
    # 配置缺失时保留未导入的名字，由 __getattr__ 在首次访问时重试；其余异常照常抛出。
    pass

# 名称到来源模块的映射。仅在配置缺失导致上面的导入中断时使用。
LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "akaribot.core.alive": ("Alive",),
    "akaribot.core.builtins.bot": ("Bot",),
    "akaribot.core.builtins.converter": ("converter",),
    "akaribot.core.builtins.message.chain": (
        "Chainable",
        "I18NMessageChain",
        "MessageChain",
        "MessageNodes",
        "PlatformMessageChain",
        "escape_special_char",
        "get_message_chain",
        "match_kecode",
    ),
    "akaribot.core.builtins.message.elements": (
        "ActionTextElement",
        "AudioElement",
        "BaseElement",
        "ButtonElement",
        "ButtonFrameElement",
        "ButtonPayload",
        "ButtonPermission",
        "ButtonRows",
        "EmbedElement",
        "EmbedFieldElement",
        "FormattedTimeElement",
        "I18NContextElement",
        "ImageElement",
        "MarkdownElement",
        "MentionElement",
        "PlainElement",
        "RawElement",
        "URLElement",
        "VideoElement",
        "markdown_to_plain_text",
        "normalize_button_click_limit",
    ),
    "akaribot.core.builtins.message.internal": (
        "ActionText",
        "Audio",
        "Button",
        "ButtonFrame",
        "Embed",
        "EmbedField",
        "FormattedTime",
        "I18NContext",
        "Image",
        "Markdown",
        "Mention",
        "Plain",
        "Raw",
        "Url",
        "Video",
    ),
    "akaribot.core.builtins.message.mention": ("InlineMention", "iter_at_code", "render_at_code", "wrap_sender_id"),
    "akaribot.core.builtins.parser.args": ("ArgumentPattern", "Template", "templates_to_str"),
    "akaribot.core.builtins.parser.command": ("CommandParser",),
    "akaribot.core.builtins.parser.hooks": ("Handled", "HookPoint", "RecoveryProposal", "Stop", "StopScope"),
    "akaribot.core.builtins.session.info": ("EventInfo", "SessionInfo"),
    "akaribot.core.builtins.session.internal": (
        "FetchedMessageSession",
        "FinishedSession",
        "MessageSession",
        "confirm_prompt_key",
    ),
    "akaribot.core.builtins.session.lock": ("ExecutionLockList",),
    "akaribot.core.builtins.utils": ("command_prefix", "confirm_command"),
    "akaribot.core.component": ("Bind", "module"),
    "akaribot.core.config": ("CFGManager",),
    "akaribot.core.config.base": ("BaseConfig", "CoreConfig", "CoreSecretConfig"),
    "akaribot.core.config.decorator": ("on_bot_config", "on_module_config"),
    "akaribot.core.constants": ("config_filename", "dev_mode"),
    "akaribot.core.constants.default": (
        "confirm_command_default",
        "lang_list",
        "matrix_homeserver_default",
        "matrix_user_default",
        "qq_host_default",
        "weblate_lang_codes",
        "wiki_allowlist_url_default",
    ),
    "akaribot.core.constants.exceptions": (
        "AbuseWarning",
        "ConfigValueError",
        "ExternalException",
        "InvalidHelpDocTypeError",
        "NoReportException",
        "SendMessageFailed",
        "SessionContextUnavailable",
        "SessionFinished",
        "TestException",
        "WaitCancelException",
    ),
    "akaribot.core.constants.info": ("Info", "Secret"),
    "akaribot.core.database": ("fetch_module_db", "get_model_fields", "get_model_names"),
    "akaribot.core.database.base": ("DBModel",),
    "akaribot.core.database.migration": ("MigrationContext",),
    "akaribot.core.database.models": (
        "AnalyticsData",
        "JobQueuesTable",
        "MaliciousLoginRecords",
        "ModuleStatus",
        "SenderUnionBind",
        "SenderUnionInfo",
        "StoredData",
        "TargetUnionBind",
        "TargetUnionInfo",
        "UNION_SCOPE_SENDER",
        "UNION_SCOPE_TARGET",
        "UnfriendlyActionRecords",
        "UnionDeleteBlocked",
        "union_mutation",
    ),
    "akaribot.core.i18n": ("Locale", "collect_locale_paths", "get_available_locales"),
    "akaribot.core.loader": ("ModulesManager",),
    "akaribot.core.logger": ("Logger",),
    "akaribot.core.module_runtime": ("ModuleRuntimeManager",),
    "akaribot.core.queue.contracts": ("ServerAPI",),
    "akaribot.core.queue.errors": ("RpcError",),
    "akaribot.core.scheduler": ("AndTrigger", "CronTrigger", "DateTrigger", "IntervalTrigger", "OrTrigger"),
    "akaribot.core.server.terminate": ("restart",),
    "akaribot.core.smtp": ("send_report",),
    "akaribot.core.types": ("Module", "Param"),
    "akaribot.core.types.module.component_meta": ("CommandMeta",),
    "akaribot.core.utils.bash": ("run_sys_command",),
    "akaribot.core.utils.button": ("arrange_buttons", "build_button_rows"),
    "akaribot.core.utils.cache": ("random_cache_path",),
    "akaribot.core.utils.container": ("ExpiringTempDict", "TokenBucket"),
    "akaribot.core.utils.cooldown": ("CoolDown",),
    "akaribot.core.utils.dirty_check": ("check", "check_bool", "rickroll"),
    "akaribot.core.utils.func": ("chunk_list", "is_float", "is_int", "parse_time_string", "truncate_text"),
    "akaribot.core.utils.game": ("GAME_EXPIRED", "PlayState"),
    "akaribot.core.utils.http": (
        "delete_url",
        "download",
        "get_url",
        "patch_url",
        "post_url",
        "proxy",
        "put_url",
        "request_url",
        "url_pattern",
    ),
    "akaribot.core.utils.image": ("cb64imglst", "get_fontsize", "msgchain2image", "svg_render"),
    "akaribot.core.utils.image_table": ("ImageTable", "image_table_render"),
    "akaribot.core.utils.petal": ("cost_petal", "gained_petal", "lost_petal", "settle_petals", "sign_get_petal"),
    "akaribot.core.utils.random": ("Random", "SecureRandom"),
    "akaribot.core.utils.retired": (
        "RETIRED_SOURCES",
        "RETIRED_TARGETS",
        "enqueue_notice",
        "is_merge_route_allowed",
        "is_module_allowed_when_retired",
        "is_retired_client",
        "is_retired_target",
        "should_yield_channel",
    ),
    "akaribot.core.utils.storedata": ("get_stored_list", "update_stored_list"),
    "akaribot.core.utils.table": ("escape_table_cell", "format_table_code", "resolve_table_columns"),
    "akaribot.core.utils.url_audit": (
        "GlobalURLAllowlist",
        "GlobalURLBlocklist",
        "URLRule",
        "URLRuleError",
        "evaluate_url_policy",
    ),
    "akaribot.core.utils.web_render": (
        "ElementScreenshotOptions",
        "LegacyScreenshotOptions",
        "PageScreenshotOptions",
        "RawOptions",
        "SectionScreenshotOptions",
        "SourceOptions",
        "check_web_render_status",
        "close_web_render",
        "init_web_render",
        "web_render",
    ),
}

_LAZY_INDEX: dict[str, str] = {name: path for path, names in LAZY_MODULES.items() for name in names}


def __getattr__(name: str) -> Any:
    """按来源索引导入单个门面名字。

    配置在导入期不可用时模块层的导入整体中断，未绑定的名字在此重试；重试仍失败则原样抛出
    ``ConfigFileNotFound``，让调用方看到真实原因。解析结果写回模块命名空间，后续访问不再
    经过本函数。

    :param name: 门面名字。
    :return: 名字对应的对象。
    :raises AttributeError: 该名字不在门面承诺的清单内。
    """
    module_path = _LAZY_INDEX.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module_path), name)
    globals()[name] = value
    return value
