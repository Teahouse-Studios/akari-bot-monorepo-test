"""配置页：配置表浏览、表单编辑与原始文本编辑。

数据通过 :class:`ConfigSource` 读取，保存通过 ``akaribot config set`` 执行。
密钥写入 ``<表>_secret`` 段；``config`` 表的密钥段为 ``secret``。
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import tomlkit
from tomlkit.exceptions import ParseError
from tomlkit.items import Table

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui import cli_process
from akaribot.cli.tui import context

KIND_BOOL = "bool"
KIND_INT = "int"
KIND_FLOAT = "float"
KIND_STR = "str"
KIND_LIST = "list"
KIND_OTHER = "other"

MODE_FORM = "form"
MODE_RAW = "raw"

# 类型标签保存文案键，按当前语言解析。
_KIND_KEYS = {
    KIND_BOOL: "cli.tui.config.kind_bool",
    KIND_INT: "cli.tui.config.kind_int",
    KIND_FLOAT: "cli.tui.config.kind_float",
    KIND_STR: "cli.tui.config.kind_str",
    KIND_LIST: "cli.tui.config.kind_list",
    KIND_OTHER: "cli.tui.config.kind_other",
}
# 类型名归一化：schema 的 type 取自运行期值的 __name__，会随模板写法变化，故按子串匹配。
_KIND_MARKERS = (
    ("bool", KIND_BOOL),
    ("int", KIND_INT),
    ("float", KIND_FLOAT),
    ("list", KIND_LIST),
    ("tuple", KIND_LIST),
    ("set", KIND_LIST),
    ("array", KIND_LIST),
    ("str", KIND_STR),
)
_TRUE_WORDS = frozenset({"true", "1", "yes", "y", "on", "是", "真", "开"})
_FALSE_WORDS = frozenset({"false", "0", "no", "n", "off", "否", "假", "关"})
_NUMBER_PATTERN = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?")
_LIST_SPLIT_PATTERN = re.compile(r"[,，]")
_ERROR_TAIL_PATTERN = re.compile(r"\s*at line \d+ col \d+\s*$")

# 表名与配置文件一一对应：config.toml 同时承载 config 与 secret 两段。
_FILE_BY_TABLE = {"config": "config.toml", "secret": "config.toml"}
_CONFIG_SUBDIRS = ("", "modules", "adapters", "core")


# region 外部编辑器


def editor_setting(env: Mapping[str, str] | None = None) -> str:
    """返回外部编辑器命令文本，取值顺序与 ``akaribot config open`` 一致。

    :param env: 环境变量映射，默认取 ``os.environ``。
    :return: ``VISUAL`` / ``EDITOR`` 的取值；两者都为空时按平台取默认命令。
    """
    source = os.environ if env is None else env
    chosen = source.get("VISUAL") or source.get("EDITOR")
    if chosen:
        return chosen
    if sys.platform.startswith("win"):
        return "notepad"
    return "open" if sys.platform == "darwin" else "xdg-open"


def editor_argv(env: Mapping[str, str] | None = None) -> list[str] | None:
    """把编辑器命令文本拆成 argv，无法获取可执行文件时返回 ``None``。

    :param env: 环境变量映射，默认取 ``os.environ``。
    :return: 命令 argv；引号不配对或首个词不是可执行文件时为 ``None``。
    """
    try:
        parts = shlex.split(editor_setting(env))
    except ValueError:
        return None
    if not parts or shutil.which(parts[0]) is None:
        return None
    return parts


def _stdin_isatty() -> bool:
    # 标准输入必须连接终端，否则外部编辑器无法交互。
    return bool(sys.stdin.isatty())


# endregion


# region 字段模型与值文本


def kind_of_type(type_name: str) -> str:
    """把对端给的类型名归一到 :data:`KIND_BOOL` 等六种取值。

    :param type_name: ``akaribot config schema --json`` 中的 ``type`` 字段。
    :return: 归一化类型；无法识别时为 :data:`KIND_OTHER`。
    """
    raw = (type_name or "").strip().casefold()
    if not raw:
        return KIND_STR
    for marker, kind in _KIND_MARKERS:
        if marker in raw:
            return kind
    return KIND_OTHER


def kind_of_value(value: Any) -> str:
    """按运行期值的 Python 类型推断归一化类型。"""
    if isinstance(value, bool):
        return KIND_BOOL
    if isinstance(value, int):
        return KIND_INT
    if isinstance(value, float):
        return KIND_FLOAT
    if isinstance(value, (list, tuple, set)):
        return KIND_LIST
    if isinstance(value, str):
        return KIND_STR
    return KIND_OTHER


def _list_items(value: Any) -> list[Any]:
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [] if value is None else [value]


def _item_write_text(item: Any) -> str:
    if isinstance(item, bool):
        return "true" if item else "false"
    if isinstance(item, int):
        return str(item)
    if isinstance(item, float):
        return repr(item)
    text = str(item)
    if _NUMBER_PATTERN.fullmatch(text):
        return text
    return json.dumps(text, ensure_ascii=False)


def write_text(value: Any, kind: str = "") -> str:
    """把值渲染为可交给 ``config set`` 的规范文本。

    :param value: 运行期值。
    :param kind: 归一化类型；默认按值推断。
    :return: 布尔为 ``true`` / ``false``，列表为 TOML 数组字面量，字符串不加引号。
    """
    if value is None:
        return ""
    kind = kind or kind_of_value(value)
    if kind == KIND_BOOL:
        return "true" if value else "false"
    if kind == KIND_INT:
        return str(int(value))
    if kind == KIND_FLOAT:
        return repr(float(value))
    if kind == KIND_LIST:
        return "[" + ", ".join(_item_write_text(item) for item in _list_items(value)) + "]"
    return str(value)


def edit_text(value: Any, kind: str = "") -> str:
    """把值渲染为输入框中的文本：列表按中英文逗号分隔，其余同 :func:`write_text`。"""
    if value is None:
        return ""
    if (kind or kind_of_value(value)) == KIND_LIST:
        return ", ".join(item if isinstance(item, str) else write_text(item) for item in _list_items(value))
    return write_text(value, kind)


def _split_list(text: str) -> list[str]:
    items: list[str] = []
    for chunk in _LIST_SPLIT_PATTERN.split(text):
        item = chunk.strip().strip("'\"")
        if item:
            items.append(item)
    return items


def _short(text: str, limit: int = 24) -> str:
    shown = compat.truncate_cells(text.strip(), limit)
    return shown or i18n.t("cli.tui.config.empty_value")


@dataclass(frozen=True)
class ConfigField:
    """一个配置项，字段名按 ``config schema --json`` 的契约归一化。

    :param key: 键名。
    :param table: 逻辑表名，如 ``module_wiki``。
    :param kind: 归一化类型，见 :func:`kind_of_type`。
    :param type_name: 对端给出的原始类型名，未知类型时展示用。
    :param default: 配置模板声明的默认值。
    :param secret: 是否来自密钥段。
    :param comment: i18n 注释，即帮助文本。
    :param value: 当前值。
    :param is_placeholder: 当前值是否为模板占位符。
    """

    key: str
    table: str = ""
    kind: str = KIND_STR
    type_name: str = ""
    default: Any = None
    secret: bool = False
    comment: str = ""
    value: Any = None
    is_placeholder: bool = False

    @property
    def kind_label(self) -> str:
        """返回类型的本地化标签；未知类型附带原始类型名。"""
        label = i18n.t(_KIND_KEYS.get(self.kind, _KIND_KEYS[KIND_OTHER]))
        if self.kind == KIND_OTHER and self.type_name:
            return i18n.t("cli.tui.config.kind_with_type", label=label, name=_short(self.type_name, 12))
        return label

    @property
    def section(self) -> str:
        """返回 ``config set --table`` 用的表引用：密钥段带 ``_secret`` 后缀。"""
        if not self.secret:
            return self.table
        return "secret" if self.table == "config" else f"{self.table}_secret"

    @property
    def edit_value(self) -> str:
        """返回输入控件中的初始文本。"""
        return edit_text(self.value, self.kind)

    @property
    def write_value(self) -> str:
        """返回当前值对应的写入文本，也用于判断字段是否被更改。"""
        return write_text(self.value, self.kind)

    @property
    def help_text(self) -> str:
        """返回帮助文本；优先使用注释，空值时补充默认值。"""
        parts = [self.comment.strip()] if self.comment.strip() else []
        if self.value in (None, "") and self.default not in (None, ""):
            parts.append(i18n.t("cli.tui.config.default_value", value=_short(edit_text(self.default), 40)))
        return i18n.t("cli.tui.common.error_separator").join(parts)

    @property
    def marks(self) -> str:
        """返回表头中的本地化徽标：密钥与待填写。"""
        marks = []
        if self.secret:
            marks.append(i18n.t("cli.tui.config.mark_secret"))
        if self.is_placeholder:
            marks.append(i18n.t("cli.tui.config.mark_placeholder"))
        return "".join(marks)


def parse_field(field: ConfigField, text: str) -> tuple[bool, str, str]:
    """按类型校验一行输入。

    :param field: 配置项，提供类型。
    :param text: 用户输入的文本。
    :return: 三元组——是否通过；写入文本（通过时有效）；错误说明（通过时为空串）。
    """
    raw = text.strip()
    if field.kind == KIND_BOOL:
        lowered = raw.casefold()
        if lowered in _TRUE_WORDS:
            return True, "true", ""
        if lowered in _FALSE_WORDS:
            return True, "false", ""
        return False, "", i18n.t("cli.tui.config.err_boolean", value=repr(_short(text)))
    if field.kind == KIND_INT:
        try:
            return True, write_text(int(raw), KIND_INT), ""
        except ValueError:
            return False, "", i18n.t("cli.tui.config.err_integer", value=repr(_short(text)))
    if field.kind == KIND_FLOAT:
        try:
            return True, write_text(float(raw), KIND_FLOAT), ""
        except ValueError:
            return False, "", i18n.t("cli.tui.config.err_number", value=repr(_short(text)))
    if field.kind == KIND_LIST:
        return True, write_text(_split_list(raw), KIND_LIST), ""
    if isinstance(field.value, Mapping):
        return False, "", i18n.t("cli.tui.config.err_nested_field")
    return True, text, ""


def aligned_headers(fields: Sequence[ConfigField]) -> dict[str, str]:
    """为每个字段生成按显示宽度对齐的表头行。

    键列宽度取最长键，类型列宽度取最宽的本地化标签，故中英混排仍逐列对齐。

    :param fields: 字段序列。
    :return: 键名到表头文本的映射。
    """
    if not fields:
        return {}
    kind_width = compat.column_width(field.kind_label for field in fields)
    rows = [(field.key, f"{compat.pad_cells(field.kind_label, kind_width)}{field.marks}") for field in fields]
    return {field.key: line for field, line in zip(fields, compat.align_rows(rows, gap=2), strict=True)}


def normalize_schema(payload: Any, table: str) -> list[ConfigField]:
    """把 ``config schema --json`` 的输出归一化为字段列表。

    接受三种形态：条目数组、``{"items": [...]}`` 之类的包装对象、键名到条目的映射。

    :param payload: ``json.loads`` 的结果。
    :param table: 逻辑表名。
    :return: 按键名排序的字段列表。
    """
    items: list[Any] = []
    if isinstance(payload, Mapping):
        for key in ("items", "fields", "schema", "data"):
            nested = payload.get(key)
            if isinstance(nested, (list, tuple, Mapping)) and not isinstance(nested, str):
                return normalize_schema(nested, table)
        items = [
            {"key": str(key), **value} if isinstance(value, Mapping) else {"key": str(key)}
            for key, value in payload.items()
        ]
    elif isinstance(payload, (list, tuple)):
        items = list(payload)
    fields: list[ConfigField] = []
    for item in items:
        if isinstance(item, str):
            item = {"key": item}
        if not isinstance(item, Mapping):
            continue
        key = _text(_pick(item, "key", "name", "id"))
        if not key:
            continue
        type_name = _text(_pick(item, "type", "cfg_type", "value_type"))
        value = _pick(item, "value", "current", "value_now", default=None)
        fields.append(
            ConfigField(
                key=key,
                table=table,
                kind=kind_of_type(type_name) if type_name else kind_of_value(value),
                type_name=type_name,
                default=_pick(item, "default", "default_value", default=None),
                secret=bool(_pick(item, "secret", "is_secret", default=False)),
                comment=_text(_pick(item, "comment", "description", "help", "doc")),
                value=value,
                is_placeholder=bool(_pick(item, "is_placeholder", "placeholder", default=False)),
            )
        )
    return sorted(fields, key=lambda field: field.key)


def _pick(source: Any, *names: str, default: Any = "") -> Any:
    for name in names:
        if isinstance(source, Mapping) and source.get(name) is not None:
            return source[name]
        value = getattr(source, name, None)
        if value is not None:
            return value
    return default


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value)


# endregion


# region 原始文本的解析与摊平


@dataclass(frozen=True)
class RawParseResult:
    """原始 TOML 文本的解析结果。

    :param ok: 是否解析成功。
    :param document: ``tomlkit.parse`` 的结果，失败时为 ``None``。
    :param message: 失败说明，含出错行与列。
    :param line: 出错行号（从 1 起），定位不到时为 ``None``。
    """

    ok: bool
    document: Any = None
    message: str = ""
    line: int | None = None


@dataclass(frozen=True)
class RawEntry:
    """原始文本中的一条可写入项。

    :param section: ``config set --table`` 用的表引用。
    :param key: 键名。
    :param text: 写入文本。
    """

    section: str
    key: str
    text: str

    @property
    def label(self) -> str:
        """返回「表.键=值」形式的一行说明。"""
        return f"{self.section}.{self.key}={self.text}"


def _error_reason(error: ParseError) -> str:
    return _ERROR_TAIL_PATTERN.sub("", str(error)).strip()


def _error_position(error: ParseError, text: str) -> tuple[int | None, int | None]:
    # tomlkit 对文件尾部的未闭合结构会报回第 1 行第 0 列，此处校正到最后一行。
    line = getattr(error, "line", None)
    column = getattr(error, "col", None)
    if line is None:
        return None, None
    if "\x00" in str(error) and int(line) <= 1:
        lines = text.splitlines() or [""]
        return len(lines), len(lines[-1]) + 1
    return int(line), (int(column) + 1 if column is not None else None)


def parse_toml_text(text: str) -> RawParseResult:
    """解析原始 TOML 文本，失败时给出可定位到行的说明。

    :param text: 编辑区中的全文。
    :return: 解析结果；失败时 ``message`` 形如「TOML 解析失败（第 2 行第 5 列）：…」。
    """
    try:
        return RawParseResult(True, tomlkit.parse(text))
    except ParseError as error:
        line, column = _error_position(error, text)
        where = (
            i18n.t("cli.tui.config.error_position", line=line, column=column)
            if line is not None and column is not None
            else i18n.t("cli.tui.config.error_position_unknown")
        )
        lines = text.splitlines()
        snippet = (
            i18n.t("cli.tui.config.error_snippet", content=repr(lines[line - 1].strip()))
            if line is not None and 0 < line <= len(lines)
            else ""
        )
        return RawParseResult(
            False,
            None,
            i18n.t("cli.tui.config.error_toml", where=where, reason=_error_reason(error), snippet=snippet),
            line,
        )
    except Exception as error:  # noqa: BLE001 - 解析器的其他异常同样只用于展示，不应中断界面
        return RawParseResult(
            False, None, i18n.t("cli.tui.config.error_toml_generic", kind=type(error).__name__, error=error)
        )


def _unwrap(item: Any) -> Any:
    return item.unwrap() if hasattr(item, "unwrap") else item


def _section_matches(section: str, table: str) -> bool:
    if section == table:
        return True
    return section in ({"secret"} if table == "config" else {f"{table}_secret"})


def flatten_document(document: Any, table: str) -> tuple[list[RawEntry], list[str]]:
    """把 TOML 文档摊平为可经 ``config set`` 写入的条目。

    嵌套表与顶层键无法表达为一次 ``config set``（写路径仅支持「段 + 键」两层），故跳过并给出原因。

    :param document: ``tomlkit.parse`` 的结果。
    :param table: 当前编辑的表名。
    :return: 二元组——条目列表；跳过项的说明列表。
    """
    entries: list[RawEntry] = []
    skipped: list[str] = []
    for name, value in document.items():
        section = str(name)
        if isinstance(value, Table):
            if not _section_matches(section, table):
                skipped.append(i18n.t("cli.tui.config.skipped_section", section=section, table=table))
                continue
            for key, item in value.items():
                if isinstance(item, Table):
                    skipped.append(i18n.t("cli.tui.config.skipped_nested_table", section=section, name=key))
                    continue
                unwrapped = _unwrap(item)
                if _is_nested(unwrapped):
                    skipped.append(i18n.t("cli.tui.config.skipped_nested_value", section=section, name=key))
                    continue
                entries.append(RawEntry(section=section, key=str(key), text=write_text(unwrapped)))
            continue
        skipped.append(i18n.t("cli.tui.config.skipped_top_level", section=section, table=table))
    return entries, skipped


def _is_nested(value: Any) -> bool:
    if isinstance(value, Mapping):
        return True
    return isinstance(value, (list, tuple)) and any(isinstance(item, Mapping) for item in value)


def diff_document(
    document: Any, fields: Sequence[ConfigField], table: str
) -> tuple[list[RawEntry], list[str], list[str]]:
    """比较原始文本与当前值，给出需要写入的条目。

    :param document: 解析后的文档。
    :param fields: 当前表的字段，提供各键的类型与当前值。
    :param table: 表名。
    :return: 三元组——更改条目；跳过说明；值未变的键名。
    """
    entries, skipped = flatten_document(document, table)
    current = {(field.section, field.key): field.write_value for field in fields}
    changes: list[RawEntry] = []
    unchanged: list[str] = []
    for entry in entries:
        if current.get((entry.section, entry.key)) == entry.text:
            unchanged.append(entry.key)
            continue
        changes.append(entry)
    return changes, skipped, unchanged


# endregion


# region 数据源


class ConfigSourceError(RuntimeError):
    """数据源不可用：子进程缺失、退出码非零或输出不是 JSON。"""


@dataclass(frozen=True)
class SetResult:
    """一次写入的结果。

    :param ok: 子进程是否成功。
    :param message: 一行结论，用于状态栏与通知。
    :param detail: 失败时的补充信息，通常为子进程输出尾部。
    """

    ok: bool
    message: str
    detail: str = ""


class StaticConfigSource:
    """固定数据的替身数据源，供自动化断言与自检使用，不产生任何子进程。

    :param tables: 配置表列表。
    :param fields: 表名到字段序列的映射。
    :param raw: 表名到原始 TOML 文本的映射。
    :param files: 表名到配置文件路径的映射，供编辑器动作定位文件。
    :param set_result: 写入返回值；默认为成功。
    """

    def __init__(
        self,
        tables: Sequence[str] = (),
        fields: Mapping[str, Sequence[ConfigField]] | None = None,
        raw: Mapping[str, str] | None = None,
        *,
        files: Mapping[str, str | Path] | None = None,
        set_result: SetResult | None = None,
    ) -> None:
        self._tables = tuple(tables)
        self._fields = {name: tuple(items) for name, items in (fields or {}).items()}
        self._raw = dict(raw or {})
        self._files = {name: Path(path) for name, path in (files or {}).items()}
        self._set_result = set_result or SetResult(True, i18n.t("cli.tui.config.stub_write_ok"), "stub")
        self.calls = {"list": 0, "schema": 0, "raw": 0, "set": 0}
        self.applied: list[tuple[str, str, str]] = []

    def list_tables(self) -> Sequence[str]:
        """见 :meth:`ConfigSource.list_tables`。"""
        self.calls["list"] += 1
        return self._tables

    def schema(self, table: str) -> Sequence[ConfigField]:
        """见 :meth:`ConfigSource.schema`。"""
        self.calls["schema"] += 1
        return self._fields.get(table, ())

    def read_raw(self, table: str) -> str:
        """见 :meth:`ConfigSource.read_raw`。"""
        self.calls["raw"] += 1
        return self._raw.get(table, "")

    def set_value(self, section: str, key: str, value: str) -> SetResult:
        """见 :meth:`ConfigSource.set_value`。"""
        self.calls["set"] += 1
        self.applied.append((section, key, value))
        return self._set_result

    def config_file(self, table: str) -> Path | None:
        """见 :meth:`ConfigSource.config_file`。"""
        return self._files.get(table)


@runtime_checkable
class ConfigSource(Protocol):
    """配置数据源接口；测试注入替身，实际运行通过子进程访问。"""

    def list_tables(self) -> Sequence[str]:
        """返回实例内的全部配置表名。"""

    def schema(self, table: str) -> Sequence[ConfigField]:
        """返回一张表的全部字段。"""

    def read_raw(self, table: str) -> str:
        """返回一张表的原始 TOML 文本，只供展示与编辑。"""

    def set_value(self, section: str, key: str, value: str) -> SetResult:
        """写入一项；``section`` 为 ``config set --table`` 的表引用。"""

    def config_file(self, table: str) -> Path | None:
        """返回一张表对应的配置文件路径；定位不到实例时返回 ``None``。"""


class SubprocessConfigSource:
    """配置数据源：通过 CLI 读取配置表列表和字段、写入配置，原始文本直接读取配置文件。

    :param root: 实例根目录，默认当前工作目录。
    :param timeout: 单个子进程的超时秒数。
    :param runner: 子进程执行函数，签名同 :func:`subprocess.run`，测试可注入。
    :param instance_factory: ``Instance`` 的构造回调，测试可注入以避开实例落盘。
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        timeout: float = 120.0,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        instance_factory: Callable[[], Any] | None = None,
    ) -> None:
        # 每次读取时解析实例根，确保切换实例后使用当前实例的配置。
        self._root_override = Path(root).expanduser().resolve() if root is not None else None
        self.timeout = timeout
        self.calls = {"list": 0, "schema": 0, "raw": 0, "set": 0}
        self.last_raw_origin = ""
        self._runner = runner or subprocess.run
        self._instance_factory = instance_factory
        self._instance_cache: Any = None

    @property
    def root(self) -> Path:
        """实例根：显式给定优先，其次界面当前选中的实例，最后自动定位。"""
        return context.resolve_root(self._root_override)

    def list_tables(self) -> Sequence[str]:
        """见 :meth:`ConfigSource.list_tables`。"""
        self.calls["list"] += 1
        errors: list[str] = []
        for strategy in (self._tables_from_cli, self._tables_from_directory):
            try:
                return strategy()
            except ConfigSourceError as error:
                errors.append(str(error))
        raise ConfigSourceError(i18n.t("cli.tui.common.error_separator").join(errors))

    def schema(self, table: str) -> Sequence[ConfigField]:
        """见 :meth:`ConfigSource.schema`。"""
        self.calls["schema"] += 1
        return normalize_schema(self._core_json("schema", "--table", table, label="config schema"), table)

    def read_raw(self, table: str) -> str:
        """见 :meth:`ConfigSource.read_raw`。"""
        self.calls["raw"] += 1
        path = self.config_file(table)
        if path is not None and path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as error:
                raise ConfigSourceError(i18n.t("cli.tui.config.err_read_file", path=path, error=error)) from error
            self.last_raw_origin = i18n.t("cli.tui.config.raw_origin_file", path=path)
            return text
        self.last_raw_origin = i18n.t("cli.tui.config.raw_origin_rebuilt", table=table)
        return rebuild_raw_text(self.schema(table))

    def set_value(self, section: str, key: str, value: str) -> SetResult:
        """见 :meth:`ConfigSource.set_value`。"""
        self.calls["set"] += 1
        instance = self._instance()
        try:
            completed = instance.run_core_capture("config", "set", key, value, "--table", section)
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的结果
            raise ConfigSourceError(
                i18n.t(
                    "cli.tui.config.err_core_write",
                    section=section,
                    name=key,
                    kind=type(error).__name__,
                    error=error,
                )
            ) from error
        if completed.returncode == 0:
            return SetResult(
                True,
                i18n.t("cli.tui.config.result_write_ok", section=section, name=key),
                self._tail(completed.stdout),
            )
        return SetResult(
            False,
            i18n.t("cli.tui.config.err_write_exit", section=section, name=key, code=completed.returncode),
            self._tail(completed.stderr),
        )

    def cli_argv(self, *args: str) -> list[str]:
        """构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。"""
        return cli_process.cli_argv(*args)

    def config_file(self, table: str) -> Path | None:
        """定位配置表对应的文件；实例未找到时返回 ``None``。

        :param table: 表引用（可能带 ``_secret`` 后缀；与基表同文件）。
        :return: 配置文件路径（未必存在）。
        """
        root = self._instance_root()
        if root is None:
            return None
        base = root / "config"
        name = _FILE_BY_TABLE.get(table, f"{table}.toml")
        for sub in _CONFIG_SUBDIRS:
            candidate = base / sub / name if sub else base / name
            if candidate.is_file():
                return candidate
        return base / name

    def _tables_from_cli(self) -> list[str]:
        argv = self.cli_argv("config", "list", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise ConfigSourceError(
                i18n.t(
                    "cli.tui.config.err_cmd_exit",
                    cmd=" ".join(argv),
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return normalize_tables(self._parse_json(completed.stdout, "config list --json"))

    def _tables_from_directory(self) -> list[str]:
        root = self._instance_root()
        if root is None:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_not_instance", root=self.root))
        base = root / "config"
        if not base.is_dir():
            raise ConfigSourceError(i18n.t("cli.tui.config.err_no_config_dir", path=base))
        return normalize_tables(sorted(path.stem for path in base.rglob("*.toml")))

    def _core_json(self, *args: str, label: str) -> Any:
        instance = self._instance()
        try:
            completed = instance.run_core_capture("config", *args, "--json")
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的错误
            raise ConfigSourceError(
                i18n.t("cli.tui.config.err_core_call", label=label, kind=type(error).__name__, error=error)
            ) from error
        if completed.returncode != 0:
            raise ConfigSourceError(
                i18n.t(
                    "cli.tui.config.err_cmd_exit",
                    cmd=label,
                    code=completed.returncode,
                    tail=self._tail(completed.stderr),
                )
            )
        return self._parse_json(completed.stdout, label)

    def _instance_root(self) -> Path | None:
        try:
            from akaribot.cli.instance import find_instance_root
        except ImportError:
            return None
        try:
            return find_instance_root(self.root)
        except Exception:  # noqa: BLE001 - 定位失败按「没有实例」处理，由调用方给出提示
            return None

    def _instance(self) -> Any:
        if self._instance_cache is not None:
            return self._instance_cache
        if self._instance_factory is not None:
            self._instance_cache = self._instance_factory()
            return self._instance_cache
        try:
            from akaribot.cli.instance import Instance
        except ImportError as error:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_instance_module")) from error
        root = self._instance_root()
        if root is None:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_no_instance_hint", root=self.root))
        try:
            self._instance_cache = Instance(root)
        except Exception as error:  # noqa: BLE001 - 实例构造失败同样只作为降级原因上报
            raise ConfigSourceError(
                i18n.t("cli.tui.config.err_instance_failed", kind=type(error).__name__, error=error)
            ) from error
        return self._instance_cache

    def _run(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        env = cli_process.cli_env(self.root)
        try:
            return self._runner(
                list(argv),
                cwd=str(self.root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                env=env,
            )
        except FileNotFoundError as error:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_exe_missing", path=argv[0], error=error)) from error
        except subprocess.TimeoutExpired as error:
            raise ConfigSourceError(
                i18n.t("cli.tui.config.err_timeout", cmd=" ".join(argv), seconds=f"{self.timeout:.0f}")
            ) from error
        except OSError as error:
            raise ConfigSourceError(
                i18n.t("cli.tui.config.err_exec_failed", cmd=" ".join(argv), error=error)
            ) from error

    def _parse_json(self, stdout: str, label: str) -> Any:
        text = (stdout or "").strip()
        if not text:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_empty_output", label=label))
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ConfigSourceError(i18n.t("cli.tui.config.err_bad_json", label=label, error=error)) from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        return (text or "").strip()[-limit:]


def normalize_tables(payload: Any) -> list[str]:
    """把 ``config list --json`` 的输出归一化为去重保序的表名列表。

    :param payload: ``json.loads`` 的结果，可为字符串数组或 ``{"tables": [...]}`` 包装对象。
    :return: 表名列表。
    """
    if isinstance(payload, Mapping):
        for key in ("tables", "items", "data"):
            nested = payload.get(key)
            if isinstance(nested, (list, tuple)):
                return normalize_tables(nested)
        return [str(key) for key in payload]
    if isinstance(payload, (list, tuple)):
        names = [str(item).strip() for item in payload if isinstance(item, str) and item.strip()]
        return list(dict.fromkeys(names))
    return []


def rebuild_raw_text(fields: Sequence[ConfigField]) -> str:
    """由字段重建一份可解析的 TOML 文本，供未找到配置文件时展示。

    仅在文件缺失时使用；保存通过 ``config set`` 执行。

    :param fields: 字段序列。
    :return: TOML 文本。
    """
    sections: dict[str, list[ConfigField]] = {}
    for field in fields:
        sections.setdefault(field.section, []).append(field)
    lines: list[str] = []
    for section, items in sections.items():
        lines.append(f"[{section}]")
        lines.extend(f"{item.key} = {_toml_literal(item.value, item.kind)}" for item in items)
    return "\n".join(lines) + ("\n" if lines else "")


def _toml_literal(value: Any, kind: str) -> str:
    if isinstance(value, Mapping):
        if not value:
            return "{}"
        body = ", ".join(f"{key} = {_toml_literal(item, '')}" for key, item in value.items())
        return "{ " + body + " }"
    if isinstance(value, (list, tuple)) and any(isinstance(item, Mapping) for item in value):
        return "[" + ", ".join(_toml_literal(item, "") for item in value) + "]"
    if kind == KIND_STR or isinstance(value, str):
        return json.dumps("" if value is None else str(value), ensure_ascii=False)
    if kind == KIND_LIST:
        return "[" + ", ".join(_item_write_text(item) for item in _list_items(value)) + "]"
    if value is None:
        return '""'
    return write_text(value, kind)


# endregion


# region 控件


def _optional_widget(name: str) -> Any | None:
    # 原生控件是否可用由兼容层决定，页面通过属性检测选择实现。
    return getattr(compat, name, None)


class BoolToggle(compat.Horizontal):
    """布尔开关：``_compat`` 未导出 ``Switch`` / ``Checkbox`` 时用按钮模拟。

    :param value: 初始值。
    :param classes: 附加的 CSS 类。
    """

    def __init__(self, value: bool, *, classes: str | None = None, id: str | None = None) -> None:
        super().__init__(id=id, classes=classes)
        self._value = bool(value)

    def compose(self) -> compat.ComposeResult:
        """装配开关按钮与状态说明。"""
        yield compat.Button(self.label_text(), classes="bool-button")
        yield compat.Static(compat.plain_text(i18n.t("cli.tui.config.bool_hint")), markup=False)

    @property
    def value(self) -> bool:
        """返回当前值。"""
        return self._value

    def label_text(self) -> str:
        """返回按钮文字，开与关配符号区分。"""
        return i18n.t("cli.tui.config.bool_on") if self._value else i18n.t("cli.tui.config.bool_off")

    def set_value(self, value: bool) -> None:
        """设置值并刷新按钮外观。"""
        self._value = bool(value)
        button = self._button()
        if button is None:
            return
        button.label = self.label_text()
        button.variant = "success" if self._value else "default"

    def toggle(self) -> None:
        """在开与关之间切换。"""
        self.set_value(not self._value)

    def _button(self) -> compat.Button | None:
        try:
            return self.query_one(compat.Button)
        except Exception:  # noqa: BLE001 - 未挂载时按无按钮处理
            return None


class FieldRow(compat.Vertical):
    """一个配置项的编辑行：对齐表头、帮助文本、按类型的控件与校验提示。

    :param field: 配置项。
    :param header: 已按显示宽度对齐的表头文本。
    """

    def __init__(self, field: ConfigField, header: str, *, id: str | None = None) -> None:
        super().__init__(id=id)
        self.field = field
        self.header = header
        self.help_text = field.help_text
        self.placeholder_notice = (
            i18n.t("cli.tui.config.placeholder_notice", value=_short(field.edit_value, 40))
            if field.is_placeholder
            else ""
        )
        self.error_text = ""

    def compose(self) -> compat.ComposeResult:
        """按字段类型装配控件；密钥用密码框，占位符另起一行高亮提示。"""
        yield compat.Static(compat.plain_text(self.header), classes="field-header", markup=False)
        if self.help_text:
            yield compat.Static(compat.plain_text(self.help_text), classes="field-help", markup=False)
        if self.placeholder_notice:
            yield compat.Static(
                compat.plain_text(self.placeholder_notice, style="bold yellow"),
                classes="field-placeholder",
                markup=False,
            )
        yield self._build_control()
        yield compat.Static(compat.plain_text(""), classes="field-error", markup=False)

    def _build_control(self) -> compat.Widget:
        if self.field.kind == KIND_BOOL:
            switch = _optional_widget("Switch")
            if switch is not None:
                return switch(value=bool(self.field.value), classes="field-control")
            return BoolToggle(bool(self.field.value))
        placeholder = i18n.t("cli.tui.config.list_placeholder") if self.field.kind == KIND_LIST else ""
        return compat.Input(
            self.field.edit_value,
            password=self.field.secret,
            placeholder=placeholder,
            classes="field-input field-control",
        )

    def control(self) -> compat.Widget:
        """返回本行的输入控件。"""
        return self.query_one(".field-control")

    @property
    def text(self) -> str:
        """返回控件中的当前编辑文本。"""
        control = self.control()
        if isinstance(control, BoolToggle):
            return "true" if control.value else "false"
        if isinstance(control, compat.Input):
            return control.value
        return "true" if getattr(control, "value", False) else "false"

    def set_text(self, text: str) -> None:
        """设置控件文本，等价于用户键入。"""
        control = self.control()
        if isinstance(control, BoolToggle):
            control.set_value(text.strip().casefold() in _TRUE_WORDS)
        elif isinstance(control, compat.Input):
            control.value = text
        else:
            control.value = text.strip().casefold() in _TRUE_WORDS

    def toggle(self) -> None:
        """切换布尔控件；非布尔行不执行操作。"""
        control = self.control()
        if isinstance(control, BoolToggle):
            control.toggle()

    def focus_control(self) -> None:
        """聚焦本行控件。"""
        self.control().focus()

    def show_error(self, message: str) -> None:
        """在行内显示校验错误。"""
        self.error_text = message
        self._error_widget().update(compat.plain_text(message, style="bold red"))

    def clear_error(self) -> None:
        """清空行内校验错误。"""
        self.error_text = ""
        self._error_widget().update(compat.plain_text(""))

    def _error_widget(self) -> compat.Static:
        return self.query_one(".field-error", compat.Static)


class RawTextEditor(compat.VerticalScroll):
    """原始 TOML 编辑区：优先用 ``_compat`` 导出的 ``TextArea``，未导出时降级为逐行输入。

    :param text: 初始文本。
    """

    def __init__(self, text: str = "", *, id: str | None = None) -> None:
        super().__init__(id=id)
        self._lines = text.split("\n") if text else [""]
        self._textarea_cls = _optional_widget("TextArea")

    @property
    def degraded(self) -> bool:
        """是否处于降级实现（``_compat`` 未导出 ``TextArea``）。"""
        return self._textarea_cls is None

    def compose(self) -> compat.ComposeResult:
        """装配编辑区：原生 ``TextArea`` 或「操作按钮 + 逐行输入框」。"""
        if self._textarea_cls is not None:
            yield self._textarea_cls("\n".join(self._lines), language="toml", id="raw-textarea")
            return
        with compat.Horizontal(id="raw-actions"):
            yield compat.Button(i18n.t("cli.tui.config.raw_add_line"), id="raw-add")
            yield compat.Button(i18n.t("cli.tui.config.raw_del_line"), id="raw-del")
            yield compat.Static(
                compat.plain_text(i18n.t("cli.tui.config.raw_hint")),
                id="raw-hint",
                markup=False,
            )
        for index, line in enumerate(self._lines):
            yield compat.Input(line, id=f"raw-line-{index}", classes="raw-line")

    @property
    def text(self) -> str:
        """返回编辑区当前文本。"""
        textarea = self._textarea()
        if textarea is not None:
            return str(textarea.text)
        return "\n".join(item.value for item in self.query(compat.Input))

    async def load_text(self, text: str) -> None:
        """用新文本替换编辑区内容。"""
        textarea = self._textarea()
        if textarea is not None:
            textarea.load_text(text)
            return
        self._lines = text.split("\n") if text else [""]
        await self._remount_lines()

    async def append_line(self) -> None:
        """在末尾追加一空行。"""
        textarea = self._textarea()
        if textarea is not None:
            textarea.load_text(f"{textarea.text}\n")
            return
        self._lines = [*self.text.split("\n"), ""]
        await self._remount_lines()

    async def remove_last_line(self) -> None:
        """删除末尾一行；只剩一行时清空该行。"""
        textarea = self._textarea()
        if textarea is not None:
            lines = str(textarea.text).split("\n")
            textarea.load_text("\n".join(lines[:-1]) if len(lines) > 1 else "")
            return
        lines = self.text.split("\n")
        self._lines = lines[:-1] if len(lines) > 1 else [""]
        await self._remount_lines()

    def _textarea(self) -> Any | None:
        if self._textarea_cls is None:
            return None
        try:
            return self.query_one("#raw-textarea")
        except Exception:  # noqa: BLE001 - 未挂载时按无 TextArea 处理
            return None

    async def _remount_lines(self) -> None:
        await self.remove_children(".raw-line")
        await self.mount(
            *[compat.Input(line, id=f"raw-line-{index}", classes="raw-line") for index, line in enumerate(self._lines)]
        )


# endregion


# region 页面


class ConfigPage(compat.Vertical):
    """配置页控件。

    :param source: 数据源，默认为 :class:`SubprocessConfigSource`。
    :param cache_ttl: 配置表列表缓存有效期秒数；保存与重新加载会立即失效。
    """

    # 限制按钮最小宽度，确保 80 列终端能够显示全部操作。
    DEFAULT_CSS = """
    ConfigPage {
        layout: vertical;
        height: 1fr;
    }
    ConfigPage #config-toolbar {
        height: 3;
        padding: 0 0 0 1;
    }
    ConfigPage #config-toolbar Button {
        min-width: 10;
    }
    ConfigPage #config-caption {
        width: 1fr;
        height: 3;
        padding: 0 1;
        content-align: left middle;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    ConfigPage #config-body {
        height: 1fr;
    }
    ConfigPage #table-list {
        width: 26;
        min-width: 18;
        border: round $primary;
    }
    ConfigPage #table-list > ListItem {
        padding: 0 1;
    }
    ConfigPage #table-list Static {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    ConfigPage #form-pane, ConfigPage #raw-pane {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    ConfigPage .hidden {
        display: none;
    }
    ConfigPage FieldRow {
        height: auto;
        margin: 0 0 1 0;
    }
    ConfigPage .field-header {
        height: 1;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        text-style: bold;
    }
    ConfigPage .field-help {
        height: auto;
        color: $text-muted;
    }
    ConfigPage .field-placeholder {
        height: auto;
    }
    ConfigPage .field-error {
        height: auto;
    }
    ConfigPage .field-input {
        width: 1fr;
    }
    ConfigPage BoolToggle {
        height: 3;
    }
    ConfigPage BoolToggle Button {
        min-width: 10;
    }
    ConfigPage BoolToggle Static {
        height: 3;
        padding: 1 1 0 1;
        color: $text-muted;
    }
    ConfigPage RawTextEditor Input {
        width: 1fr;
    }
    ConfigPage #raw-actions {
        height: 3;
    }
    ConfigPage #raw-hint {
        height: 3;
        padding: 1 1 0 1;
        color: $text-muted;
    }
    ConfigPage #config-status {
        height: 2;
        padding: 0 0 0 1;
        color: $text-muted;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }
    """

    # 文案在类创建时取值：main.py 的 --lang 早于界面模块导入，改语言需重启进程。
    can_focus = True

    # 低频操作由工具栏提供入口，页脚为全局键位保留空间。
    BINDINGS = compat.bindings(
        ("s", "save", i18n.t("cli.tui.config.action_save")),
        ("o", "open_editor", i18n.t("cli.tui.config.action_open_editor"), False),
        ("f", "mode_form", i18n.t("cli.tui.config.action_mode_form"), False),
        ("t", "mode_raw", i18n.t("cli.tui.config.action_mode_raw"), False),
        ("ctrl+r", "reload", i18n.t("cli.tui.config.action_reload"), False),
        ("escape", "focus_tables", i18n.t("cli.tui.config.action_focus_tables"), False),
    )

    def __init__(
        self,
        source: ConfigSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self._activated = False
        self.source: ConfigSource = source if source is not None else SubprocessConfigSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = i18n.t("cli.tui.common.status_ready")
        self._tables: tuple[str, ...] = ()
        self._fields: tuple[ConfigField, ...] = ()
        self._schemas: dict[str, tuple[ConfigField, ...]] = {}
        self._loaded_at: float = 0.0
        self._selected: str | None = None
        self._raw_table: str | None = None
        self._raw_original: str = ""
        self._mode: str = MODE_FORM
        self._saved: tuple[str, ...] = ()
        self._skipped: tuple[str, ...] = ()
        self._confirming: bool = False
        self._rendered_tables: tuple[str, ...] = ()
        self._caption_rendered: str = ""
        self._status_rendered: str = i18n.t("cli.tui.common.status_ready")
        # 终端挂起和编辑器启动允许注入替身，避免自动化测试启动交互进程。
        self._editor_runner: Callable[..., Any] = subprocess.run
        self._suspend: Callable[[], Any] | None = None
        self._stdin_isatty: Callable[[], bool] = _stdin_isatty

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：工具条、配置表列表、表单区、文本区、状态栏。"""
        with compat.Horizontal(id="config-toolbar"):
            yield compat.Button(i18n.t("cli.tui.config.action_mode_form"), id="mode-form", variant="primary")
            yield compat.Button(i18n.t("cli.tui.config.action_mode_raw"), id="mode-raw")
            yield compat.Button(i18n.t("cli.tui.config.action_open_editor"), id="open-editor")
            yield compat.Static(
                compat.plain_text(i18n.t("cli.tui.config.caption_unloaded")), id="config-caption", markup=False
            )
            yield compat.Button(i18n.t("cli.tui.config.action_save"), id="save", variant="success")
            yield compat.Button(i18n.t("cli.tui.config.action_reload"), id="reload")
        with compat.Horizontal(id="config-body"):
            yield compat.ListView(id="table-list")
            with compat.VerticalScroll(id="form-pane"):
                yield compat.Static(
                    compat.plain_text(i18n.t("cli.tui.config.form_hint_loading")), id="form-hint", markup=False
                )
            with compat.VerticalScroll(id="raw-pane", classes="hidden"):
                yield RawTextEditor("", id="raw-editor")
        yield compat.Static(compat.plain_text(i18n.t("cli.tui.common.status_ready")), id="config-status", markup=False)

    def on_mount(self) -> None:
        """挂载后只装配控件；读取数据推迟到首次显示。"""
        compat.set_text_selection(self, False)

    def activate(self) -> None:
        """首次显示时读取配置表列表。"""
        if self._activated:
            return
        self._activated = True
        self.refresh_tables()

    # region 状态读取（供测试与 App 使用）

    @property
    def tables(self) -> tuple[str, ...]:
        """返回缓存中的配置表列表，不触发子进程。"""
        return self._tables

    @property
    def selected_table(self) -> str | None:
        """返回当前表的表名。"""
        return self._selected

    @property
    def fields(self) -> tuple[ConfigField, ...]:
        """返回当前表的字段。"""
        return self._fields

    @property
    def mode(self) -> str:
        """返回当前模式：``form`` 或 ``raw``。"""
        return self._mode

    @property
    def status_text(self) -> str:
        """返回状态栏当前文本。"""
        return self._status_rendered

    @property
    def caption_text(self) -> str:
        """返回表头上方摘要栏当前文本。"""
        return self._caption_rendered

    @property
    def saved_entries(self) -> tuple[str, ...]:
        """返回最近一次保存写入的「表.键=值」列表。"""
        return self._saved

    @property
    def skipped_notes(self) -> tuple[str, ...]:
        """返回最近一次保存中跳过项的说明。"""
        return self._skipped

    def cache_age(self) -> float:
        """返回配置表列表缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    def field_rows(self) -> tuple[FieldRow, ...]:
        """返回表单区中的全部字段行（按渲染顺序）。"""
        return tuple(self.query(FieldRow))

    def row_for(self, key: str) -> FieldRow | None:
        """按键名取字段行，未找到时返回 ``None``。"""
        for row in self.field_rows():
            if row.field.key == key:
                return row
        return None

    def is_dirty(self) -> bool:
        """是否存在未保存的编辑：表单行与原始文本任一与载入值不同即为真。"""
        for row in self.field_rows():
            if self._row_text(row) != row.field.edit_value:
                return True
        return self._raw_table is not None and self.raw_editor().text != self._raw_original

    def dirty_note(self) -> str:
        """返回未保存更改的说明；没有更改时为空串。"""
        if not self.is_dirty():
            return ""
        return i18n.t("cli.tui.config.dirty_note", table=self._selected or i18n.t("cli.tui.common.none"))

    def _row_text(self, row: FieldRow) -> str:
        # 重新挂载期间输入控件可能尚未创建，此时使用载入值。
        try:
            return row.text
        except Exception:  # noqa: BLE001 - 未装配完成的行不构成脏值
            return row.field.edit_value

    def raw_editor(self) -> RawTextEditor:
        """返回原始文本编辑区。"""
        return self.query_one("#raw-editor", RawTextEditor)

    def table_row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的配置表列表行文本，供自动化断言核对宽度。"""
        return self._rendered_tables

    def header_texts(self) -> tuple[str, ...]:
        """返回各字段行的表头文本，供自动化断言核对列对齐。"""
        return tuple(row.header for row in self.field_rows())

    def help_texts(self) -> tuple[str, ...]:
        """返回各字段行的帮助文本，即配置模板的 i18n 注释。"""
        return tuple(row.help_text for row in self.field_rows())

    def form_hint(self) -> str:
        """返回表单区当前显示的提示文本；正在显示字段时为空串。"""
        try:
            hint = self.query_one("#form-hint", compat.Static)
        except Exception:  # noqa: BLE001 - 没有提示控件时按空串处理
            return ""
        # ``Static.content`` 是 update() 传进来的原对象：文本控件收到的是 rich 的 Text。
        content = hint.content
        return str(getattr(content, "plain", content))

    # endregion

    # region 读取与渲染

    def refresh_tables(self, *, force: bool = False) -> None:
        """读取配置表列表。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不读取数据。
        """
        # 强制刷新会重建编辑区，必须确认未保存更改的处理方式。
        if force and self.is_dirty():
            self._confirm_discard(self.reload)
            return
        if not force and self._tables and self.cache_age() < self.cache_ttl:
            self._render_tables()
            self._set_status(
                i18n.t("cli.tui.config.status_cached", age=f"{self.cache_age():.1f}", count=len(self._tables))
            )
            return
        self._set_status(i18n.t("cli.tui.config.status_loading_tables"))
        self.run_worker(self.reload_tables(), group="config-tables", exclusive=True)

    async def reload_tables(self) -> bool:
        """后台读取配置表列表并载入当前表，返回是否成功。"""
        if not compat.mounted(self):
            return False
        try:
            tables = await asyncio.to_thread(self.source.list_tables)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._tables = ()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_tables()
            await self._show_form_hint(i18n.t("cli.tui.config.hint_load_tables_failed", error=error))
            self._set_status(i18n.t("cli.tui.config.status_load_failed", error=error))
            return False
        self._tables = tuple(normalize_tables(list(tables)))
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = i18n.t("cli.tui.config.result_tables_loaded", count=len(self._tables))
        self._render_tables()
        target = self._selected if self._selected in self._tables else (self._tables[0] if self._tables else None)
        if target is None:
            await self._show_form_hint(i18n.t("cli.tui.config.hint_no_tables"))
            self._selected = None
            self._fields = ()
            self._sync_caption()
            self._set_status(i18n.t("cli.tui.config.status_no_tables"))
            return True
        await self.select_table(target)
        return True

    async def select_table(self, table: str | None, *, force: bool = False) -> bool:
        """切换当前表：读取字段（有缓存）并重建右侧面板。

        :param table: 目标表名；``None`` 表示清空。
        :param force: 为 ``True`` 时忽略字段缓存。
        :return: 是否成功。
        """
        if not compat.mounted(self):
            return False
        if table is None:
            self._selected = None
            self._fields = ()
            self._raw_table = None
            await self._rebuild_form(())
            self._sync_caption()
            self._set_status(i18n.t("cli.tui.config.status_no_tables"))
            return False
        self._selected = table
        try:
            self._fields = await self._load_fields(table, force=force)
        except Exception as error:  # noqa: BLE001 - 读取数据失败只影响本页展示
            self._fields = ()
            self.last_error = f"{type(error).__name__}: {error}"
            self._sync_caption()
            await self._show_form_hint(i18n.t("cli.tui.config.hint_table_fields_failed", table=table, error=error))
            self._set_status(i18n.t("cli.tui.config.status_table_failed", table=table, error=error))
            return False
        self.last_error = ""
        await self._rebuild_form(self._fields)
        if self._mode == MODE_RAW:
            await self.load_raw(table, force=force)
        self._sync_caption()
        self._set_status(i18n.t("cli.tui.config.result_table_loaded", table=table, count=len(self._fields)))
        return True

    async def load_raw(self, table: str | None = None, *, force: bool = False) -> bool:
        """读取并展示某表的原始 TOML 文本。

        :param table: 目标表；默认为当前表。
        :param force: 为 ``True`` 时即使已载入也重新加载。
        :return: 是否成功。
        """
        table = table if table is not None else self._selected
        if table is None:
            return False
        if not force and self._raw_table == table:
            return True
        try:
            text = await asyncio.to_thread(self.source.read_raw, table)
        except Exception as error:  # noqa: BLE001 - 读文件失败同样只影响展示
            self.last_error = f"{type(error).__name__}: {error}"
            self._set_status(i18n.t("cli.tui.config.status_raw_failed", table=table, error=error))
            return False
        await self.raw_editor().load_text(text)
        self._raw_table = table
        self._raw_original = text
        return True

    async def set_mode(self, mode: str) -> None:
        """切换编辑模式：表单模式与原始文本模式。

        :param mode: ``form`` 或 ``raw``；其他取值不执行操作。
        """
        if mode not in (MODE_FORM, MODE_RAW):
            return
        self._mode = mode
        form_pane = self.query_one("#form-pane", compat.VerticalScroll)
        raw_pane = self.query_one("#raw-pane", compat.VerticalScroll)
        form_pane.set_class(mode == MODE_RAW, "hidden")
        raw_pane.set_class(mode != MODE_RAW, "hidden")
        self.query_one("#mode-form", compat.Button).variant = "primary" if mode == MODE_FORM else "default"
        self.query_one("#mode-raw", compat.Button).variant = "primary" if mode == MODE_RAW else "default"
        if mode == MODE_RAW and self._selected is not None:
            await self.load_raw(self._selected)
        self._sync_caption()
        mode_key = "cli.tui.config.mode_raw" if mode == MODE_RAW else "cli.tui.config.mode_form"
        self._set_status(i18n.t("cli.tui.config.status_mode_switched", mode=i18n.t(mode_key)))

    async def _load_fields(self, table: str, *, force: bool = False) -> tuple[ConfigField, ...]:
        if not force and table in self._schemas:
            return self._schemas[table]
        fields = tuple(await asyncio.to_thread(self.source.schema, table))
        self._schemas[table] = fields
        return fields

    def invalidate_cache(self, table: str | None = None) -> None:
        """使字段缓存失效；``table`` 为 ``None`` 时清空全部。"""
        if table is None:
            self._schemas.clear()
            self._loaded_at = 0.0
            self._tables = ()
            return
        self._schemas.pop(table, None)
        self._raw_table = None

    async def reload(self, *, force: bool = True) -> bool:
        """作废缓存并重新读取配置表列表与当前表。"""
        self.invalidate_cache()
        self._raw_table = None
        self._raw_original = ""
        return await self.reload_tables()

    async def _rebuild_form(self, fields: Sequence[ConfigField]) -> None:
        if not compat.mounted(self):
            return
        pane = self.query_one("#form-pane", compat.VerticalScroll)
        await pane.remove_children()
        headers = aligned_headers(fields)
        rows = [FieldRow(field, headers[field.key]) for field in fields]
        if rows:
            await pane.mount(*rows)
            return
        hint_key = "cli.tui.config.hint_table_empty" if self._selected else "cli.tui.config.hint_no_selection"
        await pane.mount(compat.Static(compat.plain_text(i18n.t(hint_key)), id="form-hint", markup=False))

    async def _show_form_hint(self, text: str) -> None:
        if not compat.mounted(self):
            return
        pane = self.query_one("#form-pane", compat.VerticalScroll)
        await pane.remove_children()
        await pane.mount(compat.Static(compat.plain_text(text), id="form-hint", markup=False))

    def _render_tables(self) -> None:
        list_view = self.query_one("#table-list", compat.ListView)
        width = self._table_inner_width(list_view)
        rows = [compat.fit_cells(name, width) for name in self._tables]
        list_view.clear()
        if rows:
            list_view.extend([compat.ListItem(compat.Static(compat.plain_text(row), markup=False)) for row in rows])
        list_view.index = self._index_for(self._selected)
        self._rendered_tables = tuple(rows)
        self._sync_caption()

    def _table_inner_width(self, list_view: compat.ListView) -> int:
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 22
        return max(outer - 4, 8)

    def _index_for(self, table: str | None) -> int:
        if table is not None and table in self._tables:
            return self._tables.index(table)
        return 0

    def _sync_caption(self) -> None:
        if self._selected is None:
            text = i18n.t("cli.tui.config.caption_no_selection", total=len(self._tables))
        else:
            secrets = sum(1 for field in self._fields if field.secret)
            placeholders = sum(1 for field in self._fields if field.is_placeholder)
            mode_key = "cli.tui.config.mode_form" if self._mode == MODE_FORM else "cli.tui.config.mode_raw"
            text = i18n.t(
                "cli.tui.config.caption_table",
                table=self._selected,
                total=len(self._fields),
                secrets=secrets,
                placeholders=placeholders,
                mode=i18n.t(mode_key),
            )
        self._caption_rendered = text
        self.query_one("#config-caption", compat.Static).update(compat.plain_text(text))

    def _set_status(self, text: str) -> None:
        self.last_result = text
        self._status_rendered = text
        self.query_one("#config-status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排配置表列表，不重新读取数据。"""
        if self._tables:
            self._render_tables()

    # endregion

    # region 保存

    async def save(self) -> bool:
        """保存当前表，返回是否全部写入成功。

        表单模式逐项校验类型后只写入被更改的键；原始文本模式先用 ``tomlkit.parse()``
        校验全文，解析失败直接拒绝保存并给出出错行，不发出任何写入调用。
        """
        if self._selected is None:
            self._set_status(i18n.t("cli.tui.config.status_no_selection_save"))
            return False
        if not self._fields:
            self._set_status(i18n.t("cli.tui.config.status_no_fields_save"))
            return False
        self._skipped = ()
        if self._mode == MODE_RAW:
            plan = await self._plan_raw_save()
            if plan is None:
                return False
        else:
            plan, errors = self._plan_form_save()
            if errors:
                self.last_error = i18n.t("cli.tui.common.error_separator").join(errors)
                self._set_status(i18n.t("cli.tui.config.status_validation_failed", error=self.last_error))
                compat.notify(
                    self.app,
                    self.last_error,
                    severity="error",
                    title=i18n.t("cli.tui.config.notify_unsaved_title"),
                )
                return False
        if not plan:
            self.last_result = i18n.t("cli.tui.config.result_no_changes")
            self._set_status(
                i18n.t(
                    "cli.tui.config.status_no_changes",
                    table=self._selected,
                    hint=i18n.t("cli.tui.config.help_hint"),
                )
            )
            return True
        return await self._apply(plan)

    def _plan_form_save(self) -> tuple[list[RawEntry], list[str]]:
        # 未更改的字段保留原值，避免将表单不支持的嵌套结构提交给 ``config set``。
        plan: list[RawEntry] = []
        errors: list[str] = []
        for row in self.field_rows():
            row.clear_error()
            field = row.field
            if row.text == field.edit_value:
                continue
            ok, text, message = parse_field(field, row.text)
            if not ok:
                row.show_error(message)
                errors.append(i18n.t("cli.tui.config.err_field", name=field.key, message=message))
                continue
            plan.append(RawEntry(section=field.section, key=field.key, text=text))
        return plan, errors

    async def _plan_raw_save(self) -> list[RawEntry] | None:
        parsed = parse_toml_text(self.raw_editor().text)
        if not parsed.ok:
            self.last_error = parsed.message
            self._set_status(i18n.t("cli.tui.config.status_save_rejected", message=parsed.message))
            compat.notify(
                self.app,
                parsed.message,
                severity="error",
                title=i18n.t("cli.tui.config.notify_toml_title"),
            )
            return None
        assert self._selected is not None
        changes, skipped, unchanged = diff_document(parsed.document, self._fields, self._selected)
        self._skipped = tuple(skipped)
        self.last_result = i18n.t("cli.tui.config.result_diff", changed=len(changes), unchanged=len(unchanged))
        return changes

    async def _apply(self, plan: Sequence[RawEntry]) -> bool:
        assert self._selected is not None
        self._set_status(i18n.t("cli.tui.config.status_writing", count=len(plan)))
        written: list[str] = []
        failures: list[str] = []
        for entry in plan:
            try:
                result = await asyncio.to_thread(self.source.set_value, entry.section, entry.key, entry.text)
            except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成失败项展示
                result = SetResult(
                    False,
                    i18n.t("cli.tui.config.err_write_failed", label=entry.label),
                    f"{type(error).__name__}: {error}",
                )
            if result.ok:
                written.append(entry.label)
                continue
            failures.append(
                i18n.t("cli.tui.config.err_entry", label=entry.label, detail=result.detail or result.message)
            )
        self._saved = tuple(written)
        if failures:
            self.last_error = i18n.t("cli.tui.common.error_separator").join(failures)
            self._set_status(
                i18n.t(
                    "cli.tui.config.status_write_summary",
                    ok=len(written),
                    failed=len(failures),
                    first=failures[0],
                )
            )
            compat.notify(
                self.app,
                failures[0],
                severity="error",
                title=i18n.t("cli.tui.config.notify_write_failed_title"),
            )
            return False
        self.invalidate_cache(self._selected)
        await self.select_table(self._selected, force=True)
        self._set_status(
            i18n.t(
                "cli.tui.config.status_written",
                count=len(written),
                entries=i18n.t("cli.tui.common.list_separator").join(written),
                hint=i18n.t("cli.tui.config.help_hint"),
            )
        )
        compat.notify(
            self.app,
            i18n.t("cli.tui.config.notify_written", count=len(written)),
            severity="information",
            title=self._selected,
        )
        return True

    # endregion

    # region 交互

    @compat.on(compat.ListView.Highlighted, "#table-list")
    def _on_table_highlighted(self, event: compat.ListView.Highlighted) -> None:
        index = compat.highlighted_index(self.query_one("#table-list", compat.ListView))
        if index is None or index >= len(self._tables):
            return
        table = self._tables[index]
        if table != self._selected:
            self.request_table(table)

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "save":
            self.action_save()
        elif button_id == "reload":
            self.action_reload()
        elif button_id == "mode-form":
            self.request_mode(MODE_FORM)
        elif button_id == "mode-raw":
            self.request_mode(MODE_RAW)
        elif button_id == "open-editor":
            self.action_open_editor()
        elif button_id == "raw-add":
            self.run_worker(self.raw_editor().append_line(), group="config-raw", exclusive=True)
        elif button_id == "raw-del":
            self.run_worker(self.raw_editor().remove_last_line(), group="config-raw", exclusive=True)

    def request_table(self, table: str) -> None:
        """切换表前先处理未保存的编辑。

        :param table: 目标表名。
        """

        def _switch() -> Any:
            return self.select_table(table)

        self._confirm_discard(_switch, on_keep=self._restore_table_highlight)

    def request_mode(self, mode: str) -> None:
        """切换编辑模式前先处理未保存的编辑。

        :param mode: ``form`` 或 ``raw``。
        """
        if mode == self._mode:
            return

        def _switch() -> Any:
            return self.set_mode(mode)

        self._confirm_discard(_switch)

    def _confirm_discard(self, proceed: Callable[[], Any], *, on_keep: Callable[[], None] | None = None) -> None:
        # 重建编辑区前必须确认未保存更改的处理方式。
        if self._confirming:
            return
        if not self.is_dirty():
            self.run_worker(proceed(), group="config-select", exclusive=True)
            return

        def _decide(choice: str | None) -> None:
            self._confirming = False
            if choice == "discard":
                # 刷新会触发切换任务，使用独立任务组避免自我取消。
                self.run_worker(self._discard_then(proceed), group="config-switch", exclusive=True)
                return
            self._set_status(i18n.t("cli.tui.config.dirty_kept"))
            if on_keep is not None:
                on_keep()

        self._confirming = True
        compat.ask_choice(
            self.app,
            title=i18n.t("cli.tui.config.dirty_title"),
            hint=i18n.t("cli.tui.config.dirty_hint", table=self._selected or i18n.t("cli.tui.common.none")),
            options=(("discard", i18n.t("cli.tui.config.dirty_discard")),),
            cancel_label=i18n.t("cli.tui.config.dirty_keep"),
            callback=_decide,
        )

    async def _discard_then(self, proceed: Callable[[], Any]) -> None:
        await self._discard_edits()
        await proceed()

    async def _discard_edits(self) -> None:
        for row in self.field_rows():
            try:
                row.clear_error()
                row.set_text(row.field.edit_value)
            except Exception:  # noqa: BLE001 - 行未装配完成时没有可回退的控件
                continue
        if self._raw_table is not None:
            await self.raw_editor().load_text(self._raw_original)

    def _restore_table_highlight(self) -> None:
        # 保留更改时恢复当前表的高亮，确保选中项与编辑内容一致。
        list_view = self.query_one("#table-list", compat.ListView)
        index = self._index_for(self._selected)
        if compat.highlighted_index(list_view) != index:
            list_view.index = index

    def action_save(self) -> None:
        """键位动作：保存当前表。"""
        self.run_worker(self.save(), group="config-save", exclusive=True)

    def action_reload(self) -> None:
        """键位动作：作废缓存并重新加载。"""
        self._confirm_discard(self.reload)

    def action_mode_form(self) -> None:
        """键位动作：切换到表单模式。"""
        self.request_mode(MODE_FORM)

    def action_mode_raw(self) -> None:
        """键位动作：切换到原始文本模式。"""
        self.request_mode(MODE_RAW)

    def config_path(self, table: str | None = None) -> Path | None:
        """返回表的配置文件路径，沿用本页数据源的定位规则。

        :param table: 表名；默认取当前选中的表。
        :return: 配置文件路径；没有选中表或数据源定位不到实例时为 ``None``。
        """
        name = table if table is not None else self._selected
        if name is None:
            return None
        try:
            path = self.source.config_file(name)
        except Exception:  # noqa: BLE001 - 文件定位失败由调用方显示错误
            return None
        return None if path is None else Path(path)

    async def open_in_editor(self) -> bool:
        """使用外部编辑器编辑当前配置文件，退出后重新加载配置。

        :return: 是否启动编辑器并完成重新加载；非交互终端返回 ``False``。
        """
        table = self._selected
        if table is None:
            self._set_status(i18n.t("cli.tui.config.status_editor_no_selection"))
            return False
        path = self.config_path(table)
        if path is None or not path.is_file():
            self._set_status(i18n.t("cli.tui.config.status_editor_no_file", table=table))
            return False
        editor = editor_argv()
        if editor is None:
            self._set_status(i18n.t("cli.tui.config.status_editor_missing", editor=editor_setting()))
            return False
        argv = [*editor, str(path)]
        if not self._stdin_isatty():
            message = i18n.t(
                "cli.tui.config.editor_noninteractive",
                path=str(path.resolve()),
                command=shlex.join(argv),
            )
            compat.notify(
                self.app,
                message,
                severity="warning",
                title=i18n.t("cli.tui.config.action_open_editor"),
            )
            self._set_status(message)
            return False
        suspend = self._suspend if self._suspend is not None else self.app.suspend
        with suspend():
            completed = self._editor_runner(argv)
        await self.reload()
        self._set_status(
            i18n.t(
                "cli.tui.config.status_editor_done",
                table=table,
                code=getattr(completed, "returncode", -1),
            )
        )
        return True

    def action_open_editor(self) -> None:
        """键位动作：用外部编辑器打开当前表的配置文件。"""
        self._confirm_discard(self.open_in_editor)

    def focus_primary(self) -> None:
        """聚焦配置表列表；列表为空时聚焦页面容器。"""
        compat.focus_first(self, "#table-list")

    def action_focus_tables(self) -> None:
        """键位动作：聚焦配置表列表。"""
        self.query_one("#table-list", compat.ListView).focus()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()

    # endregion


# endregion
