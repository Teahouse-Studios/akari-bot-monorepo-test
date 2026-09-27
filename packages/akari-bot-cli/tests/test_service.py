"""服务化：单元文件渲染、安装卸载、状态探测与实例守护。

系统命令一律经注入的 runner 记录，文件写在临时 home 下，故用例不调用 ``launchctl`` /
``systemctl``，也不启动任何实例进程。守护循环用假控制器与可推进的假时钟驱动，观测「恢复」「崩溃
重启」「退避与上限」「跳过」四类分支。
"""

from __future__ import annotations

import json
import os
import plistlib
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli.instance import DetachedRun, Instance, InstanceMeta, RunState, StopOutcome
from akaribot.cli.instances import STATE_RUNNING, STATE_STOPPED, InstanceRegistry
from akaribot.cli.main import app as cli_app
from akaribot.cli.service import (
    BACKEND_LAUNCHD,
    BACKEND_SYSTEMD,
    BACKEND_UNSUPPORTED,
    KIND_ABANDONED,
    KIND_FAILED,
    KIND_MISSING,
    KIND_OBSERVED,
    KIND_RECOVERED,
    KIND_REFUSED,
    KIND_RESTARTED,
    KIND_STRAY,
    LAUNCHD_LABEL,
    ServiceBackend,
    ServiceError,
    Supervisor,
    detect_backend,
    render_unit,
    unit_path,
)
from akaribot.testing import Tester, func_case

PYTHON_ARGV = ("/usr/bin/python3", "-m", "akaribot.cli.main")
CLI_BIN = ("/usr/bin/python3", "-m", "akaribot.cli.main")


class _FakeRunner:
    # 记录被调用的命令，并按前缀回放预设退出码；没有预设前缀的命令按成功处理。
    def __init__(self, results=None):
        self.calls: list[list[str]] = []
        self.results: dict[tuple[str, ...], int] = dict(results or {})

    def __call__(self, argv):
        self.calls.append(list(argv))
        for prefix, code in sorted(self.results.items(), key=lambda item: -len(item[0])):
            if tuple(argv[: len(prefix)]) == prefix:
                return subprocess.CompletedProcess(list(argv), code, "", "probe failed")
        return subprocess.CompletedProcess(list(argv), 0, "", "")


class _FakeInstance:
    # 守护循环的假控制器：只回答运行状态与进程信息，拉起由外部函数记账。
    def __init__(self, root: Path):
        self.root = root
        self.running = False
        self.pid = 4242

    def is_running(self) -> bool:
        return self.running

    def run_state(self) -> RunState:
        return RunState(running=self.running, pid=self.pid if self.running else None)


class _Rig:
    # 一轮守护所需的假注册表、假控制器、假时钟与拉起记账。
    def __init__(self, config: Path):
        self.config = config
        self.instances: dict[str, _FakeInstance] = {}
        self.spawned: list[str] = []
        self.now = 1000.0

    def registry(self) -> InstanceRegistry:
        return InstanceRegistry(self.config / "instances.toml")

    def add(self, name: str, *, restart_on_crash: bool = False, desired: str = STATE_RUNNING) -> Path:
        root = self.config / name
        root.mkdir(parents=True, exist_ok=True)
        InstanceMeta.create(root, venv="").save()
        registry = self.registry()
        registry.add(root, name=name, restart_on_crash=restart_on_crash)
        registry.update(name, desired=desired)
        self.instances[name] = _FakeInstance(root)
        return root

    def open_instance(self, root: Path) -> _FakeInstance:
        return self.instances[root.name]

    def spawn(self, controller: _FakeInstance) -> int:
        self.spawned.append(controller.root.name)
        controller.running = True
        return controller.pid

    def clock(self) -> float:
        return self.now

    def supervisor(self, **kwargs) -> Supervisor:
        return Supervisor(
            registry=self.registry(),
            open_instance=self.open_instance,
            spawn=self.spawn,
            clock=self.clock,
            **kwargs,
        )


