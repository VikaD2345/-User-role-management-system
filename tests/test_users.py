"""Автоматические тесты функций работы с пользователями."""

from datetime import date

from users import (
    add_user,
    convert_age,
    filter_users_by_role,
    find_users,
    format_user_card,
    sort_users,
)


def test_add_user():
    users = {}
    user = add_user(
        users,
        "Иванова А.С.",
        27,
        2,
        1,
        date(2026, 9, 1),
    )
    assert len(users) == 1
    assert user["id"] == 1
    assert users[1]["name"] == "Иванова А.С."


def test_find_users():
    users = {}
    add_user(users, "Иванова А.С.", 27, 2, 1, date(2026, 9, 1))
    add_user(users, "Петров И.К.", 31, 3, 1, date(2026, 9, 3))
    found = find_users(users, "иванова")
    assert len(found) == 1
    assert found[0]["name"] == "Иванова А.С."


def test_convert_age():
    assert convert_age("27") == 27
    assert convert_age("-1") == 0
    assert convert_age("abc") == 0


def test_format_user_card():
    card = format_user_card("Иванова А.С.", "менеджер", "Отдел продаж", 27)
    assert "Иванова А.С." in card
    assert "менеджер" in card
    assert "Отдел продаж" in card


def test_filter_and_sort_users():
    users = {}
    add_user(users, "Петров И.К.", 31, 3, 1, date(2026, 9, 3))
    add_user(users, "Иванова А.С.", 27, 2, 1, date(2026, 9, 1))
    add_user(users, "Кузнецов Д.А.", 22, 3, 3, date(2026, 9, 10))
    employees = list(filter_users_by_role(users, 3))
    assert len(employees) == 2
    sorted_users = sort_users(users, "age")
    assert sorted_users[0]["age"] == 22
    assert sorted_users[-1]["age"] == 31
