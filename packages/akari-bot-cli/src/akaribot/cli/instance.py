"""实例模型：定位实例根、读写 ``akaribot.toml``，并经子进程与 core 交互。

CLI 进程不 import ``akaribot.core``：实例操作一律经实例 venv 的解释器执行
``python -m akaribot.core.entrypoints.<x>``，本模块只拼装命令、注入环境变量并解析 JSON 回传。
"""

from __future__ import annotations

import json
import os
import subprocess
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, Mapping, NoReturn, Sequence

import click
import tomlkit
import typer
from packaging.requirements import InvalidRequirement, Requirement
from rich.console import Console
from typer.core import TyperGroup

from akaribot.cli import i18n

console = Console()
err_console = Console(stderr=True)

InstancePathOption = Annotated[
    Path | None,
    typer.Option(
        "--instance",
        "-I",
        help=i18n.t("cli.common.instance_option"),
    ),
]


class FlatCommandGroup(TyperGroup):
    """单命令子应用的分组：位置参数之后仍解析选项，usage 里不出现 COMMAND。

    Typer 的子应用默认是多命令分组，`akaribot init` 会退化成 `akaribot init init`；
    本类让唯一命令直接在分组层生效。多余 token 默认报错，子类可改为透传。
    """

    allow_interspersed_args = True
    passthrough_extra_args = False

    def collect_usage_pieces(self, ctx: click.Context) -> list[str]:
        """usage 里不追加子命令占位符。"""
        return super(TyperGroup, self).collect_usage_pieces(ctx)

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """把剩余 token 交给唯一的命令；不支持透传时按多余参数报错。

        剩余 token 存在上下文私有字段 ``_protected_args``（click 8.4 与 typer 0.27 均如此），
        取空后分组即视为「没有子命令」，回调照常执行。
        """
        rest = super().parse_args(ctx, args)
        pending = list(getattr(ctx, "_protected_args", None) or ())
        if pending:
            if self.passthrough_extra_args:
                ctx.args = [*pending, *ctx.args]
            else:
                ctx.fail(f"Got unexpected extra argument ({' '.join(pending)})")
            ctx._protected_args = []
        return rest


class PassthroughCommandGroup(FlatCommandGroup):
    """把未识别参数原样透传给 core 的单命令分组。"""

    passthrough_extra_args = True


INSTANCE_META_FILENAME = "akaribot.toml"
# 非托管模式要用的解释器路径；冻结产物下没有可用的 sys.executable。
PYTHON_ENV = "AKARIBOT_PYTHON"
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"
CORE_ENTRYPOINT_PREFIX = "akaribot.core.entrypoints"
LOCK_FILENAME = ".bot.lock"
DEFAULT_VENV = ".venv"
DEFAULT_LOCALE = "zh_cn"
DEFAULT_REGISTRY_SOURCE = "https://akaribot.teahou.se/registry.json"
# 实例目录结构见 monorepo_refactor_plan.md §2.3；config 的子树由 config sync 按需补齐。
INSTANCE_DIRS = (
    "config",
    "config/core",
    "config/adapters",
    "config/modules",
    "data",
    "database",
    "cache",
    "logs",
    "assets/private",
)


def no_instance_hint() -> str:
    """不在任何实例内时的可执行提示；运行期取值，不冻结语言。"""
    return i18n.t("cli.error.not_instance_hint")


class CliError(Exception):
    """面向用户的失败。命令层捕获后打印消息并以非零码退出。"""


class InstanceNotFound(CliError):
    """实例根不存在或其中没有 akaribot.toml。"""


class CoreInvocationError(CliError):
    """经子进程调用 core 失败。

    :param message: 面向用户的原因说明。
    :param returncode: 子进程退出码；未执行时为 ``None``。
    :param stderr: 子进程标准错误，供 ``--verbose`` 展示。
    """

    def __init__(self, message: str, *, returncode: int | None = None, stderr: str = "") -> None:
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr


def fail(message: str, *, code: int = 1) -> NoReturn:
    """打印错误并退出。消息须自带可执行的下一步提示。"""
    err_console.print(f"[bold red]{i18n.t('cli.common.error_label')}[/bold red] {message}")
    raise typer.Exit(code)


def warn(message: str) -> None:
    """打印警告，不中断流程。"""
    err_console.print(f"[bold yellow]{i18n.t('cli.common.warning_label')}[/bold yellow] {message}")


def ok(message: str) -> None:
    """打印成功项。"""
    console.print(f"[green]✓[/green] {message}")


def step(index: int, total: int, title: str) -> None:
    """打印流水线的步骤标题。"""
    console.print(f"[bold cyan][{index}/{total}][/bold cyan] {title}")


