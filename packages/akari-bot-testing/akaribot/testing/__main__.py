"""``python -m akaribot.testing`` 的入口。

测试配置的初始化发生在 :mod:`akaribot.testing.runner` 的导入期，且必须早于任何
``akaribot.core`` 导入，因此该模块仅做转发，不在导入期触碰 core（参见 ``__init__.py``）。
"""

import sys

from .runner import run

if __name__ == "__main__":
    sys.exit(run())
