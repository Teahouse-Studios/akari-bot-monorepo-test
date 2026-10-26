"""``akaribot docs``：目录、构建、预览、状态与清理的命令层行为。

引擎与子进程调用全部替身化：用例只验证参数转交、JSON 契约、确认流程与错误渲染，
不启动 Node、npm 或真实 HTTP 服务。
"""

import json
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import docs as docs_command
from akaribot.cli.docs.config import DocsBuildConfig, DocsConfig, DocsSiteConfig
from akaribot.cli.docs.model import BuildResult, DocCatalog, DocPackage, DocPage, DocsError, ToolchainInfo
from akaribot.cli.docs.state import record_deploy, save_build_state
from akaribot.testing import Tester, func_case


class _FakeInstance:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _package(
    key: str,
    *,
    group: str = "module",
    title: str = "",
    summary: str = "",
    pages: tuple[DocPage, ...] = (),
) -> DocPackage:
    return DocPackage(
        key=key,
        group=group,
        dist=f"akari-bot-{group}-{key}",
        name=key,
        version="1.0.0",
        title=title or key,
        summary=summary,
        doc_path=Path("/tmp/doc") / key,
        pages=pages,
        order=10,
        editable=False,
    )


def _catalog(*packages: DocPackage, warnings: tuple[str, ...] = ()) -> DocCatalog:
    return DocCatalog(packages=packages or (_package("demo"),), warnings=warnings)


def _config(root: Path, deploy: dict | None = None) -> DocsConfig:
    return DocsConfig(
        root=root,
        site=DocsSiteConfig(title="Akari 文档", lang="zh-CN", base="/docs/"),
        build=DocsBuildConfig(out_dir="cache/docs/site"),
        deploy=deploy or {},
    )


def _toolchain(ready: bool = True, detail: str = "node v20.0.0, npm 10.0.0") -> ToolchainInfo:
    return ToolchainInfo("/usr/bin/node", "/usr/bin/npm", "v20.0.0", "10.0.0", ready, detail)


def _build_result(root: Path, *, reused: bool = False, packages: tuple[str, ...] = ("demo",)) -> BuildResult:
    return BuildResult(
        out_dir=root / "cache" / "docs" / "site",
        packages=packages,
        fingerprint="f" * 64,
        reused=reused,
        duration_ms=123,
        log="built\n",
    )


def _flat(text: str) -> str:
    return "".join(text.split())


@contextmanager
def _engine(instance: _FakeInstance, *, catalog: DocCatalog | None = None, config: DocsConfig | None = None):
    with (
        patch.object(docs_command, "require_instance", return_value=instance),
        patch.object(docs_command, "load_catalog", return_value=catalog or _catalog()),
        patch.object(docs_command, "load_config", return_value=config or _config(instance.root)),
        patch.object(docs_command, "detect", return_value=_toolchain()),
    ):
        yield


def _invoke(argv: list[str], input_text: str | None = None):
    return CliRunner().invoke(docs_command.app, argv, input=input_text)


async def _test_list_json_contract():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        page = DocPage(path="index.md", title="概览", order=0, description="首页")
        catalog = _catalog(
            _package("demo", title="示例", summary="演示包", pages=(page,)),
            _package("hook", group="adapter", title="钩子"),
            warnings=("docs 入口不可用，已回退 registry",),
        )
        with _engine(instance, catalog=catalog):
            result = _invoke(["list", "--json"])
        payload = json.loads(result.stdout)
    return (
        result.exit_code == 0
        and set(payload)
        == {
            "instance",
            "config",
            "toolchain",
            "packages",
            "warnings",
            "build",
            "deploys",
            "instance_warnings",
        }
        and payload["instance"] == str(root)
        and set(payload["config"]) == {"path", "site", "out_dir"}
        and payload["config"]["path"] is None
        and payload["config"]["site"] == {"title": "Akari 文档", "lang": "zh-CN", "base": "/docs/"}
        and payload["config"]["out_dir"] == str(root / "cache" / "docs" / "site")
        and set(payload["toolchain"]) == {"node", "npm", "node_version", "npm_version", "ready", "detail"}
        and payload["toolchain"]["ready"] is True
        and payload["packages"][0]
        == {
            "key": "demo",
            "group": "module",
            "dist": "akari-bot-module-demo",
            "name": "demo",
            "version": "1.0.0",
            "title": "示例",
            "summary": "演示包",
            "order": 10,
            "doc_path": str(Path("/tmp/doc") / "demo"),
            "editable": False,
            "pages": [{"path": "index.md", "title": "概览", "order": 0, "description": "首页"}],
        }
        and payload["warnings"] == ["docs 入口不可用，已回退 registry"]
        and payload["instance_warnings"] == payload["warnings"]
        and payload["build"] is None
        and payload["deploys"] == []
        and len(result.stdout.strip().splitlines()) == 1
    )


