"""Вспомогательные функции ввода, идентификаторов и интроспекции."""

from datetime import date, datetime
from functools import wraps
import inspect
from typing import Any, Callable


def next_id(items: list[Any]) -> int:
    """Вернуть следующий целочисленный идентификатор для коллекции."""
    if not items:
        return 1
    return max(item.id for item in items) + 1


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется, программа не падает.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            return int(raw_value)
        except ValueError:
            print("Нужно целое число. Повторите ввод.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return datetime.strptime(raw_value, "%d.%m.%Y").date()
        except ValueError:
            print("Некорректная дата. Используйте формат ДД.ММ.ГГГГ.")


def input_nonempty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        raw_value = input(prompt).strip()
        if raw_value:
            return raw_value
        print("Значение не может быть пустым. Повторите ввод.")


def describe_function(func: Callable[..., Any]) -> str:
    """Кратко описать функцию средствами интроспекции."""
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func) or "Документация отсутствует"
    first_line = docstring.splitlines()[0]
    return f"{func.__name__}{signature} — {first_line}"


def log_action(func: Callable[..., Any]) -> Callable[..., Any]:
    """Учебный декоратор: сохраняет метаданные функции через wraps."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper
