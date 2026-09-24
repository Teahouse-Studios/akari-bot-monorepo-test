"""删去非公开符号上的 docstring，并把其中的说明上提为行注释。

规范要求 docstring 只出现在公开 API 上：私有函数、私有类与模块内部实现不需要 docstring，
它们的「为什么」由行注释承担（见 `.agents/skills/akaribot-dev/references/workflow-and-style.md`）。
本工具按该规范机械处理，并把 docstring 里**除首行概括与 `:param:` / `:return:` 之外**的散文
上提为行注释——那些内容往往正是读代码读不出来的约束，直接删掉会丢信息。

保留不动的：模块级 docstring、`test_*` 入口的 docstring（测试框架把它作为 `DOC:` 输出）、
以及名字不以 `_` 开头的符号。

用法：
    python tools/codemod_private_docstrings.py            # 只报告
    python tools/codemod_private_docstrings.py --write    # 落盘

退出码：0 正常；2 有文件无法解析。
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ("packages", "tools", "tests")
EXCLUDED_DIR_NAMES = {"__pycache__", ".venv", ".git"}
# 内嵌的第三方副本保持上游原样。
EXCLUDED_DISTS = ("packages/akari-bot-html2text",)
# docstring 里属于结构化字段而非散文的行。
FIELD_PATTERN = (" :param ", " :return", " :raises", " :rtype", " :type ")
DEF_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
DUNDER_PATTERN = re.compile(r"^__\w+__$")


def is_private(name: str) -> bool:
    """该名字是否属于非公开 API。

    双下划线方法（``__init__``、``__str__``、``__getattr__``）实现的是语言协议，是公开面的一部分，
    不算非公开 API。

    :param name: 符号名。
    :return: 非公开时为 ``True``。
    """
    return name.startswith("_") and not DUNDER_PATTERN.match(name)


@dataclass
class FilePlan:
    """单个文件的改写计划。

    :param path: 文件路径。
    :param removals: 删除的 docstring 数。
    :param hoisted: 上提为行注释的散文行数。
    :param text: 改写后的全文；无需改写时为 ``None``。
    """

    path: Path
    removals: int = 0
    hoisted: int = 0
    text: str | None = None
    details: list[str] = field(default_factory=list)


def iter_sources() -> list[Path]:
    """枚举待处理的 Python 文件。"""
    files: list[Path] = []
    for dir_name in SCAN_DIRS:
        base = PROJECT_ROOT / dir_name
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if EXCLUDED_DIR_NAMES & set(path.parts):
                continue
            if path.relative_to(PROJECT_ROOT).as_posix().startswith(EXCLUDED_DISTS):
                continue
            files.append(path)
    return sorted(set(files))


def docstring_node(node: ast.AST) -> ast.Expr | None:
    """取该定义的首条语句——若它是 docstring 则返回，否则返回 ``None``。"""
    body = getattr(node, "body", None)
    if not body:
        return None
    first = body[0]
    if not isinstance(first, ast.Expr) or not isinstance(first.value, ast.Constant):
        return None
    return first if isinstance(first.value.value, str) and first.value.value.strip() else None


def prose_lines(text: str) -> list[str]:
    """取 docstring 中值得保留的散文行。

    首行是概括，`:param:` / `:return:` 等是签名已经表达的信息，都不保留；其余非空行是
    读代码读不出来的约束，上提为行注释。

    :param text: docstring 正文。
    :return: 散文行列表。
    """
    kept: list[str] = []
    for raw in text.splitlines()[1:]:
        line = raw.strip()
        if not line or any(line.startswith(prefix.strip()) for prefix in FIELD_PATTERN):
            continue
        kept.append(line)
    return kept


def plan_file(path: Path) -> FilePlan:
    """算出一个文件的改写方案。

    :param path: 源码文件。
    :return: 改写计划。
    :raises SyntaxError: 文件无法解析。
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    lines = source.splitlines(keepends=True)
    plan = FilePlan(path=path)
    edits: list[tuple[int, int, list[str]]] = []

    for node in ast.walk(tree):
        if not isinstance(node, DEF_NODES) or not is_private(node.name):
            continue
        doc = docstring_node(node)
        if doc is None:
            continue
        start = doc.lineno - 1
        end = doc.end_lineno or doc.lineno
        # 删除后紧跟的空行一并吃掉，避免函数体以空行开头。
        if end < len(lines) and not lines[end].strip():
            end += 1
        anchor = node.decorator_list[0].lineno if node.decorator_list else node.lineno
        indent = lines[anchor - 1][: len(lines[anchor - 1]) - len(lines[anchor - 1].lstrip())]
        replacement = [f"{indent}# {line}\n" for line in prose_lines(doc.value.value)]
        plan.hoisted += len(replacement)
        plan.removals += 1
        plan.details.append(f"{node.name}@{node.lineno}")
        if len(getattr(node, "body", [])) == 1:
            # 只剩 docstring 的定义删空后会语法错误，补 pass；缩进取函数体而非 def 行。
            replacement.append(f"{indent}    pass\n")
        edits.append((start, end, replacement))

    if not edits:
        return plan
    for start, end, replacement in sorted(edits, reverse=True):
        lines[start:end] = replacement
    plan.text = "".join(lines)
    return plan


def main(argv: list[str] | None = None) -> int:
    """入口。返回进程退出码。"""
    parser = argparse.ArgumentParser(description="删去非公开符号的 docstring")
    parser.add_argument("--write", action="store_true", help="落盘；缺省只报告")
    args = parser.parse_args(argv)

    plans: list[FilePlan] = []
    for path in iter_sources():
        try:
            plan = plan_file(path)
        except (SyntaxError, UnicodeDecodeError) as error:
            print(f"无法解析 {path}：{error}", file=sys.stderr)
            return 2
        if plan.removals:
            plans.append(plan)

    removed = sum(plan.removals for plan in plans)
    hoisted = sum(plan.hoisted for plan in plans)
    print(f"可删除 {removed} 处 docstring，涉及 {len(plans)} 个文件；其中上提为行注释 {hoisted} 行。")
    if args.write:
        for plan in plans:
            plan.path.write_text(plan.text or "", encoding="utf-8")
        print(f"已改写 {len(plans)} 个文件。")
    else:
        for plan in plans[:10]:
            print(f"  {plan.path.relative_to(PROJECT_ROOT)}：{plan.removals} 处")
        if len(plans) > 10:
            print(f"  ……另有 {len(plans) - 10} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
