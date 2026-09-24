"""初始化实例"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from akaribot.cli import i18n
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
    help=i18n.t("cli.init.help"),
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

# 默认安装的 core extra：full 含 emotes 表情资源包（T3.3），--minimal 装裸 core 时跳过。
DEFAULT_CORE_EXTRA = "full"


def _core_extras(minimal: bool, extra: list[str]) -> list[str]:
    if minimal:
        return []
    return list(dict.fromkeys((DEFAULT_CORE_EXTRA, *extra)))


def _config_version(instance: Instance) -> int:
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
    warn(i18n.t("cli.init.config_version_unknown"))
    return 1


def _write_config_skeleton(instance: Instance, locale: str) -> None:
    path = instance.config_dir / "config.toml"
    if path.exists():
        console.print(i18n.t("cli.init.skeleton_exists", path=path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_HEADER.format(locale=locale, version=_config_version(instance)), encoding="utf-8")
    ok(i18n.t("cli.init.skeleton_written", path=path))


def _ask_questions(
    locale: str | None,
    adapters: list[str],
    workspace_root: Path | None,
    no_venv: bool,
) -> tuple[str, list[str], Path | None, bool]:
    if locale is None:
        locale = typer.prompt(i18n.t("cli.init.ask.locale"), default=DEFAULT_LOCALE).strip()
    if not adapters:
        answer = typer.prompt(i18n.t("cli.init.ask.adapters"), default="telegram")
        adapters = split_names([answer])
    managed = True
    if not no_venv:
        managed = typer.confirm(i18n.t("cli.init.ask.managed_venv", venv=DEFAULT_VENV), default=True)
    if workspace_root is None:
        if typer.confirm(i18n.t("cli.init.ask.workspace"), default=False):
            detected = engine.find_workspace_root(Path.cwd())
            answer = typer.prompt(i18n.t("cli.init.ask.workspace_root"), default=str(detected or Path.cwd()))
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
    path: Annotated[Path, typer.Argument(help=i18n.t("cli.init.arg_path"))] = Path("."),
    locale: Annotated[str | None, typer.Option("--locale", help=i18n.t("cli.init.option_locale"))] = None,
    adapter: Annotated[list[str] | None, typer.Option("--adapter", help=i18n.t("cli.init.option_adapter"))] = None,
    module: Annotated[list[str] | None, typer.Option("--module", help=i18n.t("cli.init.option_module"))] = None,
    no_venv: Annotated[bool, typer.Option("--no-venv", help=i18n.t("cli.init.option_no_venv"))] = False,
    workspace_root: Annotated[
        Path | None,
        typer.Option("--workspace-root", "--dev", help=i18n.t("cli.init.option_workspace_root")),
    ] = None,
    python: Annotated[str | None, typer.Option("--python", help=i18n.t("cli.init.option_python"))] = None,
    extra: Annotated[list[str] | None, typer.Option("--extra", help=i18n.t("cli.init.option_extra"))] = None,
    minimal: Annotated[bool, typer.Option("--minimal", help=i18n.t("cli.init.option_minimal"))] = False,
    non_interactive: Annotated[
        bool, typer.Option("--non-interactive", help=i18n.t("cli.init.option_non_interactive"))
    ] = False,
    skip_config_sync: Annotated[
        bool, typer.Option("--skip-config-sync", help=i18n.t("cli.init.option_skip_config_sync"))
    ] = False,
    offline: Annotated[bool, typer.Option("--offline", help=i18n.t("cli.init.option_offline"))] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help=i18n.t("cli.init.option_dry_run"))] = False,
    force: Annotated[bool, typer.Option("--force", help=i18n.t("cli.init.option_force"))] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help=i18n.t("cli.init.option_verbose"))] = False,
) -> None:
    """创建实例目录、写元数据、安装 core 与适配器，并生成最小配置。"""
    root = path.expanduser().resolve()
    if (root / INSTANCE_META_FILENAME).exists() and not force:
        fail(i18n.t("cli.init.already_instance", root=root, meta=INSTANCE_META_FILENAME))
    if root.exists() and any(root.iterdir()) and not (root / INSTANCE_META_FILENAME).exists() and not force:
        if non_interactive:
            fail(i18n.t("cli.init.not_empty", root=root))
        typer.confirm(i18n.t("cli.init.not_empty_confirm", root=root), abort=True)
    if minimal and extra:
        fail(i18n.t("cli.init.minimal_conflict"))

    adapters = split_names(adapter)
    modules = split_names(module)
    extras = _core_extras(minimal, split_names(extra))
    if workspace_root is not None:
        workspace_root = workspace_root.expanduser().resolve()
        if not (workspace_root / "packages").is_dir():
            fail(i18n.t("cli.init.not_workspace", root=workspace_root))
    if not non_interactive:
        locale, adapters, workspace_root, managed = _ask_questions(locale, adapters, workspace_root, no_venv)
    else:
        managed = not no_venv
        if not adapters:
            console.print(i18n.t("cli.init.default_adapter"))
            adapters = ["telegram"]
    locale = locale or DEFAULT_LOCALE
    if no_venv:
        managed = False

    runner = engine.CommandRunner(dry_run=dry_run, verbose=verbose)
    try:
        targets = _plan(Instance.detached(root, locale=locale), workspace_root, adapters, modules, extras, offline)
    except CliError as exc:
        fail(str(exc))

    table = Table(title=i18n.t("cli.init.plan.title"), show_header=False, padding=(0, 2))
    table.add_row(i18n.t("cli.init.plan.root"), str(root))
    table.add_row(i18n.t("cli.init.plan.locale"), locale)
    venv_text = (
        i18n.t("cli.init.plan.venv_managed", venv=DEFAULT_VENV) if managed else i18n.t("cli.init.plan.venv_unmanaged")
    )
    table.add_row("venv", venv_text)
    workspace_text = str(workspace_root) if workspace_root else i18n.t("cli.init.plan.workspace_none")
    table.add_row(i18n.t("cli.init.plan.workspace"), workspace_text)
    installs = "\n".join(
        i18n.t("cli.init.plan.install_item", dist=target.dist, source=target.source) for target in targets
    )
    table.add_row(i18n.t("cli.init.plan.install"), installs)
    console.print(table)

    step(1, 5, i18n.t("cli.init.step.dirs"))
    if dry_run:
        console.print(i18n.t("cli.init.dry_run.dirs"))
    else:
        created = Instance.create_dirs(root)
        names = i18n.t("cli.common.list_separator").join(item.name for item in created)
        ok(i18n.t("cli.init.dirs_created", count=len(created), names=names or i18n.t("cli.init.none")))

    step(2, 5, i18n.t("cli.init.step.meta"))
    if dry_run:
        console.print(i18n.t("cli.init.dry_run.meta"))
    else:
        meta = InstanceMeta.create(
            root,
            locale=locale,
            mode="workspace" if workspace_root else "installed",
            venv=DEFAULT_VENV if managed else "",
            workspace_root=str(workspace_root) if workspace_root else "",
        )
        meta.save()
        ok(i18n.t("cli.init.meta_written", path=meta.path))

    instance = Instance.detached(
        root,
        locale=locale,
        venv=DEFAULT_VENV if managed else "",
        workspace_root=str(workspace_root) if workspace_root else "",
        mode="workspace" if workspace_root else "installed",
    )
    if managed:
        step(3, 5, i18n.t("cli.init.step.venv"))
        if dry_run:
            runner.run(engine.create_venv_argv(instance.venv_dir, python=python or str(system_python()), clear=force))
        else:
            try:
                runner.run_checked(
                    engine.create_venv_argv(instance.venv_dir, python=python or str(system_python()), clear=force),
                    what=i18n.t("cli.venv_engine.what_create_venv"),
                )
            except CliError as exc:
                fail(i18n.t("cli.init.venv_failed", error=exc))
    else:
        step(3, 5, i18n.t("cli.init.step.current_env"))
        console.print(i18n.t("cli.init.target_python", python=instance.python))
        if not dry_run:
            warn(i18n.t("cli.init.unmanaged_warning"))

    try:
        # 同上：what 由 venv.py 拼接「完成/失败」，保持原文。
        what = i18n.t("cli.init.what_install")
        runner.run_checked(engine.install_argv(instance.python, _install_specs(targets)), what=what)
    except CliError as exc:
        fail(str(exc))

    if dry_run:
        console.print(i18n.t("cli.init.dry_run.rest"))
        return

    step(4, 5, i18n.t("cli.init.step.config"))
    _write_config_skeleton(instance, locale)
    if skip_config_sync:
        warn(i18n.t("cli.init.config_sync_skipped"))
    else:
        try:
            for target in targets:
                engine.config_sync(instance, target.dist)
        except CliError as exc:
            warn(f"{exc}")
            warn(i18n.t("cli.init.config_sync_failed"))
        try:
            engine.db_upgrade(instance, "akari-bot-core")
        except CliError as exc:
            warn(i18n.t("cli.init.db_upgrade_failed", error=exc))

    step(5, 5, i18n.t("cli.init.step.verify"))
    code = "import akaribot.core, akaribot.core.constants; print(akaribot.core.constants.config_version)"
    try:
        proc = instance.run_python_capture("-c", code)
    except CliError as exc:
        fail(str(exc))
    if proc.returncode != 0:
        tail = " ".join((proc.stderr or "").strip().splitlines()[-2:]) or i18n.t("cli.init.no_stderr")
        fail(i18n.t("cli.init.import_failed", detail=tail))
    reported = ((proc.stdout or "").strip().splitlines() or ["?"])[-1]
    ok(i18n.t("cli.init.import_ok", version=reported))

    instance.invalidate()
    console.print(i18n.t("cli.init.next_steps"))
    console.print(f"  cd {root}")
    console.print(i18n.t("cli.init.next_config_edit"))
    console.print(i18n.t("cli.init.next_run"))
