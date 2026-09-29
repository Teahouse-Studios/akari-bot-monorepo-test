"""杂项页：只放不属于其它页面的一次性操作，目前是「迁移项目」。

页面平时只有一个按钮，点击后弹出输入框要旧项目路径；拿到路径后再从确认框里选「先预演」或
「开始迁移」。迁移会往实例里写配置与数据，故路径提交后还要在确认框里选一次才会执行，切页即作废。
按钮上方一行开关随 ``migrate legacy`` 下发，全不勾时 argv 不带这些参数。
"""

import asyncio
import subprocess
import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.dashboard import StaticDashboardSource
from akaribot.cli.tui.misc import (
    MIGRATE_SWITCHES,
    MiscSource,
    StaticMiscSource,
    SubprocessMiscSource,
    _option_id,
)
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


PROJECT = "/tmp/old-project"


async def _wait_until(predicate, timeout: float = 1.0) -> bool:
    # 模态框的关闭与 worker 的落地时刻不确定，用轮询等条件成立。
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(0.01)
    return False


async def _with_page(body, source: MiscSource | None = None, size=(120, 34)):
    chosen = source or StaticMiscSource()
    app = TuiApp(
        sources={"misc": chosen, "dashboard": StaticDashboardSource()},
        initial_page="misc",
        boot_started_at=time.monotonic(),
    )
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("misc")
        await pilot.pause()
        return await body(app, page, pilot, chosen)


async def _enter_path(app, page, pilot, path: str = PROJECT) -> None:
    page.request_migrate()
    await pilot.pause()
    app.screen.query_one("#prompt-input", compat.Input).value = path
    await pilot.press("enter")
    await _wait_until(lambda: not app.screen.query("#prompt-input"))


def _prompt_open(app) -> bool:
    return bool(app.screen.query("#prompt-input"))


async def _choose(app, pilot, index: int) -> None:
    # 按确认框里的第 index 个选项（0 先预演，1 开始迁移）；模态框关掉即回调已经执行。
    app.screen.query_one(f"#choice-{index}", compat.Button).press()
    await _wait_until(lambda: not app.screen.query("#choice-0"))
    await pilot.pause()


async def _test_page_offers_one_button():
    # 页面只放一个按钮，不常驻输入框。
    async def body(app, page, pilot, source):
        buttons = [child.id for child in page.query(compat.Button)]
        inputs = len(page.query(compat.Input))
        await pilot.press("q")
        return buttons, inputs

    buttons, inputs = await _with_page(body)
    return buttons == ["migrate"] and inputs == 0


async def _test_click_opens_prompt_and_cancel_is_safe():
    # 点击后弹出输入框；取消不会调用数据源。
    async def body(app, page, pilot, source):
        page.request_migrate()
        await pilot.pause()
        opened = len(app.screen_stack) > 1
        await pilot.press("escape")
        await pilot.pause()
        closed = len(app.screen_stack) == 1
        status = page.status_text
        await pilot.press("q")
        return opened, closed, status, list(source.migrated)

    opened, closed, status, migrated = await _with_page(body)
    return opened and closed and migrated == [] and status


