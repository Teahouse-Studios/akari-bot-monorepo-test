"""环境页：托管方式、环境里装了什么、清单里记了什么，以及装卸与三个解释器动作。

环境是实例级信息，单独一页展示：页面上半是托管方式、解释器、包数量与选中项，下半是包清单（含
httpx 这类传递依赖），底部按性质分两行——包装卸与解释器动作。装卸分两种去处：写进实例清单
（环境重建时补装）与只装进当前环境；三个解释器动作会换掉解释器，实例运行期间一律拒绝。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.environment import (
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


# 把高亮移到指定分发那一行。
def _select(page, dist: str) -> None:
    index = next(position for position, row in enumerate(page.visible_packages) if row.dist == dist)
    page.query_one("#package-list", compat.ListView).index = index


async def _test_lists_every_installed_package():
    # 页面要回答「环境里装了什么」：连 httpx 这类传递依赖也在列，标记区分清单记录与其它。
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
    # 记录在清单里却没装上的（例如只从环境卸载过）要看得见，否则用户不知道重建时会补装什么。
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
    # 装运行库要先问去处：写进清单的会在重建时补装，只装进环境的不会。
    async def body(app, page, pilot, source):
        page.request_install()
        await pilot.pause()
        app.screen.query_one("#prompt-input", compat.Input).value = "httpx"
        await pilot.press("enter")
        await pilot.pause()
        labels = [str(button.label) for button in app.screen.query("#choice-actions Button")]
        await pilot.click("#choice-0")
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
        await pilot.click("#choice-1")
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
        await pilot.click("#choice-1")
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


async def _test_uninstall_plain_package_needs_two_presses():
    # 没记在清单里的包（传递依赖是这种）只有一种去处，连按两次确认即可。
    async def body(app, page, pilot, source):
        _select(page, "certifi")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        armed = page.status_text
        first = list(source.package_calls)
        page.request_uninstall()
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return armed, first, list(source.package_calls)

    armed, first, second = await _with_page(body)
    return (
        i18n.t("cli.tui.environment.uninstall_confirm", dist="certifi") == armed
        and first == []
        and second == [PackageCall("remove", "certifi", False)]
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
    # 装卸只动 site-packages，运行期间允许，但已经 import 的模块要重启实例才换版本。
    source = _source(running=True)

    async def body(app, page, pilot, source):
        _select(page, "certifi")
        await pilot.pause()
        page.request_uninstall()
        await pilot.pause()
        page.request_uninstall()
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

    # 模式读不到时不能当成「外部解释器」展示：那会让人以为可以接管。
    text = await _with_page(fields_body, _source(state=EnvironmentState()))
    return (
        managed == ["release", "recreate"]
        and external == ["adopt"]
        and unknown == []
        and i18n.t("cli.tui.environment.mode_unknown") in text
    )


async def _test_action_needs_two_presses():
    async def body(app, page, pilot, source):
        page.request_action("recreate")
        await pilot.pause()
        first = list(source.actions), page.status_text
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return first, list(source.actions)

    first, second = await _with_page(body)
    return first[0] == [] and first[1] and second == ["recreate"]


async def _test_switching_action_asks_again():
    async def body(app, page, pilot, source):
        page.request_action("release")
        await pilot.pause()
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("release")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return list(source.actions)

    actions = await _with_page(body)
    return actions == []


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
    # 快捷键绕过隐藏也能按到，此时必须拒绝，而不是跑一个注定失败的命令。
    async def body(app, page, pilot, source):
        page.request_action("adopt")
        await pilot.pause()
        adopted = list(source.actions)
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        await pilot.press("q")
        return adopted, list(source.actions)

    adopted, rebuilt = await _with_page(body)
    return adopted == [] and rebuilt == ["recreate"]


async def _test_failure_reports_detail_and_reloads():
    source = _source(action_result=OperationResult(False, "重建失败", "boom"))

    async def body(app, page, pilot, source):
        before = source.calls["state"]
        page.request_action("recreate")
        await pilot.pause()
        page.request_action("recreate")
        await page.wait_for_idle()
        await pilot.pause()
        # 动作结束后会重新读取一次；后台任务注册有延迟，轮询到计数变化为止。
        deadline = time.monotonic() + 5.0
        while source.calls["state"] <= before and time.monotonic() < deadline:
            await pilot.pause()
        status = page.status_text
        after = source.calls["state"]
        await pilot.press("q")
        return status, after, before

    status, after, before = await _with_page(body, source)
    return "重建失败" in status and "boom" in status and after > before


@func_case
async def test_tui_environment(tester: Tester):
    """cli.tui.environment: 环境清单、包装卸与环境动作测试"""
    _use_cli_locale()
    await tester.test(_test_lists_every_installed_package, "列出环境里的全部分发（含传递依赖）")
    await tester.test(_test_search_and_filter_narrow_the_list, "搜索与「只看清单里的」收窄清单")
    await tester.test(_test_recorded_but_missing_row_is_listed, "清单里记着但没装上的条目也在列")
    await tester.test(_test_package_probe_failure_degrades, "包列表探测失败只降级")
    await tester.test(_test_install_choice_decides_recording, "安装先选去处：写进清单")
    await tester.test(_test_install_env_only_skips_recording, "安装先选去处：只装进环境")
    await tester.test(_test_install_cancelled_by_empty_spec, "取消安装不调用子进程")
    await tester.test(_test_uninstall_recorded_package_offers_modes, "卸载已记录的包可选是否删记录")
    await tester.test(_test_uninstall_plain_package_needs_two_presses, "卸载普通包连按两次确认")
    await tester.test(_test_uninstall_needs_selection, "没有选中项时拒绝卸载")
    await tester.test(_test_package_change_while_running_notes_restart, "运行期间装卸提示重启生效")
    await tester.test(_test_selected_package_shows_dependents, "选中项显示被谁依赖")
    await tester.test(_test_only_applicable_action_is_offered, "只放出当前模式适用的动作")
    await tester.test(_test_action_needs_two_presses, "环境动作连按两次确认")
    await tester.test(_test_switching_action_asks_again, "换动作后重新确认且不执行")
    await tester.test(_test_refused_while_running, "实例运行中拒绝环境动作")
    await tester.test(_test_inapplicable_action_refused, "不适用的动作被拒绝")
    await tester.test(_test_failure_reports_detail_and_reloads, "失败时给出原因并重新读取")

    return tester