def now_iso() -> str:
    """当前时刻的 ISO 8601 UTC 表示，形如 ``2026-09-18T00:00:00Z``。"""
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def split_names(values: Sequence[str] | None) -> list[str]:
    """把可重复选项与逗号分隔写法拆成名字列表，去重并保持顺序。"""
    result: list[str] = []
    for value in values or ():
        for item in str(value).replace("，", ",").split(","):
            name = item.strip()
            if name and name not in result:
                result.append(name)
    return result


def is_windows() -> bool:
    """当前平台是否为 Windows。"""
    return os.name == "nt"


def system_python() -> Path:
    """解析非托管模式要用的系统 Python。

    :return: 解释器绝对路径。
    :raises CliError: 找不到可用解释器。
    """
    override = os.environ.get(PYTHON_ENV)
    if override:
        candidate = Path(override).expanduser()
        if candidate.is_file():
            return candidate
        raise CliError(i18n.t("cli.instance.python_env_missing", env=PYTHON_ENV, path=candidate))
    # 非冻结时当前解释器就是可用的 Python，且与项目要求的版本一致；冻结后 sys.executable 指向
    # CLI 二进制自身，才需要回退到系统搜索。回退时优先带版本号的名字，避免拿到过旧的 python3。
    if not (getattr(sys, "frozen", False) or hasattr(sys, "__compiled__")):
        return Path(sys.executable)
    for name in ("python3.13", "python3.12", "python3", "python"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise CliError(i18n.t("cli.instance.no_system_python", env=PYTHON_ENV))


def venv_python_path(venv_dir: Path) -> Path:
    """虚拟环境中的解释器路径，兼容 posix 与 Windows 两种布局。"""
    if is_windows():
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def venv_scripts_dir(venv_dir: Path) -> Path:
    """虚拟环境中的可执行文件目录。"""
    return venv_dir / ("Scripts" if is_windows() else "bin")


@dataclass(frozen=True)
class DependencyInfo:
    """一个分发在 metadata 里声明的依赖项。

    :param dist: 依赖的分发名，已规范化。
    :param specifier: 版本描述符，如 ``>=1.0,<2.0``；未限定时为空串。
    :param satisfied: 已装版本是否满足该描述符。
    :param installed_version: 已装版本；未安装时为 ``None``。
    """

    dist: str
    specifier: str = ""
    satisfied: bool = True
    installed_version: str | None = None


@dataclass(frozen=True)
class PackageInfo:
    """一个已装 akaribot 包的展示信息，来自 ``registry --json`` 的回传。

    ``registry --json`` 的确切字段由 core 侧决定，本类型按已知字段名解析并容忍同义写法，
    因此 core 调整字段时只需保证 :meth:`from_mapping` 仍能取到值。

    :param dist: 分发名，如 ``akari-bot-module-wiki``。
    :param version: 已装版本。
    :param kind: ``module`` / ``adapter`` / ``core`` / ``testing`` / ``unknown``。
    :param name: 短名，如 ``wiki``。
    :param import_path: 导入路径，如 ``akaribot.modules.wiki``。
    :param editable: 是否为可编辑安装。
    :param requires_core_api: 声明的 core API 区间。
    :param provides_modules: 该包注册的模块名。
    :param owned_tables: 该包拥有的数据表，供 ``--purge-data`` 使用。
    :param dependencies: 该包声明的依赖项。
    :param dependents: 依赖该包的分发名，core 侧可缺省。
    :param summary: 一句话简介，取自分发包元数据；取不到时为空串。
    """

    dist: str
    version: str = ""
    kind: str = "unknown"
    name: str = ""
    import_path: str = ""
    editable: bool = False
    requires_core_api: str = ""
    summary: str = ""
    provides_modules: tuple[str, ...] = ()
    owned_tables: tuple[str, ...] = ()
    dependencies: tuple[DependencyInfo, ...] = ()
    dependents: tuple[str, ...] = ()

    @property
    def display_name(self) -> str:
        """列表展示用的短名，取不到短名时退回分发名。"""
        return self.name or self.dist

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> PackageInfo:
        """由 ``registry --json`` 的一项构造。

        :param data: 一项包的 JSON 对象。
        :return: 解析后的包信息。
        """
        manifest = data.get("manifest") if isinstance(data.get("manifest"), Mapping) else {}
        dist = _first_str(data, ("dist", "dist_name", "distribution", "package")) or _first_str(manifest, ("dist",))
        name = _first_str(data, ("name", "module", "short_name")) or ""
        import_path = _first_str(data, ("import_path", "import", "module_path")) or ""
        if not dist:
            dist = name or Path(import_path).name
        if not name:
            provides = _as_tuple(data.get("provides_modules"))
            name = provides[0] if provides else _short_name(dist)
        kind = _normalize_kind(_first_str(data, ("kind", "type", "category")) or "")
        return cls(
            dist=dist,
            version=_first_str(data, ("version", "installed_version")) or "",
            kind=kind,
            name=name,
            import_path=import_path,
            editable=bool(data.get("editable", False)),
            requires_core_api=_first_str(data, ("requires_core_api",))
            or _first_str(manifest, ("requires_core_api",))
            or "",
            summary=_first_str(data, ("summary", "description")) or _first_str(manifest, ("summary",)) or "",
            provides_modules=_as_tuple(data.get("provides_modules")) or _as_tuple(manifest.get("provides_modules")),
            owned_tables=_as_tuple(data.get("owned_tables")) or _as_tuple(manifest.get("owned_tables")),
            dependencies=_parse_dependencies(data.get("dependencies", data.get("requires", data.get("requires_dist")))),
            dependents=_parse_names(data.get("dependents", data.get("required_by"))),
        )


def _first_str(data: Mapping[str, Any], keys: Sequence[str]) -> str | None:
    """取第一个存在且非空的字符串字段。"""
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _as_tuple(value: Any) -> tuple[str, ...]:
    """把 JSON 里的字符串列表归一为元组；非列表输入返回空元组。"""
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, Sequence):
        return tuple(str(item) for item in value if isinstance(item, (str, int)))
    return ()


