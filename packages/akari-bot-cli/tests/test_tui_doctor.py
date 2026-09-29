"""体检页：结论列表、检查项统计、重新体检与跳转处理页面。

本文件固定四条链路：状态栏汇总 error/warning 与实现来源；退出码 1 但 stdout 仍是完整 JSON 时结论
照常展示；取数失败只在状态栏给出原因，界面不崩；回车按结论种类切到对应处理页面。新文案键尚未并入
locales 时先从片段合并一份语言快照，故断言取到的插值文案是真实渲染结果。
"""

import json
import os
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui.adapters import StaticAdapterSource
from akaribot.cli.tui.app import TuiApp
from akaribot.cli.tui.config import StaticConfigSource
from akaribot.cli.tui.dashboard import StaticDashboardSource
from akaribot.cli.tui.doctor import (
    DoctorChecks,
    DoctorConflict,
    DoctorSnapshot,
    DoctorSourceError,
    StaticDoctorSource,
    SubprocessDoctorSource,
    normalize_snapshot,
)
from akaribot.testing import Tester, func_case

PORT_MESSAGE = "端口冲突：bot_a 与 bot_b 都监听 0.0.0.0:8080"
ORPHAN_MESSAGE = "孤立配置：bot_kook 的适配器未安装"

PORT_CONFLICT = DoctorConflict(
    kind="port",
    level="error",
    message=PORT_MESSAGE,
    platform="telegram",
    instances=("bot_a", "bot_b"),
    detail={"address": "0.0.0.0:8080", "port": 8080},
)
ORPHAN_CONFLICT = DoctorConflict(
    kind="orphan",
    level="warning",
    message=ORPHAN_MESSAGE,
    platform="kook",
    instances=("bot_kook",),
    detail={"config_file": "config/bot_kook.toml"},
)
CONFIG_CONFLICT = DoctorConflict(
    kind="config",
    level="error",
    message="配置文件无法解析：config/bot_x.toml",
    detail={"error": "缺少 platform"},
)
UNKNOWN_CONFLICT = DoctorConflict(kind="quota", level="warning", message="额度结论：无法定位处理入口")
REPORT_CHECKS = DoctorChecks(
    instances=3,
    installed_adapters=("telegram", "discord"),
    unconfigured_adapters=("kook",),
    orphan_check="ran",
    credential_scope="manifest credential_fields",
)
STATUS_LOADED = "cli.tui.doctor.status_loaded"
STATUS_LOADING = "cli.tui.doctor.status_loading"
STATUS_FAILED = "cli.tui.doctor.status_failed"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _snapshot(conflicts=(PORT_CONFLICT, ORPHAN_CONFLICT), **kwargs) -> DoctorSnapshot:
    entries = tuple(conflicts)
    params = {
        "instance_root": "/tmp/inst",
        "config_root": "/tmp/inst/config",
        "implementation": "core（config conflicts）",
        "registry_available": True,
        "conflicts": entries,
        "error_count": sum(1 for item in entries if item.level == "error"),
        "warning_count": sum(1 for item in entries if item.level != "error"),
        "checks": REPORT_CHECKS,
    }
    params.update(kwargs)
    return DoctorSnapshot(**params)


