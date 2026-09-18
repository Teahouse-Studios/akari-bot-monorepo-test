"""渲染校验：用一组占位值渲染 templates/ 下的全部模板，并校验产物语法。

模板以 ``.j2`` 后缀存放，ruff 等工具默认不会读取，因此需要本脚本保证模板与渲染契约
同步：任何一处占位符改名、括号写错或语法错误都会在此暴露。

用法：
    uv run python tools/render_templates.py
"""

from __future__ import annotations

import ast
import html
import json
import re
import sys
import tomllib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = PROJECT_ROOT / "templates"

# 占位值。模块名取纯小写与下划线，与模板 README 所述的限制一致。
SAMPLE_CONTEXT = {
    "module_name": "sample",
    "module_class": "Sample",
    "module_desc": "渲染校验用的示例模块。",
    "author": "AkariBot",
    "license": "AGPL-3.0",
}

# 占位符形态：[@name@]。两处替换都要做——路径占位符在复制目录时替换，
# 文本占位符在渲染内容时替换。
PLACEHOLDER_PATTERN = re.compile(r"\[@([a-z_]+)@\]")

VALIDATORS = {
    ".py": ("python", ast.parse),
    ".json": ("json", json.loads),
    ".toml": ("toml", tomllib.loads),
}


def fill_placeholders(text: str) -> str:
    """还原模板转义并替换占位符，未声明的名称原样保留。

    模板中的命令语法标记写成 HTML 实体（``&#123;&#123;I18N:...&#125;&#125;``），
    以免被 Jinja2 当作变量表达式；此处统一还原为 ``{{I18N:...}}``。

    :param text: 模板路径或渲染后的文本。
    :return: 还原并替换后的文本。
    """
    return PLACEHOLDER_PATTERN.sub(
        lambda match: SAMPLE_CONTEXT.get(match.group(1), match.group(0)),
        html.unescape(text),
    )


def output_name(name: str) -> str:
    """模板路径去掉 ``.j2`` 后缀，并把路径占位符替换为样例值。

    :param name: 相对 templates/ 的模板路径。
    :return: 产物路径。
    """
    return fill_placeholders(name[: -len(".j2")])


def template_names() -> list[str]:
    """列出 templates/ 下的全部模板，返回相对 templates/ 的 POSIX 路径。"""
    return sorted(path.relative_to(TEMPLATE_ROOT).as_posix() for path in TEMPLATE_ROOT.rglob("*.j2"))


def describe_error(name: str, error: Exception) -> str:
    """把校验异常转成一行可读说明。

    :param name: 模板路径。
    :param error: 捕获到的异常。
    :return: 说明文本。
    """
    detail = getattr(error, "msg", None) or str(error)
    line = getattr(error, "lineno", None)
    if line:
        return f"{name}: 第 {line} 行：{detail}"
    return f"{name}: {detail}"


def validate_render(name: str, rendered: str, label: str, check) -> None:
    """校验单个渲染产物。

    :param name: 模板路径，用于报错定位。
    :param rendered: 渲染并还原后的文本。
    :param label: 产物类型的展示名。
    :param check: 校验函数，语法错误时抛异常。
    :raises AssertionError: 产物缺失末尾换行，与仓库的 ruff format 结果不一致。
    """
    check(rendered)
    if not rendered.endswith("\n"):
        raise AssertionError("产物缺少末尾换行，检查 Environment 是否设置了 keep_trailing_newline")


def main() -> int:
    """入口。返回进程退出码，0 表示全部模板的渲染产物语法正确。"""
    if not TEMPLATE_ROOT.is_dir():
        print(f"未找到模板目录：{TEMPLATE_ROOT}", file=sys.stderr)
        return 1

    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATE_ROOT)),
        undefined=StrictUndefined,
        # 默认会吞掉模板末尾的换行，产物将不符合本项目的 ruff format 结果。
        keep_trailing_newline=True,
    )

    names = template_names()
    if not names:
        print("templates/ 下没有任何 .j2 模板。", file=sys.stderr)
        return 1

    failures: list[str] = []
    skipped: list[str] = []
    for name in names:
        target = output_name(name)
        suffix = Path(target).suffix
        validator = VALIDATORS.get(suffix)
        if validator is None:
            skipped.append(f"{name}（无针对 {suffix or '无后缀'} 的校验器）")
            continue
        label, check = validator
        try:
            rendered = fill_placeholders(environment.get_template(name).render())
            validate_render(name, rendered, label, check)
        except Exception as error:  # noqa: BLE001
            failures.append(describe_error(name, error))
            continue
        print(f"OK    {name} -> {target}（{label}）")

    for item in skipped:
        print(f"SKIP  {item}")
    for failure in failures:
        print(f"FAIL  {failure}", file=sys.stderr)
    print(
        f"\n模板 {len(names)} 个：通过 {len(names) - len(failures) - len(skipped)}，跳过 {len(skipped)}，失败 {len(failures)}。"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
