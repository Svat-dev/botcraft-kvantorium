import json
import os
from datetime import datetime
from typing import Dict, Optional
from modules.constants import EnumUserRoles
import uuid


def init_json(file_path: str = "data.json"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({"users": {}}, f)


def read_data(file_path: str = "data.json") -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


def write_data(data: dict, file_path: str = "data.json"):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def update_user(user_id: int, key: str, value, file_path: str = "data.json"):
    data = read_data(file_path)
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {}
    data["users"][str(user_id)][key] = value
    write_data(data, file_path)


def get_user_data(user_id: int, file_path: str = "data.json") -> Optional[Dict]:
    data = read_data(file_path)

    return data["users"].get(str(user_id))


def get_events_data(file_path: str = "data.json") -> dict:
    data = read_data(file_path)

    return data["events"]


def get_event(event_id: str) -> dict:
    events = get_events_data()

    return events.get(event_id)


def create_event(date: str, max: int, duration: str, desc: str, name: str):
    data = read_data()
    id = uuid.uuid4()

    data["events"][str(id)] = {
        "date": date,
        "participants_limit": max,
        "title": name,
        "desc": desc,
        "duration": duration,
    }

    write_data(data)


def create_user(
    user_id: int, password: str, _role: EnumUserRoles = EnumUserRoles.STUDENT
):
    data = read_data()

    data["users"] = {
        str(user_id): {
            "pwd": password,
            "role": str(_role),
            "events": [],
            "created_at": datetime(1900, 1, 1).now().date().isoformat(),
        }
    }

    write_data(data)


def remove_user(user_id: int) -> bool:
    data = read_data()

    if str(user_id) not in data["users"]:
        return False

    data["users"].pop(str(user_id))
    write_data(data)