async def _with_page(source, body, *, size=(150, 40), sources=None):
    mapping = {"doctor": source}
    mapping.update(sources or {})
    app = TuiApp(sources=mapping, initial_page="doctor", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("doctor")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


def _visible_detail_rows(page) -> tuple[str, ...]:
    # 详情被父容器裁掉尾部时 region 会超出屏幕：取 region 与屏幕可视区的交集，再逐行取控件自己的渲染结果。
    detail = page.query_one("#detail", compat.Static)
    region = detail.region
    screen = page.app.screen.region
    first = max(0, max(region.y, screen.y) - region.y)
    last = max(first, min(region.bottom, screen.bottom) - region.y)
    return tuple(detail.render_line(y).text.rstrip() for y in range(first, last))


class _SlowDoctorSource(StaticDoctorSource):
    # 取数放慢，便于观察进行中的状态栏与按钮。
    def load_snapshot(self, *, strict: bool = False):
        time.sleep(0.4)
        return super().load_snapshot(strict=strict)


# 假 CLI 写成带 shebang 的可执行文件：AKARIBOT_CLI_BIN 是单一路径，不按空格拆解释器与脚本。
FAKE_CLI_DOCTOR_EXIT_ONE = """#!/usr/bin/env python3
import json
import sys

payload = {
    "instance_root": "/tmp/inst",
    "config_root": "/tmp/inst/config",
    "implementation": "core（config conflicts）",
    "registry_available": True,
    "registry_note": "",
    "conflicts": [
        {
            "kind": "port",
            "level": "error",
            "platform": "telegram",
            "instances": ["bot_a", "bot_b"],
            "message": "端口冲突：bot_a 与 bot_b 都监听 0.0.0.0:8080",
            "detail": {"port": 8080},
        }
    ],
    "summary": {"error": 1, "warning": 0},
    "checks": {
        "instances": 2,
        "installed_adapters": ["telegram"],
        "unconfigured_adapters": [],
        "orphan_check": "ran",
        "credential_scope": "manifest credential_fields",
    },
}
print(json.dumps(payload, ensure_ascii=False))
sys.exit(1)
"""

FAKE_CLI_DOCTOR_GARBAGE = """#!/usr/bin/env python3
import sys

print("体检输出被日志污染")
sys.exit(1)
"""


def _fake_cli(root: Path, name: str, body: str) -> str:
    path = root / name
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return str(path)


async def _test_lists_conflicts_and_summarizes():
    source = StaticDoctorSource(_snapshot())

    async def body(app, page, pilot):
        observed = {
            "rows": page.row_texts(),
            "cells": page.row_cells(),
            "listed": len(page.query_one("#conflict-list", compat.ListView)),
            "summary": page.summary_text,
            "verdict": page.verdict_text,
            "status": page.status_text,
            "status_key": page.status_key,
            "snapshot": page.snapshot,
        }
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body)
    snapshot = observed["snapshot"]
    checks = snapshot.checks
    return (
        observed["listed"] == 2
        and len(observed["rows"]) == 2
        and observed["cells"][0] == ("✖", "error", PORT_MESSAGE)
        and observed["cells"][1] == ("!", "warning", ORPHAN_MESSAGE)
        and PORT_MESSAGE in observed["rows"][0]
        and ORPHAN_MESSAGE in observed["rows"][1]
        and snapshot.error_count == 1
        and snapshot.warning_count == 1
        and checks.instances == 3
        and checks.installed_adapters == ("telegram", "discord")
        and checks.unconfigured_adapters == ("kook",)
        and checks.orphan_check == "ran"
        and checks.credential_scope == "manifest credential_fields"
        and "/tmp/inst/config" in observed["summary"]
        and "telegram" in observed["summary"]
        and "discord" in observed["summary"]
        and "kook" in observed["summary"]
        and observed["summary"].count("\n") == 6
        and observed["status_key"] == STATUS_LOADED
        and observed["status"]
        == i18n.t(
            "cli.tui.doctor.status_loaded",
            errors=1,
            warnings=1,
            implementation=snapshot.implementation_label,
        )
        and observed["verdict"] == i18n.t("cli.tui.doctor.verdict_conflicts", errors=1, warnings=1)
        and source.calls["load"] == 1
    )


