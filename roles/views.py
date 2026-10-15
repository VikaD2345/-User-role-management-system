"""View-функции списка и карточки роли."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.roles import find_role_by_id
from models.users import filter_users_by_role
from storage import (
    data_path,
    load_groups,
    load_permissions,
    load_roles,
    load_users,
)

DELETE_USERS = "удаление_пользователей"


def _load_roles_and_users() -> tuple:
    """Загрузить роли и пользователей средствами ПР3."""
    permissions = load_permissions(data_path("permissions.json"))
    roles_list = load_roles(data_path("roles.json"), permissions)
    groups_list = load_groups(data_path("groups.json"))
    users_list = load_users(
        data_path("users.json"),
        roles_list,
        groups_list,
    )
    return roles_list, users_list


def _mark_delete_access(role) -> None:
    """Подготовить флаг отображения: шаблон не вызывает метод с аргументом."""
    role.can_delete = role.has_permission(DELETE_USERS)


def roles(request: HttpRequest) -> HttpResponse:
    """Страница списка ролей."""
    roles_list, _users = _load_roles_and_users()
    for role in roles_list:
        _mark_delete_access(role)
    context = {"roles": roles_list}
    return render(request, "roles/role_list.html", context)


def role_detail(request: HttpRequest, role_id: int) -> HttpResponse:
    """Страница одной роли; 404, если роль не найдена."""
    roles_list, users_list = _load_roles_and_users()
    role = find_role_by_id(roles_list, role_id)
    members = []
    if role is not None:
        _mark_delete_access(role)
        members = list(filter_users_by_role(users_list, role))
    context = {"role": role, "members": members}
    return render(
        request,
        "roles/role_detail.html",
        context,
        status=404 if role is None else 200,
    )
