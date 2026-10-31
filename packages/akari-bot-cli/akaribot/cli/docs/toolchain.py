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
from .theme import ThemeSpec

MIN_NODE_MAJOR = 18
VITEPRESS_VERSION = "1.6.4"
NPM_INSTALL_ARGS = ("ci", "--no-audit", "--no-fund")
NPM_INSTALL_PLAIN_ARGS = ("install", "--no-audit", "--no-fund")
TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
VITEPRESS_BIN = Path("node_modules") / "vitepress" / "bin" / "vitepress.js"
VITEPRESS_PACKAGE = Path("node_modules") / "vitepress" / "package.json"
THEME_STAMP = ".akaribot-theme.json"
_NODE_VERSION_PATTERN = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_LOG_TAIL_LIMIT = 2000

Runner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]
LogSink = Callable[[str], None]


def detect(min_major: int = MIN_NODE_MAJOR) -> ToolchainInfo:
    """探测本机的 node 与 npm。

    :param min_major: 主题要求的 Node 主版本下限。
    """
    node = shutil.which("node") or ""
    npm = shutil.which("npm") or ""
    node_version = _probe(node, "--version") if node else ""
    npm_version = _probe(npm, "--version") if npm else ""
    major = parse_node_major(node_version)
    if not node:
        return ToolchainInfo(node, npm, node_version, npm_version, False, "node not found")
    if major is None:
        return ToolchainInfo(node, npm, node_version, npm_version, False, f"node version unreadable: {node_version}")
    if major < min_major:
        return ToolchainInfo(node, npm, node_version, npm_version, False, f"node {node_version} < {min_major}")
    if not npm:
        return ToolchainInfo(node, npm, node_version, npm_version, False, "npm not found")
    return ToolchainInfo(node, npm, node_version, npm_version, True, f"node {node_version}, npm {npm_version}")


def parse_node_major(version: str) -> int | None:
    """从 ``v24.21.0`` 形式的输出里取主版本号。"""
    match = _NODE_VERSION_PATTERN.search(version or "")
    return int(match.group(1)) if match else None


def ensure_toolchain(
    cache_dir: Path,
    template_dir: Path | None = None,
    offline: bool = False,
    runner: Runner | None = None,
    *,
    theme: ThemeSpec | None = None,
    log: LogSink | None = None,
) -> Path:
    """准备 ``<cache>/docs`` 下的 Node 依赖，返回该目录。

    :param cache_dir: 实例缓存目录，依赖装在它的 ``docs`` 子目录。
    :param template_dir: 兼容参数；未给 ``theme`` 时以该目录构造内置主题。
    :param offline: 只接受已装依赖，不执行安装。
    :param runner: 子进程执行器，测试可注入。
    :param theme: 主题；决定 VitePress 版本、Node 下限与依赖清单。
    :param log: 子进程输出行的回调，用于实时展示安装进度。
    :raises DocsError: 主题缺文件、离线且依赖缺失，或安装失败。
    """
    spec = theme or _theme_from_template(template_dir or TEMPLATE_DIR)
    target = Path(cache_dir) / "docs"
    target.mkdir(parents=True, exist_ok=True)
    if spec.install_mode == "ci":
        _copy_bundled_package(spec, target)
        installed = (target / VITEPRESS_BIN).is_file() and _installed_version(target) == spec.vitepress_version
        if installed:
            return target
        if offline:
            raise DocsError(
                "cli.docs.error.install_failed",
                reason=f"offline mode requires vitepress {spec.vitepress_version}",
                path=str(target / "node_modules"),
            )
        proc = _execute(package_argv("npm", *NPM_INSTALL_ARGS), target, runner, log)
    else:
        _write_external_package(spec, target)
        stamp = _read_stamp(target)
        installed = (
            (target / VITEPRESS_BIN).is_file()
            and _installed_version(target) == spec.vitepress_version
            and stamp.get("digest") == spec.digest
        )
        if installed:
            return target
        if offline:
            raise DocsError(
                "cli.docs.error.install_failed",
                reason=f"offline mode requires theme {spec.name} {spec.version}",
                path=str(target / "node_modules"),
            )
        proc = _execute(package_argv("npm", *NPM_INSTALL_PLAIN_ARGS), target, runner, log)
    if proc.returncode != 0:
        raise DocsError("cli.docs.error.install_failed", reason=_tail(proc.stderr or proc.stdout), path=str(target))
    if not (target / VITEPRESS_BIN).is_file():
        raise DocsError("cli.docs.error.install_failed", reason="vitepress binary is missing", path=str(target))
    if _installed_version(target) != spec.vitepress_version:
        raise DocsError(
            "cli.docs.error.install_failed",
            reason=f"installed vitepress is not {spec.vitepress_version}",
            path=str(target / VITEPRESS_PACKAGE),
        )
    if spec.install_mode != "ci":
        _write_stamp(target, spec)
    return target


