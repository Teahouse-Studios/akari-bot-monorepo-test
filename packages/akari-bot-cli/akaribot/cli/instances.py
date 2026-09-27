"""本机实例注册表：记住这台机器上有哪些 AkariBot 环境。

CLI 与界面都能管理多个实例，故「有哪些实例」必须落在一处：默认在 ``~/.akaribot/instances.toml``
（``AKARIBOT_HOME`` 可改），每条记录含实例根、语言、加入时间，以及服务相关的策略——是否随服务启动、
崩溃后是否重启、最后已知的期望状态（用于「恢复到上次停电前的状态」）。

注册表只记位置与策略，不碰实例本身：删掉一条记录不会动实例目录。
"""

from __future__ import annotations

import os
import re
import tomlkit
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path

from akaribot.cli import i18n
from akaribot.cli.instance import INSTANCE_META_FILENAME, InstanceMeta

HOME_ENV = "AKARIBOT_HOME"
REGISTRY_FILENAME = "instances.toml"
DEFAULT_HOME_DIR = ".akaribot"

STATE_RUNNING = "running"
STATE_STOPPED = "stopped"
STATES = (STATE_RUNNING, STATE_STOPPED)

# 名称只用于展示与命令行引用，故限制在小写字母、数字、连字符与下划线。
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,31}$")


class RegistryError(RuntimeError):
    """注册表不可用：文件损坏、名称重复或实例不存在。"""


def registry_home() -> Path:
    """返回注册表所在目录。

    :return: ``AKARIBOT_HOME`` 指定的目录，未设置时为 ``~/.akaribot``。
    """
    override = os.environ.get(HOME_ENV)
    if override:
        return Path(override).expanduser()
    return Path.home() / DEFAULT_HOME_DIR


def registry_path() -> Path:
    """返回注册表文件路径。"""
    return registry_home() / REGISTRY_FILENAME


def suggested_name(root: Path) -> str:
    """按目录名推一个合法实例名。

    :param root: 实例根目录。
    :return: 小写、只含字母数字与连字符的名称；推不出时返回 ``instance``。
    """
    text = re.sub(r"[^a-z0-9]+", "-", root.name.strip().lower()).strip("-")
    return text[:32] or "instance"


def child_instances(root: Path, *, limit: int | None = 4) -> tuple[Path, ...]:
    """列出目录下第一层的实例目录。

    登记时常被指向「装着实例的项目目录」而不是实例本身，报错时列出这些候选比只说缺文件有用。

    :param root: 要检查的目录。
    :param limit: 最多列出几个候选；``None`` 表示不限。
    :return: 含 ``akaribot.toml`` 的直接子目录；``root`` 本身就是实例时为空。
    """
    if (root / INSTANCE_META_FILENAME).is_file():
        return ()
    try:
        found = sorted(path for path in root.iterdir() if (path / INSTANCE_META_FILENAME).is_file())
    except OSError:
        return ()
    return tuple(found if limit is None else found[:limit])


def register_existing(root: Path) -> InstanceEntry | None:
    """登记目录对应的实例；已登记或目录不是实例时返回 ``None``。

    站在实例目录里启动界面时自动走这一步，省掉「先手动登记才能管理」的前置动作。

    :param root: 实例根目录。
    :return: 新登记的记录；无需登记时为 ``None``。
    :raises RegistryError: 名称冲突或注册表写入失败。
    """
    resolved = _resolve(root)
    registry = InstanceRegistry()
    if registry.find_by_root(resolved) is not None:
        return None
    if not (resolved / INSTANCE_META_FILENAME).is_file():
        return None
    locale = ""
    try:
        locale = InstanceMeta.load(resolved).locale
    except Exception:  # noqa: BLE001 - 读不出语言不影响登记
        locale = ""
    return registry.add(resolved, locale=locale)


