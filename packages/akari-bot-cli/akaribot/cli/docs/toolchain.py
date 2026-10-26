"""Node 工具链：探测、依赖安装与 VitePress 构建。

依赖固定在模板的 ``package-lock.json`` 里，安装只执行 ``npm ci``；构建直接调用 VitePress 的
入口脚本，不经过 shell，参数顺序与日志都可预测。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Callable, Sequence

from .model import DocsError, ToolchainInfo

MIN_NODE_MAJOR = 18
VITEPRESS_VERSION = "1.6.4"
NPM_INSTALL_ARGS = ("ci", "--no-audit", "--no-fund")
TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
VITEPRESS_BIN = Path("node_modules") / "vitepress" / "bin" / "vitepress.js"
VITEPRESS_PACKAGE = Path("node_modules") / "vitepress" / "package.json"
_NODE_VERSION_PATTERN = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
_LOG_TAIL_LIMIT = 2000

Runner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]


def detect() -> ToolchainInfo:
    """探测本机的 node 与 npm。"""
    node = shutil.which("node") or ""
    npm = shutil.which("npm") or ""
    node_version = _probe(node, "--version") if node else ""
    npm_version = _probe(npm, "--version") if npm else ""
    major = parse_node_major(node_version)
    if not node:
        return ToolchainInfo(node, npm, node_version, npm_version, False, "node not found")
    if major is None:
        return ToolchainInfo(node, npm, node_version, npm_version, False, f"node version unreadable: {node_version}")
    if major < MIN_NODE_MAJOR:
        return ToolchainInfo(node, npm, node_version, npm_version, False, f"node {node_version} < {MIN_NODE_MAJOR}")
    if not npm:
        return ToolchainInfo(node, npm, node_version, npm_version, False, "npm not found")
    return ToolchainInfo(node, npm, node_version, npm_version, True, f"node {node_version}, npm {npm_version}")


def parse_node_major(version: str) -> int | None:
    """从 ``v24.21.0`` 形式的输出里取主版本号。"""
    match = _NODE_VERSION_PATTERN.search(version or "")
    return int(match.group(1)) if match else None


def ensure_toolchain(
    cache_dir: Path, template_dir: Path = TEMPLATE_DIR, offline: bool = False, runner: Runner | None = None
) -> Path:
    """准备 ``<cache>/docs`` 下的 Node 依赖，返回该目录。

    :param cache_dir: 实例缓存目录，依赖装在它的 ``docs`` 子目录。
    :param template_dir: 含 ``package.json`` 与 ``package-lock.json`` 的模板目录。
    :param offline: 只接受已装依赖，不执行 ``npm ci``。
    :param runner: 子进程执行器，测试可注入。
    :raises DocsError: 模板缺文件、离线且依赖缺失，或安装失败。
    """
    target = Path(cache_dir) / "docs"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("package.json", "package-lock.json"):
        origin = Path(template_dir) / name
        if not origin.is_file():
            raise DocsError("cli.docs.error.install_failed", reason=f"template is missing {name}", path=str(origin))
        shutil.copy2(origin, target / name)
    if (target / VITEPRESS_BIN).is_file() and _installed_version(target) == VITEPRESS_VERSION:
        return target
    if offline:
        raise DocsError(
            "cli.docs.error.install_failed",
            reason=f"offline mode requires vitepress {VITEPRESS_VERSION}",
            path=str(target / "node_modules"),
        )
    run = runner or _default_runner
    proc = run(package_argv("npm", *NPM_INSTALL_ARGS), target)
    if proc.returncode != 0:
        raise DocsError("cli.docs.error.install_failed", reason=_tail(proc.stderr or proc.stdout), path=str(target))
    if not (target / VITEPRESS_BIN).is_file():
        raise DocsError("cli.docs.error.install_failed", reason="vitepress binary is missing", path=str(target))
    return target


def build_argv(docs_dir: Path, src_dir: Path, out_dir: Path) -> list[str]:
    """组装 VitePress 构建命令。"""
    node = shutil.which("node") or "node"
    return [
        node,
        str(Path(docs_dir) / VITEPRESS_BIN),
        "build",
        str(src_dir),
        "--outDir",
        str(out_dir),
    ]


def run_build(docs_dir: Path, src_dir: Path, out_dir: Path, runner: Runner | None = None) -> str:
    """执行构建并返回标准输出。

    :raises DocsError: VitePress 入口缺失或构建失败。
    """
    binary = Path(docs_dir) / VITEPRESS_BIN
    if not binary.is_file():
        raise DocsError("cli.docs.error.install_failed", reason="vitepress binary is missing", path=str(binary))
    argv = build_argv(docs_dir, src_dir, out_dir)
    proc = (runner or _default_runner)(argv, Path(docs_dir))
    if proc.returncode != 0:
        raise DocsError("cli.docs.error.build_failed", reason=_tail(proc.stderr or proc.stdout), path=str(out_dir))
    return proc.stdout or ""


def template_version(template_dir: Path = TEMPLATE_DIR) -> str:
    """读取模板 ``package.json`` 的版本号，供构建指纹使用。"""
    try:
        payload = json.loads((Path(template_dir) / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    return str(payload.get("version", ""))


def package_argv(executable: str, *args: str, windows: bool | None = None) -> list[str]:
    """组装包管理器命令；Windows 下 npm 是批处理脚本，须经 ``cmd /c`` 启动。"""
    if (os.name == "nt" if windows is None else windows) and executable == "npm":
        return ["cmd", "/c", executable, *args]
    return [executable, *args]


def _installed_version(docs_dir: Path) -> str:
    try:
        payload = json.loads((Path(docs_dir) / VITEPRESS_PACKAGE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    return str(payload.get("version", ""))


def _probe(executable: str, flag: str) -> str:
    try:
        proc = subprocess.run(  # noqa: S603 - 参数为固定可执行文件与版本旗标
            [executable, flag],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return (proc.stdout or "").strip().splitlines()[0].strip() if proc.returncode == 0 else ""


def _default_runner(argv: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603 - 命令由本模块组装，不含用户输入
        list(argv),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def _tail(text: str | None) -> str:
    content = (text or "").strip()
    return content[-_LOG_TAIL_LIMIT:] if content else "command failed"
