import _thread
import ctypes
import os
import threading
from contextlib import contextmanager
from ctypes import wintypes


@contextmanager
def listen_for_windows_stop():
    """监听实例停止事件，使主线程执行正常的退出清理。"""
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateEventW.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.BOOL, wintypes.LPCWSTR)
    kernel.CreateEventW.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL
    handle = kernel.CreateEventW(None, True, False, f"Local\\AkariBotStop-{os.getpid()}")
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    closing = threading.Event()

    def wait():
        while not closing.is_set():
            result = kernel.WaitForSingleObject(handle, 100)
            if result == 0:
                if not closing.is_set():
                    _thread.interrupt_main()
                return
            if result != 258:
                return

    thread = threading.Thread(target=wait, name="instance-stop", daemon=True)
    thread.start()
    try:
        yield
    finally:
        closing.set()
        thread.join()
        kernel.CloseHandle(handle)
