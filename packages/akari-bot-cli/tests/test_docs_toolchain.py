"""``akaribot.cli.docs.toolchain``：版本探测、依赖安装与构建命令。"""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli.docs import toolchain
from akaribot.cli.docs.model import DocsError
from akaribot.testing import Tester, func_case


def _template(base: Path) -> Path:
    directory = base / "template"
    directory.mkdir()
    (directory / "package.json").write_text(
        json.dumps({"name": "akaribot-docs", "version": "0.1.0", "devDependencies": {"vitepress": "1.6.4"}}),
        encoding="utf-8",
    )
    (directory / "package-lock.json").write_text('{"lockfileVersion": 3}\n', encoding="utf-8")
    return directory


def _installer(calls: list[tuple[list[str], Path]]):
    def run(argv, cwd: Path):
        calls.append((list(argv), Path(cwd)))
        binary = Path(cwd) / toolchain.VITEPRESS_BIN
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_text("", encoding="utf-8")
        (Path(cwd) / toolchain.VITEPRESS_PACKAGE).write_text(
            json.dumps({"version": toolchain.VITEPRESS_VERSION}), encoding="utf-8"
        )
        return subprocess.CompletedProcess(list(argv), 0, "installed\n", "")

    return run


async def _test_node_version_parsing():
    return (
        toolchain.parse_node_major("v24.21.0") == 24
        and toolchain.parse_node_major("18.0.0") == 18
        and toolchain.parse_node_major("") is None
        and toolchain.parse_node_major("not-a-version") is None
    )


