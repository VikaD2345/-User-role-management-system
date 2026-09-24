"""Класс разрешения и функции работы со справочником прав."""

from __future__ import annotations

from .entity import Entity
from utils import next_id


class Permission(Entity):
    """Разрешение на выполнение действия в системе."""

    def __init__(
        self,
        permission_id: int,
        code: str,
        title: str,
    ) -> None:
        super().__init__(permission_id, title)
        self.code = code
        self.title = title

    @classmethod
    def from_data(cls, data: dict) -> Permission:
        """Создать разрешение из словаря JSON."""
        return cls(data["id"], data["code"], data["title"])

    def __str__(self) -> str:
        return f"{self.code} — {self.title}"


def find_permission_by_id(
    permissions: list[Permission],
    permission_id: int,
) -> Permission | None:
    """Найти разрешение по идентификатору."""
    for permission in permissions:
        if permission.id == permission_id:
            return permission
    return None


def add_permission(
    permissions: list[Permission],
    code: str,
    title: str,
) -> Permission:
    """Добавить разрешение в коллекцию."""
    permission = Permission(next_id(permissions), code, title)
    permissions.append(permission)
    return permission
