from __future__ import annotations

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
