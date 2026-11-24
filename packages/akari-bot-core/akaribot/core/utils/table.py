"""Markdown 表格工具，提供单元格转义与“高度封顶、宽度按需”的列数计算。"""

import math
import re

# 表格的高度上限。条目增多时通过增加列数分摊，使表格高度不超过该上限。
TABLE_MAX_ROWS = 10

# 表格的最少列数。条目较少时如果仍然按照高度上限倒推计算列数，会导致生成极窄的长条表格，
# 该下限仅会使表格更宽，不会反向增加高度。
TABLE_MIN_COLUMNS = 3


def escape_table_cell(text: str) -> str:
    """
    将文本转换为可置入 Markdown 表格单元格的格式。

    :param text: 原始文本。
    :return: 可安全放入单元格的文本。
    """
    return text.replace("|", "\\|").replace("\r\n", "\n").replace("\n", "  <br>  ")


def format_table_code(text: str) -> str:
    """
    将文本包装为 Markdown 行内代码，避免其中的格式标记被解析。

    :param text: 原始文本。
    :return: 可安全放入单元格的行内代码。文本为空时返回空字符串。
    """
    if not text:
        return ""
    body = text.replace("|", "\\|").replace("\r\n", "\n").replace("\n", " ")
    longest = max((len(run) for run in re.findall(r"`+", body)), default=0)
    fence = "`" * (longest + 1)
    padding = " " if body.startswith("`") or body.endswith("`") else ""
    return f"{fence}{padding}{body}{padding}{fence}"


def resolve_table_columns(
    sizes: list[int],
    separators: int = 0,
    minimum: int = TABLE_MIN_COLUMNS,
    max_rows: int = TABLE_MAX_ROWS,
) -> int:
    """按高度上限反算表格的列数。

    :param sizes: 各节的条目数量，均大于零。
    :param separators: 区隔行的数量，一并计入高度。
    :param minimum: 列数下限。
    :param max_rows: 高度上限。
    :return: 列数。
    """
    widest = max(sizes)
    columns = minimum
    while columns < widest:
        if sum(math.ceil(size / columns) for size in sizes) + separators <= max_rows:
            break
        columns += 1
    return min(columns, widest)
