"""文档站点命令：列目录、构建、预览、部署与清理。

业务实现都在 :mod:`akaribot.cli.docs`；本模块只负责参数解析、确认、输出与退出码。
``--json`` 模式下 stdout 只承载结果 JSON，提示与警告一律走 stderr。
"""

from __future__ import annotations

import contextlib
import json
import shutil
import sys
import webbrowser
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, NoReturn

import typer
from rich.markup import escape
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli.docs.builder import build
from akaribot.cli.docs.catalog import load_catalog
from akaribot.cli.docs.config import CONFIG_FILENAME, DocsConfig, load_config
from akaribot.cli.docs.deploy import DocsDeployError, get_provider
from akaribot.cli.docs.model import BuildResult, DocPackage, DocsError, ToolchainInfo
from akaribot.cli.docs.server import StaticServer
from akaribot.cli.docs.state import load_state, record_deploy
from akaribot.cli.docs.toolchain import detect
from akaribot.cli.instance import (
    InstancePathOption,
    console,
    err_console,
    fail,
    ok,
    require_instance,
    split_names,
    warn,
)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4173
PROVIDER_NAMES = ("vercel", "s3")
DEFAULT_PROVIDER = "vercel"

JsonOption = Annotated[bool, typer.Option("--json", help=i18n.t("cli.docs.option_json"))]
YesOption = Annotated[bool, typer.Option("--yes", "-y", help=i18n.t("cli.common.yes_option"))]

app = typer.Typer(help=i18n.t("cli.docs.help"))


def _render_error(error: DocsError) -> str:
    # ``i18n.t`` 的形参名为 ``key``；引擎的 unknown_key 以 ``key=`` 传参，直接展开会与形参重名。
    params = dict(error.params)
    if "key" in params:
        params["name"] = params.pop("key")
    return i18n.t(error.key, **params)


def _fail(error: DocsError) -> NoReturn:
    fail(escape(_render_error(error)))


def _config_path(instance_root: Path) -> Path | None:
    path = Path(instance_root) / CONFIG_FILENAME
    return path if path.is_file() else None


def _config_payload(config: DocsConfig) -> dict[str, Any]:
    return {
        "path": str(path) if (path := _config_path(config.root)) else None,
        "site": {"title": config.site.title, "lang": config.site.lang, "base": config.base},
        "out_dir": str(config.out_dir),
    }


def _toolchain_payload(info: ToolchainInfo) -> dict[str, Any]:
    return {
        "node": info.node,
        "npm": info.npm,
        "node_version": info.node_version,
        "npm_version": info.npm_version,
        "ready": info.ready,
        "detail": info.detail,
    }


def _package_payload(package: DocPackage) -> dict[str, Any]:
    return {
        "key": package.key,
        "group": package.group,
        "dist": package.dist,
        "name": package.name,
        "version": package.version,
        "title": package.title,
        "summary": package.summary,
        "order": package.order,
        "doc_path": str(package.doc_path),
        "editable": package.editable,
        "pages": [
            {
                "path": page.path,
                "title": page.title,
                "order": page.order,
                "description": page.description,
            }
            for page in package.pages
        ],
    }


def _build_payload(result: BuildResult) -> dict[str, Any]:
    return {
        "out_dir": str(result.out_dir),
        "packages": list(result.packages),
        "fingerprint": result.fingerprint,
        "reused": result.reused,
        "duration_ms": result.duration_ms,
        "log": result.log,
    }


def _build_detail(build_state: Mapping[str, Any] | None) -> str:
    if not build_state:
        return i18n.t("cli.docs.status.none")
    packages = build_state.get("packages")
    return i18n.t(
        "cli.docs.status.build_detail",
        at=build_state.get("generated_at") or i18n.t("cli.docs.status.none"),
        count=len(packages) if isinstance(packages, list) else 0,
        fingerprint=str(build_state.get("fingerprint") or "-")[:12],
    )


def _deploy_detail(deploy: Mapping[str, Any] | None) -> str:
    if not deploy:
        return i18n.t("cli.docs.status.none")
    return i18n.t(
        "cli.docs.status.deploy_detail",
        at=deploy.get("at") or i18n.t("cli.docs.status.none"),
        target=deploy.get("target") or "-",
        status=deploy.get("status") or "-",
    )


