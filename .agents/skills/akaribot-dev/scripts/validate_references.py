#!/usr/bin/env python3
"""校验 akaribot-dev 技能目录的结构约束。

检查项：
1. SKILL.md 行数少于 500。
2. SKILL.md 链接的 reference 都存在。
3. references/ 下没有未被 SKILL.md 直接链接的孤立文件。
4. 超过 100 行的 reference 在顶部保留 `## 目录`。
5. SKILL.md 仍然覆盖若干条必须守住的规则。
6. reference 里出现的仓库路径真实存在（迁移与拆包后最容易失效的一类内容）。

用法：.venv/bin/python .agents/skills/akaribot-dev/scripts/validate_references.py
"""

import re
import sys
from pathlib import Path

MAX_ROOT_LINES = 500
TOC_REQUIRED_AFTER_LINES = 100
TOC_HEADING = "## 目录"
TOC_MAX_INDEX = 10

LINK_PATTERN = re.compile(r"\]\(references/([^)#]+\.md)(?:#[^)]+)?\)")
# 反引号包裹的仓库相对路径；含通配符或占位符的跳过。
PATH_PATTERN = re.compile(r"`((?:packages|tools|tests|\.agents|\.github|docs)/[^`\s]+?)`")

# SKILL.md 必须守住的规则。改动技能正文时若移除了其中任意一条，这里会失败。
REQUIRED_GUARDS = [
    ("zh_cn.json", r"zh_cn\.json"),
    ("Weblate", r"Weblate"),
    ("CI=1", r"CI=1"),
    ("union_id", r"union_id"),
    ("union_scope", r"union_scope"),
    ("Features instance rule", r"Features\(\.\.\.\).*实例"),
    ("SessionInfo", r"SessionInfo"),
    ("JobQueue", r"JobQueue"),
    ("core.exports", r"core\.exports"),
    ("only-current-state rule", r"只描述当前状态"),
]


def check_paths(skill_root: Path, repo_root: Path) -> list[str]:
    """核对 reference 里出现的仓库路径真实存在。

    :param skill_root: 技能目录。
    :param repo_root: 仓库根。
    :return: 问题列表。
    """
    problems: list[str] = []
    for path in [skill_root / "SKILL.md", *sorted((skill_root / "references").glob("*.md"))]:
        for token in sorted(set(PATH_PATTERN.findall(path.read_text(encoding="utf-8")))):
            if any(marker in token for marker in ("*", "<", ">", "...")):
                continue
            if not (repo_root / token).exists():
                problems.append(f"Path in {path.name} does not exist: {token}")
    return problems


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    repo_root = skill_root.parents[2]
    root_path = skill_root / "SKILL.md"
    reference_dir = skill_root / "references"

    if not root_path.is_file():
        print(f"SKILL.md not found: {root_path}", file=sys.stderr)
        return 1
    if not reference_dir.is_dir():
        print(f"references directory not found: {reference_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []

    root_text = root_path.read_text(encoding="utf-8")
    root_line_count = len(root_text.splitlines())
    if root_line_count >= MAX_ROOT_LINES:
        errors.append(f"SKILL.md has {root_line_count} lines; expected fewer than {MAX_ROOT_LINES}.")

    # 链接名按大小写不敏感比对，与文件系统的实际行为保持一致。
    linked: set[str] = set()
    for name in LINK_PATTERN.findall(root_text):
        linked.add(name.casefold())
        if not (reference_dir / name).is_file():
            errors.append(f"Missing reference linked from SKILL.md: {name}")

    reference_files = sorted(p for p in reference_dir.glob("*.md") if p.is_file())
    for file in reference_files:
        if file.name.casefold() not in linked:
            errors.append(f"Orphan reference not linked directly from SKILL.md: {file.name}")

        lines = file.read_text(encoding="utf-8").splitlines()
        if len(lines) > TOC_REQUIRED_AFTER_LINES:
            toc_index = lines.index(TOC_HEADING) if TOC_HEADING in lines else -1
            if toc_index < 0 or toc_index > TOC_MAX_INDEX:
                errors.append(f"Long reference lacks a top-level TOC: {file.name}")

    for label, pattern in REQUIRED_GUARDS:
        if not re.search(pattern, root_text):
            errors.append(f"Required root guard is missing: {label}")

    errors.extend(check_paths(skill_root, repo_root))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Reference validation passed: SKILL.md={root_line_count} lines, references={len(reference_files)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
