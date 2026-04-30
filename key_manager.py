import json
import os

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "key.json")


def ensure_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": ""}, f)


def load_api_key():
    ensure_config()

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("api_key", "")
    except:
        return ""


def save_api_key(key):
    ensure_config()

    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)