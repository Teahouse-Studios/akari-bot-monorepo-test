"""构造无法录制的测试语料。"""

import json
import sys

sys.path.insert(0, ".")

from akaribot.testing.mock.webrender import save_webrender_fixture

MINECRAFT_NEWS_URL = (
    "https://www.minecraft.net/content/minecraftnet/language-masters/en-us/"
    "jcr:content/root/container/image_grid_a_copy_64.articles.page-1.json"
)

# minecraft_news 逐条读取 default_tile.title / sub_header 与 article_url、image.imageURL。
MINECRAFT_NEWS_PAYLOAD = {
    "article_grid": [
        {
            "default_tile": {
                "title": "Test Article Alpha",
                "sub_header": "A synthetic entry used by the scheduled task test.",
                "image": {"imageURL": "/content/test-alpha.png"},
            },
            "article_url": "/en-us/article/test-alpha",
        },
        {
            "default_tile": {
                "title": "Test Article Beta",
                "sub_header": "A second synthetic entry to cover multi-item handling.",
                "image": {"imageURL": "/content/test-beta.png"},
            },
            "article_url": "/en-us/article/test-beta",
        },
    ]
}

# mcv_rss 的 get_article 仅从页面中提取首个 h1 作为标题，并以 "404" 判定页面不存在。
MCV_ARTICLE_TEMPLATE = (
    "<!DOCTYPE html><html><head><title>{title}</title></head>"
    "<body><h1>{title}</h1><p>Synthetic changelog body.</p></body></html>"
)

# minecraft_news 获取图片链接后通过 get_raw 拉取图片内容，语料按照 URL 匹配即可满足要求。
NEWS_IMAGE_URLS = [
    "https://www.minecraft.net/content/test-alpha.png",
    "https://www.minecraft.net/content/test-beta.png",
]

# 需要预置变更日志语料的版本号。线上版本推进后需要同步更新，
# 缺失时 mcv_rss 无法获取文章标题，但不影响版本推送的检查。
MCV_VERSIONS = ("26.2", "26.3-snapshot-6")


# 稳定失败的外部端点。录制工具仅保存成功响应，此类请求在测试中会改用真实网络，
# 携带重试与超时耗费数十秒，且结果随对方服务状态波动。此处以其真实状态码固定下来，
# 使模块进入与线上一致的错误分支，同时将耗时降为零。
NEGATIVE_RESPONSES = [
    # 该推文不存在，接口稳定返回 404，模块据此提示“未找到推文”。
    ("https://react-tweet.vercel.app/api/tweet/1", 404, "Not Found"),
    # 皮肤渲染服务源站长期不可用，Cloudflare 返回 521。
    ("https://crafatar.com/renders/body/069a79f444e94726a5befca90e38aaf5?overlay", 521, ""),
    # 基岩版查询接口无响应，以 5xx 复现其超时后的对外表现。
    ("http://motd.wd-api.com/v1/bedrock?host=mc.hypixel.net&port=19132", 502, ""),
]


def build():
    saved = []

    from akaribot.testing.mock.fixtures import save_fixture

    for url, status, text in NEGATIVE_RESPONSES:
        saved.append(save_fixture(url=url, status_code=status, text=text, method="GET"))

    saved.append(save_webrender_fixture(MINECRAFT_NEWS_URL, json.dumps(MINECRAFT_NEWS_PAYLOAD, ensure_ascii=False)))

    for url in NEWS_IMAGE_URLS:
        saved.append(save_webrender_fixture(url, "synthetic-image-bytes"))

    # 变更日志的 URL 通过模块自身推导，此处直接复用其实现，避免规则不一致。
    from akaribot.modules.mcv_rss import get_changelog_url

    for version in MCV_VERSIONS:
        link = get_changelog_url(version)
        if not link:
            print(f"  skipped {version}: 无法推导变更日志地址")
            continue
        saved.append(save_webrender_fixture(link, MCV_ARTICLE_TEMPLATE.format(title=f"Minecraft {version}")))

    for path in saved:
        print(f"  built {path.name}")
    print(f"\nBuilt {len(saved)} synthetic fixtures ({len(NEGATIVE_RESPONSES)} HTTP, rest WebRender).")


if __name__ == "__main__":
    build()
