"""Маршруты приложения ролей."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.roles, name="roles"),
    path("<int:role_id>/", views.role_detail, name="role_detail"),
]
