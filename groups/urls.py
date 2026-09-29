"""Маршруты приложения групп."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.groups, name="groups"),
    path("<int:group_id>/", views.group_detail, name="group_detail"),
]
