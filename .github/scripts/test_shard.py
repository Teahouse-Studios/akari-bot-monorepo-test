"""输出某一分片应当执行的测试文件。

CI 把全量用例拆到多个 job 并行执行。分片规则是按文件在收集顺序中的序号取模，新增用例文件自动落入某个
分片，不需要维护分片清单。收集范围与 runner 的 ``_test_roots`` 一致（仓库根目录的 ``tests/`` 与各成员包
的 ``tests/``），否则分片会遗漏默认运行覆盖到的测试文件。

用法：
    python .github/scripts/test_shard.py --shard 1 --total 8
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_ROOT_PATTERNS = ("tests", "packages/*/tests", "packages/*/*/tests")
INTEGRATION_DIR = REPO_ROOT / "tests" / "integration"


def collect_test_files() -> list[str]:
    """按仓库相对路径列出全部测试文件，顺序固定。

    runner 收集 ``tests/integration`` 时跳过 ``_`` 与 ``.`` 开头的文件，其余测试根目录整份收集。此处
    沿用同一规则，否则分片会执行默认运行根本不加载的文件。

    :return: 测试文件路径，已排序。
    """
    files = {
        path
        for pattern in TEST_ROOT_PATTERNS
        for path in REPO_ROOT.glob(f"{pattern}/**/*.py")
        if not (path.name.startswith(("_", ".")) and INTEGRATION_DIR in path.parents)
    }
    return [str(path.relative_to(REPO_ROOT)) for path in sorted(files)]


def main() -> int:
    """打印本分片的文件路径，空分片返回非 0，使调用方显式失败。

    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(description="输出某一分片应当执行的测试文件")
    parser.add_argument("--shard", type=int, required=True, help="分片序号，从 1 开始")
    parser.add_argument("--total", type=int, required=True, help="分片总数")
    args = parser.parse_args()
    if args.total < 1 or not 1 <= args.shard <= args.total:
        parser.error(f"分片序号超出范围：{args.shard}/{args.total}")

    selected = collect_test_files()[args.shard - 1 :: args.total]
    if not selected:
        print("分片没有选中任何测试文件，分片数多于文件数。", file=sys.stderr)
        return 1
    for path in selected:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
