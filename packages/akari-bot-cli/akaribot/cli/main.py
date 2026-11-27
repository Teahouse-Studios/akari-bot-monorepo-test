"""CLI 入口：注册全部子命令。

命令实现分散在 :mod:`akaribot.cli.commands` 下，各自导出一个 Typer 子应用。该模块仅负责装配，
不承载业务逻辑。实例操作一律通过 :class:`akaribot.cli.instance.Instance`，CLI 进程内不导入 core。
"""

from importlib import metadata
from pathlib import Path

import typer

from akaribot.cli import __version__, i18n
from akaribot.cli.commands import (
    adapter,
    config,
    db,
    docs,
    doctor,
    init,
    instance,
    logs,
    migrate,
    module,
    new,
    run,
    service,
    test,
    tui,
    venv,
)

DIST_NAME = "akari-bot-cli"
# 无子命令时的退出码。click ≥8.2 将 no_args_is_help 实现为 NoArgsIsHelpError（UsageError，退出码 2），
# 语义是“参数不足”而非成功。此处沿用该退出码，同时将帮助文本保留在标准输出通道，不进入错误面板。
NO_COMMAND_EXIT_CODE = 2


def version_string() -> str:
    """返回 CLI 版本号。

    版本号以分发 metadata 为真源，``pyproject.toml`` 只需维护一处。Nuitka onefile 冻结后
    ``.dist-info`` 可能未随产物保留，查询会抛 PackageNotFoundError，此时回退到包内常量，
    再取不到则返回 ``unknown``——版本查询是只读旁路，不应成为 CLI 的失败点，故冻结环境下
    metadata 的其它失败形态（文件缺失、路径扫描异常）同样按回退处理。

    :return: 版本号字符串。
    """
    try:
        return metadata.version(DIST_NAME)
    except Exception:  # noqa: BLE001 - 回退必须覆盖冻结产物的全部 metadata 读取失败。
        return __version__ or "unknown"


def _version_callback(value: bool) -> None:
    # eager 是必需的，因为 click 先解析完参数再判定是否存在子命令，非 eager 的回调排在该判定之后，
    # ``akaribot --version`` 会被 ``Missing command.`` 拦截。``--help`` 同为 eager，两者同时指定时
    # 按命令行顺序优先采用先出现的参数（click 对 eager 参数的既定处理），且均以状态码 0 退出。
    if value:
        typer.echo(version_string())
        raise typer.Exit()


app = typer.Typer(
    name="akaribot",
    help="AkariBot 实例管理工具。",
    # 不使用 click 的 no_args_is_help，因为 click ≥8.2 会将其视为错误抛出，导致帮助文本通过异常通道显示（带错误面板）。
    # 无参数调用改由下方回调显式打印帮助，输出通道与退出码均可控。
    no_args_is_help=False,
    add_completion=False,
)

for sub in (
    init,
    run,
    service,
    test,
    module,
    config,
    db,
    instance,
    adapter,
    venv,
    doctor,
    docs,
    new,
    tui,
    logs,
    migrate,
):
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
    # 无参数调用在可交互终端下直接进入界面。若无可用实例则引导初始化。非终端（管道、CI、重定向）仍打印
    # 帮助，因为该环境下界面无法启动，将帮助文本输出到错误面板容易误导用户判定为异常。
    if not _tui_available():
        typer.echo(ctx.get_help())
        raise typer.Exit(code=NO_COMMAND_EXIT_CODE)
    if _ensure_instance(lang) is None:
        raise typer.Exit(code=NO_COMMAND_EXIT_CODE)
    from akaribot.cli.commands.tui import run_interactive

    run_interactive()


def _tui_available() -> bool:
    from akaribot.cli.tui import _compat as compat

    # 界面需要读取按键并绘制全屏内容，在管道与重定向环境下不可用。
    return compat.is_interactive_terminal()


def _ensure_instance(lang: str | None) -> Path | None:
    # 初始化直接调用 ``akaribot init`` 的命令本体，不复制创建目录、安装包、写入元数据的流程。交互问答亦由
    # init 独立完成，避免重复提问。返回实例根目录路径，用户放弃或初始化未成功时返回 ``None``。
    from akaribot.cli.instance import resolve_instance_root

    # 在实例之外时按注册表中的默认实例进入，若本机已记录默认实例则直接沿用，无需每次询问是否执行初始化。
    found = resolve_instance_root()
    if found is not None:
        return found
    from akaribot.cli.commands.init import init

    typer.confirm(i18n.t("cli.main.init_confirm", root=Path.cwd()), abort=True)
    init(Path.cwd(), locale=lang)
    found = resolve_instance_root()
    if found is None:
        typer.echo(i18n.t("cli.main.init_failed"), err=True)
    return found


if __name__ == "__main__":
    app()
