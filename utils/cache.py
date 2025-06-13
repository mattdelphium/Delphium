import os
import json
import pickle
from config.settings import CACHE_DIR, SUMMARY_CACHE_DIR

def get_game_cache_path(username, game_hash):
    path = os.path.join(CACHE_DIR, username)
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"{game_hash}.pkl")

def get_summary_cache_path(username, game_hash):
    path = os.path.join(SUMMARY_CACHE_DIR, username)
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"{game_hash}.json")

def load_cached_game(username, game_hash):
    path = get_game_cache_path(username, game_hash)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_cached_game(username, game_hash, data):
    path = get_game_cache_path(username, game_hash)
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_cached_summary(username, game_hash):
    path = get_summary_cache_path(username, game_hash)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_cached_summary(username, game_hash, summary):
    path = get_summary_cache_path(username, game_hash)
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
