"""多实例身份模型单元测试。

覆盖阶段 1B：

- 身份派生（T1B.1 / T1B.2）：默认实例的 client_name 逐字节不变，实例名带 ``-<实例 ID>``；
- 配置的实例作用域（T1B.3）：实例表存在时接管读取、``enable`` 不回退、写入只落实例表；
- 守护进程的实例发现与前置冲突检查（T1B.4）：孤立配置只告警，端口与凭据冲突中止启动；
- 四元组平台判据（T1B.5）：``available_for="Telegram"`` 覆盖全部 Telegram 实例，
  ``_return_cache`` 不把两个实例的结果混在一起。

守护进程与配置表的用例一律使用临时配置目录，退出时完整还原 CFGManager 与 Info 的类属性。
"""

import ast
import importlib
import shutil
import tempfile
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import bot as daemon
from core.alive import Alive
from core.config import CFGManager
from core.constants import Info
from core.loader import ModulesManager
from core.registry import PackageEntry, PackageManifest, PackageRegistry
from core.tester import Tester, func_case
from core.types import Module
from core.types.module.component_meta import CommandMeta, EventMeta

# 目录名 → 平台展示名。onebot 与 milky 都为 "QQ"：二者是同一批账号与场景数据的两种协议接入。
PLATFORM_NAMES = {
    "discord": "Discord",
    "kook": "KOOK",
    "matrix": "Matrix",
    "milky": "QQ",
    "onebot": "QQ",
    "qqbot": "QQBot",
    "telegram": "Telegram",
    "web": "Web",
}

BASE_CONFIG = 'default_locale = "zh_cn"\nconfig_version = 3\n[config]\n[secret]\n'

SCOPE_CONFIG_FILES = {
    "config.toml": BASE_CONFIG,
    "bot_telegram.toml": (
        '[bot_telegram]\nenable = true\ntelegram_api_url = "https://base.example"\n'
        '[bot_telegram_secret]\ntelegram_token = "base-token"\n'
    ),
    "bot_telegram-alt.toml": (
        '[bot_telegram-alt]\nenable = false\ntelegram_api_url = "https://alt.example"\n'
        '[bot_telegram-alt_secret]\ntelegram_token = "alt-token"\n'
    ),
    "bot_kook.toml": '[bot_kook]\nenable = true\n[bot_kook_secret]\nkook_token = "kook-token"\n',
}

DISCOVERY_CONFIG_FILES = {
    "config.toml": BASE_CONFIG,
    "bot_telegram.toml": "[bot_telegram]\nenable = true\n",
    "bot_telegram-alt.toml": "[bot_telegram-alt]\nenable = true\n",
    "bot_telegram-alt2.toml": "[bot_telegram-alt2]\nenable = false\n",
    "bot_telegram-bad-id.toml": "[bot_telegram-bad-id]\nenable = true\n",
    "bot_foo-alt.toml": "[bot_foo-alt]\nenable = true\n",
    "bot_kook.toml": "[bot_kook]\n",
}

CONFLICT_CONFIG_FILES = {
    "config.toml": BASE_CONFIG,
    "bot_telegram.toml": '[bot_telegram]\nenable = true\n[bot_telegram_secret]\ntelegram_token = "same-token"\n',
    "bot_telegram-alt.toml": (
        '[bot_telegram-alt]\nenable = true\n[bot_telegram-alt_secret]\ntelegram_token = "same-token"\n'
    ),
    "bot_web.toml": '[bot_web]\nenable = true\nweb_host = "127.0.0.1"\nweb_port = 6485\n',
    "bot_web-alt.toml": '[bot_web-alt]\nenable = true\nweb_host = "127.0.0.1"\nweb_port = 6485\n',
    "bot_onebot.toml": '[bot_onebot]\nenable = true\nqq_host = "127.0.0.1:8080"\n',
    "bot_onebot-alt.toml": '[bot_onebot-alt]\nenable = true\nqq_host = "0.0.0.0:8080"\n',
    "bot_milky.toml": '[bot_milky]\nenable = true\nqq_host = "http://milky.example.com:8080"\n',
}


