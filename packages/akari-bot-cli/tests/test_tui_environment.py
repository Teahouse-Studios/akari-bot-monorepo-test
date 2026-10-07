"""环境页的包列表、安装方式、实例清单与解释器操作测试。"""

import time
from unittest import mock

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.environment import (
    DRY_RUN_SUFFIX,
    EnvironmentPackage,
    EnvironmentState,
    PackageCall,
    StaticEnvironmentSource,
)
from akaribot.cli.tui.modules import OperationResult
from akaribot.testing import Tester, func_case

PACKAGES = (
    EnvironmentPackage("akari-bot-core", "0.1.0", akari=True, requires=("httpx>=0.27",)),
    EnvironmentPackage(
        "akari-bot-module-wiki",
        "0.2.0",
        editable=True,
        akari=True,
        groups=("akaribot.modules",),
    ),
    EnvironmentPackage("httpx", "0.28.1", recorded=True),
    EnvironmentPackage("certifi", "2025.1.31"),
)

REQUIREMENTS = ("httpx>=0.27",)


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _source(**kwargs) -> StaticEnvironmentSource:
    params = {
        "state": EnvironmentState(
            mode="managed",
            python="/tmp/inst/.venv/bin/python",
            venv_dir="/tmp/inst/.venv",
            ready=True,
            packages=PACKAGES,
            core_version="0.1.0",
            requirements=REQUIREMENTS,
        )
    }
    params.update(kwargs)
    return StaticEnvironmentSource(**params)


async def _with_page(body, source=None, size=(120, 34)):
    chosen = source if source is not None else _source()
    app = TuiApp(sources={"environment": chosen}, initial_page="environment", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("environment")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot, chosen)


def _shown(page) -> list[str]:
    return [kind for kind in ("adopt", "release", "recreate") if page.query_one(f"#{kind}", compat.Button).display]


def _select(page, dist: str) -> None:
    index = next(position for position, row in enumerate(page.visible_packages) if row.dist == dist)
    page.query_one("#package-list", compat.ListView).index = index


async def _test_lists_every_installed_package():
    # 包列表包含 httpx 等传递依赖，并区分实例清单记录。
    async def body(app, page, pilot, source):
        rows = page.rows
        fields = str(page.query_one("#fields", compat.Static).render())
        columns = page.column_text
        await pilot.press("q")
        return rows, fields, columns

    rows, fields, columns = await _with_page(body)
    joined = "\n".join(rows)
    return (
        len(rows) == 4
        and "httpx" in joined
        and "0.28.1" in joined
        and any(row.startswith("●") and "httpx" in row for row in rows)
        and i18n.t("cli.tui.environment.tag_module") in joined
        and i18n.t("cli.tui.environment.tag_editable") in joined
        and i18n.t("cli.tui.environment.column_name") in columns
        and i18n.t("cli.tui.environment.package_count", count=4) in fields
        and i18n.t("cli.tui.environment.requirement_count", count=1) in fields
        and i18n.t("cli.tui.environment.mode_managed", venv="/tmp/inst/.venv") in fields
    )


async def _test_search_and_filter_narrow_the_list():
    async def body(app, page, pilot, source):
        page.set_query("module")
        await pilot.pause()
        narrowed = page.rows
        page.set_query("")
        await pilot.pause()
        restored = len(page.rows)
        page.set_recorded_only(True)
        await pilot.pause()
        recorded = [package.dist for package in page.visible_packages]
        await pilot.press("q")
        return narrowed, restored, recorded

    narrowed, restored, recorded = await _with_page(body)
    return len(narrowed) == 1 and "akari-bot-module-wiki" in narrowed[0] and restored == 4 and recorded == ["httpx"]


async def _test_recorded_but_missing_row_is_listed():
    # 清单中的未安装包应保持可见，以说明重建环境时的安装范围。
    state = EnvironmentState(
        mode="managed",
        python="/tmp/inst/.venv/bin/python",
        venv_dir="/tmp/inst/.venv",
        ready=True,
        packages=(EnvironmentPackage("httpx", "0.28.1", recorded=True),),
        requirements=("httpx>=0.27", "akari-bot-assets-emotes @ file:///tmp/emotes"),
    )

    async def body(app, page, pilot, source):
        rows = page.rows
        page.set_recorded_only(True)
        await pilot.pause()
        recorded = [package.dist for package in page.visible_packages]
        await pilot.press("q")
        return rows, recorded

    rows, recorded = await _with_page(body, _source(state=state))
    return (
        any(i18n.t("cli.tui.environment.tag_missing") in row for row in rows)
        and "akari-bot-assets-emotes" in recorded
        and recorded == ["akari-bot-assets-emotes", "httpx"]
    )


