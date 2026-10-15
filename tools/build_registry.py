"""registry.json 生成。

汇总 workspace 全部包的静态文件，产出 CLI 安装模块所需的在线清单（结构见 tasks 附录 A.3）：

    pyproject.toml       分发名、版本、简介（[project].description）、entry point 名与导入路径
    manifest.toml        requires_core_api、locales 路径、provides_modules，以及可选的平台与分类声明
    locales/<code>.json  ``<entry point 名>.help.desc``，缺失时退回 ``<entry point 名>.help``
    core/registry.py     CORE_API_VERSION，registry 顶层 core.api_version 的取值来源

成员清单与分发名口径与 tools/lint_versions.py 一致：根 pyproject 的 [tool.uv.workspace].members glob
展开，不硬编码包名。工具只读文件、不 import akaribot，未配置的实例与裸 CI 环境都能运行。

generated_at 默认取 HEAD 提交时间（SOURCE_DATE_EPOCH 与 --generated-at 可覆盖），因此输入未变时两次
运行的输出逐字节一致，registry.json 的 diff 只反映包元数据的真实变更。

用法：
    uv run python tools/build_registry.py                     # 写仓库根的 registry.json
    uv run python tools/build_registry.py --json              # 打印到 stdout
    uv run python tools/build_registry.py --dist-dir dist --dist-base-url https://host/wheels
    uv run python tools/build_registry.py --verify-against-installed --python .venv/bin/python

退出码：0 正常；2 输入不满足生成前提，或自检与交叉核对发现不一致。
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from packaging.utils import canonicalize_name

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_PYPROJECT = PROJECT_ROOT / "pyproject.toml"
DEFAULT_OUTPUT = PROJECT_ROOT / "registry.json"

MODULE_GROUP = "akaribot.modules"
ADAPTER_GROUP = "akaribot.adapters"
CORE_DISTRIBUTION = "akari-bot-core"
CORE_NAME = canonicalize_name(CORE_DISTRIBUTION)

# manifest 的 schema 与分发默认值，与 core.registry 的 PackageManifest、MANIFEST_SCHEMA 对齐。
MANIFEST_FILENAME = "manifest.toml"
MANIFEST_SCHEMA = 1
DEFAULT_REQUIRES_CORE_API = ">=1,<2"
DEFAULT_LOCALES_DIR = "locales"

REGISTRY_SCHEMA = 1
DEFAULT_LOCALE = "zh_cn"
# 模块简介的 locale 键，按序取首个命中：desc 是 module() 的 desc= 指向，help 是模块级帮助首行。
SUMMARY_KEY_TEMPLATES = ("{name}.help.desc", "{name}.help")

# manifest 未进 PackageManifest 的字段：清单里写了就照读，没写则留空。
OPTIONAL_MANIFEST_SEQUENCE_FIELDS = ("available_for", "exclude_from", "categories")

# A.3 未列出的两个键，承载本工具新增的构建产物定位信息。
ARTIFACT_FIELDS = ("url", "sha256")
ENTRY_REQUIRED_FIELDS = (
    "name",
    "dist",
    "latest",
    "summary",
    "categories",
    "requires_core_api",
    "source",
    "homepage",
    "authors",
    "available_for",
    "exclude_from",
    *ARTIFACT_FIELDS,
)
TOP_LEVEL_FIELDS = ("schema", "generated_at", "core", "modules", "adapters")

# wheel 文件名按 PEP 427 把分发名里的非字母数字字符替换为下划线。
WHEEL_NAME_ESCAPE_PATTERN = re.compile(r"[^\w\d.]+")
CORE_API_VERSION_PATTERN = re.compile(r"^CORE_API_VERSION\s*=\s*(\d+)\s*$", re.MULTILINE)
GIT_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

PackageKind = Literal["module", "adapter"]


class ConfigError(RuntimeError):
    """workspace 或包元数据不满足生成 registry 所需的结构。"""


@dataclass(frozen=True)
class Package:
    """一个 workspace 成员包。

    :param kind: ``module`` 或 ``adapter``，由 entry point 所在分组决定。
    :param name: entry point 名，也是 registry 条目的 ``name``。
    :param dist: pyproject 书写的分发名。
    :param version: 静态版本。
    :param description: ``[project].description``，简介的最后回退来源。
    :param import_path: entry point 指向的导入路径。
    :param path: 该包 pyproject.toml 的仓库根相对 POSIX 路径，报告用。
    :param root: import_path 对应的包目录。
    :param manifest: manifest.toml 的原始内容；文件缺失时为空字典。
    """

    kind: PackageKind
    name: str
    dist: str
    version: str
    description: str
    import_path: str
    path: str
    root: Path
    manifest: dict[str, Any]


def load_toml(path: Path) -> dict[str, Any]:
    """读取 TOML 文件。"""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def workspace_pyprojects() -> list[Path]:
    """按根 pyproject 的 members glob 展开成员清单，排除 exclude。"""
    workspace = load_toml(ROOT_PYPROJECT).get("tool", {}).get("uv", {}).get("workspace", {})
    excluded = {path for pattern in workspace.get("exclude", []) for path in PROJECT_ROOT.glob(pattern)}
    found: set[Path] = set()
    for pattern in workspace.get("members", []):
        for candidate in PROJECT_ROOT.glob(pattern):
            if not candidate.is_dir() or candidate in excluded:
                continue
            pyproject = candidate / "pyproject.toml"
            if pyproject.is_file():
                found.add(pyproject)
    if not found:
        raise ConfigError(f"{ROOT_PYPROJECT.name} 的 [tool.uv.workspace].members 未展开出任何成员")
    return sorted(found)


def entry_points(project: dict[str, Any], group: str, path: str) -> dict[str, str]:
    """取某个 entry point 分组的名字到导入路径映射。

    :param project: 解析后的 ``[project]`` 表。
    :param group: 分组名，如 ``akaribot.modules``。
    :param path: 出错信息里用于定位的 pyproject 路径。
    :return: 名字到导入路径的映射；分组不存在时为空字典。
    """
    groups = project.get("entry-points", {})
    found = groups.get(group)
    if found is None:
        return {}
    if not isinstance(found, dict):
        raise ConfigError(f"{path} 的 [project.entry-points.{group}] 不是表结构")
    return {str(name): str(target) for name, target in found.items()}


def package_root(pyproject: Path, import_path: str) -> Path:
    """由 entry point 的导入路径定位包目录。

    源码根优先取分发根本身，其次取分发根下的 ``src``——按固定层级拼接会在另一种布局下
    静默落空或直接报「目录不存在」。

    :param pyproject: 该分发的 pyproject.toml。
    :param import_path: entry point 的导入路径。
    :return: 导入包目录。
    """
    for base in (pyproject.parent, pyproject.parent / "src"):
        root = base
        for part in import_path.split("."):
            root = root / part
        if root.is_dir():
            return root
    raise ConfigError(f"{pyproject.name} 的 entry point {import_path} 指向的目录不存在（试过分发根与 src）")


def read_manifest(package_path: str, root: Path) -> dict[str, Any]:
    """读包内 manifest.toml；缺文件时按运行期口径取全默认值。

    schema 不认识时直接失败：运行期会退回默认值，生成期必须报出来，否则清单字段会被静默忽略。
    """
    manifest_path = root / MANIFEST_FILENAME
    if not manifest_path.is_file():
        return {}
    manifest = load_toml(manifest_path)
    declared = manifest.get("schema", MANIFEST_SCHEMA)
    if declared != MANIFEST_SCHEMA:
        raise ConfigError(f"{package_path} 的 manifest schema 为 {declared}，本工具只认识 {MANIFEST_SCHEMA}")
    return manifest


def discover_packages() -> tuple[list[Package], list[str]]:
    """遍历全部成员，按 entry point 分组归类为模块包与适配器包。

    :return: 二元组——包清单（按分发名规范化排序）；无模块与适配器 entry point 的分发名。
    """
    packages: list[Package] = []
    skipped: list[str] = []
    for pyproject in workspace_pyprojects():
        relative = pyproject.relative_to(PROJECT_ROOT).as_posix()
        project = load_toml(pyproject).get("project", {})
        dist = str(project.get("name") or "")
        if not dist:
            raise ConfigError(f"{relative} 缺少 [project].name")
        version = str(project.get("version") or "")
        if not version:
            raise ConfigError(f"{relative} 缺少静态 [project].version，registry 的 latest 无来源")

        modules = entry_points(project, MODULE_GROUP, relative)
        adapters = entry_points(project, ADAPTER_GROUP, relative)
        if len(modules) + len(adapters) != 1:
            skipped.append(dist)
            continue
        kind: PackageKind = "module" if modules else "adapter"
        name, import_path = next(iter((modules or adapters).items()))
        root = package_root(pyproject, import_path)
        packages.append(
            Package(
                kind=kind,
                name=name,
                dist=dist,
                version=version,
                description=str(project.get("description") or "").strip(),
                import_path=import_path,
                path=relative,
                root=root,
                manifest=read_manifest(relative, root),
            )
        )
    packages.sort(key=lambda item: canonicalize_name(item.dist))
    return packages, skipped


def provides(package: Package) -> list[str]:
    """条目声明的可安装单元：模块包取清单的 provides_modules，适配器取自身名字。"""
    if package.kind == "adapter":
        return [package.name]
    declared = package.manifest.get("provides_modules", [])
    if not isinstance(declared, list) or not declared:
        raise ConfigError(f"{package.path} 的 manifest 未声明 provides_modules，模块名无来源")
    return [str(item) for item in declared]


def locale_summaries(package: Package) -> dict[str, str]:
    """读包内 locales 的逐语言简介。

    键取 entry point 名而非分发名：``module()`` 的 desc= 指向 ``<名字>.help.desc``，
    无该键的模块退回 ``<名字>.help``（模块级帮助首行）。
    """
    directory = package.root / str(package.manifest.get("locales") or DEFAULT_LOCALES_DIR)
    if not directory.is_dir():
        return {}
    keys = [template.format(name=package.name) for template in SUMMARY_KEY_TEMPLATES]
    summaries: dict[str, str] = {}
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ConfigError(f"{package.dist} 的 locale 文件无法解析：{path.name}：{error}") from error
        if not isinstance(payload, dict):
            continue
        for key in keys:
            text = payload.get(key)
            if isinstance(text, str) and text.strip():
                summaries[path.stem] = text.strip()
                break
    return summaries


def order_summaries(summaries: dict[str, str]) -> dict[str, str]:
    """简介按语言代码排序，默认 locale 置首，保证同一输入产出同一字节序列。"""
    ordered = {key: summaries[key] for key in sorted(summaries)}
    if DEFAULT_LOCALE in ordered:
        ordered = {DEFAULT_LOCALE: ordered[DEFAULT_LOCALE], **ordered}
    return ordered


def entry_summary(package: Package) -> dict[str, str]:
    """按 manifest 简介、locales 描述键、pyproject description 的顺序合成一句话简介。

    pyproject 的 description 只有一种语言，落在默认 locale；其余语言的缺项留空不补，
    以免把中文塞进 en_us 之类的键。
    """
    declared = package.manifest.get("summary")
    if isinstance(declared, dict) and declared:
        return order_summaries({str(key): str(value) for key, value in declared.items()})
    single = package.manifest.get("description")
    if isinstance(single, str) and single.strip():
        return {DEFAULT_LOCALE: single.strip()}

    summaries = locale_summaries(package)
    if DEFAULT_LOCALE not in summaries and package.description:
        summaries[DEFAULT_LOCALE] = package.description
    return order_summaries(summaries)


def legacy_module_map(package: Package) -> list[str]:
    """旧模块名映射：把提供的模块名的连字符换成下划线，未改名的模块得到同名映射。

    旧版按模块目录名索引（``weekly_rss``），拆包后部分模块名改用连字符（``weekly-rss``）；
    T7.1 的迁移需要旧名到新分发的完整映射，故同名项也保留。
    """
    return [name.replace("-", "_") for name in provides(package)]


def as_str_list(value: Any) -> list[str]:
    """把清单里的序列字段规整为字符串列表，单值按一元列表处理。"""
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value] if isinstance(value, list) else []


def manifest_sequences(package: Package) -> dict[str, list[str]]:
    """读清单里可选的序列字段，缺项为空列表。"""
    return {field: as_str_list(package.manifest.get(field, [])) for field in OPTIONAL_MANIFEST_SEQUENCE_FIELDS}


def wheel_artifact(package: Package, dist_dir: Path, base_url: str | None) -> tuple[str, str]:
    """在 --dist-dir 下定位该分发本次构建的 wheel，算 sha256 并拼出下载地址。

    :param package: 目标包。
    :param dist_dir: wheel 所在目录。
    :param base_url: 托管地址前缀；缺省时用 wheel 的 ``file://`` 绝对路径。
    :return: 二元组——下载地址与 sha256 十六进制摘要。
    """
    escaped = WHEEL_NAME_ESCAPE_PATTERN.sub("_", package.dist)
    matches = sorted(dist_dir.glob(f"{escaped}-{package.version}-*.whl"))
    if not matches:
        raise ConfigError(f"{dist_dir} 下找不到 {package.dist} {package.version} 的 wheel")
    if len(matches) > 1:
        names = "、".join(path.name for path in matches)
        raise ConfigError(f"{package.dist} 在 {dist_dir} 下匹配到多个 wheel：{names}")
    wheel = matches[0]
    digest = hashlib.sha256()
    with wheel.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    url = f"{base_url.rstrip('/')}/{wheel.name}" if base_url else wheel.resolve().as_uri()
    return url, digest.hexdigest()


def build_entry(package: Package, artifacts: dict[str, tuple[str, str]]) -> dict[str, Any]:
    """由包元数据构造一个 registry 条目，键序固定以便逐字节比较。"""
    url, sha256 = artifacts.get(canonicalize_name(package.dist), ("", ""))
    entry: dict[str, Any] = {
        "name": package.name,
        "dist": package.dist,
        "latest": package.version,
        "summary": entry_summary(package),
        "categories": manifest_sequences(package)["categories"],
        "requires_core_api": str(package.manifest.get("requires_core_api") or DEFAULT_REQUIRES_CORE_API),
        "source": {"type": "pypi"},
        "homepage": str(package.manifest.get("homepage") or ""),
        "authors": as_str_list(package.manifest.get("authors", [])),
        "available_for": manifest_sequences(package)["available_for"],
        "exclude_from": manifest_sequences(package)["exclude_from"],
        "url": url,
        "sha256": sha256,
    }
    if package.kind == "adapter":
        entry["provides_adapters"] = provides(package)
    else:
        entry["provides_modules"] = provides(package)
        entry["legacy_module_map"] = legacy_module_map(package)
    return entry


def core_api_version(packages: list[Package]) -> int:
    """从 core 源码静态取 CORE_API_VERSION，作为 ``api_version`` 的唯一来源。"""
    core = next((item for item in packages if canonicalize_name(item.dist) == CORE_NAME), None)
    if core is None:
        raise ConfigError(f"workspace 里没有 {CORE_DISTRIBUTION}，registry 的 core 段无来源")
    # import_path 末段是包名，其上各级依次是 modules 与 akaribot 命名空间根。
    namespace_root = core.root.parents[len(core.import_path.split(".")) - 2]
    source = namespace_root / "core" / "registry.py"
    if not source.is_file():
        raise ConfigError(f"找不到 {CORE_DISTRIBUTION} 的常量定义：{source}")
    match = CORE_API_VERSION_PATTERN.search(source.read_text(encoding="utf-8"))
    if match is None:
        raise ConfigError(f"{source} 里没有 CORE_API_VERSION 的字面量赋值")
    return int(match.group(1))


def resolve_generated_at(explicit: str | None) -> str:
    """取内容时间戳：显式参数、SOURCE_DATE_EPOCH、HEAD 提交时间依次回退。"""
    if explicit:
        return explicit
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch and epoch.strip().isdigit():
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime(GIT_TIMESTAMP_FORMAT)
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise ConfigError("无法取 HEAD 提交时间；请用 --generated-at 或 SOURCE_DATE_EPOCH 指定") from None
    stamp = datetime.fromisoformat(result.stdout.strip()).astimezone(timezone.utc)
    return stamp.strftime(GIT_TIMESTAMP_FORMAT)


def build_registry(
    packages: list[Package],
    artifacts: dict[str, tuple[str, str]],
    generated_at: str,
) -> dict[str, Any]:
    """组装完整 registry 结构。"""
    core = next((item for item in packages if canonicalize_name(item.dist) == CORE_NAME), None)
    if core is None:
        raise ConfigError(f"workspace 里没有 {CORE_DISTRIBUTION}")
    others = [item for item in packages if canonicalize_name(item.dist) != CORE_NAME]
    return {
        "schema": REGISTRY_SCHEMA,
        "generated_at": generated_at,
        "core": {"dist": core.dist, "latest": core.version, "api_version": core_api_version(packages)},
        "modules": [build_entry(item, artifacts) for item in others if item.kind == "module"],
        "adapters": [build_entry(item, artifacts) for item in others if item.kind == "adapter"],
    }


def source_module_names(package: Package) -> set[str]:
    """AST 扫描包源码里 ``module()`` 注册的名字，支持位置参数与 ``module_name=`` 两种写法。

    名字写成非常量表达式时扫不到，此时会报成「清单声明但源码未注册」，须改为字面量。
    """
    found: set[str] = set()
    for path in sorted(package.root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError) as error:
            raise ConfigError(f"{package.dist} 的源码无法解析：{path.name}：{error}") from error
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "module":
                continue
            literal = next((arg for arg in node.args if isinstance(arg, ast.Constant)), None)
            keyword = next((item.value for item in node.keywords if item.arg == "module_name"), None)
            value = literal.value if literal is not None else getattr(keyword, "value", None)
            if isinstance(value, str):
                found.add(value)
    return found


def check_manifest_sources(packages: list[Package]) -> list[str]:
    """核对清单的 provides_modules 与源码里实际注册的模块名，防止清单漂移。"""
    problems: list[str] = []
    for package in packages:
        if package.kind != "module" or canonicalize_name(package.dist) == CORE_NAME:
            continue
        declared = set(provides(package))
        actual = source_module_names(package)
        missing = sorted(declared - actual)
        extra = sorted(actual - declared)
        if missing:
            problems.append(f"{package.path}：清单声明但源码未注册 {missing}")
        if extra:
            problems.append(f"{package.path}：源码注册但清单未声明 {extra}")
    return problems


def self_check(registry: dict[str, Any]) -> list[str]:
    """结构自证：顶层键与 core 段键序、条目必填字段、提供的名字非空、分发名唯一。"""
    problems: list[str] = []
    if tuple(registry) != TOP_LEVEL_FIELDS:
        problems.append(f"顶层键序与 A.3 不符：{tuple(registry)}")
    core = registry.get("core", {})
    if set(core) != {"dist", "latest", "api_version"}:
        problems.append(f"core 段键与 A.3 不符：{sorted(core)}")
    seen: dict[str, str] = {}
    for section in ("modules", "adapters"):
        for entry in registry.get(section, []):
            label = f"{section}/{entry.get('dist', '?')}"
            missing = [field for field in ENTRY_REQUIRED_FIELDS if field not in entry]
            if missing:
                problems.append(f"{label} 缺字段：{missing}")
            provides_field = "provides_adapters" if section == "adapters" else "provides_modules"
            provided = entry.get(provides_field, [])
            if not provided:
                problems.append(f"{label} 的 {provides_field} 为空")
            if not entry.get("summary"):
                problems.append(f"{label} 没有一句话简介")
            # name 取 entry point 名，与注册名可以无关（threedsdb 包注册的是 3dsdb）。
            if not entry.get("name"):
                problems.append(f"{label} 的 name 为空")
            if len(set(provided)) != len(provided):
                problems.append(f"{label} 的 {provides_field} 有重复项")
            if bool(entry.get("url")) != bool(entry.get("sha256")):
                problems.append(f"{label} 的 url 与 sha256 只有一个非空")
            key = canonicalize_name(str(entry.get("dist", "")))
            if key in seen:
                problems.append(f"{label} 的分发名与 {seen[key]} 重复")
            seen[key] = label
    if canonicalize_name(str(core.get("dist", ""))) in seen:
        problems.append("core 的分发名同时出现在条目里")
    return problems


def installed_registry(python: str) -> dict[str, Any]:
    """在目标解释器里运行 core 的清单入口，取已装包视图用于交叉核对。"""
    command = [python, "-m", "akaribot.core.entrypoints.registry", "--json"]
    try:
        result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        detail = getattr(error, "stderr", "") or error
        raise ConfigError(f"{' '.join(command[:3])} 执行失败：{detail}") from None
    return json.loads(result.stdout)


def check_against_installed(registry: dict[str, Any], installed: dict[str, Any]) -> list[str]:
    """交叉核对 registry 与已装包视图的分发名、entry point 名与提供的模块名。"""
    problems: list[str] = []
    views: dict[str, dict[str, dict[str, Any]]] = {}
    for item in installed.get("packages", []):
        kind = "adapters" if item.get("kind") == "adapter" else "modules"
        views.setdefault(kind, {})[canonicalize_name(str(item.get("dist", "")))] = item
    for section in ("modules", "adapters"):
        built = {canonicalize_name(str(entry["dist"])): entry for entry in registry.get(section, [])}
        found = {key: value for key, value in views.get(section, {}).items() if key != CORE_NAME}
        only_built = sorted(set(built) - set(found))
        only_installed = sorted(set(found) - set(built))
        if only_built or only_installed:
            problems.append(f"{section} 分发名差异：仅 registry {only_built}，仅已装 {only_installed}")
        provides_field = "provides_adapters" if section == "adapters" else "provides_modules"
        for key in sorted(set(built) & set(found)):
            entry, view = built[key], found[key]
            if entry["name"] != view.get("name"):
                problems.append(f"{entry['dist']} 的 entry point 名不一致：{entry['name']} / {view.get('name')}")
            # 已装视图的 modules 字段对适配器为命名空间名，故适配器只比 entry point 名。
            if section == "adapters":
                continue
            declared = [str(item) for item in entry.get(provides_field, [])]
            actual = [str(item) for item in view.get("modules", [])]
            if sorted(declared) != sorted(actual):
                problems.append(f"{entry['dist']} 的模块名集合不一致：{sorted(declared)} / {sorted(actual)}")
    return problems


def dumps(registry: dict[str, Any]) -> str:
    """序列化为稳定文本：固定缩进、不转义非 ASCII、末尾换行。"""
    return json.dumps(registry, ensure_ascii=False, indent=2) + "\n"


def write_output(path: Path, text: str) -> None:
    """原子写文件，避免 CI 中途失败留下半份 registry.json。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False)
    try:
        with handle:
            handle.write(text)
        os.replace(handle.name, path)
    except BaseException:
        Path(handle.name).unlink(missing_ok=True)
        raise


