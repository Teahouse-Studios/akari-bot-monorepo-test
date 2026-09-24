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
import ast
import io
import re
import subprocess
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "tools" / "comment_lint_baseline.txt"

# 收录范围：本仓库自有 Python 源码，即 packages/ 下的分发源码与 tests/、templates/、tools/。
# 第三方内嵌库与迁移产物不在约束内。
SCAN_DIRS = ("packages", "tests", "templates", "tools")
SCAN_ROOT_FILES = ("bot.py", "tester.py", "conftest.py")
EXCLUDED_DIR_NAMES = {"__pycache__", ".venv", ".git"}
# 内嵌的第三方副本保持上游原样，不按本仓库的书写规范改写。
EXCLUDED_DISTS = ("packages/akari-bot-html2text",)

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
# 「关于我们」是帮助菜单里的入口名，不是叙述人称。
PERSON_PATTERN = re.compile(r"(我们|咱们|你们|您)")
PERSON_EXEMPT_PATTERN = re.compile(r"关于我们")

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
# 引号内是面向用户的原文（如“正在输入……”），其中的省略号属于该文案本身。
QUOTED_ELLIPSIS_PATTERN = re.compile(r"[“「][^”」]*(?:…|\.{3,})[^”」]*[”」]")
# 省略号被用作占位符标记（整行只有它，或它单独占一段）时不算情绪标点；列举后的「……」
# 是「等等」义（`fc`、`fs`……），同样不算。
ELLIPSIS_MARKER_PATTERN = re.compile(r"^\s*\.{3,}\s*$|^\s*\.{3,}\s|\.{3,}\s*$|、[^、。]{0,20}(?:…|\.{3,})")

# 规则 8：时间性表述。
TEMPORAL_PATTERN = re.compile(r"(暂时|先这样|以后再改|回头再|待补|先放着|后面再说|临时性|暂定)")

# 规则 8：变更叙述。只收录无歧义地指向「已经不存在的那种写法」的词；「旧版本号」「旧库」
# 「旧数据」指迁移历史数据，属规范明确保留的兼容说明，不在其中。
NARRATION_PATTERN = re.compile(
    r"(旧实现|旧写法|旧布局|旧行为|旧方案|从前|原先|曾经|此前(?!缀)|迁移前|上一版|之前是(?!否)|以前是|一度是|已迁移|迁移到了)"
)

# 规则 9：中文里的半角标点。反引号包裹的代码片段与 Sphinx 字段（`:param x:`）先剔除。
HALFWIDTH_PUNCT_PATTERN = re.compile(r"[\u4e00-\u9fff][,;!?]|[,;!?][\u4e00-\u9fff]")
BACKTICK_SPAN_PATTERN = re.compile(r"`[^`]*`")
# 形如 `种类:包名`、`(用例名, 类型, 消息)` 的取值格式说明属代码记号，不是中文句子里的标点。
CODE_SHAPE_PATTERN = re.compile(r"\([^()]*[,:][^()]*\)")
# docstring 里的示例代码整行都不是散文，不按中文排版检查。
CODE_LINE_PATTERN = re.compile(r"[(){}\[\]=\"]|^\s*>|^\s*\.\.\.")

# 规则 10：中英文之间缺空格。数字与拉丁字母都算「西文」，但行内代码、URL、占位符先剔除。
CJK_LATIN_PATTERN = re.compile(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]")
# 整行不含中文时属外部引用文本（英文规范原文、英文 docstring），中文排版与长度规则都不适用。
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff]")
# 双下划线方法属语言协议，不是非公开 API。
DUNDER_PATTERN = re.compile(r"^__\w+__$")
URL_PATTERN = re.compile(r"https?://\S+")
PLACEHOLDER_PATTERN = re.compile(r"\$\{[^}]*\}")

