"""CLI 侧包变更通知：结果解析与卸载顺序。

``Instance.notify_package_change`` 只解析 core 入口回传的 JSON，不 import core；本文件把子进程
结果替换成固定的 ``CompletedProcess``，在不启动真实实例的前提下断言「未运行 / 投递失败 / 远端
拒绝 / 超时」的分支、卸载阻塞判定，以及 ``module remove`` 在热拆卸未确认时不得执行 uv uninstall。
"""

import contextlib
import io
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import typer

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import module as module_command
from akaribot.cli.instance import CliError, Instance, _parse_notify_payload
from akaribot.testing import Tester, func_case

DIST = "akari-bot-module-dice"


def _use_cli_locale() -> None:
    """把语言快照切回 CLI 命名空间。

    测试框架在每个用例前重跑 ``load_modules()``，它会把当前快照连到 core 的命名空间；而 CLI 的
    ``Locale`` 按当前快照取键，不切回来就只会拿到键名。生产里 CLI 进程不加载 core，无此问题。
    """
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path) -> Instance:
    """建一个只带元数据文件的最小实例。"""
    (root / "akaribot.toml").write_text("", encoding="utf-8")
    return Instance(root)


def _stub_result(instance: Instance, payload: dict | None, *, returncode: int, stderr: str = "") -> None:
    """把实例的子进程调用替换成固定结果；``payload`` 为 ``None`` 时不回传 JSON。"""
    stdout = "" if payload is None else json.dumps(payload, ensure_ascii=False) + "\n"

    def run_core_capture(entrypoint: str, *args: str, timeout: float | None = 120.0, **env: str):
        return subprocess.CompletedProcess([entrypoint, *args], returncode, stdout, stderr)

    instance.is_running = lambda: True
    instance.run_core_capture = run_core_capture


def _notify(instance: Instance, payload: dict | None, *, returncode: int, stderr: str = ""):
    _stub_result(instance, payload, returncode=returncode, stderr=stderr)
    return instance.notify_package_change("install", DIST)


async def _test_delivered_confirms_and_unblocks():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        result = _notify(
            instance,
            {"ok": True, "status": "delivered", "remote": "server.post_package_install", "result": True, "detail": ""},
            returncode=0,
        )
    return (
        result.attempted
        and result.delivered
        and result.status == "delivered"
        and not result.blocks_uninstall
        and "server.post_package_install" in result.detail
    )


async def _test_rejected_surfaces_reason_and_blocks():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        result = _notify(
            instance,
            {
                "ok": False,
                "status": "rejected",
                "remote": "server.post_package_remove",
                "result": False,
                "detail": "包未注册，或另有热重载正在进行。",
            },
            returncode=4,
        )
    # 旧实现只看 returncode，既给不出「远端拒绝」的状态，也丢掉了 core 给出的具体原因。
    return (
        result.attempted
        and not result.delivered
        and result.status == "rejected"
        and result.blocks_uninstall
        and "包未注册" in result.detail
    )


async def _test_remote_not_running_blocks_uninstall():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        result = _notify(
            instance,
            {
                "ok": False,
                "status": "not_running",
                "remote": "server.post_package_remove",
                "result": None,
                "detail": "实例未运行：JobQueue 注册表里没有在线的 Server 实例",
            },
            returncode=3,
        )
    return result.status == "not_running" and result.blocks_uninstall and "没有在线的 Server" in result.detail


async def _test_timeout_is_not_silently_ok():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        result = _notify(
            instance,
            {
                "ok": False,
                "status": "timeout",
                "remote": "server.post_package_remove",
                "result": None,
                "detail": "已投递，但 300 秒内未收到实例确认",
            },
            returncode=5,
        )
    return result.status == "timeout" and result.blocks_uninstall and "结果未知" in result.detail


async def _test_missing_entrypoint_keeps_reason():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        result = _notify(
            instance,
            None,
            returncode=1,
            stderr="No module named 'akaribot.core.entrypoints.rpc'\n",
        )
    return (
        result.attempted
        and not result.delivered
        and result.status == "error"
        and result.blocks_uninstall
        and "akaribot.core.entrypoints" in result.detail
    )


async def _test_instance_not_running_does_not_block():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        instance.is_running = lambda: False
        result = instance.notify_package_change("remove", DIST)
    # 实例确实没在跑时没有可拆卸的对象，卸载必须继续而不是被自己的保护条件挡住。
    return not result.attempted and not result.delivered and result.status == "" and not result.blocks_uninstall


async def _test_unknown_action_raises():
    with TemporaryDirectory(prefix="akari-cli-notify-") as directory:
        instance = _make_instance(Path(directory))
        try:
            instance.notify_package_change("frobnicate", DIST)
        except CliError:
            return True
        return False


