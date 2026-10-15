"""Проверка страниц Django: шаблоны, контекст и коды ответа."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rolely.settings")
django.setup()

from django.template.loader import render_to_string  # noqa: E402
from django.test import Client  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

setup_test_environment()


def client() -> Client:
    """Клиент с хостом из ALLOWED_HOSTS."""
    return Client(HTTP_HOST="127.0.0.1")


def test_home_uses_base_template() -> None:
    """Главная наследует базовый шаблон и подключает статику."""
    response = client().get("/")
    names = [item.name for item in response.templates]
    body = response.content.decode()
    assert response.status_code == 200
    assert "homepage/index.html" in names
    assert "base.html" in names
    assert "includes/navigation.html" in names
    assert "Система ролей" in body
    assert 'href="/roles/"' in body
    assert 'href="/groups/"' in body
    assert "/static/homepage/css/style.css" in body
    assert "/static/homepage/js/main.js" in body
    assert "/static/homepage/img/logo.png" in body
    assert 'id="current-year"' in body


def test_role_list_renders_objects() -> None:
    """Список ролей выводит объекты Role через include и фильтр length."""
    response = client().get("/roles/")
    names = [item.name for item in response.templates]
    body = response.content.decode()
    assert response.status_code == 200
    assert "roles/role_list.html" in names
    assert "roles/includes/role_card.html" in names
    assert "Всего ролей: 3" in body
    assert "администратор" in body
    assert "может удалять пользователей" in body
    assert "удаление пользователей запрещено" in body


def test_admin_role_can_delete_users() -> None:
    """Карточка администратора показывает разрешение на удаление."""
    response = client().get("/roles/1/")
    body = response.content.decode()
    assert response.status_code == 200
    assert "может удалять пользователей" in body
    assert "Соколова М.В." in body
    assert "удаление_пользователей" in body
    assert "20.08.2026" in body


def test_manager_role_cannot_delete_users() -> None:
    """Карточка менеджера запрещает удаление пользователей."""
    response = client().get("/roles/2/")
    body = response.content.decode()
    assert response.status_code == 200
    assert "удаление пользователей запрещено" in body
    assert "Иванова А.С." in body


def test_missing_role_returns_404() -> None:
    """Несуществующая роль открывает ветку шаблона со статусом 404."""
    response = client().get("/roles/999/")
    names = [item.name for item in response.templates]
    assert response.status_code == 404
    assert "roles/role_detail.html" in names
    assert "Роль не найдена" in response.content.decode()


def test_group_page_shows_member_role() -> None:
    """Карточка группы показывает user.role.name и общий статус."""
    response = client().get("/groups/1/")
    names = [item.name for item in response.templates]
    body = response.content.decode()
    assert response.status_code == 200
    assert "groups/group_detail.html" in names
    assert "groups/includes/group_status.html" in names
    assert "Отдел продаж" in body
    assert "Иванова А.С." in body
    assert "роль: менеджер" in body
    assert "Петров И.К." in body
    assert "роль: сотрудник" in body


def test_missing_group_returns_404() -> None:
    """Несуществующая группа возвращает 404."""
    response = client().get("/groups/999/")
    assert response.status_code == 404
    assert "Группа не найдена" in response.content.decode()


def test_empty_role_list_uses_empty_block() -> None:
    """Пустая коллекция показывает текст из {% empty %}."""
    html = render_to_string("roles/role_list.html", {"roles": []})
    assert "Роли не найдены." in html
    assert "Всего ролей: 0" in html