@contextmanager
def _temp_config(files: dict[str, str]):
    """把 CFGManager 切到一份临时配置，退出时完整还原。

    :param files: 文件名到内容的映射，一律写在该目录下。
    """
    original_path = CFGManager.config_path
    original_values = CFGManager.values
    original_tss = CFGManager._tss
    original_file_list = CFGManager.config_file_list
    original_readonly = CFGManager.readonly
    original_instance_id = Info.instance_id

    tmp = Path(tempfile.mkdtemp(prefix="akari_multi_instance_"))
    try:
        for name, content in files.items():
            (tmp / name).write_text(content, encoding="utf-8")
        CFGManager.switch_config_path(tmp)
        CFGManager.readonly = False
        Info.instance_id = ""
        yield tmp
    finally:
        Info.instance_id = original_instance_id
        CFGManager.readonly = original_readonly
        CFGManager.config_path = original_path
        CFGManager.values = original_values
        CFGManager._tss = original_tss
        CFGManager.config_file_list = original_file_list
        shutil.rmtree(tmp, ignore_errors=True)


@contextmanager
def _adapters_only(*names: str):
    """把发现层的适配器清单收窄到给定几项，退出时还原。

    :param names: 保留的适配器包名。
    """
    real = PackageRegistry.adapters()
    with patch.object(PackageRegistry, "adapters", return_value={name: real[name] for name in names}):
        yield


@contextmanager
def _temporary_module(module_name: str, **fields):
    """注册一个临时模块，退出时移除。

    :param module_name: 模块名。
    :param fields: 传给 ``Module.assign`` 的字段。
    """
    module = Module.assign(module_name=module_name, alias=None, recommend_modules=None, developers=None, **fields)
    module._db_load = True
    ModulesManager.add_module(module, "test.py")
    ModulesManager.refresh()
    try:
        yield module
    finally:
        ModulesManager.modules.pop(module_name, None)
        ModulesManager.modules_origin.pop(module_name, None)
        ModulesManager.refresh()


def _test_default_instance_names_are_byte_identical():
    """默认实例（instance_id 为空）下八个适配器的 client_name 与改造前逐字节一致。"""
    saved = Info.instance_id
    try:
        Info.instance_id = ""
        for platform, expected in PLATFORM_NAMES.items():
            info = importlib.import_module(f"bots.{platform}.info")
            if info.platform_name != expected or info.client_name != expected:
                return False
            if Info.resolve_client_name(expected) != expected:
                return False
            if Info.resolve_client_name(expected, "") != expected:
                return False
            if not expected.startswith(info.target_prefix_list[0].split("|")[0]):
                return False
        # 显式传参派生实例名，且不得改动类属性
        if Info.resolve_client_name("Telegram", "alt") != "Telegram-alt":
            return False
        if Info.resolve_client_name("QQBot", "alt") != "QQBot-alt":
            return False
        if Info.instance_id != "":
            return False
        Info.instance_id = "alt"
        return Info.resolve_client_name("Telegram") == "Telegram-alt"
    finally:
        Info.instance_id = saved


def _test_platform_identity_derivation():
    """platform_from 是 target_from 换掉客户端段；缺信息时退化为旧的两段判据。"""
    from core.utils.platform_scope import resolve_platform_identity

    saved_platform_name = Info.platform_name
    try:
        Info.platform_name = "Telegram"
        if resolve_platform_identity("Telegram-alt|Group", "Telegram-alt") != ("Telegram", "Telegram|Group"):
            return False
        if resolve_platform_identity("Telegram|Group", "Telegram") != ("Telegram", "Telegram|Group"):
            return False
        # 前缀只差一个字符时不误替换客户端段
        if resolve_platform_identity("Telegram2|Group", "Telegram") != ("Telegram", "Telegram2|Group"):
            return False
        # 显式给出的两段优先于推导
        if resolve_platform_identity("Telegram-alt|Group", "Telegram-alt", "Telegram", "Telegram|Group") != (
            "Telegram",
            "Telegram|Group",
        ):
            return False
        # 平台进程取不到平台名（server、测试桩）时退回 client_name
        Info.platform_name = ""
        return resolve_platform_identity("Telegram-alt|Group", "Telegram-alt") == (
            "Telegram-alt",
            "Telegram-alt|Group",
        )
    finally:
        Info.platform_name = saved_platform_name


