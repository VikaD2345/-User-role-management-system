"""Автоматические тесты функций ролей и разрешений."""

from roles import (
    add_role,
    check_permission,
    describe_role,
    get_permission_codes,
    role_allows_permission,
)


def test_check_permission():
    assert check_permission("администратор", "удаление_пользователей")
    assert check_permission("менеджер", "просмотр_данных")
    assert not check_permission("менеджер", "удаление_пользователей")
    assert check_permission("сотрудник", "просмотр_данных")
    assert not check_permission("сотрудник", "редактирование_данных")


def test_describe_role():
    text = describe_role("менеджер")
    assert "кроме удаления пользователей" in text


def test_role_allows_permission():
    roles = {}
    add_role(roles, "менеджер", [1, 2])
    permissions = {
        1: {"id": 1, "code": "просмотр_данных", "title": "Просмотр"},
        2: {"id": 2, "code": "редактирование_данных", "title": "Правка"},
        3: {"id": 3, "code": "удаление_пользователей", "title": "Удаление"},
    }
    codes = get_permission_codes(roles, permissions, 1)
    assert "просмотр_данных" in codes
    assert role_allows_permission(
        roles,
        permissions,
        1,
        "просмотр_данных",
    )
    assert not role_allows_permission(
        roles,
        permissions,
        1,
        "удаление_пользователей",
    )
