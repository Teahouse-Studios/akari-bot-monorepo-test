"""配置入口的占位符统计（``entrypoints/config.py`` 的 ``placeholders`` 子命令）。

概览页与 ``akaribot config placeholders`` 共用这一份判定：计数按 core 的 ``PLACEHOLDER_PATTERN``
逐表给出，注释与字符串里的同形文本不计入，损坏或读不到的表进 ``failed``。用例在隔离子进程里跑
真实入口，断言计数边界与失败归集。

未覆盖：``schema`` / ``set`` 等既有子命令的行为，那些由配置文件与 CLI 侧用例覆盖。
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from akaribot.testing import Tester, func_case

ENTRYPOINT = "akaribot.core.entrypoints.config"

INSTANCE_CONFIG = """config_version = 6
default_locale = "zh_cn"

[config]
debug = false
ffmpeg_path = "<Replace me with str value>"
suffixed = "<Replace me with (str, int) value>"
note = "文档里的 <Replace me> 字样"
# 注释里的示例：<Replace me>
"""

SUFFIX_CONFIG = """[config]
plain = "<Replace me>"
typed = "<Replace me with (str, int) value>"
described = "<Replace me 的取值说明>"
"""

PARTNER_CONFIG = """[bot_telegram]
telegram_token = "<Replace me with str value>"
telegram_api_url = "https://api.telegram.org"
"""


@contextmanager
def _instance():
    root = Path(tempfile.mkdtemp(prefix="akari-config-entry-"))
    (root / "config").mkdir()
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _run(root: Path, *args: str) -> tuple[int, dict]:
    env = dict(os.environ, AKARI_INSTANCE_DIR=str(root))
    # 引导代码可能为整个测试进程设过配置目录，子进程必须只认本次的实例根。
    env.pop("AKARI_CONFIG_PATH", None)
    result = subprocess.run(
        [sys.executable, "-m", ENTRYPOINT, "placeholders", *args, "--json"],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    payload = json.loads(result.stdout) if result.stdout.strip() else {}
    return result.returncode, payload


async def _test_comment_and_string_are_not_counted():
    # 注释里的示例文本与字符串值里嵌的同形文本都不构成占位项，只有整值等于标记才算。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(INSTANCE_CONFIG, encoding="utf-8")
        code, payload = _run(root)
    return (
        code == 0
        and payload["tables"] == {"config": {"placeholder": 2, "total": 4}}
        and payload["count"] == 2
        and payload["scanned"] == ["config"]
        and payload["failed"] == {}
    )


async def _test_suffixed_marker_variants_are_counted():
    # 标记形状按 core 的正则判定：裸标记与带后缀、带类型说明的写法都算，同一表内逐项累计。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(SUFFIX_CONFIG, encoding="utf-8")
        code, payload = _run(root)
    return code == 0 and payload["tables"]["config"] == {"placeholder": 3, "total": 3} and payload["count"] == 3


async def _test_broken_table_is_reported_not_skipped():
    # 单张表解析失败或不是 UTF-8 时只把该表记入 failed，其余表照常统计，命令仍以 0 退出。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(SUFFIX_CONFIG, encoding="utf-8")
        (root / "config" / "broken.toml").write_text("not = = toml\n", encoding="utf-8")
        (root / "config" / "binary.toml").write_bytes(b"\xff\xfe\x00<Replace me>")
        code, payload = _run(root)
    return (
        code == 0
        and payload["count"] == 3
        and payload["scanned"] == ["config"]
        and set(payload["tables"]) == {"config"}
        and "解析失败" in payload["failed"]["broken"]
        and "读取失败" in payload["failed"]["binary"]
    )


async def _test_missing_table_and_separator_are_rejected():
    # 缺文件与含路径分隔符的表名各留一条原因：表名只用于拼接配置目录下的文件名。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(SUFFIX_CONFIG, encoding="utf-8")
        code, payload = _run(root, "--tables", "config,absent,../outside")
    return (
        code == 0
        and payload["scanned"] == ["config"]
        and "读取失败" in payload["failed"]["absent"]
        and payload["failed"]["../outside"] == "表名含路径分隔符"
        and "outside" not in payload["tables"]
    )


async def _test_default_scan_covers_every_table():
    # 缺 --tables 时遍历配置目录下的全部表，逐表给出占位与总项数，并汇总总数。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(SUFFIX_CONFIG, encoding="utf-8")
        (root / "config" / "bot_telegram.toml").write_text(PARTNER_CONFIG, encoding="utf-8")
        (root / "config" / "empty.toml").write_text('[empty]\nkey = "value"\n', encoding="utf-8")
        code, payload = _run(root)
    return (
        code == 0
        and payload["scanned"] == ["bot_telegram", "config", "empty"]
        and payload["tables"]["config"] == {"placeholder": 3, "total": 3}
        and payload["tables"]["bot_telegram"] == {"placeholder": 1, "total": 2}
        and payload["tables"]["empty"] == {"placeholder": 0, "total": 1}
        and payload["count"] == 4
        and payload["failed"] == {}
    )


@func_case
async def test_entrypoint_config(tester: Tester):
    """core.entrypoints.config: 占位符统计入口测试"""
    await tester.test(_test_comment_and_string_are_not_counted, "注释与字符串里的同形文本不计入")
    await tester.test(_test_suffixed_marker_variants_are_counted, "带后缀的标记按项计入")
    await tester.test(_test_broken_table_is_reported_not_skipped, "解析失败与乱码表进 failed")
    await tester.test(_test_missing_table_and_separator_are_rejected, "缺表与含分隔符的表名进 failed")
    await tester.test(_test_default_scan_covers_every_table, "缺省遍历配置目录下的全部表")
    return tester
