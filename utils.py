import json
import os
from config import USERS_FILE


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)
