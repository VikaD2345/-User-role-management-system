"""View-функции списка и карточки группы."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.groups import find_group_by_id, get_group_members
from storage import (
    data_path,
    load_groups,
    load_permissions,
    load_roles,
    load_users,
)


def _load_groups_and_users() -> tuple:
    """Загрузить группы и пользователей средствами ПР3."""
    permissions = load_permissions(data_path("permissions.json"))
    roles_list = load_roles(data_path("roles.json"), permissions)
    groups_list = load_groups(data_path("groups.json"))
    users_list = load_users(
        data_path("users.json"),
        roles_list,
        groups_list,
    )
    return groups_list, users_list


def _mark_member_count(group, users) -> None:
    """Посчитать участников для шаблона статуса группы."""
    group.member_count = len(get_group_members(users, group))


def groups(request: HttpRequest) -> HttpResponse:
    """Страница списка групп."""
    groups_list, users = _load_groups_and_users()
    for group in groups_list:
        _mark_member_count(group, users)
    context = {"groups": groups_list}
    return render(request, "groups/group_list.html", context)


def group_detail(request: HttpRequest, group_id: int) -> HttpResponse:
    """Страница одной группы; 404, если группа не найдена."""
    groups_list, users = _load_groups_and_users()
    group = find_group_by_id(groups_list, group_id)
    members = []
    if group is not None:
        members = get_group_members(users, group)
        group.member_count = len(members)
    context = {"group": group, "members": members}
    return render(
        request,
        "groups/group_detail.html",
        context,
        status=404 if group is None else 200,
    )