async def _test_exit_code_one_with_json_still_renders():
    # 存在 error 级结论时 doctor 以退出码 1 结束，stdout 仍是完整 JSON，结论照常展示。
    with TemporaryDirectory(prefix="akari-doctor-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_doctor_exit_one", FAKE_CLI_DOCTOR_EXIT_ONE)
        source = SubprocessDoctorSource(root=root, timeout=30.0)

        async def body(app, page, pilot):
            observed = {
                "rows": page.row_texts(),
                "errors": page.snapshot.errors,
                "error_count": page.snapshot.error_count,
                "status_key": page.status_key,
                "status": page.status_text,
                "verdict": page.verdict_text,
            }
            await pilot.press("q")
            return observed

        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            observed = await _with_page(source, body)

    return (
        source.calls["load"] == 1
        and observed["errors"] == ()
        and observed["error_count"] == 1
        and len(observed["rows"]) == 1
        and PORT_MESSAGE in observed["rows"][0]
        and observed["status_key"] == STATUS_LOADED
        and observed["status"] != ""
        and observed["verdict"] == i18n.t("cli.tui.doctor.verdict_conflicts", errors=1, warnings=0)
    )


async def _test_passed_when_no_conflicts():
    source = StaticDoctorSource(_snapshot(conflicts=()))

    async def body(app, page, pilot):
        observed = {
            "conflicts": page.conflicts,
            "listed": len(page.query_one("#conflict-list", compat.ListView)),
            "verdict": page.verdict_text,
            "detail": page.detail_text,
            "status_key": page.status_key,
        }
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body)
    return (
        observed["conflicts"] == ()
        and observed["listed"] == 0
        and observed["verdict"] == i18n.t("cli.tui.doctor.verdict_passed")
        and observed["detail"] == i18n.t("cli.tui.doctor.detail_passed")
        and observed["status_key"] == STATUS_LOADED
    )


async def _test_source_exception_reports_reason():
    source = StaticDoctorSource(error=DoctorSourceError("体检数据源不可用"))

    async def body(app, page, pilot):
        observed = {
            "last_error": page.last_error,
            "conflicts": page.conflicts,
            "listed": len(page.query_one("#conflict-list", compat.ListView)),
            "status_key": page.status_key,
            "status": page.status_text,
            "verdict": page.verdict_text,
            "detail": page.detail_text,
        }
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body)
    return (
        "体检数据源不可用" in observed["last_error"]
        and observed["conflicts"] == ()
        and observed["listed"] == 0
        and observed["status_key"] == STATUS_FAILED
        and observed["status"] != ""
        and observed["verdict"] == i18n.t("cli.tui.doctor.verdict_failed")
        and observed["detail"] == i18n.t("cli.tui.doctor.detail_failed")
    )


async def _test_bad_json_reports_reason():
    with TemporaryDirectory(prefix="akari-doctor-") as raw:
        root = Path(raw)
        fake = _fake_cli(root, "fake_doctor_garbage", FAKE_CLI_DOCTOR_GARBAGE)
        source = SubprocessDoctorSource(root=root, timeout=30.0)

        async def body(app, page, pilot):
            observed = {
                "last_error": page.last_error,
                "errors": page.snapshot.errors,
                "rows": page.row_texts(),
                "status_key": page.status_key,
                "status": page.status_text,
                "summary": page.summary_text,
            }
            await pilot.press("q")
            return observed

        with patch.dict(os.environ, {"AKARIBOT_CLI_BIN": fake}):
            observed = await _with_page(source, body)

    return (
        source.calls["load"] == 1
        and len(observed["errors"]) == 2
        and observed["last_error"] != ""
        and observed["rows"] == ()
        and observed["status_key"] == STATUS_FAILED
        and observed["status"] != ""
        and observed["summary"] != ""
    )


