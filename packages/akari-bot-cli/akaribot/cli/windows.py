"""Windows 实例停止协议。"""

from __future__ import annotations

import ctypes
from ctypes import wintypes


def request_stop(pid: int) -> bool:
    """请求持有对应停止事件的实例自行退出。"""
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenEventW.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR)
    kernel.OpenEventW.restype = wintypes.HANDLE
    kernel.SetEvent.argtypes = (wintypes.HANDLE,)
    kernel.SetEvent.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL
    handle = kernel.OpenEventW(0x0002, False, f"Local\\AkariBotStop-{pid}")
    if not handle:
        return False
    try:
        return bool(kernel.SetEvent(handle))
    finally:
        kernel.CloseHandle(handle)
