"""CLI 入口：注册全部子命令。

命令实现分散在 :mod:`akaribot.cli.commands` 下，各自导出一个 Typer 子应用；本模块只做装配，
不承载业务逻辑。实例操作一律经 :class:`akaribot.cli.instance.Instance`，CLI 进程内不 import core。
"""

from importlib import metadata
from pathlib import Path

import typer

from akaribot.cli import __version__, i18n
from akaribot.cli.commands import adapter, config, db, doctor, init, migrate, module, new, run, test, tui, venv

DIST_NAME = "akari-bot-cli"
# 无子命令时的退出码。click ≥8.2 把 no_args_is_help 实现为 NoArgsIsHelpError（UsageError，退出码 2），
# 语义是「参数不足」而非成功；这里沿用该码，同时把帮助文本留在正常输出通道，不落进错误面板。
NO_COMMAND_EXIT_CODE = 2


def version_string() -> str:
    """返回 CLI 版本号。

    版本号以分发 metadata 为真源，``pyproject.toml`` 只需维护一处。Nuitka onefile 冻结后
    ``.dist-info`` 可能未随产物保留，查询会抛 PackageNotFoundError；此时回退到包内常量，
    再取不到则返回 ``unknown``——版本查询是只读旁路，不应成为 CLI 的失败点，故冻结环境下
    metadata 的其它失败形态（文件缺失、路径扫描异常）同样走兜底。

    :return: 版本号字符串。
    """
    try:
        return metadata.version(DIST_NAME)
    except Exception:  # noqa: BLE001 - 兜底必须覆盖冻结产物的全部 metadata 读取失败
        return __version__ or "unknown"


def _version_callback(value: bool) -> None:
    # eager 是必需的：click 先解析完参数、再判定「有没有子命令」，非 eager 的回调排在该判定之后，
    # ``akaribot --version`` 会被 ``Missing command.`` 抢先。``--help`` 同为 eager，两者同时给出时
    # 按命令行顺序先出现的先生效（click 对 eager 参数的既定处理），且都以 0 退出。
    if value:
        typer.echo(version_string())
        raise typer.Exit()


app = typer.Typer(
    name="akaribot",
    help="AkariBot 实例管理工具。",
    # 不用 click 的 no_args_is_help：click ≥8.2 把它当错误抛出，帮助文本经异常通道显示（带错误面板）。
    # 裸调用改由下方回调显式打印帮助，输出通道与退出码都可控。
    no_args_is_help=False,
    add_completion=False,
)

for sub in (init, run, test, module, config, db, adapter, venv, doctor, new, tui, migrate):
    app.add_typer(sub.app, name=sub.__name__.rsplit(".", 1)[-1])


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", callback=_version_callback, is_eager=True, help="打印版本后退出"),
    lang: str | None = typer.Option(None, "--lang", help="界面语言，如 zh_cn / en_us"),
) -> None:
    """AkariBot 实例管理工具。"""
    i18n.set_locale(lang)
    if ctx.invoked_subcommand is not None:
        return
    # 裸调用在可交互终端下直接进界面；没有实例就先引导初始化。非终端（管道、CI、重定向）仍打印
    # 帮助：那种环境下界面起不来，把帮助塞进错误面板只会让人以为出错了。
    if not _tui_available():
        typer.echo(ctx.get_help())
        raise typer.Exit(code=NO_COMMAND_EXIT_CODE)
    if _ensure_instance(lang) is None:
        raise typer.Exit(code=NO_COMMAND_EXIT_CODE)
    from akaribot.cli.commands.tui import run_interactive

    run_interactive()


def _tui_available() -> bool:
    from akaribot.cli.tui import _compat as compat

    # 界面需要能读键、能画全屏，管道与重定向下不可用。
    return compat.is_interactive_terminal()


def _ensure_instance(lang: str | None) -> Path | None:
    # 初始化直接调用 ``akaribot init`` 的命令本体，不复制它建目录、装包、写元数据的流程；问答也由
    # init 自己完成，两边不会各问一套。返回实例根，用户放弃或初始化未成功时为 ``None``。
    from akaribot.cli.instance import find_instance_root

    found = find_instance_root()
    if found is not None:
        return found
    from akaribot.cli.commands.init import init

    typer.confirm(i18n.t("cli.main.init_confirm", root=Path.cwd()), abort=True)
    init(Path.cwd(), locale=lang)
    found = find_instance_root()
    if found is None:
        typer.echo(i18n.t("cli.main.init_failed"), err=True)
    return found


if __name__ == "__main__":
    app()
