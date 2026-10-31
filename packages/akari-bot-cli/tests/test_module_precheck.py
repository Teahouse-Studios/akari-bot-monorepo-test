"""``module add`` 的兼容性预检。

``uv pip install`` 求解时不看其他已装包的依赖，预检因此按 uv 的安装计划（``--dry-run``）核对全部已装包：
待装包要求的依赖版本只是需要调整时放行并提示，计划会破坏已装包或 uv 无解时拦截。用例不真的跑 uv，
安装计划与环境探测都注入替身。
"""

import io
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from rich.console import Console
from typer import Exit

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import module as module_command
from akaribot.testing import Tester, func_case

DICE = engine.InstallTarget(
    dist="akari-bot-module-dice", specs=("akari-bot-module-dice",), dependencies=("numpy<2.5.3",)
)
WEB = engine.InstallTarget(dist="akari-bot-adapter-web", specs=("akari-bot-adapter-web",), dependencies=("pillow",))


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _dist(name: str, version: str, *requires: str) -> engine.InstalledDist:
    return engine.InstalledDist(dist=name, version=version, requires=requires)


def _environment(*dists: engine.InstalledDist) -> dict[str, engine.InstalledDist]:
    return {engine.canonical(item.dist): item for item in dists}


def _precheck(target: engine.InstallTarget, installed, plan: str, *, returncode: int = 0) -> tuple[bool, str]:
    buffer = io.StringIO()
    instance = SimpleNamespace(python=Path("/instance/python"), api_version=lambda: 1)
    completed = subprocess.CompletedProcess([], returncode, stdout="", stderr=plan)
    with (
        patch.object(module_command, "console", Console(file=buffer, width=400)),
        patch.object(engine, "uv_binary", return_value="uv"),
        patch.object(engine, "probe_environment", return_value=installed),
        patch.object(engine.CommandRunner, "run", return_value=completed),
    ):
        try:
            module_command._precheck(instance, target, force=False)
        except Exit:
            return False, buffer.getvalue()
    return True, buffer.getvalue()


def _test_adjustable_dependency_passes_with_notice():
    # 已装包对 numpy 的要求在新版本下仍满足；只在请求 extra 时生效的依赖不参与判断。
    installed = _environment(
        _dist("numpy", "2.5.3"),
        _dist("matplotlib", "3.10.0", "numpy>=1.25"),
        _dist("pint", "0.24", "numpy>=2.5.3; extra == 'numpy'"),
    )
    passed, output = _precheck(DICE, installed, " - numpy==2.5.3\n + numpy==2.5.2\n")
    notice = i18n.t(
        "cli.module.precheck.adjust",
        dist=DICE.dist,
        requirement="numpy",
        specifier="<2.5.3",
        current="2.5.3",
        version="2.5.2",
    )
    return passed and notice in output


def _test_editable_packages_are_judged_by_source():
    # 可编辑安装的元数据停在安装那一刻；源码已放宽的约束不应再拦截依赖升级。
    with TemporaryDirectory(prefix="akari-precheck-") as raw:
        source = Path(raw)
        (source / "pyproject.toml").write_text(
            '[project]\nname = "akari-bot-module-wiki"\ndependencies = ["attrs>=26.1.0"]\n', encoding="utf-8"
        )
        wiki = engine.InstalledDist(
            dist="akari-bot-module-wiki",
            version="0.1.0",
            path=source,
            editable=True,
            requires=("pillow<13.0.0,>=12.0.0",),
        )
        installed = _environment(_dist("pillow", "12.3.0"), wiki)
        passed, _ = _precheck(WEB, installed, " - pillow==12.3.0\n + pillow==13.0.0\n")
    return passed


def _test_plan_that_breaks_installed_packages_is_blocked():
    # 直接依赖与传递依赖的调整都要核对；uv 无解时同样拦截并给出原因。
    cases = [
        (
            DICE,
            _environment(_dist("numpy", "2.5.3"), _dist("needs-new-numpy", "0.1", "numpy>=2.5.3")),
            " - numpy==2.5.3\n + numpy==2.5.2\n",
            0,
            i18n.t(
                "cli.venv_engine.conflict_change_breaks",
                installed="needs-new-numpy",
                requirement="numpy",
                specifier=">=2.5.3",
                version="2.5.2",
            ),
        ),
        (
            WEB,
            _environment(_dist("pillow", "12.3.0"), _dist("akari-bot-module-wiki", "0.1.0", "pillow<13.0.0,>=12.0.0")),
            " - pillow==12.3.0\n + pillow==13.0.0\n + akari-bot-adapter-web==0.1.0\n",
            0,
            i18n.t(
                "cli.venv_engine.conflict_change_breaks",
                installed="akari-bot-module-wiki",
                requirement="pillow",
                specifier="<13.0.0,>=12.0.0",
                version="13.0.0",
            ),
        ),
        (
            DICE,
            _environment(_dist("numpy", "2.5.3")),
            "Because numpy<2.5.3 is unavailable, we can conclude that the requirements are unsatisfiable.\n",
            1,
            "Because numpy<2.5.3 is unavailable",
        ),
    ]
    for target, installed, plan, returncode, expected in cases:
        passed, output = _precheck(target, installed, plan, returncode=returncode)
        if passed or expected not in output:
            return False
    return True


def _test_api_version_probe_reads_core_constant():
    # 预检据此判断 requires_core_api；读错位置时恒为 None，兼容性检查会被静默跳过。
    return isinstance(engine.probe_api_version(Path(sys.executable)), int)


@func_case
async def test_module_precheck(tester: Tester):
    """cli.commands.module: 安装前兼容性预检测试"""
    _use_cli_locale()
    await tester.test(_test_adjustable_dependency_passes_with_notice, "可调整的依赖版本放行并提示")
    await tester.test(_test_editable_packages_are_judged_by_source, "可编辑安装按源码声明的依赖核对")
    await tester.test(_test_plan_that_breaks_installed_packages_is_blocked, "安装计划破坏已装包或无解时拦截")
    await tester.test(_test_api_version_probe_reads_core_constant, "core API 版本探针读到整数版本")
    return tester
