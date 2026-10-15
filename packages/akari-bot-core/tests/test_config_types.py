import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from contextlib import contextmanager
from pathlib import Path

from akaribot.core.config import CFGManager
from akaribot.testing import Tester, func_case


@contextmanager
def _instance():
    with tempfile.TemporaryDirectory(prefix="akari-config-types-") as raw:
        root = Path(raw)
        shutil.copytree(CFGManager.config_path, root / "config")
        web = root / "config" / "bot_web.toml"
        (root / "config" / "bot_web-alt.toml").write_text(
            web.read_text(encoding="utf-8")
            .replace("[bot_web]", "[bot_web-alt]")
            .replace("[bot_web_secret]", "[bot_web-alt_secret]"),
            encoding="utf-8",
        )
        yield root


def _run(root, *args):
    env = dict(os.environ, AKARI_INSTANCE_DIR=str(root))
    env.pop("AKARI_CONFIG_PATH", None)
    result = subprocess.run(
        [sys.executable, "-m", "akaribot.core.entrypoints.config", *args, "--json"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )
    return result.returncode, json.loads(result.stdout) if result.stdout.strip() else None


def _test_core_types_and_top_level_keys():
    with _instance() as root:
        for field, raw, expected in (
            ("enable_analytics", "false", False),
            ("tos_warning_counts", "12", 12),
            ("media_compression_threshold", "2.5", 2.5),
            ("command_prefix", '["~", "!"]', ["~", "!"]),
            ("default_locale", "zh_cn", "zh_cn"),
        ):
            code, payload = _run(root, "set", field, raw, "--table", "config")
            if code or type(payload["value"]) is not type(expected) or payload["value"] != expected:
                return False
        document = tomllib.loads((root / "config" / "config.toml").read_text(encoding="utf-8"))
        return document["config"]["enable_analytics"] is False and "default_locale" not in document["config"]


def _test_secret_and_instance_fields_keep_schema_types():
    with _instance() as root:
        cases = (
            ("secret", "db_path", "sqlite://database/typed.db", "sqlite://database/typed.db"),
            ("smtp_secret", "smtp_password", "typed password", "typed password"),
            ("bot_web-alt", "heartbeat_timeout", "13", 13),
            ("bot_web-alt_secret", "forwarded_allow_ips", '["127.0.0.1", "::1"]', ["127.0.0.1", "::1"]),
        )
        for table, field, raw, expected in cases:
            code, payload = _run(root, "set", field, raw, "--table", table)
            if code or payload["value"] != expected:
                return False
            code, payload = _run(root, "get", field, "--table", table)
            if code or payload["value"] != expected:
                return False
        code, schema = _run(root, "schema", "--table", "bot_web-alt_secret")
        field = next(item for item in schema if item["key"] == "forwarded_allow_ips")
        base = tomllib.loads((root / "config" / "bot_web.toml").read_text(encoding="utf-8"))
        return code == 0 and field["type"] == "list" and field["secret"] and base["bot_web"]["heartbeat_timeout"] == 5


def _test_invalid_values_leave_config_unchanged():
    with _instance() as root:
        before = {path.name: path.read_bytes() for path in (root / "config").glob("*.toml")}
        for field, value in (
            ("enable_analytics", "perhaps"),
            ("tos_warning_counts", "not-an-int"),
            ("media_compression_threshold", "NaN"),
            ("command_prefix", "[broken"),
            ("unknown_config_field", "value"),
        ):
            code, payload = _run(root, "set", field, value, "--table", "config")
            if code != 2 or payload is not None:
                return False
        after = {path.name: path.read_bytes() for path in (root / "config").glob("*.toml")}
        return before == after


def _test_invalid_input_does_not_generate_missing_defaults():
    from akaribot.core.constants.version import config_version

    with tempfile.TemporaryDirectory(prefix="akari-minimal-config-") as raw:
        root = Path(raw)
        (root / "config").mkdir()
        path = root / "config" / "config.toml"
        source = f'config_version = {config_version}\ndefault_locale = "zh_cn"\n[config]\nenable_analytics = true\n'
        path.write_text(source, encoding="utf-8")
        code, payload = _run(root, "set", "enable_analytics", "perhaps", "--table", "config")
        return (
            code == 2
            and payload is None
            and path.read_text(encoding="utf-8") == source
            and len(list((root / "config").glob("*.toml"))) == 1
        )


@func_case
async def test_config_types(tester: Tester):
    await tester.test(_test_core_types_and_top_level_keys, "核心布尔数值列表与顶层字段按声明写入")
    await tester.test(_test_secret_and_instance_fields_keep_schema_types, "密钥和实例表类型保持且不改基表")
    await tester.test(_test_invalid_values_leave_config_unchanged, "非法输入与未知字段拒绝且不改配置")
    await tester.test(_test_invalid_input_does_not_generate_missing_defaults, "最小配置拒绝非法输入时不补写其他默认值")
    return tester
