"""Автоматические тесты функций групп."""

from datetime import date

from groups import (
    add_group,
    add_user_to_group,
    get_group_members,
    remove_user_from_group,
)
from users import add_user


def test_add_group():
    groups = {}
    group = add_group(groups, "Отдел продаж")
    assert len(groups) == 1
    assert group["name"] == "Отдел продаж"


def test_group_membership():
    users = {}
    groups = {}
    add_group(groups, "Отдел продаж")
    add_user(users, "Иванова А.С.", 27, 2, None, date(2026, 9, 1))
    assert add_user_to_group(users, 1, 1)
    members = get_group_members(users, 1)
    assert len(members) == 1
    assert members[0]["name"] == "Иванова А.С."
    assert remove_user_from_group(users, 1)
    assert users[1]["group_id"] is None