def _test_instance_config_scope():
    """实例表存在时接管读取，enable 不回退，写入与删除只落实例表。"""
    with _temp_config(SCOPE_CONFIG_FILES):
        base_url = CFGManager.get("telegram_api_url", table_name="bot_telegram")
        base_token = CFGManager.get("telegram_token", secret=True, table_name="bot_telegram")
        if base_url != "https://base.example" or base_token != "base-token":
            return False

        Info.instance_id = "alt"
        if CFGManager.get("telegram_api_url", table_name="bot_telegram") != "https://alt.example":
            return False
        if CFGManager.get("telegram_token", secret=True, table_name="bot_telegram") != "alt-token":
            return False
        if CFGManager.get("enable", table_name="bot_telegram") is not False:
            return False
        if not CFGManager.has("telegram_token", secret=True, table_name="bot_telegram"):
            return False

        # 实例表不存在时回退基表；enable 例外，不回退
        if CFGManager.get("kook_token", secret=True, table_name="bot_kook") != "kook-token":
            return False
        if CFGManager.get("enable", table_name="bot_kook", _fallback=False) is not None:
            return False
        if CFGManager.get("enable", table_name="bot_kook") is not True:
            return False

        # 模块配置与全局配置不参与实例作用域
        if CFGManager._resolve_table("module_dice") != "module_dice":
            return False
        if CFGManager._resolve_table("config") != "config":
            return False
        # 已指名实例表时不再二次拼接
        if CFGManager._resolve_table("bot_telegram-alt") != "bot_telegram-alt":
            return False

        # 写入与删除都只动实例表
        CFGManager.write("telegram_api_url", "https://written.example", str, False, "bot_telegram")
        Info.instance_id = ""
        if CFGManager.get("telegram_api_url", table_name="bot_telegram") != "https://base.example":
            return False
        Info.instance_id = "alt"
        if CFGManager.get("telegram_api_url", table_name="bot_telegram") != "https://written.example":
            return False
        if not CFGManager.delete("telegram_api_url", table_name="bot_telegram"):
            return False
        Info.instance_id = ""
        return CFGManager.get("telegram_api_url", table_name="bot_telegram") == "https://base.example"


def _test_discover_adapter_instances():
    """实例发现按配置表枚举：孤立配置与非法实例 ID 只告警并跳过，enable 缺失视为未启用。"""
    with _temp_config(DISCOVERY_CONFIG_FILES), _adapters_only("telegram", "kook"):
        daemon.disabled_bots.clear()
        with patch.object(daemon.Logger, "warning") as warning:
            instances = daemon.discover_adapter_instances()
        discovered = [(item.platform, item.instance_id, item.client_name, item.table) for item in instances]
        if discovered != [
            ("telegram", "", "Telegram", "bot_telegram"),
            ("telegram", "alt", "Telegram-alt", "bot_telegram-alt"),
        ]:
            return False
        if sorted(daemon.disabled_bots) != ["kook", "telegram-alt2"]:
            return False
        messages = " ".join(str(call.args[0]) for call in warning.call_args_list)
        return (
            "foo-alt" in messages
            and "no adapter is installed" in messages
            and "bot_telegram-bad-id" in messages
            and "invalid instance id" in messages
            and "kook" in messages
        )


def _fake_adapter_entry(name: str, credential_fields: tuple[str, ...] = ()) -> PackageEntry:
    """构造一个带清单的适配器条目。"""
    return PackageEntry(
        kind="adapter",
        name=name,
        dist_name="",
        version="0+local",
        import_path=f"bots.{name}",
        root=Path("bots") / name,
        manifest=PackageManifest(config_table=f"bot_{name}", credential_fields=credential_fields),
    )


def _run_conflict_check(instances) -> tuple[object, str]:
    """跑一次冲突检查，返回 ``(终止异常或 None, critical 消息)``。"""
    with patch.object(daemon.Logger, "critical") as critical:
        try:
            daemon.check_instance_conflicts(instances)
            terminal = None
        except SystemExit as exc:
            terminal = exc
    return terminal, (critical.call_args.args[0] if critical.call_args else "")


def _instance(platform: str, instance_id: str = "", platform_name: str | None = None) -> daemon.AdapterInstance:
    """按命名规则构造实例记录。

    :param platform: 适配器名。
    :param instance_id: 实例 ID。
    :param platform_name: 平台展示名；缺省时取适配器名（合成适配器可如此简化）。
    """
    table = f"bot_{platform}" + (f"-{instance_id}" if instance_id else "")
    return daemon.AdapterInstance(
        platform=platform,
        instance_id=instance_id,
        client_name=Info.resolve_client_name(platform_name or platform, instance_id),
        table=table,
    )


