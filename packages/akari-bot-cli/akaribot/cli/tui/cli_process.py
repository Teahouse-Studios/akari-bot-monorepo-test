"""界面调用本 CLI 的统一入口。

界面里的每个动作最终都是一次 ``akaribot <子命令>`` 子进程调用，argv 与环境的拼装规则集中在这里：
冻结产物（Nuitka onefile）里 ``sys.executable`` 就是 CLI 本体，不能再加 ``-m``；实例根同时是子进程
的工作目录与 ``AKARI_INSTANCE_DIR``，只认其一会在仓库根运行界面时静默读到另一个实例。
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
    frozen = bool(getattr(sys, "frozen", False)) or hasattr(sys, "__compiled__")
    if frozen:
        return [sys.executable, *args]
    return [sys.executable, "-m", "akaribot.cli.main", *args]


def cli_env(root: Path | str, *, extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """构造子进程环境：钉住实例根与输出编码。

    :param root: 实例根，写入 ``AKARI_INSTANCE_DIR``。
    :param extra: 需要额外覆盖的环境变量。
    :return: 可直接交给 :mod:`subprocess` 的环境映射。
    """
    env = dict(os.environ)
    env[INSTANCE_DIR_ENV] = str(root)
    # 子进程输出含中文与 JSON，Windows 控制台默认代码页可能是 GBK，两侧编码不一致会得到乱码或解析失败。
    env["PYTHONIOENCODING"] = "utf-8"
    if extra:
        env.update(extra)
    return env