def collect_artifacts(
    packages: list[Package],
    dist_dir: Path | None,
    base_url: str | None,
    allow_missing: bool,
) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """按需为每个分发算 wheel 的下载地址与校验和。

    core 不参与：A.3 的 core 段只承载分发名、版本与 API 版本，无处安放产物信息。

    :return: 二元组——分发名到（地址， sha256）的映射；缺 wheel 的分发名列表。
    """
    artifacts: dict[str, tuple[str, str]] = {}
    missing: list[str] = []
    if dist_dir is None:
        return artifacts, missing
    if not dist_dir.is_dir():
        raise ConfigError(f"--dist-dir 不是目录：{dist_dir}")
    for package in packages:
        if canonicalize_name(package.dist) == CORE_NAME:
            continue
        try:
            artifacts[canonicalize_name(package.dist)] = wheel_artifact(package, dist_dir, base_url)
        except ConfigError:
            if not allow_missing:
                raise
            missing.append(package.dist)
    return artifacts, missing


def describe(registry: dict[str, Any], skipped: list[str]) -> str:
    """生成一行运行摘要，供 stderr 使用。"""
    entries = registry["modules"] + registry["adapters"]
    counts = f"core 1、模块 {len(registry['modules'])}、适配器 {len(registry['adapters'])}"
    filled = sum(1 for entry in entries if entry["sha256"])
    artifact_note = f"，填了下载地址与校验和的条目 {filled}/{len(entries)}" if filled else "，未填下载地址与校验和"
    skipped_note = f"，跳过无模块与适配器入口点的分发 {len(skipped)} 个：{'、'.join(skipped)}" if skipped else ""
    return f"registry.json 已生成：{counts}{artifact_note}{skipped_note}。"


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(
        description="由 workspace 各包的 pyproject、manifest 与 locales 生成 registry.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--output", metavar="PATH", type=Path, help="输出路径，默认仓库根的 registry.json")
    parser.add_argument("--json", action="store_true", help="打印到 stdout；同时给出 --output 时两处都写")
    parser.add_argument("--dist-dir", metavar="DIR", type=Path, help="wheel 所在目录，用于填下载地址与 sha256")
    parser.add_argument("--dist-base-url", metavar="URL", help="wheel 的托管地址前缀，缺省用 file:// 绝对路径")
    parser.add_argument(
        "--allow-missing-artifacts",
        action="store_true",
        help="--dist-dir 下缺 wheel 的包留空而跳过，不视为错误",
    )
    parser.add_argument("--generated-at", metavar="TIMESTAMP", help="覆盖 generated_at，便于可复现构建")
    parser.add_argument(
        "--verify-against-installed",
        action="store_true",
        help="与该解释器里已装包的 registry --json 输出交叉核对",
    )
    parser.add_argument("--python", metavar="PATH", default=sys.executable, help="交叉核对使用的解释器")
    return parser