async def _test_detail_follows_selection():
    source = StaticDoctorSource(_snapshot())

    async def body(app, page, pilot):
        list_view = page.query_one("#conflict-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        first = (page.detail_text, page.selected_conflict)
        list_view.index = 1
        await pilot.pause()
        second = (page.detail_text, page.selected_conflict)
        await pilot.press("q")
        return first, second

    first, second = await _with_page(source, body)
    return (
        first[1] is PORT_CONFLICT
        and second[1] is ORPHAN_CONFLICT
        and PORT_MESSAGE in first[0]
        and ORPHAN_MESSAGE not in first[0]
        and "address=0.0.0.0:8080" in first[0]
        and ORPHAN_MESSAGE in second[0]
        and PORT_MESSAGE not in second[0]
        and "config_file=config/bot_kook.toml" in second[0]
    )


async def _test_refresh_key_reloads():
    source = StaticDoctorSource(_snapshot())

    async def body(app, page, pilot):
        before = source.calls["load"]
        await pilot.press("r")
        await page.wait_for_idle()
        await pilot.pause()
        after = source.calls["load"]
        status_key = page.status_key
        await pilot.press("q")
        return before, after, status_key

    before, after, status_key = await _with_page(source, body)
    return before == 1 and after == 2 and status_key == STATUS_LOADED


async def _test_busy_disables_refresh_button():
    source = _SlowDoctorSource(_snapshot())

    async def body(app, page, pilot):
        button = page.query_one("#refresh", compat.Button)
        await pilot.press("r")
        await pilot.pause()
        during = (page.status_key, button.disabled)
        await page.wait_for_idle()
        await pilot.pause()
        after = (page.status_key, button.disabled, source.calls["load"])
        await pilot.press("q")
        return during, after

    during, after = await _with_page(source, body)
    return during == (STATUS_LOADING, True) and after == (STATUS_LOADED, False, 2)


def _test_subprocess_source_argv_and_env():
    recorded = []

    def runner(argv, **kwargs):
        recorded.append((argv, kwargs))
        payload = {
            "instance_root": "/tmp/inst",
            "implementation": "CLI 本地（core 入口不可用）",
            "conflicts": [],
            "summary": {"error": 0, "warning": 0},
            "checks": {"instances": 3, "installed_adapters": ["telegram"], "orphan_check": "ran"},
        }
        return subprocess.CompletedProcess(argv, 1, stdout=json.dumps(payload, ensure_ascii=False), stderr="")

    source = SubprocessDoctorSource(root="/tmp/inst", timeout=5.0, runner=runner)
    snapshot = source.load_snapshot()
    argv, kwargs = recorded[0]
    return (
        argv[-2:] == ["doctor", "--json"]
        and kwargs["cwd"] == str(source.root)
        and kwargs["env"]["AKARI_INSTANCE_DIR"] == str(source.root)
        and kwargs["env"]["PYTHONIOENCODING"] == "utf-8"
        and kwargs["encoding"] == "utf-8"
        and snapshot.implementation_kind == "cli"
        and snapshot.error_count == 0
        and snapshot.checks.instances == 3
        and source.calls["load"] == 1
    )


def _test_normalize_defaults_and_shape():
    snapshot = normalize_snapshot(
        {
            "conflicts": [
                {"kind": "port", "message": "端口冲突"},
                {"kind": "orphan", "message": "孤立配置"},
            ],
            "checks": {},
        }
    )
    rejected = False
    try:
        normalize_snapshot(["不是对象"])
    except DoctorSourceError:
        rejected = True
    return (
        snapshot.conflicts[0].level == "error"
        and snapshot.conflicts[1].level == "warning"
        and snapshot.error_count == 1
        and snapshot.warning_count == 1
        and snapshot.checks.orphan_label == i18n.t("cli.tui.doctor.orphan_unknown")
        and rejected
    )


def _test_implementation_kind_detection():
    core = DoctorSnapshot(implementation="core（config conflicts）")
    local = DoctorSnapshot(implementation="CLI 本地（core 入口不可用）")
    unknown = DoctorSnapshot(implementation="")
    return (
        core.implementation_kind == "core"
        and local.implementation_kind == "cli"
        and unknown.implementation_kind == "unknown"
        and core.implementation_label == i18n.t("cli.tui.doctor.impl_core")
        and local.implementation_label == i18n.t("cli.tui.doctor.impl_local")
        and unknown.implementation_label == i18n.t("cli.tui.doctor.impl_unknown")
    )


async def _test_enter_jumps_to_target_page():
    # 平台类结论去适配器页，config 类去配置页，落不到页面的去概览页。
    source = StaticDoctorSource(_snapshot(conflicts=(PORT_CONFLICT, CONFIG_CONFLICT, UNKNOWN_CONFLICT)))
    jump_sources = {
        "adapters": StaticAdapterSource(),
        "config": StaticConfigSource(),
        "dashboard": StaticDashboardSource(),
    }

    async def body(app, page, pilot):
        observed = []
        list_view = page.query_one("#conflict-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        for expected in ("adapters", "config", "dashboard"):
            await pilot.press("enter")
            await pilot.pause()
            observed.append((expected, app.active_page, page.status_text))
            app.show_page("doctor")
            await pilot.pause()
            if expected != "dashboard":
                # 上下键仍归列表：类型按钮改绑回车不能把游标键一起丢掉。
                await pilot.press("down")
                await pilot.pause()
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body, sources=jump_sources)
    return all(
        expected == page_key
        and status == i18n.t("cli.tui.doctor.status_jumped", page=i18n.t(f"cli.tui.nav.{expected}"))
        for expected, page_key, status in observed
    )


async def _test_button_jumps_to_target_page():
    source = StaticDoctorSource(_snapshot(conflicts=(CONFIG_CONFLICT,)))

    async def body(app, page, pilot):
        page.query_one("#open-conflict", compat.Button).press()
        await pilot.pause()
        observed = (app.active_page, page.status_text)
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body, sources={"config": StaticConfigSource()})
    return observed == ("config", i18n.t("cli.tui.doctor.status_jumped", page=i18n.t("cli.tui.nav.config")))


