"""S3 兼容存储的部署 provider。

同步只比较 ``prefix`` 下的键：本地文件的 MD5 与大小对上远端 ETag 即跳过，其余 PUT 上传；
``delete`` 为真时再删除远端多出的键。上传并发执行，单个失败不中断其余文件，最后汇总成一个错误。
"""

from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import xml.etree.ElementTree as ET
from collections.abc import Iterator, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

import httpx

from .base import DeployResult, DeployTarget, DocsDeployError, Reporter
from .sigv4 import Credentials, canonical_query, sha256_hex, sign_request

DEFAULT_REGION = "us-east-1"
DEFAULT_TIMEOUT = 60.0
UPLOAD_WORKERS = 8
DETAIL_LIMIT = 300
IMMUTABLE_CACHE = "public, max-age=31536000, immutable"
NO_CACHE = "no-cache"
ASSET_PREFIX = "assets/"
HTML_SUFFIXES = frozenset({".html", ".htm"})
CHUNK_SIZE = 1024 * 1024
LIST_FAILED = "cli.docs.deploy.s3.list_failed"
UPLOAD_FAILED = "cli.docs.deploy.s3.upload_failed"
DELETE_FAILED = "cli.docs.deploy.s3.delete_failed"
_DNS_BUCKET = re.compile(r"^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$")


@dataclass(frozen=True)
class _LocalFile:
    relative: str
    key: str
    path: Path
    size: int
    md5: str


@dataclass(frozen=True)
class _RemoteObject:
    key: str
    etag: str
    size: int | None


