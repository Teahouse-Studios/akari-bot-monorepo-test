"""体检页：结论列表、检查项统计与重新体检。

本文件固定三条链路：状态栏汇总 error/warning 与实现来源；退出码 1 但 stdout 仍是完整 JSON 时结论
照常展示；取数失败只在状态栏给出原因，界面不崩。文案键尚未并入 locales，故断言一律针对状态与结构
（状态栏文案键、结论条数、选中项、数据源调用次数），不比对中文文案。
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
from akaribot.cli.tui.app import TuiApp
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


async def _with_page(source, body, *, size=(150, 40)):
    app = TuiApp(sources={"doctor": source}, initial_page="doctor", boot_started_at=time.monotonic())
    async with compat.app_test(app, size=size) as pilot:
        page = app.page("doctor")
        await page.wait_for_idle()
        await pilot.pause()
        return await body(app, page, pilot)


class _SlowDoctorSource(StaticDoctorSource):
    # 取数放慢，便于观察进行中的状态栏与按钮。
    def load_snapshot(self):
        time.sleep(0.4)
        return super().load_snapshot()


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
        and observed["summary"].count("\n") == 5
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


@func_case
async def test_tui_doctor(tester: Tester):
    """cli.tui.doctor: 体检页结论、统计与重新体检测试"""
    _use_cli_locale()
    await tester.test(_test_lists_conflicts_and_summarizes, "列出结论行并汇总 error/warning")
    await tester.test(_test_exit_code_one_with_json_still_renders, "退出码 1 但 stdout 是 JSON 仍展示结论")
    await tester.test(_test_passed_when_no_conflicts, "无冲突时展示通过文案")
    await tester.test(_test_source_exception_reports_reason, "数据源抛异常时状态栏给出原因")
    await tester.test(_test_bad_json_reports_reason, "输出不是 JSON 时状态栏给出原因")
    await tester.test(_test_detail_follows_selection, "详情区随选中项切换")
    await tester.test(_test_refresh_key_reloads, "按 r 重新取数")
    await tester.test(_test_busy_disables_refresh_button, "取数期间禁用按钮并显示进行中")
    await tester.test(_test_subprocess_source_argv_and_env, "子进程源构造 argv 与环境")
    await tester.test(_test_normalize_defaults_and_shape, "负载归一化与形状校验")
    await tester.test(_test_implementation_kind_detection, "区分 core 入口与 CLI 本地实现")
    return tester
