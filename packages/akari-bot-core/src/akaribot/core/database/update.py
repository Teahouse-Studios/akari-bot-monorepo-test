"""数据库升级的兼容入口。

v1→v6 的升级逻辑与旧版本号转换已整体移入 :mod:`core.database.legacy`，按包登记的 revision
由 :mod:`core.database.migration` 执行。本模块只为既有的 ``from core.database.update import
update_database`` 导入点保留，不再承载任何迁移步骤。
"""

from core.database.legacy import update_database

__all__ = ["update_database"]