def main(argv: list[str] | None = None) -> int:
    """入口。返回进程退出码，0 表示生成的 registry 通过全部自检。"""
    args = build_parser().parse_args(argv)
    try:
        packages, skipped = discover_packages()
        artifacts, missing = collect_artifacts(
            packages,
            args.dist_dir,
            args.dist_base_url,
            args.allow_missing_artifacts,
        )
        registry = build_registry(packages, artifacts, resolve_generated_at(args.generated_at))
        problems = self_check(registry) + check_manifest_sources(packages)
    except (ConfigError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"无法生成 registry：{error}", file=sys.stderr)
        return 2

    if args.verify_against_installed:
        try:
            problems.extend(check_against_installed(registry, installed_registry(args.python)))
        except (ConfigError, json.JSONDecodeError) as error:
            print(f"交叉核对无法完成：{error}", file=sys.stderr)
            return 2
    if missing:
        print(f"注意：{args.dist_dir} 下缺 wheel 的分发 {len(missing)} 个：{'、'.join(missing)}", file=sys.stderr)
    if problems:
        for problem in problems:
            print(f"自检失败：{problem}", file=sys.stderr)
        return 2

    text = dumps(registry)
    if args.json:
        sys.stdout.write(text)
    if args.output or not args.json:
        output = args.output or DEFAULT_OUTPUT
        try:
            write_output(output, text)
        except OSError as error:
            print(f"写入 {output} 失败：{error}", file=sys.stderr)
            return 2
        print(f"{describe(registry, skipped)}写入 {output}", file=sys.stderr)
    else:
        print(describe(registry, skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