async def _test_enter_without_conflicts_reports_nothing():
    source = StaticDoctorSource(_snapshot(conflicts=()))

    async def body(app, page, pilot):
        await pilot.press("enter")
        await pilot.pause()
        observed = (app.active_page, page.status_text)
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body)
    return observed == ("doctor", i18n.t("cli.tui.doctor.status_nothing"))


async def _test_detail_shows_next_step():
    source = StaticDoctorSource(_snapshot(conflicts=(PORT_CONFLICT, UNKNOWN_CONFLICT)))

    async def body(app, page, pilot):
        list_view = page.query_one("#conflict-list", compat.ListView)
        list_view.index = 0
        await pilot.pause()
        mapped = page.detail_text
        list_view.index = 1
        await pilot.pause()
        unmapped = page.detail_text
        await pilot.press("q")
        return mapped, unmapped

    mapped, unmapped = await _with_page(source, body)
    return (
        i18n.t("cli.tui.doctor.next_step_page", page=i18n.t("cli.tui.nav.adapters")) in mapped
        and i18n.t("cli.tui.doctor.next_step_cli") in unmapped
        and "${" not in mapped
        and "${" not in unmapped
    )


async def _test_detail_orders_next_step_before_facts():
    # 详情重排后「级别」与「种类」合成一行，总行数不超过六行。
    source = StaticDoctorSource(_snapshot())

    async def body(app, page, pilot):
        lines = page.detail_text.split("\n")
        await pilot.press("q")
        return lines

    lines = await _with_page(source, body)
    labels = (
        i18n.t("cli.tui.doctor.field_message"),
        i18n.t("cli.tui.doctor.field_next"),
        i18n.t("cli.tui.doctor.field_level_kind"),
        i18n.t("cli.tui.doctor.field_platform"),
        i18n.t("cli.tui.doctor.field_instances"),
        i18n.t("cli.tui.doctor.field_detail"),
    )
    merged = lines[2] if len(lines) > 2 else ""
    return (
        len(lines) == 6
        and all(line.startswith(label) for line, label in zip(lines, labels))
        and PORT_MESSAGE in lines[0]
        and i18n.t("cli.tui.doctor.next_step_page", page=i18n.t("cli.tui.nav.adapters")) in lines[1]
        and "✖" in merged
        and i18n.t("cli.tui.doctor.level_error") in merged
        and "port" in merged
        and "${" not in "\n".join(lines)
    )


