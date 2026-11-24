"""配置入口的占位符统计（``entrypoints/config.py`` 的 ``placeholders`` 子命令）。

概览页与 ``akaribot config placeholders`` 共用这一份判定：计数按 core 的 ``PLACEHOLDER_PATTERN``
逐表给出，注释与字符串里的同形文本不计入，损坏或读不到的表进 ``failed``。用例在隔离子进程中运行
真实入口，检查计数边界与失败归集。

另覆盖 ``schema`` 对适配器 ``enable`` 的注释取键。未覆盖：``schema`` / ``set`` 的其余行为，那些由配置文件
与 CLI 侧用例覆盖。
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
    # 引导代码可能为整个测试进程设置过配置目录，子进程必须仅使用本次的实例根目录。
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
    # 注释中的示例文本与字符串值中内嵌的同形文本均不构成占位项，仅当完整值等于标记时才计入统计。
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
    # 占位标记格式按照 core 的正则表达式判定，无后缀标记与带后缀、带类型说明的写法均计入统计，同一表内逐项累计。
    with _instance() as root:
        (root / "config" / "config.toml").write_text(SUFFIX_CONFIG, encoding="utf-8")
        code, payload = _run(root)
    return code == 0 and payload["tables"]["config"] == {"placeholder": 3, "total": 3} and payload["count"] == 3


async def _test_broken_table_is_reported_not_skipped():
    # 单张表解析失败或编码非 UTF-8 时，仅将该表记入 failed，其余表正常执行统计，命令仍然以退出码 0 结束。
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
    # 缺少文件与包含路径分隔符的表名各保留一条原因说明，由于表名称仅用于拼接配置目录下的文件名。
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
    # 未传入 --tables 参数时遍历配置目录下的全部数据表，逐表输出占位项与总项数，并汇总总数量。
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


async def _test_adapter_enable_comment_is_localized():
    # 实例配置文件的注释提取自 schema，缺少专属注释时采用各适配器共用的 enable 注释，不输出 {I18N:...} 标记。
    with _instance() as root:
        (root / "config" / "config.toml").write_text('default_locale = "zh_cn"\n', encoding="utf-8")
        (root / "config" / "bot_demo-alt.toml").write_text("[bot_demo-alt]\nenable = false\n", encoding="utf-8")
        env = dict(os.environ, AKARI_INSTANCE_DIR=str(root))
        env.pop("AKARI_CONFIG_PATH", None)
        result = subprocess.run(
            [sys.executable, "-m", ENTRYPOINT, "schema", "--table", "bot_demo-alt", "--json"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
            check=False,
        )
    rows = json.loads(result.stdout) if result.stdout.strip() else []
    comment = next((row["comment"] for row in rows if row["key"] == "enable"), None)
    return result.returncode == 0 and comment and "I18N" not in comment and "config.comments" not in comment


async def _test_sync_reloads_new_adapter_table():
    # 适配器配置模板在导入阶段写入磁盘。入口必须在读取 schema 前重新加载配置，
    # 避免首次安装阶段配置表尚不存在而导致配置补全流程失败。
    with _instance() as root:
        (root / "config" / "config.toml").write_text('default_locale = "zh_cn"\n', encoding="utf-8")
        fake = root / "fake-site"
        adapter = fake / "fakeadapter"
        adapter.mkdir(parents=True)
        (adapter / "__init__.py").write_text("", encoding="utf-8")
        (adapter / "manifest.toml").write_text(
            'schema = 1\nrequires_core_api = ">=1"\nconfig_table = "bot_demo"\n', encoding="utf-8"
        )
        (adapter / "config.py").write_text(
            "from pathlib import Path\n"
            "from akaribot.core.paths import Paths\n"
            "(Path(Paths.config) / 'bot_demo.toml').write_text("
            "'[bot_demo]\\nenable = false\\n[bot_demo_secret]\\ntoken = \"<Replace me with str value>\"\\n',"
            " encoding='utf-8')\n",
            encoding="utf-8",
        )
        dist = fake / "fake_adapter-0.1.0.dist-info"
        dist.mkdir()
        (dist / "METADATA").write_text("Metadata-Version: 2.1\nName: fake-adapter\nVersion: 0.1.0\n", encoding="utf-8")
        (dist / "entry_points.txt").write_text("[akaribot.adapters]\ndemo = fakeadapter\n", encoding="utf-8")
        env = dict(os.environ, AKARI_INSTANCE_DIR=str(root), PYTHONPATH=str(fake))
        env.pop("AKARI_CONFIG_PATH", None)
        result = subprocess.run(
            [sys.executable, "-m", ENTRYPOINT, "sync", "--package", "fake-adapter"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
            check=False,
        )
    return result.returncode == 0 and "bot_demo" in result.stdout and "占位 1 项" in result.stdout


@func_case
async def test_entrypoint_config(tester: Tester):
    """core.entrypoints.config 占位符统计入口测试"""
    await tester.test(_test_comment_and_string_are_not_counted, "注释与字符串里的同形文本不计入")
    await tester.test(_test_suffixed_marker_variants_are_counted, "带后缀的标记按项计入")
    await tester.test(_test_broken_table_is_reported_not_skipped, "解析失败与乱码表进 failed")
    await tester.test(_test_missing_table_and_separator_are_rejected, "缺表与含分隔符的表名进 failed")
    await tester.test(_test_default_scan_covers_every_table, "默认遍历配置目录下的全部表")
    await tester.test(_test_adapter_enable_comment_is_localized, "schema 给适配器 enable 输出已翻译的注释")
    await tester.test(_test_sync_reloads_new_adapter_table, "config sync 在导入新适配器后重新加载配置")
    return tester
