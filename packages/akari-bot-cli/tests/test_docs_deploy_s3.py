"""``cli.docs.deploy.s3``：S3 兼容存储部署 provider。

用例用 ``httpx.MockTransport`` 模拟 ListObjectsV2、PUT 与 DELETE，覆盖分页、跳过未变、
上传、删除、试运行、前缀隔离、寻址方式、区域回退与错误汇总；全程不访问网络。
"""

import hashlib
import os
import threading
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.parse import parse_qsl, urlsplit

import httpx

from akaribot.cli.docs.deploy import get_provider
from akaribot.cli.docs.deploy.base import DocsDeployError
from akaribot.cli.docs.deploy.s3 import IMMUTABLE_CACHE
from akaribot.testing import Tester, func_case

ACCESS_KEY = "AKIATESTACCESS"
SECRET_KEY = "test-secret-key"
SESSION_TOKEN = "test-session-token"
ENV = {"AWS_ACCESS_KEY_ID": ACCESS_KEY, "AWS_SECRET_ACCESS_KEY": SECRET_KEY}


@dataclass(frozen=True)
class _Record:
    method: str
    url: str
    headers: dict[str, str]
    content: bytes


class _FakeS3:
    def __init__(self, objects=None, *, page_size: int = 2, failures=None, raw_list: str = "") -> None:
        self.objects = dict(objects or {})
        self.page_size = page_size
        self.failures = dict(failures or {})
        self.raw_list = raw_list
        self.requests: list[_Record] = []
        self._lock = threading.Lock()

    def __call__(self, request: httpx.Request) -> httpx.Response:
        url = urlsplit(str(request.url))
        key = _key_from_path(url.path)
        with self._lock:
            self.requests.append(_Record(request.method, str(request.url), dict(request.headers), request.content))
        failure = self.failures.get((request.method, key)) or self.failures.get((request.method, "*"))
        if failure:
            return httpx.Response(failure, text=f"<Error><Code>Denied</Code><Message>{SECRET_KEY}</Message></Error>")
        if request.method == "GET":
            if self.raw_list:
                return httpx.Response(200, text=self.raw_list)
            with self._lock:
                entries = sorted(self.objects.items())
            params = dict(parse_qsl(url.query, keep_blank_values=True))
            start = int(params.get("continuation-token") or 0)
            page = entries[start : start + self.page_size]
            token = str(start + self.page_size) if start + self.page_size < len(entries) else ""
            payload = _list_xml([(name, etag, size) for name, (etag, size) in page], bool(token), token)
            return httpx.Response(200, text=payload)
        if request.method == "PUT":
            with self._lock:
                self.objects[key] = (_md5(request.content), len(request.content))
            return httpx.Response(200)
        if request.method == "DELETE":
            with self._lock:
                self.objects.pop(key, None)
            return httpx.Response(204)
        return httpx.Response(405)


def _md5(value: str | bytes) -> str:
    data = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


def _list_xml(entries, truncated: bool, token: str) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">',
    ]
    for key, etag, size in entries:
        parts.append(f"<Contents><Key>{key}</Key><ETag>&quot;{etag}&quot;</ETag><Size>{size}</Size></Contents>")
    parts.append(f"<IsTruncated>{str(truncated).lower()}</IsTruncated>")
    if token:
        parts.append(f"<NextContinuationToken>{token}</NextContinuationToken>")
    parts.append("</ListBucketResult>")
    return "".join(parts)


def _key_from_path(path: str) -> str:
    if path.startswith("/docs/"):
        return path[len("/docs/") :]
    return "" if path == "/docs" else path.lstrip("/")


def _write_site(tmp: str, files: dict[str, str]) -> Path:
    site = Path(tmp) / "site"
    for relative, text in files.items():
        path = site / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return site


def _provider(tmp: str, fake: _FakeS3, **config):
    settings = {
        "endpoint": "https://s3.example.test",
        "bucket": "docs",
        "region": "us-east-1",
        "prefix": "site",
        "addressing": "path",
    }
    settings.update(config)
    return get_provider("s3", settings, instance_root=Path(tmp), transport=httpx.MockTransport(fake))


