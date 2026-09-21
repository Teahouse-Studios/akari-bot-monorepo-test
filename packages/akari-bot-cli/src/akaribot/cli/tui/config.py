"""Config 页：表切换 + 表单模式 + 原始文本模式。

数据流：界面只读 :class:`ConfigSource`，默认实现 :class:`SubprocessConfigSource` 以子进程取数
（CLI 进程不 import core）。表清单来自 ``akaribot config list --json``，字段来自
``akaribot config schema --table <表> --json``；原始文本模式读配置文件只为展示，保存一律经
``akaribot config set <键> <值> --table <表>``，与命令行走同一条 ``CFGManager.edit_write()`` 原子路径。

写路径说明：本页不打开配置文件写，也不自己拼 tmp 文件；密钥字段按 ``<表>_secret`` 段写
（``config`` 表的密钥段为 ``secret``），与 core 的 ``write()`` 对表名的约定一致。
"""

from __future__ import annotations

import asyncio
import json
import os
import re
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

from akaribot.cli.tui import _compat as compat

KIND_BOOL = "bool"
KIND_INT = "int"
KIND_FLOAT = "float"
KIND_STR = "str"
KIND_LIST = "list"
KIND_OTHER = "other"

MODE_FORM = "form"
MODE_RAW = "raw"

