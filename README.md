# Система управления пользовательскими ролями

Консольное приложение ПР3 дополнено веб-интерфейсом на Django 5.2 (ПР5).
Предметная область — ролевая модель доступа (RBAC): пользователи, роли,
разрешения и группы.

На этом этапе сущности **не переносятся в Django ORM**. View-функции
загружают объекты ПР3 из JSON и формируют HTML-страницы.

## Возможности

Веб-интерфейс (ПР5):
- просматривать роли в браузере;
- открывать карточку роли, разрешения и правило доступа ПР1;
- просматривать группы и состав группы;
- видеть связанного пользователя и его роль (`user.role.name`).

Консольная версия (ПР3, сохранена):
- добавлять пользователя и назначать роль;
- проверять разрешение;
- включать пользователя в группу;
- сортировать пользователей и смотреть статистику.

## Используемые технологии
- Python 3;
- Django 5.2 — веб-фреймворк;
- Django Template Language — шаблоны страниц;
- HTML — разметка страниц;
- CSS, Bootstrap 5.3 и собственный `style.css`;
- JavaScript — год в подвале страницы;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Целевая аудитория
Администраторы корпоративных информационных систем и руководители отделов.

## Предметная область
Основные объекты: пользователь, роль, разрешение, группа.

Пользователь имеет объект роли и может состоять в группе. Роль содержит
объекты разрешений. Проверка права — метод объекта, не поиск по словарю.

## Основные классы ПР3

### Entity
Базовый класс (`id`, `name`, `__str__`).
От него наследуют `User`, `Role`, `Group`, `Permission`.

### User
Атрибуты: `id`, `name`, `age`, `role`, `group`, `registration_date`.
Методы: `assign_role()`, `set_group()`, `has_permission()`, `from_data()`,
`__str__()`.

### Role
Атрибуты: `id`, `name`, `permissions`.
Методы: `has_permission()`, `check_permission()`, `access_description`,
`from_data()`, `__str__()`.

### Permission
Атрибуты: `id`, `code`, `title`. Методы: `from_data()`, `__str__()`.

### Group
Атрибуты: `id`, `name`. Методы: `from_data()`, `__str__()`.

## Страницы веб-интерфейса
Страницы собирает Django Template Language. Общий каркас —
`templates/base.html`. Дочерние шаблоны подключают его через
`{% extends %}`. Навигация вынесена в
`templates/includes/navigation.html`.

- `/` — главная (`homepage:index`, шаблон `homepage/index.html`);
- `/roles/` — список ролей (`roles:list`, цикл и карточка
  `roles/includes/role_card.html`);
- `/roles/<int:role_id>/` — карточка роли (`roles:detail`);
- `/groups/` — список групп (`groups:groups`);
- `/groups/<int:group_id>/` — карточка группы (`groups:detail`).

Если роль или группа не найдены, тот же шаблон карточки показывает
сообщение, а view возвращает HTTP 404. Ссылки строятся тегом
`{% url %}`, а не жёстким адресом.

Отдельное приложение пользователей не создаётся: Django уже даёт
`django.contrib.auth`. Модуль `models/users.py` остаётся в консоли.

## Основные операции

Используется в вебе (ПР6, шаблоны поверх страниц ПР5):
- список и карточка роли;
- проверка права на удаление пользователей (логика ПР1, флаг
  `can_delete` готовится во view);
- список и карточка группы;
- состав группы через объекты `User` и `Role` (`user.role.name`).

Отложено (есть в консоли, в вебе появятся с формами):
- добавление пользователя;
- назначение роли;
- включение в группу;
- поиск и сортировка.

## Хранение данных
JSON-файлы в `data/`:
- `users.json`, `roles.json`, `permissions.json`, `groups.json`.

В файлах хранятся `role_id`, `group_id`, `permission_ids`.
При загрузке `storage.py` восстанавливает объекты.

## Структура проекта
```text
role-management-system/
├── README.md
├── requirements.txt
├── manage.py
├── main.py
├── storage.py
├── utils.py
├── templates/
│   ├── base.html
│   └── includes/
│       └── navigation.html
├── rolely/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/
│   ├── urls.py
│   ├── views.py
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   └── templates/homepage/index.html
├── roles/
│   ├── urls.py
│   ├── views.py
│   └── templates/roles/
├── groups/
│   ├── urls.py
│   ├── views.py
│   └── templates/groups/
├── models/
│   ├── __init__.py
│   ├── entity.py
│   ├── users.py
│   ├── roles.py
│   ├── permissions.py
│   └── groups.py
├── data/
│   ├── users.json
│   ├── roles.json
│   ├── permissions.json
│   └── groups.json
└── tests/
    ├── test_users.py
    ├── test_roles.py
    ├── test_groups.py
    └── test_storage.py
```

## Назначение модулей

### `manage.py`
Запуск команд Django: `runserver`, `migrate`, `check`.

### `rolely/`
Настройки проекта: `settings.py`, корневой `urls.py`.

### `homepage/`
Главная страница через `render()`. Общий HTML больше не собирается
функцией `page()`: каркас лежит в `templates/base.html`. Свои CSS,
JavaScript и логотип — в `homepage/static/homepage/`.

### `roles/`
View-функции `roles()` и `role_detail()`. `models.py` пока пустой.

### `groups/`
View-функции `groups()` и `group_detail()`. `models.py` пока пустой.

### `models/`
Классы предметной области ПР3: `User`, `Role`, `Permission`, `Group`.

### `storage.py` и `utils.py`
Загрузка JSON и вспомогательный ввод.

### `main.py`
Консольная версия приложения (сохранена с ПР3).

### `tests/`
Автоматизированные тесты ПР3 и проверки страниц ПР6.

## Запуск приложения

Веб-версия:

```
python manage.py migrate
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/

Проверить, например:
- `/roles/1/` — администратор;
- `/roles/2/` — менеджер (удаление запрещено);
- `/roles/999/` — 404;
- `/groups/1/` — отдел продаж.

Консольная версия:

```
python main.py
```

## Тестирование

```
python -m pytest -v
```

## Проверка качества кода

```
python -m flake8 .
```

## Зависимости
- `Django==5.2.*`;
- `pytest`;
- `flake8`.

## Git
Исходный код хранится в Git.
Репозиторий: https://github.com/VikaD2345/-User-role-management-system

## Текущее состояние и план развития

Реализовано (ПР6):
- шаблоны Django вместо сборки HTML в Python;
- `base.html`, `{% extends %}`, `{% block %}`, `{% include %}`;
- контекст, `{% for %}`, `{% if %}`, `{% empty %}`;
- именованные URL и пространства имён `homepage`, `roles`, `groups`;
- фильтры `length` и `default`;
- свои CSS, логотип и JavaScript;
- данные ПР3 по-прежнему из JSON, без Django ORM;
- обработка 404;
- консоль и тесты ПР3 сохранены.

Планируется:
- формы создания и редактирования;
- база данных и Django ORM;
- API, Docker, CI/CD.
