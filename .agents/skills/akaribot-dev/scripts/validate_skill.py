#!/usr/bin/env python3
"""校验 akaribot-dev 技能与文档页的映射。

检查项：
1. SKILL.md 行数少于 500。
2. SKILL.md 引用的文档页都存在于仓库内。
3. 路由表覆盖各领域的主要文档页。
4. SKILL.md 不含已失效的旧路径。
5. SKILL.md 仍然覆盖若干条必须守住的规则。

用法：uv run python .agents/skills/akaribot-dev/scripts/validate_skill.py
"""

import re
import sys
from pathlib import Path

MAX_ROOT_LINES = 500

DOC_LINK_PATTERN = re.compile(r"`(packages/[^`]+?/doc/[^`]+?\.md)`")

REQUIRED_DOCS = [
    "packages/akari-bot-core/akaribot/core/doc/architecture.md",
    "packages/akari-bot-core/akaribot/core/doc/config.md",
    "packages/akari-bot-core/akaribot/core/doc/database.md",
    "packages/akari-bot-core/akaribot/core/doc/queue.md",
    "packages/akari-bot-core/akaribot/core/doc/module-development.md",
    "packages/akari-bot-core/akaribot/core/doc/message-api.md",
    "packages/akari-bot-core/akaribot/core/doc/permissions.md",
    "packages/akari-bot-core/akaribot/core/doc/adapter-development.md",
    "packages/akari-bot-core/akaribot/core/doc/public-api.md",
    "packages/akari-bot-core/akaribot/core/doc/i18n.md",
    "packages/akari-bot-core/akaribot/core/doc/placeholders.md",
    "packages/akari-bot-core/akaribot/core/doc/development-workflow.md",
    "packages/akari-bot-testing/akaribot/testing/doc/index.md",
    "packages/akari-bot-testing/akaribot/testing/doc/writing-tests.md",
]

STALE_PATTERNS = [
    ("旧测试框架目录", r"core/tester"),
    ("旧适配器目录", r"(^|[^a-z])bots/"),
    ("旧 reference 链接", r"references/"),
]

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
]


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    repo_root = skill_root.parents[2]
    root_path = skill_root / "SKILL.md"

    if not root_path.is_file():
        print(f"SKILL.md not found: {root_path}", file=sys.stderr)
        return 1

    errors: list[str] = []
    root_text = root_path.read_text(encoding="utf-8")
    root_line_count = len(root_text.splitlines())
    if root_line_count >= MAX_ROOT_LINES:
        errors.append(f"SKILL.md has {root_line_count} lines; expected fewer than {MAX_ROOT_LINES}.")

    linked = set(DOC_LINK_PATTERN.findall(root_text))
    for doc in sorted(linked):
        if not (repo_root / doc).is_file():
            errors.append(f"Missing doc page linked from SKILL.md: {doc}")

    for doc in REQUIRED_DOCS:
        if doc not in linked:
            errors.append(f"Routing table does not cover: {doc}")

    for label, pattern in STALE_PATTERNS:
        match = re.search(pattern, root_text, re.MULTILINE)
        if match:
            errors.append(f"Stale path in SKILL.md ({label}): {match.group(0)!r}")

    for label, pattern in REQUIRED_GUARDS:
        if not re.search(pattern, root_text):
            errors.append(f"Required rule is missing: {label}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Skill validation passed: SKILL.md={root_line_count} lines, docs={len(linked)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
