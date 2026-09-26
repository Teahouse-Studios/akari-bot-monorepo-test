"""适配器与实例管理。

``akaribot adapter list`` 与 ``akaribot adapter instance add|remove`` 的实现。本模块不导入 core：
一切实例数据来自实例目录下的配置文件与 core 入口的子进程输出。

数据来源：

- 实例清单：``config/adapters/*.toml`` 中的 ``[bot_<平台>]`` / ``[bot_<平台>-<实例 ID>]`` 表及其配对的
  ``_secret`` 表。分层布局迁移尚未执行的实例（``config/bot_<平台>.toml``）一并识别，并在输出中标注。
- 已装适配器：``python -m akaribot.core.entrypoints.registry --json``。
- 配置模板：``python -m akaribot.core.entrypoints.config schema --table <表名> --json``。

不提供 ``instance rename``：实例 ID 是 ``target_id`` 前缀的一部分（如 ``Telegram-alt|Group|12345``），
改名要跨 ``target_union_info``、``target_union_bind``、``sender_union_info``、``analytics_data``、
``unfriendly_actions`` 这 5 张核心表与各模块表迁移 ``target_id`` / ``sender_id`` 前缀，收益与风险严重
不成比例。**实例 ID 一旦使用请勿更改**；确需更换时按「新建实例 + 迁移数据」处理。

实例定位见 :func:`load_instance`。命令只依赖最小的 ``Instance`` 协议（``root`` / ``meta`` / ``python``）；
:class:`LocalInstance` 是该协议在 ``akaribot.cli.instance`` 落地之前的顶替实现，本节的公共件同时供
:mod:`akaribot.cli.commands.doctor` 复用。
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any, NoReturn, Protocol

import tomlkit
import typer
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from akaribot.cli import i18n
from akaribot.cli.instance import INSTANCE_ID_PATTERN

INSTANCE_ENV = "AKARI_INSTANCE_DIR"
CONFIG_ENV = "AKARI_CONFIG_PATH"
INSTANCE_META_FILE = "akaribot.toml"
CONFIG_DIR_NAME = "config"
ADAPTERS_DIR_NAME = "adapters"
DEFAULT_VENV_DIR = ".venv"
CORE_ENTRYPOINT_ROOT = "akaribot.core.entrypoints"
CORE_TIMEOUT_SECONDS = 120.0

PLACEHOLDER_PATTERN = re.compile(r"^<Replace me.*>$")
BOT_TABLE_PREFIX = "bot_"
SECRET_TABLE_SUFFIX = "_secret"

EXIT_FAILURE = 1

# 适配器包在 registry --json 中的 kind 取值；缺 kind 时按 import_path 判定。
ADAPTER_KINDS = frozenset({"adapter", "adapters", "bot", "bot_adapter"})
MODULE_KINDS = frozenset({"module", "modules"})

# 实例数据清理涉及的核心表。表名取自 core/database/models.py 的 Meta.table，行以 client_name 前缀
# 出现在 union_id / target_id / sender_id 列上。模块表由各包 manifest 的 owned_tables 与 id_columns 声明。
PURGE_SCOPE_CORE_TABLES = (
    "target_union_info",
    "target_union_bind",
    "sender_union_info",
    "sender_union_bind",
    "analytics_data",
    "unfriendly_actions",
)

# 适配器未声明 listen_fields 时，按字段名识别监听项的候选集合（见 _guess_listen_fields）。
LISTEN_FIELD_EXACT = ("host", "port", "listen", "listen_host", "listen_port", "bind", "addr", "address")
WILDCARD_HOSTS = frozenset({"", "*", "0.0.0.0", "::", "[::]", "::0"})
LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "[::1]"})

RENAME_NOTE = i18n.t("cli.adapter.instance.rename_note")

NOT_AN_INSTANCE_HINT = i18n.t("cli.adapter.not_instance_hint")


class NotAnInstanceError(RuntimeError):
    """当前目录不在任何 AkariBot 实例内。"""


class CoreCallError(RuntimeError):
    """core 入口调用失败，或其输出无法解析。"""


def fail(message: str, *, hint: str | None = None, code: int = EXIT_FAILURE) -> NoReturn:
    """打印错误信息并以非零码退出。

    :param message: 错误描述。
    :param hint: 可选的可执行提示。
    :param code: 进程退出码。
    """
    typer.secho(i18n.t("cli.adapter.fail_prefix", message=message), fg=typer.colors.RED, err=True)
    if hint:
        typer.secho(hint, fg=typer.colors.YELLOW, err=True)
    raise typer.Exit(code)


def warn(message: str) -> None:
    """打印警告信息。

    :param message: 警告描述。
    """
    typer.secho(i18n.t("cli.adapter.warn_prefix", message=message), fg=typer.colors.YELLOW, err=True)


class InstanceLike(Protocol):
    """命令依赖的最小实例协议。

    ``akaribot.cli.instance.Instance`` 满足该协议；本模块只使用 ``root`` / ``meta`` / ``python`` 三项，
    不触碰其内部实现。``meta`` 既可以是映射（``akaribot.toml`` 的解析结果），也可以是带同名属性的对象。
    """

    root: Path
    meta: Any

    @property
    def python(self) -> Path:
        """实例解释器。"""


@dataclass
class LocalInstance:
    """最小 ``Instance`` 实现。

    仅在 ``akaribot.cli.instance`` 尚不可用时顶替，字段与协议一致。

    :param root: 实例根目录。
    :param meta: ``akaribot.toml`` 的解析结果。
    """

    root: Path
    meta: Mapping[str, Any] = field(default_factory=dict)

    @property
    def python(self) -> Path:
        """实例 venv 的解释器；``runtime.venv`` 为空或解释器缺失时回退到当前解释器。"""
        venv_setting = meta_get(meta_get(self.meta, "runtime"), "venv")
        venv_dir = DEFAULT_VENV_DIR if venv_setting is None else str(venv_setting).strip()
        if not venv_dir:
            return system_python()
        candidate = Path(venv_dir).expanduser()
        if not candidate.is_absolute():
            candidate = self.root / candidate
        return venv_python(candidate)


def meta_get(container: Any, key: str) -> Any:
    """从映射或对象中读取一项配置。

    :param container: 映射或带同名属性的对象。
    :param key: 键名或属性名。
    :return: 取到的值；容器为空或不存在该项时返回 ``None``。
    """
    if container is None:
        return None
    if isinstance(container, Mapping):
        return container.get(key)
    return getattr(container, key, None)


def venv_python(venv_dir: Path) -> Path:
    """由 venv 目录推出解释器路径。

    :param venv_dir: venv 目录。
    :return: 存在的解释器路径；不存在时回退到当前解释器。
    """
    candidates = (venv_dir / "bin" / "python", venv_dir / "Scripts" / "python.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return system_python()


def read_instance_meta(root: Path) -> dict[str, Any]:
    """读取实例的 ``akaribot.toml``。

    :param root: 实例根目录。
    :return: 解析结果；文件缺失或损坏时返回空映射。
    """
    path = root / INSTANCE_META_FILE
    if not path.is_file():
        return {}
    try:
        return dict(tomlkit.parse(path.read_text(encoding="utf-8")).unwrap())
    except (OSError, ValueError):
        return {}


def config_root(instance: InstanceLike) -> Path:
    """取实例的配置根目录，``AKARI_CONFIG_PATH`` 优先。

    :param instance: 目标实例。
    :return: 配置根目录。
    """
    override = os.environ.get(CONFIG_ENV, "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path(instance.root) / CONFIG_DIR_NAME


def instance_module() -> Any | None:
    """取 ``akaribot.cli.instance`` 模块。

    :return: 模块对象；该模块不可用时返回 ``None``。
    """
    try:
        return __import__("akaribot.cli.instance", fromlist=["Instance"])
    except ImportError:
        return None


def system_python() -> Path:
    """解析非托管模式要用的系统 Python。

    不得用 ``sys.executable``：Nuitka onefile 冻结后它指向 CLI 二进制自身。优先复用
    ``akaribot.cli.instance.system_python``，该模块不可用时退回本模块的等价实现。

    :return: 解释器绝对路径。
    """
    module = instance_module()
    resolver = getattr(module, "system_python", None) if module is not None else None
    if callable(resolver):
        return Path(resolver())
    import shutil as _shutil

    for name in ("python3", "python"):
        found = _shutil.which(name)
        if found:
            return Path(found)
    raise RuntimeError(i18n.t("cli.adapter.system_python_missing"))


def find_instance_root(start: Path | None = None) -> Path | None:
    """定位实例根目录。

    ``akaribot.cli.instance`` 提供 ``find_instance_root`` 时以它为准，避免两处发现规则分叉；否则用本
    函数的兜底实现：``AKARI_INSTANCE_DIR`` 指向含 ``akaribot.toml`` 的目录时直接采用，其余情况自
    ``start`` 逐级向上查找 ``akaribot.toml``。

    :param start: 起始目录，默认为当前工作目录。
    :return: 实例根目录；未找到时返回 ``None``。
    """
    module = instance_module()
    finder = getattr(module, "find_instance_root", None) if module is not None else None
    if callable(finder):
        try:
            found = finder(start) if start is not None else finder()
        except TypeError:
            found = None
        if found is not None:
            return Path(found).resolve()
    override = os.environ.get(INSTANCE_ENV, "").strip()
    if override:
        candidate = Path(override).expanduser()
        return candidate.resolve() if (candidate / INSTANCE_META_FILE).is_file() else None
    current = (start or Path.cwd()).expanduser()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / INSTANCE_META_FILE).is_file():
            return candidate.resolve()
    return None


def _colleague_instance(root: Path) -> InstanceLike | None:
    module = instance_module()
    if module is None:
        return None
    for factory_name in ("resolve_instance", "load_instance", "discover_instance"):
        factory = getattr(module, factory_name, None)
        if not callable(factory):
            continue
        try:
            candidate = factory(root)
        except TypeError:
            continue
        except Exception:
            # 同事实现的入口可能以自身异常类型报错；此处只做定位，失败时退回本地实例对象
            break
        if candidate is not None:
            return candidate
    instance_cls = getattr(module, "Instance", None)
    if instance_cls is None:
        return None
    try:
        return instance_cls(root)
    except TypeError:
        return None


def load_instance(start: Path | None = None) -> InstanceLike:
    """定位当前实例。

    :param start: 起始目录，默认为当前工作目录。
    :raises NotAnInstanceError: 未找到实例根目录。
    :return: 满足 :class:`InstanceLike` 的实例对象。
    """
    root = find_instance_root(start)
    if root is None:
        raise NotAnInstanceError(i18n.t("cli.adapter.not_instance", start=start or Path.cwd(), meta=INSTANCE_META_FILE))
    colleague = _colleague_instance(root)
    if colleague is not None:
        return colleague
    return LocalInstance(root=root, meta=read_instance_meta(root))


def open_instance() -> InstanceLike:
    """命令入口的实例定位，失败时给出可执行提示并退出。

    :return: 满足 :class:`InstanceLike` 的实例对象。
    """
    try:
        return load_instance()
    except NotAnInstanceError as error:
        fail(str(error), hint=NOT_AN_INSTANCE_HINT)


def instance_python(instance: InstanceLike) -> Path:
    """取实例解释器。

    :param instance: 目标实例。
    :return: 解释器路径；实例未给出可用解释器时回退到当前解释器。
    """
    try:
        candidate = Path(instance.python)
    except (AttributeError, TypeError, ValueError, OSError):
        candidate = system_python()
    return candidate if candidate.exists() else system_python()


@dataclass(frozen=True)
class CoreCall:
    """一次 core 入口子进程调用的结果。

    :param argv: 实际执行的命令行。
    :param returncode: 退出码。
    :param stdout: 标准输出。
    :param stderr: 标准错误。
    """

    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def command(self) -> str:
        """命令行的可读形式。"""
        return " ".join(self.argv)

    def failure_reason(self) -> str:
        """调用失败时的简短原因。"""
        detail = (self.stderr or self.stdout).strip().splitlines()
        summary = detail[-1] if detail else "无输出"
        return f"退出码 {self.returncode}：{summary}"

    def json(self) -> Any:
        """解析标准输出中的 JSON。

        :raises CoreCallError: 退出码非零或输出不是合法 JSON。
        :return: 解析结果。
        """
        if self.returncode != 0:
            raise CoreCallError(f"{self.command} 失败（{self.failure_reason()}）")
        try:
            return json.loads(self.stdout or "null")
        except ValueError as error:
            snippet = (self.stdout or "").strip().replace("\n", " ")[:200]
            raise CoreCallError(f"{self.command} 的输出不是 JSON：{snippet}（{error}）") from error


def spawn_core(instance: InstanceLike, *args: str, timeout: float = CORE_TIMEOUT_SECONDS) -> CoreCall:
    """以实例解释器执行 core 入口并捕获输出。

    ``args`` 的第一项是入口模块名，其余为它的命令行参数，例如
    ``spawn_core(instance, "config", "schema", "--table", "bot_telegram", "--json")`` 对应
    ``<解释器> -m akaribot.core.entrypoints.config schema --table bot_telegram --json``。

    启动逻辑以实例对象为准：``akaribot.cli.instance.Instance`` 提供 ``run_core_capture``，解释器、环境
    变量与编码都由它决定；只有该能力缺失时才自行启动子进程（``run_core`` 只回传退出码，取不到
    ``--json`` 输出，不足以支撑本命令的数据通道）。

    :param instance: 目标实例。
    :param args: 入口模块名与其命令行参数。
    :param timeout: 超时秒数，超时按调用失败处理。
    :raises CoreCallError: 解释器无法启动、调用超时或实例对象报错。
    :return: 调用结果。
    """
    entrypoint, *rest = args
    capture = getattr(instance, "run_core_capture", None)
    if callable(capture):
        try:
            completed = capture(entrypoint, *rest, timeout=timeout)
        except TypeError:
            completed = None
        except Exception as error:
            raise CoreCallError(f"core 入口 {entrypoint} 调用失败：{error}") from error
        if completed is not None:
            return CoreCall(
                tuple(str(item) for item in completed.args),
                completed.returncode,
                completed.stdout or "",
                completed.stderr or "",
            )
    argv = [str(instance_python(instance)), "-m", f"{CORE_ENTRYPOINT_ROOT}.{entrypoint}", *rest]
    env = dict(os.environ)
    env[INSTANCE_ENV] = str(instance.root)
    try:
        completed = subprocess.run(
            argv,
            cwd=str(instance.root),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise CoreCallError(f"core 入口 {entrypoint} 超时（{timeout:.0f} 秒）。") from error
    except OSError as error:
        raise CoreCallError(f"无法启动实例解释器 {argv[0]}：{error}") from error
    return CoreCall(tuple(argv), completed.returncode, completed.stdout or "", completed.stderr or "")


@dataclass(frozen=True)
class InstalledAdapter:
    """一个已安装的适配器包。

    :param name: entry point 名，即命令中的平台名，如 ``telegram``。
    :param dist: 分发名。
    :param version: 已安装版本。
    :param import_path: 导入路径。
    :param config_table: 基表表名，如 ``bot_telegram``；registry 未提供时为空。
    :param platform_name: 平台展示名，如 ``Telegram``；registry 未提供时为空。
    :param credential_fields: manifest 声明的凭据字段，供重复凭据检查使用。
    :param listen_fields: manifest 声明的监听字段，供端口冲突检查使用。
    """

    name: str
    dist: str = ""
    version: str = ""
    import_path: str = ""
    config_table: str = ""
    platform_name: str = ""
    credential_fields: tuple[str, ...] = ()
    listen_fields: tuple[str, ...] = ()

    @property
    def base_table(self) -> str:
        """基表表名；registry 未提供 ``config_table`` 时按 ``bot_<平台>`` 约定推导。"""
        return self.config_table or f"{BOT_TABLE_PREFIX}{self.name}"

    @property
    def inferred_platform_name(self) -> bool:
        """平台展示名是否为推断值。"""
        return not self.platform_name

    @property
    def display_name(self) -> str:
        """平台展示名；registry 未提供时按平台名首字母大写推断。"""
        return self.platform_name or self.name.capitalize()


@dataclass(frozen=True)
class AdapterRegistry:
    """已装适配器清单及其可用性。

    :param adapters: 平台名到已装适配器的映射。
    :param available: ``registry --json`` 是否可用。
    :param note: 不可用的原因或清单形状的补充说明。
    """

    adapters: Mapping[str, InstalledAdapter] = field(default_factory=dict)
    available: bool = False
    note: str = ""


def _unwrap_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        try:
            return dict(value.unwrap())
        except AttributeError:
            return {str(key): item for key, item in value.items()}
    return {}


def _iter_package_entries(payload: Any) -> list[tuple[Mapping[str, Any], str]]:
    # 兼容三种包装：条目列表、``{"packages"|"adapters"|...: [...]}``、``{名称： 条目}``。
    if isinstance(payload, Mapping):
        for key in ("packages", "adapters", "installed", "entries", "items", "registry"):
            value = payload.get(key)
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                hint = key[:-1] if key.endswith("s") else key
                return [(item, hint) for item in value if isinstance(item, Mapping)]
        loose = [(value, "") for value in payload.values() if isinstance(value, Mapping)]
        if loose and all("name" in entry or "dist" in entry or "dist_name" in entry for entry, _ in loose):
            return loose
        return []
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
        return [(item, "") for item in payload if isinstance(item, Mapping)]
    return []


def _string_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(str(item) for item in value)
    return ()


def _parse_installed_adapter(entry: Mapping[str, Any], hint: str = "") -> InstalledAdapter | None:
    # 条目可以是扁平结构，也可以把 manifest 字段嵌在 ``manifest`` 下，两种形状都接受。
    manifest = entry.get("manifest")
    manifest = manifest if isinstance(manifest, Mapping) else {}
    name = str(entry.get("name") or entry.get("stem") or "").strip()
    if not name:
        return None
    kind = str(entry.get("kind") or hint or "").strip().lower()
    import_path = str(entry.get("import_path") or "").strip()
    if kind in MODULE_KINDS:
        return None
    if kind not in ADAPTER_KINDS and ".adapters." not in import_path:
        return None
    return InstalledAdapter(
        name=name,
        dist=str(entry.get("dist") or entry.get("dist_name") or ""),
        version=str(entry.get("version") or ""),
        import_path=import_path,
        config_table=str(entry.get("config_table") or manifest.get("config_table") or ""),
        platform_name=str(entry.get("platform_name") or manifest.get("platform_name") or ""),
        credential_fields=_string_tuple(entry.get("credential_fields") or manifest.get("credential_fields")),
        listen_fields=_string_tuple(entry.get("listen_fields") or manifest.get("listen_fields")),
    )


def fetch_adapters(instance: InstanceLike) -> AdapterRegistry:
    """询问 core 本实例已安装的适配器。

    :param instance: 目标实例。
    :return: 已装适配器清单；入口不可用时 ``available`` 为 False 并带失败原因。
    """
    try:
        call = spawn_core(instance, "registry", "--json")
    except CoreCallError as error:
        return AdapterRegistry(note=str(error))
    if call.returncode != 0:
        return AdapterRegistry(note=f"{call.command} {call.failure_reason()}")
    try:
        payload = call.json()
    except CoreCallError as error:
        return AdapterRegistry(note=str(error))
    adapters: dict[str, InstalledAdapter] = {}
    undetermined = 0
    for entry, hint in _iter_package_entries(payload):
        adapter = _parse_installed_adapter(entry, hint)
        if adapter is None:
            kind = str(entry.get("kind") or hint or "").strip().lower()
            if kind not in MODULE_KINDS:
                undetermined += 1
            continue
        adapters[adapter.name] = adapter
    note = ""
    if undetermined:
        note = f"registry 返回的 {undetermined} 条条目无法判定为适配器，已忽略。"
    return AdapterRegistry(adapters=adapters, available=True, note=note)


@dataclass(frozen=True)
class AdapterInstanceConfig:
    """一个适配器实例的配置。

    :param path: 配置文件路径。
    :param table: 非密钥表名，如 ``bot_telegram-alt``。
    :param platform: 平台名（entry point 名），如 ``telegram``。
    :param instance_id: 实例 ID；默认实例为空串。
    :param values: 非密钥表的键值。
    :param secrets: 密钥表的键值。
    :param legacy_layout: 配置是否来自尚未迁移的扁平布局。
    """

    path: Path
    table: str
    platform: str
    instance_id: str
    values: Mapping[str, Any]
    secrets: Mapping[str, Any]
    legacy_layout: bool = False

    @property
    def secret_table(self) -> str:
        """密钥表表名。"""
        return f"{self.table}{SECRET_TABLE_SUFFIX}"

    @property
    def enable(self) -> bool | None:
        """实例的 ``enable``；键缺失时返回 ``None``（按 T1B.3 不回退，视为未启用）。"""
        value = self.values.get("enable")
        return None if value is None else bool(value)

    @property
    def enabled(self) -> bool:
        """实例是否已启用。"""
        return bool(self.values.get("enable"))

    @property
    def instance_id_valid(self) -> bool:
        """实例 ID 是否符合 ``[a-z0-9_]{1,24}``。"""
        return not self.instance_id or bool(INSTANCE_ID_PATTERN.fullmatch(self.instance_id))


@dataclass(frozen=True)
class AdapterScan:
    """一次适配器配置扫描的结果。

    :param instances: 识别到的实例配置。
    :param errors: 无法解析的文件及原因。
    :param legacy_layout: 是否使用了扁平布局兜底。
    """

    instances: tuple[AdapterInstanceConfig, ...] = ()
    errors: tuple[str, ...] = ()
    legacy_layout: bool = False


def parse_bot_table(table: str) -> tuple[str, str] | None:
    """由表名拆出平台名与实例 ID。

    平台名不含 ``-``（T1B.1 的 CI 约束），故首个 ``-`` 之后即实例 ID。

    :param table: 表名，如 ``bot_telegram`` / ``bot_telegram-alt``。
    :return: 二元组（平台名，实例 ID）；不是 ``bot_`` 表时返回 ``None``。
    """
    if not table.startswith(BOT_TABLE_PREFIX):
        return None
    rest = table[len(BOT_TABLE_PREFIX) :]
    platform, separator, instance_id = rest.partition("-")
    if not platform:
        return None
    return platform, instance_id if separator else ""


def _adapter_config_files(root: Path) -> list[tuple[Path, bool]]:
    found: list[tuple[Path, bool]] = []
    layered = root / ADAPTERS_DIR_NAME
    if layered.is_dir():
        found.extend((path, False) for path in sorted(layered.glob("*.toml")) if path.is_file())
    if root.is_dir():
        found.extend((path, True) for path in sorted(root.glob(f"{BOT_TABLE_PREFIX}*.toml")) if path.is_file())
    return found


def _read_adapter_config(path: Path, *, legacy_layout: bool) -> tuple[list[AdapterInstanceConfig], str | None]:
    try:
        document = tomlkit.parse(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [], f"{path} 无法解析：{error}"
    plain: dict[str, Mapping[str, Any]] = {}
    secrets: dict[str, Mapping[str, Any]] = {}
    for key, value in document.items():
        name = str(key)
        if not isinstance(value, Mapping) or not name.startswith(BOT_TABLE_PREFIX):
            continue
        if name.endswith(SECRET_TABLE_SUFFIX):
            secrets[name[: -len(SECRET_TABLE_SUFFIX)]] = _unwrap_mapping(value)
        else:
            plain[name] = _unwrap_mapping(value)
    instances: list[AdapterInstanceConfig] = []
    # 密钥表可能单独成表：先按非密钥表建实例，再补上仅有密钥表的条目
    for table in list(plain) + [table for table in secrets if table not in plain]:
        parsed = parse_bot_table(table)
        if parsed is None:
            continue
        platform, instance_id = parsed
        instances.append(
            AdapterInstanceConfig(
                path=path,
                table=table,
                platform=platform,
                instance_id=instance_id,
                values=plain.get(table, {}),
                secrets=secrets.get(table, {}),
                legacy_layout=legacy_layout,
            )
        )
    return instances, None


def scan_adapter_instances(instance: InstanceLike) -> AdapterScan:
    """扫描实例目录下的全部适配器实例配置。

    :param instance: 目标实例。
    :return: 扫描结果。
    """
    root = config_root(instance)
    instances: list[AdapterInstanceConfig] = []
    errors: list[str] = []
    legacy = False
    seen: set[str] = set()
    for path, is_legacy in _adapter_config_files(root):
        found, error = _read_adapter_config(path, legacy_layout=is_legacy)
        if error:
            errors.append(error)
        for item in found:
            if item.table in seen:
                continue
            seen.add(item.table)
            instances.append(item)
        if found and is_legacy:
            legacy = True
    instances.sort(key=lambda item: (item.platform, item.instance_id))
    return AdapterScan(instances=tuple(instances), errors=tuple(errors), legacy_layout=legacy)


def resolve_client_name(platform_display: str, instance_id: str) -> str:
    """按 T1B.1 的规则拼接 ``client_name``。

    :param platform_display: 平台展示名，如 ``Telegram``。
    :param instance_id: 实例 ID；默认实例为空串。
    :return: ``client_name``，如 ``Telegram-alt``。
    """
    return platform_display if not instance_id else f"{platform_display}-{instance_id}"


def client_name_for(config: AdapterInstanceConfig, registry: AdapterRegistry) -> tuple[str, bool]:
    """取实例的 ``client_name``。

    :param config: 实例配置。
    :param registry: 已装适配器清单。
    :return: 二元组——``client_name`` 与展示名是否为推断值。
    """
    adapter = registry.adapters.get(config.platform)
    if adapter is not None:
        return resolve_client_name(adapter.display_name, config.instance_id), adapter.inferred_platform_name
    return resolve_client_name(config.platform.capitalize(), config.instance_id), True


@dataclass(frozen=True)
class ListenEndpoint:
    """实例声明的一处监听地址。

    :param host: 主机部分。
    :param port: 端口；未给出时为 ``None``。
    :param raw: 配置中的原值。
    :param local: 是否为本机监听。带协议头的地址是外连目标（如 milky 的 ``qq_host``），不参与冲突比对。
    """

    host: str
    port: int | None
    raw: str
    local: bool = True

    def display(self) -> str:
        """可读的地址形式。"""
        if not self.local or self.port is None:
            return self.raw or self.host
        return f"{self.host or '*'}:{self.port}"


def _coerce_port(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    return int(text) if text.isdigit() else None


def _split_host_port(raw: str) -> tuple[str, int | None]:
    text = raw.strip()
    if not text:
        return "", None
    if text.startswith("["):
        host, _, tail = text.partition("]")
        port = _coerce_port(tail.lstrip(":"))
        return host.lstrip("["), port
    head, separator, tail = text.rpartition(":")
    if separator and tail.isdigit():
        return head, int(tail)
    return text, None


def _endpoint_from_value(value: Any) -> ListenEndpoint:
    raw = "" if value is None else str(value).strip()
    if "://" in raw:
        authority = raw.split("://", 1)[1].split("/", 1)[0]
        host, port = _split_host_port(authority)
        return ListenEndpoint(host=host, port=port, raw=raw, local=False)
    host, port = _split_host_port(raw)
    return ListenEndpoint(host=host, port=port, raw=raw, local=True)


def _guess_listen_fields(values: Mapping[str, Any]) -> tuple[str, ...]:
    # 现有 8 个适配器的 manifest 均未声明 ``listen_fields``（附录 A 已预留该字段），故端口检查依赖
    # 本推断：``web_host`` / ``web_port`` / ``qq_host`` 这类名字命中，其余平台不受影响。
    names: list[str] = []
    for key in values:
        lowered = str(key).lower()
        if lowered in LISTEN_FIELD_EXACT or lowered.endswith(("_host", "_port")):
            names.append(str(key))
    return tuple(names)


def listen_endpoints(values: Mapping[str, Any], declared: Iterable[str] = ()) -> list[ListenEndpoint]:
    """解析实例声明的监听地址。

    ``<前缀>_host`` 与 ``<前缀>_port`` 成对合并为 ``host:port``；只有 ``_host`` 时按 ``host:port``
    字面量解析（onebot 的 ``qq_host`` 即此形式）。

    :param values: 非密钥表的键值。
    :param declared: 适配器 manifest 声明的监听字段；为空时按字段名推断。
    :return: 端点列表。
    """
    declared_names = [str(name) for name in declared]
    fields = declared_names or list(_guess_listen_fields(values))
    pairs: dict[str, dict[str, Any]] = defaultdict(dict)
    singles: list[Any] = []
    for name in fields:
        if name not in values:
            continue
        if name.endswith("_port"):
            pairs[name[: -len("_port")]]["port"] = values[name]
        elif name.endswith("_host"):
            pairs[name[: -len("_host")]]["host"] = values[name]
        else:
            singles.append(values[name])
    endpoints: list[ListenEndpoint] = []
    for prefix in sorted(pairs):
        pair = pairs[prefix]
        host = pair.get("host")
        port = pair.get("port")
        if port is None:
            endpoints.append(_endpoint_from_value(host))
            continue
        endpoints.append(
            ListenEndpoint(
                host=str(host).strip() if host is not None else "*",
                port=_coerce_port(port),
                raw=f"{host}:{port}",
                local=True,
            )
        )
    endpoints.extend(_endpoint_from_value(value) for value in singles)
    return endpoints


def hosts_overlap(first: str, second: str) -> bool:
    """判断两个监听主机是否可能抢占同一端口。

    :param first: 主机一。
    :param second: 主机二。
    :return: 通配地址、回环地址或同名地址视为重叠。
    """
    left = first.strip().lower()
    right = second.strip().lower()
    if left in WILDCARD_HOSTS or right in WILDCARD_HOSTS:
        return True
    if left in LOOPBACK_HOSTS and right in LOOPBACK_HOSTS:
        return True
    return left == right


def is_placeholder(value: Any) -> bool:
    """判断取值是否为 ``<Replace me ...>`` 占位符。

    :param value: 配置值。
    :return: 是占位符时为 ``True``。
    """
    return isinstance(value, str) and bool(PLACEHOLDER_PATTERN.match(value.strip()))


@dataclass(frozen=True)
class SchemaField:
    """``config schema --json`` 返回的一个配置项。

    :param key: 键名。
    :param type_name: 类型名，如 ``str`` / ``(str, int)`` / ``list``。
    :param default: 模板默认值；无默认值时为 ``None``。
    :param secret: 是否属于密钥表。
    :param comment: i18n 注释。
    :param placeholder: 该键在模板中是否为待填写占位符。
    :param placeholder_text: 模板中的占位符原文（如 ``<Replace me with str value>``）。
    """

    key: str
    type_name: str = ""
    default: Any = None
    secret: bool = False
    comment: str = ""
    placeholder: bool = False
    placeholder_text: str = ""

    def initial_value(self) -> Any:
        """生成文件时该键应写入的值。

        ``enable`` 一律显式写 ``false``：实例文件的 ``enable`` 不回退到基表，新实例必须由用户确认后
        自行开启，否则「新建实例文件」等同于「立即上线一个机器人」。

        :return: 写入值。
        """
        if self.key == "enable":
            return False
        if self.placeholder or self.default is None:
            return self.placeholder_text or "<Replace me>"
        return self.default

    def needs_filling(self) -> bool:
        """该键是否需要用户填写。"""
        return self.key != "enable" and (self.placeholder or self.default is None)


def _normalize_type_name(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Sequence):
        return "(" + ", ".join(str(item) for item in value) + ")"
    if isinstance(value, type):
        return value.__name__
    return ""


def _parse_schema_field(entry: Mapping[str, Any]) -> SchemaField | None:
    key = str(entry.get("key") or entry.get("name") or "").strip()
    if not key:
        return None
    value = entry.get("value")
    raw_type = entry.get("type", entry.get("cfg_type"))
    default = entry.get("default")
    type_name = _normalize_type_name(raw_type) or _normalize_type_name(type(default))
    if isinstance(value, str) and PLACEHOLDER_PATTERN.match(value.strip()):
        placeholder, placeholder_text = True, value.strip()
    else:
        placeholder, placeholder_text = bool(entry.get("is_placeholder")), ""
    return SchemaField(
        key=key,
        type_name=type_name,
        default=default,
        secret=bool(entry.get("secret")),
        comment=str(entry.get("comment") or "").strip(),
        placeholder=placeholder,
        placeholder_text=placeholder_text,
    )


def fetch_schema(instance: InstanceLike, table: str) -> list[SchemaField]:
    """取某个基表的配置模板。

    :param instance: 目标实例。
    :param table: 基表表名，如 ``bot_telegram``。
    :raises CoreCallError: 入口不可用或输出无法解析。
    :return: 配置项列表，顺序即模板声明顺序。
    """
    call = spawn_core(instance, "config", "schema", "--table", table, "--json")
    payload = call.json()
    if isinstance(payload, Mapping):
        raw_entries: Any = None
        for key in ("fields", "schema", "keys", "items"):
            candidate = payload.get(key)
            if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes)):
                raw_entries = candidate
                break
        if raw_entries is None:
            raw_entries = [{"key": key, **value} for key, value in payload.items() if isinstance(value, Mapping)]
    else:
        raw_entries = payload
    if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
        raise CoreCallError(f"{call.command} 的输出结构无法识别：{str(payload)[:200]}")
    fields = [field for entry in raw_entries if isinstance(entry, Mapping) and (field := _parse_schema_field(entry))]
    return fields


def _placeholder_for(type_name: str) -> str:
    return f"<Replace me with {type_name} value>" if type_name else "<Replace me>"


def render_instance_config(
    fields: Sequence[SchemaField], table: str, secret_table: str, header_lines: Sequence[str] = ()
) -> str:
    """按配置模板生成实例配置文件的内容。

    :param fields: 配置项清单，顺序即文件中的书写顺序。
    :param table: 非密钥表名，如 ``bot_telegram-alt``。
    :param secret_table: 密钥表名，如 ``bot_telegram-alt_secret``。
    :param header_lines: 复用自基表配置文件的文件头注释行。
    :return: TOML 文本。
    """
    plain_fields = [item for item in fields if not item.secret and item.key != "enable"]
    secret_fields = [item for item in fields if item.secret]
    document = tomlkit.document()
    plain = tomlkit.table()
    # enable 写在非密钥表首位：core 的模板声明顺序本就如此，模板缺失该项时补一个显式的 false
    plain["enable"] = False
    enable_comment = next((item.comment for item in fields if item.key == "enable"), "")
    if enable_comment:
        plain.item("enable").comment(enable_comment)
    for item in plain_fields:
        plain[item.key] = item.initial_value()
        if item.comment:
            plain.item(item.key).comment(item.comment)
    document[table] = plain
    if secret_fields:
        secret = tomlkit.table()
        for item in secret_fields:
            secret[item.key] = item.initial_value()
            if item.comment:
                secret.item(item.key).comment(item.comment)
        document[secret_table] = secret
    header = "".join(f"{line.rstrip()}\n" for line in header_lines)
    return f"{header}{tomlkit.dumps(document)}"


def _read_header_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            break
        lines.append(line)
    return lines


def base_config_path(instance: InstanceLike, base_table: str) -> Path:
    """基表配置文件的路径。

    与其它配置表一致的一名一文件扁平布局：core 的 ``CFGManager.load()`` 只扫描
    ``config/*.toml``，写到 ``config/adapters/`` 的表对 core 不可见，`config set` 会另写一份
    扁平文件。分层布局待 P4.4 的 ``ConfigLayout`` 落地后再迁移（读取侧已同时兼容两种布局）。

    :param instance: 目标实例。
    :param base_table: 基表表名，如 ``bot_telegram``。
    :return: 配置文件路径。
    """
    return config_root(instance) / f"{base_table}.toml"


def base_table_stem(base_table: str) -> str:
    """基表表名到文件名主干：``bot_telegram`` 对应 ``telegram.toml``。

    :param base_table: 基表表名。
    :return: 文件名主干。
    """
    return base_table[len(BOT_TABLE_PREFIX) :] if base_table.startswith(BOT_TABLE_PREFIX) else base_table


def base_header_lines(instance: InstanceLike, base_table: str) -> list[str]:
    """取基表配置文件的文件头注释，供新实例文件复用。

    分层布局优先；布局迁移尚未执行时回退到扁平的 ``config/bot_<平台>.toml``。

    :param instance: 目标实例。
    :param base_table: 基表表名。
    :return: 注释行；两处都不存在时为空列表。
    """
    root = config_root(instance)
    stem = base_table_stem(base_table)
    lines = _read_header_lines(root / ADAPTERS_DIR_NAME / f"{stem}.toml")
    if lines:
        return lines
    return _read_header_lines(root / f"{BOT_TABLE_PREFIX}{stem}.toml")


def _client_name_summary(config: AdapterInstanceConfig, registry: AdapterRegistry) -> str:
    client_name, _ = client_name_for(config, registry)
    return i18n.t(
        "cli.adapter.instance.summary",
        platform=config.platform,
        instance=config.instance_id or i18n.t("cli.adapter.instance.default_id"),
        client_name=client_name,
        enabled=str(config.enabled).lower(),
    )


app = typer.Typer(help=i18n.t("cli.adapter.help"), no_args_is_help=True)
instance_app = typer.Typer(
    help=i18n.t("cli.adapter.instance.help", rename_note=RENAME_NOTE),
    no_args_is_help=True,
)


def _print_registry_note(registry: AdapterRegistry) -> None:
    if not registry.available:
        warn(i18n.t("cli.adapter.registry_unavailable", note=registry.note))
        warn(i18n.t("cli.adapter.registry_inferred"))
    elif registry.note:
        # registry.note 同时进入 --json 的 registry_note 字段，属机器可读契约，保持原文。
        warn(registry.note)


def _instance_rows(scan: AdapterScan, registry: AdapterRegistry) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config in scan.instances:
        adapter = registry.adapters.get(config.platform)
        client_name, inferred = client_name_for(config, registry)
        endpoints = listen_endpoints(config.values, adapter.listen_fields if adapter else ())
        issues: list[str] = []
        if registry.available and adapter is None:
            issues.append("孤立配置：该平台的适配器包未安装")
        if not config.instance_id_valid:
            issues.append("实例 ID 不符合 [a-z0-9_]{1,24}")
        if config.enable is None:
            issues.append("缺 enable 键（视为未启用）")
        rows.append(
            {
                "platform": config.platform,
                "instance_id": config.instance_id,
                "client_name": client_name,
                "client_name_inferred": inferred,
                "table": config.table,
                "config_file": str(config.path),
                "enable": config.enable,
                "enabled": config.enabled,
                "listen": [endpoint.display() for endpoint in endpoints],
                "installed": adapter is not None,
                "legacy_layout": config.legacy_layout,
                "issues": issues,
            }
        )
    return rows


def _issue_labels(row: Mapping[str, Any], registry: AdapterRegistry) -> list[str]:
    labels: list[str] = []
    if registry.available and not row["installed"]:
        labels.append(i18n.t("cli.adapter.list.issue_orphan"))
    instance_id = str(row["instance_id"] or "")
    if instance_id and not INSTANCE_ID_PATTERN.fullmatch(instance_id):
        labels.append(i18n.t("cli.adapter.list.issue_instance_id"))
    if row["enable"] is None:
        labels.append(i18n.t("cli.adapter.list.issue_enable_missing"))
    return labels


@app.command("list", help=i18n.t("cli.adapter.list.help"))
def list_instances(
    json_output: bool = typer.Option(False, "--json", help=i18n.t("cli.adapter.list.option_json")),
) -> None:
    """按平台分组列出全部适配器实例。

    实例 ID、``client_name``、``enable``、监听地址来自 ``config/adapters/*.toml``；平台是否已安装来自
    ``registry --json``。
    """
    instance = open_instance()
    scan = scan_adapter_instances(instance)
    registry = fetch_adapters(instance)
    rows = _instance_rows(scan, registry)
    if json_output:
        payload = {
            "instance_root": str(instance.root),
            "config_root": str(config_root(instance)),
            "registry_available": registry.available,
            "registry_note": registry.note,
            "platform_name_missing": any(row["installed"] and row["client_name_inferred"] for row in rows),
            "legacy_layout": scan.legacy_layout,
            "instances": rows,
            "errors": list(scan.errors),
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    console = Console()
    # 路径、平台名与注释里可能出现方括号（IPv6 地址、TOML 表名），故先 escape 再进入 rich 标记解析
    console.print(i18n.t("cli.adapter.list.instance_root", path=escape(str(instance.root))))
    for error in scan.errors:
        console.print(f"[red]{escape(error)}[/red]")
    if not scan.instances:
        console.print(i18n.t("cli.adapter.list.empty"))
        console.print(i18n.t("cli.adapter.list.empty_hint"))
        _print_registry_note(registry)
        return

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["platform"]].append(row)
    # 只有「平台已安装但清单未给出展示名」才值得提示；孤立配置的展示名本就无从取得
    inferred_any = any(row["installed"] and row["client_name_inferred"] for row in rows)
    for platform in sorted(grouped):
        adapter = registry.adapters.get(platform)
        if adapter is not None:
            suffix = i18n.t("cli.adapter.list.platform_suffix", name=adapter.display_name)
        else:
            # 清单不可用时无从判断平台是否已安装，不能标成「未安装」
            suffix = (
                i18n.t("cli.adapter.list.not_installed")
                if registry.available
                else i18n.t("cli.adapter.list.registry_unavailable")
            )
        title = escape(f"{platform}{suffix}")
        table = Table(title=title, title_justify="left", box=None, pad_edge=False)
        for column in (
            i18n.t("cli.adapter.list.column_instance_id"),
            "client_name",
            "enable",
            i18n.t("cli.adapter.list.column_listen"),
            i18n.t("cli.adapter.list.column_notes"),
        ):
            table.add_column(column, overflow="fold")
        for row in grouped[platform]:
            if row["enable"] is None:
                enable_text = i18n.t("cli.adapter.list.enable_missing")
            elif row["enabled"]:
                enable_text = "[green]true[/green]"
            else:
                enable_text = "false"
            table.add_row(
                escape(row["instance_id"] or i18n.t("cli.adapter.instance.default_id")),
                escape(row["client_name"]),
                enable_text,
                escape(i18n.t("cli.common.list_separator").join(row["listen"]) or "—"),
                escape(i18n.t("cli.common.clause_separator").join(_issue_labels(row, registry))),
            )
        console.print(table)
    if scan.legacy_layout:
        console.print(i18n.t("cli.adapter.list.legacy_note"))
    if inferred_any:
        console.print(i18n.t("cli.adapter.list.inferred_note"))
    _print_registry_note(registry)


@instance_app.command("add", help=i18n.t("cli.adapter.instance.add.help"))
def instance_add(
    platform: str = typer.Argument(..., help=i18n.t("cli.adapter.instance.arg_platform")),
    instance_id: str | None = typer.Argument(None, help=i18n.t("cli.adapter.instance.add.arg_instance_id")),
) -> None:
    """新建适配器实例配置。

    实例 ID 一旦使用请勿更改：它是 ``target_id`` 前缀的一部分，改名要跨核心表与模块表迁移数据。
    生成的配置文件里 ``enable`` 显式写 ``false``，填完凭据后自行开启。
    """
    instance = open_instance()
    platform = platform.strip().lower()
    instance_id = (instance_id or "").strip()
    if instance_id and not INSTANCE_ID_PATTERN.fullmatch(instance_id):
        fail(
            i18n.t("cli.adapter.instance.add.invalid_id", instance_id=repr(instance_id)),
            hint=i18n.t("cli.adapter.instance.add.invalid_id_hint"),
        )

    registry = fetch_adapters(instance)
    if not registry.available:
        fail(i18n.t("cli.adapter.instance.registry_unavailable", note=registry.note))
    adapter = registry.adapters.get(platform)
    if adapter is None:
        installed = i18n.t("cli.common.list_separator").join(sorted(registry.adapters))
        installed = installed or i18n.t("cli.adapter.instance.none")
        fail(
            i18n.t("cli.adapter.instance.add.not_installed", platform=platform),
            hint=i18n.t("cli.adapter.instance.add.not_installed_hint", installed=installed),
        )

    base_table = adapter.base_table
    if not base_table.startswith(BOT_TABLE_PREFIX):
        fail(i18n.t("cli.adapter.instance.add.bad_table", platform=platform, table=base_table))
    table = base_table if not instance_id else f"{base_table}-{instance_id}"
    target = base_config_path(instance, table)
    client_name = resolve_client_name(adapter.display_name, instance_id)

    scan = scan_adapter_instances(instance)
    for existing in scan.instances:
        if existing.platform == platform and existing.instance_id == instance_id:
            fail(
                i18n.t("cli.adapter.instance.add.exists", table=existing.table, path=existing.path),
                hint=i18n.t("cli.adapter.instance.add.exists_hint"),
            )
    if target.exists():
        fail(
            i18n.t("cli.adapter.instance.add.target_exists", target=target),
            hint=i18n.t("cli.adapter.instance.add.target_exists_hint"),
        )

    try:
        fields = fetch_schema(instance, base_table)
    except CoreCallError as error:
        fail(i18n.t("cli.adapter.instance.add.template_unavailable", table=base_table, error=error))
    if not fields:
        fail(
            i18n.t("cli.adapter.instance.add.template_empty", platform=platform),
            hint=i18n.t("cli.adapter.instance.add.template_empty_hint"),
        )

    content = render_instance_config(
        fields, table, f"{table}{SECRET_TABLE_SUFFIX}", base_header_lines(instance, base_table)
    )
    try:
        tomlkit.parse(content)
    except ValueError as error:
        fail(i18n.t("cli.adapter.instance.add.invalid_toml", error=error))
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.write_text(content, encoding="utf-8")
    except OSError as error:
        fail(i18n.t("cli.adapter.instance.add.write_failed", target=target, error=error))

    console = Console()
    secret_table = f"{table}{SECRET_TABLE_SUFFIX}"
    console.print(i18n.t("cli.adapter.instance.add.created", target=escape(str(target))))
    console.print(escape(i18n.t("cli.adapter.instance.add.table_line", table=table, secret_table=secret_table)))
    console.print(escape(i18n.t("cli.adapter.instance.add.client_name_line", client_name=client_name)))
    console.print(i18n.t("cli.adapter.instance.add.enable_line"))
    if adapter.inferred_platform_name:
        console.print(i18n.t("cli.adapter.instance.add.inferred_note"))

    pending = [item for item in fields if item.needs_filling()]
    if pending:
        checklist = Table(
            title=i18n.t("cli.adapter.instance.add.checklist_title"), title_justify="left", box=None, pad_edge=False
        )
        for column in (
            i18n.t("cli.adapter.instance.add.column_table"),
            i18n.t("cli.adapter.instance.add.column_key"),
            i18n.t("cli.adapter.instance.add.column_type"),
            i18n.t("cli.adapter.instance.add.column_comment"),
        ):
            checklist.add_column(column, overflow="fold")
        for item in pending:
            section = secret_table if item.secret else table
            checklist.add_row(
                escape(section), escape(item.key), escape(item.type_name or "?"), escape(item.comment or "—")
            )
        console.print(checklist)
        console.print(i18n.t("cli.adapter.instance.add.next_steps"))
        for item in pending:
            console.print(escape(i18n.t("cli.adapter.instance.add.set_hint", field=item.key, table=table)))
        console.print(escape(i18n.t("cli.adapter.instance.add.enable_hint", table=table)))
    else:
        console.print(i18n.t("cli.adapter.instance.add.no_pending"))
        console.print(escape(f"  akaribot config set enable true --table {table}"))
    console.print(i18n.t("cli.adapter.instance.add.doctor_note"))


def remove_instance_config(config: AdapterInstanceConfig) -> bool:
    """移除一个实例的配置。

    文件中若还有其它表，只摘除该实例的表；否则删除整个文件。

    :param config: 目标实例配置。
    :raises OSError: 文件读写失败。
    :raises ValueError: 文件内容不是合法 TOML。
    :return: 是否删除了整个文件。
    """
    document = tomlkit.parse(config.path.read_text(encoding="utf-8"))
    keys = (config.table, config.secret_table)
    remaining = [str(key) for key in document.keys() if str(key) not in keys]
    if not remaining:
        config.path.unlink()
        return True
    for key in keys:
        if key in document:
            del document[key]
    config.path.write_text(tomlkit.dumps(document), encoding="utf-8")
    return False


def _purge_scope_lines(client_name: str) -> list[str]:
    tables = i18n.t("cli.common.list_separator").join(PURGE_SCOPE_CORE_TABLES)
    return [
        i18n.t("cli.adapter.instance.purge.scope_intro", client_name=client_name),
        i18n.t("cli.adapter.instance.purge.core_tables", tables=tables),
        i18n.t("cli.adapter.instance.purge.core_tables_hint"),
        i18n.t("cli.adapter.instance.purge.module_tables"),
        i18n.t("cli.adapter.instance.purge.row_count"),
    ]


@instance_app.command("remove", help=i18n.t("cli.adapter.instance.remove.help"))
def instance_remove(
    platform: str = typer.Argument(..., help=i18n.t("cli.adapter.instance.arg_platform")),
    instance_id: str | None = typer.Argument(None, help=i18n.t("cli.adapter.instance.remove.arg_instance_id")),
    purge_data: bool = typer.Option(
        False, "--purge-data", help=i18n.t("cli.adapter.instance.remove.option_purge_data")
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help=i18n.t("cli.common.yes_option")),
    dry_run: bool = typer.Option(False, "--dry-run", help=i18n.t("cli.adapter.instance.remove.option_dry_run")),
) -> None:
    """移除适配器实例配置。

    默认只删除配置文件，数据保留；``--purge-data`` 追加清理该 ``client_name`` 前缀下的场景与用户数据，
    执行前要求二次确认并列出影响范围。实例 ID 一旦使用请勿更改，本命令不提供改名。
    """
    instance = open_instance()
    platform = platform.strip().lower()
    instance_id = (instance_id or "").strip()
    scan = scan_adapter_instances(instance)
    registry = fetch_adapters(instance)
    match = next(
        (item for item in scan.instances if item.platform == platform and item.instance_id == instance_id), None
    )
    if match is None:
        available = i18n.t("cli.common.list_separator").join(
            _client_name_summary(item, registry) for item in scan.instances
        )
        available = available or i18n.t("cli.adapter.instance.none")
        target_name = instance_id or i18n.t("cli.adapter.instance.default_id")
        fail(
            i18n.t("cli.adapter.instance.remove.not_found", platform=platform, instance=target_name),
            hint=i18n.t("cli.adapter.instance.remove.not_found_hint", available=available),
        )

    client_name, _ = client_name_for(match, registry)
    console = Console()
    console.print(escape(i18n.t("cli.adapter.instance.remove.target", summary=_client_name_summary(match, registry))))
    console.print(escape(i18n.t("cli.adapter.instance.remove.config_file", path=match.path)))
    if match.enabled:
        warn(i18n.t("cli.adapter.instance.remove.enabled_warning"))

    if purge_data:
        for line in _purge_scope_lines(client_name):
            console.print(escape(line))
    if dry_run:
        console.print(i18n.t("cli.adapter.instance.remove.dry_run"))
        return
    if purge_data and not yes:
        typer.confirm(i18n.t("cli.adapter.instance.remove.confirm"), abort=True)

    try:
        removed_file = remove_instance_config(match)
    except (OSError, ValueError) as error:
        fail(i18n.t("cli.adapter.instance.remove.failed", path=match.path, error=error))
    if removed_file:
        console.print(escape(i18n.t("cli.adapter.instance.remove.file_removed", path=match.path)))
    else:
        console.print(escape(i18n.t("cli.adapter.instance.remove.table_removed", path=match.path, table=match.table)))

    if purge_data:
        console.print(i18n.t("cli.adapter.instance.remove.data_kept"))
        console.print(escape(i18n.t("cli.adapter.instance.remove.purge_later", client_name=client_name)))
    else:
        console.print(escape(i18n.t("cli.adapter.instance.remove.keep_hint", client_name=client_name)))
    console.print(i18n.t("cli.adapter.instance.remove.recheck"))


app.add_typer(instance_app, name="instance")
