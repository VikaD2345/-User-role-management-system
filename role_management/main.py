"""Точка запуска системы управления пользовательскими ролями."""

from datetime import date
import os

from models import Group, Permission, Role, User
from models.groups import (
    add_user_to_group,
    find_group_by_id,
    remove_user_from_group,
    show_groups,
)
from models.roles import (
    check_permission,
    find_role_by_id,
    find_role_by_name,
    show_roles,
)
from models.users import (
    add_user,
    convert_age,
    filter_users_by_role,
    find_users,
    format_user_card,
    get_user,
    show_users,
    sort_users,
)
from storage import (
    load_groups,
    load_permissions,
    load_roles,
    load_users,
    save_groups,
    save_roles,
    save_users,
)
from utils import (
    describe_function,
    input_int,
    input_nonempty,
    log_action,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ROLES_FILE = os.path.join(DATA_DIR, "roles.json")
PERMISSIONS_FILE = os.path.join(DATA_DIR, "permissions.json")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.json")

MENU_TEXT = """
=== Система управления пользовательскими ролями ===
1. Показать пользователей
2. Найти пользователя по имени
3. Добавить пользователя
4. Назначить роль
5. Проверить разрешение
6. Показать роли и разрешения
7. Показать группы
8. Добавить пользователя в группу
9. Исключить пользователя из группы
10. Статистика
11. Сортировка пользователей
12. Справка по функциям
0. Выход
"""


def choose_user(users: list[User]) -> User | None:
    """Запросить идентификатор пользователя."""
    user_id = input_int("ID пользователя: ")
    user = get_user(users, user_id)
    if user is None:
        print("Пользователь не найден.")
    return user


def choose_role(roles: list[Role]) -> Role | None:
    """Запросить роль по идентификатору."""
    role_id = input_int("ID роли: ")
    role = find_role_by_id(roles, role_id)
    if role is None:
        print("Роль не найдена.")
    return role


def handle_find_users(users: list[User]) -> None:
    """Найти и показать пользователей по подстроке имени."""
    query = input_nonempty("Подстрока имени: ")
    found = find_users(users, query)
    if not found:
        print("Никого не нашли.")
        return
    print(f"Найдено записей: {len(found)}")
    for user in found:
        print(f"[{user.id}] {user}")


def handle_add_user(
    users: list[User],
    roles: list[Role],
    groups: list[Group],
) -> None:
    """Добавить пользователя с проверкой ввода."""
    name = input_nonempty("ФИО: ")
    age = convert_age(str(input_int("Возраст: ")))
    if age == 0:
        print("Возраст некорректен, пользователь не добавлен.")
        return
    print("Доступные роли:")
    for item in roles:
        print(f"  [{item.id}] {item.name}")
    role = choose_role(roles)
    if role is None:
        return
    print("0 — без группы")
    show_groups(groups, users)
    group_id = input_int("ID группы: ")
    group = None
    if group_id != 0:
        group = find_group_by_id(groups, group_id)
        if group is None:
            print("Группа не найдена.")
            return
    user = add_user(users, name, age, role, group, date.today())
    print(f"Пользователь добавлен с ID {user.id}.")


def handle_assign_role(users: list[User], roles: list[Role]) -> None:
    """Назначить пользователю новую роль."""
    user = choose_user(users)
    if user is None:
        return
    print("Доступные роли:")
    for item in roles:
        print(f"  [{item.id}] {item.name}")
    role = choose_role(roles)
    if role is None:
        return
    user.assign_role(role)
    print(f"Пользователю {user.name} назначена роль {role.name}.")


def handle_check_permission(
    users: list[User],
    permissions: list[Permission],
) -> None:
    """Проверить, есть ли у пользователя разрешение на действие."""
    user = choose_user(users)
    if user is None:
        return
    print("Доступные коды разрешений:")
    for permission in permissions:
        print(f"  {permission.code} — {permission.title}")
    permission_code = input_nonempty("Код разрешения: ")
    role = user.role
    has_access = user.has_permission(permission_code)
    print(f"Роль: {role.name}")
    print(f"Уровень доступа роли: {role.access_description}")
    print(f"Запрошенное разрешение: {permission_code}")
    print(
        "Результат проверки (функция ПР1): "
        + (
            "доступ разрешён"
            if check_permission(role.name, permission_code)
            else "доступ запрещён"
        )
    )
    print(
        "Результат по объекту роли: "
        + ("доступ разрешён" if has_access else "доступ запрещён")
    )


def handle_add_to_group(
    users: list[User],
    groups: list[Group],
) -> None:
    """Включить пользователя в группу."""
    user = choose_user(users)
    if user is None:
        return
    show_groups(groups, users)
    group_id = input_int("ID группы: ")
    group = find_group_by_id(groups, group_id)
    if group is None:
        print("Группа не найдена.")
        return
    add_user_to_group(user, group)
    print(f"Пользователь {user.name} добавлен в группу {group.name}.")


def handle_remove_from_group(users: list[User]) -> None:
    """Исключить пользователя из группы."""
    user = choose_user(users)
    if user is None:
        return
    remove_user_from_group(user)
    print(f"Пользователь {user.name} исключён из группы.")


def handle_sort_users(users: list[User]) -> None:
    """Показать пользователей, отсортированных по имени или возрасту."""
    print("Поля сортировки: name, age")
    field = input_nonempty("Поле: ").casefold()
    if field not in {"name", "age"}:
        print("Можно сортировать только по name или age.")
        return
    print(f"\nПользователи по полю {field}:")
    for user in sort_users(users, field):
        print(user)


def show_statistics(
    users: list[User],
    roles: list[Role],
    groups: list[Group],
    permissions: list[Permission],
) -> None:
    """Показать сводку по пользователям, ролям и группам."""
    print("\nСтатистика:")
    print(f"Пользователей: {len(users)}")
    print(f"Ролей: {len(roles)}")
    print(f"Групп: {len(groups)}")
    print(f"Разрешений в справочнике: {len(permissions)}")
    print("Пользователи по ролям:")
    for role in roles:
        count = len(list(filter_users_by_role(users, role)))
        print(f"  {role.name}: {count}")
    used_permissions: set[str] = set()
    for role in roles:
        used_permissions |= role.permission_codes()
    print(
        "Используемые разрешения: "
        + (", ".join(sorted(used_permissions)) or "нет")
    )


def show_function_help() -> None:
    """Показать документацию ключевых функций через интроспекцию."""
    functions = (
        check_permission,
        format_user_card,
        convert_age,
        find_users,
        sort_users,
        find_role_by_name,
        User.has_permission,
        Role.check_permission,
        User.from_data,
    )
    print("\nСправка по функциям и методам проекта:")
    for func in functions:
        print("- " + describe_function(func))


@log_action
def persist(
    users: list[User],
    roles: list[Role],
    groups: list[Group],
) -> None:
    """Сохранить изменённые данные в JSON-файлы."""
    save_users(USERS_FILE, users)
    save_roles(ROLES_FILE, roles)
    save_groups(GROUPS_FILE, groups)


def pause() -> None:
    """Подождать Enter, чтобы результат не скрывался новым меню."""
    input("\nНажмите Enter, чтобы вернуться в меню...")


def main() -> None:
    """Точка запуска приложения: цикл меню и вызов функций проекта."""
    permissions = load_permissions(PERMISSIONS_FILE)
    roles = load_roles(ROLES_FILE, permissions)
    groups = load_groups(GROUPS_FILE)
    users = load_users(USERS_FILE, roles, groups)

    while True:
        print(MENU_TEXT)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_users(users)
        elif choice == "2":
            handle_find_users(users)
        elif choice == "3":
            handle_add_user(users, roles, groups)
            persist(users, roles, groups)
        elif choice == "4":
            handle_assign_role(users, roles)
            persist(users, roles, groups)
        elif choice == "5":
            handle_check_permission(users, permissions)
        elif choice == "6":
            show_roles(roles)
        elif choice == "7":
            show_groups(groups, users)
        elif choice == "8":
            handle_add_to_group(users, groups)
            persist(users, roles, groups)
        elif choice == "9":
            handle_remove_from_group(users)
            persist(users, roles, groups)
        elif choice == "10":
            show_statistics(users, roles, groups, permissions)
        elif choice == "11":
            handle_sort_users(users)
        elif choice == "12":
            show_function_help()
        elif choice == "0":
            persist(users, roles, groups)
            print("Данные сохранены. До свидания.")
            break
        else:
            print("Нет такого пункта меню. Повторите выбор.")
        if choice != "0":
            pause()


if __name__ == "__main__":
    main()
