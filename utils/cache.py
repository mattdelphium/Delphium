import os
import json
import pickle
from config.settings import CACHE_DIR, SUMMARY_CACHE_DIR

def get_cache_path(game_hash, ext):
    folder = CACHE_DIR if ext == "pkl" else SUMMARY_CACHE_DIR
    return os.path.join(folder, f"{game_hash}.{ext}")

def load_cached_game(game_hash):
    path = get_cache_path(game_hash, "pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_cached_game(game_hash, data):
    path = get_cache_path(game_hash, "pkl")
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_cached_summary(game_hash):
    path = get_cache_path(game_hash, "json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_cached_summary(game_hash, summary):
    path = get_cache_path(game_hash, "json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)