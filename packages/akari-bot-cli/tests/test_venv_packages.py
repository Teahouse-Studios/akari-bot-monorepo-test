"""``akaribot venv add/remove/status``：环境里的全部包与清单记录的运行库。

这一组命令是 uv 的薄封装：``add`` / ``remove`` 装卸运行库，``--save`` 决定要不要记进实例清单
（``akaribot.toml`` 的 ``runtime.requirements``，环境重建时按它补装）。用例不真的跑 uv：命令执行器
与探测结果都注入替身，只断言 argv、清单写回与 JSON 形态。
"""

import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from rich.console import Console
from typer.testing import CliRunner

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import venv as venv_command
from akaribot.cli.instance import InstanceMeta
from akaribot.testing import Tester, func_case


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


# 记录 uv 调用，不真的执行；dry_run 与 verbose 与真实执行器同名，命令层会原样传进来。
class _FakeRunner:
    # 命令层自行构造执行器，故按构造顺序留一份引用，供用例读回实际 argv。
    created: list["_FakeRunner"] = []

    def __init__(self, *, dry_run: bool = False, verbose: bool = False) -> None:
        self.dry_run = dry_run
        self.verbose = verbose
        self.calls: list[list[str]] = []
        _FakeRunner.created.append(self)

    def run_checked(self, argv, *, what, env=None, stream=False) -> None:
        """记下 argv，不执行。"""
        self.calls.append([str(item) for item in argv])


def _instance(tmp: Path, *, requirements: tuple[str, ...] = ()):
    root = tmp / "instance"
    (root / engine.venv_python_path(Path(".venv")).parent).mkdir(parents=True, exist_ok=True)
    instance = engine.Instance.detached(root, venv=".venv")
    if requirements:
        instance.meta.set_requirements(list(requirements))
    instance.meta.save()
    # 解释器存在与否只影响状态探测，写个占位文件即可。
    engine.venv_python_path(root / ".venv").write_text("", encoding="utf-8")
    return instance


def _installed(*items: engine.InstalledDist) -> dict[str, engine.InstalledDist]:
    return {engine.canonical(item.dist): item for item in items}


def _invoke(instance, argv: list[str]):
    _FakeRunner.created.clear()
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    with (
        patch.object(venv_command, "require_instance", return_value=instance),
        patch.object(venv_command, "console", console),
        patch.object(engine, "CommandRunner", _FakeRunner),
    ):
        result = CliRunner().invoke(venv_command.app, argv)
    runner = _FakeRunner.created[-1] if _FakeRunner.created else _FakeRunner()
    return result, runner, buffer.getvalue() or result.stdout


def _requirements(instance) -> tuple[str, ...]:
    return InstanceMeta.load(instance.root).requirements


def _test_status_json_lists_every_distribution():
    # 界面据此管理环境：装了什么、哪些是 AkariBot 的、哪些记在清单里，一次取齐。
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw), requirements=("httpx>=0.27",))
        found = _installed(
            engine.InstalledDist("akari-bot-core", "0.1.0"),
            engine.InstalledDist("httpx", "0.28.1", requires=("certifi",)),
            engine.InstalledDist("certifi", "2025.1.31"),
        )
        with patch.object(engine, "probe_environment", return_value=found):
            result, _runner, _text = _invoke(instance, ["status", "--json"])
        payload = json.loads(result.stdout)
    by_name = {item["dist"]: item for item in payload["installed"]}
    return (
        result.exit_code == 0
        and payload["requirements"] == ["httpx>=0.27"]
        and payload["installed_count"] == 3
        and payload["package_count"] == 1
        and payload["core_version"] == "0.1.0"
        and by_name["httpx"]["recorded"] is True
        and by_name["certifi"]["recorded"] is False
        and by_name["akari-bot-core"]["akari"] is True
        and by_name["httpx"]["akari"] is False
        and by_name["httpx"]["requires"] == ["certifi"]
    )


def _test_add_saves_pinned_spec():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        with patch.object(
            engine, "probe_environment", return_value=_installed(engine.InstalledDist("httpx", "0.28.1"))
        ):
            result, runner, _text = _invoke(instance, ["add", "httpx"])
        recorded = _requirements(instance)
    return (
        result.exit_code == 0
        and recorded == ("httpx==0.28.1",)
        and any("install" in call and call[-1] == "httpx" for call in runner.calls)
    )


def _test_add_without_save_keeps_manifest():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        with patch.object(
            engine, "probe_environment", return_value=_installed(engine.InstalledDist("httpx", "0.28.1"))
        ):
            result, runner, _text = _invoke(instance, ["add", "httpx", "--no-save"])
        recorded = _requirements(instance)
    return result.exit_code == 0 and recorded == () and runner.calls != []


def _test_add_dry_run_changes_nothing():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        result, runner, _text = _invoke(instance, ["add", "httpx", "--dry-run"])
        recorded = _requirements(instance)
    # 试运行由执行器自己短路：命令层仍然构造执行器并下发 argv，但不落盘也不写清单。
    return result.exit_code == 0 and recorded == () and runner.dry_run is True and runner.calls != []


