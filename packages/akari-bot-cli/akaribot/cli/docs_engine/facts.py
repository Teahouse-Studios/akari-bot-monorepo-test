"""构建期读取 Typer 命令树，供文档站点渲染命令用法与选项。"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

MAX_PATH_DEPTH = 2


def collect_cli_commands() -> dict[str, dict[str, Any]]:
    """返回以命令路径为键的用法、摘要、参数与选项清单。

    采集在构建期执行，导入或遍历失败时返回空映射，站点其余内容照常生成。
    """
    try:
        import typer.main

        from akaribot.cli.main import app

        root = typer.main.get_command(app)
        return _walk(root, ())
    except Exception:
        return {}


def _walk(command: Any, path: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    children = getattr(command, "commands", None)
    is_group = isinstance(children, Mapping) and bool(children)
    if is_group and len(path) < MAX_PATH_DEPTH:
        entries: dict[str, dict[str, Any]] = {}
        for name, child in children.items():
            if getattr(child, "hidden", False):
                continue
            entries.update(_walk(child, (*path, str(name))))
        return entries
    if not path:
        # 根命令不是分组时以自身名称作为路径，单命令应用同样能生成条目。
        name = str(getattr(command, "name", "") or "")
        if not name:
            return {}
        path = (name,)
    joined = " ".join(path)
    return {joined: _command_entry(command, joined)}


def _command_entry(command: Any, path: str) -> dict[str, Any]:
    params = tuple(getattr(command, "params", ()) or ())
    return {
        "usage": _usage(command, path),
        "summary": _summary(command),
        "arguments": [_argument_entry(param) for param in params if _is_argument(param)],
        "options": [_option_entry(param) for param in params if _is_documented_option(param)],
    }


def _is_option(param: Any) -> bool:
    return bool(getattr(param, "opts", ())) and hasattr(param, "is_flag")


def _is_argument(param: Any) -> bool:
    return not _is_option(param) and hasattr(param, "name")


def _is_documented_option(param: Any) -> bool:
    names = getattr(param, "opts", ()) or ()
    return _is_option(param) and "--help" not in names


def _argument_entry(param: Any) -> dict[str, Any]:
    return {
        "name": str(getattr(param, "name", "") or ""),
        "required": bool(getattr(param, "required", False)),
    }


def _option_entry(param: Any) -> dict[str, Any]:
    return {
        "names": [str(name) for name in getattr(param, "opts", ()) or ()],
        "metavar": _metavar(param),
        "help": str(getattr(param, "help", "") or ""),
        "isFlag": bool(getattr(param, "is_flag", False)),
        "required": bool(getattr(param, "required", False)),
        "default": _default_text(getattr(param, "default", None)),
    }


def _metavar(param: Any) -> str:
    declared = getattr(param, "metavar", None)
    if isinstance(declared, str) and declared:
        return declared
    if getattr(param, "is_flag", False):
        return ""
    # click 8.2 起 make_metavar 必须传入上下文，这里改用类型名兜底，避免文档里显示占位符为空。
    kind = getattr(getattr(param, "type", None), "name", "")
    return str(kind).upper() if kind else ""


def _default_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _summary(command: Any) -> str:
    try:
        return str(command.get_short_help_str())
    except Exception:
        return ""


def _usage(command: Any, path: str) -> str:
    # 命令自带所属 click 的上下文类型，可避免依赖未在包内声明的 click。
    context_class = getattr(command, "context_class", None)
    if context_class is not None:
        try:
            rendered = str(context_class(command, info_name=path).get_usage())
            body = rendered.removeprefix("Usage: ").strip()
            return f"akaribot {body}" if body else f"akaribot {path}"
        except Exception:
            pass
    return f"akaribot {path}"