async def _test_next_step_visible_at_narrow_sizes():
    # 80×24 只放得下详情的前几行：尾部可以裁掉，但「下一步」必须落在可视区内。
    async def body(app, page, pilot):
        detail = page.query_one("#detail", compat.Static)
        observed = (page.detail_text.split("\n"), detail.region, app.size.height, _visible_detail_rows(page))
        await pilot.press("q")
        return observed

    narrow = await _with_page(StaticDoctorSource(_snapshot()), body, size=(80, 24))
    wide = await _with_page(StaticDoctorSource(_snapshot()), body, size=(120, 34))
    next_step = i18n.t("cli.tui.doctor.next_step_page", page=i18n.t("cli.tui.nav.adapters"))
    narrow_lines, narrow_region, narrow_height, narrow_visible = narrow
    wide_lines, wide_region, wide_height, wide_visible = wide
    next_index = next((index for index, line in enumerate(narrow_lines) if next_step in line), None)
    return (
        next_index == 1
        and narrow_height == 24
        and narrow_region.height < len(narrow_lines)
        and narrow_region.y + next_index < narrow_height
        and next_index < len(narrow_visible)
        and len(narrow_visible) < len(narrow_lines)
        and narrow_visible == tuple(line.rstrip() for line in narrow_lines[: len(narrow_visible)])
        and i18n.t("cli.tui.doctor.field_detail") not in "\n".join(narrow_visible)
        and wide_height == 34
        and wide_region.y + next_index < wide_height
        and len(wide_visible) == len(wide_lines)
        and i18n.t("cli.tui.doctor.field_detail") in "\n".join(wide_visible)
    )


async def _test_strict_option_reloads_with_flag():
    # 勾选严格模式即重新体检，状态同时写进页面字段区；复选框在 80 列下完整可见。
    source = StaticDoctorSource(_snapshot())

    async def body(app, page, pilot):
        actions = page.query_one("#actions")
        checkbox = page.query_one("#strict", compat.Checkbox)
        before = (
            checkbox.value,
            page.strict,
            source.calls["load"],
            source.calls["strict"],
            i18n.t("cli.tui.doctor.field_strict") in page.summary_text,
            i18n.t("cli.tui.doctor.strict_off") in page.summary_text,
        )
        label = checkbox.render_line(0).text
        checkbox.focus()
        await pilot.pause()
        focused = app.focused is checkbox
        await pilot.press("space")
        await page.wait_for_idle()
        await pilot.pause()
        after = (
            checkbox.value,
            page.strict,
            source.calls["load"],
            source.calls["strict"],
            i18n.t("cli.tui.doctor.strict_on") in page.summary_text,
        )
        accepted = checkbox.region.right <= actions.region.right
        unresolved = "{I18N" in page.summary_text
        await pilot.press("q")
        return before, after, focused, accepted, label, unresolved

    before, after, focused, accepted, label, unresolved = await _with_page(source, body, size=(80, 24))
    return (
        before == (False, False, 1, 0, True, True)
        and after == (True, True, 2, 1, True)
        and focused
        and accepted
        and i18n.t("cli.tui.doctor.strict_option") in label
        and not unresolved
    )


async def _test_strict_toggle_restarts_running_load():
    # 取数期间勾选：正在跑的那次按旧选项下发，结论作废，必须按新选项重来。
    source = _SlowDoctorSource(_snapshot())

    async def body(app, page, pilot):
        refresh = page.query_one("#refresh", compat.Button)
        await pilot.press("r")
        await pilot.pause()
        during = (page.status_key, refresh.disabled)
        page.query_one("#strict", compat.Checkbox).value = True
        await pilot.pause()
        await page.wait_for_idle()
        await pilot.pause()
        after = (page.status_key, refresh.disabled, source.calls["load"], source.calls["strict"])
        await pilot.press("q")
        return during, after

    during, after = await _with_page(source, body)
    return during == (STATUS_LOADING, True) and after == (STATUS_LOADED, False, 3, 1)


