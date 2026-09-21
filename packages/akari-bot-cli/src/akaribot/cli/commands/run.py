"""运行机器人"""

from __future__ import annotations

from typing import Annotated

import typer

from akaribot.cli.instance import InstancePathOption, PassthroughCommandGroup, require_instance

app = typer.Typer(
    help="运行机器人（等价于 python -m akaribot.core.entrypoints.run）",
    cls=PassthroughCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)


@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def run(
    ctx: typer.Context,
    adapter: Annotated[
        list[str] | None,
        typer.Option("--adapter", "-a", help="只启动指定适配器，可重复；缺省启动全部已配置适配器"),
    ] = None,
    foreground: Annotated[bool, typer.Option("--foreground", help="前台运行（默认即为前台）")] = False,
    no_auto_migrate: Annotated[bool, typer.Option("--no-auto-migrate", help="启动时不自动应用数据库迁移")] = False,
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
