"""数据库升级的兼容入口。

v1→v6 的升级逻辑与旧版本号转换由 :mod:`core.database.legacy` 承载，按包注册的 revision
由 :mod:`core.database.migration` 执行。本模块只提供既有的 ``from core.database.update
import update_database`` 导入点，不含迁移步骤。
"""

from akaribot.core.database.legacy import update_database

__all__ = ["update_database"]
