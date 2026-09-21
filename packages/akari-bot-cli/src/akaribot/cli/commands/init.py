"""初始化实例"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import venv as engine
from akaribot.cli.instance import (
    system_python,
    DEFAULT_LOCALE,
    DEFAULT_VENV,
    INSTANCE_META_FILENAME,
    CliError,
    FlatCommandGroup,
    Instance,
    InstanceMeta,
    console,
    fail,
    ok,
    split_names,
    step,
    warn,
)

app = typer.Typer(
    help="初始化实例：建目录、写 akaribot.toml、装 core 与适配器、生成最小配置",
    cls=FlatCommandGroup,
    invoke_without_command=True,
    no_args_is_help=False,
)

# 与 bot.py 的首次运行骨架一致：顶层键不属于任何模板，扫描补不出来，只能显式落盘。
# 花括号在 str.format 里需写成双写；落盘后的单写 {I18N:...} 由 core 按所选语言翻译。
CONFIG_HEADER = (
    "# {{I18N:config.header.line.1}}\n"
    "# {{I18N:config.header.line.2}}\n"
    "# {{I18N:config.header.line.3}}\n"
    "\n"
    'default_locale = "{locale}" # {{I18N:config.comments.default_locale}}\n'
    "config_version = {version} # {{I18N:config.comments.config_version}}\n"
)


def _config_version(instance: Instance) -> int:
    """问实例解释器要 core 的配置版本号；失败时退回 1 并告警。"""
    code = "from akaribot.core.constants import config_version; print(config_version)"
    try:
        proc = instance.run_python_capture("-c", code)
    except CliError:
        proc = None
    if proc is not None and proc.returncode == 0:
        try:
            return int((proc.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            pass
    warn("未能从 core 读取 config_version，骨架暂写 1；首次启动会由核心配置迁移修正。")
    return 1


def _write_config_skeleton(instance: Instance, locale: str) -> None:
    """写出最小 config.toml 骨架，已存在时不覆盖。"""
    path = instance.config_dir / "config.toml"
    if path.exists():
        console.print(f"  已存在配置骨架，保留不动：{path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_HEADER.format(locale=locale, version=_config_version(instance)), encoding="utf-8")
    ok(f"已写出配置骨架 {path}")


def _ask_questions(
    locale: str | None,
    adapters: list[str],
    workspace_root: Path | None,
    no_venv: bool,
) -> tuple[str, list[str], Path | None, bool]:
    """交互式补齐未给出的选项，全部为线性问答（typer 内建 prompt/confirm）。"""
    if locale is None:
        locale = typer.prompt("实例默认语言（zh_cn / en_us / ja_jp / ko_kr / zh_tw）", default=DEFAULT_LOCALE).strip()
    if not adapters:
        answer = typer.prompt("要安装的适配器（逗号分隔，留空只装 core）", default="telegram")
        adapters = split_names([answer])
    managed = True
    if not no_venv:
        managed = typer.confirm(f"由 CLI 托管实例 venv（{DEFAULT_VENV}，推荐）", default=True)
    if workspace_root is None:
        if typer.confirm("从本地工作区源码安装（PyPI 上尚未发布时必选）", default=False):
            detected = engine.find_workspace_root(Path.cwd())
            answer = typer.prompt("工作区根目录", default=str(detected or Path.cwd()))
            workspace_root = Path(answer)
    return locale, adapters, workspace_root, managed


def _plan(
    instance: Instance,
    workspace_root: Path | None,
    adapters: list[str],
    modules: list[str],
    extras: list[str],
    offline: bool,
) -> list[engine.InstallTarget]:
    """解析 core、适配器与初始模块的安装目标并去重。"""
    catalog: engine.RegistryCatalog | None = None
    if workspace_root is None:
        catalog = engine.RegistryCatalog.load(instance.meta.registry_sources, offline=offline)
    targets: list[engine.InstallTarget] = []
    core = engine.resolve_target(
        "akari-bot-core",
        workspace_root=workspace_root,
        catalog=catalog,
        dist=None if workspace_root is not None else "akari-bot-core",
        extra=extras,
        kind="core",
    )
    targets.append(core)
    for name in adapters:
        targets.append(engine.resolve_target(name, workspace_root=workspace_root, catalog=catalog, kind="adapter"))
    for name in modules:
        targets.append(engine.resolve_target(name, workspace_root=workspace_root, catalog=catalog, kind="module"))
    return targets


def _install_specs(targets: list[engine.InstallTarget]) -> list[str]:
    """按分发名去重后拼出 uv 参数，本地依赖闭包里的重复路径只保留一次。"""
    specs: list[str] = []
    seen: set[str] = set()
    for target in targets:
        for spec in target.specs:
            if spec not in seen:
                seen.add(spec)
                specs.append(spec)
    return specs


@app.callback()
def init(
    path: Annotated[Path, typer.Argument(help="实例目录，缺省为当前目录")] = Path("."),
    locale: Annotated[str | None, typer.Option("--locale", help="实例默认语言，如 zh_cn / en_us")] = None,
    adapter: Annotated[list[str] | None, typer.Option("--adapter", help="要安装的适配器，可重复")] = None,
    module: Annotated[list[str] | None, typer.Option("--module", help="要额外安装的初始模块，可重复")] = None,
    no_venv: Annotated[bool, typer.Option("--no-venv", help="不托管 venv，直接安装到当前环境")] = False,
    workspace_root: Annotated[
        Path | None,
        typer.Option("--workspace-root", "--dev", help="使用工作区本地源码安装（本地路径模式）"),
    ] = None,
    python: Annotated[str | None, typer.Option("--python", help="建 venv 用的解释器，缺省与当前解释器一致")] = None,
    extra: Annotated[list[str] | None, typer.Option("--extra", help="core 的可选 extras，可重复")] = None,
    minimal: Annotated[bool, typer.Option("--minimal", help="不装任何 extras，与默认行为一致")] = False,
    non_interactive: Annotated[bool, typer.Option("--non-interactive", help="不提问，全部取默认值或选项值")] = False,
    skip_config_sync: Annotated[
        bool, typer.Option("--skip-config-sync", help="跳过 config sync（core 侧入口未就绪时使用）")
    ] = False,
    offline: Annotated[bool, typer.Option("--offline", help="registry 只用本地缓存，不联网")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="只打印将执行的命令，不写任何文件")] = False,
    force: Annotated[bool, typer.Option("--force", help="目标目录已存在实例或非空时继续")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="回显 uv 的全部输出")] = False,
) -> None:
    """创建实例目录、写元数据、安装 core 与适配器，并生成最小配置。"""
    root = path.expanduser().resolve()
    if (root / INSTANCE_META_FILENAME).exists() and not force:
        fail(
            f"{root} 已是 AkariBot 实例（存在 {INSTANCE_META_FILENAME}）。要改配置请用 `akaribot config`，确认覆盖加 --force。"
        )
    if root.exists() and any(root.iterdir()) and not (root / INSTANCE_META_FILENAME).exists() and not force:
        if non_interactive:
            fail(f"{root} 非空。换一个空目录，或确认可写入后加 --force。")
        typer.confirm(f"{root} 非空，继续会在其中创建实例文件。继续", abort=True)
    if minimal and extra:
        fail("--minimal 与 --extra 互斥：前者不装任何 extras。")

    adapters = split_names(adapter)
    modules = split_names(module)
    extras = split_names(extra)
    if workspace_root is not None:
        workspace_root = workspace_root.expanduser().resolve()
        if not (workspace_root / "packages").is_dir():
            fail(f"{workspace_root} 下没有 packages 目录，不像是 monorepo 工作区根。")
    if not non_interactive:
        locale, adapters, workspace_root, managed = _ask_questions(locale, adapters, workspace_root, no_venv)
    else:
        managed = not no_venv
        if not adapters:
            console.print("未指定 --adapter，按默认安装 telegram 适配器。")
            adapters = ["telegram"]
    locale = locale or DEFAULT_LOCALE
    if no_venv:
        managed = False

    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    try:
        targets = _plan(Instance.detached(root, locale=locale), workspace_root, adapters, modules, extras, offline)
    except CliError as exc:
        fail(str(exc))

    table = Table(title="将创建实例", show_header=False, padding=(0, 2))
    table.add_row("实例根", str(root))
    table.add_row("语言", locale)
    table.add_row("venv", f"托管 {DEFAULT_VENV}" if managed else "不托管（使用当前环境）")
    table.add_row("工作区", str(workspace_root) if workspace_root else "不使用（走 registry/PyPI）")
    table.add_row("安装", "\n".join(f"{target.dist}（{target.source}）" for target in targets))
    console.print(table)

    step(1, 5, "创建目录结构")
    if dry_run:
        console.print("[dim]dry-run：跳过目录创建[/dim]")
    else:
        created = Instance.create_dirs(root)
        ok(f"新建 {len(created)} 个目录：{'、'.join(item.name for item in created) or '无'}")

    step(2, 5, "写入 akaribot.toml")
    if dry_run:
        console.print("[dim]dry-run：跳过元数据写入[/dim]")
    else:
        meta = InstanceMeta.create(
            root,
            locale=locale,
            mode="workspace" if workspace_root else "installed",
            venv=DEFAULT_VENV if managed else "",
            workspace_root=str(workspace_root) if workspace_root else "",
        )
        meta.save()
        ok(f"已写入 {meta.path}")

    instance = Instance.detached(
        root,
        locale=locale,
        venv=DEFAULT_VENV if managed else "",
        workspace_root=str(workspace_root) if workspace_root else "",
        mode="workspace" if workspace_root else "installed",
    )
    if managed:
        step(3, 5, "创建实例 venv 并安装包")
        if dry_run:
            runner.run(engine.create_venv_argv(instance.venv_dir, python=python or str(system_python()), clear=force))
        else:
            try:
                runner.run_checked(
                    engine.create_venv_argv(instance.venv_dir, python=python or str(system_python()), clear=force),
                    what="创建实例 venv",
                )
            except CliError as exc:
                fail(f"{exc}。若本机没有 uv，可安装后重试，或用 --no-venv 直接装到当前环境。")
    else:
        step(3, 5, "在当前环境安装包")
        console.print(f"  目标解释器：{instance.python}")
        if not dry_run:
            warn("非托管模式会改动当前 Python 环境：确认该环境就是实例的运行环境。")

    try:
        runner.run_checked(engine.install_argv(instance.python, _install_specs(targets)), what="安装 core 与适配器")
    except CliError as exc:
        fail(str(exc))

    if dry_run:
        console.print("[dim]dry-run：跳过配置生成、数据库迁移与验证[/dim]")
        return

    step(4, 5, "生成配置")
    _write_config_skeleton(instance, locale)
    if skip_config_sync:
        warn("已跳过 config sync：配置项需在 core 侧入口就绪后运行 `akaribot config sync --package <dist>` 补齐。")
    else:
        try:
            for target in targets:
                engine.config_sync(instance, target.dist)
        except CliError as exc:
            warn(f"{exc}")
            warn("配置未补齐时机器人仍可启动（首次运行会扫描模板），也可稍后重试 config sync。")
        try:
            engine.db_upgrade(instance, "akari-bot-core")
        except CliError as exc:
            warn(f"{exc}；机器人启动时会自动迁移。")

    step(5, 5, "验证安装")
    code = "import akaribot.core, akaribot.core.constants; print(akaribot.core.constants.config_version)"
    try:
        proc = instance.run_python_capture("-c", code)
    except CliError as exc:
        fail(str(exc))
    if proc.returncode != 0:
        tail = " ".join((proc.stderr or "").strip().splitlines()[-2:]) or "无错误输出"
        fail(f"实例解释器无法 import core：{tail}")
    reported = ((proc.stdout or "").strip().splitlines() or ["?"])[-1]
    ok(f"core 在实例环境中可导入（config_version={reported}）")

    instance.invalidate()
    console.print("\n下一步：")
    console.print(f"  cd {root}")
    console.print("  akaribot config edit          # 填写 <Replace me> 占位符")
    console.print("  akaribot run                  # 启动机器人")