async def _test_payload_parser_tolerates_noise():
    noisy = "warning: something\n" + json.dumps({"status": "delivered", "detail": "ok"}) + "\n"
    return (
        _parse_notify_payload(noisy) == {"status": "delivered", "detail": "ok"}
        and _parse_notify_payload("") is None
        and _parse_notify_payload("not json at all") is None
        and _parse_notify_payload('{"no_status": 1}') is None
    )


class _RecordingRunner:
    """替身：记录 argv，不真的执行 uv。"""

    calls: list[list[str]]

    def __init__(self, dry_run: bool = False, verbose: bool = False) -> None:
        self.calls = []

    def run(self, argv: Any, *, env: Any = None) -> subprocess.CompletedProcess[str]:
        self.calls.append(list(argv))
        return subprocess.CompletedProcess(list(argv), 0, "", "")

    def run_checked(self, argv: Any, *, what: str, env: Any = None) -> None:
        self.run(argv, env=env)


def _registry_payload(kind: str = "module") -> dict:
    return {
        "packages": [
            {
                "dist": DIST,
                "name": "dice",
                "kind": kind,
                "version": "0.1.0",
                "import_path": "akaribot.modules.dice",
                "provides_modules": ["dice"],
            }
        ]
    }


def _remove_with_notify(notify: dict, returncode: int) -> tuple[int | None, list[list[str]], str]:
    """跑一次 ``module remove``，返回退出码、卸载 argv 与输出文本。"""
    runner = _RecordingRunner()
    previous_runner = engine.CommandRunner
    previous_resolver = module_command.require_instance
    engine.CommandRunner = lambda **kwargs: runner  # type: ignore[assignment]
    out, err = io.StringIO(), io.StringIO()
    code: int | None = None
    try:
        with TemporaryDirectory(prefix="akari-cli-remove-") as directory:
            root = Path(directory)
            instance = _make_instance(root)
            # remove() 自己解析实例，故连解析器一起替换，才能把子进程结果与运行状态都固定下来。
            instance.is_running = lambda: True
            instance.run_core_capture = lambda entrypoint, *args, timeout=120.0, **env: subprocess.CompletedProcess(
                [entrypoint, *args],
                0 if entrypoint == "registry" else returncode,
                json.dumps(_registry_payload()) + "\n" if entrypoint == "registry" else json.dumps(notify) + "\n",
                "",
            )
            module_command.require_instance = lambda *args, **kwargs: instance
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    module_command.remove(DIST, instance=root)
                except typer.Exit as exc:
                    code = exc.exit_code
    finally:
        engine.CommandRunner = previous_runner  # type: ignore[assignment]
        module_command.require_instance = previous_resolver  # type: ignore[assignment]
    return code, runner.calls, out.getvalue() + err.getvalue()


async def _test_remove_aborts_before_uninstall_when_detach_unconfirmed():
    code, calls, text = _remove_with_notify(
        {
            "ok": False,
            "status": "rejected",
            "remote": "server.post_package_remove",
            "result": False,
            "detail": "包未注册，或另有热重载正在进行。",
        },
        4,
    )
    return code == 1 and calls == [] and DIST in text and "包未注册" in text


async def _test_remove_uninstalls_after_confirmed_detach():
    code, calls, _ = _remove_with_notify(
        {"ok": True, "status": "delivered", "remote": "server.post_package_remove", "result": True, "detail": ""},
        0,
    )
    return code is None and len(calls) == 1 and DIST in calls[0] and "uninstall" in calls[0]


class _Catalog:
    """替身 registry：固定给出一个更高版本，使 update 一定有更新计划。"""

    def latest(self, dist: str) -> str:
        return "0.2.0"


