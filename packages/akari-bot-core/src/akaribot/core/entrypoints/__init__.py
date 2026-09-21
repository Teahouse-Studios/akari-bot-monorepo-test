"""core 的命令行入口。

CLI 进程不 import core，一切实例操作经子进程调用这里的模块；因此每个模块都必须能独立
``python -m akaribot.core.entrypoints.<名>`` 运行，并自行解析 ``AKARI_INSTANCE_DIR``。
"""
