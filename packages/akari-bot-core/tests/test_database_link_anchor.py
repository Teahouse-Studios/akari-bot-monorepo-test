"""SQLite 链接锚定实例根的回归测试。

默认链接是相对路径 ``sqlite://database/save.db``，驱动按进程 cwd 解析它；core 入口若不是从
实例根启动，库就会建到调用目录。这里既校验链接解析规则，也实测「cwd 在实例外」的子进程。
"""

import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.core.constants import config_filename
from akaribot.core.constants.path import CONFIG_PATH_ENV, INSTANCE_DIR_ENV
from akaribot.core.constants.version import config_version
from akaribot.core.database.link import prepare_db_link
from akaribot.core.paths import Paths
from akaribot.testing import Tester, func_case


def _file_target(link: str) -> str:
    return link.split("://", 1)[1].partition("?")[0]


def _test_relative_sqlite_is_anchored_to_instance():
    link = prepare_db_link("sqlite://database/save.db")
    target = Path(_file_target(link))
    return (
        target.is_absolute()
        and target == Paths.instance / "database" / "save.db"
        and "busy_timeout=30000" in link
        and "journal_mode=WAL" in link
    )


def _test_relative_subdirectory_is_anchored_to_instance():
    target = Path(_file_target(prepare_db_link("sqlite://db/sub/save.db")))
    return target == Paths.instance / "db" / "sub" / "save.db"


def _test_absolute_and_memory_links_are_untouched():
    absolute = _file_target(prepare_db_link("sqlite:///tmp/akari-anchor/save.db"))
    memory = _file_target(prepare_db_link("sqlite://:memory:"))
    return absolute == "/tmp/akari-anchor/save.db" and memory == ":memory:"


def _test_windows_drive_path_is_not_anchored():
    target = _file_target(prepare_db_link("sqlite://C:/akari/save.db"))
    return target == "C:/akari/save.db"


def _test_non_sqlite_links_are_untouched():
    link = prepare_db_link("mysql+asyncmy://user:pass@localhost/akari?charset=utf8mb4")
    return link == "mysql://user:pass@localhost/akari?charset=utf8mb4"


def _write_minimal_config(config_dir: Path) -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / config_filename).write_text(
        f'default_locale = "zh_cn"\nconfig_version = {config_version}\n',
        encoding="utf-8",
    )


def _test_entrypoint_keeps_artifacts_inside_instance():
    with TemporaryDirectory() as temp:
        base = Path(temp)
        instance_root = base / "instance"
        caller = base / "caller"
        _write_minimal_config(instance_root / "config")
        caller.mkdir()
        env = dict(os.environ)
        env[INSTANCE_DIR_ENV] = str(instance_root)
        env.pop(CONFIG_PATH_ENV, None)
        env["PYTHONIOENCODING"] = "UTF-8"
        try:
            completed = subprocess.run(  # noqa: S603
                [sys.executable, "-m", "akaribot.core.entrypoints.db", "upgrade", "--json"],
                cwd=str(caller),
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=180.0,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return (
            completed.returncode == 0
            and (instance_root / "database" / "save.db").is_file()
            and (instance_root / "database" / "local.db").is_file()
            and (instance_root / "config" / "jobqueue.toml").is_file()
            and (instance_root / "logs").is_dir()
            and list(caller.iterdir()) == []
        )


@func_case
async def test_database_link_anchoring(tester: Tester):
    """相对 SQLite 链接锚定实例根，绝对路径、内存库与非 SQLite 链接不受影响。"""
    await tester.test(_test_relative_sqlite_is_anchored_to_instance, "相对链接锚定实例根")
    await tester.test(_test_relative_subdirectory_is_anchored_to_instance, "相对子目录锚定实例根")
    await tester.test(_test_absolute_and_memory_links_are_untouched, "绝对路径与内存库保持原样")
    await tester.test(_test_windows_drive_path_is_not_anchored, "Windows 盘符路径保持原样")
    await tester.test(_test_non_sqlite_links_are_untouched, "非 SQLite 链接保持原样")
    await tester.test(_test_entrypoint_keeps_artifacts_inside_instance, "cwd 在实例外时产物只落实例根")
    return tester
