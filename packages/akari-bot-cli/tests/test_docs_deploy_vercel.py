"""``cli.docs.deploy.vercel``：Vercel 部署 provider。

用例注入子进程执行器，确认命令落在实例 ``.docs/vercel``、令牌只经环境变量传递，
并覆盖项目链接、失败脱敏与 Windows 命令包装。全程不执行 vercel。
"""

import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from akaribot.cli.docs.deploy import get_provider
from akaribot.cli.docs.deploy.base import DocsDeployError
from akaribot.cli.docs.deploy.vercel import VercelProvider
from akaribot.testing import Tester, func_case

TOKEN = "vercel-secret-token"
URL = "https://akari-docs.vercel.app"


@dataclass(frozen=True)
class _Call:
    argv: list[str]
    cwd: Path
    env: dict[str, str]


class _FakeRunner:
    def __init__(self, *results: tuple[int, str, str]) -> None:
        self.results = list(results)
        self.calls: list[_Call] = []

    def __call__(self, argv, cwd, env):
        self.calls.append(_Call(list(argv), Path(cwd), dict(env)))
        returncode, stdout, stderr = self.results.pop(0) if self.results else (0, "", "")
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _site(tmp: str) -> Path:
    site = Path(tmp) / "site"
    site.mkdir()
    (site / "index.html").write_text("<html></html>", encoding="utf-8")
    return site


def _provider(tmp: str, config, runner: _FakeRunner, **kwargs) -> VercelProvider:
    return VercelProvider(config, instance_root=Path(tmp), runner=runner, which=lambda _name: None, **kwargs)


def _test_plan_and_dry_run_start_nothing():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        runner = _FakeRunner()
        provider = get_provider(
            "vercel", {"project_id": "prj_1", "org_id": "org_1"}, instance_root=Path(tmp), runner=runner
        )
        target = provider.plan(site)
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            dry = provider.deploy(site, dry_run=True)
    return (
        target.provider == "vercel"
        and target.label == "Vercel"
        and "prj_1" in target.detail
        and not target.destructive
        and dry.ok
        and dry.dry_run
        and dry.url == ""
        and dry.provider == "vercel"
        and not runner.calls
        and not (Path(tmp) / ".docs").exists()
    )


def _test_deploy_sends_token_only_through_env():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        runner = _FakeRunner((0, f"Preview: https://preview.vercel.app\nProduction: {URL}\n", ""))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            provider = _provider(tmp, {"project_id": "prj_1", "org_id": "org_1"}, runner)
            result = provider.deploy(site)
        call = runner.calls[0]
        cwd_was_dir = call.cwd.is_dir()
    joined = " ".join(call.argv)
    return (
        result.ok
        and result.url == URL
        and call.argv[:3] == ["npx", "--yes", "vercel@latest"]
        and "deploy" in call.argv
        and str(site.resolve()) in call.argv
        and "--prod" in call.argv
        and "--yes" in call.argv
        and "--token" not in call.argv
        and TOKEN not in joined
        and call.env["VERCEL_TOKEN"] == TOKEN
        and call.env["VERCEL_PROJECT_ID"] == "prj_1"
        and call.env["VERCEL_ORG_ID"] == "org_1"
        and call.cwd == Path(tmp) / ".docs" / "vercel"
        and cwd_was_dir
    )


def _test_project_is_linked_before_deploy():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        runner = _FakeRunner((0, "linked\n", ""), (0, f"Production: {URL}\n", ""))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            provider = _provider(tmp, {"project": "docs-site", "scope": "team"}, runner)
            result = provider.deploy(site)
        first, second = runner.calls
    return (
        result.ok
        and result.url == URL
        and len(runner.calls) == 2
        and first.argv[:3] == ["npx", "--yes", "vercel@latest"]
        and first.argv[3:] == ["link", "--yes", "--project", "docs-site", "--scope", "team"]
        and second.argv[3:6] == ["deploy", str(site.resolve()), "--prod"]
        and "--scope" in second.argv
        and "VERCEL_PROJECT_ID" not in first.env
        and TOKEN not in " ".join(first.argv + second.argv)
        and first.env["VERCEL_TOKEN"] == TOKEN
    )