def _backend(kind: str, home: Path, *, runner=None, which: bool = True, workdir: Path | None = None) -> ServiceBackend:
    return ServiceBackend(
        kind=kind,
        home=home,
        workdir=workdir,
        runner=runner if runner is not None else _FakeRunner(),
        which=(lambda name: f"/usr/bin/{name}") if which else (lambda name: None),
        cli_argv=CLI_BIN,
        uid=501,
    )


def _kinds(report) -> list[str]:
    return [event.kind for event in report.events]


async def _test_launchd_render_and_path():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        text = render_unit(BACKEND_LAUNCHD, cli_argv=PYTHON_ARGV, workdir=Path("/tmp/akari"), log_dir=home / "Logs")
        payload = plistlib.loads(text.encode("utf-8"))
        return (
            unit_path(BACKEND_LAUNCHD, home=home) == home / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
            and payload["Label"] == LAUNCHD_LABEL
            and payload["ProgramArguments"] == [*PYTHON_ARGV, "service", "supervise"]
            and payload["RunAtLoad"] is True
            and payload["KeepAlive"] == {"SuccessfulExit": False}
            and payload["ProcessType"] == "Background"
            and payload["WorkingDirectory"] == "/tmp/akari"
            and payload["StandardOutPath"] == str(home / "Logs" / "service.log")
            and payload["StandardErrorPath"] == str(home / "Logs" / "service.err.log")
        )


async def _test_systemd_render_and_path():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        text = render_unit(BACKEND_SYSTEMD, cli_argv=PYTHON_ARGV, workdir=Path("/tmp/akari"), log_dir=home / "Logs")
        quoted = render_unit(BACKEND_SYSTEMD, cli_argv=("/opt/my cli/akaribot",), workdir=None, log_dir=home / "Logs")
        return (
            unit_path(BACKEND_SYSTEMD, home=home) == home / ".config" / "systemd" / "user" / "akaribot.service"
            and f"ExecStart={' '.join(PYTHON_ARGV)} service supervise" in text
            and "Restart=on-failure" in text
            and "RestartSec=5" in text
            and "WantedBy=default.target" in text
            and "After=network-online.target" in text
            and "WorkingDirectory=/tmp/akari" in text
            and 'ExecStart="/opt/my cli/akaribot" service supervise' in quoted
            and "WorkingDirectory=" not in quoted
        )


async def _test_unsupported_platform_reports_hint():
    with TemporaryDirectory() as raw:
        backend = _backend(BACKEND_UNSUPPORTED, Path(raw))
        raised = ""
        try:
            backend.install()
        except ServiceError as error:
            raised = str(error)
        report = backend.status()
        return (
            detect_backend("darwin") == BACKEND_LAUNCHD
            and detect_backend("linux") == BACKEND_SYSTEMD
            and detect_backend("win32") == BACKEND_UNSUPPORTED
            and bool(raised)
            and report.backend == BACKEND_UNSUPPORTED
            and report.installed is False
            and report.enabled is None
            and report.path is None
        )


async def _test_install_writes_unit_and_registers():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner, workdir=home / "work")
        report = backend.install()
        path = home / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
        return (
            report.installed is True
            and report.enabled is True
            and report.path == path
            and path.is_file()
            and plistlib.loads(path.read_bytes())["Label"] == LAUNCHD_LABEL
            and (home / "work").is_dir()
            and runner.calls == [["launchctl", "bootstrap", "gui/501", str(path)]]
        )


async def _test_install_falls_back_to_load():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner({("launchctl", "bootstrap"): 1})
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner)
        report = backend.install()
        path = backend.path()
        return report.enabled is True and runner.calls == [
            ["launchctl", "bootstrap", "gui/501", str(path)],
            ["launchctl", "load", "-w", str(path)],
        ]


async def _test_install_reports_registration_failure():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner({("launchctl",): 113})
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner)
        report = backend.install()
        return report.installed is True and report.enabled is False and bool(report.detail)


async def _test_install_without_tool_skips_registration():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_SYSTEMD, home, runner=runner, which=False)
        report = backend.install()
        return report.installed is True and report.enabled is None and runner.calls == []


