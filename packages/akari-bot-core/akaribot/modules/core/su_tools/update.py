"""自更新：委托 CLI 执行，本进程只读。

机器人与 server 一律以只读配置运行（``AKARI_CONFIG_READONLY``），而更新要写配置（新版本可能带来
新配置项）与数据库（迁移），故更新动作必须交给 CLI 子进程（tasks T7.2 / D7）。本模块只负责定位
CLI、以子进程执行 ``akaribot module update --all --non-interactive --defer-runtime --json`` 并转述其结果。
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import psutil

from akaribot.core.builtins.bot import Bot
from akaribot.core.builtins.message.internal import I18NContext, Plain
from akaribot.core.component import module

upd = module("update", required_superuser=True, base=True, doc=True)

# CLI 可执行文件的定位途径（T7.2）：CLI 注入的环境变量最可靠，其次随解释器同目录，最后查 PATH。
CLI_PATH_ENV = "AKARIBOT_CLI_PATH"
CLI_NAMES = ("akaribot", "akaribot.exe", "akari.exe")

# 只读标记与实例根目录的环境变量名；二者不在 core 门面内，故按引导代码的做法写为字面量。
CONFIG_READONLY_ENV = "AKARI_CONFIG_READONLY"
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"

# 委托参数固定，不接受用户输入拼接：--all 覆盖全部已装包，--json 让结果可解析。
UPDATE_ARGV = ("module", "update", "--all", "--non-interactive", "--defer-runtime", "--json")

# 更新要在子进程里跑 uv 下载、配置补写与数据库迁移，等待上限按分钟计。
UPDATE_TIMEOUT_SECONDS = 1800

# 回报附带的错误输出行数上限，避免把 CLI 的整段日志刷进会话。
OUTPUT_TAIL_LINES = 6


@dataclass
class CliLocation:
    """CLI 可执行文件的定位结果。

    :param path: 命中路径；三条途径都落空时为 ``None``。
    :param attempts: 逐条途径的说明，失败回报据此告诉操作者差在哪一步。
    """

    path: str | None
    attempts: list[str] = field(default_factory=list)


@dataclass
class UpdateOutcome:
    """一次委托更新的结果。

    :param location: CLI 定位结果。
    :param returncode: CLI 退出码；未执行时为 ``None``。
    :param payload: CLI 回传的 JSON 主体；未回传或无法解析时为 ``None``。
    :param stderr: CLI 的标准错误。
    :param error: 过程性失败说明（未找到、超时、无 JSON）。
    """

    location: CliLocation
    returncode: int | None = None
    payload: dict | None = None
    stderr: str = ""
    error: str = ""


def _executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def locate_cli() -> CliLocation:
    """按序定位 CLI 可执行文件。

    顺序为 ``AKARIBOT_CLI_PATH`` → 与当前解释器同目录的 ``akaribot`` / ``akari.exe``
    → ``shutil.which("akaribot")``；每条途径无论命中与否都留下说明。

    :return: 命中路径与逐条尝试说明。
    """
    attempts: list[str] = []
    override = os.environ.get(CLI_PATH_ENV, "").strip()
    if not override:
        attempts.append(f"{CLI_PATH_ENV} 未设置")
    else:
        candidate = Path(override).expanduser()
        if _executable(candidate):
            return CliLocation(str(candidate), [*attempts, f"{CLI_PATH_ENV}={override} 可用"])
        attempts.append(f"{CLI_PATH_ENV}={override} 不是可执行文件")

    interpreter_dir = Path(sys.executable).parent
    for name in CLI_NAMES:
        candidate = interpreter_dir / name
        if _executable(candidate):
            return CliLocation(str(candidate), [*attempts, f"解释器同目录命中 {candidate}"])
    attempts.append(f"解释器同目录（{interpreter_dir}）没有 {' / '.join(CLI_NAMES)}")

    found = shutil.which("akaribot")
    if found:
        return CliLocation(found, [*attempts, f"PATH 命中 {found}"])
    attempts.append("PATH 里没有 akaribot")
    return CliLocation(None, attempts)


async def _run_cli(path: str, argv: list[str]) -> tuple[int, str, str, bool]:
    env = dict(os.environ)
    # 只读标记只约束 server 自身：更新要写配置，须让子进程按宿主机 CLI 的权限运行。
    env.pop(CONFIG_READONLY_ENV, None)
    env["PYTHONIOENCODING"] = "utf-8"
    instance_dir = env.get(INSTANCE_DIR_ENV, "").strip()
    cwd = instance_dir if instance_dir and Path(instance_dir).is_dir() else None
    try:
        process = await asyncio.create_subprocess_exec(
            path, *argv, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env, cwd=cwd
        )
    except OSError as exc:
        return -1, "", f"无法执行 {path}：{exc}", False
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=UPDATE_TIMEOUT_SECONDS)
    except asyncio.CancelledError:
        await asyncio.shield(_stop_cli(process))
        raise
    except asyncio.TimeoutError:
        await _stop_cli(process)
        return -1, "", f"CLI 超过 {UPDATE_TIMEOUT_SECONDS} 秒未返回", True
    return (
        process.returncode if process.returncode is not None else -1,
        stdout.decode("utf-8", errors="replace").strip(),
        stderr.decode("utf-8", errors="replace").strip(),
        False,
    )


async def _stop_cli(process) -> None:
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


def extract_update_payload(stdout: str) -> dict | None:
    """从 CLI 输出里截取更新结果 JSON 主体。

    与 CLI 侧的 ``extract_json`` 同一策略：自每个 ``{`` 起尝试解码，容忍日志混入 stdout。

    :param stdout: CLI 的标准输出。
    :return: JSON 对象；无法解析时为 ``None``。
    """
    decoder = json.JSONDecoder()
    for index, char in enumerate(stdout):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(stdout[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


async def delegate_update(*, force: bool = False) -> UpdateOutcome:
    """定位 CLI 并以子进程委托它完成更新。

    :param force: 为真时追加 ``--force``，已是最新的包也重装。
    :return: 委托结果；一切失败都写进结果，不向调用方抛异常。
    """
    location = locate_cli()
    if location.path is None:
        return UpdateOutcome(location=location, error="未找到 CLI 可执行文件")
    argv = [*UPDATE_ARGV, *(("--force",) if force else ())]
    returncode, stdout, stderr, timed_out = await _run_cli(location.path, argv)
    outcome = UpdateOutcome(location=location, returncode=returncode, stderr=stderr)
    if timed_out:
        outcome.error = stderr
        return outcome
    outcome.payload = extract_update_payload(stdout)
    if outcome.payload is None:
        outcome.error = "CLI 未回传可解析的 JSON 结果"
    return outcome


def _names(payload: dict, key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _details(payload: dict, key: str, names: list[str]) -> list[str]:
    reasons: dict[str, str] = {}
    for item in payload.get(key) or []:
        if isinstance(item, dict) and item.get("dist"):
            reasons[str(item["dist"])] = str(item.get("reason", "")).strip()
    return [f"{name}（{reasons[name]}）" if reasons.get(name) else name for name in names]


def _tail(text: str, lines: int = OUTPUT_TAIL_LINES) -> str:
    return "\n".join([line for line in text.splitlines() if line.strip()][-lines:])


def _reload_pending(payload: dict, updated: list[str]) -> list[str]:
    # 新版 CLI 直接回传 ``reload_pending``；旧版只回传 ``notified`` 明细，据此推导；
    # 两者都没有时保守地把全部已更新包视为待重载。
    if isinstance(payload.get("reload_pending"), list):
        return _names(payload, "reload_pending")
    notified = payload.get("notified")
    if isinstance(notified, list):
        delivered = {str(item.get("dist")) for item in notified if isinstance(item, dict) and item.get("delivered")}
        return [dist for dist in updated if dist not in delivered]
    return list(updated)


def format_update_report(outcome: UpdateOutcome) -> str:
    """把委托结果整理成用户可读的中文回报。

    成功、部分成功、全部失败、超时与「未找到 CLI」各有文案，任何一类结果都不隐藏。

    :param outcome: 委托结果。
    :return: 可直接发进会话的文本。
    """
    if outcome.location.path is None:
        return "\n".join(
            [
                f"未找到 CLI，请在宿主机执行 `akaribot module update --all`；或设置 {CLI_PATH_ENV} 指向 CLI 后重试。",
                "定位过程：" + "；".join(outcome.location.attempts),
            ]
        )

    source = f"（CLI：{outcome.location.path}，退出码 {outcome.returncode}）"
    if outcome.payload is None:
        lines = [f"委托 CLI 更新失败{source}：{outcome.error or '未知原因'}。"]
        if outcome.stderr:
            lines.append("CLI 错误输出：\n" + _tail(outcome.stderr))
        lines.append("请在宿主机手动执行 `akaribot module update --all` 核对。")
        return "\n".join(lines)

    payload = outcome.payload
    updated = _names(payload, "updated")
    failed = _names(payload, "failed")
    skipped = _names(payload, "skipped")
    planned = _names(payload, "planned")
    if payload.get("dry_run"):
        lines = ["演练模式：未改动任何文件。计划更新 " + ("、".join(planned) or "无")]
    elif not updated and failed:
        lines = [f"更新失败：{len(failed)} 个包全部未更新成功{source}。"]
    elif failed:
        lines = [f"更新部分成功：成功 {len(updated)} 个，失败 {len(failed)} 个{source}。"]
    elif updated:
        lines = [f"更新成功：{len(updated)} 个包{source}。"]
    else:
        lines = [f"没有需要更新的包{source}。"]

    if updated:
        lines.append("成功：" + "、".join(updated))
    if failed:
        lines.append("失败：" + "、".join(_details(payload, "failed_details", failed)))
    if skipped:
        lines.append("跳过：" + "、".join(_details(payload, "skipped_details", skipped)))

    # 缺少 reload_pending 字段说明 CLI 版本较旧，此时保守地提示重启而不是假定已热装载。
    pending = _reload_pending(payload, updated)
    if pending:
        lines.append("以下包尚未热装载：" + "、".join(pending) + "；请执行 `~restart` 让新版本生效。")
    elif updated:
        lines.append("运行中的实例已收到热装载通知，无需重启。")
    return "\n".join(lines)


@upd.command("[--force] {{I18N:core.help.update}}", options_desc={"--force": "{I18N:core.help.update.option.force}"})
async def _(msg: Bot.MessageSession, force: bool = False):
    if Bot.Info.binary_mode:
        await msg.finish(I18NContext("core.message.update.binary_mode"))
    outcome = await delegate_update(force=force)
    await msg.finish(Plain(format_update_report(outcome), disable_joke=True))
