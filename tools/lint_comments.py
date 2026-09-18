"""注释书面语检查。

按 generated_docs/monorepo_refactor_prep.md §8 的规则，对本仓库的行注释做可机械判定的检查。
既有违规记录在 tools/comment_lint_baseline.txt 中豁免，检查只对新增与修改的行生效。

用法：
    uv run python tools/lint_comments.py                    # 检查全部文件，仅报基线外违规
    uv run python tools/lint_comments.py --diff HEAD~1      # 只检查该提交之后新增/修改的行
    uv run python tools/lint_comments.py --generate-baseline  # 重建基线文件
"""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "tools" / "comment_lint_baseline.txt"

# 收录范围：本仓库自有 Python 源码。第三方内嵌库与迁移产物不在约束内。
SCAN_DIRS = ("core", "modules", "bots", "tests", "templates", "tools")
SCAN_ROOT_FILES = ("bot.py", "tester.py", "conftest.py")
EXCLUDED_DIR_NAMES = {"__pycache__", ".venv", ".git"}

# 工具指令注释不构成文档，不予检查。
TOOL_DIRECTIVE_PATTERN = re.compile(
    r"^#\s*(noqa|type:|skipcq|ruff:|fmt:|pragma:|mypy:|pyright:|pylint:|isort:|coverage:|nosec)\b"
)
SHEBANG_PATTERN = re.compile(r"^#!")
CODING_PATTERN = re.compile(r"^#.*coding[:=]")

# 规则 5：装饰性分隔注释。同一分隔字符在首尾各出现三次以上，中间允许夹带标题；
# 纯字符行与「### 标题」式 Markdown 标题不在此列。
_DECORATION_CHARS = "=-*~_+"
DECORATIVE_SEPARATOR_PATTERN = re.compile(rf"^#\s*([{re.escape(_DECORATION_CHARS)}])\1{{2,}}.*?\1{{3,}}\s*$")
MARKDOWN_HEADING_PATTERN = re.compile(r"^#+\s")

# 规则 4：口语词。只收录在本仓库语境下无歧义的搭配，避免伤及正常用词（如「处理」「弄清」）。
COLLOQUIAL_PATTERN = re.compile(
    r"("
    r"踩坑|踩过坑|填坑|大坑"
    r"|炸了|搞炸|写炸|跑炸|炸掉"
    r"|挂了(?!钩)|搞挂"
    r"|懒得|反正|干脆|索性"
    r"|搞定|搞完|搞好|搞成|搞出|搞乱|搞错|搞个|搞点"
    r"|弄好|弄完|弄成|弄出|弄乱|弄错|弄得|弄个|弄点"
    r"|写死|硬塞|硬凑|瞎写|乱写|随手写"
    r"|凑合|将就用"
    r")"
)

# 规则 2：第一/第二人称。只收录原文明确点名的词，避免「我」在其他语境下的误判。
PERSON_PATTERN = re.compile(r"(我们|咱们|你们|您)")

# 规则 3：语气词与情绪标点。省略号只认中文双省略号、四个以上英文点与行尾三点，
# 以免把代码占位符（`<...>`、`[...]`）与引用文本里的标点算作情绪标点。
TONE_PATTERN = re.compile(
    r"("
    r"吧[。！!，,、；;）)]?$|呢[。！!，,、；;）)]?$|嘛|呗|啦|咯|喽"
    r"|[?？!！]{2,}"
    r"|!$|！$"
    r"|……|\.{4,}|\.{3}$"
    r")"
)
# 条件连词之后的省略号属于「等等」义，不视为情绪标点。
ELLIPSIS_EXEMPT_PATTERN = re.compile(r"(如果|若|否则|比如|例如|如|诸如|等)[^。]{0,20}(…|\.{3,})")

# 规则 8：时间性表述。
TEMPORAL_PATTERN = re.compile(r"(暂时|先这样|以后再改|回头再|待补|先放着|后面再说|临时性|暂定)")

# 规则 7：连续行注释块。
COMMENT_BLOCK_MIN_LINES = 3

# 行注释长度上限，与 Ruff 的 line-length 一致。
MAX_COMMENT_LENGTH = 120