async def _test_systemd_install_calls_user_systemctl():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_SYSTEMD, home, runner=runner)
        report = backend.install()
        return report.enabled is True and runner.calls == [
            ["systemctl", "--user", "daemon-reload"],
            ["systemctl", "--user", "enable", "--now", "akaribot.service"],
        ]


async def _test_install_dry_run_writes_nothing():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner)
        report = backend.install(dry_run=True)
        return (
            report.installed is False
            and report.enabled is None
            and not report.path.exists()
            and runner.calls == []
            and LAUNCHD_LABEL in backend.render()
        )


async def _test_install_refuses_existing_without_force():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        backend = _backend(BACKEND_LAUNCHD, home)
        backend.install()
        refused = False
        try:
            backend.install()
        except ServiceError:
            refused = True
        backend.path().write_text("stale", encoding="utf-8")
        forced = backend.install(force=True)
        return refused and forced.installed is True and "stale" not in backend.path().read_text(encoding="utf-8")


async def _test_uninstall_removes_unit():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner)
        backend.install()
        runner.calls.clear()
        report = backend.uninstall()
        return (
            report.installed is False
            and report.enabled is False
            and not backend.path().exists()
            and runner.calls == [["launchctl", "bootout", f"gui/501/{LAUNCHD_LABEL}"]]
        )


async def _test_uninstall_when_absent_is_not_an_error():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner()
        backend = _backend(BACKEND_SYSTEMD, home, runner=runner)
        report = backend.uninstall()
        return report.installed is False and bool(report.detail) and runner.calls == []


async def _test_status_reports_installation_and_registration():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        missing = _backend(BACKEND_LAUNCHD, home, which=False).status()
        runner = _FakeRunner({("launchctl", "print"): 113})
        idle = _backend(BACKEND_LAUNCHD, home, runner=runner).status()
        installed_backend = _backend(BACKEND_LAUNCHD, home, runner=_FakeRunner())
        installed_backend.install()
        report = installed_backend.status()
        return (
            missing.installed is False
            and missing.enabled is None
            and idle.installed is False
            and idle.enabled is False
            and report.installed is True
            and report.enabled is True
            and report.path == installed_backend.path()
            and bool(report.detail)
        )


async def _test_supervise_recovers_once_and_quiets_down():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        rig.add("alpha")
        supervisor = rig.supervisor()
        first = supervisor.run_once()
        second = supervisor.run_once()
        third = supervisor.run_once()
        return (
            first.started == 1
            and _kinds(first) == [KIND_RECOVERED]
            and rig.spawned == ["alpha"]
            and _kinds(second) == [KIND_OBSERVED]
            and _kinds(third) == []
        )


async def _test_supervise_restarts_with_backoff_and_cap():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        rig.add("alpha", restart_on_crash=True)
        supervisor = rig.supervisor(max_restarts=2, backoff=2.0)
        rig.instances["alpha"].running = True
        supervisor.run_once()
        rig.instances["alpha"].running = False
        waiting = supervisor.run_once()
        rig.now += 2.0
        first = supervisor.run_once()
        rig.instances["alpha"].running = False
        too_early = supervisor.run_once()
        rig.now += 4.0
        second = supervisor.run_once()
        rig.instances["alpha"].running = False
        given_up = supervisor.run_once()
        afterwards = supervisor.run_once()
        return (
            _kinds(waiting) == []
            and _kinds(first) == [KIND_RESTARTED]
            and _kinds(too_early) == []
            and _kinds(second) == [KIND_RESTARTED]
            and _kinds(given_up) == [KIND_ABANDONED]
            and _kinds(afterwards) == []
            and rig.spawned == ["alpha", "alpha"]
            and given_up.abandoned == 1
        )


async def _test_supervise_keeps_crashed_instance_without_policy():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        rig.add("alpha", restart_on_crash=False)
        supervisor = rig.supervisor()
        rig.instances["alpha"].running = True
        supervisor.run_once()
        rig.instances["alpha"].running = False
        refused = supervisor.run_once()
        repeated = supervisor.run_once()
        return _kinds(refused) == [KIND_REFUSED] and _kinds(repeated) == [] and rig.spawned == []


