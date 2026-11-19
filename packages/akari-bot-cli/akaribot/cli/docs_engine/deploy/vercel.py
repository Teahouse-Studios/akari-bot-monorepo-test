"""Vercel 部署 provider。

命令固定在实例的 ``.docs/vercel`` 目录执行，使 ``vercel link`` 记住的项目配置落在实例内；
令牌与项目标识只经环境变量传入，不出现在命令行、日志或异常消息里。
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .base import DeployResult, DeployTarget, DocsDeployError, Reporter

TOKEN_ENV = "VERCEL_TOKEN"
PROJECT_ENV = "VERCEL_PROJECT_ID"
ORG_ENV = "VERCEL_ORG_ID"
STATE_SUBDIR = ".docs"
STATE_DIR_NAME = "vercel"
TAIL_LIMIT = 2000
FAILED_KEY = "cli.docs.deploy.vercel.failed"
URL_PATTERN = re.compile(r"https://[A-Za-z0-9][A-Za-z0-9._-]*\.vercel\.app(?:/[^\s]*)?")

Runner = Callable[[Sequence[str], Path, Mapping[str, str]], subprocess.CompletedProcess[str]]


class VercelProvider:
    """Vercel 部署 provider。

    :param config: ``docs.toml`` 的 ``[deploy.vercel]`` 子表。
    :param instance_root: 实例根目录，命令状态目录位于其 ``.docs/vercel``。
    :param runner: 子进程执行器，测试可注入。
    :param which: 可执行文件查找函数，测试可注入。
    :param windows: 是否按 Windows 规则包装命令；缺省按当前平台判断。
    """

    name = "vercel"

    def __init__(
        self,
        config: Mapping[str, Any],
        *,
        instance_root: Path,
        runner: Runner | None = None,
        which: Callable[[str], str | None] | None = None,
        windows: bool | None = None,
    ) -> None:
        self._project_id = _text(config, "project_id")
        self._org_id = _text(config, "org_id")
        self._project = _text(config, "project")
        self._scope = _text(config, "scope")
        self._root = Path(instance_root)
        self._runner = runner or _default_runner
        self._which = which or shutil.which
        self._windows = os.name == "nt" if windows is None else windows

    def plan(self, site_dir: Path) -> DeployTarget:
        """返回目标摘要，不启动子进程。"""
        site = _require_site(site_dir)
        project = self._project_value()
        if not project:
            raise DocsDeployError("cli.docs.deploy.vercel.missing_project")
        return DeployTarget("vercel", "Vercel", f"{project} ({site})")

    def deploy(
        self,
        site_dir: Path,
        *,
        dry_run: bool = False,
        delete: bool = False,
        reporter: Reporter | None = None,
    ) -> DeployResult:
        """执行 ``vercel deploy --prod``。

        Vercel 的历史部署不提供删除入口，``delete`` 对本 provider 无效。
        """
        site = _require_site(site_dir)
        project = self._project_value()
        if not project:
            raise DocsDeployError("cli.docs.deploy.vercel.missing_project")
        token = str(os.environ.get(TOKEN_ENV) or "").strip()
        if not token:
            raise DocsDeployError("cli.docs.deploy.vercel.missing_token")
        target = DeployTarget("vercel", "Vercel", f"{project} ({site})")
        if dry_run:
            return DeployResult(ok=True, provider="vercel", detail=target.detail, dry_run=True)

        state_dir = self._root / STATE_SUBDIR / STATE_DIR_NAME
        state_dir.mkdir(parents=True, exist_ok=True)
        environment = self._environment(token)
        notify = reporter or _ignore

        if self._project and not self._project_id:
            notify("link")
            link_argv = _wrap_windows(
                [*self._cli_prefix(), "link", "--yes", "--project", self._project, *self._scope_args()],
                self._windows,
            )
            linked = self._run(link_argv, state_dir, environment, token)
            if linked.returncode != 0:
                raise _failure(linked, token)

        notify("deploy")
        deploy_argv = _wrap_windows(
            [*self._cli_prefix(), "deploy", str(site), "--prod", "--yes", *self._scope_args()],
            self._windows,
        )
        finished = self._run(deploy_argv, state_dir, environment, token)
        if finished.returncode != 0:
            raise _failure(finished, token)
        url = _find_url(finished.stdout or "") or _find_url(finished.stderr or "")
        if not url:
            raise DocsDeployError(FAILED_KEY, detail=_tail((finished.stdout or finished.stderr or ""), token))
        notify("done")
        return DeployResult(ok=True, provider="vercel", url=url, detail=target.detail)

    def _project_value(self) -> str:
        return self._project_id or self._project

    def _scope_args(self) -> list[str]:
        if self._scope and not self._org_id:
            return ["--scope", self._scope]
        return []

    def _cli_prefix(self) -> list[str]:
        vercel = self._which("vercel")
        if vercel:
            return [vercel]
        npx = self._which("npx") or "npx"
        return [npx, "--yes", "vercel@latest"]

    def _environment(self, token: str) -> dict[str, str]:
        environment = dict(os.environ)
        environment[TOKEN_ENV] = token
        if self._project_id:
            environment[PROJECT_ENV] = self._project_id
        if self._org_id:
            environment[ORG_ENV] = self._org_id
        return environment

    def _run(
        self,
        argv: Sequence[str],
        cwd: Path,
        environment: Mapping[str, str],
        token: str,
    ) -> subprocess.CompletedProcess[str]:
        try:
            return self._runner(argv, cwd, environment)
        except OSError as exc:
            raise DocsDeployError(FAILED_KEY, detail=_redact(str(exc), token)) from exc


def _default_runner(
    argv: Sequence[str],
    cwd: Path,
    environment: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603 - 命令由本模块组装，凭据只经环境变量传递
        list(argv),
        cwd=str(cwd),
        env=dict(environment),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _wrap_windows(argv: Sequence[str], windows: bool) -> list[str]:
    if not windows:
        return list(argv)
    executable = str(argv[0])
    name = Path(executable).name.lower()
    if name in {"npx", "npx.cmd", "npx.bat"} or name.endswith((".cmd", ".bat")):
        return [os.environ.get("COMSPEC", "cmd"), "/d", "/s", "/c", *argv]
    return list(argv)


def _failure(process: subprocess.CompletedProcess[str], token: str) -> DocsDeployError:
    output = _tail(process.stderr or process.stdout or "", token)
    return DocsDeployError(FAILED_KEY, detail=f"exit {process.returncode}: {output}")


def _tail(text: str, token: str) -> str:
    content = _redact(str(text or "").strip(), token)
    return content[-TAIL_LIMIT:] if content else "command failed"


def _redact(text: str, token: str) -> str:
    return text.replace(token, "***") if token else text


def _find_url(text: str) -> str:
    matches = URL_PATTERN.findall(text or "")
    return matches[-1].rstrip(".,);]") if matches else ""


def _require_site(site_dir: Path) -> Path:
    site = Path(site_dir).expanduser().resolve()
    if not site.is_dir():
        raise DocsDeployError("cli.docs.deploy.site_missing", path=str(site_dir))
    return site


def _text(data: Mapping[str, Any], name: str) -> str:
    value = data.get(name)
    return "" if value is None else str(value).strip()


def _ignore(_: str) -> None:
    return None
