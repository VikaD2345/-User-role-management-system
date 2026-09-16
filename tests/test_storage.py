"""Автоматические тесты загрузки JSON через контекстный менеджер."""

import json
import os

from storage import load_json, load_users, save_json, save_users


def test_save_and_load_json(tmp_path):
    filename = os.path.join(tmp_path, "sample.json")
    payload = [{"id": 1, "name": "тест"}]
    save_json(filename, payload)
    loaded = load_json(filename, [])
    assert loaded == payload


def test_load_missing_file(tmp_path):
    filename = os.path.join(tmp_path, "no-such-file.json")
    assert load_json(filename, []) == []


def test_save_and_load_users(tmp_path):
    filename = os.path.join(tmp_path, "users.json")
    users = {
        1: {
            "id": 1,
            "name": "Иванова А.С.",
            "age": 27,
            "role_id": 2,
            "group_id": 1,
            "registration_date": "2026-09-01",
        }
    }
    save_users(filename, users)
    loaded = load_users(filename)
    assert loaded[1]["name"] == "Иванова А.С."
    with open(filename, "r", encoding="utf-8") as file:
        raw = json.load(file)
    assert isinstance(raw, list)
