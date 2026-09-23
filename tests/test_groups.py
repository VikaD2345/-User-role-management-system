"""Автоматические тесты группы и связи пользователь — группа."""

from datetime import date

from models import Group, Permission, Role, User
from models.groups import (
    add_group,
    add_user_to_group,
    get_group_members,
    remove_user_from_group,
)
from models.users import add_user


def test_group_creation() -> None:
    group = Group(1, "Отдел продаж")
    assert group.id == 1
    assert group.name == "Отдел продаж"
    assert "Отдел продаж" in str(group)


def test_add_group() -> None:
    groups: list[Group] = []
    group = add_group(groups, "Отдел продаж")
    assert len(groups) == 1
    assert group.name == "Отдел продаж"


def test_group_membership() -> None:
    role = Role(2, "менеджер", [Permission(1, "просмотр_данных", "Просмотр")])
    groups: list[Group] = []
    users: list[User] = []
    group = add_group(groups, "Отдел продаж")
    user = add_user(
        users,
        "Иванова А.С.",
        27,
        role,
        None,
        date(2026, 9, 1),
    )
    add_user_to_group(user, group)
    members = get_group_members(users, group)
    assert len(members) == 1
    assert members[0] is user
    assert user.group is group
    remove_user_from_group(user)
    assert user.group is None
