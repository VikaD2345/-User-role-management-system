"""Класс группы и функции работы с группами."""

from __future__ import annotations

from typing import TYPE_CHECKING

from models.entity import Entity
from utils import next_id

if TYPE_CHECKING:
    from models.users import User


class Group(Entity):
    """Группа пользователей, например отдел организации."""

    def __init__(self, group_id: int, name: str) -> None:
        super().__init__(group_id, name)

    @classmethod
    def from_data(cls, data: dict) -> Group:
        """Создать группу из словаря JSON."""
        return cls(data["id"], data["name"])

    def __str__(self) -> str:
        return f"{self.name}"


def find_group_by_id(groups: list[Group], group_id: int) -> Group | None:
    """Найти группу по идентификатору."""
    for group in groups:
        if group.id == group_id:
            return group
    return None


def find_groups(groups: list[Group], query: str) -> list[Group]:
    """Найти группы по подстроке названия."""
    needle = query.casefold()
    found = []
    for group in groups:
        if needle in group.name.casefold():
            found.append(group)
    return found


def add_group(groups: list[Group], name: str) -> Group:
    """Создать объект Group и добавить его в коллекцию."""
    group = Group(next_id(groups), name)
    groups.append(group)
    return group


def add_user_to_group(user: User, group: Group) -> None:
    """Включить пользователя в группу через объект Group."""
    user.set_group(group)


def remove_user_from_group(user: User) -> None:
    """Исключить пользователя из группы."""
    user.set_group(None)


def get_group_members(users: list[User], group: Group) -> list[User]:
    """Вернуть список пользователей указанной группы."""
    members = []
    for user in users:
        if user.group is not None and user.group.id == group.id:
            members.append(user)
    return members


def show_groups(groups: list[Group], users: list[User]) -> None:
    """Вывести группы и число участников."""
    if not groups:
        print("Группы пока не добавлены.")
        return
    print("\nГруппы:")
    for group in groups:
        members = get_group_members(users, group)
        print(
            f"[{group.id}] {group.name} — участников: {len(members)}"
        )
        for member in members:
            print(f"    - {member.name}")
