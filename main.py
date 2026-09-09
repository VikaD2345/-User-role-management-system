from datetime import date

# --- Данные пользователя ---
username = "Иванова А.С."
user_role = "менеджер"          # варианты: администратор, менеджер, сотрудник, гость
group_name = "Отдел продаж"
registration_date = date(2026, 9, 1)

# Преобразование типов: возраст пришёл строкой (например, из формы ввода)
age_input = "27"
user_age = int(age_input)

# Запрошенное действие, доступ к которому нужно проверить
requested_permission = "удаление_пользователей"


def check_permission(role, permission):
    """Проверяет, разрешено ли роли выполнять указанное действие."""
    if role == "администратор":
        return True
    elif role == "менеджер" and permission != "удаление_пользователей":
        return True
    elif role == "сотрудник" and permission == "просмотр_данных":
        return True
    else:
        return False


has_access = check_permission(user_role, requested_permission)

print(f"Пользователь: {username}")
print(f"Роль: {user_role}")
print(f"Группа: {group_name}")
print(f"Возраст: {user_age} лет")
print(f"Дата регистрации: {registration_date}")
print(f"Запрошенное разрешение: {requested_permission}")

if has_access:
    print("Результат проверки: доступ разрешён")
else:
    print("Результат проверки: доступ запрещён")
