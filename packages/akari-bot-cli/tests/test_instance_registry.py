"""本机实例注册表与 `akaribot instance` 子命令。

注册表只记位置与策略（开机自启、崩溃重启、最后已知的期望状态），删记录不动实例目录；实例解析在
站在任何实例之外时回落到注册表里的缺省实例——那正是「这台机器上要管哪一个」的答案。
"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli.commands import instance as instance_cmd
from akaribot.cli.instance import resolve_instance_root
from akaribot.cli.instances import InstanceRegistry, RegistryError, probe_running
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path, name: str = "demo") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "akaribot.toml").write_text(f'[instance]\nname = "{name}"\n', encoding="utf-8")
    return root


def _invoke(args, *, home: Path):
    with patch.dict(os.environ, {"AKARIBOT_HOME": str(home), "AKARI_INSTANCE_DIR": ""}):
        return CliRunner().invoke(instance_cmd.app, args)


async def _test_add_list_remove():
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        home = base / "home"
        first = _make_instance(base / "one")
        second = _make_instance(base / "two")
        with patch.dict(os.environ, {"AKARIBOT_HOME": str(home)}):
            registry = InstanceRegistry()
            entry = registry.add(first, locale="zh_cn", autostart=True)
            registry.add(second)
            names = [item.name for item in registry.load()]
            listed = _invoke(["list", "--json"], home=home)
            payload = json.loads(listed.stdout)
            removed = registry.remove(entry.name)
            after = [item.name for item in registry.load()]
    return (
        names == ["one", "two"]
        and entry.autostart
        and removed
        and after == ["two"]
        and listed.exit_code == 0
        and len(payload) == 2
        and payload[0]["default"] is True
    )


async def _test_duplicate_root_keeps_existing_entry():
    # 同一个目录登记两次不该产生两条记录，也不该改掉已有策略。
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        target = _make_instance(base / "one")
        with patch.dict(os.environ, {"AKARIBOT_HOME": str(base / "home")}):
            registry = InstanceRegistry()
            first = registry.add(target, autostart=True)
            second = registry.add(target, name="other")
            entries = registry.load()
    return first.name == second.name and len(entries) == 1 and entries[0].autostart


async def _test_add_rejects_non_instance():
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        plain = base / "plain"
        plain.mkdir()
        with patch.dict(os.environ, {"AKARIBOT_HOME": str(base / "home")}):
            try:
                InstanceRegistry().add(plain)
            except RegistryError:
                rejected = True
            else:
                rejected = False
    return rejected


async def _test_policy_and_default():
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        home = base / "home"
        first = _make_instance(base / "one")
        second = _make_instance(base / "two")
        with patch.dict(os.environ, {"AKARIBOT_HOME": str(home)}):
            registry = InstanceRegistry()
            registry.add(first)
            second_entry = registry.add(second)
            registry.set_default(second_entry.name)
            updated = registry.update(second_entry.name, autostart=True, restart_on_crash=True)
            default = registry.default_name()
        return updated.autostart and updated.restart_on_crash and default == second_entry.name


async def _test_resolution_falls_back_to_default():
    # 站在任何实例之外时，缺省实例就是「要管哪一个」的答案。
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        home = base / "home"
        elsewhere = base / "elsewhere"
        elsewhere.mkdir()
        target = _make_instance(base / "one")
        with patch.dict(os.environ, {"AKARIBOT_HOME": str(home), "AKARI_INSTANCE_DIR": ""}):
            registry = InstanceRegistry()
            entry = registry.add(target)
            # add() 会把第一个实例设为缺省，这里直接核对解析结果。
            found = resolve_instance_root(elsewhere)
            registry.remove(entry.name)
            empty = resolve_instance_root(elsewhere)
    return found == target.resolve() and empty is None


async def _test_cli_add_use_policy_remove():
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        home = base / "home"
        target = _make_instance(base / "one")
        added = _invoke(["add", str(target), "--name", "demo", "--locale", "zh_cn"], home=home)
        used = _invoke(["use", "demo"], home=home)
        policy = _invoke(["policy", "demo", "--autostart", "--restart-on-crash"], home=home)
        listed = _invoke(["list", "--json"], home=home)
        payload = json.loads(listed.stdout)
        removed = _invoke(["remove", "demo", "--yes"], home=home)
        missing = _invoke(["remove", "demo", "--yes"], home=home)
    return (
        added.exit_code == 0
        and used.exit_code == 0
        and policy.exit_code == 0
        and payload[0]["autostart"] is True
        and payload[0]["restart_on_crash"] is True
        and payload[0]["default"] is True
        and removed.exit_code == 0
        and missing.exit_code != 0
    )


async def _test_policy_requires_a_flag():
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        base = Path(raw)
        home = base / "home"
        target = _make_instance(base / "one")
        _invoke(["add", str(target), "--name", "demo"], home=home)
        result = _invoke(["policy", "demo"], home=home)
    return result.exit_code != 0


async def _test_probe_running_reports_unknown_when_unreadable():
    # 探测失败返回 None 而不是抛异常：清单里一格未知不该拖垮整页。
    with TemporaryDirectory(prefix="akari-reg-") as raw:
        root = Path(raw) / "broken"
        root.mkdir()
        with patch("akaribot.cli.instance.Instance.is_running", side_effect=RuntimeError("boom")):
            outcome = probe_running(root)
    return outcome is None


@func_case
async def test_instance_registry(tester: Tester):
    """cli.instances: 注册表与 instance 子命令测试"""
    _use_cli_locale()
    await tester.test(_test_add_list_remove, "登记、列出与移除")
    await tester.test(_test_duplicate_root_keeps_existing_entry, "同目录重复登记不产生第二条")
    await tester.test(_test_add_rejects_non_instance, "非实例目录拒绝登记")
    await tester.test(_test_policy_and_default, "策略与缺省实例写回注册表")
    await tester.test(_test_resolution_falls_back_to_default, "实例解析回落到缺省实例")
    await tester.test(_test_cli_add_use_policy_remove, "instance 子命令增删改查")
    await tester.test(_test_policy_requires_a_flag, "policy 未给参数时报错")
    await tester.test(_test_probe_running_reports_unknown_when_unreadable, "探测失败按未知处理")
    return tester
