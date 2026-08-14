from __future__ import annotations

import ctypes
from ctypes import wintypes

import psutil
import win32gui
import win32process

QQ_PROCESS_NAME: str = "QQ.exe"


def is_qq_process(process_name: str) -> bool:
    return process_name.lower() == QQ_PROCESS_NAME.lower()


def current_foreground_process_name() -> str | None:
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return psutil.Process(pid).name()
    except Exception:
        return None


def is_qq_foreground() -> bool:
    name = current_foreground_process_name()
    return name is not None and is_qq_process(name)


_imm32 = ctypes.windll.imm32
_imm32.ImmGetContext.argtypes = [wintypes.HWND]
_imm32.ImmGetContext.restype = ctypes.c_void_p
_imm32.ImmGetCompositionStringW.argtypes = [ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
_imm32.ImmGetCompositionStringW.restype = ctypes.c_long
_imm32.ImmReleaseContext.argtypes = [wintypes.HWND, ctypes.c_void_p]
_imm32.ImmReleaseContext.restype = wintypes.BOOL

_GCS_COMPSTR = 0x0008


def is_ime_composing() -> bool:
    """当前前台窗口的输入法是否处于组合状态（有拼音组合串/候选词未上屏）。"""
    hwnd = win32gui.GetForegroundWindow()
    himc = _imm32.ImmGetContext(hwnd)
    if not himc:
        return False
    try:
        size = _imm32.ImmGetCompositionStringW(himc, _GCS_COMPSTR, None, 0)
        return size > 0
    finally:
        _imm32.ImmReleaseContext(hwnd, himc)
