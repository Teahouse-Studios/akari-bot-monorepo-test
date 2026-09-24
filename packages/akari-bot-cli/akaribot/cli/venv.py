"""uv 安装命令的拼装、安装源解析与实例 venv 托管。

本模块只经子进程调用 uv（``uv pip install --python <解释器>``），CLI 进程不 import core、不 import pip。
adopt / release 的步骤顺序不可颠倒，理由见 :func:`adopt` 与 :func:`release` 的文档串。
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys

from rich.markup import escape
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import httpx
import tomllib
from packaging.requirements import InvalidRequirement, Requirement
from packaging.version import InvalidVersion, Version

from akaribot.cli import i18n
from akaribot.cli.instance import (
    system_python,
    DEFAULT_REGISTRY_SOURCE,
    CliError,
    Instance,
    console,
    err_console,
    explain_process_failure,
    extract_json,
    ok,
    step,
    venv_python_path,
    warn,
)

UV_ENV_VAR = "AKARIBOT_UV"
CACHE_DIR_ENV = "AKARIBOT_CACHE_DIR"
PROBE_NAMES_ENV = "AKARI_PROBE_NAMES"
REGISTRY_CACHE_TTL = 3600.0
# 实时转发时保留的末尾行数，供失败时摘要使用。
STREAM_TAIL_LINES = 40
CLI_DIST = "akari-bot-cli"
CORE_DIST = "akari-bot-core"
AKARIBOT_PREFIX = "akari-bot-"
AKARIBOT_ENTRY_POINT_GROUPS = ("akaribot.modules", "akaribot.adapters")
WORKSPACE_PYPROJECT_PATTERNS = ("packages/*/pyproject.toml", "packages/*/*/pyproject.toml")
MANIFEST_FILENAME = "manifest.toml"
# 清单未声明 requires_core_api 时的默认区间；与 core.registry.PackageManifest 及
# tools/build_registry.py 的 DEFAULT_REQUIRES_CORE_API 同口径，工作区视图与 registry 视图必须一致。
DEFAULT_REQUIRES_CORE_API = ">=1"
# 内置 uv 的文件名：Windows 上必须是带 .exe 的完整名，CreateProcess 不接受无扩展名的可执行文件。
UV_BUNDLED_NAME = "uv"
UV_BUNDLED_WINDOWS_NAME = "uv.exe"
UV_WINDOWS_SUFFIXES = (".exe", ".com", ".bat", ".cmd")
# 冻结后本文件落在解包目录内的包层级里，资源根只在上面若干级；设上限以免把无关祖先目录当成资源根。
FROZEN_ROOT_MAX_DEPTH = 6


def canonical(name: str) -> str:
    """分发名规范化：小写并把下划线、点号归一为连字符。"""
    return name.strip().lower().replace("_", "-").replace(".", "-")


def _windows_platform() -> bool:
    return os.name == "nt"


def bundled_uv_names() -> tuple[str, ...]:
    """内置 uv 的候选文件名，按尝试顺序排列。"""
    if _windows_platform():
        return (UV_BUNDLED_WINDOWS_NAME, UV_BUNDLED_NAME)
    return (UV_BUNDLED_NAME,)


def is_executable(path: Path) -> bool:
    """判断路径是否为可执行文件。

    Windows 按扩展名判定；POSIX 按可执行位判定，并在缺失时补一次权限位——Nuitka onefile 解包
    不保证保留数据文件的可执行位，只看权限位会让内置 uv 被静默跳过。

    :param path: 待判定的路径。
    :return: 可作为可执行文件启动时为 ``True``。
    """
    if not path.is_file():
        return False
    if _windows_platform():
        return path.suffix.lower() in UV_WINDOWS_SUFFIXES
    if os.access(path, os.X_OK):
        return True
    try:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        return False
    return os.access(path, os.X_OK)


def is_frozen() -> bool:
    """是否运行在 Nuitka 冻结产物里。

    Nuitka 会往每个被编译模块的全局名字里注入 ``__compiled__``，源码与普通安装下没有该名字。
    """
    return "__compiled__" in globals()


def frozen_candidate_dirs() -> tuple[Path, ...]:
    """冻结产物里可能承载包内资源的目录，按可信度排序。

    三个探测点都取自 Nuitka 的既有机制，不依赖任何绝对路径：``__compiled__.containing_dir`` 是
    Nuitka 直接给出的产物目录；``sys.argv[0]`` 在 standalone 下与资源同目录；本文件 ``__file__``
    在 onefile 下落在解包目录内，其父目录里必有资源根。

    :return: 去重后的候选目录。
    """
    directories: list[Path] = []
    containing = getattr(globals().get("__compiled__"), "containing_dir", None)
    if containing:
        directories.append(Path(containing))
    if sys.argv and sys.argv[0]:
        directories.append(Path(sys.argv[0]).resolve().parent)
    source = globals().get("__file__")
    if source:
        directories.extend(Path(source).resolve().parents[:FROZEN_ROOT_MAX_DEPTH])
    ordered: list[Path] = []
    for path in directories:
        if path not in ordered:
            ordered.append(path)
    return tuple(ordered)


def frozen_bundled_uv() -> Path | None:
    """定位冻结产物内置的 uv；非冻结或资源未打包时返回 ``None``。

    :return: 内置 uv 的路径。
    """
    if not is_frozen():
        return None
    for directory in frozen_candidate_dirs():
        for name in bundled_uv_names():
            candidate = directory / name
            if is_executable(candidate):
                return candidate
    return None


def frozen_resource_root() -> Path | None:
    """冻结产物承载包内资源的根目录，供后续内置资源复用。

    当前以内置 uv 作为存在性探针：``include-data-files`` 落下的资源与二进制同层，找到可执行的
    uv 即证明该目录就是资源根。

    :return: 资源根目录；非冻结或资源未打包时为 ``None``。
    """
    bundled = frozen_bundled_uv()
    return bundled.parent if bundled is not None else None


def _override_uv(value: str) -> Path | None:
    # 取值既可以是路径，也可以是 PATH 上的命令名（与 shell 用法一致）；不可用时返回 ``None``，
    # 由调用方回退到内置资源或 PATH。
    candidate = Path(value).expanduser()
    if is_executable(candidate):
        return candidate
    separators = {os.sep, os.altsep} - {None}
    if not any(separator in value for separator in separators):
        found = shutil.which(value)
        if found and is_executable(Path(found)):
            return Path(found)
    return None


def uv_binary() -> str:
    """定位 uv 可执行文件。

    顺序为显式覆盖 ``AKARIBOT_UV`` → 冻结产物内置的 uv → ``PATH``。显式覆盖排在首位：用户指定
    的来源被静默忽略比找不到 uv 更难排查。内置的排在 ``PATH`` 之前，因为冻结产物带的那一份才是
    构建时验证过的版本，用户机器上也不必预装 uv。

    :return: uv 的路径。
    :raises CliError: 三个来源都不可用，提示安装方式或环境变量。
    """
    override = os.environ.get(UV_ENV_VAR)
    if override:
        resolved = _override_uv(override)
        if resolved is not None:
            return str(resolved)
        warn(i18n.t("cli.venv_engine.uv_override_unusable", env=UV_ENV_VAR, path=override))
    bundled = frozen_bundled_uv()
    if bundled is not None:
        return str(bundled)
    found = shutil.which("uv")
    if found:
        return found
    raise CliError(i18n.t("cli.venv_engine.uv_not_found", env=UV_ENV_VAR))


def create_venv_argv(venv_dir: Path, *, python: str | None = None, clear: bool = False) -> list[str]:
    """``uv venv`` 的 argv；``clear`` 为真时覆盖已存在的环境。"""
    argv = [uv_binary(), "venv", str(venv_dir)]
    if clear:
        argv.append("--clear")
    if python:
        argv += ["--python", str(python)]
    return argv


def install_argv(python: Path, specs: Sequence[str], *, upgrade: bool = False) -> list[str]:
    """``uv pip install --python <解释器>`` 的 argv。"""
    argv = [uv_binary(), "pip", "install", "--python", str(python)]
    if upgrade:
        argv.append("--upgrade")
    argv.extend(specs)
    return argv


def uninstall_argv(python: Path, dists: Sequence[str]) -> list[str]:
    """``uv pip uninstall --python <解释器>`` 的 argv。"""
    return [uv_binary(), "pip", "uninstall", "--python", str(python), *dists]


def dry_run_confirm_argv(python: Path, specs: Sequence[str]) -> list[str]:
    """``--dry-run`` 用的解析检查 argv：只求解依赖，不落盘。"""
    return [uv_binary(), "pip", "install", "--dry-run", "--python", str(python), *specs]


def summarize_uv_error(stderr: str, *, limit: int = 3) -> str:
    """把 uv 解析器的原始报错压缩成可读说明。

    uv 的冲突说明以 ``Because ...`` 起句，逐条列出约束来源；取前若干条即可说明矛盾，
    完整输出留给 ``--verbose``。

    :param stderr: uv 的标准错误。
    :param limit: 最多摘录的约束条数。
    :return: 面向用户的一句话说明。
    """
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    reasons = [line for line in lines if line.startswith(("Because", "The conflict is caused by", "hint:"))]
    if not reasons:
        reasons = lines[-limit:]
    picked = reasons[:limit]
    text = i18n.t("cli.common.clause_separator").join(picked) if picked else i18n.t("cli.venv_engine.uv_no_reason")
    return i18n.t("cli.venv_engine.dependency_resolve_failed", detail=text)


@dataclass
class CommandRunner:
    """外部命令的执行者。

    :param dry_run: 为真时只打印 argv，不真正执行，供自证与离线检查。
    :param verbose: 为真时连命令本身一并回显。
    """

    dry_run: bool = False
    verbose: bool = False

    def run(self, argv: Sequence[str], *, env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        """执行命令并捕获文本输出。"""
        if self.dry_run:
            console.print(f"[dim]$ {escape(' '.join(argv))}[/dim]")
            return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")
        try:
            completed = subprocess.run(  # noqa: S603
                list(argv),
                env=dict(env) if env is not None else None,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as exc:
            raise CliError(i18n.t("cli.venv_engine.exec_failed", command=argv[0], error=exc)) from exc
        if self.verbose:
            for stream in (completed.stdout, completed.stderr):
                if stream and stream.strip():
                    console.print(stream.rstrip())
        return completed

    def run_streaming(
        self, argv: Sequence[str], *, env: Mapping[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        """执行命令并实时转发输出。

        安装与卸载可能跑上几分钟（解析依赖、下载 wheel、写 venv）。若沿用 ``capture_output``，
        这段时间界面上没有任何变化，操作者无法区分「正在装」与「卡住了」。故逐行转发：uv 即使
        输出被重定向也会打印 ``Resolved … / Installed …`` 这类进度行，转发即可见。

        输出走 stderr，``--json`` 的 stdout 因此保持干净；同时保留末尾若干行供失败时摘要。
        """
        if self.dry_run:
            console.print(f"[dim]$ {escape(' '.join(argv))}[/dim]")
            return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")
        if self.verbose:
            err_console.print(f"[dim]$ {escape(' '.join(argv))}[/dim]")
        try:
            process = subprocess.Popen(  # noqa: S603
                list(argv),
                env=dict(env) if env is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except OSError as exc:
            raise CliError(i18n.t("cli.venv_engine.exec_failed", command=argv[0], error=exc)) from exc
        tail: deque[str] = deque(maxlen=STREAM_TAIL_LINES)
        for line in process.stdout or ():
            stripped = line.rstrip()
            if not stripped:
                continue
            tail.append(stripped)
            err_console.print(f"[dim]{escape(stripped)}[/dim]")
        returncode = process.wait()
        return subprocess.CompletedProcess(list(argv), returncode, stdout="", stderr="\n".join(tail))

    def run_checked(
        self, argv: Sequence[str], *, what: str, env: Mapping[str, str] | None = None, stream: bool = False
    ) -> None:
        """执行命令，失败时抛出带摘要的错误。

        :param what: 动作描述，用于成功与失败消息。
        :param stream: 为真时实时转发输出，供耗时命令显示进度。
        """
        completed = self.run_streaming(argv, env=env) if stream else self.run(argv, env=env)
        if completed.returncode != 0:
            detail = summarize_uv_error(completed.stderr or completed.stdout or "")
            raise CliError(i18n.t("cli.common.action_failed", what=what, detail=detail))
        ok(i18n.t("cli.common.action_done", what=what))


_PROBE_SCRIPT = r"""
import json, os, sys
from importlib import metadata