def _test_missing_credentials_and_project_are_reported():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        runner = _FakeRunner()
        with patch.dict(os.environ, {}, clear=True):
            provider = _provider(tmp, {"project_id": "prj_1"}, runner)
            try:
                provider.deploy(site, dry_run=True)
                dry_token = ""
            except DocsDeployError as error:
                dry_token = error.key
            try:
                provider.deploy(site)
                missing_token = ""
            except DocsDeployError as error:
                missing_token = error.key
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            empty = _provider(tmp, {}, runner)
            try:
                empty.plan(site)
                missing_project = ""
            except DocsDeployError as error:
                missing_project = error.key
            try:
                empty.deploy(site)
                deploy_error = ""
            except DocsDeployError as error:
                deploy_error = error.key
            try:
                empty.deploy(Path(tmp) / "absent")
                missing_site = ""
            except DocsDeployError as error:
                missing_site = error.key
    return (
        dry_token == "cli.docs.deploy.vercel.missing_token"
        and missing_token == "cli.docs.deploy.vercel.missing_token"
        and missing_project == "cli.docs.deploy.vercel.missing_project"
        and deploy_error == "cli.docs.deploy.vercel.missing_project"
        and missing_site == "cli.docs.deploy.site_missing"
        and not runner.calls
    )


def _test_failure_tail_is_redacted():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        runner = _FakeRunner((1, "", f"error: token {TOKEN} is invalid\n"))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            provider = _provider(tmp, {"project_id": "prj_1"}, runner)
            try:
                provider.deploy(site)
                detail = ""
                key = ""
            except DocsDeployError as error:
                key = error.key
                detail = error.params.get("detail", "")
        no_url = _FakeRunner((0, "done without url\n", ""))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            provider = _provider(tmp, {"project_id": "prj_1"}, no_url)
            try:
                provider.deploy(site)
                missing_url = ""
            except DocsDeployError as error:
                missing_url = error.key
    return (
        key == "cli.docs.deploy.vercel.failed"
        and "exit 1" in detail
        and "***" in detail
        and TOKEN not in detail
        and missing_url == "cli.docs.deploy.vercel.failed"
    )


def _test_windows_wraps_batch_launchers():
    with TemporaryDirectory() as tmp:
        site = _site(tmp)
        npx_runner = _FakeRunner((0, f"Production: {URL}\n", ""))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            npx_provider = VercelProvider(
                {"project_id": "prj_1"},
                instance_root=Path(tmp),
                runner=npx_runner,
                which=lambda name: "C:/node/npx.cmd" if name == "npx" else None,
                windows=True,
            )
            npx_provider.deploy(site)
        npx_argv = npx_runner.calls[0].argv
        vercel_runner = _FakeRunner((0, f"Production: {URL}\n", ""))
        with patch.dict(os.environ, {"VERCEL_TOKEN": TOKEN}, clear=True):
            vercel_provider = VercelProvider(
                {"project_id": "prj_1"},
                instance_root=Path(tmp),
                runner=vercel_runner,
                which=lambda name: "C:/tools/vercel.exe" if name == "vercel" else None,
                windows=True,
            )
            vercel_provider.deploy(site)
        vercel_argv = vercel_runner.calls[0].argv
    return (
        npx_argv[0] == "cmd"
        and npx_argv[1:4] == ["/d", "/s", "/c"]
        and "C:/node/npx.cmd" in npx_argv
        and vercel_argv[0] == "C:/tools/vercel.exe"
        and "cmd" not in vercel_argv[:1]
    )


@func_case
async def test_docs_deploy_vercel(tester: Tester):
    """cli.docs.deploy.vercel: Vercel 部署 provider 测试"""
    await tester.test(_test_plan_and_dry_run_start_nothing, "计划与试运行不启动子进程")
    await tester.test(_test_deploy_sends_token_only_through_env, "令牌只经环境变量传递")
    await tester.test(_test_project_is_linked_before_deploy, "仅配置项目名时先 link 再 deploy")
    await tester.test(_test_missing_credentials_and_project_are_reported, "缺少令牌、项目与站点目录时报错")
    await tester.test(_test_failure_tail_is_redacted, "失败尾部输出脱敏")
    await tester.test(_test_windows_wraps_batch_launchers, "Windows 下经 cmd 启动批处理")
    return tester
