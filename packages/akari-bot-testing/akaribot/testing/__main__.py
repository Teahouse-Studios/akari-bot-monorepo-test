"""``python -m akaribot.testing`` 的入口。

测试配置的铺设发生在 :mod:`akaribot.testing.runner` 的导入期，且必须早于任何
``akaribot.core`` 导入，故本模块只做转发，不在导入期触碰 core（见 ``__init__.py``）。
"""

import sys

from .runner import run

if __name__ == "__main__":
    sys.exit(run())
