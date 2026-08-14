from __future__ import annotations

import tkinter as tk
from pathlib import Path

from qq_suffix.config import load_config, save_config
from qq_suffix.listener import Listener
from qq_suffix.window import is_qq_foreground

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.json"


class App:
    def __init__(self, root: tk.Tk, listener: Listener, config_path: Path) -> None:
        self.root = root
        self.listener = listener
        self.config_path = config_path

        config = load_config(config_path)

        root.title("QQ 频道自动后缀")
        root.resizable(False, False)

        self.suffix_var = tk.StringVar(value=config.suffix)
        self.newline_var = tk.BooleanVar(value=config.newline)
        self.status_var = tk.StringVar(value="已停止")

        tk.Label(root, text="后缀内容：").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry = tk.Entry(root, textvariable=self.suffix_var, width=30)
        self.entry.grid(row=0, column=1, padx=8, pady=8)

        self.toggle_btn = tk.Button(root, text="启动", command=self.toggle)
        self.toggle_btn.grid(row=1, column=0, padx=8, pady=8)

        self.status_label = tk.Label(root, textvariable=self.status_var, fg="red")
        self.status_label.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        self.newline_check = tk.Checkbutton(
            root, text="后缀另起一行", variable=self.newline_var, command=self._on_config_change
        )
        self.newline_check.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="w")

        self.suffix_var.trace_add("write", self._on_config_change)
        self.root.after(100, self._poll_status)

    def toggle(self) -> None:
        self.listener.set_enabled(not self.listener.enabled)

    def _poll_status(self) -> None:
        if self.listener.enabled:
            self.status_var.set("运行中")
            self.toggle_btn.config(text="停止")
            self.status_label.config(fg="green")
        else:
            self.status_var.set("已停止")
            self.toggle_btn.config(text="启动")
            self.status_label.config(fg="red")
        self.root.after(100, self._poll_status)

    def _on_config_change(self, *_args) -> None:
        save_config(self.config_path, self.suffix_var.get(), self.newline_var.get())


def main() -> None:
    root = tk.Tk()
    listener = Listener(
        get_config=lambda: load_config(CONFIG_PATH),
        is_qq_window=is_qq_foreground,
    )
    listener.start()
    try:
        App(root, listener, CONFIG_PATH)
        root.mainloop()
    finally:
        listener.stop()


if __name__ == "__main__":
    main()
