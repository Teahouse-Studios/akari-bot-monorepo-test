"""运行机器人"""

from __future__ import annotations

from typing import Annotated

import typer

from akaribot.cli import i18n
from akaribot.cli.instance import InstancePathOption, PassthroughCommandGroup, require_instance

app = typer.Typer(
    help=i18n.t("cli.run.help"),
    cls=PassthroughCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)


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
    instance: InstancePathOption = None,
) -> None:
    """启动实例机器人；未知参数原样透传给 core。"""
    target = require_instance(instance)
    args: list[str] = []
    for name in adapter or []:
        args += ["--adapter", name]
    if foreground:
        args.append("--foreground")
    if no_auto_migrate:
        args.append("--no-auto-migrate")
    args += list(ctx.args)
    raise typer.Exit(target.run_core("run", *args))
