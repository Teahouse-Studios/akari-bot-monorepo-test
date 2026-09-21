"""脚手架。

`akaribot new module <name>` 按问卷生成模块包：分发元数据、包清单、包内代码、locale、可选的
配置与数据库骨架、可选的测试，以及第三方作者用的发布工作流。问卷每一项都对应一个命令行选项，
`--non-interactive` 下只取选项值与默认值，全程不提问。

`akaribot new adapter <name>` 用同一套问卷与渲染机制生成平台适配器包：info / features / context /
bot 四个骨架文件，加可选的配置模板，对照 `packages/adapters/` 下既有适配器的文件构成。

模板取自仓库内的 `templates/module/` 与 `templates/adapter/`，渲染契约见 `templates/README.md`：
路径与正文中的 `[@name@]` 占位符在 Jinja2 渲染之后替换。
"""

from __future__ import annotations

import html
import json
import keyword
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import typer
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from akaribot.cli import i18n

app = typer.Typer(help="脚手架")


def apply_argv_locale() -> None:
    """让帮助文本也跟随 ``--lang``。

    选项帮助在命令树物化时即已固化，早于根回调解析 ``--lang``；故导入本模块时先从 ``sys.argv``
    取一次语言，未给出时不改动当前语言。
    """
    argv = sys.argv[1:]
    for index, item in enumerate(argv):
        if item == "--lang" and index + 1 < len(argv):
            i18n.set_locale(argv[index + 1])
            return
        if item.startswith("--lang="):
            i18n.set_locale(item.partition("=")[2])
            return


apply_argv_locale()

# 模板目录的定位顺序：显式参数、环境变量、当前目录向上的 templates/module、CLI 源码目录。
TEMPLATE_DIR_ENV = "AKARIBOT_TEMPLATE_DIR"
TEMPLATE_RELATIVE = ("templates", "module")
TEMPLATE_MARKER = "pyproject.toml.j2"

PLACEHOLDER_PATTERN = re.compile(r"\[@([a-z_]+)@\]")
MODULE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,47}$")
COMMAND_SEPARATOR = "::"
COMPONENT_CHOICES = ("command", "regex", "schedule", "hook", "event")
GIT_AUTHOR_FALLBACK = "AkariBot"
DEFAULT_LICENSE = "AGPL-3.0"
DEFAULT_COMMAND_DOC = "执行 {name} 的默认命令。"
DEFAULT_MESSAGE = "Hello World!"
MODULE_ADD_TIMEOUT = 120.0

# 问卷选项控制的模板文件：未启用时该文件不渲染，其独占目录也不会创建。
OPTIONAL_TEMPLATES: dict[str, str] = {
    "src/akaribot/modules/[@module_name@]/config.py.j2": "has_config",
    "src/akaribot/modules/[@module_name@]/database/__init__.py.j2": "has_database",
    "src/akaribot/modules/[@module_name@]/database/models.py.j2": "has_database",
    "src/akaribot/modules/[@module_name@]/migrations/__init__.py.j2": "has_database",
    "src/akaribot/modules/[@module_name@]/migrations/0001_initial.py.j2": "has_database",
    "src/akaribot/modules/[@module_name@]/assets/.gitkeep": "has_assets",
    "tests/test_[@module_name@].py.j2": "with_tests",
}

# 门面导入的书写顺序，按实际用到的组件裁剪，避免生成未使用的 import。
API_IMPORT_ORDER = ("Bot", "EventInfo", "HookPoint", "I18NContext", "IntervalTrigger", "module")

# 适配器模板的定位顺序与模块一致，只是相对目录与 README 里的取值含义不同。
ADAPTER_TEMPLATE_RELATIVE = ("templates", "adapter")
ADAPTER_TEMPLATE_MARKER = "pyproject.toml.j2"
# 模板维护说明与自检脚本留在仓库内，不随生成物分发。
ADAPTER_TEMPLATE_SKIP = frozenset({"TEMPLATE.md", "selfcheck.py"})

# 问卷选项控制的适配器模板文件：未启用时该文件不渲染。
ADAPTER_OPTIONAL_TEMPLATES: dict[str, str] = {
    "src/akaribot/adapters/[@module_name@]/config.py.j2": "has_config",
}

PLATFORM_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,47}$")
FEATURE_PATTERN = re.compile(r"^([a-z][a-z0-9_]*)(?:=(true|false))?$")
FIELD_PATTERN = re.compile(r"^([a-z][a-z0-9_]*)(?::([a-z]+))?(?:=(.*))?$", re.DOTALL)
FIELD_TYPES = ("str", "bool", "int", "float", "list")
# 默认能力集是聊天平台的常见能力；未实现的由作者在 features.py 中改回 False。
ADAPTER_DEFAULT_FEATURES = ("support_image", "support_mention", "support_quote", "support_delete")
CREDENTIAL_DEFAULT_SUFFIX = "_token"
TRUTHY_VALUES = ("true", "1", "yes")

FLAG_WITH_ARG_PATTERN = re.compile(r"\[-{1,2}([A-Za-z][A-Za-z0-9_-]*)\s+<([A-Za-z_][A-Za-z0-9_]*)>\]")
OPTIONAL_ARG_PATTERN = re.compile(r"\[\s*<([A-Za-z_][A-Za-z0-9_]*)>\s*\]")
REQUIRED_ARG_PATTERN = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")
FLAG_PATTERN = re.compile(r"\[-{0,2}([A-Za-z_][A-Za-z0-9_]*)\]")


@dataclass(frozen=True)
class CommandEntry:
    """一条命令的模板与文案。

    :param template: 命令模板，空串表示模块的默认命令。
    :param help_text: 写入 locale 的帮助文本。
    :param message_text: 回复文案，同时作为生成测试的断言值。
    """

    template: str
    help_text: str = ""
    message_text: str = ""

    @property
    def token(self) -> str:
        """命令在 locale 键与测试名中使用的短名，取自模板的第一个字面量词。"""
        for word in self.template.split():
            if word.startswith(("-", "<", "[")):
                continue
            cleaned = re.sub(r"[^a-z0-9_]", "", word.lower())
            if cleaned:
                return cleaned
        return "default"


