"""``akaribot.cli.docs.catalog``：清单解析、去重、CLI 本地合并与 registry 回退。"""

import json
from importlib import metadata
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from akaribot.cli import __version__ as cli_version
from akaribot.cli.docs import catalog as docs_catalog
from akaribot.cli.docs.model import DocsError
from akaribot.testing import Tester, func_case


class _FakeInstance:
    def __init__(self, root: Path, responses: dict[str, object]) -> None:
        self.root = Path(root)
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def run_core_capture(self, entrypoint: str, *args: str, timeout: float | None = None, **env: str):
        self.calls.append((entrypoint, *args))
        value = self.responses.get(entrypoint)
        if isinstance(value, BaseException):
            raise value
        return value


def _proc(payload: object = None, *, returncode: int = 0, stderr: str = "") -> SimpleNamespace:
    stdout = "" if payload is None else json.dumps(payload, ensure_ascii=False)
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _page(path: str, title: str, order: int) -> dict[str, object]:
    return {"path": path, "title": title, "order": order}


def _docs_payload(root: Path) -> dict[str, object]:
    return {
        "schema": 1,
        "packages": [
            {
                "key": "wiki",
                "group": "module",
                "dist": "akari-bot-module-wiki",
                "name": "wiki",
                "version": "1.2.0",
                "title": "Wiki 查询",
                "summary": "查询 MediaWiki",
                "doc_path": str(root / "doc" / "wiki"),
                "pages": [_page("guide/setup.md", "安装", 20), _page("index.md", "概览", 0)],
                "editable": True,
            },
            {
                "key": "wiki",
                "group": "module",
                "dist": "akari-bot-module-wiki",
                "name": "wiki",
                "version": "9.9.9",
                "title": "重复条目",
                "summary": "",
                "doc_path": str(root / "doc" / "wiki"),
                "pages": [],
            },
        ],
    }


def _local_doc_dir(base: Path) -> Path:
    directory = base / "cli-docs"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.md").write_text("# 概览\n", encoding="utf-8")
    (directory / "commands.md").write_text("# 命令\n", encoding="utf-8")
    return directory


def _local_version() -> str:
    try:
        return metadata.version(docs_catalog.CLI_DIST)
    except Exception:  # noqa: BLE001 - 与实现一致，冻结环境下没有 metadata
        return cli_version


async def _test_parse_docs_payload():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root, {"docs": _proc(_docs_payload(root))})
        catalog = docs_catalog.load_catalog(instance, include_cli=False)
        first = catalog.packages[0]
        keys = catalog.keys()
        pages = [(page.path, page.title) for page in first.pages]
        calls = instance.calls
    return (
        keys == ("wiki",)
        and first.title == "Wiki 查询"
        and first.version == "1.2.0"
        and first.editable
        and pages == [("index.md", "概览"), ("guide/setup.md", "安装")]
        and calls == [("docs", "list", "--json")]
    )


async def _test_select_filters_and_rejects_unknown():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root, {"docs": _proc(_docs_payload(root))})
        catalog = docs_catalog.load_catalog(instance, include_cli=False)
        selected = catalog.select(["wiki"])
        try:
            catalog.select(["missing"])
        except DocsError as exc:
            error = (str(exc), exc.key, exc.params.get("key"))
        else:
            error = ("", "", "")
    return (
        selected.keys() == ("wiki",)
        and error == ("cli.docs.error.unknown_key", "cli.docs.error.unknown_key", "missing")
        and catalog.select(None) is catalog
    )


async def _test_local_cli_docs_merge():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        local = _local_doc_dir(root)
        payload = _docs_payload(root)
        payload["packages"].append(
            {
                "key": "cli",
                "group": "cli",
                "dist": "akari-bot-cli",
                "name": "cli",
                "version": "0.0.1",
                "title": "远端 CLI",
                "summary": "",
                "doc_path": str(local),
                "pages": [],
            }
        )
        instance = _FakeInstance(root, {"docs": _proc(payload)})
        plain = _FakeInstance(root, {"docs": _proc(_docs_payload(root))})
        with patch.object(docs_catalog, "CLI_DOC_PATH", local):
            merged = docs_catalog.load_catalog(instance)
            without = docs_catalog.load_catalog(plain, include_cli=False)
        cli = [package for package in merged.packages if package.key == "cli"]
        pages = [page.path for page in cli[0].pages] if cli else []
    return (
        len(cli) == 1
        and cli[0].title == "AkariBot CLI"
        and cli[0].version == _local_version()
        and pages == ["index.md", "commands.md"]
        and "cli" in merged.keys()
        and "cli" not in without.keys()
    )


async def _test_registry_fallback_builds_minimal_entries():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        base = Path(raw)
        instance_root = base / "instance"
        package_root = base / "pkg"
        doc = package_root / "doc"
        doc.mkdir(parents=True)
        (doc / "index.md").write_text("# 包首页\n", encoding="utf-8")
        (doc / "notes.md").write_text("正文\n", encoding="utf-8")
        registry = {
            "packages": [
                {
                    "name": "wiki",
                    "kind": "module",
                    "dist": "akari-bot-module-wiki",
                    "version": "1.0.0",
                    "root": str(package_root),
                },
                {
                    "name": "nodocs",
                    "kind": "module",
                    "dist": "akari-bot-module-nodocs",
                    "version": "1.0.0",
                    "root": str(base / "missing"),
                },
            ]
        }
        instance = _FakeInstance(
            instance_root,
            {
                "docs": _proc(returncode=2, stderr="module not found: akaribot.core.entrypoints.docs"),
                "registry": _proc(registry),
            },
        )
        catalog = docs_catalog.load_catalog(instance, include_cli=False)
        package = catalog.packages[0]
        titles = [(page.path, page.title) for page in package.pages]
    return (
        catalog.keys() == ("wiki",)
        and package.doc_path == doc
        and titles == [("index.md", "概览"), ("notes.md", "notes")]
        and len(catalog.warnings) == 1
        and "registry" in catalog.warnings[0]
    )


async def _test_unsupported_schema_falls_back():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        instance = _FakeInstance(
            root,
            {
                "docs": _proc({"schema": 2, "packages": []}),
                "registry": _proc({"packages": []}),
            },
        )
        catalog = docs_catalog.load_catalog(instance, include_cli=False)
        calls = instance.calls
    return catalog.keys() == () and len(catalog.warnings) == 1 and calls[0][0] == "docs" and calls[1][0] == "registry"


async def _test_registry_failure_keeps_warnings():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        instance = _FakeInstance(
            root,
            {
                "docs": RuntimeError("no interpreter"),
                "registry": _proc(returncode=1, stderr="boom"),
            },
        )
        catalog = docs_catalog.load_catalog(instance, include_cli=False)
    return catalog.keys() == () and len(catalog.warnings) == 2 and "no interpreter" in catalog.warnings[0]


@func_case
async def test_docs_catalog(tester: Tester):
    """cli.docs.catalog: 文档目录解析与回退"""
    await tester.test(_test_parse_docs_payload, "解析 docs list 清单并按 order 排序")
    await tester.test(_test_select_filters_and_rejects_unknown, "select 过滤并拒绝未知 key")
    await tester.test(_test_local_cli_docs_merge, "CLI 本地文档覆盖同名远端条目")
    await tester.test(_test_registry_fallback_builds_minimal_entries, "docs 入口不可用时回退 registry")
    await tester.test(_test_unsupported_schema_falls_back, "清单版本不支持时回退 registry")
    await tester.test(_test_registry_failure_keeps_warnings, "两个入口都失败时返回空目录并保留警告")
    return tester
