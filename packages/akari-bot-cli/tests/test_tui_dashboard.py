"""概览页的实例信息、运行状态、实例切换与服务操作测试。"""

import threading
import asyncio
import json
import shutil
import subprocess
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
    LocalSetupSummarySource,
    ServiceRow,
    SetupSummary,
    StaticDashboardSource,
    StaticInitRunner,
    StaticInstanceListSource,
    StaticServiceControl,
    StaticSetupSummarySource,
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

# 页底按钮按 ButtonFlow 的排列顺序列出。
BUTTON_IDS = (
    "switch",
    "new-instance",
    "add-instance",
    "remove-instance",
    "autostart",
    "crash-restart",
    "service-toggle",
    "refresh",
)

FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "dashboard.json"
_KEEP_ALIVE: list[TemporaryDirectory] = []


def _button(page, button_id: str) -> compat.Button:
    return page.query_one(f"#{button_id}", compat.Button)


def _labels(page) -> dict[str, str]:
    return {button_id: str(_button(page, button_id).label) for button_id in BUTTON_IDS}


def _disabled(page) -> dict[str, bool]:
    return {button_id: _button(page, button_id).disabled for button_id in BUTTON_IDS}


def _merged_locale_dir() -> Path:
    # 测试片段覆盖包内语言文件，以核对实际渲染文案。
    holder = TemporaryDirectory(prefix="akari-dashboard-locale-")
    _KEEP_ALIVE.append(holder)
    root = Path(holder.name)
    for path in Path(i18n.locales_dir()).glob("*.json"):
        shutil.copy(path, root / path.name)
    target = root / "zh_cn.json"
    document = json.loads(target.read_text(encoding="utf-8"))
    document.update(json.loads(FRAGMENT.read_text(encoding="utf-8")))
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return root


def _use_cli_locale() -> None:
    # CLI 首次读取文案会初始化快照，需在初始化后应用测试片段。
    i18n.t("cli.tui.common.status_ready")
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [str(_merged_locale_dir())], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _instance_rows() -> tuple[InstanceRow, ...]:
    return (
        InstanceRow(name="alpha", root=Path("/tmp/alpha"), running=True, autostart=True),
        InstanceRow(name="beta", root=Path("/tmp/beta"), running=False, restart_on_crash=True),
    )


async def _wait_until(predicate, timeout: float = 1.0) -> bool:
    # 后台任务完成时间不确定，轮询条件以避免固定延迟导致误判。
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


# 记录写操作的 argv；on_run 暂停首条命令，用于验证忙碌状态。
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
    # 模拟轮询更新实例运行状态，验证待确认操作不受显示更新影响。
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
    # 实例切换要求目标目录包含 akaribot.toml。
    roots: dict[str, Path] = {}
    for name in names:
        root = Path(raw) / name
        root.mkdir()
        (root / "akaribot.toml").write_text(f"[instance]\nname = '{name}'\n", encoding="utf-8")
        roots[name] = root
    return roots


async def _pick_choice(app, pilot, index: int) -> None:
    # 此用例通过控件 API 验证操作流程，按钮可见性由布局用例验证。
    app.screen.query_one(f"#choice-{index}", compat.Button).press()
    await pilot.pause()


async def _pick_cancel(app, pilot) -> None:
    app.screen.query_one("#choice-cancel", compat.Button).press()
    await pilot.pause()


