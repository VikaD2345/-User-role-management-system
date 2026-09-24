"""Загрузка и сохранение объектов проекта в JSON-файлах."""

from __future__ import annotations

import json
import os
from typing import Any

from models import Group, Permission, Role, User


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


def load_permissions(filename: str) -> list[Permission]:
    """Загрузить разрешения из JSON как объекты Permission."""
    items = load_json(filename, [])
    return [Permission.from_data(item) for item in items]


def save_permissions(
    filename: str,
    permissions: list[Permission],
) -> None:
    """Сохранить разрешения в JSON."""
    payload = [
        {"id": item.id, "code": item.code, "title": item.title}
        for item in permissions
    ]
    save_json(filename, payload)


def load_roles(
    filename: str,
    permissions: list[Permission],
) -> list[Role]:
    """Загрузить роли из JSON как объекты Role."""
    items = load_json(filename, [])
    return [Role.from_data(item, permissions) for item in items]


def save_roles(filename: str, roles: list[Role]) -> None:
    """Сохранить роли в JSON, записывая id разрешений."""
    payload = [
        {
            "id": role.id,
            "name": role.name,
            "permission_ids": [item.id for item in role.permissions],
        }
        for role in roles
    ]
    save_json(filename, payload)


def load_groups(filename: str) -> list[Group]:
    """Загрузить группы из JSON как объекты Group."""
    items = load_json(filename, [])
    return [Group.from_data(item) for item in items]


def save_groups(filename: str, groups: list[Group]) -> None:
    """Сохранить группы в JSON."""
    payload = [
        {"id": group.id, "name": group.name}
        for group in groups
    ]
    save_json(filename, payload)


def load_users(
    filename: str,
    roles: list[Role],
    groups: list[Group],
) -> list[User]:
    """Загрузить пользователей и восстановить связи с Role и Group."""
    users: list[User] = []
    for item in load_json(filename, []):
        user = User.from_data(item, roles, groups)
        if user is not None:
            users.append(user)
    return users


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей, записывая id роли и группы."""
    payload = []
    for user in users:
        payload.append(
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "role_id": user.role.id,
                "group_id": user.group.id if user.group else None,
                "registration_date": user.registration_date,
            }
        )
    save_json(filename, payload)
