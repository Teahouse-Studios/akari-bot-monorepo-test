"""``akaribot.cli.docs.builder``：构建编排、指纹复用与强制重建。"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from akaribot.cli.docs import builder
from akaribot.cli.docs import catalog as docs_catalog
from akaribot.cli.docs.model import DocsError, ToolchainInfo
from akaribot.testing import Tester, func_case


class _FakeInstance:
    def __init__(self, root: Path, payload: dict[str, object]) -> None:
        self.root = Path(root)
        self.payload = payload

    def run_core_capture(self, entrypoint: str, *args: str, timeout: float | None = None, **env: str):
        if entrypoint == "docs":
            return SimpleNamespace(returncode=0, stdout=json.dumps(self.payload, ensure_ascii=False), stderr="")
        return SimpleNamespace(returncode=0, stdout=json.dumps({"packages": []}), stderr="")


def _payload(doc_path: Path) -> dict[str, object]:
    return {
        "schema": 1,
        "packages": [
            {
                "key": "demo",
                "group": "module",
                "dist": "akari-bot-module-demo",
                "name": "demo",
                "version": "1.0.0",
                "title": "Demo",
                "summary": "示例",
                "doc_path": str(doc_path),
                "pages": [
                    {"path": "index.md", "title": "概览", "order": 0},
                    {"path": "guide.md", "title": "指南", "order": 10},
                ],
            }
        ],
    }


async def _test_build_reuses_fingerprint_and_force():
    with TemporaryDirectory(prefix="akari-docs-build-") as raw:
        root = Path(raw)
        doc = root / "doc-demo"
        doc.mkdir()
        (doc / "index.md").write_text("# Demo\n", encoding="utf-8")
        (doc / "guide.md").write_text("# 指南\n", encoding="utf-8")
        instance = _FakeInstance(root, _payload(doc))
        counters = {"ensure": 0, "build": 0, "detect": 0}
        offline_flags: list[bool] = []
        stages: list[str] = []

        def fake_detect():
            counters["detect"] += 1
            return ToolchainInfo("/bin/node", "/bin/npm", "v24.21.0", "11.19.0", True, "")

        def fake_ensure(cache_dir, template_dir, offline=False):
            counters["ensure"] += 1
            offline_flags.append(offline)
            return Path(cache_dir) / "docs"

        def fake_build(docs_dir, src_dir, out_dir):
            counters["build"] += 1
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            (Path(out_dir) / "index.html").write_text("site", encoding="utf-8")
            return "built\n"

        with (
            patch.object(builder, "detect", side_effect=fake_detect),
            patch.object(builder, "ensure_toolchain", side_effect=fake_ensure),
            patch.object(builder, "run_build", side_effect=fake_build),
            patch.object(docs_catalog, "CLI_DOC_PATH", root / "absent-cli-doc"),
        ):
            first = builder.build(instance, reporter=stages.append)
            second = builder.build(instance)
            after_second = counters["build"]
            (doc / "guide.md").write_text("# 指南（更新）\n", encoding="utf-8")
            third = builder.build(instance)
            after_third = counters["build"]
            (doc / "doc.toml").write_text('schema = 1\n[[meta.modules]]\nname = "demo"\n', encoding="utf-8")
            fourth = builder.build(instance)
            after_fourth = counters["build"]
            forced = builder.build(instance, force=True, offline=True)
            selected = builder.build(instance, keys=["demo"], force=True)
            try:
                builder.build(instance, keys=["missing"])
            except DocsError as exc:
                unknown = (str(exc), exc.params.get("key"))
            else:
                unknown = ("", "")
            state = json.loads((root / ".docs" / "state.json").read_text(encoding="utf-8"))

        out = root / "cache" / "docs" / "site"
        generated = root / "cache" / "docs" / "src"
        out_exists = (out / "index.html").is_file()
        generated_exists = (generated / "demo" / "guide.md").is_file()
    return (
        not first.reused
        and first.packages == ("demo",)
        and first.log == "built\n"
        and stages == ["toolchain", "generate", "build", "done"]
        and out_exists
        and generated_exists
        and second.reused
        and second.fingerprint == first.fingerprint
        and after_second == 1
        and counters["ensure"] == 5
        and counters["detect"] == 5
        and not third.reused
        and third.fingerprint != first.fingerprint
        and after_third == 2
        and not fourth.reused
        and fourth.fingerprint != third.fingerprint
        and after_fourth == 3
        and not forced.reused
        and offline_flags[3] is True
        and selected.packages == ("demo",)
        and unknown == ("cli.docs.error.unknown_key", "missing")
        and counters["build"] == 5
        and state["schema"] == 1
        and state["build"]["fingerprint"] == selected.fingerprint
        and state["build"]["base"] == "/"
    )


async def _test_build_reports_missing_toolchain():
    with TemporaryDirectory(prefix="akari-docs-build-") as raw:
        root = Path(raw)
        doc = root / "doc-demo"
        doc.mkdir()
        (doc / "index.md").write_text("# Demo\n", encoding="utf-8")
        instance = _FakeInstance(root, _payload(doc))
        with patch.object(builder, "detect", return_value=ToolchainInfo("", "", "", "", False, "node not found")):
            try:
                builder.build(instance)
            except DocsError as exc:
                error = (str(exc), exc.params.get("detail"))
            else:
                error = ("", "")
    return error == ("cli.docs.error.toolchain_missing", "node not found")


@func_case
async def test_docs_builder(tester: Tester):
    """cli.docs.builder: 构建编排与缓存复用"""
    await tester.test(_test_build_reuses_fingerprint_and_force, "指纹复用、内容变更、force 与未知 key")
    await tester.test(_test_build_reports_missing_toolchain, "工具链不可用时报错")
    return tester