async def _with_page(
    body,
    source=None,
    size=(110, 32),
    instances=None,
    service=None,
    setup=None,
    boot_note="",
    cli=None,
):
    chosen = source if source is not None else StaticDashboardSource(SNAPSHOT, running=True)
    listed = instances if instances is not None else StaticInstanceListSource(_instance_rows())
    control = service if service is not None else StaticServiceControl()
    # 摘要默认使用替身数据源，避免启动诊断子进程。
    brief = setup if setup is not None else StaticSetupSummarySource()
    app = TuiApp(
        sources={
            "dashboard": chosen,
            "dashboard_instances": listed,
            "dashboard_service": control,
            "dashboard_setup": brief,
        },
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
    # 当前实例即使未登记也应显示，确保用户能够识别操作目标。
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
    # 选择实例后更新共享上下文，后续读取均使用该实例。
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
        # macOS 临时目录可能为符号链接，实例根按解析后的路径保存。
        expected = roots["beta"].resolve()
    return active == expected and status and list(runner.calls) == [("instance", "use", "beta")]


async def _test_switch_sends_default_write():
    # 默认实例通过 `instance use` 保存，执行结果通过通知显示。
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
    # 实例上下文即时切换，默认实例异步保存；同一目标不重复提交。
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
    # 默认实例记录与当前选择一致，切换返回同一实例时仍需更新。
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
                # 切换实例会重新挂载页面，因此需重新获取页面并注入执行器。
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
    # 执行结果通过应用级通知显示，不依赖页面的挂载状态。
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
    # 写入失败时显示 CLI 结果和输出尾部，并清除记录以允许重试。
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
    # 写操作执行期间拒绝新请求，避免多个进程同时修改注册表。
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
    # 从实例目录启动界面时，登记框预填当前实例路径。
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
    # 启动阶段的结果应在首屏显示，与初始页面无关。
    note = i18n.t("cli.tui.dashboard.register_auto", name="demo", root="/tmp/demo")
    seen: list[str] = []

    async def body(app, page, pilot, source, listed, control):
        await pilot.press("q")

    with mock.patch.object(compat, "notify", side_effect=lambda app, message, **_: seen.append(message)):
        await _with_page(body, boot_note=note)
    return seen == [note]


async def _test_local_source_follows_switched_instance():
    # 默认数据源每次读取共享实例状态，以适应实例切换。
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
    # 移除登记的确认框应说明实例目录保留。
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
    # 取消后关闭确认框并更新状态，不执行子进程。
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
    # 防抖窗口内的重复请求不得叠加确认框。
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
    # 已安装的服务应显示后端、注册状态与单元文件位置。
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
    # 确认框提供执行与预览选项。
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
    # 单元文件存在时应明确提示覆盖，确认执行后添加 --force。
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
    # 预览仅执行 --dry-run 并展示输出，用户可据此确认实际操作。
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
    # 防抖窗口内的重复请求不得叠加确认框。
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
    # reset_pending() 复位后，同一目标可立即重新发起确认。
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
    # 高亮项切换后清除防抖状态，返回同一项时需重新确认。
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
    # 周期轮询仅更新显示，不清除待确认状态或重复打开确认框。
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
    # 刷新服务状态或取消确认后，允许重新发起确认。
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
    # --non-interactive 使用默认选项；--no-venv 指定安装到当前环境。
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
    # 写操作使用对应 CLI 子命令，环境与编码设置与其他页面一致。
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
    # accept 在防抖窗口内拒绝重复确认请求。
    gate = compat.PendingConfirm()
    return (
        gate.accept("x", now=100.0) is True
        and gate.accept("x", now=100.1) is False
        and gate.accept("x", now=101.0) is True
    )


async def _test_bindings_follow_key_convention():
    # 破坏性操作使用组合键；隐藏低频键位以保证 80 列页脚可见。
    shown = {binding.key: binding.show for binding in DashboardPage.BINDINGS}
    return (
        "d" not in shown
        and shown.get("ctrl+d") is False
        and shown.get("ctrl+n") is True
        and all(shown.get(key) is False for key in ("a", "c", "n", "i"))
    )


async def _test_button_switch_matches_key():
    # 按钮与回车均切换到高亮实例，并通过 instance use 保存默认实例。
    runner = _RecordingRunner()
    with TemporaryDirectory(prefix="akari-btn-switch-") as raw:
        roots = _temp_instances(raw, "alpha", "beta")
        listed = StaticInstanceListSource(
            (
                InstanceRow(name="alpha", root=roots["alpha"], running=True),
                InstanceRow(name="beta", root=roots["beta"], running=False),
            )
        )

        async def body(app, page, pilot, source, chosen, control):
            page.query_one("#instance-list", compat.ListView).index = 1
            await pilot.pause()
            _button(page, "switch").press()
            await pilot.pause()
            status = page.status_text
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return context.active_root(), status

        active, status = await _with_page(body, instances=listed, cli=runner)
        expected = roots["beta"].resolve()
    return (
        active == expected
        and status.startswith(i18n.t("cli.tui.dashboard.switch_done", name="beta"))
        and list(runner.calls) == [("instance", "use", "beta")]
    )


async def _test_button_new_instance_runs_init():
    # 新建按钮与 ctrl+n 共用目录输入、环境选择和 init 流程。
    runner = StaticInitRunner()

    with TemporaryDirectory(prefix="akari-btn-new-") as raw:
        root = Path(raw) / "inst"
        root.mkdir()
        (root / "akaribot.toml").write_text("[instance]\nname = 'inst'\n", encoding="utf-8")
        previous = context.active_root()
        context.set_active_root(root)

        async def body(app, page, pilot, source, listed, control):
            page.init_runner = runner
            _button(page, "new-instance").press()
            await pilot.pause()
            opened = len(app.screen_stack) > 1
            prefilled = app.screen.query_one("#prompt-input", compat.Input).value
            app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/btn-new"
            await pilot.press("enter")
            await pilot.pause()
            await _pick_choice(app, pilot, 0)
            await page.wait_for_idle()
            await pilot.pause()
            await pilot.press("q")
            return opened, prefilled, list(runner.created), page.status_text

        try:
            opened, prefilled, created, status = await _with_page(body)
        finally:
            context.set_active_root(previous)
    return (
        opened
        and prefilled == str(root.resolve().parent)
        and created == [("/tmp/btn-new", True, i18n.current_locale())]
        and status == i18n.t("cli.tui.dashboard.new_done", name="btn-new", root=Path("/tmp/btn-new"))
    )


async def _test_button_add_instance_registers_directory():
    # 登记按钮与 n 共用目录输入及 instance add 流程。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        _button(page, "add-instance").press()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        app.screen.query_one("#prompt-input", compat.Input).value = "/tmp/btn-gamma"
        await pilot.press("enter")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, list(runner.calls), page.status_text

    opened, calls, status = await _with_page(body, cli=runner)
    return (
        opened
        and calls == [("instance", "add", "/tmp/btn-gamma")]
        and status == i18n.t("cli.tui.dashboard.add_done", name="btn-gamma", root=Path("/tmp/btn-gamma"))
    )


async def _test_button_remove_instance_opens_confirm_modal():
    # 移除按钮与 ctrl+d 均在确认后调用 instance remove。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        _button(page, "remove-instance").press()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        asked = list(runner.calls)
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, asked, list(runner.calls), page.status_text

    opened, asked, calls, status = await _with_page(body, cli=runner)
    return (
        opened
        and asked == []
        and calls == [("instance", "remove", "alpha", "--yes")]
        and status == i18n.t("cli.tui.dashboard.remove_done", name="alpha")
    )


async def _test_button_policy_toggles_send_cli_flags():
    # 策略按钮与 a / c 共用 instance policy 流程，按当前值切换。
    runner = _RecordingRunner()

    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        _button(page, "autostart").press()
        await page.wait_for_idle()
        await pilot.pause()
        _button(page, "crash-restart").press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(runner.calls)

    calls = await _with_page(body, cli=runner)
    return calls == [
        ("instance", "policy", "alpha", "--no-autostart"),
        ("instance", "policy", "alpha", "--restart-on-crash"),
    ]


async def _test_button_service_opens_confirm_modal():
    # 服务按钮与 i 均打开包含执行和预览选项的确认框。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))
    runner = _RecordingRunner(
        on_run=lambda _args: control.set_status(
            ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist"))
        )
    )

    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        _button(page, "service-toggle").press()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        await _pick_choice(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, labels, list(runner.calls), page.status_text

    opened, labels, calls, status = await _with_page(body, service=control, cli=runner)
    return (
        opened
        and labels[:2]
        == [
            i18n.t("cli.tui.dashboard.service_choice_install"),
            i18n.t("cli.tui.dashboard.service_choice_dry_run"),
        ]
        and calls == [("service", "install")]
        and status == i18n.t("cli.tui.dashboard.service_added", path="/tmp/agent.plist")
    )


async def _test_button_refresh_rereads_snapshot():
    # 刷新按钮与 r 均忽略缓存重新读取快照。
    async def body(app, page, pilot, source, listed, control):
        before = source.calls["snapshot"]
        _button(page, "refresh").press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return before, source.calls["snapshot"]

    before, after = await _with_page(body)
    return after > before


async def _test_action_buttons_follow_state():
    # 按钮状态与实例登记、策略和服务状态一致；未登记时禁用注册表写操作。
    control = StaticServiceControl(ServiceRow(backend="launchd", installed=False))
    listed = StaticInstanceListSource(
        (
            InstanceRow(name="alpha", root=Path("/tmp/alpha"), running=True, autostart=True),
            InstanceRow(name="", root=Path("/tmp/plain"), running=False, registered=False),
        )
    )
    previous = context.active_root()
    context.set_active_root("/tmp/alpha")

    async def body(app, page, pilot, source, chosen, control):
        list_view = page.query_one("#instance-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        current = (_labels(page), _disabled(page))
        control.set_status(ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist")))
        page.refresh_service()
        await pilot.pause()
        installed = (_labels(page)["service-toggle"], _disabled(page)["service-toggle"])
        control.set_status(ServiceRow(backend="unsupported", detail="未支持"))
        page.refresh_service()
        await pilot.pause()
        unsupported = _disabled(page)["service-toggle"]
        list_view.index = 1
        await pilot.pause()
        unregistered = (_labels(page), _disabled(page))
        await pilot.press("q")
        return current, installed, unsupported, unregistered

    try:
        current, installed, unsupported, unregistered = await _with_page(body, instances=listed, service=control)
    finally:
        context.set_active_root(previous)
    current_labels, current_disabled = current
    unregistered_labels, unregistered_disabled = unregistered
    return (
        current_disabled
        == {
            "switch": True,
            "new-instance": False,
            "add-instance": False,
            "remove-instance": False,
            "autostart": False,
            "crash-restart": False,
            "service-toggle": False,
            "refresh": False,
        }
        and current_labels["autostart"] == i18n.t("cli.tui.dashboard.button_autostart_on")
        and current_labels["crash-restart"] == i18n.t("cli.tui.dashboard.button_crash_off")
        and current_labels["service-toggle"] == i18n.t("cli.tui.dashboard.button_service_install")
        and installed == (i18n.t("cli.tui.dashboard.button_service_uninstall"), False)
        and unsupported is True
        and unregistered_disabled
        == {
            "switch": False,
            "new-instance": False,
            "add-instance": False,
            "remove-instance": True,
            "autostart": True,
            "crash-restart": True,
            "service-toggle": True,
            "refresh": False,
        }
        and unregistered_labels["autostart"] == i18n.t("cli.tui.dashboard.button_autostart_off")
        and unregistered_labels["crash-restart"] == i18n.t("cli.tui.dashboard.button_crash_off")
    )


async def _test_action_buttons_disable_while_busy():
    # 写操作执行期间禁用按钮，避免多个子进程同时修改注册表。
    gate = threading.Event()
    runner = _RecordingRunner(on_run=lambda _args: gate.wait(2.0))
    previous = context.active_root()
    context.set_active_root("/tmp/elsewhere")

    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        _button(page, "autostart").press()
        started = await _wait_until(lambda: page._busy)
        busy = _disabled(page)
        gate.set()
        await page.wait_for_idle()
        await pilot.pause()
        idle = _disabled(page)
        await pilot.press("q")
        return started, busy, idle, list(runner.calls)

    try:
        started, busy, idle, calls = await _with_page(body, cli=runner)
    finally:
        context.set_active_root(previous)
    return (
        started
        and all(busy.values())
        and not any(idle.values())
        and calls == [("instance", "policy", "alpha", "--no-autostart")]
    )


async def _test_action_buttons_share_one_row_when_wide():
    # 宽终端采用单行按钮布局，减少高度占用。
    async def body(app, page, pilot, source, listed, control):
        # 标签在首次读取后更新，需等待重新排布再测量宽度。
        await pilot.pause()
        page_region = page.region
        boxes = {button_id: _button(page, button_id).region for button_id in BUTTON_IDS}
        fields = page.query_one("#fields-pane").region
        status = page.query_one("#status", compat.Static).region
        await pilot.press("q")
        return page_region, boxes, fields, status

    page_region, boxes, fields, status = await _with_page(body, size=(120, 32))
    inside = all(box.width > 0 and box.x >= page_region.x and box.right <= page_region.right for box in boxes.values())
    return (
        inside
        and len({box.y for box in boxes.values()}) == 1
        and min(box.y for box in boxes.values()) >= fields.bottom
        and status.y >= max(box.bottom for box in boxes.values())
    )


async def _test_action_buttons_wrap_after_remove_instance():
    # 80 列下折成两行，断点落在 remove-instance 之后：实例操作与策略服务各占一行。
    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        page_region = page.region
        fields = page.query_one("#fields-pane").region
        status = page.query_one("#status", compat.Static).region
        boxes = {button_id: _button(page, button_id).region for button_id in BUTTON_IDS}
        # 服务安装状态改变标签后，需重新验证按钮边界。
        control.set_status(ServiceRow(backend="launchd", installed=True, enabled=True, path=Path("/tmp/agent.plist")))
        page.refresh_service()
        await pilot.pause()
        rewritten = {button_id: _button(page, button_id).region for button_id in BUTTON_IDS}
        labels = _labels(page)
        await pilot.press("q")
        return page_region, boxes, rewritten, labels, fields, status

    page_region, boxes, rewritten, labels, fields, status = await _with_page(body, size=(80, 24))
    rows = {button_id: box.y for button_id, box in boxes.items()}
    instance_rows = {rows[button_id] for button_id in BUTTON_IDS[:4]}
    policy_rows = {rows[button_id] for button_id in BUTTON_IDS[4:]}
    expected_labels = {
        "switch": i18n.t("cli.tui.dashboard.button_switch"),
        "new-instance": i18n.t("cli.tui.dashboard.button_new_instance"),
        "add-instance": i18n.t("cli.tui.dashboard.button_add_instance"),
        "remove-instance": i18n.t("cli.tui.dashboard.button_remove_instance"),
        "autostart": i18n.t("cli.tui.dashboard.button_autostart_on"),
        "crash-restart": i18n.t("cli.tui.dashboard.button_crash_off"),
        "service-toggle": i18n.t("cli.tui.dashboard.button_service_uninstall"),
        "refresh": i18n.t("cli.tui.dashboard.action_refresh"),
    }
    return (
        all(
            box.width > 0 and box.x >= page_region.x and box.right <= page_region.right
            for box in (*boxes.values(), *rewritten.values())
        )
        and len(instance_rows) == 1
        and len(policy_rows) == 1
        and len(set(rows.values())) == 2
        and max(instance_rows) < min(policy_rows)
        and min(rows.values()) >= fields.bottom
        and status.y >= max(box.bottom for box in boxes.values())
        and labels == expected_labels
    )


async def _test_instances_caption_points_to_buttons():
    # 说明行按当前条数插值，完整显示对应文案。
    async def body(app, page, pilot, source, listed, control):
        caption = str(page.query_one("#instances-caption", compat.Static).render())
        await pilot.press("q")
        return caption

    caption = await _with_page(body)
    return caption == i18n.t("cli.tui.dashboard.instances_keys_caption_with_count", count=len(_instance_rows()))


async def _test_instances_caption_drops_key_list():
    # 操作提示指向页底按钮，完整快捷键通过 ? 查看。
    counted = i18n.t("cli.tui.dashboard.instances_keys_caption_with_count", count=2)
    single = i18n.t("cli.tui.dashboard.instances_keys_caption")
    return "ctrl+d" not in counted and "ctrl+d" not in single and "2" in counted and "${count}" not in counted


SETUP = SetupSummary(unconfigured_adapters=2, pending_placeholders=38, doctor_errors=1, doctor_warnings=3)

SETUP_IDS = ("goto-config", "goto-run", "goto-doctor")


def _setup_button_state(page) -> dict[str, tuple[bool, str]]:
    return {
        button_id: (
            page.query_one(f"#{button_id}", compat.Button).disabled,
            str(page.query_one(f"#{button_id}", compat.Button).label),
        )
        for button_id in SETUP_IDS
    }


def _setup_label(key: str, *, blocked: bool = False) -> str:
    suffix = "_blocked" if blocked else ""
    return i18n.t(f"cli.tui.dashboard.setup_button_{key}{suffix}")


def _inside(region, page_region) -> bool:
    return region.x >= page_region.x and region.right <= page_region.right and region.bottom <= page_region.bottom


def _setup_expected(state_label: str) -> dict[str, str]:
    return {
        i18n.t("cli.tui.dashboard.setup_adapters_label"): i18n.t(
            "cli.tui.dashboard.setup_adapters_value", count=SETUP.unconfigured_adapters
        ),
        i18n.t("cli.tui.dashboard.setup_placeholders_label"): i18n.t(
            "cli.tui.dashboard.setup_placeholders_value", count=SETUP.pending_placeholders
        ),
        i18n.t("cli.tui.dashboard.setup_instance_label"): state_label,
        i18n.t("cli.tui.dashboard.setup_doctor_label"): i18n.t(
            "cli.tui.dashboard.setup_doctor_value", errors=SETUP.doctor_errors, warnings=SETUP.doctor_warnings
        ),
    }


async def _test_setup_summary_renders_four_items():
    # 四项摘要以两行显示，标签与取值一一对应。
    brief = StaticSetupSummarySource(SETUP)

    async def body(app, page, pilot, source, listed, control):
        rows = dict(page.setup_rows)
        text = page.setup_text
        lines = text.splitlines()
        calls = brief.calls["summary"]
        # 摘要仅在首次显示时加载，周期探测使用缓存。
        page.refresh_running()
        page.refresh_instances(polling=True)
        await pilot.pause()
        await pilot.press("q")
        return rows, text, lines, calls, brief.calls["summary"]

    rows, text, lines, calls, calls_after = await _with_page(body, setup=brief)
    expected = _setup_expected(SNAPSHOT.state_label)
    return (
        rows == expected
        and len(lines) == 2
        and all(f"{label} {value}" in text for label, value in expected.items())
        and calls == 1
        and calls_after == 1
    )


async def _test_setup_state_follows_snapshot():
    # 摘要与字段区共用运行状态，随探测结果同步更新。
    async def body(app, page, pilot, source, listed, control):
        running = dict(page.setup_rows)[i18n.t("cli.tui.dashboard.setup_instance_label")]
        source.set_running(False)
        page.refresh_running()
        await pilot.pause()
        stopped = dict(page.setup_rows)[i18n.t("cli.tui.dashboard.setup_instance_label")]
        await pilot.press("q")
        return running, stopped

    running, stopped = await _with_page(body)
    return running == SNAPSHOT.state_label and stopped == DashboardSnapshot(running=False).state_label


async def _test_setup_missing_values_say_missing():
    # 无法读取的摘要项应显示失败原因。
    reasons = {
        "adapters_reason": "体检统计缺少需要的字段",
        "placeholders_reason": "配置目录读不到",
        "doctor_reason": "体检输出无法解析（退出码 1）",
    }
    brief = StaticSetupSummarySource(SetupSummary(**reasons))

    async def body(app, page, pilot, source, listed, control):
        rows = dict(page.setup_rows)
        await pilot.press("q")
        return rows

    rows = await _with_page(body, setup=brief)
    expected = {
        i18n.t("cli.tui.dashboard.setup_adapters_label"): i18n.t(
            "cli.tui.dashboard.setup_value_missing_reason", reason=reasons["adapters_reason"]
        ),
        i18n.t("cli.tui.dashboard.setup_placeholders_label"): i18n.t(
            "cli.tui.dashboard.setup_value_missing_reason", reason=reasons["placeholders_reason"]
        ),
        i18n.t("cli.tui.dashboard.setup_doctor_label"): i18n.t(
            "cli.tui.dashboard.setup_value_missing_reason", reason=reasons["doctor_reason"]
        ),
    }
    return all(rows[label] == value for label, value in expected.items()) and all(
        rows[label] != i18n.t("cli.tui.dashboard.setup_value_missing") for label in expected
    )


async def _test_setup_load_failure_degrades():
    # 摘要读取失败时逐项显示原因，其他区域继续更新。
    brief = StaticSetupSummarySource(error=RuntimeError("boom"))

    async def body(app, page, pilot, source, listed, control):
        rows = dict(page.setup_rows)
        await pilot.press("q")
        return rows, page.fields_text, page.status_text, brief.calls["summary"]

    rows, fields, status, calls = await _with_page(body, setup=brief)
    expected = i18n.t("cli.tui.dashboard.setup_value_missing_reason", reason="RuntimeError: boom")
    return (
        calls == 1
        and rows[i18n.t("cli.tui.dashboard.setup_adapters_label")] == expected
        and rows[i18n.t("cli.tui.dashboard.setup_placeholders_label")] == expected
        and rows[i18n.t("cli.tui.dashboard.setup_doctor_label")] == expected
        and i18n.t("cli.tui.dashboard.field_instance_root") in fields
        and status
    )


async def _test_setup_estimated_placeholders_are_labelled():
    # 估算值使用估算标签，并说明估算依据。
    reason = i18n.t("cli.tui.dashboard.setup_placeholders_estimated_reason", detail="统计命令超时")
    brief = StaticSetupSummarySource(
        SetupSummary(pending_placeholders=31, placeholders_reason=reason, placeholders_estimated=True)
    )

    async def body(app, page, pilot, source, listed, control):
        rows = dict(page.setup_rows)
        await pilot.press("q")
        return rows

    rows = await _with_page(body, setup=brief)
    # 渲染用例验证估算标签，具体措辞由语言片段用例校验。
    estimated_key = "cli.tui.dashboard.setup_placeholders_label_estimated"
    fragment = json.loads(FRAGMENT.read_text(encoding="utf-8"))
    return (
        rows[i18n.t(estimated_key)]
        == i18n.t("cli.tui.dashboard.setup_placeholders_value_note", count=31, reason=reason)
        and i18n.t("cli.tui.dashboard.setup_placeholders_label") not in rows
        and "疑似待填写" in fragment[estimated_key]
        and "估算" in fragment[estimated_key]
        and "估算" in fragment["cli.tui.dashboard.setup_placeholders_estimated_reason"]
    )


async def _test_setup_loads_lazily_on_first_display():
    # 摘要仅在首次显示页面时读取，重绘和轮询使用缓存。
    brief = StaticSetupSummarySource(SETUP)
    app = TuiApp(
        sources={
            "dashboard": StaticDashboardSource(SNAPSHOT, running=True),
            "dashboard_instances": StaticInstanceListSource(_instance_rows()),
            "dashboard_service": StaticServiceControl(),
            "dashboard_setup": brief,
        },
        initial_page="modules",
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=(110, 32)) as pilot:
        await pilot.pause()
        before = brief.calls["summary"]
        app.show_page("dashboard")
        page = app.page("dashboard")
        await page.wait_for_idle()
        await pilot.pause()
        page.refresh_snapshot(force=True)
        await page.wait_for_idle()
        await pilot.pause()
        after = brief.calls["summary"]
        app.show_page("modules")
        await pilot.pause()
    return before == 0 and after == 1


async def _test_setup_buttons_jump_pages():
    # 三个按钮通过 show_page 切换到配置、运行与诊断页面。
    async def body(app, page, pilot, source, listed, control):
        visited: list[str] = []
        for page_key, button_id in zip(("config", "run", "doctor"), SETUP_IDS, strict=True):
            page.query_one(f"#{button_id}", compat.Button).press()
            await pilot.pause()
            visited.append(app.active_page)
            app.show_page("dashboard")
            await pilot.pause()
        await pilot.press("q")
        return visited, app.active_page

    visited, active = await _with_page(body, source=StaticDashboardSource(SNAPSHOT, running=False))
    return visited == ["config", "run", "doctor"] and active == "dashboard"


async def _test_setup_buttons_disabled_rules():
    # 缺少实例时禁用全部按钮；实例运行时禁用启动按钮，标签注明原因。
    brief = StaticSetupSummarySource(SETUP)
    empty = StaticInstanceListSource(())
    previous = context.active_root()
    context.set_active_root(None)

    async def body(app, page, pilot, source, listed, control):
        state = _setup_button_state(page)
        page.open_setup_page("run")
        await pilot.pause()
        blocked = (app.active_page, page.status_text)
        await pilot.press("q")
        return state, blocked

    try:
        state, blocked = await _with_page(body, setup=brief, instances=empty)
    finally:
        context.set_active_root(previous)
    blocked_status = i18n.t(
        "cli.tui.dashboard.setup_blocked_status",
        action=i18n.t("cli.tui.dashboard.setup_button_run"),
        reason=i18n.t("cli.tui.dashboard.setup_block_no_instance"),
    )
    no_instance = state == {
        "goto-config": (True, _setup_label("config", blocked=True)),
        "goto-run": (True, _setup_label("run", blocked=True)),
        "goto-doctor": (True, _setup_label("doctor", blocked=True)),
    }
    refused = blocked == ("dashboard", blocked_status)

    async def running_body(app, page, pilot, source, listed, control):
        state = _setup_button_state(page)
        await pilot.press("q")
        return state

    running = await _with_page(running_body, setup=brief)
    return (
        no_instance
        and refused
        and running
        == {
            "goto-config": (False, _setup_label("config")),
            "goto-run": (True, i18n.t("cli.tui.dashboard.setup_button_run_running")),
            "goto-doctor": (False, _setup_label("doctor")),
        }
    )


async def _test_setup_buttons_enabled_when_stopped():
    # 实例已登记且停止运行时，三个按钮均可用并显示操作名称。
    async def body(app, page, pilot, source, listed, control):
        state = _setup_button_state(page)
        await pilot.press("q")
        return state

    state = await _with_page(body, source=StaticDashboardSource(SNAPSHOT, running=False))
    return state == {
        "goto-config": (False, _setup_label("config")),
        "goto-run": (False, _setup_label("run")),
        "goto-doctor": (False, _setup_label("doctor")),
    }


async def _test_setup_layout_at_80x24():
    async def body(app, page, pilot, source, listed, control):
        page_region = page.region
        list_region = page.query_one("#instance-list", compat.ListView).region
        setup_region = page.query_one("#setup", compat.Static).region
        flow = page.query_one("#setup-actions", compat.ButtonFlow).region
        boxes = {button_id: page.query_one(f"#{button_id}", compat.Button).region for button_id in SETUP_IDS}
        status = page.query_one("#status", compat.Static).region
        fields = page.query_one("#fields-pane", compat.VerticalScroll).content_region
        await pilot.press("q")
        return page_region, list_region, setup_region, flow, boxes, status, fields

    page_region, list_region, setup_region, flow, boxes, status, fields = await _with_page(body, size=(80, 24))
    rows = {box.y for box in boxes.values()}
    return (
        list_region.height - 2 >= 4
        and fields.height >= 6
        and setup_region.height == 2
        and _inside(flow, page_region)
        and _inside(status, page_region)
        and all(_inside(box, page_region) and box.height == 1 for box in boxes.values())
        # 按钮按可用宽度自动折行。
        and 1 <= len(rows) <= 3
        and min(box.y for box in boxes.values()) >= setup_region.bottom
        and status.y >= max(box.bottom for box in boxes.values())
    )


async def _test_compact_layout_and_resize():
    async def body(app, page, pilot, source, listed, control):
        results = []
        for width, height, minimum_lines in ((80, 24, 6), (60, 20, 2), (120, 40, 10)):
            await pilot.resize_terminal(width, height)
            await pilot.pause()
            fields = page.query_one("#fields-pane", compat.VerticalScroll)
            status = page.query_one("#status", compat.Static)
            buttons = [page.query_one(f"#{button_id}", compat.Button) for button_id in (*BUTTON_IDS, *SETUP_IDS)]
            instance_labels = [str(label.render()) for label in page.query("#instance-list Static")]
            results.append(
                fields.content_region.height >= minimum_lines
                and _inside(status.region, page.region)
                and all(_inside(button.region, page.region) and button.content_region.height >= 1 for button in buttons)
                and page.query_one("#instance-list", compat.ListView).content_region.height >= (2 if height < 24 else 4)
                and all(str(row.root) in label for row, label in zip(page.instance_rows, instance_labels, strict=True))
            )
            if width == 60:
                fields.scroll_end(animate=False)
                await pilot.pause()
                results.append(fields.scroll_offset.y > 0 and fields.is_vertical_scroll_end)
            if height == 40:
                results.append(all(_button(page, button_id).region.height == 3 for button_id in BUTTON_IDS))
        return all(results)

    return await _with_page(body, size=(120, 40))


async def _test_setup_buttons_wrap_when_narrow():
    # 窄终端下按钮折行后不得越出页面边界。
    async def body(app, page, pilot, source, listed, control):
        page_region = page.region
        boxes = {button_id: page.query_one(f"#{button_id}", compat.Button).region for button_id in SETUP_IDS}
        await pilot.press("q")
        return page_region, boxes

    page_region, boxes = await _with_page(body, size=(44, 24))
    return len({box.y for box in boxes.values()}) >= 2 and all(
        box.x >= page_region.x and box.right <= page_region.right for box in boxes.values()
    )


async def _test_local_setup_source_reads_doctor_and_placeholders():
    # 诊断统计通过 doctor --json 读取，占位符由 config placeholders --json 判定。
    calls: list[tuple[list[str], dict]] = []
    doctor = {
        "registry_available": True,
        "registry_note": "",
        "summary": {"error": 2, "warning": 1},
        "checks": {"unconfigured_adapters": ["telegram", "qqbot"]},
    }
    placeholders = {
        "tables": {"config": {"placeholder": 3, "total": 8}},
        "count": 3,
        "scanned": ["config"],
        "failed": {},
    }

    def runner(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        payload = doctor if "doctor" in argv else placeholders
        return SimpleNamespace(returncode=0, stdout=json.dumps(payload, ensure_ascii=False), stderr="")

    with TemporaryDirectory(prefix="akari-setup-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        (root / "config" / "config.toml").write_text('[config]\nkey = "<Replace me with str value>"\n', "utf-8")
        brief = LocalSetupSummarySource(root=root, runner=runner)
        summary = brief.summary()
    doctor_argv, doctor_options = calls[0]
    placeholders_argv, placeholders_options = calls[1]
    return (
        doctor_argv[3:] == ["doctor", "--json"]
        and placeholders_argv[3:] == ["config", "placeholders", "--json"]
        and doctor_options["cwd"] == str(root)
        and doctor_options["encoding"] == "utf-8"
        and doctor_options["env"]["AKARI_INSTANCE_DIR"] == str(root)
        and placeholders_options["cwd"] == str(root)
        and placeholders_options["env"]["AKARI_INSTANCE_DIR"] == str(root)
        and brief.calls["summary"] == 1
        and summary.unconfigured_adapters == 2
        and summary.doctor_errors == 2
        and summary.doctor_warnings == 1
        and summary.pending_placeholders == 3
        and summary.placeholders_estimated is False
        and summary.adapters_reason == ""
        and summary.doctor_reason == ""
        and summary.placeholders_reason == ""
    )


async def _test_local_setup_source_falls_back_to_estimate():
    # 统计命令失败时使用配置文本标记估算，并注明依据。
    # CLI 子进程可能重建共享语言快照，需重新连接测试快照。
    _use_cli_locale()
    doctor = {
        "registry_available": True,
        "registry_note": "",
        "summary": {"error": 0, "warning": 0},
        "checks": {"unconfigured_adapters": []},
    }

    def unreachable(argv, **kwargs):
        if "doctor" in argv:
            return SimpleNamespace(returncode=0, stdout=json.dumps(doctor), stderr="")
        raise OSError("no cli")

    def timed_out(argv, **kwargs):
        if "doctor" in argv:
            return SimpleNamespace(returncode=0, stdout=json.dumps(doctor), stderr="")
        raise subprocess.TimeoutExpired(cmd="akaribot", timeout=60.0)

    def garbled(argv, **kwargs):
        if "doctor" in argv:
            return SimpleNamespace(returncode=0, stdout=json.dumps(doctor), stderr="")
        return SimpleNamespace(returncode=0, stdout="不是 JSON", stderr="")

    with TemporaryDirectory(prefix="akari-setup-estimate-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        (root / "config" / "config.toml").write_text(
            '[config]\nkey = "<Replace me with str value>"\nnote = "见 <Replace me> 说明"\n# <Replace me>\n',
            "utf-8",
        )
        summaries = [LocalSetupSummarySource(root=root, runner=runner).summary() for runner in (unreachable, timed_out)]
        garbled_summary = LocalSetupSummarySource(root=root, runner=garbled).summary()
    timeout_detail = i18n.t("cli.tui.dashboard.setup_placeholders_timeout", seconds="60")
    unreadable = i18n.t("cli.tui.dashboard.setup_placeholders_unreadable", code=0)
    # 文本估算包含配置值、字符串和注释中的标记，因此计数为 3；core 仅计入有效配置值。
    return (
        all(summary.pending_placeholders == 3 and summary.placeholders_estimated is True for summary in summaries)
        and summaries[0].placeholders_reason
        == i18n.t("cli.tui.dashboard.setup_placeholders_estimated_reason", detail="OSError: no cli")
        and summaries[1].placeholders_reason
        == i18n.t("cli.tui.dashboard.setup_placeholders_estimated_reason", detail=timeout_detail)
        and garbled_summary.pending_placeholders == 3
        and garbled_summary.placeholders_estimated is True
        and unreadable in garbled_summary.placeholders_reason
        and "不是 JSON" in garbled_summary.placeholders_reason
    )


async def _test_local_setup_source_marks_uncounted_tables():
    # 部分表未纳入统计时保留已知计数，并明确说明覆盖范围。
    doctor = {
        "registry_available": True,
        "registry_note": "",
        "summary": {"error": 0, "warning": 0},
        "checks": {"unconfigured_adapters": []},
    }
    placeholders = {
        "tables": {"config": {"placeholder": 5, "total": 9}},
        "count": 5,
        "scanned": ["config"],
        "failed": {"binary": "读取失败：UnicodeDecodeError"},
    }

    def runner(argv, **kwargs):
        payload = doctor if "doctor" in argv else placeholders
        return SimpleNamespace(returncode=0, stdout=json.dumps(payload, ensure_ascii=False), stderr="")

    with TemporaryDirectory(prefix="akari-setup-partial-") as raw:
        summary = LocalSetupSummarySource(root=Path(raw), runner=runner).summary()
    return (
        summary.pending_placeholders == 5
        and summary.placeholders_estimated is False
        and summary.placeholders_reason
        == i18n.t("cli.tui.dashboard.setup_placeholders_partial_reason", count=1, tables="binary")
    )


async def _test_local_setup_source_degrades_per_item():
    # 子进程、输出解析或清单读取失败时分别报告原因；占位符使用注明依据的估算值。
    def unreachable(argv, **kwargs):
        raise OSError("no cli")

    def garbled(argv, **kwargs):
        return SimpleNamespace(returncode=1, stdout="不是 JSON", stderr="体检失败")

    unavailable = {
        "registry_available": False,
        "registry_note": "registry --json 不可用",
        "summary": {"error": 0, "warning": 0},
        "checks": {},
    }

    def no_registry(argv, **kwargs):
        return SimpleNamespace(returncode=0, stdout=json.dumps(unavailable, ensure_ascii=False), stderr="")

    with TemporaryDirectory(prefix="akari-setup-bad-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        broken = LocalSetupSummarySource(root=root, runner=unreachable).summary()
        unreadable = LocalSetupSummarySource(root=root, runner=garbled).summary()
        partial = LocalSetupSummarySource(root=root, runner=no_registry).summary()
    return (
        broken.unconfigured_adapters is None
        and broken.doctor_errors is None
        and "no cli" in broken.adapters_reason
        and unreadable.unconfigured_adapters is None
        and i18n.t("cli.tui.dashboard.setup_doctor_unreadable", code=1) in unreadable.doctor_reason
        and "体检失败" in unreadable.doctor_reason
        and partial.unconfigured_adapters is None
        and partial.adapters_reason == "registry --json 不可用"
        and partial.doctor_errors == 0
        and partial.doctor_warnings == 0
        and partial.pending_placeholders == 0
        and broken.placeholders_estimated is True
        and unreadable.placeholders_estimated is True
        and unreadable.placeholders_reason
        == i18n.t("cli.tui.dashboard.setup_placeholders_estimated_reason", detail="体检失败")
        and partial.placeholders_estimated is True
    )


async def _test_setup_actions_follow_busy_state():
    # 写操作不影响摘要展示；导航按钮按目标是否可用决定禁用状态。
    gate = threading.Event()
    runner = _RecordingRunner(on_run=lambda _args: gate.wait(2.0))

    async def body(app, page, pilot, source, listed, control):
        page.query_one("#instance-list", compat.ListView).index = 0
        await pilot.pause()
        _button(page, "autostart").press()
        started = await _wait_until(lambda: page._busy)
        disabled = {button_id: page.query_one(f"#{button_id}", compat.Button).disabled for button_id in SETUP_IDS}
        gate.set()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return started, disabled

    started, disabled = await _with_page(body, cli=runner)
    return started and disabled == {"goto-config": False, "goto-run": True, "goto-doctor": False}


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
    # 关闭防抖延迟，使交互用例无需等待；防抖行为由专项用例验证。
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
        await tester.test(_test_button_switch_matches_key, "按钮切换实例与键位同效")
        await tester.test(_test_button_new_instance_runs_init, "按钮新建实例弹输入框并执行 init")
        await tester.test(_test_button_add_instance_registers_directory, "按钮登记目录弹输入框并下发")
        await tester.test(_test_button_remove_instance_opens_confirm_modal, "按钮移除登记一次触发即弹确认框")
        await tester.test(_test_button_policy_toggles_send_cli_flags, "按钮翻转自启与崩溃重启")
        await tester.test(_test_button_service_opens_confirm_modal, "按钮装卸服务一次触发即弹确认框")
        await tester.test(_test_button_refresh_rereads_snapshot, "按钮刷新重新读取快照")
        await tester.test(_test_action_buttons_follow_state, "按钮禁用与标签跟着数据走")
        await tester.test(_test_action_buttons_disable_while_busy, "忙时禁用全部按钮")
        await tester.test(_test_action_buttons_share_one_row_when_wide, "宽终端下按钮只占一行")
        await tester.test(_test_action_buttons_wrap_after_remove_instance, "80 列下在移除登记后折行")
        await tester.test(_test_instances_caption_points_to_buttons, "说明行按条数插值后指向按钮")
        await tester.test(_test_instances_caption_drops_key_list, "说明行新文案不再逐条列键位")
        await tester.test(_test_setup_summary_renders_four_items, "首次使用摘要四项各自渲染")
        await tester.test(_test_setup_state_follows_snapshot, "摘要里的运行状态跟着探测结果")
        await tester.test(_test_setup_missing_values_say_missing, "取不到的摘要项写未取到并附原因")
        await tester.test(_test_setup_estimated_placeholders_are_labelled, "估算口径在摘要里标明并附原因")
        await tester.test(_test_setup_load_failure_degrades, "摘要取数失败只降级为逐项说明")
        await tester.test(_test_setup_loads_lazily_on_first_display, "摘要首次显示时取一次")
        await tester.test(_test_setup_buttons_jump_pages, "行动区按钮切到配置、运行与体检页")
        await tester.test(_test_setup_buttons_disabled_rules, "前提不满足时按钮置灰并写明原因")
        await tester.test(_test_setup_buttons_enabled_when_stopped, "实例停止时三个按钮都可用")
        await tester.test(_test_setup_layout_at_80x24, "80×24 下清单留 4 行且按钮与状态栏不出页")
        await tester.test(_test_compact_layout_and_resize, "短屏可读详情且全部按钮可见，放大后恢复布局")
        await tester.test(_test_setup_buttons_wrap_when_narrow, "窄终端下按钮按宽度折行")
        await tester.test(_test_setup_actions_follow_busy_state, "写动作进行时摘要按钮不跟着置灰")
        await tester.test(_test_local_setup_source_reads_doctor_and_placeholders, "默认数据源取体检统计与占位符")
        await tester.test(_test_local_setup_source_falls_back_to_estimate, "统计命令失败后退化为标明口径的估算")
        await tester.test(_test_local_setup_source_marks_uncounted_tables, "未纳入统计的表写进口径说明")
        await tester.test(_test_local_setup_source_degrades_per_item, "默认数据源逐项降级说明原因")
    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        await tester.test(_test_remove_gate_reset_on_page_reset, "reset_pending() 后同一目标可重新弹框")
    return tester
