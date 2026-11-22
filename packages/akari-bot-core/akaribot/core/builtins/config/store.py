"""TOML/JSON 配置文件的存储层。

用户配置文件位于配置目录根部，文件名是 ``<表名>.toml``。全局默认值镜像存放在
``global/`` 子目录：文件名可以是 ``<表名>.global.toml`` 或 ``<表名>.global.json``。
读取时按表递归合并，用户配置覆盖全局默认值。写回只写用户文件，不修改全局默认值。
"""

import json
import os
import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from time import sleep

from loguru import logger
from tomlkit import TOMLDocument, document, dumps as toml_dumps, item, parse as toml_parser, table
from tomlkit.items import Table

from akaribot.core.constants.exceptions import ConfigOperationError, ConfigValueError

_GLOBAL_SUFFIX = ".global.toml"
_GLOBAL_JSON_SUFFIX = ".global.json"


class TomlStore:
    """一个配置目录下全部配置文件的合并副本。"""

    # 两次检查配置文件改动之间的最小间隔（秒）
    WATCH_INTERVAL = 1.0
    # 等待进入临界区的上限（秒）
    LOCK_TIMEOUT = 10.0
    # 锁文件被判定为陈旧的时长（秒）。该值须显著大于一次正常读写的耗时，
    # 否则会回收仍处于临界区内的进程所持有的锁，导致两个进程同时改写而使配置项互相覆盖
    LOCK_STALE = 60.0

    def __init__(self, path: Path):
        self.path = path
        self.global_path = path / "global"
        # values 是合并后的只读视图，user_values 才是可写回磁盘的用户配置。
        self.values: dict[str, TOMLDocument] = {}
        self.user_values: dict[str, TOMLDocument] = {}
        self._mtimes: dict[str, float] = {}
        self._watch_lock = False
        self._last_watch = 0.0
        self._lock_depth = 0

    @contextmanager
    def exclusive(self) -> Iterator[None]:
        if self._lock_depth:
            self._lock_depth += 1
            try:
                yield
            finally:
                self._lock_depth -= 1
            return

        lock_path = self.path / ".config.lock"
        deadline = time.monotonic() + self.LOCK_TIMEOUT
        fd = None
        while fd is None:
            try:
                fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                # 持锁进程若被强制结束会遗留锁文件，超过时限即判定为陈旧锁并予以回收。
                try:
                    if time.time() - lock_path.stat().st_mtime > self.LOCK_STALE:
                        lock_path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                if time.monotonic() > deadline:
                    raise ConfigOperationError("Operation timeout.")
                sleep(0.05)
        self._lock_depth = 1
        try:
            yield
        finally:
            self._lock_depth = 0
            os.close(fd)
            lock_path.unlink(missing_ok=True)

    def load(self) -> None:
        with self.exclusive():
            try:
                user_values, user_mtimes = self._load_user()
                global_values, global_mtimes = self._load_global()
                self.user_values = user_values
                self._mtimes = {**global_mtimes, **user_mtimes}
                self.values = {
                    name: _merge_documents(global_values.get(name), user_values.get(name))
                    for name in sorted(set(global_values) | set(user_values))
                }
            except Exception as e:
                raise ConfigValueError(e)

    def _load_user(self) -> tuple[dict[str, TOMLDocument], dict[str, float]]:
        values: dict[str, TOMLDocument] = {}
        mtimes: dict[str, float] = {}
        for path in sorted(self.path.glob("*.toml")):
            if not path.is_file():
                continue
            cfg_name = path.name.removesuffix(".toml")
            parsed, mtime = self._read_toml(path)
            # 空 TOML 属于合法输入，解析不会报错。若磁盘上的文件已被清空而内存中仍有内容，
            # 直接覆盖会在下一次保存时将该空状态写回磁盘，配置即永久丢失。
            if not parsed and self.user_values.get(cfg_name):
                logger.error(f"[Config] Config file {path.name} is empty, keeping the loaded values.")
                values[cfg_name] = self.user_values[cfg_name]
                mtimes[cfg_name] = self._mtimes.get(cfg_name, mtime)
                continue
            values[cfg_name] = parsed
            mtimes[cfg_name] = mtime
        return values, mtimes

    def _load_global(self) -> tuple[dict[str, TOMLDocument], dict[str, float]]:
        values: dict[str, TOMLDocument] = {}
        mtimes: dict[str, float] = {}
        if not self.global_path.is_dir():
            return values, mtimes
        for path in sorted(self.global_path.rglob("*")):
            if not path.is_file():
                continue
            table_name = _global_table_name(path)
            if not table_name:
                continue
            if path.name.endswith(_GLOBAL_JSON_SUFFIX) or path.suffix.lower() == ".json":
                parsed, mtime = self._read_json(path)
            else:
                parsed, mtime = self._read_toml(path)
            if table_name in values:
                raise ConfigValueError(f"duplicate global config table {table_name!r}")
            values[table_name] = parsed
            mtimes[table_name] = mtime
        return values, mtimes

    @staticmethod
    def _read_toml(path: Path) -> tuple[TOMLDocument, float]:
        with open(path, "r", encoding="utf-8") as handle:
            return toml_parser(handle.read()), path.stat().st_mtime

    @staticmethod
    def _read_json(path: Path) -> tuple[TOMLDocument, float]:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, Mapping):
            raise ConfigValueError(f"{path}: JSON root must be an object")
        return _json_document(payload), path.stat().st_mtime

    def save(self) -> None:
        with self.exclusive():
            try:
                for cfg_name, cfg in self.user_values.items():
                    file_path = self.path / (cfg_name if cfg_name.endswith(".toml") else f"{cfg_name}.toml")
                    content = toml_dumps(cfg, sort_keys=True)
                    # 仅写入内容确有变化的文件。一次改写通常只涉及一个配置项，
                    # 若重写全部二十余个文件，既会延长临界区，也会触发其它进程的无谓重新加载。
                    if file_path.exists() and file_path.read_text(encoding="utf-8") == content:
                        continue
                    self._atomic_write(file_path, content)
            except Exception as e:
                raise ConfigValueError(e)

    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        tmp_path = path.with_name(f"{path.name}.{os.getpid()}.tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def watch(self) -> None:
        if self._watch_lock:
            return
        # 若每次读取配置都对全部文件执行 stat，单次属性访问将产生数十次系统调用，
        # 代价与读取一个已在内存里的值完全不成比例。配置改动晚至多 WATCH_INTERVAL 秒生效即可。
        now = time.monotonic()
        if now - self._last_watch < self.WATCH_INTERVAL:
            return
        self._last_watch = now

        self._watch_lock = True
        try:
            mtimes = self._scan_mtimes()
            for cfg, mtime in mtimes.items():
                if mtime != self._mtimes.get(cfg):
                    logger.warning("[Config] Config file has been modified, reloading...")
                    self.load()
                    break
        finally:
            # 若不置于 finally 中，一旦加载抛出异常，此后 watch() 将永久空转，磁盘上的改动无法再被读取。
            self._watch_lock = False

    def _scan_mtimes(self) -> dict[str, float]:
        mtimes: dict[str, float] = {}
        try:
            for entry in os.scandir(self.path):
                if entry.is_file() and entry.name.endswith(".toml"):
                    mtimes[entry.name.removesuffix(".toml")] = entry.stat().st_mtime
        except OSError:
            pass
        try:
            for current, _dirs, files in os.walk(self.global_path):
                for name in files:
                    path = Path(current) / name
                    table_name = _global_table_name(path)
                    if table_name:
                        mtimes[table_name] = path.stat().st_mtime
        except OSError:
            pass
        return mtimes

    def switch_path(self, path: Path) -> None:
        self.path = path.resolve()
        self.global_path = self.path / "global"
        self.values = {}
        self.user_values = {}
        self._mtimes = {}
        self._watch_lock = False
        # 切换目录后必须立刻重新检查，不能让上一份目录的节流状态把首次检查挡掉
        self._last_watch = 0.0
        self.load()


def _global_table_name(path: Path) -> str:
    name = path.name
    if name.endswith(_GLOBAL_SUFFIX):
        return name[: -len(_GLOBAL_SUFFIX)]
    if name.endswith(_GLOBAL_JSON_SUFFIX):
        return name[: -len(_GLOBAL_JSON_SUFFIX)]
    if path.suffix.lower() == ".json":
        return path.stem
    return ""


# 递归合并全局默认值与用户配置，后者优先。
def _merge_documents(base: TOMLDocument | None, override: TOMLDocument | None) -> TOMLDocument:
    ""
    if base is None and override is None:
        return document()
    if base is None:
        return _copy_document(override)
    if override is None:
        return _copy_document(base)
    return _merge_mapping(base, override)


def _merge_mapping(base: Mapping, override: Mapping) -> TOMLDocument:
    result = document()
    for key in set(base) | set(override):
        if key in override and isinstance(override[key], Mapping):
            result[key] = _merge_value(base.get(key), override[key])
        elif key in override:
            result[key] = _copy_value(override[key])
        else:
            result[key] = _copy_value(base[key])
    return result


def _merge_value(base: object, override: Mapping) -> Table:
    if isinstance(base, Mapping):
        return _merge_mapping(base, override)
    result = table()
    for key, value in override.items():
        result[key] = _copy_value(value)
    return result


def _copy_document(source: TOMLDocument | None) -> TOMLDocument:
    return _merge_mapping(source or {}, {})


def _copy_value(value: object) -> object:
    if isinstance(value, Mapping):
        result = table()
        for key, item_value in value.items():
            result[key] = _copy_value(item_value)
        return result
    if isinstance(value, list):
        return item([_copy_value(element) for element in value])
    return item(value)


def _json_document(payload: Mapping) -> TOMLDocument:
    result = document()
    for key, value in payload.items():
        result[str(key)] = _copy_value(value)
    return result


__all__ = ["TomlStore"]
