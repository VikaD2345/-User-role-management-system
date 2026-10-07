"""Автоматические тесты JSON и восстановления объектных связей."""

import json
import os

from models import Group, Permission, Role, User
from storage import (
    load_json,
    load_users,
    save_json,
    save_users,
)


def test_save_and_load_json(tmp_path) -> None:
    filename = os.path.join(tmp_path, "sample.json")
    payload = [{"id": 1, "name": "тест"}]
    save_json(filename, payload)
    loaded = load_json(filename, [])
    assert loaded == payload


def test_load_missing_file(tmp_path) -> None:
    filename = os.path.join(tmp_path, "no-such-file.json")
    assert load_json(filename, []) == []


def test_save_and_load_users(tmp_path) -> None:
    filename = os.path.join(tmp_path, "users.json")
    role = Role(2, "менеджер", [])
    group = Group(1, "Отдел продаж")
    users = [
        User(1, "Иванова А.С.", 27, role, group, "2026-09-01"),
    ]
    save_users(filename, users)
    loaded = load_users(filename, [role], [group])
    assert loaded[0].name == "Иванова А.С."
    assert loaded[0].role is role
    assert loaded[0].group is group
    with open(filename, "r", encoding="utf-8") as file:
        raw = json.load(file)
    assert isinstance(raw, list)
    assert raw[0]["role_id"] == 2
    assert raw[0]["group_id"] == 1


def test_permission_object_in_role() -> None:
    permission = Permission.from_data(
        {"id": 1, "code": "просмотр_данных", "title": "Просмотр"}
    )
    role = Role.from_data(
        {"id": 3, "name": "сотрудник", "permission_ids": [1]},
        [permission],
    )
    assert role.permissions[0] is permission
