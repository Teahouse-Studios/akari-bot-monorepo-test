"""``cli.docs.deploy.sigv4``：AWS Signature Version 4 签名。

覆盖 S3 需要的 GET(ListObjectsV2)、PUT 与 DELETE。前两个期望值取自 AWS 文档的
GET Object 与 GET Bucket 示例，其余由 botocore 交叉核对后固化，用例全程离线。
"""

from datetime import UTC, datetime

from akaribot.cli.docs.deploy.base import DocsDeployError
from akaribot.cli.docs.deploy.sigv4 import (
    Credentials,
    canonical_query,
    canonical_uri,
    sha256_hex,
    sign_request,
)
from akaribot.testing import Tester, func_case

ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
NOW = datetime(2013, 5, 24, tzinfo=UTC)
BUCKET_URL = "https://examplebucket.s3.amazonaws.com"


def _credentials(token: str = "") -> Credentials:
    return Credentials(ACCESS_KEY, SECRET_KEY, token)


def _signature(authorization: str) -> str:
    return authorization.rsplit("Signature=", 1)[-1]


def _sign(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    body: bytes = b"",
    credentials: Credentials | None = None,
) -> dict[str, str]:
    return sign_request(
        method,
        url,
        credentials=credentials or _credentials(),
        region="us-east-1",
        headers=headers,
        payload_hash=sha256_hex(body),
        now=NOW,
    )


def _test_official_get_object_vector():
    signed = _sign("GET", f"{BUCKET_URL}/test.txt", {"Range": "bytes=0-9"})
    return (
        _signature(signed["Authorization"]) == "f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41"
        and "SignedHeaders=host;range;x-amz-content-sha256;x-amz-date" in signed["Authorization"]
        and signed["Host"] == "examplebucket.s3.amazonaws.com"
        and signed["x-amz-date"] == "20130524T000000Z"
        and signed["x-amz-content-sha256"] == sha256_hex(b"")
        and "Range" in signed
    )


def _test_official_list_vector():
    signed = _sign("GET", f"{BUCKET_URL}/?max-keys=2&prefix=J")
    return (
        _signature(signed["Authorization"]) == "34b48302e7b5fa45bde8084f4b7868a86f0a534bc59db6670ed5711ef69dc6f7"
        and "SignedHeaders=host;x-amz-content-sha256;x-amz-date" in signed["Authorization"]
        and canonical_query([("prefix", "J"), ("max-keys", "2")]) == "max-keys=2&prefix=J"
    )


def _test_put_and_delete_vectors():
    put = _sign(
        "PUT",
        f"{BUCKET_URL}/upload/a.txt",
        {"Content-Type": "text/plain", "Cache-Control": "no-cache"},
        b"hello",
    )
    delete = _sign("DELETE", f"{BUCKET_URL}/upload/a.txt")
    return (
        _signature(put["Authorization"]) == "d8e9a002e95899cc5231a280744180a8dfeee09940fb05b8ab724e994ccf87f8"
        and "SignedHeaders=cache-control;content-type;host;x-amz-content-sha256;x-amz-date" in put["Authorization"]
        and put["x-amz-content-sha256"] == sha256_hex(b"hello")
        and _signature(delete["Authorization"]) == "88796840db6ce1a1338b24f6d9ee8265ee8f9e3cd34cb675746da96448f10d4d"
    )


def _test_encoded_path_is_not_double_encoded():
    signed = _sign(
        "PUT",
        f"{BUCKET_URL}/test%24file.text",
        {"Content-Type": "text/plain; charset=utf-8"},
        b"hello",
    )
    return (
        _signature(signed["Authorization"]) == "db2f6612a499e991276ac3c8b76233c5414f37f2df55d0a0ba2fce2e61660ab6"
        and canonical_uri("/test%24file.text") == "/test%24file.text"
        and canonical_uri("/a b/中") == "/a%20b/%E4%B8%AD"
        and canonical_uri("") == "/"
    )


def _test_query_encoding_and_sorting():
    query = canonical_query([("prefix", "a b/c"), ("list-type", "2"), ("continuation-token", "x/y"), ("empty", "")])
    return (
        query == "continuation-token=x%2Fy&empty=&list-type=2&prefix=a%20b%2Fc"
        and canonical_query([("b", "2"), ("a", "1"), ("a", "0")]) == "a=0&a=1&b=2"
    )


def _test_session_token_is_signed():
    signed = _sign("GET", f"{BUCKET_URL}/test.txt", credentials=_credentials("SESSIONTOKEN"))
    return (
        signed["x-amz-security-token"] == "SESSIONTOKEN"
        and "x-amz-security-token" in signed["Authorization"]
        and _signature(signed["Authorization"]) == "1db744c2885650b493959873e99d1835a31a5b7a627e9b7913836b78175e4332"
    )


def _test_credentials_come_from_env():
    loaded = Credentials.from_env(
        {
            "AWS_ACCESS_KEY_ID": ACCESS_KEY,
            "AWS_SECRET_ACCESS_KEY": SECRET_KEY,
            "AWS_SESSION_TOKEN": "TOKEN",
        }
    )
    try:
        Credentials.from_env({"AWS_ACCESS_KEY_ID": ACCESS_KEY})
        missing = ""
    except DocsDeployError as error:
        missing = error.key
    return (
        loaded == Credentials(ACCESS_KEY, SECRET_KEY, "TOKEN") and missing == "cli.docs.deploy.s3.missing_credentials"
    )


@func_case
async def test_docs_sigv4(tester: Tester):
    """cli.docs.deploy.sigv4: SigV4 签名测试"""
    await tester.test(_test_official_get_object_vector, "AWS 官方 GET Object 向量")
    await tester.test(_test_official_list_vector, "AWS 官方 GET Bucket 向量")
    await tester.test(_test_put_and_delete_vectors, "PUT 与 DELETE 向量")
    await tester.test(_test_encoded_path_is_not_double_encoded, "已编码路径不重复编码")
    await tester.test(_test_query_encoding_and_sorting, "查询参数编码与排序")
    await tester.test(_test_session_token_is_signed, "会话令牌参与签名")
    await tester.test(_test_credentials_come_from_env, "凭据只从环境变量读取")
    return tester
