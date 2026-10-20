"""把 workspace 全部分发切到同一批次版本，用于 TestPyPI 重复演练。

首次候选用各包 pyproject 里声明的版本（当前均为 ``0.1.0``）。同名文件在 TestPyPI 上不能覆盖，
因此代码改动后重跑演练需要换批次版本：本工具把全部 workspace 分发的 ``version`` 改成给定值
（例如 ``0.1.0.post1``），内部依赖约束 ``>=0.1.0,<1.0`` 继续成立，无需改动依赖声明。

用法：::

    python tools/set_batch_version.py 0.1.0.post1
    python tools/set_batch_version.py 0.1.0.post1 --dry-run
    git checkout -- packages            # 本地演练结束后恢复

CI 在一次性 checkout 里运行，不需要恢复。
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_LINE = re.compile(r'^version = "[^"]*"$', re.MULTILINE)


def workspace_pyprojects() -> list[Path]:
    """列出 workspace 内全部成员包的 pyproject。

    :return: pyproject 路径列表。
    """
    return sorted((REPO_ROOT / "packages").glob("**/pyproject.toml"))


def set_version(path: Path, version: str, dry_run: bool) -> str:
    """改一个 pyproject 的 project.version。

    :param path: pyproject 路径。
    :param version: 目标版本。
    :param dry_run: 只报告不写入。
    :return: 原版本。
    """
    text = path.read_text(encoding="utf-8")
    project = tomllib.loads(text).get("project", {})
    current = project.get("version")
    if not current:
        raise SystemExit(f"{path} 缺少 project.version")
    if VERSION_LINE.search(text) is None:
        raise SystemExit(f"{path} 的 version 行格式不受支持")
    if not dry_run:
        updated = VERSION_LINE.sub(f'version = "{version}"', text, count=1)
        path.write_text(updated, encoding="utf-8")
    return current


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(description="把全部分发切到同一批次版本。")
    parser.add_argument("version", help="目标版本，如 0.1.0.post1")
    parser.add_argument("--dry-run", action="store_true", help="只列出将改动的包")
    args = parser.parse_args(argv)

    files = workspace_pyprojects()
    if not files:
        print("没有发现 packages/ 下的 pyproject", file=sys.stderr)
        return 1
    changed = 0
    for path in files:
        current = set_version(path, args.version, args.dry_run)
        if current != args.version:
            changed += 1
            print(f"{path.relative_to(REPO_ROOT)}: {current} -> {args.version}")
    action = "将改动" if args.dry_run else "已改动"
    print(f"{action} {changed} 个分发（共 {len(files)} 个）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