@dataclass(frozen=True)
class CommandParam:
    """命令模板元素对应的函数参数。

    :param name: 参数名，连字符统一写作下划线。
    :param annotation: 类型标注。
    :param default: 默认值字面量。
    """

    name: str
    annotation: str
    default: str


@dataclass
class ModulePlan:
    """一次生成的问卷答案。

    :param name: 模块名，同时用作包名、entry point 名、locale 键前缀与表名前缀。
    :param desc: 模块的一句话说明。
    :param author: 作者名。
    :param license: 许可证标识。
    :param aliases: 命令别名。
    :param available_for: 支持平台，空表示全部平台。
    :param exclude_from: 排除平台。
    :param components: 勾选的组件。
    :param commands: 命令列表，仅在勾选 command 组件时非空。
    :param has_config: 是否生成配置骨架。
    :param has_database: 是否生成数据库骨架与迁移。
    :param has_assets: 是否生成包内只读资源目录。
    :param has_data_dir: 是否生成运行时数据目录示例。
    :param with_tests: 是否生成测试。
    """

    name: str
    desc: str
    author: str
    license: str
    aliases: list[str] = field(default_factory=list)
    available_for: list[str] = field(default_factory=list)
    exclude_from: list[str] = field(default_factory=list)
    components: list[str] = field(default_factory=list)
    commands: list[CommandEntry] = field(default_factory=list)
    has_config: bool = False
    has_database: bool = False
    has_assets: bool = False
    has_data_dir: bool = False
    with_tests: bool = False


@dataclass(frozen=True)
class ConfigField:
    """一条平台配置字段声明。

    :param name: 字段名，同时用作配置表的键与 locale 注释键的后半段。
    :param annotation: 类型标注，取值来自 ``FIELD_TYPES``。
    :param default: 默认值字面量，直接写进 config.py。
    """

    name: str
    annotation: str
    default: str


@dataclass
class AdapterPlan:
    """一次适配器生成的问卷答案。

    :param name: 适配器名，同时用作目录名、entry point 名、配置表后缀与 locale 键前缀。
    :param platform_name: 平台显示名，写入 info.py 并经 ``Info.resolve_client_name()`` 派生前缀。
    :param desc: 适配器的一句话说明。
    :param author: 作者名。
    :param license: 许可证标识。
    :param features: 平台能力开关，按录入顺序排列。
    :param has_config: 是否生成 config.py 与 manifest 的配置表声明。
    :param config_fields: 非机密的配置字段。
    :param credential_fields: 凭据字段，写入 secret 表与 manifest 的 credential_fields。
    """

    name: str
    platform_name: str
    desc: str
    author: str
    license: str
    features: list[tuple[str, bool]] = field(default_factory=list)
    has_config: bool = False
    config_fields: list[ConfigField] = field(default_factory=list)
    credential_fields: list[ConfigField] = field(default_factory=list)


def snake_case(name: str) -> str:
    """把模板元素名归一为合法参数名。

    :param name: 模板中的元素名。
    :return: 连字符替换为下划线后的名字。
    """
    return name.replace("-", "_")


def camel_case(name: str) -> str:
    """模块名转大驼峰，用于数据库模型类名。

    :param name: 模块名，形如 ``twenty_four``。
    :return: 大驼峰形式，形如 ``TwentyFour``。
    """
    return "".join(part.capitalize() for part in name.split("_") if part)