GROUPS = ("akaribot.modules", "akaribot.adapters")


def norm(name):
    return name.strip().lower().replace("_", "-").replace(".", "-")


wanted = {norm(item) for item in json.loads(os.environ.get("AKARI_PROBE_NAMES", "[]"))}
distributions = {}
for dist in metadata.distributions():
    raw = (dist.metadata["Name"] if dist.metadata else None) or ""
    if not raw:
        continue
    name = norm(raw)
    entry_points = {}
    try:
        for entry in dist.entry_points:
            entry_points[f"{entry.group}|{entry.name}"] = entry.value
    except Exception:
        entry_points = {}
    is_akari = name.startswith("akaribot-")
    in_groups = any(key.split("|", 1)[0] in GROUPS for key in entry_points)
    if name in distributions or not (is_akari or in_groups or name in wanted):
        continue
    info = {
        "name": raw,
        "version": dist.version or "",
        "entry_points": entry_points,
        "requires": [],
        "editable": False,
    }
    if is_akari or name in wanted:
        try:
            info["requires"] = [str(item) for item in (dist.requires or [])]
        except Exception:
            info["requires"] = []
    try:
        payload = dist.read_text("direct_url.json")
    except Exception:
        payload = None
    if payload:
        try:
            data = json.loads(payload)
        except Exception:
            data = {}
        url = data.get("url") or ""
        info["editable"] = bool((data.get("dir_info") or {}).get("editable"))
        if url.startswith("file://"):
            info["path"] = url[len("file://") :]
    distributions[name] = info
