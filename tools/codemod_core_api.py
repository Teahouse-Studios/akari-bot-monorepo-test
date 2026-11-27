"""把模块包与适配器包里的 core 深路径 import 改为从 ``akaribot.core.api`` 公开接口导入。

模块包与适配器包虽然已独立发包，却仍大范围绑定 core 的内部目录。core 内部一旦重构，这些包就需要同步
修改。公开接口 :mod:`akaribot.core.api` 已经承诺了其中绝大多数符号，其余符号尚未迁移到公开接口。

判定以**逐个符号的对象同一性核对**为准。``akaribot.core.api.<名>`` 必须与
``akaribot.core.<深路径>.<名>`` 为同一对象，才允许改写。名字相同但对象不同（例如两处各定义一个
同名类）时保持原样，避免静默替换语义。尚未收录于公开接口的符号也保持原样，其去留属于公开 API 决策，
不由本工具处理。

用法：
    python tools/codemod_core_api.py            # 仅报告，不改文件
    python tools/codemod_core_api.py --write    # 写入磁盘

退出码：0 正常，2 表示有文件无法解析。
"""

from __future__ import annotations

import argparse
import ast
import importlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_GLOBS = ("packages/modules/*/akaribot/modules", "packages/adapters/*/akaribot/adapters")
CORE_ROOT = "akaribot.core"
FACADE = "akaribot.core.api"
# 适配器具有独立的公开接口，其中的符号仅供适配器使用，模块包导入该接口将被规则 B3 拦截。
ADAPTER_FACADE = "akaribot.core.api.adapters"

# 必须保持最小范围导入的文件不改写，因为公开接口在导入阶段即展开，会将 web_render 连同 playwright 引入
# ``sys.modules``，而 Telegram 适配器专门保证“仅导入 message_builder 而不连带引入 web_render”。
KEEP_DEEP_IMPORTS = frozenset(
    {
        "packages/adapters/akari-bot-adapter-telegram/akaribot/adapters/telegram/info.py",
        "packages/adapters/akari-bot-adapter-telegram/akaribot/adapters/telegram/message_builder.py",
    }
)


@dataclass
class FilePlan:
    """单个文件的改写计划。

    :param path: 文件路径。
    :param moved: 迁移到公开接口的符号数。
    :param kept: 因公开接口未收录或对象不同而保留的符号数。
    :param text: 改写后的全文。无需改写时为 ``None``。
    """

    path: Path
    moved: int = 0
    kept: int = 0
    text: str | None = None
    details: list[str] = field(default_factory=list)


def facade_names(module: str = FACADE) -> dict[str, object]:
    """获取某个公开接口承诺的名字与其对象。

    :param module: 公开接口模块名。
    :return: 名字到对象的映射。
    """
    facade = importlib.import_module(module)
    return {name: getattr(facade, name) for name in getattr(facade, "__all__", ()) if not name.startswith("_")}


def target_facade(path: Path) -> str:
    """该文件应当改为通过哪个公开接口导入。

    适配器优先使用 ``api.adapters``。那里的符号仅供适配器使用，模块包导入会被 B3 判错。

    :param path: 源码文件。
    :return: 公开接口模块名。
    """
    return ADAPTER_FACADE if "akaribot/adapters" in path.as_posix() else FACADE


def is_same_object(module: str, symbol: str, facade: dict[str, object]) -> bool:
    """核对深路径符号与公开接口符号是否同一个对象。

    :param module: 深路径模块名。
    :param symbol: 符号名。
    :param facade: 公开接口名字到对象的映射。
    :return: 同一对象时为 ``True``。
    """
    if symbol not in facade:
        return False
    try:
        deep = importlib.import_module(module)
    except Exception:  # noqa: BLE001，无法导入的模块统一不执行改写。
        return False
    if not hasattr(deep, symbol):
        return False
    return getattr(deep, symbol) is facade[symbol]


def iter_sources() -> list[Path]:
    """全部模块包与适配器包的源码文件（不含测试与缓存）。

    :return: 文件路径列表，按路径排序。
    """
    files: list[Path] = []
    for pattern in PACKAGE_GLOBS:
        for root in sorted(PROJECT_ROOT.glob(pattern)):
            files.extend(sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts))
    return files


def _render(module: str, names: list[tuple[str, str | None]]) -> str:
    rendered = ", ".join(name if alias is None else f"{name} as {alias}" for name, alias in names)
    return f"from {module} import {rendered}"


