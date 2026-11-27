import feedparser
from html2text import html2text

from akaribot.core.api import Url, get_url


async def get_rss():
    """获取 lakeus.xyz 的 RSS 源。"""
    url = await get_url(
        "https://lakeus.xyz/api.php?action=featuredfeed&feed=teahouse-weekly&feedformat=atom",
        status_code=200,
        fmt="text",
    )
    feed_data = feedparser.parse(url)
    entries = feed_data.get("entries", [])
    if not entries:
        return ""
    feed = entries[-1]
    title = feed.get("title", "")
    summary = html2text(feed.get("summary", ""), baseurl="https://lakeus.xyz", url_formatter=lambda u: str(Url(u)))
    return title + "\n" + summary