@dataclass(frozen=True)
class InstanceEntry:
    """注册表里的一条实例记录。

    :param name: 注册名，命令行与界面都用它引用实例。
    :param root: 实例根目录绝对路径。
    :param locale: 实例默认语言；空串表示未记录。
    :param added_at: 加入时间，ISO 8601 字符串。
    :param autostart: 是否随服务启动而拉起（开机自启）。
    :param restart_on_crash: 崩溃后是否自动重启。
    :param desired: 最后已知的期望状态：``running`` 或 ``stopped``。
    """

    name: str
    root: Path
    locale: str = ""
    added_at: str = ""
    autostart: bool = False
    restart_on_crash: bool = False
    desired: str = STATE_STOPPED

    def to_mapping(self) -> dict[str, object]:
        """转成写盘用的映射。"""
        return {
            "root": str(self.root),
            "locale": self.locale,
            "added_at": self.added_at,
            "autostart": self.autostart,
            "restart_on_crash": self.restart_on_crash,
            "desired": self.desired,
        }

    @property
    def exists(self) -> bool:
        """实例目录是否仍是一个实例（含 ``akaribot.toml``）。"""
        return (self.root / INSTANCE_META_FILENAME).is_file()


class InstanceRegistry:
    """注册表读写。

    :param path: 注册表文件路径；缺省为 :func:`registry_path`。
    """

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path is not None else registry_path()

    def load(self) -> tuple[InstanceEntry, ...]:
        """读取全部记录，按名称排序。

        :raises RegistryError: 文件存在但无法解析。
        """
        if not self.path.is_file():
            return ()
        try:
            document = tomlkit.parse(self.path.read_text(encoding="utf-8"))
        except Exception as error:  # noqa: BLE001 - 解析失败的原因照实上报
            raise RegistryError(i18n.t("cli.instance_registry.bad_file", path=self.path, error=error)) from error
        section = document.get("instances")
        if section is None:
            return ()
        if not isinstance(section, dict):
            raise RegistryError(i18n.t("cli.instance_registry.bad_section", path=self.path))
        entries: list[InstanceEntry] = []
        for name, raw in section.items():
            if not isinstance(raw, dict):
                continue
            entries.append(
                InstanceEntry(
                    name=str(name),
                    root=Path(str(raw.get("root") or "")).expanduser(),
                    locale=str(raw.get("locale") or ""),
                    added_at=str(raw.get("added_at") or ""),
                    autostart=bool(raw.get("autostart")),
                    restart_on_crash=bool(raw.get("restart_on_crash")),
                    desired=str(raw.get("desired") or STATE_STOPPED),
                )
            )
        return tuple(sorted(entries, key=lambda entry: entry.name))

    def default_name(self) -> str:
        """返回缺省实例名；未设置时为空串。"""
        if not self.path.is_file():
            return ""
        try:
            document = tomlkit.parse(self.path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - 读不出缺省名时按未设置处理
            return ""
        return str(document.get("default") or "")

    def get(self, name: str) -> InstanceEntry | None:
        """按名称取一条记录；不存在时返回 ``None``。"""
        for entry in self.load():
            if entry.name == name:
                return entry
        return None

    def find_by_root(self, root: Path) -> InstanceEntry | None:
        """按实例根取记录；比较真实路径，软链接与相对写法都能命中。"""
        wanted = _resolve(root)
        for entry in self.load():
            if _resolve(entry.root) == wanted:
                return entry
        return None

    def add(
        self,
        root: Path,
        *,
        name: str | None = None,
        locale: str = "",
        autostart: bool = False,
        restart_on_crash: bool = False,
    ) -> InstanceEntry:
        """登记一个实例；已登记过同一目录时原样返回既有记录。

        :param root: 实例根目录，须含 ``akaribot.toml``。
        :param name: 注册名；缺省按目录名推一个不冲突的名字。
        :param locale: 实例默认语言。
        :param autostart: 是否随服务启动而拉起。
        :param restart_on_crash: 崩溃后是否自动重启。
        :raises RegistryError: 目录不是实例，或名称已被别的目录占用。
        """
        root = _resolve(root)
        if not (root / INSTANCE_META_FILENAME).is_file():
            raise RegistryError(_not_instance_message(root))
        existing = self.find_by_root(root)
        if existing is not None:
            return existing
        entries = {entry.name: entry for entry in self.load()}
        chosen = name or self._free_name(entries, suggested_name(root))
        if not NAME_PATTERN.fullmatch(chosen):
            raise RegistryError(i18n.t("cli.instance_registry.bad_name", name=chosen))
        if chosen in entries:
            raise RegistryError(i18n.t("cli.instance_registry.name_taken", name=chosen, root=entries[chosen].root))
        entry = InstanceEntry(
            name=chosen,
            root=root,
            locale=locale,
            added_at=datetime.now(UTC).isoformat(),
            autostart=autostart,
            restart_on_crash=restart_on_crash,
            desired=STATE_STOPPED,
        )
        entries[chosen] = entry
        self._write(entries, default=self.default_name() or chosen)
        return entry

    def remove(self, name: str) -> bool:
        """删除一条记录；目录本身不动。

        :param name: 注册名。
        :return: 是否确实删掉了一条。
        """
        entries = {entry.name: entry for entry in self.load()}
        if name not in entries:
            return False
        del entries[name]
        default = self.default_name()
        self._write(entries, default="" if default == name else default)
        return True

    def update(self, name: str, **fields: object) -> InstanceEntry:
        """改写一条记录的字段。

        :param name: 注册名。
        :param fields: 要改写的字段，取值同 :class:`InstanceEntry`。
        :raises RegistryError: 实例未登记。
        """
        entries = {entry.name: entry for entry in self.load()}
        entry = entries.get(name)
        if entry is None:
            raise RegistryError(i18n.t("cli.instance_registry.unknown", name=name))
        updated = replace(entry, **fields)  # type: ignore[arg-type]
        entries[name] = updated
        self._write(entries, default=self.default_name())
        return updated

    def set_default(self, name: str) -> None:
        """设置缺省实例。

        :param name: 注册名。
        :raises RegistryError: 实例未登记。
        """
        entries = {entry.name: entry for entry in self.load()}
        if name not in entries:
            raise RegistryError(i18n.t("cli.instance_registry.unknown", name=name))
        self._write(entries, default=name)

    def _free_name(self, entries: dict[str, InstanceEntry], base: str) -> str:
        if base not in entries:
            return base
        for index in range(2, 100):
            candidate = f"{base}-{index}"
            if candidate not in entries:
                return candidate
        return base

    def _write(self, entries: dict[str, InstanceEntry], default: str) -> None:
        document = tomlkit.document()
        document.add(tomlkit.comment("本机已知的 AkariBot 实例。由 akaribot instance 子命令维护。"))
        document["default"] = default
        section = tomlkit.table(is_super_table=True)
        for name in sorted(entries):
            table = tomlkit.table()
            for key, value in entries[name].to_mapping().items():
                table[key] = value
            section[name] = table
        document["instances"] = section
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(tomlkit.dumps(document), encoding="utf-8")


def probe_running(root: Path) -> bool | None:
    """探测实例是否在运行；探测机制不可用时返回 ``None``。

    :param root: 实例根目录。
    :return: 是否在运行；无法判定时为 ``None``。
    """
    from akaribot.cli.instance import Instance, system_python

    try:
        return bool(Instance(root, python_override=system_python()).is_running())
    except Exception:  # noqa: BLE001 - 探测失败按未知处理，不中断调用方
        return None


def _not_instance_message(root: Path) -> str:
    found = child_instances(root)
    if not found:
        return i18n.t("cli.instance_registry.not_instance", path=root, meta=INSTANCE_META_FILENAME)
    listing = i18n.t("cli.common.list_separator").join(str(path) for path in found)
    return i18n.t(
        "cli.instance_registry.not_instance_with_children",
        path=root,
        meta=INSTANCE_META_FILENAME,
        found=listing,
    )


def _resolve(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except OSError:
        return path.expanduser()
