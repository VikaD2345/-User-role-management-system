"""Автоматические тесты роли, разрешения и доступа."""

from models import Permission, Role
from models.roles import add_role, check_permission, describe_role


def test_permission_creation() -> None:
    permission = Permission(1, "просмотр_данных", "Просмотр данных")
    assert permission.id == 1
    assert permission.code == "просмотр_данных"
    assert "просмотр_данных" in str(permission)


def test_role_creation() -> None:
    view = Permission(1, "просмотр_данных", "Просмотр")
    edit = Permission(2, "редактирование_данных", "Правка")
    role = Role(2, "менеджер", [view, edit])
    assert role.id == 2
    assert role.name == "менеджер"
    assert view in role.permissions


def test_check_permission() -> None:
    assert check_permission("администратор", "удаление_пользователей")
    assert check_permission("менеджер", "просмотр_данных")
    assert not check_permission("менеджер", "удаление_пользователей")
    assert check_permission("сотрудник", "просмотр_данных")
    assert not check_permission("сотрудник", "редактирование_данных")


def test_describe_role() -> None:
    text = describe_role("менеджер")
    assert "кроме удаления пользователей" in text


def test_role_has_permission() -> None:
    view = Permission(1, "просмотр_данных", "Просмотр")
    edit = Permission(2, "редактирование_данных", "Правка")
    role = add_role([], "менеджер", [view, edit])
    assert "просмотр_данных" in role.permission_codes()
    assert role.has_permission("просмотр_данных")
    assert not role.has_permission("удаление_пользователей")


def test_role_from_data() -> None:
    permissions = [
        Permission(1, "просмотр_данных", "Просмотр"),
        Permission(3, "удаление_пользователей", "Удаление"),
    ]
    data = {"id": 1, "name": "администратор", "permission_ids": [1, 3]}
    role = Role.from_data(data, permissions)
    assert role.name == "администратор"
    assert len(role.permissions) == 2
    assert role.has_permission("удаление_пользователей")


def test_role_static_validate() -> None:
    assert Role.check_permission("сотрудник", "просмотр_данных")
    assert not Role.check_permission("сотрудник", "удаление_пользователей")
