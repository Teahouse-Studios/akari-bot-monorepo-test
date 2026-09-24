"""冻结产物的内置 uv 解析：来源顺序、可执行判据与 Windows 命名。

workflow 把 ``uv-bundled`` 打进 Nuitka onefile 并命名为 ``uv``，但 ``uv_binary()`` 原先只看
``AKARIBOT_UV`` 与 ``PATH``：没预装 uv 的用户机器上，冻结 CLI 的 init/module/venv/migrate 仍报
找不到 uv，内置资源形同虚设。此处固定三个来源的先后与各自的可执行判据。
"""

import os
import stat
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import CliError
from akaribot.testing import Tester, func_case

UV_ENV_VAR = engine.UV_ENV_VAR


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_executable(path: Path) -> Path:
    path.write_text("#!/bin/sh\n", encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _test_windows_prefers_exe_name():
    with patch.object(engine, "_windows_platform", return_value=True):
        windows = engine.bundled_uv_names()
    with patch.object(engine, "_windows_platform", return_value=False):
        posix = engine.bundled_uv_names()
    return windows == ("uv.exe", "uv") and posix == ("uv",)


def _test_executable_requires_a_real_file():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        (root / "uv").mkdir()
        directory_ok = engine.is_executable(root / "uv")
        missing_ok = engine.is_executable(root / "absent")
    return directory_ok is False and missing_ok is False


def _test_missing_execute_bit_is_repaired():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        path = Path(raw) / "uv"
        path.write_text("#!/bin/sh\n", encoding="utf-8")
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        before = os.access(path, os.X_OK)
        after = engine.is_executable(path)
    return before is False and after is True


def _test_non_frozen_never_reports_bundled():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        _make_executable(root / "uv")
        with (
            patch.object(engine, "is_frozen", return_value=False),
            patch.object(engine, "frozen_candidate_dirs", return_value=(root,)),
        ):
            found = engine.frozen_bundled_uv()
    return found is None


def _test_frozen_locates_bundled_uv_in_candidate_dirs():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        expected = _make_executable(root / "uv")
        with (
            patch.object(engine, "is_frozen", return_value=True),
            patch.object(engine, "frozen_candidate_dirs", return_value=(root / "absent", root)),
        ):
            found = engine.frozen_bundled_uv()
            resource_root = engine.frozen_resource_root()
    return found == expected and resource_root == root


def _test_candidate_dirs_include_compiled_dir():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        containing = Path(raw)

        class _Compiled:
            containing_dir = str(containing)

        with patch.dict(engine.__dict__, {"__compiled__": _Compiled()}):
            dirs = engine.frozen_candidate_dirs()
    return containing in dirs


def _test_override_wins_over_bundled():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        override = _make_executable(root / "custom-uv")
        bundled = _make_executable(root / "uv")
        with (
            patch.dict(os.environ, {UV_ENV_VAR: str(override)}),
            patch.object(engine, "is_frozen", return_value=True),
            patch.object(engine, "frozen_candidate_dirs", return_value=(root,)),
        ):
            resolved = engine.uv_binary()
    return resolved == str(override) and resolved != str(bundled)


def _test_bundled_wins_over_path():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        bundled = _make_executable(root / "uv")
        with (
            patch.dict(os.environ, {}, clear=False),
            patch.object(engine, "is_frozen", return_value=True),
            patch.object(engine, "frozen_candidate_dirs", return_value=(root,)),
            patch.object(engine.shutil, "which", return_value="/usr/local/bin/uv"),
        ):
            os.environ.pop(UV_ENV_VAR, None)
            resolved = engine.uv_binary()
    return resolved == str(bundled)


def _test_unusable_override_falls_back_instead_of_failing():
    with TemporaryDirectory(prefix="akari-frozen-uv-") as raw:
        root = Path(raw)
        bundled = _make_executable(root / "uv")
        with (
            patch.dict(os.environ, {UV_ENV_VAR: str(root / "typo")}),
            patch.object(engine, "is_frozen", return_value=True),
            patch.object(engine, "frozen_candidate_dirs", return_value=(root,)),
        ):
            resolved = engine.uv_binary()
    return resolved == str(bundled)


def _test_missing_everywhere_raises_with_hint():
    with (
        patch.dict(os.environ, {}, clear=False),
        patch.object(engine, "is_frozen", return_value=False),
        patch.object(engine.shutil, "which", return_value=None),
    ):
        os.environ.pop(UV_ENV_VAR, None)
        try:
            engine.uv_binary()
        except CliError as error:
            return "uv" in str(error)
    return False


@func_case
async def test_frozen_uv(tester: Tester):
    """cli.venv: 冻结产物内置 uv 解析测试"""
    _use_cli_locale()
    await tester.test(_test_windows_prefers_exe_name, "Windows 先试 uv.exe")
    await tester.test(_test_executable_requires_a_real_file, "目录与非文件不算可执行")
    await tester.test(_test_missing_execute_bit_is_repaired, "缺可执行位时补权限位")
    await tester.test(_test_non_frozen_never_reports_bundled, "非冻结不报告内置 uv")
    await tester.test(_test_frozen_locates_bundled_uv_in_candidate_dirs, "冻结时按候选目录定位内置 uv")
    await tester.test(_test_candidate_dirs_include_compiled_dir, "候选目录含 Nuitka 的 containing_dir")
    await tester.test(_test_override_wins_over_bundled, "显式覆盖优先于内置")
    await tester.test(_test_bundled_wins_over_path, "内置优先于 PATH")
    await tester.test(_test_unusable_override_falls_back_instead_of_failing, "覆盖不可用时回退")
    await tester.test(_test_missing_everywhere_raises_with_hint, "全都不可用时给出安装指引")
    return tester