def _test_lists_pages_and_uploads_changes():
    home = "<html>home</html>"
    old_js = "console.log('old')"
    new_js = "console.log('new')"
    guide = "<html>guide</html>"
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": home, "assets/app.js": new_js, "guide/index.html": guide})
        fake = _FakeS3(
            {
                "site/index.html": (_md5(home), len(home)),
                "site/assets/app.js": (_md5(old_js), len(old_js)),
                "site/old.html": (_md5("old"), 3),
                "site2/keep.html": (_md5("keep"), 4),
                "other/page.html": (_md5("other"), 5),
            }
        )
        with patch.dict(os.environ, ENV, clear=True):
            provider = _provider(tmp, fake)
            target = provider.plan(site)
            result = provider.deploy(site, delete=False)
        lists = [record for record in fake.requests if record.method == "GET"]
        puts = [record for record in fake.requests if record.method == "PUT"]
        deletes = [record for record in fake.requests if record.method == "DELETE"]
        by_path = {urlsplit(record.url).path: record for record in puts}
        tokens = [dict(parse_qsl(urlsplit(record.url).query)).get("continuation-token") for record in lists]
        leaked = any(SECRET_KEY in str(record) or ACCESS_KEY in record.url for record in fake.requests)
    return (
        "3 objects" in target.detail
        and result.ok
        and not result.dry_run
        and result.uploaded == 2
        and result.skipped == 1
        and result.deleted == 0
        and set(by_path) == {"/docs/site/assets/app.js", "/docs/site/guide/index.html"}
        and IMMUTABLE_CACHE in by_path["/docs/site/assets/app.js"].headers.get("cache-control", "")
        and "javascript" in by_path["/docs/site/assets/app.js"].headers.get("content-type", "")
        and by_path["/docs/site/guide/index.html"].headers.get("cache-control") == "no-cache"
        and "text/html" in by_path["/docs/site/guide/index.html"].headers.get("content-type", "")
        and not deletes
        and len(lists) == 3
        and None in tokens
        and "2" in tokens
        and all(record.headers.get("authorization", "").startswith("AWS4-HMAC-SHA256 ") for record in fake.requests)
        and all(record.headers.get("x-amz-date") for record in fake.requests)
        and all(record.headers.get("x-amz-content-sha256") for record in fake.requests)
        and all(record.headers.get("host") == "s3.example.test" for record in fake.requests)
        and not leaked
        and result.url == "https://s3.example.test/docs/site/index.html"
        and result.detail == "s3://docs/site/"
    )


def _test_delete_only_touches_prefix():
    home = "home"
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": home})
        fake = _FakeS3(
            {
                "site/index.html": (_md5(home), len(home)),
                "site/old.html": (_md5("old"), 3),
                "site2/keep.html": (_md5("keep"), 4),
                "other/page.html": (_md5("other"), 5),
            }
        )
        with patch.dict(os.environ, ENV, clear=True):
            result = _provider(tmp, fake).deploy(site, delete=True)
        deleted = [urlsplit(record.url).path for record in fake.requests if record.method == "DELETE"]
    return (
        result.uploaded == 0
        and result.deleted == 1
        and result.skipped == 1
        and deleted == ["/docs/site/old.html"]
        and "site2/keep.html" in fake.objects
        and "other/page.html" in fake.objects
    )


def _test_dry_run_counts_without_writes():
    home = "home"
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": home, "assets/app.js": "new"})
        fake = _FakeS3({"site/index.html": (_md5(home), len(home)), "site/old.html": (_md5("old"), 3)})
        with patch.dict(os.environ, ENV, clear=True):
            provider = _provider(tmp, fake, public_url="https://docs.example.test/")
            provider.plan(site)
            after_plan = len(fake.requests)
            dry = provider.deploy(site, dry_run=True, delete=True)
        writes = [record for record in fake.requests if record.method in {"PUT", "DELETE"}]
        lists = [record for record in fake.requests if record.method == "GET"]
    return (
        after_plan == 0
        and dry.ok
        and dry.dry_run
        and dry.uploaded == 1
        and dry.deleted == 1
        and dry.skipped == 1
        and dry.url == "https://docs.example.test/"
        and not writes
        and bool(lists)
    )


