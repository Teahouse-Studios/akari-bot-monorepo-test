"""``docs`` 入口的单元测试。

发现过程不导入目标包，测试一律以假 entry point 与假 find_spec 注入包目录；另覆盖 doc.toml、
front matter、隐藏页、无文档告警、符号链接逃逸、目录扫描回退与命令行输出。
"""

import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.core.entrypoints import docs
from akaribot.testing import Tester, func_case


class _Spec:
    def __init__(self, locations: list[str] | None = None, origin: str | None = None):
        self.submodule_search_locations = list(locations or [])
        self.origin = origin


class _Dist:
    def __init__(self, name: str, version: str, summary: str = "", direct_url: str | None = None):
        self.name = name
        self.version = version
        self.metadata = {"Summary": summary}
        self._direct_url = direct_url

    def read_text(self, filename: str) -> str | None:
        return self._direct_url if filename == "direct_url.json" else None


class _EntryPoint:
    def __init__(self, name: str, value: str, dist: _Dist | None = None):
        self.name = name
        self.value = value
        self.dist = dist


def _locator(mapping: dict[str, _Spec]):
    def find_spec(name: str) -> _Spec | None:
        return mapping.get(name)

    return find_spec


def _make_package(root: Path, import_path: str, files: dict[str, str]) -> _Spec:
    directory = root.joinpath(*import_path.split("."))
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "__init__.py").write_text("", encoding="utf-8")
    for name, text in files.items():
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return _Spec([str(directory)])


def _item(payload: dict, key: str) -> dict:
    return next(item for item in payload["packages"] if item["key"] == key)


def _test_metadata_and_sorting():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        specs = {
            "akaribot.core": _make_package(
                root, "akaribot.core", {"doc/index.md": "# 核心\n", "doc/guide.md": "# 指南\n"}
            ),
            "akaribot.modules.alpha": _make_package(
                root, "akaribot.modules.alpha", {"doc/index.md": "# Alpha\n", "doc/doc.toml": "order = 10\n"}
            ),
            "akaribot.modules.beta": _make_package(
                root, "akaribot.modules.beta", {"doc/index.md": "# Beta\n", "doc/doc.toml": "order = 10\n"}
            ),
            "akaribot.modules.zebra": _make_package(
                root, "akaribot.modules.zebra", {"doc/index.md": "# Zebra\n", "doc/doc.toml": "order = 20\n"}
            ),
            "akaribot.adapters.bot": _make_package(
                root, "akaribot.adapters.bot", {"doc/index.md": "# Bot\n", "doc/doc.toml": "order = 5\n"}
            ),
            "akaribot.assets.brand": _make_package(root, "akaribot.assets.brand", {"doc/index.md": "# 品牌\n"}),
            "html2text": _make_package(root, "html2text", {"doc/index.md": "# HTML\n"}),
        }
        editable = '{"dir_info": {"editable": true}}'
        entry_points = [
            _EntryPoint("html2text", "html2text", _Dist("akari-bot-html2text", "2024.2.26", "HTML to text")),
            _EntryPoint("core", "akaribot.core", _Dist("akari-bot-core", "0.1.0", "核心运行时")),
            _EntryPoint(
                "module-zebra", "akaribot.modules.zebra", _Dist("akari-bot-module-zebra", "1.0.0", "", editable)
            ),
            _EntryPoint("module-beta", "akaribot.modules.beta"),
            _EntryPoint("module-alpha", "akaribot.modules.alpha", _Dist("akari-bot-module-alpha", "1.0.0")),
            _EntryPoint("adapter-bot", "akaribot.adapters.bot", _Dist("akari-bot-adapter-bot", "1.0.0")),
            _EntryPoint("assets-brand", "akaribot.assets.brand", _Dist("akari-bot-assets-brand", "1.0.0")),
        ]
        payload = docs.collect(entry_points=lambda: entry_points, find_spec=_locator(specs))

    keys = [item["key"] for item in payload["packages"]]
    groups = [item["group"] for item in payload["packages"]]
    core = _item(payload, "core")
    beta = _item(payload, "module-beta")
    zebra = _item(payload, "module-zebra")
    return (
        payload["schema"] == 1
        and keys
        == [
            "core",
            "module-alpha",
            "module-beta",
            "module-zebra",
            "adapter-bot",
            "assets-brand",
            "html2text",
        ]
        and groups == ["core", "module", "module", "module", "adapter", "asset", "library"]
        and core["dist"] == "akari-bot-core"
        and core["name"] == "core"
        and core["version"] == "0.1.0"
        and core["summary"] == "核心运行时"
        and core["title"] == "core"
        and core["order"] == 500
        and core["editable"] is False
        and core["doc_path"] == str((root / "akaribot" / "core" / "doc").resolve())
        and [Path(page["path"]).name for page in core["pages"]] == ["index.md", "guide.md"]
        and core["pages"][0]["title"] == "核心"
        and core["pages"][0]["path"] == "index.md"
        and beta["dist"] == "akari-bot-module-beta"
        and beta["version"] == "0+local"
        and beta["summary"] == ""
        and zebra["editable"] is True
        and _item(payload, "html2text")["group"] == "library"
    )


