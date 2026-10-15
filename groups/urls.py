"""Маршруты приложения групп."""

from django.urls import path

from . import views

app_name = "groups"

urlpatterns = [
    path("", views.groups, name="groups"),
    path("<int:group_id>/", views.group_detail, name="detail"),
]