async def _test_package_probe_failure_degrades():
    source = _source(state=EnvironmentState(mode="managed", python="/tmp/inst/.venv/bin/python", packages=None))

    async def body(app, page, pilot, source):
        rows = page.rows
        fields = str(page.query_one("#fields", compat.Static).render())
        await pilot.press("q")
        return rows, fields

    rows, fields = await _with_page(body, source)
    return rows == () and i18n.t("cli.tui.environment.probe_failed") in fields


async def _test_install_choice_decides_recording():
    # 安装前需选择是否写入实例清单，以确定环境重建时是否恢复安装。
    async def body(app, page, pilot, source):
        page.request_install()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "httpx"
        await pilot.press("enter")
        await pilot.pause()
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        app.screen.query_one("#choice-0", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, list(source.package_calls)

    labels, calls = await _with_page(body)
    return i18n.t("cli.tui.environment.install_to_manifest") in labels and calls == [PackageCall("add", "httpx", True)]


async def _test_install_env_only_skips_recording():
    async def body(app, page, pilot, source):
        page.request_install()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "git+https://github.com/psf/requests"
        await pilot.press("enter")
        await pilot.pause()
        app.screen.query_one("#choice-1", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.package_calls)

    calls = await _with_page(body)
    return calls == [PackageCall("add", "git+https://github.com/psf/requests", False)]


async def _test_install_cancelled_by_empty_spec():
    async def body(app, page, pilot, source):
        page.request_install()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        status = page.status_text
        calls = list(source.package_calls)
        await pilot.press("q")
        return status, calls

    status, calls = await _with_page(body)
    return calls == [] and status == i18n.t("cli.tui.environment.install_cancelled")


async def _test_uninstall_recorded_package_offers_modes():
    async def body(app, page, pilot, source):
        _select(page, "httpx")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        app.screen.query_one("#choice-1", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return labels, list(source.package_calls)

    labels, calls = await _with_page(body)
    return (
        i18n.t("cli.tui.environment.uninstall_drop_record") in labels
        and i18n.t("cli.tui.environment.uninstall_keep_record") in labels
        and calls == [PackageCall("remove", "httpx", True)]
    )


async def _test_uninstall_plain_package_opens_confirm():
    # 未登记在实例清单中的包仍需确认卸载。
    async def body(app, page, pilot, source):
        _select(page, "certifi")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        opened = type(app.screen).__name__
        hint = str(app.screen.query_one("#choice-hint", compat.Static).content)
        before = list(source.package_calls)
        app.screen.query_one("#choice-0", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return opened, hint, before, list(source.package_calls)

    opened, hint, before, after = await _with_page(body)
    return (
        opened == "ChoiceScreen"
        and hint == i18n.t("cli.tui.environment.uninstall_confirm", dist="certifi")
        and before == []
        and after == [PackageCall("remove", "certifi", False)]
    )


async def _test_uninstall_needs_selection():
    async def body(app, page, pilot, source):
        page.set_query("nothing-matches")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        status = page.status_text
        await pilot.press("q")
        return status, list(source.package_calls)

    status, calls = await _with_page(body)
    return calls == [] and status == i18n.t("cli.tui.environment.no_selection")


async def _test_package_change_while_running_notes_restart():
    # 运行期间允许修改 site-packages，已导入模块需重启实例后更新。
    source = _source(running=True)

    async def body(app, page, pilot, source):
        _select(page, "certifi")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        app.screen.query_one("#choice-0", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        status = page.status_text
        calls = list(source.package_calls)
        await pilot.press("q")
        return status, calls

    label = i18n.t("cli.tui.environment.label_remove_package", dist="certifi")
    status, calls = await _with_page(body, source)
    return (
        calls == [PackageCall("remove", "certifi", False)]
        and i18n.t("cli.tui.environment.restart_needed", label=label) in status
    )


async def _test_selected_package_shows_dependents():
    async def body(app, page, pilot, source):
        _select(page, "httpx")
        await pilot.pause()
        fields = str(page.query_one("#fields", compat.Static).render())
        await pilot.press("q")
        return fields

    fields = await _with_page(body)
    return i18n.t("cli.tui.environment.selected_depended_by", names="akari-bot-core") in fields


async def _test_only_applicable_action_is_offered():
    async def body(app, page, pilot, source):
        shown = _shown(page)
        await pilot.press("q")
        return shown

    managed = await _with_page(body)
    external = await _with_page(
        body, _source(state=EnvironmentState(mode="external", python="/usr/bin/python3", ready=True, packages=()))
    )
    unknown = await _with_page(body, _source(state=EnvironmentState()))

    async def fields_body(app, page, pilot, source):
        text = str(page.query_one("#fields", compat.Static).render())
        await pilot.press("q")
        return text

    # 无法识别管理模式时应标记未知，避免误导用户执行接管。
    text = await _with_page(fields_body, _source(state=EnvironmentState()))
    return (
        managed == ["release", "recreate"]
        and external == ["adopt"]
        and unknown == []
        and i18n.t("cli.tui.environment.mode_unknown") in text
    )


async def _submit_recreate_confirmation(app, pilot):
    app.screen.query_one("#prompt-input", compat.Input).value = i18n.t("cli.tui.environment.recreate_token")
    await pilot.press("enter")
    await pilot.pause()


async def _test_action_asks_before_running():
    async def body(app, page, pilot, source):
        page.request_action("recreate")
        await pilot.pause()
        asked = type(app.screen).__name__
        before = list(source.actions)
        app.screen.query_one("#choice-0", compat.Button).press()
        await pilot.pause()
        typed = type(app.screen).__name__
        pending = list(source.actions)
        await _submit_recreate_confirmation(app, pilot)
        await page.wait_for_idle()
        await pilot.pause()
        return asked, before, typed, pending, list(source.actions)

    asked, before, typed, pending, after = await _with_page(body)
    return (
        asked == "ChoiceScreen"
        and before == []
        and typed == "TextPromptScreen"
        and pending == []
        and after == ["recreate"]
    )


async def _test_recreate_rejects_unconfirmed_input():
    async def body(app, page, pilot, source):
        for value in ("incorrect", None):
            page.request_action("recreate")
            await pilot.pause()
            app.screen.query_one("#choice-0", compat.Button).press()
            await pilot.pause()
            if value is None:
                await pilot.press("escape")
            else:
                app.screen.query_one("#prompt-input", compat.Input).value = value
                await pilot.press("enter")
            await pilot.pause()
            if source.actions:
                return False
        return True

    return await _with_page(body)


async def _test_recreate_rechecks_runtime_after_confirmation():
    async def body(app, page, pilot, source):
        page.request_action("recreate")
        await pilot.pause()
        app.screen.query_one("#choice-0", compat.Button).press()
        await pilot.pause()
        page._running = True
        await _submit_recreate_confirmation(app, pilot)
        await page.wait_for_idle()
        return not source.actions

    return await _with_page(body)


async def _test_action_dry_run_option():
    # 预览通过 --dry-run 执行，并在操作记录中标记。
    async def body(app, page, pilot, source):
        page.request_action("recreate")
        await pilot.pause()
        app.screen.query_one("#choice-1", compat.Button).press()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.actions)

    actions = await _with_page(body)
    return actions == [f"recreate{DRY_RUN_SUFFIX}"]


async def _test_cancelled_action_does_nothing():
    # 取消后不执行操作，再次触发时重新确认。
    async def body(app, page, pilot, source):
        page.request_action("release")
        await pilot.pause()
        await pilot.press("escape")
        await page.wait_for_idle()
        await pilot.pause()
        cancelled = list(source.actions)
        page.request_action("release")
        await pilot.pause()
        asked = type(app.screen).__name__
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("q")
        return cancelled, asked, list(source.actions)

    cancelled, asked, after = await _with_page(body)
    return cancelled == [] and asked == "ChoiceScreen" and after == []


async def _test_refused_while_running():
    source = _source(running=True)

    async def body(app, page, pilot, source):
        before = page.status_text
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.actions), page.status_text == before

    actions, untouched = await _with_page(body, source)
    return actions == [] and untouched


async def _test_inapplicable_action_refused():
    # 隐藏按钮的快捷键仍可能触发，操作入口必须校验前置条件。
    async def body(app, page, pilot, source):
        page.request_action("adopt")
        await pilot.pause()
        adopted, modal = list(source.actions), type(app.screen).__name__
        page.request_action("recreate")
        await pilot.pause()
        app.screen.query_one("#choice-0", compat.Button).press()
        await pilot.pause()
        await _submit_recreate_confirmation(app, pilot)
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return adopted, modal, list(source.actions)

    adopted, modal, rebuilt = await _with_page(body)
    return adopted == [] and modal == "Screen" and rebuilt == ["recreate"]


async def _test_failure_reports_detail_and_reloads():
    source = _source(action_result=OperationResult(False, "重建失败", "boom"))

    async def body(app, page, pilot, source):
        before = source.calls["state"]
        page.request_action("recreate")
        await pilot.pause()
        app.screen.query_one("#choice-0", compat.Button).press()
        await pilot.pause()
        await _submit_recreate_confirmation(app, pilot)
        await page.wait_for_idle()
        await pilot.pause()
        # 操作结束后重新读取；轮询计数以等待后台任务完成。
        deadline = time.monotonic() + 5.0
        while source.calls["state"] <= before and time.monotonic() < deadline:
            await pilot.pause()
        status = page.status_text
        after = source.calls["state"]
        await pilot.press("q")
        return status, after, before

    status, after, before = await _with_page(body, source)
    return "重建失败" in status and "boom" in status and after > before


async def _test_narrow_layout_keeps_package_list_usable():
    async def body(app, page, pilot, source):
        for width, height in ((80, 24), (60, 20), (120, 34)):
            await pilot.resize_terminal(width, height)
            await pilot.pause()
            widgets = [widget for widget in page.query("#actions Button") if widget.display]
            widgets.extend(
                page.query(selector).first() for selector in ("#package-search", "#recorded-only", "#status")
            )
            if any(not page.region.contains_region(widget.region) for widget in widgets):
                return False
            search = page.query_one("#package-search", compat.Input)
            if search.content_region.width < 10:
                return False
            list_view = page.query_one("#package-list", compat.ListView)
            if list_view.content_region.height < (4 if height >= 24 else 3):
                return False
            page.set_query("httpx")
            await pilot.pause()
            if len(page.visible_packages) != 1:
                return False
            page.set_query("")
            await pilot.pause()
        return True

    return await _with_page(body)


@func_case
async def test_tui_environment(tester: Tester):
    """cli.tui.environment: 环境清单、包装卸与环境动作测试"""
    _use_cli_locale()
    # 交互用例关闭防抖延迟，重复触发保护由专项用例验证。
    with mock.patch.object(compat.PendingConfirm, "debounce", 0.0):
        await tester.test(_test_lists_every_installed_package, "列出环境里的全部分发（含传递依赖）")
        await tester.test(_test_search_and_filter_narrow_the_list, "搜索与「只看清单里的」收窄清单")
        await tester.test(_test_recorded_but_missing_row_is_listed, "清单里记着但没装上的条目也在列")
        await tester.test(_test_package_probe_failure_degrades, "包列表探测失败只降级")
        await tester.test(_test_install_choice_decides_recording, "安装先选去处：写进清单")
        await tester.test(_test_install_env_only_skips_recording, "安装先选去处：只装进环境")
        await tester.test(_test_install_cancelled_by_empty_spec, "取消安装不调用子进程")
        await tester.test(_test_uninstall_recorded_package_offers_modes, "卸载已记录的包可选是否删记录")
        await tester.test(_test_uninstall_plain_package_opens_confirm, "卸载普通包也弹确认框")
        await tester.test(_test_uninstall_needs_selection, "没有选中项时拒绝卸载")
        await tester.test(_test_package_change_while_running_notes_restart, "运行期间装卸提示重启生效")
        await tester.test(_test_selected_package_shows_dependents, "选中项显示被谁依赖")
        await tester.test(_test_only_applicable_action_is_offered, "只放出当前模式适用的动作")
        await tester.test(_test_action_asks_before_running, "重建环境须先选择执行，再输入确认")
        await tester.test(_test_recreate_rejects_unconfirmed_input, "重建输入错误或取消均不执行")
        await tester.test(_test_recreate_rechecks_runtime_after_confirmation, "输入确认后重新检查运行状态")
        await tester.test(_test_narrow_layout_keeps_package_list_usable, "窄屏保留包列表、搜索框与所有操作按钮")
        await tester.test(_test_action_dry_run_option, "预演选项把 --dry-run 交给 CLI")
        await tester.test(_test_cancelled_action_does_nothing, "取消后不动作，再按仍先问")
        await tester.test(_test_refused_while_running, "实例运行中拒绝环境动作")
        await tester.test(_test_inapplicable_action_refused, "不适用的动作被拒绝")
        await tester.test(_test_failure_reports_detail_and_reloads, "失败时给出原因并重新读取")

        return tester