def _state_parts(instance: Any) -> tuple[Mapping[str, Any] | None, list[Any]]:
    state = load_state(instance)
    build_state = state.get("build")
    deploys = state.get("deploys")
    return (
        build_state if isinstance(build_state, Mapping) else None,
        deploys if isinstance(deploys, list) else [],
    )


def _emit_json(payload: Mapping[str, Any], *, flush: bool = False) -> None:
    typer.echo(json.dumps(payload, ensure_ascii=False))
    if flush:
        sys.stdout.flush()


def _confirm(text: str, *, as_json: bool) -> None:
    # click 会把读入的答案回显到 stdout；JSON 模式下整段改道 stderr，保证结果行不被污染。
    if as_json:
        with contextlib.redirect_stdout(sys.stderr):
            typer.confirm(text, abort=True)
        return
    typer.confirm(text, abort=True)


def _filter_packages(packages: tuple[DocPackage, ...], query: str | None, kind: str | None) -> list[DocPackage]:
    needle = (query or "").strip().casefold()
    selected = [
        package
        for package in packages
        if (kind is None or package.group == kind)
        and (not needle or needle in f"{package.key}\n{package.title}\n{package.summary}".casefold())
    ]
    return selected


def _print_package_table(packages: list[DocPackage]) -> None:
    if not packages:
        console.print(i18n.t("cli.docs.list.empty"))
        return
    table = Table(title=i18n.t("cli.docs.list.header", count=len(packages)))
    table.add_column(i18n.t("cli.docs.list.column_key"))
    table.add_column(i18n.t("cli.docs.list.column_group"))
    table.add_column(i18n.t("cli.docs.list.column_title"))
    table.add_column(i18n.t("cli.docs.list.column_version"))
    table.add_column(i18n.t("cli.docs.list.column_pages"))
    for package in packages:
        table.add_row(
            escape(package.key),
            escape(package.group),
            escape(package.title),
            escape(package.version or "-"),
            str(len(package.pages)),
        )
    console.print(table)
    console.print(
        i18n.t(
            "cli.docs.list.summary",
            count=len(packages),
            pages=sum(len(package.pages) for package in packages),
        )
    )


