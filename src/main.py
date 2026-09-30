"""Shell emulator module: Stage 2 configuration."""

import argparse
import getpass
import shlex
import socket
import tkinter as tk
from tkinter import scrolledtext
from typing import Callable, Dict, List, Tuple

from logger import XMLLogger
from script_runner import run_script

WINDOW_WIDTH = 80
WINDOW_HEIGHT = 20


class ParseError(Exception):
    """Raised when a command line cannot be parsed."""


def get_prompt_data() -> str:
    """Return username@hostname for the window title."""
    try:
        username = getpass.getuser()
    except Exception:
        username = "user"
    hostname = socket.gethostname()
    return f"{username}@{hostname}"


def parse_line(line: str) -> Tuple[str, List[str]]:
    """Split a line into command and arguments.

    Supports quoted arguments. Raises ParseError on unclosed quote.
    """
    stripped = line.strip()
    if not stripped:
        return "", []
    try:
        parts = shlex.split(stripped, posix=True)
    except ValueError as exc:
        raise ParseError("незакрытая кавычка") from exc
    if not parts:
        return "", []
    return parts[0], parts[1:]


def cmd_ls(args: List[str]) -> str:
    """Stub for the 'ls' command."""
    return f"ls: имя команды = ls, аргументы = {args}"


def cmd_cd(args: List[str]) -> str:
    """Stub for the 'cd' command."""
    return f"cd: имя команды = cd, аргументы = {args}"


def cmd_exit(args: List[str]) -> str:
    """Stub for the 'exit' command."""
    return "EXIT"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Shell emulator")
    parser.add_argument("--vfs", default="", help="Путь к VFS")
    parser.add_argument("--log", default="", help="Путь к лог-файлу")
    parser.add_argument("--script", default="", help="Стартовый скрипт")
    return parser.parse_args()


class ShellEmulator:
    """Graphical shell emulator (Stage 2)."""

    def __init__(self, root: tk.Tk, logger=None) -> None:
        """Set up window title, logger and widgets."""
        self.root = root
        self.logger = logger
        self.commands: Dict[str, Callable] = {
            "ls": cmd_ls,
            "cd": cmd_cd,
            "exit": cmd_exit,
        }
        self.root.title(f"Эмулятор - {get_prompt_data()}")
        self._build_ui()

    def _build_ui(self) -> None:
        """Create output area and input field."""
        self.output = scrolledtext.ScrolledText(
            self.root, width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT, state="disabled"
        )
        self.output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(padx=5, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def print_output(self, text: str) -> None:
        """Append a message to the output area."""
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def execute(self, line: str) -> str:
        """Execute a command line and return the result."""
        try:
            cmd, args = parse_line(line)
        except ParseError as exc:
            error = f"Ошибка: {exc}"
            if self.logger:
                self.logger.log(line, [], error)
            return error
        if not cmd:
            return ""
        if cmd not in self.commands:
            error = f"Ошибка: неизвестная команда '{cmd}'"
            if self.logger:
                self.logger.log(cmd, args, error)
            return error
        try:
            result = self.commands[cmd](args)
        except Exception as exc:
            error = f"Ошибка выполнения: {exc}"
            if self.logger:
                self.logger.log(cmd, args, error)
            return error
        if self.logger:
            self.logger.log(cmd, args, "")
        return result

    def on_enter(self, event: tk.Event) -> None:
        """Handle Enter key in the input field."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print_output(f"> {line}")
        result = self.execute(line)
        if result == "EXIT":
            self.root.destroy()
            return
        self.print_output(result)


def main() -> None:
    """Start the GUI application."""
    args = parse_args()
    print("Параметры запуска:")
    print(f"  VFS:              {args.vfs or '(не задан)'}")
    print(f"  Лог-файл:         {args.log or '(не задан)'}")
    print(f"  Стартовый скрипт: {args.script or '(не задан)'}")

    logger = XMLLogger(args.log) if args.log else None

    root = tk.Tk()
    emulator = ShellEmulator(root, logger)
    if args.script:
        root.after(300, lambda: run_script(emulator, args.script))
    root.mainloop()


if __name__ == "__main__":
    main()