def _facade_statements(tree: ast.Module) -> dict[str, ast.ImportFrom]:
    found: dict[str, ast.ImportFrom] = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module in (FACADE, ADAPTER_FACADE):
            found[node.module] = node
    return found


def plan_file(path: Path, facades: dict[str, dict[str, object]]) -> FilePlan:
    """计算一个文件的改写方案。

    :param path: 源码文件。
    :param facades: 公开接口模块名到“名字 → 对象”的映射。
    :return: 改写计划。无需改写时 ``text`` 为 ``None``。
    :raises SyntaxError: 文件无法解析。
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    lines = source.splitlines(keepends=True)
    plan = FilePlan(path=path)

    primary = target_facade(path)
    existing = _facade_statements(tree)
    merged: dict[str, list[tuple[str, str | None]]] = {
        module: [(alias.name, alias.asname) for alias in node.names] for module, node in existing.items()
    }
    replacements: list[tuple[int, int, str]] = []

    def destination(module: str, symbol: str) -> str | None:
        """获取该符号应当改用的公开接口。若两个公开接口均未提供，则返回 None。"""
        for candidate in (primary, FACADE):
            if is_same_object(module, symbol, facades[candidate]):
                return candidate
        return None

    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.level != 0 or not node.module:
            continue
        if not node.module.startswith(CORE_ROOT) or node.module in (FACADE, ADAPTER_FACADE):
            continue
        if node.module.startswith(f"{FACADE}."):
            continue
        keep: list[tuple[str, str | None]] = []
        for alias in node.names:
            target = destination(node.module, alias.name)
            if target is None:
                keep.append((alias.name, alias.asname))
                plan.kept += 1
                plan.details.append(f"保留 {node.module}::{alias.name}")
                continue
            merged.setdefault(target, []).append((alias.name, alias.asname))
            plan.moved += 1
        if len(keep) == len(node.names):
            continue
        replacements.append(
            (node.lineno - 1, node.end_lineno or node.lineno, _render(node.module, keep) if keep else "")
        )

    if not plan.moved:
        return plan

    if replacements:
        anchor = min(start for start, _, _ in replacements)
    else:
        anchor = 0
    for module, names in merged.items():
        deduped: list[tuple[str, str | None]] = []
        seen: set[str] = set()
        for name, alias in names:
            if name in seen:
                continue
            seen.add(name)
            deduped.append((name, alias))
        if module in existing:
            node = existing[module]
            replacements.append((node.lineno - 1, node.end_lineno or node.lineno, _render(module, deduped)))
        else:
            replacements.append((anchor, anchor, _render(module, deduped) + "\n"))

    for start, end, replacement in sorted(replacements, reverse=True):
        block = [line if line.endswith("\n") else line + "\n" for line in replacement.splitlines()]
        lines[start:end] = block
    plan.text = "".join(lines)
    return plan


def main(argv: list[str] | None = None) -> int:
    """主入口函数，返回进程退出码。"""
    parser = argparse.ArgumentParser(description="把 core 深路径 import 改走 akaribot.core.api 门面")
    parser.add_argument("--write", action="store_true", help="写入磁盘。默认只报告")
    args = parser.parse_args(argv)

    facades = {FACADE: facade_names(FACADE), ADAPTER_FACADE: facade_names(ADAPTER_FACADE)}
    plans: list[FilePlan] = []
    for path in iter_sources():
        if path.relative_to(PROJECT_ROOT).as_posix() in KEEP_DEEP_IMPORTS:
            continue
        try:
            plan = plan_file(path, facades)
        except (SyntaxError, UnicodeDecodeError) as error:
            print(f"无法解析 {path}：{error}", file=sys.stderr)
            return 2
        if plan.moved:
            plans.append(plan)

    moved = sum(plan.moved for plan in plans)
    kept = sum(plan.kept for plan in plans)
    print(f"可迁移 {moved} 处，涉及 {len(plans)} 个文件；保留 {kept} 处（门面未收录或对象不同）。")
    if args.write:
        for plan in plans:
            plan.path.write_text(plan.text or "", encoding="utf-8")
        print(f"已改写 {len(plans)} 个文件。")
    else:
        for plan in plans[:10]:
            print(f"  {plan.path.relative_to(PROJECT_ROOT)}：迁移 {plan.moved}，保留 {plan.kept}")
        if len(plans) > 10:
            print(f"  ……另有 {len(plans) - 10} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
