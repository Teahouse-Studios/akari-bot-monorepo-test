"""``akaribot config placeholders``：表名清单来自实例，计数与失败明细原样来自 core。

CLI 不 import core，统计一律经 ``python -m akaribot.core.entrypoints.config placeholders``。用例
注入替身实例，检查下发的表名、``--json`` 的结构透出与失败路径。
"""

import io
import json
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from rich.console import Console
from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import config as config_command
from akaribot.testing import Tester, func_case

FRAGMENT = Path(__file__).resolve().parents[3] / "generated_docs" / "i18n_fragments" / "config_placeholders.json"
_KEEP_ALIVE: list[TemporaryDirectory] = []

PAYLOAD = {
    "tables": {
        "config": {"placeholder": 7, "total": 62},
        "module_ai": {"placeholder": 2, "total": 9},
    },
    "count": 9,
    "scanned": ["config", "module_ai"],
    "failed": {},
}


def _merged_locale_dir() -> Path:
    # 片段中的新增键尚未并入 locales，合成合并后的语言目录后，检查才能获取真实的渲染结果。
    holder = TemporaryDirectory(prefix="akari-config-placeholders-locale-")
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
    # CLI 首次读取文案时使用包内 locales 重建快照，会覆盖合并目录。先获取一次以完成重建，再创建合并快照。
    i18n.t("cli.common.error_label")
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [str(_merged_locale_dir())], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


class _FakeInstance:
    # 仅响应 run_core_capture 的模拟对象，stdout 是 core 返回的文本，returncode 是其退出码。
    def __init__(
        self, payload: object = None, *, stdout: str | None = None, returncode: int = 0, stderr: str = ""
    ) -> None:
        self.payload = payload
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr
        self.calls: list[tuple[str, tuple[str, ...]]] = []
        self.meta = SimpleNamespace(root=Path("/tmp/fake-instance"))

    def run_core_capture(self, entrypoint: str, *args: str, timeout: float | None = 120.0, **env: str):
        """记录 entrypoint 与参数，返回预设输出。"""
        self.calls.append((entrypoint, tuple(args)))
        text = self.stdout if self.stdout is not None else json.dumps(self.payload, ensure_ascii=False)
        return subprocess.CompletedProcess(list(args), self.returncode, text, self.stderr)


def _invoke(instance, argv: list[str]):
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with (
        patch.object(config_command, "require_instance", return_value=instance),
        patch.object(config_command, "console", console),
    ):
        result = CliRunner().invoke(config_command.app, argv)
    return result, buffer.getvalue()


def _instance_with_config(*names: str) -> _FakeInstance:
    holder = TemporaryDirectory(prefix="akari-config-placeholders-")
    _KEEP_ALIVE.append(holder)
    root = Path(holder.name)
    (root / "config").mkdir()
    for name in names:
        target = root / "config" / f"{name}.toml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("[x]\n", encoding="utf-8")
    instance = _FakeInstance(PAYLOAD)
    instance.meta = SimpleNamespace(root=root)
    return instance


def _test_placeholders_passes_table_list():
    # 表名清单提取实例 config 目录下的全部 toml（包含子目录），去重排序后一次性传递给 core。
    instance = _instance_with_config("config", "module_ai", "adapters/bot_telegram")
    result, text = _invoke(instance, ["placeholders"])
    entrypoint, args = instance.calls[0]
    return (
        result.exit_code == 0
        and entrypoint == "config"
        and args == ("placeholders", "--tables", "bot_telegram,config,module_ai", "--json")
        and "config" in text
        and "9" in text
    )


def _test_placeholders_json_is_passthrough():
    # --json 原样输出 core 的结构，总数、逐表明细、已扫描与失败归集均不执行改写。
    payload = dict(PAYLOAD, failed={"broken": "解析失败：ParseError"})
    instance = _instance_with_config("config")
    instance.payload = payload
    result, text = _invoke(instance, ["placeholders", "--json"])
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return len(lines) == 1 and json.loads(lines[-1]) == payload and text == ""


def _test_placeholders_reports_failed_tables():
    # core 判定结果中包含失败配置表时，明细中逐条列出表名与原因。
    instance = _instance_with_config("config")
    instance.payload = dict(PAYLOAD, failed={"binary": "读取失败：UnicodeDecodeError"})
    result, text = _invoke(instance, ["placeholders"])
    expected = i18n.t(
        "cli.config.placeholders.failed_line",
        count=1,
        detail="binary（读取失败：UnicodeDecodeError）",
    )
    return result.exit_code == 0 and expected in text and i18n.t("cli.config.placeholders.column_table") in text


def _test_placeholders_empty_instance_omits_tables():
    # 实例不存在配置表时不传入 --tables，由 core 按照自身的配置目录判定，输出如实记录无可用配置表。
    instance = _FakeInstance({"tables": {}, "count": 0, "scanned": [], "failed": {}})
    with TemporaryDirectory(prefix="akari-config-placeholders-empty-") as raw:
        instance.meta = SimpleNamespace(root=Path(raw))
        result, text = _invoke(instance, ["placeholders"])
    _entrypoint, args = instance.calls[0]
    return (
        result.exit_code == 0 and args == ("placeholders", "--json") and i18n.t("cli.config.placeholders.none") in text
    )


def _test_placeholders_core_failure_is_reported():
    # core 退出码非零时输出其最后一行原因，CLI 保持同一退出码。
    instance = _instance_with_config("config")
    instance.returncode = 2
    instance.stdout = ""
    instance.stderr = "配置操作失败：配置表不存在\n"
    result, _text = _invoke(instance, ["placeholders"])
    return result.exit_code != 0 and "配置表不存在" in result.output


def _test_placeholders_unparseable_output_is_reported():
    # 退出码为 0 但输出不是 JSON 时作为格式错误返回，不将不完整文本视为统计结果。
    instance = _instance_with_config("config")
    instance.stdout = "不是 JSON"
    result, _text = _invoke(instance, ["placeholders"])
    return result.exit_code != 0 and "JSON" in str(result.exception)


def _test_fragment_covers_command_keys():
    # 命令引用的键必须在片段里有定义，否则界面会将键名本身当作界面文案显示。
    source = Path(config_command.__file__).read_text(encoding="utf-8")
    used = set(re.findall(r"cli\.config\.placeholders\.[a-z_]+", source))
    fragment = json.loads(FRAGMENT.read_text(encoding="utf-8"))
    return bool(used) and used <= set(fragment)


@func_case
async def test_config_placeholders(tester: Tester):
    """cli.config.placeholders 占位符统计命令测试"""
    _use_cli_locale()
    await tester.test(_test_placeholders_passes_table_list, "表名清单取实例配置目录并下发给 core")
    await tester.test(_test_placeholders_json_is_passthrough, "--json 原样透出 core 结构")
    await tester.test(_test_placeholders_reports_failed_tables, "失败表在明细里给出原因")
    await tester.test(_test_placeholders_empty_instance_omits_tables, "实例无配置表时不传表名清单")
    await tester.test(_test_placeholders_core_failure_is_reported, "core 失败时透出原因与退出码")
    await tester.test(_test_placeholders_unparseable_output_is_reported, "输出不可解析时按契约错误报出")
    await tester.test(_test_fragment_covers_command_keys, "命令引用的文案键都在片段里定义")
    return tester
