"""View-функции списка и карточки группы."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
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


def groups(request: HttpRequest) -> HttpResponse:
    """Страница списка групп."""
    groups, users = _load_groups_and_users()
    items = ""
    for group in groups:
        count = len(get_group_members(users, group))
        items += (
            f'<li class="list-group-item '
            f'd-flex justify-content-between">'
            f'<a href="/groups/{group.id}/">{group.name}</a>'
            f'<span class="badge bg-success">'
            f"участников: {count}</span>"
            f"</li>"
        )
    content = f"""
    <h1>Группы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Система ролей – группы", content))


def group_detail(request: HttpRequest, group_id: int) -> HttpResponse:
    """Страница одной группы; 404, если группа не найдена."""
    groups, users = _load_groups_and_users()
    group = find_group_by_id(groups, group_id)
    if group is None:
        content = """
        <h1 class="text-danger">Группа не найдена</h1>
        <a href="/groups/" class="btn btn-outline-secondary">
            ← к списку групп
        </a>
        """
        return HttpResponse(
            page("Группа не найдена", content),
            status=404,
        )
    members = get_group_members(users, group)
    members_html = ""
    for user in members:
        members_html += (
            f"<li>{user.name} — роль: {user.role.name}</li>"
        )
    if not members_html:
        members_html = "<li>в группе пока нет участников</li>"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{group.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {group.id}
            </p>
            <p class="card-text">
                <strong>Участников:</strong> {len(members)}
            </p>
            <p class="card-text"><strong>Состав:</strong></p>
            <ul>{members_html}</ul>
            <a href="/groups/" class="btn btn-outline-secondary">
                ← к списку групп
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(group.name, content), status=200)
