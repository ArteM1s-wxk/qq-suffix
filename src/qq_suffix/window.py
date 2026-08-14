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
_GCS_RESULTSTR = 0x0800


class _RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


class _GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hwndActive", wintypes.HWND),
        ("hwndFocus", wintypes.HWND),
        ("hwndCapture", wintypes.HWND),
        ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize", wintypes.HWND),
        ("hwndCaret", wintypes.HWND),
        ("rcCaret", _RECT),
    ]


def _get_focus_window() -> int:
    fg = win32gui.GetForegroundWindow()
    tid = ctypes.windll.user32.GetWindowThreadProcessId(fg, None)
    info = _GUITHREADINFO()
    info.cbSize = ctypes.sizeof(_GUITHREADINFO)
    ctypes.windll.user32.GetGUIThreadInfo(tid, ctypes.byref(info))
    return info.hwndFocus or fg


def is_ime_composing() -> bool:
    """当前焦点窗口的输入法是否处于组合状态（有拼音组合串/候选词未上屏）。"""
    hwnd = _get_focus_window()
    himc = _imm32.ImmGetContext(hwnd)
    if not himc:
        return False
    try:
        if _imm32.ImmGetCompositionStringW(himc, _GCS_COMPSTR, None, 0) > 0:
            return True
        if _imm32.ImmGetCompositionStringW(himc, _GCS_RESULTSTR, None, 0) > 0:
            return True
        return False
    finally:
        _imm32.ImmReleaseContext(hwnd, himc)
