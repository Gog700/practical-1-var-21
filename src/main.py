"""Shell emulator module: Stage 1 REPL."""

import getpass
import shlex
import socket
import tkinter as tk
from tkinter import scrolledtext
from typing import Callable, Dict, List, Tuple

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

    Supports both unquoted and quoted arguments.
    Raises ParseError if a quotation mark is not closed.
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


class ShellEmulator:
    """Graphical shell emulator (Stage 1)."""

    def __init__(self, root: tk.Tk) -> None:
        """Set up window title and widgets."""
        self.root = root
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

    def _print(self, text: str) -> None:
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
            return f"Ошибка: {exc}"
        if not cmd:
            return ""
        if cmd not in self.commands:
            return f"Ошибка: неизвестная команда '{cmd}'"
        try:
            return self.commands[cmd](args)
        except Exception as exc:
            return f"Ошибка выполнения: {exc}"

    def on_enter(self, event: tk.Event) -> None:
        """Handle Enter key in the input field."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._print(f"> {line}")
        result = self.execute(line)
        if result == "EXIT":
            self.root.destroy()
            return
        self._print(result)


def main() -> None:
    """Start the GUI application."""
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()