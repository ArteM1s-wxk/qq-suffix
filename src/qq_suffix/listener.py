from __future__ import annotations

import threading
from collections.abc import Callable

import keyboard


def should_append(enabled: bool, is_qq: bool) -> bool:
    return enabled and is_qq


class Listener:
    def __init__(
        self,
        get_suffix: Callable[[], str],
        is_qq_window: Callable[[], bool],
    ) -> None:
        self._get_suffix = get_suffix
        self._is_qq_window = is_qq_window
        self._enabled = threading.Event()
        self._hook = None

    def start(self) -> None:
        if self._hook is None:
            self._hook = keyboard.on_press_key("enter", self._on_enter, suppress=True)

    def stop(self) -> None:
        if self._hook is not None:
            keyboard.unhook(self._hook)
            self._hook = None

    def set_enabled(self, value: bool) -> None:
        if value:
            self._enabled.set()
        else:
            self._enabled.clear()

    @property
    def enabled(self) -> bool:
        return self._enabled.is_set()

    def _on_enter(self, _event) -> None:
        # 回车被全局抑制，需临时移除 hook 再补发，否则模拟的 enter 会被再次抑制。
        keyboard.unhook(self._hook)
        try:
            if should_append(self._enabled.is_set(), self._is_qq_window()):
                keyboard.write(self._get_suffix())
            keyboard.send("enter")
        finally:
            self._hook = keyboard.on_press_key("enter", self._on_enter, suppress=True)