def _test_front_matter_overrides_titles():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        specs = {
            "akaribot.modules.demo": _make_package(
                root,
                "akaribot.modules.demo",
                {
                    "doc/index.md": "没有标题\n",
                    "doc/a.md": (
                        '---\ntitle: "自定义标题"\norder: 2\ndescription: 页面摘要\ntags: 忽略\n---\n# 正文标题\n'
                    ),
                    "doc/b.md": "# 正文标题\n",
                    "doc/c.md": "```\n# 代码块内标题\n```\n",
                    "doc/.hidden.md": "# 隐藏页\n",
                    "doc/.draft/inside.md": "# 草稿\n",
                },
            )
        }
        payload = docs.collect(
            entry_points=lambda: [_EntryPoint("module-demo", "akaribot.modules.demo")],
            find_spec=_locator(specs),
        )

    pages = _item(payload, "module-demo")["pages"]
    titles = {Path(page["path"]).name: page["title"] for page in pages}
    return (
        [Path(page["path"]).name for page in pages] == ["index.md", "a.md", "b.md", "c.md"]
        and pages[0]["title"] == "index"
        and titles["a.md"] == "自定义标题"
        and pages[1]["summary"] == "页面摘要"
        and pages[1]["order"] == 2
        and titles["b.md"] == "正文标题"
        and titles["c.md"] == "c"
        and ".hidden.md" not in titles
        and "inside.md" not in titles
    )


def _test_doc_meta_defaults_and_corruption():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        specs = {
            "akaribot.modules.coin": _make_package(root, "akaribot.modules.coin", {"doc/index.md": "# 硬币\n"}),
            "akaribot.modules.broken": _make_package(
                root, "akaribot.modules.broken", {"doc/index.md": "# 损坏\n", "doc/doc.toml": "[broken\n"}
            ),
            "akaribot.modules.wiki": _make_package(
                root,
                "akaribot.modules.wiki",
                {
                    "doc/index.md": "# 维基\n",
                    "doc/doc.toml": 'title = "维基"\nsummary = "文档摘要"\norder = 3\n',
                },
            ),
        }
        entry_points = [
            _EntryPoint("module-coin", "akaribot.modules.coin", _Dist("akari-bot-module-coin", "1.0.0", "硬币模块")),
            _EntryPoint(
                "module-broken", "akaribot.modules.broken", _Dist("akari-bot-module-broken", "1.0.0", "损坏模块")
            ),
            _EntryPoint("module-wiki", "akaribot.modules.wiki", _Dist("akari-bot-module-wiki", "1.0.0", "维基模块")),
        ]
        payload = docs.collect(entry_points=lambda: entry_points, find_spec=_locator(specs))

    coin = _item(payload, "module-coin")
    broken = _item(payload, "module-broken")
    wiki = _item(payload, "module-wiki")
    return (
        coin["title"] == "coin"
        and coin["summary"] == "硬币模块"
        and coin["order"] == 500
        and broken["title"] == "broken"
        and broken["summary"] == "损坏模块"
        and broken["order"] == 500
        and any("doc.toml" in warning and "module-broken" in warning for warning in payload["warnings"])
        and wiki["title"] == "维基"
        and wiki["summary"] == "文档摘要"
        and wiki["order"] == 3
        and len(payload["packages"]) == 3
    )


def _test_hidden_package_is_skipped():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        specs = {
            "akaribot.modules.hidden": _make_package(
                root,
                "akaribot.modules.hidden",
                {"doc/index.md": "# 隐藏\n", "doc/doc.toml": "hidden = true\n"},
            ),
            "akaribot.modules.visible": _make_package(root, "akaribot.modules.visible", {"doc/index.md": "# 可见\n"}),
        }
        payload = docs.collect(
            entry_points=lambda: [
                _EntryPoint("module-hidden", "akaribot.modules.hidden"),
                _EntryPoint("module-visible", "akaribot.modules.visible"),
            ],
            find_spec=_locator(specs),
        )
    return [item["key"] for item in payload["packages"]] == ["module-visible"] and not any(
        "module-hidden" in warning for warning in payload["warnings"]
    )


def _test_missing_documentation_is_reported():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        specs = {
            "akaribot.modules.empty": _make_package(
                root, "akaribot.modules.empty", {"doc/notes.txt": "不是 Markdown\n"}
            ),
            "akaribot.modules.absent": _make_package(root, "akaribot.modules.absent", {"__init__.py": ""}),
        }
        payload = docs.collect(
            entry_points=lambda: [
                _EntryPoint("module-empty", "akaribot.modules.empty"),
                _EntryPoint("module-absent", "akaribot.modules.absent"),
                _EntryPoint("module-unknown", "akaribot.modules.unknown"),
            ],
            find_spec=_locator(specs),
        )
    warnings = "\n".join(payload["warnings"])
    return (
        payload["packages"] == []
        and "module-empty" in warnings
        and "没有 Markdown 文档" in warnings
        and "module-absent" in warnings
        and "module-unknown" in warnings
        and "无法定位导入路径" in warnings
    )


