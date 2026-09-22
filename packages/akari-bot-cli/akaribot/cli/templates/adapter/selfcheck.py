"""适配器生成物自检。

对 `akaribot new adapter` 的生成目录做机器可判定的检查：ruff check / ruff format（仓库配置与
ruff 默认配置各跑一遍）、tomllib 解析 pyproject.toml 与 manifest.toml、entry point 名不含
连字符、core 约束字面一致，以及导入面只用 `akaribot.core.api` 门面。

本文件是模板维护工具，由生成器跳过，不随生成物分发。

用法：
    .venv/bin/python templates/adapter/selfcheck.py <生成目录> [...]
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_RUFF = PROJECT_ROOT / ".venv/bin/ruff"
EXPECTED_CORE = "akari-bot-core>=0.1.0,<1.0"
ALLOWED_IMPORT_PREFIX = "akaribot.core.api"
DEEP_CORE_PATH = re.compile(r"akaribot\.core\.(?!api(\.|$))")
PACKAGE_GLOB = "akari-bot-adapter-*"
SKELETON_FILES = ("info.py", "features.py", "context.py", "bot.py")

failures: list[str] = []


def report(label: str, ok: bool, detail: str = "") -> None:
    """打印一条检查结果并记录失败项。"""
    print(f"{'PASS' if ok else 'FAIL'}  {label}{'：' + detail if detail else ''}")
    if not ok:
        failures.append(label)


def ruff_binary() -> str:
    """取 ruff 可执行文件，优先仓库虚拟环境内的那份。"""
    return str(REPO_RUFF) if REPO_RUFF.is_file() else "ruff"


def ruff(arguments: list[str], files: list[Path]) -> tuple[bool, str]:
    """对一组文件跑 ruff，返回是否通过与合并后的输出。"""
    result = subprocess.run(
        [ruff_binary(), *arguments, *map(str, files)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip().replace("\n", " | ")


def core_imports(tree: ast.AST) -> list[str]:
    """列出源码里出现的 akaribot.core 导入路径。"""
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names if alias.name.startswith("akaribot.core"))
        elif (
            isinstance(node, ast.ImportFrom)
            and node.level == 0
            and node.module
            and node.module.startswith("akaribot.core")
        ):
            found.append(node.module)
    return found


def check_layout(package: Path) -> Path:
    """断言骨架文件齐全，返回导入包目录。"""
    stem = package.name.removeprefix("akari-bot-adapter-")
    source = package / "akaribot/adapters" / stem
    missing = [name for name in SKELETON_FILES if not (source / name).is_file()]
    report(f"{package.name} 骨架文件齐全", not missing, ",".join(missing))
    return source


def check_metadata(package: Path) -> None:
    """检查 pyproject 与 manifest 的解析结果与关键字段。"""
    project = tomllib.loads((package / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    entry_points = project["entry-points"]["akaribot.adapters"]
    stem = package.name.removeprefix("akari-bot-adapter-")
    report("entry point 只有一个", len(entry_points) == 1, str(dict(entry_points)))
    for name, value in entry_points.items():
        report(f"entry point 名不含连字符（{name}）", "-" not in name)
        report(f"entry point 指向导入路径（{value}）", value == f"akaribot.adapters.{stem}")
    report("core 约束字面一致", EXPECTED_CORE in project["dependencies"], str(project["dependencies"]))

    manifest = tomllib.loads((package / "akaribot/adapters" / stem / "manifest.toml").read_text(encoding="utf-8"))
    report("manifest 非空", bool(manifest), str(sorted(manifest)))
    report("manifest 声明 schema", manifest.get("schema") == 1, str(manifest.get("schema")))
    report("manifest 声明 requires_core_api", manifest.get("requires_core_api") == ">=1")
    report("manifest 声明 locales", manifest.get("locales") == "locales")


def check_package(package: Path) -> None:
    """检查一个生成的适配器包。"""
    print(f"\n=== {package.name} ===")
    python_files = sorted(package.rglob("*.py"))
    for label, arguments in (
        ("ruff check（ruff 默认配置）", ["check", "--isolated"]),
        ("ruff format --check（ruff 默认配置）", ["format", "--check", "--isolated"]),
        ("ruff check（仓库配置）", ["check", "--config", str(PROJECT_ROOT / "pyproject.toml")]),
        (
            "ruff format --check（仓库配置）",
            ["format", "--check", "--config", str(PROJECT_ROOT / "pyproject.toml")],
        ),
    ):
        ok, output = ruff(arguments, python_files)
        report(f"{package.name} {label}", ok, output)

    check_metadata(package)
    check_layout(package)
    for python_file in python_files:
        tree = ast.parse(python_file.read_text(encoding="utf-8"))
        for module in core_imports(tree):
            report(
                f"{python_file.relative_to(package)} 导入面（{module}）",
                module.startswith(ALLOWED_IMPORT_PREFIX) and not DEEP_CORE_PATH.search(module),
            )


def main() -> int:
    """入口：逐个检查命令行给出的生成目录。返回进程退出码。"""
    targets = [Path(argument).resolve() for argument in sys.argv[1:]]
    if not targets:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    packages: list[Path] = []
    for target in targets:
        packages.extend(sorted(path for path in target.glob(PACKAGE_GLOB) if path.is_dir()))
    if not packages:
        print(f"{', '.join(map(str, targets))} 下没有 {PACKAGE_GLOB} 目录。", file=sys.stderr)
        return 2
    for package in packages:
        check_package(package)
    print(f"\n检查 {len(packages)} 个生成包：失败 {len(failures)} 项")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
