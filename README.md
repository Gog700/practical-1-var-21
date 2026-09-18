# Эмулятор оболочки ОС — Вариант №21

## Общее описание

Минимальный прототип эмулятора UNIX-подобной оболочки
с графическим интерфейсом (Tkinter). Этап 1 — REPL.

## Функции

- `get_prompt_data()` — возвращает `username@hostname`.
- `parse_line(line)` — делит строку на команду и аргументы.
- `cmd_ls`, `cmd_cd`, `cmd_exit` — команды-заглушки.
- `ShellEmulator` — класс GUI-приложения.

## Сборка и запуск

```bash
./run.sh
```

Или напрямую:

```bash
python3 src/main.py
```

## Тесты

```bash
python -m unittest discover tests
```

## Примеры использования

```
> ls -la
ls: имя команды = ls, аргументы = ['-la']

> cd /home
cd: имя команды = cd, аргументы = ['/home']

> unknown
Ошибка: неизвестная команда 'unknown'

> exit
(окно закрывается)
```