def _test_symlink_escape_is_skipped():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        spec = _make_package(root, "akaribot.modules.demo", {"doc/index.md": "# 可见\n"})
        doc_dir = root / "akaribot" / "modules" / "demo" / "doc"
        outside = root / "outside.md"
        outside.write_text("# 外部\n", encoding="utf-8")
        try:
            (doc_dir / "escape.md").symlink_to(outside)
        except OSError:
            return True
        payload = docs.collect(
            entry_points=lambda: [_EntryPoint("module-demo", "akaribot.modules.demo")],
            find_spec=_locator({"akaribot.modules.demo": spec}),
        )
    pages = _item(payload, "module-demo")["pages"]
    return [Path(page["path"]).name for page in pages] == ["index.md"] and any(
        "escape.md" in warning and "指向文档目录之外" in warning for warning in payload["warnings"]
    )


def _test_directory_scan_fallback():
    with TemporaryDirectory(prefix="akari-docs-") as raw:
        root = Path(raw)
        core_pkg = root / "core_pkg"
        modules_ns = root / "modules_ns"
        adapters_ns = root / "adapters_ns"
        for directory in (core_pkg / "doc", modules_ns / "coin" / "doc", modules_ns / "core" / "doc"):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "index.md").write_text("# 文档\n", encoding="utf-8")
        (adapters_ns / "qqbot" / "doc").mkdir(parents=True, exist_ok=True)
        (adapters_ns / "qqbot" / "doc" / "index.md").write_text("# QQ\n", encoding="utf-8")
        specs = {
            "akaribot.core": _Spec([str(core_pkg)]),
            "akaribot.modules": _Spec([str(modules_ns)]),
            "akaribot.adapters": _Spec([str(adapters_ns)]),
            "akaribot.modules.core": _Spec([str(modules_ns / "core")]),
            "akaribot.modules.coin": _Spec([str(modules_ns / "coin")]),
            "akaribot.adapters.qqbot": _Spec([str(adapters_ns / "qqbot")]),
        }
        payload = docs.collect(entry_points=lambda: [], find_spec=_locator(specs))

    keys = [item["key"] for item in payload["packages"]]
    coin = _item(payload, "module-coin")
    return (
        keys == ["core", "builtin", "module-coin", "adapter-qqbot"]
        and coin["dist"] == "akari-bot-module-coin"
        and coin["name"] == "coin"
        and coin["group"] == "module"
        and coin["version"] == "0+local"
        and coin["summary"] == ""
        and coin["editable"] is True
        and coin["doc_path"] == str((modules_ns / "coin" / "doc").resolve())
        and _item(payload, "adapter-qqbot")["group"] == "adapter"
        and _item(payload, "core")["group"] == "core"
    )


def _test_main_output_contract():
    payload = {
        "schema": 1,
        "packages": [
            {
                "key": "core",
                "group": "core",
                "title": "核心",
                "doc_path": "/tmp/core/doc",
                "pages": [{"title": "首页", "path": "/tmp/core/doc/index.md", "order": 500, "summary": ""}],
            }
        ],
        "warnings": ["提示"],
    }
    json_out = io.StringIO()
    json_err = io.StringIO()
    with patch.object(docs, "collect", return_value=payload), redirect_stdout(json_out), redirect_stderr(json_err):
        json_code = docs.main(["--json"])
        json_text = json_out.getvalue()
        json_stderr = json_err.getvalue()

    human_out = io.StringIO()
    human_err = io.StringIO()
    with patch.object(docs, "collect", return_value=payload), redirect_stdout(human_out), redirect_stderr(human_err):
        list_code = docs.main(["list"])
        human_text = human_out.getvalue()
        human_stderr = human_err.getvalue()

    try:
        with redirect_stderr(io.StringIO()):
            docs.main(["unknown"])
    except SystemExit as exc:
        bad_code = exc.code
    else:
        bad_code = None
    return (
        json_code == 0
        and json.loads(json_text) == payload
        and json_stderr == ""
        and list_code == 0
        and human_text.startswith("core\tcore\t核心\t1\t/tmp/core/doc")
        and "! 提示" in human_stderr
        and bad_code == 2
    )


@func_case
async def test_docs_entrypoint(tester: Tester):
    """core.entrypoints.docs: 包文档清单入口测试"""
    await tester.test(_test_metadata_and_sorting, "元数据字段与分组排序")
    await tester.test(_test_front_matter_overrides_titles, "front matter 覆盖标题与页面排序")
    await tester.test(_test_doc_meta_defaults_and_corruption, "doc.toml 缺省、覆盖与损坏告警")
    await tester.test(_test_hidden_package_is_skipped, "hidden 包被跳过")
    await tester.test(_test_missing_documentation_is_reported, "无文档与无法定位的包产生告警")
    await tester.test(_test_symlink_escape_is_skipped, "符号链接逃逸被拒绝")
    await tester.test(_test_directory_scan_fallback, "entry point 为空时回退目录扫描")
    await tester.test(_test_main_output_contract, "命令行 JSON、人类可读输出与参数错误")
    return tester
