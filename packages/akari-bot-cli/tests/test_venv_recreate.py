import subprocess
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import CliError, Instance, InstanceMeta, is_windows, venv_scripts_dir
from akaribot.testing import Tester, func_case


def _wheel(root: Path):
    wheel = root / "akari_bot_module_recreate_probe-0.1.0-py3-none-any.whl"
    prefix = "akari_bot_module_recreate_probe-0.1.0.dist-info"
    contents = {
        "akaribot/modules/recreate_probe/__init__.py": 'def main():\n    print("recreated-entry")\n',
        f"{prefix}/METADATA": "Metadata-Version: 2.1\nName: akari-bot-module-recreate-probe\nVersion: 0.1.0\n",
        f"{prefix}/WHEEL": "Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        f"{prefix}/entry_points.txt": (
            "[console_scripts]\nrecreate-probe = akaribot.modules.recreate_probe:main\n"
            "[akaribot.modules]\nrecreate_probe = akaribot.modules.recreate_probe\n"
        ),
    }
    contents[f"{prefix}/RECORD"] = "".join(f"{name},,\n" for name in contents) + f"{prefix}/RECORD,,\n"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, text in contents.items():
            archive.writestr(name, text)
    return wheel


class _LocalWheelRunner(engine.CommandRunner):
    def __init__(self, wheel: Path):
        super().__init__()
        self.wheel = wheel

    def run_checked(self, argv, **kwargs):
        if "pip" in argv and "install" in argv:
            argv = [*argv[: argv.index("--python") + 2], "--no-deps", str(self.wheel)]
        return super().run_checked(argv, **kwargs)


def _fixture(root: Path):
    wheel = _wheel(root)
    instance_root = root / "instance"
    instance_root.mkdir()
    InstanceMeta.create(instance_root).save()
    instance = Instance(instance_root)
    python = engine.system_python()
    runner = _LocalWheelRunner(wheel)
    runner.run_checked(engine.create_venv_argv(instance.venv_dir, python=str(python)), what="venv")
    runner.run_checked(engine.install_argv(instance.python, [str(wheel)]), what="wheel")
    (instance.venv_dir / "old-marker").write_text("old", encoding="utf-8")
    return instance, runner, python


def _run_script(instance: Instance):
    name = "recreate-probe.exe" if is_windows() else "recreate-probe"
    script = venv_scripts_dir(instance.venv_dir) / name
    completed = subprocess.run([str(script)], text=True, capture_output=True, check=False, timeout=20)
    return completed.returncode == 0 and completed.stdout.strip() == "recreated-entry"


def _test_recreated_console_script_runs_after_swap():
    with tempfile.TemporaryDirectory(prefix="akari-recreate-") as temporary:
        instance, runner, python = _fixture(Path(temporary))
        engine.recreate(instance, runner=runner, python=str(python))
        return (
            _run_script(instance)
            and not instance.venv_dir.with_name(".venv.new").exists()
            and not instance.venv_dir.with_name(".venv.old").exists()
        )


def _test_second_rename_failure_restores_old_environment():
    with tempfile.TemporaryDirectory(prefix="akari-recreate-") as temporary:
        instance, runner, python = _fixture(Path(temporary))
        original = Path.rename

        def rename(path, target):
            if path == instance.venv_dir.with_name(".venv.new"):
                raise OSError("injected swap failure")
            return original(path, target)

        with patch.object(Path, "rename", rename):
            try:
                engine.recreate(instance, runner=runner, python=str(python))
            except CliError:
                return (instance.venv_dir / "old-marker").is_file() and _run_script(instance)
        return False


def _test_final_verification_failure_restores_old_environment():
    with tempfile.TemporaryDirectory(prefix="akari-recreate-") as temporary:
        instance, runner, python = _fixture(Path(temporary))
        with patch.object(engine, "_verify_recreated_environment", side_effect=CliError("injected probe failure")):
            try:
                engine.recreate(instance, runner=runner, python=str(python))
            except CliError:
                return (
                    (instance.venv_dir / "old-marker").is_file()
                    and instance.venv_dir.with_name(".venv.new").is_dir()
                    and _run_script(instance)
                )
        return False


def _test_first_rename_failure_keeps_old_environment():
    with tempfile.TemporaryDirectory(prefix="akari-recreate-") as temporary:
        instance, runner, python = _fixture(Path(temporary))
        original = Path.rename

        def rename(path, target):
            if path == instance.venv_dir:
                raise OSError("injected backup failure")
            return original(path, target)

        with patch.object(Path, "rename", rename):
            try:
                engine.recreate(instance, runner=runner, python=str(python))
            except CliError:
                return (instance.venv_dir / "old-marker").is_file() and _run_script(instance)
        return False


def _test_dry_run_keeps_existing_staging():
    with tempfile.TemporaryDirectory(prefix="akari-recreate-") as temporary:
        instance, _runner, python = _fixture(Path(temporary))
        staging = instance.venv_dir.with_name(".venv.new")
        staging.mkdir()
        marker = staging / "keep"
        marker.write_text("keep", encoding="utf-8")
        engine.recreate(instance, runner=engine.CommandRunner(dry_run=True), python=str(python), force=True)
        return marker.read_text(encoding="utf-8") == "keep" and _run_script(instance)


@func_case
async def test_venv_recreate(tester: Tester):
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")
    await tester.test(_test_recreated_console_script_runs_after_swap, "重建并换位后真实 console script 可执行")
    await tester.test(_test_first_rename_failure_keeps_old_environment, "备份换位失败时旧环境可执行")
    await tester.test(_test_second_rename_failure_restores_old_environment, "新环境换位失败时恢复旧环境")
    await tester.test(_test_final_verification_failure_restores_old_environment, "最终路径验证失败时恢复旧环境")
    await tester.test(_test_dry_run_keeps_existing_staging, "重建预演保留已有临时环境")
    return tester
