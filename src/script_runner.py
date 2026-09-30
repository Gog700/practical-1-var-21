"""Runs a startup script for the shell emulator."""


def run_script(emulator, path: str) -> bool:
    """Execute commands from a script file.

    Stops at the first error. Returns True on success.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        emulator.print_output(f"Ошибка: скрипт не найден: {path}")
        return False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        emulator.print_output(f"> {line}")
        result = emulator.execute(line)
        if result == "EXIT":
            emulator.root.destroy()
            return True
        if result:
            emulator.print_output(result)
        if result.startswith("Ошибка"):
            emulator.print_output("Скрипт остановлен из-за ошибки.")
            return False
    return True