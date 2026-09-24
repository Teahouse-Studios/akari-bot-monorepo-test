"""运行测试"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from akaribot.cli import i18n
from akaribot.cli.instance import CliError, InstancePathOption, PassthroughCommandGroup, fail, require_instance

app = typer.Typer(
    help=i18n.t("cli.test.help"),
    cls=PassthroughCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)

TESTING_MODULE = "akaribot.testing"
TESTING_DIST = "akari-bot-testing"


def _ensure_testing_installed(target) -> None:
    # ``init`` 默认只装 core、适配器与用户选的模块，不装 ``akari-bot-testing``——它是开发期依赖。
    # 缺包时若直接把子进程的 ``No module named`` 抛给用户，没人知道该装什么；这里换成一句明确的
    # 下一步。
    try:
        proc = target.run_python_capture("-c", f"import {TESTING_MODULE}", timeout=60.0)
    except CliError as exc:
        raise CliError(i18n.t("cli.test.probe_failed", error=exc)) from exc
    if proc.returncode != 0:
        raise CliError(i18n.t("cli.test.testing_missing", dist=TESTING_DIST))


@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument(help=i18n.t("cli.test.arg_path"))] = None,
    ci: Annotated[bool, typer.Option("--ci", help=i18n.t("cli.test.option_ci"))] = False,
    coverage: Annotated[bool, typer.Option("--coverage", help=i18n.t("cli.test.option_coverage"))] = False,
    case: Annotated[list[str] | None, typer.Option("--case", help=i18n.t("cli.test.option_case"))] = None,
    instance: InstancePathOption = None,
) -> None:
    """在实例环境里运行测试；未知参数原样透传给 akaribot.testing。"""
    target = require_instance(instance)
    try:
        _ensure_testing_installed(target)
    except CliError as exc:
        fail(str(exc))
    args: list[str] = []
    if path is not None:
        args.append(str(path))
    for name in case or []:
        args += ["--case", name]
    args += list(ctx.args)
    # 模式必须经环境变量传：runner 在导入期读 CI / COVERAGE，argv 里的开关到得太晚（这正是
    # 「--ci 仍是非 CI 模式」的原因）；argv 里也留一份，让两条入口语义一致。
    env: dict[str, str] = {}
    if ci:
        args.append("--ci")
        env["CI"] = "1"
    if coverage:
        args.append("--coverage")
        env["COVERAGE"] = "1"
    raise typer.Exit(target.run_module("akaribot.testing", *args, **env))
