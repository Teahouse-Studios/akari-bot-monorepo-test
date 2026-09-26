"""运行机器人"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from akaribot.cli import i18n
from akaribot.cli.instance import (
    CliError,
    InstancePathOption,
    PassthroughCommandGroup,
    fail,
    ok,
    require_instance,
)
from akaribot.cli.process import pid_alive, wait_until

app = typer.Typer(
    help=i18n.t("cli.run.help"),
    cls=PassthroughCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)

# 后台启动后等待实例取到锁的秒数。取锁前要跑完 pre-init（配置、数据库），故留出余量。
READY_TIMEOUT_SECONDS = 30.0
LOG_TAIL_CHARS = 800


def console_log_path(root: Path) -> Path:
    """后台实例控制台输出的落盘路径。"""
    return root / "logs" / f"RunConsole_{datetime.now().strftime('%Y-%m-%d')}.log"


@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def run(
    ctx: typer.Context,
    adapter: Annotated[
        list[str] | None,
        typer.Option("--adapter", "-a", help=i18n.t("cli.run.option_adapter")),
    ] = None,
    foreground: Annotated[bool, typer.Option("--foreground", help=i18n.t("cli.run.option_foreground"))] = False,
    no_auto_migrate: Annotated[
        bool, typer.Option("--no-auto-migrate", help=i18n.t("cli.run.option_no_auto_migrate"))
    ] = False,
    detach: Annotated[bool, typer.Option("--detach", "-d", help=i18n.t("cli.run.option_detach"))] = False,
    stop: Annotated[bool, typer.Option("--stop", help=i18n.t("cli.run.option_stop"))] = False,
    restart: Annotated[bool, typer.Option("--restart", help=i18n.t("cli.run.option_restart"))] = False,
    status: Annotated[bool, typer.Option("--status", help=i18n.t("cli.run.option_status"))] = False,
    as_json: Annotated[bool, typer.Option("--json", help=i18n.t("cli.common.json_option"))] = False,
    timeout: Annotated[float, typer.Option("--timeout", help=i18n.t("cli.run.option_timeout"))] = 20.0,
    instance: InstancePathOption = None,
) -> None:
    """启动、停止或查看实例；未知参数原样透传给 core。"""
    target = require_instance(instance)
    chosen = [name for name, picked in (("--stop", stop), ("--restart", restart), ("--status", status)) if picked]
    if detach:
        chosen.append("--detach")
    if len(chosen) > 1:
        fail(i18n.t("cli.run.conflict_actions", actions=", ".join(chosen)))
    if detach and foreground:
        fail(i18n.t("cli.run.conflict_foreground"))
    if status:
        _print_status(target, as_json=as_json)
        return
    if stop:
        _stop(target, as_json=as_json, timeout=timeout)
        return
    if restart:
        _stop(target, as_json=as_json, timeout=timeout)
    args: list[str] = []
    for name in adapter or []:
        args += ["--adapter", name]
    if foreground:
        args.append("--foreground")
    if no_auto_migrate:
        args.append("--no-auto-migrate")
    args += list(ctx.args)
    if detach or restart:
        _start_detached(target, args, as_json=as_json)
        return
    raise typer.Exit(target.run_core("run", *args))


def _print_status(target, *, as_json: bool) -> None:
    state = target.run_state()
    if as_json:
        typer.echo(
            json.dumps(
                {
                    "running": state.running,
                    "pid": state.pid,
                    "started_at": state.started_at,
                    "argv": list(state.argv),
                    "lock": str(target.lock_path()),
                    "console_log": str(console_log_path(target.root)),
                    "detail": state.detail,
                },
                ensure_ascii=False,
            )
        )
        return
    if not state.running:
        typer.echo(i18n.t("cli.run.status_stopped", lock=target.lock_path()))
        return
    if state.pid is None:
        typer.echo(i18n.t("cli.run.status_unmanaged", lock=target.lock_path()))
        return
    typer.echo(
        i18n.t(
            "cli.run.status_running",
            pid=state.pid,
            started=state.started_at or i18n.t("cli.common.unknown"),
        )
    )


def _stop(target, *, as_json: bool, timeout: float) -> None:
    try:
        outcome = target.stop_running(timeout=timeout)
    except CliError as exc:
        fail(str(exc))
    if as_json:
        typer.echo(
            json.dumps(
                {"stopped": outcome.ok, "forced": outcome.forced, "message": outcome.message, "detail": outcome.detail},
                ensure_ascii=False,
            )
        )
    elif outcome.ok:
        ok(outcome.message)
    else:
        fail(outcome.message)


def _start_detached(target, args: list[str], *, as_json: bool) -> None:
    log_path = console_log_path(target.root)
    try:
        launched = target.spawn_detached(*args, log_path=log_path)
    except CliError as exc:
        fail(str(exc))
    # 取到锁才算启动成功：进程可能在 pre-init 阶段就因配置或数据库问题退出。
    ready = wait_until(lambda: target.is_running() or not pid_alive(launched.pid), timeout=READY_TIMEOUT_SECONDS)
    if ready and target.is_running():
        if as_json:
            typer.echo(
                json.dumps({"started": True, "pid": launched.pid, "log": str(launched.log_path)}, ensure_ascii=False)
            )
        else:
            ok(i18n.t("cli.run.detached_started", pid=launched.pid, log=launched.log_path))
        return
    detail = i18n.t("cli.run.detached_failed_detail", log=launched.log_path, tail=_log_tail(launched.log_path))
    if as_json:
        typer.echo(json.dumps({"started": False, "pid": launched.pid, "detail": detail}, ensure_ascii=False))
    else:
        fail(i18n.t("cli.run.detached_failed", detail=detail))
    raise typer.Exit(1)


def _log_tail(path: Path, limit: int = LOG_TAIL_CHARS) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return text.strip()[-limit:] or i18n.t("cli.common.no_output")
