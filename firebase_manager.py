import requests

FIREBASE_URL = "https://die-again-game-default-rtdb.firebaseio.com"


# ===== REGISTER =====
def register_user(username, password):
    users = requests.get(f"{FIREBASE_URL}/users.json").json()

    if users and username in users:
        return False

    data = {
        "password": password,
        "level": 0,
        "deaths": 0
    }

    requests.put(f"{FIREBASE_URL}/users/{username}.json", json=data)
    return True


# ===== LOGIN =====
def login_user(username, password):
    user = requests.get(f"{FIREBASE_URL}/users/{username}.json").json()

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


# ===== SAVE PROGRESS =====
def save_progress(username, level, deaths):
    data = {
        "level": level,
        "deaths": deaths
    }

    requests.patch(f"{FIREBASE_URL}/users/{username}.json", json=data)


# ===== GET LEADERBOARD =====
def get_leaderboard():
    users = requests.get(f"{FIREBASE_URL}/users.json").json()

    if not users:
        return []

    players = []

    for name, data in users.items():
        players.append({
            "name": name,
            "level": data["level"],
            "deaths": data["deaths"]
        })

    # ⭐ SORT LOGIC
    players.sort(
        key=lambda x: (-x["level"], x["deaths"])
    )

    return players[:5]