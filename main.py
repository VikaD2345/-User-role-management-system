"""Точка запуска системы управления пользовательскими ролями."""

from datetime import date
import os

from groups import add_user_to_group, get_group_members, remove_user_from_group
from roles import (
    check_permission,
    describe_role,
    find_role_by_name,
    get_permission_codes,
    role_allows_permission,
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
from users import (
    add_user,
    assign_role,
    convert_age,
    filter_users_by_role,
    find_users,
    format_user_card,
    get_user,
    sort_users,
)
from utils import (
    describe_function,
    input_int,
    input_nonempty,
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


def resolve_names(
    user: dict,
    roles: dict[int, dict],
    groups: dict[int, dict],
) -> tuple[str, str]:
    """Вернуть названия роли и группы пользователя."""
    role_id = user.get("role_id")
    group_id = user.get("group_id")
    role = roles.get(role_id, {}) if isinstance(role_id, int) else {}
    group = groups.get(group_id, {}) if isinstance(group_id, int) else {}
    role_name = role.get("name", "не назначена")
    group_name = group.get("name", "без группы")
    return role_name, group_name


def show_users(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
) -> None:
    """Вывести список пользователей в виде карточек."""
    if not users:
        print("Пользователи пока не добавлены.")
        return
    print("\nСписок пользователей:")
    for user in users.values():
        role_name, group_name = resolve_names(user, roles, groups)
        card = format_user_card(
            user["name"],
            role_name,
            group_name,
            user["age"],
        )
        print(
            f"[{user['id']}] {card} | "
            f"дата регистрации: {user['registration_date']}"
        )


def show_roles(
    roles: dict[int, dict],
    permissions: dict[int, dict],
) -> None:
    """Вывести роли и связанные с ними разрешения."""
    if not roles:
        print("Роли пока не добавлены.")
        return
    print("\nРоли и разрешения:")
    for role in roles.values():
        codes = get_permission_codes(roles, permissions, role["id"])
        codes_text = ", ".join(sorted(codes)) if codes else "нет"
        print(
            f"[{role['id']}] {role['name']} — {describe_role(role['name'])}"
        )
        print(f"    разрешения: {codes_text}")


def show_groups(
    groups: dict[int, dict],
    users: dict[int, dict],
) -> None:
    """Вывести группы и число участников."""
    if not groups:
        print("Группы пока не добавлены.")
        return
    print("\nГруппы:")
    for group in groups.values():
        members = get_group_members(users, group["id"])
        print(
            f"[{group['id']}] {group['name']} — "
            f"участников: {len(members)}"
        )
        for member in members:
            print(f"    - {member['name']}")


def show_statistics(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
    permissions: dict[int, dict],
) -> None:
    """Показать сводку по пользователям, ролям и группам."""
    print("\nСтатистика:")
    print(f"Пользователей: {len(users)}")
    print(f"Ролей: {len(roles)}")
    print(f"Групп: {len(groups)}")
    print(f"Разрешений в справочнике: {len(permissions)}")

    print("Пользователи по ролям:")
    for role in roles.values():
        count = len(list(filter_users_by_role(users, role["id"])))
        print(f"  {role['name']}: {count}")

    used_permissions = set()
    for role in roles.values():
        used_permissions |= get_permission_codes(
            roles,
            permissions,
            role["id"],
        )
    print(
        "Используемые разрешения: "
        + (", ".join(sorted(used_permissions)) or "нет")
    )


def choose_user(users: dict[int, dict]) -> dict | None:
    """Запросить идентификатор пользователя."""
    user_id = input_int("ID пользователя: ")
    user = get_user(users, user_id)
    if user is None:
        print("Пользователь не найден.")
    return user


def choose_role(roles: dict[int, dict]) -> dict | None:
    """Запросить роль по идентификатору."""
    role_id = input_int("ID роли: ")
    role = roles.get(role_id)
    if role is None:
        print("Роль не найдена.")
    return role


def handle_find_users(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
) -> None:
    """Найти и показать пользователей по подстроке имени."""
    query = input_nonempty("Подстрока имени: ")
    found = find_users(users, query)
    if not found:
        print("Никого не нашли.")
        return
    print(f"Найдено записей: {len(found)}")
    for user in found:
        role_name, group_name = resolve_names(user, roles, groups)
        print(
            f"[{user['id']}] "
            + format_user_card(
                user["name"],
                role_name,
                group_name,
                user["age"],
            )
        )


def handle_add_user(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
) -> None:
    """Добавить пользователя с проверкой ввода."""
    name = input_nonempty("ФИО: ")
    age = convert_age(str(input_int("Возраст: ")))
    if age == 0:
        print("Возраст некорректен, пользователь не добавлен.")
        return
    print("Доступные роли:")
    for item in roles.values():
        print(f"  [{item['id']}] {item['name']}")
    role = choose_role(roles)
    if role is None:
        return
    print("0 — без группы")
    show_groups(groups, users)
    group_id = input_int("ID группы: ")
    group_value = None if group_id == 0 else group_id
    if group_value is not None and group_value not in groups:
        print("Группа не найдена.")
        return
    user = add_user(
        users,
        name,
        age,
        role["id"],
        group_value,
        date.today(),
    )
    print(f"Пользователь добавлен с ID {user['id']}.")


def handle_assign_role(
    users: dict[int, dict],
    roles: dict[int, dict],
) -> None:
    """Назначить пользователю новую роль."""
    user = choose_user(users)
    if user is None:
        return
    print("Доступные роли:")
    for item in roles.values():
        print(f"  [{item['id']}] {item['name']}")
    role = choose_role(roles)
    if role is None:
        return
    assign_role(users, user["id"], role["id"])
    print(f"Пользователю {user['name']} назначена роль {role['name']}.")


def handle_check_permission(
    users: dict[int, dict],
    roles: dict[int, dict],
    permissions: dict[int, dict],
) -> None:
    """Проверить, есть ли у пользователя разрешение на действие."""
    user = choose_user(users)
    if user is None:
        return
    print("Доступные коды разрешений:")
    for permission in permissions.values():
        print(f"  {permission['code']} — {permission['title']}")
    permission_code = input_nonempty("Код разрешения: ")
    role_id = user.get("role_id")
    if not isinstance(role_id, int):
        print("Роль не назначена.")
        return
    role = roles.get(role_id, {})
    role_name = role.get("name", "")
    has_access = role_allows_permission(
        roles,
        permissions,
        role_id,
        permission_code,
    )
    print(f"Роль: {role_name}")
    print(f"Уровень доступа роли: {describe_role(role_name)}")
    print(f"Запрошенное разрешение: {permission_code}")
    print(
        "Результат проверки (функция ПР1): "
        + (
            "доступ разрешён"
            if check_permission(role_name, permission_code)
            else "доступ запрещён"
        )
    )
    print(
        "Результат по данным ролей: "
        + ("доступ разрешён" if has_access else "доступ запрещён")
    )


def handle_add_to_group(
    users: dict[int, dict],
    groups: dict[int, dict],
) -> None:
    """Включить пользователя в группу."""
    user = choose_user(users)
    if user is None:
        return
    show_groups(groups, users)
    group_id = input_int("ID группы: ")
    if group_id not in groups:
        print("Группа не найдена.")
        return
    add_user_to_group(users, user["id"], group_id)
    print(
        f"Пользователь {user['name']} добавлен в группу "
        f"{groups[group_id]['name']}."
    )


def handle_remove_from_group(users: dict[int, dict]) -> None:
    """Исключить пользователя из группы."""
    user = choose_user(users)
    if user is None:
        return
    if remove_user_from_group(users, user["id"]):
        print(f"Пользователь {user['name']} исключён из группы.")


def handle_sort_users(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
) -> None:
    """Показать пользователей, отсортированных по имени или возрасту."""
    print("Поля сортировки: name, age")
    field = input_nonempty("Поле: ").casefold()
    if field not in {"name", "age"}:
        print("Можно сортировать только по name или age.")
        return
    print(f"\nПользователи по полю {field}:")
    for user in sort_users(users, field):
        role_name, group_name = resolve_names(user, roles, groups)
        print(
            format_user_card(
                user["name"],
                role_name,
                group_name,
                user["age"],
            )
        )


def show_function_help() -> None:
    """Показать документацию ключевых функций через интроспекцию."""
    functions = (
        check_permission,
        describe_role,
        format_user_card,
        convert_age,
        find_users,
        sort_users,
        role_allows_permission,
        find_role_by_name,
    )
    print("\nСправка по функциям проекта:")
    for func in functions:
        print("- " + describe_function(func))


def persist(
    users: dict[int, dict],
    roles: dict[int, dict],
    groups: dict[int, dict],
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
    users = load_users(USERS_FILE)
    roles = load_roles(ROLES_FILE)
    permissions = load_permissions(PERMISSIONS_FILE)
    groups = load_groups(GROUPS_FILE)

    while True:
        print(MENU_TEXT)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_users(users, roles, groups)
        elif choice == "2":
            handle_find_users(users, roles, groups)
        elif choice == "3":
            handle_add_user(users, roles, groups)
            persist(users, roles, groups)
        elif choice == "4":
            handle_assign_role(users, roles)
            persist(users, roles, groups)
        elif choice == "5":
            handle_check_permission(users, roles, permissions)
        elif choice == "6":
            show_roles(roles, permissions)
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
            handle_sort_users(users, roles, groups)
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
