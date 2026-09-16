"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
import os
from typing import Any


def load_json(filename: str, default: Any) -> Any:
    """Загрузить данные из JSON-файла.

    Отсутствие файла и повреждённый JSON не завершают программу аварийно.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, используются пустые данные.")
        return default


def save_json(filename: str, data: Any) -> None:
    """Сохранить данные в JSON-файл через контекстный менеджер with."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def _to_dict(items: list[dict]) -> dict[int, dict]:
    """Преобразовать список записей в словарь по полю id."""
    result = {}
    for item in items:
        result[item["id"]] = item
    return result


def load_users(filename: str) -> dict[int, dict]:
    """Загрузить пользователей из JSON-файла."""
    return _to_dict(load_json(filename, []))


def save_users(filename: str, users: dict[int, dict]) -> None:
    """Сохранить пользователей в JSON-файл."""
    save_json(filename, list(users.values()))


def load_roles(filename: str) -> dict[int, dict]:
    """Загрузить роли из JSON-файла."""
    return _to_dict(load_json(filename, []))


def save_roles(filename: str, roles: dict[int, dict]) -> None:
    """Сохранить роли в JSON-файл."""
    save_json(filename, list(roles.values()))


def load_permissions(filename: str) -> dict[int, dict]:
    """Загрузить разрешения из JSON-файла."""
    return _to_dict(load_json(filename, []))


def save_permissions(
    filename: str,
    permissions: dict[int, dict],
) -> None:
    """Сохранить разрешения в JSON-файл."""
    save_json(filename, list(permissions.values()))


def load_groups(filename: str) -> dict[int, dict]:
    """Загрузить группы из JSON-файла."""
    return _to_dict(load_json(filename, []))


def save_groups(filename: str, groups: dict[int, dict]) -> None:
    """Сохранить группы в JSON-файл."""
    save_json(filename, list(groups.values()))