_KIND_LABELS = {
    KIND_BOOL: "布尔",
    KIND_INT: "整数",
    KIND_FLOAT: "数值",
    KIND_STR: "文本",
    KIND_LIST: "列表",
    KIND_OTHER: "类型未知",
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
_CLI_ENV_BIN = "AKARIBOT_CLI_BIN"

_HELP_HINT = "帮助文本取自配置模板的 i18n 注释；保存经 `akaribot config set`，不直接改文件。"


# region 字段模型与值文本


def kind_of_type(type_name: str) -> str:
    """把对端给的类型名归一到 :data:`KIND_BOOL` 等六种取值。

    :param type_name: ``akaribot config schema --json`` 里的 ``type`` 字段。
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
    """把列表值归一为元素列表，非序列输入按单元素处理。"""
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [] if value is None else [value]


def _item_write_text(item: Any) -> str:
    """返回列表元素的写入文本：数字与布尔不加引号，其余按 TOML 字符串转义。"""
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
    :param kind: 归一化类型；缺省按值推断。
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
    """把值渲染为输入框里的文本：列表按中英文逗号分隔，其余同 :func:`write_text`。"""
    if value is None:
        return ""
    if (kind or kind_of_value(value)) == KIND_LIST:
        return ", ".join(item if isinstance(item, str) else write_text(item) for item in _list_items(value))
    return write_text(value, kind)


def _split_list(text: str) -> list[str]:
    """按中英文逗号拆分列表输入，去空白与成对引号，丢弃空项。"""
    items: list[str] = []
    for chunk in _LIST_SPLIT_PATTERN.split(text):
        item = chunk.strip().strip("'\"")
        if item:
            items.append(item)
    return items


def _short(text: str, limit: int = 24) -> str:
    """截断错误信息里的用户输入，避免状态栏被长值挤爆。"""
    shown = compat.truncate_cells(text.strip(), limit)
    return shown or "空"


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
        """返回类型的中文标签，未知类型带上对端给出的原始类型名。"""
        if self.kind == KIND_OTHER and self.type_name:
            return f"{_KIND_LABELS[KIND_OTHER]}({_short(self.type_name, 12)})"
        return _KIND_LABELS.get(self.kind, _KIND_LABELS[KIND_OTHER])

    @property
    def section(self) -> str:
        """返回 ``config set --table`` 用的表引用：密钥段带 ``_secret`` 后缀。"""
        if not self.secret:
            return self.table
        return "secret" if self.table == "config" else f"{self.table}_secret"

    @property
    def edit_value(self) -> str:
        """返回输入控件里的初始文本。"""
        return edit_text(self.value, self.kind)

    @property
    def write_value(self) -> str:
        """返回当前值对应的写入文本，也用于判断字段是否被改动。"""
        return write_text(self.value, self.kind)

    @property
    def help_text(self) -> str:
        """返回帮助文本：注释优先，值为空时补一句默认值。"""
        parts = [self.comment.strip()] if self.comment.strip() else []
        if self.value in (None, "") and self.default not in (None, ""):
            parts.append(f"默认值：{_short(edit_text(self.default), 40)}")
        return "；".join(parts)

    @property
    def marks(self) -> str:
        """返回表头里的中文徽标：密钥与待填写。"""
        marks = []
        if self.secret:
            marks.append("（密钥）")
        if self.is_placeholder:
            marks.append("（待填写）")
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
        return False, "", f"布尔值只能填 true 或 false，当前为 {_short(text)!r}"
    if field.kind == KIND_INT:
        try:
            return True, write_text(int(raw), KIND_INT), ""
        except ValueError:
            return False, "", f"整数格式无效：{_short(text)!r}"
    if field.kind == KIND_FLOAT:
        try:
            return True, write_text(float(raw), KIND_FLOAT), ""
        except ValueError:
            return False, "", f"数值格式无效：{_short(text)!r}"
    if field.kind == KIND_LIST:
        return True, write_text(_split_list(raw), KIND_LIST), ""
    if isinstance(field.value, Mapping):
        return False, "", "该键是嵌套结构，表单模式无法安全写入，请用 `akaribot config open` 编辑"
    return True, text, ""


def aligned_headers(fields: Sequence[ConfigField]) -> dict[str, str]:
    """为每个字段生成按显示宽度对齐的表头行。

    键列宽度取最长键，类型列宽度取最宽中文标签（如「类型未知」），故中英混排仍逐列对齐。

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
    """从字典或对象上按候选名取值，兼容对端契约未冻结时的字段别名。"""
    for name in names:
        if isinstance(source, Mapping) and source.get(name) is not None:
            return source[name]
        value = getattr(source, name, None)
        if value is not None:
            return value
    return default


def _text(value: Any) -> str:
    """把任意标量转为展示用字符串。"""
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
    """原始文本里的一条可写入项。

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
    """取 tomlkit 错误原文中不含行列的部分。"""
    return _ERROR_TAIL_PATTERN.sub("", str(error)).strip()


def _error_position(error: ParseError, text: str) -> tuple[int | None, int | None]:
    """取错误的行列号（行从 1 起、列从 1 起）。

    tomlkit 对文件尾部的未闭合结构会报回第 1 行第 0 列，此处校正到最后一行。

    :param error: tomlkit 抛出的解析错误。
    :param text: 被解析的原文。
    :return: 二元组——行号与列号；取不到时为 ``None``。
    """
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

    :param text: 编辑区里的全文。
    :return: 解析结果；失败时 ``message`` 形如「TOML 解析失败（第 2 行第 5 列）：…」。
    """
    try:
        return RawParseResult(True, tomlkit.parse(text))
    except ParseError as error:
        line, column = _error_position(error, text)
        where = f"第 {line} 行第 {column} 列" if line is not None and column is not None else "行列未知"
        lines = text.splitlines()
        snippet = f"，该行内容为 {lines[line - 1].strip()!r}" if line is not None and 0 < line <= len(lines) else ""
        return RawParseResult(False, None, f"TOML 解析失败（{where}）：{_error_reason(error)}{snippet}", line)
    except Exception as error:  # noqa: BLE001 - 解析器的其它异常同样只用于展示，不应中断界面
        return RawParseResult(False, None, f"TOML 解析失败：{type(error).__name__}: {error}")


def _unwrap(item: Any) -> Any:
    """取 tomlkit 条目的普通 Python 值。"""
    return item.unwrap() if hasattr(item, "unwrap") else item


def _section_matches(section: str, table: str) -> bool:
    """判断文件里的段名是否属于当前表（含密钥段）。"""
    if section == table:
        return True
    return section in ({"secret"} if table == "config" else {f"{table}_secret"})


def flatten_document(document: Any, table: str) -> tuple[list[RawEntry], list[str]]:
    """把 TOML 文档摊平为可经 ``config set`` 写入的条目。

    嵌套表与顶层键无法表达为一次 ``config set``（写路径只认「段 + 键」两层），故跳过并给出原因。

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
                skipped.append(f"[{section}] 不属于表 {table}")
                continue
            for key, item in value.items():
                if isinstance(item, Table):
                    skipped.append(f"{section}.{key} 是嵌套表")
                    continue
                unwrapped = _unwrap(item)
                if _is_nested(unwrapped):
                    skipped.append(f"{section}.{key} 是嵌套结构")
                    continue
                entries.append(RawEntry(section=section, key=str(key), text=write_text(unwrapped)))
            continue
        skipped.append(f"{section} 是顶层键（不属于 [{table}] 段）")
    return entries, skipped


def _is_nested(value: Any) -> bool:
    """判断值是否为无法经 ``config set`` 写入的嵌套结构。"""
    if isinstance(value, Mapping):
        return True
    return isinstance(value, (list, tuple)) and any(isinstance(item, Mapping) for item in value)


def diff_document(
    document: Any, fields: Sequence[ConfigField], table: str
) -> tuple[list[RawEntry], list[str], list[str]]:
    """比较原始文本与当前值，给出真正需要写入的条目。

    :param document: 解析后的文档。
    :param fields: 当前表的字段，提供各键的类型与当前值。
    :param table: 表名。
    :return: 三元组——改动条目；跳过说明；值未变的键名。
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

    :param tables: 表清单。
    :param fields: 表名到字段序列的映射。
    :param raw: 表名到原始 TOML 文本的映射。
    :param set_result: 写入返回值；缺省为成功。
    """

    def __init__(
        self,
        tables: Sequence[str] = (),
        fields: Mapping[str, Sequence[ConfigField]] | None = None,
        raw: Mapping[str, str] | None = None,
        *,
        set_result: SetResult | None = None,
    ) -> None:
        self._tables = tuple(tables)
        self._fields = {name: tuple(items) for name, items in (fields or {}).items()}
        self._raw = dict(raw or {})
        self._set_result = set_result or SetResult(True, "写入成功", "stub")
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


@runtime_checkable
class ConfigSource(Protocol):
    """配置数据源接口；测试注入替身，生产走子进程。"""

    def list_tables(self) -> Sequence[str]:
        """返回实例内的全部配置表名。"""

    def schema(self, table: str) -> Sequence[ConfigField]:
        """返回一张表的全部字段。"""

    def read_raw(self, table: str) -> str:
        """返回一张表的原始 TOML 文本，只供展示与编辑。"""

    def set_value(self, section: str, key: str, value: str) -> SetResult:
        """写入一项；``section`` 为 ``config set --table`` 的表引用。"""


class SubprocessConfigSource:
    """默认数据源：一律经子进程取数与写入，CLI 进程内不 import core。

    取数按优先级降级：表清单先调 ``akaribot config list --json``，失败时退回
    :class:`akaribot.cli.instance.Instance` 的实例目录枚举；字段与写入经
    ``Instance.run_core_capture("config", ...)``，与 ``akaribot config schema/set`` 命令同一条路径。
    原始文本只读配置文件（读不是写，写一律经 ``config set``）。

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
        self.root = Path(root) if root is not None else Path.cwd()
        self.timeout = timeout
        self.calls = {"list": 0, "schema": 0, "raw": 0, "set": 0}
        self.last_raw_origin = ""
        self._runner = runner or subprocess.run
        self._instance_factory = instance_factory
        self._instance_cache: Any = None

    def list_tables(self) -> Sequence[str]:
        """见 :meth:`ConfigSource.list_tables`。"""
        self.calls["list"] += 1
        errors: list[str] = []
        for strategy in (self._tables_from_cli, self._tables_from_directory):
            try:
                return strategy()
            except ConfigSourceError as error:
                errors.append(str(error))
        raise ConfigSourceError("；".join(errors))

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
                raise ConfigSourceError(f"读取 {path} 失败：{error}") from error
            self.last_raw_origin = f"文件 {path}"
            return text
        self.last_raw_origin = f"由 config schema 重建（未找到 {table} 的配置文件）"
        return rebuild_raw_text(self.schema(table))

    def set_value(self, section: str, key: str, value: str) -> SetResult:
        """见 :meth:`ConfigSource.set_value`。"""
        self.calls["set"] += 1
        instance = self._instance()
        try:
            completed = instance.run_core_capture("config", "set", key, value, "--table", section)
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的结果
            raise ConfigSourceError(f"调用 core 写入 {section}.{key} 失败：{type(error).__name__}: {error}") from error
        if completed.returncode == 0:
            return SetResult(True, f"已写入 {section}.{key}", self._tail(completed.stdout))
        return SetResult(
            False,
            f"写入 {section}.{key} 失败（退出码 {completed.returncode}）",
            self._tail(completed.stderr),
        )

    def cli_argv(self, *args: str) -> list[str]:
        """构造调用本 CLI 的 argv；冻结产物去掉 ``-m``，可用 ``AKARIBOT_CLI_BIN`` 覆盖。"""
        override = os.environ.get(_CLI_ENV_BIN)
        if override:
            return [override, *args]
        frozen = bool(getattr(sys, "frozen", False)) or hasattr(sys, "__compiled__")
        if frozen:
            return [sys.executable, *args]
        return [sys.executable, "-m", "akaribot.cli.main", *args]

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
        """经 ``akaribot config list --json`` 取表清单。"""
        argv = self.cli_argv("config", "list", "--json")
        completed = self._run(argv)
        if completed.returncode != 0:
            raise ConfigSourceError(f"`{' '.join(argv)}` 退出码 {completed.returncode}：{self._tail(completed.stderr)}")
        return normalize_tables(self._parse_json(completed.stdout, "config list --json"))

    def _tables_from_directory(self) -> list[str]:
        """退回实例目录枚举：``<实例>/config`` 下的 ``*.toml`` 文件名即表名。"""
        root = self._instance_root()
        if root is None:
            raise ConfigSourceError(f"{self.root} 不是 AkariBot 实例（未找到 akaribot.toml）")
        base = root / "config"
        if not base.is_dir():
            raise ConfigSourceError(f"{base} 不存在，无法枚举配置表")
        return normalize_tables(sorted(path.stem for path in base.rglob("*.toml")))

    def _core_json(self, *args: str, label: str) -> Any:
        """调用 core 配置入口并解析 JSON 输出。"""
        instance = self._instance()
        try:
            completed = instance.run_core_capture("config", *args, "--json")
        except Exception as error:  # noqa: BLE001 - 对端实现未知，统一转成可展示的错误
            raise ConfigSourceError(f"调用 core 的 `{label}` 失败：{type(error).__name__}: {error}") from error
        if completed.returncode != 0:
            raise ConfigSourceError(f"`{label}` 退出码 {completed.returncode}：{self._tail(completed.stderr)}")
        return self._parse_json(completed.stdout, label)

    def _instance_root(self) -> Path | None:
        """定位实例根：优先环境变量，其次自当前目录向上查找 ``akaribot.toml``。"""
        try:
            from akaribot.cli.instance import find_instance_root
        except ImportError:
            return None
        try:
            return find_instance_root(self.root)
        except Exception:  # noqa: BLE001 - 定位失败按「没有实例」处理，由调用方给出提示
            return None

    def _instance(self) -> Any:
        """构造实例对象；模块缺失或实例不存在时给出可读原因。"""
        if self._instance_cache is not None:
            return self._instance_cache
        if self._instance_factory is not None:
            self._instance_cache = self._instance_factory()
            return self._instance_cache
        try:
            from akaribot.cli.instance import Instance
        except ImportError as error:
            raise ConfigSourceError("尚未提供 akaribot.cli.instance，无法调用 core 配置入口") from error
        root = self._instance_root()
        if root is None:
            raise ConfigSourceError(
                f"{self.root} 不是 AkariBot 实例（未找到 akaribot.toml）；"
                "先运行 `akaribot init`，或用 AKARI_INSTANCE_DIR 指定实例根"
            )
        try:
            self._instance_cache = Instance(root)
        except Exception as error:  # noqa: BLE001 - 实例构造失败同样只作为降级原因上报
            raise ConfigSourceError(f"构造 Instance 失败：{type(error).__name__}: {error}") from error
        return self._instance_cache

    def _run(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        """执行子进程并把常见失败转成 :class:`ConfigSourceError`。"""
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
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
            raise ConfigSourceError(f"找不到可执行文件：{argv[0]}（{error}）") from error
        except subprocess.TimeoutExpired as error:
            raise ConfigSourceError(f"`{' '.join(argv)}` 超过 {self.timeout:.0f} 秒未返回") from error
        except OSError as error:
            raise ConfigSourceError(f"`{' '.join(argv)}` 执行失败：{error}") from error

    def _parse_json(self, stdout: str, label: str) -> Any:
        """解析子进程 JSON 输出。"""
        text = (stdout or "").strip()
        if not text:
            raise ConfigSourceError(f"`{label}` 没有输出")
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ConfigSourceError(f"`{label}` 输出不是 JSON：{error}") from error

    def _tail(self, text: str | None, limit: int = 400) -> str:
        """截取子进程输出的尾部，供状态栏展示。"""
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
    """由字段重建一份可解析的 TOML 文本，供找不到配置文件时展示。

    重建会丢掉原有注释与书写顺序，故只在文件缺失时使用；保存仍逐键经 ``config set``。
    同一段只输出一次表头：密钥段可能夹在普通段中间，重复表头会让 TOML 解析失败。

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
    """把值渲染为 TOML 字面量，用于重建文本；嵌套表渲染为行内表。"""
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
    """从 ``_compat`` 取可选控件，未收口时返回 ``None`` 由调用方降级。

    理由：``TextArea`` / ``Switch`` 尚未在 ``_compat`` 再导出，而页面不得直接 import textual，
    故按名字探测；``_compat`` 一旦导出，本页无需改动即自动切换到原生控件。
    """
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
        yield compat.Static(compat.plain_text("（点击按钮或按 s 保存前先切换；写入 true / false）"), markup=False)

    @property
    def value(self) -> bool:
        """返回当前值。"""
        return self._value

    def label_text(self) -> str:
        """返回按钮文字，开与关用中文并配符号。"""
        return "✓ 开" if self._value else "✗ 关"

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
        """取内部按钮；未挂载时返回 ``None``。"""
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
            f"待填写：模板占位符 {_short(field.edit_value, 40)}，请替换为真实值" if field.is_placeholder else ""
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
        """构造本行的输入控件：布尔用开关，其余用输入框（密钥遮罩）。"""
        if self.field.kind == KIND_BOOL:
            switch = _optional_widget("Switch")
            if switch is not None:
                return switch(value=bool(self.field.value), classes="field-control")
            return BoolToggle(bool(self.field.value))
        placeholder = "逗号分隔，例如：a, b, c" if self.field.kind == KIND_LIST else ""
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
        """返回控件里的当前编辑文本。"""
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
        """切换布尔控件；非布尔行不动作。"""
        control = self.control()
        if isinstance(control, BoolToggle):
            control.toggle()

    def focus_control(self) -> None:
        """把焦点交给本行控件。"""
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
        """取行内的错误提示控件。"""
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
            yield compat.Button("追加行", id="raw-add")
            yield compat.Button("删除末行", id="raw-del")
            yield compat.Static(
                compat.plain_text("逐行编辑（_compat 尚未导出 TextArea）：每行一个输入框，保存前做 TOML 校验"),
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
        """取原生 ``TextArea``；降级实现下返回 ``None``。"""
        if self._textarea_cls is None:
            return None
        try:
            return self.query_one("#raw-textarea")
        except Exception:  # noqa: BLE001 - 未挂载时按无 TextArea 处理
            return None

    async def _remount_lines(self) -> None:
        """重建逐行输入框。"""
        await self.remove_children(".raw-line")
        await self.mount(
            *[compat.Input(line, id=f"raw-line-{index}", classes="raw-line") for index, line in enumerate(self._lines)]
        )


# endregion


# region 页面


class ConfigPage(compat.Vertical):
    """Config 页控件。

    :param source: 数据源，缺省为 :class:`SubprocessConfigSource`。
    :param cache_ttl: 表清单缓存有效期秒数；保存与重读会立即失效。
    """

    DEFAULT_CSS = """
    ConfigPage {
        layout: vertical;
        height: 1fr;
    }
    ConfigPage #config-toolbar {
        height: 3;
        padding: 0 0 0 1;
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

    BINDINGS = compat.bindings(
        ("s", "save", "保存"),
        ("f", "mode_form", "表单模式"),
        ("t", "mode_raw", "原始文本"),
        ("ctrl+r", "reload", "重读"),
        ("escape", "focus_tables", "表清单"),
    )

    def __init__(
        self,
        source: ConfigSource | None = None,
        *,
        cache_ttl: float = 30.0,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.source: ConfigSource = source if source is not None else SubprocessConfigSource()
        self.cache_ttl = cache_ttl
        self.last_error: str = ""
        self.last_result: str = "就绪"
        self._tables: tuple[str, ...] = ()
        self._fields: tuple[ConfigField, ...] = ()
        self._schemas: dict[str, tuple[ConfigField, ...]] = {}
        self._loaded_at: float = 0.0
        self._selected: str | None = None
        self._raw_table: str | None = None
        self._mode: str = MODE_FORM
        self._saved: tuple[str, ...] = ()
        self._skipped: tuple[str, ...] = ()
        self._rendered_tables: tuple[str, ...] = ()
        self._caption_rendered: str = ""
        self._status_rendered: str = "就绪"

    def compose(self) -> compat.ComposeResult:
        """装配页面控件树：工具条、表清单、表单区、文本区、状态栏。"""
        with compat.Horizontal(id="config-toolbar"):
            yield compat.Button("表单模式", id="mode-form", variant="primary")
            yield compat.Button("原始文本", id="mode-raw")
            yield compat.Static(compat.plain_text("尚未读取配置表"), id="config-caption", markup=False)
            yield compat.Button("保存", id="save", variant="success")
            yield compat.Button("重读", id="reload")
        with compat.Horizontal(id="config-body"):
            yield compat.ListView(id="table-list")
            with compat.VerticalScroll(id="form-pane"):
                yield compat.Static(compat.plain_text("正在读取配置表…"), id="form-hint", markup=False)
            with compat.VerticalScroll(id="raw-pane", classes="hidden"):
                yield RawTextEditor("", id="raw-editor")
        yield compat.Static(compat.plain_text("就绪"), id="config-status", markup=False)

    def on_mount(self) -> None:
        """挂载后读取一次表清单，并把焦点交给表清单使键位立即可用。"""
        compat.set_text_selection(self, False)
        self.query_one("#table-list", compat.ListView).focus()
        self.refresh_tables()

    # region 状态读取（供测试与 App 使用）

    @property
    def tables(self) -> tuple[str, ...]:
        """返回缓存中的表清单，不触发子进程。"""
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
        """返回最近一次保存真正写入的「表.键=值」列表。"""
        return self._saved

    @property
    def skipped_notes(self) -> tuple[str, ...]:
        """返回最近一次保存中跳过项的说明。"""
        return self._skipped

    def cache_age(self) -> float:
        """返回表清单缓存自上次读取以来的秒数；从未读取时为无穷大。"""
        if not self._loaded_at:
            return float("inf")
        return time.monotonic() - self._loaded_at

    def field_rows(self) -> tuple[FieldRow, ...]:
        """返回表单区里的全部字段行（按渲染顺序）。"""
        return tuple(self.query(FieldRow))

    def row_for(self, key: str) -> FieldRow | None:
        """按键名取字段行，找不到时返回 ``None``。"""
        for row in self.field_rows():
            if row.field.key == key:
                return row
        return None

    def raw_editor(self) -> RawTextEditor:
        """返回原始文本编辑区。"""
        return self.query_one("#raw-editor", RawTextEditor)

    def table_row_texts(self) -> tuple[str, ...]:
        """返回最近一次渲染出的表清单行文本，供自动化断言核对宽度。"""
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
        return str(getattr(hint.renderable, "plain", hint.renderable))

    # endregion

    # region 读取与渲染

    def refresh_tables(self, *, force: bool = False) -> None:
        """读取配置表清单。

        :param force: 为 ``True`` 时忽略缓存；否则缓存有效期内只重绘不取数。
        """
        if not force and self._tables and self.cache_age() < self.cache_ttl:
            self._render_tables()
            self._set_status(f"使用 {self.cache_age():.1f} 秒前的缓存，共 {len(self._tables)} 张配置表")
            return
        self._set_status("正在读取配置表清单…")
        self.run_worker(self.reload_tables(), group="config-tables", exclusive=True)

    async def reload_tables(self) -> bool:
        """后台读取表清单并载入当前表，返回是否成功。"""
        try:
            tables = await asyncio.to_thread(self.source.list_tables)
        except Exception as error:  # noqa: BLE001 - 数据源任意异常都不应中断界面
            self._tables = ()
            self._loaded_at = time.monotonic()
            self.last_error = f"{type(error).__name__}: {error}"
            self._render_tables()
            await self._show_form_hint(f"读取配置表失败：{error}")
            self._set_status(f"读取失败：{error}")
            return False
        self._tables = tuple(normalize_tables(list(tables)))
        self._loaded_at = time.monotonic()
        self.last_error = ""
        self.last_result = f"已读取 {len(self._tables)} 张配置表"
        self._render_tables()
        target = self._selected if self._selected in self._tables else (self._tables[0] if self._tables else None)
        if target is None:
            await self._show_form_hint("实例里没有任何配置表：先运行 `akaribot init` 或安装模块")
            self._selected = None
            self._fields = ()
            self._sync_caption()
            self._set_status("没有可编辑的配置表")
            return True
        await self.select_table(target)
        return True

    async def select_table(self, table: str | None, *, force: bool = False) -> bool:
        """切换当前表：读取字段（有缓存）并重建右侧面板。

        :param table: 目标表名；``None`` 表示清空。
        :param force: 为 ``True`` 时忽略字段缓存。
        :return: 是否成功。
        """
        if table is None:
            self._selected = None
            self._fields = ()
            self._raw_table = None
            await self._rebuild_form(())
            self._sync_caption()
            self._set_status("没有可编辑的配置表")
            return False
        self._selected = table
        try:
            self._fields = await self._load_fields(table, force=force)
        except Exception as error:  # noqa: BLE001 - 取数失败只影响本页展示
            self._fields = ()
            self.last_error = f"{type(error).__name__}: {error}"
            self._sync_caption()
            await self._show_form_hint(f"读取表 {table} 的字段失败：{error}")
            self._set_status(f"读取表 {table} 失败：{error}")
            return False
        self.last_error = ""
        await self._rebuild_form(self._fields)
        if self._mode == MODE_RAW:
            await self.load_raw(table, force=force)
        self._sync_caption()
        self._set_status(f"已载入表 {table}：{len(self._fields)} 项")
        return True

    async def load_raw(self, table: str | None = None, *, force: bool = False) -> bool:
        """读取并展示某表的原始 TOML 文本。

        :param table: 目标表；缺省为当前表。
        :param force: 为 ``True`` 时即使已载入也重读。
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
            self._set_status(f"读取 {table} 的原始文本失败：{error}")
            return False
        await self.raw_editor().load_text(text)
        self._raw_table = table
        return True

    async def set_mode(self, mode: str) -> None:
        """切换编辑模式：表单模式与原始文本模式。

        :param mode: ``form`` 或 ``raw``；其它取值不动作。
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
        self._set_status(f"已切换到{'原始文本' if mode == MODE_RAW else '表单'}模式")

    async def _load_fields(self, table: str, *, force: bool = False) -> tuple[ConfigField, ...]:
        """读取字段，命中缓存时不取数。"""
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
        """作废缓存并重新读取表清单与当前表。"""
        self.invalidate_cache()
        self._raw_table = None
        return await self.reload_tables()

    async def _rebuild_form(self, fields: Sequence[ConfigField]) -> None:
        """按字段序列重建表单区。"""
        pane = self.query_one("#form-pane", compat.VerticalScroll)
        await pane.remove_children()
        headers = aligned_headers(fields)
        rows = [FieldRow(field, headers[field.key]) for field in fields]
        if rows:
            await pane.mount(*rows)
            return
        await pane.mount(
            compat.Static(
                compat.plain_text("该表没有配置项" if self._selected else "未选中配置表"), id="form-hint", markup=False
            )
        )

    async def _show_form_hint(self, text: str) -> None:
        """在表单区显示一条提示，替代字段列表。"""
        pane = self.query_one("#form-pane", compat.VerticalScroll)
        await pane.remove_children()
        await pane.mount(compat.Static(compat.plain_text(text), id="form-hint", markup=False))

    def _render_tables(self) -> None:
        """按缓存中的表清单重绘左侧列表与摘要栏。"""
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
        """返回表清单可用内容宽度：外框宽减去边框与左右内边距。"""
        try:
            outer = compat.widget_cells(list_view)[0]
        except Exception:  # noqa: BLE001 - 未挂载时按保守宽度排版
            return 22
        return max(outer - 4, 8)

    def _index_for(self, table: str | None) -> int:
        """定位要高亮的表；找不到时回到首项。"""
        if table is not None and table in self._tables:
            return self._tables.index(table)
        return 0

    def _sync_caption(self) -> None:
        """更新摘要栏：表名、项数、密钥与占位符数量、当前模式。"""
        if self._selected is None:
            text = f"共 {len(self._tables)} 张配置表，未选中任何表"
        else:
            secrets = sum(1 for field in self._fields if field.secret)
            placeholders = sum(1 for field in self._fields if field.is_placeholder)
            mode_label = "表单" if self._mode == MODE_FORM else "原始文本"
            text = (
                f"表 {self._selected}：共 {len(self._fields)} 项，密钥 {secrets} 项，"
                f"待填写 {placeholders} 项；模式：{mode_label}"
            )
        self._caption_rendered = text
        self.query_one("#config-caption", compat.Static).update(compat.plain_text(text))

    def _set_status(self, text: str) -> None:
        """更新状态栏。"""
        self.last_result = text
        self._status_rendered = text
        self.query_one("#config-status", compat.Static).update(compat.plain_text(text))

    def on_resize(self, event: compat.events.Resize) -> None:
        """终端尺寸变化时按缓存重排表清单，不重新取数。"""
        if self._tables:
            self._render_tables()

    # endregion

    # region 保存

    async def save(self) -> bool:
        """保存当前表，返回是否全部写入成功。

        表单模式逐项校验类型后只写入被改动的键；原始文本模式先用 ``tomlkit.parse()``
        校验全文，解析失败直接拒绝保存并给出出错行，不发出任何写入调用。
        """
        if self._selected is None:
            self._set_status("没有选中的配置表，无法保存")
            return False
        if not self._fields:
            self._set_status("尚未读到字段，无法保存；先按 ctrl+r 重读")
            return False
        self._skipped = ()
        if self._mode == MODE_RAW:
            plan = await self._plan_raw_save()
            if plan is None:
                return False
        else:
            plan, errors = self._plan_form_save()
            if errors:
                self.last_error = "；".join(errors)
                self._set_status(f"校验未通过，未写入任何配置：{self.last_error}")
                compat.notify(self.app, self.last_error, severity="error", title="配置未保存")
                return False
        if not plan:
            self.last_result = "没有需要写入的改动"
            self._set_status(f"表 {self._selected} 没有需要写入的改动；{_HELP_HINT}")
            return True
        return await self._apply(plan)

    def _plan_form_save(self) -> tuple[list[RawEntry], list[str]]:
        """收集表单里被改动的字段；校验失败的行在行内标出。

        未改动的行既不校验也不写入：值原样来自 schema，重新写回没有意义，还可能把
        未知结构（嵌套表等）交给 ``config set``。
        """
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
                errors.append(f"{field.key}：{message}")
                continue
            plan.append(RawEntry(section=field.section, key=field.key, text=text))
        return plan, errors

    async def _plan_raw_save(self) -> list[RawEntry] | None:
        """校验原始文本并给出改动条目；解析失败时返回 ``None`` 且不写任何键。"""
        parsed = parse_toml_text(self.raw_editor().text)
        if not parsed.ok:
            self.last_error = parsed.message
            self._set_status(f"拒绝保存：{parsed.message}")
            compat.notify(self.app, parsed.message, severity="error", title="TOML 校验失败")
            return None
        assert self._selected is not None
        changes, skipped, unchanged = diff_document(parsed.document, self._fields, self._selected)
        self._skipped = tuple(skipped)
        self.last_result = f"改动 {len(changes)} 项，未改动 {len(unchanged)} 项"
        return changes

    async def _apply(self, plan: Sequence[RawEntry]) -> bool:
        """逐项经数据源写入，成功后重读当前表。"""
        assert self._selected is not None
        self._set_status(f"正在写入 {len(plan)} 项…")
        written: list[str] = []
        failures: list[str] = []
        for entry in plan:
            try:
                result = await asyncio.to_thread(self.source.set_value, entry.section, entry.key, entry.text)
            except Exception as error:  # noqa: BLE001 - 数据源任意异常都转成失败项展示
                result = SetResult(False, f"写入 {entry.label} 失败", f"{type(error).__name__}: {error}")
            if result.ok:
                written.append(entry.label)
                continue
            failures.append(f"{entry.label}：{result.detail or result.message}")
        self._saved = tuple(written)
        if failures:
            self.last_error = "；".join(failures)
            self._set_status(f"写入完成：成功 {len(written)} 项，失败 {len(failures)} 项——{failures[0]}")
            compat.notify(self.app, failures[0], severity="error", title="配置写入失败")
            return False
        self.invalidate_cache(self._selected)
        await self.select_table(self._selected, force=True)
        self._set_status(f"已写入 {len(written)} 项：{'、'.join(written)}；{_HELP_HINT}")
        compat.notify(self.app, f"已写入 {len(written)} 项配置", severity="information", title=self._selected)
        return True

    # endregion

    # region 交互

    @compat.on(compat.ListView.Highlighted, "#table-list")
    def _on_table_highlighted(self, event: compat.ListView.Highlighted) -> None:
        """表清单高亮项变化时切换当前表。"""
        index = compat.highlighted_index(self.query_one("#table-list", compat.ListView))
        if index is None or index >= len(self._tables):
            return
        table = self._tables[index]
        if table != self._selected:
            self.run_worker(self.select_table(table), group="config-select", exclusive=True)

    @compat.on(compat.Button.Pressed)
    def _on_button_pressed(self, event: compat.Button.Pressed) -> None:
        """按钮回调：保存、重读、模式切换、文本区增删行。"""
        button_id = event.button.id
        if button_id == "save":
            self.action_save()
        elif button_id == "reload":
            self.action_reload()
        elif button_id == "mode-form":
            self.action_mode_form()
        elif button_id == "mode-raw":
            self.action_mode_raw()
        elif button_id == "raw-add":
            self.run_worker(self.raw_editor().append_line(), group="config-raw", exclusive=True)
        elif button_id == "raw-del":
            self.run_worker(self.raw_editor().remove_last_line(), group="config-raw", exclusive=True)

    def action_save(self) -> None:
        """键位动作：保存当前表。"""
        self.run_worker(self.save(), group="config-save", exclusive=True)

    def action_reload(self) -> None:
        """键位动作：作废缓存并重读。"""
        self.run_worker(self.reload(), group="config-reload", exclusive=True)

    def action_mode_form(self) -> None:
        """键位动作：切到表单模式。"""
        self.run_worker(self.set_mode(MODE_FORM), group="config-mode", exclusive=True)

    def action_mode_raw(self) -> None:
        """键位动作：切到原始文本模式。"""
        self.run_worker(self.set_mode(MODE_RAW), group="config-mode", exclusive=True)

    def action_focus_tables(self) -> None:
        """键位动作：把焦点交回表清单。"""
        self.query_one("#table-list", compat.ListView).focus()

    async def wait_for_idle(self) -> None:
        """等待本页发起的后台任务结束，供自动化断言与脚本使用。"""
        await self.app.workers.wait_for_complete()

    # endregion


# endregion