def _short_name(dist: str) -> str:
    """由分发名推出短名：去掉 ``akari-bot-(module|adapter)-`` 前缀。"""
    stem = dist.lower().replace("_", "-")
    for prefix in ("akari-bot-module-", "akari-bot-adapter-", "akari-bot-"):
        if stem.startswith(prefix):
            return stem[len(prefix) :]
    return stem


_KIND_ALIASES = {
    "module": "module",
    "modules": "module",
    "adapter": "adapter",
    "adapters": "adapter",
    "core": "core",
    "testing": "testing",
    "test": "testing",
}


def _normalize_kind(value: str) -> str:
    """把 core 侧的种类写法归一到 CLI 的四种取值。"""
    return _KIND_ALIASES.get(value.strip().lower(), "unknown")


def _parse_names(value: Any) -> tuple[str, ...]:
    """解析 ``dependents`` 这类「分发名列表」，允许元素是对象。"""
    if isinstance(value, Mapping):
        return tuple(str(key) for key in value)
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, Sequence):
        return ()
    names: list[str] = []
    for item in value:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, Mapping):
            name = _first_str(item, ("dist", "dist_name", "name", "package"))
            if name:
                names.append(name)
    return tuple(names)


def _parse_dependencies(value: Any) -> tuple[DependencyInfo, ...]:
    """解析依赖项列表，兼容字符串、对象与「名字到描述符」的映射三种写法。"""
    if isinstance(value, Mapping):
        raw_items: list[Any] = [{"dist": key, "specifier": item} for key, item in value.items()]
    elif isinstance(value, str):
        raw_items = [value]
    elif isinstance(value, Sequence):
        raw_items = list(value)
    else:
        return ()
    result: list[DependencyInfo] = []
    for item in raw_items:
        if isinstance(item, str):
            result.append(_requirement_to_dependency(item))
        elif isinstance(item, Mapping):
            dist = _first_str(item, ("dist", "dist_name", "name", "package")) or ""
            if not dist:
                continue
            installed = item.get("installed_version")
            result.append(
                DependencyInfo(
                    dist=dist,
                    specifier=_first_str(item, ("specifier", "version", "constraint", "spec")) or "",
                    satisfied=bool(item.get("satisfied", True)),
                    installed_version=str(installed) if installed else None,
                )
            )
    return tuple(result)


def _requirement_to_dependency(text: str) -> DependencyInfo:
    """由 PEP 508 依赖串构造依赖项；解析失败时按分发名处理。"""
    try:
        requirement = Requirement(text)
    except InvalidRequirement:
        return DependencyInfo(dist=text.strip())
    return DependencyInfo(dist=requirement.name, specifier=str(requirement.specifier))


def extract_json(text: str) -> Any:
    """从子进程输出里截取 JSON 主体，容忍 core 日志混入 stdout。

    自每个 ``{`` 或 ``[`` 起尝试解析，第一个能完整解码的位置即为正文起点。
    """
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        return value
    raise CoreInvocationError(
        i18n.t("cli.instance.core_json_unparsable", text=text.strip()[:200] or i18n.t("cli.instance.empty_output"))
    )