class S3Provider:
    """S3 兼容存储的部署 provider。

    :param config: ``docs.toml`` 的 ``[deploy.s3]`` 子表。
    :param instance_root: 实例根目录。
    :param transport: httpx transport，测试可注入。
    :raises DocsDeployError: 端点或存储桶缺失、端点无效。
    """

    name = "s3"

    def __init__(
        self,
        config: Mapping[str, Any],
        *,
        instance_root: Path,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        endpoint = _text(config, "endpoint").strip().rstrip("/")
        if not endpoint:
            raise DocsDeployError("cli.docs.deploy.s3.missing_endpoint")
        if "://" not in endpoint:
            endpoint = f"https://{endpoint}"
        parsed = urlsplit(endpoint)
        if not parsed.scheme or not parsed.netloc:
            raise DocsDeployError("cli.docs.deploy.s3.missing_endpoint")
        self._endpoint = endpoint
        self._bucket = _text(config, "bucket").strip()
        if not self._bucket:
            raise DocsDeployError("cli.docs.deploy.s3.missing_bucket")
        self._region = _text(config, "region").strip()
        self._prefix = _normalize_prefix(_text(config, "prefix"))
        self._public_url = _text(config, "public_url").strip().rstrip("/")
        self._addressing = _addressing(_text(config, "addressing"))
        self._cache_control = _text(config, "cache_control").strip()
        self._transport = transport

    def plan(self, site_dir: Path) -> DeployTarget:
        """返回目标摘要，不访问远端。"""
        files = _scan(_require_site(site_dir), self._prefix)
        return DeployTarget("s3", "S3", f"{self._target_text()} ({len(files)} objects)")

    def deploy(
        self,
        site_dir: Path,
        *,
        dry_run: bool = False,
        delete: bool = False,
        reporter: Reporter | None = None,
    ) -> DeployResult:
        """把站点目录同步到存储桶。

        试运行仍会列出一遍远端对象，以便给出准确的上传与删除数量；除列取外不写入远端。
        """
        site = _require_site(site_dir)
        local = {item.key: item for item in _scan(site, self._prefix)}
        credentials = Credentials.from_env()
        notify = reporter or _ignore
        notify("list")
        with self._client() as client:
            remote = self._list_remote(client, credentials)
            changed = [item for key, item in local.items() if _needs_upload(item, remote.get(key))]
            stale = [key for key in remote if key not in local]
            skipped = len(local) - len(changed)
            if dry_run:
                return DeployResult(
                    ok=True,
                    provider="s3",
                    url=self._site_url(),
                    detail=self._target_text(),
                    uploaded=len(changed),
                    deleted=len(stale) if delete else 0,
                    skipped=skipped,
                    dry_run=True,
                )
            uploaded = 0
            if changed:
                notify("upload")
                uploaded = self._upload_all(client, credentials, changed)
            deleted = 0
            if delete and stale:
                notify("delete")
                deleted = self._delete_all(client, credentials, stale)
            notify("done")
            return DeployResult(
                ok=True,
                provider="s3",
                url=self._site_url(),
                detail=self._target_text(),
                uploaded=uploaded,
                deleted=deleted,
                skipped=skipped,
            )

    def _list_remote(self, client: httpx.Client, credentials: Credentials) -> dict[str, _RemoteObject]:
        objects: dict[str, _RemoteObject] = {}
        token = ""
        while True:
            params = [("list-type", "2")]
            if self._prefix:
                params.append(("prefix", self._prefix))
            if token:
                params.append(("continuation-token", token))
            response = self._request(
                client,
                "GET",
                self._object_url("", params),
                credentials,
                error_key=LIST_FAILED,
            )
            try:
                root = ET.fromstring(response.text)
            except ET.ParseError as exc:
                raise DocsDeployError(LIST_FAILED, detail=f"invalid XML: {exc}") from exc
            for node in root.iter():
                if _local_name(node.tag) != "Contents":
                    continue
                key = _child_text(node, "Key")
                if not key or not self._in_prefix(key):
                    continue
                etag = _child_text(node, "ETag").strip('"')
                size_text = _child_text(node, "Size")
                size = int(size_text) if size_text.isdigit() else None
                objects[key] = _RemoteObject(key, etag, size)
            token = _child_text(root, "NextContinuationToken")
            if _child_text(root, "IsTruncated").lower() != "true" or not token:
                return objects

    def _upload_all(
        self,
        client: httpx.Client,
        credentials: Credentials,
        files: Sequence[_LocalFile],
    ) -> int:
        uploaded = 0
        failures: list[str] = []
        with ThreadPoolExecutor(max_workers=min(UPLOAD_WORKERS, len(files))) as pool:
            futures = {pool.submit(self._upload_one, client, credentials, item): item for item in files}
            for future in as_completed(futures):
                try:
                    future.result()
                    uploaded += 1
                except DocsDeployError as exc:
                    failures.append(f"{futures[future].key}: {exc.params.get('detail') or exc.key}")
        if failures:
            detail = f"{uploaded} uploaded, {len(failures)} failed: {failures[0]}"
            raise DocsDeployError(UPLOAD_FAILED, detail=detail, uploaded=uploaded, failed=len(failures))
        return uploaded

    def _upload_one(self, client: httpx.Client, credentials: Credentials, item: _LocalFile) -> None:
        try:
            body = item.path.read_bytes()
        except OSError as exc:
            raise DocsDeployError(UPLOAD_FAILED, detail=f"{item.key}: {exc}") from exc
        headers = {"Content-Type": _content_type(item.relative)}
        cache_control = _cache_control(item.relative, self._cache_control)
        if cache_control:
            headers["Cache-Control"] = cache_control
        self._request(
            client,
            "PUT",
            self._object_url(item.key),
            credentials,
            body=body,
            headers=headers,
            error_key=UPLOAD_FAILED,
        )

    def _delete_all(self, client: httpx.Client, credentials: Credentials, keys: Sequence[str]) -> int:
        deleted = 0
        failures: list[str] = []
        for key in keys:
            try:
                self._request(client, "DELETE", self._object_url(key), credentials, error_key=DELETE_FAILED)
                deleted += 1
            except DocsDeployError as exc:
                failures.append(f"{key}: {exc.params.get('detail') or exc.key}")
        if failures:
            detail = f"{deleted} deleted, {len(failures)} failed: {failures[0]}"
            raise DocsDeployError(DELETE_FAILED, detail=detail, deleted=deleted, failed=len(failures))
        return deleted

    def _request(
        self,
        client: httpx.Client,
        method: str,
        url: str,
        credentials: Credentials,
        *,
        body: bytes = b"",
        headers: Mapping[str, str] | None = None,
        error_key: str,
    ) -> httpx.Response:
        signed = sign_request(
            method,
            url,
            credentials=credentials,
            region=self._region_value(),
            headers=headers,
            payload_hash=sha256_hex(body),
        )
        try:
            response = client.request(method, url, headers=signed, content=body or None)
        except httpx.HTTPError as exc:
            raise DocsDeployError(error_key, detail=_redact(str(exc), credentials)) from exc
        if response.status_code >= 300:
            raise DocsDeployError(error_key, detail=_http_detail(response, credentials))
        return response

    @contextmanager
    def _client(self) -> Iterator[httpx.Client]:
        client = httpx.Client(transport=self._transport, timeout=DEFAULT_TIMEOUT)
        try:
            yield client
        finally:
            client.close()

    def _object_url(self, key: str, params: Sequence[tuple[str, str]] = ()) -> str:
        url = self._base_url(key)
        query = canonical_query(params)
        return f"{url}?{query}" if query else url

    def _base_url(self, key: str) -> str:
        parsed = urlsplit(self._endpoint)
        base_path = parsed.path.rstrip("/")
        encoded = quote(key, safe="/-_.~")
        if self._addressing_value() == "virtual":
            netloc = f"{self._bucket}.{parsed.netloc}"
            path = f"{base_path}/{encoded}" if encoded else f"{base_path}/"
            return urlunsplit((parsed.scheme, netloc, path or "/", "", ""))
        path = f"{base_path}/{self._bucket}"
        if encoded:
            path = f"{path}/{encoded}"
        return urlunsplit((parsed.scheme, parsed.netloc, path or "/", "", ""))

    def _addressing_value(self) -> str:
        if self._addressing != "auto":
            return self._addressing
        host = urlsplit(self._endpoint).hostname or ""
        if host.endswith(".amazonaws.com") and _DNS_BUCKET.fullmatch(self._bucket) and ".." not in self._bucket:
            return "virtual"
        return "path"

    def _in_prefix(self, key: str) -> bool:
        return not self._prefix or key.startswith(self._prefix)

    def _target_text(self) -> str:
        return f"s3://{self._bucket}/{self._prefix}"

    def _site_url(self) -> str:
        if self._public_url:
            return f"{self._public_url}/"
        return self._object_url(f"{self._prefix}index.html")

    def _region_value(self) -> str:
        return (
            self._region
            or str(os.environ.get("AWS_REGION") or "").strip()
            or str(os.environ.get("AWS_DEFAULT_REGION") or "").strip()
            or DEFAULT_REGION
        )


def _scan(site: Path, prefix: str) -> list[_LocalFile]:
    files: list[_LocalFile] = []
    for current, dirs, names in os.walk(site, followlinks=False):
        dirs.sort()
        for name in sorted(names):
            path = Path(current) / name
            if path.is_symlink():
                continue
            relative = path.relative_to(site).as_posix()
            md5 = hashlib.md5(usedforsecurity=False)
            try:
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
                        md5.update(chunk)
                size = path.stat().st_size
            except OSError as exc:
                raise DocsDeployError(UPLOAD_FAILED, detail=f"{relative}: {exc}") from exc
            files.append(
                _LocalFile(
                    relative=relative,
                    key=f"{prefix}{relative}",
                    path=path,
                    size=size,
                    md5=md5.hexdigest(),
                )
            )
    return files


def _needs_upload(local: _LocalFile, remote: _RemoteObject | None) -> bool:
    if remote is None:
        return True
    if remote.etag != local.md5:
        return True
    return remote.size is not None and remote.size != local.size


def _require_site(site_dir: Path) -> Path:
    site = Path(site_dir).expanduser().resolve()
    if not site.is_dir():
        raise DocsDeployError("cli.docs.deploy.site_missing", path=str(site_dir))
    return site


def _normalize_prefix(value: str) -> str:
    text = value.strip().strip("/")
    return f"{text}/" if text else ""


def _addressing(value: str) -> str:
    text = value.strip().lower()
    return text if text in {"path", "virtual"} else "auto"


def _content_type(relative: str) -> str:
    return mimetypes.guess_type(relative)[0] or "application/octet-stream"


def _cache_control(relative: str, override: str) -> str:
    if override:
        return override
    if relative.startswith(ASSET_PREFIX):
        return IMMUTABLE_CACHE
    if Path(relative).suffix.lower() in HTML_SUFFIXES:
        return NO_CACHE
    return ""


def _http_detail(response: httpx.Response, credentials: Credentials) -> str:
    text = " ".join((response.text or "").split())
    detail = f"HTTP {response.status_code}"
    if text:
        detail = f"{detail}: {text[:DETAIL_LIMIT]}"
    return _redact(detail, credentials)


def _redact(text: str, credentials: Credentials) -> str:
    for secret in (credentials.secret_key, credentials.session_token, credentials.access_key):
        if secret:
            text = text.replace(secret, "***")
    return text


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(node: ET.Element, name: str) -> str:
    for child in node:
        if _local_name(child.tag) == name:
            return (child.text or "").strip()
    return ""


def _text(data: Mapping[str, Any], name: str) -> str:
    value = data.get(name)
    return "" if value is None else str(value)


def _ignore(_: str) -> None:
    return None
