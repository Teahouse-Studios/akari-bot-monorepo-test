"""T4.1 命名空间改写：把旧顶层命名空间 core/modules/bots 改写为 akaribot.* 形式。

import 语句按前缀映射全自动改写；字符串字面量只在命中真实模块路径白名单时改写，
i18n 文案键与目录名因此不受影响。改动逐条写入仓库根的报告，供人工逐行过目。

用法：
    PYTHONPATH=.codemod-deps .venv/bin/python tools/codemod_namespace.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import libcst as cst
from libcst.metadata import CodeRange, MetadataWrapper, PositionProvider

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 扫描范围：物理移动后仍可能引用旧命名空间的 Python 源码。example/ 是脚手架样例，不在 packages/ 下。
SCAN_DIRS = ("packages", "tests", "tools", "example")
SCAN_ROOT_FILES = ("bot.py", "tester.py", "conftest.py")
PRUNED_DIR_NAMES = frozenset(
    {"__pycache__", ".git", ".venv", ".mypy_cache", ".pytest_cache", ".ruff_cache", "build", "dist", "node_modules"}
)

STRINGS_REPORT_NAME = "codemod_strings_report.txt"
MANUAL_LIST_NAME = "codemod_manual_list.txt"

# 旧→新前缀映射，按段匹配且长前缀优先。core.tester 已移出 core 成为独立包，是 core.* 的例外。
PREFIX_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("core", "tester"), ("akaribot", "testing")),
    (("core",), ("akaribot", "core")),
    (("modules",), ("akaribot", "modules")),
    (("bots",), ("akaribot", "adapters")),
)

# 新→旧前缀映射，用于把 packages 下的真实模块路径反推成旧点分路径。
REVERSE_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("akaribot", "testing"), ("core", "tester")),
    (("akaribot", "core"), ("core",)),
    (("akaribot", "modules"), ("modules",)),
    (("akaribot", "adapters"), ("bots",)),
)

# 单段旧根名同时充当 JSON 键、数据库字段名与文件系统目录名，无法与模块路径区分，故不入白名单。
MIN_KNOWN_SEGMENTS = 2

BARE_ROOTS = frozenset({"core", "modules", "bots"})

# 裸 import 绑定旧根名，改写后绑定名变为 akaribot，引用处必须一并调整，属人工事项。
IMPORT_MANUAL_HINT = "裸 import 无点号，需人工改写并调整引用"

# i18n 调用上下文中的点分字符串是文案键，即使与真实模块路径同名也不改写。
I18N_CALLEE_NAMES = frozenset({"I18NContext", "t", "gettext", "ngettext", "gettext_lazy"})
I18N_CALLEE_ATTRS = frozenset({"t", "gettext", "ngettext", "I18NContext"})
I18N_MANUAL_HINT = "i18n 调用实参且与真实模块路径同名，需确认是文案键还是模块路径"

# patch 调用中承载点分路径的实参形式：位置参数下标与关键字名。
PATCH_POSITIONAL_INDEXES = frozenset({0})
PATCH_OBJECT_POSITIONAL_INDEXES = frozenset({0, 1})
PATCH_KEYWORDS = frozenset({"target"})
PATCH_OBJECT_KEYWORDS = frozenset({"attribute"})

# f-string 中出现的旧命名空间形态：字面量片段的根名之后紧跟标识符或插值，排除句末的散文误报。
FSTRING_LITERAL_PATTERN = re.compile(r"(?<![0-9A-Za-z_])(?:core|modules|bots)\.(?=[A-Za-z_{])")
FSTRING_SNIPPET_LIMIT = 80


def _dotted_segments(node: cst.CSTNode | None) -> list[str] | None:
    if isinstance(node, cst.Name):
        return [node.value]
    if isinstance(node, cst.Attribute):
        head = _dotted_segments(node.value)
        if head is None or not isinstance(node.attr, cst.Name):
            return None
        return [*head, node.attr.value]
    return None


def _build_dotted(segments: Sequence[str]) -> cst.BaseExpression:
    node: cst.BaseExpression = cst.Name(segments[0])
    for segment in segments[1:]:
        node = cst.Attribute(value=node, attr=cst.Name(segment))
    return node


def _apply_prefix(
    segments: Sequence[str], rules: Sequence[tuple[tuple[str, ...], tuple[str, ...]]]
) -> list[str] | None:
    for old, new in rules:
        if tuple(segments[: len(old)]) == old:
            return [*new, *segments[len(old) :]]
    return None


def remap_old_to_new(segments: Sequence[str]) -> list[str] | None:
    """旧点分路径转新点分路径，不属于旧命名空间时返回 None。"""
    return _apply_prefix(segments, PREFIX_RULES)


def remap_new_to_old(segments: Sequence[str]) -> list[str] | None:
    """新点分路径反推旧点分路径，不属于旧命名空间时返回 None。"""
    return _apply_prefix(segments, REVERSE_RULES)


def build_known(root: Path) -> frozenset[str]:
    """遍历 packages/**/akaribot，反推出旧点分模块路径全集。"""
    known: set[str] = set()
    for package_root in sorted(root.glob("packages/**/akaribot")):
        if not package_root.is_dir():
            continue
        for path in sorted(package_root.rglob("*.py")):
            if PRUNED_DIR_NAMES.intersection(path.relative_to(root).parts):
                continue
            parts = ["akaribot", *path.relative_to(package_root).parts]
            if parts[-1] == "__init__.py":
                parts.pop()
            else:
                parts[-1] = parts[-1][: -len(".py")]
            # 模块路径与逐级向上的包路径都算真实路径。
            for depth in range(len(parts), 0, -1):
                old = remap_new_to_old(parts[:depth])
                if old is not None and len(old) >= MIN_KNOWN_SEGMENTS:
                    known.add(".".join(old))
    return frozenset(known)


def longest_known_prefix(text: str, known: frozenset[str]) -> str | None:
    """取 text 落在白名单里的最长点分前缀，无命中返回 None。"""
    segments = text.split(".")
    for depth in range(len(segments), 0, -1):
        candidate = ".".join(segments[:depth])
        if candidate in known:
            return candidate
    return None


def _leftmost_name(node: cst.CSTNode) -> str | None:
    while isinstance(node, (cst.Attribute, cst.Subscript)):
        node = node.value
    return node.value if isinstance(node, cst.Name) else None


def _patch_argument_kinds(call: cst.Call) -> tuple[frozenset[int], frozenset[str]]:
    segments = _dotted_segments(call.func)
    if segments is None:
        return frozenset(), frozenset()
    if segments[-1] == "patch":
        return PATCH_POSITIONAL_INDEXES, PATCH_KEYWORDS
    if len(segments) >= 2 and segments[-1] == "object" and segments[-2] == "patch":
        return PATCH_OBJECT_POSITIONAL_INDEXES, PATCH_OBJECT_KEYWORDS
    return frozenset(), frozenset()


def _rewrite_literal(node: cst.SimpleString, old: str, new: str) -> str | None:
    raw = node.raw_value
    if not raw.startswith(old):
        return None
    return f"{node.prefix}{node.quote}{new}{raw[len(old) :]}{node.quote}"


def _fstring_snippet(node: cst.FormattedString) -> str:
    try:
        snippet = cst.Module(body=[]).code_for_node(node)
    except Exception:  # noqa: BLE001 - 片段仅用于报告，取不到源码时退回占位文本
        return "f-string"
    snippet = " ".join(snippet.split())
    return snippet if len(snippet) <= FSTRING_SNIPPET_LIMIT else f"{snippet[:FSTRING_SNIPPET_LIMIT]}..."


@dataclass
class FileOutcome:
    """单文件改写结果，字段直接进入报告与汇总。"""

    string_report: list[str] = field(default_factory=list)
    manual: list[str] = field(default_factory=list)
    import_count: int = 0
    string_count: int = 0
    failure: str | None = None


class NamespaceTransformer(cst.CSTTransformer):
    """改写 import 语句，并按白名单改写字符串字面量。"""

    def __init__(self, known: frozenset[str], positions: Mapping[cst.CSTNode, CodeRange], label: str) -> None:
        self._known = known
        self._positions = positions
        self._label = label
        self._calls: list[cst.Call] = []
        self._outcome = FileOutcome()

    @property
    def outcome(self) -> FileOutcome:
        return self._outcome

    def _line(self, node: cst.CSTNode) -> int:
        position = self._positions.get(node)
        return position.start.line if position is not None else 0

    def _record_string(self, node: cst.CSTNode, old: str, new: str) -> None:
        self._outcome.string_count += 1
        self._outcome.string_report.append(f"{self._label}:{self._line(node)}: {old} -> {new}")

    def _record_import(self) -> None:
        self._outcome.import_count += 1

    def _record_manual(self, node: cst.CSTNode, text: str, hint: str) -> None:
        self._outcome.manual.append(f"{self._label}:{self._line(node)}: {text} -> [人工] {hint}")

    def visit_Call(self, node: cst.Call) -> bool:
        self._calls.append(node)
        return True

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        self._calls.pop()
        return updated_node

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.Import:
        names: list[cst.ImportAlias] = []
        changed = False
        # 位置元数据以原始节点为键，遍历产出的新节点不在其中。
        for alias in original_node.names:
            segments = _dotted_segments(alias.name)
            if segments is None:
                names.append(alias)
                continue
            if len(segments) == 1:
                if segments[0] in BARE_ROOTS:
                    self._record_manual(alias, f"import {segments[0]}", IMPORT_MANUAL_HINT)
                names.append(alias)
                continue
            remapped = remap_old_to_new(segments)
            if remapped is None:
                names.append(alias)
                continue
            self._record_import()
            changed = True
            names.append(alias.with_changes(name=_build_dotted(remapped)))
        return updated_node.with_changes(names=names) if changed else updated_node

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        if original_node.relative:
            return updated_node
        segments = _dotted_segments(original_node.module)
        if segments is None:
            return updated_node
        remapped = remap_old_to_new(segments)
        if remapped is None:
            return updated_node
        self._record_import()
        return updated_node.with_changes(module=_build_dotted(remapped))

    def _in_i18n_context(self) -> bool:
        if not self._calls:
            return False
        func = self._calls[-1].func
        if isinstance(func, cst.Name):
            return func.value in I18N_CALLEE_NAMES
        if isinstance(func, cst.Attribute) and isinstance(func.attr, cst.Name):
            return func.attr.value in I18N_CALLEE_ATTRS
        return False

    def _is_patch_target(self, node: cst.CSTNode) -> bool:
        if not self._calls:
            return False
        call = self._calls[-1]
        indexes, keywords = _patch_argument_kinds(call)
        if not indexes and not keywords:
            return False
        for index, argument in enumerate(call.args):
            if argument.value is node and index in indexes:
                return True
        for keyword in call.keywords:
            if keyword.value is node and keyword.keyword is not None and keyword.keyword.value in keywords:
                return True
        return False

    def leave_SimpleString(self, original_node: cst.SimpleString, updated_node: cst.SimpleString) -> cst.SimpleString:
        try:
            text = original_node.evaluated_value
        except Exception:  # noqa: BLE001 - 无法求值的字面量不参与改写
            return updated_node
        if not isinstance(text, str) or not text:
            return updated_node
        prefix = longest_known_prefix(text, self._known)
        if prefix is None:
            return updated_node
        if prefix == text:
            if self._in_i18n_context():
                self._record_manual(original_node, text, I18N_MANUAL_HINT)
                return updated_node
        elif not self._is_patch_target(original_node):
            return updated_node
        remapped = remap_old_to_new(prefix.split("."))
        if remapped is None:
            return updated_node
        new_text = f"{'.'.join(remapped)}{text[len(prefix) :]}"
        value = _rewrite_literal(original_node, prefix, ".".join(remapped))
        if value is None:
            self._record_manual(original_node, text, "字面量含转义，无法安全改写")
            return updated_node
        self._record_string(original_node, text, new_text)
        return updated_node.with_changes(value=value)

    def leave_FormattedString(
        self, original_node: cst.FormattedString, updated_node: cst.FormattedString
    ) -> cst.FormattedString:
        if self._in_i18n_context():
            return updated_node
        shape = "".join(
            part.value if isinstance(part, cst.FormattedStringText) else "{...}" for part in original_node.parts
        )
        roots = {
            _leftmost_name(part.expression)
            for part in original_node.parts
            if isinstance(part, cst.FormattedStringExpression)
        }
        if FSTRING_LITERAL_PATTERN.search(shape) or roots & BARE_ROOTS:
            self._record_manual(original_node, _fstring_snippet(original_node), "f-string 拼接模块路径，不自动改写")
        return updated_node


def _read_source(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _write_source(path: Path, source: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(source)


def iter_target_files(root: Path, self_path: Path) -> list[Path]:
    """枚举待扫描的 Python 文件，排除缓存目录与工具自身。"""
    files: set[Path] = set()
    for dir_name in SCAN_DIRS:
        base = root / dir_name
        if not base.is_dir():
            continue
        files.update(
            path for path in base.rglob("*.py") if not PRUNED_DIR_NAMES.intersection(path.relative_to(root).parts)
        )
    files.update(root / name for name in SCAN_ROOT_FILES if (root / name).is_file())
    files.discard(self_path)
    return sorted(files)


def process_file(path: Path, root: Path, known: frozenset[str], dry_run: bool) -> FileOutcome:
    """改写单个文件；解析失败记入 outcome.failure 并跳过。"""
    label = path.relative_to(root).as_posix()
    try:
        source = _read_source(path)
        module = cst.parse_module(source)
    except Exception as error:  # noqa: BLE001 - 单个文件异常不中断整轮改写
        return FileOutcome(failure=f"{label}: {type(error).__name__}: {error}")
    try:
        wrapper = MetadataWrapper(module, unsafe_skip_copy=True)
        positions = wrapper.resolve(PositionProvider)
        transformer = NamespaceTransformer(known, positions, label)
        updated = wrapper.visit(transformer)
    except Exception as error:  # noqa: BLE001 - 单个文件异常不中断整轮改写
        return FileOutcome(failure=f"{label}: {type(error).__name__}: {error}")
    outcome = transformer.outcome
    if (outcome.import_count or outcome.string_count) and not dry_run:
        _write_source(path, updated.code)
    return outcome


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="T4.1 命名空间改写工具")
    parser.add_argument("--dry-run", action="store_true", help="只统计与打印，不写入任何文件")
    args = parser.parse_args(argv)

    root = PROJECT_ROOT
    known = build_known(root)
    if not known:
        print(
            "错误：packages/**/akaribot 下未发现模块，字符串白名单无法建立；确认物理移动已完成。",
            file=sys.stderr,
        )
        return 2

    string_report: list[str] = []
    manual_lines: list[str] = []
    failures: list[str] = []
    import_total = 0
    string_total = 0
    targets = iter_target_files(root, Path(__file__).resolve())
    for path in targets:
        outcome = process_file(path, root, known, args.dry_run)
        string_report.extend(outcome.string_report)
        manual_lines.extend(outcome.manual)
        import_total += outcome.import_count
        string_total += outcome.string_count
        if outcome.failure is not None:
            failures.append(outcome.failure)

    if args.dry_run:
        print("[dry-run] 只统计与打印，不写入任何文件")
        for line in string_report:
            print(f"  待改写 {line}")
    if manual_lines:
        print("人工清单（工具不改写）：")
        for line in manual_lines:
            print(f"  {line}")
    if failures:
        print("解析失败或处理异常的文件：")
        for failure in failures:
            print(f"  {failure}")

    report_path = root / STRINGS_REPORT_NAME
    manual_path = root / MANUAL_LIST_NAME
    if not args.dry_run:
        report_path.write_text("".join(f"{line}\n" for line in string_report), encoding="utf-8")
        manual_path.write_text("".join(f"{line}\n" for line in manual_lines), encoding="utf-8")

    print(f"扫描文件数: {len(targets)}")
    print(f"改写 import: {import_total} 处")
    print(f"改写字符串: {string_total} 处")
    print(f"人工清单: {len(manual_lines)} 条")
    print(f"解析失败: {len(failures)} 个文件")
    print(f"字符串报告: {STRINGS_REPORT_NAME}（{len(string_report)} 条）")
    print(f"人工清单文件: {MANUAL_LIST_NAME}（{len(manual_lines)} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
