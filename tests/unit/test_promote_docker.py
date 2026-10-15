import io
import json
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch

from akaribot.testing import Tester, func_case
from tools import promote_docker as tool


def _test_old_run_selects_highest_available_image():
    with (
        patch.object(tool, "_token", return_value="token"),
        patch.object(tool, "_digest", side_effect=lambda image, version, token: "sha256:" + "a" * 64),
    ):
        result = tool._resolve("example/bot", ["v5.1.2", "v6.0.0", "v6.0.1rc1", "nightly"])
    return result["version"] == "v6.0.0"


def _test_new_tag_without_image_keeps_highest_built_version():
    with (
        patch.object(tool, "_token", return_value="token"),
        patch.object(tool, "_digest", side_effect=[None, "sha256:" + "b" * 64]),
    ):
        result = tool._resolve("example/bot", ["v6.0.1", "v6.0.0", "v5.1.2"])
    return result["version"] == "v6.0.0"


def _test_auth_failure_cannot_fall_back_to_old_image():
    with (
        patch.object(tool, "_token", return_value="token"),
        patch.object(tool, "_digest", side_effect=HTTPError("url", 401, "unauthorized", {}, None)),
    ):
        try:
            tool._resolve("example/bot", ["v6.0.0", "v5.1.2"])
        except HTTPError:
            return True
    return False


def _test_only_manifest_unknown_is_absent():
    missing = HTTPError(
        "url", 404, "missing", {}, io.BytesIO(json.dumps({"errors": [{"code": "MANIFEST_UNKNOWN"}]}).encode())
    )
    forbidden = HTTPError(
        "url", 404, "missing", {}, io.BytesIO(json.dumps({"errors": [{"code": "UNAUTHORIZED"}]}).encode())
    )
    with patch.object(tool, "urlopen", side_effect=missing):
        absent = tool._digest("example/bot", "v6.0.0", "token")
    with patch.object(tool, "urlopen", side_effect=forbidden):
        try:
            tool._digest("example/bot", "v6.0.0", "token")
        except HTTPError:
            return absent is None
    return False


def _test_promotion_verifies_final_remote_digest():
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "promotion.json"
        output.write_text(json.dumps({"image": "example/bot", "version": "v6.0.0", "digest": "sha256:" + "a" * 64}))
        argv = ["promote_docker.py", "--image", "example/bot", "--output", str(output), "--verify-latest"]
        with (
            patch.object(sys, "argv", argv),
            patch.object(tool, "_token", return_value="token"),
            patch.object(tool, "_digest", return_value="sha256:" + "a" * 64),
        ):
            tool.main()
        with (
            patch.object(sys, "argv", argv),
            patch.object(tool, "_token", return_value="token"),
            patch.object(tool, "_digest", return_value="sha256:" + "b" * 64),
        ):
            try:
                tool.main()
            except ValueError:
                return True
    return False


@func_case
async def test_promote_docker(tester: Tester):
    """稳定 Docker 镜像 promotion 版本与错误处理验证。"""
    for function, label in (
        (_test_old_run_selects_highest_available_image, "旧运行也选择已构建的最高稳定产品镜像"),
        (_test_new_tag_without_image_keeps_highest_built_version, "尚未构建的新 tag 不覆盖可用镜像"),
        (_test_auth_failure_cannot_fall_back_to_old_image, "认证错误不能降级选择旧镜像"),
        (_test_only_manifest_unknown_is_absent, "只有明确的 manifest 不存在才跳过版本"),
        (_test_promotion_verifies_final_remote_digest, "推广后校验远端 latest 的确切摘要"),
    ):
        await tester.test(function, label)
    return tester
