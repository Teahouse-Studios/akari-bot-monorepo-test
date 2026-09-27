"""服务化：把本 CLI 装成常驻服务，并由它守护实例。

``service install`` 写入系统服务单元并注册；``service supervise`` 是单元真正执行的常驻进程，每轮读
实例注册表，按记录里的策略恢复、重启或跳过各个实例。CLI 进程不 import core，本模块同样只经注册表
与 :class:`akaribot.cli.instance.Instance` 工作。
"""

from __future__ import annotations

import json
import signal
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.markup import escape

from akaribot.cli import i18n
from akaribot.cli.instance import console, fail, ok, warn
from akaribot.cli.instances import registry_home
from akaribot.cli.service import (
    DEFAULT_BACKOFF,
    DEFAULT_INTERVAL,
    DEFAULT_MAX_RESTARTS,
    ServiceBackend,
    ServiceError,
    ServiceStatus,
    SuperviseRound,
    Supervisor,
    detect_backend,
)

app = typer.Typer(help=i18n.t("cli.service.help"))

DryRunOption = Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.service.option_dry_run"))]
JsonOption = Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))]


def build_backend(*, kind: str | None = None, home: Path | None = None, workdir: Path | None = None) -> ServiceBackend:
    """构造系统服务管理器后端。

    :param kind: 后端名；缺省按当前平台判定。
    :param home: 家目录；缺省用当前用户的家目录。
    :param workdir: 服务工作目录；缺省用注册表目录。
    :return: 可直接执行安装、卸载与状态查询的后端。
    """
    return ServiceBackend(
        kind=kind or detect_backend(),
        home=Path(home) if home is not None else Path.home(),
        workdir=workdir if workdir is not None else registry_home(),
    )


def build_supervisor(*, max_restarts: int, backoff: float) -> Supervisor:
    """构造绑定本机注册表的守护循环。

    :param max_restarts: 单个实例允许的自动重启次数上限。
    :param backoff: 指数退避的基数秒数。
    :return: 守护循环。
    """
    return Supervisor(max_restarts=max_restarts, backoff=backoff)


def _guard(action: Callable[[], ServiceStatus]) -> ServiceStatus:
    try:
        return action()
    except ServiceError as exc:
        fail(str(exc))


def _report_round(report: SuperviseRound, *, summary: bool) -> None:
    for event in report.events:
        console.print(escape(event.message))
    if not summary:
        return
    typer.echo(
        i18n.t(
            "cli.service.supervise.summary",
            checked=report.checked,
            running=report.running,
            started=report.started,
            restarted=report.restarted,
            failed=report.failed,
            abandoned=report.abandoned,
            skipped=report.skipped,
        )
    )


def _serve(supervisor: Supervisor, interval: float) -> None:
    stop = threading.Event()
    received: list[int] = []

    def _on_signal(signum: int, _frame: Any) -> None:
        received.append(signum)
        stop.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, _on_signal)
    while not stop.is_set():
        _report_round(supervisor.run_once(), summary=False)
        # 等待期间收到信号也能立刻收工，不必睡满一个间隔。
        stop.wait(interval)
    name = signal.Signals(received[0]).name if received else ""
    typer.echo(i18n.t("cli.service.supervise.stopped", signal=name))


@app.command("install", help=i18n.t("cli.service.install.help"))
def install(
    dry_run: DryRunOption = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.service.install.option_force"))] = False,
) -> None:
    """写入系统服务单元并注册服务；``--dry-run`` 只打印将写入的内容。"""
    backend = build_backend()
    report = _guard(lambda: backend.install(dry_run=dry_run, force=force))
    if dry_run:
        typer.echo(report.detail)
        typer.echo(backend.render())
        return
    if report.enabled is False:
        fail(report.detail)
    ok(i18n.t("cli.service.install.written", path=escape(str(report.path))))
    if report.enabled is None:
        warn(report.detail)
        return
    ok(report.detail)


@app.command("uninstall", help=i18n.t("cli.service.uninstall.help"))
def uninstall(dry_run: DryRunOption = False) -> None:
    """注销服务并删除单元文件；本来就没装时如实说明，不算失败。"""
    backend = build_backend()
    report = _guard(lambda: backend.uninstall(dry_run=dry_run))
    if dry_run:
        typer.echo(report.detail)
        return
    if report.installed:
        fail(report.detail)
    if report.enabled is None:
        warn(report.detail)
        return
    ok(report.detail)


@app.command("status", help=i18n.t("cli.service.status.help"))
def status(as_json: JsonOption = False) -> None:
    """查看服务单元是否安装、是否已在系统中注册。"""
    report = build_backend().status()
    if as_json:
        typer.echo(json.dumps(report.as_dict(), ensure_ascii=False))
        return
    console.print(i18n.t("cli.service.status.backend", backend=report.backend))
    if report.path is not None:
        unit_key = "cli.service.status.unit_installed" if report.installed else "cli.service.status.unit_missing"
        console.print(i18n.t(unit_key, path=escape(str(report.path))))
    state = {True: "yes", False: "no", None: "unknown"}[report.enabled]
    console.print(i18n.t(f"cli.service.status.enabled.{state}"))
    console.print(i18n.t("cli.service.status.detail", detail=escape(report.detail)))


@app.command("supervise", help=i18n.t("cli.service.supervise.help"))
def supervise(
    once: Annotated[bool, typer.Option("--once", help=i18n.t("cli.service.supervise.option_once"))] = False,
    interval: Annotated[
        float, typer.Option("--interval", help=i18n.t("cli.service.supervise.option_interval"))
    ] = DEFAULT_INTERVAL,
    max_restarts: Annotated[
        int, typer.Option("--max-restarts", help=i18n.t("cli.service.supervise.option_max_restarts"))
    ] = DEFAULT_MAX_RESTARTS,
    backoff: Annotated[
        float, typer.Option("--backoff", help=i18n.t("cli.service.supervise.option_backoff"))
    ] = DEFAULT_BACKOFF,
) -> None:
    """守护本机实例：期望运行的恢复或重启，期望停止的保持不动。"""
    if interval <= 0:
        fail(i18n.t("cli.service.supervise.bad_interval", seconds=f"{interval:g}"))
    if max_restarts < 0 or backoff < 0:
        fail(i18n.t("cli.service.supervise.bad_policy"))
    supervisor = build_supervisor(max_restarts=max_restarts, backoff=backoff)
    if once:
        _report_round(supervisor.run_once(), summary=True)
        return
    _serve(supervisor, interval)
