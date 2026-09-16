"""Функции для работы с группами пользователей."""

from utils import next_id


def add_group(groups: dict[int, dict], name: str) -> dict:
    """Добавить группу в словарь groups."""
    group_id = next_id(groups)
    group = {
        "id": group_id,
        "name": name,
    }
    groups[group_id] = group
    return group


def find_groups(groups: dict[int, dict], query: str) -> list[dict]:
    """Найти группы по подстроке названия."""
    needle = query.casefold()
    found = []
    for group in groups.values():
        if needle in str(group.get("name", "")).casefold():
            found.append(group)
    return found


def add_user_to_group(
    users: dict[int, dict],
    user_id: int,
    group_id: int,
) -> bool:
    """Включить пользователя в группу."""
    user = users.get(user_id)
    if user is None:
        return False
    user["group_id"] = group_id
    return True


def remove_user_from_group(users: dict[int, dict], user_id: int) -> bool:
    """Исключить пользователя из группы."""
    user = users.get(user_id)
    if user is None:
        return False
    user["group_id"] = None
    return True


def get_group_members(
    users: dict[int, dict],
    group_id: int,
) -> list[dict]:
    """Вернуть список пользователей указанной группы."""
    members = []
    for user in users.values():
        if user.get("group_id") == group_id:
            members.append(user)
    return members
