# Эмулятор оболочки ОС — Вариант №21

## Общее описание

Эмулятор UNIX-подобной оболочки с графическим интерфейсом (Tkinter).
Реализованы Этапы 1 и 2:

- **Этап 1 (REPL):** интерактивный ввод команд, парсер с поддержкой
  кавычек, команды-заглушки `ls`, `cd`, `exit`, обработка ошибок.
- **Этап 2 (Конфигурация):** параметры командной строки, XML-логирование
  событий, запуск стартового скрипта с остановкой при первой ошибке.

## Структура проекта

```
shell-emulator/
├── src/
│   ├── main.py            # точка входа, GUI, парсер, обработка команд
│   ├── logger.py          # XML-логирование событий
│   └── script_runner.py   # запуск стартового скрипта
├── tests/
│   └── test_parser.py     # unit-тесты на парсер и заглушки
├── scripts/
│   ├── start.txt          # стартовый скрипт эмулятора
│   ├── run_windows.bat    # запуск на Windows
│   ├── run_linux.sh       # запуск на Linux/macOS
│   ├── test_no_args.bat   # тест без параметров
│   ├── test_log_only.bat  # тест только с --log
│   ├── test_script_only.bat
│   └── test_all_args.bat
├── logs/                  # создаётся автоматически, в .gitignore
├── .gitignore
├── README.md
├── run.bat                # ярлык запуска для Windows
└── run.sh                 # ярлык запуска для Linux/macOS
```

## Функции и настройки

### Параметры командной строки

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--vfs` | Путь к физическому расположению VFS | не задан |
| `--log` | Путь к лог-файлу в формате XML | не задан |
| `--script` | Путь к стартовому скрипту | не задан |

### Основные модули

- **`main.py`**
  - `parse_args()` — парсинг аргументов командной строки.
  - `parse_line(line)` — разбор строки на команду и аргументы с
    поддержкой кавычек (одинарных и двойных).
  - `cmd_ls`, `cmd_cd`, `cmd_exit` — команды-заглушки.
  - `ShellEmulator` — класс GUI-приложения.
  - `execute(line)` — выполнение команды с логированием.

- **`logger.py`**
  - `XMLLogger` — ведёт XML-лог событий.
  - Каждая запись `<event>` содержит `timestamp`, `user`, `command`,
    `args`, `error`.

- **`script_runner.py`**
  - `run_script(emulator, path)` — выполняет команды из файла
    последовательно, останавливается при первой ошибке.

### Команды оболочки

| Команда | Описание |
|---------|----------|
| `ls` | Заглушка: выводит своё имя и аргументы |
| `cd` | Заглушка: выводит своё имя и аргументы |
| `exit` | Завершает работу эмулятора |

### Обработка ошибок

- **Незакрытая кавычка** → `Ошибка: незакрытая кавычка`
- **Неизвестная команда** → `Ошибка: неизвестная команда 'имя'`

## Сборка и запуск

### Linux / macOS

```bash
./run.sh
```

или

```bash
./scripts/run_linux.sh
```

### Windows

```bat
run.bat
```

или

```bat
scripts\run_windows.bat
```

### Универсально (любая ОС с Python 3.8+)

```bash
python src/main.py
```

### С параметрами

```bash
python src/main.py \
  --vfs data/vfs.zip \
  --log logs/emulator.xml \
  --script scripts/start.txt
```

### Запуск тестов

```bash
python -m unittest discover tests
```

Ожидаемый результат: `Ran 8 tests ... OK`.

## Примеры использования

### Интерактивный режим

После запуска в поле ввода введите команду и нажмите Enter:

```
> ls -la
ls: имя команды = ls, аргументы = ['-la']

> cd /home
cd: имя команды = cd, аргументы = ['/home']

> ls "hello world"
ls: имя команды = ls, аргументы = ['hello world']

> ls "hello
Ошибка: незакрытая кавычка

> qwerty
Ошибка: неизвестная команда 'qwerty'

> exit
(окно закрывается)
```

### Стартовый скрипт (`scripts/start.txt`)

```
ls -la
cd /home
ls "hello world"
qwerty
exit
```

При запуске с `--script scripts/start.txt` команды выполнятся
автоматически. На строке `qwerty` скрипт остановится из-за ошибки —
это требование этапа.

### Пример XML-лога

```xml
<?xml version='1.0' encoding='utf-8'?>
<log>
  <event>
    <timestamp>2026-09-30T14:22:01.123</timestamp>
    <user>User</user>
    <command>ls</command>
    <args>-la</args>
    <error />
  </event>
  <event>
    <timestamp>2026-09-30T14:22:01.130</timestamp>
    <user>User</user>
    <command>qwerty</command>
    <args />
    <error>Ошибка: неизвестная команда 'qwerty'</error>
  </event>
</log>
```

## Тестирование параметров командной строки

Созданы скрипты реальной ОС для проверки всех комбинаций:

| Скрипт | Что проверяет |
|--------|---------------|
| `scripts/test_no_args.bat` | Запуск без параметров |
| `scripts/test_log_only.bat` | Только `--log` |
| `scripts/test_script_only.bat` | Только `--script` |
| `scripts/test_all_args.bat` | Все три параметра |

## Требования к окружению

- Python 3.8 или новее
- Модуль `tkinter` (входит в стандартную поставку Python для
  Windows и macOS; на Linux может потребоваться
  `sudo apt install python3-tk`)