def _test_instance_conflict_checks():
    """端口冲突与同平台凭据重复中止启动并指名道姓；跨主机同端口不误报。"""
    with _temp_config(CONFLICT_CONFIG_FILES), _adapters_only("telegram", "web", "onebot", "milky"):
        terminal, message = _run_conflict_check([_instance("web", platform_name="Web"), _instance("web", "alt", "Web")])
        if not isinstance(terminal, SystemExit) or terminal.code != 1:
            return False
        if "Web" not in message or "Web-alt" not in message or "6485" not in message:
            return False

        # 通配地址与具体地址争用同一端口
        terminal, _ = _run_conflict_check([_instance("onebot", platform_name="QQ"), _instance("onebot", "alt", "QQ")])
        if not isinstance(terminal, SystemExit) or terminal.code != 1:
            return False

        # milky 的 qq_host 是远端服务地址：同端口不同主机不构成冲突
        terminal, _ = _run_conflict_check(
            [_instance("onebot", platform_name="QQ"), _instance("milky", platform_name="QQ")]
        )
        if terminal is not None:
            return False

        telegram_entry = _fake_adapter_entry("telegram", ("telegram_token",))
        with patch.object(PackageRegistry, "adapters", return_value={"telegram": telegram_entry}):
            terminal, message = _run_conflict_check(
                [_instance("telegram", platform_name="Telegram"), _instance("telegram", "alt", "Telegram")]
            )
        if not isinstance(terminal, SystemExit) or terminal.code != 1:
            return False
        return "Telegram" in message and "Telegram-alt" in message and "telegram_token" in message


def _declared_bot_tables(source: str) -> set[str]:
    """从适配器的 config.py 源码中取出 ``on_bot_config`` 声明的表名。"""
    tables = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        func_name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
        if func_name != "on_bot_config":
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            tables.add(f"bot_{first.value}")
    return tables


def _declared_field_names(source: str) -> set[str]:
    """从适配器的 config.py 源码中取出全部带类型标注的字段名。"""
    fields = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.ClassDef):
            continue
        for statement in node.body:
            if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                fields.add(statement.target.id)
    return fields


def _test_adapter_manifests_match_config_templates():
    """适配器清单的 config_table 必须等于 config.py 实际登记的表；包名不得含分隔符。"""
    adapters = PackageRegistry.adapters()
    if not adapters:
        return False
    for name, entry in adapters.items():
        # 适配器名含 `-` 会让 bot_<平台>-<实例> 的拆分产生歧义
        if "-" in name:
            return False
        config_source = (entry.root / "config.py").read_text(encoding="utf-8")
        if _declared_bot_tables(config_source) != {entry.manifest.config_table}:
            return False
        # 凭据字段必须真的存在于某个配置模板类上，否则重复凭据检查会静默失效
        if not set(entry.manifest.credential_fields) <= _declared_field_names(config_source):
            return False
    return True


def _test_four_way_scope_matches():
    """available_for 的平台级声明覆盖该平台的全部实例，实例级声明只覆盖该实例。"""
    from core.loader import ModulesManager as manager

    with (
        _temporary_module("__test_mi_platform", available_for=["Telegram"]),
        _temporary_module("__test_mi_instance", available_for=["Telegram-alt"]),
        _temporary_module("__test_mi_excluded", available_for=["*"], exclude_from=["Telegram"]),
    ):
        base = manager.return_modules_list("Telegram|Group", "Telegram", "Telegram|Group", "Telegram")
        alt_scoped = manager.return_modules_list("Telegram-alt|Group", "Telegram-alt", "Telegram|Group", "Telegram")
        alt_legacy = manager.return_modules_list("Telegram-alt|Group", "Telegram-alt")

        if "__test_mi_platform" not in base or "__test_mi_platform" not in alt_scoped:
            return False
        # 缺平台两段时退化为旧的两段判据：平台级声明落不到该实例上，实例级声明仍然命中
        if "__test_mi_platform" in alt_legacy or "__test_mi_instance" not in alt_legacy:
            return False
        if "__test_mi_instance" in base or "__test_mi_instance" not in alt_scoped:
            return False
        # exclude_from 的平台级声明同样覆盖实例
        if "__test_mi_excluded" in base or "__test_mi_excluded" in alt_scoped:
            return False

        command = CommandMeta(function=lambda msg: None, command_template=[], available_for=["Telegram"])
        event = EventMeta(function=lambda msg: None, name="test.multi_instance", available_for=["Telegram"])
        if not command.available_for or command.exclude_from:
            return False
        from core.types.module.component_matches import CommandMatches, EventMatches

        commands = CommandMatches.init()
        commands.add(command)
        events = EventMatches.init()
        events.add(event)
        return (
            bool(commands.get("Telegram-alt|Group", "Telegram-alt", "Telegram|Group", "Telegram"))
            and not commands.get("Telegram-alt|Group", "Telegram-alt")
            and bool(events.get("Telegram-alt|Group", "Telegram-alt", "Telegram|Group", "Telegram"))
            and not events.get("Telegram-alt|Group", "Telegram-alt")
        )


