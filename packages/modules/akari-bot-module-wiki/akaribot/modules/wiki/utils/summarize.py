"""Wikitext 离线摘要提取。"""

import re

import orjson
import wikitextparser as wtp

from akaribot.core.api import Logger

# 引用来源、图库、代码块等标签的内容不属于正文。
# wikitextparser 的 plain_text() 不剥离标签内容，因此必须在其之前显式清除。
NOISE_TAGS = frozenset(
    {
        "div",
        "gallery",
        "imagemap",
        "maplink",
        "ref",
        "references",
        "score",
        "syntaxhighlight",
        "table",
        "timeline",
    }
)

# 章节标题行，形如 == 标题 == 或 === 子标题 ===
_HEADING = re.compile(r"^={2,6}.*?={2,6}$")

# MediaWiki 行为开关，如 __TOC__、__NOTOC__、__NOEDITSECTION__。
# 其仅控制页面渲染，不属于正文，而 plain_text() 不会执行剥离。
_BEHAVIOR_SWITCH = re.compile(r"__[A-Z][A-Z_]*__")

# 分类链接与跨语言链接的目标前缀，如 Category:、分类：、de:、zh-hans:。
# 这两类链接不出现在渲染后的正文中，但 plain_text() 会将其还原为链接目标文本。
_HIDDEN_LINK = re.compile(
    r"^\s*:?\s*(?:category|分类|分類|カテゴリ|kategorie|categoría|catégorie|категория"
    r"|[a-z]{2,3}(?:-[a-z0-9-]+)?)\s*:",
    re.I,
)

# 语义属性链接 [[属性：值：]]，在页面上渲染为其值。值中可能包含嵌套的内外链接，因此需要允许单层嵌套。
# 必须在解析前以文本替换处理，因为将 WikiLink 的 string 改写成非链接文本会导致该对象失效，
# 其后 plain_text() 遍历到它便会抛出 AttributeError。
_SEMANTIC_LINK = re.compile(r"\[\[[^\[\]|]*?::((?:[^\[\]]|\[\[[^\[\]]*?\]\]|\[[^\[\]]*?\])*?)\]\]")

# 未被 wikitextparser 识别的扩展标签，如 Translate 扩展的 <translate>。
# 这类标签包裹的是正文本身，仅去除标签并保留内容。
_RESIDUAL_TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9_:-]*(?:\s[^>]*?)?/?>")

# 若语法结构未闭合或无法识别，此类标记会残留于输出中。
# 此处直接舍弃对应行，正文缺失时避免生成包含残缺源码的摘要。
_UNPARSED_MARKUP = re.compile(r"\{\{|\}\}|\{\||\|\}|\[\[|\]\]")

# TemplateData 扩展的标签，其内容为描述模板用法的 JSON。
_TEMPLATEDATA = re.compile(r"<templatedata\s*>(.*?)</templatedata\s*>", re.I | re.S)

# 句末标点包括中英文的句号、问号、叹号。英文标点必须后随空白，避免将小数点与缩写误判为句末标点。
_SENTENCE_END = r"(.*?(?:!\s|\?\s|\.\s|！|？|。)).*"
# 首句包含左括号时改用该模式，获取右括号之后的句末标点，避免在括号内部截断。
_SENTENCE_END_AFTER_BRACKET = r"(.*?[)}\]>\"\'》】’”」）].*?(?:!\s|\?\s|\.\s|！|？|。)).*"
_OPEN_BRACKET = r"[({\[>\"\'《【‘“「（]"

# 首句短于此长度时追加第二句。“石头（Stone）是在主世界中大量存在的方块。”为 23 字符，
# 属于应当补充的范围。首句本身超过此长度的条目不再追加。
MIN_FIRST_SENTENCE_LENGTH = 40
MAX_SUMMARY_LENGTH = 250
MAX_SUMMARY_LINES = 5


def _strip_braced(text: str) -> str:
    # 必须在解析前自行扫描，无法交由 wikitextparser 处理。若结构内部包含未配对的花括号，
    # 括号匹配将发生偏差，导致残留在 plain_text() 输出中被视为正文。
    # 仅移除成对结构，避免因贪婪匹配至结尾导致正文丢失。
    spans = []
    stack = []
    i = 0
    length = len(text)
    while i < length:
        if text.startswith("{{", i):
            stack.append(i)
            i += 2
            continue
        if text.startswith("}}", i):
            if stack:
                start = stack.pop()
                if not stack:  # 最外层构造闭合，整段一并移除。
                    spans.append((start, i + 2))
            i += 2
            continue
        i += 1
    if not spans:
        return text
    out = []
    prev = 0
    for start, end in spans:
        out.append(text[prev:start])
        prev = end
    out.append(text[prev:])
    return "".join(out)


def _normalize_section(title: str) -> str:
    # 规范化章节名以供比较。
    # 章节锚点中的下划线与标题中的空格等价，wikilib 传入的章节名已将空格替换为下划线。
    return title.strip().replace("_", " ")