@dataclass
class InstanceMeta:
    """``akaribot.toml`` 的内存视图。写回时保持注释与书写格式（tomlkit）。"""

    root: Path
    doc: Any

    @property
    def path(self) -> Path:
        """元数据文件路径。"""
        return self.root / INSTANCE_META_FILENAME

    @classmethod
    def load(cls, root: Path) -> InstanceMeta:
        """读取实例元数据。

        :param root: 实例根目录。
        :return: 元数据视图。
        :raises InstanceNotFound: 目录或文件缺失。
        """
        path = root / INSTANCE_META_FILENAME
        if not path.is_file():
            raise InstanceNotFound(i18n.t("cli.instance.meta_missing", path=path, hint=no_instance_hint()))
        try:
            doc = tomlkit.parse(path.read_text(encoding="utf-8"))
        except (OSError, tomlkit.exceptions.ParseError) as exc:
            raise CliError(i18n.t("cli.instance.meta_parse_failed", path=path, error=exc)) from exc
        return cls(root=root, doc=doc)

    @classmethod
    def create(
        cls,
        root: Path,
        *,
        name: str = "default",
        locale: str = DEFAULT_LOCALE,
        mode: str = "installed",
        venv: str = DEFAULT_VENV,
        workspace_root: str = "",
        registry_sources: Sequence[str] = (DEFAULT_REGISTRY_SOURCE,),
        created_at: str | None = None,
    ) -> InstanceMeta:
        """构造一份带注释的默认元数据，字段集见 tasks 附录 A.2。

        :param root: 实例根目录。
        :return: 尚未写盘的元数据视图。
        """
        sources = ", ".join(json.dumps(source) for source in registry_sources)
        text = (
            "schema = 1\n"
            "\n"
            "[instance]\n"
            f"name = {json.dumps(name)}\n"
            f"created_at = {json.dumps(created_at or now_iso())}\n"
            f"locale = {json.dumps(locale)}\n"
            f"mode = {json.dumps(mode)}  # installed | workspace（源代码来源，与 venv 托管无关）\n"
            "\n"
            "[runtime]\n"
            f"venv = {json.dumps(venv)}  # 相对实例目录；空串表示使用当前环境\n"
            "\n"
            "[dev]\n"
            f"workspace_root = {json.dumps(workspace_root)}  # 非空时安装一律取工作区内的本地路径\n"
            "\n"
            "[registry]\n"
            f"sources = [{sources}]\n"
        )
        return cls(root=root, doc=tomlkit.parse(text))

    @property
    def schema(self) -> int:
        """元数据结构版本。"""
        return int(self.doc.get("schema", 1))

    @property
    def name(self) -> str:
        """实例名。"""
        return str(self._section("instance").get("name", "default"))

    @property
    def created_at(self) -> str:
        """创建时刻。"""
        return str(self._section("instance").get("created_at", ""))

    @property
    def locale(self) -> str:
        """实例默认语言。"""
        return str(self._section("instance").get("locale", DEFAULT_LOCALE))

    @property
    def mode(self) -> str:
        """``installed`` 或 ``workspace``，描述源代码来源。"""
        return str(self._section("instance").get("mode", "installed"))

    @property
    def venv(self) -> str:
        """实例 venv 的相对路径；空串表示不托管、使用当前环境。"""
        return str(self._section("runtime").get("venv", ""))

    @property
    def workspace_root(self) -> str:
        """本地工作区根；非空时安装取本地路径。"""
        return str(self._section("dev").get("workspace_root", ""))

    @property
    def registry_sources(self) -> tuple[str, ...]:
        """registry.json 的来源列表。"""
        value = self._section("registry").get("sources", [])
        return _as_tuple(value)

    def set_venv(self, value: str) -> None:
        """设置 venv 相对路径；空串表示释放托管。"""
        self._section("runtime")["venv"] = value

    def set_workspace_root(self, value: str) -> None:
        """设置本地工作区根。"""
        self._section("dev")["workspace_root"] = value

    def set_locale(self, value: str) -> None:
        """设置实例语言。"""
        self._section("instance")["locale"] = value

    def set_mode(self, value: str) -> None:
        """设置源代码来源模式。"""
        self._section("instance")["mode"] = value

    def save(self) -> None:
        """原子写回 ``akaribot.toml``，未知键与注释一并保留。"""
        text = tomlkit.dumps(self.doc)
        temporary = self.path.with_name(self.path.name + ".tmp")
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(self.path)

    def _section(self, key: str) -> Any:
        """取得（必要时创建）一个子表。"""
        if key not in self.doc:
            self.doc[key] = tomlkit.table()
        return self.doc[key]


