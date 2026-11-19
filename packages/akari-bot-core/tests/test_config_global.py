"""全局默认配置与用户配置覆盖的单元测试。"""

import json
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from akaribot.core.builtins.config import CFGManager
from akaribot.testing import func_case, Tester

MINIMAL_CONFIG = """[config]
debug = false
"""


@contextmanager
def _temp_config():
    original_path = CFGManager.config_path
    original_readonly = CFGManager.readonly

    tmp = Path(tempfile.mkdtemp(prefix="akari_cfg_global_"))
    try:
        (tmp / "config.toml").write_text(MINIMAL_CONFIG, encoding="utf-8")
        (tmp / "global").mkdir()
        (tmp / "config.toml").write_text('[config]\ndebug = false\nname = "user"\n', encoding="utf-8")
        (tmp / "global" / "config.global.toml").write_text(
            '[config]\ndebug = true\nname = "global"\nfallback = 7\n', encoding="utf-8"
        )
        (tmp / "global" / "jobqueue.global.json").write_text(
            json.dumps({"jobqueue": {"node_id": "global-node", "workers": 2}}), encoding="utf-8"
        )
        CFGManager.switch_config_path(tmp)
        CFGManager.readonly = False
        yield tmp
    finally:
        CFGManager.readonly = original_readonly
        CFGManager.switch_config_path(original_path)
        shutil.rmtree(tmp, ignore_errors=True)


def _test_user_values_override_global_values():
    with _temp_config():
        config = CFGManager.document("config")["config"]
        return config["debug"] is False and config["name"] == "user" and config["fallback"] == 7


def _test_json_global_table_is_readable():
    with _temp_config():
        jobqueue = CFGManager.document("jobqueue")["jobqueue"]
        return jobqueue["node_id"] == "global-node" and jobqueue["workers"] == 2


def _test_write_only_persists_user_file():
    with _temp_config() as tmp:
        CFGManager.write("name", "changed", str, table_name="config")
        user = (tmp / "config.toml").read_text(encoding="utf-8")
        default = (tmp / "global" / "config.global.toml").read_text(encoding="utf-8")
        return 'name = "changed"' in user and "fallback" not in user and 'name = "global"' in default


def _test_delete_falls_back_to_global_value():
    with _temp_config():
        CFGManager.delete("name", "config")
        config = CFGManager.document("config")["config"]
        return config["name"] == "global" and config["fallback"] == 7


@func_case
async def test_config_global(tester: Tester):
    """core.config: 全局默认配置与用户覆盖测试"""
    await tester.test(_test_user_values_override_global_values, "用户配置覆盖全局默认值")
    await tester.test(_test_json_global_table_is_readable, "JSON 全局配置可读取")
    await tester.test(_test_write_only_persists_user_file, "写回只落用户文件")
    await tester.test(_test_delete_falls_back_to_global_value, "删除用户键后回退到全局值")
    return tester
