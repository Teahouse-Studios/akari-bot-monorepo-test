"""概览页：实例信息与运行状态。

环境信息与环境动作已移到「环境」页、旧项目迁移移到「杂项」页，本页只留实例本身：根目录、名称、
语言、core 版本与来源、运行状态与判据、更新提示，以及实例清单与服务行的动作。切换实例立即生效，
缺省项经 `instance use` 子进程异步写回并以通知报出结论；移除登记与装卸服务都经模态确认框。
"""

import threading
import asyncio
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import context
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dashboard import (
    CLI_WRITE_TIMEOUT_SECONDS,
    INIT_TIMEOUT_SECONDS,
    DashboardPage,
    DashboardSnapshot,
    InstanceRow,
    ServiceRow,
    StaticDashboardSource,
    StaticInitRunner,
    StaticInstanceListSource,
    StaticServiceControl,
    SubprocessCliRunner,
    SubprocessInitRunner,
)
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case

SNAPSHOT = DashboardSnapshot(
    instance_root="/tmp/fake-instance",
    instance_name="demo",
    instance_mode="installed",
    locale="zh_cn",
    core_version="0.1.0",
    core_origin="akaribot.toml",
    running=True,
    running_detail="锁文件被持有：/tmp/fake-instance/.bot.lock",
    update_hint="",
)

FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "dashboard.json"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _instance_rows() -> tuple[InstanceRow, ...]:
    return (
        InstanceRow(name="alpha", root=Path("/tmp/alpha"), running=True, autostart=True),
        InstanceRow(name="beta", root=Path("/tmp/beta"), running=False, restart_on_crash=True),
    )


async def _wait_until(predicate, timeout: float = 1.0) -> bool:
    # 后台 worker 的落地时刻不确定，用轮询等条件成立，避免用固定 sleep 拖慢或漏判。
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


# 记录写动作下发的 argv，供断言核对；on_run 用于卡住第一条命令观察忙状态。
class _RecordingRunner:
    def __init__(self, result: OperationResult | None = None, on_run=None) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.labels: list[str] = []
        self._result = result
        self._on_run = on_run

    def run(self, args, label: str = "") -> OperationResult:
        self.calls.append(tuple(args))
        self.labels.append(label)
        if self._on_run is not None:
            self._on_run(args)
        return self._result or OperationResult(True, i18n.t("cli.tui.dashboard.cli_stub_ok"), "stub")


class _ChangingListSource(StaticInstanceListSource):
    # 第二次取数把首条实例的运行状态翻面：轮询改了内容，待确认状态却该保留。
    def list_instances(self) -> tuple[InstanceRow, ...]:
        rows = list(super().list_instances())
        if self.calls["list"] > 1 and rows:
            first = rows[0]
            rows[0] = InstanceRow(
                name=first.name,
                root=first.root,
                locale=first.locale,
                running=not first.running,
                autostart=first.autostart,
                restart_on_crash=first.restart_on_crash,
                registered=first.registered,
            )
        return tuple(rows)


def _temp_instances(raw: str, *names: str) -> dict[str, Path]:
    # 切换要求目标目录里有 akaribot.toml，临时造几个可切换的实例。
    roots: dict[str, Path] = {}
    for name in names:
        root = Path(raw) / name
        root.mkdir()
        (root / "akaribot.toml").write_text(f"[instance]\nname = '{name}'\n", encoding="utf-8")
        roots[name] = root
    return roots


async def _pick_choice(app, pilot, index: int) -> None:
    # 直接触发按钮：选项文案可能长到把按钮撑出屏幕，坐标点击会落空。
    app.screen.query_one(f"#choice-{index}", compat.Button).press()
    await pilot.pause()


async def _pick_cancel(app, pilot) -> None:
    app.screen.query_one("#choice-cancel", compat.Button).press()
    await pilot.pause()


async def _with_page(body, source=None, size=(110, 32), instances=None, service=None, boot_note="", cli=None):
    chosen = source if source is not None else StaticDashboardSource(SNAPSHOT, running=True)
    listed = instances if instances is not None else StaticInstanceListSource(_instance_rows())
    control = service if service is not None else StaticServiceControl()
    app = TuiApp(
        sources={"dashboard": chosen, "dashboard_instances": listed, "dashboard_service": control},
        initial_page="dashboard",
        boot_started_at=time.monotonic(),
        boot_note=boot_note,
    )
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("dashboard")
        if cli is not None:
            page.cli_runner = cli
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen, listed, control)


