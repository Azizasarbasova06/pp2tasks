import json
from pathlib import Path


SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [40, 220, 90],
    "grid_overlay": True,
    "sound": True,
}

COLOR_OPTIONS = {
    "Green": [40, 220, 90],
    "Blue": [60, 150, 255],
    "Yellow": [240, 210, 60],
    "Purple": [170, 80, 230],
    "White": [245, 245, 245],
}


def load_settings():
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    color = settings.get("snake_color")
    if (
        not isinstance(color, list)
        or len(color) != 3
        or not all(isinstance(value, int) and 0 <= value <= 255 for value in color)
    ):
        settings["snake_color"] = DEFAULT_SETTINGS["snake_color"]

    settings["grid_overlay"] = bool(settings.get("grid_overlay", True))
    settings["sound"] = bool(settings.get("sound", True))

    return settings


def save_settings(settings):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding="utf-8")
