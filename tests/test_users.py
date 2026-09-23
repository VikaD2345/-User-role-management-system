"""Автоматические тесты пользователя и коллекции User."""

from datetime import date

from models import Group, Permission, Role, User
from models.users import (
    add_user,
    convert_age,
    filter_users_by_role,
    find_users,
    format_user_card,
    sort_users,
)


def _sample_role() -> Role:
    permission = Permission(1, "просмотр_данных", "Просмотр данных")
    return Role(2, "менеджер", [permission])


def test_user_creation() -> None:
    role = _sample_role()
    group = Group(1, "Отдел продаж")
    user = User(1, "Иванова А.С.", 27, role, group, "2026-09-01")
    assert user.id == 1
    assert user.name == "Иванова А.С."
    assert user.age == 27
    assert user.role is role
    assert user.group is group


def test_user_str() -> None:
    role = _sample_role()
    group = Group(1, "Отдел продаж")
    user = User(1, "Иванова А.С.", 27, role, group, "2026-09-01")
    text = str(user)
    assert "Иванова А.С." in text
    assert "менеджер" in text
    assert "Отдел продаж" in text


def test_user_from_data() -> None:
    role = _sample_role()
    group = Group(1, "Отдел продаж")
    data = {
        "id": 1,
        "name": "Иванова А.С.",
        "age": 27,
        "role_id": 2,
        "group_id": 1,
        "registration_date": "2026-09-01",
    }
    user = User.from_data(data, [role], [group])
    assert user is not None
    assert user.role is role
    assert user.group is group


def test_add_user() -> None:
    users: list[User] = []
    role = _sample_role()
    user = add_user(
        users,
        "Иванова А.С.",
        27,
        role,
        None,
        date(2026, 9, 1),
    )
    assert len(users) == 1
    assert user.id == 1
    assert users[0].name == "Иванова А.С."


def test_find_users() -> None:
    users: list[User] = []
    role = _sample_role()
    add_user(users, "Иванова А.С.", 27, role, None, date(2026, 9, 1))
    add_user(users, "Петров И.К.", 31, role, None, date(2026, 9, 3))
    found = find_users(users, "иванова")
    assert len(found) == 1
    assert found[0].name == "Иванова А.С."


def test_convert_age() -> None:
    assert convert_age("27") == 27
    assert convert_age("-1") == 0
    assert convert_age("abc") == 0


def test_format_user_card() -> None:
    card = format_user_card("Иванова А.С.", "менеджер", "Отдел продаж", 27)
    assert "Иванова А.С." in card
    assert "менеджер" in card


def test_filter_and_sort_users() -> None:
    manager = _sample_role()
    employee = Role(3, "сотрудник", [])
    users: list[User] = []
    add_user(users, "Петров И.К.", 31, employee, None, date(2026, 9, 3))
    add_user(users, "Иванова А.С.", 27, manager, None, date(2026, 9, 1))
    add_user(users, "Кузнецов Д.А.", 22, employee, None, date(2026, 9, 10))
    employees = list(filter_users_by_role(users, employee))
    assert len(employees) == 2
    sorted_users = sort_users(users, "age")
    assert sorted_users[0].age == 22
    assert sorted_users[-1].age == 31
