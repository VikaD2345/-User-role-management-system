"""View-функции списка и карточки роли."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.roles import find_role_by_id
from models.users import filter_users_by_role
from storage import (
    data_path,
    load_groups,
    load_permissions,
    load_roles,
    load_users,
)


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


def roles(request: HttpRequest) -> HttpResponse:
    """Страница списка ролей."""
    roles_list, _users = _load_roles_and_users()
    items = ""
    for role in roles_list:
        items += (
            f'<li class="list-group-item">'
            f'<a href="/roles/{role.id}/">{role.name}</a>'
            f" — {role.access_description}"
            f"</li>"
        )
    content = f"""
    <h1>Роли</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Система ролей – роли", content))


def role_detail(request: HttpRequest, role_id: int) -> HttpResponse:
    """Страница одной роли; 404, если роль не найдена."""
    roles_list, users_list = _load_roles_and_users()
    role = find_role_by_id(roles_list, role_id)
    if role is None:
        content = """
        <h1 class="text-danger">Роль не найдена</h1>
        <a href="/roles/" class="btn btn-outline-secondary">
            ← к списку ролей
        </a>
        """
        return HttpResponse(
            page("Роль не найдена", content),
            status=404,
        )
    can_delete = role.has_permission("удаление_пользователей")
    status = (
        "может удалять пользователей"
        if can_delete
        else "удаление пользователей запрещено"
    )
    badge = "bg-success" if can_delete else "bg-danger"
    codes = sorted(role.permission_codes())
    codes_text = ", ".join(codes) if codes else "нет"
    members = list(filter_users_by_role(users_list, role))
    members_html = ""
    for user in members:
        members_html += f"<li>{user.name}</li>"
    if not members_html:
        members_html = "<li>нет пользователей с этой ролью</li>"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{role.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {role.id}
            </p>
            <p class="card-text">
                <strong>Уровень доступа:</strong>
                {role.access_description}
            </p>
            <p class="card-text">
                <strong>Разрешения:</strong> {codes_text}
            </p>
            <p class="card-text">
                Правило ПР1:
                <span class="badge {badge}">{status}</span>
            </p>
            <p class="card-text"><strong>Пользователи:</strong></p>
            <ul>{members_html}</ul>
            <a href="/roles/" class="btn btn-outline-secondary">
                ← к списку ролей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(role.name, content), status=200)
