import json, os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "blue",       # blue | red | green
    "difficulty": "normal",     # easy | normal | hard
}

def load_settings():
    if not os.path.isfile(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.isfile(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

def save_score(name: str, score: int, distance: int):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)
    return board