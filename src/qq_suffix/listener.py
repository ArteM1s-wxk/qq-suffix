from __future__ import annotations

import threading
from collections.abc import Callable

import keyboard

from qq_suffix.config import Config


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
        self._hook = None
        self._hotkey = None
        self._running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            if self._hook is None:
                self._running = True
                self._hook = keyboard.on_press_key("enter", self._on_enter, suppress=True)
            if self._hotkey is None:
                self._hotkey = keyboard.add_hotkey("f8", self.toggle_enabled)

    def stop(self) -> None:
        with self._lock:
            self._running = False
            hook = self._hook
            self._hook = None
            if hook is not None:
                keyboard.unhook(hook)
            hotkey = self._hotkey
            self._hotkey = None
            if hotkey is not None:
                keyboard.remove_hotkey(hotkey)

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

    def _on_enter(self, _event) -> None:
        # 回调运行在键盘钩子线程；与 start/stop 共用同一把锁，
        # 避免卸载后 stop() 仍尝试卸载旧 hook，或 stop() 返回后回调又重新装回 hook。
        with self._lock:
            try:
                if not self._running:
                    return
                hook = self._hook
                self._hook = None
                if hook is not None:
                    # 回车被全局抑制，需临时移除 hook 再补发，否则模拟的 enter 会被再次抑制。
                    keyboard.unhook(hook)
                if should_append(self._enabled.is_set(), self._is_qq_window()):
                    config = self._get_config()
                    if config.newline:
                        # Shift+Enter 在 QQ 里是换行，让后缀另起一行
                        keyboard.send("shift+enter")
                    keyboard.write(config.suffix)
                keyboard.send("enter")
            finally:
                if self._running:
                    self._hook = keyboard.on_press_key("enter", self._on_enter, suppress=True)
                else:
                    self._hook = None
