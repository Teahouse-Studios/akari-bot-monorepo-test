"""根目录兼容实现：把 ``python tester.py`` 转发到 :mod:`akaribot.testing.runner`。

既有 CI 与文档仍以根目录脚本为入口（.github/workflows/run-builtin-tester.yml、CONTRIBUTING.md），
故保留本文件。它只做两件事：把自身所在的仓库根显式告知 runner，再转到同一份实现。新脚本与
安装形态请改用 ``python -m akaribot.testing``。
"""

import os
import sys
from pathlib import Path

# 该文件位于仓库根目录，仓库根目录由调用方显式传入，runner 不需要再从自身位置反推。
# 变量名必须与 akaribot.testing.runner.REPO_ROOT_ENV 一致，取值必须早于该模块的导入。
os.environ.setdefault("AKARI_REPO_ROOT", str(Path(__file__).resolve().parent))

from akaribot.testing import runner as _runner  # noqa: E402

if __name__ == "__main__":
    sys.exit(_runner.run())

# 使用模块别名而非逐个再导出，因为 conftest.py 与包内测试会 patch tester 模块的属性，别名可以使对应补丁
# 与 runner 的全局状态指向同一对象（tester.py 与 runner 属于同一模块）。
else:
    sys.modules[__name__] = _runner