def python_literal(value: str) -> str:
    """把字符串写成双引号 Python 字面量。

    :param value: 原始文本。
    :return: 可直接嵌入源码的字面量。
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def command_params(template: str) -> list[CommandParam]:
    """由命令模板推导函数参数。

    四条规则与 parser 的解析约定一致：``<arg>`` 与 ``[<arg>]`` 是取值参数，``[flag]`` 与
    ``[-f]`` 是布尔开关，``[--foo <bar>]`` 按其子参数名取值。带冒号等无法作为参数名的元素
    不生成参数，需要时由作者自行用 ``Param`` 标注。

    :param template: 命令模板。
    :return: 按模板出现顺序排列的参数。
    """
    remaining = template
    found: list[tuple[int, CommandParam]] = []
    for pattern in (FLAG_WITH_ARG_PATTERN, OPTIONAL_ARG_PATTERN, REQUIRED_ARG_PATTERN):
        for match in pattern.finditer(remaining):
            name = match.group(2) if pattern is FLAG_WITH_ARG_PATTERN else match.group(1)
            found.append((match.start(), CommandParam(snake_case(name), "str | None", "None")))
        remaining = pattern.sub(" ", remaining)
    for match in FLAG_PATTERN.finditer(remaining):
        found.append((match.start(), CommandParam(snake_case(match.group(1)), "bool", "False")))
    return [param for _, param in sorted(found, key=lambda item: item[0])]


def command_example(template: str) -> str:
    """取命令模板的字面量部分，作为集成测试的输入。

    :param template: 命令模板。
    :return: 去掉 ``<arg>`` 与 ``[opt]`` 元素并归一空白后的文本。
    """
    stripped = template
    for pattern in (FLAG_WITH_ARG_PATTERN, OPTIONAL_ARG_PATTERN, FLAG_PATTERN, REQUIRED_ARG_PATTERN):
        stripped = pattern.sub(" ", stripped)
    stripped = re.sub(r"\[[^\]]*\]", " ", stripped)
    return " ".join(stripped.split())


def fill_placeholders(text: str, values: dict[str, str]) -> str:
    """还原 HTML 实体并替换占位符，与 ``tools/render_templates.py`` 同一套规则。

    :param text: 模板路径或渲染后的文本。
    :param values: 占位符取值。
    :return: 还原并替换后的文本。
    """
    return PLACEHOLDER_PATTERN.sub(lambda match: values.get(match.group(1), match.group(0)), html.unescape(text))


def placeholder_values(plan: ModulePlan) -> dict[str, str]:
    """占位符取值。名称与模板 README 的表格一致。

    :param plan: 问卷答案。
    :return: 占位符到取值的映射。
    """
    return {
        "module_name": plan.name,
        "module_class": camel_case(plan.name),
        "module_desc": plan.desc,
        "author": plan.author,
        "license": plan.license,
    }


def template_root(
    override: Path | None = None,
    relative: tuple[str, ...] = TEMPLATE_RELATIVE,
    marker: str = TEMPLATE_MARKER,
    missing_message: str | None = None,
) -> Path:
    """定位模板目录。

    顺序：命令行参数、``AKARIBOT_TEMPLATE_DIR``、当前目录逐级向上的相对目录、CLI 源码目录逐级
    向上。前两条服务于打包分发与本地调试，后两条服务于源码检出。

    :param override: 命令行给出的模板目录，未给出时为 ``None``。
    :param relative: 相对仓库根的模板目录，模块与适配器各一套。
    :param marker: 用于判定候选目录是否为目标模板目录的文件名。
    :param missing_message: 全部候选位置都不存在时的报错文本。
    :return: 模板目录的绝对路径。
    :raises typer.BadParameter: 全部候选位置都没有模板。
    """
    candidates: list[Path] = []
    if override is not None:
        candidates.append(override)
    if configured := os.environ.get(TEMPLATE_DIR_ENV):
        candidates.append(Path(configured))
    for base in (Path.cwd(), *Path.cwd().parents):
        candidates.append(base.joinpath(*relative))
    for base in Path(__file__).resolve().parents[:8]:
        candidates.append(base.joinpath(*relative))
    for candidate in candidates:
        if (candidate / marker).is_file():
            return candidate.resolve()
    if missing_message is not None:
        raise typer.BadParameter(missing_message)
    raise typer.BadParameter(f"未找到模块模板目录（应包含 {marker}），请用 --template-dir 或 {TEMPLATE_DIR_ENV} 指定。")


def split_entries(answer: str) -> list[str]:
    """切分逗号分隔的作答，去空白、去重并保持输入顺序。

    :param answer: 原始作答，中英文逗号均可。
    :return: 条目列表。
    """
    entries: list[str] = []
    for item in re.split(r"[,，]", answer):
        cleaned = item.strip()
        if cleaned and cleaned not in entries:
            entries.append(cleaned)
    return entries


def split_platforms(answer: str) -> tuple[list[str], list[str]]:
    """把一份平台作答拆成支持与排除两组。

    ``*`` 表示全部平台，等价于不限制；以 ``-`` 开头的条目进入排除组，如 ``-web``。

    :param answer: 原始作答。
    :return: 二元组——available_for 与 exclude_from。
    """
    available: list[str] = []
    excluded: list[str] = []
    for entry in split_entries(answer):
        if entry == "*":
            available.clear()
        elif entry.startswith("-"):
            excluded.append(entry[1:])
        else:
            available.append(entry)
    return available, excluded


def parse_command_option(value: str) -> CommandEntry:
    """解析一个 ``--command`` 取值。

    形态为 ``模板`` 或 ``模板 :: 说明``；模板留空表示模块的默认命令。

    :param value: 命令行取值。
    :return: 命令条目。
    """
    template, separator, help_text = value.partition(COMMAND_SEPARATOR)
    return CommandEntry(template=template.strip(), help_text=help_text.strip() if separator else "")


def validate_module_name(name: str) -> None:
    """校验模块名可用作包名、entry point 名与 TOML 裸键。

    :param name: 模块名。
    :raises typer.BadParameter: 名字不合规。
    """
    if not MODULE_NAME_PATTERN.match(name):
        raise typer.BadParameter("模块名须为小写字母开头的 [a-z0-9_]+，长度不超过 48，且不得含连字符。")
    if keyword.iskeyword(name):
        raise typer.BadParameter(f"{name} 是 Python 关键字，不能用作模块名。")


def validate_components(components: list[str]) -> list[str]:
    """校验并去重组件勾选。

    :param components: 原始勾选。
    :return: 去重后的组件列表。
    :raises typer.BadParameter: 出现未知组件名。
    """
    unknown = [item for item in components if item not in COMPONENT_CHOICES]
    if unknown:
        raise typer.BadParameter(f"未知组件：{', '.join(unknown)}；可选：{', '.join(COMPONENT_CHOICES)}。")
    return list(dict.fromkeys(components))


def prompt_text(value: str | None, question: str, default: str, non_interactive: bool) -> str:
    """取一个文本答案：选项优先，交互模式提问，非交互模式取默认值。

    :param value: 命令行给出的取值。
    :param question: 交互提问文本。
    :param default: 默认值。
    :param non_interactive: 是否为非交互模式。
    :return: 最终取值。
    """
    if value is not None:
        return value
    if non_interactive:
        return default
    return typer.prompt(question, default=default)


def prompt_flag(value: bool | None, question: str, default: bool, non_interactive: bool) -> bool:
    """取一个布尔答案，取值顺序同 :func:`prompt_text`。

    :param value: 命令行给出的取值。
    :param question: 交互提问文本。
    :param default: 默认值。
    :param non_interactive: 是否为非交互模式。
    :return: 最终取值。
    """
    if value is not None:
        return value
    if non_interactive:
        return default
    return typer.confirm(question, default=default)


def prompt_list(values: list[str], question: str, default: list[str], non_interactive: bool) -> list[str]:
    """取一组可重复选项的答案，取值顺序同 :func:`prompt_text`。

    :param values: 命令行给出的取值。
    :param question: 交互提问文本。
    :param default: 默认值。
    :param non_interactive: 是否为非交互模式。
    :return: 最终取值。
    """
    if values:
        return list(values)
    if non_interactive:
        return list(default)
    return split_entries(typer.prompt(question, default=", ".join(default)))


def ask_commands(module_name: str) -> list[CommandEntry]:
    """逐条录入命令，直到作者表示不再添加。

    :param module_name: 模块名，用于生成默认说明。
    :return: 命令条目列表，可能为空。
    """
    entries: list[CommandEntry] = []
    while typer.confirm("是否添加一条命令？", default=not entries):
        template = typer.prompt("命令模板（如 echo <word>；留空生成默认命令）", default="").strip()
        default_help = command_doc(module_name, template)
        help_text = typer.prompt("命令说明", default=default_help).strip()
        entries.append(CommandEntry(template=template, help_text=help_text))
    return entries


def command_doc(module_name: str, template: str) -> str:
    """命令的默认说明文本。

    :param module_name: 模块名。
    :param template: 命令模板，空串表示默认命令。
    :return: 帮助文本。
    """
    if not template:
        return DEFAULT_COMMAND_DOC.format(name=module_name)
    return f"执行 ~{module_name} {template.split()[0]} 命令。"


def build_commands(module_name: str, entries: list[CommandEntry]) -> list[CommandEntry]:
    """补齐命令的说明与回复文案。

    :param module_name: 模块名。
    :param entries: 录入的命令条目。
    :return: 补齐后的命令条目。
    """
    built: list[CommandEntry] = []
    for entry in entries:
        token = entry.token
        help_text = entry.help_text or command_doc(module_name, entry.template)
        message_text = entry.message_text or (DEFAULT_MESSAGE if not entry.template else f"{token} 命令的返回文本。")
        built.append(CommandEntry(entry.template, help_text, message_text))
    return built


def collect_plan(
    *,
    name: str | None,
    desc: str | None,
    author: str | None,
    license: str | None,
    aliases: list[str],
    platforms: list[str],
    excluded_platforms: list[str],
    components: list[str],
    commands: list[str],
    has_config: bool | None,
    has_database: bool | None,
    has_assets: bool | None,
    has_data_dir: bool | None,
    with_tests: bool | None,
    non_interactive: bool,
) -> ModulePlan:
    """按 §3.4.4 的问卷顺序收集答案，交互模式逐项提问，非交互模式取选项与默认值。

    :return: 问卷答案。
    """
    if name is None:
        if non_interactive:
            raise typer.BadParameter("非交互模式必须给出模块名：akaribot new module <name> --non-interactive")
        name = typer.prompt("模块名")
    validate_module_name(name)

    desc = prompt_text(desc, "模块说明（写入 desc 与帮助文档）", f"{name} 模块。", non_interactive)
    default_author = detect_author()
    author = prompt_text(author, "作者", default_author, non_interactive)
    license = prompt_text(license, "许可证标识", DEFAULT_LICENSE, non_interactive)

    aliases = prompt_list(aliases, "命令别名（逗号分隔，可留空）", [], non_interactive)
    if not platforms and not excluded_platforms and not non_interactive:
        answer = typer.prompt("支持平台（逗号分隔，留空表示全部，条目以 - 开头表示排除）", default="")
        platforms, excluded_platforms = split_platforms(answer)

    components = validate_components(
        prompt_list(
            components,
            f"需要的组件（逗号分隔，可选：{', '.join(COMPONENT_CHOICES)}）",
            ["command"],
            non_interactive,
        )
    )

    entries = [parse_command_option(value) for value in commands] if "command" in components else []
    if "command" in components:
        if not entries and not non_interactive:
            entries = ask_commands(name)
        if not entries:
            entries = [CommandEntry(template="")]

    return ModulePlan(
        name=name,
        desc=desc,
        author=author,
        license=license,
        aliases=aliases,
        available_for=list(platforms),
        exclude_from=list(excluded_platforms),
        components=components,
        commands=build_commands(name, entries),
        has_config=prompt_flag(has_config, "是否需要配置？", False, non_interactive),
        has_database=prompt_flag(has_database, "是否需要数据库？", False, non_interactive),
        has_assets=prompt_flag(has_assets, "是否需要包内资源目录？", False, non_interactive),
        has_data_dir=prompt_flag(has_data_dir, "是否需要运行时数据目录示例？", False, non_interactive),
        with_tests=prompt_flag(with_tests, "是否生成测试？", True, non_interactive),
    )


def detect_author() -> str:
    """取默认作者名：优先本机 git 配置，取不到时回落到固定值。"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.name"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return GIT_AUTHOR_FALLBACK
    return result.stdout.strip() or GIT_AUTHOR_FALLBACK