async def _test_list_filters_and_human_output():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        catalog = _catalog(
            _package("demo", title="示例", summary="演示包"),
            _package("wiki", title="Wiki 查询", summary="查询 MediaWiki"),
            _package("hook", group="adapter", title="钩子"),
        )
        with _engine(instance, catalog=catalog):
            by_query = json.loads(_invoke(["list", "--json", "--query", "mediawiki"]).stdout)
            by_kind = json.loads(_invoke(["list", "--json", "--kind", "adapter"]).stdout)
            human = _invoke(["list"])
        flat = _flat(human.stdout)
    return (
        [item["key"] for item in by_query["packages"]] == ["wiki"]
        and [item["key"] for item in by_kind["packages"]] == ["hook"]
        and human.exit_code == 0
        and _flat(i18n.t("cli.docs.list.header", count=3)) in flat
        and _flat(i18n.t("cli.docs.list.summary", count=3, pages=0)) in flat
    )


async def _test_build_passes_options_and_outputs_json():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        calls: list[dict] = []

        def fake_build(target, keys=None, force=False, offline=False, reporter=None):
            calls.append({"target": target, "keys": keys, "force": force, "offline": offline})
            return _build_result(root, packages=("a", "b", "c"))

        with _engine(instance), patch.object(docs_command, "build", side_effect=fake_build):
            selected = _invoke(["build", "--package", "a,b", "--package", "c", "--force", "--offline", "--json"])
            everything = _invoke(["build", "--all", "--json"])
        payload = json.loads(selected.stdout)
    return (
        selected.exit_code == 0
        and calls[0]["target"].root == root
        and calls[0]["keys"] == ["a", "b", "c"]
        and calls[0]["force"] is True
        and calls[0]["offline"] is True
        and calls[1]["keys"] is None
        and payload
        == {
            "ok": True,
            "out_dir": str(root / "cache" / "docs" / "site"),
            "packages": ["a", "b", "c"],
            "fingerprint": "f" * 64,
            "reused": False,
            "duration_ms": 123,
            "log": "built\n",
        }
        and everything.exit_code == 0
        and len(selected.stdout.strip().splitlines()) == 1
    )


async def _test_build_human_reports_reuse():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        with _engine(instance), patch.object(docs_command, "build", return_value=_build_result(root, reused=True)):
            result = _invoke(["build"])
        flat = _flat(result.stdout)
    return (
        result.exit_code == 0
        and _flat(i18n.t("cli.docs.build.reused", count=1)) in flat
        and _flat(i18n.t("cli.docs.build.summary", out_dir=root / "cache" / "docs" / "site", duration=123)) in flat
    )


class _FakeServer:
    def __init__(self, directory, host="127.0.0.1", port=0) -> None:
        self.directory = Path(directory)
        self.host = host
        self.port = port
        self.started = 0
        self.stopped = 0
        self.interrupt = False

    def start(self) -> str:
        self.started += 1
        return f"http://{self.host}:{self.port}/"

    def wait(self) -> None:
        if self.interrupt:
            raise KeyboardInterrupt

    def stop(self) -> None:
        self.stopped += 1