def _select_section(parsed: wtp.WikiText, section: str | None):
    # 取出目标章节。
    sections = parsed.sections
    if not sections:
        return None
    if not section:
        # wikitextparser 的首个章节即引言段，其 title 为 None。
        return sections[0]
    normalized = _normalize_section(section)
    for sec in sections:
        if sec.title is not None and _normalize_section(sec.title) == normalized:
            return sec
    return None


def _templatedata_description(wikitext: str) -> str:
    # 模板文档页的说明通常记录于 <templatedata> 的 description 字段中，外层
    # {{TemplateData|...}} 会被视为模板剥离导致无法获取正文。提取的说明仍为 Wikitext，
    # 需要由调用方进一步清理。
    match = _TEMPLATEDATA.search(wikitext)
    if not match:
        return ""
    try:
        data = orjson.loads(match.group(1))
    except orjson.JSONDecodeError:
        # 页面中的 TemplateData 可能无效，解析失败时按照空值处理。
        return ""
    if not isinstance(data, dict):
        return ""
    description = data.get("description")
    return description if isinstance(description, str) else ""


def _extract_section_text(wikitext: str, section: str | None) -> str:
    # 解析 Wikitext 并取出指定章节的正文纯文本。
    # 行为开关、模板类构造与语义属性链接必须在解析前以文本处理，因为行为开关不构成任何
    # 可识别的节点，模板类构造可能因内部包含未配对的花括号而不被识别，改写链接节点则会使其失效。
    cleaned = _BEHAVIOR_SWITCH.sub("", wikitext)
    cleaned = _strip_braced(cleaned)
    cleaned = _SEMANTIC_LINK.sub(r"\1", cleaned)
    parsed = wtp.parse(cleaned)
    # 倒序清除，避免靠前的节点被置空后导致靠后节点的 span 偏移。
    for tag in reversed(parsed.get_tags()):
        if tag.name in NOISE_TAGS:
            tag.string = ""
    for table in reversed(parsed.get_tables()):
        table.string = ""
    for link in reversed(parsed.wikilinks):
        # 包含展示文本的内容为正文行内链接，plain_text() 能够正确还原。
        if link.text is None and _HIDDEN_LINK.match(link.title):
            link.string = ""

    target = _select_section(parsed, section)
    if target is None:
        return ""
    # 过滤章节标题行与仍包含结构标记的残留行，前者一并覆盖目标章节自身的标题
    # 与其下的子章节标题。
    lines = [
        line.strip()
        for line in _RESIDUAL_TAG.sub("", target.plain_text()).split("\n")
        if line.strip() and not _HEADING.match(line.strip()) and not _UNPARSED_MARKUP.search(line)
    ]
    return "\n".join(lines)


def extract_summary(wikitext: str, section: str | None = None) -> str:
    """离线解析 Wikitext，取出指定章节的正文纯文本。

    :param wikitext: 页面的原始 Wikitext。
    :param section: 章节名。为 None 时取引言段。
    :returns: 清理后的纯文本。解析失败或未匹配到章节时返回空字符串。
    """
    if not wikitext:
        return ""
    try:
        text = _extract_section_text(wikitext, section)
        if not text and not section:
            # TemplateData 仅作为补充，引言已有散文者以引言为准，指定章节时也不覆盖正文。
            description = _templatedata_description(wikitext)
            if description:
                text = _extract_section_text(description, None)
        return text
    except Exception:
        Logger.exception()
        return ""


def _take_sentence(text: str) -> str | None:
    # 取出文本开头的一个完整句子。
    matched = re.findall(_SENTENCE_END, text, re.S | re.M)
    if not matched:
        return None
    if re.findall(_OPEN_BRACKET, matched[0]):
        after_bracket = re.findall(_SENTENCE_END_AFTER_BRACKET, text, re.S | re.M)
        # 括号未闭合时选取首个匹配结果。此处若直接取下标，空列表会抛出 IndexError 并导致整段摘要缺失。
        if after_bracket:
            return after_bracket[0]
    return matched[0]


def truncate_summary(text: str) -> str:
    """将正文截断为摘要。

    :param text: 待截断的正文纯文本。
    :returns: 截断后的摘要。
    """
    try:
        desc = "\n".join([line for line in text.split("\n") if line != ""])
        first = _take_sentence(desc)
        if first:
            summary = first
            if len(summary) < MIN_FIRST_SENTENCE_LENGTH:
                # 第二句必须与首句同处一段。句末标点的匹配跨换行，不加此限制会将
                # TextExtracts 输出中的章节标题、子章节正文一类的无关内容并入摘要。
                remainder = desc[len(first) :].split("\n", 1)[0]
                second = _take_sentence(remainder)
                if second:
                    summary += second
            desc = summary
    except Exception:
        Logger.exception()
        desc = ""
    if desc in ["...", "…"]:
        desc = ""
    ellipsis = False
    if len(desc) > MAX_SUMMARY_LENGTH:
        desc = desc[0:MAX_SUMMARY_LENGTH]
        ellipsis = True
    lines = desc.split("\n")
    if len(lines) > MAX_SUMMARY_LINES:
        lines = lines[0:MAX_SUMMARY_LINES]
        ellipsis = True
    return "\n".join(lines) + ("..." if ellipsis else "")
