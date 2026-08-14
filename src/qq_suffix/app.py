from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path

import customtkinter as ctk

from qq_suffix.config import load_config, save_config
from qq_suffix.listener import Listener
from qq_suffix.window import is_qq_foreground

EMOJI_FONT = ("Segoe UI Emoji", 16)
EMOJIS = [
    "😀", "😂", "😊", "😍", "🤔", "😭",
    "👍", "🔥", "🎉", "❤️", "💯", "😅",
    "🙏", "✨", "😎", "🤣", "🥰", "😴",
    "🤯", "🎊", "💪", "🌟", "💖", "🥳",
]


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        # PyInstaller 打包后，config.json 放在 exe 所在目录
        return Path(sys.executable).parent
    return Path(__file__).resolve().parents[2]


CONFIG_PATH = get_base_dir() / "config.json"


class App:
    def __init__(self, root: ctk.CTk, listener: Listener, config_path: Path) -> None:
        self.root = root
        self.listener = listener
        self.config_path = config_path

        config = load_config(config_path)

        root.title("QQ 频道自动后缀")
        root.resizable(False, False)

        self.suffix_var = tk.StringVar(value=config.suffix)
        self.newline_var = tk.BooleanVar(value=config.newline)
        self.status_var = tk.StringVar(value="已停止")

        ctk.CTkLabel(root, text="后缀内容：").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry = ctk.CTkEntry(root, textvariable=self.suffix_var, width=240, font=EMOJI_FONT)
        self.entry.grid(row=0, column=1, padx=8, pady=8)

        self.emoji_toggle_btn = ctk.CTkButton(
            root, text="😊", width=40, font=EMOJI_FONT, command=self.toggle_emoji_panel
        )
        self.emoji_toggle_btn.grid(row=0, column=2, padx=8, pady=8)

        self.toggle_btn = ctk.CTkButton(root, text="启动", width=80, command=self.toggle)
        self.toggle_btn.grid(row=1, column=0, padx=8, pady=8)

        self.status_label = ctk.CTkLabel(root, textvariable=self.status_var, text_color="red")
        self.status_label.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        self.newline_check = ctk.CTkCheckBox(
            root, text="后缀另起一行", variable=self.newline_var, command=self._on_config_change
        )
        self.newline_check.grid(row=2, column=0, columnspan=3, padx=8, pady=8, sticky="w")

        self._build_emoji_panel()

        self.suffix_var.trace_add("write", self._on_config_change)
        self.root.after(100, self._poll_status)

    def _build_emoji_panel(self) -> None:
        self.emoji_panel = ctk.CTkFrame(self.root)
        self.emoji_panel.grid(row=3, column=0, columnspan=3, padx=8, pady=(0, 8), sticky="w")
        for i, emoji in enumerate(EMOJIS):
            row, col = divmod(i, 6)
            ctk.CTkButton(
                self.emoji_panel,
                text=emoji,
                width=36,
                height=32,
                font=EMOJI_FONT,
                command=lambda e=emoji: self.insert_emoji(e),
            ).grid(row=row, column=col, padx=2, pady=2)
        self.emoji_panel.grid_remove()

    def toggle_emoji_panel(self) -> None:
        if self.emoji_panel.winfo_manager():
            self.emoji_panel.grid_remove()
        else:
            self.emoji_panel.grid()

    def insert_emoji(self, emoji: str) -> None:
        self.suffix_var.set(self.suffix_var.get() + emoji)

    def toggle(self) -> None:
        self.listener.set_enabled(not self.listener.enabled)

    def _poll_status(self) -> None:
        if self.listener.enabled:
            self.status_var.set("运行中")
            self.toggle_btn.configure(text="停止")
            self.status_label.configure(text_color="green")
        else:
            self.status_var.set("已停止")
            self.toggle_btn.configure(text="启动")
            self.status_label.configure(text_color="red")
        self.root.after(100, self._poll_status)

    def _on_config_change(self, *_args) -> None:
        save_config(self.config_path, self.suffix_var.get(), self.newline_var.get())


def main() -> None:
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
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
