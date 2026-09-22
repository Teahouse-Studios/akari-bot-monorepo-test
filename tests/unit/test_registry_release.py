"""tools/verify_registry_release.py 的索引核对测试。

该工具是「包已发布、索引仍旧」这一部分成功状态的唯一闸门：它若漏判，push 到 gh-pages 的
就是一份指向旧版本的索引，而发布流程会显示为全绿。故逐条固定各段定位、版本比对与退出码。
"""

import importlib.util
import json
import tempfile
from pathlib import Path

from akaribot.testing import func_case, Tester

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "verify_registry_release.py"

REGISTRY_SAMPLE = {
    "schema": 1,
    "generated_at": "2026-01-01T00:00:00Z",
    "core": {"dist": "akari-bot-core", "latest": "0.3.0", "api_version": 1},
    "modules": [
        {"name": "wiki", "dist": "akari-bot-module-wiki", "latest": "0.2.0"},
        {"name": "no_latest", "dist": "akari-bot-module-blank"},
    ],
    "adapters": [{"name": "telegram", "dist": "akari-bot-adapter-telegram", "latest": "0.4.1"}],
}


def _tool():
    """按路径加载工具模块：tools/ 不是可导入包，只能显式加载。"""
    spec = importlib.util.spec_from_file_location("verify_registry_release", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_registry(payload) -> Path:
    """把索引写到临时文件，供按路径读取的入口使用。"""
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle, ensure_ascii=False)
    return Path(handle.name)


def _test_verify_locates_every_section():
    """core、modules、adapters 三段都能定位到本次发布的分发。"""
    tool = _tool()
    results = [
        tool.verify(REGISTRY_SAMPLE, "akari-bot-core", "0.3.0"),
        tool.verify(REGISTRY_SAMPLE, "akari-bot-module-wiki", "0.2.0"),
        tool.verify(REGISTRY_SAMPLE, "akari-bot-adapter-telegram", "0.4.1"),
    ]
    return all("索引核对通过" in line for line in results)


def _test_verify_normalizes_dist_name():
    """分发名按 PEP 503 规范化后比对，大小写与分隔符差异不算不一致。"""
    tool = _tool()
    tool.verify(REGISTRY_SAMPLE, "Akari_Bot.Module-Wiki", "0.2.0")
    return True


def _test_verify_rejects_stale_version():
    """latest 与本次版本不符时必须抛错，否则旧索引会被推上去。"""
    tool = _tool()
    try:
        tool.verify(REGISTRY_SAMPLE, "akari-bot-module-wiki", "0.3.0")
    except tool.VerifyError as error:
        return "0.2.0" in str(error) and "0.3.0" in str(error)
    return False


def _test_verify_rejects_unknown_dist():
    """索引里没有该分发时抛错，而不是静默通过。"""
    tool = _tool()
    try:
        tool.verify(REGISTRY_SAMPLE, "akari-bot-module-missing", "1.0.0")
    except tool.VerifyError as error:
        return "akari-bot-module-missing" in str(error)
    return False


def _test_verify_rejects_entry_without_latest():
    """条目缺 latest 时抛错：无从确认版本，不能当成通过。"""
    tool = _tool()
    try:
        tool.verify(REGISTRY_SAMPLE, "akari-bot-module-blank", "1.0.0")
    except tool.VerifyError as error:
        return "latest" in str(error)
    return False


def _test_main_exit_codes_follow_verification():
    """入口以退出码表达结论：一致为 0，不一致与文件不可读均为非 0。"""
    tool = _tool()
    registry = _write_registry(REGISTRY_SAMPLE)
    try:
        matched = tool.main(["--registry", str(registry), "--dist", "akari-bot-module-wiki", "--version", "0.2.0"])
        stale = tool.main(["--registry", str(registry), "--dist", "akari-bot-module-wiki", "--version", "9.9.9"])
        missing = tool.main(["--registry", str(registry.with_suffix(".absent")), "--dist", "x", "--version", "1"])
    finally:
        registry.unlink(missing_ok=True)
    return matched == 0 and stale == 2 and missing == 2


@func_case
async def test_registry_release(tester: Tester):
    """tools.verify_registry_release: 发布索引核对测试"""
    await tester.test(_test_verify_locates_every_section, "三段都能定位本次发布的分发")
    await tester.test(_test_verify_normalizes_dist_name, "分发名按 PEP 503 规范化比对")
    await tester.test(_test_verify_rejects_stale_version, "latest 与本次版本不符时抛错")
    await tester.test(_test_verify_rejects_unknown_dist, "索引缺少该分发时抛错")
    await tester.test(_test_verify_rejects_entry_without_latest, "条目缺 latest 时抛错")
    await tester.test(_test_main_exit_codes_follow_verification, "入口退出码跟随核对结论")
    return tester