def _test_add_repository_url_records_named_spec():
    # 直接粘贴仓库地址：补 git+ 前缀，装完按 direct_url 反查分发名再记录。
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        found = _installed(engine.InstalledDist("requests", "2.32.3", url="git+https://github.com/psf/requests"))
        with patch.object(engine, "probe_environment", return_value=found):
            result, runner, _text = _invoke(instance, ["add", "https://github.com/psf/requests"])
        recorded = _requirements(instance)
    return (
        result.exit_code == 0
        and recorded == ("requests @ git+https://github.com/psf/requests",)
        and any(call[-1] == "git+https://github.com/psf/requests" for call in runner.calls)
    )


def _test_add_unresolvable_reference_warns_and_skips_record():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        with patch.object(engine, "probe_environment", return_value=_installed()):
            result, _runner, _text = _invoke(instance, ["add", "git+https://example.invalid/repo"])
        recorded = _requirements(instance)
    # 警告经 stderr 输出，CliRunner 把两路合在 output 里。
    return result.exit_code == 0 and recorded == () and "git+https://example.invalid/repo" in result.output


def _test_remove_save_drops_record():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw), requirements=("httpx>=0.27",))
        with patch.object(
            engine, "probe_environment", return_value=_installed(engine.InstalledDist("httpx", "0.28.1"))
        ):
            result, runner, _text = _invoke(instance, ["remove", "httpx"])
        recorded = _requirements(instance)
    return (
        result.exit_code == 0
        and recorded == ()
        and any("uninstall" in call and call[-1] == "httpx" for call in runner.calls)
    )


def _test_remove_without_save_keeps_record():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw), requirements=("httpx>=0.27",))
        with patch.object(
            engine, "probe_environment", return_value=_installed(engine.InstalledDist("httpx", "0.28.1"))
        ):
            result, runner, _text = _invoke(instance, ["remove", "httpx", "--no-save"])
        recorded = _requirements(instance)
    return result.exit_code == 0 and recorded == ("httpx>=0.27",) and runner.calls != []


def _test_remove_record_without_install_only_drops_record():
    # 记录还在、环境里已经没有了：卸载无处可卸，但仍要能删掉清单里的记录。
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw), requirements=("httpx>=0.27",))
        with patch.object(engine, "probe_environment", return_value=_installed()):
            result, runner, _text = _invoke(instance, ["remove", "httpx"])
        recorded = _requirements(instance)
    return result.exit_code == 0 and recorded == () and runner.calls == []


def _test_remove_absent_fails():
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        instance = _instance(Path(raw))
        with patch.object(engine, "probe_environment", return_value=_installed()):
            result, runner, _text = _invoke(instance, ["remove", "nosuchpkg"])
    return result.exit_code != 0 and runner.calls == []


def _test_recreate_reinstalls_recorded_requirements():
    # 记录在清单里的运行库要跟着环境重建走；没有记录时不多发一次 uv 调用。
    with TemporaryDirectory(prefix="akari-venv-") as raw:
        root = Path(raw)
        instance = _instance(root, requirements=("httpx>=0.27", "git+https://github.com/psf/requests"))
        runner = _FakeRunner()
        installed = engine.install_runtime_requirements(instance, instance.python, runner=runner)
        empty_root = root / "empty"
        empty_root.mkdir()
        plain = _instance(empty_root)
        nothing = engine.install_runtime_requirements(plain, plain.python, runner=runner)
    return (
        installed == ("httpx>=0.27", "git+https://github.com/psf/requests")
        and len(runner.calls) == 1
        and "httpx>=0.27" in runner.calls[0]
        and nothing == ()
        and len(runner.calls) == 1
    )


def _test_probe_sees_distributions_without_entry_points():
    # 探针按分发名前缀判定 AkariBot 包：资源包这类没有入口点的分发也必须被枚举到。
    found = engine.probe_environment(engine.system_python())
    return "akari-bot-core" in found and "akari-bot-html2text" in found


@func_case
async def test_venv_packages(tester: Tester):
    """cli.venv: 环境包清单与运行库装卸测试"""
    _use_cli_locale()
    await tester.test(_test_status_json_lists_every_distribution, "status --json 列出全部分发与记录标记")
    await tester.test(_test_add_saves_pinned_spec, "add 记录补版本的需求串")
    await tester.test(_test_add_without_save_keeps_manifest, "--no-save 只装不记录")
    await tester.test(_test_add_dry_run_changes_nothing, "试运行不改环境也不改清单")
    await tester.test(_test_add_repository_url_records_named_spec, "仓库地址补 git+ 并记录分发名")
    await tester.test(_test_add_unresolvable_reference_warns_and_skips_record, "认不出分发名时只装不记录")
    await tester.test(_test_remove_save_drops_record, "remove 同时删记录并卸载")
    await tester.test(_test_remove_without_save_keeps_record, "--no-save 卸载但保留记录")
    await tester.test(_test_remove_record_without_install_only_drops_record, "环境里没有时只删记录")
    await tester.test(_test_remove_absent_fails, "既没装也没记录时报错")
    await tester.test(_test_recreate_reinstalls_recorded_requirements, "环境重建按清单补装运行库")
    await tester.test(_test_probe_sees_distributions_without_entry_points, "探针按前缀认出无入口点的 AkariBot 包")

    return tester
