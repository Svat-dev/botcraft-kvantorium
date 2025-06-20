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


def get_users(file_path: str = "data.json") -> Optional[dict]:
    data = read_data(file_path)
    return data["users"]


def get_user_data(user_id: int, file_path: str = "data.json") -> Optional[Dict]:
    users = get_users(file_path)

    return users.get(str(user_id))


def get_user_by_name(first: str, last: str):
    users = get_users()
    user_id: str = ""
    
    for id, data in users.items():
        if data["first_name"].lower() == first.lower() and data["last_name"].lower() == last.lower():
            user_id = str(id)

    user = get_user_data(user_id)
    return {
        "user": user,
        "id": user_id
    }


def get_events_data(file_path: str = "data.json") -> dict:
    data = read_data(file_path)

    return data["events"]


def get_event(event_id: str) -> dict:
    events = get_events_data()

    return events.get(event_id)


def get_event_by_name(name: str) -> dict:
    events = get_events_data()
    event_id: str = ""
    
    for id, data in events.items():
        if data["title"] == name:
            event_id = id

    event = get_event(event_id)
    return {
        "event": event,
        "id": event_id
    }


def create_event(date: str, max: int, duration: str, desc: str, name: str):
    data = read_data()
    id = uuid.uuid4()

    data["events"][str(id)] = {
        "date": date,
        "participants_limit": max,
        "participants": {},
        "mentor_id": "",
        "title": name,
        "desc": desc,
        "duration": duration,
    }

    write_data(data)


def update_event(event_id: int, key: str, value, file_path: str = "data.json"):
    data = read_data(file_path)

    if event_id not in data["events"]:
        data["events"][event_id] = {}

    data["users"][event_id][key] = value
    write_data(data, file_path)


def create_user(
    user_id: int, name: str, _role: EnumUserRoles = EnumUserRoles.STUDENT
):
    data = read_data()
    first_name = name.split()[1]
    last_name = name.split()[0]

    data["users"] = {
        str(user_id): {
            "first_name": first_name,
            "last_name": last_name,
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
