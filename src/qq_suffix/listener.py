from __future__ import annotations

import threading
import time
from collections.abc import Callable

import keyboard

from qq_suffix.config import DEFAULT_HOTKEY, Config


def should_append(enabled: bool, is_qq: bool) -> bool:
    return enabled and is_qq


class Listener:
    def __init__(
        self,
        get_config: Callable[[], Config],
        is_qq_window: Callable[[], bool],
    ) -> None:
        self._get_config = get_config
        self._is_qq_window = is_qq_window
        self._enabled = threading.Event()
        self._send_hotkey = None
        self._pause_hotkey = None
        self._running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            self._running = True
            if self._send_hotkey is None:
                config = self._get_config()
                self._send_hotkey = keyboard.add_hotkey(config.hotkey, self._on_send, suppress=True)
            if self._pause_hotkey is None:
                self._pause_hotkey = keyboard.add_hotkey("f8", self.toggle_enabled)

    def stop(self) -> None:
        with self._lock:
            self._running = False
            send = self._send_hotkey
            self._send_hotkey = None
            if send is not None:
                keyboard.remove_hotkey(send)
            pause = self._pause_hotkey
            self._pause_hotkey = None
            if pause is not None:
                keyboard.remove_hotkey(pause)

    def update_hotkey(self) -> None:
        with self._lock:
            if self._send_hotkey is not None:
                keyboard.remove_hotkey(self._send_hotkey)
                self._send_hotkey = None
            if not self._running:
                return
            config = self._get_config()
            hotkey = config.hotkey or DEFAULT_HOTKEY
            try:
                self._send_hotkey = keyboard.add_hotkey(hotkey, self._on_send, suppress=True)
            except (ValueError, KeyError):
                self._send_hotkey = keyboard.add_hotkey(DEFAULT_HOTKEY, self._on_send, suppress=True)

    def set_enabled(self, value: bool) -> None:
        if value:
            self._enabled.set()
        else:
            self._enabled.clear()

    def toggle_enabled(self) -> None:
        if self._enabled.is_set():
            self._enabled.clear()
        else:
            self._enabled.set()

    @property
    def enabled(self) -> bool:
        return self._enabled.is_set()

    def _on_send(self) -> None:
        # 释放被 suppress 的修饰键，避免 Ctrl 等组合键卡住
        for modifier in ("ctrl", "shift", "alt"):
            keyboard.release(modifier)
        if not should_append(self._enabled.is_set(), self._is_qq_window()):
            return
        config = self._get_config()
        if config.newline:
            # 用右 Shift：QQ 英文输入状态下对左 Shift+Enter 换行不敏感
            keyboard.send("right shift+enter")
            time.sleep(0.15)
        keyboard.write(config.suffix)
        keyboard.send("enter")
