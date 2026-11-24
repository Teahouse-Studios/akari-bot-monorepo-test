"""运行测试。"""

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
    # ``init`` 默认仅安装 core、适配器与用户选择的模块，不安装 ``akari-bot-testing``——它是开发阶段依赖。
    # 缺少依赖包时若直接将子进程抛出的 ``No module named`` 返回给用户，用户无法明确所需安装的依赖。此处给出明确的
    # 下一步提示。
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
    """在实例环境中运行测试。未知参数原样传递给 akaribot.testing。"""
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
    # 模式必须通过环境变量传递，因为 runner 在导入阶段读取 CI / COVERAGE，argv 中的开关生效过晚（这正是
    # “--ci 仍是非 CI 模式”的原因）。argv 中亦保留一份记录，确保两个入口的语义完全一致。
    env: dict[str, str] = {}
    if ci:
        args.append("--ci")
        env["CI"] = "1"
    if coverage:
        args.append("--coverage")
        env["COVERAGE"] = "1"
    raise typer.Exit(target.run_module("akaribot.testing", *args, **env))
