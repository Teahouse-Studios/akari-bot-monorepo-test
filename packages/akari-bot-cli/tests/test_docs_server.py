"""``akaribot.cli.docs.server``：预览服务器的 clean URL、目录索引与 404。"""

import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs.server import StaticServer
from akaribot.testing import Tester, func_case


async def _test_serve_clean_urls_and_404():
    with TemporaryDirectory(prefix="akari-docs-srv-") as raw:
        root = Path(raw)
        (root / "index.html").write_text("home", encoding="utf-8")
        (root / "foo.html").write_text("foo", encoding="utf-8")
        (root / "404.html").write_text("custom-404", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "index.html").write_text("sub-index", encoding="utf-8")
        server = StaticServer(root)
        try:
            url = server.start()
            again = server.start()
            home = urllib.request.urlopen(url)
            home_type = home.headers.get("Content-Type")
            home_body = home.read().decode("utf-8")
            clean = urllib.request.urlopen(f"{url}foo").read().decode("utf-8")
            directory = urllib.request.urlopen(f"{url}sub").read().decode("utf-8")
            try:
                urllib.request.urlopen(f"{url}missing")
            except urllib.error.HTTPError as exc:
                missing = (exc.code, exc.read().decode("utf-8"))
            else:
                missing = (0, "")
            try:
                urllib.request.urlopen(f"{url}../../etc/passwd")
            except urllib.error.HTTPError as exc:
                traversal = exc.code
            else:
                traversal = 0
        finally:
            server.stop()
    return (
        url == again
        and url.startswith("http://127.0.0.1:")
        and url.endswith("/")
        and ":0/" not in url
        and home_body == "home"
        and home_type.startswith("text/html")
        and "charset=utf-8" in home_type
        and clean == "foo"
        and directory == "sub-index"
        and missing == (404, "custom-404")
        and traversal == 404
    )


async def _test_missing_without_404_page():
    with TemporaryDirectory(prefix="akari-docs-srv-") as raw:
        root = Path(raw)
        (root / "index.html").write_text("home", encoding="utf-8")
        server = StaticServer(root)
        try:
            url = server.start()
            try:
                urllib.request.urlopen(f"{url}nope")
            except urllib.error.HTTPError as exc:
                result = (exc.code, exc.read().decode("utf-8"))
            else:
                result = (0, "")
        finally:
            server.stop()
    return result == (404, "404 Not Found\n")


async def _test_stop_is_idempotent():
    with TemporaryDirectory(prefix="akari-docs-srv-") as raw:
        root = Path(raw)
        (root / "index.html").write_text("home", encoding="utf-8")
        server = StaticServer(root)
        server.start()
        server.stop()
        server.stop()
    return True


@func_case
async def test_docs_server(tester: Tester):
    """cli.docs.server: 本机静态预览"""
    await tester.test(_test_serve_clean_urls_and_404, "clean URL、目录索引、404 与路径穿越")
    await tester.test(_test_missing_without_404_page, "无 404 页时返回纯文本")
    await tester.test(_test_stop_is_idempotent, "重复 stop 不报错")
    return tester
