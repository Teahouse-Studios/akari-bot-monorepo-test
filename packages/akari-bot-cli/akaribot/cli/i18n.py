"""CLI 与 TUI 的本地化。

CLI 不依赖 core，故直接用发布在 PyPI 的 ``akari-bot-i18n``。``zh_cn`` 是唯一手工编辑的真源，
其余语言缺键时按回退链取值——与仓库既有约定一致：其余语言交给 Weblate，本仓库只维护 zh_cn。
语言文件是包内资源，经 ``importlib.resources`` 定位，冻结或 wheel 安装后仍可读。
"""

from __future__ import annotations

import os
import sys
from importlib.resources import files
from typing import Any

from akari_bot_i18n.i18n import Locale, build_locale_snapshot, connect_locale_snapshot

# 与 core 的 lang_list 同集合；新增语言时两边一起加。
SUPPORTED_LOCALES = ("zh_cn", "zh_tw", "en_us", "ja_jp", "ko_kr")
DEFAULT_LOCALE = "zh_cn"
# 缺键时的回退顺序：先英文，再真源。
FALLBACK_LOCALES = ("en_us", "zh_cn")

LOCALE_ENV = "AKARIBOT_LANG"
_NAMESPACE = "akaribot-cli"

_connected = False
_cache: dict[str, Locale] = {}


def locales_dir() -> str:
    """返回语言文件所在目录。

    :return: 目录路径字符串。
    """
    return str(files("akaribot.cli").joinpath("locales"))


def normalize(value: str | None) -> str:
    """把各种写法归一为受支持的语言码。

    接受 ``zh-CN``、``zh_CN.UTF-8``、``en`` 这类系统 locale 写法。

    :param value: 原始语言标识。
    :return: 受支持的语言码；无法识别时返回默认语言。
    """
    if not value:
        return DEFAULT_LOCALE
    text = value.split(".")[0].split("@")[0].replace("-", "_").strip()
    if text in SUPPORTED_LOCALES:
        return text
    lowered = text.lower()
    for code in SUPPORTED_LOCALES:
        if lowered == code or lowered.startswith(f"{code.split('_')[0]}_"):
            return code
    # 只给了主语言时取该语言的第一个变体（en → en_us，zh → zh_cn）。
    for code in SUPPORTED_LOCALES:
        if lowered == code.split("_")[0]:
            return code
    return DEFAULT_LOCALE


def resolve_locale(explicit: str | None = None, instance_locale: str | None = None) -> str:
    """按优先级确定界面语言。

    顺序为 ``--lang`` → ``AKARIBOT_LANG`` → 实例 ``akaribot.toml`` 的 locale → 系统 ``LC_ALL`` /
    ``LANG`` → 默认语言。

    :param explicit: 命令行显式给出的语言。
    :param instance_locale: 实例元数据里的语言。
    :return: 受支持的语言码。
    """
    for candidate in (
        explicit,
        os.environ.get(LOCALE_ENV),
        instance_locale,
        os.environ.get("LC_ALL"),
        os.environ.get("LANG"),
    ):
        if candidate:
            return normalize(candidate)
    return DEFAULT_LOCALE


def _connect() -> None:
    """接上语言快照，只做一次。"""
    global _connected
    if _connected:
        return
    build_locale_snapshot(list(SUPPORTED_LOCALES), [locales_dir()], _NAMESPACE)
    connect_locale_snapshot(_NAMESPACE)
    _connected = True


def locale(code: str | None = None) -> Locale:
    """取指定语言的 :class:`Locale`。

    :param code: 语言码；缺省用当前解析结果。
    :return: 可直接 ``.t()`` 的对象。
    """
    _connect()
    resolved = normalize(code) if code else _current()
    if resolved not in _cache:
        _cache[resolved] = Locale(resolved, fallback_lng=[code for code in FALLBACK_LOCALES if code != resolved])
    return _cache[resolved]


_current_code = DEFAULT_LOCALE


def set_locale(code: str | None) -> str:
    """设置本次进程使用的语言。

    :param code: 语言码或系统 locale 写法。
    :return: 实际生效的语言码。
    """
    global _current_code
    _current_code = normalize(code)
    return _current_code


def current_locale() -> str:
    """返回当前语言码。"""
    return _current_code


def _argv_locale() -> str | None:
    """从命令行里嗅探 ``--lang``。

    typer 的 ``help=`` 在**导入期**求值，而根回调要等参数解析完才执行，故只靠 ``set_locale()``
    无法本地化 ``--help``。这里提前读一次 argv，使导入期取到的就是用户要的语言。

    :return: 嗅探到的语言码；未给出时为 ``None``。
    """
    argv = sys.argv[1:]
    for index, item in enumerate(argv):
        if item == "--lang" and index + 1 < len(argv):
            return argv[index + 1]
        if item.startswith("--lang="):
            return item.split("=", 1)[1]
    return None


def _current() -> str:
    """取当前语言码，未显式设置时按 argv 与环境解析一次。"""
    global _current_code
    if _current_code == DEFAULT_LOCALE:
        _current_code = resolve_locale(_argv_locale())
    return _current_code


def t(key: str, **kwargs: Any) -> str:
    """取本地化文案。

    :param key: 文案键，形如 ``cli.module.add.help``。
    :param kwargs: 插值参数。
    :return: 本地化后的文本；键不存在时回退链仍取不到则返回键名。
    """
    return locale().t(key, **kwargs)