@app.command("list", help=i18n.t("cli.docs.list.help"))
def list_docs(
    query: Annotated[str | None, typer.Option("--query", help=i18n.t("cli.docs.option_query"))] = None,
    kind: Annotated[str | None, typer.Option("--kind", help=i18n.t("cli.docs.option_kind"))] = None,
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """列出参与构建的包与页面；``--json`` 同时给出配置、工具链与最近状态。"""
    target = require_instance(instance)
    try:
        config = load_config(target)
        catalog = load_catalog(target)
        toolchain = detect()
    except DocsError as error:
        _fail(error)
    selected = _filter_packages(catalog.packages, query, kind)
    build_state, deploys = _state_parts(target)
    warnings = list(catalog.warnings)
    if as_json:
        _emit_json(
            {
                "instance": str(target.root),
                "config": _config_payload(config),
                "toolchain": _toolchain_payload(toolchain),
                "packages": [_package_payload(package) for package in selected],
                "warnings": warnings,
                "build": dict(build_state) if build_state else None,
                "deploys": deploys,
                "instance_warnings": warnings,
            }
        )
        return
    _print_package_table(selected)
    for message in warnings:
        warn(escape(message))


@app.command("build", help=i18n.t("cli.docs.build.help"))
def build_docs(
    package: Annotated[list[str] | None, typer.Option("--package", help=i18n.t("cli.docs.option_package"))] = None,
    all_packages: Annotated[bool, typer.Option("--all", help=i18n.t("cli.docs.option_all"))] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.docs.option_force"))] = False,
    offline: Annotated[bool, typer.Option("--offline", help=i18n.t("cli.docs.option_offline"))] = False,
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """生成站点源文件并调用 VitePress 构建。

    默认构建全部包；``--package`` 可重复或逗号分隔，指定后只构建列出的包。``--json`` 的 stdout
    只输出一行结果，构建日志放在 ``log`` 字段。
    """
    target = require_instance(instance)
    keys = None if all_packages else (split_names(package) or None)
    try:
        result = build(target, keys=keys, force=force, offline=offline)
    except DocsError as error:
        _fail(error)
    if as_json:
        _emit_json({"ok": True, **_build_payload(result)})
        return
    if result.reused:
        ok(i18n.t("cli.docs.build.reused", count=len(result.packages)))
    else:
        ok(i18n.t("cli.docs.build.done", count=len(result.packages)))
    console.print(escape(i18n.t("cli.docs.build.summary", out_dir=result.out_dir, duration=result.duration_ms)))


@app.command("serve", help=i18n.t("cli.docs.serve.help"))
def serve_docs(
    host: Annotated[str, typer.Option("--host", help=i18n.t("cli.docs.option_host"))] = DEFAULT_HOST,
    port: Annotated[int, typer.Option("--port", help=i18n.t("cli.docs.option_port"))] = DEFAULT_PORT,
    open_browser: Annotated[bool, typer.Option("--open", help=i18n.t("cli.docs.option_open"))] = False,
    no_build: Annotated[bool, typer.Option("--no-build", help=i18n.t("cli.docs.option_no_build"))] = False,
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """构建并启动静态预览服务，直到 Ctrl+C。"""
    target = require_instance(instance)
    try:
        config = load_config(target)
    except DocsError as error:
        _fail(error)
    if not no_build:
        try:
            build(target)
        except DocsError as error:
            _fail(error)
    site_dir = config.out_dir
    if not (site_dir / "index.html").is_file():
        fail(escape(i18n.t("cli.docs.error.not_built", path=site_dir)))
    server = StaticServer(site_dir, host=host, port=port)
    try:
        url = server.start()
    except OSError as error:
        fail(escape(i18n.t("cli.docs.error.serve_failed", detail=error)))
    if open_browser:
        webbrowser.open(url)
    if as_json:
        _emit_json({"event": "ready", "url": url, "mode": "static"}, flush=True)
    else:
        console.print(escape(i18n.t("cli.docs.serve.ready", url=url)))
        console.print(i18n.t("cli.docs.serve.summary"))
    try:
        server.wait()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
    if as_json:
        _emit_json({"event": "stopped"})
    else:
        console.print(i18n.t("cli.docs.serve.stopped"))


def _provider_name(config: DocsConfig) -> str:
    declared = config.deploy.get("provider")
    if isinstance(declared, str) and declared.strip():
        return declared.strip().lower()
    for name in PROVIDER_NAMES:
        if name in config.deploy:
            return name
    return DEFAULT_PROVIDER


def _provider_config(config: DocsConfig, name: str) -> Mapping[str, Any]:
    value = config.deploy.get(name, {})
    return value if isinstance(value, Mapping) else {}


@app.command("deploy", help=i18n.t("cli.docs.deploy.help"))
def deploy_docs(
    provider: Annotated[str | None, typer.Option("--provider", help=i18n.t("cli.docs.option_provider"))] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.docs.option_dry_run"))] = False,
    delete: Annotated[bool, typer.Option("--delete", help=i18n.t("cli.docs.option_delete"))] = False,
    yes: YesOption = False,
    no_build: Annotated[bool, typer.Option("--no-build", help=i18n.t("cli.docs.option_no_build"))] = False,
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """把构建产物部署到 Vercel 或 S3。"""
    target = require_instance(instance)
    try:
        config = load_config(target)
    except DocsError as error:
        _fail(error)
    name = (provider or "").strip().lower() or _provider_name(config)
    if not no_build:
        try:
            build(target)
        except DocsError as error:
            _fail(error)
    site_dir = config.out_dir
    if not (site_dir / "index.html").is_file():
        fail(escape(i18n.t("cli.docs.error.not_built", path=site_dir)))
    try:
        deploy_provider = get_provider(name, _provider_config(config, name), instance_root=target.root)
        plan = deploy_provider.plan(site_dir)
    except DocsDeployError as error:
        _fail(error)
    except DocsError as error:
        _fail(error)
    target_line = escape(i18n.t("cli.docs.deploy.target", label=plan.label, detail=plan.detail))
    if as_json:
        err_console.print(target_line)
    else:
        console.print(target_line)
    if not yes:
        confirm_key = "cli.docs.deploy.confirm_delete" if delete else "cli.docs.deploy.confirm"
        _confirm(
            i18n.t(confirm_key, label=plan.label, detail=plan.detail),
            as_json=as_json,
        )
    try:
        result = deploy_provider.deploy(site_dir, dry_run=dry_run, delete=delete)
    except DocsDeployError as error:
        _fail(error)
    except DocsError as error:
        _fail(error)
    if result.ok and not dry_run and not result.dry_run:
        record_deploy(target, plan.detail or plan.label, status="ok", detail=result.url or result.detail)
    payload = {
        "ok": result.ok,
        "provider": result.provider,
        "url": result.url,
        "detail": result.detail,
        "uploaded": result.uploaded,
        "deleted": result.deleted,
        "skipped": result.skipped,
        "dry_run": dry_run or result.dry_run,
    }
    if as_json:
        _emit_json(payload)
        return
    if dry_run or result.dry_run:
        console.print(
            i18n.t(
                "cli.docs.deploy.dry_run",
                uploaded=result.uploaded,
                deleted=result.deleted,
                skipped=result.skipped,
            )
        )
        return
    ok(escape(i18n.t("cli.docs.deploy.done", provider=result.provider, url=result.url or result.detail or "-")))
    console.print(
        i18n.t(
            "cli.docs.deploy.summary",
            uploaded=result.uploaded,
            deleted=result.deleted,
            skipped=result.skipped,
        )
    )


@app.command("status", help=i18n.t("cli.docs.status.help"))
def status_docs(
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """显示工具链、配置、文档包与最近的构建和部署。"""
    target = require_instance(instance)
    try:
        config = load_config(target)
        catalog = load_catalog(target)
        toolchain = detect()
    except DocsError as error:
        _fail(error)
    build_state, deploys = _state_parts(target)
    keys = list(catalog.keys())
    if as_json:
        _emit_json(
            {
                "instance": str(target.root),
                "config": _config_payload(config),
                "toolchain": _toolchain_payload(toolchain),
                "packages": {"count": len(keys), "keys": keys},
                "build": dict(build_state) if build_state else None,
                "deploys": deploys,
            }
        )
        return
    console.print(i18n.t("cli.docs.status.title"))
    console.print(escape(i18n.t("cli.docs.status.instance", path=target.root)))
    console.print(escape(i18n.t("cli.docs.status.toolchain", detail=toolchain.detail or "-")))
    config_path = _config_path(target.root)
    console.print(escape(i18n.t("cli.docs.status.config", path=config_path or i18n.t("cli.docs.status.none"))))
    console.print(escape(i18n.t("cli.docs.status.site", title=config.site.title, lang=config.site.lang)))
    console.print(escape(i18n.t("cli.docs.status.base", base=config.base)))
    console.print(escape(i18n.t("cli.docs.status.out_dir", path=config.out_dir)))
    console.print(i18n.t("cli.docs.status.packages", count=len(keys)))
    console.print(escape(i18n.t("cli.docs.status.build", detail=_build_detail(build_state))))
    latest = deploys[-1] if deploys and isinstance(deploys[-1], Mapping) else None
    console.print(escape(i18n.t("cli.docs.status.deploy", detail=_deploy_detail(latest))))


@app.command("clean", help=i18n.t("cli.docs.clean.help"))
def clean_docs(
    yes: YesOption = False,
    as_json: JsonOption = False,
    instance: InstancePathOption = None,
) -> None:
    """删除实例的文档缓存目录 ``cache/docs``。"""
    target = require_instance(instance)
    path = target.root / "cache" / "docs"
    if not path.exists():
        if as_json:
            _emit_json({"ok": True, "removed": False, "path": str(path)})
        else:
            ok(escape(i18n.t("cli.docs.clean.done", path=path)))
        return
    if not yes:
        _confirm(i18n.t("cli.docs.clean.confirm", path=path), as_json=as_json)
    shutil.rmtree(path)
    if as_json:
        _emit_json({"ok": True, "removed": True, "path": str(path)})
        return
    ok(escape(i18n.t("cli.docs.clean.done", path=path)))