def unique_token(token: str, module_name: str, used: set[str]) -> str:
    """为命令分配在 locale 键中不冲突的短名。

    :param token: 原始短名。
    :param module_name: 模块名。
    :param used: 已占用的 locale 键集合，函数就地更新。
    :return: 可用的短名。
    """
    candidate = token
    index = 2
    while f"{module_name}.help.{candidate}" in used or f"{module_name}.message.{candidate}" in used:
        candidate = f"{token}_{index}"
        index += 1
    used.add(f"{module_name}.help.{candidate}")
    used.add(f"{module_name}.message.{candidate}")
    return candidate


def prepare_commands(plan: ModulePlan) -> list[dict[str, object]]:
    """把命令条目装配成模板可直接拼进源码的结构。

    :param plan: 问卷答案。
    :return: 每条命令的声明、函数签名、locale 键与测试取值。
    """
    prepared: list[dict[str, object]] = []
    used: set[str] = set()
    for entry in plan.commands:
        is_default = not entry.template
        if is_default:
            used.add(f"{plan.name}.help")
            used.add(f"{plan.name}.message.hello")
        token = unique_token(entry.token, plan.name, used) if not is_default else "default"
        help_key = f"{plan.name}.help" if is_default else f"{plan.name}.help.{token}"
        message_key = f"{plan.name}.message.hello" if is_default else f"{plan.name}.message.{token}"
        params = command_params(entry.template)
        signature = "msg: Bot.MessageSession" + "".join(
            f", {param.name}: {param.annotation} = {param.default}" for param in params
        )
        declaration = "" if is_default else python_literal(f"{entry.template} {{{{I18N:{help_key}}}}}")
        prepared.append(
            {
                "token": token,
                "suffix": entry.template,
                "doc": entry.help_text,
                "help_key": help_key,
                "message_key": message_key,
                "message_text": entry.message_text,
                "declaration": declaration,
                "signature": signature,
                "message_literal": python_literal(message_key),
            }
        )
    return prepared


