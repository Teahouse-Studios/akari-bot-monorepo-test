"""``akaribot module available``：可安装集合的列举。

``add`` 只认名字，而名字从哪来看不到；本命令把可安装集合连同「是否已装」列出来。工作区模式下
安装一律取本地源码，此时 registry 不是「能装什么」的答案来源，故集合必须改取本地成员——这条
分叉是本文件主要守住的东西。
"""

import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import module as module_command
from akaribot.cli.instance import PackageInfo
from rich.console import Console

from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _workspace(tmp: Path) -> Path:
    root = tmp / "ws"
    specs = (
        ("akari-bot-core", "akaribot/core", None, None),
        ("akari-bot-module-dice", "akaribot/modules/dice", "dice", None),
        ("akari-bot-adapter-telegram", "akaribot/adapters/telegram", None, "telegram"),
    )
    for dist, import_dir, module_name, adapter_name in specs:
        package = root / "packages" / dist
        (package / import_dir).mkdir(parents=True)
        entry = ""
        if module_name:
            entry = f'\n[project.entry-points."akaribot.modules"]\n{module_name} = "{import_dir.replace("/", ".")}"\n'
        elif adapter_name:
            entry = f'\n[project.entry-points."akaribot.adapters"]\n{adapter_name} = "{import_dir.replace("/", ".")}"\n'
        (package / "pyproject.toml").write_text(
            f'[project]\nname = "{dist}"\nversion = "0.1.0"\n{entry}', encoding="utf-8"
        )
    return root


def _instance(tmp: Path, workspace_root: Path, *, installed: tuple[str, ...] = ()):
    root = tmp / "instance"
    root.mkdir(parents=True, exist_ok=True)
    (root / "akaribot.toml").write_text("", encoding="utf-8")
    instance = engine.Instance.detached(root, workspace_root=str(workspace_root), mode="workspace")
    instance.installed = lambda: {name: PackageInfo(dist=name, kind="module", name=name) for name in installed}
    return instance


def _run(instance, **kwargs) -> str:
    # 命令经 ``rich.console.Console`` 输出，不是 stdout，故必须换掉 console 本身；宽度放宽，
    # 免得表格截断长分发名而让断言失真。
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with (
        patch.object(module_command, "require_instance", return_value=instance),
        patch.object(module_command, "console", console),
    ):
        module_command.available(**kwargs)
    return buffer.getvalue()


def _dists(instance, **kwargs) -> list[str]:
    # 表格会按终端宽度截断长名字，断言分发名只能走 JSON。
    payload = json.loads(_run(instance, as_json=True, **kwargs))
    return sorted(item["dist"] for item in payload)


def _test_workspace_mode_lists_local_members():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        dists = _dists(_instance(tmp, ws))
    return dists == ["akari-bot-adapter-telegram", "akari-bot-module-dice"]


def _test_core_is_not_offered():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        dists = _dists(_instance(tmp, ws))
    return "akari-bot-core" not in dists


def _test_installed_state_is_marked():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        out = _run(_instance(tmp, ws, installed=("akari-bot-module-dice",)))
    return (
        i18n.t("cli.module.available.state_installed") in out and i18n.t("cli.module.available.state_available") in out
    )


def _test_kind_and_search_filters():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        instance = _instance(tmp, ws)
        adapters = _dists(instance, kind="adapter")
        searched = _dists(instance, search="tele")
        both = _run(instance, kind="module", search="tele")
    return (
        adapters == ["akari-bot-adapter-telegram"]
        and searched == ["akari-bot-adapter-telegram"]
        and i18n.t("cli.module.available.none", search="tele") in both
    )


def _test_json_payload_shape():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        out = _run(_instance(tmp, ws, installed=("akari-bot-module-dice",)), as_json=True)
    payload = json.loads(out)
    by_dist = {item["dist"]: item for item in payload}
    dice = by_dist["akari-bot-module-dice"]
    return (
        len(payload) == 2
        and dice["kind"] == "module"
        and dice["installed"] is True
        and by_dist["akari-bot-adapter-telegram"]["installed"] is False
        and dice["version"] == "0.1.0"
    )


def _test_no_match_reports_source_and_hint():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        ws = _workspace(tmp)
        out = _run(_instance(tmp, ws), search="definitely_absent")
    return i18n.t("cli.module.available.none_hint") in out and str(ws) in out


def _test_registry_mode_uses_catalog():
    with TemporaryDirectory(prefix="akari-available-") as raw:
        tmp = Path(raw)
        root = tmp / "instance"
        root.mkdir(parents=True, exist_ok=True)
        (root / "akaribot.toml").write_text("", encoding="utf-8")
        instance = engine.Instance.detached(root, mode="installed")
        instance.installed = lambda: {}
        catalog = engine.RegistryCatalog.from_payload(
            {
                "core": {"dist": "akari-bot-core", "latest": "0.1.0"},
                "modules": [
                    {"name": "dice", "dist": "akari-bot-module-dice", "latest": "0.2.0", "summary": {"zh_cn": "骰子"}}
                ],
                "adapters": [],
            },
            source="test://registry.json",
        )
        with patch.object(module_command, "_load_catalog", return_value=catalog):
            out = _run(instance)
    return "akari-bot-module-dice" in out and "骰子" in out and "0.2.0" in out


@func_case
async def test_module_available(tester: Tester):
    """cli.commands.module: 可安装包列举测试"""
    _use_cli_locale()
    await tester.test(_test_workspace_mode_lists_local_members, "工作区模式列本地成员")
    await tester.test(_test_core_is_not_offered, "core 不作为可安装候选")
    await tester.test(_test_installed_state_is_marked, "区分已装与可安装")
    await tester.test(_test_kind_and_search_filters, "--kind 与 --search 过滤")
    await tester.test(_test_json_payload_shape, "--json 字段稳定")
    await tester.test(_test_no_match_reports_source_and_hint, "空结果说明来源与下一步")
    await tester.test(_test_registry_mode_uses_catalog, "无工作区时列 registry 条目")
    return tester
