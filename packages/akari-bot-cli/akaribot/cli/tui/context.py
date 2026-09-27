"""界面当前操作的实例。

界面可以管理本机多个实例，故「现在管理哪一个」必须有一处共享状态：各页的数据源在取数时读它，
而不是在构造时把实例根固定下来。显式给定的根（自检、用例注入）优先级最高，其次才是这里选中的，
最后回落到按环境变量与向上查找自动定位。
"""

from __future__ import annotations

from pathlib import Path

from akaribot.cli.instance import default_instance_root

_active_root: Path | None = None


def active_root() -> Path | None:
    """返回界面当前选中的实例根；未选过时为 ``None``。"""
    return _active_root


def set_active_root(root: Path | str | None) -> None:
    """设置界面当前操作的实例。

    :param root: 实例根；``None`` 表示回到自动定位。
    """
    global _active_root
    _active_root = Path(root).expanduser().resolve() if root is not None else None


def resolve_root(explicit: Path | str | None = None) -> Path:
    """解析实例根：显式给定 > 界面当前选中 > 环境变量与向上查找 > 当前目录。

    :param explicit: 构造数据源时显式给定的根。
    :return: 实例根绝对路径。
    """
    if explicit is not None:
        return Path(explicit).expanduser().resolve()
    found = active_root()
    if found is not None:
        return found
    return default_instance_root()
