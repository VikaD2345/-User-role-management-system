"""Маршруты приложения ролей."""

from django.urls import path

from . import views

app_name = "roles"

urlpatterns = [
    path("", views.roles, name="list"),
    path("<int:role_id>/", views.role_detail, name="detail"),
]
