from __future__ import annotations

import tkinter as tk
from pathlib import Path

from qq_suffix.config import load_suffix, save_suffix
from qq_suffix.listener import Listener
from qq_suffix.window import is_qq_foreground

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.json"


class App:
    def __init__(self, root: tk.Tk, listener: Listener, config_path: Path) -> None:
        self.root = root
        self.listener = listener
        self.config_path = config_path

        root.title("QQ 频道自动后缀")
        root.resizable(False, False)

        self.suffix_var = tk.StringVar(value=load_suffix(config_path))
        self.status_var = tk.StringVar(value="已停止")

        tk.Label(root, text="后缀内容：").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry = tk.Entry(root, textvariable=self.suffix_var, width=30)
        self.entry.grid(row=0, column=1, padx=8, pady=8)

        self.toggle_btn = tk.Button(root, text="启动", command=self.toggle)
        self.toggle_btn.grid(row=1, column=0, padx=8, pady=8)

        self.status_label = tk.Label(root, textvariable=self.status_var, fg="red")
        self.status_label.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        self.suffix_var.trace_add("write", self._on_suffix_change)

    def toggle(self) -> None:
        if self.listener.enabled:
            self.listener.set_enabled(False)
            self.status_var.set("已停止")
            self.toggle_btn.config(text="启动")
            self.status_label.config(fg="red")
        else:
            self.listener.set_enabled(True)
            self.status_var.set("运行中")
            self.toggle_btn.config(text="停止")
            self.status_label.config(fg="green")

    def _on_suffix_change(self, *_args) -> None:
        save_suffix(self.config_path, self.suffix_var.get())


def main() -> None:
    root = tk.Tk()
    listener = Listener(
        get_suffix=lambda: load_suffix(CONFIG_PATH),
        is_qq_window=is_qq_foreground,
    )
    listener.start()
    App(root, listener, CONFIG_PATH)
    root.mainloop()
    listener.stop()


if __name__ == "__main__":
    main()