def _test_virtual_host_and_auto_addressing():
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": "x"})
        virtual_fake = _FakeS3()
        with patch.dict(os.environ, ENV, clear=True):
            _provider(tmp, virtual_fake, addressing="virtual").deploy(site)
        virtual_put = next(record for record in virtual_fake.requests if record.method == "PUT")
        auto_fake = _FakeS3()
        with patch.dict(os.environ, ENV, clear=True):
            _provider(tmp, auto_fake, endpoint="https://s3.us-east-1.amazonaws.com", addressing="auto").deploy(site)
        auto_put = next(record for record in auto_fake.requests if record.method == "PUT")
    virtual_url = urlsplit(virtual_put.url)
    auto_url = urlsplit(auto_put.url)
    return (
        virtual_url.hostname == "docs.s3.example.test"
        and virtual_url.path == "/site/index.html"
        and virtual_put.headers.get("host") == "docs.s3.example.test"
        and auto_url.hostname == "docs.s3.us-east-1.amazonaws.com"
        and auto_url.path == "/site/index.html"
    )


def _test_config_is_validated():
    with TemporaryDirectory() as tmp:
        try:
            get_provider("s3", {"bucket": "docs"}, instance_root=Path(tmp))
            missing_endpoint = ""
        except DocsDeployError as error:
            missing_endpoint = error.key
        try:
            get_provider("s3", {"endpoint": "https://s3.example.test"}, instance_root=Path(tmp))
            missing_bucket = ""
        except DocsDeployError as error:
            missing_bucket = error.key
        try:
            get_provider("ftp", {}, instance_root=Path(tmp))
            unknown = ""
            provider_name = ""
        except DocsDeployError as error:
            unknown = error.key
            provider_name = error.params.get("provider")
    return (
        missing_endpoint == "cli.docs.deploy.s3.missing_endpoint"
        and missing_bucket == "cli.docs.deploy.s3.missing_bucket"
        and unknown == "cli.docs.deploy.unknown_provider"
        and provider_name == "ftp"
    )


def _test_missing_credentials_are_reported():
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": "x"})
        fake = _FakeS3()
        provider = _provider(tmp, fake)
        with patch.dict(os.environ, {}, clear=True):
            try:
                provider.deploy(site)
                key = ""
            except DocsDeployError as error:
                key = error.key
    return key == "cli.docs.deploy.s3.missing_credentials" and not fake.requests