LEVEL_ERROR = "error"
LEVEL_WARN = "warn"

# 规则编号与说明，输出与基线文件共用。
RULE_DESCRIPTIONS = {
    "R1": "行注释超过 120 字符",
    "R2": "注释含第一/第二人称",
    "R3": "注释含语气词或情绪标点",
    "R4": "注释含口语词",
    "R5": "新增装饰性分隔注释",
    "R6": "时间性表述",
    "R7": "连续 3 行以上的行注释块",
}
RULE_LEVELS = {
    "R1": LEVEL_ERROR,
    "R2": LEVEL_ERROR,
    "R3": LEVEL_ERROR,
    "R4": LEVEL_ERROR,
    "R5": LEVEL_ERROR,
    "R6": LEVEL_WARN,
    "R7": LEVEL_WARN,
}


@dataclass(frozen=True, order=True)
class Violation:
    """一处注释违规。

    :param path: 相对仓库根的 POSIX 路径。
    :param line: 行号，从 1 开始。
    :param rule: 规则编号。
    :param text: 违规的注释文本，已去除首尾空白。
    """

    path: str
    line: int
    rule: str
    text: str

    def key(self) -> str:
        """基线文件的稳定键。不含行号，代码移动后仍能命中豁免。"""
        return f"{self.path}\t{self.rule}\t{self.text}"

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {RULE_LEVELS[self.rule]} {self.rule} {RULE_DESCRIPTIONS[self.rule]}\n    {self.text}"


def iter_source_files() -> list[Path]:
    """枚举需要检查的 Python 文件，按路径排序。"""
    files: list[Path] = []
    for dir_name in SCAN_DIRS:
        base = PROJECT_ROOT / dir_name
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if EXCLUDED_DIR_NAMES & set(path.parts):
                continue
            files.append(path)
    for file_name in SCAN_ROOT_FILES:
        path = PROJECT_ROOT / file_name
        if path.is_file():
            files.append(path)
    return sorted(set(files))


def extract_comments(source: str) -> tuple[dict[int, str], set[int]]:
    """抽取行注释。

    :param source: 文件源码。
    :return: 二元组——行号到注释文本的映射；含代码 token 的行号集合。
    """
    comments: dict[int, str] = {}
    code_lines: set[int] = set()
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return comments, code_lines

    for token in tokens:
        if token.type == tokenize.COMMENT:
            line = token.start[0]
            if line in comments:
                continue
            comments[line] = token.string.rstrip()
        elif token.type not in (
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.ENDMARKER,
            tokenize.ENCODING,
        ):
            code_lines.add(token.start[0])
    return comments, code_lines


def is_checkable(comment: str) -> bool:
    """工具指令、shebang 与编码声明不参与检查。"""
    if SHEBANG_PATTERN.match(comment) or CODING_PATTERN.match(comment):
        return False
    return not TOOL_DIRECTIVE_PATTERN.match(comment)


def check_comment(path: str, line: int, comment: str) -> list[Violation]:
    """对单条行注释施加规则 1~5、8。"""
    body = comment.lstrip("#").strip()
    if not body:
        return []

    found: list[Violation] = []
    if len(comment) > MAX_COMMENT_LENGTH:
        found.append(Violation(path, line, "R1", body))
    if PERSON_PATTERN.search(body):
        found.append(Violation(path, line, "R2", body))
    if TONE_PATTERN.search(body) and not ELLIPSIS_EXEMPT_PATTERN.search(body):
        found.append(Violation(path, line, "R3", body))
    if COLLOQUIAL_PATTERN.search(body):
        found.append(Violation(path, line, "R4", body))
    if DECORATIVE_SEPARATOR_PATTERN.match(comment) and not MARKDOWN_HEADING_PATTERN.match(comment):
        found.append(Violation(path, line, "R5", body))
    if TEMPORAL_PATTERN.search(body):
        found.append(Violation(path, line, "R6", body))
    return found


