"""``akaribot db rows``：把筛选、搜索与排序透传给 core，并把页码显示出来。

CLI 不 import core，读数据一律经 ``python -m akaribot.core.entrypoints.data``；用例注入替身实例，
断言下发的 argv、单行 JSON 输出与失败时的退出码，不真的连库。
"""

import io
import json
import subprocess
from pathlib import Path
from unittest.mock import patch

from rich.console import Console
from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import db as db_command
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


# 只回答 run_core_capture 的替身实例：payload 是 core 要回传的 JSON，returncode 是它的退出码。
class _FakeInstance:
    def __init__(self, payload: object, *, returncode: int = 0) -> None:
        self.payload = payload
        self.returncode = returncode
        self.calls: list[tuple[str, tuple[str, ...]]] = []
        self.root = Path("/tmp/fake-instance")

    def run_core_capture(self, entrypoint: str, *args: str, timeout: float | None = 120.0, **env: str):
        """记下 entrypoint 与参数，返回预设输出。"""
        self.calls.append((entrypoint, tuple(args)))
        text = json.dumps(self.payload, ensure_ascii=False)
        return subprocess.CompletedProcess(list(args), self.returncode, text, "")


def _page(**overrides) -> dict[str, object]:
    payload: dict[str, object] = {
        "table": "module_status",
        "total": 587,
        "rows": [{"module_name": "wordle", "load": True}],
        "limit": 50,
        "offset": 100,
        "order_by": "module_name:asc",
        "filters": ["load=true"],
        "search": "wik",
    }
    payload.update(overrides)
    return payload


def _invoke(instance, argv: list[str]):
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with (
        patch.object(db_command, "require_instance", return_value=instance),
        patch.object(db_command, "console", console),
    ):
        result = CliRunner().invoke(db_command.app, argv)
    return result, buffer.getvalue()


def _test_rows_passes_query_to_core():
    instance = _FakeInstance(_page())
    result, text = _invoke(
        instance,
        [
            "rows",
            "module_status",
            "--limit",
            "50",
            "--offset",
            "100",
            "--filter",
            "load=true",
            "--search",
            "wik",
            "--order-by",
            "module_name:asc",
        ],
    )
    entrypoint, args = instance.calls[0]
    return (
        result.exit_code == 0
        and entrypoint == "data"
        and args
        == (
            "rows",
            "module_status",
            "--limit",
            "50",
            "--offset",
            "100",
            "--filter",
            "load=true",
            "--search",
            "wik",
            "--order-by",
            "module_name:asc",
            "--json",
        )
        and i18n.t("cli.db.rows.conditions", conditions="load=true、搜索 wik") in text
    )


def _test_rows_shows_page_numbers():
    instance = _FakeInstance(_page())
    _result, text = _invoke(instance, ["rows", "module_status", "--limit", "50", "--offset", "100"])
    title = i18n.t("cli.db.rows.table_title", table="module_status", total=587, count=1, page=3, pages=12, offset=100)
    return title in text and "wordle" in text


def _test_rows_json_is_single_line():
    instance = _FakeInstance(_page())
    result, _text = _invoke(instance, ["rows", "module_status", "--filter", "load=true", "--json"])
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    payload = json.loads(lines[-1])
    return len(lines) == 1 and payload["total"] == 587 and payload["filters"] == ["load=true"]


def _test_rows_without_conditions():
    # 不给条件时不下发 --filter / --search / --order-by，命令行保持最短。
    instance = _FakeInstance(_page(filters=[], search="", offset=0))
    _result, text = _invoke(instance, ["rows", "module_status"])
    _entrypoint, args = instance.calls[0]
    return (
        "--filter" not in args
        and "--search" not in args
        and "--order-by" not in args
        and i18n.t("cli.db.rows.conditions", conditions="x") not in text
    )


def _test_rows_core_error_is_reported():
    # core 把原因写进 stdout 的 JSON，退出码 2 表示用户错误；CLI 保持该退出码。
    instance = _FakeInstance({"error": "表 module_status 没有列 'nosuch'。"}, returncode=2)
    result, _text = _invoke(instance, ["rows", "module_status", "--filter", "nosuch=1"])
    return result.exit_code == 2 and "nosuch" in result.output


@func_case
async def test_db_rows(tester: Tester):
    """cli.db.rows: 筛选、搜索、排序与分页展示测试"""
    _use_cli_locale()
    await tester.test(_test_rows_passes_query_to_core, "条件、搜索与排序透传给 core")
    await tester.test(_test_rows_shows_page_numbers, "标题给出总条数与页码")
    await tester.test(_test_rows_json_is_single_line, "--json 输出单行且带条件回显")
    await tester.test(_test_rows_without_conditions, "无条件时不下发多余参数")
    await tester.test(_test_rows_core_error_is_reported, "core 的用户错误按退出码 2 上报")

    return tester
