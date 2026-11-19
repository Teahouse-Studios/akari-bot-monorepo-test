"""AWS Signature Version 4 的最小实现。

只覆盖 S3 需要的请求签名：固定签名 ``host``、``x-amz-content-sha256``、``x-amz-date``
与会话令牌；查询参数按编码后的键值排序，路径段只编码一次。
"""

from __future__ import annotations

import hashlib
import hmac
import os
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import quote, unquote, urlsplit

from .base import DocsDeployError

ALGORITHM = "AWS4-HMAC-SHA256"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
_UNRESERVED = "-_.~"


@dataclass(frozen=True)
class Credentials:
    """一组 AWS 凭据。

    :param access_key: Access Key ID。
    :param secret_key: Secret Access Key。
    :param session_token: 临时凭据的会话令牌，长期凭据为空串。
    """

    access_key: str
    secret_key: str
    session_token: str = ""

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Credentials:
        """从环境变量读取凭据。

        :param environ: 环境变量映射；缺省读取 ``os.environ``。
        :return: 凭据。
        :raises DocsDeployError: Access Key ID 或 Secret Access Key 缺失。
        """
        source = os.environ if environ is None else environ
        access_key = str(source.get("AWS_ACCESS_KEY_ID") or "").strip()
        secret_key = str(source.get("AWS_SECRET_ACCESS_KEY") or "").strip()
        if not access_key or not secret_key:
            raise DocsDeployError("cli.docs.deploy.s3.missing_credentials")
        return cls(
            access_key=access_key,
            secret_key=secret_key,
            session_token=str(source.get("AWS_SESSION_TOKEN") or "").strip(),
        )


def sha256_hex(data: bytes) -> str:
    """返回请求体的 SHA-256 十六进制摘要。"""
    return hashlib.sha256(data).hexdigest()


def canonical_uri(path: str) -> str:
    """返回签名用的规范化路径，保留已有的百分号转义。"""
    return quote(path or "/", safe="/%")


def canonical_query(pairs: Iterable[tuple[str, str]]) -> str:
    """把查询参数编码并按 AWS 规则排序。

    排序依据是编码后的键与值；空值保留为 ``key=``。
    """
    encoded = sorted((quote(str(key), safe=_UNRESERVED), quote(str(value), safe=_UNRESERVED)) for key, value in pairs)
    return "&".join(f"{key}={value}" for key, value in encoded)


def sign_request(
    method: str,
    url: str,
    *,
    credentials: Credentials,
    region: str,
    service: str = "s3",
    headers: Mapping[str, str] | None = None,
    payload_hash: str | None = None,
    now: datetime | None = None,
) -> dict[str, str]:
    """为一次请求生成签名头。

    :param method: HTTP 方法。
    :param url: 完整请求地址，路径可以已编码。
    :param credentials: 签名凭据。
    :param region: 区域。
    :param service: 服务名，S3 固定为 ``s3``。
    :param headers: 参与签名的附加请求头。
    :param payload_hash: 请求体的 SHA-256 摘要；缺省按空请求体处理。
    :param now: 签名时间，缺省取当前 UTC 时间。
    :return: 可直接发送的请求头，含 ``Authorization``、``Host`` 与 ``x-amz-*``。
    """
    parsed = urlsplit(url)
    host = parsed.netloc.rsplit("@", 1)[-1]
    stamp = (now or datetime.now(UTC)).astimezone(UTC)
    amz_date = stamp.strftime("%Y%m%dT%H%M%SZ")
    date = stamp.strftime("%Y%m%d")
    digest = payload_hash or EMPTY_SHA256

    canonical_headers: dict[str, str] = {}
    for key, value in (headers or {}).items():
        name = key.strip().lower()
        if name == "authorization":
            continue
        canonical_headers[name] = _normalize_header(value)
    canonical_headers["host"] = host
    canonical_headers["x-amz-content-sha256"] = digest
    canonical_headers["x-amz-date"] = amz_date
    if credentials.session_token:
        canonical_headers["x-amz-security-token"] = credentials.session_token
    signed_names = sorted(canonical_headers)
    canonical_request = "\n".join(
        [
            method.upper(),
            canonical_uri(parsed.path),
            canonical_query(_query_pairs(parsed.query)),
            "".join(f"{name}:{canonical_headers[name]}\n" for name in signed_names),
            ";".join(signed_names),
            digest,
        ]
    )
    scope = f"{date}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [ALGORITHM, amz_date, scope, hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()]
    )
    signing_key = _signing_key(credentials.secret_key, date, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"{ALGORITHM} Credential={credentials.access_key}/{scope}, "
        f"SignedHeaders={';'.join(signed_names)}, Signature={signature}"
    )

    result = {key: value for key, value in (headers or {}).items() if key.strip().lower() != "authorization"}
    result["Host"] = host
    result["x-amz-content-sha256"] = digest
    result["x-amz-date"] = amz_date
    if credentials.session_token:
        result["x-amz-security-token"] = credentials.session_token
    result["Authorization"] = authorization
    return result


def _query_pairs(query: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for part in query.split("&"):
        if not part:
            continue
        key, _, value = part.partition("=")
        pairs.append((unquote(key), unquote(value)))
    return pairs


def _normalize_header(value: object) -> str:
    return " ".join(str(value).split())


def _signing_key(secret_key: str, date: str, region: str, service: str) -> bytes:
    key = _hmac(("AWS4" + secret_key).encode("utf-8"), date)
    key = _hmac(key, region)
    key = _hmac(key, service)
    return _hmac(key, "aws4_request")


def _hmac(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()