def _fields(page) -> dict[str, str]:
    return dict(page.rows)


async def _test_fields_show_instance_facts():
    async def body(app, page, pilot, source, listed, control):
        rows = _fields(page)
        await pilot.press("q")
        return rows

    rows = await _with_page(body)
    return (
        rows[i18n.t("cli.tui.dashboard.field_instance_root")] == "/tmp/fake-instance"
        and rows[i18n.t("cli.tui.dashboard.field_instance_name")] == "demo"
        and rows[i18n.t("cli.tui.dashboard.field_core_version")] == "0.1.0"
        and rows[i18n.t("cli.tui.dashboard.field_core_origin")] == "akaribot.toml"
        and i18n.t("cli.tui.common.unknown") not in rows.values()
    )


async def _test_state_follows_probe():
    # 运行状态由锁文件探测决定，行文本带状态标记。
    async def body(app, page, pilot, source, listed, control):
        running = _fields(page)[i18n.t("cli.tui.dashboard.field_state")]
        source.set_running(False)
        page.refresh_running()
        await pilot.pause()
        stopped = _fields(page)[i18n.t("cli.tui.dashboard.field_state")]
        await pilot.press("q")
        return running, stopped

    running, stopped = await _with_page(body)
    return running.startswith("●") and stopped.startswith("○") and running != stopped


async def _test_refresh_rereads_snapshot():
    async def body(app, page, pilot, source, listed, control):
        before = source.calls["snapshot"]
        page.refresh_snapshot(force=True)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return before, source.calls["snapshot"]

    before, after = await _with_page(body)
    return after > before


async def _test_load_failure_degrades_to_status():
    class Failing:
        """快照读取必定失败的数据源，用于断言降级行为。"""

        calls = {"snapshot": 0, "probe": 0}

        def snapshot(self):
            self.calls["snapshot"] += 1
            raise RuntimeError("boom")

        def probe_running(self):
            return None

    async def body(app, page, pilot, source, listed, control):
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body, Failing())
    return "boom" in status


async def _test_instance_list_marks_state_and_policy():
    # 清单每行给运行状态与策略标记，未登记的当前实例也要出现，否则看不到自己在管哪个。
    async def body(app, page, pilot, source, listed, control):
        context.set_active_root("/tmp/alpha")
        page.refresh_instances()
        await pilot.pause()
        rows = page.instance_rows
        await pilot.press("q")
        return rows

    rows = await _with_page(body)
    return (
        [row.name for row in rows] == ["alpha", "beta"]
        and rows[0].autostart
        and rows[1].restart_on_crash
        and rows[0].state_label.startswith("●")
        and rows[1].state_label.startswith("○")
    )


