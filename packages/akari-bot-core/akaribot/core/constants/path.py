"""路径常量。

取值一律由 :class:`core.paths.Paths` 提供 —— 那里是「实例目录在哪里」的唯一答案。
本模块保留模块级常量名，是为了让既有的 ``from core.constants.path import ...`` 无需改动；
新增代码应直接使用 :class:`core.paths.Paths`。

取值在**导入期**完成，故 ``AKARI_INSTANCE_DIR``、``AKARI_CONFIG_PATH``、
``AKARI_UNION_MERGE_LOGS_PATH`` 须在任何 ``core.*`` 导入之前置位，否则被固化为默认值且不报错。
引导代码只能以字面量重复这些名称，``tester.py`` / ``tests/run_one.py`` / ``conftest.py`` 即如此。
"""

import os
from pathlib import Path

from akaribot.core.paths import CONFIG_PATH_ENV, INSTANCE_DIR_ENV, Paths  # noqa: F401

# 配置只读模式的环境变量名：守护进程 spawn 子进程前置位，pre-init 进程清除。
# 该常量须位于不依赖 core.config 的模块，以免提前触发导入期版本迁移。
CONFIG_READONLY_ENV = "AKARI_CONFIG_READONLY"

# union 合并日志目录的环境变量名，测试引导据此写入临时目录。
# 取值发生在导入期，引导代码须以字面量重复该名称。
UNION_MERGE_LOGS_PATH_ENV = "AKARI_UNION_MERGE_LOGS_PATH"

# 基本路径
assets_path = Paths.assets
bots_path = Paths.instance / "bots"
cache_path = Paths.cache
config_path = Paths.config
data_path = Paths.data
database_path = Paths.database
base_locales_path = Paths.instance / "core" / "locales"
logs_path = Paths.logs
modules_path = Paths.instance / "modules"
tests_path = Paths.tests

# assets 只放随仓库分发的只读内容，运行时与部署者产生的内容一律写进 data。目录创建不在
# 此处发生，否则只读取版本号的调用也会在当前目录留下副作用；使用方经 Paths.ensure() 创建。

# assets 子路径（只读）
fonts_path = assets_path / "fonts"
# 模板随 core wheel 分发（akaribot/core/assets/templates）；实例的 assets/templates 存在时优先，
# 便于部署者覆盖。打包形态下 __file__ 与包内资源都可用，故直接由包位置推导。
_PACKAGE_TEMPLATES_PATH = Path(__file__).resolve().parents[1] / "assets" / "templates"
templates_path = assets_path / "templates" if (assets_path / "templates").is_dir() else _PACKAGE_TEMPLATES_PATH

# data 子路径（可写）
filter_words_path = data_path / "filter_words"
retired_path = data_path / "retired"
union_merge_logs_path = Path(os.environ.get(UNION_MERGE_LOGS_PATH_ENV) or data_path / "union_merge_logs").resolve()
url_audit_data_path = data_path / "url_audit"

# 字体文件路径的三个常量已弃用：字体随 akari-bot-assets-fonts 分发，路径不再固定，取值一律改用
# akaribot.core.api.find_font()。下面的映射只为兼容既有 import 保留，取用时才查找，找不到即抛错。
_DEPRECATED_FONT_CONSTANTS = {
    "noto_sans_bold_path": "Noto Sans CJK Bold.otf",
    "noto_sans_demilight_path": "Noto Sans CJK DemiLight.otf",
    "noto_sans_symbol_path": "Noto Sans Symbols2 Regular.ttf",
}


def __getattr__(name: str) -> Path:
    """
    已弃用字体常量的取用口，替代品为 ``akaribot.core.api.find_font``。

        惰性导入避免导入期多拉一层依赖：字体查找要用 importlib.resources 与 matplotlib，而本模块
        在引导阶段就被读入。

        :param name: 常量名。
        :return: 字体文件路径。
        :raises AttributeError: 名字不在已弃用清单内。
    """
    # 惰性导入避免导入期多拉一层依赖：字体查找要用 importlib.resources 与 matplotlib，而本模块
    # 在引导阶段就被读入。
    font_name = _DEPRECATED_FONT_CONSTANTS.get(name)
    if font_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from akaribot.core.utils.font import find_font

    return find_font(font_name)


class PrivateData:
    """客户端私有资源目录，存放需要跨重启保留的运行时文件。

    ``path`` 是普通类属性，首次使用前须调用 :meth:`ensure`；不设访问器属性是为了让
    检测工具能从 ``path`` 的赋值处看到它是目录。使用方包括 ``bot.py`` 的
    ``pre_init()``（启动时创建）与 :meth:`set`。
    """

    path = data_path / "private" / "default"

    @classmethod
    def ensure(cls) -> Path:
        """创建私有目录并返回其路径。"""
        cls.path.mkdir(parents=True, exist_ok=True)
        return cls.path

    @classmethod
    def set(cls, path: str | Path):
        path_ = Path(path).resolve()
        path_.mkdir(parents=True, exist_ok=True)
        cls.path = path_


def module_data_path(module_dir: str | Path) -> Path:
    """取模块的可写数据目录，不创建它。

    已弃用：模块包的可写数据一律经 :meth:`core.registry.PackageRegistry.package_data` 取实例
    ``data`` 目录；包内 ``data`` 在只读部署与 wheel 安装下均不可写。本函数仅为兼容既有调用保留。

    不在此处建目录：调用方常在导入期取路径，而导入期建目录会让只读安装（``chmod a-w`` 或
    wheel）下的 ``import`` 本身抛 ``PermissionError``。目录由写入方在使用时创建。

    :param module_dir: 模块根目录，例如 ``Path(__file__).parent``。
    :return: 数据目录路径，可能尚不存在。
    """
    return Path(module_dir).resolve() / "data"
