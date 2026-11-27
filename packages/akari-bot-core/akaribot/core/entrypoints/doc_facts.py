"""包事实采集。

文档站点在构建期渲染配置字段与适配器能力。解析只读源码，不导入被扫描的包，以免触发配置读取与
其它导入期副作用。
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

_COMMENT_PREFIX = "config.comments."
_CONFIG_FILE = "config.py"
_FEATURES_FILE = "features.py"
_FEATURES_NAME = "features"
_SECRET_SUFFIX = "_secret"
_ADAPTER_DIR = "adapters"
# 适配器以 on_bot_config 声明平台表，表名规则与模块表一致，两者都从装饰器的首个位置参数取基础名。
_CONFIG_DECORATORS = ("on_module_config", "on_bot_config")


def collect_package_facts(package_dir: Path, warnings: list[str]) -> dict[str, Any]:
    """采集配置表与适配器能力。

    :param package_dir: 包的导入目录，配置与能力文件位于该目录下。
    :param warnings: 采集过程中的失败说明，追加到该列表。
    :return: ``{"config": [...], "features": {...}}``，读取失败的项为空。能力项取值为布尔，来自
        运行时配置的项记在 ``features_dynamic``，该键仅在存在此类项时出现。
    """
    try:
        config = _collect_config(package_dir, warnings)
    except Exception:  # noqa: BLE001 - 单个包采集失败不得中断整个文档构建。
        warnings.append(f"{package_dir.name}: 采集配置表失败，已跳过。")
        config = []
    try:
        features, dynamic = _collect_features(package_dir, warnings)
    except Exception:  # noqa: BLE001 - 能力文件与配置表互不影响，失败时仅清空能力。
        warnings.append(f"{package_dir.name}: 采集适配器能力失败，已跳过。")
        features, dynamic = {}, []
    facts: dict[str, Any] = {"config": config, "features": features}
    if dynamic:
        # 这些能力的取值由配置在运行时决定，前端只渲染布尔项，来源信息必须与能力表分开存放。
        facts["features_dynamic"] = dynamic
    return facts


def _collect_config(package_dir: Path, warnings: list[str]) -> list[dict[str, Any]]:
    tree = _parse_module(package_dir / _CONFIG_FILE, package_dir, warnings)
    if tree is None:
        return []
    comments = _read_comments(package_dir, warnings)
    tables: list[dict[str, Any]] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        call = _config_decorator(node)
        if call is None:
            continue
        base = _decorator_base(call, node, package_dir, warnings)
        if base is None:
            continue
        secret = _decorator_secret(call)
        fields = _config_fields(node)
        if not fields:
            continue
        names = [field["name"] for field in fields]
        table = _match_table(names, comments, secret) or _fallback_table(package_dir, base, secret)
        table_secret = secret or table.endswith(_SECRET_SUFFIX)
        for field in fields:
            field["secret"] = table_secret
            field["comment"] = comments.get(table, {}).get(field["name"], "")
        tables.append(
            {
                "table": table,
                "file": f"config/{_public_table(table)}.toml",
                "secret": table_secret,
                "fields": fields,
            }
        )
    return sorted(tables, key=lambda item: item["table"])


def _parse_module(path: Path, package_dir: Path, warnings: list[str]) -> ast.Module | None:
    if not path.is_file():
        return None
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        warnings.append(f"{package_dir.name}: 解析 {path.name} 失败（{exc}），已跳过。")
        return None


def _config_decorator(node: ast.ClassDef) -> ast.Call | None:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and _symbol_name(decorator.func) in _CONFIG_DECORATORS:
            return decorator
    return None


def _symbol_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _decorator_base(call: ast.Call, node: ast.ClassDef, package_dir: Path, warnings: list[str]) -> str | None:
    if call.args:
        first = call.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str) and first.value:
            return first.value
    warnings.append(f"{package_dir.name}: 配置类 {node.name} 的表名不是字符串字面量，已跳过。")
    return None


def _decorator_secret(call: ast.Call) -> bool:
    for keyword in call.keywords:
        if keyword.arg == "secret" and isinstance(keyword.value, ast.Constant):
            return keyword.value.value is True
    return False


def _config_fields(node: ast.ClassDef) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for item in node.body:
        field = _config_field(item)
        if field is not None:
            fields.append(field)
    return fields


def _config_field(node: ast.stmt) -> dict[str, Any] | None:
    if isinstance(node, ast.AnnAssign):
        target, annotation, value = node.target, node.annotation, node.value
    elif isinstance(node, ast.Assign) and len(node.targets) == 1:
        target, annotation, value = node.targets[0], None, node.value
    else:
        return None
    if not isinstance(target, ast.Name) or target.id.startswith("_"):
        return None
    default, required = _field_default(value)
    return {
        "name": target.id,
        "type": ast.unparse(annotation) if annotation is not None else "",
        "default": default,
        "secret": False,
        "comment": "",
        "required": required,
    }


def _field_default(value: ast.expr | None) -> tuple[Any, bool]:
    if value is None:
        return None, True
    try:
        default = ast.literal_eval(value)
    except (ValueError, TypeError, SyntaxError, RecursionError, MemoryError):
        # 名称与调用的结果在运行时才确定，展示源码文本比留空更有参考价值。
        return ast.unparse(value), False
    try:
        json.dumps(default)
    except (TypeError, ValueError):
        return ast.unparse(value), False
    return default, False


def _read_comments(package_dir: Path, warnings: list[str]) -> dict[str, dict[str, str]]:
    path = package_dir / "locales" / "zh_cn.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        warnings.append(f"{package_dir.name}: 解析 locales/zh_cn.json 失败（{exc}），配置说明留空。")
        return {}
    if not isinstance(payload, dict):
        warnings.append(f"{package_dir.name}: locales/zh_cn.json 不是对象，配置说明留空。")
        return {}
    comments: dict[str, dict[str, str]] = {}
    # locale 使用扁平点号键，表名与字段名由键路径切分，值不是字符串的条目视为未提供说明。
    for key, value in payload.items():
        if not isinstance(key, str) or not key.startswith(_COMMENT_PREFIX) or not isinstance(value, str):
            continue
        parts = key[len(_COMMENT_PREFIX) :].split(".")
        if len(parts) == 2:
            comments.setdefault(parts[0], {})[parts[1]] = value
    return comments


def _match_table(names: list[str], comments: dict[str, dict[str, str]], secret: bool) -> str:
    # 字段集合全部命中才认定该表，并按敏感标记区分同名表，公开表与敏感表的字段不会混用。
    wanted = set(names)
    tables = sorted(
        table
        for table, fields in comments.items()
        if wanted <= set(fields) and table.endswith(_SECRET_SUFFIX) == secret
    )
    return tables[0] if tables else ""


def _fallback_table(package_dir: Path, base: str, secret: bool) -> str:
    # 注释缺失时按目录约定推断表名，适配器目录下为平台表，其余为模块表。
    prefix = "bot" if package_dir.parent.name == _ADAPTER_DIR else "module"
    table = f"{prefix}_{base}"
    return f"{table}{_SECRET_SUFFIX}" if secret else table


def _public_table(table: str) -> str:
    return table[: -len(_SECRET_SUFFIX)] if table.endswith(_SECRET_SUFFIX) else table


def _collect_features(package_dir: Path, warnings: list[str]) -> tuple[dict[str, bool], list[str]]:
    tree = _parse_module(package_dir / _FEATURES_FILE, package_dir, warnings)
    if tree is None:
        return {}, []
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id != _FEATURES_NAME:
            continue
        value = node.value
        if isinstance(value, ast.Call) and _symbol_name(value.func).endswith("Features"):
            return _features_from_call(value)
    return {}, []


def _features_from_call(call: ast.Call) -> tuple[dict[str, bool], list[str]]:
    features: dict[str, bool] = {}
    dynamic: list[str] = []
    for keyword in call.keywords:
        if keyword.arg is None:
            continue
        if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, bool):
            features[keyword.arg] = keyword.value.value
        else:
            # 取值来自配置的开关由运行时决定，与能力表分开记录，避免非布尔值混入能力。
            dynamic.append(keyword.arg)
    return features, dynamic