def prepare_test_cases(plan: ModulePlan, commands: list[dict[str, object]]) -> list[dict[str, str]]:
    """由命令生成集成用例的取值。

    :param plan: 问卷答案。
    :param commands: :func:`prepare_commands` 的结果。
    :return: 每个用例的短名、输入、断言文案与说明。
    """
    cases: list[dict[str, str]] = []
    for command in commands:
        token = str(command["token"])
        example = command_example(str(command["suffix"])) or token
        message_text = str(command["message_text"])
        note = f"{plan.name} 的 {token} 命令应返回预期文案"
        cases.append(
            {
                "token": token,
                "doc": f"{token} 命令返回预期文案。",
                "input_literal": python_literal(f"~{plan.name} {example}".strip()),
                "expected_literal": python_literal(message_text),
                "note_literal": python_literal(note),
            }
        )
    return cases


def locale_entries(plan: ModulePlan, commands: list[dict[str, object]]) -> dict[str, str]:
    """装配 ``locales/zh_cn.json`` 的全部键值，只含简体中文。

    :param plan: 问卷答案。
    :param commands: :func:`prepare_commands` 的结果。
    :return: 键到文案的映射，键按字面序排列后写入文件。
    """
    entries: dict[str, str] = {f"{plan.name}.help.desc": plan.desc}
    for entry, command in zip(plan.commands, commands):
        entries[str(command["help_key"])] = entry.help_text
        entries[str(command["message_key"])] = entry.message_text
    if "regex" in plan.components:
        entries[f"{plan.name}.message.reply"] = "请回复本条消息。"
    if "schedule" in plan.components:
        entries[f"{plan.name}.message.scheduled"] = "定时任务已触发。"
    if plan.has_config:
        entries[f"config.comments.module_{plan.name}.{plan.name}_example"] = f"{plan.name} 模块的示例配置项。"
    return dict(sorted(entries.items()))


def api_names(plan: ModulePlan, commands: list[dict[str, object]]) -> list[str]:
    """按实际用到的组件裁剪 ``akaribot.core.api`` 的导入清单。

    :param plan: 问卷答案。
    :param commands: :func:`prepare_commands` 的结果。
    :return: 需要导入的名字，按固定顺序排列。
    """
    names = {"module"}
    if commands or {"regex", "schedule", "hook"} & set(plan.components):
        names.add("Bot")
    if commands or {"regex", "schedule"} & set(plan.components):
        names.add("I18NContext")
    if "schedule" in plan.components:
        names.add("IntervalTrigger")
    if "hook" in plan.components:
        names.add("HookPoint")
    if "event" in plan.components:
        names.add("EventInfo")
    return [name for name in API_IMPORT_ORDER if name in names]


def template_context(plan: ModulePlan) -> dict[str, object]:
    """渲染上下文。

    :param plan: 问卷答案。
    :return: 模板变量。
    """
    commands = prepare_commands(plan)
    context: dict[str, object] = dict(placeholder_values(plan))
    context.update(
        {
            "aliases": plan.aliases,
            "available_for": plan.available_for,
            "exclude_from": plan.exclude_from,
            "api_names": api_names(plan, commands),
            "commands": commands,
            "test_cases": prepare_test_cases(plan, commands),
            "locale_json": json.dumps(locale_entries(plan, commands), ensure_ascii=False, indent=4),
            "has_config": plan.has_config,
            "has_database": plan.has_database,
            "has_assets": plan.has_assets,
            "has_data_dir": plan.has_data_dir,
            "with_tests": plan.with_tests,
            "has_regex": "regex" in plan.components,
            "has_schedule": "schedule" in plan.components,
            "has_hook": "hook" in plan.components,
            "has_event": "event" in plan.components,
        }
    )
    return context


def template_enabled(relative: str, plan: ModulePlan) -> bool:
    """判断一个模板文件是否属于本次生成范围。

    :param relative: 模板相对路径。
    :param plan: 问卷答案。
    :return: 需要生成时返回 ``True``。
    """
    attribute = OPTIONAL_TEMPLATES.get(relative)
    return attribute is None or bool(getattr(plan, attribute))