def _serve_env(instance: _FakeInstance, config: DocsConfig, *, build_called: list[bool]):
    def fake_build(target):
        build_called.append(True)
        return _build_result(instance.root)

    return patch.object(docs_command, "build", side_effect=fake_build)


async def _test_serve_json_ready_and_stopped():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root)
        (config.out_dir).mkdir(parents=True)
        (config.out_dir / "index.html").write_text("site", encoding="utf-8")
        servers: list[_FakeServer] = []

        def fake_server(directory, host="127.0.0.1", port=0):
            server = _FakeServer(directory, host, port)
            servers.append(server)
            return server

        opened: list[str] = []
        built: list[bool] = []
        with (
            _engine(instance, config=config),
            _serve_env(instance, config, build_called=built),
            patch.object(docs_command, "StaticServer", side_effect=fake_server),
            patch.object(docs_command.webbrowser, "open", side_effect=opened.append),
        ):
            result = _invoke(["serve", "--json", "--host", "0.0.0.0", "--port", "4174", "--open"])
        lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
    return (
        result.exit_code == 0
        and built == [True]
        and servers[0].directory == config.out_dir
        and (servers[0].host, servers[0].port) == ("0.0.0.0", 4174)
        and servers[0].started == 1
        and servers[0].stopped == 1
        and opened == ["http://0.0.0.0:4174/"]
        and lines
        == [
            {"event": "ready", "url": "http://0.0.0.0:4174/", "mode": "static"},
            {"event": "stopped"},
        ]
    )


async def _test_serve_keyboard_interrupt_stops_server():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root)
        config.out_dir.mkdir(parents=True)
        (config.out_dir / "index.html").write_text("site", encoding="utf-8")
        servers: list[_FakeServer] = []

        def fake_server(directory, host="127.0.0.1", port=0):
            server = _FakeServer(directory, host, port)
            server.interrupt = True
            servers.append(server)
            return server

        built: list[bool] = []
        with (
            _engine(instance, config=config),
            _serve_env(instance, config, build_called=built),
            patch.object(docs_command, "StaticServer", side_effect=fake_server),
        ):
            result = _invoke(["serve", "--json", "--no-build"])
    lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
    return result.exit_code == 0 and built == [] and servers[0].stopped == 1 and lines[-1] == {"event": "stopped"}


async def _test_serve_requires_existing_site_without_build():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root)
        built: list[bool] = []
        with _engine(instance, config=config), _serve_env(instance, config, build_called=built):
            result = _invoke(["serve", "--json", "--no-build"])
        expected = i18n.t("cli.docs.error.not_built", path=config.out_dir)
    return result.exit_code == 1 and result.stdout == "" and built == [] and _flat(expected) in _flat(result.stderr)


async def _test_status_json_and_human():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root)
        save_build_state(
            instance,
            fingerprint="a" * 64,
            packages=["demo", "hook"],
            out_dir=config.out_dir,
            base="/docs/",
        )
        record_deploy(instance, "s3://bucket/site/", status="ok", detail="https://example.test/")
        with _engine(instance, config=config, catalog=_catalog(_package("demo"), _package("hook", group="adapter"))):
            result = _invoke(["status", "--json"])
            human = _invoke(["status"])
        payload = json.loads(result.stdout)
    return (
        result.exit_code == 0
        and payload["instance"] == str(root)
        and payload["packages"] == {"count": 2, "keys": ["demo", "hook"]}
        and payload["build"]["fingerprint"] == "a" * 64
        and payload["deploys"][-1]["target"] == "s3://bucket/site/"
        and human.exit_code == 0
        and _flat(i18n.t("cli.docs.status.title")) in _flat(human.stdout)
        and _flat(i18n.t("cli.docs.status.packages", count=2)) in _flat(human.stdout)
    )


