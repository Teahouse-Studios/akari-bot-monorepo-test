"""CLI 入口：注册全部子命令。

命令实现分散在 :mod:`akaribot.cli.commands` 下，各自导出一个 Typer 子应用；本模块只做装配，
不承载业务逻辑。实例操作一律经 :class:`akaribot.cli.instance.Instance`，CLI 进程内不 import core。
"""

import typer

from akaribot.cli import __version__, i18n
from akaribot.cli.commands import adapter, config, doctor, init, migrate, module, new, run, test, tui, venv

app = typer.Typer(
    name="akaribot",
    help="AkariBot 实例管理工具。",
    no_args_is_help=True,
    add_completion=False,
)

for sub in (init, run, test, module, config, adapter, venv, doctor, new, tui, migrate):
    app.add_typer(sub.app, name=sub.__name__.rsplit(".", 1)[-1])


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", help="打印版本后退出"),
    lang: str | None = typer.Option(None, "--lang", help="界面语言，如 zh_cn / en_us"),
) -> None:
    """AkariBot 实例管理工具。"""
    i18n.set_locale(lang)
    if version:
        typer.echo(__version__)
        raise typer.Exit()


if __name__ == "__main__":
    app()
