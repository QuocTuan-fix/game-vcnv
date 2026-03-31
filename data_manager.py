import json
import os

DATA_PATH = "data/player_data.json"


def load_data():
    if not os.path.exists(DATA_PATH):
        return {"players": []}

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def save_player_score(name, score):
    data = load_data()

    data["players"].append({
        "name": name,
        "score": score
    })

    save_data(data)


def get_top_players(limit=5):
    data = load_data()

    players = sorted(
        data["players"],
        key=lambda x: x["score"],
        reverse=True
    )

    return players[:limit]