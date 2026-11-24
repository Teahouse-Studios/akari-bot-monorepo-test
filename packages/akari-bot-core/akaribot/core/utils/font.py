"""字体查找：资源包、实例 data、系统字体三级回退。

模块包经 :func:`find_font` 取字体路径，不依赖 ``assets/fonts`` 这类相对仓库布局的常量：字体由
``akari-bot-assets-fonts`` 分发，源码克隆与 wheel 安装两种形态下的位置不同。

三级顺序固定为资源包、``Paths.data/fonts``（部署者自备）、系统字体。三级都取不到时抛
:class:`FontNotFoundError`，其消息给出三条修复路径，而不是让 ``ImageFont.truetype`` 抛出未包装的 ``OSError``。
"""

from __future__ import annotations

from pathlib import Path

from akaribot.core.paths import Paths

# 字体资源包与用户自定义字体的目录名称。资源包通过 ``fonts_dir()`` 声明资源根目录，此处不假定其内部布局。
ASSETS_PACKAGE = "akaribot.assets.fonts"
FONTS_DIR_NAME = "fonts"

# CJK 字族候选按顺序选取首个匹配项，Docker 镜像安装的 fonts-noto-cjk 位于最前，其后是各平台内置的字体族。
_CJK_FAMILIES = (
    "Noto Sans CJK JP",
    "Noto Sans CJK SC",
    "Noto Sans CJK TC",
    "Noto Sans SC",
    "Source Han Sans SC",
    "PingFang SC",
    "PingFang HK",
    "Hiragino Sans GB",
    "Microsoft YaHei",
    "STHeiti",
    "WenQuanYi Zen Hei",
    "Arial Unicode MS",
)

# 符号字族候选仅收录同类字族，避免回退至缺少汉字字形的默认字族时将中文渲染为方框。
_SYMBOL_FAMILIES = ("Noto Sans Symbols 2", "Noto Sans Symbols2", "Apple Symbols", "Segoe UI Symbol")

# 已知字体名称至系统字族候选的映射。未收录的名称仅在资源包与实例 data 两级目录中查找。
SYSTEM_FAMILIES: dict[str, tuple[str, ...]] = {
    "Noto Sans CJK Bold.otf": _CJK_FAMILIES,
    "Noto Sans CJK DemiLight.otf": _CJK_FAMILIES,
    "Noto Sans Symbols2 Regular.ttf": _SYMBOL_FAMILIES,
}


class FontNotFoundError(FileNotFoundError):
    """三级回退都没有取到字体。

    继承 ``FileNotFoundError`` 是为了兼容既有调用方：它同时是 ``OSError``，``except OSError``
    照常捕获。消息含修复指引，这一点是 ``ImageFont.truetype`` 抛出的 ``OSError`` 不具备的。
    """


def _from_assets_package(name: str) -> Path | None:
    # 资源包属于可选依赖，因此按名称按需导入，出现 ImportError 即判定该级不可用，core 的依赖清单不变。
    try:
        from akaribot.assets.fonts import fonts_dir
    except ImportError:
        return None
    candidate = fonts_dir() / name
    return candidate if candidate.is_file() else None


def _from_instance_data(name: str) -> Path | None:
    candidate = Paths.data / FONTS_DIR_NAME / name
    return candidate if candidate.is_file() else None


def _from_system_fonts(name: str) -> Path | None:
    families = SYSTEM_FAMILIES.get(name)
    if not families:
        return None
    try:
        from matplotlib import font_manager
    except ImportError:
        return None
    for family in families:
        try:
            # fallback_to_default=False 用于在未匹配时抛出 ValueError，避免静默回退至 DejaVu Sans。
            found = font_manager.findfont(font_manager.FontProperties(family=family), fallback_to_default=False)
        except ValueError:
            continue
        return Path(found)
    return None


def find_font(name: str) -> Path:
    """取字体文件路径，按资源包、实例 data、系统字体三级回退。

    :param name: 字体文件名，如 ``"Noto Sans CJK DemiLight.otf"``，系统一级只认 :data:`SYSTEM_FAMILIES`
        收录的名字，未收录的名字仅前两级可命中。
    :return: 字体文件路径。
    :raises FontNotFoundError: 三级都没有该字体。
    """
    for finder in (_from_assets_package, _from_instance_data, _from_system_fonts):
        found = finder(name)
        if found is not None:
            return found
    user_dir = Paths.data / FONTS_DIR_NAME
    raise FontNotFoundError(
        f"未找到字体「{name}」。已依次查找资源包 {ASSETS_PACKAGE}、{user_dir} 与系统字体。"
        f"修复方式任选其一：安装字体资源包（pip install akari-bot-assets-fonts）；"
        f"把字体文件放入 {user_dir}/；安装系统字体（Debian/Ubuntu 为 apt-get install fonts-noto-cjk）。"
    )