def _test_subprocess_source_adds_strict_flag():
    recorded = []

    def runner(argv, **kwargs):
        recorded.append(list(argv))
        payload = {"conflicts": [], "summary": {"error": 0, "warning": 0}}
        return subprocess.CompletedProcess(argv, 0, stdout=json.dumps(payload, ensure_ascii=False), stderr="")

    def silent(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    source = SubprocessDoctorSource(root="/tmp/inst", timeout=5.0, runner=runner)
    plain = source.load_snapshot()
    strict = source.load_snapshot(strict=True)
    failure = SubprocessDoctorSource(root="/tmp/inst", timeout=5.0, runner=silent).load_snapshot(strict=True)
    return (
        recorded == [cli_process.cli_argv("doctor", "--json"), cli_process.cli_argv("doctor", "--strict", "--json")]
        and plain.errors == ()
        and strict.errors == ()
        and failure.errors == (i18n.t("cli.tui.doctor.src_empty_output", label="doctor --strict --json"),)
    )


async def _test_click_only_moves_highlight():
    # 单击一行只更新高亮与详情：列表把点击也发成 Selected，跳转只认键盘回车。
    source = StaticDoctorSource(_snapshot(conflicts=(PORT_CONFLICT, CONFIG_CONFLICT)))

    async def body(app, page, pilot):
        await pilot.click("#conflict-list > ListItem")
        await pilot.pause()
        observed = (app.active_page, page.detail_text)
        await pilot.press("q")
        return observed

    observed = await _with_page(source, body)
    return observed[0] == "doctor" and PORT_MESSAGE in observed[1]


@func_case
async def test_tui_doctor(tester: Tester):
    """cli.tui.doctor: 体检页结论、统计、重新体检与跳转测试"""
    _use_cli_locale()
    await tester.test(_test_lists_conflicts_and_summarizes, "列出结论行并汇总 error/warning")
    await tester.test(_test_exit_code_one_with_json_still_renders, "退出码 1 但 stdout 是 JSON 仍展示结论")
    await tester.test(_test_passed_when_no_conflicts, "无冲突时展示通过文案")
    await tester.test(_test_source_exception_reports_reason, "数据源抛异常时状态栏给出原因")
    await tester.test(_test_bad_json_reports_reason, "输出不是 JSON 时状态栏给出原因")
    await tester.test(_test_detail_follows_selection, "详情区随选中项切换")
    await tester.test(_test_refresh_key_reloads, "按 r 重新取数")
    await tester.test(_test_busy_disables_refresh_button, "取数期间禁用按钮并显示进行中")
    await tester.test(_test_enter_jumps_to_target_page, "回车按结论种类切到处理页面")
    await tester.test(_test_button_jumps_to_target_page, "按钮切到处理页面")
    await tester.test(_test_enter_without_conflicts_reports_nothing, "无结论时回车只提示")
    await tester.test(_test_click_only_moves_highlight, "单击一行只移动高亮")
    await tester.test(_test_detail_shows_next_step, "详情给出下一步或终端命令")
    await tester.test(_test_detail_orders_next_step_before_facts, "详情按结论、下一步、定位信息、细节排列")
    await tester.test(_test_next_step_visible_at_narrow_sizes, "80×24 与 120×34 下下一步仍在可视区")
    await tester.test(_test_strict_option_reloads_with_flag, "勾选严格模式即按 --strict 重新体检")
    await tester.test(_test_strict_toggle_restarts_running_load, "取数期间勾选严格模式按新选项重来")
    await tester.test(_test_subprocess_source_adds_strict_flag, "子进程源按严格模式追加 --strict")
    await tester.test(_test_subprocess_source_argv_and_env, "子进程源构造 argv 与环境")
    await tester.test(_test_normalize_defaults_and_shape, "负载归一化与形状校验")
    await tester.test(_test_implementation_kind_detection, "区分 core 入口与 CLI 本地实现")
    return tester
