"""实例生命周期：后台启动、状态读取与跨进程停止。

固定三条链路：``run --detach`` 启动的进程脱离当前会话并写下进程记录；``run --status`` 从锁与
记录推出状态；``run --stop`` 按记录终止进程——**包括不是本次启动、甚至不是本控制器启动的实例**。
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.instance import Instance, InstanceMeta
from akaribot.cli.main import app
from akaribot.testing import Tester, func_case

# 假实例进程：取锁、写下进程记录、按参数决定是否响应 SIGTERM，然后一直等待。
FAKE_BOT = """#!/usr/bin/env python3
import fcntl, json, os, signal, sys, time

root = os.environ["AKARI_INSTANCE_DIR"]
lock = os.path.join(root, ".bot.lock")
handle = os.fdopen(os.open(lock, os.O_RDWR | os.O_CREAT, 0o644), "r+")
fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0)
handle.write(json.dumps({"pid": os.getpid(), "started_at": "2026-01-01T00:00:00+00:00", "argv": sys.argv[1:]}))
handle.truncate()
handle.flush()
if os.environ.get("FAKE_BOT_IGNORE_TERM") == "1":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
else:
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
while True:
    time.sleep(0.1)
"""


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path, bot: Path) -> Instance:
    # 非托管实例：解释器走 AKARIBOT_PYTHON，测试据此把假实例进程当作解释器启动。
    root.mkdir(parents=True, exist_ok=True)
    Instance.create_dirs(root)
    InstanceMeta.create(root, venv="").save()
    return Instance(root, python_override=bot)


def _fake_bot(root: Path) -> Path:
    bot = root / "fake_bot.py"
    bot.write_text(FAKE_BOT, encoding="utf-8")
    bot.chmod(0o755)
    return bot


def _invoke(args, *, instance_root: Path, bot: Path):
    with patch.dict(os.environ, {"AKARIBOT_PYTHON": str(bot), "AKARI_INSTANCE_DIR": str(instance_root)}):
        return CliRunner().invoke(app, args)


def _status(instance_root: Path, bot: Path) -> dict:
    result = _invoke(["run", "--status", "--json"], instance_root=instance_root, bot=bot)
    return json.loads(result.stdout.strip().splitlines()[-1])


def _wait_lock_held(instance: Instance, timeout: float = 10.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if instance.is_running():
            return True
        time.sleep(0.1)
    return False


def _wait_stopped(instance: Instance, timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not instance.is_running():
            return True
        time.sleep(0.1)
    return False


async def _test_status_reports_stopped_without_lock():
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        _make_instance(root, bot)
        state = _status(root, bot)
        return state["running"] is False and state["pid"] is None


async def _test_detach_records_pid_and_survives_parent():
    # 后台启动后控制器立即返回，进程记录写在锁文件里，界面/终端退出不影响它。
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        instance = _make_instance(root, bot)
        try:
            result = _invoke(["run", "--detach", "--json"], instance_root=root, bot=bot)
            started = json.loads(result.stdout.strip().splitlines()[-1])
            held = _wait_lock_held(instance)
            state = _status(root, bot)
            return (
                result.exit_code == 0
                and started["started"] is True
                and held
                and state["running"] is True
                and state["pid"] == started["pid"]
                and state["started_at"]
            )
        finally:
            _invoke(["run", "--stop", "--timeout", "5"], instance_root=root, bot=bot)


async def _test_stop_takes_over_foreign_process():
    # 关键回归：由别的控制器（另一个 TUI、终端、systemd）启动的实例，新开的界面同样能停。
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        instance = _make_instance(root, bot)
        foreign = subprocess.Popen(  # noqa: S603 - 测试替身，参数固定
            [sys.executable, str(bot)],
            env={**os.environ, "AKARI_INSTANCE_DIR": str(root)},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            if not _wait_lock_held(instance):
                return False
            before = _status(root, bot)
            result = _invoke(["run", "--stop", "--timeout", "10"], instance_root=root, bot=bot)
            return (
                before["running"] is True
                and before["pid"] == foreign.pid
                and result.exit_code == 0
                and _wait_stopped(instance)
                and foreign.poll() is not None
            )
        finally:
            if foreign.poll() is None:
                foreign.kill()
                foreign.wait(timeout=10)


async def _test_stop_force_kills_unresponsive_process():
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        instance = _make_instance(root, bot)
        foreign = subprocess.Popen(  # noqa: S603 - 测试替身，参数固定
            [sys.executable, str(bot)],
            env={**os.environ, "AKARI_INSTANCE_DIR": str(root), "FAKE_BOT_IGNORE_TERM": "1"},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            if not _wait_lock_held(instance):
                return False
            result = _invoke(["run", "--stop", "--timeout", "1", "--json"], instance_root=root, bot=bot)
            outcome = json.loads(result.stdout.strip().splitlines()[-1])
            return outcome["stopped"] is True and outcome["forced"] is True and _wait_stopped(instance)
        finally:
            if foreign.poll() is None:
                foreign.kill()
                foreign.wait(timeout=10)


async def _test_stop_when_idle_is_success():
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        _make_instance(root, bot)
        result = _invoke(["run", "--stop"], instance_root=root, bot=bot)
        return result.exit_code == 0


async def _test_stop_refuses_without_record():
    # 锁被持有但文件里没有进程记录时不能瞎猜进程号，如实报「无法停止」。
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        instance = _make_instance(root, bot)
        lock = instance.lock_path()
        lock.write_text("", encoding="utf-8")
        handle = lock.open("r+")
        try:
            import fcntl

            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = _invoke(["run", "--stop"], instance_root=root, bot=bot)
            return result.exit_code != 0 and instance.is_running()
        finally:
            handle.close()


async def _test_conflicting_actions_rejected():
    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        _make_instance(root, bot)
        both = _invoke(["run", "--detach", "--status"], instance_root=root, bot=bot)
        mixed = _invoke(["run", "--detach", "--foreground"], instance_root=root, bot=bot)
        return both.exit_code != 0 and mixed.exit_code != 0


async def _test_stop_process_primitive_skips_own_group():
    # 与控制器同组的实例只能按进程号发信号：对整组发信号会把控制器自己一起终止。
    from akaribot.cli.process import SystemProcessControl

    control = SystemProcessControl()
    if os.name == "nt":
        return control.process_group(os.getpid()) is None
    sibling = subprocess.Popen(  # noqa: S603 - 测试替身，参数固定
        [sys.executable, "-c", "import time; time.sleep(30)"]
    )
    leader = subprocess.Popen(  # noqa: S603 - 测试替身，参数固定
        [sys.executable, "-c", "import time; time.sleep(30)"],
        start_new_session=True,
    )
    try:
        # 同组但非组长的进程只按进程号处理；自建会话的组长可以整组处理。
        return control.process_group(sibling.pid) is None and control.process_group(leader.pid) == leader.pid
    finally:
        for process in (sibling, leader):
            process.kill()
            process.wait(timeout=10)


async def _test_tui_source_takes_over_foreign_process():
    # 界面侧的同一条链路：状态与停止都走 CLI，因此新开的界面能接管别的控制器启动的实例。
    from akaribot.cli.tui.run import SubprocessRunSource

    with TemporaryDirectory(prefix="akari-life-") as raw:
        root = Path(raw) / "instance"
        bot = _fake_bot(Path(raw))
        instance = _make_instance(root, bot)
        foreign = subprocess.Popen(  # noqa: S603 - 测试替身，参数固定
            [sys.executable, str(bot)],
            env={**os.environ, "AKARI_INSTANCE_DIR": str(root)},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            if not _wait_lock_held(instance):
                return False
            with patch.dict(os.environ, {"AKARIBOT_PYTHON": str(bot)}):
                source = SubprocessRunSource(root=root, timeout=60.0, stop_timeout=10.0)
                records = source.status()
                running = [record for record in records if record.running]
                stopped = source.stop()
                idle = source.status()
            return (
                len(running) == 1
                and running[0].pid == foreign.pid
                and running[0].origin == i18n.t("cli.tui.run.origin_cli")
                and stopped.ok
                and _wait_stopped(instance)
                and not any(record.running for record in idle)
            )
        finally:
            if foreign.poll() is None:
                foreign.kill()
                foreign.wait(timeout=10)


async def _test_run_page_renders_cli_state():
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.run import STATE_RUNNING, ProcessRecord, StaticRunSource

    source = StaticRunSource(
        [ProcessRecord(pid=4321, state=STATE_RUNNING, origin=i18n.t("cli.tui.run.origin_cli"), detail="recorded")]
    )
    app = TuiApp(sources={"run": source}, initial_page="run")
    async with compat.app_test(app, size=(110, 32)) as pilot:
        page = app.query_one("#page-run")
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        table = page.table_text
        running = page.running
        page.request_stop()
        await pilot.pause()
        asked = (source.calls["stop"], page.status_text)
        page.request_stop()
        await page.wait_for_idle()
        await pilot.pause()
        calls = dict(source.calls)
        await pilot.press("q")
    return (
        "4321" in table
        and running
        and asked == (0, i18n.t("cli.tui.run.confirm_stop", hotkey="x"))
        and calls["stop"] == 1
    )


def _running_source():
    from akaribot.cli.tui.run import STATE_RUNNING, ProcessRecord, StaticRunSource

    return StaticRunSource(
        [ProcessRecord(pid=4321, state=STATE_RUNNING, origin=i18n.t("cli.tui.run.origin_cli"), detail="recorded")]
    )


async def _with_run_page(body, source=None, size=(110, 32)):
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.app import TuiApp
    from akaribot.cli.tui.run import StaticRunSource

    chosen = source if source is not None else StaticRunSource()
    app = TuiApp(sources={"run": chosen}, initial_page="run")
    async with compat.app_test(app, size=size) as pilot:
        page = app.query_one("#page-run")
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _test_pending_confirm_gate():
    # 闸门本身：注入时钟，第一次记下、防抖窗口内忽略、过后放行、超时作废且不误放行。
    from akaribot.cli.tui import _compat as compat

    gate = compat.PendingConfirm()
    first = gate.arm("x", now=100.0)
    debounced = gate.arm("x", now=100.1)
    accepted = gate.arm("x", now=101.0)
    other = gate.arm("y", now=200.0)
    expired = gate.arm("y", now=220.0)
    return first is False and debounced is False and accepted is True and other is False and expired is False


async def _test_show_page_resets_confirmation():
    # 切页会作废待确认：回到运行页后第一次按键只重新询问。
    source = _running_source()

    async def body(app, page, pilot, source):
        page.request_stop()
        await pilot.pause()
        app.show_page("misc")
        await pilot.pause()
        app.show_page("run")
        await pilot.pause()
        page.request_stop()
        await pilot.pause()
        after_return = source.calls["stop"]
        page.request_stop()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return after_return, source.calls["stop"]

    after_return, executed = await _with_run_page(body, source)
    return after_return == 0 and executed == 1


async def _test_refresh_invalidates_confirmation():
    # 手动刷新（r 与刷新按钮）后状态可能已变，待确认作废，需要重新按两次。
    source = _running_source()

    async def body(app, page, pilot, source):
        page.request_stop()
        await pilot.pause()
        page.action_refresh()
        await page.wait_for_idle()
        await pilot.pause()
        page.request_stop()
        await pilot.pause()
        after_refresh = source.calls["stop"]
        page.request_stop()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return after_refresh, source.calls["stop"]

    after_refresh, executed = await _with_run_page(body, source)
    return after_refresh == 0 and executed == 1


async def _test_poll_keeps_confirmation():
    # 轮询不作废待确认：等待期间状态栏仍显示那句提示，第二次按键直接执行。
    source = _running_source()

    async def body(app, page, pilot, source):
        page.request_stop()
        await pilot.pause()
        page._on_tick()
        await page.wait_for_idle()
        await pilot.pause()
        asked = page.status_text
        page.request_stop()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, source.calls["stop"]

    asked, executed = await _with_run_page(body, source)
    expected = i18n.t("cli.tui.run.confirm_stop", hotkey="x")
    return asked == expected and executed == 1


async def _test_adapter_start_collects_platform():
    # `a` 先弹输入框收平台，随后仍要确认一次；执行时把平台交给数据源。
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.run import StaticRunSource

    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        app.screen.query_one("#prompt-input", compat.Input).value = "telegram"
        await pilot.press("enter")
        await pilot.pause()
        asked = (source.calls["start"], page.status_text)
        await pilot.press("a")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, asked, source.calls["start"], list(source.adapters)

    opened, asked, starts, adapters = await _with_run_page(body, StaticRunSource())
    expected = i18n.t("cli.tui.run.confirm_start_adapter", platform="telegram", hotkey="a")
    return opened and asked == (0, expected) and starts == 1 and adapters == ["telegram"]


async def _test_foreground_only_prints_command():
    # `--foreground` 会占住终端，界面只给命令与说明，绝不代为执行。
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.run import StaticRunSource

    async def body(app, page, pilot, source):
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "telegram"
        await pilot.press("enter")
        await pilot.pause()
        with mock.patch.object(compat, "notify") as notify:
            page.action_foreground()
            await pilot.pause()
            message = notify.call_args.args[1] if notify.call_args else ""
        hint = (message, page.status_text, dict(source.calls))
        await pilot.press("q")
        return hint

    (message, status, calls) = await _with_run_page(body, StaticRunSource())
    command = "akaribot run --foreground --adapter telegram"
    return (
        message == i18n.t("cli.tui.run.foreground_hint", command=command)
        and status
        and calls["start"] == 0
        and calls["restart"] == 0
    )


async def _test_subprocess_start_passes_adapter():
    # 只启动指定适配器时，argv 里必须带上 `--adapter <平台>`。
    from akaribot.cli.tui.run import SubprocessRunSource

    seen: list[list[str]] = []

    def runner(argv, **kwargs):
        seen.append([str(item) for item in argv])
        payload = json.dumps({"started": True, "pid": 7, "log": "/tmp/run.log"})
        return subprocess.CompletedProcess(argv, 0, stdout=payload, stderr="")

    with TemporaryDirectory(prefix="akari-run-") as raw:
        source = SubprocessRunSource(root=Path(raw), runner=runner)
        result = source.start(adapter="telegram")
    argv = seen[0] if seen else []
    return result.ok and "--detach" in argv and "--adapter" in argv and argv[argv.index("--adapter") + 1] == "telegram"


async def _test_low_frequency_bindings_stay_out_of_footer():
    # 操作行上都有按钮的动作不进页脚，80 列下才能容纳全局键位。
    from akaribot.cli.tui import _compat as compat
    from akaribot.cli.tui.run import RunPage

    async def body(app, page, pilot, source):
        footer = app.query_one(compat.Footer)
        actions = {"start", "stop", "restart", "adapter_start", "foreground", "refresh"}
        keys = [child for child in footer.children if getattr(child, "action", "") in actions]
        width = sum(compat.widget_cells(child)[0] for child in keys)
        await pilot.press("q")
        return len(keys), width

    count, width = await _with_run_page(body, size=(80, 24))
    visible = tuple(binding.key for binding in RunPage.BINDINGS if binding.show)
    hidden = tuple(binding.key for binding in RunPage.BINDINGS if not binding.show)
    return count == 3 and width <= 80 and visible == ("s", "x", "r") and hidden == ("ctrl+r", "a", "f")


@func_case
async def test_run_lifecycle(tester: Tester):
    """cli.run: 实例生命周期（后台启动、状态、跨进程停止）测试"""
    from akaribot.cli.tui import _compat as compat

    _use_cli_locale()
    if os.name == "nt":
        # 假实例进程依赖 fcntl 取锁，Windows 上跳过；生产代码的 Windows 分支另行实机验证。
        return tester
    await tester.test(_test_status_reports_stopped_without_lock, "未运行时状态为空")
    await tester.test(_test_detach_records_pid_and_survives_parent, "后台启动写下进程记录并可被读到")
    await tester.test(_test_stop_takes_over_foreign_process, "能停止由别的控制器启动的实例")
    await tester.test(_test_stop_force_kills_unresponsive_process, "不响应信号的实例被强制终止")
    await tester.test(_test_stop_when_idle_is_success, "未运行时停止视为成功")
    await tester.test(_test_stop_refuses_without_record, "没有进程记录时拒绝停止")
    await tester.test(_test_conflicting_actions_rejected, "互斥动作被拒绝")
    await tester.test(_test_stop_process_primitive_skips_own_group, "同组进程不按进程组处理")
    await tester.test(_test_tui_source_takes_over_foreign_process, "界面数据源接管别的控制器启动的实例")
    await tester.test(_test_subprocess_start_passes_adapter, "只启动指定适配器时 argv 带 --adapter")
    await tester.test(_test_pending_confirm_gate, "确认闸门的防抖与超时")
    # 用例里的两次按键几乎同时发生，压缩防抖窗口，免得每条确认都等 0.4 秒。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_run_page_renders_cli_state, "运行页展示 CLI 记录并需两次确认才停止")
        await tester.test(_test_show_page_resets_confirmation, "切页作废待确认")
        await tester.test(_test_refresh_invalidates_confirmation, "手动刷新作废待确认")
        await tester.test(_test_poll_keeps_confirmation, "轮询不作废待确认")
        await tester.test(_test_adapter_start_collects_platform, "只启动指定适配器")
        await tester.test(_test_foreground_only_prints_command, "前台运行只给命令不代为执行")
        await tester.test(_test_low_frequency_bindings_stay_out_of_footer, "低频键位不进页脚")
    return tester
