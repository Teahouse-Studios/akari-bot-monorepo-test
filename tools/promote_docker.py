"""解析已构建的最高稳定产品镜像及其确切摘要。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from packaging.version import Version


def _token(image: str) -> str:
    url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{image}:pull"
    with urlopen(url, timeout=30) as response:
        return json.load(response)["token"]


def _digest(image: str, version: str, token: str) -> str | None:
    request = Request(
        f"https://registry-1.docker.io/v2/{image}/manifests/{version}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": ", ".join(
                (
                    "application/vnd.oci.image.index.v1+json",
                    "application/vnd.docker.distribution.manifest.list.v2+json",
                    "application/vnd.oci.image.manifest.v1+json",
                    "application/vnd.docker.distribution.manifest.v2+json",
                )
            ),
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            digest = response.headers.get("Docker-Content-Digest", "")
    except HTTPError as error:
        if error.code == 404:
            payload = json.loads(error.read())
            if payload.get("errors") and all(item.get("code") == "MANIFEST_UNKNOWN" for item in payload["errors"]):
                return None
        raise
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("镜像服务没有提供有效的 manifest SHA256")
    return digest


def _resolve(image: str, tags: list[str]) -> dict:
    versions = sorted(
        (tag for tag in tags if re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag)),
        key=lambda tag: Version(tag[1:]),
        reverse=True,
    )
    token = _token(image)
    for version in versions:
        digest = _digest(image, version, token)
        if digest is not None:
            return {"image": image, "version": version, "digest": digest}
    raise ValueError("没有已构建的稳定产品镜像")


def main() -> None:
    parser = argparse.ArgumentParser(description="选择 Docker latest 应指向的稳定镜像")
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-latest", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*", args.image):
        parser.error("必须提供 Docker Hub 的组织与镜像名")
    if args.verify_latest:
        expected = json.loads(args.output.read_text(encoding="utf-8"))
        if expected["image"] != args.image or _digest(args.image, "latest", _token(args.image)) != expected["digest"]:
            raise ValueError("latest 的远端摘要与本次 promotion 不符")
    else:
        tags = subprocess.check_output(["git", "tag", "--list"], text=True).splitlines()
        args.output.write_text(json.dumps(_resolve(args.image, tags), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
