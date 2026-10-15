"""TUI 调用 CLI 子进程的统一入口。

冻结可执行文件直接接受子命令；实例根目录同时用于工作目录和 AKARI_INSTANCE_DIR。
"""

from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from pathlib import Path

# 显式指定 CLI 入口，供自检与冻结产物使用。
CLI_BIN_ENV = "AKARIBOT_CLI_BIN"
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"


def cli_argv(*args: str) -> list[str]:
    """构造调用本 CLI 的 argv。

    :param args: 子命令及其参数。
    :return: 可直接交给 :mod:`subprocess` 的参数列表。
    """
    override = os.environ.get(CLI_BIN_ENV)
    if override:
        return [override, *args]
    frozen = bool(getattr(sys, "frozen", False)) or "__compiled__" in globals()
    if frozen:
        return [sys.executable, *args]
    return [sys.executable, "-m", "akaribot.cli.main", *args]


def cli_env(root: Path | str, *, extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """构造包含实例根目录和输出编码的子进程环境。

    :param root: 实例根目录。
    :param extra: 额外覆盖的环境变量。
    :return: 子进程环境映射。
    """
    env = dict(os.environ)
    env[INSTANCE_DIR_ENV] = str(root)
    env["AKARI_CONFIG_PATH"] = str(Path(root).expanduser().resolve() / "config")
    env.pop("AKARI_CONFIG_READONLY", None)
    # 子进程输出含中文与 JSON，Windows 控制台默认代码页可能是 GBK，两侧编码不一致会得到乱码或解析失败。
    env["PYTHONIOENCODING"] = "utf-8"
    if extra:
        env.update(extra)
    return env
