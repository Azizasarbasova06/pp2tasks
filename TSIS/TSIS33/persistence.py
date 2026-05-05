import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")
LEADERBOARD_FILE = Path("leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "Normal"
}

def load_json(path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_settings():
    data = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
    for key, value in DEFAULT_SETTINGS.items():
        data.setdefault(key, value)
    return data

def save_settings(settings):
    save_json(SETTINGS_FILE, settings)

def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])
    if not isinstance(data, list):
        return []
    return data

def save_score(entry):
    leaderboard = load_leaderboard()
    leaderboard.append(entry)
    leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
    leaderboard = leaderboard[:10]
    save_json(LEADERBOARD_FILE, leaderboard)

def clear_leaderboard():
    save_json(LEADERBOARD_FILE, [])
