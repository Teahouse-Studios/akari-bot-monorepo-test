"""运行测试"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from akaribot.cli.instance import InstancePathOption, PassthroughCommandGroup, require_instance

app = typer.Typer(
    help="运行测试（等价于 python -m akaribot.testing）",
    cls=PassthroughCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)


@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument(help="要跑的测试路径；缺省跑全部")] = None,
    ci: Annotated[bool, typer.Option("--ci", help="CI 模式：非交互、失败即退出")] = False,
    coverage: Annotated[bool, typer.Option("--coverage", help="统计覆盖率")] = False,
    case: Annotated[list[str] | None, typer.Option("--case", help="只跑指定用例，可重复")] = None,
    instance: InstancePathOption = None,
) -> None:
    """在实例环境里运行测试；未知参数原样透传给 akaribot.testing。"""
    target = require_instance(instance)
    args: list[str] = []
    if path is not None:
        args.append(str(path))
    if ci:
        args.append("--ci")
    if coverage:
        args.append("--coverage")
    for name in case or []:
        args += ["--case", name]
    args += list(ctx.args)
    raise typer.Exit(target.run_module("akaribot.testing", *args))
