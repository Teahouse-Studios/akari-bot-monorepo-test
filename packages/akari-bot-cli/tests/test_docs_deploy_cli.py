"""``akaribot docs deploy``：provider 解析、确认流程、结果契约与部署记录。

provider 与构建全部替身化；用例不读取真实凭据，也不连接 Vercel 或 S3。
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
from akaribot.cli.docs.deploy import DeployResult, DeployTarget, DocsDeployError
from akaribot.cli.docs.model import BuildResult
from akaribot.cli.docs.state import load_state
from akaribot.testing import Tester, func_case


class _FakeInstance:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _config(root: Path, deploy: dict | None = None) -> DocsConfig:
    return DocsConfig(
        root=root,
        site=DocsSiteConfig(title="Akari 文档", lang="zh-CN", base="/"),
        build=DocsBuildConfig(out_dir="cache/docs/site"),
        deploy=deploy or {},
    )


def _build_result(root: Path) -> BuildResult:
    return BuildResult(
        out_dir=root / "cache" / "docs" / "site",
        packages=("demo",),
        fingerprint="f" * 64,
        reused=False,
        duration_ms=10,
        log="",
    )


def _flat(text: str) -> str:
    return "".join(text.split())


class _Provider:
    def __init__(self, *, result: DeployResult | None = None, error: DocsDeployError | None = None) -> None:
        self.name = "s3"
        self.result = result or DeployResult(
            ok=True,
            provider="s3",
            url="https://docs.example.test/",
            detail="s3://bucket/site/",
            uploaded=3,
            deleted=1,
            skipped=2,
            dry_run=False,
        )
        self.error = error
        self.plans: list[Path] = []
        self.deploys: list[dict] = []

    def plan(self, site_dir: Path) -> DeployTarget:
        self.plans.append(Path(site_dir))
        return DeployTarget("s3", "S3", "s3://bucket/site/")

    def deploy(self, site_dir: Path, *, dry_run: bool = False, delete: bool = False, reporter=None):
        self.deploys.append({"site_dir": Path(site_dir), "dry_run": dry_run, "delete": delete})
        if self.error is not None:
            raise self.error
        return self.result


@contextmanager
def _deploy_env(instance: _FakeInstance, config: DocsConfig, provider, *, built: list[bool]):
    def fake_build(target):
        built.append(True)
        return _build_result(instance.root)

    with (
        patch.object(docs_command, "require_instance", return_value=instance),
        patch.object(docs_command, "load_config", return_value=config),
        patch.object(docs_command, "build", side_effect=fake_build),
        patch.object(docs_command, "get_provider", return_value=provider) as get_provider,
    ):
        yield get_provider


def _invoke(argv: list[str], input_text: str | None = None):
    return CliRunner().invoke(docs_command.app, argv, input=input_text)


def _site(config: DocsConfig) -> None:
    config.out_dir.mkdir(parents=True)
    (config.out_dir / "index.html").write_text("site", encoding="utf-8")


async def _test_deploy_confirms_and_records():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {"s3": {"bucket": "bucket"}})
        _site(config)
        provider = _Provider()
        built: list[bool] = []
        with _deploy_env(instance, config, provider, built=built) as get_provider:
            result = _invoke(["deploy", "--json"], input_text="y\n")
        payload = json.loads(result.stdout)
        state = load_state(instance)
    args, kwargs = get_provider.call_args
    return (
        result.exit_code == 0
        and built == [True]
        and args[0] == "s3"
        and args[1] == {"bucket": "bucket"}
        and kwargs["instance_root"] == root
        and provider.plans == [config.out_dir]
        and provider.deploys == [{"site_dir": config.out_dir, "dry_run": False, "delete": False}]
        and payload
        == {
            "ok": True,
            "provider": "s3",
            "url": "https://docs.example.test/",
            "detail": "s3://bucket/site/",
            "uploaded": 3,
            "deleted": 1,
            "skipped": 2,
            "dry_run": False,
        }
        and len(result.stdout.strip().splitlines()) == 1
        and state["deploys"][-1]["target"] == "s3://bucket/site/"
        and state["deploys"][-1]["status"] == "ok"
    )


async def _test_deploy_yes_dry_run_delete_skips_record():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {"provider": "vercel"})
        _site(config)
        provider = _Provider(
            result=DeployResult(
                ok=True,
                provider="vercel",
                url="",
                detail="project (site)",
                uploaded=4,
                deleted=2,
                skipped=0,
                dry_run=True,
            )
        )
        built: list[bool] = []
        with _deploy_env(instance, config, provider, built=built) as get_provider:
            result = _invoke(["deploy", "--json", "--yes", "--dry-run", "--delete", "--no-build"])
        payload = json.loads(result.stdout)
        state = load_state(instance)
    args, _ = get_provider.call_args
    return (
        result.exit_code == 0
        and built == []
        and args[0] == "vercel"
        and provider.deploys == [{"site_dir": config.out_dir, "dry_run": True, "delete": True}]
        and payload["dry_run"] is True
        and payload["uploaded"] == 4
        and payload["deleted"] == 2
        and state["deploys"] == []
    )


async def _test_deploy_delete_confirmation_mentions_removal():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {"s3": {}})
        _site(config)
        provider = _Provider()
        built: list[bool] = []
        with _deploy_env(instance, config, provider, built=built):
            result = _invoke(["deploy", "--json", "--delete"], input_text="n\n")
        expected = i18n.t("cli.docs.deploy.confirm_delete", label="S3", detail="s3://bucket/site/")
    return (
        result.exit_code != 0
        and result.stdout == ""
        and provider.deploys == []
        and _flat(expected) in _flat(result.stderr)
        and "删除" in result.stderr
    )


async def _test_deploy_human_reports_target_and_counts():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {"s3": {}})
        _site(config)
        provider = _Provider()
        built: list[bool] = []
        with _deploy_env(instance, config, provider, built=built):
            result = _invoke(["deploy", "--yes"])
        flat = _flat(result.stdout)
    return (
        result.exit_code == 0
        and _flat(i18n.t("cli.docs.deploy.target", label="S3", detail="s3://bucket/site/")) in flat
        and "https://docs.example.test/" in result.stdout
        and _flat(i18n.t("cli.docs.deploy.summary", uploaded=3, deleted=1, skipped=2)) in flat
    )


async def _test_deploy_provider_errors_are_rendered():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {})
        _site(config)
        built: list[bool] = []
        with (
            _deploy_env(instance, config, _Provider(), built=built),
            patch.object(
                docs_command,
                "get_provider",
                side_effect=DocsDeployError("cli.docs.deploy.s3.missing_bucket"),
            ),
        ):
            missing = _invoke(["deploy", "--json", "--yes", "--provider", "s3"])
        with _deploy_env(
            instance,
            config,
            _Provider(error=DocsDeployError("cli.docs.deploy.s3.upload_failed", detail="boom")),
            built=built,
        ):
            failed = _invoke(["deploy", "--json", "--yes", "--provider", "s3"])
    expected_missing = i18n.t("cli.docs.deploy.s3.missing_bucket")
    expected_failed = i18n.t("cli.docs.deploy.s3.upload_failed", detail="boom")
    return (
        missing.exit_code == 1
        and missing.stdout == ""
        and _flat(expected_missing) in _flat(missing.stderr)
        and failed.exit_code == 1
        and failed.stdout == ""
        and _flat(expected_failed) in _flat(failed.stderr)
    )


async def _test_deploy_no_build_requires_site():
    with TemporaryDirectory(prefix="akari-docs-deploy-") as raw:
        root = Path(raw)
        instance = _FakeInstance(root)
        config = _config(root, {})
        provider = _Provider()
        built: list[bool] = []
        with _deploy_env(instance, config, provider, built=built):
            result = _invoke(["deploy", "--json", "--yes", "--no-build"])
        expected = i18n.t("cli.docs.error.not_built", path=config.out_dir)
    return (
        result.exit_code == 1
        and result.stdout == ""
        and built == []
        and provider.plans == []
        and _flat(expected) in _flat(result.stderr)
    )


@func_case
async def test_docs_deploy_cli(tester: Tester):
    """cli.docs.deploy: provider 解析、确认、结果契约与部署记录"""
    _use_cli_locale()
    await tester.test(_test_deploy_confirms_and_records, "确认后部署并记录目标")
    await tester.test(_test_deploy_yes_dry_run_delete_skips_record, "--yes 跳过确认，试运行不写记录")
    await tester.test(_test_deploy_delete_confirmation_mentions_removal, "--delete 的确认文案说明删除远端文件")
    await tester.test(_test_deploy_human_reports_target_and_counts, "人类输出展示目标与文件统计")
    await tester.test(_test_deploy_provider_errors_are_rendered, "provider 错误键渲染为文案")
    await tester.test(_test_deploy_no_build_requires_site, "--no-build 且站点缺失时报错")
    return tester