@dataclass(frozen=True)
class NotifyResult:
    """热装载通知的结果。

    :param attempted: 是否尝试了 RPC。
    :param delivered: RPC 是否成功送达。
    :param detail: 面向用户的说明。
    """

    attempted: bool
    delivered: bool
    detail: str


class Instance:
    """一个 AkariBot 实例。根目录下必须有 ``akaribot.toml``。

    :param root: 实例根目录。
    :param python_override: 指定解释器，用于测试替身；缺省按托管模式解析。
    :param meta: 元数据视图；缺省自磁盘读取。写盘前的规划用 :meth:`detached` 传入。
    """

    def __init__(self, root: Path, *, python_override: Path | None = None, meta: InstanceMeta | None = None) -> None:
        self.root = Path(root).expanduser().resolve()
        self.meta = meta or InstanceMeta.load(self.root)
        self._python_override = Path(python_override) if python_override else None
        self._installed: dict[str, PackageInfo] | None = None
        self._registry_payload: Mapping[str, Any] | None = None

    @classmethod
    def detached(
        cls,
        root: Path,
        *,
        locale: str = DEFAULT_LOCALE,
        venv: str = DEFAULT_VENV,
        workspace_root: str = "",
        mode: str = "installed",
    ) -> Instance:
        """构造不读磁盘的实例对象，供写盘前的解析与 ``--dry-run`` 使用。"""
        resolved = Path(root).expanduser().resolve()
        meta = InstanceMeta.create(resolved, locale=locale, venv=venv, workspace_root=workspace_root, mode=mode)
        return cls(resolved, meta=meta)

    @staticmethod
    def create_dirs(root: Path) -> list[Path]:
        """创建实例目录结构，返回新建的目录。

        :param root: 实例根目录。
        :return: 本次真正创建的目录列表。
        """
        created: list[Path] = []
        for name in INSTANCE_DIRS:
            path = root / name
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created.append(path)
        return created

    @property
    def managed(self) -> bool:
        """是否由 CLI 托管 venv。"""
        return bool(self.meta.venv)

    @property
    def venv_dir(self) -> Path:
        """实例 venv 目录；未托管时返回默认位置，仅供展示。"""
        return self.root / (self.meta.venv or DEFAULT_VENV)

    @property
    def python(self) -> Path:
        """实例解释器：托管模式取 venv 内的解释器，非托管模式取系统 Python。

        非托管模式**不得**用 ``sys.executable``：Nuitka onefile 冻结后它指向 CLI 二进制自身，
        拿它启动实例进程会重新调起 CLI 而不是 Python。改为按 ``AKARIBOT_PYTHON`` → 系统
        ``python3`` / ``python`` 的顺序解析，解析不到时抛出带指引的错误。
        """
        if self._python_override is not None:
            return self._python_override
        if self.managed:
            return venv_python_path(self.venv_dir)
        return system_python()

    @property
    def python_exists(self) -> bool:
        """实例解释器是否存在。"""
        return self.python.is_file()

    @property
    def workspace_root(self) -> Path | None:
        """本地工作区根；未配置时为 ``None``。"""
        value = self.meta.workspace_root
        return Path(value).expanduser().resolve() if value else None

    @property
    def config_dir(self) -> Path:
        """配置目录。"""
        return self.root / "config"

    def core_module(self, entrypoint: str) -> str:
        """把入口名补成完整模块路径；已含点号者原样返回。"""
        if "." in entrypoint:
            return entrypoint
        return f"{CORE_ENTRYPOINT_PREFIX}.{entrypoint}"

    def python_argv(self, *args: str) -> list[str]:
        """以实例解释器执行任意参数。"""
        return [str(self.python), *args]

    def module_argv(self, module: str, *args: str) -> list[str]:
        """以实例解释器执行 ``-m <module>``。"""
        return [str(self.python), "-m", module, *args]

    def core_argv(self, entrypoint: str, *args: str) -> list[str]:
        """以实例解释器执行 ``-m akaribot.core.entrypoints.<entrypoint>``。"""
        return self.module_argv(self.core_module(entrypoint), *args)

    def core_env(self, **env: str) -> dict[str, str]:
        """构造子进程环境：注入实例根，叠加调用方给出的变量。

        :param env: 额外的环境变量，值非字符串时先转换。
        :return: 完整环境变量映射。
        """
        result = dict(os.environ)
        result[INSTANCE_DIR_ENV] = str(self.root)
        result["PYTHONIOENCODING"] = result.get("PYTHONIOENCODING", "utf-8")
        for key, value in env.items():
            result[key] = str(value)
        return result

    def run_core(self, entrypoint: str, *args: str, **env: str) -> int:
        """执行 core 入口并返回退出码，标准流直接继承。

        :param entrypoint: 入口名（``run``）或完整模块路径。
        :param args: 传给入口的参数。
        :param env: 额外注入的环境变量。
        :return: 子进程退出码。
        """
        return self._run(self.core_argv(entrypoint, *args), **env)

    def run_core_capture(
        self, entrypoint: str, *args: str, timeout: float | None = 120.0, **env: str
    ) -> subprocess.CompletedProcess[str]:
        """执行 core 入口并捕获输出，供解析 JSON 回传。"""
        return self.run_module_capture(self.core_module(entrypoint), *args, timeout=timeout, **env)

    def run_module(self, module: str, *args: str, **env: str) -> int:
        """执行任意模块并返回退出码，标准流直接继承。"""
        return self._run(self.module_argv(module, *args), **env)

    def run_module_capture(
        self, module: str, *args: str, timeout: float | None = 120.0, **env: str
    ) -> subprocess.CompletedProcess[str]:
        """执行任意模块并捕获输出。

        :param timeout: 超时秒数；``None`` 表示不设限（热装载 RPC 用）。
        """
        return self._capture(self.module_argv(module, *args), timeout=timeout, **env)

    def run_python_capture(
        self, *args: str, timeout: float | None = 120.0, **env: str
    ) -> subprocess.CompletedProcess[str]:
        """以实例解释器执行任意参数并捕获输出，供版本探测等一次性查询使用。"""
        return self._capture(self.python_argv(*args), timeout=timeout, **env)

    def installed(self, *, refresh: bool = False) -> dict[str, PackageInfo]:
        """经 ``registry --json`` 取得已装包清单，按规范化分发名索引。

        子进程开销可观，结果缓存在实例对象上；安装或卸载后调用 :meth:`invalidate` 失效。

        :param refresh: 为真时忽略缓存重新询问。
        :return: 分发名到包信息的映射。
        """
        if self._installed is not None and not refresh:
            return self._installed
        proc = self.run_core_capture("registry", "--json", timeout=60.0)
        if proc.returncode != 0:
            raise CoreInvocationError(
                self._explain_failure(proc, i18n.t("cli.instance.what_read_packages")),
                returncode=proc.returncode,
                stderr=proc.stderr or "",
            )
        payload = extract_json(proc.stdout or "")
        if isinstance(payload, Mapping):
            self._registry_payload = payload
        packages: dict[str, PackageInfo] = {}
        for item in _iter_package_items(payload):
            info = PackageInfo.from_mapping(item)
            if info.dist:
                packages[_canonical(info.dist)] = info
        self._installed = packages
        return packages

    def invalidate(self) -> None:
        """清空已装包缓存与 registry 回传缓存。"""
        self._installed = None
        self._registry_payload = None

    def find_package(self, name: str) -> PackageInfo | None:
        """按分发名、短名或导入路径查找已装包。"""
        packages = self.installed()
        wanted = _canonical(name)
        if wanted in packages:
            return packages[wanted]
        for info in packages.values():
            candidates = {_canonical(info.dist), _canonical(info.name), _canonical(info.import_path.rsplit(".", 1)[-1])}
            candidates.update(_canonical(module) for module in info.provides_modules)
            if wanted in candidates:
                return info
        return None

    def dependents_of(self, dist: str) -> list[PackageInfo]:
        """列出直接依赖该分发的已装包，用于卸载前的反向依赖检查。

        优先采用 core 回传的 ``dependents`` 字段；缺失时按各包声明的依赖名自行推算。
        """
        target = _canonical(dist)
        result: dict[str, PackageInfo] = {}
        for info in self.installed().values():
            if _canonical(info.dist) == target:
                continue
            if any(_canonical(name) == target for name in info.dependents):
                result[_canonical(info.dist)] = info
                continue
            if any(_canonical(dep.dist) == target for dep in info.dependencies):
                result[_canonical(info.dist)] = info
        return list(result.values())

    def api_version(self) -> int | None:
        """已装 core 的公共 API 版本；取不到时返回 ``None``。

        优先读 ``registry --json`` 的 ``core.api_version``；缺失时在实例解释器里读取
        ``akaribot.core.version.__api_version__``（仍是子进程，不在 CLI 进程内 import core）。
        """
        payload = self._registry_payload
        if payload is None:
            try:
                self.installed()
            except (CoreInvocationError, CliError):
                payload = None
            else:
                payload = self._registry_payload
        if isinstance(payload, Mapping):
            core = payload.get("core")
            if isinstance(core, Mapping):
                value = core.get("api_version")
                if isinstance(value, int):
                    return value
        code = "from akaribot.core.version import __api_version__ as v; print(v)"
        try:
            proc = self._capture(self.python_argv("-c", code), timeout=30.0)
        except CliError:
            return None
        if proc.returncode != 0:
            return None
        try:
            return int((proc.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            return None

    def is_running(self) -> bool:
        """机器人是否在运行。

        以 ``<实例根>/.bot.lock`` 的排他锁是否被持有为准（``Paths.lock`` 的定义），
        锁定探测只读文件本身，不会截断运行中进程持有的锁文件。
        """
        lock = self.root / LOCK_FILENAME
        if not lock.exists():
            return False
        try:
            handle = lock.open("rb+")
        except OSError:
            try:
                handle = lock.open("rb")
            except OSError:
                return False
        with handle:
            if is_windows():
                import msvcrt

                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError:
                    return True
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                return False
            import fcntl

            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False

    def notify_package_change(self, action: str, dist: str) -> NotifyResult:
        """把安装或卸载事件通知运行中的机器人，触发热装载。

        沿用 T5.3 的 RPC 契约 ``server.post_package_install`` / ``server.post_package_remove``，
        经假定入口 ``python -m akaribot.core.entrypoints.rpc <remote> <dist>`` 送达。
        未运行时跳过；入口缺失时只告警，安装结果不回滚。

        :param action: ``install`` 或 ``remove``。
        :param dist: 分发名。
        :return: 通知结果。
        """
        remote = {"install": "server.post_package_install", "remove": "server.post_package_remove"}.get(action)
        if remote is None:
            raise CliError(i18n.t("cli.instance.notify_unknown_action", action=action))
        if not self.is_running():
            return NotifyResult(False, False, i18n.t("cli.instance.notify_not_running"))
        try:
            proc = self.run_core_capture("rpc", remote, dist, timeout=None)
        except CliError as exc:
            return NotifyResult(True, False, i18n.t("cli.instance.notify_not_delivered", error=exc))
        if proc.returncode == 0:
            return NotifyResult(True, True, i18n.t("cli.instance.notify_delivered", remote=remote))
        detail = self._explain_failure(proc, i18n.t("cli.instance.notify_failed", remote=remote))
        return NotifyResult(True, False, detail)

    def _run(self, argv: list[str], **env: str) -> int:
        """执行命令并继承标准流。"""
        if not self.python_exists:
            raise CliError(i18n.t("cli.instance.python_missing", python=self.python))
        try:
            completed = subprocess.run(argv, env=self.core_env(**env), check=False)  # noqa: S603
        except OSError as exc:
            raise CliError(i18n.t("cli.instance.exec_failed", argv0=argv[0], error=exc)) from exc
        return completed.returncode

    def _capture(self, argv: list[str], *, timeout: float | None, **env: str) -> subprocess.CompletedProcess[str]:
        """执行命令并捕获文本输出。"""
        if not self.python_exists:
            raise CliError(i18n.t("cli.instance.python_missing", python=self.python))
        try:
            return subprocess.run(  # noqa: S603
                argv,
                env=self.core_env(**env),
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            seconds = f"{timeout:g}"
            raise CliError(i18n.t("cli.instance.timeout", seconds=seconds, command=" ".join(argv))) from exc
        except OSError as exc:
            raise CliError(i18n.t("cli.instance.exec_failed", argv0=argv[0], error=exc)) from exc

    @staticmethod
    def _explain_failure(proc: subprocess.CompletedProcess[str], prefix: str) -> str:
        """把子进程失败翻译成可执行的提示，必要时附 stderr 尾部。"""
        return explain_process_failure(proc, prefix)


def explain_process_failure(proc: subprocess.CompletedProcess[str], prefix: str) -> str:
    """把 core 子进程的失败翻译成可执行的提示，必要时附 stderr 尾部。

    :param proc: 已完成的子进程。
    :param prefix: 面向用户的前缀，说明刚才在做什么。
    :return: 完整的一句话说明。
    """
    stderr = (proc.stderr or "").strip()
    if "akaribot.core.entrypoints" in stderr and "No module named" in stderr:
        return i18n.t("cli.instance.failure_core_entrypoint", prefix=prefix)
    if "No module named 'akaribot.core" in stderr or 'No module named "akaribot.core' in stderr:
        return i18n.t("cli.instance.failure_core_missing", prefix=prefix)
    if "No module named 'akaribot.testing" in stderr or 'No module named "akaribot.testing' in stderr:
        return i18n.t("cli.instance.failure_testing_missing", prefix=prefix)
    tail = "\n".join(stderr.splitlines()[-3:])
    return i18n.t(
        "cli.instance.failure_exit_code",
        prefix=prefix,
        code=proc.returncode,
        tail=tail or i18n.t("cli.instance.no_error_output"),
    )


def _canonical(name: str) -> str:
    """分发名规范化：小写并把下划线、点号归一为连字符。"""
    return name.strip().lower().replace("_", "-").replace(".", "-")


def _iter_package_items(payload: Any) -> list[Mapping[str, Any]]:
    """从 ``registry --json`` 的多种可能结构里取出包条目列表。

    兼容顶层数组、``packages``/``entries``/``installed`` 列表、``modules`` 与 ``adapters``
    分组，以及「分发名到对象」的映射四种形态，core 侧只需命中其一。
    """
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, Mapping)]
    if not isinstance(payload, Mapping):
        return []
    items: list[Mapping[str, Any]] = []
    for key in ("packages", "entries", "installed", "items"):
        value = payload.get(key)
        if isinstance(value, Mapping):
            items.extend(_mapping_items(value))
        elif isinstance(value, list):
            items.extend(item for item in value if isinstance(item, Mapping))
    for key, kind in (("modules", "module"), ("adapters", "adapter")):
        value = payload.get(key)
        if isinstance(value, Mapping):
            for name, item in value.items():
                if isinstance(item, Mapping):
                    items.append({"kind": kind, "name": name, **item})
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, Mapping):
                    items.append({"kind": kind, **item})
    if not items and "dist" in payload:
        items.append(payload)
    return items