def _copy_bundled_package(theme: ThemeSpec, target: Path) -> None:
    package_dir = theme.package_dir or theme.root
    for name in ("package.json", "package-lock.json"):
        origin = package_dir / name
        if not origin.is_file():
            raise DocsError("cli.docs.error.install_failed", reason=f"template is missing {name}", path=str(origin))
        shutil.copy2(origin, target / name)


def _write_external_package(theme: ThemeSpec, target: Path) -> None:
    payload = {
        "name": "akaribot-docs-site",
        "private": True,
        "type": "module",
        "dependencies": dict(theme.dependencies),
    }
    (target / "package.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_stamp(target: Path) -> dict[str, object]:
    try:
        payload = json.loads((target / THEME_STAMP).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return dict(payload) if isinstance(payload, dict) else {}


def _write_stamp(target: Path, theme: ThemeSpec) -> None:
    payload = {
        "schema": 1,
        "name": theme.name,
        "version": theme.version,
        "digest": theme.digest,
        "vitepress": theme.vitepress_version,
    }
    (target / THEME_STAMP).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _theme_from_template(template_dir: Path) -> ThemeSpec:
    # 兼容旧调用：测试只提供 package.json 与 lock，没有主题目录，故不读取 docs-theme.json。
    try:
        package = json.loads((Path(template_dir) / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        package = {}
    version = str(package.get("version") or "")
    vitepress = str((package.get("devDependencies") or {}).get("vitepress") or VITEPRESS_VERSION)
    return ThemeSpec(
        name="bundled",
        version=version,
        source="bundled",
        root=Path(template_dir),
        theme_dir=Path(template_dir) / "theme",
        package_dir=Path(template_dir),
        vitepress_version=vitepress,
        node_major=MIN_NODE_MAJOR,
        install_mode="ci",
    )


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


def run_build(
    docs_dir: Path,
    src_dir: Path,
    out_dir: Path,
    runner: Runner | None = None,
    *,
    log: LogSink | None = None,
) -> str:
    """执行构建并返回标准输出。

    :param log: 子进程输出行的回调，用于实时展示 VitePress 日志。
    :raises DocsError: VitePress 入口缺失或构建失败。
    """
    binary = Path(docs_dir) / VITEPRESS_BIN
    if not binary.is_file():
        raise DocsError("cli.docs.error.install_failed", reason="vitepress binary is missing", path=str(binary))
    argv = build_argv(docs_dir, src_dir, out_dir)
    proc = _execute(argv, Path(docs_dir), runner, log)
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


def _execute(
    argv: Sequence[str],
    cwd: Path,
    runner: Runner | None,
    log: LogSink | None,
) -> subprocess.CompletedProcess[str]:
    # 测试注入的 runner 优先，保证调用参数可断言且不启动真实子进程。
    if runner is not None:
        return runner(argv, cwd)
    if log is None:
        return _default_runner(argv, cwd)
    return _run_streaming(argv, cwd, log)


def _run_streaming(argv: Sequence[str], cwd: Path, log: LogSink) -> subprocess.CompletedProcess[str]:
    # 输出同时转发给终端与 TUI，颜色转义码在非终端消费方会原样显示，因此统一关闭颜色。
    env = {**os.environ, "NO_COLOR": "1", "FORCE_COLOR": "0"}
    process = subprocess.Popen(  # noqa: S603 - 命令由本模块组装，不含用户输入
        list(argv),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )
    lines: list[str] = []
    try:
        stream = process.stdout
        if stream is not None:
            for raw in stream:
                line = _ANSI_ESCAPE.sub("", raw).rstrip()
                lines.append(line)
                if line:
                    log(line)
        returncode = process.wait()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    return subprocess.CompletedProcess(list(argv), returncode, "\n".join(lines), "")


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