async def _test_detect_requires_node_eighteen():
    with patch.object(toolchain.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"):
        with patch.object(
            toolchain,
            "_probe",
            side_effect=lambda executable, flag: "v24.21.0" if executable.endswith("node") else "11.19.0",
        ):
            ready = toolchain.detect()
        with patch.object(
            toolchain,
            "_probe",
            side_effect=lambda executable, flag: "v16.4.0" if executable.endswith("node") else "8.0.0",
        ):
            old = toolchain.detect()
    return (
        ready.ready
        and ready.node_version == "v24.21.0"
        and ready.npm_version == "11.19.0"
        and not old.ready
        and "< 18" in old.detail
    )


async def _test_detect_reports_missing_node():
    with patch.object(toolchain.shutil, "which", return_value=None):
        info = toolchain.detect()
    return not info.ready and info.detail == "node not found"


async def _test_ensure_toolchain_runs_npm_ci():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        template = _template(base)
        calls: list[tuple[list[str], Path]] = []
        target = toolchain.ensure_toolchain(base / "cache", template, runner=_installer(calls))
        copied = (target / "package.json").is_file() and (target / "package-lock.json").is_file()
        installed = (target / toolchain.VITEPRESS_BIN).is_file()
    return (
        target == base / "cache" / "docs"
        and copied
        and installed
        and len(calls) == 1
        and calls[0][0] == ["npm", "ci", "--no-audit", "--no-fund"]
        and calls[0][1] == target
    )


async def _test_ensure_toolchain_offline_without_dependencies():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        template = _template(base)
        calls: list[tuple[list[str], Path]] = []
        try:
            toolchain.ensure_toolchain(base / "cache", template, offline=True, runner=_installer(calls))
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return error == "cli.docs.error.install_failed" and calls == []


async def _test_ensure_toolchain_reuses_installed_modules():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        template = _template(base)
        target = base / "cache" / "docs"
        binary = target / toolchain.VITEPRESS_BIN
        binary.parent.mkdir(parents=True)
        binary.write_text("", encoding="utf-8")
        (target / toolchain.VITEPRESS_PACKAGE).write_text(
            json.dumps({"version": toolchain.VITEPRESS_VERSION}), encoding="utf-8"
        )
        calls: list[tuple[list[str], Path]] = []
        result = toolchain.ensure_toolchain(base / "cache", template, runner=_installer(calls))
    return result == target and calls == []


async def _test_ensure_toolchain_reinstalls_on_version_mismatch():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        template = _template(base)
        target = base / "cache" / "docs"
        binary = target / toolchain.VITEPRESS_BIN
        binary.parent.mkdir(parents=True)
        binary.write_text("", encoding="utf-8")
        (target / toolchain.VITEPRESS_PACKAGE).write_text(json.dumps({"version": "0.0.1"}), encoding="utf-8")
        calls: list[tuple[list[str], Path]] = []
        result = toolchain.ensure_toolchain(base / "cache", template, runner=_installer(calls))
        installed = toolchain._installed_version(result)
    return result == target and len(calls) == 1 and installed == toolchain.VITEPRESS_VERSION


async def _test_package_argv_wraps_npm_on_windows():
    return (
        toolchain.package_argv("npm", "ci", windows=True) == ["cmd", "/c", "npm", "ci"]
        and toolchain.package_argv("npm", "ci", windows=False) == ["npm", "ci"]
        and toolchain.package_argv("node", "--version", windows=True) == ["node", "--version"]
    )


async def _test_run_build_argv_and_failure():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        docs = base / "docs"
        binary = docs / toolchain.VITEPRESS_BIN
        binary.parent.mkdir(parents=True)
        binary.write_text("", encoding="utf-8")
        source = base / "src"
        output = base / "out"
        calls: list[tuple[list[str], Path]] = []

        def succeed(argv, cwd: Path):
            calls.append((list(argv), Path(cwd)))
            Path(output).mkdir(parents=True, exist_ok=True)
            (Path(output) / "index.html").write_text("ok", encoding="utf-8")
            return subprocess.CompletedProcess(list(argv), 0, "built\n", "")

        log = toolchain.run_build(docs, source, output, runner=succeed)
        argv = calls[0][0]

        def fail(argv, cwd: Path):
            return subprocess.CompletedProcess(list(argv), 2, "", "boom")

        try:
            toolchain.run_build(docs, source, output, runner=fail)
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return (
        log == "built\n"
        and argv[0].endswith("node")
        and argv[1] == str(binary)
        and argv[2:] == ["build", str(source), "--outDir", str(output)]
        and error == "cli.docs.error.build_failed"
    )


async def _test_run_build_requires_vitepress_binary():
    with TemporaryDirectory(prefix="akari-docs-tc-") as raw:
        base = Path(raw)
        try:
            toolchain.run_build(base / "docs", base / "src", base / "out", runner=lambda argv, cwd: None)
        except DocsError as exc:
            error = str(exc)
        else:
            error = ""
    return error == "cli.docs.error.install_failed"


@func_case
async def test_docs_toolchain(tester: Tester):
    """cli.docs.toolchain: Node 工具链探测与命令组装"""
    await tester.test(_test_node_version_parsing, "解析 node 主版本号")
    await tester.test(_test_detect_requires_node_eighteen, "node 主版本低于 18 时不可用")
    await tester.test(_test_detect_reports_missing_node, "缺少 node 时报告原因")
    await tester.test(_test_ensure_toolchain_runs_npm_ci, "复制模板并执行 npm ci")
    await tester.test(_test_ensure_toolchain_offline_without_dependencies, "离线且无依赖时失败")
    await tester.test(_test_ensure_toolchain_reuses_installed_modules, "已装依赖且版本一致时不重复安装")
    await tester.test(_test_ensure_toolchain_reinstalls_on_version_mismatch, "VitePress 版本不一致时重装")
    await tester.test(_test_package_argv_wraps_npm_on_windows, "Windows 下经 cmd /c 启动 npm")
    await tester.test(_test_run_build_argv_and_failure, "构建命令参数与失败映射")
    await tester.test(_test_run_build_requires_vitepress_binary, "缺少 VitePress 入口时失败")
    return tester
