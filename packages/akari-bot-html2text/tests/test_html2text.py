"""html2text 独立包的输出与注入点测试。

本包是上游 2020.1.16 的维护分支。用例锁定两件事：拆包不得改变既有输出；
url_formatter 的默认值与注入行为须与拆包前一致。
"""

from akaribot.testing import func_case, Tester
from html2text import HTML2Text, html2text

_LINK_IMG_HTML = (
    '<p>See <a href="https://example.com/a">Example</a> and <img src="https://example.com/i.png" alt="图片"> here.</p>'
)
_TABLE_HTML = "<table><tr><th>项目</th><th>值</th></tr><tr><td>甲</td><td>1</td></tr></table>"
_REF_HTML = '<p><a href="https://example.com/a">A</a> and <a href="https://example.com/b">B</a></p>'

_LINK_IMG_EXPECTED = "See [Example](https://example.com/a) and ![图片](https://example.com/i.png)\nhere.\n\n"
_TABLE_EXPECTED = "项目| 值  \n---|---  \n甲| 1\n\n"
_WIKI_CONFIG_EXPECTED = "See Example and  here.\n\n"
_MIRROR_LINK_IMG_EXPECTED = (
    "See [Example](https://mirror.example.com/a) and\n![图片](https://mirror.example.com/i.png) here.\n\n"
)
_MIRROR_REF_EXPECTED = (
    "[A][1] and [B][2]\n\n   [1]: https://mirror.example.com/a\n\n   [2]: https://mirror.example.com/b\n\n"
)


def _mirror_formatter(url: str) -> str:
    """把示例域名改写为镜像域名，用于观察注入是否生效。"""
    return url.replace("example.com", "mirror.example.com")


async def _test_link_and_image_output():
    """测试默认输出 - 行内链接与图片按上游格式渲染"""
    try:
        return HTML2Text().handle(_LINK_IMG_HTML) == _LINK_IMG_EXPECTED

    except Exception:
        return False


async def _test_table_output():
    """测试默认输出 - 表格按上游 pipe 格式渲染"""
    try:
        return HTML2Text().handle(_TABLE_HTML) == _TABLE_EXPECTED

    except Exception:
        return False


async def _test_url_formatter_rewrites_links():
    """测试注入改写 - 链接与图片的 URL 均经过 url_formatter"""
    try:
        return HTML2Text(url_formatter=_mirror_formatter).handle(_LINK_IMG_HTML) == _MIRROR_LINK_IMG_EXPECTED

    except Exception:
        return False


async def _test_url_formatter_rewrites_reference_links():
    """测试注入改写 - 引用式链接定义中的 URL 同样经过 url_formatter"""
    try:
        h = HTML2Text(url_formatter=_mirror_formatter)
        h.inline_links = False
        return h.handle(_REF_HTML) == _MIRROR_REF_EXPECTED

    except Exception:
        return False


async def _test_url_formatter_skipped_when_links_ignored():
    """测试注入点边界 - 忽略链接与图片的配置不调用 url_formatter

    wiki 模块即用此配置，故其行为与拆包前一致地不依赖注入对象。
    """
    try:
        calls: list[str] = []

        def _record(url: str) -> str:
            calls.append(url)
            return url

        h = HTML2Text(url_formatter=_record)
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        h.single_line_break = True
        return h.handle(_LINK_IMG_HTML) == _WIKI_CONFIG_EXPECTED and calls == []

    except Exception:
        return False


async def _test_default_formatter_equals_str():
    """测试默认值 - 不传 url_formatter 与显式传 str 等价，模块级入口亦然"""
    try:
        implicit = HTML2Text().handle(_LINK_IMG_HTML)
        explicit = HTML2Text(url_formatter=str).handle(_LINK_IMG_HTML)
        module_level = html2text(_LINK_IMG_HTML)
        return implicit == explicit == module_level == _LINK_IMG_EXPECTED

    except Exception:
        return False


@func_case
async def test_html2text(tester: Tester):
    """html2text 独立包：输出格式与 url_formatter 注入测试"""
    await tester.test(_test_link_and_image_output, "链接与图片默认输出测试")
    await tester.test(_test_table_output, "表格默认输出测试")
    await tester.test(_test_url_formatter_rewrites_links, "链接与图片注入改写测试")
    await tester.test(_test_url_formatter_rewrites_reference_links, "引用式链接注入改写测试")
    await tester.test(_test_url_formatter_skipped_when_links_ignored, "忽略链接时不调用注入测试")
    await tester.test(_test_default_formatter_equals_str, "默认值与 str 等价测试")

    return tester
