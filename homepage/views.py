"""View-функции главной страницы и общий HTML-каркас."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с Bootstrap, CSS и навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP}">
    <style>
        nav.nav {{
            background: #f8f9fa;
            padding: 0.5rem 1rem;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/roles/">Роли</a>
        <a class="nav-link" href="/groups/">Группы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    content = """
    <h1 class="display-4">Система ролей</h1>
    <p class="lead">
        Управление пользователями, ролями и группами.
    </p>
    <p>Основные разделы:</p>
    <a href="/roles/" class="btn btn-primary me-2">Роли</a>
    <a href="/groups/" class="btn btn-secondary">Группы</a>
    """
    return HttpResponse(page("Система ролей", content))