def render_tree(
    *,
    root: Path,
    target: Path,
    values: dict[str, str],
    context: dict[str, object],
    enabled: Callable[[str], bool] | None = None,
    skip: frozenset[str] = frozenset(),
    force: bool = False,
    conflict_message: str = "",
) -> list[Path]:
    """渲染模板树并写出包目录，模块与适配器共用同一套渲染机制。

    :param root: 模板目录。
    :param target: 包目录。
    :param values: 占位符取值，用于路径与正文的明文替换。
    :param context: Jinja2 渲染上下文。
    :param enabled: 相对路径到「是否生成」的判定，``None`` 表示全部生成。
    :param skip: 只留在模板仓库内、不随生成物分发的相对路径。
    :param force: 目标目录非空时是否覆盖。
    :param conflict_message: 目标目录非空且未加 ``--force`` 时的报错文本，空串表示用默认文本。
    :return: 写出的文件列表。
    :raises typer.BadParameter: 目标目录非空且未加 ``--force``。
    """
    environment = Environment(
        loader=FileSystemLoader(str(root)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    if target.exists() and any(target.iterdir()) and not force:
        raise typer.BadParameter(conflict_message or f"目标目录非空：{target}；确认覆盖请加 --force。")
    written: list[Path] = []
    for source in sorted(root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(root).as_posix()
        if relative in skip or (enabled is not None and not enabled(relative)):
            continue
        output_relative = fill_placeholders(relative[: -len(".j2")] if relative.endswith(".j2") else relative, values)
        destination = target / output_relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative.endswith(".j2"):
            rendered = environment.get_template(relative).render(**context)
            destination.write_text(fill_placeholders(rendered, values), encoding="utf-8")
        else:
            shutil.copyfile(source, destination)
        written.append(destination)
    return written


def write_package(plan: ModulePlan, root: Path, target: Path, force: bool) -> list[Path]:
    """按模块问卷答案渲染模板树并写出包目录。

    :param plan: 问卷答案。
    :param root: 模板目录。
    :param target: 包目录。
    :param force: 目标目录非空时是否覆盖。
    :return: 写出的文件列表。
    """
    return render_tree(
        root=root,
        target=target,
        values=placeholder_values(plan),
        context=template_context(plan),
        enabled=lambda relative: template_enabled(relative, plan),
        force=force,
        conflict_message=f"目标目录非空：{target}；确认覆盖请加 --force。",
    )


def cli_command() -> list[str]:
    """定位 CLI 入口：优先 PATH 上的 akaribot，否则用当前解释器执行模块入口。"""
    found = shutil.which("akaribot")
    return [found] if found else [sys.executable, "-m", "akaribot.cli.main"]


def run_module_add(target: Path, failure_message: str | None = None) -> bool:
    """尝试执行一次 ``akaribot module add -e .``。

    :param target: 包目录。
    :param failure_message: 未成功时的完整提示，含手动命令；空表示沿用模块脚手架的既有文本。
    :return: 成功返回 ``True``；该子命令尚未实现或执行失败时返回 ``False``。
    """
    command = [*cli_command(), "module", "add", "-e", "."]
    try:
        result = subprocess.run(
            command,
            cwd=target,
            capture_output=True,
            text=True,
            check=False,
            stdin=subprocess.DEVNULL,
            timeout=MODULE_ADD_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        typer.echo(f"跳过 akaribot module add（{error}）。")
        return False
    if result.returncode != 0:
        if failure_message is not None:
            typer.echo(failure_message)
            return False
        typer.echo("akaribot module add 未成功，该子命令可能尚未实现；请稍后手动执行：")
        typer.echo(f"  cd {target} && akaribot module add -e .")
        return False
    if result.stdout.strip():
        typer.echo(result.stdout.strip())
    return True


def adapter_class_name(platform_name: str) -> str:
    """取类名前缀：已是大写开头的标识符原样保留，其余按 ``_`` 分段转大驼峰。"""
    if platform_name[:1].isupper() and platform_name.isidentifier():
        return platform_name
    return camel_case(platform_name)


def adapter_placeholder_values(plan: AdapterPlan) -> dict[str, str]:
    """适配器占位符取值，名字沿用 ``templates/module/`` 的五项。

    :param plan: 问卷答案。
    :return: 占位符到取值的映射。
    """
    return {
        "module_name": plan.name,
        "module_class": adapter_class_name(plan.platform_name),
        "module_desc": plan.desc,
        "author": plan.author,
        "license": plan.license,
    }


def validate_adapter_name(name: str) -> None:
    """校验适配器名可用作包名、entry point 名与 TOML 裸键。

    :param name: 适配器名。
    :raises typer.BadParameter: 名字不合规。
    """
    if not MODULE_NAME_PATTERN.match(name) or keyword.iskeyword(name):
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_name"))


def validate_platform_name(name: str) -> None:
    """校验平台显示名：字母开头，其后只允许字母、数字与下划线。

    :param name: 平台显示名。
    :raises typer.BadParameter: 名字不合规。
    """
    if not PLATFORM_NAME_PATTERN.match(name):
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_platform_name"))


def parse_feature(value: str) -> tuple[str, bool]:
    """解析一个 ``--feature`` 取值，形如 ``support_image`` 或 ``support_image=false``。

    :param value: 命令行取值。
    :return: 能力名与开关。
    :raises typer.BadParameter: 取值不合规。
    """
    match = FEATURE_PATTERN.match(value.strip())
    if match is None:
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_feature", value=value))
    return match.group(1), match.group(2) != "false"


def field_default(annotation: str, raw: str) -> str:
    """把默认值原文转成该类型的 Python 字面量。

    :param annotation: 类型名，取值来自 ``FIELD_TYPES``。
    :param raw: 默认值原文，空串表示取该类型的零值。
    :return: 可直接写进 config.py 的字面量。
    :raises ValueError: 原文无法按该类型解析。
    """
    text = raw.strip()
    if annotation == "bool":
        return "True" if text.lower() in TRUTHY_VALUES else "False"
    if annotation == "int":
        return str(int(text)) if text else "0"
    if annotation == "float":
        return repr(float(text)) if text else "0.0"
    if annotation == "list":
        return "[" + ", ".join(python_literal(item.strip()) for item in raw.split(",") if item.strip()) + "]"
    return python_literal(raw)


def parse_field(value: str) -> ConfigField:
    """解析一个 ``--field`` 取值，形如 ``字段名[:类型][=默认值]``。

    :param value: 命令行取值。
    :return: 配置字段声明。
    :raises typer.BadParameter: 取值不合规。
    """
    match = FIELD_PATTERN.match(value.strip())
    annotation = match.group(2) if match else None
    if match is None or (annotation is not None and annotation not in FIELD_TYPES):
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_field", value=value))
    annotation = annotation or "str"
    try:
        default = field_default(annotation, match.group(3) or "")
    except ValueError as error:
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_field", value=value)) from error
    return ConfigField(match.group(1), annotation, default)


def parse_credential_field(value: str) -> ConfigField:
    """解析一个 ``--credential-field`` 取值，只接受字段名。

    :param value: 命令行取值。
    :return: 凭据字段声明，类型固定为 ``str``，默认空串。
    :raises typer.BadParameter: 字段名不合规。
    """
    name = value.strip()
    if not MODULE_NAME_PATTERN.match(name):
        raise typer.BadParameter(i18n.t("cli.new.adapter.invalid_credential", value=value))
    return ConfigField(name, "str", python_literal(""))


def resolve_adapter_features(values: list[str]) -> list[tuple[str, bool]]:
    """解析能力勾选：同名取最后一条，结果为空时回落到默认能力集。

    :param values: ``--feature`` 取值或问卷作答拆出的条目。
    :return: 能力名与开关，按首次出现顺序排列。
    """
    resolved: dict[str, bool] = {}
    for value in values:
        feature_name, enabled = parse_feature(value)
        resolved[feature_name] = enabled
    if not resolved:
        return [(feature_name, True) for feature_name in ADAPTER_DEFAULT_FEATURES]
    return list(resolved.items())


def ask_entries(confirm_question: str, question: str, default: str = "") -> list[str]:
    """逐条录入取值，直到作者表示不再添加。

    :param confirm_question: 是否继续添加的提问文本。
    :param question: 单条取值的提问文本。
    :param default: 单条取值的默认值。
    :return: 录入的取值列表。
    """
    entries: list[str] = []
    while typer.confirm(confirm_question, default=not entries):
        entry = typer.prompt(question, default=default).strip()
        if entry:
            entries.append(entry)
    return entries


def collect_adapter_plan(
    *,
    name: str | None,
    platform_name: str | None,
    desc: str | None,
    author: str | None,
    license: str | None,
    features: list[str],
    has_config: bool | None,
    fields: list[str],
    credential_fields: list[str],
    non_interactive: bool,
) -> AdapterPlan:
    """按问卷顺序收集适配器答案，交互模式逐项提问，非交互模式取选项与默认值。

    :return: 问卷答案。
    """
    if name is None:
        if non_interactive:
            raise typer.BadParameter(i18n.t("cli.new.adapter.name_required"))
        name = typer.prompt(i18n.t("cli.new.adapter.prompt_name"))
    validate_adapter_name(name)

    platform_name = prompt_text(
        platform_name,
        i18n.t("cli.new.adapter.prompt_platform_name"),
        camel_case(name),
        non_interactive,
    )
    validate_platform_name(platform_name)
    desc = prompt_text(
        desc,
        i18n.t("cli.new.adapter.prompt_desc"),
        i18n.t("cli.new.adapter.desc_default", name=platform_name),
        non_interactive,
    )
    author = prompt_text(author, i18n.t("cli.new.adapter.prompt_author"), detect_author(), non_interactive)
    license = prompt_text(license, i18n.t("cli.new.adapter.prompt_license"), DEFAULT_LICENSE, non_interactive)

    selected = prompt_list(
        features,
        i18n.t("cli.new.adapter.prompt_features"),
        list(ADAPTER_DEFAULT_FEATURES),
        non_interactive,
    )
    # 给出字段即隐含启用配置，避免 --field / --credential-field 被静默丢弃。
    with_fields = bool(fields or credential_fields)
    has_config = prompt_flag(has_config, i18n.t("cli.new.adapter.prompt_config"), with_fields, non_interactive)
    if with_fields and not has_config:
        raise typer.BadParameter(i18n.t("cli.new.adapter.config_required"))
    if has_config and not fields and not non_interactive:
        fields = ask_entries(i18n.t("cli.new.adapter.prompt_add_field"), i18n.t("cli.new.adapter.prompt_field"))
    if has_config and not credential_fields and not non_interactive:
        credential_fields = ask_entries(
            i18n.t("cli.new.adapter.prompt_add_credential"),
            i18n.t("cli.new.adapter.prompt_credential"),
            default=f"{name}{CREDENTIAL_DEFAULT_SUFFIX}",
        )

    return AdapterPlan(
        name=name,
        platform_name=platform_name,
        desc=desc,
        author=author,
        license=license,
        features=resolve_adapter_features(selected),
        has_config=has_config,
        config_fields=[parse_field(value) for value in fields],
        credential_fields=[parse_credential_field(value) for value in credential_fields],
    )


def config_field_entries(fields: list[ConfigField]) -> list[dict[str, str]]:
    """把配置字段装配成模板可直接拼进源码的结构。

    :param fields: 普通字段或凭据字段。
    :return: 每项的字段名、类型标注与默认值字面量。
    """
    return [{"name": item.name, "annotation": item.annotation, "default": item.default} for item in fields]


def adapter_locale_entries(plan: AdapterPlan) -> dict[str, str]:
    """装配 ``locales/zh_cn.json`` 的全部键值，只含简体中文。

    普通字段的注释键落在基表上，凭据字段的表名由 ``CFGManager`` 加 ``_secret`` 后缀派生。

    :param plan: 问卷答案。
    :return: 键到文案的映射，键按字面序排列后写入文件。
    """
    entries: dict[str, str] = {}
    for item in plan.config_fields:
        entries[f"config.comments.bot_{plan.name}.{item.name}"] = f"{plan.platform_name} 平台的 {item.name} 配置项。"
    for item in plan.credential_fields:
        entries[f"config.comments.bot_{plan.name}_secret.{item.name}"] = f"{plan.platform_name} 平台的凭据。"
    return dict(sorted(entries.items()))


def adapter_template_context(plan: AdapterPlan) -> dict[str, object]:
    """适配器模板的渲染上下文。

    :param plan: 问卷答案。
    :return: 模板变量。
    """
    context: dict[str, object] = dict(adapter_placeholder_values(plan))
    context.update(
        {
            "platform_name": plan.platform_name,
            "features": [{"name": feature_name, "value": str(enabled)} for feature_name, enabled in plan.features],
            "config_fields": config_field_entries(plan.config_fields),
            "credential_fields": config_field_entries(plan.credential_fields),
            "credential_fields_toml": json.dumps([item.name for item in plan.credential_fields]),
            "has_config": plan.has_config,
            "locale_json": json.dumps(adapter_locale_entries(plan), ensure_ascii=False, indent=4),
        }
    )
    return context


def adapter_template_enabled(relative: str, plan: AdapterPlan) -> bool:
    """判断一个适配器模板文件是否属于本次生成范围。

    :param relative: 模板相对路径。
    :param plan: 问卷答案。
    :return: 需要生成时返回 ``True``。
    """
    attribute = ADAPTER_OPTIONAL_TEMPLATES.get(relative)
    return attribute is None or bool(getattr(plan, attribute))


def write_adapter_package(plan: AdapterPlan, root: Path, target: Path, force: bool) -> list[Path]:
    """按适配器问卷答案渲染模板树并写出包目录。

    :param plan: 问卷答案。
    :param root: 模板目录。
    :param target: 包目录。
    :param force: 目标目录非空时是否覆盖。
    :return: 写出的文件列表。
    """
    return render_tree(
        root=root,
        target=target,
        values=adapter_placeholder_values(plan),
        context=adapter_template_context(plan),
        enabled=lambda relative: adapter_template_enabled(relative, plan),
        skip=ADAPTER_TEMPLATE_SKIP,
        force=force,
        conflict_message=i18n.t("cli.new.adapter.target_not_empty", target=target),
    )


@app.command("adapter", help=i18n.t("cli.new.adapter.help"))
def new_adapter(
    name: str | None = typer.Argument(None, help=i18n.t("cli.new.adapter.name_argument")),
    directory: Path = typer.Option(Path("."), "--dir", "-d", help=i18n.t("cli.new.adapter.dir_option")),
    template_dir: Path | None = typer.Option(
        None, "--template-dir", help=i18n.t("cli.new.adapter.template_dir_option")
    ),
    platform_name: str | None = typer.Option(
        None, "--platform-name", help=i18n.t("cli.new.adapter.platform_name_option")
    ),
    desc: str | None = typer.Option(None, "--desc", help=i18n.t("cli.new.adapter.desc_option")),
    author: str | None = typer.Option(None, "--author", help=i18n.t("cli.new.adapter.author_option")),
    license: str | None = typer.Option(None, "--license", help=i18n.t("cli.new.adapter.license_option")),
    feature: list[str] = typer.Option([], "--feature", help=i18n.t("cli.new.adapter.feature_option")),
    with_config: bool | None = typer.Option(None, "--config/--no-config", help=i18n.t("cli.new.adapter.config_option")),
    field: list[str] = typer.Option([], "--field", help=i18n.t("cli.new.adapter.field_option")),
    credential_field: list[str] = typer.Option(
        [], "--credential-field", help=i18n.t("cli.new.adapter.credential_option")
    ),
    non_interactive: bool = typer.Option(
        False, "--non-interactive", help=i18n.t("cli.new.adapter.non_interactive_option")
    ),
    add: bool = typer.Option(True, "--add/--no-add", help=i18n.t("cli.new.adapter.add_option")),
    force: bool = typer.Option(False, "--force", help=i18n.t("cli.new.adapter.force_option")),
) -> None:
    """生成适配器包。"""
    plan = collect_adapter_plan(
        name=name,
        platform_name=platform_name,
        desc=desc,
        author=author,
        license=license,
        features=feature,
        has_config=with_config,
        fields=field,
        credential_fields=credential_field,
        non_interactive=non_interactive,
    )
    root = template_root(
        template_dir,
        ADAPTER_TEMPLATE_RELATIVE,
        ADAPTER_TEMPLATE_MARKER,
        i18n.t("cli.new.adapter.template_missing", marker=ADAPTER_TEMPLATE_MARKER, env=TEMPLATE_DIR_ENV),
    )
    target = (directory / f"akari-bot-adapter-{plan.name}").resolve()
    written = write_adapter_package(plan, root, target, force)
    typer.echo(i18n.t("cli.new.adapter.generated", count=len(written), target=target))
    for path in written:
        typer.echo(f"  {path.relative_to(target)}")
    if add:
        # 失败提示（含手动命令）由 run_module_add 打印，此处不再补一行命令。
        run_module_add(target, i18n.t("cli.new.adapter.add_failed", target=target))
    typer.echo(i18n.t("cli.new.adapter.next_steps"))


@app.command("module")
def new_module(
    name: str | None = typer.Argument(None, help="模块名：小写字母、数字与下划线，如 dice"),
    directory: Path = typer.Option(
        Path("."), "--dir", "-d", help="生成目录，包目录为 <生成目录>/akari-bot-module-<name>"
    ),
    template_dir: Path | None = typer.Option(None, "--template-dir", help="模板目录，默认自动定位"),
    alias: list[str] = typer.Option([], "--alias", help="命令别名，可重复"),
    desc: str | None = typer.Option(None, "--desc", help="一句话说明，写入 module() 的 desc 与 zh_cn 的 help.desc"),
    author: str | None = typer.Option(None, "--author", help="作者名，写入 pyproject 与 module() 的 developers"),
    license: str | None = typer.Option(None, "--license", help="许可证标识，写入 pyproject"),
    platform: list[str] = typer.Option([], "--platform", help="支持平台（available_for），可重复；留空表示全部平台"),
    exclude_platform: list[str] = typer.Option([], "--exclude-platform", help="排除平台（exclude_from），可重复"),
    component: list[str] = typer.Option(
        [], "--component", help="组件：command / regex / schedule / hook / event，可重复"
    ),
    command: list[str] = typer.Option([], "--command", help="命令模板，可重复；模板与说明用 :: 分隔"),
    with_config: bool | None = typer.Option(None, "--config/--no-config", help="生成 config.py 与配置注释键"),
    with_database: bool | None = typer.Option(None, "--database/--no-database", help="生成 database/ 与 migrations/"),
    with_assets: bool | None = typer.Option(None, "--assets/--no-assets", help="生成包内只读资源目录 assets/"),
    with_data_dir: bool | None = typer.Option(None, "--data-dir/--no-data-dir", help="生成 data_dir() 使用示例"),
    with_tests: bool | None = typer.Option(None, "--tests/--no-tests", help="生成 tests/test_<name>.py"),
    non_interactive: bool = typer.Option(False, "--non-interactive", help="不提问，未给出的选项取默认值"),
    add: bool = typer.Option(True, "--add/--no-add", help="生成后执行 akaribot module add -e ."),
    force: bool = typer.Option(False, "--force", help="目标目录非空时覆盖"),
) -> None:
    """生成模块包。"""
    plan = collect_plan(
        name=name,
        desc=desc,
        author=author,
        license=license,
        aliases=alias,
        platforms=platform,
        excluded_platforms=exclude_platform,
        components=component,
        commands=command,
        has_config=with_config,
        has_database=with_database,
        has_assets=with_assets,
        has_data_dir=with_data_dir,
        with_tests=with_tests,
        non_interactive=non_interactive,
    )
    if plan.with_tests and not plan.commands:
        typer.echo("未勾选 command 组件，没有可断言的命令，跳过测试文件。")
        plan.with_tests = False

    root = template_root(template_dir)
    target = (directory / f"akari-bot-module-{plan.name}").resolve()
    written = write_package(plan, root, target, force)
    typer.echo(f"已生成 {len(written)} 个文件：{target}")
    for path in written:
        typer.echo(f"  {path.relative_to(target)}")
    if add and not run_module_add(target):
        typer.echo(f"  cd {target} && akaribot module add -e .")


if __name__ == "__main__":
    app()
