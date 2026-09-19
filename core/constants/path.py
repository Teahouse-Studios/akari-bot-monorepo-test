"""路径常量。

取值一律由 :class:`core.paths.Paths` 提供 —— 那里是「实例目录在哪里」的唯一答案。
本模块保留模块级常量名，是为了让既有的 ``from core.constants.path import ...`` 无需改动；
新增代码应直接使用 :class:`core.paths.Paths`。
"""

import os
from pathlib import Path

from core.paths import CONFIG_PATH_ENV, INSTANCE_DIR_ENV, Paths  # noqa: F401

# 配置只读模式的环境变量名。守护进程在 spawn bot 与 server 子进程前置位，
# pre-init 进程则清除此标记，以保证配置迁移与缺失项补全只发生在该进程中。
# 该常量必须位于不依赖 core.config 的模块：若为取得常量而提前导入 core.config，
# 其导入期版本迁移会在 i18n 快照初始化之前执行。
CONFIG_READONLY_ENV = "AKARI_CONFIG_READONLY"

# union 合并日志目录的环境变量名。测试引导据此把测试合成的合并记录写进临时目录，
# 不让它们随着每次测试运行堆积在开发者的 data/ 中。
# 与 CONFIG_PATH_ENV 同理，此处的取值发生在导入期，引导代码须先于 core 导入置位，
# 故该名称在 tester.py 与 tests/run_one.py 中各以字面量重复了一次。
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
templates_path = assets_path / "templates"
url_audit_assets_path = assets_path / "url_audit"

# data 子路径（可写）
bad_words_path = data_path / "bad_words"
retired_path = data_path / "retired"
union_merge_logs_path = Path(os.environ.get(UNION_MERGE_LOGS_PATH_ENV) or data_path / "union_merge_logs").resolve()
url_audit_data_path = data_path / "url_audit"

# 字体文件路径
noto_sans_bold_path = fonts_path / "Noto Sans CJK Bold.otf"
noto_sans_demilight_path = fonts_path / "Noto Sans CJK DemiLight.otf"
noto_sans_symbol_path = fonts_path / "Noto Sans Symbols2 Regular.ttf"


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

    模块内的 ``assets`` 只放随仓库分发的只读内容；下载所得的资源、运行时生成的索引等
    应写入模块的 ``data`` 目录。

    **不在此处建目录**：模块常在导入期调用本函数，而导入期建目录会使只读安装
    （包目录 ``chmod a-w`` 或 wheel 安装）下 ``import`` 本身抛 ``PermissionError``，
    模块连加载都失败。目录由写入方在使用时创建。

    :param module_dir: 模块根目录，例如 ``Path(__file__).parent``。
    :return: 数据目录路径，可能尚不存在。
    """
    return Path(module_dir).resolve() / "data"
