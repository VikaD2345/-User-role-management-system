"""Функции для работы с пользователями."""

from datetime import date

from utils import next_id


def convert_age(age_str: str) -> int:
    """Преобразует возраст из строки в число и проверяет его корректность."""
    try:
        age_value = int(age_str)
    except ValueError:
        return 0
    if age_value < 0 or age_value > 120:
        return 0
    return age_value


def format_user_card(name: str, role: str, group: str, age: int) -> str:
    """Формирует единую строку-карточку пользователя для вывода."""
    return (
        f"{name} | роль: {role} | группа: {group} | возраст: {age} лет"
    )


def add_user(
    users: dict[int, dict],
    name: str,
    age: int,
    role_id: int,
    group_id: int | None,
    registration_date: date,
) -> dict:
    """Добавить пользователя в словарь users и вернуть его запись."""
    user_id = next_id(users)
    user = {
        "id": user_id,
        "name": name,
        "age": age,
        "role_id": role_id,
        "group_id": group_id,
        "registration_date": registration_date.isoformat(),
    }
    users[user_id] = user
    return user


def get_user(users: dict[int, dict], user_id: int) -> dict | None:
    """Вернуть пользователя по идентификатору или None."""
    return users.get(user_id)


def find_users(users: dict[int, dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке имени."""
    needle = query.casefold()
    found = []
    for user in users.values():
        if needle in str(user.get("name", "")).casefold():
            found.append(user)
    return found


def filter_users_by_role(users: dict[int, dict], role_id: int):
    """Отобрать пользователей с указанной ролью.

    Возвращает генератор, чтобы не создавать лишний список заранее.
    """
    return (
        user
        for user in users.values()
        if user.get("role_id") == role_id
    )


def sort_users(
    users: dict[int, dict],
    field: str = "name",
) -> list[dict]:
    """Отсортировать пользователей по полю с помощью lambda-функции."""
    return sorted(
        users.values(),
        key=lambda item: item.get(field, ""),
    )


def assign_role(
    users: dict[int, dict],
    user_id: int,
    role_id: int,
) -> bool:
    """Назначить пользователю роль. Вернуть True, если пользователь найден."""
    user = users.get(user_id)
    if user is None:
        return False
    user["role_id"] = role_id
    return True
