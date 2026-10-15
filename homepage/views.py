"""View-функции главной страницы."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    return render(request, "homepage/index.html")