async def _test_clean_confirms_and_reports_json():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        cache = root / "cache" / "docs"
        (cache / "src").mkdir(parents=True)
        (cache / "src" / "index.md").write_text("page", encoding="utf-8")
        with _engine(instance):
            declined = _invoke(["clean", "--json"], input_text="n\n")
        kept = cache.is_dir()
        with _engine(instance):
            confirmed = _invoke(["clean", "--json"], input_text="y\n")
        payload = json.loads(confirmed.stdout)
        with _engine(instance):
            missing = _invoke(["clean", "--json", "--yes"])
        missing_payload = json.loads(missing.stdout)
    return (
        declined.exit_code != 0
        and declined.stdout == ""
        and kept
        and confirmed.exit_code == 0
        and payload == {"ok": True, "removed": True, "path": str(cache)}
        and not cache.exists()
        and missing.exit_code == 0
        and missing_payload == {"ok": True, "removed": False, "path": str(cache)}
    )


async def _test_clean_yes_skips_prompt_without_json():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        cache = root / "cache" / "docs"
        cache.mkdir(parents=True)
        with _engine(instance):
            result = _invoke(["clean", "--yes"])
    return (
        result.exit_code == 0
        and not cache.exists()
        and _flat(i18n.t("cli.docs.clean.done", path=cache)) in _flat(result.stdout)
    )


async def _test_errors_are_rendered_from_engine_keys():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        with (
            _engine(instance),
            patch.object(
                docs_command,
                "load_config",
                side_effect=DocsError("cli.docs.error.bad_config", path=root / "docs.toml", reason="bad toml"),
            ),
        ):
            config_error = _invoke(["list", "--json"])
        with (
            _engine(instance),
            patch.object(
                docs_command,
                "build",
                side_effect=DocsError("cli.docs.error.unknown_key", key="missing", keys="missing, other"),
            ),
        ):
            unknown = _invoke(["build", "--package", "missing", "--json"])
    expected_config = i18n.t("cli.docs.error.bad_config", path=root / "docs.toml", reason="bad toml")
    expected_unknown = i18n.t("cli.docs.error.unknown_key", name="missing", keys="missing, other")
    return (
        config_error.exit_code == 1
        and config_error.stdout == ""
        and _flat(expected_config) in _flat(config_error.stderr)
        and unknown.exit_code == 1
        and unknown.stdout == ""
        and _flat(expected_unknown) in _flat(unknown.stderr)
        and "cli.docs.error.unknown_key" not in unknown.stderr
    )


async def _test_list_warns_and_empty_state():
    with TemporaryDirectory(prefix="akari-docs-cli-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        with _engine(instance, catalog=DocCatalog(packages=(), warnings=("目录降级",))):
            result = _invoke(["list"])
    return (
        result.exit_code == 0
        and _flat(i18n.t("cli.docs.list.empty")) in _flat(result.stdout)
        and _flat(i18n.t("cli.common.warning_label") + " 目录降级") in _flat(result.stderr)
    )


@func_case
async def test_docs_cli(tester: Tester):
    """cli.docs: 目录、构建、预览、状态与清理"""
    _use_cli_locale()
    await tester.test(_test_list_json_contract, "list --json 输出稳定契约")
    await tester.test(_test_list_filters_and_human_output, "list 支持 query 与 kind 过滤")
    await tester.test(_test_build_passes_options_and_outputs_json, "build 转交包选择与构建选项")
    await tester.test(_test_build_human_reports_reuse, "build 人类输出报告复用与摘要")
    await tester.test(_test_serve_json_ready_and_stopped, "serve --json 输出 ready 与 stopped")
    await tester.test(_test_serve_keyboard_interrupt_stops_server, "serve 捕获 Ctrl+C 并停止服务")
    await tester.test(_test_serve_requires_existing_site_without_build, "--no-build 且站点缺失时报错")
    await tester.test(_test_status_json_and_human, "status 输出工具链、包与最近构建部署")
    await tester.test(_test_clean_confirms_and_reports_json, "clean 确认与 JSON 输出")
    await tester.test(_test_clean_yes_skips_prompt_without_json, "clean --yes 跳过确认")
    await tester.test(_test_errors_are_rendered_from_engine_keys, "引擎错误键渲染为文案")
    await tester.test(_test_list_warns_and_empty_state, "目录警告与空目录提示")
    return tester