def check_comment_blocks(path: str, comments: dict[int, str], code_lines: set[int]) -> list[Violation]:
    """规则 7：连续 3 行以上、且各行均无代码的行注释块。"""
    found: list[Violation] = []
    standalone = sorted(line for line in comments if line not in code_lines)
    block: list[int] = []
    for line in standalone + [0]:
        if block and line == block[-1] + 1:
            block.append(line)
            continue
        if len(block) >= COMMENT_BLOCK_MIN_LINES:
            found.append(Violation(path, block[0], "R7", comments[block[0]].lstrip("#").strip()))
        block = [line] if line else []
    return found


def check_file(path: Path) -> list[Violation]:
    """检查单个文件。"""
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    source = path.read_text(encoding="utf-8")
    comments, code_lines = extract_comments(source)
    found: list[Violation] = []
    for line, comment in sorted(comments.items()):
        if is_checkable(comment):
            found.extend(check_comment(relative, line, comment))
    found.extend(check_comment_blocks(relative, comments, code_lines))
    return found


def load_baseline() -> set[str]:
    """读取基线豁免键。"""
    if not BASELINE_PATH.is_file():
        return set()
    keys: set[str] = set()
    for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        keys.add(line)
    return keys


def changed_lines(base_ref: str) -> set[tuple[str, int]]:
    """取 `git diff <base_ref>` 中新增或修改的行号集合。

    :param base_ref: 比较基准，如 `HEAD~1` 或提交 SHA。
    :return: (POSIX 路径, 行号) 集合。diff 失败时返回空集，调用方应回退到全量检查。
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--unified=0", "--no-color", base_ref, "--", "*.py"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"git diff {base_ref} 失败，回退为全量检查：{error}", file=sys.stderr)
        return set()

    lines: set[tuple[str, int]] = set()
    current: str | None = None
    hunk = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
    for raw in result.stdout.splitlines():
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            current = None if target == "/dev/null" else target[2:] if target.startswith("b/") else target
            continue
        match = hunk.match(raw)
        if match and current:
            start = int(match.group(1))
            count = int(match.group(2) or 1)
            for offset in range(count):
                lines.add((current, start + offset))
    return lines


def generate_baseline(violations: list[Violation]) -> None:
    """把当前全部违规写入基线文件。"""
    keys = sorted({v.key() for v in violations})
    header = [
        "# 注释书面语检查的基线豁免清单。",
        "# 每行一条，格式：<路径>\\t<规则编号>\\t<注释文本>。不含行号，代码移动后豁免仍然有效。",
        "# 键由 tools/lint_comments.py --generate-baseline 生成，随清理逐步缩小。",
        f"# 生成时的违规总数：{len(keys)}",
        "",
    ]
    BASELINE_PATH.write_text("\n".join(header + keys) + "\n", encoding="utf-8")
    print(f"基线已写入 {BASELINE_PATH.relative_to(PROJECT_ROOT)}，共 {len(keys)} 条。")


def main() -> int:
    """入口。返回进程退出码，0 表示无基线外违规。"""
    parser = argparse.ArgumentParser(description="注释书面语检查")
    parser.add_argument("--diff", metavar="BASE_REF", help="只检查该基准之后新增或修改的行")
    parser.add_argument("--generate-baseline", action="store_true", help="重建基线豁免文件")
    parser.add_argument("--show-baseline", action="store_true", help="同时打印基线内的违规")
    args = parser.parse_args()

    all_violations: list[Violation] = []
    for path in iter_source_files():
        all_violations.extend(check_file(path))
    all_violations.sort()

    if args.generate_baseline:
        generate_baseline(all_violations)
        return 0

    baseline = load_baseline()
    scope = changed_lines(args.diff) if args.diff else None

    reported: list[Violation] = []
    baselined = 0
    for violation in all_violations:
        if scope is not None and (violation.path, violation.line) not in scope:
            continue
        if violation.key() in baseline:
            baselined += 1
            if args.show_baseline:
                reported.append(violation)
            continue
        reported.append(violation)

    for violation in reported:
        print(violation)

    errors = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_ERROR]
    warns = [v for v in reported if RULE_LEVELS[v.rule] == LEVEL_WARN]
    scope_note = f"，范围为 {args.diff} 之后的新增/修改行" if args.diff else ""
    print(
        f"\n检查文件 {len(iter_source_files())} 个{scope_note}："
        f"error {len(errors)}，warn {len(warns)}，基线豁免 {baselined}。"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
