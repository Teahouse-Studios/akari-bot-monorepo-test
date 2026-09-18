from akari_bot_i18n.i18n import (
    Locale,
    build_locale_snapshot,
    connect_locale_snapshot,
    get_available_locales,
    safe_strftime,
)

__all__ = [
    "Locale",
    "build_locale_snapshot",
    "collect_locale_paths",
    "connect_locale_snapshot",
    "get_available_locales",
    "safe_strftime",
]


def collect_locale_paths() -> list[str]:
    """收集全部 locale 目录。

    由发现层给出，而非在导入期 glob 目录：安装为 wheel 之后不再存在
    ``./modules/*/locales`` 这样的路径，导入期 glob 会得到空列表，全部文案退化为键名。

    :return: locale 目录路径列表，核心的目录排在最前。
    """
    from core.registry import PackageRegistry

    return PackageRegistry.locales_paths()