def _update_with_notify(
    detach: tuple[dict, int], install: tuple[dict, int], *, kind: str = "module"
) -> tuple[list[str], dict, list[list[str]]]:
    """跑一次 ``module update``，返回 RPC 契约调用顺序、结果载荷与执行过的 argv。"""
    runner = _RecordingRunner()
    remotes: list[str] = []
    previous = (
        engine.CommandRunner,
        engine.config_sync,
        engine.db_upgrade,
        module_command.require_instance,
        module_command._load_catalog,
    )
    engine.CommandRunner = lambda **kwargs: runner  # type: ignore[assignment]
    engine.config_sync = lambda *args, **kwargs: None  # type: ignore[assignment]
    engine.db_upgrade = lambda *args, **kwargs: None  # type: ignore[assignment]
    module_command._load_catalog = lambda *args, **kwargs: _Catalog()  # type: ignore[assignment]
    out, err = io.StringIO(), io.StringIO()
    try:
        with TemporaryDirectory(prefix="akari-cli-update-") as directory:
            root = Path(directory)
            instance = _make_instance(root)
            instance.is_running = lambda: True

            def run_core_capture(entrypoint: str, *args: str, timeout: float | None = 120.0, **env: str):
                if entrypoint == "registry":
                    return subprocess.CompletedProcess(
                        [entrypoint, *args], 0, json.dumps(_registry_payload(kind)) + "\n", ""
                    )
                remotes.append(args[0])
                payload, returncode = detach if args[0].endswith("post_package_remove") else install
                return subprocess.CompletedProcess([entrypoint, *args], returncode, json.dumps(payload) + "\n", "")

            instance.run_core_capture = run_core_capture
            module_command.require_instance = lambda *args, **kwargs: instance
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                _, payload = module_command._perform_update(
                    None,
                    [DIST],
                    all_packages=False,
                    offline=False,
                    force=False,
                    assume_yes=True,
                    dry_run=False,
                    verbose=False,
                    json_mode=False,
                )
    finally:
        (
            engine.CommandRunner,
            engine.config_sync,
            engine.db_upgrade,
            module_command.require_instance,
            module_command._load_catalog,
        ) = previous
    return remotes, payload, runner.calls


def _notify_payload(status: str, remote: str) -> tuple[dict, int]:
    codes = {"delivered": 0, "rejected": 4, "not_running": 3, "timeout": 5}
    return (
        {
            "ok": status == "delivered",
            "status": status,
            "remote": remote,
            "result": status == "delivered",
            "detail": "实例拒绝本次变更：包未注册，或另有热重载正在进行。" if status == "rejected" else "",
        },
        codes[status],
    )


async def _test_update_detaches_before_reloading():
    remotes, payload, argv = _update_with_notify(
        _notify_payload("delivered", "server.post_package_remove"),
        _notify_payload("delivered", "server.post_package_install"),
    )
    # 先热拆卸旧代际再热装载，否则服务端会以「包已注册」拒绝，更新永远落不到运行态。
    return (
        remotes == ["server.post_package_remove", "server.post_package_install"]
        and payload["updated"] == [DIST]
        and payload["restart_required"] is False
        and argv
    )


async def _test_update_skips_reload_when_detach_unconfirmed():
    remotes, payload, _ = _update_with_notify(
        _notify_payload("rejected", "server.post_package_remove"),
        _notify_payload("delivered", "server.post_package_install"),
    )
    # 旧代际没拆掉就不必再投递热装载（必被拒），但要把「需要重启」如实写进结果。
    return (
        remotes == ["server.post_package_remove"]
        and payload["updated"] == [DIST]
        and payload["reload_pending"] == [DIST]
        and payload["restart_required"] is True
    )


async def _test_update_does_not_detach_adapters():
    remotes, payload, _ = _update_with_notify(
        _notify_payload("delivered", "server.post_package_remove"),
        _notify_payload("delivered", "server.post_package_install"),
        kind="adapter",
    )
    # 适配器不支持整包热换，沿用「装好后提示重启」的既有语义，不投递拆卸。
    return remotes == ["server.post_package_install"] and payload["restart_required"] is False


@func_case
async def test_cli_notify(tester: Tester):
    """包变更通知的结果解析与卸载顺序。"""
    _use_cli_locale()
    await tester.test(_test_delivered_confirms_and_unblocks, "实例确认后视为已送达，不阻塞卸载")
    await tester.test(_test_rejected_surfaces_reason_and_blocks, "远端拒绝时保留原因并阻塞卸载")
    await tester.test(_test_remote_not_running_blocks_uninstall, "实例在跑但 Server 缺席时阻塞卸载")
    await tester.test(_test_timeout_is_not_silently_ok, "超时按结果未知处理，不当作成功")
    await tester.test(_test_missing_entrypoint_keeps_reason, "入口缺失时给出真实原因，安装侧仍只告警")
    await tester.test(_test_instance_not_running_does_not_block, "实例未运行时不阻塞卸载")
    await tester.test(_test_unknown_action_raises, "未知动作直接报错")
    await tester.test(_test_payload_parser_tolerates_noise, "结果解析容忍 stdout 噪声")
    await tester.test(
        _test_remove_aborts_before_uninstall_when_detach_unconfirmed, "热拆卸未确认时不得执行 uv uninstall"
    )
    await tester.test(_test_remove_uninstalls_after_confirmed_detach, "热拆卸确认后才执行 uv uninstall")
    await tester.test(_test_update_detaches_before_reloading, "更新先热拆卸旧代际再热装载")
    await tester.test(_test_update_skips_reload_when_detach_unconfirmed, "热拆卸未确认时跳过热装载并标记需重启")
    await tester.test(_test_update_does_not_detach_adapters, "适配器更新不投递热拆卸")
    return tester
