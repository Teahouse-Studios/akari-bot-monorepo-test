import feedparser

from akaribot.core.builtins.message.internal import Url
from akaribot.core.utils.html2text import html2text
from akaribot.core.utils.http import get_url


async def get_rss():
    """
    Get RSS feed from lakeus.xyz
    """
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
