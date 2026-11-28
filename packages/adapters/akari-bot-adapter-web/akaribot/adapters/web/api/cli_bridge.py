import asyncio
import codecs
import json
import os
import re
import shutil
import sys
from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil

from akaribot.core.paths import Paths

# core 公开接口未导出以下名称，此处直接定义为字符串常量。
CLI_PATH_ENV = "AKARIBOT_CLI_PATH"
CONFIG_READONLY_ENV = "AKARI_CONFIG_READONLY"
CLI_NAMES = ("akaribot", "akaribot.exe", "akari.exe")

# 读取类命令仅查询本机状态，单次最长等待 120 秒。
CLI_QUERY_TIMEOUT_SECONDS = 120
# 安装与更新需要下载依赖，单次最长等待 30 分钟。
CLI_WRITE_TIMEOUT_SECONDS = 1800

LINE_SPLIT_PATTERN = re.compile(r"[\r\n]")

# 写入类命令会修改同一个虚拟环境与配置目录，同一时刻仅允许执行一条。
write_lock = asyncio.Lock()


class CliUnavailable(RuntimeError):
    pass


class CliTimeout(RuntimeError):
    pass


@dataclass(frozen=True)
class CliResult:
    returncode: int
    stdout: str
    stderr: str


def locate_cli() -> str:
    override = os.environ.get(CLI_PATH_ENV, "").strip()
    candidates = [Path(override).expanduser()] if override else []
    interpreter_dir = Path(sys.executable).parent
    candidates.extend(interpreter_dir / name for name in CLI_NAMES)
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    found = shutil.which("akaribot")
    if found:
        return found
    raise CliUnavailable("The akaribot CLI was not found.")


def _cli_env() -> dict[str, str]:
    env = dict(os.environ)
    # 只读标记仅约束 Web 进程自身，写入类命令需要修改配置与数据库。
    env.pop(CONFIG_READONLY_ENV, None)
    env["PYTHONIOENCODING"] = "utf-8"
    env["AKARI_INSTANCE_DIR"] = str(Paths.instance)
    env["AKARI_CONFIG_PATH"] = str(Paths.config)
    return env


async def _spawn(args: Sequence[str], *, stderr: int) -> asyncio.subprocess.Process:
    path = locate_cli()
    try:
        return await asyncio.create_subprocess_exec(
            path,
            *args,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=stderr,
            env=_cli_env(),
            cwd=Paths.instance,
        )
    except OSError as exc:
        raise CliUnavailable(f"Failed to start {path}: {exc}") from exc


async def _stop_process(process: asyncio.subprocess.Process) -> None:
    try:
        descendants = psutil.Process(process.pid).children(recursive=True)
    except psutil.Error:
        descendants = []
    if process.returncode is None:
        try:
            process.kill()
        except ProcessLookupError:
            pass
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            pass
    await process.wait()


async def run_cli(*args: str, timeout: float = CLI_QUERY_TIMEOUT_SECONDS) -> CliResult:
    process = await _spawn(args, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except TimeoutError as exc:
        await _stop_process(process)
        raise CliTimeout(f"Command timed out after {int(timeout)} seconds.") from exc
    except asyncio.CancelledError:
        await asyncio.shield(_stop_process(process))
        raise
    return CliResult(
        process.returncode if process.returncode is not None else -1,
        stdout.decode("utf-8", errors="replace").strip(),
        stderr.decode("utf-8", errors="replace").strip(),
    )


async def stream_cli(*args: str, timeout: float = CLI_WRITE_TIMEOUT_SECONDS) -> AsyncIterator[tuple[str, str | int]]:
    try:
        process = await _spawn(args, stderr=asyncio.subprocess.STDOUT)
    except CliUnavailable as exc:
        yield "line", str(exc)
        yield "exit", -1
        return

    assert process.stdout is not None
    try:
        async with asyncio.timeout(timeout):
            decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
            buffer = ""
            while chunk := await process.stdout.read(4096):
                buffer += decoder.decode(chunk)
                *lines, buffer = LINE_SPLIT_PATTERN.split(buffer)
                for line in lines:
                    if line.strip():
                        yield "line", line
            buffer += decoder.decode(b"", final=True)
            if buffer.strip():
                yield "line", buffer
            returncode = await process.wait()
        yield "exit", returncode
    except TimeoutError:
        yield "line", f"Command timed out after {int(timeout)} seconds."
        yield "exit", -1
    finally:
        if process.returncode is None:
            await _stop_process(process)


def parse_json(text: str) -> Any:
    # CLI 的 JSON 输出前可能混入警告行，因此从每个起始符号开始尝试解码。
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        return value
    raise ValueError("The CLI output does not contain JSON.")
