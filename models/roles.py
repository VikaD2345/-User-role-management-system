"""Класс роли и функции работы с ролями."""

from __future__ import annotations

from .entity import Entity
from .permissions import Permission, find_permission_by_id
from utils import next_id


class Role(Entity):
    """Роль пользователя: набор разрешений и правила доступа."""

    def __init__(
        self,
        role_id: int,
        name: str,
        permissions: list[Permission] | None = None,
    ) -> None:
        super().__init__(role_id, name)
        self._permissions = permissions if permissions is not None else []

    @property
    def permissions(self) -> list[Permission]:
        """Вернуть список разрешений роли."""
        return self._permissions

    @staticmethod
    def check_permission(role: str, permission: str) -> bool:
        """Проверить право по имени роли (функция ПР1)."""
        if role == "администратор":
            return True
        if role == "менеджер" and permission != "удаление_пользователей":
            return True
        if role == "сотрудник" and permission == "просмотр_данных":
            return True
        return False

    @property
    def access_description(self) -> str:
        """Текстовое описание уровня доступа роли."""
        return describe_role(self.name)

    def permission_codes(self) -> set[str]:
        """Вернуть множество кодов разрешений роли."""
        return {item.code for item in self._permissions}

    def has_permission(self, permission_code: str) -> bool:
        """Проверить право по JSON-данным роли и правилу ПР1."""
        if permission_code in self.permission_codes():
            return True
        return Role.check_permission(self.name, permission_code)

    @classmethod
    def from_data(
        cls,
        data: dict,
        permissions: list[Permission],
    ) -> Role:
        """Создать роль из словаря JSON и списка разрешений."""
        linked: list[Permission] = []
        for permission_id in data.get("permission_ids", []):
            permission = find_permission_by_id(permissions, permission_id)
            if permission is not None:
                linked.append(permission)
        return cls(data["id"], data["name"], linked)

    def __str__(self) -> str:
        return f"{self.name} — {self.access_description}"


def check_permission(role: str, permission: str) -> bool:
    """Обёртка ПР1: проверка права по имени роли."""
    return Role.check_permission(role, permission)


def describe_role(role: str) -> str:
    """Вернуть текстовое описание уровня доступа для роли."""
    if role == "администратор":
        return "полный доступ ко всем разделам системы"
    if role == "менеджер":
        return "доступ ко всем разделам, кроме удаления пользователей"
    if role == "сотрудник":
        return "доступ только на просмотр данных"
    return "доступ не определён"


def find_role_by_id(roles: list[Role], role_id: int) -> Role | None:
    """Найти роль по идентификатору."""
    for role in roles:
        if role.id == role_id:
            return role
    return None


def find_role_by_name(roles: list[Role], name: str) -> Role | None:
    """Найти роль по точному имени без учёта регистра."""
    needle = name.casefold()
    for role in roles:
        if role.name.casefold() == needle:
            return role
    return None


def add_role(
    roles: list[Role],
    name: str,
    permissions: list[Permission],
) -> Role:
    """Создать объект Role и добавить его в коллекцию."""
    role = Role(next_id(roles), name, permissions)
    roles.append(role)
    return role


def show_roles(roles: list[Role]) -> None:
    """Вывести роли и связанные с ними разрешения."""
    if not roles:
        print("Роли пока не добавлены.")
        return
    print("\nРоли и разрешения:")
    for role in roles:
        codes = sorted(role.permission_codes())
        codes_text = ", ".join(codes) if codes else "нет"
        print(f"[{role.id}] {role}")
        print(f"    разрешения: {codes_text}")