print(json.dumps({"python": sys.executable, "distributions": distributions}, sort_keys=True))
"""


@dataclass(frozen=True)
class InstalledDist:
    """目标环境里的一个已装分发。

    :param dist: 规范化分发名。
    :param version: 版本。
    :param path: 可编辑或本地安装的源目录。
    :param editable: 是否为可编辑安装。
    :param requires: metadata 里的依赖串。
    :param entry_points: ``"<group>|<name>" -> value``。
    """

    dist: str
    version: str = ""
    path: Path | None = None
    editable: bool = False
    requires: tuple[str, ...] = ()
    entry_points: Mapping[str, str] = field(default_factory=dict)

    def requirement(self) -> str:
        """重装到另一环境时使用的 uv 参数 token。"""
        if self.path is not None and self.path.exists():
            if self.editable:
                return f"--editable={self.path}"
            return str(self.path)
        if self.version:
            return f"{self.dist}=={self.version}"
        return self.dist


def _probe_env(names: Sequence[str]) -> dict[str, str]:
    result = dict(os.environ)
    result[PROBE_NAMES_ENV] = json.dumps([canonical(name) for name in names])
    result["PYTHONIOENCODING"] = "utf-8"
    return result


def probe_environment(python: Path, *, names: Sequence[str] = (), timeout: float = 120.0) -> dict[str, InstalledDist]:
    """询问目标解释器里装了哪些 akaribot 包，以及指定名字的分发详情。

    :param python: 目标解释器。
    :param names: 额外需要读取 metadata 的分发名（用于依赖冲突检查）。
    :return: 规范化分发名到已装信息的映射。
    :raises CliError: 解释器不存在或探测失败。
    """
    if not Path(python).is_file():
        raise CliError(i18n.t("cli.venv_engine.interpreter_missing", python=python))
    try:
        completed = subprocess.run(  # noqa: S603
            [str(python), "-c", _PROBE_SCRIPT],
            env=_probe_env(names),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise CliError(i18n.t("cli.venv_engine.probe_timeout", python=python)) from exc
    except OSError as exc:
        raise CliError(i18n.t("cli.venv_engine.exec_failed", command=python, error=exc)) from exc
    if completed.returncode != 0:
        tail = "\n".join((completed.stderr or "").strip().splitlines()[-3:])
        raise CliError(i18n.t("cli.venv_engine.probe_failed", python=python, code=completed.returncode, tail=tail))
    try:
        payload = extract_json(completed.stdout or "")
    except CliError as exc:
        raise CliError(i18n.t("cli.venv_engine.probe_unparsable", error=exc)) from exc
    result: dict[str, InstalledDist] = {}
    for name, item in (payload.get("distributions") or {}).items():
        path = item.get("path")
        result[canonical(name)] = InstalledDist(
            dist=canonical(name),
            version=str(item.get("version") or ""),
            path=Path(path) if path else None,
            editable=bool(item.get("editable")),
            requires=tuple(item.get("requires") or ()),
            entry_points={str(key): str(value) for key, value in (item.get("entry_points") or {}).items()},
        )
    return result


def entry_point_map(dists: Mapping[str, InstalledDist]) -> dict[str, str]:
    """把多个分发的 entry points 摊平成 ``"<dist>|group|name" -> value``。"""
    result: dict[str, str] = {}
    for dist, info in dists.items():
        for key, value in info.entry_points.items():
            result[f"{dist}|{key}"] = value
    return result


def compare_entry_points(source: Mapping[str, InstalledDist], target: Mapping[str, InstalledDist]) -> list[str]:
    """比较两侧的 entry points，返回差异描述。

    :param source: 源环境的已装包。
    :param target: 目标环境的已装包。
    :return: 差异列表；为空表示一致。
    """
    source_points = entry_point_map(source)
    target_points = entry_point_map(target)
    problems: list[str] = []
    for key, value in source_points.items():
        actual = target_points.get(key)
        if actual is None:
            problems.append(i18n.t("cli.venv_engine.entry_point_missing", name=key, value=value))
        elif actual != value:
            problems.append(i18n.t("cli.venv_engine.entry_point_mismatch", name=key, source=value, target=actual))
    return problems


def probe_api_version(python: Path) -> int | None:
    """在目标解释器里读取 core 的公共 API 版本。"""
    if not Path(python).is_file():
        return None
    code = "from akaribot.core.version import __api_version__ as v; print(v)"
    try:
        completed = subprocess.run(  # noqa: S603
            [str(python), "-c", code], check=False, capture_output=True, text=True, timeout=60.0
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    try:
        return int((completed.stdout or "").strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


@dataclass(frozen=True)
class WorkspacePackage:
    """工作区内的一个本地分发。

    :param dist: 分发名。
    :param version: ``[project].version``。
    :param path: 包根目录。
    :param dependencies: ``[project].dependencies`` 的原始串。
    :param module_names: ``akaribot.modules`` entry point 名。
    :param adapter_names: ``akaribot.adapters`` entry point 名。
    :param requires_core_api: manifest.toml 声明的 core API 区间。
    :param provides_modules: manifest.toml 声明的模块名。
    :param owned_tables: manifest.toml 声明的数据表。
    """

    dist: str
    version: str
    path: Path
    dependencies: tuple[str, ...] = ()
    module_names: tuple[str, ...] = ()
    adapter_names: tuple[str, ...] = ()
    requires_core_api: str = ""
    provides_modules: tuple[str, ...] = ()
    owned_tables: tuple[str, ...] = ()


def _read_toml(path: Path) -> dict[str, Any]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def package_root_from_entry_point(pyproject: Path, import_path: str) -> Path | None:
    """由 entry point 的导入路径定位导入包目录。

    源码根优先取分发根，其次取分发根下的 ``src``：与 ``tools/build_registry.py`` 的
    ``package_root()`` 同一口径。CLI 既不能 import core 内部，也不该在运行时依赖仓库工具，
    故按同一规则实现，并由用例与工具对拍，避免分化出第三套规则。

    :param pyproject: 该分发的 pyproject.toml。
    :param import_path: entry point 的取值，如 ``akaribot.modules.wiki``。
    :return: 导入包目录；两种布局都不存在时为 ``None``。
    """
    for base in (pyproject.parent, pyproject.parent / "src"):
        root = base
        for part in import_path.split("."):
            root = root / part
        if root.is_dir():
            return root
    return None


def entry_point_manifest(pyproject: Path, entry_points: Mapping[str, Any]) -> dict[str, Any]:
    """读入口点指向的导入包目录下的 ``manifest.toml``。

    仓库契约是 manifest 位于 entry point 指向的导入包目录，分发根下的同名文件不是清单：发现层与
    registry 生成工具都按导入路径定位包根，locales、assets、migrations 也相对它解析。多个入口点时
    取第一个能定位到包目录的清单，与生成工具「每个分发恰好一个模块或适配器入口点」的口径一致。

    :param pyproject: 该分发的 pyproject.toml。
    :param entry_points: ``[project.entry-points]`` 表。
    :return: 清单内容；定位不到包目录或文件缺失时为空字典。
    """
    for group in AKARIBOT_ENTRY_POINT_GROUPS:
        targets = entry_points.get(group)
        if not isinstance(targets, dict):
            continue
        for name in sorted(targets):
            root = package_root_from_entry_point(pyproject, str(targets[name]))
            if root is not None:
                return _read_toml(root / MANIFEST_FILENAME)
    return {}


def workspace_index(workspace_root: Path) -> dict[str, WorkspacePackage]:
    """扫描工作区内的全部分发，按规范化分发名索引。

    :param workspace_root: 工作区根目录。
    :return: 分发名到本地包信息的映射。
    """
    index: dict[str, WorkspacePackage] = {}
    for pattern in WORKSPACE_PYPROJECT_PATTERNS:
        for pyproject in sorted(workspace_root.glob(pattern)):
            data = _read_toml(pyproject)
            project = data.get("project") or {}
            dist = str(project.get("name") or "")
            if not dist:
                continue
            entry_points = (project.get("entry-points") or {}) if isinstance(project.get("entry-points"), dict) else {}
            manifest = entry_point_manifest(pyproject, entry_points)
            index[canonical(dist)] = WorkspacePackage(
                dist=dist,
                version=str(project.get("version") or ""),
                path=pyproject.parent,
                dependencies=tuple(str(item) for item in (project.get("dependencies") or ())),
                module_names=tuple((entry_points.get("akaribot.modules") or {}).keys()),
                adapter_names=tuple((entry_points.get("akaribot.adapters") or {}).keys()),
                requires_core_api=str(manifest.get("requires_core_api") or DEFAULT_REQUIRES_CORE_API),
                provides_modules=tuple(str(item) for item in (manifest.get("provides_modules") or ())),
                owned_tables=tuple(str(item) for item in (manifest.get("owned_tables") or ())),
            )
    return index


def workspace_lookup(
    index: Mapping[str, WorkspacePackage], name: str, *, kind: str | None = None
) -> WorkspacePackage | None:
    """在工作区索引里按分发名、短名或 entry point 名查找。"""
    wanted = canonical(name)
    if wanted in index:
        return index[wanted]
    prefixes = [f"akari-bot-{kind}-"] if kind else ["akari-bot-module-", "akari-bot-adapter-"]
    for prefix in prefixes:
        candidate = prefix + wanted
        if candidate in index:
            return index[candidate]
    for package in index.values():
        if wanted in {canonical(item) for item in (*package.module_names, *package.adapter_names)}:
            return package
    return None


def local_dependency_closure(index: Mapping[str, WorkspacePackage], root: WorkspacePackage) -> list[WorkspacePackage]:
    """求工作区内部的依赖闭包，按依赖先、根包后的顺序返回。

    闭包内只含工作区里的本地分发：已发布到 PyPI 的依赖仍由 uv 正常解析，
    未发布的本地分发必须显式给出路径，否则 uv 会去索引上找同名包。

    :param index: :func:`workspace_index` 的结果。
    :param root: 起始包。
    :return: 有序的本地包列表。
    """
    ordered: list[WorkspacePackage] = []
    seen: set[str] = set()

    def visit(package: WorkspacePackage) -> None:
        key = canonical(package.dist)
        if key in seen:
            return
        seen.add(key)
        for text in package.dependencies:
            try:
                requirement = Requirement(text)
            except InvalidRequirement:
                continue
            dependency = index.get(canonical(requirement.name))
            if dependency is not None:
                visit(dependency)
        ordered.append(package)

    visit(root)
    return ordered


def _spec_with_version(dist: str, version: str | None, *, extra: Sequence[str] = ()) -> str:
    base = dist + ("[" + ",".join(extra) + "]" if extra else "")
    if not version:
        return base
    if version[0] in "<>=!~":
        return f"{base}{version}"
    return f"{base}=={version}"


def _specs_for_paths(
    paths: Sequence[WorkspacePackage], *, editable: bool, extra: Sequence[str] = ()
) -> tuple[str, ...]:
    specs: list[str] = []
    for item in paths:
        suffix = ""
        if extra and item is paths[-1]:
            suffix = "[" + ",".join(extra) + "]"
        if editable:
            specs.append(f"--editable={item.path}{suffix}")
        else:
            specs.append(f"{item.path}{suffix}")
    return tuple(specs)


@dataclass(frozen=True)
class InstallTarget:
    """事先解析好的安装目标。

    :param dist: 分发名。
    :param version: 目标版本；本地路径模式下取自 pyproject。
    :param specs: 直接交给 uv 的参数 token。
    :param requires_core_api: 声明的 core API 区间。
    :param provides_modules: 该包提供的模块名。
    :param owned_tables: 该包拥有的数据表。
    :param dependencies: 该包声明的依赖串（本地可见时非空）。
    :param source: ``workspace`` / ``path`` / ``registry`` / ``dist``。
    :param editable: 是否以可编辑方式安装。
    :param path: 本地包根目录。
    """

    dist: str
    version: str = ""
    specs: tuple[str, ...] = ()
    requires_core_api: str = ""
    provides_modules: tuple[str, ...] = ()
    owned_tables: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    source: str = "registry"
    editable: bool = False
    path: Path | None = None


def path_target(
    path: Path, *, editable: bool = True, extra: Sequence[str] = (), workspace_root: Path | None = None
) -> InstallTarget:
    """由本地目录构造安装目标；目录位于工作区内时补齐本地依赖闭包。

    :param path: 包根目录。
    :param editable: 是否以可编辑方式安装。
    :param extra: 该包要装的 extra。
    :param workspace_root: 已知的工作区根；缺省时自动向上查找。
    :return: 安装目标。
    :raises CliError: 目录里没有可识别的 pyproject.toml。
    """
    root = Path(path).expanduser().resolve()
    data = _read_toml(root / "pyproject.toml")
    project = data.get("project") or {}
    dist = str(project.get("name") or "")
    if not dist:
        raise CliError(i18n.t("cli.venv_engine.no_pyproject", path=root))
    workspace = workspace_root or find_workspace_root(root)
    paths: list[WorkspacePackage] = []
    if workspace is not None:
        index = workspace_index(workspace)
        package = index.get(canonical(dist))
        if package is not None:
            paths = local_dependency_closure(index, package)
    if not paths:
        paths = [
            WorkspacePackage(
                dist=dist,
                version=str(project.get("version") or ""),
                path=root,
                dependencies=tuple(str(item) for item in (project.get("dependencies") or ())),
            )
        ]
    return InstallTarget(
        dist=dist,
        version=paths[-1].version,
        specs=_specs_for_paths(paths, editable=editable, extra=extra),
        requires_core_api=paths[-1].requires_core_api,
        provides_modules=paths[-1].provides_modules,
        owned_tables=paths[-1].owned_tables,
        dependencies=paths[-1].dependencies,
        source="workspace" if workspace is not None else "path",
        editable=editable,
        path=root,
    )


def find_workspace_root(path: Path) -> Path | None:
    """自某目录向上查找工作区根：含 ``packages`` 目录且其中有 pyproject 的目录。"""
    for candidate in (path, *path.parents):
        packages = candidate / "packages"
        if packages.is_dir() and any(packages.glob("*/pyproject.toml")):
            return candidate
    return None


def workspace_target(
    workspace_root: Path,
    name: str,
    *,
    kind: str | None = None,
    editable: bool = True,
    extra: Sequence[str] = (),
) -> InstallTarget | None:
    """在本地工作区里解析包名。

    :param workspace_root: 工作区根目录。
    :param name: 分发名、短名或 entry point 名。
    :param kind: ``module`` 或 ``adapter``，用于按前缀约束查找。
    :return: 安装目标；工作区里没有该包时为 ``None``。
    """
    index = workspace_index(workspace_root)
    package = workspace_lookup(index, name, kind=kind)
    if package is None:
        return None
    paths = local_dependency_closure(index, package)
    return InstallTarget(
        dist=package.dist,
        version=package.version,
        specs=_specs_for_paths(paths, editable=editable, extra=extra),
        requires_core_api=package.requires_core_api,
        provides_modules=package.provides_modules or tuple((*package.module_names,)),
        owned_tables=package.owned_tables,
        dependencies=package.dependencies,
        source="workspace",
        editable=editable,
        path=package.path,
    )


@dataclass(frozen=True)
class RegistryEntry:
    """registry.json 里的一条包记录（结构见 tasks 附录 A.3）。"""

    name: str
    dist: str
    latest: str = ""
    kind: str = "module"
    requires_core_api: str = ""
    provides_modules: tuple[str, ...] = ()
    legacy_module_map: tuple[str, ...] = ()
    summary: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any], *, kind: str = "module") -> RegistryEntry:
        """由一条 JSON 记录构造。"""
        summary = data.get("summary")
        return cls(
            name=str(data.get("name") or ""),
            dist=str(data.get("dist") or data.get("name") or ""),
            latest=str(data.get("latest") or data.get("version") or ""),
            kind=str(data.get("kind") or kind),
            requires_core_api=str(data.get("requires_core_api") or ""),
            provides_modules=tuple(str(item) for item in (data.get("provides_modules") or ())),
            legacy_module_map=tuple(str(item) for item in (data.get("legacy_module_map") or ())),
            summary={str(key): str(value) for key, value in summary.items()} if isinstance(summary, Mapping) else {},
        )


@dataclass
class RegistryCatalog:
    """远端 registry.json 的本地视图。"""

    entries: dict[str, RegistryEntry] = field(default_factory=dict)
    generated_at: str = ""
    source: str = ""
    from_cache: bool = False

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], *, source: str = "") -> RegistryCatalog:
        """由 registry.json 的内容构造。"""
        catalog = cls(generated_at=str(payload.get("generated_at") or ""), source=source)
        core = payload.get("core")
        if isinstance(core, Mapping):
            entry = RegistryEntry.from_mapping(core, kind="core")
            if entry.dist:
                catalog.entries[canonical(entry.dist)] = entry
        for group, kind in (("modules", "module"), ("adapters", "adapter")):
            for item in payload.get(group) or ():
                if not isinstance(item, Mapping):
                    continue
                entry = RegistryEntry.from_mapping(item, kind=kind)
                if entry.dist:
                    catalog.entries[canonical(entry.dist)] = entry
        # 兼容另一种写法：单个 packages 列表，逐项用 kind 字段分类。
        for item in payload.get("packages") or ():
            if not isinstance(item, Mapping):
                continue
            entry = RegistryEntry.from_mapping(item, kind=str(item.get("kind") or "module"))
            if entry.dist:
                catalog.entries[canonical(entry.dist)] = entry
        return catalog

    @classmethod
    def load(
        cls,
        sources: Sequence[str] = (DEFAULT_REGISTRY_SOURCE,),
        *,
        cache_dir: Path | None = None,
        ttl: float = REGISTRY_CACHE_TTL,
        offline: bool = False,
    ) -> RegistryCatalog:
        """拉取 registry.json，带 ETag 缓存；失败时回退到本地缓存。

        :param sources: 来源 URL 列表，按序尝试。
        :param cache_dir: 缓存目录，缺省为 ``$AKARIBOT_CACHE_DIR`` 或 ``~/.cache/akaribot``。
        :param ttl: 缓存的软过期秒数。
        :param offline: 为真时只用缓存。
        :return: catalog。
        :raises CliError: 全部来源不可用且没有可用缓存。
        """
        directory = cache_dir or default_cache_dir()
        cache_path = directory / "registry.json"
        stamp_path = directory / "registry.stamp.json"
        cached = _read_json(cache_path)
        if offline:
            if cached is None:
                raise CliError(i18n.t("cli.venv_engine.offline_no_cache", path=cache_path))
            return cls.from_payload(cached, source=str(cache_path)).mark_cached()
        errors: list[str] = []
        for url in sources:
            etag = ""
            stamp = _read_json(stamp_path)
            if isinstance(stamp, Mapping) and stamp.get("source") == url:
                etag = str(stamp.get("etag") or "")
            headers = {"If-None-Match": etag} if etag else {}
            try:
                response = httpx.get(url, headers=headers, timeout=15.0, follow_redirects=True)
            except httpx.HTTPError as exc:
                errors.append(i18n.t("cli.venv_engine.registry_source_error", url=url, error=exc))
                continue
            if response.status_code == 304 and cached is not None:
                return cls.from_payload(cached, source=url).mark_cached()
            if response.status_code != 200:
                errors.append(
                    i18n.t("cli.venv_engine.registry_source_error", url=url, error=f"HTTP {response.status_code}")
                )
                continue
            try:
                payload = response.json()
            except ValueError as exc:
                errors.append(
                    i18n.t(
                        "cli.venv_engine.registry_source_error",
                        url=url,
                        error=i18n.t("cli.venv_engine.registry_bad_json", error=exc),
                    )
                )
                continue
            if not isinstance(payload, Mapping):
                errors.append(i18n.t("cli.venv_engine.registry_not_object", url=url))
                continue
            directory.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            stamp_path.write_text(
                json.dumps({"source": url, "etag": response.headers.get("etag", ""), "fetched_at": time.time()}),
                encoding="utf-8",
            )
            return cls.from_payload(payload, source=url)
        if cached is not None:
            console.print(f"[yellow]{i18n.t('cli.venv_engine.registry_cache_fallback')}[/yellow]")
            return cls.from_payload(cached, source=str(cache_path)).mark_cached()
        detail = i18n.t("cli.common.clause_separator").join(errors) or i18n.t("cli.venv_engine.registry_no_source")
        raise CliError(i18n.t("cli.venv_engine.registry_unavailable", detail=detail))

    def mark_cached(self) -> RegistryCatalog:
        """标记为来自缓存。"""
        self.from_cache = True
        return self

    def find(self, name: str) -> RegistryEntry | None:
        """按分发名、短名、provides_modules 或 legacy 名查找。"""
        wanted = canonical(name)
        if wanted in self.entries:
            return self.entries[wanted]
        for entry in self.entries.values():
            names = {canonical(entry.dist), canonical(entry.name)}
            names.update(canonical(item) for item in (*entry.provides_modules, *entry.legacy_module_map))
            if wanted in names:
                return entry
        return None

    def latest(self, dist: str) -> str | None:
        """某分发在 registry 里的最新版本。"""
        entry = self.entries.get(canonical(dist))
        return entry.latest if entry and entry.latest else None


def default_cache_dir() -> Path:
    """registry 缓存目录：``$AKARIBOT_CACHE_DIR`` 优先，否则 ``~/.cache/akaribot``。"""
    override = os.environ.get(CACHE_DIR_ENV)
    if override:
        return Path(override).expanduser()
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "akaribot"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def registry_target(
    catalog: RegistryCatalog,
    name: str,
    *,
    version: str | None = None,
    kind: str | None = None,
    extra: Sequence[str] = (),
) -> InstallTarget | None:
    """在 registry 里解析包名，得到分发名与版本约束。"""
    entry = catalog.find(name)
    if entry is None:
        return None
    if kind and entry.kind not in (kind, "unknown"):
        return None
    spec_version = version or (entry.latest or None)
    return InstallTarget(
        dist=entry.dist,
        version=entry.latest,
        specs=(_spec_with_version(entry.dist, spec_version, extra=extra),),
        requires_core_api=entry.requires_core_api,
        provides_modules=entry.provides_modules,
        source="registry",
    )


def _candidate_hint(names: Sequence[str]) -> str:
    if not names:
        return ""
    return "\n" + i18n.t("cli.venv_engine.candidate_hint", names=i18n.t("cli.common.list_separator").join(names))


def available_names(
    *,
    workspace_root: Path | None = None,
    catalog: RegistryCatalog | None = None,
    kind: str | None = None,
    limit: int = 24,
) -> list[str]:
    """列出该来源下可安装的短名，供「找不到包」时直接给出候选。

    只报名字，不解释来源差异：调用方已经知道自己走的是哪条路径。

    :param workspace_root: 工作区根；非空时取本地成员。
    :param catalog: 已加载的 registry。
    :param kind: ``module`` 或 ``adapter``；``None`` 表示两者都要。
    :param limit: 最多返回多少个名字。
    :return: 排序后的短名列表。
    """
    names: list[str] = []
    if workspace_root is not None:
        for package in workspace_index(workspace_root).values():
            if canonical(package.dist) == CORE_DIST:
                continue
            if kind == "adapter" and not package.adapter_names:
                continue
            if kind == "module" and not package.module_names:
                continue
            names.extend(package.adapter_names or package.module_names)
    elif catalog is not None:
        for entry in catalog.entries.values():
            if entry.kind == "core" or (kind is not None and entry.kind != kind):
                continue
            names.append(entry.name)
    return sorted(dict.fromkeys(names))[:limit]


def resolve_target(
    name: str | None,
    *,
    workspace_root: Path | None = None,
    catalog: RegistryCatalog | None = None,
    dist: str | None = None,
    version: str | None = None,
    editable_path: Path | None = None,
    extra: Sequence[str] = (),
    kind: str | None = None,
) -> InstallTarget:
    """把命令行给出的名字解析成安装目标，工作区与 registry 两条路径共用。

    解析优先级：``-e/--editable`` 的本地目录 → 工作区本地源码 → registry → 分发名约定。

    :param name: 包名（短名或分发名）。
    :param workspace_root: 本地工作区根；非空时优先本地路径。
    :param catalog: 已加载的 registry；为 ``None`` 时跳过 registry 解析。
    :param dist: 直接指定分发名，跳过 registry 查名。
    :param version: 版本或版本区间。
    :param editable_path: ``-e`` 给出的本地目录。
    :param extra: 需要安装的 extra。
    :param kind: ``module`` 或 ``adapter``。
    :return: 安装目标。
    :raises CliError: 名字无法解析，或 registry 里没有该包。
    """
    if editable_path is not None:
        target = path_target(editable_path, editable=True, extra=extra, workspace_root=workspace_root)
        return target
    query = dist or name
    if not query:
        raise CliError(i18n.t("cli.venv_engine.package_name_required"))
    if workspace_root is not None:
        target = workspace_target(workspace_root, query, kind=kind, extra=extra)
        if target is not None and dist is None:
            return target
        if target is not None and canonical(target.dist) == canonical(dist or ""):
            return target
        if target is None and dist is None:
            raise CliError(
                i18n.t("cli.venv_engine.workspace_package_missing", root=workspace_root, name=query)
                + _candidate_hint(available_names(workspace_root=workspace_root, kind=kind))
            )
    if not dist and catalog is not None:
        target = registry_target(catalog, query, version=version, kind=kind, extra=extra)
        if target is None:
            raise CliError(
                i18n.t("cli.venv_engine.registry_package_missing", name=query)
                + _candidate_hint(available_names(catalog=catalog, kind=kind))
            )
        return target
    if not dist:
        prefix = f"akari-bot-{kind}-" if kind else "akari-bot-module-"
        dist = prefix + canonical(query)
    return InstallTarget(
        dist=dist, version=version or "", specs=(_spec_with_version(dist, version, extra=extra),), source="dist"
    )


@dataclass(frozen=True)
class VenvStatus:
    """``akaribot venv status`` 的数据。

    :param mode: ``managed`` 或 ``external``。
    :param venv_dir: 托管 venv 的目标目录。
    :param python: 当前生效的解释器。
    :param exists: 解释器是否存在。
    :param packages: 已装 akaribot 包；探测失败时为 ``None``。
    :param error: 探测失败的原因。
    """

    mode: str
    venv_dir: Path
    python: Path
    exists: bool
    packages: Mapping[str, InstalledDist] | None = None
    error: str = ""

    @property
    def package_count(self) -> int:
        """已装 akaribot 包数量。"""
        return len(self.packages or {})

    @property
    def core_version(self) -> str | None:
        """core 的版本；未装时为 ``None``。"""
        info = (self.packages or {}).get(CORE_DIST)
        return info.version if info else None


def venv_status(instance: Instance) -> VenvStatus:
    """采集 venv 状态；解释器缺失或探测失败都不抛异常，交命令层展示。"""
    mode = "managed" if instance.managed else "external"
    python = instance.python
    if not instance.python_exists:
        return VenvStatus(
            mode, instance.venv_dir, python, False, None, i18n.t("cli.venv_engine.interpreter_missing_bare")
        )
    try:
        packages = probe_environment(python)
    except CliError as exc:
        return VenvStatus(mode, instance.venv_dir, python, True, None, str(exc))
    return VenvStatus(mode, instance.venv_dir, python, True, packages)


@dataclass(frozen=True)
class HostingReport:
    """adopt / release / recreate 的结果。

    :param action: 动作名。
    :param source: 源解释器。
    :param target: 目标解释器。
    :param moved: 重装的分发名。
    :param removed_from_source: 从源环境卸载的分发名。
    :param detail: 需要用户知道的一句话。
    """

    action: str
    source: Path
    target: Path
    moved: tuple[str, ...] = ()
    removed_from_source: tuple[str, ...] = ()
    detail: str = ""


def _check_distinct(source: Path, target: Path) -> None:
    try:
        same = source.resolve() == target.resolve()
    except OSError:
        same = str(source) == str(target)
    if same:
        raise CliError(i18n.t("cli.venv_engine.same_interpreter", python=source))


def adopt(
    instance: Instance,
    *,
    runner: CommandRunner | None = None,
    host_python: Path | None = None,
    python: str | None = None,
    keep_source: bool = False,
    force: bool = False,
) -> HostingReport:
    """从「使用当前环境」切换为「CLI 托管 venv」。

    步骤顺序不可颠倒：枚举源环境已装的 akaribot 包与版本 → 目标环境全部装好 →
    验证 entry points 与源环境一致 → 最后才卸载源环境的包。先删后装一旦中途失败，
    两边都不完整，用户会在既没有可用环境、也没有可回退环境的状态下停机。

    :param instance: 目标实例。
    :param runner: 命令执行者。
    :param host_python: 源解释器，缺省为当前解释器。
    :param python: 建 venv 用的解释器，缺省与源解释器相同，以保持版本一致。
    :param keep_source: 为真时不卸载源环境的包。
    :param force: 目标 venv 已存在时是否覆盖重建。
    :return: 结果报告。
    """
    runner = runner or CommandRunner()
    source_python = Path(host_python) if host_python else system_python()
    target_python = venv_python_path(instance.venv_dir)
    _check_distinct(source_python, target_python)

    step(1, 5, i18n.t("cli.venv_engine.step_enumerate_source", python=source_python))
    source_dists = probe_environment(source_python)
    if CORE_DIST not in source_dists:
        raise CliError(i18n.t("cli.venv_engine.source_missing_core", python=source_python))
    names = i18n.t("cli.common.list_separator").join(sorted(source_dists))
    console.print("  " + i18n.t("cli.venv_engine.package_count", count=len(source_dists), names=names))

    step(2, 5, i18n.t("cli.venv_engine.step_create_and_install", venv_dir=instance.venv_dir))
    if instance.venv_dir.exists() and any(instance.venv_dir.iterdir()) and not force:
        raise CliError(i18n.t("cli.venv_engine.target_venv_exists", venv_dir=instance.venv_dir))
    runner.run_checked(
        create_venv_argv(instance.venv_dir, python=python or str(source_python), clear=force),
        what=i18n.t("cli.venv_engine.what_create_venv"),
    )
    specs = [info.requirement() for info in source_dists.values()]
    runner.run_checked(
        install_argv(target_python, specs), what=i18n.t("cli.venv_engine.what_install_to_venv"), stream=True
    )

    step(3, 5, i18n.t("cli.venv_engine.step_verify_source"))
    if runner.dry_run:
        consumed = [info.requirement() for info in source_dists.values() if canonical(info.dist) != CLI_DIST]
        plan = i18n.t("cli.common.list_separator").join(consumed) or i18n.t("cli.venv_engine.none")
        console.print(f"[dim]{i18n.t('cli.venv_engine.adopt_dry_run', names=plan)}[/dim]")
        return HostingReport(
            "adopt",
            source_python,
            target_python,
            tuple(source_dists),
            (),
            i18n.t("cli.venv_engine.detail_dry_run"),
        )
    target_dists = probe_environment(target_python)
    problems = compare_entry_points(source_dists, target_dists)
    if problems:
        for item in problems[:10]:
            console.print(f"[red]  {escape(str(item))}[/red]")
        raise CliError(i18n.t("cli.venv_engine.entry_points_mismatch_source"))
    ok(i18n.t("cli.venv_engine.entry_points_consistent", count=len(source_dists)))

    step(4, 5, i18n.t("cli.venv_engine.step_uninstall_source"))
    removed: tuple[str, ...] = ()
    if keep_source:
        console.print(f"[dim]{i18n.t('cli.venv_engine.adopt_keep_source')}[/dim]")
    else:
        removable = [info.dist for info in source_dists.values() if canonical(info.dist) != CLI_DIST]
        if CLI_DIST in {canonical(item) for item in source_dists}:
            warn(i18n.t("cli.venv_engine.keep_cli_in_source", dist=CLI_DIST))
        if removable:
            runner.run_checked(
                uninstall_argv(source_python, removable),
                what=i18n.t("cli.venv_engine.what_uninstall_from_source"),
                stream=True,
            )
            removed = tuple(removable)

    step(5, 5, i18n.t("cli.venv_engine.step_update_metadata"))
    relative = os.path.relpath(instance.venv_dir, instance.root)
    if Path(relative).is_absolute() or relative.startswith(".."):
        raise CliError(i18n.t("cli.venv_engine.venv_outside_instance", venv_dir=instance.venv_dir))
    if not runner.dry_run:
        instance.meta.set_venv(relative)
        instance.meta.save()
        instance.invalidate()
    ok(i18n.t("cli.venv_engine.switched_to_managed", venv=relative))
    return HostingReport(
        "adopt",
        source_python,
        target_python,
        tuple(source_dists),
        removed,
        i18n.t("cli.venv_engine.detail_venv_written", venv=relative),
    )


def release(
    instance: Instance,
    *,
    runner: CommandRunner | None = None,
    host_python: Path | None = None,
    keep_source: bool = False,
) -> HostingReport:
    """放弃托管：把实例 venv 里的包迁到当前环境。

    顺序与 :func:`adopt` 相同且同样是硬约束：先在目标环境装好并验证，
    之后才卸载源环境的包，中途失败时实例 venv 仍完整可用。
    """
    runner = runner or CommandRunner()
    if not instance.managed:
        raise CliError(i18n.t("cli.venv_engine.release_not_managed"))
    source_python = venv_python_path(instance.venv_dir)
    target_python = Path(host_python) if host_python else system_python()
    _check_distinct(source_python, target_python)
    if not source_python.is_file():
        raise CliError(i18n.t("cli.venv_engine.instance_venv_python_missing", python=source_python))

    step(1, 4, i18n.t("cli.venv_engine.step_enumerate_venv", python=source_python))
    source_dists = probe_environment(source_python)
    if not source_dists:
        raise CliError(i18n.t("cli.venv_engine.instance_venv_no_packages", venv_dir=instance.venv_dir))
    names = i18n.t("cli.common.list_separator").join(sorted(source_dists))
    console.print("  " + i18n.t("cli.venv_engine.package_count", count=len(source_dists), names=names))

    step(2, 4, i18n.t("cli.venv_engine.step_install_current", python=target_python))
    specs = [info.requirement() for info in source_dists.values()]
    runner.run_checked(
        install_argv(target_python, specs), what=i18n.t("cli.venv_engine.what_install_to_current"), stream=True
    )

    step(3, 4, i18n.t("cli.venv_engine.step_verify_venv"))
    if runner.dry_run:
        console.print(f"[dim]{i18n.t('cli.venv_engine.release_dry_run')}[/dim]")
        return HostingReport(
            "release",
            source_python,
            target_python,
            tuple(source_dists),
            (),
            i18n.t("cli.venv_engine.detail_dry_run"),
        )
    target_dists = probe_environment(target_python)
    problems = compare_entry_points(source_dists, target_dists)
    if problems:
        for item in problems[:10]:
            console.print(f"[red]  {escape(str(item))}[/red]")
        raise CliError(i18n.t("cli.venv_engine.entry_points_mismatch_venv"))
    ok(i18n.t("cli.venv_engine.entry_points_consistent", count=len(source_dists)))

    step(4, 4, i18n.t("cli.venv_engine.step_uninstall_venv_and_metadata"))
    removed: tuple[str, ...] = ()
    if keep_source:
        console.print(f"[dim]{i18n.t('cli.venv_engine.release_keep_source')}[/dim]")
    else:
        running_inside = target_python.resolve() == source_python.resolve()
        removable = [
            info.dist for info in source_dists.values() if not (running_inside and canonical(info.dist) == CLI_DIST)
        ]
        if running_inside and len(removable) != len(source_dists):
            warn(i18n.t("cli.venv_engine.keep_cli_in_venv", dist=CLI_DIST))
        if removable:
            runner.run_checked(
                uninstall_argv(source_python, removable),
                what=i18n.t("cli.venv_engine.what_uninstall_from_venv"),
                stream=True,
            )
            removed = tuple(removable)
    instance.meta.set_venv("")
    instance.meta.save()
    instance.invalidate()
    ok(i18n.t("cli.venv_engine.switched_to_external", venv_dir=instance.venv_dir))
    return HostingReport(
        "release",
        source_python,
        target_python,
        tuple(source_dists),
        removed,
        i18n.t("cli.venv_engine.detail_venv_cleared"),
    )


def recreate(
    instance: Instance,
    *,
    runner: CommandRunner | None = None,
    python: str | None = None,
    force: bool = False,
) -> HostingReport:
    """重建实例 venv，用于 Python 升级后修复。

    新环境在临时目录里装好并验证通过后才与旧目录换位，失败时旧 venv 原样保留。
    """
    runner = runner or CommandRunner()
    if not instance.managed:
        raise CliError(i18n.t("cli.venv_engine.recreate_not_managed"))
    old_python = venv_python_path(instance.venv_dir)
    if not old_python.is_file():
        raise CliError(i18n.t("cli.venv_engine.recreate_python_missing", python=old_python))

    step(1, 4, i18n.t("cli.venv_engine.step_enumerate_existing"))
    source_dists = probe_environment(old_python)
    names = i18n.t("cli.common.list_separator").join(sorted(source_dists))
    console.print("  " + i18n.t("cli.venv_engine.package_count", count=len(source_dists), names=names))

    staging = instance.venv_dir.with_name(instance.venv_dir.name + ".new")
    step(2, 4, i18n.t("cli.venv_engine.step_create_staging", staging=staging))
    if staging.exists():
        if not force:
            raise CliError(i18n.t("cli.venv_engine.staging_exists", staging=staging))
        shutil.rmtree(staging)
    interpreter = Path(python) if python else system_python()
    console.print("  " + i18n.t("cli.venv_engine.new_interpreter", python=interpreter))
    runner.run_checked(
        create_venv_argv(staging, python=interpreter), what=i18n.t("cli.venv_engine.what_create_new_venv")
    )
    specs = [info.requirement() for info in source_dists.values()]
    runner.run_checked(
        install_argv(venv_python_path(staging), specs),
        what=i18n.t("cli.venv_engine.what_install_to_new_venv"),
        stream=True,
    )

    step(3, 4, i18n.t("cli.venv_engine.step_verify_new_venv"))
    if runner.dry_run:
        console.print(f"[dim]{i18n.t('cli.venv_engine.recreate_dry_run')}[/dim]")
        return HostingReport(
            "recreate",
            old_python,
            venv_python_path(staging),
            tuple(source_dists),
            (),
            i18n.t("cli.venv_engine.detail_dry_run"),
        )
    target_dists = probe_environment(venv_python_path(staging))
    problems = compare_entry_points(source_dists, target_dists)
    if problems:
        for item in problems[:10]:
            console.print(f"[red]  {escape(str(item))}[/red]")
        raise CliError(i18n.t("cli.venv_engine.entry_points_mismatch_new", staging=staging))

    step(4, 4, i18n.t("cli.venv_engine.step_swap_and_cleanup"))
    retired = instance.venv_dir.with_name(instance.venv_dir.name + ".old")
    if retired.exists():
        shutil.rmtree(retired)
    instance.venv_dir.rename(retired)
    staging.rename(instance.venv_dir)
    shutil.rmtree(retired, ignore_errors=True)
    instance.invalidate()
    ok(i18n.t("cli.venv_engine.venv_recreated", venv_dir=instance.venv_dir))
    return HostingReport(
        "recreate",
        old_python,
        venv_python_path(instance.venv_dir),
        tuple(source_dists),
        (),
        i18n.t("cli.venv_engine.detail_old_venv_removed"),
    )


def dependency_conflicts(
    candidate: InstallTarget,
    installed: Mapping[str, InstalledDist],
) -> list[str]:
    """在下载前把待装包与已装环境做一次依赖对称检查。

    两侧都查：待装包的依赖是否被已装版本满足，以及已装包的依赖是否被待装版本满足。
    发现的矛盾以「谁要求什么、实际是什么」的可读形式返回，不把 uv 解析器原始报错抛给用户。

    :param candidate: 待装目标；``dependencies`` 与 ``version`` 仅在本地模式可读。
    :param installed: 目标环境的已装包。
    :return: 冲突说明列表；为空表示预检通过。
    """
    problems: list[str] = []
    candidate_key = canonical(candidate.dist)
    for text in candidate.dependencies:
        try:
            requirement = Requirement(text)
        except InvalidRequirement:
            continue
        info = installed.get(canonical(requirement.name))
        if (
            info is not None
            and requirement.specifier
            and not requirement.specifier.contains(info.version, prereleases=True)
        ):
            problems.append(
                i18n.t(
                    "cli.venv_engine.conflict_candidate_needs",
                    dist=candidate.dist,
                    requirement=requirement.name,
                    specifier=requirement.specifier,
                    version=info.version,
                )
            )
    for info in installed.values():
        for text in info.requires:
            try:
                requirement = Requirement(text)
            except InvalidRequirement:
                continue
            if canonical(requirement.name) != candidate_key or not requirement.specifier:
                continue
            if candidate.version:
                try:
                    satisfied = requirement.specifier.contains(Version(candidate.version), prereleases=True)
                except InvalidVersion:
                    satisfied = True
                if not satisfied:
                    problems.append(
                        i18n.t(
                            "cli.venv_engine.conflict_installed_needs_pending",
                            installed=info.dist,
                            requirement=requirement.name,
                            specifier=requirement.specifier,
                            version=candidate.version,
                        )
                    )
            elif not requirement.specifier.contains(info.version, prereleases=True):
                problems.append(
                    i18n.t(
                        "cli.venv_engine.conflict_installed_needs_conflict",
                        installed=info.dist,
                        requirement=requirement.name,
                        specifier=requirement.specifier,
                    )
                )
    return problems


def installed_api_requirements(candidate: InstallTarget, installed: Mapping[str, InstalledDist]) -> list[str]:
    """列出已装包中要求「待装分发」的那些依赖串，供冲突说明引用。"""
    candidate_key = canonical(candidate.dist)
    result: list[str] = []
    for info in installed.values():
        for text in info.requires:
            try:
                requirement = Requirement(text)
            except InvalidRequirement:
                continue
            if canonical(requirement.name) == candidate_key:
                result.append(
                    i18n.t(
                        "cli.venv_engine.requires_line",
                        dist=info.dist,
                        requirement=requirement.name,
                        specifier=requirement.specifier,
                    )
                )
    return result


def run_core_checked(instance: Instance, entrypoint: str, *args: str, what: str) -> None:
    """执行 core 入口，失败时抛出带解释的错误。

    :param instance: 目标实例。
    :param entrypoint: 入口名。
    :param what: 动作描述。
    """
    proc = instance.run_core_capture(entrypoint, *args, timeout=None)
    if proc.returncode != 0:
        raise CliError(explain_process_failure(proc, what))
    ok(i18n.t("cli.common.action_done", what=what))


@dataclass(frozen=True)
class ConfigSnapshot:
    """安装前对 ``config/`` 目录的快照，用于失败回滚。

    :param files: 相对实例根的 POSIX 路径到文件内容的映射。
    """

    files: Mapping[str, bytes]

    @classmethod
    def take(cls, instance: Instance) -> ConfigSnapshot:
        """抓取当前配置目录的快照。"""
        files: dict[str, bytes] = {}
        config_dir = instance.config_dir
        if config_dir.is_dir():
            for path in sorted(config_dir.rglob("*")):
                if path.is_file():
                    files[path.relative_to(instance.root).as_posix()] = path.read_bytes()
        return cls(files=files)

    def changed_paths(self, instance: Instance) -> tuple[Path, ...]:
        """列出快照之后新增或内容有变的配置文件。"""
        changed: list[Path] = []
        for relative, content in self.files.items():
            path = instance.root / relative
            if not path.is_file() or path.read_bytes() != content:
                changed.append(path)
        current = instance.config_dir
        if current.is_dir():
            for path in sorted(current.rglob("*")):
                if path.is_file() and path.relative_to(instance.root).as_posix() not in self.files:
                    changed.append(path)
        return tuple(changed)

    def restore(self, instance: Instance) -> tuple[Path, ...]:
        """把配置目录恢复到快照状态，返回被动过的文件。"""
        touched: list[Path] = []
        for relative, content in self.files.items():
            path = instance.root / relative
            if not path.is_file() or path.read_bytes() != content:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                touched.append(path)
        current = instance.config_dir
        if current.is_dir():
            for path in sorted(current.rglob("*"), reverse=True):
                if path.is_file() and path.relative_to(instance.root).as_posix() not in self.files:
                    path.unlink()
                    touched.append(path)
            for path in sorted(current.rglob("*"), reverse=True):
                if path.is_dir() and not any(path.iterdir()):
                    path.rmdir()
        return tuple(touched)


PLACEHOLDER_MARKER = "<Replace me>"


def count_placeholders(paths: Sequence[Path]) -> int:
    """统计给定配置文件里 ``<Replace me>`` 占位符的个数。"""
    total = 0
    for path in paths:
        try:
            total += path.read_text(encoding="utf-8").count(PLACEHOLDER_MARKER)
        except (OSError, UnicodeDecodeError):
            continue
    return total


def config_sync(instance: Instance, dist: str) -> None:
    """第 4 步：补写该包的配置。

    补写必须发生在 CLI 子进程：机器人与 server 一律以只读配置运行，
    ``CFGManager._ensure_writable()`` 会拒绝它们写入（tasks T5.2 的硬约束）。
    调用方应在调用前抓取 :class:`ConfigSnapshot`，以便失败时回滚本次写入。
    """
    run_core_checked(
        instance, "config", "sync", "--package", dist, what=i18n.t("cli.venv_engine.what_config_sync", dist=dist)
    )


def db_upgrade(instance: Instance, dist: str) -> None:
    """第 5 步：应用该包自己的数据库迁移。"""
    run_core_checked(
        instance, "db", "upgrade", "--package", dist, what=i18n.t("cli.venv_engine.what_db_upgrade", dist=dist)
    )


PURGE_REASON_KEYS = ("error", "errors", "failures", "failed")
PURGE_TABLE_STATUS_KEYS = ("table", "name")


def _text_of(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Mapping):
        for key in ("message", "reason", "detail", "error", "code"):
            text = value.get(key)
            if isinstance(text, str) and text.strip():
                return text.strip()
    return ""


def purge_failure_reasons(payload: Any) -> tuple[str, ...]:
    """从 ``db purge --json`` 的回传里提取逐项失败原因。

    结构化错误的键名与嵌套形状由 core 侧定义，此处按「整体错误 → 逐表错误」的顺序收敛成可读行，
    认不出的结构一律忽略，由调用方退回 stderr 摘要，避免把不可读的原始输出抛给用户。

    :param payload: ``--json`` 回传解析出的对象。
    :return: 去重后的失败原因，每项一行。
    """
    if not isinstance(payload, Mapping):
        return ()
    reasons: list[str] = []
    for key in PURGE_REASON_KEYS:
        value = payload.get(key)
        for item in value if isinstance(value, list) else [value]:
            text = _text_of(item)
            if text:
                reasons.append(text)
    tables = payload.get("tables")
    for item in tables if isinstance(tables, list) else []:
        if not isinstance(item, Mapping) or item.get("ok") is True:
            continue
        status = str(item.get("status") or "")
        if status in ("ok", "dropped", "skipped"):
            continue
        text = _text_of(item)
        if not text:
            continue
        table = next((str(item[key]) for key in PURGE_TABLE_STATUS_KEYS if item.get(key)), "")
        reasons.append(f"{table}: {text}" if table else text)
    return tuple(dict.fromkeys(reasons))


def db_purge(instance: Instance, dist: str) -> bool:
    """删除该包拥有的数据表，返回是否成功。

    core 侧以 ``db purge --package <分发> --json`` 执行：失败时非零退出并回传结构化原因，这里把
    原因逐条打印出来，命令层才能逐项显示成功与失败，而不是只留一句「退出码 1」。

    :param instance: 目标实例。
    :param dist: 分发名。
    :return: 删除成功为 ``True``。
    """
    proc = instance.run_core_capture("db", "purge", "--package", dist, "--json", timeout=None)
    if proc.returncode == 0:
        ok(i18n.t("cli.venv_engine.tables_purged", dist=dist))
        return True
    reasons = purge_failure_reasons(extract_json(proc.stdout or ""))
    if reasons:
        for reason in reasons:
            warn(i18n.t("cli.venv_engine.tables_purge_failed", dist=dist, reason=reason))
    else:
        warn(explain_process_failure(proc, i18n.t("cli.venv_engine.what_purge_tables", dist=dist)))
    return False
