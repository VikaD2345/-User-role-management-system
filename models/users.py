"""Класс пользователя и функции работы с пользователями."""

from __future__ import annotations

from datetime import date

from .entity import Entity
from .groups import Group, find_group_by_id
from .roles import Role, find_role_by_id
from utils import next_id


class User(Entity):
    """Пользователь системы с ролью и группой."""

    def __init__(
        self,
        user_id: int,
        name: str,
        age: int,
        role: Role,
        group: Group | None,
        registration_date: str,
    ) -> None:
        super().__init__(user_id, name)
        self.age = age
        self.role = role
        self.group = group
        self.registration_date = registration_date

    def assign_role(self, role: Role) -> None:
        """Назначить пользователю роль."""
        self.role = role

    def set_group(self, group: Group | None) -> None:
        """Назначить или сбросить группу пользователя."""
        self.group = group

    def has_permission(self, permission_code: str) -> bool:
        """Проверить, есть ли у пользователя разрешение."""
        return self.role.has_permission(permission_code)

    @staticmethod
    def validate_age(age: int) -> bool:
        """Проверить, что возраст находится в допустимом диапазоне."""
        return 0 < age <= 120

    @classmethod
    def from_data(
        cls,
        data: dict,
        roles: list[Role],
        groups: list[Group],
    ) -> User | None:
        """Создать пользователя из JSON, связав роль и группу."""
        role = find_role_by_id(roles, data["role_id"])
        if role is None:
            return None
        group = None
        group_id = data.get("group_id")
        if isinstance(group_id, int):
            group = find_group_by_id(groups, group_id)
        return cls(
            data["id"],
            data["name"],
            data["age"],
            role,
            group,
            data["registration_date"],
        )

    def __str__(self) -> str:
        group_name = self.group.name if self.group else "без группы"
        return (
            f"{self.name} | роль: {self.role.name} | "
            f"группа: {group_name} | возраст: {self.age} лет"
        )


def convert_age(age_str: str) -> int:
    """Преобразует возраст из строки в число и проверяет его корректность."""
    try:
        age_value = int(age_str)
    except ValueError:
        return 0
    if not User.validate_age(age_value):
        return 0
    return age_value


def format_user_card(name: str, role: str, group: str, age: int) -> str:
    """Формирует единую строку-карточку пользователя для вывода."""
    return (
        f"{name} | роль: {role} | группа: {group} | возраст: {age} лет"
    )


def add_user(
    users: list[User],
    name: str,
    age: int,
    role: Role,
    group: Group | None,
    registration_date: date,
) -> User:
    """Создать объект User и добавить его в коллекцию."""
    user = User(
        next_id(users),
        name,
        age,
        role,
        group,
        registration_date.isoformat(),
    )
    users.append(user)
    return user


def get_user(users: list[User], user_id: int) -> User | None:
    """Вернуть пользователя по идентификатору или None."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_users(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени."""
    needle = query.casefold()
    found = []
    for user in users:
        if needle in user.name.casefold():
            found.append(user)
    return found


def filter_users_by_role(users: list[User], role: Role):
    """Отобрать пользователей с указанной ролью (генератор)."""
    return (user for user in users if user.role.id == role.id)


def sort_users(users: list[User], field: str = "name") -> list[User]:
    """Отсортировать пользователей по полю с помощью lambda-функции."""
    return sorted(
        users,
        key=lambda item: getattr(item, field),
    )


def show_users(users: list[User]) -> None:
    """Вывести список пользователей в виде карточек."""
    if not users:
        print("Пользователи пока не добавлены.")
        return
    print("\nСписок пользователей:")
    for user in users:
        print(
            f"[{user.id}] {user} | "
            f"дата регистрации: {user.registration_date}"
        )