# 规则 7：连续行注释块。规范允许单条说明写到三行，四行起视为该抽函数或补文档。
COMMENT_BLOCK_MIN_LINES = 4

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
    "R8": "注释叙述变更而非当前状态",
    "R9": "中文里使用半角标点",
    "R10": "中英文之间缺空格",
    "R11": "非公开符号带 docstring",
}
RULE_LEVELS = {
    "R1": LEVEL_ERROR,
    "R2": LEVEL_ERROR,
    "R3": LEVEL_ERROR,
    "R4": LEVEL_ERROR,
    "R5": LEVEL_ERROR,
    "R6": LEVEL_WARN,
    "R7": LEVEL_WARN,
    "R8": LEVEL_ERROR,
    "R9": LEVEL_ERROR,
    "R10": LEVEL_ERROR,
    "R11": LEVEL_ERROR,
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
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if relative.startswith(EXCLUDED_DISTS):
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


def prose_for_spacing(text: str) -> str:
    """去掉代码记号，只留下需要按中文排版检查的散文部分。

    行内代码、URL 与模板占位符不是句子成分：`` `config/` `` 前后不加空格是既有排版，
    ``${name}`` 与链接同理。

    :param text: 注释或 docstring 正文。
    :return: 剔除代码记号后的文本。
    """
    cleaned = BACKTICK_SPAN_PATTERN.sub(" ", text)
    cleaned = URL_PATTERN.sub(" ", cleaned)
    cleaned = PLACEHOLDER_PATTERN.sub(" ", cleaned)
    return CODE_SHAPE_PATTERN.sub(" ", cleaned)


def check_prose(path: str, line: int, body: str) -> list[Violation]:
    """规则 8~10：变更叙述、半角标点与中英文间距。

    :param path: 仓库根相对路径。
    :param line: 行号。
    :param body: 注释或 docstring 的正文。
    :return: 违规列表。
    """
    found: list[Violation] = []
    if NARRATION_PATTERN.search(body):
        found.append(Violation(path, line, "R8", body))
    prose = prose_for_spacing(body)
    if HALFWIDTH_PUNCT_PATTERN.search(prose):
        found.append(Violation(path, line, "R9", body))
    if CJK_LATIN_PATTERN.search(prose):
        found.append(Violation(path, line, "R10", body))
    return found


def check_comment(path: str, line: int, comment: str) -> list[Violation]:
    """对单条行注释施加规则 1~5、8~10。"""
    body = comment.lstrip("#").strip()
    if not body:
        return []

    found: list[Violation] = []
    if len(comment) > MAX_COMMENT_LENGTH and CJK_PATTERN.search(body):
        found.append(Violation(path, line, "R1", body))
    if PERSON_PATTERN.search(body) and not PERSON_EXEMPT_PATTERN.search(body):
        found.append(Violation(path, line, "R2", body))
    if TONE_PATTERN.search(body) and not (
        ELLIPSIS_EXEMPT_PATTERN.search(body)
        or QUOTED_ELLIPSIS_PATTERN.search(body)
        or ELLIPSIS_MARKER_PATTERN.search(body)
    ):
        found.append(Violation(path, line, "R3", body))
    if COLLOQUIAL_PATTERN.search(body):
        found.append(Violation(path, line, "R4", body))
    if DECORATIVE_SEPARATOR_PATTERN.match(comment) and not MARKDOWN_HEADING_PATTERN.match(comment):
        found.append(Violation(path, line, "R5", body))
    if TEMPORAL_PATTERN.search(body):
        found.append(Violation(path, line, "R6", body))
    found.extend(check_prose(path, line, body))
    return found


def is_private_symbol(name: str) -> bool:
    """该符号是否属于非公开 API。

    双下划线方法实现的是语言协议（``__init__``、``__str__``、``__getattr__``），属公开面，
    与模块内部的 ``_helper`` 不同。

    :param name: 符号名。
    :return: 非公开时为 ``True``。
    """
    return name.startswith("_") and not DUNDER_PATTERN.match(name)


def extract_docstrings(source: str) -> dict[int, tuple[str, bool]]:
    """抽取模块、类与函数的 docstring，按起始行号索引。

    「只描述当前状态」与中文排版同时约束 docstring——规范面向的是全部书面说明，不只是行注释。
    同时标出该符号是否非公开（名字以 ``_`` 开头）：非公开符号不该有 docstring，其说明归行注释。

    :param source: 文件源码。
    :return: 起始行号到 ``(正文, 是否非公开)`` 的映射。
    """
    found: dict[int, tuple[str, bool]] = {}
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return found
    for node in ast.walk(tree):
        if not isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        if not isinstance(first, ast.Expr) or not isinstance(first.value, ast.Constant):
            continue
        value = first.value.value
        if isinstance(value, str) and value.strip():
            found[first.lineno] = (value.strip(), is_private_symbol(str(getattr(node, "name", ""))))
    return found


def check_docstring(path: str, line: int, text: str) -> list[Violation]:
    """对 docstring 逐行施加规则 1~4、8~10。

    :param path: 仓库根相对路径。
    :param line: docstring 起始行号。
    :param text: docstring 正文。
    :return: 违规列表。
    """
    found: list[Violation] = []
    for offset, raw in enumerate(text.splitlines()):
        body = raw.strip()
        if not body:
            continue
        current = line + offset
        # docstring 里的示例代码整行按代码看；不含中文的整行是外部引用文本，都不施加散文规则。
        if CODE_LINE_PATTERN.search(body) or not CJK_PATTERN.search(body):
            continue
        if len(body) > MAX_COMMENT_LENGTH:
            found.append(Violation(path, current, "R1", body))
        if PERSON_PATTERN.search(body) and not PERSON_EXEMPT_PATTERN.search(body):
            found.append(Violation(path, current, "R2", body))
        if TONE_PATTERN.search(body) and not (
            ELLIPSIS_EXEMPT_PATTERN.search(body)
            or QUOTED_ELLIPSIS_PATTERN.search(body)
            or ELLIPSIS_MARKER_PATTERN.search(body)
        ):
            found.append(Violation(path, current, "R3", body))
        if COLLOQUIAL_PATTERN.search(body):
            found.append(Violation(path, current, "R4", body))
        found.extend(check_prose(path, current, body))
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
    for line, (text, private) in sorted(extract_docstrings(source).items()):
        if private:
            found.append(Violation(relative, line, "R11", text.splitlines()[0]))
        found.extend(check_docstring(relative, line, text))
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
    :return: (POSIX 路径， 行号) 集合。diff 失败时返回空集，调用方应回退到全量检查。
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