async def _test_supervise_skips_missing_and_stray():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        gone = rig.add("gone")
        rig.add("idle", desired=STATE_STOPPED)
        rig.instances["idle"].running = True
        shutil.rmtree(gone)
        report = rig.supervisor().run_once()
        return (
            _kinds(report) == [KIND_MISSING, KIND_STRAY]
            and rig.spawned == []
            and rig.instances["idle"].running is True
            and report.checked == 2
            and report.skipped == 2
        )


async def _test_supervise_reports_spawn_failure():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        rig.add("alpha")

        def _boom(_controller):
            raise ServiceError("no interpreter")

        supervisor = Supervisor(
            registry=rig.registry(),
            open_instance=rig.open_instance,
            spawn=_boom,
            clock=rig.clock,
        )
        report = supervisor.run_once()
        return report.failed == 1 and _kinds(report) == [KIND_FAILED]


async def _test_cli_dry_run_and_status_json():
    with TemporaryDirectory() as raw:
        home = Path(raw)
        runner = _FakeRunner({("launchctl", "print"): 113})
        backend = _backend(BACKEND_LAUNCHD, home, runner=runner)
        with patch("akaribot.cli.commands.service.build_backend", return_value=backend):
            dry = CliRunner().invoke(cli_app, ["service", "install", "--dry-run"])
            dry_calls = [list(call) for call in runner.calls]
            status = CliRunner().invoke(cli_app, ["service", "status", "--json"])
        path = backend.path()
        payload = json.loads(status.stdout.strip().splitlines()[-1])
        return (
            dry.exit_code == 0
            and LAUNCHD_LABEL in dry.stdout
            and "RunAtLoad" in dry.stdout
            and not path.exists()
            and dry_calls == []
            and status.exit_code == 0
            and payload["backend"] == BACKEND_LAUNCHD
            and payload["installed"] is False
            and payload["enabled"] is False
            and payload["path"] == str(path)
        )


async def _test_cli_supervise_once_prints_summary():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        rig.add("alpha")
        captured: dict[str, object] = {}

        def _build(*, max_restarts, backoff):
            captured["max_restarts"] = max_restarts
            captured["backoff"] = backoff
            return rig.supervisor(max_restarts=max_restarts, backoff=backoff)

        with patch("akaribot.cli.commands.service.build_supervisor", side_effect=_build):
            result = CliRunner().invoke(
                cli_app, ["service", "supervise", "--once", "--max-restarts", "3", "--backoff", "1.5"]
            )
        return (
            result.exit_code == 0
            and captured == {"max_restarts": 3, "backoff": 1.5}
            and rig.spawned == ["alpha"]
            and bool(result.stdout.strip())
        )


async def _test_cli_supervise_rejects_bad_options():
    with TemporaryDirectory() as raw:
        rig = _Rig(Path(raw))
        with patch("akaribot.cli.commands.service.build_supervisor", return_value=rig.supervisor()):
            zero = CliRunner().invoke(cli_app, ["service", "supervise", "--once", "--interval", "0"])
            negative = CliRunner().invoke(cli_app, ["service", "supervise", "--once", "--max-restarts=-1"])
        return zero.exit_code != 0 and negative.exit_code != 0


def _invoke_run(args, *, home: Path, root: Path, bot: Path):
    environment = {
        "AKARIBOT_HOME": str(home),
        "AKARIBOT_PYTHON": str(bot),
        "AKARI_INSTANCE_DIR": str(root),
    }
    with patch.dict(os.environ, environment):
        return CliRunner().invoke(cli_app, args)


def _run_fixture(base: Path) -> tuple[Path, Path, Path, InstanceRegistry]:
    root = base / "instance"
    root.mkdir(parents=True, exist_ok=True)
    InstanceMeta.create(root, venv="").save()
    bot = base / "fake_bot.py"
    bot.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    home = base / "home"
    home.mkdir(parents=True, exist_ok=True)
    registry = InstanceRegistry(home / "instances.toml")
    registry.add(root, name="alpha")
    return root, bot, home, registry