def _test_return_cache_does_not_collide():
    """同一 target_from / client_name 下，带与不带平台两段的结果不得互相顶替缓存。"""
    with _temporary_module("__test_mi_cache", available_for=["Telegram"]):
        scoped = ModulesManager.return_modules_list("Telegram-alt|Group", "Telegram-alt", "Telegram|Group", "Telegram")
        legacy = ModulesManager.return_modules_list("Telegram-alt|Group", "Telegram-alt")
        return "__test_mi_cache" in scoped and "__test_mi_cache" not in legacy


async def _test_session_info_platform_fields():
    """入站会话按进程的 Info.platform_name 填平台两段；旧会话在 refresh_info 后退化为两段判据。"""
    from core.builtins.session.info import SessionInfo

    saved_platform_name, saved_instance_id = Info.platform_name, Info.instance_id
    try:
        Info.platform_name = "Telegram"
        Info.instance_id = "alt"
        session = await SessionInfo.assign(
            target_id="Telegram-alt|Group|1",
            target_from="Telegram-alt|Group",
            client_name="Telegram-alt",
        )
        if (session.platform_name, session.platform_from) != ("Telegram", "Telegram|Group"):
            return False
        # 升级前入队的旧会话没有平台两段，且 server 进程没有平台身份
        session.platform_name = ""
        session.platform_from = ""
        Info.platform_name = ""
        await session.refresh_info()
        return (session.platform_name, session.platform_from) == ("Telegram-alt", "Telegram-alt|Group")
    finally:
        Info.platform_name = saved_platform_name
        Info.instance_id = saved_instance_id


def _test_alive_prefix_disambiguation():
    """Telegram-alt 的前缀不得被 Telegram 抢走，判定取最长匹配。"""
    lease = datetime.now(UTC) + timedelta(seconds=300)
    Alive.refresh_peer("mi-p1", "Telegram", metadata={"target_prefix_list": ["Telegram|Group"]}, lease_until=lease)
    Alive.refresh_peer(
        "mi-p2", "Telegram-alt", metadata={"target_prefix_list": ["Telegram-alt|Group"]}, lease_until=lease
    )
    try:
        return (
            Alive.determine_client("Telegram|Group|1") == "Telegram"
            and Alive.determine_client("Telegram-alt|Group|1") == "Telegram-alt"
            and Alive.determine_target_from("Telegram-alt|Group|1") == "Telegram-alt|Group"
            and Alive.determine_target_from("Telegram|Group|1") == "Telegram|Group"
        )
    finally:
        Alive.values.pop("mi-p1", None)
        Alive.values.pop("mi-p2", None)


@func_case
async def test_multi_instance(tester: Tester):
    """阶段 1B: 多实例身份模型"""
    await tester.test(_test_default_instance_names_are_byte_identical, "默认实例 client_name 逐字节不变")
    await tester.test(_test_platform_identity_derivation, "平台两段的推导与退化")
    await tester.test(_test_instance_config_scope, "配置的实例作用域与 enable 不回退")
    await tester.test(_test_discover_adapter_instances, "实例发现与孤立配置跳过")
    await tester.test(_test_instance_conflict_checks, "端口与凭据冲突中止启动")
    await tester.test(_test_adapter_manifests_match_config_templates, "适配器清单与配置模板一致")
    await tester.test(_test_four_way_scope_matches, "四元组平台判据")
    await tester.test(_test_return_cache_does_not_collide, "return_modules_list 缓存键不串")
    await tester.test(_test_session_info_platform_fields, "会话的平台两段填充与退化")
    await tester.test(_test_alive_prefix_disambiguation, "实例前缀不被平台前缀抢占")
    return tester