def _test_http_failures_are_summarized():
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": "home", "assets/app.js": "js"})
        list_failure = _FakeS3(failures={("GET", "*"): 403})
        with patch.dict(os.environ, ENV, clear=True):
            try:
                _provider(tmp, list_failure).deploy(site)
                list_key = ""
                list_detail = ""
            except DocsDeployError as error:
                list_key = error.key
                list_detail = error.params.get("detail", "")
        upload_failure = _FakeS3(failures={("PUT", "site/assets/app.js"): 500})
        with patch.dict(os.environ, ENV, clear=True):
            try:
                _provider(tmp, upload_failure).deploy(site)
                upload_key = ""
                uploaded = -1
                failed = -1
                upload_detail = ""
            except DocsDeployError as error:
                upload_key = error.key
                uploaded = error.params.get("uploaded", -1)
                failed = error.params.get("failed", -1)
                upload_detail = error.params.get("detail", "")
        delete_failure = _FakeS3(
            {
                "site/index.html": (_md5("home"), 4),
                "site/old.html": (_md5("old"), 3),
            },
            failures={("DELETE", "site/old.html"): 403},
        )
        with patch.dict(os.environ, ENV, clear=True):
            try:
                _provider(tmp, delete_failure).deploy(site, delete=True)
                delete_key = ""
                delete_detail = ""
            except DocsDeployError as error:
                delete_key = error.key
                delete_detail = error.params.get("detail", "")
        invalid = _FakeS3(raw_list="not xml")
        with patch.dict(os.environ, ENV, clear=True):
            try:
                _provider(tmp, invalid).deploy(site)
                xml_key = ""
                xml_detail = ""
            except DocsDeployError as error:
                xml_key = error.key
                xml_detail = error.params.get("detail", "")
    return (
        list_key == "cli.docs.deploy.s3.list_failed"
        and "403" in list_detail
        and "Denied" in list_detail
        and SECRET_KEY not in list_detail
        and "***" in list_detail
        and upload_key == "cli.docs.deploy.s3.upload_failed"
        and uploaded == 1
        and failed == 1
        and "500" in upload_detail
        and delete_key == "cli.docs.deploy.s3.delete_failed"
        and "403" in delete_detail
        and xml_key == "cli.docs.deploy.s3.list_failed"
        and "invalid XML" in xml_detail
    )


def _test_region_fallback_and_session_token():
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": "x"})
        region_fake = _FakeS3()
        env = {**ENV, "AWS_REGION": "eu-west-1", "AWS_SESSION_TOKEN": SESSION_TOKEN}
        with patch.dict(os.environ, env, clear=True):
            _provider(tmp, region_fake, region="").deploy(site)
        region_auth = region_fake.requests[0].headers["authorization"]
        token_header = region_fake.requests[0].headers.get("x-amz-security-token")
        default_fake = _FakeS3()
        with patch.dict(os.environ, {**ENV, "AWS_DEFAULT_REGION": "ap-south-1"}, clear=True):
            _provider(tmp, default_fake, region="").deploy(site)
        default_auth = default_fake.requests[0].headers["authorization"]
        config_fake = _FakeS3()
        with patch.dict(os.environ, {**ENV, "AWS_REGION": "eu-west-1"}, clear=True):
            _provider(tmp, config_fake, region="us-west-2").deploy(site)
        config_auth = config_fake.requests[0].headers["authorization"]
    return (
        "/eu-west-1/s3/aws4_request" in region_auth
        and "x-amz-security-token" in region_auth
        and token_header == SESSION_TOKEN
        and "/ap-south-1/s3/aws4_request" in default_auth
        and "/us-west-2/s3/aws4_request" in config_auth
    )


def _test_cache_control_override():
    with TemporaryDirectory() as tmp:
        site = _write_site(tmp, {"index.html": "x"})
        fake = _FakeS3()
        with patch.dict(os.environ, ENV, clear=True):
            _provider(tmp, fake, cache_control="max-age=120").deploy(site)
        put = next(record for record in fake.requests if record.method == "PUT")
    return put.headers.get("cache-control") == "max-age=120"


@func_case
async def test_docs_deploy_s3(tester: Tester):
    """cli.docs.deploy.s3: S3 兼容存储部署 provider 测试"""
    await tester.test(_test_lists_pages_and_uploads_changes, "分页列取、跳过未变并上传变化文件")
    await tester.test(_test_delete_only_touches_prefix, "删除只触及前缀内的多余键")
    await tester.test(_test_dry_run_counts_without_writes, "试运行只统计不写入")
    await tester.test(_test_virtual_host_and_auto_addressing, "path-style、virtual-host 与自动寻址")
    await tester.test(_test_config_is_validated, "端点、存储桶与 provider 名称校验")
    await tester.test(_test_missing_credentials_are_reported, "缺少凭据时报错")
    await tester.test(_test_http_failures_are_summarized, "列取、上传、删除与响应解析失败")
    await tester.test(_test_region_fallback_and_session_token, "区域回退与会话令牌")
    await tester.test(_test_cache_control_override, "cache_control 覆盖默认缓存策略")
    return tester