async def _test_run_detach_and_stop_sync_desired():
    with TemporaryDirectory() as raw:
        root, bot, home, registry = _run_fixture(Path(raw))
        launched = DetachedRun(pid=4242, log_path=root / "logs" / "RunConsole.log")
        with (
            patch.object(Instance, "spawn_detached", return_value=launched),
            patch.object(Instance, "is_running", return_value=True),
        ):
            started = _invoke_run(["run", "--detach", "--json"], home=home, root=root, bot=bot)
        after_start = registry.get("alpha").desired
        with patch.object(Instance, "stop_running", return_value=StopOutcome(True, "stopped", forced=False)):
            stopped = _invoke_run(["run", "--stop", "--json"], home=home, root=root, bot=bot)
        after_stop = registry.get("alpha").desired
        return (
            started.exit_code == 0
            and stopped.exit_code == 0
            and after_start == STATE_RUNNING
            and after_stop == STATE_STOPPED
        )


async def _test_run_without_registry_entry_skips_silently():
    with TemporaryDirectory() as raw:
        base = Path(raw)
        root = base / "instance"
        root.mkdir(parents=True, exist_ok=True)
        InstanceMeta.create(root, venv="").save()
        bot = base / "fake_bot.py"
        bot.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        home = base / "home"
        home.mkdir(parents=True, exist_ok=True)
        with patch.object(Instance, "stop_running", return_value=StopOutcome(True, "stopped", forced=False)):
            result = _invoke_run(["run", "--stop"], home=home, root=root, bot=bot)
        return result.exit_code == 0 and not (home / "instances.toml").exists()


@func_case
async def test_service(tester: Tester):
    """cli.service: 服务单元渲染、安装卸载、状态与守护循环测试"""
    await tester.test(_test_launchd_render_and_path, "launchd 单元含 Label、ProgramArguments、RunAtLoad 与 KeepAlive")
    await tester.test(_test_systemd_render_and_path, "systemd 单元含 ExecStart、Restart、RestartSec 与 WantedBy")
    await tester.test(_test_unsupported_platform_reports_hint, "其它平台报尚未支持并给出路径提示")
    await tester.test(_test_install_writes_unit_and_registers, "安装落盘并调用注册命令")
    await tester.test(_test_install_falls_back_to_load, "bootstrap 失败时回退 load -w")
    await tester.test(_test_install_reports_registration_failure, "注册命令失败时如实报告未注册")
    await tester.test(_test_install_without_tool_skips_registration, "系统工具缺失时只写单元不注册")
    await tester.test(_test_systemd_install_calls_user_systemctl, "systemd 安装先 daemon-reload 再 enable --now")
    await tester.test(_test_install_dry_run_writes_nothing, "dry-run 不落盘不调用系统工具")
    await tester.test(_test_install_refuses_existing_without_force, "已存在单元文件时要求 --force")
    await tester.test(_test_uninstall_removes_unit, "卸载注销并删除单元文件")
    await tester.test(_test_uninstall_when_absent_is_not_an_error, "卸载未安装的服务不算失败")
    await tester.test(_test_status_reports_installation_and_registration, "状态区分未安装、未注册与已注册")
    await tester.test(_test_supervise_recovers_once_and_quiets_down, "期望运行且未在跑时恢复拉起且不重复刷屏")
    await tester.test(_test_supervise_restarts_with_backoff_and_cap, "崩溃后按退避重启并在上限处放弃")
    await tester.test(_test_supervise_keeps_crashed_instance_without_policy, "未开启崩溃重启时保持不动")
    await tester.test(_test_supervise_skips_missing_and_stray, "目录不存在与期望停止在跑时都跳过")
    await tester.test(_test_supervise_reports_spawn_failure, "拉起失败如实上报且不中断循环")
    await tester.test(_test_cli_dry_run_and_status_json, "service install --dry-run 与 status --json 可用")
    await tester.test(_test_cli_supervise_once_prints_summary, "service supervise --once 透传策略并打印摘要")
    await tester.test(_test_cli_supervise_rejects_bad_options, "非法的间隔与上限被拒绝")
    await tester.test(_test_run_detach_and_stop_sync_desired, "run --detach / --stop 同步注册表 desired")
    await tester.test(_test_run_without_registry_entry_skips_silently, "实例未登记时静默跳过")
    return tester