def _mapping_items(value: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """把「名字到对象」的映射展开为带名字的条目列表。"""
    result: list[Mapping[str, Any]] = []
    for name, item in value.items():
        if isinstance(item, Mapping):
            result.append({"name": name, **item})
    return result


def find_instance_root(start: Path | None = None) -> Path | None:
    """定位实例根：优先环境变量 ``AKARI_INSTANCE_DIR``，否则自起点向上找 ``akaribot.toml``。

    :param start: 起点目录，缺省为当前工作目录。
    :return: 实例根；未找到时为 ``None``。
    """
    override = os.environ.get(INSTANCE_DIR_ENV)
    if override:
        candidate = Path(override).expanduser()
        if (candidate / INSTANCE_META_FILENAME).is_file():
            return candidate.resolve()
        return None
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / INSTANCE_META_FILENAME).is_file():
            return candidate
    return None


def resolve_instance(
    path: Path | None = None, *, required: bool = True, python_override: Path | None = None
) -> Instance | None:
    """解析实例。

    :param path: 显式实例根；缺省时按环境变量与向上查找定位。
    :param required: 为假时未找到返回 ``None``，为真时抛出带提示的错误。
    :param python_override: 解释器替身，供测试使用。
    :return: 实例对象。
    :raises InstanceNotFound: 实例不存在而 ``required`` 为真。
    """
    if path is not None:
        root = Path(path).expanduser().resolve()
        if not (root / INSTANCE_META_FILENAME).is_file():
            if not required:
                return None
            raise InstanceNotFound(
                i18n.t(
                    "cli.instance.not_instance_root", path=root, meta=INSTANCE_META_FILENAME, hint=no_instance_hint()
                )
            )
        return Instance(root, python_override=python_override)
    override = os.environ.get(INSTANCE_DIR_ENV)
    root = find_instance_root()
    if root is None:
        if not required:
            return None
        if override:
            raise InstanceNotFound(
                i18n.t(
                    "cli.instance.not_instance_env", env=INSTANCE_DIR_ENV, path=override, meta=INSTANCE_META_FILENAME
                )
            )
        # 这条是「既没给路径也没设环境变量」的独立场景，需要完整诊断句而不只是操作提示。
        raise InstanceNotFound(i18n.t("cli.error.not_instance"))
    return Instance(root, python_override=python_override)


def require_instance(path: Path | None = None, *, python_override: Path | None = None) -> Instance:
    """命令层入口：解析实例，失败时打印提示并退出。"""
    try:
        instance = resolve_instance(path, python_override=python_override)
    except InstanceNotFound as exc:
        fail(str(exc))
    assert instance is not None
    return instance


def relative_venv_display(instance: Instance) -> str:
    """venv 路径的展示形式：托管模式显示相对路径，非托管模式显示当前解释器。"""
    if instance.managed:
        return instance.meta.venv
    return i18n.t("cli.instance.unmanaged_python", python=instance.python)
