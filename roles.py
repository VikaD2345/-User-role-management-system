"""Функции для работы с ролями и разрешениями."""

from utils import next_id


def check_permission(role: str, permission: str) -> bool:
    """Проверяет, разрешено ли роли выполнять указанное действие."""
    if role == "администратор":
        return True
    elif role == "менеджер" and permission != "удаление_пользователей":
        return True
    elif role == "сотрудник" and permission == "просмотр_данных":
        return True
    else:
        return False


def describe_role(role: str) -> str:
    """Возвращает текстовое описание уровня доступа для роли."""
    if role == "администратор":
        return "полный доступ ко всем разделам системы"
    elif role == "менеджер":
        return "доступ ко всем разделам, кроме удаления пользователей"
    elif role == "сотрудник":
        return "доступ только на просмотр данных"
    else:
        return "доступ не определён"


def add_role(
    roles: dict[int, dict],
    name: str,
    permission_ids: list[int],
) -> dict:
    """Добавить роль в словарь roles."""
    role_id = next_id(roles)
    role = {
        "id": role_id,
        "name": name,
        "permission_ids": permission_ids,
    }
    roles[role_id] = role
    return role


def find_role_by_name(roles: dict[int, dict], name: str) -> dict | None:
    """Найти роль по точному имени без учёта регистра."""
    needle = name.casefold()
    for role in roles.values():
        if str(role.get("name", "")).casefold() == needle:
            return role
    return None


def get_permission_codes(
    roles: dict[int, dict],
    permissions: dict[int, dict],
    role_id: int,
) -> set[str]:
    """Вернуть множество кодов разрешений роли."""
    role = roles.get(role_id)
    if role is None:
        return set()
    codes = set()
    for permission_id in role.get("permission_ids", []):
        permission = permissions.get(permission_id)
        if permission is not None:
            codes.add(permission["code"])
    return codes


def role_allows_permission(
    roles: dict[int, dict],
    permissions: dict[int, dict],
    role_id: int,
    permission_code: str,
) -> bool:
    """Проверить разрешение по данным роли и функции из ПР1."""
    role = roles.get(role_id)
    if role is None:
        return False
    codes = get_permission_codes(roles, permissions, role_id)
    if permission_code in codes:
        return True
    return check_permission(role["name"], permission_code)