async def _test_enter_switches_instance():
    # 在清单里选中一条即切换当前实例：上下文与所有页面的下一次取数都指向它。
    runner = _RecordingRunner()
    with TemporaryDirectory(prefix="akari-switch-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            await page.wait_for_idle()
            await pilot.pause()
            active = context.active_root()
            status = page.status_text
            await pilot.press("q")
            return active, status, chosen

        active, status, _ = await _with_page(body, instances=listed, cli=runner)
        # 上下文里的根按真实路径保存：macOS 的临时目录本身是软链接。
        expected = roots["beta"].resolve()
    return active == expected and status and list(runner.calls) == [("instance", "use", "beta")]


async def _test_switch_sends_default_write():
    # 切换把缺省项经 `instance use` 交给命令层，状态栏写明已下发；结论另经通知报出。
    runner = _RecordingRunner()
    with TemporaryDirectory(prefix="akari-default-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            status = page.status_text
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return status

        status = await _with_page(body, instances=listed, cli=runner)
    separator = i18n.t("cli.tui.common.error_separator")
    expected = f"{i18n.t('cli.tui.dashboard.switch_done', name='beta')}{separator}"
    expected = f"{expected}{i18n.t('cli.tui.dashboard.use_calling', name='beta')}"
    return list(runner.calls) == [("instance", "use", "beta")] and status == expected


async def _test_switch_does_not_wait_for_cli():
    # 切换立即生效：子进程还卡着时上下文已改，同一目标不重复下发，忙标志也没有被占。
    gate = threading.Event()
    runner = _RecordingRunner(on_run=lambda _args: gate.wait(2.0))
    with TemporaryDirectory(prefix="akari-async-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            switched = context.active_root()
            page.switch_to_selected()
            status = page.status_text
            busy = page._busy
            started = await _wait_until(lambda: list(runner.calls))
            while_blocked = list(runner.calls)
            gate.set()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return switched, status, busy, started, while_blocked

        switched, status, busy, started, while_blocked = await _with_page(body, instances=listed, cli=runner)
        expected_active = roots["beta"].resolve()
    separator = i18n.t("cli.tui.common.error_separator")
    expected_status = f"{i18n.t('cli.tui.dashboard.switch_done', name='beta')}{separator}"
    expected_status = f"{expected_status}{i18n.t('cli.tui.dashboard.use_calling', name='beta')}"
    return (
        switched == expected_active
        and status == expected_status
        and busy is False
        and started
        and while_blocked == [("instance", "use", "beta")]
    )


async def _test_switch_default_rewrites_after_return():
    # 切到别的实例后记录随之更新，再切回来仍要写一次缺省项。
    runner = _RecordingRunner()
    with TemporaryDirectory(prefix="akari-back-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            for index in (1, 0, 1):
                # 每次切换都会重挂载本页，新一轮要重新注入替身执行器并重新取页面。
                current = app.page("dashboard")
                current.cli_runner = runner
                current.query_one("#instance-list", compat.ListView).index = index
                await pilot.pause()
                current.switch_to_selected()
                await current.wait_for_idle()
                await pilot.pause()
            await pilot.press("q")
            return list(runner.calls)

        calls = await _with_page(body, instances=listed, cli=runner)
    return calls == [
        ("instance", "use", "beta"),
        ("instance", "use", "alpha"),
        ("instance", "use", "beta"),
    ]


async def _test_switch_skips_default_for_unregistered():
    runner = _RecordingRunner()
    with TemporaryDirectory(prefix="akari-plain-") as raw:
        plain = Path(raw) / "plain"
        plain.mkdir()
        (plain / "akaribot.toml").write_text("[instance]\nname = 'plain'\n", encoding="utf-8")
        listed = StaticInstanceListSource((InstanceRow(name="", root=plain, running=False, registered=False),))

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 0
            await pilot.pause()
            page.switch_to_selected()
            await page.wait_for_idle()
            await pilot.pause()
            status = page.status_text
            await pilot.press("q")
            return status

        status = await _with_page(body, instances=listed, cli=runner)
    separator = i18n.t("cli.tui.common.error_separator")
    expected = f"{i18n.t('cli.tui.dashboard.switch_done', name=str(plain))}{separator}"
    expected = f"{expected}{i18n.t('cli.tui.dashboard.switch_default_skipped')}"
    return list(runner.calls) == [] and status == expected


async def _test_switch_default_result_is_notified():
    # 写回结论经应用级通知报出：本页随切换重挂载后仍看得见。
    runner = _RecordingRunner()
    label = i18n.t("cli.tui.dashboard.use_label", name="beta")
    with TemporaryDirectory(prefix="akari-notify-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")

        seen: list[tuple[str, dict]] = []
        with mock.patch.object(
            compat, "notify", side_effect=lambda _app, message, **kwargs: seen.append((message, kwargs))
        ):
            await _with_page(body, instances=listed, cli=runner)
    return seen == [(i18n.t("cli.tui.dashboard.switch_default_done"), {"title": label})]


async def _test_switch_default_failure_is_reported():
    # 写失败时通知里给出 CLI 的结论与输出尾部，并撤掉记录让用户能重试。
    runner = _RecordingRunner(OperationResult(False, "把 beta 设为缺省实例失败（退出码 1）", "registry down"))
    with TemporaryDirectory(prefix="akari-badreg-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            list_view = page.query_one("#instance-list", compat.ListView)
            list_view.index = 1
            await pilot.pause()
            page.switch_to_selected()
            await page.wait_for_idle()
            await pilot.pause()
            current = app.page("dashboard")
            current.cli_runner = runner
            current.query_one("#instance-list", compat.ListView).index = 1
            await pilot.pause()
            current.switch_to_selected()
            await current.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return list(runner.calls)

        seen: list[tuple[str, str, str]] = []
        with mock.patch.object(
            compat,
            "notify",
            side_effect=lambda _app, message, **kwargs: seen.append(
                (message, kwargs.get("severity", "information"), kwargs.get("title", ""))
            ),
        ):
            calls = await _with_page(body, instances=listed, cli=runner)
    separator = i18n.t("cli.tui.common.error_separator")
    expected = i18n.t(
        "cli.tui.dashboard.switch_default_failed",
        error=f"把 beta 设为缺省实例失败（退出码 1）{separator}registry down",
    )
    label = i18n.t("cli.tui.dashboard.use_label", name="beta")
    return calls == [("instance", "use", "beta"), ("instance", "use", "beta")] and seen == [
        (expected, "error", label),
        (expected, "error", label),
    ]


async def _test_switch_refused_for_missing_directory():
    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.switch_to_selected()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body)
    return i18n.t("cli.tui.dashboard.switch_missing").split("${")[0].strip() in status


async def _test_policy_toggle_sends_cli_flags():
    # 策略开关经 `instance policy` 下发，方向由取值翻转决定。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.toggle_policy("autostart")
        await page.wait_for_idle()
        await pilot.pause()
        page.toggle_policy("restart_on_crash")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(runner.calls)

    calls = await _with_page(body, cli=runner)
    return calls == [
        ("instance", "policy", "alpha", "--no-autostart"),
        ("instance", "policy", "alpha", "--restart-on-crash"),
    ]


async def _test_busy_rejects_second_action():
    # 上一条命令没跑完时拒绝新动作，免得连点叠起多个改注册表的子进程。
    gate = threading.Event()
    runner = _RecordingRunner(on_run=lambda _args: gate.wait(2.0))

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.toggle_policy("autostart")
        await pilot.pause()
        page.toggle_policy("restart_on_crash")
        await pilot.pause()
        busy_status = page.status_text
        gate.set()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return busy_status, list(runner.calls)

    busy_status, calls = await _with_page(body, cli=runner)
    return busy_status == i18n.t("cli.tui.dashboard.busy_running") and calls == [
        ("instance", "policy", "alpha", "--no-autostart")
    ]


async def _test_cli_failure_is_reported():
    # 子进程报错时状态栏给出 CLI 的结论与输出尾部。
    runner = _RecordingRunner(OperationResult(False, "移除 alpha 的登记失败（退出码 1）", "instance not found"))

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body, cli=runner)
    separator = i18n.t("cli.tui.common.error_separator")
    expected = i18n.t(
        "cli.tui.dashboard.remove_failed",
        error=f"移除 alpha 的登记失败（退出码 1）{separator}instance not found",
    )
    return status == expected


async def _test_register_instance_from_prompt():
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        page.request_add_instance()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/gamma"
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, list(runner.calls), page.status_text

    opened, calls, status = await _with_page(body, cli=runner)
    return (
        opened
        and calls == [("instance", "add", "/tmp/gamma")]
        and status == i18n.t("cli.tui.dashboard.add_done", name="gamma", root=Path("/tmp/gamma"))
    )


async def _test_add_prompt_prefills_active_root():
    # 在实例目录里启动界面时，登记框预填当前实例：直接回车即可登记，不必手打路径。
    with TemporaryDirectory(prefix="akari-add-") as raw:
        root = Path(raw) / "inst"
        root.mkdir()
        previous = context.active_root()
        context.set_active_root(root)

        async def body(app, page, pilot, source, listed, control):
            page.request_add_instance()
            await pilot.pause()
            value = app.screen.query_one("#prompt-input", compat.Input).value
            await pilot.press("escape")
            await pilot.pause()
            await pilot.press("q")
            return value

        try:
            value = await _with_page(body)
        finally:
            context.set_active_root(previous)
    return value == str(root.resolve())


async def _test_boot_note_is_announced():
    # 进界面前发生的事（如自动登记）要在首屏就报出来，不能等用户翻到概览页才看到。
    note = i18n.t("cli.tui.dashboard.register_auto", name="demo", root="/tmp/demo")
    seen: list[str] = []

    async def body(app, page, pilot, source, listed, control):
        await pilot.press("q")

    with mock.patch.object(compat, "notify", side_effect=lambda app, message, **_: seen.append(message)):
        await _with_page(body, boot_note=note)
    return seen == [note]


async def _test_local_source_follows_switched_instance():
    # 切换实例后概览页自己的描述也要跟着走：默认数据源在取数时读共享状态，而不是记住启动目录。
    from akaribot.cli.tui.dashboard import LocalDashboardSource

    with TemporaryDirectory(prefix="akari-root-") as raw:
        switched = Path(raw) / "switched"
        switched.mkdir()
        (switched / "akaribot.toml").write_text('[instance]\nname = "switched"\nlocale = "zh_cn"\n', encoding="utf-8")
        previous = context.active_root()
        context.set_active_root(switched)
        try:
            snapshot = LocalDashboardSource().snapshot()
        finally:
            context.set_active_root(previous)
    return snapshot.instance_root == str(switched.resolve()) and snapshot.instance_name == "switched"


async def _test_unregister_opens_confirm_modal():
    # ctrl+d 一次触发即弹确认框：框里只有「移除登记」与「取消」，并写明实例目录不动。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        asked = list(runner.calls)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, hint, labels, asked, list(runner.calls), page.status_text

    opened, hint, labels, asked, calls, status = await _with_page(body, cli=runner)
    return (
        opened
        and asked == []
        and i18n.t("cli.tui.dashboard.remove_choice_hint") in hint
        and labels
        == [
            i18n.t("cli.tui.dashboard.remove_choice_confirm"),
            i18n.t("cli.tui.dashboard.add_cancel"),
        ]
        and calls == [("instance", "remove", "alpha", "--yes")]
        and status == i18n.t("cli.tui.dashboard.remove_done", name="alpha")
    )


async def _test_remove_modal_cancel_keeps_registry():
    # 选「取消」只关掉确认框：不下发子进程，状态栏说明动作已取消。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        await _pick_cancel(app, pilot)
        status = page.status_text
        await pilot.press("q")
        return list(runner.calls), status

    calls, status = await _with_page(body, cli=runner)
    return calls == [] and status == i18n.t("cli.tui.dashboard.remove_cancelled")


async def _test_remove_repeat_press_keeps_single_modal():
    # 连发第二次落在防抖窗口内，不该叠起两层模态框。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return opened, list(runner.calls)

    opened, calls = await _with_page(body, cli=runner)
    return opened == 2 and calls == []


async def _test_policy_refused_for_unregistered():
    listed = StaticInstanceListSource((InstanceRow(name="", root=Path("/tmp/plain"), registered=False),))
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        page.toggle_policy("autostart")
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status, list(runner.calls)

    status, calls = await _with_page(body, instances=listed, cli=runner)
    return calls == [] and status


async def _test_service_row_reports_state():
    # 概览页要能看出服务装没装：装了就写清后端、注册状态与单元文件位置。
    control = StaticServiceControl(
        ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist"))
    )

    async def body(app, page, pilot, source, listed, control):
        text = str(page.query_one("#service", compat.Static).render())
        await pilot.press("q")
        return text

    text = await _with_page(body, service=control)
    return "launchd" in text and "/tmp/agent.plist" in text


async def _test_service_row_reports_unsupported():
    control = StaticServiceControl(ServiceRow(backend="unsupported", detail="Windows 尚未支持"))

    async def body(app, page, pilot, source, listed, control):
        text = str(page.query_one("#service", compat.Static).render())
        await pilot.press("q")
        return text

    text = await _with_page(body, service=control)
    return "Windows" in text


async def _test_service_install_opens_confirm_modal():
    # 一次触发即弹模态：框里给执行与预演两个去处，模态本身就是确认。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))
    runner = _RecordingRunner(
        on_run=lambda _args: control.set_status(
            ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist"))
        )
    )

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        asked = list(runner.calls)
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, asked, labels, list(runner.calls), page.service_row.installed, page.status_text

    opened, asked, labels, calls, installed, status = await _with_page(body, service=control, cli=runner)
    return (
        opened
        and asked == []
        and labels[:2]
        == [
            i18n.t("cli.tui.dashboard.service_choice_install"),
            i18n.t("cli.tui.dashboard.service_choice_dry_run"),
        ]
        and calls == [("service", "install")]
        and installed
        and status == i18n.t("cli.tui.dashboard.service_added", path="/tmp/agent.plist")
    )


async def _test_service_uninstall_when_installed():
    control = StaticServiceControl(
        ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist"))
    )
    runner = _RecordingRunner(
        on_run=lambda _args: control.set_status(ServiceRow(backend="launchd", installed=False, enabled=False))
    )

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(runner.calls), page.service_row.installed, labels

    calls, installed, labels = await _with_page(body, service=control, cli=runner)
    return (
        calls == [("service", "uninstall")]
        and not installed
        and i18n.t("cli.tui.dashboard.service_choice_uninstall") in labels
    )


async def _test_service_install_confirms_overwrite_before_force():
    # 缓存的安装状态可能过期：单元文件已存在时确认框要写明覆盖，执行时才带 --force。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        control.set_status(ServiceRow(backend="launchd", installed=True, path=Path("/tmp/agent.plist")))
        page.request_toggle_service()
        await pilot.pause()
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return hint, list(runner.calls)

    hint, calls = await _with_page(body, service=control, cli=runner)
    expected = i18n.t("cli.tui.dashboard.service_choice_hint_force", path="/tmp/agent.plist")
    return expected in hint and calls == [("service", "install", "--force")]


async def _test_service_confirmation_offers_dry_run():
    # 确认框里的「先预演」只跑 --dry-run 并把输出留在状态栏与预演区，看过之后仍可执行真动作。
    preview = OperationResult(True, "预演成功", "将写入 /tmp/agent.plist\nlaunchctl bootstrap gui/501")
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False), preview_result=preview)
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        await _pick_choice(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        after_preview = (list(runner.calls), page.status_text, page.service_preview)
        page.request_toggle_service()
        await pilot.pause()
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, after_preview, list(runner.calls), control.calls, list(control.previewed)

    labels, after_preview, calls, service_calls, previewed = await _with_page(body, service=control, cli=runner)
    return (
        i18n.t("cli.tui.dashboard.service_choice_dry_run") in labels
        and after_preview[0] == []
        and after_preview[1] == i18n.t("cli.tui.dashboard.service_preview_done", output="将写入 /tmp/agent.plist")
        and after_preview[2] == preview.detail
        and service_calls["preview"] == 1
        and previewed == ["install"]
        and calls == [("service", "install")]
    )


async def _test_service_repeat_press_keeps_single_modal():
    # 连发第二次落在防抖窗口内，不该叠起两层模态框。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        page.request_toggle_service()
        await pilot.pause()
        opened = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return opened

    opened = await _with_page(body, service=control)
    return opened == 2


async def _test_remove_gate_reset_on_page_reset():
    # reset_pending() 清掉闸门后，同一目标可以立刻重新弹框：防抖窗口不再挡它。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        page.reset_pending()
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return opened, list(runner.calls)

    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        opened, calls = await _with_page(body, cli=runner)
    return opened == 3 and calls == []


async def _test_remove_modal_resets_on_highlight_change():
    # 光标离开又回到同一行要重新弹框：换选中项时闸门已作废。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        list_view.index = 1
        await pilot.pause()
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return opened, list(runner.calls)

    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        opened, calls = await _with_page(body, cli=runner)
    return opened == 3 and calls == []


async def _test_polling_keeps_pending_confirm():
    # 周期轮询只刷新显示：清单内容变化与高亮回拨都不作废待确认，也不会叠出第二层模态框。
    listed = _ChangingListSource(_instance_rows())
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        page.request_remove_instance()
        await pilot.pause()
        before = page.instance_rows[0].running
        page.refresh_instances(polling=True)
        await pilot.pause()
        flipped = page.instance_rows[0].running != before
        restored = compat.highlighted_index(list_view)
        page.request_remove_instance()
        await pilot.pause()
        opened = len(app.screen_stack)
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return flipped, restored, opened, list(runner.calls)

    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        flipped, restored, opened, calls = await _with_page(body, instances=listed, cli=runner)
    return flipped is True and restored == 0 and opened == 2 and calls == []


async def _test_service_confirm_resets_on_status_reread():
    # 服务状态重读后闸门作废：取消模态后紧接着再按一次，仍应弹出新的确认框。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))

    async def body(app, page, pilot, source, listed, control):
        page.request_toggle_service()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        page.refresh_service()
        page.request_toggle_service()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return opened

    opened = await _with_page(body, service=control)
    return opened


async def _test_new_instance_runs_init():
    # 新建实例：输入目录 → 选环境方式 → init 子进程 → 刷新清单。
    runner = StaticInitRunner()

    with TemporaryDirectory(prefix="akari-new-") as raw:
        root = Path(raw) / "inst"
        root.mkdir()
        (root / "akaribot.toml").write_text("[instance]\nname = 'inst'\n", encoding="utf-8")
        previous = context.active_root()
        context.set_active_root(root)

        async def body(app, page, pilot, source, listed, control):
            page.init_runner = runner
            page.request_new_instance()
            await pilot.pause()
            prefilled = app.screen.query_one("#prompt-input", compat.Input).value
            app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/newbie"
            await pilot.press("enter")
            await pilot.pause()
            labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
            await _pick_choice(app, pilot, 0)
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return prefilled, labels, list(runner.created), page.status_text

        try:
            prefilled, labels, created, status = await _with_page(body)
        finally:
            context.set_active_root(previous)
    return (
        prefilled == str(root.resolve().parent)
        and labels
        == [
            i18n.t("cli.tui.dashboard.new_venv_managed"),
            i18n.t("cli.tui.dashboard.new_venv_current"),
            i18n.t("cli.tui.dashboard.add_cancel"),
        ]
        and created == [("/tmp/newbie", True, i18n.current_locale())]
        and status == i18n.t("cli.tui.dashboard.new_done", name="newbie", root=Path("/tmp/newbie"))
    )


async def _test_new_instance_current_env_skips_managed_venv():
    runner = StaticInitRunner()

    async def body(app, page, pilot, source, listed, control):
        page.init_runner = runner
        page.request_new_instance()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/plain"
        await pilot.press("enter")
        await pilot.pause()
        await _pick_choice(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(runner.created), page.status_text

    created, status = await _with_page(body)
    return created == [("/tmp/plain", False, i18n.current_locale())] and status


async def _test_new_instance_failure_is_reported():
    runner = StaticInitRunner(OperationResult(False, "创建实例失败", "目录非空"))

    async def body(app, page, pilot, source, listed, control):
        page.init_runner = runner
        page.request_new_instance()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/busy"
        await pilot.press("enter")
        await pilot.pause()
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status

    status = await _with_page(body)
    separator = i18n.t("cli.tui.common.error_separator")
    return status == i18n.t("cli.tui.dashboard.new_failed", error=f"创建实例失败{separator}目录非空")


async def _test_subprocess_init_runner_builds_argv():
    # init 的开关必须与命令层一致：--non-interactive 取缺省选项，--no-venv 才是装进当前环境。
    calls: list[tuple[list[str], dict]] = []

    def runner(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    init = SubprocessInitRunner(runner=runner)
    managed = init.create(Path("/tmp/newbie"), managed_venv=True, locale="zh_cn")
    plain = init.create(Path("/tmp/newbie"), managed_venv=False, locale="en_us")
    first, second = calls[0][0], calls[1][0]
    options = calls[0][1]
    env = options["env"]
    return (
        managed.ok
        and plain.ok
        and first[-5:] == ["init", "/tmp/newbie", "--non-interactive", "--locale", "zh_cn"]
        and second[-6:] == ["init", "/tmp/newbie", "--non-interactive", "--locale", "en_us", "--no-venv"]
        and options["cwd"] == "/tmp"
        and options["timeout"] == INIT_TIMEOUT_SECONDS
        and env["AKARI_INSTANCE_DIR"] == "/tmp/newbie"
        and env["PYTHONIOENCODING"] == "utf-8"
    )


async def _test_subprocess_cli_runner_builds_argv():
    # 写动作的 argv 落在真实子命令上，环境与编码与其它页一致。
    calls: list[tuple[list[str], dict]] = []

    def runner(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    cli = SubprocessCliRunner(runner=runner)
    result = cli.run(("instance", "policy", "alpha", "--no-autostart"), label="设置 alpha 的服务策略")
    argv, options = calls[0]
    env = options["env"]
    return (
        result.ok
        and argv[3:] == ["instance", "policy", "alpha", "--no-autostart"]
        and options["timeout"] == CLI_WRITE_TIMEOUT_SECONDS
        and options["encoding"] == "utf-8"
        and env["PYTHONIOENCODING"] == "utf-8"
    )


async def _test_accept_window():
    # accept 给「一次触发就弹模态」的动作挡重复触发：防抖窗口内忽略，之后照常放行。
    gate = compat.PendingConfirm()
    return (
        gate.accept("x", now=100.0) is True
        and gate.accept("x", now=100.1) is False
        and gate.accept("x", now=101.0) is True
    )


async def _test_bindings_follow_key_convention():
    # 破坏性动作不用单字母键；低频键位不进页脚，80 列终端才放得下高频的那几条。
    shown = {binding.key: binding.show for binding in DashboardPage.BINDINGS}
    return (
        "d" not in shown
        and shown.get("ctrl+d") is False
        and shown.get("ctrl+n") is True
        and all(shown.get(key) is False for key in ("a", "c", "n", "i"))
    )


@func_case
async def test_tui_dashboard(tester: Tester):
    """cli.tui.dashboard: 实例信息与运行状态测试"""
    _use_cli_locale()
    await tester.test(_test_accept_window, "一次触发的闸门挡重复触发")
    await tester.test(_test_subprocess_init_runner_builds_argv, "init 子进程按命令层开关拼装")
    await tester.test(_test_subprocess_cli_runner_builds_argv, "写动作子进程按命令层 argv 拼装")
    await tester.test(_test_bindings_follow_key_convention, "键位约定：破坏性动作带修饰键")
    await tester.test(_test_service_repeat_press_keeps_single_modal, "连发第二次不叠模态框")
    await tester.test(_test_service_confirm_resets_on_status_reread, "服务状态重读后闸门作废")
    await tester.test(_test_remove_repeat_press_keeps_single_modal, "移除登记连发第二次不叠模态框")
    # 用例里的两次按键相隔只有几毫秒，压缩防抖窗口，免得每条确认都等 0.4 秒。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_fields_show_instance_facts, "展示实例根、名称与版本")
        await tester.test(_test_state_follows_probe, "运行状态跟着探测结果")
        await tester.test(_test_refresh_rereads_snapshot, "刷新重新读取快照")
        await tester.test(_test_load_failure_degrades_to_status, "读取失败只降级到状态栏")
        await tester.test(_test_instance_list_marks_state_and_policy, "实例清单带状态与策略标记")
        await tester.test(_test_enter_switches_instance, "在清单里切换实例")
        await tester.test(_test_switch_sends_default_write, "切换实例下发缺省项写入")
        await tester.test(_test_switch_does_not_wait_for_cli, "切换不等子进程且不占忙标志")
        await tester.test(_test_switch_default_rewrites_after_return, "切回原实例仍写缺省项")
        await tester.test(_test_switch_skips_default_for_unregistered, "未登记实例不改写缺省项")
        await tester.test(_test_switch_default_result_is_notified, "缺省项成功以通知报出")
        await tester.test(_test_switch_default_failure_is_reported, "缺省项失败以通知报出并允许重试")
        await tester.test(_test_switch_refused_for_missing_directory, "目录无 akaribot.toml 时拒绝切换")
        await tester.test(_test_policy_toggle_sends_cli_flags, "自启与崩溃重启经 CLI 下发")
        await tester.test(_test_busy_rejects_second_action, "上一条命令未完成时拒绝新动作")
        await tester.test(_test_register_instance_from_prompt, "输入框登记实例")
        await tester.test(_test_add_prompt_prefills_active_root, "登记框预填当前实例目录")
        await tester.test(_test_new_instance_runs_init, "新建实例经 init 并刷新清单")
        await tester.test(_test_new_instance_current_env_skips_managed_venv, "用当前环境时不建托管 venv")
        await tester.test(_test_new_instance_failure_is_reported, "新建失败不登记且报出原因")
        await tester.test(_test_boot_note_is_announced, "进界面时的自动登记以通知报出")
        await tester.test(_test_local_source_follows_switched_instance, "概览页描述跟着切换后的实例")
        await tester.test(_test_unregister_opens_confirm_modal, "移除登记一次触发即弹确认框")
        await tester.test(_test_remove_modal_cancel_keeps_registry, "取消移除登记不动注册表")
        await tester.test(_test_cli_failure_is_reported, "CLI 报错时状态栏给出原因")
        await tester.test(_test_remove_modal_resets_on_highlight_change, "高亮换过再回来要重新弹框")
        await tester.test(_test_polling_keeps_pending_confirm, "周期轮询不作废待确认")
        await tester.test(_test_policy_refused_for_unregistered, "未登记实例不设策略")
        await tester.test(_test_service_row_reports_state, "服务行展示后端与单元文件")
        await tester.test(_test_service_row_reports_unsupported, "平台不支持时如实说明")
        await tester.test(_test_service_install_opens_confirm_modal, "一次触发即弹服务确认框")
        await tester.test(_test_service_install_confirms_overwrite_before_force, "单元文件已存在时写明覆盖")
        await tester.test(_test_service_confirmation_offers_dry_run, "确认框可先预演再决定")
        await tester.test(_test_service_uninstall_when_installed, "已安装时按键走卸载")
    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        await tester.test(_test_remove_gate_reset_on_page_reset, "reset_pending() 后同一目标可重新弹框")
    return tester