async def _test_prompt_asks_before_migrating():
    # 输入路径后不立即执行：先弹确认框，选「开始迁移」才迁移。
    async def body(app, page, pilot, source):
        await _enter_path(app, page, pilot)
        asked = (list(source.migrated), page.status_text, page.pending_project, len(app.screen_stack) > 1)
        await _choose(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return asked, list(source.migrated)

    asked, migrated = await _with_page(body)
    return (
        asked[0] == []
        and asked[1] == i18n.t("cli.tui.misc.confirm_migrate_pending", project=PROJECT)
        and asked[2] == PROJECT
        and asked[3]
        and migrated == [(PROJECT, False, ())]
    )


async def _test_enter_key_submits_prompt():
    async def body(app, page, pilot, source):
        await _enter_path(app, page, pilot, "/tmp/other")
        pending = page.pending_project
        await pilot.press("escape")
        await pilot.pause()
        cleared = page.pending_project
        await pilot.press("q")
        return pending, cleared

    pending, cleared = await _with_page(body)
    return pending == "/tmp/other" and cleared == ""


async def _test_cancel_choice_clears_pending():
    # 确认框取消后路径作废：再按 m 重新要路径，不会拿旧路径直接迁移。
    async def body(app, page, pilot, source):
        await _enter_path(app, page, pilot)
        await pilot.press("escape")
        await pilot.pause()
        cleared = page.pending_project
        page.request_migrate()
        await pilot.pause()
        reopened = _prompt_open(app)
        await pilot.press("escape")
        await pilot.press("q")
        return cleared, reopened, list(source.migrated)

    cleared, reopened, migrated = await _with_page(body)
    return cleared == "" and reopened and migrated == []


async def _test_switch_page_clears_pending_path():
    # 待确认状态随切页作废：切回本页再按 m 必须重新输入路径。
    async def body(app, page, pilot, source):
        await _enter_path(app, page, pilot)
        await _choose(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        armed = page.pending_project
        app.show_page("dashboard")
        await pilot.pause()
        after_switch = page.pending_project
        app.show_page("misc")
        await pilot.pause()
        page.request_migrate()
        await pilot.pause()
        reopened = _prompt_open(app)
        await pilot.press("escape")
        await pilot.press("q")
        return armed, after_switch, reopened, list(source.migrated)

    armed, after_switch, reopened, migrated = await _with_page(body)
    return armed == PROJECT and after_switch == "" and reopened and migrated == [(PROJECT, True, ())]


async def _test_dry_run_option_prints_plan():
    plan = ("计划：复制 config/config.toml", "计划：复制 data/dice.db", "计划：写入 migration-report.md")
    source = StaticMiscSource(
        OperationResult(
            True,
            i18n.t("cli.tui.common.op_ok", label=i18n.t("cli.tui.misc.label_dry_run")),
            "\n".join(plan),
        )
    )

    async def body(app, page, pilot, chosen):
        await _enter_path(app, page, pilot)
        await _choose(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        output = page.output_text
        status = page.status_text
        await pilot.press("q")
        return output, status, list(chosen.migrated)

    output, status, migrated = await _with_page(body, source)
    return (
        migrated == [(PROJECT, True, ())]
        and all(line in output for line in plan)
        and i18n.t("cli.tui.misc.label_dry_run") in status
    )


async def _test_confirm_within_debounce_is_ignored():
    # 提交路径后紧接着选「开始迁移」属连发，不算确认：闸门挡下，迁移不执行。
    async def body(app, page, pilot, source):
        await _enter_path(app, page, pilot)
        await _choose(app, pilot, 1)
        await pilot.pause()
        observed = (page.status_text, list(source.migrated), page.pending_project)
        await pilot.press("escape")
        await pilot.press("q")
        return observed

    with mock.patch.object(compat.PendingConfirm, "debounce", 10.0):
        status, migrated, pending = await _with_page(body)
    return (
        migrated == []
        and pending == PROJECT
        and status == i18n.t("cli.tui.misc.confirm_migrate_again", project=PROJECT)
    )


async def _test_failure_keeps_page_usable():
    source = StaticMiscSource(OperationResult(False, "迁移失败", "boom"))

    async def body(app, page, pilot, chosen):
        await _enter_path(app, page, pilot, "/tmp/old")
        await _choose(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        page.request_migrate()
        await pilot.pause()
        reopened = bool(app.screen.query("#choice-0"))
        await pilot.press("escape")
        await pilot.press("q")
        return status, reopened, list(chosen.migrated)

    status, reopened, migrated = await _with_page(body, source)
    return "迁移失败" in status and "boom" in status and reopened and migrated == [("/tmp/old", False, ())]


async def _test_output_panel_hidden_until_output():
    async def body(app, page, pilot, source):
        hidden = page.query_one("#migrate-output", compat.Static).display
        await pilot.press("q")
        return hidden, page.output_text

    hidden, output = await _with_page(body)
    return hidden is False and output == ""


def _test_pending_confirm_windows():
    # 闸门自身的窗口：两次触发相隔不足防抖窗口时忽略后一次，换目标或复位后立即放行。
    with mock.patch.object(compat.PendingConfirm, "debounce", compat.CONFIRM_DEBOUNCE_SECONDS):
        gate = compat.PendingConfirm()
        accepted = gate.accept("x", now=100.0)
        debounced = gate.accept("x", now=100.1)
        again = gate.accept("x", now=101.0)
        other = gate.accept("y", now=200.0)
        gate.reset()
        after_reset = gate.accept("y", now=200.0)

    return accepted and not debounced and again and other and after_reset


def _test_subprocess_source_appends_dry_run_and_switches():
    recorded = []

    def runner(argv, **kwargs):
        recorded.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, stdout="计划：写入 migration-report.md", stderr="")

    source = SubprocessMiscSource(root="/tmp/inst", timeout=5.0, runner=runner)
    real = source.migrate_legacy("/tmp/old")
    dry = source.migrate_legacy("/tmp/old", dry_run=True)
    checked = source.migrate_legacy("/tmp/old", dry_run=True, flags=("--force", "--offline"))
    argv, kwargs = recorded[0]
    target = ("--instance", str(source.root))
    return (
        argv == cli_process.cli_argv("migrate", "legacy", "/tmp/old", *target)
        and recorded[1][0] == cli_process.cli_argv("migrate", "legacy", "/tmp/old", *target, "--dry-run")
        and recorded[2][0]
        == cli_process.cli_argv("migrate", "legacy", "/tmp/old", *target, "--dry-run", "--force", "--offline")
        and kwargs["cwd"] == str(source.root)
        and kwargs["env"]["AKARI_INSTANCE_DIR"] == str(source.root)
        and real.ok
        and dry.ok
        and checked.ok
        and "计划" in dry.detail
        and source.calls["migrate"] == 3
    )


async def _test_option_row_lists_switches():
    # 四个开关一行排开，默认全不勾；空选择让 argv 不带任何多余参数。
    async def body(app, page, pilot, source):
        row = page.query_one("#migrate-options")
        observed = []
        for flag, label_key in MIGRATE_SWITCHES:
            checkbox = page.query_one(f"#{_option_id(flag)}", compat.Checkbox)
            observed.append(
                (
                    checkbox.value,
                    str(checkbox.label),
                    checkbox.region.right <= row.region.right,
                    checkbox.render_line(0).text.strip(),
                )
            )
        await pilot.press("q")
        return observed, page.selected_flags, row.region

    observed, selected, row_region = await _with_page(body, size=(80, 24))
    return (
        [item[0] for item in observed] == [False, False, False, False]
        and [item[1] for item in observed] == [i18n.t(key) for _, key in MIGRATE_SWITCHES]
        and all(item[2] for item in observed)
        and all(i18n.t(key) in item[3] for item, (_, key) in zip(observed, MIGRATE_SWITCHES))
        and all("{I18N" not in item[3] for item in observed)
        and selected == ()
        and row_region.height == 1
    )


async def _test_confirm_hint_lists_switches():
    # 确认模态框里列出本次将下发的开关；没勾选时写明没有附加开关。
    async def body(app, page, pilot, source):
        page.query_one("#option-force", compat.Checkbox).value = True
        page.query_one("#option-skip-install", compat.Checkbox).value = True
        await pilot.pause()
        selected = page.selected_flags
        await _enter_path(app, page, pilot)
        hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await pilot.press("escape")
        await pilot.pause()
        page.query_one("#option-force", compat.Checkbox).value = False
        page.query_one("#option-skip-install", compat.Checkbox).value = False
        await pilot.pause()
        await _enter_path(app, page, pilot)
        empty_hint = str(app.screen.query_one("#choice-hint", compat.Static).render())
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return selected, hint, empty_hint

    selected, hint, empty_hint = await _with_page(body)
    return (
        selected == ("--skip-install", "--force")
        and i18n.t("cli.tui.misc.choice_options", options="--skip-install --force") in hint
        and i18n.t("cli.tui.misc.choice_hint", project=PROJECT) in hint
        and i18n.t("cli.tui.misc.choice_options", options=i18n.t("cli.tui.misc.choice_options_none")) in empty_hint
        and "--force" not in empty_hint
    )


async def _test_switches_ride_along_with_dispatch():
    # 勾选的开关随每次下发：先预演与真正迁移带的是同一份集合，顺序与界面一致。
    async def body(app, page, pilot, source):
        page.query_one("#option-offline", compat.Checkbox).value = True
        page.query_one("#option-no-venv", compat.Checkbox).value = True
        await pilot.pause()
        await _enter_path(app, page, pilot)
        await _choose(app, pilot, 0)
        await page.wait_for_idle()
        await pilot.pause()
        dry_run_call = list(source.migrated)
        # 预演不作废路径：再按一次 m 直接回到确认框，不必重输。
        page.request_migrate()
        await _wait_until(lambda: bool(app.screen.query("#choice-0")))
        await pilot.pause()
        await _choose(app, pilot, 1)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return dry_run_call, list(source.migrated)

    dry_run_call, migrated = await _with_page(body)
    flags = ("--no-venv", "--offline")
    return dry_run_call == [(PROJECT, True, flags)] and migrated == [(PROJECT, True, flags), (PROJECT, False, flags)]


@func_case
async def test_tui_misc(tester: Tester):
    """cli.tui.misc: 迁移项目的按钮、确认与预演测试"""
    _use_cli_locale()
    # 用例里的两次按键相隔只有几毫秒，压缩防抖窗口，免得每条确认都等 0.4 秒。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_page_offers_one_button, "页面只放一个按钮")
        await tester.test(_test_click_opens_prompt_and_cancel_is_safe, "点击弹出输入框且取消安全")
        await tester.test(_test_prompt_asks_before_migrating, "输入路径后仍需确认")
        await tester.test(_test_enter_key_submits_prompt, "回车提交输入框")
        await tester.test(_test_cancel_choice_clears_pending, "确认框取消后路径作废")
        await tester.test(_test_switch_page_clears_pending_path, "切页作废待确认的路径")
        await tester.test(_test_dry_run_option_prints_plan, "先预演只回显计划")
        await tester.test(_test_confirm_within_debounce_is_ignored, "防抖窗口内的确认被忽略")
        await tester.test(_test_failure_keeps_page_usable, "迁移失败后界面仍可用")
        await tester.test(_test_output_panel_hidden_until_output, "无输出时输出区不占屏幕")
        await tester.test(_test_option_row_lists_switches, "开关行默认全不勾且在 80 列内完整可见")
        await tester.test(_test_confirm_hint_lists_switches, "确认框列出本次将下发的开关")
        await tester.test(_test_switches_ride_along_with_dispatch, "勾选的开关随预演与迁移一起下发")
        await tester.test(_test_subprocess_source_appends_dry_run_and_switches, "生产数据源追加 --dry-run 与勾选的开关")
    await tester.test(_test_pending_confirm_windows, "确认闸门的防抖与超时窗口")
    return tester
